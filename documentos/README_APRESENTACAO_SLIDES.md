# Guia Completo para Slides - Projeto de Otimizacao de Grade (GA + Fuzzy)

Este documento foi criado para te ajudar a montar uma apresentacao **completa e bem explicada**, cobrindo:

1. O problema e sua motivacao
2. Como o Algoritmo Genetico foi modelado (cromossomo, operadores, fitness)
3. Como a Logica Fuzzy foi modelada (variaveis, regras, inferencia)
4. Resultados numericos e comparativos
5. Graficos/plots recomendados
6. Roteiro de fala para cada slide

---

## 1. Estrutura Recomendada dos Slides (15-20 slides)

## Slide 1 - Titulo

**Titulo sugerido:**

> Otimizacao de Plano de Curso em Engenharia de Computacao:\
> Comparacao entre Algoritmo Genetico e Logica Fuzzy

**Subtitulo:**
- Disciplina de Inteligencia Artificial
- Seu nome + data

---

## Slide 2 - Problema

### O que queremos otimizar?

Montar automaticamente uma grade de disciplinas por semestre que:

- Minimize tempo de formatura
- Minimize reprovacoes esperadas
- Respeite pre-requisitos
- Respeite carga maxima por semestre
- Garanta carga minima de optativas

### Por que isso e dificil?

- Espaco de busca combinatorial enorme
- Restricoes academicas duras
- Diferentes perfis de aluno (trabalha, estagio, IC, etc.)
- Objetivos conflitantes (terminar rapido vs evitar sobrecarga)

---

## Slide 3 - Abordagem Geral

### Metodologias comparadas

1. **Algoritmo Genetico (GA)**
- Busca evolutiva populacional
- Crossover + mutacao + selecao

2. **Logica Fuzzy**
- Regras linguisticas (IF-THEN)
- Decisao local por disciplina/semestre
- Refinamento com busca local (hill-climbing)

### Justificativa da comparacao

- GA: geralmente melhor em otimizacao global
- Fuzzy: maior interpretabilidade das decisoes

---

## Slide 4 - Modelagem dos Dados

### Entidades principais

- Disciplinas: codigo, carga, dificuldade, pre-requisitos, tipo
- Perfil do aluno: trabalha, estagio, IC, escola_publica, horas_estudo, mora_na_cidade
- Grade: lista de semestres com disciplinas

### Restricoes principais (config)

- `CARGA_MAX_SEMESTRE = 480`
- `OPTATIVAS_MIN = 360`
- `SEMESTRES_MAX = 12`

---

## Slide 5 - Representacao do Cromossomo (GA)

### Como o cromossomo foi definido

**Cromossomo = Grade Completa do Aluno**

- Estrutura: lista de 12 semestres
- Cada gene-semestre contem uma lista de codigos de disciplinas
- 1o semestre fixo (grade oficial obrigatoria)

### Exemplo conceitual

```text
Cromossomo C = [S1, S2, S3, ..., S12]
S1 = [ECT3101, ECT3102, ..., ECT3203]  (fixo)
S2 = [DCA3206, ECT3201, ...]
...
S12 = [...]
```

### Por que essa representacao?

- Natural para o problema (semestres ja sao a unidade real)
- Facil aplicar restricoes por semestre
- Facil simular progresso academico

---

## Slide 6 - Funcao de Fitness

### Formula da fitness

A funcao minimiza:

$$
\text{fitness} =
\text{tempo}
+ w_r \cdot \text{reprovacoes}
+ w_p \cdot \text{violacoes\_prereq}
+ w_c \cdot \text{violacoes\_carga}
+ w_o \cdot \text{optativas\_insuficientes}
+ w_n \cdot \text{nao\_concluidas}
$$

Com pesos (config):

- `PESO_REPROVACAO = 1.5`
- `PESO_VIOL_PREREQ = 5.0`
- `PESO_VIOL_CARGA = 3.0`
- `PESO_OPT_INSUF = 4.0`
- `PESO_DISC_NAO_CONCLUIDA = 8.0`

### Interpretacao

- Fitness menor = solucao melhor
- Penalidades altas para inviabilidade estrutural

---

## Slide 7 - Operadores do GA

### Fluxo por geracao

1. Avaliar populacao
2. Selecionar pais (torneio)
3. Aplicar crossover (`CROSSOVER_RATE = 0.85`)
4. Aplicar mutacao (`MUTATION_RATE = 0.30`)
5. Reparar individuos inviaveis
6. Preservar elite (`ELITE = 2`)
7. Atualizar historico de evolucao

### Vantagem principal

- Equilibrio entre exploracao global e refinamento local

---

## Slide 8 - Sistema Fuzzy: Ideia

