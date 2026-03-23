import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt

def _resolver_caminho_log():
    # Permite: python plot.py /caminho/para/evolucao.json
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()

    raiz_projeto = Path(__file__).resolve().parent
    return raiz_projeto / "logs" / "evolucao.json"


caminho_log = _resolver_caminho_log()
if not caminho_log.exists():
    raise FileNotFoundError(
        f"Arquivo de log nao encontrado: {caminho_log}. "
        "Execute o main.py primeiro ou informe o caminho do JSON."
    )

with caminho_log.open(encoding="utf-8") as f:

    bruto = json.load(f)

if isinstance(bruto, dict):
    data = bruto.get("historico", [])
    categorias = bruto.get("categorias", [])
    top3 = bruto.get("top3", [])
else:
    data = bruto
    categorias = []
    top3 = []

if not data:
    raise ValueError("logs/evolucao.json não possui histórico para plotar")

ger = [d["geracao"] for d in data]
fit_melhor = [d["melhor"] for d in data]
fit_melhor_acumulado = [d.get("melhor_ate_agora", d["melhor"]) for d in data]
fit_media = [d.get("media", d["melhor"]) for d in data]
fit_pior = [d.get("pior", d.get("media", d["melhor"])) for d in data]
fit_mediana = [d.get("mediana", d.get("media", d["melhor"])) for d in data]
fit_q1 = [d.get("q1", d.get("media", d["melhor"])) for d in data]
fit_q3 = [d.get("q3", d.get("media", d["melhor"])) for d in data]
tempo_melhor = [d.get("tempo", 0) for d in data]
tempo_melhor_acumulado = [d.get("tempo_melhor_ate_agora", d.get("tempo", 0)) for d in data]
tempo_pior = [d.get("tempo_pior", d.get("tempo", 0)) for d in data]
tempo_mediana = [d.get("tempo_mediana", d.get("tempo", 0)) for d in data]
tempo_q1 = [d.get("tempo_q1", d.get("tempo", 0)) for d in data]
tempo_q3 = [d.get("tempo_q3", d.get("tempo", 0)) for d in data]
diversidade = [d.get("diversidade", 0.0) for d in data]
mut_rate = [d.get("mutation_rate", 0.0) for d in data]

idx_melhor_global = min(range(len(data)), key=lambda i: fit_melhor_acumulado[i])

quedas_tempo = []
for i in range(1, len(tempo_melhor_acumulado)):
    if tempo_melhor_acumulado[i] < tempo_melhor_acumulado[i - 1]:
        quedas_tempo.append(i)

print("Resumo do histórico")
print(f"- Log carregado: {caminho_log}")
print(f"- Melhor fitness global: {fit_melhor_acumulado[idx_melhor_global]:.2f}")
print(f"- Geração do melhor global: {ger[idx_melhor_global]}")
print(f"- Tempo total no melhor global: {tempo_melhor_acumulado[idx_melhor_global]} semestres")
print(f"- Quedas de tempo observadas: {len(quedas_tempo)}")
print(f"- Pior fitness na geração inicial: {fit_pior[0]:.2f}")
print(f"- Mediana de fitness na geração inicial: {fit_mediana[0]:.2f}")
if categorias:
    melhor_categoria = min(categorias, key=lambda c: c.get("tempo_medio", float("inf")))
    print(
        f"- Melhor categoria observada: {melhor_categoria['categoria']} "
        f"(media {melhor_categoria['tempo_medio']:.2f} semestres, "
        f"min {melhor_categoria.get('tempo_min', 0):.0f})"
    )

fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1.0])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

ax1.fill_between(ger, fit_q1, fit_q3, alpha=0.18, label="Faixa central (Q1-Q3)")
ax1.fill_between(ger, fit_melhor, fit_pior, alpha=0.08, label="Faixa total (melhor-pior)")
ax1.plot(ger, fit_melhor, label="Melhor fitness (geração)", linewidth=2)
ax1.plot(ger, fit_melhor_acumulado, label="Melhor fitness (acumulado)", linestyle="--", linewidth=2)
ax1.plot(ger, fit_media, label="Média da população", alpha=0.8)
ax1.plot(ger, fit_mediana, label="Mediana da população", linestyle=":")
ax1.plot(ger, fit_pior, label="Pior fitness", alpha=0.9)
ax1.set_ylabel("Fitness")
ax1.set_title("Convergência do GA com dispersão da população")
ax1.legend()
ax1.grid(alpha=0.2)

