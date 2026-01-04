"""
pipeline.py
Pipeline RAG Enterprise completo.
"""

import time
import logging
from typing import List, Optional

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LCDocument
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rank_bm25 import BM25Okapi
import re

from src.config import settings
from src.models import QueryResponse, SearchResult, EvaluationResult

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Pipeline RAG Enterprise com todas as funcionalidades."""
    
    def __init__(self):
        # Embeddings e LLM
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key
        )
        self.llm = ChatOpenAI(
            model=settings.default_model,
            temperature=0.1,
            api_key=settings.openai_api_key
        )
        
        # Text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Stores
        self.vector_store = None
        self.documents: List[str] = []
        self.bm25 = None
        
        # Prompts
        self._init_prompts()
        
        # Métricas
        self.total_queries = 0
        self.total_tokens = 0
    
    def _init_prompts(self):
        """Inicializa prompts."""
        self.generate_prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um assistente especializado.
Responda baseando-se APENAS no contexto fornecido.
Se não souber, diga que não encontrou a informação.

Contexto:
{context}"""),
            ("user", "{question}")
        ])
        
        self.evaluate_prompt = ChatPromptTemplate.from_template("""
Avalie esta resposta.

Contexto: {context}
Resposta: {answer}

JSON (sem markdown):
{{"support": "fully/partially/no", "utility": 1-5, "issues": []}}
""")
    
    def add_documents(self, documents: List[str]):
        """Adiciona documentos ao índice."""
        self.documents = documents
        
        # Cria chunks
        all_docs = []
        for i, doc in enumerate(documents):
            chunks = self.splitter.split_text(doc)
            for chunk in chunks:
                all_docs.append(LCDocument(
                    page_content=chunk,
                    metadata={"source": f"doc_{i}"}
                ))
        
        # Vector store
        self.vector_store = Chroma.from_documents(
            all_docs,
            self.embeddings,
            collection_name=settings.collection_name,
            persist_directory=settings.chroma_dir
        )
        
        # BM25
        self.tokenized = [self._tokenize(d) for d in documents]
        self.bm25 = BM25Okapi(self.tokenized)
        
        logger.info(f"Indexados {len(documents)} docs, {len(all_docs)} chunks")
    
    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'[\w-]+', text.lower())
    
    def hybrid_search(self, query: str, k: int = None) -> List[SearchResult]:
        """Busca híbrida: semântico + BM25."""
        k = k or settings.retriever_k
        
        # Semântico
        if self.vector_store:
            sem_results = self.vector_store.similarity_search_with_score(query, k=k)
            semantic = [
                SearchResult(content=doc.page_content, score=1-score, source=doc.metadata.get("source", ""))
                for doc, score in sem_results
            ]
        else:
            semantic = []
        
        # BM25
        if self.bm25:
            tokens = self._tokenize(query)
            scores = self.bm25.get_scores(tokens)
            ranked = sorted(enumerate(scores), key=lambda x: -x[1])[:k]
            bm25_results = [
                SearchResult(content=self.documents[i], score=s, source=f"doc_{i}")
                for i, s in ranked if s > 0
            ]
        else:
            bm25_results = []
        
        # RRF Fusion
        return self._rrf_fusion([semantic, bm25_results], k)
    
    def _rrf_fusion(self, rankings: List[List[SearchResult]], k: int) -> List[SearchResult]:
        """Reciprocal Rank Fusion."""
        scores = {}
        docs = {}
        rrf_k = 60
        
        for ranking in rankings:
            for rank, result in enumerate(ranking):
                key = result.content[:100]
                if key not in scores:
                    scores[key] = 0
                    docs[key] = result
                scores[key] += 1 / (rrf_k + rank + 1)
        
        ranked = sorted(scores.items(), key=lambda x: -x[1])[:k]
        return [docs[key] for key, _ in ranked]
    
    def generate(self, query: str, context: List[SearchResult]) -> str:
        """Gera resposta."""
        context_str = "\n\n---\n\n".join([r.content for r in context])
        
        chain = self.generate_prompt | self.llm | StrOutputParser()
        return chain.invoke({"question": query, "context": context_str})
    
    def evaluate(self, answer: str, context: List[SearchResult]) -> EvaluationResult:
        """Avalia resposta."""
        import json
        context_str = "\n".join([r.content[:200] for r in context[:3]])
        
        try:
            chain = self.evaluate_prompt | self.llm | StrOutputParser()
            result = chain.invoke({"context": context_str, "answer": answer})
            data = json.loads(result.replace("```json", "").replace("```", ""))
            
            return EvaluationResult(
                support_level=data.get("support", "partially"),
                utility_score=data.get("utility", 3),
                unsupported_claims=data.get("issues", []),
                needs_refinement=data.get("support") == "no" or data.get("utility", 3) < settings.utility_threshold
            )
        except Exception as e:
            logger.error(f"Erro na avaliação: {e}")
            return EvaluationResult(support_level="partially", utility_score=3)
    
    def process(self, question: str, k: int = None) -> QueryResponse:
        """Processa uma pergunta."""
        start = time.time()
        self.total_queries += 1
        
        # 1. Busca híbrida
        results = self.hybrid_search(question, k or settings.rerank_k)
        
        # 2. Gera resposta
        answer = self.generate(question, results)
        
        # 3. Avalia
        evaluation = self.evaluate(answer, results)
        
        # 4. Refina se necessário
        was_refined = False
        if evaluation.needs_refinement and settings.max_refinements > 0:
            # Simplified refinement
            answer = self.generate(question, results)
            was_refined = True
        
        latency = (time.time() - start) * 1000
        
        return QueryResponse(
            answer=answer,
            confidence=evaluation.utility_score / 5,
            sources=[r.source for r in results[:3]],
            latency_ms=latency,
            strategy_used="hybrid",
            was_refined=was_refined
        )
    
    def get_stats(self) -> dict:
        """Retorna estatísticas."""
        return {
            "total_queries": self.total_queries,
            "documents_indexed": len(self.documents),
            "vector_store_ready": self.vector_store is not None
        }
