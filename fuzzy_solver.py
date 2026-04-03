"""
Solver Fuzzy para Otimização de Plano de Curso

Utiliza lógica fuzzy para construir um plano de curso iterativamente,
sem usar algoritmo genético. Produz resultados comparáveis ao GA.
"""

import random
from copy import deepcopy
from individuo import Individuo
from fuzzy_logic import criar_sistema_fuzzy
from config import (
    SEMESTRES_MAX,
    CARGA_MAX_SEMESTRE,
    PESO_VIOL_PREREQ,
    PESO_VIOL_CARGA,
    PESO_OPT_INSUF,
    PESO_DISC_NAO_CONCLUIDA,
)
from disciplinas import disciplinas, PRIMEIRO_SEMESTRE_FIXO
from simulation import simular


class FuzzySolver:
    """
    Solver fuzzy para otimizar plano de curso.
    
    Estratégia: Construir iterativamente um plano de curso usando
    scores fuzzy para decidir quais disciplinas alocar a cada semestre.
    """
    
    def __init__(self, perfil_aluno=None, iteracoes=50, threshold_alocacao=0.3):
        """
        Initializa o solver.
        
        Args:
            perfil_aluno: dict, perfil específico (se None, usa aleatório)
            iteracoes: int, número de iterações/melhorias
            threshold_alocacao: float, threshold mínimo para alocar [0.0-1.0]
                - Padrão 0.3: "low" para cima
                - 0.5: "medium" para cima  
                - 0.7: "high" para cima
        """
        self.sistema_fuzzy = criar_sistema_fuzzy()
        self.iteracoes = iteracoes
        self.threshold_alocacao = threshold_alocacao
        
        # Criar indivíduo (plano de curso)
        self.melhor_individuo = Individuo()
        if perfil_aluno:
            self.melhor_individuo.perfil = perfil_aluno
        else:
                self.melhor_individuo.gerar_perfil_random()
        
        # Usar disciplinas fixas do primeiro semestre
        self.melhor_individuo.grade[0] = PRIMEIRO_SEMESTRE_FIXO.copy()
        
        # Resto do plano começa como vazio
        for i in range(1, SEMESTRES_MAX):
            self.melhor_individuo.grade[i] = []
        
        self.melhor_fitness = float('inf')
        self.historico_fitness = []
        self.historico_tempo = []
        
    def _obter_disciplinas_elegveis(self, semestre_atual):
        """
        Obtém disciplinas que podem ser cursadas no semestre atual.
        
        Retorna: lista de (id_disciplina, dados_disciplina)
        """
        # Disciplinas já cursadas
        cursadas = set()
        for sem in range(semestre_atual):
            cursadas.update(self.melhor_individuo.grade[sem])
        
        # Disciplinas já alocadas para semestres futuros
        ja_alocadas = set()
        for sem in range(semestre_atual, SEMESTRES_MAX):
            ja_alocadas.update(self.melhor_individuo.grade[sem])
        
        elegveis = []
        for disc_id, disc_info in disciplinas.items():
            # Não incluir se já alocada
            if disc_id in ja_alocadas:
                continue
            
            # Não incluir se já cursada
            if disc_id in cursadas:
                continue
            
            # Verificar pré-requisitos
            prereqs_atendidos = all(p in cursadas for p in disc_info['prereq'])
            if not prereqs_atendidos:
                continue
            
            elegveis.append((disc_id, disc_info))
        
        return elegveis
    
    def _ranked_por_fuzzy(self, disciplinas_elegveis, semestre_atual):
        """
        Ranqueia disciplinas elegíveis usando scores fuzzy.
        
        Retorna: lista sorted de (id_disciplina, dados, score_fuzzy)
        """
        ranked = []
        
        # Calcular carga atual do semestre
        carga_atual = sum(
            disciplinas[d]['carga'] for d in self.melhor_individuo.grade[semestre_atual]
        )
        
        for disc_id, disc_info in disciplinas_elegveis:
            score_fuzzy = self.sistema_fuzzy.calcular_score_alocacao(
                carga_atual,
                disc_info['dificuldade'],
                semestre_atual
            )
            ranked.append((disc_id, disc_info, score_fuzzy))
        
        # Sort por score descending (melhor primeiro)
        ranked.sort(key=lambda x: x[2], reverse=True)
        return ranked
    
    def _construir_plano_fuzzy(self):
        """
        Constrói um plano de curso usando lógica fuzzy.
        
        Algoritmo:
        - Para cada semestre, ranquear disciplinas elegíveis por score fuzzy
        - Alocar disciplinas with score alto, respeitando carga máxima
        - Avançar para próximo semestre
        """
        import logging
        
        for semestre in range(1, SEMESTRES_MAX):
            elegveis = self._obter_disciplinas_elegveis(semestre)
            
            if not elegveis:
                # Nenhuma disciplina elegível, passar
                logging.debug(f"Semestre {semestre}: nenhuma disciplina elegível")
                continue
            
            # Ranquear por fuzzy
            ranked = self._ranked_por_fuzzy(elegveis, semestre)
            
            # Alocar disciplinas com score >= threshold, até carga máxima
            carga_atual = sum(
                disciplinas[d]['carga'] for d in self.melhor_individuo.grade[semestre]
            )
            
            for disc_id, disc_info, score_fuzzy in ranked:
                # Threshold: só aloca se score >= threshold_alocacao
                if score_fuzzy < self.threshold_alocacao:
                    continue
                
                nova_carga = carga_atual + disc_info['carga']
                
                # Respeitar carga máxima
                if nova_carga > CARGA_MAX_SEMESTRE:
                    continue
                
                self.melhor_individuo.grade[semestre].append(disc_id)
                carga_atual = nova_carga
    
    def _aplicar_reparacao(self, individuo=None):
        """
        Repara o plano (similar ao reparo.py do GA).
        Valida a grade após reparação.
        
        Args:
            individuo: Individuo a reparar. Se None, usa self.melhor_individuo
        """
        from reparo import reparar_individuo
        
        if individuo is None:
            individuo = self.melhor_individuo
        
        reparar_individuo(individuo)
        
        # Validação básica da grade após reparação
        self._validar_grade(individuo)
    
    def _validar_grade(self, individuo):
        """
        Valida a grade do indivíduo com checagens básicas.
        
        Checagens:
        - Todos códigos de disciplina existem em disciplinas
        - Não há duplicatas em semestres
        - Primeiro semestre tem PRIMEIRO_SEMESTRE_FIXO
        """
        import logging
        
        todas_disc = []
        for sem_idx, semestre in enumerate(individuo.grade):
            # Verificar códigos válidos
            for disc in semestre:
                if disc not in disciplinas:
                    raise ValueError(f"Semestre {sem_idx}: Disciplina inválida '{disc}'")
                todas_disc.append(disc)
        
        # Verificar duplicatas
        if len(todas_disc) != len(set(todas_disc)):
            raise ValueError("Duplicatas de disciplinas na grade")
        
        # Verificar primeiro semestre
        primeiro_sem_set = set(individuo.grade[0])
        fixo_set = set(PRIMEIRO_SEMESTRE_FIXO)
        if not fixo_set.issubset(primeiro_sem_set):
            logging.warning(
                f"Primeiro semestre não contempla todas as disciplinas fixas. "
                f"Faltam: {fixo_set - primeiro_sem_set}"
            )
    
    def resolver(self):
        """
        Executa o solver fuzzy com busca local (hill-climbing).
        
        Estratégia:
        - Iteração 0: Construir plano novo com fuzzy
        - Iterações 1+: Fazer pequenas mutações (mover disciplinas entre semestres próximos)
        - Aceitar melhoria; rejeitar piora (hill-climbing puro)
        """
        from ga import fitness
        
        # Iteração 0: Construir plano inicial com fuzzy
        novo_individuo = Individuo()
        novo_individuo.perfil = deepcopy(self.melhor_individuo.perfil)
        novo_individuo.grade[0] = PRIMEIRO_SEMESTRE_FIXO.copy()
        for i in range(1, SEMESTRES_MAX):
            novo_individuo.grade[i] = []
        
        self.melhor_individuo = novo_individuo
        self._construir_plano_fuzzy()
        self._aplicar_reparacao()
        
        novo_fitness = fitness(self.melhor_individuo)
        self.melhor_individuo.fitness = novo_fitness
        tempo, reprov = simular(self.melhor_individuo, self.melhor_individuo.perfil)[0:2]
        self.melhor_individuo.tempo_formatura = tempo
        self.melhor_individuo.reprovacoes = reprov
        
        self.melhor_fitness = novo_fitness
        self.historico_fitness.append(self.melhor_fitness)
        self.historico_tempo.append(self.melhor_individuo.tempo_formatura)
        
        # Iterações 1+: Busca local com mutações pequenas
        for iteracao in range(1, self.iteracoes):
            # Copiar melhor candidato
            candidato = deepcopy(self.melhor_individuo)
            
            # Fazer mutação pequena: permute disciplinas entre semestres próximos
            self._mutar_localmente(candidato)
            
            # Reparar o candidato (não self.melhor_individuo)
            self._aplicar_reparacao(candidato)
            
            # Avaliar
            novo_fitness = fitness(candidato)
            candidato.fitness = novo_fitness
            tempo, reprov = simular(candidato, candidato.perfil)[0:2]
            candidato.tempo_formatura = tempo
            candidato.reprovacoes = reprov
            
            # Hill-climbing: aceitar se melhorar
            if novo_fitness < self.melhor_fitness:
                self.melhor_individuo = candidato
                self.melhor_fitness = novo_fitness
                if iteracao % 5 == 0:
                    print(f"Iteração {iteracao}: Novo melhor fitness = {novo_fitness:.2f}, "
                          f"Tempo = {self.melhor_individuo.tempo_formatura:.1f} semestres")
            # Senão: descartar candidato (não aceitamos piora)
            
            self.historico_fitness.append(self.melhor_fitness)
            self.historico_tempo.append(self.melhor_individuo.tempo_formatura)
    
    def _mutar_localmente(self, individuo):
        """
        Aplica pequenas mutações: move disciplinas entre semestres próximos.
        
        Isso permite exploração local do espaço de soluções sem
        descartar a estrutura da grade atual.
        """
        # Selecionar um semestre aleatório (não primeiro)
        sem_origem = random.randint(1, SEMESTRES_MAX - 2)
        
        if not individuo.grade[sem_origem]:  # Vazio
            return
        
        # Selecionar semestre vizinho (sem_origem ± 1)
        sem_destino = sem_origem + random.choice([-1, 1])
        if sem_destino < 1 or sem_destino >= SEMESTRES_MAX:
            return
        
        # Mover uma disciplina aleatória
        disc = random.choice(individuo.grade[sem_origem])
        
        # Checar se é viável mover
        carga_destino = sum(
            disciplinas[d]['carga'] for d in individuo.grade[sem_destino]
        )
        if carga_destino + disciplinas[disc]['carga'] > CARGA_MAX_SEMESTRE:
            return  # Não é viável, desistir
        
        # Mover
        individuo.grade[sem_origem].remove(disc)
        individuo.grade[sem_destino].append(disc)
    
    def obter_resultado(self):
        """Retorna o melhor plano encontrado."""
        return self.melhor_individuo


def resolver_com_fuzzy(seed=None, iteracoes=50):
    """
    Função helper para resolver o problema com fuzzy.
    
    Args:
        seed: int, seed para reproducibilidade
        iteracoes: int, número de iterações
    
    Returns:
        tuple: (individuo_melhor, historico_fitness, historico_tempo)
    """
    if seed is not None:
        random.seed(seed)
    
    solver = FuzzySolver(iteracoes=iteracoes)
    solver.resolver()
    
    return solver.melhor_individuo, solver.historico_fitness, solver.historico_tempo
