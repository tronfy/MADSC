import math
from pseudoaleatorio import uniforme
from estatistica import media, desvio_padrao

seed = 57
NUM_SIMS = 1000
TEMPO_MAX = 1800

cliente = {
    "tipo": 0,
    "TEC": 0,
    "TS": 0,
    "TCR": 0,
    "TIS": 0,
    "TFS": 0,
    "TF": 0,
    "TSis": 0,
    "TOF": 0,
    "tempo_chegada": 0,
}


def simulacao(seed, tempo_max=TEMPO_MAX):
    U = uniforme(0, 1, seed)
    clientes = []
    tempo_total = 0
    while True:
        a, b, c = next(U), next(U), next(U)

        if 0 <= a <= 0.6:
            tipo = 1
            ts = -15 * math.log(c) + 15
        elif 0.6 < a <= 0.9:
            tipo = 2
            ts = -40 * math.log(c) + 30
        else:
            tipo = 3
            ts = -140 * math.log(c) + 60

        tec = -15 * math.log(b)

        tec = round(tec, 2)
        ts = round(ts, 2)

        tempo_total += tec
        if tempo_total > tempo_max:
            break

        cli = cliente.copy()
        cli["tipo"] = tipo
        cli["TEC"] = tec
        cli["TS"] = ts
        cli["tempo_chegada"] = tempo_total
        clientes.append(cli)

    # primeiro cliente
    clientes[0]["TCR"] = clientes[0]["TEC"]
    clientes[0]["TIS"] = clientes[0]["TCR"]
    clientes[0]["TFS"] = clientes[0]["TIS"] + clientes[0]["TS"]
    clientes[0]["TF"] = 0
    clientes[0]["TSis"] = clientes[0]["TS"]
    clientes[0]["TOF"] = clientes[0]["TCR"]

    for i in range(1, len(clientes)):
        prev = clientes[i - 1]
        c = clientes[i]

        c["TCR"] = c["TEC"] + prev["TCR"]
        c["TIS"] = max(c["TCR"], prev["TFS"])
        c["TFS"] = c["TIS"] + c["TS"]
        c["TF"] = c["TIS"] - c["TCR"]
        c["TSis"] = c["TFS"] - c["TCR"]
        c["TOF"] = c["TIS"] - prev["TFS"]

    ts_med = sum(c["TS"] for c in clientes) / len(clientes)
    tf_med = sum(c["TF"] for c in clientes) / len(clientes)
    tsis_med = sum(c["TSis"] for c in clientes) / len(clientes)
    tof_med = sum(c["TOF"] for c in clientes) / len(clientes)

    return clientes, (ts_med, tf_med, tsis_med, tof_med)


if __name__ == "__main__":
    U = uniforme(0, 1, seed)
    sims = [simulacao(int(next(U) * 9999) + 1) for _ in range(NUM_SIMS)]

    print("{} simulações, tempo max {}:".format(NUM_SIMS, TEMPO_MAX))
    print("{:>7} {:>8} | {:>8} | {:>8} | {:>8}".format(" ", "TS", "TF", "TSis", "TOF"))

    ts_med = media([ts_med for _, (ts_med, _, _, _) in sims])
    tf_med = media([tf_med for _, (_, tf_med, _, _) in sims])
    tsis_med = media([tsis_med for _, (_, _, tsis_med, _) in sims])
    tof_med = media([tof_med for _, (_, _, _, tof_med) in sims])
    print(
        "{:<7} {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f}".format(
            "média:", ts_med, tf_med, tsis_med, tof_med
        )
    )

    ts_dp = desvio_padrao([ts_med for _, (ts_med, _, _, _) in sims])
    tf_dp = desvio_padrao([tf_med for _, (_, tf_med, _, _) in sims])
    tsis_dp = desvio_padrao([tsis_med for _, (_, _, tsis_med, _) in sims])
    tof_dp = desvio_padrao([tof_med for _, (_, _, _, tof_med) in sims])
    print(
        "{:<7} {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f}".format(
            "desvio:", ts_dp, tf_dp, tsis_dp, tof_dp
        )
    )

    # intervalo de confiança
    t = 1.96  # 95% de confiança
    ts_ic = t * ts_dp / math.sqrt(NUM_SIMS)
    tf_ic = t * tf_dp / math.sqrt(NUM_SIMS)
    tsis_ic = t * tsis_dp / math.sqrt(NUM_SIMS)
    tof_ic = t * tof_dp / math.sqrt(NUM_SIMS)
    print(
        "{:<7} {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f}".format(
            "IC:", ts_ic, tf_ic, tsis_ic, tof_ic
        )
    )
