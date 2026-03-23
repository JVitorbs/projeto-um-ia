import random
from copy import deepcopy
from individuo import Individuo
from ga import fitness,selecao,crossover,mutacao
from config import *
from disciplinas import disciplinas, PRIMEIRO_SEMESTRE_FIXO
from logger import salvar_evolucao
from simulation import simular

pop=[]

for _ in range(POPULACAO):

    i=Individuo()
    i.inicializar_random()
    pop.append(i)

hist=[]
melhor_ate_agora = float("inf")
tempo_do_melhor_ate_agora = 0
sem_melhoria = 0
melhor_global = None


def assinatura(ind):
    return tuple(tuple(s) for s in ind.grade)


def diversidade_populacao(populacao):
    if not populacao:
        return 0.0
    unicos = {assinatura(ind) for ind in populacao}
    return len(unicos) / len(populacao)


def percentil(valores_ordenados, p):
    if not valores_ordenados:
        return 0.0
    if len(valores_ordenados) == 1:
        return float(valores_ordenados[0])

    pos = (len(valores_ordenados) - 1) * p
    idx = int(pos)
    frac = pos - idx

    if idx + 1 < len(valores_ordenados):
        return valores_ordenados[idx] * (1 - frac) + valores_ordenados[idx + 1] * frac
    return float(valores_ordenados[idx])

for g in range(GERACOES):

    for ind in pop:

        fitness(ind)

    pop.sort(key=lambda x:x.fitness)

    melhor=pop[0]

    if melhor.fitness < melhor_ate_agora:
        melhor_ate_agora = melhor.fitness
        tempo_do_melhor_ate_agora = melhor.tempo_formatura
        melhor_global = deepcopy(melhor)
        sem_melhoria = 0
    else:
        sem_melhoria += 1

    mutation_rate_efetiva = min(MUTATION_MAX, MUTATION_RATE + sem_melhoria * 0.005)
    diversidade = diversidade_populacao(pop)

    media = sum(ind.fitness for ind in pop) / len(pop)
    fitness_ordenados = sorted(ind.fitness for ind in pop)
    tempos_ordenados = sorted(ind.tempo_formatura for ind in pop)

    hist.append({
        "geracao":g,
        "melhor":melhor.fitness,
        "melhor_ate_agora":melhor_ate_agora,
        "media":media,
        "pior":fitness_ordenados[-1],
        "mediana":percentil(fitness_ordenados, 0.50),
        "q1":percentil(fitness_ordenados, 0.25),
        "q3":percentil(fitness_ordenados, 0.75),
        "diversidade":diversidade,
        "mutation_rate":mutation_rate_efetiva,
        "sem_melhoria":sem_melhoria,
        "reprovacoes":melhor.reprovacoes,
        "tempo":melhor.tempo_formatura,
        "tempo_melhor_ate_agora":tempo_do_melhor_ate_agora,
        "tempo_pior":tempos_ordenados[-1],
        "tempo_mediana":percentil(tempos_ordenados, 0.50),
        "tempo_q1":percentil(tempos_ordenados, 0.25),
        "tempo_q3":percentil(tempos_ordenados, 0.75)
    })

    nova=pop[:ELITE]

    # Preserva explicitamente o melhor global encontrado para evitar regressao.
    if melhor_global is not None and nova:
        nova[0] = deepcopy(melhor_global)

    while len(nova)<POPULACAO:

        p1=selecao(pop)
        p2=selecao(pop)

        if random.random() < CROSSOVER_RATE:
            filho = crossover(p1, p2)
        else:
            filho = deepcopy(p1)

        if random.random() < mutation_rate_efetiva:
            mutacao(filho)

        nova.append(filho)

    if sem_melhoria >= 20:
        qtd_imigrantes = max(1, int(POPULACAO * TAXA_IMIGRANTES))
        for i in range(qtd_imigrantes):
            imigrante = Individuo()
            imigrante.inicializar_random()
            nova[-(i + 1)] = imigrante

    pop=nova

    if sem_melhoria >= SEM_MELHORIA_STOP:
        break

for ind in pop:
    fitness(ind)
pop.sort(key=lambda x: x.fitness)

if melhor_global is not None and melhor_global.fitness < pop[0].fitness:
    pop[-1] = deepcopy(melhor_global)
    pop.sort(key=lambda x: x.fitness)

melhor_final = pop[0]

print(f"Gerações executadas: {len(hist)}")
print(f"Sem melhoria final: {sem_melhoria}")


def _str_perfil(p):
    partes = []
    if p.get("trabalha"):       partes.append("trabalha")
    if p.get("estagio"):        partes.append("estágio")
    if p.get("ic"):             partes.append("IC")
    if p.get("escola_publica"): partes.append("escola pública")
    if not p.get("mora_na_cidade", True): partes.append("fora da cidade")
    partes.append(f"{p.get('horas_estudo', 0)}h/sem estudo")
    return ", ".join(partes) if partes else "sem atividades extras"


top3 = pop[:3]
top3_resumo = []
for rank, ind in enumerate(top3, 1):
    print(f"\n{'='*60}")
    print(f"  TOP {rank}  |  fitness={ind.fitness:.2f}  |  tempo={ind.tempo_formatura:.2f} semestres")
    print(f"  Reprovações: {ind.reprovacoes:.2f}  |  Perfil: {_str_perfil(ind.perfil)}")
    print(f"  Detalhes do perfil: {ind.perfil}")
    print(f"{'='*60}")
    top3_resumo.append({
        "rank": rank,
        "fitness": round(ind.fitness, 4),
        "tempo": round(ind.tempo_formatura, 4),
        "reprovacoes": round(ind.reprovacoes, 4),
        "perfil": dict(ind.perfil),
        "perfil_str": _str_perfil(ind.perfil),
    })
    for i, semestre in enumerate(ind.grade):
        if semestre:
            carga_semestre = sum(disciplinas[c]["carga"] for c in semestre if c in disciplinas)
            marcador = " (fixo)" if i == 0 else ""
            print(f"  Semestre {i + 1}{marcador} - {carga_semestre}h")
            for codigo in semestre:
                nome = disciplinas.get(codigo, {}).get("nome", codigo)
                print(f"    - {codigo} - {nome}")


