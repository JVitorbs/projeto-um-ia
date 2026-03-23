import random
import math
from disciplinas import disciplinas

from config import (
    CARGA_MAX_SEMESTRE,
    OPTATIVAS_MIN,
    PESO_CONTEXTO_REPROVACAO,
    SEMESTRES_MAX,
    SEMESTRES_EXTRA_SIMULACAO,
)


def prob_reprovacao(nome, perfil, carga_semestre, muitas_dificeis):

    dificuldade = disciplinas[nome]["dificuldade"]
    # Dificuldade da disciplina influencia, mas nao equivale diretamente a
    # probabilidade bruta de reprovacao.
    base = 0.03 + 0.28 * (dificuldade ** 1.4)
    pressao_contexto = 0.0

    if perfil.get("trabalha"):
        pressao_contexto += 1.00

    if perfil.get("estagio"):
        pressao_contexto += 0.70

    if perfil.get("ic"):
        pressao_contexto += 0.40

    if perfil.get("escola_publica"):
        pressao_contexto += 0.60

    if not perfil.get("mora_na_cidade", True):
        pressao_contexto += 0.70

    if carga_semestre > 300:
        pressao_contexto += ((carga_semestre - 300) / 120.0) * 0.60

    if muitas_dificeis:
        pressao_contexto += 0.50

    horas_estudo = max(0, min(30, perfil.get("horas_estudo", 0)))
    alivio_estudo = min(0.12, 0.035 * math.log1p(horas_estudo))

    prob = base + PESO_CONTEXTO_REPROVACAO * pressao_contexto - alivio_estudo

    return max(0.03, min(prob, 0.85))


def _ordenar_unicos(disciplinas_lista):
    vistos = set()
    ordenadas = []
    for disc in disciplinas_lista:
        if disc in vistos:
            continue
        vistos.add(disc)
        ordenadas.append(disc)
    return ordenadas


def simular(individuo, perfil):

    aprovadas = set()
    todas_disciplinas = {
        d for semestre in individuo.grade for d in semestre if d in disciplinas
    }
    pendentes = []

    reprovacoes = 0
    violacoes_prereq = 0
    violacoes_carga = 0
    ultimo_semestre_ativo = 0
    total_semestres_limite = SEMESTRES_MAX + SEMESTRES_EXTRA_SIMULACAO

    for s_idx in range(total_semestres_limite):

        semestre_planejado = individuo.grade[s_idx] if s_idx < SEMESTRES_MAX else []

        # Pendencias de semestres anteriores entram primeiro para simular atraso.
        demanda = _ordenar_unicos(pendentes + semestre_planejado)
        demanda = [d for d in demanda if d in disciplinas and d not in aprovadas]

        if not demanda:
            if len(aprovadas) == len(todas_disciplinas):
                break
            continue

        ultimo_semestre_ativo = s_idx + 1

        carga_demanda = sum(disciplinas[d]["carga"] for d in demanda)
        if carga_demanda > CARGA_MAX_SEMESTRE:
            violacoes_carga += 1

        aprovadas_antes = set(aprovadas)
        carga_executada = 0
        tentadas = []
        pendentes_prox = []

        for disc in demanda:
            prereqs = disciplinas[disc]["prereq"]
            if any(pr not in aprovadas_antes for pr in prereqs):
                violacoes_prereq += 1
                pendentes_prox.append(disc)
                continue

            carga_disc = disciplinas[disc]["carga"]
            if carga_executada + carga_disc > CARGA_MAX_SEMESTRE:
                pendentes_prox.append(disc)
                continue

            tentadas.append(disc)
            carga_executada += carga_disc

        qtd_dificeis = sum(1 for d in tentadas if disciplinas[d]["dificuldade"] >= 0.75)
        muitas_dificeis = qtd_dificeis >= 3

        for disc in tentadas:
            prob = prob_reprovacao(disc, perfil, carga_executada, muitas_dificeis)

            if random.random() < prob:
                reprovacoes += 1
                pendentes_prox.append(disc)
            else:
                aprovadas.add(disc)

        pendentes = _ordenar_unicos(pendentes_prox)

        if len(aprovadas) == len(todas_disciplinas) and not pendentes:
            break

    carga_optativas = sum(
        disciplinas[d]["carga"]
        for d in aprovadas
        if disciplinas[d].get("tipo") == "optativa"
    )
    optativas_insuficientes = 1 if carga_optativas < OPTATIVAS_MIN else 0
    disciplinas_nao_concluidas = len(todas_disciplinas - aprovadas)

    individuo.reprovacoes = reprovacoes
    individuo.tempo_formatura = ultimo_semestre_ativo
    individuo.violacoes_prereq = violacoes_prereq
    individuo.violacoes_carga = violacoes_carga
    individuo.optativas_insuficientes = optativas_insuficientes
    individuo.disciplinas_nao_concluidas = disciplinas_nao_concluidas

    return (
        ultimo_semestre_ativo,
        reprovacoes,
        violacoes_prereq,
        violacoes_carga,
        optativas_insuficientes,
        disciplinas_nao_concluidas,
    )