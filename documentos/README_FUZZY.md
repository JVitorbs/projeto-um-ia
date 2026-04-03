# README - Solucao com Logica Fuzzy

Este documento descreve como a abordagem fuzzy foi montada para resolver o mesmo problema do GA: montar um plano de curso de Engenharia de Computacao minimizando tempo de formatura e penalidades de viabilidade academica.

## 1. Objetivo da abordagem fuzzy

A versao fuzzy foi criada para:

- Rodar separada do GA
- Usar regras linguisticas (IF-THEN) para decidir alocacao de disciplinas por semestre
- Manter avaliacao e metricas comparaveis com o restante do projeto
- Salvar resultados em arquivo proprio: `logs/evolucao_fuzzy.json`

Arquivos principais da solucao fuzzy:

- `fuzzy_logic.py`: sistema de inferencia fuzzy (variaveis, funcoes de pertinencia, regras)
- `fuzzy_solver.py`: construcao iterativa do plano usando score fuzzy
- `main_fuzzy.py`: execucao completa, consolidacao de resultados e exportacao JSON

---

## 2. Arquitetura geral

Fluxo da abordagem fuzzy:

1. Inicializa seed do experimento (`SEED_EXPERIMENTO` ou variavel de ambiente)
2. Cria um `FuzzySolver`
3. Em cada iteracao do solver:
   - gera um candidato de grade
   - aplica o sistema fuzzy para ranquear disciplinas elegiveis
   - aloca disciplinas respeitando carga maxima
   - aplica reparo (`reparo.py`) para consistencia
   - avalia com a mesma fitness do projeto (`ga.fitness`) e `simulation.simular`
4. Repete o processo em multiplas tentativas (simulando uma populacao)
5. Gera resumo (`historico`, `top3`, `categorias`) e salva em `logs/evolucao_fuzzy.json`

Observacao importante: o fuzzy nao usa crossover/mutacao; ele usa inferencia fuzzy + busca iterativa com retencao do melhor.

---

## 3. Sistema fuzzy (`fuzzy_logic.py`)

A implementacao usa `scikit-fuzzy` com modelo **Mamdani**.

### 3.1 Variaveis de entrada

1. `carga_semestre`
- Universo: `0` ate `CARGA_MAX_SEMESTRE + 30`
- Com `config.py` atual (`CARGA_MAX_SEMESTRE = 480`), o universo fica `0..510`
- Conjuntos fuzzy:
  - `baixa`: triangular `[0, 0, 0.4 * CARGA_MAX_SEMESTRE]`
  - `media`: triangular `[0.3 * CARGA_MAX_SEMESTRE, 0.6 * CARGA_MAX_SEMESTRE, 0.9 * CARGA_MAX_SEMESTRE]`
  - `alta`: triangular `[0.7 * CARGA_MAX_SEMESTRE, CARGA_MAX_SEMESTRE, CARGA_MAX_SEMESTRE + 30]`

2. `dificuldade`
- Universo: `0..1.1`
- Conjuntos fuzzy:
  - `facil`: `[0, 0, 0.5]`
  - `media_dif`: `[0.3, 0.6, 0.9]`
  - `dificil`: `[0.7, 1.0, 1.1]`

3. `semestres_cursados`
- Universo: `0..20`
- Conjuntos fuzzy:
  - `inicio`: `[0, 0, 4]`
  - `meio`: `[2, 8, 14]`
  - `final`: `[10, 20, 20]`

### 3.2 Variavel de saida

`score_alocacao`
- Universo: `0..1.1`
- Conjuntos fuzzy:
  - `very_low`: `[0, 0, 0.2]`
  - `low`: `[0, 0.25, 0.5]`
  - `medium`: `[0.25, 0.5, 0.75]`
  - `high`: `[0.5, 0.75, 1.0]`
  - `very_high`: `[0.8, 1.0, 1.1]`

### 3.3 Regras fuzzy implementadas

As regras atuais no codigo sao:

1. IF `carga_semestre` is `baixa` THEN `score_alocacao` is `very_high`
2. IF `carga_semestre` is `media` AND `dificuldade` is `facil` THEN `high`
3. IF `carga_semestre` is `alta` AND `dificuldade` is `dificil` THEN `very_low`
4. IF `carga_semestre` is `alta` AND `dificuldade` is `facil` THEN `medium`
5. IF `carga_semestre` is `media` AND `dificuldade` is `dificil` THEN `low`
6. IF `carga_semestre` is `media` AND `dificuldade` is `media_dif` THEN `medium`
7. IF `semestres_cursados` is `inicio` AND `dificuldade` is `facil` THEN `very_high`
8. IF `semestres_cursados` is `final` AND `dificuldade` is `dificil` AND `carga_semestre` is `media` THEN `low`

### 3.4 Defuzzificacao

A biblioteca `skfuzzy.control` calcula o valor crisp de `score_alocacao`.
No fim, o score eh truncado para `[0, 1]` com `np.clip`.

---

## 4. Solver fuzzy (`fuzzy_solver.py`)

Classe principal: `FuzzySolver`

