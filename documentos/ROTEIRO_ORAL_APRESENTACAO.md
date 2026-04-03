# Roteiro Oral Completo - Apresentacao do Projeto (GA + Fuzzy)

Este roteiro foi pensado para uma apresentacao de 12 a 18 minutos.
Cada slide tem:

- Objetivo
- Tempo sugerido
- Fala sugerida (natural, pronta para treino)
- Frase de transicao para o proximo slide

---

## Slide 1 - Titulo

### Objetivo
Abrir com contexto e mostrar escopo do trabalho.

### Tempo sugerido
30 a 40 segundos.

### Fala sugerida
Boa tarde. Neste trabalho eu desenvolvi e comparei duas abordagens de Inteligencia Artificial para otimizar a montagem de grade de curso em Engenharia de Computacao: Algoritmo Genetico e Logica Fuzzy. O objetivo foi gerar planos de disciplinas que reduzam tempo de formatura e reprovacoes, respeitando pre-requisitos e limites academicos reais.

### Transicao
Agora eu vou contextualizar exatamente qual problema estamos resolvendo.

---

## Slide 2 - Problema

### Objetivo
Deixar claro o problema de otimizacao e por que ele e dificil.

### Tempo sugerido
45 a 60 segundos.

### Fala sugerida
O problema e distribuir dezenas de disciplinas ao longo dos semestres sem violar regras academicas. A dificuldade vem do tamanho do espaco de busca e das restricoes: pre-requisito, carga maxima por semestre, carga minima de optativas e diferentes perfis de aluno. Entao nao e so terminar rapido, e terminar de forma viavel e com menor risco de reprovacao.

### Transicao
Com isso, eu modelei o problema de forma que os dois metodos pudessem ser comparados de forma justa.

---

## Slide 3 - Abordagem Geral

### Objetivo
Mostrar visao macro da comparacao GA vs Fuzzy.

### Tempo sugerido
40 a 50 segundos.

### Fala sugerida
Eu usei duas estrategias. No Algoritmo Genetico, as grades evoluem por selecao, crossover e mutacao. Na Logica Fuzzy, a alocacao e guiada por regras linguisticas do tipo IF-THEN, com refinamento por busca local. Em ambos os casos, a avaliacao final usa a mesma funcao de fitness e a mesma simulacao, garantindo comparacao consistente.

### Transicao
Antes de entrar nos algoritmos, vou mostrar a modelagem dos dados.

---

## Slide 4 - Modelagem dos Dados

### Objetivo
Apresentar entidades e restricoes centrais.

### Tempo sugerido
50 a 60 segundos.

### Fala sugerida
As disciplinas possuem carga, dificuldade, tipo e pre-requisitos. Cada aluno tem um perfil, como trabalha, estagio, IC, horas de estudo e local de moradia. A grade e uma sequencia de semestres contendo disciplinas. As restricoes principais foram carga maxima por semestre igual a 480 horas, minimo de optativas, limite de semestres e obrigatoriedade do primeiro semestre fixo.

### Transicao
Com os dados definidos, eu passo para a representacao do cromossomo no GA.

---

## Slide 5 - Cromossomo no GA

### Objetivo
Explicar claramente a representacao genetica.

### Tempo sugerido
60 segundos.

### Fala sugerida
No GA, cada individuo representa uma grade completa de curso. O cromossomo e uma lista de semestres, e cada semestre funciona como um gene contendo um conjunto de disciplinas. Essa escolha facilita aplicar restricoes por semestre e simular o progresso academico. O primeiro semestre e fixo por regra institucional, e os demais sao otimizados.

### Transicao
Com essa representacao, precisamos de uma forma objetiva de dizer o que e uma grade boa ou ruim.

---

## Slide 6 - Fitness

### Objetivo
Explicar a funcao objetivo e pesos.

### Tempo sugerido
60 a 75 segundos.

### Fala sugerida
A fitness minimiza uma combinacao ponderada de tempo de formatura, reprovacoes e penalidades de inviabilidade, como violacao de pre-requisito e carga. Quanto menor a fitness, melhor a solucao. Eu usei pesos maiores para componentes estruturais que quebram viabilidade academica, como nao concluir disciplinas e violar pre-requisitos. Isso garante que o algoritmo nao gere grades rapidas porem inviaveis.

