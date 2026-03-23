import random
from individuo import Individuo
from reparo import reparar_individuo


def crossover(pai1, pai2):

    filho = Individuo()

    ponto = random.randint(1, len(pai1.grade) - 2)

    filho.grade = (
        [list(s) for s in pai1.grade[:ponto]]
        + [list(s) for s in pai2.grade[ponto:]]
    )

    # Remover duplicatas (manter primeira ocorrência)
    vistas = set()
    for semestre in filho.grade:
        unicos = []
        for d in semestre:
            if d not in vistas:
                vistas.add(d)
                unicos.append(d)
        semestre[:] = unicos

    reparar_individuo(filho)

    # Herda perfil de um dos pais (filho "é" um tipo de aluno)
    filho.perfil = dict(random.choice([pai1, pai2]).perfil)

    return filho