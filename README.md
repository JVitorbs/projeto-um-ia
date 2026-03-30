# Projeto: Otimização de Plano de Curso com Algoritmo Genético

## 1. Objetivo do Problema

Minimizar o tempo necessário para concluir o curso de Engenharia de Computação, considerando:

- Pré-requisitos
- Limite de carga horária por semestre
- Dificuldade das disciplinas
- Reprovações probabilísticas
- Carga mínima de optativas
- Características do aluno

**Formalmente:**

```
minimizar: tempo_total_formatura
sujeito a: restrições curriculares
```

## Reprodutibilidade (Seed)

O projeto usa uma seed fixa por padrão para que você consiga repetir o mesmo experimento.

- Seed padrão em `config.py`: `SEED_EXPERIMENTO = 20260325`
- Para mudar sem editar código, execute com variável de ambiente:

```bash
SEED_EXPERIMENTO=12345 python main.py
```

Se mantiver a mesma seed e os mesmos parâmetros, o resultado do experimento será replicável.

---

## 2. Representação da Solução (Cromossomo)

Cada indivíduo representa um **plano completo de curso**.

**Estrutura:**

```python
cromossomo = [
    semestre1,
    semestre2,
    semestre3,
    ...
    semestreN
]
```

Cada semestre é uma lista de disciplinas:

```python
semestre = [disciplina1, disciplina2, disciplina3]
```

**Exemplo:**

```python
[
    ["Matemática Básica", "Lógica de Programação"],
    ["Cálculo I", "Programação"],
    ["Cálculo II", "Estruturas de Dados"],
    ...
]
```

**Número máximo de semestres considerados:**

```python
SEMESTRES_MAX = 12
```

---

## 3. Dados do Problema

### 3.1 Disciplinas

Cada disciplina possui:

| Campo          | Descrição                        |
|----------------|----------------------------------|
| `nome`         | Nome da disciplina               |
| `carga_horaria`| Carga horária em horas           |
| `dificuldade`  | Nível de dificuldade             |
| `prerequisitos`| Lista de pré-requisitos          |
| `tipo`         | `obrigatoria` ou `optativa`      |

**Exemplo:**

```python
disciplina = {
    "nome": "Cálculo II",
    "carga": 60,
    "dificuldade": 0.8,
    "prereq": ["Cálculo I"],
    "tipo": "obrigatoria"
}
```

### 3.2 Dificuldade

Na versão atual, a dificuldade não é categórica. Cada disciplina já possui um valor numérico próprio, normalmente entre `0.3` e `0.9`, e esse valor entra diretamente como base da probabilidade de reprovação.

Leitura prática dos valores:

- `0.3` a `0.4`: disciplinas mais leves
- `0.5` a `0.7`: disciplinas intermediárias
- `0.8` ou mais: disciplinas pesadas

### 3.3 Optativas

```python
CARGA_OPTATIVAS_MIN = 360  # horas
```

### 3.4 Limite de Carga por Semestre

```python
CARGA_MAX_SEMESTRE = 480  # horas
```

---

## 4. Características do Aluno

Essas variáveis afetam a probabilidade de reprovação:

```python
perfil_aluno = {
    "trabalha":       True,  # bool  — aluno empregado fora da faculdade
    "estagio":        False, # bool  — estágio supervisionado
    "ic":             False, # bool  — iniciação científica
    "escola_publica": True,  # bool  — egresso de escola pública
    "mora_na_cidade": True,  # bool  — False = mora em outra cidade / alto deslocamento
    "horas_estudo":   15,    # int   — horas de estudo por semana
}
```

---

## 5. Restrições do Problema

### 5.1 Pré-requisitos

Uma disciplina só pode ser cursada se todos os seus pré-requisitos foram aprovados em semestres anteriores:

```
todos_prerequisitos_aprovados == True
```

### 5.2 Carga Horária

A carga total por semestre não pode exceder o limite:

```
carga_semestre ≤ CARGA_MAX_SEMESTRE
```

### 5.3 Optativas

A soma das cargas das optativas cursadas deve atingir o mínimo exigido:

```
carga_optativas ≥ CARGA_OPTATIVAS_MIN
```

---

## 6. Simulação de Reprovação

