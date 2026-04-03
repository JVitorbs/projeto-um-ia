"""
Main para solução com Lógica Fuzzy
Executa resolver com fuzzy logic separadamente do GA
"""

import random
import os
import json
from copy import deepcopy
from individuo import Individuo
from fuzzy_solver import FuzzySolver
from fuzzy_logic import criar_sistema_fuzzy
from config import *
from disciplinas import disciplinas, PRIMEIRO_SEMESTRE_FIXO
from logger import salvar_evolucao
from simulation import simular
from ga import fitness


def _definir_seed_experimento():
    """Define a seed global do experimento para reproducibilidade."""
    valor_env = os.getenv("SEED_EXPERIMENTO")
    if valor_env is not None:
        try:
            seed = int(valor_env)
        except ValueError as exc:
            raise ValueError(
                "SEED_EXPERIMENTO deve ser um inteiro, por exemplo: 12345"
            ) from exc
    else:
        seed = SEED_EXPERIMENTO

    random.seed(seed)
    return seed


SEED_USADA = _definir_seed_experimento()
print(f"Seed do experimento (Fuzzy): {SEED_USADA}")

# Número de iterações/tentativas fuzzy (configuráveis por variável de ambiente)
ITERACOES_FUZZY = int(os.getenv("FUZZY_ITERACOES", str(min(120, GERACOES))))
TENTATIVAS_FUZZY = int(os.getenv("FUZZY_TENTATIVAS", str(min(40, POPULACAO))))

# Threshold de alocação fuzzy (0.0-1.0)
# 0.3 = "low" para cima (padrão, mais permissivo)
# 0.5 = "medium" para cima (balanceado)
# 0.7 = "high" para cima (mais restritivo)
THRESHOLD_FUZZY = float(os.getenv("FUZZY_THRESHOLD", "0.3"))


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


def _str_perfil(p):
    partes = []
    if p.get("trabalha"):       partes.append("trabalha")
    if p.get("estagio"):        partes.append("estágio")
    if p.get("ic"):             partes.append("IC")
    if p.get("escola_publica"): partes.append("escola pública")
    if not p.get("mora_na_cidade", True): partes.append("fora da cidade")
    partes.append(f"{p.get('horas_estudo', 0)}h/sem estudo")
    return ", ".join(partes) if partes else "sem atividades extras"


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


print(
    f"\nResolvendo com Lógica Fuzzy "
    f"({ITERACOES_FUZZY} iterações, {TENTATIVAS_FUZZY} tentativas, "
    f"threshold={THRESHOLD_FUZZY})...\n"
)

# Executar múltiplas tentativas fuzzy para simular uma "população"
# Cada tentativa é um solver independente
pop_fuzzy = []
hist_fuzzy = []
melhor_ate_agora = float('inf')
tempo_do_melhor_ate_agora = 0

for tentativa in range(TENTATIVAS_FUZZY):
    if tentativa % 10 == 0:
        print(f"  Tentativa {tentativa + 1}/{TENTATIVAS_FUZZY}...")
    
    solver = FuzzySolver(iteracoes=ITERACOES_FUZZY, threshold_alocacao=THRESHOLD_FUZZY)
    solver.resolver()
    individuo = solver.melhor_individuo
    
    # Avaliar o indivíduo
    fitness(individuo)
    pop_fuzzy.append(individuo)
    
    # Consolidar histórico: manter apenas o melhor acumulado
    # Se for a primeira tentativa OU melhor que o anterior
    if not hist_fuzzy or individuo.fitness < melhor_ate_agora:
        # Atualizar o melhor global
        if individuo.fitness < melhor_ate_agora:
            melhor_ate_agora = individuo.fitness
            tempo_do_melhor_ate_agora = individuo.tempo_formatura
        
        # Adicionar ao histórico consolidado
        # (cada tentativa que melhora é como uma "geração")
        hist_fuzzy.append({
            "tentativa": tentativa,
            "melhor": melhor_ate_agora,
            "tempo": tempo_do_melhor_ate_agora,
        })

# Sort população fuzzy
pop_fuzzy.sort(key=lambda x: x.fitness)

