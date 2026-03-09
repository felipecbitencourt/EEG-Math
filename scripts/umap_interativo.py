
import pandas as pd
import umap
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer

# =========================================================
# CONFIGURAÇÃO
# =========================================================
CSV_PATH = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/dados base/revisão-egg+math - Limpo.csv"
OUTPUT_HTML = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/visualizações/umap_interativo.html"
MIN_TEXT_LEN = 100

# Dicionários de Nomes
megatopicos_titles = {
    1: "Perfis Individuais e Diferenças",
    2: "Métodos Computacionais/Classificação",
    3: "Processos Cognitivos e Dinâmica Neural"
}

topicos_labels = {
    1: "T1 – Transtornos/Clínica",
    2: "T2 – Ansiedade/Estresse",
    3: "T3 – Gênero",
    4: "T4 – Superdotação/Altas Hab.",
    5: "T5 – Classificação/ML",
    6: "T6 – Conectividade/Redes",
    7: "T7 – Desempenho/Habilidade",
    8: "T8 – Carga Cognitiva/Fadiga",
    9: "T9 – Desenvolvimento/Educação",
    10: "T10 – Análise Espectral",
    11: "T11 – Contexto Experimental"
}

# =========================================================
# 1. CARREGAR DADOS
# =========================================================
print("Carregando dados...")
df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')

# Filtrar
df = df.dropna(subset=["Topico", "Megatopico", "Texto_Completo"])
df["Topico"] = pd.to_numeric(df["Topico"], errors='coerce').fillna(0).astype(int)
df["Megatopico"] = pd.to_numeric(df["Megatopico"], errors='coerce').fillna(0).astype(int)
df = df[df["Texto_Completo"].str.len() >= MIN_TEXT_LEN].reset_index(drop=True)

# Criar colunas legíveis para o Plotly
df["Megatopico_Nome"] = df["Megatopico"].map(megatopicos_titles)
df["Topico_Nome"] = df["Topico"].map(topicos_labels)

# Texto formatado para o hover (pula linha se for muito grande)
def format_title(text):
    return "<br>".join([text[i:i+60] for i in range(0, len(text), 60)])

df["Hover_Title"] = df["Titulo"].apply(lambda x: format_title(str(x)))

# =========================================================
# 2. VETORIZAÇÃO (TF-IDF)
# =========================================================
print("Vetorizando textos...")
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.9,
    min_df=2,
    ngram_range=(1, 2)
)
X = vectorizer.fit_transform(df["Texto_Completo"].astype(str))

# =========================================================
# 3. UMAP
# =========================================================
print("Executando UMAP...")
# n_neighbors: controla estrutura local vs global (maior = mais global)
# min_dist: controla o quão "apertados" os pontos ficam
umap_model = umap.UMAP(
    n_neighbors=7, 
    min_dist=0.3, 
    n_components=2, 
    random_state=42,
    metric='cosine' # Cosseno é geralmente melhor para texto/TF-IDF
)
umap_embedding = umap_model.fit_transform(X)

df["UMAP_1"] = umap_embedding[:, 0]
df["UMAP_2"] = umap_embedding[:, 1]

# =========================================================
# 4. PLOT INTERATIVO (PLOTLY)
# =========================================================
print("Gerando gráfico interativo...")

# Definir símbolos para Megatópicos (Plotly usa strings específicas)
# 1=Bolinha (circle), 2=Quadrado (square), 3=Triângulo (diamond ou triangle-up)
symbol_map = {
    "Perfis Individuais e Diferenças": "circle",
    "Métodos Computacionais/Classificação": "square",
    "Processos Cognitivos e Dinâmica Neural": "diamond"
}

fig = px.scatter(
    df,
    x="UMAP_1",
    y="UMAP_2",
    color="Topico_Nome",
    symbol="Megatopico_Nome",
    symbol_map=symbol_map,
    hover_data={
        "UMAP_1": False,
        "UMAP_2": False,
        "Topico_Nome": True,
        "Megatopico_Nome": True,
        "Ano_Publicacao": True,
        "Titulo": True
    },
    title="<b>Mapeamento Semântico UMAP – EEG & Matemática</b><br><sup>Passe o mouse para ver detalhes. Cores = Tópicos, Símbolos = Megatópicos.</sup>",
    template="plotly_white",
    width=1200,
    height=800
)

# Ajustes visuais finos
fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))

fig.update_layout(
    legend_title_text="Legenda",
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    margin=dict(l=40, r=40, t=80, b=40)
)

# Salvar
fig.write_html(OUTPUT_HTML)
print(f"✅ Gráfico interativo salvo em: {OUTPUT_HTML}")
