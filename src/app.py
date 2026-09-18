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
    "Módulo 4: Distribuições Teóricas"
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