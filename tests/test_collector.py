import pytest
from typing import Any, Dict
from core.collector import DataCollector

# Dados de exemplo para reutilização nos testes
MOCK_ITUB_INFO = {
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

MOCK_ITUB_NEWS = [
    {"title": "Itaú anuncia dividendos", "link": "http://itau.com/news1", "publisher": "InfoMoney"},
    {"title": "Análise do setor bancário", "link": "http://itau.com/news2", "publisher": "Valor"}
]

@pytest.fixture
def mock_ticker(mocker: Any) -> Any:
    """Fixture que intercepta a criação do yfinance.Ticker e retorna um mock."""
    return mocker.patch("yfinance.Ticker")

def test_collect_all_data_success(mock_ticker: Any) -> None:
    """
    Testa o fluxo de sucesso da coleta de dados.
    """
    # Configuramos o comportamento do mock ANTES de criar o coletor
    instance = mock_ticker.return_value
    instance.info = MOCK_ITUB_INFO
    instance.news = MOCK_ITUB_NEWS
    
    # Agora criamos o coletor; ele usará o mock automaticamente
    collector = DataCollector("ITUB4")
    data = collector.collect_all_data()
    
    # Asserções
    assert data["cadastral"]["nome"] == "Itaú Unibanco Holding S.A."
    assert data["market_indicators"]["preco_atual"] == 32.50
    assert data["market_indicators"]["p_l"] == 8.5
    assert len(data["news"]) == 2

def test_collect_all_data_partial_info(mock_ticker: Any) -> None:
    """
    Testa a resiliência do coletor quando a API retorna dados parciais.
    """
    instance = mock_ticker.return_value
    instance.info = {
        "symbol": "ITUB4.SA",
        "longName": "Itaú Unibanco Holding S.A.",
        "currentPrice": 32.50
    }
    instance.news = []
    
    collector = DataCollector("ITUB4")
    data = collector.collect_all_data()
    
    # Verifica se os campos ausentes foram tratados como None ou N/A
    assert data["market_indicators"].get("dy") is None
    assert data["cadastral"]["setor"] == "N/A"

def test_collect_all_data_not_found(mock_ticker: Any) -> None:
    """
    Testa o comportamento quando o ticker não existe ou a API não retorna nada.
    """
    instance = mock_ticker.return_value
    instance.info = {} # Simula retorno vazio da API
    
    collector = DataCollector("INVALIDO")
    data = collector.collect_all_data()
    
    assert data == {}
