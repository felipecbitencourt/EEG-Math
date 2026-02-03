import pandas as pd
import sys

input_file = r"C:\Users\FELIPE BITENCOURT\.gemini\antigravity\scratch\EEG-Math\dados base\revisão-egg+math - Limpo.csv"
output_file = r"C:\Users\FELIPE BITENCOURT\.gemini\antigravity\scratch\EEG-Math\relatorio_analise.md"

try:
    print("Reading data...")
    df = pd.read_csv(input_file, sep=';', encoding='utf-8')

    with open(output_file, 'w', encoding='utf-8') as f:
        def write_md(text):
            f.write(text + "\n")
        
        # Header
        write_md("# Relatório de Análise de Dados: EEG e Matemática")
        write_md("\n## Visão Geral")
        write_md(f"- **Total de Estudos**: {len(df)}")
        if 'Ano_Publicacao' in df.columns:
            years = pd.to_numeric(df['Ano_Publicacao'], errors='coerce')
            min_year = int(years.min()) if not years.isnull().all() else "N/A"
            max_year = int(years.max()) if not years.isnull().all() else "N/A"
            write_md(f"- **Período**: {min_year} - {max_year}")
        
        # Helper for frequency tables
        def write_freq_table(col_name, title, top_n=10):
            if col_name in df.columns:
                write_md(f"\n### {title}")
                counts = df[col_name].value_counts().head(top_n)
                write_md("| Categoria | Contagem |")
                write_md("| :--- | :--- |")
                for item, count in counts.items():
                    write_md(f"| {item} | {count} |")
            else:
                write_md(f"\n> Coluna `{col_name}` não encontrada.")

        # Publications by Year
        if 'Ano_Publicacao' in df.columns:
             write_md("\n### Publicações por Ano")
             counts = df['Ano_Publicacao'].value_counts().sort_index()
             write_md("| Ano | Quantidade |")
             write_md("| :--- | :--- |")
             for year, count in counts.items():
                 write_md(f"| {year} | {count} |")

        write_freq_table('Pais', 'Top Países de Publicação')
        write_freq_table('Revista', 'Top Revistas')
        write_freq_table('Tipo_Investigacao', 'Tipos de Investigação')
        write_freq_table('Processos_Matematicos', 'Processos Matemáticos Investigados')
        write_freq_table('Software_Analise', 'Software de Análise Utilizado')
        write_freq_table('Equipamento', 'Equipamentos de EEG')
        
        # Missing Data
        write_md("\n## Dados Faltantes")
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if not missing.empty:
            write_md("| Coluna | Valores Ausentes |")
            write_md("| :--- | :--- |")
            for col, val in missing.items():
                write_md(f"| {col} | {val} |")
        else:
            write_md("Não há dados faltantes significativos.")
            
    print(f"Report generated at: {output_file}")

except Exception as e:
    print(f"Error: {e}")
