POPULACAO = 80
POPULACAO = 150
GERACOES = 500
SEM_MELHORIA_STOP = 100

CROSSOVER_RATE = 0.85
MUTATION_RATE = 0.30
MUTATION_MAX = 0.60
ELITE = 2
TORNEIO = 3
TAXA_IMIGRANTES = 0.15

CARGA_MAX_SEMESTRE = 480
OPTATIVAS_MIN = 360
SEMESTRES_MAX = 12

# Pesos da funcao de fitness (quanto maior, maior penalizacao)
PESO_REPROVACAO = 1.5
PESO_VIOL_PREREQ = 5.0
PESO_VIOL_CARGA = 3.0
PESO_OPT_INSUF = 4.0
PESO_DISC_NAO_CONCLUIDA = 8.0

# Fator que converte pressao de contexto de vida em acrescimo de probabilidade
# de reprovacao. Aumentar este valor torna o perfil do aluno mais influente.
PESO_CONTEXTO_REPROVACAO = 0.16

# Semestres extras permitidos na simulacao para pagar disciplinas atrasadas
# por reprovacao ou bloqueio de pre-requisitos.
SEMESTRES_EXTRA_SIMULACAO = 8