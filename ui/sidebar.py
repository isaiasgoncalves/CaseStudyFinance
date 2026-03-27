import streamlit as st
from config import LOGO_LIGHT, DEFAULT_TICKER, AVAILABLE_MODELS, VERSION

def render_sidebar():
    """
    Renderiza a barra lateral com o logo oficial da Hipótese Capital (Versão Clara).
    """
    with st.sidebar:
        # Logo único na sidebar (usando a versão CLARA para fundo ESCURO)
        st.image(LOGO_LIGHT, width='stretch')
        
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
        
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        
        st.caption(f"Hipótese Capital Asset Management")
        st.caption(f"Terminal Analítico | {VERSION}")
        
        return ticker, model_name, analyze_button
