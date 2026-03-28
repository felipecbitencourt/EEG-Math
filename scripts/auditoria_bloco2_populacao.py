#!/usr/bin/env python3
"""Relatório: amostra_population_type e amostra_marcadores_tags (Bloco 2 Q2)."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_MD = REPO / "resultados" / "q2" / "tabelas" / "revisao_normatizacao_bloco2.md"
def main() -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    tit = df.columns[0]
    c4 = "4. Amostra (número de participantes, idade)"
    c5 = [c for c in df.columns if c.strip().startswith("5.")][0]

    pop = df["amostra_population_type"].value_counts()
    marc = df["amostra_marcadores_tags"].fillna("").astype(str).str.strip()
    n_marc = int((marc != "").sum())

    tag_c = Counter()
    for s in marc:
        if not s or s == "nan":
            continue
        for x in s.split(";"):
            x = x.strip()
            if x:
                tag_c[x] += 1

    # unspecified: trechos para revisão humana
    uns = df[df["amostra_population_type"] == "unspecified"]
    lines = [
        "# Revisão da normatização — Bloco 2 (tipo de população e marcadores)",
        "",
        f"Fonte: `{CSV_PATH.relative_to(REPO)}`. *N* = {len(df)} estudos.",
        "",
        "## `amostra_population_type` (colunas 4 + 5 combinadas)",
        "",
        "Categorias atuais: `clinical`, `experts_maths`, `mixed_children_students`, `children`, `elderly`, `students`, `healthy`, `unspecified`.",
        "",
        "| Categoria | Estudos |",
        "|-----------|--------:|",
    ]
    for k, v in pop.items():
        lines.append(f"| {k} | {int(v)} |")
    lines.extend(
        [
            "",
            "## `amostra_marcadores_tags` (principalmente coluna 5)",
            "",
            f"Linhas com pelo menos uma tag: **{n_marc}** / {len(df)}.",
            "",
            "| Tag (canônica) | Frequência |",
            "|------------------|------------:|",
        ]
    )
    for tag, cnt in tag_c.most_common(30):
        lines.append(f"| `{tag}` | {cnt} |")
    if not tag_c:
        lines.append("| — | — |")

    lines.extend(
        [
            "",
            f"## Estudos ainda `unspecified` em população (*n* = {len(uns)})",
            "",
            "Útil para checagem manual ou refinamento futuro do extrator.",
            "",
        ]
    )
    for i, r in uns.head(22).iterrows():
        t4 = str(r[c4]).replace("\n", " ")[:200]
        t5 = str(r[c5]).replace("\n", " ")[:120]
        lines.append(f"### Índice {i}\n")
        lines.append(f"- **Título:** {str(r[tit])[:80]}…\n")
        lines.append(f"- **Col. 4:** {t4}…\n")
        lines.append(f"- **Col. 5:** {t5}…\n\n")

    if len(uns) > 22:
        lines.append(f"\n*… e mais {len(uns) - 22} registros unspecified.*\n")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Escrito: {OUT_MD}")


if __name__ == "__main__":
    main()
