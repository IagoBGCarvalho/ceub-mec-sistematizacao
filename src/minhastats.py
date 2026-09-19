import math
import random

def media(dados):
    """
    Calcula a média aritmética simples.
    Fórmula: (Σ x_i) / n
    """
    if not dados:
        raise ValueError("A lista de dados não pode estar vazia.")
    return sum(dados) / len(dados)

def mediana(dados):
    """
    Encontra o valor central dos dados ordenados.
    """
    if not dados:
        raise ValueError("A lista de dados não pode estar vazia.")
    ordenados = sorted(dados)
    n = len(ordenados)
    meio = n // 2
    
    if n % 2 == 0:
        return (ordenados[meio - 1] + ordenados[meio]) / 2.0
    return ordenados[meio]

def moda(dados):
    """
    Retorna o valor mais frequente. Em caso de múltiplas modas, retorna a primeira encontrada.
    """
    if not dados:
        raise ValueError("A lista de dados não pode estar vazia.")
    contagem = {}
    for valor in dados:
        contagem[valor] = contagem.get(valor, 0) + 1
    
    maior_frequencia = max(contagem.values())
    modas = [k for k, v in contagem.items() if v == maior_frequencia]
    return modas[0]

def amplitude(dados):
    """
    Calcula a diferença entre o maior e o menor valor.
    """
    if not dados:
        raise ValueError("A lista de dados não pode estar vazia.")
    return max(dados) - min(dados)

def variancia(dados, amostral=True):
    """
    Calcula a variância. 
    Se amostral=True (padrão), divide por (n-1). Se False, divide por n.
    Fórmula (Amostral): Σ (x_i - x̄)² / (n - 1)
    """
    n = len(dados)
    if n < 2 and amostral:
        raise ValueError("A variância amostral requer pelo menos 2 dados.")
    
    m = media(dados)
    soma_quadrados = sum((x - m) ** 2 for x in dados)
    divisor = n - 1 if amostral else n
    
    return soma_quadrados / divisor

def desvio_padrao(dados, amostral=True):
    """
    Calcula o desvio padrão (raiz quadrada da variância).
    """
    return math.sqrt(variancia(dados, amostral))

def coeficiente_variacao(dados, amostral=True):
    """
    Calcula o coeficiente de variação em porcentagem.
    Fórmula: (Desvio Padrão / Média) * 100
    """
    m = media(dados)
    if m == 0:
        raise ValueError("Média é zero, impossível calcular o CV.")
    dp = desvio_padrao(dados, amostral)
    return (dp / m) * 100

