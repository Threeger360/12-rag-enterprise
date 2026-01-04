"""
🏢 RAG Enterprise - Interface Streamlit

Execute com: streamlit run app.py
"""

import streamlit as st
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

# Configuração
st.set_page_config(
    page_title="RAG Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #3b82f6;
        text-align: center;
    }
    .metric-card {
        background: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# Documentos exemplo
EXAMPLE_DOCS = [
    """Política de Férias - RH
Os colaboradores têm direito a 30 dias de férias após 12 meses.
Divisão em até 3 períodos permitida.
Solicitar com 30 dias de antecedência.""",

    """Política de Home Office
Máximo 3 dias por semana.
Elegível após 3 meses de empresa.
Equipamentos fornecidos pela empresa.""",

    """Código CLI-2024-0892: Empresa Alpha
Status: Ativo
Contrato: CNT-2024-1234
Valor: R$ 15.000/mês""",

    """Erros do Sistema
NF-404: Nota fiscal não encontrada
AUTH-401: Credenciais inválidas
API-429: Rate limit excedido"""
]


def init_state():
    if "rag" not in st.session_state:
        st.session_state.rag = None
    if "loaded" not in st.session_state:
        st.session_state.loaded = False
    if "history" not in st.session_state:
        st.session_state.history = []


def get_rag():
    if st.session_state.rag is None:
        try:
            from src.rag.pipeline import RAGPipeline
            st.session_state.rag = RAGPipeline()
        except Exception as e:
            st.error(f"Erro: {e}")
            return None
    return st.session_state.rag


def render_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ Configurações")
        
        # Status
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key.startswith("sk-"):
            st.success("✅ API Key OK")
        else:
            st.error("❌ Configure OPENAI_API_KEY")
        
        st.markdown("---")
        
        # Documentos
        st.markdown("### 📄 Documentos")
        
        if not st.session_state.loaded:
            if st.button("📥 Carregar Exemplos"):
                rag = get_rag()
                if rag:
                    with st.spinner("Indexando..."):
                        rag.add_documents(EXAMPLE_DOCS)
                    st.session_state.loaded = True
                    st.success("✅ Carregado!")
                    st.rerun()
        else:
            st.success("✅ Documentos prontos")
        
        st.markdown("---")
        
        # Stats
        if st.session_state.loaded:
            rag = get_rag()
            if rag:
                stats = rag.get_stats()
                st.markdown("### 📊 Estatísticas")
                st.metric("Queries", stats["total_queries"])
                st.metric("Documentos", stats["documents_indexed"])


def render_main():
    st.markdown('<p class="main-header">🏢 RAG Enterprise</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#60a5fa;">Sistema RAG Completo para Produção</p>', unsafe_allow_html=True)
    
    if not st.session_state.loaded:
        st.info("👈 Carregue os documentos de exemplo para começar")
        
        # Features
        st.markdown("### 🎯 Funcionalidades")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **RAG Avançado**
            - Hybrid Search
            - Self-Evaluation
            - Refinamento
            """)
        
        with col2:
            st.markdown("""
            **Multi-Agentes**
            - Orchestrator
            - Retriever
            - Validator
            """)
        
        with col3:
            st.markdown("""
            **Produção**
            - API REST
            - Métricas
            - Observabilidade
            """)
        
        return
    
    # Input
    st.markdown("### 💬 Faça sua pergunta")
    
    query = st.text_input(
        "Pergunta:",
        placeholder="Ex: Qual a política de férias?",
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Processar", type="primary"):
        if query:
            rag = get_rag()
            if rag:
                with st.spinner("🔄 Processando..."):
                    result = rag.process(query)
                
                st.markdown("---")
                
                # Métricas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Confiança", f"{result.confidence*100:.0f}%")
                with col2:
                    st.metric("Latência", f"{result.latency_ms:.0f}ms")
                with col3:
                    st.metric("Refinado", "Sim" if result.was_refined else "Não")
                
                # Resposta
                st.markdown("### 💡 Resposta")
                st.write(result.answer)
                
                # Fontes
                if result.sources:
                    with st.expander("📚 Fontes"):
                        for src in result.sources:
                            st.write(f"• {src}")
                
                # Histórico
                st.session_state.history.append({
                    "q": query,
                    "a": result.answer[:100]
                })


def main():
    init_state()
    render_sidebar()
    render_main()


if __name__ == "__main__":
    main()
