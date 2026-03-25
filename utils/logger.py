import logging
import sys
from pathlib import Path

def setup_logger(name: str = "case_finance") -> logging.Logger:
    """
    Configura um logger centralizado para o projeto com saída para console e arquivo.
    
    Args:
        name (str): Nome do logger.
        
    Returns:
        logging.Logger: Instância configurada do logger.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Formato da mensagem
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para Console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler para Arquivo
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "app.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

# Instância padrão para uso rápido
logger = setup_logger()
