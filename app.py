import streamlit as st
from core.collector import DataCollector
from core.analyzer import InvestmentAnalyzer
from utils.logger import logger

# Importações dos módulos de UI refinados
from ui.styles import apply_custom_styles
from ui.sidebar import render_sidebar
from ui.components import (
    render_header,
    render_summary_cards,
    render_price_chart,
    render_recent_news_list,
    render_ai_analysis
)

from config import PROJECT_NAME, VERSION

# Configuração da Página (Nativa e Limpa)
st.set_page_config(
    page_title=PROJECT_NAME,
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def run_analytical_pipeline(ticker_symbol: str, model_name: str):
    """
    Orquestra a coleta e análise dos dados para um determinado ticker.
    """
    # 1. Coleta de Dados (Market & News)
    with st.status(f"Coletando dados para {ticker_symbol}...", expanded=True) as status:
        collector = DataCollector(ticker_symbol)
        data = collector.collect_all_data()
        
        if not data:
            status.update(label="Falha na coleta de dados!", state="error")
            st.error("Erro na coleta de dados. Verifique se o ticker é válido na B3.")
            return

        status.update(label="Dados coletados com sucesso. Iniciando análise via LLM...", state="running")
        
        # 2. Análise Qualitativa via LLM (Chamada síncrona dentro do status)
        analyzer = InvestmentAnalyzer(model=model_name)
        analysis = analyzer.analyze_ticker(ticker_symbol, data)
        
        if "error" in analysis:
            status.update(label="Análise da IA falhou!", state="error")
            st.error(f"Erro na análise da IA: {analysis['error']}")
            return

        status.update(label="Diligência Completa!", state="complete")

    # 3. Renderização Visual dos Resultados
    nome_empresa = data.get('cadastral', {}).get('nome', ticker_symbol)
    render_header(ticker_symbol, nome_empresa)
    
    # Layout em duas colunas principais para o dashboard
    col_left, col_right = st.columns([0.65, 0.35], gap="large")
    
    with col_left:
        render_summary_cards(data)
        render_price_chart(collector)
        render_ai_analysis(analysis)
        
    with col_right:
        render_recent_news_list(
            data.get("news", []), 
            sentiment_analysis=analysis.get("sentimento_noticias")
        )
        
        # Disclaimer Legal (Padrão Financeiro)
        st.divider()
        st.caption("""
            **Aviso Legal:** Esta ferramenta é um protótipo experimental de IA para auxílio à decisão 
            de investimentos. Os dados são provenientes de fontes públicas e a análise é gerada 
            por um modelo de linguagem. Não constitui recomendação de compra ou venda de ativos.
        """)

def main():
    # Aplica Identidade Visual e CSS específico
    apply_custom_styles()
    
    # Renderiza Barra Lateral e captura inputs
    ticker_symbol, model_name, run_analysis = render_sidebar()

    if run_analysis:
        run_analytical_pipeline(ticker_symbol, model_name)
    else:
        # Estado de Boas-vindas (Initial State)
        st.title(f"🏛️ {PROJECT_NAME}")
        st.subheader("Bem-vindo ao Centro de Diligência Hipótese Capital.")
        
        st.markdown(f"""
            Este terminal foi desenvolvido para auxiliar a equipe de análise na triagem de ativos 
            sob a filosofia de **Value Investing**. 
            
            **Como começar:**
            1. Insira o ticker de uma empresa da B3 na barra lateral (ex: `ASAI3`, `RECV3`).
            2. Selecione o modelo de IA desejado.
            3. Clique em 'Executar Análise de Valor'.
            
            ---
            *Versão do Sistema: {VERSION}*
        """)
        
        # Opcional: Mostrar uma imagem inspiradora ou logo centralizado
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("Aguardando seleção de ativo na barra lateral...")

if __name__ == "__main__":
    main()
