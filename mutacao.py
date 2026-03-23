import random
from reparo import reparar_individuo

def mutacao(ind):
    """Aplica mutação: 60% move aleatório, 40% tenta adiantar para semestre anterior."""

    if len(ind.grade) <= 1:
        return

    # 60% chance: move aleatório entre semestres
    if random.random() < 0.60:
        s1 = random.randint(1, len(ind.grade) - 1)
        s2 = random.randint(1, len(ind.grade) - 1)

        if ind.grade[s1]:
            disc = random.choice(ind.grade[s1])
            ind.grade[s1].remove(disc)
            ind.grade[s2].append(disc)
            reparar_individuo(ind)
    else:
        # 40% chance: tenta adiantar disciplina para semestre anterior
        candidatos = []
        for s in range(2, len(ind.grade)):  # a partir do semestre 2
            for disc in ind.grade[s]:
                candidatos.append((s, disc))

        if candidatos:
            s, disc = random.choice(candidatos)
            # Tenta mover para um semestre anterior aleatório
            s_novo = random.randint(1, s - 1)
            ind.grade[s].remove(disc)
            ind.grade[s_novo].append(disc)
            reparar_individuo(ind)
