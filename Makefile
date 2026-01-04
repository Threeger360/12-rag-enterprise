# RAG Enterprise - Makefile

.PHONY: install init api app test clean

install:
	pip install -r requirements.txt

init:
	mkdir -p data/chroma data/documents

api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

app:
	streamlit run app.py

test:
	pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ data/chroma/ 2>/dev/null || true
