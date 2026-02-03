import pandas as pd
import re

input_file = r"C:\Users\FELIPE BITENCOURT\.gemini\antigravity\scratch\EEG-Math\dados base\revisão-egg+math - Versão reduzida.csv"
output_file = r"C:\Users\FELIPE BITENCOURT\.gemini\antigravity\scratch\EEG-Math\dados base\revisão-egg+math - Limpo.csv"

# Column Mapping
column_mapping = {
    'Título': 'Titulo',
    'Titulo': 'Titulo', # handle potential existing clean name or variation
    '  Título\n\n': 'Titulo',
    'Autores': 'Autores',
    'Ano da primeria publicação': 'Ano_Publicacao',
    'Revista': 'Revista',
    'País': 'Pais',
    'DOI': 'DOI',
    'Revisor': 'Revisor',
    'Notas adicionais': 'Notas',
    '⭐Recomendo a leitura?': 'Recomendacao'
}

# Regex based mapping for the numbered questions to handle potential minor text variations
def get_clean_col_name(col_name):
    col_name = col_name.strip()
    
    if col_name in column_mapping:
        return column_mapping[col_name]
    
    # Check for specific keywords or numbering
    if col_name.startswith('1.') and 'tipo de investigação' in col_name.lower(): return 'Tipo_Investigacao'
    if col_name.startswith('2.') and 'dimensão temporal' in col_name.lower(): return 'Dimensao_Temporal'
    if col_name.startswith('3.') and 'como os sujeitos' in col_name.lower(): return 'Comparacao_Sujeitos'
    if col_name.startswith('4.') and 'amostra' in col_name.lower(): return 'Amostra_Info'
    if col_name.startswith('5.') and 'marcadores' in col_name.lower(): return 'Marcadores_Amostra'
    if col_name.startswith('6.') and 'processos matemáticos' in col_name.lower(): return 'Processos_Matematicos'
    if col_name.startswith('7.') and 'tarefa matemática é comparada' in col_name.lower(): return 'Comparacao_Tarefa'
    if col_name.startswith('9.') and 'variáveis fisiológicas' in col_name.lower(): return 'Variaveis_Fisiologicas'
    if col_name.startswith('10.') and 'variáveis clínicas' in col_name.lower(): return 'Variaveis_Psicologicas'
    if col_name.startswith('11.') and 'variáveis comportamentais' in col_name.lower(): return 'Variaveis_Comportamentais'
    if col_name.startswith('12.') and 'posições de eletrodos' in col_name.lower(): return 'Posicao_Eletrodos'
    if col_name.startswith('13.') and 'equipamento de eeg' in col_name.lower(): return 'Equipamento'
    if col_name.startswith('14.') and 'tecnologia' in col_name.lower(): return 'Tecnologia_Eletrodos'
    if col_name.startswith('15.') and 'pré-processamento' in col_name.lower(): return 'Pre_Processamento'
    if col_name.startswith('16.') and 'faixas de frequência' in col_name.lower(): return 'Faixas_Frequencia'
    if col_name.startswith('17.') and 'linguagem' in col_name.lower(): return 'Software_Analise'
    if col_name.startswith('18.') and 'abordagem estatística' in col_name.lower(): return 'Abordagem_Estatistica'
    if col_name.startswith('19.') and 'algoritmos de classificação' in col_name.lower(): return 'Classificacao_ML'
    if col_name.startswith('20.') and 'conjunto de dados' in col_name.lower(): return 'Acesso_Dados'

    return col_name # Return original if no match

try:
    print("Reading file...")
    # Read with utf-8
    df = pd.read_csv(input_file, encoding='utf-8')

    # Rename columns
    new_columns = [get_clean_col_name(c) for c in df.columns]
    df.columns = new_columns
    print("Columns renamed.")

    # Clean string values
    print("Cleaning values...")
    def clean_text(text):
        if pd.isna(text):
            return text
        if isinstance(text, str):
            # Replace newlines with space
            text = text.replace('\n', ' ').replace('\r', '')
            # Collapse multiple spaces
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        return text

    # Apply cleaning to all columns that are object type (strings)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(clean_text)

    # Save
    print(f"Saving to {output_file}...")
    df.to_csv(output_file, index=False, encoding='utf-8-sig', sep=';') # using semi-colon for Excel friendly CSV in regions that use comma for decimals
    print("Done!")
    print(f"Final shape: {df.shape}")
    print("New Columns:")
    print(df.columns.tolist())

except Exception as e:
    print(f"An error occurred: {e}")
