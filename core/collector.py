import yfinance as yf
import pandas as pd
from curl_cffi import requests as requests_cffi
from typing import Dict, Optional, Any
from utils.logger import logger

class DataCollector:
    """
    Classe responsável por coletar dados de mercado, indicadores fundamentalistas 
    e informações cadastrais de empresas da B3 via Yahoo Finance.
    """
    
    def __init__(self, ticker: str):
        # Garante que o ticker termine com .SA para B3
        self.ticker_symbol = ticker.upper() if ticker.upper().endswith(".SA") else f"{ticker.upper()}.SA"
        
        # Cria uma sessão do curl_cffi (exigida pelas versões novas do yfinance)
        # verify=False contorna o erro de path com caracteres especiais (curl 77)
        session = requests_cffi.Session(verify=False)
        
        self.ticker = yf.Ticker(self.ticker_symbol, session=session)

    def collect_all_data(self) -> Dict[str, Any]:
        """
        Executa a coleta completa: Cadastral, Mercado e Notícias.
        
        Returns:
            Dict: Dicionário contendo todas as informações coletadas.
        """
        logger.info(f"Iniciando coleta de dados para: {self.ticker_symbol}")
        
        try:
            info = self.ticker.info
            
            if not info or 'symbol' not in info:
                logger.error(f"Ticker {self.ticker_symbol} não encontrado ou sem dados.")
                return {}

            data = {
                "cadastral": self._get_cadastral_data(info),
                "market_indicators": self._get_market_indicators(info),
                "news": self._get_recent_news()
            }
            
            logger.info(f"Coleta finalizada com sucesso para {self.ticker_symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados de {self.ticker_symbol}: {str(e)}")
            return {}

    def _get_cadastral_data(self, info: Dict) -> Dict[str, str]:
        """Extrai dados de perfil da empresa."""
        return {
            "nome": info.get("longName", "N/A"),
            "setor": info.get("sector", "N/A"),
            "segmento": info.get("industry", "N/A"),
            "resumo": info.get("longBusinessSummary", "N/A")
        }

    def _get_market_indicators(self, info: Dict) -> Dict[str, Optional[float]]:
        """Extrai indicadores fundamentalistas."""
        return {
            "preco_atual": info.get("currentPrice"),
            "p_l": info.get("trailingPE"),
            "roe": info.get("returnOnEquity"),
            "divida_ebitda": info.get("debtToEbitda"), # Nem sempre disponível no yfinance para BR
            "margem_liquida": info.get("profitMargins"),
            "dy": info.get("dividendYield")
        }

    def _get_recent_news(self, limit: int = 5) -> list:
        """Coleta notícias recentes vinculadas ao ticker."""
        news = self.ticker.news
        return news[:limit] if news else []

if __name__ == "__main__":
    # Teste rápido de execução
    ticker_test = "ITUB4" # Testando com Itaú
    collector = DataCollector(ticker_test)
    result = collector.collect_all_data()
    
    import json
    print("\n--- RESULTADO DA COLETA ---")
    print(json.dumps(result, indent=4, ensure_ascii=False))
