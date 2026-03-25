import pytest
from unittest.mock import MagicMock, patch
from core.collector import DataCollector

@pytest.fixture
def mock_yf_ticker():
    """Fixture que simula o objeto Ticker do yfinance com dados mockados."""
    with patch("yfinance.Ticker") as mock_ticker:
        # Criamos uma instância mockada
        instance = mock_ticker.return_value
        
        # Simulamos o atributo .info
        instance.info = {
            "symbol": "ITUB4.SA",
            "longName": "Itaú Unibanco Holding S.A.",
            "sector": "Financial Services",
            "industry": "Banks - Regional",
            "longBusinessSummary": "Itaú Unibanco Holding S.A. provides various banking products and services.",
            "currentPrice": 32.50,
            "trailingPE": 8.5,
            "returnOnEquity": 0.18,
            "debtToEbitda": 2.1,
            "profitMargins": 0.15,
            "dividendYield": 0.04
        }
        
        # Simulamos o atributo .news
        instance.news = [
            {"title": "Itaú anuncia dividendos", "link": "http://itau.com/news1", "publisher": "InfoMoney"},
            {"title": "Análise do setor bancário", "link": "http://itau.com/news2", "publisher": "Valor"}
        ]
        
        yield instance

def test_collect_all_data_success(mock_yf_ticker):
    """Testa se a coleta de dados processa corretamente os dados mockados."""
    collector = DataCollector("ITUB4")
    
    # Injetamos o mock no coletor para evitar chamadas reais à rede
    with patch("yfinance.Ticker", return_value=mock_yf_ticker):
        data = collector.collect_all_data()
        
    assert data["cadastral"]["nome"] == "Itaú Unibanco Holding S.A."
    assert data["market_indicators"]["preco_atual"] == 32.50
    assert len(data["news"]) == 2
    assert data["cadastral"]["setor"] == "Financial Services"

def test_collect_all_data_invalid_ticker():
    """Testa o comportamento do coletor com um ticker inválido (simulando erro)."""
    with patch("yfinance.Ticker") as mock_ticker:
        instance = mock_ticker.return_value
        instance.info = {} # Simula ticker não encontrado
        
        collector = DataCollector("INVALID")
        data = collector.collect_all_data()
        
        assert data == {} # Deve retornar dicionário vazio conforme nossa implementação
