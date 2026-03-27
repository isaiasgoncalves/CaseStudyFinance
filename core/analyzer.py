import json
from typing import Dict, Any, Optional
from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_MODEL, VALUE_INVESTING_ANALYSIS_PROMPT, SYSTEM_PERSONA
from utils.logger import logger

class InvestmentAnalyzer:
    """
    Classe responsável por realizar a síntese de dados fundamentalistas 
    e notícias sob a ótica de Value Investing usando OpenAI.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or DEFAULT_MODEL
        
        if not self.api_key:
            logger.error("API Key da OpenAI não encontrada em core/config.py ou no .env.")
            raise ValueError("OpenAI API Key é necessária.")
            
        self.client = OpenAI(api_key=self.api_key)

    def analyze_ticker(self, ticker: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia os dados coletados para o LLM e gera a análise qualitativa.
        """
        logger.info(f"Iniciando análise qualitativa via LLM para: {ticker}")
        
        prompt = self._build_prompt(ticker, data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PERSONA},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(response.choices[0].message.content)
            logger.info(f"Análise finalizada com sucesso para {ticker}")
            return analysis
            
        except Exception as e:
            logger.error(f"Erro na chamada da API OpenAI para {ticker}: {str(e)}")
            return {"error": f"Não foi possível gerar a análise: {str(e)}"}

    def _build_prompt(self, ticker: str, data: Dict[str, Any]) -> str:
        """Constrói o prompt estruturado usando o template de config.py."""
        
        cadastral = data.get("cadastral", {})
        indicators = data.get("market_indicators", {})
        news = data.get("news", [])
        
        news_titles = "\n- ".join([n.get('title', 'Sem título') for n in news])

        return VALUE_INVESTING_ANALYSIS_PROMPT.format(
            ticker=ticker,
            nome_empresa=cadastral.get('nome', 'N/A'),
            setor=cadastral.get('setor', 'N/A'),
            segmento=cadastral.get('segmento', 'N/A'),
            resumo_negocio=cadastral.get('resumo', 'N/A'),
            p_l=indicators.get('p_l', 'N/A'),
            roe=indicators.get('roe', 'N/A'),
            divida_ebitda=indicators.get('divida_ebitda', 'N/A'),
            margem_liquida=indicators.get('margem_liquida', 'N/A'),
            dy=indicators.get('dy', 'N/A'),
            noticias=news_titles if news_titles else "Nenhuma notícia relevante encontrada."
        )


if __name__ == "__main__":
    # Teste rápido de execução (necessário chave real no .env)
    # analyzer = InvestmentAnalyzer()
    # print(analyzer.analyze_ticker("TESTE", {"cadastral": {"nome": "Exemplo SA"}, "market_indicators": {"p_l": 10}}))
    pass
