import streamlit as st
from core.collector import DataCollector
from core.analyzer import InvestmentAnalyzer
from utils.logger import logger

# Importações dos módulos de UI
from ui.styles import apply_custom_styles
from ui.sidebar import render_sidebar
from ui.components import (
    render_header,
    render_summary_cards,
    render_price_chart,
    render_recent_news_list,
    render_ai_analysis
)

from config import PROJECT_NAME

# Configuração da Página
st.set_page_config(
    page_title=PROJECT_NAME,
    page_icon="🏛️",
    layout="wide"
)

def run_analytical_pipeline(ticker_symbol: str, model_name: str):
    """
    Orquestra a coleta e análise dos dados para um determinado ticker.
    """
    with st.spinner(f"Refinando análise de valor para {ticker_symbol}..."):
        # 1. Coleta de Dados (Market & News)
        collector = DataCollector(ticker_symbol)
        data = collector.collect_all_data()
        
        if not data:
            st.error("Erro na coleta de dados. Verifique se o ticker é válido na B3.")
            return

        # 2. Renderização Visual dos Dados Coletados
        nome_empresa = data.get('cadastral', {}).get('nome', ticker_symbol)
        render_header(ticker_symbol, nome_empresa)
        
        render_summary_cards(data)
        render_price_chart(collector)
        render_recent_news_list(data.get("news", []))
        
        # 3. Análise Qualitativa via LLM
        analyzer = InvestmentAnalyzer(model=model_name)
        analysis = analyzer.analyze_ticker(ticker_symbol, data)
        
        if "error" in analysis:
            st.error(f"Erro na análise da IA: {analysis['error']}")
        else:
            render_ai_analysis(analysis)

def main():
    # Aplica Identidade Visual
    apply_custom_styles()
    
    # Renderiza Barra Lateral e captura inputs
    ticker_symbol, model_name, run_analysis = render_sidebar()

    if run_analysis:
        run_analytical_pipeline(ticker_symbol, model_name)
    else:
        # Estado de Boas-vindas (Initial State) - Sem Logo (centralizado na sidebar)
        st.markdown(f"<h1>{PROJECT_NAME}</h1>", unsafe_allow_html=True)
        st.write("Selecione um ativo na barra lateral para iniciar a devida diligência sob a ótica de Value Investing.")
        
        st.info("""
            **Bem-vindo ao Terminal Hipótese Capital.** 
            Este sistema automatiza a coleta de indicadores fundamentalistas, 
            notícias de mercado e gera uma síntese qualitativa focada em proteção de downside e valor intrínseco.
        """)

if __name__ == "__main__":
    main()
