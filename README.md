# Sistematização de Matemática e Estatística para a Computação

Iago Batista Gomes de Carvalho - 72650448

Repositório referente ao desenvolvimento do projeto de Sistematização da matéria de Matemática e Estatística para Computação do curso de Análise e Desenvolvimento de Sistemas do CEUB.

Consiste em um núcleo estatístico que extrai e processa informações de um dataset público de tráfego de rede criado para detectar intrusões cibernéticas (UNSW-NB15). 

Link do dataset: https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15

As variáveis representam os metadados dos pacotes TCP/UDP, sendo elas:

*dur*: Duração total da conexão
*spkts/dpkts*: Quantidade de pacotes enviados pela origem (source) e destino (destination)
*rate*: Taxa de pacotes por segundo.
*sttl*: Time To Live do pacote de origem.
*attack_cat*: Se a conexão foi um ataque (DoS, Reconnaissance, etc) e indica a categoria.

## Como usar

### Método clássico

- Clone o repositório na sua máquina
- Garanta que o Python 3.14+ esteja instalado utilizando "python --version"
- Ative o amviente virtual (venv) utilizando o comando "source venv/bin/activate" (para desativar, basta digitar deactivate)
- Instale as bibliotecas necessárias para o funcionamento do software dentro do ambiente virtual utilizando o requirements.txt como: "pip install -r requirements.txt"
- Rode a aplicação com "python3 -m streamlit run src/app.py"

### Método conteinerizado (recomendado)

Em breve...

## Módulos

### Módulo 0

### Módulo 1

### Módulo 2

### Módulo 3

#### A Lei dos Grandes Números (LGN) 

Reflete o comportamento de convergência probabilística do próprio tráfego de rede. Pacotes aleatórios do dataset são amostrados a partir de uma determinada variável categórica e é feita uma verificação de frequência relativa de um evento relacionado à variável categórica.

Por exemplo, a variável attack_cat possui eventos (categorias), como Normal (maioria do tráfego limpo), DoS, Worms, Exploits, etc.

Quando o valor do número de pacotes inspecionados é baixo, a variância representada pela linha roxa fica caótica, saltando brutalmente, refletindo a variância e a incerteza no curto prazo. Mas quando o valor é alto, a linha roxa achata e gruda na linha vermelha, evidenciando a solidez probabilística da Lei dos Grandes Números.

#### O Teorema Central do Limite (TCL)

Prova que, ao extrair amostras repetidas de uma população e calcular a média de cada amostra, a distribuição dessas médias tenderá sempre a forma uma curva Normal (formato de sino), independentemente do quão distorcida ou caótica seja a distribuição original dos dados.

No contexto do laboratório é aplicado ao inspecionar as variávis numéricas do tráfego de rede (como dur, sbytes ou rate). O gráfico da esquerda mostra a distribuição original do dataset. Já o gráfico da direita funciona sorteando aleatoriamente um número n de pacotes, calcula a média deles, guarda o resultado e repete este processo milhares de vezes. Conforme o tamanho da amostra é aumentado, o gráfico sofre achatamentos e se ergue no centro, formando a curva Normal.

### Módulo 4

