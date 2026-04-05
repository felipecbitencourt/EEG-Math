"""
UMAP projection of EEG & Math studies coloured by topic/megatopic.
English version of umap_estatico.py — all labels in English.
Output: resultados/q1/figuras/q1_umap_topicos.png
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import umap
from sklearn.feature_extraction.text import TfidfVectorizer

# ── paths ─────────────────────────────────────────────────────────────────────
REPO     = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "revisão-egg+math - Limpo.csv"
OUT      = REPO / "resultados" / "q1" / "figuras" / "q1_umap_topicos.png"

MIN_TEXT_LEN = 100

# ── English labels ─────────────────────────────────────────────────────────────
megatopic_names = {
    1: "Individual Profiles",
    2: "Methods & Classification",
    3: "Cognitive Processes",
}

structure = {
    1: [
        (1,  "T1 – Clinical Disorders"),
        (2,  "T2 – Math Anxiety"),
        (3,  "T3 – Gender Differences"),
        (4,  "T4 – Giftedness"),
        (9,  "T9 – Education & Development"),
        (11, "T11 – Experimental Context"),
    ],
    2: [
        (5,  "T5 – Classification / ML"),
        (10, "T10 – Spectral Analysis"),
    ],
    3: [
        (6, "T6 – Connectivity & Networks"),
        (7, "T7 – Math Skill & Performance"),
        (8, "T8 – Cognitive Load & Fatigue"),
    ],
}

markers      = {1: "o", 2: "s", 3: "^"}
topic_colors = {
    1:  "#1f77b4",
    2:  "#ff7f0e",
    3:  "#2ca02c",
    4:  "#d62728",
    9:  "#bcbd22",
    11: "#7f7f7f",
    5:  "#9467bd",
    10: "#17becf",
    6:  "#8c564b",
    7:  "#e377c2",
    8:  "#000000",
}

# ── load & process ─────────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")
df = df.dropna(subset=["Topico", "Megatopico", "Texto_Completo"])
df["Topico"]     = pd.to_numeric(df["Topico"],     errors="coerce").fillna(0).astype(int)
df["Megatopico"] = pd.to_numeric(df["Megatopico"], errors="coerce").fillna(0).astype(int)
df = df[df["Texto_Completo"].str.len() >= MIN_TEXT_LEN].reset_index(drop=True)
print(f"  {len(df)} studies retained.")

# ── TF-IDF + UMAP ─────────────────────────────────────────────────────────────
print("Vectorising (TF-IDF)...")
vectorizer = TfidfVectorizer(
    stop_words="english", max_df=0.9, min_df=2, ngram_range=(1, 2)
)
X = vectorizer.fit_transform(df["Texto_Completo"].astype(str))

print("Computing UMAP...")
reducer = umap.UMAP(
    n_neighbors=7, min_dist=0.3, n_components=2,
    random_state=42, metric="cosine"
)
embedding = reducer.fit_transform(X)
df["x"] = embedding[:, 0]
df["y"] = embedding[:, 1]

# ── plot ───────────────────────────────────────────────────────────────────────
print("Plotting...")
plt.rcParams["font.family"] = "DejaVu Serif"
plt.rcParams["font.size"]   = 12

fig, ax = plt.subplots(figsize=(12, 8), facecolor="white")
ax.set_facecolor("white")

for mt_id, topics_list in structure.items():
    marker  = markers[mt_id]
    df_mega = df[df["Megatopico"] == mt_id]
    if df_mega.empty:
        continue
    for t_id, _ in topics_list:
        df_topic = df_mega[df_mega["Topico"] == t_id]
        if df_topic.empty:
            continue
        ax.scatter(
            df_topic["x"], df_topic["y"],
            color=topic_colors.get(t_id, "black"),
            marker=marker, s=80, alpha=0.8,
            edgecolor="white", linewidth=0.5,
        )

ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("UMAP Dimension 1", fontweight="bold")
ax.set_ylabel("UMAP Dimension 2", fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ── custom legend ──────────────────────────────────────────────────────────────
legend_elements = []
for mt_id, topics_list in structure.items():
    legend_elements.append(
        Line2D([0], [0], color="w",
               label=rf"$\bf{{Megatopic\ {mt_id}:\ {megatopic_names[mt_id]}}}$",
               markersize=0)
    )
    for t_id, t_label in topics_list:
        legend_elements.append(
            Line2D([0], [0], marker=markers[mt_id], color="w",
                   label=t_label,
                   markerfacecolor=topic_colors.get(t_id, "black"),
                   markersize=9,
                   markeredgecolor="white", markeredgewidth=0.5)
        )
    legend_elements.append(Line2D([0], [0], color="w", label=" ", markersize=0))

ax.legend(
    handles=legend_elements,
    loc="upper left",
    bbox_to_anchor=(1.01, 1.01),
    frameon=False,
    fontsize=10,
    labelspacing=0.4,
)

plt.tight_layout()
plt.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Saved → {OUT}")
