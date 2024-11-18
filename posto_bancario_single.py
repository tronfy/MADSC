from posto_bancario import simulacao
from estatistica import media, desvio_padrao, time_format


clientes, (_, _, _, tof) = simulacao(seed=42)


header = "{:<4} | {} | {:<8} | {:<20} | {:<8} | {:<8} | {:<8} | {:<8} | {:<18} | {:<8}".format(
    "#", "T", "TEC", "TCR", "TS", "TIS", "TFS", "TF", "TSis", "TOF"
)
print(header)
print("-" * len(header))
for i, c in enumerate(clientes):
    print(
        "{:>4} | {} | {:>8} | {:>8} {:<11} | {:>8} | {:>8} | {:>8} | {:>8} | {:>8} {:<9}".format(
            i + 1,
            c["tipo"],
            c["TEC"],
            c["TCR"],
            time_format(c["TCR"]),
            c["TS"],
            c["TIS"],
            c["TFS"],
            c["TF"],
            c["TSis"],
            time_format(c["TSis"]),
        )
    )

ts_med = media([c["TS"] for c in clientes])
tf_med = media([c["TF"] for c in clientes])
tsis_med = media([c["TSis"] for c in clientes])

print("-" * len(header))
print(
    "médias: {:<36} {:>8.2f} {:<23} {:>8.2f}   {:>8.2f} {:<9}   {:>8.2f}".format(
        "", ts_med, "", tf_med, tsis_med, time_format(tsis_med), tof
    )
)

ts_dp = desvio_padrao([c["TS"] for c in clientes])
tf_dp = desvio_padrao([c["TF"] for c in clientes])
tsis_dp = desvio_padrao([c["TSis"] for c in clientes])

print(
    "desvios: {:<35} {:>8.2f} {:<23} {:>8.2f}   {:>8.2f} {:<9}".format(
        "", ts_dp, "", tf_dp, tsis_dp, time_format(tsis_dp)
    )
)
