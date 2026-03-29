# Guia de Deploy VPS | Hipótese Capital 🏛️

Este documento descreve o processo passo a passo para realizar o deploy do Terminal Analítico na sua VPS utilizando **Docker**, **Docker Compose** e o domínio **hipotesecapital.duckdns.org**.

---

## 1. Preparação da VPS (Ubuntu/Debian)

Acesse sua VPS via SSH e garanta que o sistema esteja atualizado:

```bash
sudo apt update && sudo apt upgrade -y
```

### Instalar Docker e Docker Compose
Caso ainda não tenha o Docker instalado:

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt install docker-compose -y
```

---

## 2. Configuração do Domínio (DuckDNS)

1. Acesse [duckdns.org](https://www.duckdns.org/).
2. Aponte o domínio `hipotesecapital` para o **IP Público** da sua VPS.
3. Certifique-se de que a porta **8501** (Streamlit) está aberta no firewall da sua VPS (ex: UFW ou painel da nuvem):

```bash
sudo ufw allow 8501/tcp
```

---

## 3. Clonagem e Configuração do Projeto

Na sua VPS, clone o repositório e configure as credenciais:

```bash
# Clone o projeto
git clone https://github.com/seu-usuario/CaseStudyFinance.git
cd CaseStudyFinance

# Crie o arquivo de ambiente
nano .env
```

Dentro do `.env`, insira suas chaves:
```env
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-4o-mini
```
*(Pressione `Ctrl+O`, `Enter` e `Ctrl+X` para salvar e sair no nano)*

---

## 4. Deploy com Docker Compose

Construa a imagem e suba o serviço em modo "detatched" (em segundo plano):

```bash
sudo docker-compose up -d --build
```

### Verificação
Para garantir que tudo está rodando:
```bash
sudo docker ps
```
Você deverá ver o container `hipotesse-terminal` ativo na porta `8501`.

---

## 5. Acesso à Aplicação

Agora você pode acessar o terminal através do seu domínio:
`http://hipotesecapital.duckdns.org:8501`

---

## 6. (Opcional) SSL e HTTPS com Nginx Proxy Manager

Para um deploy verdadeiramente profissional (sem o `:8501` no final e com cadeado de segurança), recomenda-se usar um **Reverse Proxy**.

### Passos rápidos:
1. Instale o **Nginx Proxy Manager** via Docker.
2. No painel dele, adicione um **Proxy Host**:
   - Domain Name: `hipotesecapital.duckdns.org`
   - Scheme: `http`
   - Forward IP: `IP_INTERNO_DOCKER` ou `IP_DA_VPS`
   - Forward Port: `8501`
   - Habilite **Websockets Support** (Obrigatório para Streamlit).
3. Solicite o certificado SSL (Let's Encrypt) pelo próprio painel.

---

## 7. Comandos de Manutenção

- **Ver Logs**: `sudo docker-compose logs -f`
- **Parar Aplicação**: `sudo docker-compose down`
- **Atualizar Código**:
  ```bash
  git pull origin main
  sudo docker-compose up -d --build
  ```
- **Backup do Banco**: O arquivo `database.db` estará na raiz da pasta do projeto na VPS devido ao mapeamento de volume no `docker-compose.yml`.

---
**Suporte Técnico**
Caso o Streamlit exiba erro de "CORS", adicione o seguinte ao comando no `Dockerfile`:
`--server.enableCORS=false --server.enableXsrfProtection=false`