def _fitness_componentes(tempo, reprov, viol_prereq, viol_carga, opt_insuf, nao_concluidas):
    return (
        tempo
        + PESO_REPROVACAO * reprov
        + PESO_VIOL_PREREQ * viol_prereq
        + PESO_VIOL_CARGA * viol_carga
        + PESO_OPT_INSUF * opt_insuf
        + PESO_DISC_NAO_CONCLUIDA * nao_concluidas
    )


def avaliar_individuo_em_categoria(individuo, perfil_categoria, repeticoes=12):
    soma_tempo = 0.0
    soma_reprov = 0.0
    soma_viol_prereq = 0.0
    soma_viol_carga = 0.0
    soma_opt_insuf = 0.0
    soma_nao_concluidas = 0.0
    tempo_min = float("inf")

    for _ in range(repeticoes):
        clone = deepcopy(individuo)
        clone.perfil = dict(perfil_categoria)
        tempo, reprov, viol_prereq, viol_carga, opt_insuf, nao_concluidas = simular(clone, clone.perfil)
        soma_tempo += tempo
        soma_reprov += reprov
        soma_viol_prereq += viol_prereq
        soma_viol_carga += viol_carga
        soma_opt_insuf += opt_insuf
        soma_nao_concluidas += nao_concluidas
        tempo_min = min(tempo_min, tempo)

    tempo_medio = soma_tempo / repeticoes
    reprov_medio = soma_reprov / repeticoes
    viol_prereq_media = soma_viol_prereq / repeticoes
    viol_carga_media = soma_viol_carga / repeticoes
    opt_insuf_media = soma_opt_insuf / repeticoes
    nao_concluidas_media = soma_nao_concluidas / repeticoes
    fitness_medio = _fitness_componentes(
        tempo_medio,
        reprov_medio,
        viol_prereq_media,
        viol_carga_media,
        opt_insuf_media,
        nao_concluidas_media,
    )

    return {
        "fitness_medio": fitness_medio,
        "tempo_medio": tempo_medio,
        "tempo_min": tempo_min,
        "reprov_medio": reprov_medio,
        "nao_concluidas_media": nao_concluidas_media,
    }


PERFIS_CATEGORIA = {
    "geral": {
        "trabalha": False,
        "estagio": False,
        "ic": False,
        "escola_publica": False,
        "mora_na_cidade": True,
        "horas_estudo": 18,
    },
    "escola_publica": {
        "trabalha": False,
        "estagio": False,
        "ic": False,
        "escola_publica": True,
        "mora_na_cidade": True,
        "horas_estudo": 18,
    },
    "ic": {
        "trabalha": False,
        "estagio": False,
        "ic": True,
        "escola_publica": False,
        "mora_na_cidade": True,
        "horas_estudo": 18,
    },
    "trabalha": {
        "trabalha": True,
        "estagio": False,
        "ic": False,
        "escola_publica": False,
        "mora_na_cidade": True,
        "horas_estudo": 18,
    },
    "estagio": {
        "trabalha": False,
        "estagio": True,
        "ic": False,
        "escola_publica": False,
        "mora_na_cidade": True,
        "horas_estudo": 18,
    },
    "fora_cidade": {
        "trabalha": False,
        "estagio": False,
        "ic": False,
        "escola_publica": False,
        "mora_na_cidade": False,
        "horas_estudo": 18,
    },
}

print("\nResumo por categoria (melhor plano entre os indivíduos finais):")
categorias_resumo = []
for nome_cat, perfil_cat in PERFIS_CATEGORIA.items():
    melhor_idx = -1
    melhor_res = None

    for idx, ind in enumerate(pop):
        res = avaliar_individuo_em_categoria(ind, perfil_cat, repeticoes=12)
        if melhor_res is None or res["fitness_medio"] < melhor_res["fitness_medio"]:
            melhor_res = res
            melhor_idx = idx

    categorias_resumo.append({
        "categoria": nome_cat,
        "perfil": dict(perfil_cat),
        "tempo_medio": round(melhor_res["tempo_medio"], 4),
        "tempo_min": round(melhor_res["tempo_min"], 4),
        "fitness_medio": round(melhor_res["fitness_medio"], 4),
        "reprov_medio": round(melhor_res["reprov_medio"], 4),
        "nao_concluidas_media": round(melhor_res["nao_concluidas_media"], 4),
        "indice_individuo_referencia": melhor_idx + 1,
    })

categorias_resumo.sort(key=lambda c: c["tempo_medio"])
for item in categorias_resumo:
    print(
        f"- {item['categoria']}: tempo médio={item['tempo_medio']:.2f} sem | "
        f"tempo mínimo observado={item['tempo_min']:.0f} sem | "
        f"fitness médio={item['fitness_medio']:.2f} | "
        f"indivíduo referência=TOP#{item['indice_individuo_referencia']} da população final"
    )

salvar_evolucao({
    "historico": hist,
    "top3": top3_resumo,
    "categorias": categorias_resumo,
})

print("\nDisciplinas fixas do 1o semestre:")
for codigo in PRIMEIRO_SEMESTRE_FIXO:
    nome = disciplinas.get(codigo, {}).get("nome", codigo)
    print(f"  - {codigo} - {nome}")