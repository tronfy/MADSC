import math


def media(amostra):
    n = len(amostra)
    soma = sum(amostra)

    return soma / n


def desvio_padrao(amostra):
    n = len(amostra)

    quad_da_soma = sum(amostra) ** 2
    soma_dos_quads = sum([n**2 for n in amostra])

    return math.sqrt((1 / (n - 1)) * (soma_dos_quads - (quad_da_soma / n)))


def pares(amostra):
    return amostra[0:-1], amostra[1:]  # 1, 2, 3, 4 -> (1, 2), (2, 3), (3, 4)
    # return amostra[0::2], amostra[1::2]  # 1, 2, 3, 4 -> (1, 2), (3, 4)


def covariancia(amostra):
    x, y = pares(amostra)
    n = len(x)

    soma_dos_prods = sum([x[i] * y[i] for i in range(n)])
    return (n * soma_dos_prods - sum(x) * sum(y)) / (n * (n - 1))


def coef_correlacao(amostra):
    x, y = pares(amostra)
    return covariancia(amostra) / (desvio_padrao(x) * desvio_padrao(y))


def normalize(x, start, end):
    # map x from [start, end] to [0, 1]
    return (x - start) / (end - start)


def qui_quadrado(amostra, start=0, end=1):
    n = len(amostra)
    k = 10

    intervalos = [0] * k
    for i in amostra:
        intervalos[math.ceil(normalize(i, start, end) * k) - 1] += 1

    return sum([((i - (n / k)) ** 2) / (n / k) for i in intervalos])
