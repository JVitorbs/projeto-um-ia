#!/usr/bin/env python3
"""
Script para gerar resultados detalhados em formato texto para apresentação.

Gera:
1. Resumo do melhor indivíduo (GA e Fuzzy)
2. Grade de disciplinas por categoria
3. Comparativos por perfil
4. Estatísticas de evolução
"""

import json
import os
from pathlib import Path

# Carregar resultados GA
try:
    with open("logs/evolucao.json") as f:
        ga_data = json.load(f)
    print("✓ GA carregado")
except:
    ga_data = None
    print("✗ GA não encontrado")

# Carregar resultados Fuzzy
try:
    with open("logs/evolucao_fuzzy.json") as f:
        fuzzy_data = json.load(f)
    print("✓ Fuzzy carregado")
except:
    fuzzy_data = None
    print("✗ Fuzzy não encontrado")

# Criar diretório de saída
Path("resultados_apresentacao").mkdir(exist_ok=True)

# =====================================================================
# 1. COMPARATIVO GERAL
# =====================================================================

with open("resultados_apresentacao/01_comparativo_geral.txt", "w") as f:
    f.write("="*80 + "\n")
    f.write("COMPARATIVO: ALGORITMO GENÉTICO vs LÓGICA FUZZY\n")
    f.write("="*80 + "\n\n")
    
    if ga_data:
        f.write("ALGORITMO GENÉTICO\n")
        f.write("-" * 80 + "\n")
        top1_ga = ga_data['top3'][0]
        f.write(f"Melhor Fitness:   {top1_ga['fitness']:.2f}\n")
        f.write(f"Tempo Formatura:  {top1_ga['tempo']:.2f} semestres\n")
        f.write(f"Reprovações:      {top1_ga['reprovacoes']:.2f}\n")
        f.write(f"Perfil:           {top1_ga['perfil_str']}\n")
        f.write(f"Seed:             {ga_data['seed']}\n\n")
    
    if fuzzy_data:
        f.write("LÓGICA FUZZY (com Hill-Climbing)\n")
        f.write("-" * 80 + "\n")
        top1_fuzzy = fuzzy_data['top3'][0]
        f.write(f"Melhor Fitness:   {top1_fuzzy['fitness']:.2f}\n")
        f.write(f"Tempo Formatura:  {top1_fuzzy['tempo']:.2f} semestres\n")
        f.write(f"Reprovações:      {top1_fuzzy['reprovacoes']:.2f}\n")
        f.write(f"Perfil:           {top1_fuzzy['perfil_str']}\n")
        f.write(f"Seed:             {fuzzy_data['seed']}\n\n")
    
    if ga_data and fuzzy_data:
        f.write("COMPARAÇÃO\n")
        f.write("-" * 80 + "\n")
        ga_fitness = ga_data['top3'][0]['fitness']
        fuzzy_fitness = fuzzy_data['top3'][0]['fitness']
        diff = (fuzzy_fitness - ga_fitness) / ga_fitness * 100
        f.write(f"Difference em Fitness: {diff:+.1f}%\n")
        f.write(f"GA é {fuzzy_fitness/ga_fitness:.2f}x melhor\n\n")

print("✓ 01_comparativo_geral.txt")

# =====================================================================
# 2. RESUMO DAS CATEGORIAS
# =====================================================================

if ga_data:
    with open("resultados_apresentacao/02_categorias_ga.txt", "w") as f:
        f.write("="*80 + "\n")
        f.write("RESULTADOS POR CATEGORIA DE ALUNO - GA\n")
        f.write("="*80 + "\n\n")
        
        for cat in ga_data['categorias']:
            f.write(f"{cat['categoria'].upper()}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Tempo médio:           {cat['tempo_medio']:.2f} semestres\n")
            f.write(f"Tempo mínimo:          {cat['tempo_min']:.0f} semestres\n")
            f.write(f"Fitness médio:         {cat['fitness_medio']:.2f}\n")
            f.write(f"Reprovações médias:    {cat['reprov_medio']:.2f}\n")
            f.write(f"Disciplinas não concluídas: {cat['nao_concluidas_media']:.2f}\n\n")

