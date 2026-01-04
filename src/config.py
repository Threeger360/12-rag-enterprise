"""
config.py
Configurações do RAG Enterprise.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configurações do sistema."""
    
    # API Keys
    openai_api_key: str = Field(default="")
    
    # Modelos
    default_model: str = Field(default="gpt-4o-mini")
    embedding_model: str = Field(default="text-embedding-3-small")
    
    # RAG
    retriever_k: int = Field(default=10)
    rerank_k: int = Field(default=5)
    hybrid_semantic_weight: float = Field(default=0.5)
    hybrid_bm25_weight: float = Field(default=0.5)
    
    # Self-Evaluation
    support_threshold: str = Field(default="partially")
    utility_threshold: int = Field(default=3)
    max_refinements: int = Field(default=2)
    
    # API
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    api_key: str = Field(default="")
    rate_limit: int = Field(default=100)
    
    # Vector Store
    chroma_dir: str = Field(default="./data/chroma")
    collection_name: str = Field(default="rag_enterprise")
    
    # Observability
    log_level: str = Field(default="INFO")
    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9090)
    
    # Environment
    environment: str = Field(default="development")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
