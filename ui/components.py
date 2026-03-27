import streamlit as st
import pandas as pd
from config import UI_PRIMARY_COLOR, UI_TEXT_COLOR

def render_header(ticker_symbol: str, nome_empresa: str):
    """Exibe o cabeçalho de identificação da empresa."""
    st.markdown(
        f"<h1>{nome_empresa} <span style='font-size: 1.2rem; color: {UI_TEXT_COLOR}; opacity: 0.6;'>({ticker_symbol})</span></h1>", 
        unsafe_allow_html=True
    )

def render_summary_cards(data: dict):
    """Renderiza os indicadores fundamentalistas em cards."""
    st.markdown("<div class='section-header'>Indicadores Fundamentalistas</div>", unsafe_allow_html=True)
    indicators = data.get("market_indicators", {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    def fmt_pct(val): return f"{val*100:.2f}%" if val else "N/A"
    def fmt_curr(val): return f"R$ {val:.2f}" if val else "N/A"
    def fmt_num(val): return f"{val:.2f}" if val else "N/A"

    col1.metric("Cotação Atual", fmt_curr(indicators.get('preco_atual')))
    col2.metric("P/L", fmt_num(indicators.get('p_l')))
    col3.metric("ROE", fmt_pct(indicators.get('roe')))
    col4.metric("Margem Líquida", fmt_pct(indicators.get('margem_liquida')))
    col5.metric("Div. Yield", fmt_pct(indicators.get('dy')))

def render_price_chart(collector):
    """Gera o gráfico de performance histórica."""
    st.markdown("<div class='section-header'>Performance Histórica (12m)</div>", unsafe_allow_html=True)
    history = collector.get_history(period="1y")
    if not history.empty:
        # Usando a cor primária da marca (Vermelho Hipótese) para a linha
        st.line_chart(history['Close'], width='stretch', color=UI_PRIMARY_COLOR)

def render_recent_news_list(news_data: list):
    """Renderiza a lista de notícias coletadas com links."""
    st.markdown("<div class='section-header'>Notícias Mais Relevantes</div>", unsafe_allow_html=True)
    if not news_data:
        st.write("Nenhuma notícia recente encontrada.")
        return

    for n in news_data[:5]:
        with st.container():
            col_icon, col_content = st.columns([0.05, 0.95])
            col_icon.write("📰")
            title = n.get('title', 'Sem título')
            link = n.get('link', '#')
            publisher = n.get('publisher', 'Fonte desconhecida')
            col_content.markdown(f"**[{title}]({link})**  \n*Fonte: {publisher}*")
            st.write("")

def _get_sentiment_class(sentiment_text: str) -> str:
    """Determina a classe CSS com base no texto de sentimento."""
    text = sentiment_text.lower()
    if "positivo" in text: return "sentiment-positivo"
    if "negativo" in text: return "sentiment-negativo"
    return "sentiment-neutro"

def render_ai_analysis(analysis: dict):
    """Exibe a síntese gerada pelo LLM sob a ótica de Value Investing."""
    st.markdown("<div class='section-header'>Síntese do Comitê de Análise</div>", unsafe_allow_html=True)
    
    st.subheader("Resumo do Negócio")
    st.write(analysis.get("resumo_negocio", "N/A"))
    
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Análise de Valor & Downside")
        st.write(analysis.get("analise_indicadores", "N/A"))
        
        sentiment_text = analysis.get("sentimento_noticias", "Neutro")
        sentiment_class = _get_sentiment_class(sentiment_text)
        st.markdown(
            f"<div class='{sentiment_class}'><strong>Clima das Notícias:</strong><br>{sentiment_text}</div>", 
            unsafe_allow_html=True
        )

    with col2:
        st.subheader("Questões Investigativas (Checklist RI)")
        for i, q in enumerate(analysis.get("perguntas_investigativas", []), 1):
            st.markdown(f"**{i}.** {q}")
