# Anotações

> Este espaço será usado por mim _(Isaías)_ para escrever algumas anotações referentes
> ao processo de elaboração do projeto, servindo como relatório

### Etapas iniciais do projeto

De início estou definindo as stacks a serem utilizadas nas Fases 1 e 2 (mais conexas entre si), e estou configurando
o agente de IA para me auxiliar na elaboração do projeto.

De fato, não tenho muitos conhecimentos sobre análise de dados no Mercado Financeiro, então vejo aqui uma grande oportunidade
para aprender e colocar esses conhecimentos em prática

### Fase 1

Aqui vamos utilizar sobretudo a biblioteca `yfinance` para fazer a coleta dos dados desejado para cada empresa.
Antes de tudo, configuramos o ambiente com o arquivo `requirements.txt` e inserimos a base do que vai ser nosso sistema
de _logging_. 

Criamos o módulo `core` com o script `collector.py` onde são declaradas as classes para coleta de dados a partir dos tickers
desejados. Aproveitamos para criar o diretório `tests` com os primeiros testes unitários em `test_collector.py`

O próximo passo agora é criar os recursos de IA para interpretação dos dados e criação de relatórios subjetivos. Utilizamos
os modelos ChatGPT da OpenAI para fazer a análise, e configuramos um arquivo para deixar os prompts, sabendo que podem ser
aprimorados para obter uma análise ainda mais precisa e útil considerando o contexto do projeto

Temos agora um dashboard elaborado com o streamlit, capaz de mostrar várias informações úteis sobre o Tiker, coletadas via
API e sintetizadas com um LLM. 

As etapas finais da Fase 1 consistem em corrigir alguns bugs e tornar o código mais robusto para a fase 2.





