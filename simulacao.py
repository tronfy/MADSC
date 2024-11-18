import math
from tqdm.contrib.concurrent import process_map

from pseudoaleatorio import uniforme
from utils import media, desvio_padrao, time_format

SEED = 57
NUM_CAIXAS = 4
NUM_SIMS = 1000
TEMPO_MAX = 18000  # 10h às 15h


class Cliente:
    def __init__(self, tipo: int, tec: int, ts: int, tcr: int):
        self.tipo = tipo
        self.tec = tec
        self.ts = ts
        self.tcr = tcr
        self.tis = -1
        self.tfs = -1
        self.tf = -1
        self.tsis = -1


def simular(seed, tempo_max=TEMPO_MAX):
    U = uniforme(0, 1, seed)
    clientes: list[Cliente] = []

    chegando: list[int] = []
    fila: list[int] = []
    em_atendimento: list[int] = []

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

        cli = Cliente(tipo, tec, ts, tempo_total)
        clientes.append(cli)
        chegando.append(len(clientes) - 1)

    # simular
    t = 0
    caixas_livres = NUM_CAIXAS
    tof = 0
    atendidos = 0
    while True:
        indo_para_fila = []
        for id in chegando:
            # se o cliente chegou no segundo atual, entra na fila
            if t - 1 < clientes[id].tcr <= t:
                indo_para_fila.append(id)
        for id in indo_para_fila:
            chegando.remove(id)
            fila.append(id)

        # clientes esperando na fila
        for id in fila:
            clientes[id].tf += 1
        while caixas_livres > 0 and fila:
            id = fila.pop(0)
            caixas_livres -= 1
            clientes[id].tis = t
            clientes[id].tfs = t + clientes[id].ts
            em_atendimento.append(id)

        tof += caixas_livres

        # clientes em atendimento
        foram_atendidos = []
        for id in em_atendimento:
            if clientes[id].tis >= 0 and clientes[id].tsis < 0:
                if clientes[id].tfs == t:
                    clientes[id].tsis = clientes[id].ts + clientes[id].tf
                    caixas_livres += 1
                    atendidos += 1
                    foram_atendidos.append(id)
        for id in foram_atendidos:
            em_atendimento.remove(id)

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
        simular,
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