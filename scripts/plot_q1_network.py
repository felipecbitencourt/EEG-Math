"""
Q1 — Network graph linking methodological dimensions per study.
Three layers: Type of Investigation → Temporal Dimension → Subject Comparison.
Edge width ∝ number of studies sharing that combination.
Output: resultados/q1/figuras/q1_b2_rede_metodologica.png
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch, FancyBboxPatch, Circle
from matplotlib.lines import Line2D

# ── paths ─────────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parent.parent
CSV  = REPO / "dados" / "tabela_normatizada.csv"
OUT  = REPO / "resultados" / "q1" / "figuras" / "q1_b2_rede_metodologica.png"

# ── load & map ────────────────────────────────────────────────────────────────
df = pd.read_csv(CSV)
c_inv  = df.columns[6]
c_time = df.columns[7]
c_comp = df.columns[8]

inv_map = {
    "Experimental":                             "Experimental",
    "Estudo Metodológico, Experimental":        "Experimental",
    "Quase-experimental":                       "Quasi-experimental",
    "Estudo Metodológico, Quase-experimental":  "Quasi-experimental",
    "Observacional / Não-experimental":         "Observational",
    "Estudo Metodológico":                      "Methodological",
}
time_map = {
    "Transversal (Cross-sectional)": "Cross-sectional",
    "Longitudinal":                  "Longitudinal",
    "Retrospectivo":                 "Retrospective",
}
def map_comp(val):
    if pd.isna(val): return None
    v = str(val)
    if "Misto" in v or "Mixed" in v: return "Mixed design"
    if "Intra" in v or "Within" in v: return "Within-subjects"
    return "Between-subjects"

df["inv"]  = df[c_inv].map(inv_map)
df["time"] = df[c_time].map(time_map)
df["comp"] = df[c_comp].apply(map_comp)
dfc = df[["inv", "time", "comp"]].dropna()

# ── node definitions ──────────────────────────────────────────────────────────
L1 = ["Quasi-experimental", "Experimental", "Observational", "Methodological"]
L2 = ["Cross-sectional",    "Longitudinal", "Retrospective"]
L3 = ["Within-subjects",    "Mixed design", "Between-subjects"]

# counts per node
cnt1 = dfc["inv"].value_counts().reindex(L1, fill_value=0)
cnt2 = dfc["time"].value_counts().reindex(L2, fill_value=0)
cnt3 = dfc["comp"].value_counts().reindex(L3, fill_value=0)

# edge counts
edges12 = dfc.groupby(["inv",  "time"]).size().to_dict()
edges23 = dfc.groupby(["time", "comp"]).size().to_dict()

# ── layout ────────────────────────────────────────────────────────────────────
X = {1: 0.10, 2: 0.50, 3: 0.90}   # x positions of layers

def y_pos(n):
    """Vertically centred positions for n nodes."""
    if n == 1: return [0.5]
    return list(np.linspace(0.15, 0.85, n))

Y1 = {lbl: y for lbl, y in zip(L1, y_pos(len(L1)))}
Y2 = {lbl: y for lbl, y in zip(L2, y_pos(len(L2)))}
Y3 = {lbl: y for lbl, y in zip(L3, y_pos(len(L3)))}

# ── colour palettes ────────────────────────────────────────────────────────────
COL1 = {"Quasi-experimental": "#1a4e87",
        "Experimental":       "#2b7bbd",
        "Observational":      "#6aaed6",
        "Methodological":     "#b3d4ea"}

COL2 = {"Cross-sectional": "#1a6e4e",
        "Longitudinal":     "#2a9d6a",
        "Retrospective":    "#80c7a4"}

COL3 = {"Within-subjects":  "#6a1a7a",
        "Mixed design":     "#9b3bbf",
        "Between-subjects": "#c98fe0"}

ALL_COLORS = {**COL1, **COL2, **COL3}

# ── helpers ────────────────────────────────────────────────────────────────────
MAX_EDGE = max(list(edges12.values()) + list(edges23.values()))
MAX_LW   = 14.0
MIN_LW   = 0.6

def lw_scale(count):
    return MIN_LW + (count / MAX_EDGE) * (MAX_LW - MIN_LW)

def draw_bezier(ax, x0, y0, x1, y1, count, color):
    lw = lw_scale(count)
    mid_x = (x0 + x1) / 2
    verts = [(x0, y0), (mid_x, y0), (mid_x, y1), (x1, y1)]
    codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4]
    path = MPath(verts, codes)
    patch = PathPatch(path, facecolor="none", edgecolor=color,
                      lw=lw, alpha=0.40, zorder=1)
    ax.add_patch(patch)
    # count label at midpoint
    mx, my = mid_x, (y0 + y1) / 2
    ax.text(mx, my, str(count), ha="center", va="center",
            fontsize=6.5, color="#444444",
            bbox=dict(facecolor="white", edgecolor="none",
                      alpha=0.7, boxstyle="round,pad=0.1"))

NODE_R = 0.038

def draw_node(ax, x, y, label, count, color):
    # halo / shadow
    circ_shadow = Circle((x, y), NODE_R + 0.008, color="#cccccc",
                          zorder=2, alpha=0.5)
    ax.add_patch(circ_shadow)
    # main circle
    circ = Circle((x, y), NODE_R, color=color, zorder=3)
    ax.add_patch(circ)
    # count inside
    ax.text(x, y, str(count), ha="center", va="center",
            fontsize=9, fontweight="bold", color="white", zorder=4)

# ── draw ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6.5), facecolor="white")
ax.set_facecolor("#f8f9fb")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_aspect("equal", adjustable="box")
ax.set_axis_off()

# -- edges L1→L2
for (i, t), cnt in edges12.items():
    if cnt == 0 or i not in Y1 or t not in Y2: continue
    draw_bezier(ax, X[1] + NODE_R, Y1[i],
                    X[2] - NODE_R, Y2[t],
                    cnt, COL1[i])

# -- edges L2→L3
for (t, c), cnt in edges23.items():
    if cnt == 0 or t not in Y2 or c not in Y3: continue
    draw_bezier(ax, X[2] + NODE_R, Y2[t],
                    X[3] - NODE_R, Y3[c],
                    cnt, COL2[t])

# -- nodes L1
for lbl in L1:
    draw_node(ax, X[1], Y1[lbl], cnt1[lbl], cnt1[lbl], COL1[lbl])
    ax.text(X[1] - NODE_R - 0.015, Y1[lbl], lbl,
            ha="right", va="center", fontsize=9.5,
            color=COL1[lbl], fontweight="bold")

# -- nodes L2
for lbl in L2:
    draw_node(ax, X[2], Y2[lbl], cnt2[lbl], cnt2[lbl], COL2[lbl])
    ax.text(X[2], Y2[lbl] + NODE_R + 0.035, lbl,
            ha="center", va="bottom", fontsize=9.5,
            color=COL2[lbl], fontweight="bold")

# -- nodes L3
for lbl in L3:
    draw_node(ax, X[3], Y3[lbl], cnt3[lbl], cnt3[lbl], COL3[lbl])
    ax.text(X[3] + NODE_R + 0.015, Y3[lbl], lbl,
            ha="left", va="center", fontsize=9.5,
            color=COL3[lbl], fontweight="bold")

# -- layer header labels
header_y = 0.94
for x, label, color in [
    (X[1], "Type of Investigation", "#1a4e87"),
    (X[2], "Temporal Dimension",    "#1a6e4e"),
    (X[3], "Subject Comparison",    "#6a1a7a"),
]:
    ax.text(x, header_y, label, ha="center", va="bottom",
            fontsize=11, fontweight="bold", color=color,
            bbox=dict(facecolor="white", edgecolor=color,
                      linewidth=1.2, boxstyle="round,pad=0.3",
                      alpha=0.9))

# -- layer separators (faint vertical lines)
for x in [X[1], X[2], X[3]]:
    ax.axvline(x, color="#dddddd", lw=0.8, zorder=0,
               ymin=0.05, ymax=0.88)

# -- title & note
ax.set_title(
    "Network of Methodological Dimensions — EEG & Math Research  (N = 88)\n"
    "Node size = number of studies  ·  Edge width ∝ co-occurrence frequency",
    fontsize=11, pad=16, color="#333333"
)

fig.tight_layout()
fig.savefig(OUT, dpi=180, bbox_inches="tight", facecolor="white")
print(f"Saved → {OUT}")
