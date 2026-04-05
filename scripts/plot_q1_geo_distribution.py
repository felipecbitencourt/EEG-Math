"""
Geographic distribution of EEG + Mathematical Processes publications.
Style: Robinson projection, cream→dark-red choropleth, star markers per country.
Output: resultados/q1/figuras/q1_distribuicao_geografica.png
"""

from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ── paths ─────────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parent.parent
OUT  = REPO / "resultados" / "q1" / "figuras" / "q1_distribuicao_geografica.png"
SHP  = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

# ── publication data (ISO-A3) ─────────────────────────────────────────────────
pub_data = {
    "USA": 15, "CHN": 12, "KOR":  7, "GBR":  6,
    "CHE":  5, "DEU":  5, "GRC":  5,
    "IND":  4, "RUS":  4,
    "BGD":  3, "NLD":  3,
    "ITA":  2, "MYS":  2, "MEX":  2, "IRN":  2,
    "TWN":  2, "CZE":  2, "TUR":  2,
    "JPN":  1, "NZL":  1, "CHL":  1, "AUT":  1,
    "VNM":  1, "SWE":  1, "BRA":  1, "ROU":  1,
    "IDN":  1, "MAR":  1, "SGP":  1, "ESP":  1,
    "FIN":  1, "ISR":  1, "SAU":  1, "BEL":  1,
    "CAN":  1,
}

# approximate centroids for star markers (lon, lat)
centroids = {
    "USA": (-98,  38), "CHN": (105,  35), "KOR": (128,  36), "GBR":  (-2,  54),
    "CHE": (  8,  47), "DEU": ( 10,  51), "GRC": ( 22,  39),
    "IND": ( 78,  21), "RUS": ( 95,  60),
    "BGD": ( 90,  24), "NLD": (  5,  52),
    "ITA": ( 12,  43), "MYS": (110,   4), "MEX": (-102, 24), "IRN": ( 53,  33),
    "TWN": (121,  24), "CZE": ( 16,  50), "TUR": ( 35,  39),
    "JPN": (138,  37), "NZL": (172, -41), "CHL": (-71, -35), "AUT": ( 14,  47),
    "VNM": (106,  16), "SWE": ( 18,  60), "BRA": (-52, -14), "ROU": ( 25,  46),
    "IDN": (118,  -2), "MAR": ( -7,  32), "SGP": (104,   1), "ESP": ( -4,  40),
    "FIN": ( 26,  64), "ISR": ( 35,  31), "SAU": ( 45,  25), "BEL": (  4,  51),
    "CAN": (-96,  57),
}

# ── load world shapefile ──────────────────────────────────────────────────────
world = gpd.read_file(SHP)

# merge publication counts
pub_series = pd.Series(pub_data, name="pubs")
world = world.merge(pub_series, left_on="ISO_A3", right_index=True, how="left")

# Taiwan fix (ISO_A3 = -99 in some datasets; use ADM0_A3_TW)
mask_tw = world["ADM0_A3"] == "TWN"
if world.loc[mask_tw, "pubs"].isna().all():
    world.loc[mask_tw, "pubs"] = pub_data.get("TWN", np.nan)

# reproject to Robinson
world = world.to_crs("+proj=robin")

# ── colour map: cream → dark red (matching reference image) ───────────────────
cmap = LinearSegmentedColormap.from_list(
    "pub_red",
    ["#fdf0e0", "#f7c89b", "#e8855a", "#c0392b", "#7b0000"],
    N=256,
)
norm = mcolors.Normalize(vmin=0, vmax=15)

# ── figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7.5), facecolor="white")
ax.set_facecolor("white")

# base: countries without data → light cream
world_no = world[world["pubs"].isna()]
world_no.plot(ax=ax, color="#f5f0e8", edgecolor="#bbbbbb", linewidth=0.35)

# countries with data → coloured
world_yes = world[world["pubs"].notna()]
world_yes.plot(ax=ax, column="pubs", cmap=cmap, norm=norm,
               edgecolor="#888888", linewidth=0.4)

# ── star markers ──────────────────────────────────────────────────────────────
# project centroids (lon/lat → Robinson)
import pyproj
from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:4326", "+proj=robin", always_xy=True)

for iso, (lon, lat) in centroids.items():
    x, y = transformer.transform(lon, lat)
    ax.plot(x, y, marker="*", markersize=7,
            color="#9b30d0", markeredgecolor="white",
            markeredgewidth=0.4, zorder=5, linestyle="none")

# ── colour bar ────────────────────────────────────────────────────────────────
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation="vertical",
                    shrink=0.55, pad=0.02, aspect=20)
cbar.set_label("Publications (n)", fontsize=11)
cbar.set_ticks([0, 3, 6, 9, 12, 15])
cbar.ax.tick_params(labelsize=10)

# ── Robinson border (oval) ────────────────────────────────────────────────────
# draw world outline
world.boundary.plot(ax=ax, color="#aaaaaa", linewidth=0.25)

# ── title & cleanup ───────────────────────────────────────────────────────────
ax.set_title(
    "Geographic Distribution of EEG and Mathematical Processes Research\n"
    "Publications per country — systematic review corpus (N = 88)",
    fontsize=12, pad=10,
)
ax.set_axis_off()

fig.tight_layout()
fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved → {OUT}")
