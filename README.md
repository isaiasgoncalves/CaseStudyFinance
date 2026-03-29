# Hipótese Capital | Terminal de Inteligência Analítica 🏛️

Este repositório contém o Terminal Analítico desenvolvido para a **Hipótese Capital**, uma gestora de investimentos focada em *Value Investing*. O sistema automatiza a coleta de indicadores fundamentalistas, notícias de mercado e gera sínteses qualitativas de alto nível utilizando IA (GPT-4o).

---

## 🚀 Funcionalidades Principais

### 1. Coleta & Filtragem Inteligente
- **Multi-fontes**: Coleta automatizada via Yahoo Finance e fallback resiliente via Google News.
- **Filtro Temporal**: Notícias são filtradas para garantir relevância (últimos 90 dias).
- **Indicadores Chave**: Extração de P/L, ROE, Dividend Yield, Margem Líquida e Dívida/EBITDA.

### 2. Memória Histórica ("Máquina do Tempo")
- **Persistência em SQLite**: Cada consulta é salva em um banco de dados local com versionamento automático (Migrations).
- **Navegação Histórica**: Visualize capturas feitas em datas passadas instantaneamente, sem custos de API ou rede.
- **Gráficos de Tendência**: Evolução temporal de múltiplos indicadores com eixos escalonados.

### 3. Inteligência Qualitativa (IA)
- **Síntese de Valor**: Resumo do modelo de negócio e análise crítica de downside.
- **Clima de Notícias**: Classificação estruturada de sentimento (Positivo/Negativo/Neutro).
- **Checklist RI**: Geração automática de perguntas investigativas para suporte à devida diligência.

---

## 🛠️ Stack Tecnológica

- **Linguagem**: Python 3.13+
- **Interface**: Streamlit
- **Banco de Dados**: SQLite3 (com suporte a Foreign Keys e Migrations)
- **IA**: OpenAI GPT-4o-mini
- **Coleta de Dados**: yfinance, curl_cffi (anti-bot), python-dateutil
- **Testes**: Pytest (com Mocking de rede e banco em memória)

---

## 📦 Como Instalar e Rodar

### 1. Requisitos Prévios
Certifique-se de ter o Python instalado. Recomenda-se o uso de um ambiente virtual.

### 2. Configuração do Ambiente
Clone o repositório e instale as dependências:
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/CaseStudyFinance.git
cd CaseStudyFinance

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Instale os pacotes
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto seguindo o modelo `.envexample`:
```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
```

### 4. Execução Manual
Para iniciar o terminal analítico localmente:
```bash
streamlit run src/app.py
```

---

## 🐳 Execução via Docker (Recomendado para Deploy)

Para rodar a aplicação em um container isolado (ideal para VPS ou servidores de produção):

### 1. Pré-requisitos
Certifique-se de ter o **Docker** e o **Docker Compose** instalados na máquina.

### 2. Subir o Container
Na raiz do projeto, execute:
```bash
docker-compose up -d --build
```

### 3. Acessibilidade & Persistência
- A aplicação estará disponível em `http://localhost:8501`.
- O banco de dados `database.db` está mapeado como um volume na raiz do projeto, garantindo que seu histórico seja preservado mesmo após reinicializações do container.

---

### 5. Execução de Testes
Para garantir a integridade do sistema:
```bash
python -m pytest tests/
```

---

## 📂 Estrutura do Projeto (SRC Layout)

```text
CaseStudyFinance/
├── src/
│   ├── app.py              # Ponto de entrada da aplicação
│   ├── core/               # Lógica de negócio (Collector, Analyzer, Database, Orchestrator)
│   ├── ui/                 # Design System e Componentes Visuais
│   ├── utils/              # Loggers e auxiliares
│   └── config.py           # Configurações centralizadas e Prompts
├── tests/                  # Suite de testes unitários
├── migrations/             # Scripts de evolução do banco de dados
├── branding/               # Identidade visual (Logos e ícones)
├── pytest.ini              # Configuração do path de testes
└── requirements.txt        # Dependências do projeto
```

---

## 🏛️ Sobre a Hipótese Capital
A Hipótese Capital administra um fundo de ações concentrado de R$ 1,2 bilhão. Este terminal foi construído para suportar um time de análise de seis pessoas, visando reduzir o tempo gasto em tarefas repetitivas de coleta e aumentar a profundidade analítica através de sínteses inteligentes.

---
**Desenvolvido por Isaías Gouvêa Gonçalves**
*Fase 2 - Versão 2.0.0 (Estável)*
