"""
Módulo de Lógica Fuzzy para Otimização de Plano de Curso

Define conjuntos fuzzy, funções de pertencimento e regras
de inferência para alocar disciplinas nos semestres.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from config import CARGA_MAX_SEMESTRE


class SistemaFuzzyAlocacao:
    """
    Sistema de inferência fuzzy Mamdani para decidir alocação de disciplinas.
    
    Variáveis de entrada:
    - carga_semestre: carga horária atualmente no semestre [0-120]
    - dificuldade_disciplina: dificuldade da disciplina [0.3-0.9]
    - semestres_cursados: quantos semestres o aluno já cursou [0-20]
    
    Variável de saída:
    - score_alocacao: score para alocar a disciplina [0-1]
        1.0 = muito desejável alocar
        0.0 = não recomendado alocar
    """
    
    def __init__(self):
        """Inicializa o sistema fuzzy com variáveis e regras."""
        self._criar_variaveis()
        self._criar_regras()
        self._compilar_sistema()
    
    def _criar_variaveis(self):
        """Define as variáveis fuzzy de entrada/saída."""
        # Variável 1: Carga horária atual do semestre
        self.carga_semestre = ctrl.Antecedent(
            np.arange(0, CARGA_MAX_SEMESTRE + 30, 1),
            'carga_semestre'
        )
        self.carga_semestre['baixa'] = fuzz.trimf(
            self.carga_semestre.universe, [0, 0, CARGA_MAX_SEMESTRE * 0.4]
        )
        self.carga_semestre['media'] = fuzz.trimf(
            self.carga_semestre.universe,
            [CARGA_MAX_SEMESTRE * 0.3, CARGA_MAX_SEMESTRE * 0.6, CARGA_MAX_SEMESTRE * 0.9]
        )
        self.carga_semestre['alta'] = fuzz.trimf(
            self.carga_semestre.universe,
            [CARGA_MAX_SEMESTRE * 0.7, CARGA_MAX_SEMESTRE, CARGA_MAX_SEMESTRE + 30]
        )
        
        # Variável 2: Dificuldade da disciplina
        self.dificuldade = ctrl.Antecedent(np.arange(0, 1.1, 0.01), 'dificuldade')
        self.dificuldade['facil'] = fuzz.trimf(self.dificuldade.universe, [0, 0, 0.5])
        self.dificuldade['media_dif'] = fuzz.trimf(self.dificuldade.universe, [0.3, 0.6, 0.9])
        self.dificuldade['dificil'] = fuzz.trimf(self.dificuldade.universe, [0.7, 1.0, 1.1])
        
        # Variável 3: Semestres já cursados (para balancear progresso)
        self.semestres_cursados = ctrl.Antecedent(np.arange(0, 21, 1), 'semestres_cursados')
        self.semestres_cursados['inicio'] = fuzz.trimf(self.semestres_cursados.universe, [0, 0, 4])
        self.semestres_cursados['meio'] = fuzz.trimf(self.semestres_cursados.universe, [2, 8, 14])
        self.semestres_cursados['final'] = fuzz.trimf(self.semestres_cursados.universe, [10, 20, 20])
        
        # Variável de saída: Score de alocação
        self.score_alocacao = ctrl.Consequent(np.arange(0, 1.1, 0.01), 'score_alocacao')
        self.score_alocacao['very_low'] = fuzz.trimf(self.score_alocacao.universe, [0, 0, 0.2])
        self.score_alocacao['low'] = fuzz.trimf(self.score_alocacao.universe, [0, 0.25, 0.5])
        self.score_alocacao['medium'] = fuzz.trimf(self.score_alocacao.universe, [0.25, 0.5, 0.75])
        self.score_alocacao['high'] = fuzz.trimf(self.score_alocacao.universe, [0.5, 0.75, 1.0])
        self.score_alocacao['very_high'] = fuzz.trimf(self.score_alocacao.universe, [0.8, 1.0, 1.1])
    
    def _criar_regras(self):
        """Define as regras de inferência fuzzy."""
        self.regras = [
            # Regra 1: Carga baixa sempre favorece alocação
            ctrl.Rule(self.carga_semestre['baixa'], self.score_alocacao['very_high']),
            
            # Regra 2: Carga média com disciplina fácil → aloca
            ctrl.Rule(
                self.carga_semestre['media'] & self.dificuldade['facil'],
                self.score_alocacao['high']
            ),
            
            # Regra 3: Carga alta com disciplina difícil → não aloca
            ctrl.Rule(
                self.carga_semestre['alta'] & self.dificuldade['dificil'],
                self.score_alocacao['very_low']
            ),
            
            # Regra 4: Carga alta com disciplina fácil → considera (médio)
            ctrl.Rule(
                self.carga_semestre['alta'] & self.dificuldade['facil'],
                self.score_alocacao['medium']
            ),
            
            # Regra 5: Carga média com disciplina difícil → médio-baixo
            ctrl.Rule(
                self.carga_semestre['media'] & self.dificuldade['dificil'],
                self.score_alocacao['low']
            ),
            
            # Regra 6: Carga média com disciplina média → médio
            ctrl.Rule(
                self.carga_semestre['media'] & self.dificuldade['media_dif'],
                self.score_alocacao['medium']
            ),
            
            # Regra 7: Início do curso amplifica score (menos exigente)
            ctrl.Rule(
                self.semestres_cursados['inicio'] & self.dificuldade['facil'],
                self.score_alocacao['very_high']
            ),
            
            # Regra 8: Final do curso com dificuldade alta reduz score (CORRIGIDA: sem restrição de carga)
            ctrl.Rule(
                self.semestres_cursados['final'] & self.dificuldade['dificil'],
                self.score_alocacao['low']
            ),
            
            # Regra 9: Carga alta com média dificuldade reduz score
            ctrl.Rule(
                self.carga_semestre['alta'] & self.dificuldade['media_dif'],
                self.score_alocacao['low']
            ),
            
            # Regra 10: Início com disciplina difícil (desafio balanceado)
            ctrl.Rule(
                self.semestres_cursados['inicio'] & self.dificuldade['dificil'],
                self.score_alocacao['medium']
            ),
            
            # Regra 11: Final com disciplina fácil (consolidação)
            ctrl.Rule(
                self.semestres_cursados['final'] & self.dificuldade['facil'],
                self.score_alocacao['high']
            ),
        ]
    
    def _compilar_sistema(self):
        """Compila o sistema de controle fuzzy."""
        self.sistema = ctrl.ControlSystem(self.regras)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema)
    
    def calcular_score_alocacao(self, carga_semestre, dificuldade_disciplina, semestres_cursados):
        """
        Calcula o score fuzzy para alocar uma disciplina.
        
        Args:
            carga_semestre: float, carga horária atual no semestre [0-120]
            dificuldade_disciplina: float, dificuldade [0.3-0.9]
            semestres_cursados: int, número de semestres cursados [0-20]
        
        Returns:
            float: score de alocação [0.0-1.0]
        """
        try:
            # Reset explícito do simulador para garantir estado limpo
            self.simulador = ctrl.ControlSystemSimulation(self.sistema)
            
            # Validar e clipar inputs para garantir espaço fuzzy válido
            carga_semestre = np.clip(carga_semestre, 0, 600)
            dificuldade_disciplina = np.clip(dificuldade_disciplina, 0, 1.1)
            semestres_cursados = np.clip(semestres_cursados, 0, 20)
            
            self.simulador.input['carga_semestre'] = carga_semestre
            self.simulador.input['dificuldade'] = dificuldade_disciplina
            self.simulador.input['semestres_cursados'] = semestres_cursados
            
            self.simulador.compute()
            
            score = self.simulador.output['score_alocacao']
            # Garantir que score está no intervalo [0, 1]
            return np.clip(score, 0.0, 1.0)
        except Exception as e:
            import logging
            logging.warning(
                f"Erro ao calcular score fuzzy com inputs "
                f"(carga={carga_semestre}, dif={dificuldade_disciplina}, sem={semestres_cursados}): {e}"
            )
            return 0.5  # Valor neutro em caso de erro
    
    def reset(self):
        """Reseta o simulador."""
        self.simulador = ctrl.ControlSystemSimulation(self.sistema)


def criar_sistema_fuzzy():
    """Factory para criar e retornar o sistema fuzzy."""
    return SistemaFuzzyAlocacao()