ax2.fill_between(ger, tempo_q1, tempo_q3, alpha=0.18, label="Faixa central (Q1-Q3)")
ax2.fill_between(ger, tempo_melhor, tempo_pior, alpha=0.08, label="Faixa total (melhor-pior)")
ax2.plot(ger, tempo_melhor, label="Tempo do melhor da geração", linewidth=2)
ax2.plot(ger, tempo_mediana, label="Tempo mediano da população", linestyle=":")
ax2.plot(ger, tempo_pior, label="Pior tempo da geração", alpha=0.9)
ax2.step(
    ger,
    tempo_melhor_acumulado,
    where="post",
    label="Melhor tempo acumulado (deve diminuir)",
    linestyle="--",
    linewidth=2,
)

if quedas_tempo:
    xq = [ger[i] for i in quedas_tempo]
    yq = [tempo_melhor_acumulado[i] for i in quedas_tempo]
    ax2.scatter(xq, yq, color="red", s=35, zorder=3, label="Pontos de queda")

    for i in quedas_tempo:
        ax2.annotate(
            f"g{ger[i]}: {tempo_melhor_acumulado[i]}",
            (ger[i], tempo_melhor_acumulado[i]),
            textcoords="offset points",
            xytext=(4, -12),
            fontsize=8,
        )

ax2.set_xlabel("Geração")
ax2.set_ylabel("Tempo total (semestres)")
ax2.set_title("Evolução do tempo com dispersão da população")
ax2.legend()
ax2.grid(alpha=0.2)

ax3.plot(ger, diversidade, label="Diversidade da população")
ax3.plot(ger, mut_rate, label="Taxa de mutação efetiva", linestyle="--")
ax3.set_ylabel("Sinais de busca")
ax3.set_title("Diversidade e mutação adaptativa")
ax3.legend()
ax3.grid(alpha=0.2)

if categorias:
    categorias_ordenadas = sorted(categorias, key=lambda c: c.get("tempo_medio", float("inf")))
    nomes = [c["categoria"] for c in categorias_ordenadas]
    tempos_min = [c.get("tempo_min", 0) for c in categorias_ordenadas]
    tempos_medios = [c.get("tempo_medio", 0) for c in categorias_ordenadas]

    ax4.bar(nomes, tempos_medios, label="Tempo médio", alpha=0.75)
    ax4.scatter(nomes, tempos_min, color="red", label="Tempo mínimo observado", zorder=3)
    for nome, valor in zip(nomes, tempos_min):
        ax4.annotate(
            f"{valor:.1f}",
            (nome, valor),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=8,
        )
    ax4.set_ylabel("Semestres")
    ax4.set_title("Melhor resultado por categoria")
    ax4.legend()
    ax4.grid(alpha=0.2, axis="y")
    ax4.tick_params(axis="x", rotation=20)
else:
    ax4.axis("off")
    resumo = ["Sem dados de categoria no log atual."]
    if top3:
        resumo.append("")
        resumo.append("Top 3 finais:")
        for item in top3:
            resumo.append(
                f"TOP {item['rank']}: {item['tempo']:.1f} sem | fit {item['fitness']:.1f}"
            )
            resumo.append(item.get("perfil_str", ""))
    ax4.text(0.02, 0.98, "\n".join(resumo), va="top", ha="left", fontsize=10)

if top3 and categorias:
    linhas = ["Top 3 finais:"]
    for item in top3:
        linhas.append(
            f"TOP {item['rank']}: {item['tempo']:.1f} sem | fit {item['fitness']:.1f} | {item.get('perfil_str', '')}"
        )
    ax4.text(
        1.02,
        0.98,
        "\n".join(linhas),
        transform=ax4.transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85},
    )

plt.tight_layout()
plt.show()