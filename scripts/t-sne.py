# ================================================
# 📌 t-SNE COM TEXTO LIMPO DO CSV – EEG & MATEMÁTICA
# ================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings("ignore")

# ---------------------------
# Config
# ---------------------------
CSV_PATH = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/dados base/revisão-egg+math - Limpo.csv"
OUTPUT_EMBED_CSV = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/dados base/embeddings_tsne_texto_limpo.csv"
MIN_TEXT_LEN = 100  # mínimo de caracteres para considerar texto válido

# ---------------------------
# Megatópicos / Tópicos
# ---------------------------
megatopicos_titles = {
    1: "Perfis Individuais e Diferenças Cognitivas",
    2: "Métodos Computacionais e Classificação",
    3: "Processos Cognitivos e Dinâmica Neural"
}

megatopicos_dict = {
    1: [
        "T1 – Matemática e Transtornos/Condições Clínicas",
        "T2 – Ansiedade e Estresse Matemático",
        "T3 – Gênero e Diferenças Sexuais",
        "T4 – Superdotação e Altas Habilidades",
        "T9 – Desenvolvimento, Educação e Contexto Escolar",
        "T11 – Condições Experimentais e Variáveis Contextuais"
    ],
    2: [
        "T5 – Modelos de Classificação e Aprendizado de Máquina",
        "T10 – Análise Espectral"
    ],
    3: [
        "T6 – Conectividade e Redes Cerebrais",
        "T7 – Desempenho Matemático e Diferenças de Habilidade",
        "T8 – Carga Cognitiva, Fadiga e Estado Mental"
    ]
}

# ---------------------------
# CORES e SÍMBOLOS
# ---------------------------
topic_colors = {
    1:  "#1f77b4", 2:  "#ff7f0e", 3:  "#2ca02c",
    4:  "#d62728", 5:  "#9467bd", 6:  "#8c564b",
    7:  "#e377c2", 8:  "#7f7f7f", 9:  "#bcbd22",
    10: "#17becf", 11: "#000000"
}
megatopic_markers = {1: "o", 2: "s", 3: "^"}

# ---------------------------
# Parâmetros visuais
# ---------------------------
plt.rcParams["font.family"] = "serif"
SCATTER_ALPHA = 0.85
SCATTER_SIZE = 95
EDGE_COLOR = "white"
EDGE_WIDTH = 0.9

# ---------------------------
# 1. Carregar CSV
# ---------------------------
df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')

# Verificar se coluna de texto limpo existe
if "Texto_Completo" not in df.columns:
    raise ValueError("Coluna 'Texto_Completo' não encontrada no CSV. Execute primeiro o pipeline de extração.")

# Limpar dados e filtrar textos válidos
df = df.dropna(subset=["Topico", "Megatopico", "Texto_Completo"])
df["Topico"] = pd.to_numeric(df["Topico"], errors='coerce').fillna(0).astype(int)
df["Megatopico"] = pd.to_numeric(df["Megatopico"], errors='coerce').fillna(0).astype(int)
df_validos = df[df["Texto_Completo"].str.len() >= MIN_TEXT_LEN].reset_index(drop=True)

print(f"✅ Textos válidos para análise: {len(df_validos)} artigos")

if df_validos.empty:
    raise SystemExit("Nenhum texto válido encontrado. Pare e verifique o CSV.")

# ---------------------------
# 2. TF-IDF
# ---------------------------
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.9,
    min_df=2,
    ngram_range=(1,2),
    max_features=7000
)
X = vectorizer.fit_transform(df_validos["Texto_Completo"].astype(str))

# ---------------------------
# 3. t-SNE
# ---------------------------
tsne = TSNE(n_components=2, random_state=42, perplexity=25, init='pca', learning_rate='auto', max_iter=2000)
X_embedded = tsne.fit_transform(X.toarray())
df_validos["tsne_x"] = X_embedded[:,0]
df_validos["tsne_y"] = X_embedded[:,1]

# ---------------------------
# 4. Salvar embeddings + meta
# ---------------------------
df_validos.to_csv(OUTPUT_EMBED_CSV, index=False, sep=';')
print(f"\n✅ Embeddings + textos salvos em: {OUTPUT_EMBED_CSV}")

# ---------------------------
# 5. Plot t-SNE
# ---------------------------
OUTPUT_IMG = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/visualizações/tsne_plot.png"

fig, ax = plt.subplots(figsize=(20,13))
fig.patch.set_facecolor("white")

for mt, topics in megatopicos_dict.items():
    subset = df_validos[df_validos["Megatopico"] == mt]
    for topic_full in topics:
        tnum = int(topic_full.split("–")[0].strip()[1:])
        subsub = subset[subset["Topico"] == tnum]
        if subsub.empty:
            continue
        ax.scatter(
            subsub["tsne_x"],
            subsub["tsne_y"],
            c=topic_colors.get(tnum, "#333333"),
            marker=megatopic_markers.get(mt, "o"),
            s=SCATTER_SIZE,
            alpha=SCATTER_ALPHA,
            edgecolors=EDGE_COLOR,
            linewidth=EDGE_WIDTH,
            label=f"{topic_full} ({megatopicos_titles[mt]})"
        )

# Legenda combinada
legend_elements = []
legend_elements.append(Line2D([], [], linestyle="none", label="CORES = TÓPICOS"))

for mt, topics in megatopicos_dict.items():
    for topic_full in topics:
        tnum = int(topic_full.split("–")[0].strip()[1:])
        legend_elements.append(
            Line2D([], [], marker="o", color=topic_colors.get(tnum),
                   markersize=9, linestyle="none",
                   markeredgecolor="white", markeredgewidth=0.8,
                   label=topic_full)
        )

legend_elements.append(Line2D([], [], linestyle="none", label=""))
legend_elements.append(Line2D([], [], linestyle="none", label="SÍMBOLOS = MEGATÓPICOS"))

for mt, title in megatopicos_titles.items():
    legend_elements.append(
        Line2D([], [], marker=megatopic_markers.get(mt), color="black",
               linestyle="none", markersize=9, label=title)
    )

ax.legend(handles=legend_elements,
          title="Codificação Visual – EEG & Matemática",
          fontsize=11, title_fontsize=14,
          bbox_to_anchor=(1.02,1), loc="upper left", frameon=True)

ax.set_xlabel("t-SNE 1", fontsize=14, fontweight='bold')
ax.set_ylabel("t-SNE 2", fontsize=14, fontweight='bold')
ax.grid(True, linestyle="--", alpha=0.28)
plt.tight_layout()
plt.savefig(OUTPUT_IMG, dpi=300, bbox_inches="tight")
# plt.show()
print(f"✅ Gráfico t-SNE salvo em: {OUTPUT_IMG}")
