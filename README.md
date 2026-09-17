# Sistematização de Matemática e Estatística para a Computação

Iago Batista Gomes de Carvalho - 72650448

Repositório referente ao desenvolvimento do projeto de Sistematização da matéria de Matemática e Estatística para Computação do curso de Análise e Desenvolvimento de Sistemas do CEUB.

Consiste em um núcleo estatístico que extrai e processa informações de um dataset público de tráfego de rede criado para detectar intrusões cibernéticas (UNSW-NB15). As variáveis representam os metadados dos pacotes TCP/UDP, sendo elas:

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

