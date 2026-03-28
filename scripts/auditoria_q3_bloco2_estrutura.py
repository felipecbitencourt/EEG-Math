#!/usr/bin/env python3
"""Relatório: comparison_type, comparison_detail, has_control_task (Q3 Bloco 2)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_MD = REPO / "resultados" / "q3" / "tabelas" / "revisao_normatizacao_estrutura_experimental.md"

TYPE_PT = {
    "unspecified": "Não especificado / texto vazio",
    "within_task_only": "Só manipulações dentro da tarefa matemática",
    "resting_state": "Repouso / baseline de repouso",
    "baseline_epoch": "Intervalo pré-estímulo / ITI / fixação",
    "control_verbal": "Controlo verbal / linguístico",
    "control_perceptual": "Controlo perceptivo / visuoespacial",
    "control_working_memory": "Controlo de memória de trabalho (ex.: n-back)",
    "control_simple_math": "Controlo com tarefa matemática mais simples (mesmo domínio)",
    "mixed": "Várias condições de referência (ex.: repouso + outra tarefa)",
    "other_context": "Contexto experimental atípico (ex.: gravidade)",
    "other": "Outro / não classificado pelo dicionário atual",
}


def main() -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    tit = df.columns[0]
    c7 = [c for c in df.columns if c.strip().startswith("7.")][0]
    n = len(df)

    vc = df["comparison_type"].fillna("unspecified").astype(str).value_counts()
    vd = df["comparison_detail"].fillna("(vazio)").astype(str).value_counts()
    ht = df["has_control_task"].value_counts()

    lines = [
        "# Revisão da normatização — Q3 Bloco 2 (estrutura experimental)",
        "",
        f"Fonte: `{CSV_PATH.relative_to(REPO)}`. *N* = {n} estudos.",
        "",
        "Campos derivados da **coluna 7** (*«Durante a tarefa, a tarefa matemática é comparada a quê?»*) por `extract_comparison_from_text` em `scripts/normalize_eeg_math.py`.",
        "",
        "- **`comparison_type`:** categoria principal da comparação.",
        "- **`comparison_detail`:** subtipo ocular quando aplicável (`eyes_closed`, `eyes_open`, `eyes_open_and_closed`).",
        "- **`has_control_task`:** `False` só para `within_task_only` ou `unspecified` (repouso conta como referência externa, `True`).",
        "",
        "## `comparison_type`",
        "",
        "| Código | Estudos | % | Rótulo (PT) |",
        "|---|---:|---:|---|",
    ]
    for cat, cnt in vc.items():
        pct = 100 * cnt / n
        lab = TYPE_PT.get(cat, cat)
        lines.append(f"| `{cat}` | {int(cnt)} | {pct:.1f}% | {lab} |")

    lines.extend(
        [
            "",
            "## `comparison_detail`",
            "",
            "| Valor | Estudos |",
            "|---|---:|",
        ]
    )
    for v, c in vd.items():
        lines.append(f"| {v} | {int(c)} |")

    lines.extend(
        [
            "",
            "## `has_control_task`",
            "",
            "| Valor | Estudos |",
            "|---|---:|",
        ]
    )
    for v, c in ht.items():
        lines.append(f"| `{v}` | {int(c)} |")

    uns = df[df["comparison_type"].fillna("unspecified").astype(str) == "unspecified"]
    lines.extend(
        [
            "",
            f"## Estudos `unspecified` (*n* = {len(uns)})",
            "",
            "Revisar texto da coluna 7 ou alargar padrões em `extract_comparison_from_text`.",
            "",
        ]
    )
    for i, r in uns.iterrows():
        t7 = str(r[c7]).replace("\n", " ")[:240]
        lines.append(f"### Índice {i}\n")
        lines.append(f"- **Título:** {str(r[tit])[:88]}…\n")
        lines.append(f"- **Col. 7:** {t7}…\n\n")

    lines.extend(
        [
            "## Regeneração",
            "",
            "`python3 scripts/normalize_eeg_math.py`",
            "",
        ]
    )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Escrito: {OUT_MD}")


if __name__ == "__main__":
    main()
