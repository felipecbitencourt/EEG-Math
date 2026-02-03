import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths
base_dir = r"C:\Users\FELIPE BITENCOURT\.gemini\antigravity\scratch\EEG-Math"
input_file = os.path.join(base_dir, "dados base", "revisão-egg+math - Limpo.csv")
output_dir = os.path.join(base_dir, "textos")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_plot = os.path.join(output_dir, "visualizacao_temporal.png")
output_report_data = os.path.join(output_dir, "dados_temporal.txt")

try:
    print("Loading data...")
    df = pd.read_csv(input_file, sep=';', encoding='utf-8')
    
    # Pre-process Year
    df['Ano_Publicacao'] = pd.to_numeric(df['Ano_Publicacao'], errors='coerce')
    df = df.dropna(subset=['Ano_Publicacao'])
    df['Ano_Publicacao'] = df['Ano_Publicacao'].astype(int)
    
    # Identify Machine Learning / Classification
    # Keywords: SVM, LDA, Classification, Classificação, Machine Learning, RNA, Neural Network, Random Forest
    ml_keywords = ['svm', 'lda', 'classification', 'classificação', 'machine learning', 'neural network', 'random forest', 'cnn', 'knn', 'bayes']
    
    def is_ml_related(text):
        if pd.isna(text): return False
        text = str(text).lower()
        return any(k in text for k in ml_keywords)

    # Check both 'Classificacao_ML' and 'Abordagem_Estatistica' just in case, but rely mostly on the specific column if it exists
    if 'Classificacao_ML' in df.columns:
        df['is_ml'] = df['Classificacao_ML'].apply(is_ml_related)
    else:
        df['is_ml'] = False

    # Aggregating by Year
    annual_data = df.groupby('Ano_Publicacao').agg(
        Total_Publicacoes=('Titulo', 'count'),
        ML_Publicacoes=('is_ml', 'sum')
    ).reset_index()

    # Sort
    annual_data = annual_data.sort_values('Ano_Publicacao')

    # Fill missing years for continuous timeline if needed, but sparse is also okay. 
    # Let's create a full range for better plotting
    min_year = annual_data['Ano_Publicacao'].min()
    max_year = annual_data['Ano_Publicacao'].max()
    full_range = pd.DataFrame({'Ano_Publicacao': range(min_year, max_year + 1)})
    annual_data = pd.merge(full_range, annual_data, on='Ano_Publicacao', how='left').fillna(0)
    
    # Simple Moving Average for "Rhythm" smoothing
    annual_data['Moving_Avg_3y'] = annual_data['Total_Publicacoes'].rolling(window=3).mean()

    print("Generating Plot...")
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.style.use('ggplot') # Use a nice style if available
    
    # Total Publications Bar
    sns.barplot(data=annual_data, x='Ano_Publicacao', y='Total_Publicacoes', color='skyblue', alpha=0.7, label='Total Publicações')
    
    # ML Line
    sns.lineplot(data=annual_data, x=annual_data.index, y='ML_Publicacoes', color='red', marker='o', label='Tópicos ML/Classificação')
    
    # Formatting
    plt.title('Evolução Temporal das Publicações e Tópicos de Machine Learning')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de Publicações')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output_plot, dpi=300)
    print(f"Plot saved to {output_plot}")

    # Analysis Text Output
    with open(output_report_data, 'w', encoding='utf-8') as f:
        f.write(f"Intervalo: {min_year} - {max_year}\n")
        f.write("--- Dados Anuais ---\n")
        f.write(annual_data.to_string(index=False))
        
        # Identify Expansion Periods (e.g., > 2 papers and growth positive)
        f.write("\n\n--- Análise de Períodos ---\n")
        expansion = annual_data[annual_data['Total_Publicacoes'] > 2]
        f.write("Anos com mais de 2 publicações:\n")
        f.write(expansion['Ano_Publicacao'].to_string(index=False))
        
        # ML Correlation
        total_ml = annual_data['ML_Publicacoes'].sum()
        total_papers = annual_data['Total_Publicacoes'].sum()
        f.write(f"\n\nTotal Papers: {total_papers}")
        f.write(f"\nTotal ML Papers: {total_ml}")
        f.write(f"\nRatio ML: {total_ml/total_papers:.2%}")

    print("Analysis complete.")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
