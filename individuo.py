import random
from config import OPTATIVAS_MIN, SEMESTRES_MAX
from disciplinas import disciplinas
from reparo import reparar_individuo

class Individuo:

    def __init__(self):

        self.grade = [[] for _ in range(SEMESTRES_MAX)]
        self.fitness = None
        self.reprovacoes = 0
        self.tempo_formatura = 0
        self.violacoes_prereq = 0
        self.violacoes_carga = 0
        self.optativas_insuficientes = 0
        self.disciplinas_nao_concluidas = 0
        self.perfil = {}

    def gerar_perfil_random(self):
        """Gera um perfil de aluno aleatório para este indivíduo."""
        self.perfil = {
            "trabalha":       random.random() < 0.20,  # 20% trabalha
            "estagio":        random.random() < 0.25,  # 25% faz estágio
            "ic":             random.random() < 0.20,  # 20% faz IC
            "escola_publica": random.random() < 0.55,  # 55% veio de escola publica
            "mora_na_cidade": random.random() < 0.55,  # 55% mora na cidade
            "horas_estudo":   random.randint(2, 20),   # 2–20h/semana
        }

    def inicializar_random(self):
        self.gerar_perfil_random()

        obrigatorias = [
            codigo for codigo, info in disciplinas.items() if info.get("tipo") == "obrigatoria"
        ]
        optativas = [
            codigo for codigo, info in disciplinas.items() if info.get("tipo") == "optativa"
        ]
        random.shuffle(optativas)

        escolhidas_opt = []
        carga_opt = 0
        for codigo in optativas:
            escolhidas_opt.append(codigo)
            carga_opt += disciplinas[codigo]["carga"]
            if carga_opt >= OPTATIVAS_MIN:
                break

        nomes = obrigatorias + escolhidas_opt

        for d in nomes:

            s = random.randint(0,SEMESTRES_MAX-1)
            self.grade[s].append(d)

        reparar_individuo(self)