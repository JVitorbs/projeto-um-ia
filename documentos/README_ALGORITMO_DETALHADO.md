# Processo Completo do Algoritmo (Detalhado)

Este documento descreve, de ponta a ponta, como o algoritmo genetico do projeto funciona na pratica: da representacao de individuo ate a geracao de logs e graficos.

## 1. Visao geral do problema

O problema e montar uma grade de disciplinas para um aluno de Engenharia de Computacao minimizando custo academico total de formatura.

O custo (fitness) nao depende apenas da grade em si. Ele depende de:
- estrutura curricular (pre-requisitos e cargas)
- perfil do aluno
- comportamento estocastico de reprovacao
- efeitos de atraso por pendencias de disciplina

## 2. Mapa dos modulos

- `main.py`: orquestracao do GA e relatorios finais
- `individuo.py`: estrutura do individuo (grade + perfil + metricas)
- `reparo.py`: garante consistencia da grade apos criacao/crossover/mutacao
- `ga.py`: calculo do fitness e selecao por torneio
- `simulation.py`: simulacao academica detalhada
- `crossover.py`: recombinacao dos pais
- `mutacao.py`: alteracoes aleatorias na grade
- `disciplinas.py`: base curricular (nome, carga, dificuldade, prereq, tipo)
- `logger.py`: salva JSON em `logs/evolucao.json`
- `plot.py`: painel completo de monitoramento
- `plot_dispersao_evolucao.py`: painel reduzido de evolucao + dispersao

## 3. Representacao de um individuo

Cada individuo e um candidato de plano de curso:

- `grade`: lista de semestres (`SEMESTRES_MAX`), cada semestre com codigos de disciplinas
- `perfil`: caracteristicas do aluno
- metricas de avaliacao: `fitness`, `tempo_formatura`, `reprovacoes`, `violacoes_*`, etc.

Perfil aleatorio atual (`individuo.py`):
- `trabalha` com probabilidade de 20%
- `estagio` com probabilidade de 25%
- `ic` com probabilidade de 20%
- `escola_publica` com probabilidade de 55%
- `mora_na_cidade` com probabilidade de 55%
- `horas_estudo` inteiro entre 2 e 20

## 4. Inicializacao da populacao

Em `main.py`, o algoritmo cria `POPULACAO` individuos.

Para cada individuo:
1. Gera perfil aleatorio.
2. Monta uma grade inicial aleatoria com obrigatorias + optativas minimas.
3. Passa no reparo (`reparar_individuo`) para corrigir inconsistencias.

## 5. Reparo de grade (restricoes estruturais)

O reparo em `reparo.py` reconstrui a grade com base em prioridade herdada da ordem existente e aplica restricoes curriculares.

Regras relevantes:
- primeiro semestre fixo (`PRIMEIRO_SEMESTRE_FIXO`)
- satisfacao de pre-requisitos
- carga maxima por semestre (`CARGA_MAX_SEMESTRE`)
- limite de disciplinas dificeis por semestre (`MAX_DIFICEIS_SEMESTRE`)
- selecao de optativas ate atingir `OPTATIVAS_MIN`

Esse passo e critico para manter individuos viaveis apos crossover e mutacao.

## 6. Simulacao academica (core comportamental)

A simulacao (`simulation.py`) avalia uma grade para um perfil de aluno.

### 6.1 Probabilidade de reprovacao

Para cada disciplina tentada:

1. Calcula componente base pela dificuldade da disciplina:
- `base = 0.03 + 0.28 * (dificuldade ** 1.4)`

2. Soma pressao de contexto de vida:
- trabalha, estagio, IC, escola publica, morar fora
- carga academica alta no semestre
- muitas disciplinas dificeis no semestre

3. Aplica alivio por estudo:
- funcao logaritmica de `horas_estudo`

4. Combina tudo:
- `prob = base + PESO_CONTEXTO_REPROVACAO * pressao_contexto - alivio_estudo`
- truncado para intervalo `[0.03, 0.85]`

### 6.2 Dinamica de pendencias

Diferente de um contador simples de reprovar/aprovar, a simulacao atual usa pendencias:
- disciplina reprovada volta para fila de pendentes
- disciplina bloqueada por pre-requisito tambem vai para pendente
- pendentes entram com prioridade nos semestres seguintes

Isso cria atraso real de formatura.

### 6.3 Horizonte de simulacao

A simulacao considera:
- grade planejada: `SEMESTRES_MAX`
- janela extra para recuperar atrasos: `SEMESTRES_EXTRA_SIMULACAO`

Total maximo simulado:
- `SEMESTRES_MAX + SEMESTRES_EXTRA_SIMULACAO`

### 6.4 Saidas da simulacao

A funcao `simular` retorna:
- `tempo_formatura` (ultimo semestre ativo)
- `reprovacoes`
- `violacoes_prereq`
- `violacoes_carga`
- `optativas_insuficientes`
- `disciplinas_nao_concluidas`

## 7. Funcao de fitness

Em `ga.py`, o fitness e media de `AVALIACOES_POR_FITNESS` simulacoes (hoje 3), reduzindo ruido estocastico.

