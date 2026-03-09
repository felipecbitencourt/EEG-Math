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
# 2. Carregar e Processar Dados do CSV
# =========================================================
CSV_PATH = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/dados base/revisão-egg+math - Limpo.csv"

# Carregar CSV
try:
    df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')
except Exception as e:
    raise SystemExit(f"Erro ao ler CSV: {e}")

# Verificar coluna Pais
if "Pais" not in df.columns:
    raise ValueError("Coluna 'Pais' não encontrada no CSV.")

# Extrair e contar países (tratando múltiplos países separados por /)
all_countries = []
for entry in df["Pais"].dropna():
    # Remover parenteses extras como (filiação dos autores)
    entry = entry.split('(')[0]
    # Dividir por barra se houver múltiplos
    parts = entry.split('/')
    for p in parts:
        p = p.strip()
        if p:
            all_countries.append(p)

# Dicionário de tradução/normalização para inglês (Compatível com GeoJSON)
normalization_map = {
    "Brasil": "Brazil",
    "EUA": "United States of America",
    "USA": "United States of America",
    "UK": "United Kingdom",
    "Reino Unido": "United Kingdom",
    "China": "China",
    "Coréia do Sul": "South Korea",
    "Coreia do Sul": "South Korea",
    "South Korea": "South Korea",
    "Suíça": "Switzerland",
    "Switzerland": "Switzerland",
    "Alemanha": "Germany",
    "Germany": "Germany",
    "Grécia": "Greece",
    "Greece": "Greece",
    "Índia": "India",
    "India": "India",
    "Rússia": "Russia",
    "Russia": "Russia",
    "Federação Russa": "Russia",
    "Bangladesh": "Bangladesh",
    "Holanda": "Netherlands",
    "Netherlands": "Netherlands",
    "Itália": "Italy",
    "Italy": "Italy",
    "Malásia": "Malaysia",
    "Malaysia": "Malaysia",
    "México": "Mexico",
    "Mexico": "Mexico",
    "Irã": "Iran",
    "Iran": "Iran",
    "Taiwan": "Taiwan",
    "República Tcheca": "Czech Republic",
    "Czech Republic": "Czech Republic",
    "Turquia": "Turkey",
    "Turkey": "Turkey",
    "Japão": "Japan",
    "Japan": "Japan",
    "Nova Zelândia": "New Zealand",
    "New Zealand": "New Zealand",
    "Chile": "Chile",
    "Áustria": "Austria",
    "Austria": "Austria",
    "Vietnã": "Vietnam",
    "Vietnam": "Vietnam",
    "Suécia": "Sweden",
    "Sweden": "Sweden",
    "Romênia": "Romania",
    "Romania": "Romania",
    "Indonésia": "Indonesia",
    "Indonesia": "Indonesia",
    "Marrocos": "Morocco",
    "Morocco": "Morocco",
    "Cingapura": "Singapore",
    "Singapore": "Singapore",
    "Espanha": "Spain",
    "Spain": "Spain",
    "Finlândia": "Finland",
    "Finland": "Finland",
    "Israel": "Israel",
    "Arábia Saudita": "Saudi Arabia",
    "Saudi Arabia": "Saudi Arabia",
    "Bélgica": "Belgium",
    "Belgium": "Belgium",
    "Canadá": "Canada",
    "Canada": "Canada",
    "England": "United Kingdom",
    "Turquia(Kütahya)": "Turkey",
    "Índia (IN)": "India",
    "Korea": "South Korea",
    "FInland": "Finland",
    "Poland": "Poland",
    "Ukraine": "Ukraine",
    "Pakistan": "Pakistan"
}

normalized_countries = []
for c in all_countries:
    # Remove whitespace
    c_clean = c.strip()
    # Translate if in map, otherwise keep original (useful to see unmapped)
    c_final = normalization_map.get(c_clean, c_clean)
    normalized_countries.append(c_final)

# Criar DataFrame de contagem
df_counts = pd.DataFrame(normalized_countries, columns=["country"])
df_counts = df_counts["country"].value_counts().reset_index()
df_counts.columns = ["country", "count"]

print("Top 10 Países:")
print(df_counts.head(10))

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
# Note: GeoJSON names are usually standardized English
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
OUTPUT_IMG = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/visualizações/mapa_robson_frequencia_estrelas.png"
plt.savefig(OUTPUT_IMG, dpi=300)
# plt.show() # Commented out for headless environment

print(f"Mapa salvo com sucesso em: {OUTPUT_IMG}")

# =========================================================
# 6. Mostrar ranking
# =========================================================
print(df_counts.sort_values(by="count", ascending=False))
