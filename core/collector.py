import yfinance as yf
import pandas as pd
from curl_cffi import requests as requests_cffi
from typing import Dict, Optional, Any
from datetime import datetime, timezone, timedelta
from dateutil import parser as date_parser
from config import NEWS_LIMIT, DEFAULT_HISTORY_PERIOD, NEWS_MAX_AGE_DAYS
from utils.logger import logger

class DataCollector:
    """
    Classe responsável por coletar dados de mercado, indicadores fundamentalistas 
    e informações cadastrais de empresas da B3 via Yahoo Finance.
    """
    
    def __init__(self, ticker: str):
        # Garante que o ticker termine com .SA para B3
        self.ticker_symbol = ticker.upper() if ticker.upper().endswith(".SA") else f"{ticker.upper()}.SA"
        
        # Cria uma sessão do curl_cffi mimetizando um navegador Chrome real
        session = requests_cffi.Session(impersonate="chrome", verify=False)
        
        self.ticker = yf.Ticker(self.ticker_symbol, session=session)

    def _is_recent(self, date_str: str) -> bool:
        """
        Verifica se uma data (em string) está dentro do limite configurado.
        Suporta múltiplos formatos (ISO, RFC 822, etc) via dateutil.
        """
        if not date_str:
            return True # Se não tem data, mantemos por precaução
            
        try:
            publish_date = date_parser.parse(date_str)
            
            # Garante que a data seja 'aware' (com timezone) para comparar com o agora
            if publish_date.tzinfo is None:
                publish_date = publish_date.replace(tzinfo=timezone.utc)
            
            now = datetime.now(timezone.utc)
            limit = now - timedelta(days=NEWS_MAX_AGE_DAYS)
            
            return publish_date >= limit
        except Exception as e:
            logger.warning(f"Erro ao parsear data '{date_str}': {e}")
            return True

    def collect_all_data(self) -> Dict[str, Any]:
        """
        Executa a coleta completa: Cadastral, Mercado e Notícias.
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
                "news": self._get_recent_news(limit=NEWS_LIMIT)
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
            "divida_ebitda": info.get("debtToEbitda"),
            "margem_liquida": info.get("profitMargins"),
            "dy": info.get("dividendYield")
        }

    def _get_recent_news(self, limit: int = NEWS_LIMIT) -> list:
        """
        Coleta notícias recentes filtrando por data de publicação.
        """
        news = []

        # 1. Tenta Google News RSS primeiro
        try:
            clean_ticker = self.ticker_symbol.replace(".SA", "")
            url = f"https://news.google.com/rss/search?q={clean_ticker}+B3&hl=pt-BR&gl=BR&ceid=BR:pt-419"
            response = requests_cffi.get(url, impersonate="chrome", verify=False, timeout=10)

            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, features="xml")
                items = soup.find_all("item")

                for item in items:
                    pub_date_str = item.pubDate.text if item.pubDate else None

                    if not self._is_recent(pub_date_str):
                        continue

                    title = item.title.text if item.title else None
                    if title:
                        if not any(title[:30] in n["title"] for n in news):
                            news.append({
                                "title": str(title),
                                "link": item.link.text if item.link else "#",
                                "publisher": item.source.text if item.source else "Google News"
                            })
                    if len(news) >= limit: break
        except Exception as e:
            logger.error(f"Fallback Google News falhou: {e}")


        # 2. Fallback Yahoo Finance
        if len(news) < limit:
            try:
                yf_news = self.ticker.news
                if yf_news:
                    for n in yf_news:
                        content = n.get("content", n)
                        pub_date_str = content.get("pubDate") or n.get("providerPublishTime")

                        # Se vier como timestamp (inteiro), convertemos para string ISO para o parser
                        if isinstance(pub_date_str, int):
                            pub_date_str = datetime.fromtimestamp(pub_date_str, tz=timezone.utc).isoformat()

                        if not self._is_recent(pub_date_str):
                            continue

                        title = content.get("title") or content.get("headline")
                        link = content.get("canonicalUrl", {}).get("url") or n.get("link", "#")
                        publisher = content.get("provider", {}).get("displayName") or n.get("publisher",
                                                                                            "Yahoo Finance")

                        if title:
                            news.append({"title": str(title), "link": link, "publisher": publisher})
                        if len(news) >= limit: break
            except Exception as e:
                logger.warning(f"Yahoo News falhou: {e}")


        return news[:limit]

    def get_history(self, period: str = DEFAULT_HISTORY_PERIOD) -> pd.DataFrame:
        """Coleta o histórico de preços."""
        logger.info(f"Coletando histórico de {period} para {self.ticker_symbol}")
        return self.ticker.history(period=period)

if __name__ == "__main__":
    ticker_test = "ITUB4"
    collector = DataCollector(ticker_test)
    result = collector.collect_all_data()
    print(result)
