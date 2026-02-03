# =========================================================
# 1. Importações
# =========================================================
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import urllib.request
import os

# =========================================================
# 2. Frequências já consolidadas
# =========================================================
country_counts_dict = {
    "United States of America": 15,
    "China": 12,
    "South Korea": 7,
    "United Kingdom": 6,
    "Switzerland": 5,
    "Germany": 5,
    "Greece": 5,
    "India": 4,
    "Russia": 4,
    "Bangladesh": 3,
    "Netherlands": 3,
    "Italy": 2,
    "Malaysia": 2,
    "Mexico": 2,
    "Iran": 2,
    "Taiwan": 2,
    "Czech Republic": 2,
    "Turkey": 2,
    "Japan": 1,
    "New Zealand": 1,
    "Chile": 1,
    "Austria": 1,
    "Vietnam": 1,
    "Sweden": 1,
    "Brazil": 1,
    "Romania": 1,
    "Indonesia": 1,
    "Morocco": 1,
    "Singapore": 1,
    "Spain": 1,
    "Finland": 1,
    "Israel": 1,
    "Saudi Arabia": 1,
    "Belgium": 1,
    "Canada": 1
}

df_counts = pd.DataFrame(list(country_counts_dict.items()),
                         columns=["country", "count"])

# =========================================================
# 3. Baixar GeoJSON do mapa mundial (caso não exista)
# =========================================================
url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
local_path = "countries.geojson"

if not os.path.exists(local_path):
    print("Baixando GeoJSON...")
    urllib.request.urlretrieve(url, local_path)

world = gpd.read_file(local_path)

# =========================================================
# 4. Mesclar frequências com o GeoDataFrame usando a coluna 'name'
# =========================================================
world_freq = world.merge(df_counts, left_on="name",
                         right_on="country", how="left")
world_freq["count"] = world_freq["count"].fillna(0)

# =========================================================
# 5. Mapa estilo Robinson com estrelas nos países com pesquisas
# =========================================================
fig = plt.figure(figsize=(18, 10))
ax = plt.axes(projection=ccrs.Robinson())
ax.set_global()

# Mapa coroplético normal
world_freq.plot(
    column="count",
    cmap="OrRd",
    linewidth=0.3,
    edgecolor="black",
    legend=True,
    ax=ax,
    transform=ccrs.PlateCarree()
)

ax.add_feature(cfeature.COASTLINE, linewidth=0.4)
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.3)

# Adicionar estrelas nos países com count > 0
for idx, row in world_freq.iterrows():
    if row["count"] > 0:
        # Centróide do país (aproximado)
        centroid = row['geometry'].centroid
        x, y = centroid.x, centroid.y
        ax.plot(x, y, marker="*", color="purple", markersize=8,
                transform=ccrs.PlateCarree(), zorder=5)

plt.title("Frequência de Menções por País (Projeção Robinson) — Países com pesquisas marcados",
          fontsize=18)
plt.savefig("mapa_robson_frequencia_estrelas.png", dpi=300)
plt.show()

# =========================================================
# 6. Mostrar ranking
# =========================================================
df_counts.sort_values(by="count", ascending=False)
