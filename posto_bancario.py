import math
from tqdm.contrib.concurrent import process_map
from enum import Enum

from pseudoaleatorio import uniforme
from estatistica import media, desvio_padrao, time_format

SEED = 57
NUM_CAIXAS = 4
NUM_SIMS = 1000
TEMPO_MAX = 18000  # 10h às 15h


class Status(Enum):
    NULO = -1
    FILA = 0
    ATENDIMENTO = 1
    ATENDIDO = 2


class Cliente:
    def __init__(self, id: int, tipo: int, tec: int, ts: int, tcr: int):
        self.id = id
        self.tipo = tipo
        self.tec = tec
        self.ts = ts
        self.tcr = tcr
        self.tis = -1
        self.tfs = -1
        self.tf = -1
        self.tsis = -1
        self.status = Status.NULO


def simulacao(seed, tempo_max=TEMPO_MAX):
    U = uniforme(0, 1, seed)
    clientes: list[Cliente] = []

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

        tec = round(tec)
        ts = round(ts)

        tempo_total += tec
        if tempo_total > tempo_max:
            break

        cli = Cliente(len(clientes), tipo, tec, ts, tempo_total)
        clientes.append(cli)

    # simular
    t = 0
    caixas_livres = NUM_CAIXAS
    tof = 0
    atendidos = 0
    while True:
        for i in range(len(clientes)):
            if clientes[i].status == Status.NULO:
                # se o cliente chegou no segundo atual, entra na fila
                if t - 1 < clientes[i].tcr and clientes[i].tcr <= t:
                    clientes[i].status = Status.FILA

        # clientes esperando na fila
        for i in range(len(clientes)):
            if clientes[i].status == Status.FILA:
                clientes[i].tf += 1
                if caixas_livres > 0:
                    clientes[i].status = Status.ATENDIMENTO
                    caixas_livres -= 1
                    clientes[i].tis = t
                    clientes[i].tfs = t + clientes[i].ts

        tof += caixas_livres

        # clientes em atendimento
        for i in range(len(clientes)):
            if clientes[i].status == Status.ATENDIMENTO:
                if clientes[i].tfs == t:
                    clientes[i].tsis = clientes[i].ts + clientes[i].tf
                    caixas_livres += 1
                    clientes[i].status = Status.ATENDIDO
                    atendidos += 1

        t += 1
        if atendidos == len(clientes):
            break

    ts_med = media([c.ts for c in clientes])
    tf_med = media([c.tf for c in clientes])
    tsis_med = media([c.tsis for c in clientes])

    return clientes, (ts_med, tf_med, tsis_med, tof)


if __name__ == "__main__":
    U = uniforme(0, 1, SEED)
    # sims = [simulacao(int(next(U) * 9999) + 1) for _ in tqdm(range(NUM_SIMS))]
    sims = process_map(
        simulacao,
        [int(next(U) * 9999) + 1 for _ in range(NUM_SIMS)],
    )

    print(
        "{} caixas, {} simulações, tempo max {}:".format(
            NUM_CAIXAS, NUM_SIMS, TEMPO_MAX
        )
    )
    print(
        "{:>7} {:>8} | {:>8} | {:>8} {:<9} | {:>8}".format(
            " ", "TS", "TF", "TSis", "", "TOF"
        )
    )

    ts_med = media([ts_med for _, (ts_med, _, _, _) in sims])
    tf_med = media([tf_med for _, (_, tf_med, _, _) in sims])
    tsis_med = media([tsis_med for _, (_, _, tsis_med, _) in sims])
    tof_med = media([tof_med for _, (_, _, _, tof_med) in sims])
    print(
        "{:<7} {:>8.2f} | {:>8.2f} | {:>8.2f} {:<9} | {:>8.2f}".format(
            "média:", ts_med, tf_med, tsis_med, time_format(tsis_med), tof_med
        )
    )

    ts_dp = desvio_padrao([ts_med for _, (ts_med, _, _, _) in sims])
    tf_dp = desvio_padrao([tf_med for _, (_, tf_med, _, _) in sims])
    tsis_dp = desvio_padrao([tsis_med for _, (_, _, tsis_med, _) in sims])
    tof_dp = desvio_padrao([tof_med for _, (_, _, _, tof_med) in sims])
    print(
        "{:<7} {:>8.2f} | {:>8.2f} | {:>8.2f} {:<9} | {:>8.2f}".format(
            "desvio:", ts_dp, tf_dp, tsis_dp, time_format(tsis_dp), tof_dp
        )
    )

    # intervalo de confiança
    t = 1.96  # 95% de confiança
    ts_ic = t * ts_dp / math.sqrt(NUM_SIMS)
    tf_ic = t * tf_dp / math.sqrt(NUM_SIMS)
    tsis_ic = t * tsis_dp / math.sqrt(NUM_SIMS)
    tof_ic = t * tof_dp / math.sqrt(NUM_SIMS)
    print(
        "{:<7} {:>8.2f} | {:>8.2f} | {:>8.2f} {:<9} | {:>8.2f}".format(
            "IC:", ts_ic, tf_ic, tsis_ic, "", tof_ic
        )
    )
