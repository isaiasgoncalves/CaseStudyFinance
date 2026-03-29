# Estágio Único: Aplicação Python
FROM python:3.13-slim

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para compilação de alguns pacotes python
RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar a aplicação
# Nota: Usamos 0.0.0.0 para que o Streamlit aceite conexões externas no container
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
