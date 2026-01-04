"""
main.py
API FastAPI do RAG Enterprise.
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import logging

from src.config import settings
from src.models import QueryRequest, QueryResponse
from src.rag.pipeline import RAGPipeline

logger = logging.getLogger(__name__)

# App
app = FastAPI(
    title="RAG Enterprise API",
    description="Sistema RAG completo para produção",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pipeline global
rag_pipeline: Optional[RAGPipeline] = None


def get_pipeline() -> RAGPipeline:
    """Retorna pipeline RAG."""
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline


async def verify_api_key(x_api_key: str = Header(None)):
    """Verifica API key."""
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    pipeline: RAGPipeline = Depends(get_pipeline),
    api_key: str = Depends(verify_api_key)
):
    """Processa uma pergunta."""
    try:
        result = pipeline.process(request.question, request.k)
        return result
    except Exception as e:
        logger.error(f"Erro ao processar query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents")
async def add_documents(
    documents: List[str],
    pipeline: RAGPipeline = Depends(get_pipeline),
    api_key: str = Depends(verify_api_key)
):
    """Adiciona documentos."""
    try:
        pipeline.add_documents(documents)
        return {"status": "ok", "count": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def stats(
    pipeline: RAGPipeline = Depends(get_pipeline),
    api_key: str = Depends(verify_api_key)
):
    """Retorna estatísticas."""
    return pipeline.get_stats()


@app.get("/metrics")
async def metrics():
    """Métricas Prometheus."""
    from prometheus_client import generate_latest
    return generate_latest()


def start_api():
    """Inicia API."""
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development"
    )


if __name__ == "__main__":
    start_api()
