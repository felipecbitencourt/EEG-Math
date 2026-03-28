#!/usr/bin/env python3
"""Q3 Bloco 2: estrutura experimental — figuras e tabela-resumo."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_FIG = REPO / "resultados" / "q3" / "figuras"
OUT_TAB = REPO / "resultados" / "q3" / "tabelas"

TYPE_PT = {
    "unspecified": "Não especificado",
    "within_task_only": "Só dentro da tarefa matemática",
    "resting_state": "Repouso / baseline de repouso",
    "baseline_epoch": "Pré-estímulo / ITI / fixação",
    "control_verbal": "Controlo verbal",
    "control_perceptual": "Controlo perceptivo",
    "control_working_memory": "Controlo mem. trabalho",
    "control_simple_math": "Controlo matemático simples",
    "mixed": "Misto (várias referências)",
    "other_context": "Contexto atípico",
    "other": "Outro",
}


def _load() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, encoding="utf-8")


def plot_comparison_bars_h(df: pd.DataFrame, path: Path) -> None:
    vc = df["comparison_type"].fillna("unspecified").astype(str).value_counts().sort_values(ascending=True)
    n = len(df)
    pct = 100 * vc / n
    fig, ax = plt.subplots(figsize=(9, max(4.2, 0.4 * len(vc) + 1.4)))
    y = np.arange(len(vc))
    ax.barh(y, vc.values, color="#3d5a80", height=0.55, edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    labels = [f"{TYPE_PT.get(i, i)}\n({pct[i]:.1f}%)" for i in vc.index]
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Número de estudos")
    ax.set_title(f"Tipo de comparação experimental (comparison_type; N = {n})")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_comparison_pie(df: pd.DataFrame, path: Path) -> None:
    vc = df["comparison_type"].fillna("unspecified").astype(str).value_counts()
    labels = [TYPE_PT.get(i, i) for i in vc.index]
    total = int(vc.sum())

    def _lab(p: float) -> str:
        v = int(round(p / 100.0 * total))
        return f"{p:.1f}%\n(n = {v})"

    fig, ax = plt.subplots(figsize=(7.2, 7.0))
    ax.pie(
        vc.values,
        labels=labels,
        autopct=_lab,
        startangle=90,
        counterclock=False,
        wedgeprops={"linewidth": 1.0, "edgecolor": "white"},
        textprops={"fontsize": 8},
    )
    ax.set_title(f"Composição por comparison_type (N = {total})")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_has_control_donut(df: pd.DataFrame, path: Path) -> None:
    s = df["has_control_task"].apply(lambda x: bool(x) if str(x).lower() not in ("nan", "") else False)
    k_yes = int(s.sum())
    k_no = int((~s).sum())
    fig, ax = plt.subplots(figsize=(6.0, 6.0))

    def _lab(pct: float) -> str:
        tot = k_yes + k_no
        v = int(round(pct / 100.0 * tot))
        return f"{pct:.1f}%\n(n = {v})"

    _, _, autotexts = ax.pie(
        [k_yes, k_no],
        labels=["has_control_task = True", "has_control_task = False"],
        autopct=_lab,
        colors=["#3d5a80", "#d8d8d8"],
        startangle=90,
        counterclock=False,
        wedgeprops={"linewidth": 1.0, "edgecolor": "white", "width": 0.45},
        textprops={"fontsize": 10},
    )
    for t in autotexts:
        t.set_fontweight("bold")
    ax.text(0, 0, f"N = {k_yes + k_no}", ha="center", va="center", fontsize=11)
    ax.set_title("Referência externa à tarefa matemática\n(False = só within-task ou não especificado)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_summary(df: pd.DataFrame, md_path: Path) -> None:
    n = len(df)
    vc = df["comparison_type"].fillna("unspecified").astype(str).value_counts()
    vd = df["comparison_detail"].value_counts(dropna=False)
    ht = df["has_control_task"].value_counts()
    lines = [
        "# Q3 Bloco 2 — Resumo quantitativo (estrutura experimental)",
        "",
        f"Fonte: `dados/tabela_normatizada.csv`. Estudos: **{n}**.",
        "",
        "## comparison_type",
        "",
        "| Código | Estudos | % |",
        "|---|---:|---:|",
    ]
    for k, v in vc.items():
        lines.append(f"| `{k}` | {int(v)} | {100 * v / n:.1f}% |")
    lines.extend(["", "## comparison_detail", "", "| Valor | Estudos |", "|---|---:|"])
    for k, v in vd.items():
        kk = k if pd.notna(k) and str(k) != "nan" else "(vazio)"
        lines.append(f"| {kk} | {int(v)} |")
    lines.extend(["", "## has_control_task", "", "| Valor | Estudos |", "|---|---:|"])
    for k, v in ht.items():
        lines.append(f"| `{k}` | {int(v)} |")
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "figure.facecolor": "white",
        }
    )
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    OUT_TAB.mkdir(parents=True, exist_ok=True)
    df = _load()
    plot_comparison_bars_h(df, OUT_FIG / "q3_b2_barras_comparison_type.png")
    plot_comparison_pie(df, OUT_FIG / "q3_b2_pizza_comparison_type.png")
    plot_has_control_donut(df, OUT_FIG / "q3_b2_rosca_has_control_task.png")
    write_summary(df, OUT_TAB / "q3_b2_resumo.md")
    print(f"Figuras: {OUT_FIG}")
    print(f"Tabelas: {OUT_TAB}")


if __name__ == "__main__":
    main()