print("✓ 02_categorias_ga.txt")

if fuzzy_data:
    with open("resultados_apresentacao/02_categorias_fuzzy.txt", "w") as f:
        f.write("="*80 + "\n")
        f.write("RESULTADOS POR CATEGORIA DE ALUNO - FUZZY\n")
        f.write("="*80 + "\n\n")
        
        for cat in fuzzy_data['categorias']:
            f.write(f"{cat['categoria'].upper()}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Tempo médio:           {cat['tempo_medio']:.2f} semestres\n")
            f.write(f"Tempo mínimo:          {cat['tempo_min']:.0f} semestres\n")
            f.write(f"Fitness médio:         {cat['fitness_medio']:.2f}\n")
            f.write(f"Reprovações médias:    {cat['reprov_medio']:.2f}\n")
            f.write(f"Disciplinas não concluídas: {cat['nao_concluidas_media']:.2f}\n\n")

print("✓ 02_categorias_fuzzy.txt")

# =====================================================================
# 3. TOP 3 DETALHADO
# =====================================================================

if ga_data:
    with open("resultados_apresentacao/03_top3_ga.txt", "w") as f:
        f.write("="*80 + "\n")
        f.write("TOP 3 MELHORES SOLUÇÕES - ALGORITMO GENÉTICO\n")
        f.write("="*80 + "\n\n")
        
        for rank, ind in enumerate(ga_data['top3'][:3], 1):
            f.write(f"POSIÇÃO #{rank}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Fitness:               {ind['fitness']:.2f}\n")
            f.write(f"Tempo de Formatura:    {ind['tempo']:.2f} semestres\n")
            f.write(f"Reprovações Médias:    {ind['reprovacoes']:.2f}\n")
            f.write(f"Perfil:                {ind['perfil_str']}\n\n")
            f.write(f"Detalhes do Perfil:\n")
            for k, v in ind['perfil'].items():
                f.write(f"  - {k}: {v}\n")
            f.write("\n\n")

print("✓ 03_top3_ga.txt")

if fuzzy_data:
    with open("resultados_apresentacao/03_top3_fuzzy.txt", "w") as f:
        f.write("="*80 + "\n")
        f.write("TOP 3 MELHORES SOLUÇÕES - LÓGICA FUZZY\n")
        f.write("="*80 + "\n\n")
        
        for rank, ind in enumerate(fuzzy_data['top3'][:3], 1):
            f.write(f"POSIÇÃO #{rank}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Fitness:               {ind['fitness']:.2f}\n")
            f.write(f"Tempo de Formatura:    {ind['tempo']:.2f} semestres\n")
            f.write(f"Reprovações Médias:    {ind['reprovacoes']:.2f}\n")
            f.write(f"Perfil:                {ind['perfil_str']}\n\n")
            f.write(f"Detalhes do Perfil:\n")
            for k, v in ind['perfil'].items():
                f.write(f"  - {k}: {v}\n")
            f.write("\n\n")

print("✓ 03_top3_fuzzy.txt")

# =====================================================================
# 4. EVOLUÇÃO DO ALGORITMO
# =====================================================================

if ga_data:
    with open("resultados_apresentacao/04_evolucao_ga.txt", "w") as f:
        f.write("="*80 + "\n")
        f.write("EVOLUÇÃO DO ALGORITMO GENÉTICO\n")
        f.write("="*80 + "\n\n")
        f.write("Geração | Melhor Fitness | Média Pop | Pior | Sem Melhoria\n")
        f.write("-" * 80 + "\n")
        
        hist = ga_data['historico']
        # Mostrar cada 5 gerações + primeiras e últimas
        indices = set([0, 1, 2])  # Primeiras
        indices.update(range(len(hist)-3, len(hist)))  # Últimas
        for i in range(0, len(hist), 5):
            indices.add(i)
        
        for i in sorted(indices):
            if i < len(hist):
                h = hist[i]
                f.write(f"{h['geracao']:6d} | {h['melhor']:13.2f} | {h['media']:9.2f} | "
                       f"{h['pior']:7.1f} | {h['sem_melhoria']:11d}\n")
        f.write("\n")

