import streamlit as st

from config import UI_FONT_SERIF, UI_FONT_SANS, UI_PRIMARY_COLOR

def apply_custom_styles():
    """
    Aplica o design system da Hipótese Capital usando as constantes de config.py.
    """
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600&display=swap');

        /* Fontes */
        h1, h2, h3, .section-header {{
            font-family: {UI_FONT_SERIF} !important;
            color: var(--text-color);
        }}

        body, p, div {{
            font-family: {UI_FONT_SANS};
        }}

        /* Cards de Métricas */
        [data-testid="stMetric"] {{
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.2);
            padding: 20px;
            border-radius: 8px;
        }}
        
        [data-testid="stMetricValue"] {{
            font-family: {UI_FONT_SERIF};
            color: {UI_PRIMARY_COLOR} !important;
        }}

        /* Headers de Seção Customizados */
        .section-header {
            border-bottom: 1px solid rgba(128, 128, 128, 0.3);
            padding-bottom: 8px;
            margin-top: 40px;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }

        /* Callouts de Sentimento */
        .sentiment-positivo { 
            background-color: rgba(34, 197, 94, 0.15); 
            color: #4ade80; 
            padding: 15px; border-radius: 5px; border-left: 5px solid #22c55e; 
        }
        .sentiment-negativo { 
            background-color: rgba(239, 68, 68, 0.15); 
            color: #f87171; 
            padding: 15px; border-radius: 5px; border-left: 5px solid #ef4444; 
        }
        .sentiment-neutro { 
            background-color: rgba(234, 179, 8, 0.15); 
            color: #facc15; 
            padding: 15px; border-radius: 5px; border-left: 5px solid #eab308; 
        }
        </style>
        """, unsafe_allow_html=True)
