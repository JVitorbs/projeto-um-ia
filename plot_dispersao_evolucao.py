import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt


def resolver_caminho_log() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()
    return Path(__file__).resolve().parent / "logs" / "evolucao.json"


def carregar_dados(caminho_log: Path):
    if not caminho_log.exists():
        raise FileNotFoundError(
            f"Arquivo de log nao encontrado: {caminho_log}. "
            "Execute o main.py primeiro ou informe o caminho do JSON."
        )

    with caminho_log.open(encoding="utf-8") as f:
        bruto = json.load(f)

    if isinstance(bruto, dict):
        historico = bruto.get("historico", [])
        categorias = bruto.get("categorias", [])
    else:
        historico = bruto
        categorias = []

    if not historico:
        raise ValueError("O log nao possui historico para plotar.")

    return historico, categorias


def carregar_dados_fuzzy() -> tuple:
    """Tenta carregar dados do solver fuzzy, retorna (historico, categorias, caminho) ou (None, None, caminho)."""
    caminho = Path(__file__).resolve().parent / "logs" / "evolucao_fuzzy.json"
    if not caminho.exists():
        return None, None, caminho
    
    try:
        with caminho.open(encoding="utf-8") as f:
            bruto = json.load(f)
        
        if isinstance(bruto, dict):
            historico = bruto.get("historico", [])
            categorias = bruto.get("categorias", [])
        else:
            historico = bruto
            categorias = []
        
        if not historico:
            return None, None, caminho
        
        return historico, categorias, caminho
    except Exception as e:
        print(f"Aviso: Nao foi possivel carregar dados fuzzy: {e}")
        return None, None, caminho


