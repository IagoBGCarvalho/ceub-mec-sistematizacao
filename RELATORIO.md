# Relatório da sistematização de Matemática e Estatística para a Computação
# Módulo 6

## 🔬 As 3 Descobertas Estatísticas Mais Relevantes do Laboratório

Após a aplicação dos conceitos de Estatística Descritiva, Probabilidade, Correlação e Análise de Dados sobre o dataset UNSW-NB15, foram identificados três padrões estatísticos que se destacaram tanto pela relevância matemática quanto pela importância para aplicações em cyber-segurança.

O conjunto analisado contém 175.341 registros de tráfego de rede, incluindo conexões legítimas e diferentes categorias de ataques cibernéticos. A análise foi realizada utilizando os algoritmos implementados na biblioteca `minhastats.py` e os recursos de visualização desenvolvidos na aplicação.

---

# 1. Predominância de Tráfego Malicioso no Dataset

## Resultado Obtido

| Classe | Quantidade | Percentual |
| ------ | ---------: | ---------: |
| Ataque |    119.341 |     68,06% |
| Normal |     56.000 |     31,94% |

Total de registros analisados: **175.341 conexões**.

## Análise

A primeira descoberta relevante foi a identificação de um forte desbalanceamento entre as classes do dataset.

Os registros classificados como ataques representam aproximadamente 68% do conjunto de dados, enquanto as conexões normais representam apenas 32%.

Sob a perspectiva probabilística, isso significa que uma observação selecionada aleatoriamente possui mais que o dobro de chance de representar uma atividade maliciosa do que uma conexão legítima.

Durante os experimentos envolvendo a Lei dos Grandes Números, observou-se que a frequência relativa de ataques tende a convergir para aproximadamente 68% conforme o tamanho da amostra aumenta.

Esse comportamento demonstra, na prática, um dos principais conceitos estudados na disciplina: quanto maior a quantidade de observações, mais a frequência observada se aproxima da probabilidade real do fenômeno.

## Importância

Essa descoberta evidencia que o dataset UNSW-NB15 foi construído com forte foco em pesquisas de detecção de intrusão, permitindo que eventos maliciosos sejam suficientemente representativos para análises estatísticas, experimentos probabilísticos e aplicações de aprendizado de máquina.

---

# 2. O Campo TTL (sttl) Apresentou a Associação Estatística Mais Forte com Ataques

## Resultado Obtido

Para a análise de correlação, a variável de classificação (`label`) foi codificada numericamente, atribuindo:

* 0 para conexões normais;
* 1 para conexões classificadas como ataque.

As maiores correlações observadas foram:

| Variável     | Correlação com Label |
| ------------ | -------------------: |
| sttl         |                0,693 |
| ct_state_ttl |                0,578 |
| dload        |                0,394 |
| rate         |                0,338 |

## Análise

Entre todos os atributos analisados, o campo **sttl (Source Time To Live)** apresentou a maior correlação individual com a classificação das conexões.

O coeficiente de correlação obtido foi aproximadamente 0,693, indicando uma associação forte entre o valor de TTL e a probabilidade de uma conexão ser classificada como ataque.

Em termos estatísticos, esse resultado sugere que o comportamento do TTL difere significativamente entre tráfego legítimo e tráfego malicioso.

A análise indica que esse atributo possui elevado potencial discriminatório, tornando-se um dos indicadores mais informativos observados durante o laboratório.

## Importância

Esse resultado é particularmente relevante porque TTL é uma informação presente em praticamente todos os pacotes IP e pode ser coletada com baixo custo computacional.

Consequentemente, trata-se de uma característica potencialmente útil para sistemas de monitoramento de rede, análise de tráfego e mecanismos de detecção de intrusão em tempo real.

---

# 3. Existência de Multicolinearidade Entre Variáveis da Rede

## Resultado Obtido

A matriz de correlação revelou pares de variáveis com associação extremamente elevada.

Os principais casos observados foram:

| Variáveis                 | Correlação |
| ------------------------- | ---------: |
| is_ftp_login × ct_ftp_cmd |      1,000 |
| dbytes × dloss            |      0,997 |
| sbytes × sloss            |      0,996 |
| swin × dwin               |      0,990 |
| ct_srv_src × ct_srv_dst   |      0,980 |

## Análise

A terceira descoberta importante foi a identificação de pares de variáveis com correlação próxima de 1.

Correlação tão elevada indica que determinadas variáveis apresentam comportamento praticamente idêntico ao longo do conjunto de dados.

O caso mais evidente ocorreu entre `is_ftp_login` e `ct_ftp_cmd`, cuja correlação atingiu valor praticamente perfeito.

Esse comportamento caracteriza um fenômeno conhecido como **multicolinearidade**, situação em que diferentes variáveis carregam informações muito semelhantes sobre o sistema analisado.

## Importância

A presença de multicolinearidade possui impacto direto em projetos de Ciência de Dados e Aprendizado de Máquina.

Quando múltiplas variáveis representam praticamente o mesmo comportamento, podem ocorrer:

* aumento da redundância dos dados;
* modelos mais complexos sem ganho de informação;
* maior consumo computacional;
* dificuldade na interpretação dos resultados.

Por esse motivo, análises de correlação são frequentemente utilizadas como etapa preliminar para seleção de atributos e redução de dimensionalidade.

---

# Validação dos Resultados

Todos os algoritmos estatísticos utilizados durante o laboratório foram submetidos a uma suíte automatizada de testes.

Os cálculos implementados na biblioteca `minhastats.py` foram comparados com bibliotecas científicas amplamente utilizadas na comunidade acadêmica, incluindo NumPy e SciPy.

Resultado da validação:

* 75 testes executados;
* 75 testes aprovados;
* 0 falhas;
* 0 erros.

Os testes validaram funcionalidades relacionadas a:

* correlação de Pearson;
* regressão linear;
* coeficiente de determinação (R²);
* estatística descritiva;
* tratamento de valores inválidos;
* casos de borda e situações matematicamente indefinidas.

---

# Conclusão

As análises realizadas demonstraram que técnicas estatísticas permitem identificar padrões relevantes em grandes volumes de dados de rede.

Os resultados obtidos evidenciaram três características fundamentais do dataset UNSW-NB15:

1. Predominância significativa de tráfego malicioso, representando aproximadamente 68% das observações.
2. Elevada associação entre o atributo TTL (sttl) e a classificação das conexões, tornando-o um dos indicadores mais informativos do conjunto.
3. Existência de grupos de variáveis altamente correlacionadas, revelando a presença de multicolinearidade e redundância estrutural nos dados.

Essas descobertas demonstram a aplicação prática dos conceitos estudados ao longo da disciplina, conectando Estatística Descritiva, Probabilidade, Correlação e Inferência Estatística a problemas reais de análise de dados e cyber-segurança.