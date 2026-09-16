import math

def media(dados):
    """
    Calcula a média aritmética simples.
    Fórmula: (Σ x_i) / n
    Fonte: Bussab, W. O., & Morettin, P. A. (2010). Estatística Básica.
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
    Esta é a mesma regra usada no NumPy (interpolation='linear').
    """
    if not dados:
        raise ValueError("A lista de dados não pode estar vazia.")
    if not 0 <= p <= 100:
        raise ValueError("O percentil deve estar entre 0 e 100.")
        
    ordenados = sorted(dados)
    n = len(ordenados)
    
    # Índice real (pode ser fracionário)
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
    Calcula o Coeficiente de Correlação de Pearson (r).
    Fórmula: Cov(x,y) / (StdDev(x) * StdDev(y))
    """
    cov = covariancia(x, y, amostral=True)
    dp_x = desvio_padrao(x, amostral=True)
    dp_y = desvio_padrao(y, amostral=True)
    
    if dp_x == 0 or dp_y == 0:
        return 0.0 # Evita divisão por zero se uma das variáveis for constante
        
    return cov / (dp_x * dp_y)

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
    
    # Adicionamos uma pequena margem de tolerância (0.5%) para considerar como simétrica
    if abs(m - md) / (m if m != 0 else 1) < 0.005:
        return "Distribuição Simétrica (Média ≈ Mediana). Os dados estão bem distribuídos em torno do centro."
    elif m > md:
        return "Assimetria Positiva / À Direita (Média > Mediana). Há outliers com valores muito altos puxando a média."
    else:
        return "Assimetria Negativa / À Esquerda (Média < Mediana). Há outliers com valores muito baixos puxando a média."