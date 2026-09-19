import os
import streamlit as st
import pandas as st_pd
import pandas as pd
import matplotlib.pyplot as plt
import minhastats

# Configuração da página
st.set_page_config(page_title="Laboratório Estatístico - Redes", layout="wide")
st.title("Análise de Tráfego de Rede utilizando amostras do dataset UNSW-NB15")

@st.cache_data
def carregar_dados():
    # Descobre o caminho absoluto da pasta onde o script está rodando
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Constrói o caminho correto voltando uma pasta e entrando em 'data'
    caminho_arquivo = os.path.join(diretorio_atual, "..", "data", "UNSW_NB15_testing-set.csv")
    
    df = pd.read_csv(caminho_arquivo)
    return df

df = carregar_dados()

st.sidebar.header("Navegação do Laboratório")
modulo = st.sidebar.radio("Selecione a Análise", [
    "Módulo 2: Estatística Descritiva", 
    "Módulo 3: Probabilidade e Simulação",
    "Módulo 4: Distribuições Teóricas",
    "Módulo 5: Correlação e Regressão Linear",
])

if modulo == "Módulo 2: Estatística Descritiva":
    st.sidebar.header("Configurações do Módulo 2")
    variaveis_numericas = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl']
    variaveis_categoricas = ['proto', 'service', 'state', 'attack_cat']
    todas_variaveis = variaveis_numericas + variaveis_categoricas

    variavel_escolhida = st.sidebar.selectbox("Escolha uma variável para análise:", todas_variaveis)
    st.header(f"Estatística Descritiva: `{variavel_escolhida}`")
    
    if variavel_escolhida in variaveis_numericas:
        # Isolamento do núcleo estatístico (Pandas -> Lista Python)
        dados_brutos = df[variavel_escolhida].dropna().tolist()

        # Como o dataset de redes tem muitos dados, para o Streamlit não travar ao plotar, 
        # é necessário pegar uma amostra aleatória caso passe de 50.000 registros, mas os cálculos
        # estatísticos são feitos sobre a lista completa.

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Medidas Calculadas (minhastats)")
            m = minhastats.media(dados_brutos)
            md = minhastats.mediana(dados_brutos)
            mod = minhastats.moda(dados_brutos)
            dp = minhastats.desvio_padrao(dados_brutos)
            amp = minhastats.amplitude(dados_brutos)
            cv = minhastats.coeficiente_variacao(dados_brutos)

            st.write(f"**Média:** {m:.4f}")
            st.write(f"**Mediana:** {md:.4f}")
            st.write(f"**Moda:** {mod:.4f}")
            st.write(f"**Desvio Padrão:** {dp:.4f}")
            st.write(f"**Amplitude:** {amp:.4f}")
            st.write(f"**Coef. Variação:** {cv:.2f}%")

            st.info(f"💡 **Interpretação Automática:** {minhastats.interpretar_assimetria(dados_brutos)}")

        with col2:
            st.subheader("Análise de Outliers (Regra do IQR)")
            inf, sup = minhastats.limites_iqr(dados_brutos)
            outliers = minhastats.detectar_outliers(dados_brutos)
            perc_outliers = (len(outliers) / len(dados_brutos)) * 100

            st.write(f"**Limite Inferior:** {inf:.4f}")
            st.write(f"**Limite Superior:** {sup:.4f}")
            st.write(f"**Total de Outliers:** {len(outliers)} registros ({perc_outliers:.2f}%)")

            if perc_outliers > 5:
                st.warning("⚠️ Alta presença de anomalias (outliers). Comum em dados de ataques de rede.")

        st.subheader("Visualizações")
        # Utiliza matplotlib para construir o histograma (agrupando dados em bins) e o boxplot (mostrando quartis e outliers soltos)
        fig, ax = plt.subplots(1, 2, figsize=(15, 5))

        # Histograma
        ax[0].hist(dados_brutos, bins=30, color='skyblue', edgecolor='black')
        ax[0].axvline(m, color='red', linestyle='dashed', linewidth=2, label='Média')
        ax[0].axvline(md, color='green', linestyle='dashed', linewidth=2, label='Mediana')
        ax[0].set_title("Histograma de Frequências")
        ax[0].legend()

        # Boxplot
        ax[1].boxplot(dados_brutos, vert=False)
        ax[1].set_title("Boxplot (Dispersão e Outliers)")

        st.pyplot(fig)

        st.subheader("Tabela de Frequências (Classes)")
        # Visualização via Pandas
        frequencias = pd.cut(df[variavel_escolhida], bins=10).value_counts().sort_index().reset_index()
        frequencias.columns = ['Intervalo (Classe)', 'Frequência Absoluta']
        frequencias['Frequência Relativa (%)'] = (frequencias['Frequência Absoluta'] / len(dados_brutos)) * 100
        st.dataframe(frequencias, use_container_width=True)

    else:
        # Variáveis Categóricas
        dados_categoricos = df[variavel_escolhida].dropna().tolist()

        st.subheader("Medidas Categóricas")
        mod = minhastats.moda(dados_categoricos)
        st.write(f"**Moda (Classe mais frequente):** {mod}")

        st.subheader("Tabela de Frequências")

        contagem = {}
        for valor in dados_categoricos:
            contagem[valor] = contagem.get(valor, 0) + 1

        df_freq = pd.DataFrame(list(contagem.items()), columns=['Categoria', 'Frequência Absoluta']).sort_values(by='Frequência Absoluta', ascending=False)
        df_freq['Frequência Relativa (%)'] = (df_freq['Frequência Absoluta'] / len(dados_categoricos)) * 100
        st.dataframe(df_freq, use_container_width=True)

        st.subheader("Gráfico de Barras")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df_freq['Categoria'].astype(str), df_freq['Frequência Absoluta'], color='coral')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

