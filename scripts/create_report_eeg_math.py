import pandas as pd
import os

# =========================
# CONFIGURAÇÃO
# =========================
INPUT_FILE = "/home/eduarda-tessari-pereira/Documents/pesquisas/EEG-Math/dados/tabela_normatizada.csv"
REPORT_FILE = "/home/eduarda-tessari-pereira/Documents/pesquisas/EEG-Math/relatorio_revisao.md"

def generate_report():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Erro: Arquivo {INPUT_FILE} não encontrado.")
        return

    df = pd.read_csv(INPUT_FILE)
    total_artigos = len(df)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# 📊 Relatório Detalhado de Revisão Sistemática: EEG & Processos Matemáticos\n\n")
        f.write(f"**Total de artigos analisados:** {total_artigos}\n\n")

        # =========================
        # 1. PERFIL DA AMOSTRA
        # =========================
        f.write("## 👥 1. Perfil da Amostra e População\n")
        total_part = df["amostra_n_total"].sum()
        media_part = df["amostra_n_total"].mean()
        media_idade = df["amostra_age_mean"].mean()
        
        f.write(f"- **Total de participantes acumulados:** {int(total_part) if not pd.isna(total_part) else 'N/A'}\n")
        f.write(f"- **Tamanho amostral médio:** {media_part:.2f}\n")
        f.write(f"- **Idade média geral:** {media_idade:.2f} anos\n")
        
        if "amostra_population_type" in df.columns:
            pop_counts = df["amostra_population_type"].value_counts()
            f.write("### Distribuição de População:\n")
            for p, c in pop_counts.items():
                f.write(f"- **{p.capitalize()}:** {c} estudos\n")
        
        if "amostra_n_male" in df.columns and "amostra_n_female" in df.columns:
            m_sum = df["amostra_n_male"].sum()
            f.write(f"- **Distribuição de Gênero:** {int(m_sum) if not pd.isna(m_sum) else 0} homens | {int(df['amostra_n_female'].sum()) if not pd.isna(df['amostra_n_female'].sum()) else 0} mulheres\n")
        f.write("\n")

        # =========================
        # 2. CONTEXTO MATEMÁTICO E TAREFAS
        # =========================
        f.write("## 🧮 2. Tarefas e Contexto Matemático\n")
        if "comparison_type" in df.columns:
            comp_counts = df["comparison_type"].value_counts()
            f.write("### Tipos de Baseline/Controle:\n")
            for ct, c in comp_counts.items():
                f.write(f"- **{ct.replace('_', ' ').capitalize()}:** {c} estudos\n")
        f.write("\n")

        # =========================
        # 3. TECNOLOGIA E HARDWARE
        # =========================
        f.write("## 🎧 3. Tecnologia de EEG\n")
        if "eeg_device" in df.columns:
            f.write("### Equipamentos (Top 5):\n")
            dev_counts = df["eeg_device"].dropna().str.split(", ").explode().value_counts().head(5)
            for d, c in dev_counts.items():
                f.write(f"- **{d}:** {c} estudos\n")
        
        if "tech_n_channels" in df.columns:
            f.write("### Densidade de Eletrodos:\n")
            ch_counts = df["tech_n_channels"].value_counts().head(3)
            for ch, c in ch_counts.items():
                f.write(f"- **{int(ch)} canais:** {c} estudos\n")
        
        if "eeg_system" in df.columns:
            sys_counts = df["eeg_system"].value_counts()
            f.write(f"- **Sistema de Posicionamento:** {', '.join([f'{s} ({c})' for s, c in sys_counts.items()])}\n")
        f.write("\n")

        # =========================
        # 4. PRÉ-PROCESSAMENTO E CARACTERÍSTICAS
        # =========================
        f.write("## ⚙️ 4. Pré-processamento e Extração de Características\n")
        for col in ["artifact_removal", "spectral_features", "connectivity_features", "erp_features"]:
            if col in df.columns:
                counts = df[col].dropna().str.split(", ").explode().value_counts().head(3)
                if not counts.empty:
                    f.write(f"- **{col.replace('_', ' ').capitalize()} (Top):** {', '.join(counts.index.tolist())}\n")
        f.write("\n")

        # =========================
        # 5. ANÁLISE E MACHINE LEARNING
        # =========================
        f.write("## 🚀 5. Métodos de Análise e IA\n")
        if "ml_used" in df.columns:
            perc_ml = (df["ml_used"] == "yes").mean() * 100
            f.write(f"- **Prevalência de Machine Learning:** {perc_ml:.1f}% dos estudos\n")
            if perc_ml > 0:
                f.write("- **Modelos mais comuns:** " + ", ".join(df["ml_models"].dropna().str.split("; ").explode().value_counts().head(3).index.tolist()) + "\n")
                f.write("- **Métricas favoritas:** " + ", ".join(df["ml_metrics"].dropna().str.split("; ").explode().value_counts().head(3).index.tolist()) + "\n")
        
        if "soft_language" in df.columns:
            f.write("- **Linguagens de Programação:** " + ", ".join(df["soft_language"].dropna().str.split("; ").explode().value_counts().head(3).index.tolist()) + "\n")
        f.write("\n")

    print(f"✅ Relatório atualizado em: {REPORT_FILE}")

if __name__ == "__main__":
    generate_report()
