# Sistematização de Matemática e Estatística para a Computação

## 📊 Sobre o Projeto

Sistema acadêmico desenvolvido para aplicar conceitos fundamentais de Matemática e Estatística à análise de dados reais de tráfego de rede utilizados em cyber-segurança.

O projeto utiliza o dataset público **UNSW-NB15**, amplamente empregado em pesquisas de detecção de intrusões, para demonstrar visualmente e matematicamente conceitos estatísticos estudados durante a disciplina de Matemática e Estatística para Computação do curso de Análise e Desenvolvimento de Sistemas do CEUB.

A aplicação foi construída em Python e disponibiliza recursos para análise estatística, visualização de distribuições, demonstrações probabilísticas e validação matemática através de uma biblioteca própria desenvolvida pela equipe.

---

## 🎯 Objetivo

Proporcionar um ambiente interativo para estudo e aplicação prática de conceitos estatísticos através da análise de tráfego de rede real.

O sistema busca conectar teoria e prática por meio de:

* Estatística Descritiva
* Probabilidade
* Lei dos Grandes Números
* Teorema Central do Limite
* Correlação de Pearson
* Regressão Linear
* Coeficiente de Determinação (R²)
* Detecção de Outliers
* Análise de Distribuições

---

## 👥 Participantes do Projeto

* Iago Batista Gomes de Carvalho - 72650448 
* Marcos Paulo Dos Santos Júnior - 72650390
* Caio Sacramento Côrtes - 72650430

---

## 📂 Dataset Utilizado

### UNSW-NB15

Dataset público desenvolvido pelo Australian Centre for Cyber Security (ACCS).

Contém milhões de registros de tráfego de rede simulando atividades legítimas e ataques cibernéticos.

Link:

https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15

### Principais Variáveis

| Variável   | Descrição                      |
| ---------- | ------------------------------ |
| dur        | Duração da conexão             |
| spkts      | Pacotes enviados pela origem   |
| dpkts      | Pacotes enviados pelo destino  |
| sbytes     | Bytes enviados pela origem     |
| dbytes     | Bytes enviados pelo destino    |
| rate       | Taxa de transferência          |
| sttl       | Time To Live da origem         |
| dttl       | Time To Live do destino        |
| attack_cat | Categoria do ataque            |
| label      | Classificação normal ou ataque |

---

## 🚀 Funcionalidades

### Estatística Descritiva

* Média
* Mediana
* Moda
* Amplitude
* Variância Populacional
* Variância Amostral
* Desvio Padrão Populacional
* Desvio Padrão Amostral
* Coeficiente de Variação

### Probabilidade e Distribuições

* Percentis
* Quartis
* IQR (Intervalo Interquartílico)
* Detecção automática de outliers
* Interpretação de assimetria

### Estatística Inferencial

* Covariância
* Correlação de Pearson
* Regressão Linear Simples
* Predição Linear
* Coeficiente de Determinação (R²)

### Demonstrações Acadêmicas

#### Lei dos Grandes Números (LGN)

Permite visualizar a convergência da frequência relativa de eventos conforme o número de observações aumenta.

Exemplos:

* Frequência de ataques DoS
* Frequência de tráfego normal
* Frequência de categorias específicas de ataques

#### Teorema Central do Limite (TCL)

Demonstra como distribuições amostrais das médias convergem para uma distribuição normal conforme o tamanho das amostras aumenta.

Aplicado sobre:

* duração das conexões
* quantidade de pacotes
* taxas de transferência
* tamanho dos pacotes

---

## 🛠 Tecnologias Utilizadas

### Linguagem

* Python 3.14+

### Interface

* Streamlit

### Computação Científica

* NumPy
* SciPy
* Pandas

### Visualização

* Matplotlib
* Altair

### Testes

* PyTest

---

## 📁 Estrutura do Projeto

```text
ceub-mec-sistematizacao/
│
├── src/
│   ├── app.py
│   ├── minhastats.py
│   ├── test_minhastats.py
│   └── __init__.py
│
├── requirements.txt
├── pytest.ini
├── README.md
└── RELATORIO.md
```

### Arquivos Principais

#### app.py

Interface principal da aplicação utilizando Streamlit.

Responsável por:

* carregamento dos dados
* renderização dos gráficos
* interação com o usuário
* execução dos módulos estatísticos

#### minhastats.py

Biblioteca estatística desenvolvida pela equipe.

Implementa algoritmos próprios para:

* estatística descritiva
* probabilidade
* regressão linear
* correlação
* análise de distribuições

#### test_minhastats.py

Suíte completa de validação matemática comparando os resultados obtidos pela biblioteca própria com:

* NumPy
* SciPy
* statistics (biblioteca padrão do Python)

---

## 🔄 Fluxo da Aplicação

1. Inicialização da aplicação Streamlit
2. Carregamento do dataset UNSW-NB15
3. Seleção do módulo estatístico
4. Processamento dos dados
5. Geração dos gráficos
6. Exibição dos resultados
7. Interpretação estatística dos resultados

---

## 📊 Módulos Acadêmicos

### Módulo 1

Fundamentos de Estatística Descritiva.

### Módulo 2

Análise exploratória dos dados.

### Módulo 3

#### Lei dos Grandes Números

Demonstra a convergência das frequências relativas.

#### Teorema Central do Limite

Demonstra a convergência das distribuições amostrais para a distribuição normal.

