# Correções Propostas para a Implementação Fuzzy

Este arquivo contém patches e melhorias propostas para os problemas identificados.

---

## 1. ✅ CORREÇÃO: Reset do Simulador Fuzzy

**Arquivo**: `fuzzy_logic.py`  
**Método**: `calcular_score_alocacao()`  
**Prioridade**: MÉDIA

### Problema
Simulador não é resetado entre chamadas, pode deixar estado residual.

### Solução
Adicionar reset explícito. Em scikit-fuzzy, isso pode ser feito ao criar novo ControlSystemSimulation.

### Código Proposto
```python
def calcular_score_alocacao(self, carga_semestre, dificuldade_disciplina, semestres_cursados):
    """
    Calcula o score fuzzy para alocar uma disciplina.
    
    Args:
        carga_semestre: float, carga horária atual no semestre [0-480]
        dificuldade_disciplina: float, dificuldade [0.3-0.9]
        semestres_cursados: int, número de semestres cursados [0-20]
    
    Returns:
        float: score de alocação [0.0-1.0]
    """
    try:
        # ✅ NOVO: Reset explícito do simulador
        self.simulador = ctrl.ControlSystemSimulation(self.sistema)
        
        self.simulador.input['carga_semestre'] = carga_semestre
        self.simulador.input['dificuldade'] = dificuldade_disciplina
        self.simulador.input['semestres_cursados'] = semestres_cursados
        
        self.simulador.compute()
        
        score = self.simulador.output['score_alocacao']
        return np.clip(score, 0.0, 1.0)
    except Exception as e:
        # Melhorado: log mais informativo
        import logging
        logging.warning(f"Erro ao calcular score fuzzy: {e}")
        return 0.5

def reset(self):
    """Reseta o simulador."""
    self.simulador = ctrl.ControlSystemSimulation(self.sistema)
```

---

## 2. ✅ CORREÇÃO: Melhorar Regras Fuzzy

**Arquivo**: `fuzzy_logic.py`  
**Método**: `_criar_regras()`  
**Prioridade**: ALTA

### Problemas
- Regra #8 é muito restritiva (nunca acionada)
- Faltam coberturas para casos comuns

### Solução Proposta
Substituir regra 8 e adicionar novas regras.

### Código Proposto
```python
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
        
        # ✅ CORRIGIDA: Regra 8 - Remover restrição de carga
        # Versão antiga era muito específica: final & dificil & media
        # Nova: apenas final & dificil
        ctrl.Rule(
            self.semestres_cursados['final'] & self.dificuldade['dificil'],
            self.score_alocacao['low']
        ),
        
        # ✅ NOVA: Regra 9 - Carga alta com média dificuldade
        ctrl.Rule(
            self.carga_semestre['alta'] & self.dificuldade['media_dif'],
            self.score_alocacao['low']
        ),
        
        # ✅ NOVA: Regra 10 - Início com disciplina difícil
        # Encorajar desafio no início, mas com cautela
        ctrl.Rule(
            self.semestres_cursados['inicio'] & self.dificuldade['dificil'],
            self.score_alocacao['medium']
        ),
        
        # ✅ NOVA: Regra 11 - Fim com disciplina fácil (sempre bom)
        ctrl.Rule(
            self.semestres_cursados['final'] & self.dificuldade['facil'],
            self.score_alocacao['high']
        ),
    ]
```

### Justificativa
- **Regra 8 corrigida**: Remove a condição `carga_semestre['media']` que Never era acionada
- **Regra 9**: Cobre o gap "carga alta + média dificuldade"
- **Regra 10**: Permite desafios no início com score neutro
- **Regra 11**: Incentiva disciplinas fáceis no final (consolidação)

---

## 3. ✅ CORREÇÃO: Validação Pós-Reparação

**Arquivo**: `fuzzy_solver.py`  
**Método**: `_aplicar_reparacao()`  
**Prioridade**: MÉDIA

### Problema
Reparação é aplicada sem verificação de sucesso.

### Solução Proposta

```python
def _aplicar_reparacao(self):
    """
    Repara o plano garantindo viabilidade.
    Válida a grade após reparação.
    """
    from reparo import reparar_individuo
    
    # Aplicar reparação
    reparar_individuo(self.melhor_individuo)
    
    # ✅ NOVO: Validar a grade após reparação
    self._validar_grade(self.melhor_individuo)

def _validar_grade(self, individuo):
    """
    Valida a grade do indivíduo com checagens básicas.
    
    Checagens:
    - Todos códigos de disciplina existem em disciplinas
    - Não há duplicatas em semestres
    - Primera semestre tem PRIMEIRO_SEMESTRE_FIXO
    """
    # Checar se todas as disciplinas são válidas
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
        import logging
        logging.warning(
            f"Primeiro semestre não contempla todas as disciplinas fixas. "
            f"Faltam: {fixo_set - primeiro_sem_set}"
        )
```

