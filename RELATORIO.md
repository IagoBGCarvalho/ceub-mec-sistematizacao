# Relatório da sistematização de Matemática e Estatística para a Computação
# Módulo 6
## 🔬 As 3 Descobertas Estatísticas Mais Interessantes do Laboratório

Após a análise do dataset **UNSW-NB15**, contendo **175.341 registros de tráfego de rede**, foram identificados três padrões estatísticos que se destacaram tanto pela relevância matemática quanto pela importância para aplicações em cyber-segurança.

---

# 1. O Dataset é Fortemente Dominado por Tráfego Malicioso

## Resultado Encontrado

Distribuição das classes:

| Classe | Quantidade | Percentual |
| ------ | ---------: | ---------: |
| Ataque |    119.341 |     68,06% |
| Normal |     56.000 |     31,94% |

Total de registros:

**175.341 conexões**

## O Que Isso Significa

A primeira descoberta relevante foi perceber que o conjunto de dados não possui uma distribuição equilibrada entre tráfego legítimo e tráfego malicioso.

Em termos probabilísticos:

* A chance de selecionar aleatoriamente um ataque é de aproximadamente **68%**.
* A chance de selecionar uma conexão normal é de aproximadamente **32%**.

Isso significa que existe mais que o dobro de registros maliciosos em comparação aos registros legítimos.

## Importância Estatística

Esse comportamento foi visualizado claramente nas distribuições de frequência geradas pelo laboratório.

Além disso, o experimento da **Lei dos Grandes Números** mostrou que, conforme o tamanho da amostra aumenta, a frequência observada de ataques converge para aproximadamente 68%, validando empiricamente um dos principais teoremas estudados na disciplina.

## Relevância para Cyber-segurança

Essa predominância evidencia que o UNSW-NB15 foi construído especificamente para pesquisas de detecção de intrusão e análise de ameaças.

Consequentemente:

* eventos maliciosos tornam-se estatisticamente representativos;
* análises de probabilidade tornam-se mais robustas;
* algoritmos de classificação conseguem aprender melhor os padrões de ataque.

---

# 2. O Campo TTL (sttl) Apresenta Forte Associação com Ataques

## Resultado Encontrado

Foi calculada a correlação entre as variáveis numéricas e a variável de classificação (**label**).

As maiores correlações observadas foram:

| Variável     | Correlação Absoluta com Label |
| ------------ | ----------------------------: |
| sttl         |                         0,693 |
| ct_state_ttl |                         0,578 |
| dload        |                         0,394 |
| rate         |                         0,338 |

## O Que Isso Significa

A variável **sttl (Source Time To Live)** apresentou correlação de aproximadamente **0,693** com a classificação das conexões.

Na prática, isso representa uma associação estatística forte.

Quanto maior a correlação, maior a capacidade da variável em diferenciar comportamentos normais e maliciosos.

## Importância Estatística

Entre dezenas de atributos analisados, o TTL destacou-se como um dos indicadores mais informativos do conjunto.

Isso sugere que existe uma diferença consistente no comportamento dos pacotes quando comparados:

* tráfego legítimo;
* tráfego malicioso.

## Relevância para Cyber-segurança

O resultado é especialmente importante porque TTL é uma informação:

* simples de coletar;
* disponível em praticamente todo pacote IP;
* barata computacionalmente;
* utilizável em sistemas de monitoramento em tempo real.

Em outras palavras, um único campo do cabeçalho de rede demonstrou possuir alto poder discriminatório para identificação de ataques.

---

# 3. O Dataset Possui Variáveis Quase Redundantes

## Resultado Encontrado

A matriz de correlação revelou pares de variáveis com correlação extremamente elevada.

Os principais casos observados foram:

| Variáveis                 | Correlação |
| ------------------------- | ---------: |
| is_ftp_login × ct_ftp_cmd |      1,000 |
| dbytes × dloss            |      0,997 |
| sbytes × sloss            |      0,996 |
| swin × dwin               |      0,990 |
| ct_srv_src × ct_srv_dst   |      0,980 |

## O Que Isso Significa

Correlação próxima de 1 indica que duas variáveis apresentam comportamento praticamente idêntico.

No caso de:

**is_ftp_login × ct_ftp_cmd**

a correlação foi praticamente perfeita.

Isso significa que ambas carregam quase a mesma informação estatística.

## Importância Estatística

Essa descoberta evidencia um fenômeno conhecido como **multicolinearidade**.

Multicolinearidade ocorre quando várias variáveis descrevem o mesmo comportamento do sistema.

