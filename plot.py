import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D


# 1 caixas, 1000 simulações, tempo max 18000:
#               TS |       TF |     TSis           |      TOF
# média:     58.99 | 26985.97 | 27044.96 (450m44s) |    16.56
# desvio:     2.09 |  1772.18 |  1773.64 (29m33s)  |    15.91
# IC:         0.13 |   109.84 |   109.93           |     0.99

# 2 caixas, 1000 simulações, tempo max 18000:
#               TS |       TF |     TSis           |      TOF
# média:     58.99 |  8982.22 |  9041.21 (150m41s) |    67.01
# desvio:     2.09 |   888.69 |   890.13 (14m50s)  |    55.91
# IC:         0.13 |    55.08 |    55.17           |     3.47

# 3 caixas, 1000 simulações, tempo max 18000:
#               TS |       TF |     TSis           |      TOF
# média:     58.99 |  3019.34 |  3078.33 (51m18s)  |   143.88
# desvio:     2.09 |   591.77 |   593.19 (9m53s)   |    97.56
# IC:         0.13 |    36.68 |    36.77           |     6.05

# 4 caixas, 1000 simulações, tempo max 18000:
#               TS |       TF |     TSis           |      TOF
# média:     58.99 |   382.24 |   441.23 (7m21s)   |   750.24
# desvio:     2.09 |   253.37 |   254.76 (4m14s)   |   481.98
# IC:         0.13 |    15.70 |    15.79           |    29.87

# 5 caixas, 1000 simulações, tempo max 18000:
#               TS |       TF |     TSis           |      TOF
# média:     58.99 |    36.50 |    95.49 (1m35s)   |  3791.83
# desvio:     2.09 |    20.23 |    21.47 (0m21s)   |   653.18
# IC:         0.13 |     1.25 |     1.33           |    40.48

x = np.array([1, 2, 3, 4, 5])

tsis = np.array([27044.96, 9041.21, 3078.33, 441.23, 95.49])
tof = np.array([16.56, 67.01, 143.88, 750.24, 3791.83])

std_tsis = np.array([1773.64, 890.13, 593.19, 254.76, 21.47])
std_tof = np.array([15.91, 55.91, 97.56, 481.98, 653.18])

# ci_tf = np.array([109.84, 55.08, 36.68, 15.70, 1.25])
# ci_tsis = np.array([109.93, 55.17, 36.77, 15.79, 1.33])
# ci_tof = np.array([0.99, 3.47, 6.05, 29.87, 40.48])

plt.axhline(15 * 60, linestyle="--", label="15 minutos", color="gray")

trans1 = Affine2D().translate(-0.03, 0.0)
trans2 = Affine2D().translate(0.03, 0.0)
plt.plot(
    x, tsis, label="TSis médio", color="blue", transform=trans1 + plt.gca().transData
)
plt.errorbar(
    x,
    tsis,
    yerr=std_tsis,
    fmt="o",
    label="TSis DP",
    color="darkblue",
    transform=trans1 + plt.gca().transData,
)

plt.plot(
    x, tof, label="TOF médio", color="orange", transform=trans2 + plt.gca().transData
)
plt.errorbar(
    x,
    tof,
    yerr=std_tof,
    fmt="o",
    label="TOF DP",
    color="darkorange",
    transform=trans2 + plt.gca().transData,
)

plt.xlabel("Número de caixas")
plt.ylabel("Tempo (s)")
plt.yscale("log")

plt.xticks(x)

plt.grid()

# horizontal bar at 15*60

# plt.scatter(x, tsis)
# plt.scatter(x, tof)

plt.legend()
plt.show()
