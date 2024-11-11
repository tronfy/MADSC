import math
from pseudoaleatorio import uniforme

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

    ts_avg = sum(c["TS"] for c in clientes) / len(clientes)
    tf_avg = sum(c["TF"] for c in clientes) / len(clientes)
    tsis_avg = sum(c["TSis"] for c in clientes) / len(clientes)
    tof_avg = sum(c["TOF"] for c in clientes) / len(clientes)

    return clientes, (ts_avg, tf_avg, tsis_avg, tof_avg)


if __name__ == "__main__":
    U = uniforme(0, 1, seed)
    sims = [simulacao(int(next(U) * 9999) + 1) for _ in range(NUM_SIMS)]

    ts_avg = sum(ts_avg for _, (ts_avg, _, _, _) in sims) / NUM_SIMS
    tf_avg = sum(tf_avg for _, (_, tf_avg, _, _) in sims) / NUM_SIMS
    tsis_avg = sum(tsis_avg for _, (_, _, tsis_avg, _) in sims) / NUM_SIMS
    tof_avg = sum(tof_avg for _, (_, _, _, tof_avg) in sims) / NUM_SIMS

    print("médias para {} simulações, tempo max {}:".format(NUM_SIMS, TEMPO_MAX))
    print("{:>8} | {:>8} | {:>8} | {:>8}".format("TS", "TF", "TSis", "TOF"))
    print(
        "{:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f}".format(
            ts_avg, tf_avg, tsis_avg, tof_avg
        )
    )
