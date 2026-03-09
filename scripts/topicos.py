# ============================================================
# 📊 VISUALIZAÇÃO NORMAL – EEG & MATEMÁTICA (MEGATÓPICOS & TÓPICOS)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# ------------------------------------------------------------
# 1. TÍTULOS DOS MEGATÓPICOS
# ------------------------------------------------------------
megatopicos_titles = {
    1: "Perfis Individuais e Diferenças Cognitivas",
    2: "Métodos Computacionais e Classificação",
    3: "Processos Cognitivos e Dinâmica Neural"
}

# ------------------------------------------------------------
# 2. TÓPICOS POR MEGATÓPICO
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# 3. CARREGAMENTO DO CSV
# ------------------------------------------------------------
CSV_PATH = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/dados base/revisão-egg+math - Limpo.csv"
OUTPUT_IMG = "/home/eduarda-tessari-pereira/Documents/pesquisas/claudio/EEG-Math/visualizações/grafico_barras_EEG_MATH.png"

df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')

df = df.dropna(subset=["Topico", "Megatopico"])
df["Topico"] = pd.to_numeric(df["Topico"], errors='coerce').fillna(0).astype(int)
df["Megatopico"] = pd.to_numeric(df["Megatopico"], errors='coerce').fillna(0).astype(int)

# ------------------------------------------------------------
# 4. CONTAGEM POR MEGATÓPICO E TÓPICO
# ------------------------------------------------------------
contagem = (
    df.groupby(["Megatopico", "Topico"])
      .size()
      .reset_index(name="n")
      .sort_values(["Megatopico", "Topico"])
)

contagem["Label"] = contagem["Topico"].apply(lambda x: f"T{int(x)}")

# ------------------------------------------------------------
# 5. CORES POR MEGATÓPICO
# ------------------------------------------------------------
plt.rcParams['font.family'] = 'serif'

meg_colors = ["#1F3A70", "#E85C91", "#3C9D9B"]
cor_por_megatopico = {
    mt: meg_colors[(mt-1) % len(meg_colors)]
    for mt in sorted(contagem["Megatopico"].unique())
}

contagem["Cor"] = contagem["Megatopico"].map(cor_por_megatopico)

# ------------------------------------------------------------
# 6. PLOT NORMAL (BARRAS)
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor("white")

x = np.arange(len(contagem))

ax.bar(
    x,
    contagem["n"],
    color=contagem["Cor"],
    edgecolor="white",
    linewidth=1.2
)

ax.set_xticks(x)
ax.set_xticklabels(contagem["Label"], fontsize=12)
ax.set_ylabel("Número de Artigos", fontsize=14, fontweight="bold")
ax.set_xlabel("Tópicos", fontsize=14, fontweight="bold")
ax.set_title("Distribuição de Artigos por Tópicos – EEG & Matemática",
             fontsize=16, fontweight="bold")

ax.grid(axis="y", linestyle="--", alpha=0.25)

# ------------------------------------------------------------
# 7. LEGENDA HIERÁRQUICA
# ------------------------------------------------------------
legend_elements = []

for mt, topics in megatopicos_dict.items():
    legend_elements.append(
        Line2D([], [], color="white", linestyle="none",
               label=f"{megatopicos_titles[mt]}")
    )

    for topic in topics:
        legend_elements.append(
            Line2D([], [], marker="o",
                   color=cor_por_megatopico[mt],
                   markersize=9, linestyle="none",
                   label=f"   {topic}")
        )

ax.legend(
    handles=legend_elements,
    fontsize=12,
    title="Megatópicos & Tópicos",
    title_fontsize=14,
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    frameon=True
)

plt.tight_layout()
plt.savefig(OUTPUT_IMG, dpi=300, bbox_inches="tight")
# plt.show()

print(f"✅ Gráfico salvo em: {OUTPUT_IMG}")

# ============================================================
# ✅ CONTAGENS NUMÉRICAS
# ============================================================

topicos_dict = {
    1: "Matemática e Transtornos/Condições Clínicas",
    2: "Ansiedade e Estresse Matemático",
    3: "Gênero e Diferenças Sexuais",
    4: "Superdotação e Altas Habilidades",
    5: "Modelos de Classificação e Aprendizado de Máquina",
    6: "Conectividade e Redes Cerebrais",
    7: "Desempenho Matemático e Diferenças de Habilidade",
    8: "Carga Cognitiva, Fadiga e Estado Mental",
    9: "Desenvolvimento, Educação e Contexto Escolar",
    10: "Análise Espectral",
    11: "Condições Experimentais e Variáveis Contextuais"
}

# -----------------------------
# CONTAGEM POR TÓPICO
# -----------------------------
contagem_topicos = df['Topico'].value_counts().reset_index()
contagem_topicos.columns = ['Topico', 'Count']
contagem_topicos['Titulo'] = contagem_topicos['Topico'].map(topicos_dict)
contagem_topicos['Perc'] = (contagem_topicos['Count'] /
                            contagem_topicos['Count'].sum() * 100).round(2)

print("\n📌 CONTAGEM POR TÓPICO:")
print(contagem_topicos)

# -----------------------------
# CONTAGEM POR MEGATÓPICO
# -----------------------------
df['Megatopico_Titulo'] = df['Megatopico'].map(megatopicos_titles)

contagem_megatopicos = df['Megatopico_Titulo'].value_counts().reset_index()
contagem_megatopicos.columns = ['Megatopico', 'Count']
contagem_megatopicos['Perc'] = (
    contagem_megatopicos['Count'] /
    contagem_megatopicos['Count'].sum() * 100
).round(2)

print("\n📊 CONTAGEM POR MEGATÓPICO:")
print(contagem_megatopicos)

# -----------------------------
# TABELA HIERÁRQUICA FINAL
# -----------------------------
total_por_mega = df.groupby("Megatopico").size()

contagem_detalhada = (
    df.groupby(["Megatopico", "Topico"])
      .size()
      .reset_index(name="Count")
)

contagem_detalhada["Megatopico_Titulo"] = contagem_detalhada["Megatopico"].map(megatopicos_titles)
contagem_detalhada["Topico_Titulo"] = contagem_detalhada["Topico"].map(topicos_dict)
contagem_detalhada["Label"] = contagem_detalhada["Topico"].apply(lambda x: f"T{int(x)}")

contagem_detalhada["Perc_no_Megatopico"] = contagem_detalhada.apply(
    lambda row: (row["Count"] / total_por_mega[row["Megatopico"]] * 100).round(2),
    axis=1
)

print("\n====================================================")
print("📌 TABELA FINAL – MEGATÓPICOS > TÓPICOS")
print("====================================================\n")

print(contagem_detalhada.sort_values(["Megatopico", "Count"], ascending=[True, False]))