**Probabilidade base:**

```
P(reprovação) = dificuldade_disciplina
```

**Ajustes:**

| Condição                              | Ajuste              |
|---------------------------------------|---------------------|
| Aluno trabalha (`trabalha: True`)     | +0.25               |
| Aluno faz estágio (`estagio: True`)   | +0.15               |
| Aluno faz IC (`ic: True`)             | +0.10               |
| Egresso escola pública (`escola_publica: True`) | +0.20      |
| Mora fora da cidade (`mora_na_cidade: False`) | +0.10      |
| Carga do semestre > 360h              | +0.17               |
| ≥ 3 disciplinas difíceis no semestre  | +0.20               |
| Por hora de estudo semanal            | −0.01 × horas       |

A probabilidade final é limitada ao intervalo **[0.05, 0.95]**.

Hoje o algoritmo considera explicitamente os dados do indivíduo:

- cada indivíduo da população possui um `perfil` próprio
- esse perfil altera a chance de reprovação de cada disciplina
- o desempenho final do indivíduo depende da combinação entre seu perfil e sua grade

Em outras palavras, a grade não é avaliada sozinha: ela é avaliada junto com o tipo de aluno que vai cursá-la.

**Simulação:**

```python
if random() < probabilidade:
    disciplina_reprovada
```

---

## 7. Função de Avaliação (Fitness)

O algoritmo **minimiza** a seguinte função (quanto menor, melhor):

```
fitness =
    tempo_total_semestres
    + 0.5 × número_reprovações
    + 5   × violações_pré-requisito
    + 3   × violações_carga
    + 4   × optativas_insuficientes
```

Na implementação atual, o fitness de cada indivíduo é calculado pela **média de 3 simulações** para reduzir ruído estocástico.

---

## 8. Estrutura do Algoritmo Genético

**Fluxo geral:**

```
1. Gerar população inicial
2. Avaliar indivíduos
3. Repetir até critério de parada:
    a. Selecionar pais
    b. Realizar crossover
    c. Aplicar mutação
    d. Avaliar nova população
    e. Aplicar elitismo
```

---

## 9. Parâmetros do Algoritmo

| Parâmetro              | Valor |
|------------------------|-------|
| Tamanho da população   | 150   |
| Número máx. de gerações| 500   |
| Critério de parada alt.| 100 gerações sem melhoria |
| Taxa de crossover      | 0.85  |
| Mutação base           | 0.30  |
| Mutação máxima         | 0.60  |
| Elitismo               | 2     |
| Torneio                | 3     |
| Taxa de imigrantes     | 0.15  |

```python
POPULACAO = 150
GERACOES = 500
SEM_MELHORIA_STOP = 100
CROSSOVER_RATE = 0.85
MUTATION_RATE = 0.30
MUTATION_MAX = 0.60
ELITE = 2
TORNEIO = 3
TAXA_IMIGRANTES = 0.15
```

---

## 10. Estratégia de Seleção

**Método:** Seleção por torneio

```python
TORNEIO = 3
```

**Procedimento:**

1. Selecionar 3 indivíduos aleatórios
2. Escolher o melhor (menor fitness)

---

## 11. Crossover

**Tipo:** Crossover por semestre

```python
CROSSOVER_RATE = 0.85
```

**Procedimento:**

1. Escolher ponto de corte
2. Combinar semestres dos dois pais
3. Remover disciplinas duplicadas
4. Reparar a grade para restaurar as restrições
5. Herdar o perfil de um dos pais

---

## 12. Mutação

```python
MUTATION_RATE = 0.30
```

**Operadores atualmente implementados:**

| Tipo | Descrição | Participação |
|------|-----------|--------------|
| Movimento aleatório | Move uma disciplina entre dois semestres aleatórios | 60% |
| Antecipação | Tenta puxar uma disciplina de um semestre posterior para um semestre anterior | 40% |

Após a mutação, a grade passa novamente pelo reparo para respeitar pré-requisitos, carga horária e seleção mínima de optativas.

---

## 13. Elitismo

```python
ELITE = 2
```

Os `ELITE` melhores indivíduos são **preservados automaticamente** a cada geração, garantindo que os melhores resultados nunca sejam perdidos.

---