### O que o fuzzy decide?

Para cada disciplina elegivel em um semestre, calcular:

- `score_alocacao` em `[0, 1]`

Quanto maior o score, maior a chance de alocar.

### Entradas fuzzy

1. `carga_semestre`
2. `dificuldade`
3. `semestres_cursados`

### Saida fuzzy

- `score_alocacao`: very_low, low, medium, high, very_high

---

## Slide 9 - Funcoes de Pertinencia (Fuzzy)

### Exibir graficos das memberships

- `carga_semestre`: baixa, media, alta
- `dificuldade`: facil, media_dif, dificil
- `semestres_cursados`: inicio, meio, final
- `score_alocacao`: very_low..very_high

### Fala sugerida

"As funcoes triangulares transformam valores numericos em conceitos linguisticos, permitindo regras interpretableis."

---

## Slide 10 - Regras Fuzzy

### Exemplos de regras implementadas

1. IF carga baixa THEN score very_high
2. IF carga media AND dificuldade facil THEN high
3. IF carga alta AND dificuldade dificil THEN very_low
4. IF inicio AND dificuldade facil THEN very_high
5. IF final AND dificuldade dificil THEN low

### Por que usar regras?

- Incorporar conhecimento humano do dominio
- Tornar decisao explicavel

---

## Slide 11 - Solver Fuzzy + Hill-Climbing

### Pipeline fuzzy

1. Listar disciplinas elegiveis
2. Ranquear por score fuzzy
3. Alocar respeitando threshold e carga maxima
4. Aplicar reparo estrutural
5. Avaliar fitness
6. Refinar com busca local (mover disciplinas entre semestres)

### Observacao importante

- O fuzzy **tambem usa fitness** para comparar solucoes e aceitar melhorias.

---

## Slide 12 - Resultados Gerais (GA vs Fuzzy)

Use o arquivo:

- `resultados_apresentacao/01_comparativo_geral.txt`

### Mostre

- Melhor fitness de cada metodo
- Melhor tempo de formatura
- Diferenca percentual

### Mensagem chave

- GA teve melhor desempenho global
- Fuzzy entregou solucoes coerentes e explicaveis

---

## Slide 13 - Resultados por Categoria de Aluno

Use arquivos:

- `resultados_apresentacao/02_categorias_ga.txt`
- `resultados_apresentacao/02_categorias_fuzzy.txt`

### Perfis avaliados

- geral
- escola_publica
- ic
- trabalha
- estagio
- fora_cidade

### Plot recomendado

- Barras agrupadas: tempo_medio por categoria (GA vs Fuzzy)
- Barras agrupadas: fitness_medio por categoria (GA vs Fuzzy)

---

## Slide 14 - Top 3 Solucoes

Use arquivos:

- `resultados_apresentacao/03_top3_ga.txt`
- `resultados_apresentacao/03_top3_fuzzy.txt`

### Mostrar

- Fitness, tempo e reprovacoes do top 3
- Perfil associado de cada top

### Ideia visual

- Tabela lado a lado (GA x Fuzzy)

---

## Slide 15 - Evolucao dos Algoritmos

Use arquivos:

- `resultados_apresentacao/04_evolucao_ga.txt`
- `resultados_apresentacao/04_evolucao_fuzzy.txt`

### Plot principal

- Linha `melhor_ate_agora` por geracao/tentativa
- Linha de media populacional
- Faixa quartis (Q1-Q3)

### Interpretacao

- Curva descendente indica convergencia
- Plateau indica estabilizacao/local minima

---

## Slide 16 - Grades dos Melhores (visual forte)

### O que mostrar

- Grade do melhor GA (semestres 1..N)
- Grade do melhor Fuzzy (semestres 1..N)
- Carga por semestre em barras

### Ideia de visual

- Heatmap: semestre no eixo X, carga no eixo Y, intensidade por carga
- Tabela compacta por semestre

---

## Slide 17 - Analise Crtica

### Pontos fortes do GA

- Melhor otimizacao global
- Escape de minimos locais
- Melhor fitness final

### Pontos fortes do Fuzzy

- Interpretabilidade
- Decisao baseada em regras transparentes
- Facilidade de justificar escolhas

### Limites observados

- Fuzzy ainda inferior em performance numerica
- Sensivel a qualidade das regras e threshold

---

## Slide 18 - Conclusao

### Conclusoes principais

1. O problema e complexo e multiobjetivo
2. GA obteve melhores resultados quantitativos
3. Fuzzy gerou solucoes validas e explicaveis
4. Avaliacao por perfil mostrou diferencas importantes

### Trabalhos futuros

- Hibrido GA + Fuzzy
- Calibracao automatica de regras fuzzy
- Analise multiobjetivo (Pareto)

