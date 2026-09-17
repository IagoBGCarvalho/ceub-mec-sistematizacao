import statistics
import pytest
import numpy as np
from scipy import stats
import minhastats

# Dados simulando características de pacotes de rede (ex: Duração, Tamanho em Bytes)
DADOS_X = [45.2, 52.1, 48.0, 51.5, 47.9, 49.3, 50.1, 46.8]
DADOS_Y = [12.0, 14.5, 11.2, 15.1, 13.0, 12.8, 14.0, 11.9]
DADOS_MODA = [1, 2, 2, 3, 4]

def test_media():
    resultado_nosso = minhastats.media(DADOS_X)
    resultado_np = np.mean(DADOS_X)
    assert resultado_nosso == pytest.approx(resultado_np)

def test_mediana():
    resultado_nosso = minhastats.mediana(DADOS_X)
    resultado_np = np.median(DADOS_X)
    assert resultado_nosso == pytest.approx(resultado_np)

def test_moda():
    resultado_nosso = minhastats.moda(DADOS_MODA)
    resultado_stats = statistics.mode(DADOS_MODA)
    assert resultado_nosso == resultado_stats

def test_amplitude():
    resultado_nosso = minhastats.amplitude(DADOS_X)
    resultado_np = np.ptp(DADOS_X) # Peak-to-peak (max - min)
    assert resultado_nosso == pytest.approx(resultado_np)

def test_variancia_amostral():
    resultado_nosso = minhastats.variancia(DADOS_X, amostral=True)
    resultado_np = np.var(DADOS_X, ddof=1) # ddof=1 indica amostral no numpy
    assert resultado_nosso == pytest.approx(resultado_np)

def test_desvio_padrao_amostral():
    resultado_nosso = minhastats.desvio_padrao(DADOS_X, amostral=True)
    resultado_np = np.std(DADOS_X, ddof=1)
    assert resultado_nosso == pytest.approx(resultado_np)

def test_percentil():
    # Testando os quartis (25, 50, 75)
    for p in [25, 50, 75]:
        resultado_nosso = minhastats.percentil(DADOS_X, p)
        resultado_np = np.percentile(DADOS_X, p, method='linear')
        assert resultado_nosso == pytest.approx(resultado_np)

def test_covariancia():
    resultado_nosso = minhastats.covariancia(DADOS_X, DADOS_Y, amostral=True)
    resultado_np = np.cov(DADOS_X, DADOS_Y, ddof=1)[0][1]
    assert resultado_nosso == pytest.approx(resultado_np)

def test_correlacao_pearson():
    resultado_nosso = minhastats.correlacao_pearson(DADOS_X, DADOS_Y)
    resultado_scipy = stats.pearsonr(DADOS_X, DADOS_Y)[0]
    assert resultado_nosso == pytest.approx(resultado_scipy)