import streamlit as st
from config import UI_FONT_SERIF, UI_FONT_SANS, UI_PRIMARY_COLOR, UI_BG_COLOR, UI_TEXT_COLOR, BRAND_PALETTE, UI_SECONDARY_RED

def apply_custom_styles():
    """
    Aplica o design system da Hipótese Capital em TEMA ESCURO.
    Protege ícones do Streamlit e garante tipografia serifada nos locais corretos.
    """
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Sans+Pro:wght@400;600&display=swap');

        /* 1. RESET E PROTEÇÃO DE ÍCONES (IMPORTANTE) */
        /* Impede que a fonte Serif quebre os ícones nativos do Streamlit */
        [data-testid="stIcon"], .material-icons, [data-icon], svg, i {{
            font-family: inherit !important;
            font-feature-settings: normal !important;
            font-variant-ligatures: normal !important;
        }}

        /* 2. CONFIGURAÇÃO DE CORES (TEMA ESCURO) */
        :root {{
            --brand-red: {UI_PRIMARY_COLOR};
            --brand-bg: {UI_BG_COLOR};
            --brand-text: {UI_TEXT_COLOR};
            --brand-red-light: {UI_SECONDARY_RED};
        }}

        /* 3. ESTILIZAÇÃO DE FUNDO E INTERFACE GERAL */
        .stApp, [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"] {{
            background-color: var(--brand-bg) !important;
            color: var(--brand-text) !important;
        }}

        /* 4. TIPOGRAFIA SERIFADA (PLAYFAIR DISPLAY) - APENAS CONTEÚDO NOBRE */
        /* Seletores específicos para evitar quebrar botões e menus de sistema */
        h1, h2, h3, h4, h5, h6, 
        .stTitle, 
        .section-header,
        [data-testid="stMetricValue"] {{
            font-family: {UI_FONT_SERIF} !important;
            color: var(--brand-red) !important;
            font-weight: 700 !important;
        }}

        /* 5. TIPOGRAFIA SANS (SOURCE SANS PRO) - LEITURA E INTERFACE */
        body, p, span, label, input, button, 
        .stMarkdown, [data-testid="stMetricLabel"], .stSelectbox div {{
            font-family: {UI_FONT_SANS} !important;
            color: var(--brand-text) !important;
        }}

        /* 6. SIDEBAR E COMPONENTES */
        [data-testid="stSidebar"] {{
            border-right: 1px solid rgba(255, 240, 196, 0.05);
        }}
        
        /* Inputs e Seletores */
        .stTextInput > div > div > input, .stSelectbox > div > div > div {{
            background-color: rgba(255, 240, 196, 0.03) !important;
            border: 1px solid rgba(255, 240, 196, 0.1) !important;
        }}

        /* Botões */
        .stButton > button {{
            background-color: var(--brand-red) !important;
            color: var(--brand-text) !important;
            border-radius: 4px !important;
            border: 1px solid var(--brand-red) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600 !important;
        }}
        
        .stButton > button:hover {{
            background-color: var(--brand-red-light) !important;
            border-color: var(--brand-red-light) !important;
            box-shadow: 0 4px 15px rgba(102, 11, 5, 0.5);
            color: white !important;
        }}

        /* Cards de Métricas */
        [data-testid="stMetric"] {{
            background-color: rgba(255, 240, 196, 0.02) !important;
            border: 1px solid rgba(255, 240, 196, 0.08) !important;
            padding: 20px !important;
            border-radius: 4px !important;
        }}

        [data-testid="stMetricLabel"] {{
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-size: 0.7rem !important;
            opacity: 0.7;
        }}

        /* Headers de Seção */
        .section-header {{
            border-bottom: 2px solid var(--brand-red);
            padding-bottom: 10px;
            margin-top: 45px;
            margin-bottom: 25px;
            font-size: 1.8rem;
        }}

        /* Alertas e Callouts */
        .stAlert {{
            background-color: rgba(255, 240, 196, 0.05) !important;
            border: 1px solid rgba(255, 240, 196, 0.1) !important;
        }}

        .sentiment-positivo {{ 
            background-color: rgba(34, 197, 94, 0.12); color: #4ade80; 
            padding: 18px; border-radius: 4px; border-left: 5px solid #22c55e; margin: 10px 0;
        }}
        .sentiment-negativo {{ 
            background-color: rgba(239, 68, 68, 0.12); color: #f87171; 
            padding: 18px; border-radius: 4px; border-left: 5px solid #ef4444; margin: 10px 0;
        }}
        .sentiment-neutro {{ 
            background-color: rgba(234, 179, 8, 0.12); color: #facc15; 
            padding: 18px; border-radius: 4px; border-left: 5px solid #eab308; margin: 10px 0;
        }}

        hr {{ border-top: 1px solid rgba(255, 240, 196, 0.1) !important; margin: 2rem 0; }}
        
        </style>
        """, unsafe_allow_html=True)
