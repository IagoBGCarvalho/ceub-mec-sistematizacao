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
    # Carrega o dataset. Ajuste o nome do arquivo conforme o que você baixou.
    df = pd.read_csv("../data/UNSW_NB15_testing-set.csv")
    return df

df = carregar_dados()

st.sidebar.header("Configurações do Módulo 2")
# Seleciona apenas algumas variáveis relevantes para facilitar a navegação
variaveis_numericas = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl']
variaveis_categoricas = ['proto', 'service', 'state', 'attack_cat']
todas_variaveis = variaveis_numericas + variaveis_categoricas

variavel_escolhida = st.sidebar.selectbox("Escolha uma variável para análise:", todas_variaveis)

st.header(f"Estatística Descritiva: `{variavel_escolhida}`")

if variavel_escolhida in variaveis_numericas:
    # 1. Isolamento do núcleo estatístico (Pandas -> Lista Python)
    dados_brutos = df[variavel_escolhida].dropna().tolist()
    
    # Como o dataset de redes tem muitos dados, para o Streamlit não travar ao plotar, 
    # podemos pegar uma amostra aleatória caso passe de 50.000 registros, mas os cálculos
    # estatísticos serão feitos sobre a lista completa.
    
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
    # Utilizamos matplotlib para construir o histograma (agrupando dados em bins) e o boxplot (mostrando quartis e outliers soltos)[cite: 1]
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
    # Para dados contínuos, a tabela de frequências exige a criação de intervalos (bins).
    # Aqui, a visualização via Pandas é permitida pela regra para formatar a tabela.
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
    # Construindo a contagem na unha para validar a estatística
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