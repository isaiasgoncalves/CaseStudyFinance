"""
Módulo centralizado para armazenamento e gestão de prompts do LLM.
"""

# Prompt para a Fase 1: Análise Qualitativa de Value Investing
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

# Podemos adicionar outros prompts aqui no futuro (ex: para a Fase 3)
RAG_ANALYSIS_PROMPT = """
...
"""
