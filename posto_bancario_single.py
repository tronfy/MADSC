from posto_bancario import simulacao

clientes, _ = simulacao(seed=57)

header = (
    "{:<3} | {} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8}".format(
        "#", "T", "TEC", "TS", "TCR", "TIS", "TFS", "TF", "TSis", "TOF"
    )
)
print(header)
print("-" * len(header))
for i, c in enumerate(clientes):
    print(
        "{:>3} | {} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f}".format(
            i + 1,
            c["tipo"],
            c["TEC"],
            c["TS"],
            c["TCR"],
            c["TIS"],
            c["TFS"],
            c["TF"],
            c["TSis"],
            c["TOF"],
        )
    )

ts_avg = sum(c["TS"] for c in clientes) / len(clientes)
tf_avg = sum(c["TF"] for c in clientes) / len(clientes)
tsis_avg = sum(c["TSis"] for c in clientes) / len(clientes)
tof_avg = sum(c["TOF"] for c in clientes) / len(clientes)

print("-" * len(header))
print(
    "médias: {}{:>8.2f} {} {:>8.2f}   {:>8.2f}   {:>8.2f}".format(
        " " * 13, ts_avg, " " * 34, tf_avg, tsis_avg, tof_avg
    )
)