### Módulo 4

Análises estatísticas avançadas e inferência.

---

## 🧪 Testes Executados

Durante a validação deste projeto foram executados todos os testes automatizados disponíveis no repositório.

### Resultado

```text
75 passed in 1.23s
```

### Taxa de Sucesso

* Testes executados: 75
* Testes aprovados: 75
* Falhas: 0
* Erros: 0

### Funcionalidades Validadas

#### Estatística Descritiva

* Média
* Mediana
* Moda
* Variância
* Desvio padrão
* Coeficiente de variação
* Percentis

#### Associação entre Variáveis

* Covariância
* Correlação de Pearson

#### Modelagem Estatística

* Regressão Linear
* Predição Linear
* Coeficiente de Determinação (R²)

#### Casos de Borda

Validação de:

* listas vazias
* valores infinitos
* valores NaN
* variáveis constantes
* tamanhos incompatíveis
* resultados numericamente inválidos

#### Comparação Científica

Os resultados da biblioteca própria foram comparados com:

* NumPy
* SciPy
* statistics

Todos os resultados apresentaram concordância dentro das tolerâncias definidas nos testes.

---

## 📈 Qualidade Técnica Observada

### Pontos Fortes

* Implementação própria dos algoritmos estatísticos.
* Excelente documentação interna (docstrings).
* Tratamento robusto de erros.
* Cobertura abrangente de testes.
* Comparação dos cálculos com bibliotecas científicas reconhecidas.
* Código modularizado.
* Boa separação entre interface e lógica estatística.
* Uso de validações matemáticas rigorosas.

### Destaques

O módulo de regressão linear apresenta:

* validação de entradas
* proteção contra NaN e infinito
* prevenção de divisão por zero
* preservação da precisão numérica
* testes comparativos com SciPy

O módulo de correlação de Pearson valida corretamente cenários onde a correlação é matematicamente indefinida.

O cálculo de R² contempla inclusive casos onde o modelo é pior que utilizar simplesmente a média dos dados.

---

## 🎮 Como Executar

### Execução via Docker (Recomendado)

A aplicação foi empacotada em um contêiner Linux leve configurado com *multi-stage build* e permissões *rootless* para garantir segurança e isolamento total de dependências.

#### Pré-requisitos
* **Linux / macOS:** Docker Engine instalado.
* **Windows:** Instale o [Docker Desktop](https://www.docker.com/products/docker-desktop/). Durante a instalação, mantenha a opção **"Use WSL 2 instead of Hyper-V"** ativada. O WSL 2 utiliza um kernel Linux real, garantindo máxima performance e compatibilidade com o contêiner.

#### Opção 1: Executar a imagem pré-construída (Mais rápido)
Basta executar o comando abaixo no seu terminal (ou PowerShell no Windows) para baixar e rodar a imagem diretamente do Docker Hub:

```bash
docker run -d --name mec-stats -p 8501:8501 iagobgc/ceub-mec-sistematizacao:0.1.0
```

#### Opção 2: Construir a imagem localmente
Caso queira modificar o código e compilar a sua própria imagem a partir do repositório clonado:

1. **Construa a imagem:**
   ```bash
   docker build -t ceub-mec-sistematizacao:0.1.0 .
   ```

2. **Inicie o contêiner em segundo plano:**
   ```bash
   docker run -d --name mec-stats -p 8501:8501 ceub-mec-sistematizacao:0.1.0
   ```

#### Acessando a Aplicação
Independente da opção escolhida, após iniciar o contêiner, abra o seu navegador e acesse:
👉 **http://localhost:8501**

#### Comandos Úteis do Docker
* Para visualizar os logs de execução da análise estatística em tempo real:
  `docker logs -f mec-stats`
* Para parar o laboratório:
  `docker stop mec-stats`
* Para reiniciar o laboratório:
  `docker start mec-stats`
* Para remover o contêiner do seu sistema:
  `docker rm -f mec-stats`

### Execução via instalação local

#### Pré-requisitos

* Python 3.14 ou superior

#### Clonar Repositório

```bash
git clone https://github.com/IagoBGCarvalho/ceub-mec-sistematizacao.git
```

#### Entrar no Diretório

```bash
cd ceub-mec-sistematizacao
```

#### Criar Ambiente Virtual

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### Instalar Dependências

```bash
pip install -r requirements.txt
```

#### Executar Aplicação

```bash
streamlit run src/app.py
```

ou

```bash
python -m streamlit run src/app.py
```

---

## 🔍 Casos de Uso

* Ensino de Estatística Aplicada
* Ensino de Probabilidade
* Demonstração da Lei dos Grandes Números
* Demonstração do Teorema Central do Limite
* Introdução à Ciência de Dados
* Introdução à Cibersegurança
* Aprendizado de Regressão Linear
* Aprendizado de Correlação Estatística
* Estudos sobre tráfego de rede
* Validação de algoritmos estatísticos

---

## 📄 Licença

Consultar o repositório para informações de licenciamento.

---

## 👨‍💻 Desenvolvimento

Projeto desenvolvido para a disciplina de Matemática e Estatística para Computação do Centro Universitário de Brasília (CEUB).

Participantes:

* Iago Batista Gomes de Carvalho - 72650448 
* Marcos Paulo dos Santos Júnior - 72650390 
* Caio Sacramento Côrtes - 72650430