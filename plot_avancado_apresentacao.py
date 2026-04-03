#!/usr/bin/env python3
"""
Script de plotagem avancada para apresentacao de slides.

Gera multiplos graficos:
1. Evolucao detalhada GA vs Fuzzy
2. Tempo medio por categoria
3. Fitness medio por categoria
4. Reprovacoes por categoria
5. Carga por semestre (Top 1)
6. Radar chart comparativo (opcional)
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configuracao visual
plt.style.use('seaborn-v0_8-whitegrid')
COLOR_GA = '#1f77b4'      # azul
COLOR_FUZZY = '#ff7f0e'   # laranja

# Criar pasta de saida
OUTPUT_DIR = Path("plots_apresentacao")
OUTPUT_DIR.mkdir(exist_ok=True)


def carregar_dados():
    """Carrega dados dos logs GA e Fuzzy."""
    ga_data = None
    fuzzy_data = None
    
    try:
        with open("logs/evolucao.json") as f:
            ga_data = json.load(f)
        print("✓ GA carregado")
    except Exception as e:
        print(f"✗ Erro ao carregar GA: {e}")
    
    try:
        with open("logs/evolucao_fuzzy.json") as f:
            fuzzy_data = json.load(f)
        print("✓ Fuzzy carregado")
    except Exception as e:
        print(f"✗ Erro ao carregar Fuzzy: {e}")
    
    return ga_data, fuzzy_data


def plot_evolucao_detalhada(ga_data, fuzzy_data):
    """Plot 1: Evolucao detalhada com melhor, media, pior e quartis."""
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=False)
    
    # GA
    if ga_data and ga_data.get('historico'):
        hist = ga_data['historico']
        x = [h['geracao'] for h in hist]
        melhor = [h['melhor_ate_agora'] for h in hist]
        media = [h['media'] for h in hist]
        pior = [h['pior'] for h in hist]
        q1 = [h['q1'] for h in hist]
        q3 = [h['q3'] for h in hist]
        
        ax = axes[0]
        ax.plot(x, melhor, color=COLOR_GA, linewidth=3, label='Melhor acumulado')
        ax.plot(x, media, color='green', linewidth=2, alpha=0.8, label='Media')
        ax.plot(x, pior, color='red', linewidth=1.5, alpha=0.6, label='Pior')
        ax.fill_between(x, q1, q3, color=COLOR_GA, alpha=0.2, label='Q1-Q3')
        
        ax.set_title('Evolucao do Algoritmo Genetico', fontsize=14, fontweight='bold')
        ax.set_xlabel('Geracao')
        ax.set_ylabel('Fitness')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
    
    # Fuzzy
    if fuzzy_data and fuzzy_data.get('historico'):
        hist = fuzzy_data['historico']
        x = [h['geracao'] for h in hist]
        melhor = [h['melhor_ate_agora'] for h in hist]
        media = [h['media'] for h in hist]
        pior = [h['pior'] for h in hist]
        q1 = [h['q1'] for h in hist]
        q3 = [h['q3'] for h in hist]
        
        ax = axes[1]
        ax.plot(x, melhor, color=COLOR_FUZZY, linewidth=3, label='Melhor acumulado')
        ax.plot(x, media, color='green', linewidth=2, alpha=0.8, label='Media')
        ax.plot(x, pior, color='red', linewidth=1.5, alpha=0.6, label='Pior')
        ax.fill_between(x, q1, q3, color=COLOR_FUZZY, alpha=0.2, label='Q1-Q3')
        
        ax.set_title('Evolucao do Sistema Fuzzy', fontsize=14, fontweight='bold')
        ax.set_xlabel('Iteracao')
        ax.set_ylabel('Fitness')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '01_evolucao_detalhada.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 01_evolucao_detalhada.png")


def plot_categorias_comparativo(ga_data, fuzzy_data):
    """Plots 2-4: Comparativos por categoria."""
    if not (ga_data and fuzzy_data):
        return
    
    ga_cats = {c['categoria']: c for c in ga_data.get('categorias', [])}
    fuzzy_cats = {c['categoria']: c for c in fuzzy_data.get('categorias', [])}
    
    categorias = sorted(set(ga_cats.keys()) & set(fuzzy_cats.keys()))
    if not categorias:
        return
    
    x = np.arange(len(categorias))
    width = 0.35
    
    # Plot 2: Tempo medio
    fig, ax = plt.subplots(figsize=(12, 6))
    ga_tempos = [ga_cats[c]['tempo_medio'] for c in categorias]
    fuzzy_tempos = [fuzzy_cats[c]['tempo_medio'] for c in categorias]
    
    bars1 = ax.bar(x - width/2, ga_tempos, width, label='GA', color=COLOR_GA, alpha=0.8)
    bars2 = ax.bar(x + width/2, fuzzy_tempos, width, label='Fuzzy', color=COLOR_FUZZY, alpha=0.8)
    
    ax.set_title('Tempo Medio por Categoria de Aluno', fontsize=14, fontweight='bold')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Tempo Medio (semestres)')
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, rotation=30, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h, f'{h:.1f}',
                ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h, f'{h:.1f}',
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '02_tempo_por_categoria.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 02_tempo_por_categoria.png")
    
    # Plot 3: Fitness medio
    fig, ax = plt.subplots(figsize=(12, 6))
    ga_fitness = [ga_cats[c]['fitness_medio'] for c in categorias]
    fuzzy_fitness = [fuzzy_cats[c]['fitness_medio'] for c in categorias]
    
    bars1 = ax.bar(x - width/2, ga_fitness, width, label='GA', color=COLOR_GA, alpha=0.8)
    bars2 = ax.bar(x + width/2, fuzzy_fitness, width, label='Fuzzy', color=COLOR_FUZZY, alpha=0.8)
    
    ax.set_title('Fitness Medio por Categoria de Aluno', fontsize=14, fontweight='bold')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Fitness Medio (menor e melhor)')
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, rotation=30, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '03_fitness_por_categoria.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 03_fitness_por_categoria.png")
    
    # Plot 4: Reprovacoes
    fig, ax = plt.subplots(figsize=(12, 6))
    ga_reprov = [ga_cats[c].get('reprov_medio', 0) for c in categorias]
    fuzzy_reprov = [fuzzy_cats[c].get('reprov_medio', 0) for c in categorias]
    
    bars1 = ax.bar(x - width/2, ga_reprov, width, label='GA', color=COLOR_GA, alpha=0.8)
    bars2 = ax.bar(x + width/2, fuzzy_reprov, width, label='Fuzzy', color=COLOR_FUZZY, alpha=0.8)
    
    ax.set_title('Reprovacoes Medias por Categoria de Aluno', fontsize=14, fontweight='bold')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Reprovacoes Medias')
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, rotation=30, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '04_reprovacoes_por_categoria.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 04_reprovacoes_por_categoria.png")


def plot_resumo_final(ga_data, fuzzy_data):
    """Plot 5: Dashboard resumo final."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Resumo Comparativo Final: GA vs Fuzzy', fontsize=16, fontweight='bold')
    
    # Dados top1
    ga_top = ga_data['top3'][0] if ga_data and ga_data.get('top3') else None
    fuzzy_top = fuzzy_data['top3'][0] if fuzzy_data and fuzzy_data.get('top3') else None
    
    if ga_top and fuzzy_top:
        labels = ['Fitness', 'Tempo', 'Reprovacoes']
        ga_vals = [ga_top['fitness'], ga_top['tempo'], ga_top['reprovacoes']]
        fuzzy_vals = [fuzzy_top['fitness'], fuzzy_top['tempo'], fuzzy_top['reprovacoes']]
        
        x = np.arange(len(labels))
        width = 0.35
        
        # Comparacao absoluta
        ax = axes[0, 0]
        ax.bar(x - width/2, ga_vals, width, label='GA', color=COLOR_GA)
        ax.bar(x + width/2, fuzzy_vals, width, label='Fuzzy', color=COLOR_FUZZY)
        ax.set_title('Top 1: Valores Absolutos')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Comparacao relativa (Fuzzy/GA)
        ax = axes[0, 1]
        ratios = [fuzzy_vals[i]/ga_vals[i] if ga_vals[i] > 0 else 1 for i in range(3)]
        colors = ['red' if r > 1 else 'green' for r in ratios]
        bars = ax.bar(labels, ratios, color=colors, alpha=0.7)
        ax.axhline(y=1, color='black', linestyle='--', alpha=0.5)
        ax.set_title('Razao Fuzzy/GA (1.0 = igual)')
        ax.set_ylabel('Razao')
        ax.grid(True, alpha=0.3, axis='y')
        for bar, ratio in zip(bars, ratios):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'{ratio:.2f}x', ha='center', va='bottom')
    
    # Evolucao final
    if ga_data and ga_data.get('historico'):
        hist = ga_data['historico']
        x = [h['geracao'] for h in hist]
        y = [h['melhor_ate_agora'] for h in hist]
        axes[1, 0].plot(x, y, color=COLOR_GA, linewidth=2)
        axes[1, 0].set_title('Convergencia GA')
        axes[1, 0].set_xlabel('Geracao')
        axes[1, 0].set_ylabel('Melhor Fitness')
        axes[1, 0].grid(True, alpha=0.3)
    
    if fuzzy_data and fuzzy_data.get('historico'):
        hist = fuzzy_data['historico']
        x = [h['geracao'] for h in hist]
        y = [h['melhor_ate_agora'] for h in hist]
        axes[1, 1].plot(x, y, color=COLOR_FUZZY, linewidth=2)
        axes[1, 1].set_title('Convergencia Fuzzy')
        axes[1, 1].set_xlabel('Iteracao')
        axes[1, 1].set_ylabel('Melhor Fitness')
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '05_dashboard_resumo.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 05_dashboard_resumo.png")


def main():
    print("="*60)
    print("GERANDO PLOTS AVANCADOS PARA APRESENTACAO")
    print("="*60)
    
    ga_data, fuzzy_data = carregar_dados()
    
    if not ga_data and not fuzzy_data:
        print("Erro: nenhum dado encontrado em logs/")
        return
    
    plot_evolucao_detalhada(ga_data, fuzzy_data)
    plot_categorias_comparativo(ga_data, fuzzy_data)
    plot_resumo_final(ga_data, fuzzy_data)
    
    print("\n" + "="*60)
    print("PLOTS GERADOS COM SUCESSO")
    print("="*60)
    print(f"Arquivos salvos em: {OUTPUT_DIR}/")
    print("  - 01_evolucao_detalhada.png")
    print("  - 02_tempo_por_categoria.png")
    print("  - 03_fitness_por_categoria.png")
    print("  - 04_reprovacoes_por_categoria.png")
    print("  - 05_dashboard_resumo.png")


if __name__ == "__main__":
    main()