# Construir histórico compatível com GA
# Rastrear o MELHOR ACUMULADO (monotônico decrescente)
hist = []
melhor_ate_agora = float("inf")
tempo_do_melhor_ate_agora = 0
sem_melhoria = 0

# Simulação de "gerações" baseado na população fuzzy
# Vamos considerar que temos GERACOES snapshots da população
chunk_size = max(1, len(pop_fuzzy) // GERACOES)
for g in range(min(GERACOES, len(pop_fuzzy) // chunk_size)):
    inicio = g * chunk_size
    fim = min(inicio + chunk_size, len(pop_fuzzy))
    chunk = pop_fuzzy[inicio:fim]
    
    if not chunk:
        continue
    
    for ind in chunk:
        fitness(ind)
    
    chunk.sort(key=lambda x: x.fitness)
    melhor_da_geracao = chunk[0]
    
    # IMPORTANTE: Comparar com melhor acumulado, não com da geração anterior
    if melhor_da_geracao.fitness < melhor_ate_agora:
        melhor_ate_agora = melhor_da_geracao.fitness
        tempo_do_melhor_ate_agora = melhor_da_geracao.tempo_formatura
        sem_melhoria = 0
    else:
        sem_melhoria += 1
    
    media = sum(ind.fitness for ind in chunk) / len(chunk)
    fitness_ordenados = sorted(ind.fitness for ind in chunk)
    tempos_ordenados = sorted(ind.tempo_formatura for ind in chunk)
    
    hist.append({
        "geracao": g,
        "melhor": melhor_ate_agora,  # ✅ AGORA: melhor acumulado (monotônico)
        "melhor_ate_agora": melhor_ate_agora,
        "media": media,
        "pior": fitness_ordenados[-1],
        "mediana": percentil(fitness_ordenados, 0.50),
        "q1": percentil(fitness_ordenados, 0.25),
        "q3": percentil(fitness_ordenados, 0.75),
        "diversidade": 1.0,
        "mutation_rate": 0.0,  # N/A para fuzzy
        "sem_melhoria": sem_melhoria,
        "reprovacoes": melhor_da_geracao.reprovacoes,  # Da geração (informativo)
        "tempo": tempo_do_melhor_ate_agora,  # Do melhor acumulado
        "tempo_melhor_ate_agora": tempo_do_melhor_ate_agora,
        "tempo_pior": tempos_ordenados[-1],
        "tempo_mediana": percentil(tempos_ordenados, 0.50),
        "tempo_q1": percentil(tempos_ordenados, 0.25),
        "tempo_q3": percentil(tempos_ordenados, 0.75)
    })

# Avaliar população final
for ind in pop_fuzzy:
    fitness(ind)
pop_fuzzy.sort(key=lambda x: x.fitness)

melhor_final = pop_fuzzy[0]

print(f"\nIterações executadas: {len(hist)}")
print(f"Populações processadas: {len(pop_fuzzy)}")

# Top 3
print("\nTop 3 (Fuzzy):")
top3_fuzzy = pop_fuzzy[:3]
top3_resumo = []
for rank, ind in enumerate(top3_fuzzy, 1):
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

# Categorias
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

print("\nResumo por categoria (melhor plano entre os indivíduos finais) - Fuzzy:")
categorias_resumo = []
for nome_cat, perfil_cat in PERFIS_CATEGORIA.items():
    melhor_idx = -1
    melhor_res = None

    for idx, ind in enumerate(pop_fuzzy):
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

# Salvar resultados
resultado_fuzzy = {
    "seed": SEED_USADA,
    "historico": hist,
    "top3": top3_resumo,
    "categorias": categorias_resumo,
}

# Salvar em arquivo separado
import json
from pathlib import Path

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

with open(logs_dir / "evolucao_fuzzy.json", "w") as f:
    json.dump(resultado_fuzzy, f, indent=2)

print(f"\nResultados fuzzy salvos em logs/evolucao_fuzzy.json")
print("\nDisciplinas fixas do 1o semestre:")
for codigo in PRIMEIRO_SEMESTRE_FIXO:
    nome = disciplinas.get(codigo, {}).get("nome", codigo)
    print(f"  - {codigo} - {nome}")