Formula atual:

`fitness =`
- `tempo_medio`
- `+ PESO_REPROVACAO * reprov_medio`
- `+ PESO_VIOL_PREREQ * viol_prereq_media`
- `+ PESO_VIOL_CARGA * viol_carga_media`
- `+ PESO_OPT_INSUF * opt_insuf_media`
- `+ PESO_DISC_NAO_CONCLUIDA * nao_concluidas_media`

Menor fitness e melhor.

## 8. Ciclo evolutivo do GA

Em `main.py`, para cada geracao:

1. Avalia todos os individuos (`fitness`).
2. Ordena por fitness.
3. Atualiza melhor global e contador de estagnacao (`sem_melhoria`).
4. Registra estatisticas da geracao (`hist`).
5. Gera nova populacao com:
- elitismo (`ELITE`)
- selecao por torneio (`TORNEIO`)
- crossover com probabilidade `CROSSOVER_RATE`
- mutacao com taxa adaptativa

6. Se houver muita estagnacao, injeta imigrantes aleatorios.
7. Para se `sem_melhoria >= SEM_MELHORIA_STOP`.

### 8.1 Taxa de mutacao adaptativa

A taxa efetiva cresce com estagnacao:
- `mutation_rate_efetiva = min(MUTATION_MAX, MUTATION_RATE + sem_melhoria * 0.005)`

Objetivo: aumentar exploracao quando a populacao para de melhorar.

### 8.2 Imigrantes

Quando `sem_melhoria >= 20`, parte da populacao e substituida por individuos novos:
- `qtd = POPULACAO * TAXA_IMIGRANTES`

Objetivo: recuperar diversidade e escapar de minimos locais.

## 9. Operadores geneticos

### 9.1 Selecao

Metodo: torneio (`ga.py`).

Passos:
1. Amostra aleatoria de `TORNEIO` individuos.
2. Escolhe o de menor fitness.

### 9.2 Crossover (`crossover.py`)

1. Escolhe ponto de corte entre semestres.
2. Junta prefixo de um pai com sufixo do outro.
3. Remove duplicatas de disciplina.
4. Repara grade.
5. Filho herda perfil de um dos pais.

### 9.3 Mutacao (`mutacao.py`)

Duas estrategias:
- 60%: mover disciplina entre semestres aleatorios
- 40%: tentar antecipar disciplina para semestre anterior

Depois sempre executa reparo da grade.

## 10. Analise final por categoria de perfil

Depois da evolucao, o `main.py` avalia categorias fixas de perfil (`geral`, `escola_publica`, `ic`, `trabalha`, `estagio`, `fora_cidade`).

Para cada categoria:
1. Testa todos os individuos finais com esse perfil fixado.
2. Faz varias repeticoes (`repeticoes=12`) por individuo.
3. Escolhe individuo referencia com menor `fitness_medio`.
4. Registra:
- `tempo_medio`
- `tempo_min`
- `fitness_medio`
- `reprov_medio`
- `nao_concluidas_media`

A impressao final foi ajustada para ordenar categorias por `tempo_medio`.

## 11. Log gerado

`logger.py` salva em `logs/evolucao.json` um objeto com:
- `historico`: metricas por geracao
- `top3`: melhores individuos finais
- `categorias`: resumo por perfil fixo

Esse formato alimenta os scripts de plot.

## 12. Visualizacao

### 12.1 `plot.py`

Painel completo:
- convergencia de fitness com faixa interquartil
- evolucao de tempo
- diversidade e mutacao
- comparacao entre categorias

Resumo textual:
- categoria destaque por `tempo_medio` (com `tempo_min` como informacao secundaria)

### 12.2 `plot_dispersao_evolucao.py`

Painel simplificado com 2 graficos:
- evolucao do fitness
- dispersao por categoria (`tempo_medio x fitness_medio`)

Se nao houver `categorias`, usa fallback de dispersao evolutiva (`tempo x fitness`, com cor por diversidade).

## 13. Parametros e calibracao

Arquivo central: `config.py`.

Parametros com maior impacto comportamental:
- `PESO_CONTEXTO_REPROVACAO`
- `SEMESTRES_EXTRA_SIMULACAO`
- pesos da fitness (`PESO_*`)
- `MUTATION_RATE` e `MUTATION_MAX`

Boas praticas de ajuste:
- mudar poucos parametros por vez
- comparar multiplas execucoes (devido ao ruido estocastico)
- usar `tempo_medio` para comparacoes entre perfis

## 14. Limites e interpretacao dos resultados

- Nao e previsao deterministica de vida academica real.
- E uma simulacao para comparar politicas de grade/perfil de forma relativa.
- `tempo_min` e otimista; `tempo_medio` e mais robusto.
- Resultados isolados de uma unica seed podem enganar; prefira tendencia.

## 15. Fluxo resumido (pipeline)

1. Criar populacao inicial
2. Repara grades
3. Simular e calcular fitness
4. Selecionar, cruzar, mutar
5. Injetar imigrantes quando estagnar
6. Parar por criterio de sem melhora
7. Avaliar categorias fixas
8. Salvar JSON
9. Plotar resultados