### 4.1 Estado principal

- `self.melhor_individuo`: melhor plano encontrado ate o momento
- `self.melhor_fitness`: melhor fitness acumulada
- `self.historico_fitness`: fitness do melhor ao longo das iteracoes
- `self.historico_tempo`: tempo do melhor ao longo das iteracoes

### 4.2 Estrategia de construcao de plano

Para cada semestre (2 ao 12):

1. Seleciona disciplinas elegiveis:
- nao cursadas anteriormente
- nao alocadas em outros semestres
- prerequisitos satisfeitos

2. Calcula score fuzzy para cada disciplina elegivel:
- entradas: `carga_atual_semestre`, `dificuldade_disciplina`, `semestre_atual`

3. Ordena por score decrescente

4. Aloca disciplina se:
- `score_fuzzy >= 0.3` (threshold)
- nova carga nao ultrapassa `CARGA_MAX_SEMESTRE`

5. Aplica reparo via `reparo.reparar_individuo`

6. Avalia com:
- `ga.fitness(individuo)`
- `simulation.simular(individuo, perfil)`

7. Mantem apenas melhoria:
- se fitness piorar, restaura individuo anterior

### 4.3 Sobre iteracoes

Cada iteracao reconstrói um candidato e compara com o melhor acumulado.
Isso funciona como uma busca iterativa guiada por regras fuzzy.

---

## 5. Parametros usados

## 5.1 Parametros globais (`config.py`)

- `CARGA_MAX_SEMESTRE = 480`
- `OPTATIVAS_MIN = 360`
- `SEMESTRES_MAX = 12`
- `SEED_EXPERIMENTO = 20260325`

Pesos da fitness (reutilizados do GA):

- `PESO_REPROVACAO = 1.5`
- `PESO_VIOL_PREREQ = 5.0`
- `PESO_VIOL_CARGA = 3.0`
- `PESO_OPT_INSUF = 4.0`
- `PESO_DISC_NAO_CONCLUIDA = 8.0`

## 5.2 Parametros da execucao fuzzy (`main_fuzzy.py`)

Controlaveis por variavel de ambiente:

- `FUZZY_ITERACOES`
  - default: `min(120, GERACOES)`
- `FUZZY_TENTATIVAS`
  - default: `min(40, POPULACAO)`

Exemplo com override:

```bash
FUZZY_ITERACOES=80 FUZZY_TENTATIVAS=30 .venv/bin/python main_fuzzy.py
```

## 5.3 Outros parametros internos da logica fuzzy

- Threshold de alocacao no solver: `score_fuzzy >= 0.3`
- Universos e funcoes triangulares conforme secao 3

---

## 6. Formato da saida fuzzy

Arquivo: `logs/evolucao_fuzzy.json`

Estrutura de alto nivel:

- `seed`
- `historico`
- `top3`
- `categorias`

A estrutura foi mantida compativel com a analise de evolucao e comparacao com GA.

---

## 7. Como executar

## 7.1 Dependencias

```bash
.venv/bin/pip install -r requirements.txt
```

Dependencias relevantes para fuzzy:

- `scikit-fuzzy`
- `scipy`
- `networkx`

## 7.2 Rodar fuzzy

```bash
.venv/bin/python main_fuzzy.py
```

Com parametros customizados:

```bash
SEED_EXPERIMENTO=20260325 FUZZY_ITERACOES=100 FUZZY_TENTATIVAS=35 .venv/bin/python main_fuzzy.py
```

## 7.3 Plot GA e Fuzzy

```bash
.venv/bin/python plot_dispersao_evolucao.py
```

O script atual plota:

1. GA separado
2. Fuzzy separado (se `logs/evolucao_fuzzy.json` existir)
3. Comparacao GA vs Fuzzy

---

## 8. Decisoes de modelagem

- Reaproveitamento da mesma funcao de fitness e simulacao do projeto, para comparabilidade direta com GA
- Uso de regras fuzzy para priorizacao local de disciplinas por semestre
- Reparo estrutural mantido para garantir viabilidade da grade
- Execucao em tentativas multiplas para reduzir dependencia de um unico perfil/estado inicial

---

## 9. Limitacoes e possiveis melhorias

Melhorias tecnicas recomendadas:

- Ajustar/expandir regras fuzzy incluindo variaveis do perfil (trabalha, estagio, horas de estudo) diretamente no sistema de inferencia
- Refinar funcoes de pertinencia com calibracao por dados historicos
- Criar varredura automatica de threshold (`score >= 0.3`) e comparar impacto
- Salvar tambem os hiperparametros usados dentro do JSON de saida para auditoria de experimento
- Incluir metricas de diversidade mais robustas para a populacao fuzzy de tentativas

---

## 10. Resumo rapido

A solucao fuzzy foi montada como um pipeline separado, com inferencia Mamdani para score de alocacao por disciplina, construcao iterativa da grade, reparo de viabilidade e avaliacao com a mesma fitness do projeto original. Assim, ela permite comparacao justa com o GA em termos de tempo, fitness e comportamento por categoria de perfil.
