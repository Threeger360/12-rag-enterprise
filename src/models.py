"""
models.py
Schemas Pydantic para o RAG Enterprise.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Document(BaseModel):
    """Documento indexado."""
    id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None


class SearchResult(BaseModel):
    """Resultado de busca."""
    content: str
    score: float
    source: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QueryRequest(BaseModel):
    """Request para query."""
    question: str
    strategy: str = "auto"
    k: int = 5
    stream: bool = False


class QueryResponse(BaseModel):
    """Response de query."""
    answer: str
    confidence: float = 0.0
    sources: List[str] = Field(default_factory=list)
    latency_ms: float = 0.0
    tokens_used: int = 0
    strategy_used: str = ""
    was_refined: bool = False


class EvaluationResult(BaseModel):
    """Resultado de avaliação."""
    support_level: str = ""
    utility_score: int = 0
    unsupported_claims: List[str] = Field(default_factory=list)
    needs_refinement: bool = False


class AgentState(BaseModel):
    """Estado dos agentes."""
    query: str
    context: List[SearchResult] = Field(default_factory=list)
    answer: str = ""
    evaluation: Optional[EvaluationResult] = None
    current_agent: str = ""
    iteration: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class Metrics(BaseModel):
    """Métricas do sistema."""
    total_queries: int = 0
    avg_latency_ms: float = 0.0
    total_tokens: int = 0
    error_rate: float = 0.0
    support_distribution: Dict[str, int] = Field(default_factory=dict)
    avg_utility: float = 0.0
