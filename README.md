# 🏢 RAG Enterprise

## Sistema RAG Completo para Produção

> O projeto final que integra TUDO que você aprendeu.

---

## 📋 Sobre o Projeto

O **RAG Enterprise** é um sistema completo de Retrieval-Augmented Generation pronto para produção, combinando todas as técnicas do curso:

- ✅ Múltiplas estratégias de RAG (Hybrid, Adaptive, Self-RAG)
- ✅ Sistema multi-agentes especializados
- ✅ API REST com FastAPI
- ✅ Observabilidade e métricas
- ✅ Interface web completa
- ✅ Segurança e governança

---

## 🎯 Funcionalidades

### RAG Avançado
| Feature | Descrição |
|---------|-----------|
| Hybrid Search | Semântico + BM25 |
| Adaptive Routing | Escolhe estratégia |
| Self-Evaluation | Auto-avaliação |
| HyDE | Queries vagas |
| Reranking | LLM reordena |

### Agentes Especializados
| Agente | Função |
|--------|--------|
| Orchestrator | Coordena fluxo |
| Retriever | Busca documentos |
| Analyst | Analisa contexto |
| Generator | Gera respostas |
| Validator | Valida qualidade |

### Observabilidade
| Métrica | Descrição |
|---------|-----------|
| Latência | Por etapa |
| Tokens | Consumo |
| Qualidade | Scores |
| Erros | Tracking |

---

## 🚀 Quick Start

### 1. Clone o Projeto

```bash
git clone <repo>
cd 12-rag-enterprise
```

### 2. Configure o Ambiente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Variáveis

```bash
cp .env.example .env
# Edite com suas chaves
```

### 4. Inicialize

```bash
make init
```

### 5. Execute

```bash
# API
make api

# Interface
make app
```

---

## 📁 Estrutura do Projeto

```
12-rag-enterprise/
├── README.md
├── ROTEIRO.md
├── APOIO.md
├── requirements.txt
├── .env.example
├── Makefile
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── retriever.py       # Hybrid retriever
│   │   ├── reranker.py        # LLM reranker
│   │   ├── generator.py       # Response generator
│   │   ├── evaluator.py       # Self-evaluation
│   │   └── pipeline.py        # RAG pipeline
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py    # Main coordinator
│   │   ├── retriever_agent.py # Search specialist
│   │   ├── analyst_agent.py   # Analysis specialist
│   │   └── validator_agent.py # Quality validator
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app
│   │   ├── routes.py          # Endpoints
│   │   └── middleware.py      # Auth, logging
│   │
│   └── observability/
│       ├── __init__.py
│       ├── metrics.py         # Prometheus metrics
│       ├── tracing.py         # Request tracing
│       └── logging.py         # Structured logging
│
├── app.py                     # Streamlit interface
│
├── tests/
│   ├── test_rag.py
│   ├── test_agents.py
│   └── test_api.py
│
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   └── api.md
│
└── data/
    └── documents/
```

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAG ENTERPRISE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    API LAYER                            │    │
│  │            FastAPI + Auth + Rate Limiting               │    │
│  └─────────────────────────────┬───────────────────────────┘    │
│                                │                                │
│  ┌─────────────────────────────▼───────────────────────────┐    │
│  │                  ORCHESTRATOR AGENT                     │    │
│  │              Coordena todo o pipeline                   │    │
│  └─────────────────────────────┬───────────────────────────┘    │
│                                │                                │
│       ┌────────────────────────┼────────────────────────┐       │
│       │                        │                        │       │
│       ▼                        ▼                        ▼       │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │  RETRIEVER  │      │  ANALYST    │      │  VALIDATOR  │     │
│  │   AGENT     │      │   AGENT     │      │   AGENT     │     │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘     │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    RAG PIPELINE                         │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │    │
│  │  │ Hybrid  │→│ Rerank  │→│Generate │→│Evaluate │       │    │
│  │  │ Search  │ │  LLM    │ │Response │ │ Self    │       │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   OBSERVABILITY                         │    │
│  │         Metrics • Tracing • Logging • Alerts            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/query` | Processa pergunta |
| POST | `/documents` | Adiciona documentos |
| GET | `/health` | Health check |
| GET | `/metrics` | Métricas Prometheus |
| GET | `/stats` | Estatísticas |

### Exemplo de Request

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Qual a política de férias?"}'
```

### Exemplo de Response

```json
{
  "answer": "A política de férias...",
  "confidence": 0.95,
  "sources": ["doc1.pdf", "doc2.pdf"],
  "latency_ms": 1234,
  "tokens_used": 1500
}
```

---

## 🔧 Comandos

```bash
make install    # Instala dependências
make init       # Inicializa sistema
make api        # Inicia API FastAPI
make app        # Inicia Streamlit
make test       # Executa testes
make lint       # Verifica código
make clean      # Limpa cache
```

---

## 📈 Métricas

O sistema expõe métricas Prometheus:

```
# Latência
rag_latency_seconds{stage="retrieve"}
rag_latency_seconds{stage="generate"}

# Tokens
rag_tokens_total{type="input"}
rag_tokens_total{type="output"}

# Qualidade
rag_quality_score{metric="support"}
rag_quality_score{metric="utility"}
```

---

## 🔒 Segurança

| Feature | Implementação |
|---------|---------------|
| Autenticação | API Key |
| Rate Limiting | 100 req/min |
| Input Validation | Pydantic |
| SQL Injection | Prevenido |
| Prompt Injection | Sanitização |

---

## 📚 Tecnologias

| Categoria | Tecnologia |
|-----------|------------|
| LLM | OpenAI GPT-4o |
| Embeddings | OpenAI Ada |
| Vector Store | ChromaDB |
| BM25 | rank-bm25 |
| API | FastAPI |
| Frontend | Streamlit |
| Orquestração | LangGraph |

---

## 👤 Autor

**Alexsander Valente**  
[alexsander.app.br](https://alexsander.app.br)

---

*Projeto Final do curso IA Generativa na Prática*
