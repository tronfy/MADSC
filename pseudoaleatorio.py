def mcl(a, x, c, M):
    """
    Método Congruencial Linear

    x(n+1) = (a * x(n) + c) % M
    """

    return (a * x + c) % M
