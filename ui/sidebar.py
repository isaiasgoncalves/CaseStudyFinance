import streamlit as st
from config import LOGO_LIGHT, DEFAULT_TICKER, AVAILABLE_MODELS, VERSION

def render_sidebar():
    """
    Renderiza a barra lateral com o logo oficial da Hipótese Capital e controles.
    """
    with st.sidebar:
        # Logo oficial com ajuste automático de largura
        st.image(LOGO_LIGHT, width='stretch')
        
        st.divider()
        
        # Seção de Entrada
        st.subheader("🛠️ Parâmetros de Análise")
        
        ticker = st.text_input(
            "Ticker B3", 
            value=DEFAULT_TICKER,
            help="Ex: ASAI3, ITUB4, RECV3",
            placeholder="Digite o código..."
        ).upper()
        
        model_name = st.selectbox(
            "Modelo Analítico (LLM)", 
            AVAILABLE_MODELS,
            index=0,
            help="Motor de IA para síntese qualitativa."
        )
        
        st.write("") # Espaçamento
        analyze_button = st.button("Executar Análise de Valor", width='stretch', type="primary")
        
        # Rodapé com informações da versão
        st.v_spacer = st.container() # Forçar para o fundo se possível (Streamlit simplificado)
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        
        st.caption("---")
        st.caption(f"**Hipótese Capital** *Asset Management*")
        st.caption(f"por *Isaías G. Gonçalves* | Versão {VERSION}")
        
        return ticker, model_name, analyze_button
