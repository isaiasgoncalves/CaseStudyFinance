# Notas de Desenvolvimento - Case Hipótese Capital

## Fase 1: Coleta e Síntese (Refinada)

### Refinamentos Técnicos:
1. **Coleta de Notícias:**
   - Detectada mudança estrutural no `yfinance` (versão 1.2.0 local). Notícias agora vêm aninhadas em `content`.
   - Adicionado suporte a `n.get("content", n)` para retrocompatibilidade.
   - Fallback de Google News RSS ativado com sucesso após instalação de `lxml` e ajuste de parser para `xml`.

2. **Reestruturação de Código (Clean Architecture):**
   - **ui/**: Pacote isolado para interface.
     - `styles.py`: Injeção de CSS customizado.
     - `sidebar.py`: Controle de inputs e logo.
     - `components.py`: Funções de renderização de métricas e análise.
   - **config.py**: Movido para a raiz. Contém todas as constantes de branding, cores, fontes, modelos de IA e o prompt de Value Investing.

3. **Branding & UI:**
   - Tema Escuro implementado usando a paleta oficial da Hipótese Capital (Deep Red, Dark Silver, Light Beige).
   - Uso de `Playfair Display` para títulos e `Source Sans Pro` para corpo de texto.
   - **Bug Conhecido:** Injeção de CSS global no Streamlit às vezes afeta as ligaturas dos ícones nativos (Material Icons), exibindo o nome do ícone em texto. Tentativa de isolamento via seletores `[data-testid="stIcon"]` e `font-family: inherit`.

### Próximos Passos (Fase 2):
- Implementar camada de persistência com SQLite.
- Criar `core/database.py` e definir schema (Empresa vs. Snapshot de Indicadores).
- Adaptar o pipeline para verificar se os dados do dia já existem no banco antes de realizar nova chamada de API (Cache/Persistência).
