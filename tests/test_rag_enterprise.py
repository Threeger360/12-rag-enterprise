"""test_rag_enterprise.py - Testes do RAG Enterprise."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConfig:
    def test_settings(self):
        from src.config import settings
        assert settings is not None
        assert hasattr(settings, "default_model")
        assert hasattr(settings, "retriever_k")


class TestModels:
    def test_query_response(self):
        from src.models import QueryResponse
        r = QueryResponse(answer="teste", confidence=0.9)
        assert r.answer == "teste"
    
    def test_search_result(self):
        from src.models import SearchResult
        r = SearchResult(content="doc", score=0.8)
        assert r.score == 0.8


class TestRAGPipeline:
    def test_create(self):
        from src.rag.pipeline import RAGPipeline
        pipeline = RAGPipeline()
        assert pipeline is not None
    
    def test_tokenize(self):
        from src.rag.pipeline import RAGPipeline
        pipeline = RAGPipeline()
        tokens = pipeline._tokenize("Hello World!")
        assert "hello" in tokens
        assert "world" in tokens


class TestOrchestrator:
    def test_create(self):
        from src.agents.orchestrator import Orchestrator
        orch = Orchestrator()
        assert orch is not None


class TestMetrics:
    def test_collector(self):
        from src.observability.metrics import MetricsCollector
        m = MetricsCollector()
        assert m is not None


class TestAPI:
    def test_app_exists(self):
        from src.api.main import app
        assert app is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