---

## 2. Roteiro de Plotagem (graficos que voce deve gerar)

## Plot A - Evolucao detalhada

**Objetivo:** mostrar convergencia completa

- Eixo X: geracao/tentativa
- Eixo Y: fitness
- Curvas:
  - melhor_ate_agora
  - media
  - pior
- Sombrear Q1-Q3

Dados: `historico` em `logs/evolucao.json` e `logs/evolucao_fuzzy.json`

---

## Plot B - Tempo por categoria (GA vs Fuzzy)

**Objetivo:** comparar robustez por perfil

- Eixo X: categoria
- Eixo Y: tempo_medio
- Duas barras por categoria: GA/Fuzzy

---

## Plot C - Fitness por categoria (GA vs Fuzzy)

**Objetivo:** comparar qualidade por perfil

- Eixo X: categoria
- Eixo Y: fitness_medio
- Duas barras por categoria

---

## Plot D - Reprovacoes por categoria

**Objetivo:** impacto academico por perfil

- Eixo X: categoria
- Eixo Y: reprov_medio
- Duas barras por categoria

---

## Plot E - Carga por semestre (melhor individuo)

**Objetivo:** mostrar distribuicao de esforco ao longo do curso

- Eixo X: semestre
- Eixo Y: carga horaria
- Linha/barras para melhor GA e melhor Fuzzy

---

## Plot F - Radar chart por categoria (opcional)

**Objetivo:** comparacao visual multi-criterio

Dimensoes:

- tempo_medio
- fitness_medio
- reprov_medio
- nao_concluidas_media

---

## 3. Arquivos que ja foram gerados para voce

Ja estao disponiveis em `resultados_apresentacao/`:

1. `01_comparativo_geral.txt`
2. `02_categorias_ga.txt`
3. `02_categorias_fuzzy.txt`
4. `03_top3_ga.txt`
5. `03_top3_fuzzy.txt`
6. `04_evolucao_ga.txt`
7. `04_evolucao_fuzzy.txt`
8. `05_resumo_estatistico.txt`

Use esses textos como base para tabelas e bullets nos slides.

---

## 4. Roteiro de fala (resumido)

### Abertura (1 min)

"Este projeto resolve a montagem automatica de grade de curso considerando restricoes academicas e diferentes perfis de aluno. Comparamos duas abordagens de IA: Algoritmo Genetico e Logica Fuzzy."

### Metodologia (3-4 min)

"No GA, cada individuo representa uma grade completa (cromossomo), evoluida por selecao, crossover e mutacao. No Fuzzy, usamos regras linguisticas para priorizar alocacao de disciplinas, seguido de refinamento local."

### Resultados (3-4 min)

"GA apresentou melhor fitness global, mas o Fuzzy gerou solucoes consistentes e altamente interpretaveis. A avaliacao por categoria mostrou como contexto de vida impacta o desempenho academico."

### Fechamento (1 min)

"Concluimos que GA e superior em desempenho numerico, enquanto Fuzzy agrega explicabilidade. Como futuro trabalho, a combinacao das duas abordagens pode unir desempenho e interpretabilidade."

---

## 5. Checklist antes da apresentacao

- [ ] Conferir se os plots estao legiveis
- [ ] Padronizar cores (GA=azul, Fuzzy=laranja)
- [ ] Garantir que todos os valores numericos batem com os arquivos txt
- [ ] Treinar explicacao da fitness e do cromossomo
- [ ] Treinar explicacao das regras fuzzy com 2-3 exemplos
- [ ] Preparar resposta para: "por que o fuzzy precisa de fitness?"

Resposta curta sugerida:

> "Porque o score fuzzy decide localmente quais disciplinas priorizar, mas a fitness avalia globalmente a qualidade da grade inteira. Sem fitness, nao ha criterio objetivo para comparar e otimizar solucoes."

---

## 6. Comandos uteis

Gerar novamente resultados escritos:

```bash
source .venv/bin/activate
python gerar_resultados_apresentacao.py
```

Gerar resultados principais (se precisar atualizar):

```bash
# GA
python main.py

# Fuzzy
python main_fuzzy.py
```

Gerar plot comparativo existente:

```bash
python plot_dispersao_evolucao.py
```

---

## 7. Sugestao final

Se quiser uma apresentacao realmente forte, monte a narrativa em 3 blocos:

1. **Modelagem cuidadosa do problema** (restricoes reais + perfis)
2. **Comparacao justa de duas IAs diferentes** (GA x Fuzzy)
3. **Insight pratico** (como perfil de aluno muda o plano ideal)

Isso mostra maturidade tecnica e aplicacao real de IA.
