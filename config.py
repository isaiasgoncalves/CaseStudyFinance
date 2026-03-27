import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente (.env)
load_dotenv()

# --- CONFIGURAÇÕES GERAIS DO PROJETO ---
PROJECT_NAME = "Hipótese Capital | Terminal Analítico"
VERSION = "1.0.1 (Fase 1 Refinada)"
DEFAULT_TICKER = "ASAI3"
DEFAULT_HISTORY_PERIOD = "1y"
NEWS_LIMIT = 5

# --- CONFIGURAÇÕES DE IA (LLM) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
AVAILABLE_MODELS = ["gpt-4o-mini", "gpt-4o"]

# --- CONFIGURAÇÕES DE UI & DESIGN ---
BRAND_PALETTE = {
    "primary_red": "#660B05",
    "light": "#FFF0C4",
    "light_red": "#8C1007",
    "dark_red": "#3E0703",
    "light_silver": "#979797",
    "dark_silver": "#141413",
}
UI_PRIMARY_COLOR = "#1e3a8a"  # Azul Marinho Hipótese
UI_SECONDARY_COLOR = "#1e40af"
UI_FONT_SERIF = "'Playfair Display', serif"
UI_FONT_SANS = "'Source Sans Pro', sans-serif"

# --- PROMPTS DO SISTEMA (CONSOLIDADO) ---
SYSTEM_PERSONA = "Você é um Analista de Investimentos Sênior na Hipótese Capital, uma gestora focada em Value Investing."

VALUE_INVESTING_ANALYSIS_PROMPT = """
Analise a empresa {ticker} ({nome_empresa}) com base nos seguintes dados:

--- DADOS CADASTRAIS ---
Setor: {setor}
Segmento: {segmento}
Resumo do Negócio: {resumo_negocio}

--- INDICADORES DE MERCADO ---
P/L: {p_l}
ROE: {roe}
Dívida Líquida/EBITDA: {divida_ebitda}
Margem Líquida: {margem_liquida}
Dividend Yield: {dy}

--- NOTÍCIAS RECENTES ---
{noticias}

--- INSTRUÇÕES DO ANALISTA SÊNIOR (HIPÓTESE CAPITAL) ---
Você deve agir como um Analista Sênior da Hipótese Capital. Sua filosofia é o Value Investing: busca por empresas de alta qualidade, fossos econômicos (moats) defensáveis e margem de segurança.

Gere um JSON com as seguintes chaves:
1. "resumo_negocio": Uma síntese concisa do modelo de geração de valor (2-3 frases).
2. "analise_indicadores": Interpretação qualitativa. O que esses números dizem sobre a saúde do negócio e a proteção de downside? Seja crítico.
3. "sentimento_noticias": Analise o impacto das notícias recentes no valor intrínseco. Classifique como positiva, negativa ou neutra.
4. "perguntas_investigativas": Três perguntas cruciais que desafiem a tese de investimento, voltadas para o RI da empresa.

O tom deve ser técnico, direto e focado em preservação de capital.
"""

# Placeholder para prompts futuros (Fase 3)
RAG_ANALYSIS_PROMPT = """
...
"""