elif modulo == "Módulo 3: Probabilidade e Simulação":
    st.header("🎲 Probabilidade e Simulação de Monte Carlo")
    
    st.subheader("1. A Lei dos Grandes Números (LGN)")
    st.write("A simulação de Monte Carlo exige contexto. Em vez de jogar moedas virtuais, vamos simular a inspeção aleatória de pacotes da sua rede (como um IDS/IPS faria). No curto prazo, a quantidade de pacotes de um tipo específico (ex: tráfego TCP ou ataques DoS) flutua caoticamente, mas no longo prazo, a frequência de interceptação converge inexoravelmente para a probabilidade teórica daquele evento no dataset.")
    
    # Escolha da variável e do evento
    variaveis_categoricas = ['proto', 'service', 'state', 'attack_cat']
    var_lgn = st.selectbox("Escolha uma variável categórica para inspecionar:", variaveis_categoricas)
    dados_lgn = df[var_lgn].dropna().tolist()
    
    # Busca categorias únicas
    categorias_unicas = list(set(dados_lgn))
    alvo_lgn = st.selectbox("Escolha o evento (categoria) alvo da interceptação:", categorias_unicas)
    
    # Calcula a probabilidade real (Populacional)
    freq_absoluta_real = sum(1 for x in dados_lgn if x == alvo_lgn)
    prob_teorica = freq_absoluta_real / len(dados_lgn)
    
    n_lancamentos = st.slider("Número de pacotes inspecionados aleatoriamente:", min_value=10, max_value=10000, value=1000, step=100)
    
    with st.spinner('Simulando interceptação de pacotes na rede...'):
        proporcoes = minhastats.simular_frequencia_relativa(dados_lgn, alvo_lgn, n_lancamentos)
    
    # Plotagem
    fig_lgn, ax_lgn = plt.subplots(figsize=(10, 4))
    ax_lgn.plot(range(1, n_lancamentos + 1), proporcoes, color='purple', alpha=0.8, label=f'Frequência Amostral (Simulação)')
    ax_lgn.axhline(prob_teorica, color='red', linestyle='dashed', linewidth=2, label=f'Probabilidade Real ({prob_teorica*100:.2f}%)')
    
    # Define o limite do gráfico dinamicamente com base na probabilidade teórica
    margem = max(0.2, prob_teorica * 1.5)
    ax_lgn.set_ylim(0, min(1.0, prob_teorica + margem))
    
    ax_lgn.set_title(f"Convergência da Frequência de '{alvo_lgn}' ({n_lancamentos} interceptações)")
    ax_lgn.set_xlabel("Nº de Pacotes Inspecionados")
    ax_lgn.set_ylabel("Frequência Relativa")
    ax_lgn.legend()
    st.pyplot(fig_lgn)
    
    st.markdown("---")
    
    st.subheader("2. Teorema Central do Limite (TCL)")
    st.write("O TCL prova que as médias de amostras aleatórias tendem a formar uma distribuição Normal, independentemente do quão distorcida seja a distribuição original dos dados de rede.")
    
    variaveis_numericas = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl']
    var_tcl = st.selectbox("Escolha a variável do tráfego para extrair amostras:", variaveis_numericas)
    
    col1, col2 = st.columns(2)
    with col1:
        tamanho_amostra = st.slider("Tamanho de cada amostra (n):", min_value=5, max_value=200, value=30, step=5)
    with col2:
        n_repeticoes = st.slider("Número de amostras retiradas:", min_value=100, max_value=5000, value=1000, step=100)
        
    dados_brutos = df[var_tcl].dropna().tolist()
    
    with st.spinner('Sorteando amostras e calculando o núcleo estatístico...'):
        medias_amostrais = minhastats.gerar_medias_amostrais(dados_brutos, tamanho_amostra, n_repeticoes)
    
    fig_tcl, ax_tcl = plt.subplots(1, 2, figsize=(15, 5))
    
    # Gráfico 1: Distribuição original
    ax_tcl[0].hist(dados_brutos, bins=40, color='skyblue', edgecolor='black')
    ax_tcl[0].set_title(f"Distribuição Original: {var_tcl}")
    ax_tcl[0].set_ylabel("Frequência")
    
    # Gráfico 2: A ordem emergente (TCL)
    ax_tcl[1].hist(medias_amostrais, bins=40, color='lightgreen', edgecolor='black')
    ax_tcl[1].set_title(f"Distribuição das Médias Amostrais (n={tamanho_amostra})")
    
    st.pyplot(fig_tcl)
    
    # Interpretação matemática para o relatório e apresentação
    media_das_medias = minhastats.media(medias_amostrais)
    media_populacional = minhastats.media(dados_brutos)
    st.info(f"**Análise Matemática:** A média original de todos os pacotes é **{media_populacional:.2f}**. A média das médias das nossas {n_repeticoes} amostras é **{media_das_medias:.2f}**. Mesmo a distribuição original de `{var_tcl}` sendo totalmente caótica, as amostras convergiram para o formato de sino perfeitamente centralizado.")