### Transicao
Agora eu mostro como o GA explora o espaco de solucoes usando esses criterios.

---

## Slide 7 - Operadores do GA

### Objetivo
Explicar fluxo evolutivo do GA.

### Tempo sugerido
60 a 75 segundos.

### Fala sugerida
Em cada geracao, a populacao e avaliada pela fitness. Depois, ocorre selecao por torneio, crossover com taxa alta para combinar boas caracteristicas e mutacao para manter diversidade. Em seguida, aplico reparo para garantir consistencia da grade. A elite preserva os melhores individuos. Esse ciclo de exploracao e refinamento tende a reduzir a fitness de forma robusta.

### Transicao
Com o GA explicado, eu passo para a abordagem fuzzy.

---

## Slide 8 - Ideia da Logica Fuzzy

### Objetivo
Apresentar intuicao do fuzzy.

### Tempo sugerido
45 a 60 segundos.

### Fala sugerida
No fuzzy, em vez de gerar filhos por crossover, eu avalio cada disciplina elegivel por um score de alocacao entre 0 e 1. Esse score vem de regras linguisticas e considera carga atual do semestre, dificuldade da disciplina e momento do curso. A ideia e tomar decisoes locais explicaveis, aproximando como um especialista humano raciocinaria.

### Transicao
Para isso, eu defini variaveis fuzzy e funcoes de pertinencia.

---

## Slide 9 - Variaveis e Funcoes de Pertinencia

### Objetivo
Explicar universo fuzzy.

### Tempo sugerido
60 segundos.

### Fala sugerida
As entradas fuzzy sao carga do semestre, dificuldade e semestres cursados. Cada uma foi particionada em termos linguisticos, por exemplo baixa, media e alta para carga. A saida e score de alocacao com niveis de very_low ate very_high. Essas funcoes de pertinencia triangulares transformam valores numericos em graus de pertinencia e permitem inferencia com regras claras.

### Transicao
Com as variaveis definidas, o comportamento do sistema vem das regras.

---

## Slide 10 - Regras Fuzzy

### Objetivo
Mostrar regras e justificativas.

### Tempo sugerido
60 a 75 segundos.

### Fala sugerida
Exemplos de regras: se a carga esta baixa, o score tende a very_high. Se a carga esta alta e a disciplina e dificil, o score cai para very_low. Se o aluno esta no inicio e a disciplina e facil, o score sobe. Essas regras traduzem politica academica para logica computacional. O ganho principal aqui e interpretabilidade: eu consigo justificar por que uma disciplina foi alocada.

### Transicao
Depois da inferencia fuzzy, eu aplico refinamento para melhorar a solucao.

---

## Slide 11 - Fuzzy com Busca Local

### Objetivo
Explicar pipeline final do fuzzy.

### Tempo sugerido
60 a 75 segundos.

### Fala sugerida
O pipeline e: gerar elegiveis, ranquear por score fuzzy, alocar com threshold, reparar grade e avaliar fitness. Depois disso, aplico hill-climbing com pequenas mutacoes para refinar. Um ponto importante: o fuzzy tambem precisa de fitness, porque o score fuzzy decide localmente, mas a fitness mede qualidade global da grade e permite aceitar apenas melhorias.

### Transicao
Agora vamos aos resultados numericos e comparativos.

---

## Slide 12 - Resultado Geral

### Objetivo
Comparar desempenho agregado.

### Tempo sugerido
60 segundos.

### Fala sugerida
No resultado geral, o GA obteve melhor fitness e, em geral, menor tempo de formatura. O fuzzy apresentou solucoes validas e coerentes, mas com desempenho numerico inferior. Em compensacao, o fuzzy oferece maior transparencia de decisao. Entao temos um trade-off entre desempenho global e interpretabilidade.

### Transicao
Agora eu detalho os resultados por categoria de aluno.

---

## Slide 13 - Resultados por Perfil

### Objetivo
Mostrar robustez em contextos diferentes.

### Tempo sugerido
60 a 75 segundos.

### Fala sugerida
Eu avaliei categorias como geral, escola_publica, IC, trabalha, estagio e fora_da_cidade. Os graficos mostram que o contexto do aluno altera bastante tempo e fitness. O GA tende a manter vantagem na maioria dos perfis, mas a diferenca varia por categoria. Esse resultado reforca que personalizacao por perfil e essencial.

