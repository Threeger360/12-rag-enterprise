"""test_rag_enterprise.py - Testes do RAG Enterprise."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestModules:
    def test_config(self):
        from src.config import settings
        assert settings is not None
    
    def test_models(self):
        from src.models import QueryRequest, QueryResponse
        req = QueryRequest(question="teste")
        assert req.question == "teste"
    
    def test_pipeline_import(self):
        from src.rag.pipeline import RAGPipeline
        assert RAGPipeline is not None
    
    def test_orchestrator_import(self):
        from src.agents.orchestrator import Orchestrator
        assert Orchestrator is not None
    
    def test_metrics_import(self):
        from src.observability.metrics import MetricsCollector
        assert MetricsCollector is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
