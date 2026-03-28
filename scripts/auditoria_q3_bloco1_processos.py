#!/usr/bin/env python3
"""Relatório: math_processes (texto col. 6) e math_processes_tags (Q3 Bloco 1)."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_MD = REPO / "resultados" / "q3" / "tabelas" / "revisao_normatizacao_processos_matematicos.md"


def _tags_from_cell(val) -> list[str]:
    if pd.isna(val):
        return []
    s = str(val).strip()
    if not s or s == "nan":
        return []
    return [x.strip() for x in s.split(";") if x.strip()]


def main() -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    tit = df.columns[0]
    n = len(df)

    tag_c: Counter[str] = Counter()
    for val in df["math_processes_tags"]:
        for t in _tags_from_cell(val):
            tag_c[t] += 1

    empty_tags = df["math_processes_tags"].fillna("").astype(str).str.strip()
    mask_empty = (empty_tags == "") | (empty_tags == "nan")
    k_empty = int(mask_empty.sum())

    lines = [
        "# Revisão da normatização — Q3 Bloco 1 (processos matemáticos)",
        "",
        f"Fonte: `{CSV_PATH.relative_to(REPO)}`. *N* = {n} estudos.",
        "",
        "O campo **`math_processes`** reproduz o texto livre da coluna 6 da revisão. O campo **`math_processes_tags`** agrega etiquetas canónicas derivadas por palavras-chave (`MATH_PROCESS_KEYWORDS` em `scripts/normalize_eeg_math.py`).",
        "",
        "## Cobertura das tags",
        "",
        f"| Métrica | Valor |",
        f"|---|---:|",
        f"| Estudos com pelo menos uma tag | {n - k_empty} |",
        f"| Estudos sem tag detectada | {k_empty} |",
        "",
        "## Frequência por tag (nº de estudos)",
        "",
        "| Tag | Estudos |",
        "|---|---:|",
    ]
    for tag, cnt in tag_c.most_common():
        lines.append(f"| `{tag}` | {cnt} |")
    if not tag_c:
        lines.append("| — | — |")

    lines.extend(
        [
            "",
            f"## Estudos sem tag (*n* = {k_empty})",
            "",
            "Útil para revisão manual ou extensão do dicionário `MATH_PROCESS_KEYWORDS`.",
            "",
        ]
    )
    for i, r in df[mask_empty].iterrows():
        t0 = str(r["math_processes"]).replace("\n", " ")[:220]
        lines.append(f"### Índice {i}\n")
        lines.append(f"- **Título:** {str(r[tit])[:90]}…\n")
        lines.append(f"- **Col. 6 (processos):** {t0}…\n\n")

    lines.extend(
        [
            "",
            "## Referência de implementação",
            "",
            "- `extract_math_process_tags_from_text` e `MATH_PROCESS_KEYWORDS` em `scripts/normalize_eeg_math.py`.",
            "- Regenerar: `python3 scripts/normalize_eeg_math.py`.",
            "",
        ]
    )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Escrito: {OUT_MD}")


if __name__ == "__main__":
    main()