def percentil(dados, p):
    """
    Calcula o percentil 'p' (0 a 100) usando interpolação linear.
    """
    if not dados:
        raise ValueError("A lista de dados não pode estar vazia.")
    if not 0 <= p <= 100:
        raise ValueError("O percentil deve estar entre 0 e 100.")
        
    ordenados = sorted(dados)
    n = len(ordenados)
    
    # Índice real 
    k = (n - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    
    if f == c:
        return ordenados[int(k)]
        
    # Interpolação linear
    d0 = ordenados[f] * (c - k)
    d1 = ordenados[c] * (k - f)
    return d0 + d1

def covariancia(x, y, amostral=True):
    """
    Calcula a covariância entre duas listas de variáveis numéricas.
    Fórmula (Amostral): Σ ((x_i - x̄) * (y_i - ȳ)) / (n - 1)
    """
    if len(x) != len(y):
        raise ValueError("As listas X e Y devem ter o mesmo tamanho.")
    n = len(x)
    if n < 2 and amostral:
        raise ValueError("A covariância amostral requer pelo menos 2 pares de dados.")
        
    media_x = media(x)
    media_y = media(y)
    
    soma_produtos = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
    divisor = n - 1 if amostral else n
    
    return soma_produtos / divisor

def correlacao_pearson(x, y):
    """
    Calcula o coeficiente de correlação linear de Pearson (r).

    Fórmula:
        r = Cov(X, Y) / (Sx * Sy)

    onde:
        Cov(X, Y) = covariância amostral entre X e Y
        Sx = desvio padrão amostral de X
        Sy = desvio padrão amostral de Y

    Retorna:
        float: coeficiente de correlação de Pearson.

    Levanta:
        ValueError: se as listas tiverem tamanhos diferentes,
                    possuírem menos de dois pares de observações
                    ou alguma variável for constante.
    """

    if len(x) != len(y):
        raise ValueError(
            "As listas X e Y devem ter o mesmo tamanho."
        )

    if len(x) < 2:
        raise ValueError(
            "A correlação de Pearson requer pelo menos 2 pares de dados."
        )

    cov = covariancia(x, y, amostral=True)

    dp_x = desvio_padrao(x, amostral=True)
    dp_y = desvio_padrao(y, amostral=True)

    if dp_x == 0 or dp_y == 0:
        raise ValueError(
            "A correlação de Pearson é indefinida "
            "quando uma das variáveis é constante."
        )

    r = cov / (dp_x * dp_y)

    return r

def limites_iqr(dados):
    """
    Calcula os limites inferior e superior para detecção de outliers usando o IQR.
    Fórmula: Q1 - 1.5*IQR e Q3 + 1.5*IQR.
    """
    q1 = percentil(dados, 25)
    q3 = percentil(dados, 75)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    return limite_inferior, limite_superior

def detectar_outliers(dados):
    """
    Retorna uma lista contendo apenas os valores que são outliers na distribuição.
    """
    inf, sup = limites_iqr(dados)
    return [x for x in dados if x < inf or x > sup]

def interpretar_assimetria(dados):
    """
    Interpreta a assimetria da distribuição comparando a Média e a Mediana.
    """
    m = media(dados)
    md = mediana(dados)
    
    # Pequena margem de tolerância (0.5%) para considerar como simétrica
    if abs(m - md) / (m if m != 0 else 1) < 0.005:
        return "Distribuição Simétrica (Média ≈ Mediana). Os dados estão bem distribuídos em torno do centro."
    elif m > md:
        return "Assimetria Positiva / À Direita (Média > Mediana). Há outliers com valores muito altos puxando a média."
    else:
        return "Assimetria Negativa / À Esquerda (Média < Mediana). Há outliers com valores muito baixos puxando a média."

def simular_frequencia_relativa(dados_categoricos, categoria_alvo, n_sorteios):
    """
    Simula inspeções aleatórias (amostragem com reposição) de uma lista de dados reais.
    Demonstra a Lei dos Grandes Números rastreando a frequência da categoria alvo.
    """
    if not dados_categoricos:
        raise ValueError("A lista de dados não pode estar vazia.")
    if n_sorteios <= 0:
        raise ValueError("O número de sorteios deve ser > 0.")
        
    proporcoes = []
    sucessos = 0
    n_dados = len(dados_categoricos)
    
    for i in range(1, n_sorteios + 1):
        sorteado = dados_categoricos[random.randint(0, n_dados - 1)]
        if sorteado == categoria_alvo:
            sucessos += 1
        proporcoes.append(sucessos / i)
        
    return proporcoes

def gerar_medias_amostrais(dados, tamanho_amostra, n_repeticoes):
    """
    Sorteia amostras repetidas de um dataset e calcula a média de cada uma.
    Demonstra o Teorema Central do Limite.
    """
    if not dados:
        raise ValueError("A lista de dados não pode estar vazia.")
    if tamanho_amostra <= 0 or n_repeticoes <= 0:
        raise ValueError("Tamanho da amostra e repetições devem ser > 0.")
        
    medias = []
    n_dados = len(dados)
    
    for _ in range(n_repeticoes):
        amostra = [dados[random.randint(0, n_dados - 1)] for _ in range(tamanho_amostra)]
        medias.append(media(amostra))
        
    return medias

def pdf_normal(x, mu, sigma):
    """
    Calcula a densidade de probabilidade da distribuição Normal.
    Fórmula: (1 / (sigma * sqrt(2*pi))) * e^(-0.5 * ((x - mu)/sigma)^2)
    """
    if sigma == 0:
        return 0.0
    coeficiente = 1.0 / (sigma * math.sqrt(2 * math.pi))
    expoente = -0.5 * ((x - mu) / sigma) ** 2
    return coeficiente * math.exp(expoente)

def pdf_exponencial(x, lambd):
    """
    Calcula a densidade de probabilidade da distribuição Exponencial.
    Fórmula: lambda * e^(-lambda * x) para x >= 0
    """
    if x < 0 or lambd <= 0:
        return 0.0
    return lambd * math.exp(-lambd * x)

