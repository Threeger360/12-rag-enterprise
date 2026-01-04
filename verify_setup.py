#!/usr/bin/env python3
"""Verifica setup do RAG Enterprise."""
import sys, os
from dotenv import load_dotenv
load_dotenv()

print("="*50)
print("  RAG Enterprise - Verificação")
print("="*50)

# API Key
if os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
    print("✅ OPENAI_API_KEY")
else:
    print("❌ OPENAI_API_KEY não configurada")

# Módulos
for mod in ["langchain", "langgraph", "fastapi", "chromadb", "streamlit"]:
    try:
        __import__(mod)
        print(f"✅ {mod}")
    except ImportError:
        print(f"❌ {mod}")

