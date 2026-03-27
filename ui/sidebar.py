import streamlit as st

from config import DEFAULT_TICKER, AVAILABLE_MODELS, VERSION

def render_sidebar():
    """
    Renderiza a barra lateral usando configurações de config.py.
    """
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🏛️ Hipótese Capital</h2>", unsafe_allow_html=True)
        st.divider()
        
        ticker = st.text_input(
            "Ticker B3 (ex: ASAI3, ITUB4)", 
            value=DEFAULT_TICKER,
            help="Digite o código da empresa na B3."
        ).upper()
        
        model_name = st.selectbox(
            "Modelo Analítico", 
            AVAILABLE_MODELS,
            help="Escolha o motor de inteligência para a síntese qualitativa."
        )
        
        analyze_button = st.button("Executar Análise de Valor", use_container_width=True)
        
        st.v_spacer(height=20)
        st.caption(f"Terminal Analítico | {VERSION}")
        
        return ticker, model_name, analyze_button
