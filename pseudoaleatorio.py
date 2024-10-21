import math


def mcl(a, x, c, M):
    """
    Método Congruencial Linear

    x(n+1) = (a * x(n) + c) % M
    """

    while True:
        x = (a * x + c) % M
        yield x / M


def gerar(gen, n):
    """
    Gera uma amostra de n números aleatórios a partir do gerador especificado
    """
    return [next(gen) for _ in range(n)]


def skip(X, n):
    for _ in range(n):
        next(X)


def uniforme(start, end, seed=42, mcl_a=69621, mcl_c=0, mcl_M=2**31 - 1):
    """
    Gera números aleatórios uniformemente distribuídos no intervalo [a, b]
    """

    X = mcl(mcl_a, seed, mcl_c, mcl_M)
    skip(X, 2)

    while True:
        x = next(X)
        yield start + (end - start) * x


def exponencial(alpha, seed=42, mcl_a=69621, mcl_c=0, mcl_M=2**31 - 1):
    """
    Gera números aleatórios exponencialmente distribuídos
    """

    X = mcl(mcl_a, seed, mcl_c, mcl_M)
    skip(X, 2)

    while True:
        x = next(X)
        yield -math.log(x) / alpha


def weibull(alpha, beta, seed=42, mcl_a=69621, mcl_c=0, mcl_M=2**31 - 1):
    """
    Gera números aleatórios na distribuição de Weibull
    """

    X = mcl(mcl_a, seed, mcl_c, mcl_M)
    skip(X, 2)

    while True:
        x = next(X)
        yield beta * (-math.log(x)) ** (1 / alpha)


def normal(mu, sigma, seed=42, mcl_a=69621, mcl_c=0, mcl_M=2**31 - 1):
    """
    Gera números aleatórios normalmente distribuídos
    """

    X = mcl(mcl_a, seed, mcl_c, mcl_M)
    skip(X, 2)

    while True:
        x = next(X)
        y = next(X)
        f = math.sqrt(-2 * math.log(1 - x)) * math.cos(2 * math.pi * y)
        yield mu + sigma * f


def erlang(k, alpha, seed=42, mcl_a=69621, mcl_c=0, mcl_M=2**31 - 1):
    """
    Gera números aleatórios Erlang
    """

    X = mcl(mcl_a, seed, mcl_c, mcl_M)
    skip(X, 2)

    while True:
        yield -1 * sum([math.log(next(X)) for _ in range(k)]) / alpha


def poisson(lamb, seed=42, mcl_a=69621, mcl_c=0, mcl_M=2**31 - 1):
    """
    Gera números aleatórios na distribuição de Poisson
    """

    X = mcl(mcl_a, seed, mcl_c, mcl_M)
    skip(X, 2)

    B = math.exp(-lamb)

    while True:
        k = 0
        p = 1
        while p >= B:
            k += 1
            p *= next(X)
        yield k - 1


def geometrica(p, seed=42, mcl_a=69621, mcl_c=0, mcl_M=2**31 - 1):
    """
    Gera números aleatórios na distribuição geométrica
    """

    X = mcl(mcl_a, seed, mcl_c, mcl_M)
    skip(X, 2)

    while True:
        yield math.floor(math.log(next(X)) / math.log(1 - p))
