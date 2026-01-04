"""
orchestrator.py
Orquestrador de agentes do RAG Enterprise.
"""

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END, START
import logging

from src.config import settings
from src.models import SearchResult, QueryResponse
from src.rag.pipeline import RAGPipeline

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """Estado compartilhado entre agentes."""
    query: str
    strategy: str
    context: List[dict]
    answer: str
    confidence: float
    needs_refinement: bool
    iteration: int
    final_answer: str


class Orchestrator:
    """Orquestra os agentes do sistema."""
    
    def __init__(self):
        self.pipeline = RAGPipeline()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Constrói grafo de agentes."""
        workflow = StateGraph(AgentState)
        
        # Nós (agentes)
        workflow.add_node("classifier", self._classify)
        workflow.add_node("retriever", self._retrieve)
        workflow.add_node("generator", self._generate)
        workflow.add_node("validator", self._validate)
        workflow.add_node("refiner", self._refine)
        workflow.add_node("output", self._output)
        
        # Fluxo
        workflow.add_edge(START, "classifier")
        workflow.add_edge("classifier", "retriever")
        workflow.add_edge("retriever", "generator")
        workflow.add_edge("generator", "validator")
        
        workflow.add_conditional_edges(
            "validator",
            lambda s: "refiner" if s["needs_refinement"] and s["iteration"] < 2 else "output",
            {"refiner": "refiner", "output": "output"}
        )
        
        workflow.add_edge("refiner", "generator")
        workflow.add_edge("output", END)
        
        return workflow.compile()
    
    def _classify(self, state: AgentState) -> dict:
        """Classifica a query."""
        # Simplificado - sempre usa hybrid
        return {"strategy": "hybrid"}
    
    def _retrieve(self, state: AgentState) -> dict:
        """Busca documentos."""
        results = self.pipeline.hybrid_search(state["query"])
        context = [{"content": r.content, "score": r.score} for r in results]
        return {"context": context}
    
    def _generate(self, state: AgentState) -> dict:
        """Gera resposta."""
        results = [SearchResult(**c) for c in state["context"]]
        answer = self.pipeline.generate(state["query"], results)
        return {"answer": answer, "iteration": state.get("iteration", 0) + 1}
    
    def _validate(self, state: AgentState) -> dict:
        """Valida resposta."""
        results = [SearchResult(**c) for c in state["context"]]
        evaluation = self.pipeline.evaluate(state["answer"], results)
        return {
            "confidence": evaluation.utility_score / 5,
            "needs_refinement": evaluation.needs_refinement
        }
    
    def _refine(self, state: AgentState) -> dict:
        """Prepara para refinamento."""
        return {}
    
    def _output(self, state: AgentState) -> dict:
        """Prepara output final."""
        return {"final_answer": state["answer"]}
    
    def add_documents(self, documents: List[str]):
        """Adiciona documentos."""
        self.pipeline.add_documents(documents)
    
    def process(self, question: str) -> QueryResponse:
        """Processa pergunta."""
        initial: AgentState = {
            "query": question,
            "strategy": "",
            "context": [],
            "answer": "",
            "confidence": 0.0,
            "needs_refinement": False,
            "iteration": 0,
            "final_answer": ""
        }
        
        result = self.graph.invoke(initial)
        
        return QueryResponse(
            answer=result["final_answer"],
            confidence=result["confidence"],
            strategy_used=result["strategy"],
            was_refined=result["iteration"] > 1
        )
