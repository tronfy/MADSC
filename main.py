from estatistica import coef_correlacao, covariancia, desvio_padrao, media, qui_quadrado
from pseudoaleatorio import mcl


a = 16807
M = 2**31 - 1
c = 0

seed = 10
it = 1_000

print("a = {}, M = {}, c = {}".format(a, M, c))
print("seed = {}, {} iterações".format(seed, it))


x = seed
amostra = [x / M]

if it <= 10:
    print("\n{}\t{:.5f}".format(str(x).ljust(10), x / M))

for _ in range(it):
    x = mcl(a, x, c, M)
    amostra.append(x / M)

    if it <= 10:
        print("{}\t{:.5f}".format(str(x).ljust(10), x / M))

print("\nmédia = {:.5f}".format(media(amostra)))
print("desvio padrão = {:.5f}".format(desvio_padrao(amostra)))
print("covariância = {:.5f}".format(covariancia(amostra)))
print("coeficiente de correlação = {:.5f}".format(coef_correlacao(amostra)))
print("qui-quadrado = {:.5f}".format(qui_quadrado(amostra)))
