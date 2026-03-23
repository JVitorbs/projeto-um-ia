import random
from config import (
    TORNEIO,
    PESO_REPROVACAO,
    PESO_VIOL_PREREQ,
    PESO_VIOL_CARGA,
    PESO_OPT_INSUF,
    PESO_DISC_NAO_CONCLUIDA,
)
from simulation import simular
from crossover import crossover
from mutacao import mutacao


AVALIACOES_POR_FITNESS = 3


def fitness(individuo):
    soma_tempo = 0.0
    soma_reprov = 0.0
    soma_viol_prereq = 0.0
    soma_viol_carga = 0.0
    soma_opt_insuf = 0.0
    soma_nao_concluidas = 0.0

    for _ in range(AVALIACOES_POR_FITNESS):
        tempo, reprov, viol_prereq, viol_carga, opt_insuf, nao_concluidas = simular(individuo, individuo.perfil)
        soma_tempo += tempo
        soma_reprov += reprov
        soma_viol_prereq += viol_prereq
        soma_viol_carga += viol_carga
        soma_opt_insuf += opt_insuf
        soma_nao_concluidas += nao_concluidas

    tempo_medio = soma_tempo / AVALIACOES_POR_FITNESS
    reprov_medio = soma_reprov / AVALIACOES_POR_FITNESS
    viol_prereq_media = soma_viol_prereq / AVALIACOES_POR_FITNESS
    viol_carga_media = soma_viol_carga / AVALIACOES_POR_FITNESS
    opt_insuf_media = soma_opt_insuf / AVALIACOES_POR_FITNESS
    nao_concluidas_media = soma_nao_concluidas / AVALIACOES_POR_FITNESS

    f = (
        tempo_medio
        + PESO_REPROVACAO * reprov_medio
        + PESO_VIOL_PREREQ * viol_prereq_media
        + PESO_VIOL_CARGA * viol_carga_media
        + PESO_OPT_INSUF * opt_insuf_media
        + PESO_DISC_NAO_CONCLUIDA * nao_concluidas_media
    )

    individuo.fitness = f
    individuo.tempo_formatura = tempo_medio
    individuo.reprovacoes = reprov_medio
    individuo.violacoes_prereq = viol_prereq_media
    individuo.violacoes_carga = viol_carga_media
    individuo.optativas_insuficientes = opt_insuf_media
    individuo.disciplinas_nao_concluidas = nao_concluidas_media
    return f


def selecao(populacao):

    candidatos = random.sample(populacao, TORNEIO)
    return min(candidatos, key=lambda x: x.fitness)
