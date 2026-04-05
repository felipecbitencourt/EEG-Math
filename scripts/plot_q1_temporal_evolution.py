"""
Temporal evolution of publications on EEG and mathematical processes.
Bars: total publications per year.
Line: studies in Megatopic 2 (Machine Learning & Signal Classification) per year.
Output: resultados/q1/figuras/q1_evolucao_temporal.png
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── paths ─────────────────────────────────────────────────────────────────────
REPO   = Path(__file__).resolve().parent.parent
META   = REPO / "dados" / "metadados_artigos_com_topicos - Cópia de metadados_artigos_com_topicos.csv"
OUT    = REPO / "resultados" / "q1" / "figuras" / "q1_evolucao_temporal.png"

# ── load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(META, encoding="utf-8-sig")
df.columns = [c.strip() for c in df.columns]
# rename for convenience
df = df.rename(columns={df.columns[0]: "file", "Ano": "year",
                         df.columns[2]: "topic", df.columns[3]: "megatopic"})
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

# ── build yearly series ───────────────────────────────────────────────────────
year_min, year_max = df["year"].min(), df["year"].max()
all_years = list(range(year_min, year_max + 1))

total_by_year = df.groupby("year").size().reindex(all_years, fill_value=0)
mt2_by_year   = (df[df["megatopic"] == 2]
                 .groupby("year").size()
                 .reindex(all_years, fill_value=0))

# ── aesthetics ────────────────────────────────────────────────────────────────
BAR_COLOR  = "#4C72B0"   # steel blue – total
LINE_COLOR = "#DD8452"   # burnt orange – Megatopic 2
MARKER_COLOR = "#C44E52" # red accent for markers

fig, ax1 = plt.subplots(figsize=(14, 5.5))

# bars – total publications
bars = ax1.bar(all_years, total_by_year.values,
               color=BAR_COLOR, alpha=0.80,
               width=0.7, zorder=2, label="Total publications")

# thin grid
ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=6))
ax1.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.6, zorder=1)
ax1.set_axisbelow(True)

# line – ML & Classification studies (same left y-axis)
ax1.plot(all_years, mt2_by_year.values,
         color=LINE_COLOR, linewidth=2.2, marker="o",
         markersize=5, markerfacecolor=MARKER_COLOR,
         markeredgecolor="white", markeredgewidth=0.8,
         zorder=3, label="ML & Classification studies")

# ── x-axis ────────────────────────────────────────────────────────────────────
ax1.set_xlim(year_min - 0.8, year_max + 0.8)
ax1.set_xticks(all_years)
ax1.set_xticklabels([str(y) for y in all_years], rotation=90, ha="center", fontsize=8)

# ── labels & title ────────────────────────────────────────────────────────────
ax1.set_xlabel("Year of publication", fontsize=11)
ax1.set_ylabel("Number of publications", fontsize=11)
ax1.set_title(
    "Temporal Evolution of EEG and Mathematical Processes Research\n"
    "Total publications (bars) and ML & Classification studies (line)",
    fontsize=11, pad=12
)

# ── combined legend ───────────────────────────────────────────────────────────
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Patch(facecolor=BAR_COLOR, alpha=0.80, label="Total publications (N = 88)"),
    Line2D([0], [0], color=LINE_COLOR, linewidth=2.2, marker="o",
           markersize=6, markerfacecolor=MARKER_COLOR,
           markeredgecolor="white",
           label="ML & Classification (n = 23)"),
]
ax1.legend(handles=legend_elements, loc="upper left",
           framealpha=0.9, fontsize=9)

# ── value labels on bars (only non-zero) ─────────────────────────────────────
for rect, val in zip(bars, total_by_year.values):
    if val > 0:
        ax1.text(rect.get_x() + rect.get_width() / 2,
                 rect.get_height() + 0.08,
                 str(val), ha="center", va="bottom",
                 fontsize=7, color="#333333")

fig.tight_layout()
fig.savefig(OUT, dpi=180, bbox_inches="tight")
print(f"Saved → {OUT}")
