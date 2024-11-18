from simulacao import simular
from utils import media, desvio_padrao, time_format


clientes, (ts_med, tf_med, tsis_med, tof) = simular(seed=42)


header = "{:<4} | {} | {:<4} | {:<20} | {:<4} | {:<6} | {:<6} | {:<5} | {:<15} | {:<8}".format(
    "#", "T", "TEC", "TCR", "TS", "TIS", "TFS", "TF", "TSis", "TOF"
)
print(header)
print("-" * len(header))
for i, c in enumerate(clientes):
    print(
        "{:>4} | {} | {:>4} | {:>8} {:<11} | {:>4} | {:>6} | {:>6} | {:>5} | {:>5} {:<9}".format(
            i + 1,
            c.tipo,
            c.tec,
            c.tcr,
            time_format(c.tcr),
            c.ts,
            c.tis,
            c.tfs,
            c.tf,
            c.tsis,
            time_format(c.tsis),
        )
    )

print("-" * len(header))
print(header)

print("-" * len(header))
print(
    "médias: {:<29} {:>8.2f} {:<16} {:>8.2f} {:>8.2f} {:<9} {:>8.2f}".format(
        "", ts_med, "", tf_med, tsis_med, time_format(tsis_med), tof
    )
)

ts_dp = desvio_padrao([c.ts for c in clientes])
tf_dp = desvio_padrao([c.tf for c in clientes])
tsis_dp = desvio_padrao([c.tsis for c in clientes])

print(
    "desvios: {:<28} {:>8.2f} {:<16} {:>8.2f} {:>8.2f} {:<9}".format(
        "", ts_dp, "", tf_dp, tsis_dp, time_format(tsis_dp)
    )
)