def plotar_comparacao_ga_vs_fuzzy(hist_ga, cat_ga, hist_fuzzy=None, cat_fuzzy=None):
    """Plota GA vs Fuzzy lado-a-lado ou sobreposto."""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # ===== Plot 1: Fitness (Melhor) =====
    ax = axes[0, 0]
    ger_ga = [d["geracao"] for d in hist_ga]
    fit_melhor_ga = [d["melhor"] for d in hist_ga]
    ax.plot(ger_ga, fit_melhor_ga, label="GA - Melhor", linewidth=2, color='blue', marker='o', markersize=3)
    
    if hist_fuzzy:
        ger_fuzzy = [d["geracao"] for d in hist_fuzzy]
        fit_melhor_fuzzy = [d["melhor"] for d in hist_fuzzy]
        ax.plot(ger_fuzzy, fit_melhor_fuzzy, label="Fuzzy - Melhor", linewidth=2, color='red', marker='s', markersize=3)
    
    ax.set_title("Evolução: Melhor Fitness", fontsize=12, fontweight='bold')
    ax.set_xlabel("Geração / Iteração")
    ax.set_ylabel("Fitness")
    ax.grid(alpha=0.3)
    ax.legend()
    
    # ===== Plot 2: Fitness (Média) =====
    ax = axes[0, 1]
    fit_media_ga = [d.get("media", d["melhor"]) for d in hist_ga]
    ax.plot(ger_ga, fit_media_ga, label="GA - Média", linewidth=2, color='blue', linestyle='--', marker='d', markersize=3)
    
    if hist_fuzzy:
        fit_media_fuzzy = [d.get("media", d["melhor"]) for d in hist_fuzzy]
        ax.plot(ger_fuzzy, fit_media_fuzzy, label="Fuzzy - Média", linewidth=2, color='red', linestyle='--', marker='^', markersize=3)
    
    ax.set_title("Evolução: Fitness Médio", fontsize=12, fontweight='bold')
    ax.set_xlabel("Geração / Iteração")
    ax.set_ylabel("Fitness Médio")
    ax.grid(alpha=0.3)
    ax.legend()
    
    # ===== Plot 3: Tempo (Melhor) =====
    ax = axes[1, 0]
    tempo_melhor_ga = [d.get("tempo", 0) for d in hist_ga]
    ax.plot(ger_ga, tempo_melhor_ga, label="GA - Tempo", linewidth=2, color='green', marker='o', markersize=3)
    
    if hist_fuzzy:
        tempo_melhor_fuzzy = [d.get("tempo", 0) for d in hist_fuzzy]
        ax.plot(ger_fuzzy, tempo_melhor_fuzzy, label="Fuzzy - Tempo", linewidth=2, color='orange', marker='s', markersize=3)
    
    ax.set_title("Evolução: Tempo do Melhor Indivíduo", fontsize=12, fontweight='bold')
    ax.set_xlabel("Geração / Iteração")
    ax.set_ylabel("Tempo (semestres)")
    ax.grid(alpha=0.3)
    ax.legend()
    
    # ===== Plot 4: Categorias (Dispersão) =====
    ax = axes[1, 1]
    
    if cat_ga:
        x_ga = [c.get("tempo_medio", 0) for c in cat_ga]
        y_ga = [c.get("fitness_medio", 0) for c in cat_ga]
        labels_ga = [c.get("categoria", "-") for c in cat_ga]
        ax.scatter(x_ga, y_ga, s=100, alpha=0.7, label="GA", color='blue', marker='o')
        for nome, px, py in zip(labels_ga, x_ga, y_ga):
            ax.annotate(f"GA-{nome}", (px, py), textcoords="offset points", xytext=(5, 5), fontsize=8)
    
    if cat_fuzzy:
        x_fuzzy = [c.get("tempo_medio", 0) for c in cat_fuzzy]
        y_fuzzy = [c.get("fitness_medio", 0) for c in cat_fuzzy]
        labels_fuzzy = [c.get("categoria", "-") for c in cat_fuzzy]
        ax.scatter(x_fuzzy, y_fuzzy, s=100, alpha=0.7, label="Fuzzy", color='red', marker='s')
        for nome, px, py in zip(labels_fuzzy, x_fuzzy, y_fuzzy):
            ax.annotate(f"Fuzzy-{nome}", (px, py), textcoords="offset points", xytext=(5, -10), fontsize=8)
    
    ax.set_title("Dispersão por Categoria (Tempo × Fitness)", fontsize=12, fontweight='bold')
    ax.set_xlabel("Tempo médio (semestres)")
    ax.set_ylabel("Fitness médio")
    ax.grid(alpha=0.3)
    ax.legend()
    
    fig.suptitle("Comparação: GA vs Lógica Fuzzy", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plotar_dispersao_e_evolucao(historico, categorias, caminho_log: Path, nome_solver: str):
    ger = [d["geracao"] for d in historico]
    fit_melhor = [d["melhor"] for d in historico]
    fit_media = [d.get("media", d["melhor"]) for d in historico]
    tempo_melhor = [d.get("tempo", 0) for d in historico]
    diversidade = [d.get("diversidade", 0.0) for d in historico]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(ger, fit_melhor, label="Melhor fitness", linewidth=2)
    ax1.plot(ger, fit_media, label="Fitness medio", linestyle="--")
    ax1.set_title("Evolucao do Fitness")
    ax1.set_xlabel("Geracao")
    ax1.set_ylabel("Fitness")
    ax1.grid(alpha=0.2)
    ax1.legend()

    if categorias:
        # Dispersao por categoria: tempo medio x fitness medio
        x = [c.get("tempo_medio", 0) for c in categorias]
        y = [c.get("fitness_medio", 0) for c in categorias]
        labels = [c.get("categoria", "-") for c in categorias]

        ax2.scatter(x, y, s=70, alpha=0.85)
        for nome, px, py in zip(labels, x, y):
            ax2.annotate(nome, (px, py), textcoords="offset points", xytext=(4, 4), fontsize=9)
        ax2.set_title("Dispersao por Categoria")
        ax2.set_xlabel("Tempo medio (semestres)")
        ax2.set_ylabel("Fitness medio")
    else:
        # Fallback: dispersao da evolucao (tempo x fitness) colorida por diversidade.
        sc = ax2.scatter(tempo_melhor, fit_melhor, c=diversidade, cmap="viridis", s=35, alpha=0.9)
        ax2.set_title("Dispersao Evolutiva (Tempo x Fitness)")
        ax2.set_xlabel("Tempo do melhor individuo")
        ax2.set_ylabel("Melhor fitness")
        cbar = fig.colorbar(sc, ax=ax2)
        cbar.set_label("Diversidade")

    ax2.grid(alpha=0.2)

    fig.suptitle(f"Analise do {nome_solver} | log: {caminho_log.name}")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    caminho = resolver_caminho_log()
    historico_ga, categorias_ga = carregar_dados(caminho)
    print(f"Log GA carregado: {caminho}")
    print(f"Gerações GA: {len(historico_ga)}")
    print(f"Categorias GA: {len(categorias_ga)}")
    print("\nPlotando GA separado...")
    plotar_dispersao_e_evolucao(historico_ga, categorias_ga, caminho, "GA")
    
    # Tentar carregar dados fuzzy
    historico_fuzzy, categorias_fuzzy, caminho_fuzzy = carregar_dados_fuzzy()
    
    if historico_fuzzy and categorias_fuzzy:
        print(f"\nLog Fuzzy carregado: {caminho_fuzzy}")
        print(f"Iterações Fuzzy: {len(historico_fuzzy)}")
        print(f"Categorias Fuzzy: {len(categorias_fuzzy)}")
        print("\nPlotando Fuzzy separado...")
        plotar_dispersao_e_evolucao(historico_fuzzy, categorias_fuzzy, caminho_fuzzy, "Fuzzy")
        print("\nPlotando COMPARACAO GA vs Fuzzy...\n")
        plotar_comparacao_ga_vs_fuzzy(historico_ga, categorias_ga, historico_fuzzy, categorias_fuzzy)
    else:
        print("\nArquivo fuzzy nao encontrado. Comparacao nao sera gerada.")
