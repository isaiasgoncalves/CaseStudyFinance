import streamlit as st
import pandas as pd
from core.collector import DataCollector
from core.analyzer import InvestmentAnalyzer
from utils.logger import logger

# Configuração da Página
st.set_page_config(
    page_title="Hipótese Capital | Terminal Analítico",
    page_icon="🏛️",
    layout="wide"
)

# --- BRANDING & DESIGN (SERIF & TEMA ADAPTÁVEL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600&display=swap');

    /* Fontes Serifadas para Headers - Adaptável ao tema */
    h1, h2, h3, .section-header {
        font-family: 'Playfair Display', serif !important;
        color: var(--text-color);
    }

    /* Fonte para corpo de texto */
    body, p, div {
        font-family: 'Source Sans Pro', sans-serif;
    }

    /* Ajuste nos Cards de Métricas (Fundo adaptável ao tema) */
    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 20px;
        border-radius: 8px;
    }
    
    /* Cor do Título da Métrica */
    [data-testid="stMetricLabel"] {
        color: var(--text-color);
        opacity: 0.8;
    }
    
    /* Valor da Métrica em Destaque Serifado */
    [data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif;
        color: #1e40af !important; /* Um azul que funciona bem em ambos os temas */
    }

    /* Headers de Seção Customizados */
    .section-header {
        border-bottom: 1px solid rgba(128, 128, 128, 0.3);
        padding-bottom: 8px;
        margin-top: 40px;
        margin-bottom: 20px;
        font-size: 1.8rem;
    }

    /* Cores de Callouts de Sentimento (Opacidade para funcionar no Dark Mode) */
    .sentiment-positivo { 
        background-color: rgba(34, 197, 94, 0.2); 
        color: #4ade80; 
        padding: 15px; 
        border-radius: 5px; 
        border-left: 5px solid #22c55e; 
    }
    .sentiment-negativo { 
        background-color: rgba(239, 68, 68, 0.2); 
        color: #f87171; 
        padding: 15px; 
        border-radius: 5px; 
        border-left: 5px solid #ef4444; 
    }
    .sentiment-neutro { 
        background-color: rgba(234, 179, 8, 0.2); 
        color: #facc15; 
        padding: 15px; 
        border-radius: 5px; 
        border-left: 5px solid #eab308; 
    }
    
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE INTERFACE (MODULARES) ---

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🏛️ Hipótese Capital</h2>", unsafe_allow_html=True)
        st.divider()
        ticker = st.text_input("Ticker B3 (ex: ASAI3, ITUB4)", value="ASAI3").upper()
        model_name = st.selectbox("Modelo Analítico", ["gpt-4o-mini", "gpt-4o"])
        analyze_button = st.button("Executar Análise de Valor", use_container_width=True)
        return ticker, model_name, analyze_button

def render_summary_cards(data):
    st.markdown("<div class='section-header'>Indicadores Fundamentalistas</div>", unsafe_allow_html=True)
    indicators = data.get("market_indicators", {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Formatação segura de valores
    def fmt_pct(val): return f"{val*100:.2f}%" if val else "N/A"
    def fmt_curr(val): return f"R$ {val:.2f}" if val else "N/A"
    def fmt_num(val): return f"{val:.2f}" if val else "N/A"

    col1.metric("Cotação Atual", fmt_curr(indicators.get('preco_atual')))
    col2.metric("P/L", fmt_num(indicators.get('p_l')))
    col3.metric("ROE", fmt_pct(indicators.get('roe')))
    col4.metric("Margem Líquida", fmt_pct(indicators.get('margem_liquida')))
    col5.metric("Div. Yield", fmt_pct(indicators.get('dy')))

def render_price_chart(collector):
    st.markdown("<div class='section-header'>Performance Histórica (12m)</div>", unsafe_allow_html=True)
    history = collector.get_history(period="1y")
    if not history.empty:
        st.line_chart(history['Close'], width='stretch', color="#1e3a8a")

def render_recent_news_list(news_data):
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

def get_sentiment_class(sentiment_text):
    """Determina a classe CSS com base no texto de sentimento."""
    text = sentiment_text.lower()
    if "positivo" in text: return "sentiment-positivo"
    if "negativo" in text: return "sentiment-negativo"
    return "sentiment-neutro"

def render_ai_analysis(analysis):
    st.markdown("<div class='section-header'>Síntese do Comitê de Análise</div>", unsafe_allow_html=True)
    
    # Resumo como bloco de texto normal
    st.subheader("Resumo do Negócio")
    st.write(analysis.get("resumo_negocio", "N/A"))
    
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Análise de Valor & Downside")
        st.write(analysis.get("analise_indicadores", "N/A"))
        
        # Sentimento em Callout Colorido
        sentiment_text = analysis.get("sentimento_noticias", "Neutro")
        sentiment_class = get_sentiment_class(sentiment_text)
        st.markdown(f"<div class='{sentiment_class}'><strong>Clima das Notícias:</strong><br>{sentiment_text}</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("Questões Investigativas (Checklist RI)")
        for i, q in enumerate(analysis.get("perguntas_investigativas", []), 1):
            st.markdown(f"**{i}.** {q}")

# --- FLUXO PRINCIPAL ---

def main():
    ticker_symbol, model_name, run_analysis = render_sidebar()

    if run_analysis:
        with st.spinner("Refinando análise..."):
            # 1. Coleta
            collector = DataCollector(ticker_symbol)
            data = collector.collect_all_data()
            
            if not data:
                st.error("Erro na coleta. Verifique o ticker.")
                return

            # 2. Header de Identificação
            nome_empresa = data.get('cadastral', {}).get('nome', ticker_symbol)
            st.markdown(f"# {nome_empresa} <span style='font-size: 1.2rem; color: #666;'>({ticker_symbol})</span>", unsafe_allow_html=True)

            # 3. Componentes Visuais
            render_summary_cards(data)
            render_price_chart(collector)
            
            # 4. Notícias Reais
            render_recent_news_list(data.get("news", []))
            
            # 5. Inteligência Artificial
            analyzer = InvestmentAnalyzer(model=model_name)
            analysis = analyzer.analyze_ticker(ticker_symbol, data)
            
            if "error" in analysis:
                st.error(f"Erro na IA: {analysis['error']}")
            else:
                render_ai_analysis(analysis)
    else:
        # Estado Inicial
        st.title("🏛️ Terminal Hipótese Capital")
        st.write("Selecione um ativo na barra lateral para iniciar a devida diligência.")

if __name__ == "__main__":
    main()
