from posto_bancario import simulacao
from estatistica import media, desvio_padrao

clientes, _ = simulacao(seed=42)


def time_format(seconds):
    return "({}m{}s)".format(int(seconds / 60), int(seconds % 60))


header = "{:<3} | {} | {:<17} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<18} | {:<8}".format(
    "#", "T", "TEC", "TS", "TCR", "TIS", "TFS", "TF", "TSis", "TOF"
)
print(header)
print("-" * len(header))
for i, c in enumerate(clientes):
    print(
        "{:>3} | {} | {:>8.2f} {:<8} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} {:<9} | {:>8.2f}".format(
            i + 1,
            c["tipo"],
            c["TEC"],
            time_format(c["tempo_chegada"]),
            c["TS"],
            c["TCR"],
            c["TIS"],
            c["TFS"],
            c["TF"],
            c["TSis"],
            time_format(c["TSis"]),
            c["TOF"],
        )
    )

ts_med = media([c["TS"] for c in clientes])
tf_med = media([c["TF"] for c in clientes])
tsis_med = media([c["TSis"] for c in clientes])
tof_med = media([c["TOF"] for c in clientes])

print("-" * len(header))
print(
    "médias: {} {:>8.2f} {} {:>8.2f}   {:>8.2f} {:<9}   {:>8.2f}".format(
        " " * 21, ts_med, " " * 34, tf_med, tsis_med, time_format(tsis_med), tof_med
    )
)

ts_dp = desvio_padrao([c["TS"] for c in clientes])
tf_dp = desvio_padrao([c["TF"] for c in clientes])
tsis_dp = desvio_padrao([c["TSis"] for c in clientes])
tof_dp = desvio_padrao([c["TOF"] for c in clientes])

print(
    "desvios: {} {:>8.2f} {} {:>8.2f}   {:>8.2f} {:<9}   {:>8.2f}".format(
        " " * 20, ts_dp, " " * 34, tf_dp, tsis_dp, time_format(tsis_dp), tof_dp
    )
)
