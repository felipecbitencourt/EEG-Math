import pandas as pd
import numpy as np

file_path = r"C:\Users\FELIPE BITENCOURT\.gemini\antigravity\scratch\EEG-Math\dados base\embeddings_tsne_texto_completo.csv"

try:
    print(f"Reading: {file_path}")
    df = pd.read_csv(file_path, encoding='utf-8')
    
    print(f"Total Rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")

    potential_empty_markers = ['[]', 'nan', 'null', 'none', '', ' ', '-', '.']
    
    print("\n--- Detailed Inspection ---")
    found_issues = False
    
    for col in df.columns:
        # standard null metrics
        n_null = df[col].isnull().sum()
        if n_null > 0:
            print(f"Column '{col}' has {n_null} NaNs.")
            found_issues = True
        
        # string checks
        if df[col].dtype == object:
            # Check for short strings or specific markers
            for marker in potential_empty_markers:
                # Case insensitive check for string markers
                mask = df[col].astype(str).str.lower() == marker
                if mask.any():
                    count = mask.sum()
                    print(f"Column '{col}' has {count} entries matching '{marker}'")
                    print(f"   Indices: {df[mask].index.tolist()[:10]}")
                    found_issues = True

    if not found_issues:
        print("No missing or suspicious 'empty' values found.")
        print("First 3 rows for visual check:")
        print(df.head(3).to_string())

except Exception as e:
    print(f"Error: {e}")
