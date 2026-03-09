
import pandas as pd
import numpy as np
import umap
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score, pairwise_distances

# =========================================================
# CONFIGURAÇÃO
# =========================================================
CSV_PATH = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/dados base/revisão-egg+math - Limpo.csv"
MIN_TEXT_LEN = 100

# =========================================================
# 1. CARREGAR E PROCESSAR
# =========================================================
df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')
df = df.dropna(subset=["Topico", "Megatopico", "Texto_Completo"])
df["Topico"] = pd.to_numeric(df["Topico"], errors='coerce').fillna(0).astype(int)
df = df[df["Texto_Completo"].str.len() >= MIN_TEXT_LEN].reset_index(drop=True)

# Vetorização (mesma do UMAP)
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.9, min_df=2, ngram_range=(1, 2))
X_tfidf = vectorizer.fit_transform(df["Texto_Completo"].astype(str))

# UMAP embedding (mesmos parâmetros)
umap_model = umap.UMAP(n_neighbors=7, min_dist=0.3, n_components=2, random_state=42, metric='cosine')
embedding = umap_model.fit_transform(X_tfidf)

# =========================================================
# 2. MÉTRICAS
# =========================================================

# 1. Silhouette Score Global (Mede a separação geral dos Tópicos)
sil_score = silhouette_score(embedding, df["Topico"])
print(f"Silhouette Score (Tópicos): {sil_score:.4f} (Escala: -1 a 1, onde 1 é separação perfeita)")

# 2. Distância entre Centroides dos Tópicos
df["umap_x"] = embedding[:, 0]
df["umap_y"] = embedding[:, 1]

centroids = df.groupby("Topico")[["umap_x", "umap_y"]].mean()
dist_matrix = pd.DataFrame(
    pairwise_distances(centroids), 
    index=centroids.index, 
    columns=centroids.index
)

print("\n--- Pares de Tópicos Mais Próximos (Possível Sobreposição) ---")
# Encontrar os pares com menor distância (excluindo diagonal 0)
pairs = []
for i in dist_matrix.index:
    for j in dist_matrix.columns:
        if i < j: # Evitar duplicatas e diagonal
            pairs.append(((i, j), dist_matrix.loc[i, j]))

# Ordenar por proximidade
pairs.sort(key=lambda x: x[1])

for (t1, t2), dist in pairs[:5]:
    print(f"Tópico {t1} <-> Tópico {t2}: Distância {dist:.2f}")

# 3. Dispersão Intracluster (Qual tópico é mais 'espalhado'?)
print("\n--- Dispersão (Desvio Padrão) por Tópico ---")
std_devs = df.groupby("Topico")[["umap_x", "umap_y"]].std().mean(axis=1).sort_values(ascending=False)
print(std_devs)
