#!/usr/bin/env python3
"""Q3 Bloco 1: processos matemáticos — figuras e tabela-resumo."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_FIG = REPO / "resultados" / "q3" / "figuras"
OUT_TAB = REPO / "resultados" / "q3" / "tabelas"

TAG_PT = {
    "addition": "Adição",
    "subtraction": "Subtração",
    "multiplication": "Multiplicação",
    "division": "Divisão",
    "mental_arithmetic": "Cálculo mental",
    "serial_subtraction": "Subtração serial / Kraepelin",
    "fractions_ratios": "Frações / proporções",
    "algebra": "Álgebra / simbólico",
    "magnitude_comparison": "Comparação de magnitudes",
    "word_problems": "Problemas verbais",
    "problem_solving": "Resolução de problemas",
    "deductive_reasoning": "Raciocínio dedutivo",
    "inductive_reasoning": "Raciocínio indutivo",
    "geometry_spatial": "Geometria / espacial",
    "functions_representations": "Funções / representações (G↔A)",
    "standardized_test": "Prova standardizada (ex.: SAT)",
    "puzzles_games": "Puzzles / jogos (ex.: ToH, 24)",
    "verification_task": "Tarefa de verificação",
    "learning_demonstration": "Aprendizagem / demonstrações",
    "modulo": "Operações módulo",
    "broad_math_battery": "Bateria ampla de matemática",
    "written_mode": "Modo escrito (não só mental)",
    "arithmetic_mixed_ops": "Operações aritméticas mistas",
    "arithmetic_general": "Aritmética (menção geral)",
    "executive_mixed_task": "Funções executivas / tarefas mistas",
}

TAG_EN = {
    "addition": "Addition",
    "subtraction": "Subtraction",
    "multiplication": "Multiplication",
    "division": "Division",
    "mental_arithmetic": "Mental calculation",
    "serial_subtraction": "Serial subtraction / Kraepelin",
    "fractions_ratios": "Fractions / proportions",
    "algebra": "Algebra / symbolic",
    "magnitude_comparison": "Magnitude comparison",
    "word_problems": "Word problems",
    "problem_solving": "Problem solving",
    "deductive_reasoning": "Deductive reasoning",
    "inductive_reasoning": "Inductive reasoning",
    "geometry_spatial": "Geometry / spatial",
    "functions_representations": "Functions / representations (G↔A)",
    "standardized_test": "Standardized test (e.g., SAT)",
    "puzzles_games": "Puzzles / games (e.g., ToH, 24)",
    "verification_task": "Verification task",
    "learning_demonstration": "Learning / demonstrations",
    "modulo": "Modulo operations",
    "broad_math_battery": "Broad math battery",
    "written_mode": "Written mode (not just mental)",
    "arithmetic_mixed_ops": "Mixed arithmetic operations",
    "arithmetic_general": "Arithmetic (general mention)",
    "executive_mixed_task": "Executive functions / mixed tasks",
}


def _load() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, encoding="utf-8")


def _tags_from_cell(val) -> list[str]:
    if pd.isna(val):
        return []
    s = str(val).strip()
    if not s or s in ("-", "—", "nan"):
        return []
    return [x.strip() for x in s.split(";") if x.strip()]


def _tag_study_counter(df: pd.DataFrame) -> Counter[str]:
    c: Counter[str] = Counter()
    for val in df["math_processes_tags"]:
        for t in _tags_from_cell(val):
            c[t] += 1
    return c


def _n_tags_per_study(df: pd.DataFrame) -> list[int]:
    return [len(_tags_from_cell(v)) for v in df["math_processes_tags"]]


def _style_axes_minimal(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_tags_bars_h(df: pd.DataFrame, path: Path) -> None:
    c = _tag_study_counter(df)
    if not c:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.text(0.5, 0.5, "No tags", ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        return
    items = sorted(c.items(), key=lambda x: x[1])
    tags, counts = zip(*items)
    n = len(df)
    pct = [100 * x / n for x in counts]
    fig, ax = plt.subplots(figsize=(9, max(4.0, 0.38 * len(tags) + 1.5)))
    y = np.arange(len(tags))
    ax.barh(y, counts, color="#3d5a80", height=0.55, edgecolor="white", linewidth=0.55)
    ax.set_yticks(y)
    labels = [
        f"{TAG_EN.get(t, t.replace('_', ' '))}\n({p:.1f}% of studies)" for t, p in zip(tags, pct)
    ]
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Number of studies with the tag")
    ax.set_title(f"Mathematical processes (math_processes_tags; N = {n} studies)")
    _style_axes_minimal(ax)
    ax.xaxis.grid(True, linestyle=":", alpha=0.45, color="gray")
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_presence_donut(df: pd.DataFrame, path: Path) -> None:
    has = df["math_processes_tags"].apply(lambda v: bool(_tags_from_cell(v)))
    k_yes = int(has.sum())
    k_no = int((~has).sum())
    fig, ax = plt.subplots(figsize=(6.2, 6.2))

    def _lab(pct: float) -> str:
        tot = k_yes + k_no
        v = int(round(pct / 100.0 * tot))
        return f"{pct:.1f}%\n(n = {v})"

    _, _, autotexts = ax.pie(
        [k_yes, k_no],
        labels=["Com ≥1 tag normatizada", "Sem tag detectada"],
        autopct=_lab,
        colors=["#3d5a80", "#d8d8d8"],
        startangle=90,
        counterclock=False,
        wedgeprops={"linewidth": 1.0, "edgecolor": "white", "width": 0.45},
        textprops={"fontsize": 11},
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight("bold")
    ax.text(0, 0, f"N = {k_yes + k_no}\nestudos", ha="center", va="center", fontsize=11, linespacing=1.2)
    ax.set_title("Cobertura das tags de processo (coluna 6)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_n_tags_hist(df: pd.DataFrame, path: Path) -> None:
    arr = np.array(_n_tags_per_study(df), dtype=int)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    max_k = int(arr.max()) if len(arr) else 0
    bins = np.arange(-0.5, max(max_k, 1) + 1.5, 1.0)
    ax.hist(arr, bins=bins, color="#98c1d9", edgecolor="white", linewidth=0.7)
    ax.set_xlabel("Número de tags por estudo")
    ax.set_ylabel("Número de estudos")
    ax.set_title(f"Distribuição da riqueza de tags (mediana = {np.median(arr):.0f})")
    ax.set_xticks(range(0, max_k + 1))
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_summary(df: pd.DataFrame, md_path: Path) -> None:
    n = len(df)
    proc = df["math_processes"].fillna("").astype(str)
    empty_txt = ((proc.str.strip() == "") | (proc.str.strip() == "-")).sum()
    lens = proc[proc.str.strip() != "-"].str.len()
    mean_len = float(lens.mean()) if len(lens) else 0.0

    n_per = np.array(_n_tags_per_study(df), dtype=int)
    k_tagged = int((n_per > 0).sum())
    c = _tag_study_counter(df)
    n_assign = sum(c.values())

    lines = [
        "# Q3 Bloco 1 — Resumo quantitativo (processos matemáticos)",
        "",
        f"Fonte: `dados/tabela_normatizada.csv`. Estudos: **{n}**.",
        "",
        "| Métrica | Valor |",
        "|---|---|",
        f"| Texto col. 6 vazio ou «-» | {int(empty_txt)} |",
        f"| Comprimento médio do texto (excl. «-») | {mean_len:.1f} caracteres |",
        f"| Estudos com ≥1 tag (`math_processes_tags`) | {k_tagged} |",
        f"| Estudos sem tag | {n - k_tagged} |",
        f"| Total de atribuições estudo→tag* | {n_assign} |",
        f"| Média de tags por estudo (todos) | {n_per.mean():.2f} |",
        (
            f"| Média de tags (só estudos com tag) | {float(n_per[n_per > 0].mean()):.2f} |"
            if k_tagged
            else "| Média de tags (só estudos com tag) | — |"
        ),
        f"| Máximo de tags num único estudo | {int(n_per.max())} |",
        "",
        "*Cada tag conta uma vez por estudo em que o padrão lexical foi encontrado.",
        "",
        "## Frequência por tag",
        "",
        "| Tag (código) | Estudos | % do corpus |",
        "|---|---:|---:|",
    ]
    for tag, cnt in sorted(c.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| `{tag}` | {cnt} | {100 * cnt / n:.1f}% |")
    if not c:
        lines.append("| — | — | — |")
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
    plot_tags_bars_h(df, OUT_FIG / "q3_b1_barras_processos_tags.png")
    plot_presence_donut(df, OUT_FIG / "q3_b1_rosca_cobertura_tags.png")
    plot_n_tags_hist(df, OUT_FIG / "q3_b1_hist_n_tags_por_estudo.png")
    write_summary(df, OUT_TAB / "q3_b1_resumo.md")

    print(f"Figuras: {OUT_FIG}")
    print(f"Tabelas: {OUT_TAB}")


if __name__ == "__main__":
    main()
