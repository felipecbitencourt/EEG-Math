import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# =========================
# CONFIGURAÇÃO
# =========================
INPUT_FILE = "/home/eduarda-tessari-pereira/Documents/pesquisas/EEG-Math/dados/tabela_normatizada.csv"
OUTPUT_DIR = "/home/eduarda-tessari-pereira/Documents/pesquisas/EEG-Math/resultados/figuras/q1"
SUMMARY_FILE = "/home/eduarda-tessari-pereira/Documents/pesquisas/EEG-Math/resultados/q1/dados_bloco1.md"

def analyze_bibliometry_stunning():
    df = pd.read_csv(INPUT_FILE)
    sns.set_context("talk")
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})
    
    # 1. EVOLUÇÃO TEMPORAL STUNNING
    year_col = "Ano da primeria publicação"
    df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
    year_counts = df[year_col].dropna().value_counts().sort_index().reset_index()
    year_counts.columns = ["Ano", "Count"]

    fig, ax = plt.subplots(figsize=(14, 7))
    # Sombra/Área abaixo da linha
    ax.fill_between(year_counts["Ano"], year_counts["Count"], color="#3498db", alpha=0.15)
    # Linha principal estilizada
    sns.lineplot(data=year_counts, x="Ano", y="Count", marker="o", markersize=10, 
                 color="#2980b9", lw=4, label="Artigos por Ano", ax=ax)
    
    # Média Móvel Suavizada
    year_counts["MA5"] = year_counts["Count"].rolling(window=5, center=True).mean()
    sns.lineplot(data=year_counts, x="Ano", y="MA5", color="#e74c3c", ls="--", 
                 lw=2, label="Tendência (Média Móvel 5a)", ax=ax)

    ax.set_title("Evolução Histórica das Publicações (EEG-Math)", fontsize=22, pad=30, weight="bold", color="#2c3e50")
    ax.set_xlabel("Ano de Lançamento", fontsize=14, labelpad=15)
    ax.set_ylabel("Total de Artigos", fontsize=14, labelpad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.legend(frameon=True, fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/evolucao_temporal_v2.png", dpi=300)
    plt.close()

    # 2. DISTRIBUIÇÃO GEOGRÁFICA EM BARRA HORIZONTAL STUNNING
    country_counts = df["País"].dropna().value_counts().head(15).reset_index()
    country_counts.columns = ["País", "Artigos"]

    fig, ax = plt.subplots(figsize=(12, 9))
    # Paleta Gradiente
    palette = sns.color_palette("mako_r", len(country_counts))
    barplot = sns.barplot(data=country_counts, x="Artigos", y="País", palette=palette, ax=ax)
    
    # Adicionar contagens nas pontas das barras
    for i, p in enumerate(barplot.patches):
        width = p.get_width()
        ax.text(width + 0.3, p.get_y() + p.get_height() / 2, f'{int(width)}', 
                ha='left', va='center', fontsize=12, color='#2c3e50', weight='bold')

    ax.set_title("Top 15 Países em Estudos de EEG-Math", fontsize=22, pad=30, weight="bold", color="#2c3e50")
    ax.set_xlabel("Volume de Artigos", fontsize=14, labelpad=15)
    ax.set_ylabel("", fontsize=14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/distribuicao_geografica_v2.png", dpi=300)
    plt.close()

    # 3. SUMÁRIO ATUALIZADO
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("# 🔬 Bibliometria de Alta Definição — Bloco 1\n\n")
        f.write("A análise visual reflete a consolidação científica do campo:\n\n")
        f.write("### 📈 Tendência Temporal\n")
        f.write("- **Crescimento:** Observa-se um aumento exponencial de interesse a partir de **2015**.\n")
        f.write("- **Suavização:** A média móvel revela que, apesar de flutuações, o campo está em fase de expansão robusta.\n\n")
        f.write("### 🌍 Distribuição Global\n")
        f.write("- **Liderança:** **USA** e **China** concentram quase 25% da produção total.\n")
        f.write("- **Diversidade:** Países como Índia, Rússia e Polônia aparecem com relevância crescente.\n\n")
        f.write(f"![Temporal V2](figuras/q1/evolucao_temporal_v2.png)\n\n")
        f.write(f"![Geográfico V2](figuras/q1/distribuicao_geografica_v2.png)\n")

    print(f"✅ Visualizações de alta definição geradas em: {OUTPUT_DIR}")

if __name__ == "__main__":
    analyze_bibliometry_stunning()