### Transicao
Em seguida, mostro os melhores individuos encontrados por cada metodo.

---

## Slide 14 - Top 3 Solucoes

### Objetivo
Exibir qualidade das melhores grades.

### Tempo sugerido
45 a 60 segundos.

### Fala sugerida
Aqui estao os top 3 de cada metodo com fitness, tempo e reprovacoes. Isso permite comparar nao so o melhor caso, mas estabilidade entre solucoes fortes. O GA entrega solucoes mais agressivas em performance, enquanto o fuzzy tende a planos mais conservadores e explicaveis.

### Transicao
Agora vamos ver a dinamica de convergencia ao longo da execucao.

---

## Slide 15 - Evolucao dos Algoritmos

### Objetivo
Mostrar comportamento temporal.

### Tempo sugerido
60 a 75 segundos.

### Fala sugerida
Nas curvas de evolucao, observamos a queda da fitness ao longo das geracoes ou iteracoes. O GA geralmente converge mais rapido para regioes melhores. O fuzzy tambem melhora, mas com maior chance de plateau por ficar mais preso a minimos locais. Essa diferenca e esperada pelo tipo de mecanismo de busca de cada abordagem.

### Transicao
Depois da evolucao, mostro a forma final das grades vencedoras.

---

## Slide 16 - Grades dos Melhores

### Objetivo
Mostrar estrutura pratica do resultado.

### Tempo sugerido
60 segundos.

### Fala sugerida
Aqui esta a grade final dos melhores individuos, semestre a semestre, com carga distribuida ao longo do curso. Esse slide e importante para mostrar aplicabilidade real: nao e so um numero de fitness, e uma proposta concreta de trajetoria academica.

### Transicao
Com os resultados em maos, vou fechar com analise critica.

---

## Slide 17 - Analise Critica

### Objetivo
Mostrar maturidade tecnica.

### Tempo sugerido
60 segundos.

### Fala sugerida
O GA foi superior em otimizacao global. O fuzzy foi superior em interpretabilidade das decisoes. As principais limitacoes foram ajuste de hiperparametros no GA e dependencia de regras no fuzzy. Como proximo passo, uma abordagem hibrida GA + fuzzy pode combinar desempenho com explicabilidade.

### Transicao
Para encerrar, trago as conclusoes principais.

---

## Slide 18 - Conclusao

### Objetivo
Fechamento forte.

### Tempo sugerido
40 a 60 segundos.

### Fala sugerida
Concluindo: o problema foi modelado com restricoes reais e avaliado em multiplos perfis de aluno. O GA apresentou melhor performance quantitativa. O fuzzy entregou decisao interpretavel e resultados validos. O projeto demonstra que IA aplicada ao planejamento academico pode apoiar decisoes mais eficientes e personalizadas.

### Encerramento
Obrigado. Fico a disposicao para perguntas.

---

# Perguntas da Banca e Respostas Prontas

## 1. Por que o fuzzy precisa de fitness se ja existe score fuzzy?

Resposta curta:
O score fuzzy ranqueia disciplinas localmente. A fitness avalia a qualidade global da grade inteira. Sem fitness, nao existe criterio unico para comparar solucoes completas.

## 2. Por que o GA foi melhor?

Resposta curta:
Porque o GA combina exploracao global e refinamento por crossover, mutacao e selecao, escapando melhor de minimos locais.

## 3. O que o fuzzy trouxe de vantagem entao?

Resposta curta:
Interpretabilidade. As regras explicam claramente por que cada disciplina foi priorizada.

## 4. Como garantir comparacao justa entre GA e fuzzy?

Resposta curta:
Mesma base de disciplinas, mesmas restricoes, mesma simulacao e mesma funcao de fitness para avaliar ambos.

## 5. Qual seria o proximo passo do projeto?

Resposta curta:
Implementar abordagem hibrida, usando fuzzy para guiar inicializacao e GA para refinamento global.

---

# Dica de Treino (muito importante)

Treine em 3 passadas:

1. Passada tecnica: entender cada slide sem ler texto.
2. Passada de tempo: manter entre 12 e 18 minutos.
3. Passada de banca: simular perguntas acima e responder em ate 20 segundos cada.