As consequências incluem:

* aumento da redundância dos dados;
* modelos mais complexos sem ganho de informação;
* maior consumo computacional;
* dificuldade de interpretação dos resultados.

## Relevância para Ciência de Dados

Essa descoberta demonstra que nem toda variável adiciona conhecimento novo ao modelo.

Antes da construção de algoritmos de Machine Learning, variáveis altamente correlacionadas normalmente são:

* removidas;
* agrupadas;
* transformadas.

Essa etapa reduz ruído e melhora a eficiência dos modelos.

---

# Conclusão

As análises realizadas revelaram três características fundamentais do UNSW-NB15:

1. O conjunto possui forte predominância de tráfego malicioso (68,06% dos registros).
2. O atributo TTL (sttl) é um dos indicadores mais relevantes para distinguir ataques de conexões normais.
3. Existem grupos de variáveis com correlação quase perfeita, evidenciando redundância estrutural nos dados.

Essas descobertas demonstram como ferramentas estatísticas permitem identificar padrões ocultos em grandes volumes de dados e mostram, na prática, a aplicação de conceitos de Probabilidade, Correlação, Estatística Descritiva e Inferência Estatística no contexto de cyber-segurança.
# Descobertas Estatísticas com Referência aos Gráficos
# 1. O Dataset é Fortemente Dominado por Tráfego Malicioso

[...]

## Evidência Visual

Essa característica pode ser observada no **Gráfico 1 – Distribuição das Classes do Dataset**, gerado pela aplicação.

**Gráfico 1 – Distribuição de Conexões Normais e Ataques**

O gráfico evidencia visualmente a predominância de registros classificados como ataque em relação às conexões normais, demonstrando um desbalanceamento significativo entre as classes.

A diferença observada entre as barras confirma os resultados obtidos na análise estatística, onde aproximadamente 68,06% dos registros pertencem à classe de ataque.

Além disso, no experimento da Lei dos Grandes Números, representado pelo **Gráfico 2 – Convergência da Frequência Relativa dos Ataques**, observa-se que a proporção de ataques tende a estabilizar em torno de 68% à medida que o número de observações aumenta, validando empiricamente a teoria probabilística estudada.

---

# 2. O Campo TTL (sttl) Apresenta Forte Associação com Ataques

[...]

## Evidência Visual

A relação entre a variável **sttl** e a classificação das conexões pode ser observada no **Gráfico 3 – Correlação dos Atributos com a Variável Label**.

**Gráfico 3 – Correlação Absoluta dos Principais Atributos com Label**

Nesse gráfico, a variável **sttl** apresenta uma das maiores magnitudes de correlação entre todos os atributos analisados.

Visualmente, sua barra destaca-se em relação às demais variáveis, indicando forte capacidade de diferenciação entre tráfego legítimo e tráfego malicioso.

O resultado é consistente com o coeficiente de correlação calculado pelo laboratório (≈ 0,693), classificando essa associação como forte para dados reais de rede.

---

# 3. O Dataset Possui Variáveis Quase Redundantes

[...]

## Evidência Visual

A existência de relações extremamente fortes entre determinadas variáveis pode ser observada na **Matriz de Correlação** produzida pela aplicação.

**Gráfico 4 – Heatmap da Matriz de Correlação**

No heatmap, os pares:

* is_ftp_login × ct_ftp_cmd
* dbytes × dloss
* sbytes × sloss
* swin × dwin
* ct_srv_src × ct_srv_dst

aparecem com intensidade máxima de correlação, indicando dependência estatística quase perfeita.

As regiões mais escuras (ou mais claras, dependendo da paleta utilizada) concentram-se justamente nesses pares de atributos, evidenciando visualmente a presença de multicolinearidade.

Essa observação gráfica reforça os coeficientes calculados numericamente, alguns deles superiores a 0,99, revelando que certas variáveis carregam praticamente a mesma informação.

---

## Referência dos Gráficos Utilizados

**Gráfico 1.** Distribuição das Classes do Dataset (Normal × Ataque)

**Gráfico 2.** Demonstração da Lei dos Grandes Números para Frequência de Ataques

**Gráfico 3.** Correlação dos Principais Atributos com a Variável Label

**Gráfico 4.** Heatmap da Matriz de Correlação das Variáveis Numéricas

Todos os gráficos foram gerados pela própria aplicação desenvolvida para o laboratório, utilizando os dados do dataset UNSW-NB15 e os algoritmos estatísticos implementados na biblioteca `minhastats.py`.