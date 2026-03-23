from config import CARGA_MAX_SEMESTRE, OPTATIVAS_MIN, SEMESTRES_MAX
from disciplinas import PRIMEIRO_SEMESTRE_FIXO, disciplinas

DIFICIL_LIMIAR = 0.75
MAX_DIFICEIS_SEMESTRE = 2


def _prioridade_por_grade(grade):
    ordem = []
    vistos = set()
    for semestre in grade:
        for disc in semestre:
            if disc in disciplinas and disc not in vistos:
                vistos.add(disc)
                ordem.append(disc)

    return {disc: idx for idx, disc in enumerate(ordem)}


def _selecionar_optativas(prioridade):
    optativas = [
        codigo
        for codigo, info in disciplinas.items()
        if info.get("tipo") == "optativa"
    ]
    optativas.sort(key=lambda c: prioridade.get(c, 10**9))

    selecionadas = []
    carga = 0
    for codigo in optativas:
        selecionadas.append(codigo)
        carga += disciplinas[codigo]["carga"]
        if carga >= OPTATIVAS_MIN:
            break

    return selecionadas


def reparar_grade(grade):
    prioridade = _prioridade_por_grade(grade)

    nova_grade = [[] for _ in range(SEMESTRES_MAX)]
    cargas = [0 for _ in range(SEMESTRES_MAX)]
    dificeis = [0 for _ in range(SEMESTRES_MAX)]
    alocadas = {}

    # O 1o semestre e fixo, conforme grade oficial informada.
    for codigo in PRIMEIRO_SEMESTRE_FIXO:
        if codigo in disciplinas:
            nova_grade[0].append(codigo)
            cargas[0] += disciplinas[codigo]["carga"]
            if disciplinas[codigo]["dificuldade"] >= DIFICIL_LIMIAR:
                dificeis[0] += 1
            alocadas[codigo] = 0

    obrigatorias = {
        codigo
        for codigo, info in disciplinas.items()
        if info.get("tipo") == "obrigatoria"
    }
    optativas = set(_selecionar_optativas(prioridade))
    alvo = obrigatorias | optativas | set(PRIMEIRO_SEMESTRE_FIXO)

    restantes = alvo - set(alocadas.keys())

    while restantes:
        disponiveis = [
            d
            for d in restantes
            if all(pr in alocadas for pr in disciplinas[d]["prereq"])
        ]

        if not disponiveis:
            disponiveis = [min(restantes, key=lambda d: prioridade.get(d, 10**9))]

        disponiveis.sort(key=lambda d: prioridade.get(d, 10**9))
        disc = disponiveis[0]

        prereqs = disciplinas[disc]["prereq"]
        if prereqs:
            inicio = max(alocadas.get(pr, -1) for pr in prereqs) + 1
        else:
            inicio = 1

        inicio = min(inicio, SEMESTRES_MAX - 1)
        carga_disc = disciplinas[disc]["carga"]
        eh_dificil = disciplinas[disc]["dificuldade"] >= DIFICIL_LIMIAR

        escolhido = None
        for s in range(inicio, SEMESTRES_MAX):
            carga_ok = cargas[s] + carga_disc <= CARGA_MAX_SEMESTRE
            dificil_ok = (not eh_dificil) or (dificeis[s] < MAX_DIFICEIS_SEMESTRE)
            if carga_ok and dificil_ok:
                escolhido = s
                break

        if escolhido is None:
            for s in range(inicio, SEMESTRES_MAX):
                if cargas[s] + carga_disc <= CARGA_MAX_SEMESTRE:
                    escolhido = s
                    break

        if escolhido is None:
            escolhido = min(range(inicio, SEMESTRES_MAX), key=lambda s: cargas[s])

        nova_grade[escolhido].append(disc)
        cargas[escolhido] += carga_disc
        if eh_dificil:
            dificeis[escolhido] += 1

        alocadas[disc] = escolhido
        restantes.remove(disc)

    return nova_grade


def reparar_individuo(individuo):
    individuo.grade = reparar_grade(individuo.grade)
