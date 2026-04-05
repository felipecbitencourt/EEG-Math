"""
Distribution of included studies by topic and megatopic.
Style: grouped bar chart coloured by megatopic + legend on the right.
Output: resultados/q1/figuras/q1_distribuicao_topicos.png
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

# ── paths ─────────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parent.parent
OUT  = REPO / "resultados" / "q1" / "figuras" / "q1_distribuicao_topicos.png"

# ── data ──────────────────────────────────────────────────────────────────────
topics = {
    # (megatopic, topic_code): count
    (1,  1): 5,
    (1,  2): 7,
    (1,  3): 4,
    (1,  4): 8,
    (1,  9): 4,
    (1, 11): 2,
    (2,  5): 11,
    (2, 10): 12,
    (3,  6): 12,
    (3,  7): 9,
    (3,  8): 14,
}

# ordered x-axis: grouped by megatopic
ORDER = [(1,1),(1,2),(1,3),(1,4),(1,9),(1,11),(2,5),(2,10),(3,6),(3,7),(3,8)]
labels = [f"T{t}" for (_, t) in ORDER]
counts = [topics[k] for k in ORDER]
colors_map = {1: "#1c3f7a", 2: "#d63c8e", 3: "#1a9e8a"}
bar_colors = [colors_map[m] for (m, _) in ORDER]

# ── legend content ─────────────────────────────────────────────────────────────
MT_LABELS = {
    1: "Individual Profiles & Cognitive Differences",
    2: "Computational Methods & Classification",
    3: "Cognitive Processes & Neural Dynamics",
}
TOPIC_LABELS = {
    1:  "T1 – Mathematics and Clinical Disorders",
    2:  "T2 – Math Anxiety and Stress",
    3:  "T3 – Gender and Sex Differences",
    4:  "T4 – Giftedness and High Abilities",
    9:  "T9 – Development, Education & School Context",
    11: "T11 – Experimental Conditions & Context",
    5:  "T5 – Classification Models & Machine Learning",
    10: "T10 – Spectral Analysis",
    6:  "T6 – Connectivity and Brain Networks",
    7:  "T7 – Math Performance & Skill Differences",
    8:  "T8 – Cognitive Load, Fatigue & Mental State",
}
MT_TOPICS = {
    1: [1, 2, 3, 4, 9, 11],
    2: [5, 10],
    3: [6, 7, 8],
}

# ── figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6.5), facecolor="white")
ax.set_facecolor("white")

x = np.arange(len(ORDER))
bars = ax.bar(x, counts, color=bar_colors, width=0.65,
              edgecolor="white", linewidth=0.8, zorder=2)

# value labels on top of bars
for bar, val in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
            str(val), ha="center", va="bottom", fontsize=10, color="#333333")

# x-axis
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.set_xlabel("Topics", fontsize=12, labelpad=8)
ax.set_ylabel("Number of Articles", fontsize=12, labelpad=8)
ax.set_title(
    "Distribution of Included Studies by Topic and Megatopic\n"
    "EEG & Mathematical Processes — Systematic Review (N = 88)",
    fontsize=12, fontweight="bold", pad=12
)
ax.set_ylim(0, max(counts) + 2.5)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5, zorder=1)
ax.set_axisbelow(True)

# subtle vertical separators between megatopic groups
# groups end at index 5 (after T11) and 7 (after T10)
for sep_x in [5.5, 7.5]:
    ax.axvline(sep_x, color="#cccccc", linewidth=1.2, linestyle="--", zorder=0)

# ── legend (right side, outside axes) ────────────────────────────────────────
legend_handles = []

legend_handles.append(
    mpatches.Patch(facecolor="none", edgecolor="none",
                   label="Megatopics & Topics")
)

for mt in [1, 2, 3]:
    # megatopic header line (bold, colored square)
    legend_handles.append(
        mpatches.Patch(
            facecolor=colors_map[mt], edgecolor="none",
            label=f"  {MT_LABELS[mt]}"
        )
    )
    # topic lines (circle markers, same color but lighter dot)
    for t in MT_TOPICS[mt]:
        legend_handles.append(
            Line2D([0], [0], marker="o", color="none",
                   markerfacecolor=colors_map[mt],
                   markeredgecolor="none", markersize=8,
                   label=f"    {TOPIC_LABELS[t]}")
        )

leg = ax.legend(
    handles=legend_handles,
    loc="upper left",
    bbox_to_anchor=(1.01, 1.0),
    frameon=True,
    framealpha=0.95,
    edgecolor="#cccccc",
    fontsize=9,
    title="Megatopics & Topics",
    title_fontsize=9.5,
    handlelength=1.2,
    handleheight=1.1,
    borderpad=0.9,
    labelspacing=0.55,
)
# make title bold
leg.get_title().set_fontweight("bold")

# hide the dummy first handle label
leg.get_texts()[0].set_text("")
leg.legend_handles[0].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, dpi=180, bbox_inches="tight", facecolor="white")
print(f"Saved → {OUT}")
