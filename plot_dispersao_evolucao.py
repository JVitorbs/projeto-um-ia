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


def plotar_dispersao_e_evolucao(historico, categorias, caminho_log: Path):
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

    fig.suptitle(f"Analise do GA | log: {caminho_log.name}")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    caminho = resolver_caminho_log()
    historico_dados, categorias_dados = carregar_dados(caminho)
    print(f"Log carregado: {caminho}")
    print(f"Geracoes no historico: {len(historico_dados)}")
    print(f"Categorias disponiveis: {len(categorias_dados)}")
    plotar_dispersao_e_evolucao(historico_dados, categorias_dados, caminho)