print("✓ 04_evolucao_ga.txt")

if fuzzy_data:
    with open("resultados_apresentacao/04_evolucao_fuzzy.txt", "w") as f:
        f.write("="*80 + "\n")
        f.write("EVOLUÇÃO DO ALGORITMO FUZZY\n")
        f.write("="*80 + "\n\n")
        f.write("Iteração | Melhor Fitness | Média Pop | Pior | Sem Melhoria\n")
        f.write("-" * 80 + "\n")
        
        hist = fuzzy_data['historico']
        # Mostrar cada 5 iterações + primeiras e últimas
        indices = set([0, 1, 2])  # Primeiras
        indices.update(range(len(hist)-3, len(hist)))  # Últimas
        for i in range(0, len(hist), 5):
            indices.add(i)
        
        for i in sorted(indices):
            if i < len(hist):
                h = hist[i]
                f.write(f"{h['geracao']:8d} | {h['melhor']:13.2f} | {h['media']:9.2f} | "
                       f"{h['pior']:7.1f} | {h['sem_melhoria']:11d}\n")
        f.write("\n")

print("✓ 04_evolucao_fuzzy.txt")

# =====================================================================
# 5. RESUMO ESTATÍSTICO
# =====================================================================

with open("resultados_apresentacao/05_resumo_estatistico.txt", "w") as f:
    f.write("="*80 + "\n")
    f.write("RESUMO ESTATÍSTICO\n")
    f.write("="*80 + "\n\n")
    
    if ga_data:
        hist = ga_data['historico']
        f.write("ALGORITMO GENÉTICO\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total de gerações:         {len(hist)}\n")
        f.write(f"Melhor fitness (final):    {hist[-1]['melhor_ate_agora']:.2f}\n")
        f.write(f"Fitness inicial (geração 1): {hist[0]['melhor']:.2f}\n")
        f.write(f"Melhoria total:            {hist[0]['melhor'] - hist[-1]['melhor_ate_agora']:.2f}\n")
        f.write(f"% melhoria:                {(1 - hist[-1]['melhor_ate_agora']/hist[0]['melhor'])*100:.1f}%\n")
        f.write(f"Tempo (semestres) final:   {hist[-1]['tempo_melhor_ate_agora']:.1f}\n\n")
    
    if fuzzy_data:
        hist = fuzzy_data['historico']
        f.write("LÓGICA FUZZY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total de tentativas:       {len(hist)}\n")
        f.write(f"Melhor fitness (final):    {hist[-1]['melhor_ate_agora']:.2f}\n")
        f.write(f"Fitness inicial (tentativa 1): {hist[0]['melhor']:.2f}\n")
        f.write(f"Melhoria total:            {hist[0]['melhor'] - hist[-1]['melhor_ate_agora']:.2f}\n")
        f.write(f"% melhoria:                {(1 - hist[-1]['melhor_ate_agora']/hist[0]['melhor'])*100:.1f}%\n")
        f.write(f"Tempo (semestres) final:   {hist[-1]['tempo_melhor_ate_agora']:.1f}\n\n")

print("✓ 05_resumo_estatistico.txt")

print("\n" + "="*80)
print("RESUMO GERADO COM SUCESSO")
print("="*80)
print("Arquivos criados em: resultados_apresentacao/")
print("  - 01_comparativo_geral.txt")
print("  - 02_categorias_ga.txt")
print("  - 02_categorias_fuzzy.txt")
print("  - 03_top3_ga.txt")
print("  - 03_top3_fuzzy.txt")
print("  - 04_evolucao_ga.txt")
print("  - 04_evolucao_fuzzy.txt")
print("  - 05_resumo_estatistico.txt")