elif modulo == "Módulo 4: Distribuições Teóricas":
    import numpy as np
    
    st.header("📐 Distribuições Teóricas vs. Dados Reais")
    st.write("Aqui sobrepomos curvas matemáticas teóricas ao histograma real dos dados da rede para verificar se o tráfego segue um modelo matemático conhecido.")
    
    variaveis_numericas = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl']
    var_dist = st.selectbox("Escolha uma variável contínua para modelagem teórica:", variaveis_numericas, index=0)
    
    # 1. Preparação e cálculos com núcleo próprio
    dados_brutos = df[var_dist].dropna().tolist()
    
    # Filtro opcional para remover outliers extremos apenas para visualização
    # Outliers achatam o gráfico e dificultam enxergar a curva
    remover_outliers = st.checkbox("Remover outliers extremos para melhor visualização do ajuste?", value=True)
    if remover_outliers:
        inf, sup = minhastats.limites_iqr(dados_brutos)
        # Filtra os dados mantendo apenas os "inliers"
        dados_plot = [x for x in dados_brutos if inf <= x <= sup]
    else:
        dados_plot = dados_brutos
        
    media_val = minhastats.media(dados_plot)
    dp_val = minhastats.desvio_padrao(dados_plot)
    
    # Parâmetro lambda para a distribuição Exponencial (taxa = 1 / média)
    lambda_val = 1.0 / media_val if media_val > 0 else 0
    
    st.subheader(f"Ajuste Teórico para `{var_dist}`")
    st.write(f"**Parâmetros Estimados:** Média ($\mu$) = {media_val:.4f} | Desvio Padrão ($\sigma$) = {dp_val:.4f} | Taxa ($\lambda$) = {lambda_val:.4f}")
    
    # 2. Construção do Eixo X e das Curvas Teóricas
    x_min, x_max = min(dados_plot), max(dados_plot)
    x_vals = np.linspace(x_min, x_max, 1000)
    
    y_normal = [minhastats.pdf_normal(x, media_val, dp_val) for x in x_vals]
    y_exponencial = [minhastats.pdf_exponencial(x, lambda_val) for x in x_vals]
    
    # 3. Plotagem
    fig_dist, ax_dist = plt.subplots(figsize=(12, 6))
    
    # Histograma (density=True é vital para a área somar 1 e alinhar com a curva de probabilidade)
    ax_dist.hist(dados_plot, bins=50, density=True, alpha=0.5, color='skyblue', edgecolor='black', label='Dados Reais (Histograma)')
    
    # Curvas
    ax_dist.plot(x_vals, y_normal, color='red', linewidth=2.5, linestyle='dashed', label='Distribuição Normal Teórica')
    ax_dist.plot(x_vals, y_exponencial, color='purple', linewidth=2.5, label='Distribuição Exponencial Teórica')
    
    ax_dist.set_title(f"Ajuste de Distribuições - {var_dist}")
    ax_dist.set_xlabel("Valores")
    ax_dist.set_ylabel("Densidade")
    ax_dist.legend()
    
    st.pyplot(fig_dist)
    
    # Discussão automática do ajuste
    st.info("💡 **Discussão do Ajuste:** Repare como as curvas teóricas tentam modelar os blocos do histograma. Variáveis relacionadas a tempo (como `dur` - duração da conexão) geralmente decaem rapidamente, aproximando-se melhor do modelo **Exponencial** (linha roxa). A **Normal** (linha vermelha pontilhada) exige simetria, o que raramente ocorre no tráfego bruto de redes sem transformações logarítmicas.")

