"""
Q1 — B2: Global methodological profile
Three horizontal-bar panels:
  1. Type of investigation
  2. Temporal dimension
  3. Subject comparison
Output: resultados/q1/figuras/q1_b2_perfil_metodologico.png
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── paths ─────────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parent.parent
CSV  = REPO / "dados" / "tabela_normatizada.csv"
OUT  = REPO / "resultados" / "q1" / "figuras" / "q1_b2_perfil_metodologico.png"

# ── load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(CSV)
c_inv  = df.columns[6]   # tipo investigação
c_time = df.columns[7]   # dimensão temporal
c_comp = df.columns[8]   # comparação sujeitos

# ── aggregate categories ───────────────────────────────────────────────────────
# --- 1. Type of investigation (merge methodological variants) -----------------
inv_map = {
    "Experimental":                          "Experimental",
    "Estudo Metodológico, Experimental":     "Experimental",
    "Quase-experimental":                    "Quasi-experimental",
    "Estudo Metodológico, Quase-experimental": "Quasi-experimental",
    "Observacional / Não-experimental":      "Observational",
    "Estudo Metodológico":                   "Methodological study",
}
inv_counts = (
    df[c_inv].map(inv_map)
    .value_counts()
    .reindex(["Quasi-experimental", "Experimental",
              "Observational", "Methodological study"])
    .fillna(0).astype(int)
)

# --- 2. Temporal dimension ----------------------------------------------------
time_map = {
    "Transversal (Cross-sectional)": "Cross-sectional",
    "Longitudinal":                  "Longitudinal",
    "Retrospectivo":                 "Retrospective",
}
time_counts = (
    df[c_time].map(time_map)
    .value_counts()
    .reindex(["Cross-sectional", "Longitudinal", "Retrospective"])
    .fillna(0).astype(int)
)

# --- 3. Subject comparison ----------------------------------------------------
def map_comp(val):
    if pd.isna(val):
        return None
    v = str(val)
    if "Misto" in v or "Mixed" in v:
        return "Mixed design"
    if "Intra" in v or "Within" in v:
        return "Within-subjects"
    if "Entre" in v or "Between" in v:
        return "Between-subjects"
    return "Other"

comp_counts = (
    df[c_comp].apply(map_comp)
    .value_counts()
    .reindex(["Within-subjects", "Mixed design", "Between-subjects"])
    .fillna(0).astype(int)
)

# ── colour palettes ────────────────────────────────────────────────────────────
BLUE_SHADES  = ["#2166ac", "#4393c3", "#92c5de", "#d1e5f0"]
TEAL_SHADES  = ["#1a7abf", "#4da9d7", "#a8d4eb"]
GREEN_SHADES = ["#2c7bb6", "#5aaecc", "#abd9e9"]

# ── plot ───────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5),
                         gridspec_kw={"wspace": 0.55})

def hbar(ax, series, colors, title, xlabel="Number of studies (N)"):
    labels = series.index.tolist()
    values = series.values

    bars = ax.barh(labels, values, color=colors[:len(labels)],
                   edgecolor="white", height=0.55)

    # value labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
                f"n = {val}", va="center", ha="left", fontsize=9.5)

    ax.set_xlabel(xlabel, fontsize=9.5)
    ax.set_title(title, fontsize=10.5, fontweight="bold", pad=8)
    ax.set_xlim(0, max(values) * 1.28)
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=9.5)
    ax.tick_params(axis="x", labelsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)

hbar(axes[0], inv_counts,  BLUE_SHADES,  "A  —  Type of Investigation")
hbar(axes[1], time_counts, TEAL_SHADES,  "B  —  Temporal Dimension")
hbar(axes[2], comp_counts, GREEN_SHADES, "C  —  Subject Comparison")

fig.suptitle(
    "Methodological Profile of EEG and Mathematical Processes Studies  (N = 88)",
    fontsize=12, fontweight="bold", y=1.02
)

fig.tight_layout()
fig.savefig(OUT, dpi=180, bbox_inches="tight")
print(f"Saved → {OUT}")