---

## 4. ✅ CORREÇÃO: Calibrar Threshold de Alocação

**Arquivo**: `fuzzy_solver.py`  
**Método**: `_construir_plano_fuzzy()`  
**Prioridade**: BAIXA-MÉDIA

### Problema
Threshold 0.3 é hardcoded sem justificativa.

### Solução Proposta

```python
# Adicionar no __init__ do FuzzySolver:
class FuzzySolver:
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
        self.threshold_alocacao = threshold_alocacao  # ✅ NOVO
        
        # ... resto da inicialização ...

def _construir_plano_fuzzy(self):
    """
    Constrói um plano de curso usando lógica fuzzy.
    """
    for semestre in range(1, SEMESTRES_MAX):
        elegveis = self._obter_disciplinas_elegveis(semestre)
        
        if not elegveis:
            # ✅ NOVO: Log para rastrear semestres vazios
            import logging
            logging.debug(f"Semestre {semestre}: nenhuma disciplina elegível")
            continue
        
        ranked = self._ranked_por_fuzzy(elegveis, semestre)
        carga_atual = sum(
            disciplinas[d]['carga'] for d in self.melhor_individuo.grade[semestre]
        )
        
        for disc_id, disc_info, score_fuzzy in ranked:
            # ✅ MELHORADO: usar self.threshold_alocacao em vez de hardcoded
            if score_fuzzy < self.threshold_alocacao:
                continue
            
            nova_carga = carga_atual + disc_info['carga']
            
            if nova_carga > CARGA_MAX_SEMESTRE:
                continue
            
            self.melhor_individuo.grade[semestre].append(disc_id)
            carga_atual = nova_carga
```

### Calibração Recomendada
Para testar diferentes thresholds:

```python
# Em main_fuzzy.py, adicionar varredura:
thresholds_teste = [0.2, 0.3, 0.5, 0.7]

for threshold em thresholds_teste:
    print(f"\nTestando com threshold={threshold}")
    solver = FuzzySolver(iteracoes=60, threshold_alocacao=threshold)
    solver.resolver()
    # Avaliar e comparar resultados
```

---

## 5. ✅ MELHORIA: Warnings para Semestres Vazios

**Arquivo**: `fuzzy_solver.py`  
**Localização**: `_construir_plano_fuzzy()`

