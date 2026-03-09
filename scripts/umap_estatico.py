
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import umap
from sklearn.feature_extraction.text import TfidfVectorizer

# =========================================================
# CONFIGURAÇÃO
# =========================================================
CSV_PATH = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/dados base/revisão-egg+math - Limpo.csv"
OUTPUT_IMG = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/visualizações/umap_estatico_publicacao.png"
MIN_TEXT_LEN = 100

# Títulos dos Megatópicos
megatopico_names = {
    1: "Perfis Individuais",     # Megatopico 1
    2: "Métodos & Classificação", # Megatopico 2
    3: "Processos Cognitivos"    # Megatopico 3
}

# Organização da Legenda: Megatópico -> Lista de Tópicos
structure = {
    1: [ # Megatopico 1 (Círculo)
        (1, "T1 – Clínica"),
        (2, "T2 – Ansiedade"),
        (3, "T3 – Gênero"),
        (4, "T4 – Superdotação"),
        (9, "T9 – Educação"),
        (11, "T11 – Contexto")
    ],
    2: [ # Megatopico 2 (Quadrado)
        (5, "T5 – Classificação/ML"),
        (10, "T10 – Espectral")
    ],
    3: [ # Megatopico 3 (Triângulo)
        (6, "T6 – Conectividade"),
        (7, "T7 – Habilidade"),
        (8, "T8 – Carga Cognitiva")
    ]
}

# Marcadores para cada Megatópico
markers = {1: 'o', 2: 's', 3: '^'}

# Cores para cada Tópico (garantindo consistência global)
# Usando paleta tab10/tab20 modificada para distinção
topic_colors = {
    1: "#1f77b4",  # Azul
    2: "#ff7f0e",  # Laranja
    3: "#2ca02c",  # Verde
    4: "#d62728",  # Vermelho
    9: "#bcbd22",  # Amarelo/Oliva
    11: "#7f7f7f", # Cinza
    5: "#9467bd",  # Roxo
    10: "#17becf", # Ciano
    6: "#8c564b",  # Marrom
    7: "#e377c2",  # Rosa
    8: "#000000"   # Preto
}

# =========================================================
# 1. CARREGAR E PROCESSAR
# =========================================================
print("Carregando e processando dados...")
df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')

# Filtrar
df = df.dropna(subset=["Topico", "Megatopico", "Texto_Completo"])
df["Topico"] = pd.to_numeric(df["Topico"], errors='coerce').fillna(0).astype(int)
df["Megatopico"] = pd.to_numeric(df["Megatopico"], errors='coerce').fillna(0).astype(int)
df = df[df["Texto_Completo"].str.len() >= MIN_TEXT_LEN].reset_index(drop=True)

# Vetorização
print("Vetorizando (TF-IDF)...")
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.9,
    min_df=2,
    ngram_range=(1, 2)
)
X = vectorizer.fit_transform(df["Texto_Completo"].astype(str))

# UMAP
print("Calculando UMAP...")
umap_model = umap.UMAP(
    n_neighbors=7, 
    min_dist=0.3, 
    n_components=2, 
    random_state=42,
    metric='cosine'
)
embedding = umap_model.fit_transform(X)
df["x"] = embedding[:, 0]
df["y"] = embedding[:, 1]

# =========================================================
# 2. PLOTAGEM MATPLOTLIB (ESTILO ARTIGO CIENTÍFICO)
# =========================================================
print("Gerando gráfico estático...")

# Configurações de fonte para publicação (serifa, tamanho legível)
plt.rcParams['font.family'] = 'DejaVu Serif'
plt.rcParams['font.size'] = 12

fig, ax = plt.subplots(figsize=(12, 8)) # Tamanho bom para papel A4 paisagem ou meia página

# Plotar os pontos
for mt_id, topics_list in structure.items():
    marker = markers[mt_id]
    
    # Pegar todos os artigos deste megatópico
    df_mega = df[df["Megatopico"] == mt_id]
    
    if df_mega.empty:
        continue
        
    for t_id, t_name in topics_list:
        df_topic = df_mega[df_mega["Topico"] == t_id]
        if df_topic.empty:
            continue
            
        ax.scatter(
            df_topic["x"], 
            df_topic["y"], 
            color=topic_colors.get(t_id, "black"),
            marker=marker,
            s=80,    # Tamanho do ponto
            alpha=0.8, # Transparência leve para sobreposições
            edgecolor='white',
            linewidth=0.5,
            label=f"{t_name}" # Label para controle interno, legenda será manual
        )

# Remover eixos numéricos (muitas vezes irrelevantes em UMAP para o leitor final, focar na topologia)
# Mas para artigo científico às vezes preferem manter os eixos ou apenas 'Dimensão 1' / 'Dimensão 2'
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("UMAP Dimensão 1", fontweight='bold')
ax.set_ylabel("UMAP Dimensão 2", fontweight='bold')

# Remover bordas desnecessárias (spines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# =========================================================
# 3. LEGENDA PERSONALIZADA AGRUPADA
# =========================================================
legend_elements = []

for mt_id, topics_list in structure.items():
    # Título do Megatópico (Texto em Negrito ou Destaque)
    # Adicionamos um Line2D invisível apenas para o texto
    legend_elements.append(
        Line2D([0], [0], color='w', label=f"$\\bf{{Megatopic\\ {mt_id}:\ {megatopico_names[mt_id]}}}$", markersize=0)
    )
    
    # Itens do Megatópico
    for t_id, t_label in topics_list:
        legend_elements.append(
            Line2D([0], [0], 
                   marker=markers[mt_id], 
                   color='w', 
                   label=t_label,
                   markerfacecolor=topic_colors.get(t_id, 'black'), 
                   markersize=9,
                   markeredgecolor='white',
                   markeredgewidth=0.5)
        )
    
    # Espaço vazio entre grupos (opcional)
    legend_elements.append(Line2D([0], [0], color='w', label=" ", markersize=0))

# Criar a legenda fora do gráfico à direita
# bbox_to_anchor ajusta a posição. (1.05, 1) = topo direito fora do eixo.
leg = ax.legend(
    handles=legend_elements, 
    loc='upper left', 
    bbox_to_anchor=(1.01, 1.01),
    frameon=False, # Sem caixa em volta da legenda para ficar mais limpo
    fontsize=10,
    labelspacing=0.4 # Espaçamento vertical entre itens
)

# Ajustar layout para caber a legenda
plt.tight_layout()

# Salvar em alta resolução (300 DPI é padrão para artigos)
plt.savefig(OUTPUT_IMG, dpi=300, bbox_inches='tight')

print(f"✅ Gráfico estático salvo em: {OUTPUT_IMG}")