elif modulo == "Módulo 5: Correlação e Regressão Linear":
    st.header(
        "Correlação e regressão linear",
        icon=":material/query_stats:",
    )
    st.markdown(
        "Explore a associação linear entre duas características do tráfego "
        "e ajuste uma reta por mínimos quadrados. Os resultados sempre se "
        "referem ao grupo e ao protocolo selecionados."
    )
    st.warning(
        "Correlação e regressão descrevem padrões nos dados, mas não "
        "demonstram causalidade, não calculam a probabilidade de ataque e "
        "não classificam um fluxo como normal ou malicioso.",
        icon=":material/warning:",
    )

    descricoes_m5 = {
        "dur": "Duração do fluxo (s)",
        "spkts": "Pacotes enviados pela origem",
        "dpkts": "Pacotes enviados pelo destino",
        "sbytes": "Bytes enviados pela origem",
        "dbytes": "Bytes enviados pelo destino",
        "rate": "Taxa de pacotes (pacotes/s)",
        "sttl": "TTL dos pacotes de origem",
        "dttl": "TTL dos pacotes de destino",
    }
    variaveis_m5 = list(descricoes_m5)
    variaveis_discretas_m5 = {
        "spkts",
        "dpkts",
        "sbytes",
        "dbytes",
        "sttl",
        "dttl",
    }
    variaveis_ttl_m5 = {"sttl", "dttl"}

    def rotulo_variavel_m5(nome):
        return f"{nome} — {descricoes_m5[nome]}"

    def formatar_inteiro_m5(valor):
        return f"{valor:,}".replace(",", ".")

    st.sidebar.header(
        "Configurações do Módulo 5",
        icon=":material/tune:",
    )

    categorias_ataque_m5 = sorted(
        categoria
        for categoria in df["attack_cat"].dropna().unique()
        if categoria != "Normal"
    )

    grupo_m5 = st.sidebar.selectbox(
        "Grupo de tráfego",
        options=[
            "Todos os registros",
            "Normal",
            "Todos os ataques",
        ]
        + categorias_ataque_m5,
        key="modulo5_grupo",
        help=(
            "As classes são rótulos já fornecidos pelo dataset e servem "
            "para comparar grupos conhecidos."
        ),
    )

    protocolo_m5 = st.sidebar.selectbox(
        "Protocolo",
        options=[
            "Todos os protocolos",
        ]
        + sorted(df["proto"].dropna().unique()),
        key="modulo5_protocolo",
        help=(
            "Restringir o protocolo reduz a mistura de comportamentos "
            "de comunicação diferentes."
        ),
    )

    variavel_x = st.sidebar.selectbox(
        "Variável X — eixo horizontal",
        options=variaveis_m5,
        index=variaveis_m5.index("spkts"),
        format_func=rotulo_variavel_m5,
        key="modulo5_x",
        help="Variável usada pela reta para estimar Y.",
    )

    variavel_y = st.sidebar.selectbox(
        "Variável Y — resposta estimada",
        options=variaveis_m5,
        index=variaveis_m5.index("dpkts"),
        format_func=rotulo_variavel_m5,
        key="modulo5_y",
        help="Variável apresentada no eixo vertical e estimada pela reta.",
    )

    if variavel_x == variavel_y:
        st.warning(
            "Escolha variáveis diferentes para X e Y.",
            icon=":material/info:",
        )
        st.stop()

    if grupo_m5 == "Todos os registros":
        dados_recorte_m5 = df
    elif grupo_m5 == "Todos os ataques":
        dados_recorte_m5 = df.loc[df["label"] == 1]
    else:
        dados_recorte_m5 = df.loc[df["attack_cat"] == grupo_m5]

    if protocolo_m5 != "Todos os protocolos":
        dados_recorte_m5 = dados_recorte_m5.loc[
            dados_recorte_m5["proto"] == protocolo_m5
        ]

    # X e Y são selecionados juntos para preservar o pareamento por registro.
    dados_pares = dados_recorte_m5[
        [variavel_x, variavel_y]
    ].copy()

    # Somente valores ausentes ou infinitos são removidos.
    # Zeros e valores extremos finitos são preservados.
    dados_pares = dados_pares.replace(
        [float("inf"), float("-inf")],
        float("nan"),
    ).dropna(subset=[variavel_x, variavel_y])

    total_registros = len(df)
    total_recorte = len(dados_recorte_m5)
    total_pares = len(dados_pares)
    total_excluidos = total_recorte - total_pares

    with st.container(border=True):
        st.subheader(
            "Escopo da análise",
            icon=":material/filter_alt:",
        )

        with st.container(horizontal=True):
            st.metric(
                "Registros no arquivo",
                formatar_inteiro_m5(total_registros),
                border=True,
            )
            st.metric(
                "Registros no recorte",
                formatar_inteiro_m5(total_recorte),
                border=True,
            )
            st.metric(
                "Pares válidos",
                formatar_inteiro_m5(total_pares),
                border=True,
            )
            st.metric(
                "Pares excluídos",
                formatar_inteiro_m5(total_excluidos),
                border=True,
                help="Valores ausentes ou infinitos em X ou Y.",
            )

        st.markdown(
            f"**Recorte atual:** {grupo_m5} · {protocolo_m5}  \n"
            f"**Pergunta analisada:** como **{variavel_x}** e "
            f"**{variavel_y}** variam linearmente em conjunto?"
        )
        st.caption(
            "Os filtros alteram a população analisada. Comparações entre "
            "grupos devem manter o mesmo par X–Y e, preferencialmente, "
            "o mesmo protocolo."
        )

        if grupo_m5 != "Todos os registros":
            st.info(
                "O grupo foi definido por um rótulo já conhecido no dataset. "
                "Este recorte permite comparação descritiva, mas não simula "
                "a classificação de um tráfego novo.",
                icon=":material/label:",
            )

        if protocolo_m5 == "Todos os protocolos":
            st.caption(
                "O recorte mistura protocolos. Parte do resultado pode "
                "refletir diferenças entre protocolos, além da relação "
                "entre X e Y."
            )

        if total_excluidos > 0:
            st.warning(
                f"{formatar_inteiro_m5(total_excluidos)} registros foram "
                "excluídos porque X ou Y continha valor ausente ou infinito.",
                icon=":material/data_alert:",
            )

    if total_pares < 2:
        st.warning(
            "Este recorte possui menos de dois pares válidos. Selecione "
            "outro grupo, protocolo ou par de variáveis.",
            icon=":material/info:",
        )
        st.stop()

    dados_x = dados_pares[variavel_x].tolist()
    dados_y = dados_pares[variavel_y].tolist()

    x_minimo = min(dados_x)
    x_maximo = max(dados_x)
    x_constante = all(valor == dados_x[0] for valor in dados_x)
    y_constante = all(valor == dados_y[0] for valor in dados_y)

    inclinacao = None
    intercepto = None
    r_pearson = None
    r_quadrado = None
    y_estimado = []
    x_reta = []
    y_reta = []

    if x_constante:
        st.warning(
            "X é constante neste recorte. Não existe uma inclinação única "
            "para a regressão, e Pearson também é indefinido. O diagrama "
            "de dispersão permanece disponível.",
            icon=":material/info:",
        )
    else:
        try:
            # Todos os resultados estatísticos vêm da biblioteca própria.
            inclinacao, intercepto = minhastats.regressao_linear(
                dados_x,
                dados_y,
            )
            y_estimado = [
                minhastats.predicao_linear(
                    x,
                    inclinacao,
                    intercepto,
                )
                for x in dados_x
            ]

            if not y_constante:
                r_pearson = minhastats.correlacao_pearson(
                    dados_x,
                    dados_y,
                )
                r_quadrado = minhastats.coeficiente_determinacao(
                    dados_y,
                    y_estimado,
                )

            # A reta é desenhada entre os extremos de X, mas o ajuste usa
            # todos os pares válidos.
            x_reta = [x_minimo, x_maximo]
            y_reta = [
                minhastats.predicao_linear(
                    x,
                    inclinacao,
                    intercepto,
                )
                for x in x_reta
            ]
        except (ValueError, ArithmeticError) as erro:
            st.error(
                f"Não foi possível calcular o ajuste: {erro}",
                icon=":material/error:",
            )
            st.stop()

    if inclinacao is not None:
        st.subheader(
            "Resultados do ajuste",
            icon=":material/analytics:",
        )

        with st.container(horizontal=True):
            st.metric(
                "Pearson (r)",
                (
                    "Indefinido"
                    if r_pearson is None
                    else f"{r_pearson:.6f}"
                ),
                border=True,
            )
            st.metric(
                "R² no recorte",
                (
                    "Indefinido"
                    if r_quadrado is None
                    else f"{r_quadrado:.6f}"
                ),
                border=True,
            )
            st.metric(
                "Inclinação (b)",
                f"{inclinacao:.6g}",
                border=True,
            )
            st.metric(
                "Intercepto (a)",
                f"{intercepto:.6g}",
                border=True,
            )

        with st.container(border=True):
            sinal = "+" if inclinacao >= 0 else "−"

            st.markdown(
                f"**Equação ajustada:** Ŷ = {intercepto:.8g} "
                f"{sinal} {abs(inclinacao):.8g} × X"
            )
            st.caption(
                f"X representa {variavel_x}; Y representa {variavel_y}. "
                "O arredondamento ocorre somente na apresentação."
            )

            if y_constante:
                st.warning(
                    "Y é constante neste recorte. A reta horizontal pode "
                    "ser calculada, mas Pearson e R² são indefinidos porque "
                    "não existe variação em Y.",
                    icon=":material/info:",
                )
            else:
                if r_pearson > 0:
                    direcao = "positiva"
                elif r_pearson < 0:
                    direcao = "negativa"
                else:
                    direcao = "nula"

                st.markdown(
                    f"**Pearson:** a associação linear é **{direcao}** "
                    "neste recorte. O coeficiente informa direção e "
                    "intensidade linear; valores próximos de zero não "
                    "descartam relações não lineares ou subgrupos distintos."
                )
                st.markdown(
                    f"**R²:** a reta representa aproximadamente "
                    f"**{100 * r_quadrado:.2f}%** da variação observada "
                    f"de {variavel_y} em torno de sua média, nos mesmos "
                    "dados usados no ajuste. Isso não é uma porcentagem "
                    "de previsões corretas."
                )

            st.markdown(
                f"**Inclinação:** ao percorrer a reta, um aumento de uma "
                f"unidade em {variavel_x} altera Ŷ em "
                f"{inclinacao:.6g} unidades de {variavel_y}. "
                "Esse coeficiente descreve o ajuste e não um efeito causal."
            )
            st.markdown(
                f"**Intercepto:** quando X = 0, a reta retorna "
                f"{intercepto:.6g} para {variavel_y}."
            )

            if not x_minimo <= 0 <= x_maximo:
                st.caption(
                    "X = 0 está fora da faixa observada neste recorte. "
                    "Nesse caso, o intercepto é necessário para definir "
                    "a reta, mas sua interpretação prática envolve "
                    "extrapolação."
                )

            estimativas_negativas = sum(
                valor < 0
                for valor in y_estimado
            )
            if min(dados_y) >= 0 and estimativas_negativas > 0:
                percentual_negativas = (
                    100 * estimativas_negativas / total_pares
                )
                st.warning(
                    f"A reta gera {formatar_inteiro_m5(estimativas_negativas)} "
                    f"estimativas negativas ({percentual_negativas:.2f}% "
                    "dos pares), embora Y seja uma variável não negativa. "
                    "Esse resultado é matematicamente possível, mas indica "
                    "limitação prática do modelo linear.",
                    icon=":material/warning:",
                )

    with st.container(border=True):
        st.subheader(
            "Diagrama de dispersão e reta ajustada",
            icon=":material/scatter_plot:",
        )

        fig_m5, ax_m5 = plt.subplots(figsize=(10, 5.5))
        ax_m5.scatter(
            dados_x,
            dados_y,
            s=10,
            alpha=0.25,
            color="steelblue",
            linewidths=0,
            rasterized=True,
            label="Registros observados",
        )

        if inclinacao is not None:
            ax_m5.plot(
                x_reta,
                y_reta,
                color="darkorange",
                linewidth=2,
                label="Regressão por mínimos quadrados",
            )

        ax_m5.set_xlabel(rotulo_variavel_m5(variavel_x))
        ax_m5.set_ylabel(rotulo_variavel_m5(variavel_y))
        ax_m5.set_title(
            f"{variavel_y} em função de {variavel_x} "
            f"— {grupo_m5} · {protocolo_m5}"
        )
        ax_m5.grid(alpha=0.2)
        ax_m5.legend()
        fig_m5.tight_layout()

        st.pyplot(fig_m5, width="stretch")
        plt.close(fig_m5)

        st.caption(
            "O gráfico utiliza todos os pares válidos do recorte, em "
            "escala linear, mantendo zeros e valores extremos finitos. "
            "A reta é exibida entre o menor e o maior X observado."
        )

    with st.container(border=True):
        st.subheader(
            "Como interpretar sem produzir falsos diagnósticos",
            icon=":material/fact_check:",
        )
        st.markdown(
            f"**O que está sendo avaliado:** a associação linear entre "
            f"{variavel_x} e {variavel_y} nos "
            f"{formatar_inteiro_m5(total_pares)} pares do recorte atual."
        )
        st.markdown(
            "**O que o resultado pode fornecer:** direção da associação "
            "linear, uma reta descritiva, comparação entre recortes "
            "equivalentes e uma estimativa numérica de Y."
        )
        st.markdown(
            "**O que o resultado não fornece:** causa do comportamento, "
            "significância estatística, probabilidade de ataque, classe "
            "de um novo fluxo ou garantia de desempenho fora destes dados."
        )
        st.markdown(
            "**Como comparar filtros:** mantenha X e Y fixos e altere um "
            "filtro por vez. Uma mudança nos coeficientes pode decorrer "
            "do grupo, do protocolo, do tamanho do recorte, dos zeros ou "
            "dos valores extremos."
        )

        if r_quadrado is not None:
            st.caption(
                "R² e Pearson resumem aspectos específicos da relação. "
                "Mesmo valores elevados precisam ser avaliados junto ao "
                "diagrama de dispersão e, em uma próxima etapa, aos resíduos."
            )

    with st.container(border=True):
        st.subheader(
            "Predição interativa de Y",
            icon=":material/calculate:",
        )
        st.caption(
            "A predição consulta a reta do recorte atual. Ela estima "
            "somente Y; não calcula risco, probabilidade ou classe de ataque."
        )

        if inclinacao is None:
            st.info(
                "A predição requer uma reta ajustada. Escolha uma variável "
                "X que apresente variação no recorte.",
                icon=":material/info:",
            )
        else:
            st.caption(
                f"X: {descricoes_m5[variavel_x]}. "
                f"Faixa observada: {x_minimo:.10g} a {x_maximo:.10g}."
            )

            # A chave separa entradas pertencentes a modelos diferentes.
            x_informado = st.number_input(
                f"Informe X — {variavel_x}",
                value=None,
                step=(
                    1.0
                    if variavel_x in variaveis_discretas_m5
                    else 0.1
                ),
                format="%.10g",
                placeholder="Digite um valor para calcular Ŷ",
                key=(
                    f"modulo5_predicao_{variavel_x}_{variavel_y}_"
                    f"{grupo_m5}_{protocolo_m5}"
                ),
                help=(
                    "Confirme com Enter ou saia do campo. Valores fora "
                    "da faixa observada serão identificados como extrapolação."
                ),
            )

            if x_informado is None:
                st.info(
                    "Informe um valor de X para consultar a reta.",
                    icon=":material/info:",
                )
            elif x_informado < 0:
                st.error(
                    f"{variavel_x} não admite valor negativo neste módulo.",
                    icon=":material/error:",
                )
            elif (
                variavel_x in variaveis_discretas_m5
                and not float(x_informado).is_integer()
            ):
                st.error(
                    f"{variavel_x} representa uma quantidade inteira. "
                    "Informe um valor sem parte fracionária.",
                    icon=":material/error:",
                )
            elif (
                variavel_x in variaveis_ttl_m5
                and x_informado > 255
            ):
                st.error(
                    "TTL deve estar entre 0 e 255.",
                    icon=":material/error:",
                )
            else:
                try:
                    y_previsto = minhastats.predicao_linear(
                        x_informado,
                        inclinacao,
                        intercepto,
                    )
                except (ValueError, ArithmeticError) as erro:
                    st.error(
                        f"Não foi possível calcular a predição: {erro}",
                        icon=":material/error:",
                    )
                else:
                    st.metric(
                        f"Ŷ estimado — {variavel_y}",
                        f"{y_previsto:.10g}",
                        help=descricoes_m5[variavel_y],
                        border=True,
                    )
                    st.caption(
                        f"Para {variavel_x} = {x_informado:.10g}, "
                        f"a reta estima {variavel_y} = {y_previsto:.10g}."
                    )

                    if (
                        x_informado < x_minimo
                        or x_informado > x_maximo
                    ):
                        st.warning(
                            "Extrapolação: X está fora da faixa observada "
                            "neste recorte. A relação estimada pode não se "
                            "manter nessa região.",
                            icon=":material/warning:",
                        )
                    else:
                        st.caption(
                            "X está dentro da faixa observada, mas isso "
                            "não garante que a estimativa seja adequada "
                            "para um registro individual."
                        )

                    if y_previsto < 0:
                        st.warning(
                            "A reta retornou um valor negativo para uma "
                            "variável não negativa. Preserve o resultado "
                            "matemático, mas não o interprete como uma "
                            "quantidade fisicamente observável.",
                            icon=":material/warning:",
                        )
                    elif (
                        variavel_y in variaveis_ttl_m5
                        and y_previsto > 255
                    ):
                        st.warning(
                            "A estimativa ultrapassa 255, limite do campo "
                            "TTL. Isso indica inadequação prática da reta "
                            "para esse valor de X.",
                            icon=":material/warning:",
                        )

                    if variavel_y in variaveis_discretas_m5:
                        st.caption(
                            "A regressão é contínua e pode produzir Ŷ "
                            "fracionário mesmo quando Y é uma contagem "
                            "ou outro campo inteiro."
                        )

                    if grupo_m5 != "Todos os registros":
                        st.caption(
                            "A estimativa está condicionada a uma classe "
                            "já conhecida. Ela não descobre a classe do fluxo."
                        )

                    st.caption(
                        "Ŷ é uma estimativa pontual, sem intervalo de "
                        "predição. Não representa uma observação real nem "
                        "uma garantia de resultado futuro."
                    )

    with st.expander(
        "Perguntas recomendadas para explorar os dados",
        icon=":material/lightbulb:",
    ):
        st.markdown(
            "- **spkts × dpkts:** compare a relação entre pacotes nas duas "
            "direções, mantendo o mesmo protocolo nos grupos Normal e "
            "Todos os ataques.\n"
            "- **spkts × sbytes:** observe a relação estrutural entre "
            "quantidade de pacotes e bytes e verifique a influência dos "
            "valores extremos.\n"
            "- **sbytes × dbytes:** compare os volumes nas duas direções "
            "e veja se a relação muda conforme o protocolo.\n"
            "- **dur × rate:** use com cautela, porque a taxa é derivada "
            "de contagens e duração; associação não significa independência.\n"
            "- **sttl e dttl:** poucos valores distintos podem tornar "
            "gráficos de frequência mais informativos que uma reta."
        )

    with st.expander(
        "Conferência dos pares utilizados",
        icon=":material/table_view:",
    ):
        st.caption(
            "A tabela mostra somente os dez primeiros pares válidos. "
            "Todos os pares informados no escopo participam dos cálculos."
        )
        st.dataframe(
            dados_pares.head(10),
            hide_index=True,
            width="stretch",
        )