### Implementação
(Ver Correção #4 - já incluso)

---

## 6. ✅ MELHORIA: Melhor Tratamento de Exceções

**Arquivo**: `fuzzy_logic.py`  
**Método**: `calcular_score_alocacao()`

### Código Proposto

```python
def calcular_score_alocacao(self, carga_semestre, dificuldade_disciplina, semestres_cursados):
    """
    Calcula o score fuzzy para alocar uma disciplina.
    """
    try:
        self.simulador = ctrl.ControlSystemSimulation(self.sistema)
        
        # ✅ NOVO: Validar inputs antes de usar
        if not (0 <= carga_semestre <= 600):
            import logging
            logging.warning(
                f"carga_semestre fora do intervalo: {carga_semestre}, "
                "using clipping to [0, 600]"
            )
            carga_semestre = np.clip(carga_semestre, 0, 600)
        
        if not (0 <= dificuldade_disciplina <= 1.1):
            dificuldade_disciplina = np.clip(dificuldade_disciplina, 0, 1.1)
        
        if not (0 <= semestres_cursados <= 20):
            semestres_cursados = np.clip(semestres_cursados, 0, 20)
        
        self.simulador.input['carga_semestre'] = carga_semestre
        self.simulador.input['dificuldade'] = dificuldade_disciplina
        self.simulador.input['semestres_cursados'] = semestres_cursados
        
        self.simulador.compute()
        score = self.simulador.output['score_alocacao']
        return np.clip(score, 0.0, 1.0)
        
    except Exception as e:
        import logging
        logging.error(
            f"Erro ao calcular score fuzzy com inputs "
            f"(carga={carga_semestre}, dif={dificuldade_disciplina}, sem={semestres_cursados}): {e}"
        )
        return 0.5  # Valor neutro como fallback
```

---

## 7. 🚀 GRANDE MELHORIA: Busca Local em Vez de Reconstrução Completa

**Arquivo**: `fuzzy_solver.py`  
**Prioridade**: CRÍTICA

### Problema
Algoritmo reconstrói tudo a cada iteração - sem convergência eficaz.

### Solução: Hill-Climbing com Permutações Locais

```python
def resolver_com_hillclimbing(self):
    """
    Executa busca local (hill-climbing) em vez de reconstrução completa.
    
    Estratégia:
    - Iteração 0: construir plano novo com fuzzy
    - Iterações 1+: fazer pequenas mutações (mover disciplinas entre semestres próximos)
    - Aceitar melhoria; rejeitar piora (ou aceitar com prob pequena)
    """
    
    from ga import fitness
    
    # Iteração 0: Construir plano inicial
    individuo_atual = Individuo()
    individuo_atual.perfil = deepcopy(self.melhor_individuo.perfil)
    individuo_atual.grade[0] = PRIMEIRO_SEMESTRE_FIXO.copy()
    for i in range(1, SEMESTRES_MAX):
        individuo_atual.grade[i] = []
    
    self.melhor_individuo = individuo_atual
    self._construir_plano_fuzzy()
    self._aplicar_reparacao()
    self.melhor_fitness = fitness(self.melhor_individuo)
    self.melhor_individuo.fitness = self.melhor_fitness
    
    # Iterações 1+: Busca local
    for iteracao in range(1, self.iteracoes):
        # Copiar melhor candidato
        candidato = deepcopy(self.melhor_individuo)
        
        # Fazer mutação pequena: permute uma ou duas disciplinas
        self._mutar_localmente(candidato)
        
        # Reparar
        self._aplicar_reparacao()
        
        # Avaliar
        novo_fitness = fitness(candidato)
        candidato.fitness = novo_fitness
        
        # Hill-climbing: aceitar se melhorar
        if novo_fitness < self.melhor_fitness:
            self.melhor_individuo = candidato
            self.melhor_fitness = novo_fitness
            if iteracao % 5 == 0:
                print(f"Iteração {iteracao}: Novo melhor fitness = "
                      f"{novo_fitness:.2f}")
        
        self.historico_fitness.append(self.melhor_fitness)

def _mutar_localmente(self, individuo):
    """
    Aplica pequenas mutações: move disciplinas entre semestres próximos.
    """
    import random
    
    # Selecionar um semestre aleatório (não primeiro)
    sem_origem = random.randint(1, SEMESTRES_MAX - 2)
    
    if not individuo.grade[sem_origem]:  # Vazio
        return
    
    # Selecionar em semestres vizinhos (sem_origem ± 1)
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
```

---

## Plano de Implementação Recomendado

### Fase 1: Implementar Correções Essenciais (1-2 horas)
1. ✅ Correção #1: Reset do simulador
2. ✅ Correção #3: Validação pós-reparação
3. ✅ Correção #2: Melhorar regras

### Fase 2: Testar e Calibrar (1 hora)
4. ✅ Correção #4: Calibrar threshold
5. ✅ Testar com threshold=[0.2, 0.3, 0.5, 0.7]

### Fase 3: Grande Melhoria (1-2 horas, OPCIONAL)
6. ✅ Melhoria #7: Implementar hill-climbing
7. ✅ Comparar com versão original

---

## Testes Recomendados

Após implementar as correções:

```bash
# Teste 1: Execução básica
FUZZY_ITERACOES=50 FUZZY_TENTATIVAS=20 python main_fuzzy.py

# Teste 2: Com diferentes thresholds
FUZZY_THRESHOLD=0.2 FUZZY_ITERACOES=50 python main_fuzzy.py
FUZZY_THRESHOLD=0.5 FUZZY_ITERACOES=50 python main_fuzzy.py

# Teste 3: Verificar logs
python main_fuzzy.py 2>&1 | grep -i "warning\|error"

# Teste 4: Comparar com GA
GERACOES=100 python main.py
python plot_dispersao_evolucao.py
```

---

## Resumo de Impactos

| Correção | Impacto na Converência | Impacto na Qualidade | Esforço |
|----------|----------------------|----------------------|---------|
| #1 Reset | Baixo | Médio | Baixo |
| #2 Regras | **Alto** | **Alto** | Médio |
| #3 Validação | Baixo | Médio | Baixo |
| #4 Threshold | Médio | Médio | Médio |
| #7 Hill-climbing | **Muito Alto** | **Muito Alto** | **Alto** |

