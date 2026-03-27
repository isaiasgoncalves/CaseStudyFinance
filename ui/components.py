import streamlit as st
import pandas as pd
from config import CHART_COLOR_PRIMARY

def render_header(ticker_symbol: str, nome_empresa: str):
    """Exibe o cabeçalho de identificação da empresa usando componentes nativos."""
    st.title(f"{nome_empresa} :grey[({ticker_symbol})]")

def render_summary_cards(data: dict):
    """Renderiza os indicadores fundamentalistas em cards usando o sistema de colunas nativo."""
    st.header("📊 Indicadores Fundamentalistas")
    indicators = data.get("market_indicators", {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    def fmt_pct(val): return f"{val*100:.2f}%" if val else "N/A"
    def fmt_curr(val): return f"R$ {val:.2f}" if val else "N/A"
    def fmt_num(val): return f"{val:.2f}" if val else "N/A"

    with col1:
        st.metric("Cotação Atual", fmt_curr(indicators.get('preco_atual')))
    with col2:
        st.metric("P/L", fmt_num(indicators.get('p_l')))
    with col3:
        st.metric("ROE", fmt_pct(indicators.get('roe')))
    with col4:
        st.metric("Margem Líquida", fmt_pct(indicators.get('margem_liquida')))
    with col5:
        st.metric("Div. Yield", fmt_pct(indicators.get('dy')))

def render_price_chart(collector):
    """Gera o gráfico de performance histórica com a cor da marca."""
    st.subheader("📈 Performance do Ativo (12 Meses)")
    history = collector.get_history(period="1y")
    if not history.empty:
        st.line_chart(history['Close'], color=CHART_COLOR_PRIMARY)
    else:
        st.warning("Dados históricos de preço não disponíveis.")

def render_recent_news_list(news_data: list):
    """Renderiza a lista de notícias coletadas de forma limpa e organizada."""
    st.header("📰 Notícias Mais Relevantes")
    if not news_data:
        st.info("Nenhuma notícia recente encontrada para este ativo.")
        return

    for n in news_data[:5]:
        with st.expander(f"**{n.get('title', 'Sem título')}**", expanded=False):
            st.write(f"*Fonte: {n.get('publisher', 'Fonte desconhecida')}*")
            st.link_button("Ler Notícia Completa", n.get('link', '#'))

def _get_sentiment_info(sentiment_text: str):
    """Retorna o tipo de alerta e ícone baseado no sentimento."""
    text = sentiment_text.lower()
    if "positivo" in text or "positiva" in text:
        return "success", "🚀"
    if "negativo" in text or "negativa" in text:
        return "error", "⚠️"
    return "info", "🔍"

def render_ai_analysis(analysis: dict):
    """Exibe a síntese gerada pelo LLM sob a ótica de Value Investing."""
    st.header("🏛️ Síntese do Comitê de Análise")
    
    tab1, tab2, tab3 = st.tabs(["Resumo e Tese", "Análise de Risco", "Checklist Investigativo"])
    
    with tab1:
        st.subheader("📌 Resumo do Modelo de Negócio")
        st.write(analysis.get("resumo_negocio", "N/A"))
        
        sentiment_text = analysis.get("sentimento_noticias", "Neutro")
        stype, icon = _get_sentiment_info(sentiment_text)
        
        if stype == "success":
            st.success(f"**Clima das Notícias:** {sentiment_text}", icon=icon)
        elif stype == "error":
            st.error(f"**Clima das Notícias:** {sentiment_text}", icon=icon)
        else:
            st.info(f"**Clima das Notícias:** {sentiment_text}", icon=icon)

    with tab2:
        st.subheader("⚖️ Análise de Valor & Downside")
        st.markdown(f"> {analysis.get('analise_indicadores', 'N/A')}")

    with tab3:
        st.subheader("❓ Perguntas para o RI (Relação com Investidores)")
        for i, q in enumerate(analysis.get("perguntas_investigativas", []), 1):
            st.info(f"**{i}.** {q}")
