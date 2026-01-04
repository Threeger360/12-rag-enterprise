"""
metrics.py
Métricas Prometheus para RAG Enterprise.
"""

from prometheus_client import Counter, Histogram, Gauge
import time
from contextlib import contextmanager


class MetricsCollector:
    """Coletor de métricas."""
    
    def __init__(self):
        # Latência
        self.latency = Histogram(
            'rag_latency_seconds',
            'Latência por etapa',
            ['stage']
        )
        
        # Tokens
        self.tokens = Counter(
            'rag_tokens_total',
            'Total de tokens usados',
            ['type']
        )
        
        # Queries
        self.queries = Counter(
            'rag_queries_total',
            'Total de queries',
            ['status']
        )
        
        # Qualidade
        self.quality = Gauge(
            'rag_quality_score',
            'Score de qualidade',
            ['metric']
        )
    
    @contextmanager
    def measure_latency(self, stage: str):
        """Mede latência de uma etapa."""
        start = time.time()
        try:
            yield
        finally:
            self.latency.labels(stage=stage).observe(time.time() - start)
    
    def record_tokens(self, count: int, token_type: str = "total"):
        """Registra tokens usados."""
        self.tokens.labels(type=token_type).inc(count)
    
    def record_query(self, status: str = "success"):
        """Registra query."""
        self.queries.labels(status=status).inc()
    
    def set_quality(self, metric: str, value: float):
        """Define score de qualidade."""
        self.quality.labels(metric=metric).set(value)


# Singleton
metrics = MetricsCollector()
