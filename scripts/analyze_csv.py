import pandas as pd
import sys

file_path = r"C:\Users\FELIPE BITENCOURT\.gemini\antigravity\scratch\EEG-Math\dados base\revisão-egg+math - Versão reduzida.csv"
log_path = r"C:\Users\FELIPE BITENCOURT\.gemini\antigravity\scratch\EEG-Math\result.txt"

with open(log_path, 'w', encoding='utf-8') as log:
    def log_print(msg):
        print(msg)
        log.write(str(msg) + "\n")

    log_print(f"Analyzing file: {file_path}")

    # Read first few lines as text
    try:
        log_print("\n--- First 5 lines (Raw) ---")
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for i in range(5):
                log_print(repr(f.readline()))
    except Exception as e:
        log_print(f"Error reading text: {e}")

    def try_read(encoding, sep):
        try:
            log_print(f"\n--- Trying encoding: {encoding}, sep: '{sep}' ---")
            df = pd.read_csv(file_path, encoding=encoding, sep=sep, on_bad_lines='skip', engine='python')
            log_print("Success!")
            log_print(f"Shape: {df.shape}")
            log_print("Columns:")
            log_print(df.columns.tolist())
            log_print("\nFirst 3 rows:")
            log_print(df.head(3).to_string())
            log_print("\nMissing Values:")
            log_print(df.isnull().sum().to_string())
            return df
        except Exception as e:
            log_print(f"Failed: {e}")
            return None

    # Try utf-8 with comma
    df = try_read('utf-8', ',')
    if df is None or df.shape[1] < 2:
        df = try_read('latin1', ',')
