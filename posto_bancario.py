import math
from tqdm import tqdm
from pseudoaleatorio import uniforme
from estatistica import media, desvio_padrao

SEED = 57
NUM_CAIXAS = 4
NUM_SIMS = 1000
TEMPO_MAX = 18000  # 10h às 15h

cliente = {
    "id": -1,
    "tipo": -1,
    "TEC": -1,
    "TS": -1,
    "TCR": -1,
    "TIS": -1,
    "TFS": -1,
    "TF": -1,
    "TSis": -1,
}


def simulacao(seed, tempo_max=TEMPO_MAX):
    U = uniforme(0, 1, seed)
    clientes = []

    fila = []
    em_atendimento = []
    atendidos = []

    tof = 0

    t = 0
    caixas_livres = NUM_CAIXAS

    # gerar clientes
    tempo_total = 0
    while True:
        a, b, id = next(U), next(U), next(U)

        if 0 <= a <= 0.6:
            tipo = 1
            ts = -15 * math.log(id) + 15
        elif 0.6 < a <= 0.9:
            tipo = 2
            ts = -40 * math.log(id) + 30
        else:
            tipo = 3
            ts = -140 * math.log(id) + 60

        tec = -15 * math.log(b)

        # tec = round(tec, 2)
        tec = round(tec)
        # ts = round(ts, 2)
        ts = round(ts)

        tempo_total += tec
        if tempo_total > tempo_max:
            break

        cli = cliente.copy()
        cli["id"] = len(clientes)
        cli["tipo"] = tipo
        cli["TEC"] = tec
        cli["TS"] = ts
        cli["TCR"] = tempo_total
        clientes.append(cli)

    while True:
        # clientes que chegaram no ultimo segundo
        chegaram = [c["id"] for c in clientes if t - 1 < c["TCR"] and c["TCR"] <= t]
        fila.extend(chegaram)

        # clientes esperando na fila
        for id in fila:
            c = clientes[id]
            c["TF"] += 1
            if caixas_livres > 0:
                # mover para em atendimento
                em_atendimento.append(id)
                fila = list(filter(lambda x: x != id, fila))
                caixas_livres -= 1
                c["TIS"] = t
                c["TFS"] = t + c["TS"]

        tof += caixas_livres

        # clientes em atendimento
        for id in em_atendimento:
            c = clientes[id]
            if c["TFS"] == t:
                c["TSis"] = c["TS"] + c["TF"]
                caixas_livres += 1
                # mover para atendidos
                atendidos.append(id)
                em_atendimento = list(filter(lambda x: x != id, em_atendimento))

        t += 1
        if len(atendidos) == len(clientes):
            break

    ts_med = sum(c["TS"] for c in clientes) / len(clientes)
    tf_med = sum(c["TF"] for c in clientes) / len(clientes)
    tsis_med = sum(c["TSis"] for c in clientes) / len(clientes)

    return clientes, (ts_med, tf_med, tsis_med, tof)


if __name__ == "__main__":
    U = uniforme(0, 1, SEED)
    sims = [simulacao(int(next(U) * 9999) + 1) for _ in tqdm(range(NUM_SIMS))]

    print(
        "{} caixas, {} simulações, tempo max {}:".format(
            NUM_CAIXAS, NUM_SIMS, TEMPO_MAX
        )
    )
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
