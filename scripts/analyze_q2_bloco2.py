#!/usr/bin/env python3
"""Q2 Bloco 2: tipo de população e marcadores — figuras e tabela-resumo."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_FIG = REPO / "resultados" / "q2" / "figuras"
OUT_TAB = REPO / "resultados" / "q2" / "tabelas"

POP_PT = {
    "clinical": "População clínica / neurológica",
    "experts_maths": "Expertise ou talento em matemática",
    "mixed_children_students": "Misto (crianças e estudantes)",
    "children": "Crianças",
    "elderly": "Idosos",
    "students": "Estudantes",
    "healthy": "Adultos (amostra de conveniência)",
    "unspecified": "Não especificado",
}

MARKER_PT = {
    "math_anxiety": "Ansiedade matemática / ameaça de estereótipo",
    "dyscalculia": "Discalculia",
    "gifted": "Alto desempenho / talento",
    "experts_novices": "Especialistas vs. novatos",
    "mci_dementia": "DCI / demência",
    "schizophrenia": "Esquizofrenia",
    "autism": "TEA / autismo",
    "adhd": "TDAH",
    "epilepsy": "Epilepsia",
    "stroke": "AVC",
    "meditators": "Meditação / mindfulness",
    "teachers": "Professores",
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


def _population_counts(df: pd.DataFrame) -> pd.Series:
    s = df["amostra_population_type"].fillna("unspecified").astype(str)
    return s.value_counts()


def _marker_study_counter(df: pd.DataFrame) -> Counter[str]:
    c: Counter[str] = Counter()
    for val in df["amostra_marcadores_tags"]:
        for t in _tags_from_cell(val):
            c[t] += 1
    return c


def plot_population_bars_h(df: pd.DataFrame, path: Path) -> None:
    vc = _population_counts(df).sort_values(ascending=True)
    n = len(df)
    pct = 100 * vc / n
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    colors = plt.cm.Blues(np.linspace(0.35, 0.85, len(vc)))[::-1]
    y = np.arange(len(vc))
    ax.barh(y, vc.values, color=colors, height=0.62, edgecolor="white", linewidth=0.6)
    ax.set_yticks(y)
    labels = [f"{POP_PT.get(i, i)}\n({pct[i]:.1f}%)" for i in vc.index]
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Número de estudos")
    ax.set_title(f"Tipo de população (amostra_population_type; k = {n})")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_population_pie(df: pd.DataFrame, path: Path) -> None:
    vc = _population_counts(df)
    order_pref = [
        "students",
        "healthy",
        "clinical",
        "experts_maths",
        "children",
        "mixed_children_students",
        "elderly",
        "unspecified",
    ]
    idx = [x for x in order_pref if x in vc.index] + [x for x in vc.index if x not in order_pref]
    vc = vc.reindex(idx)
    palette = {
        "students": "#3d5a80",
        "healthy": "#98c1d9",
        "clinical": "#ee6c4d",
        "experts_maths": "#e07a5f",
        "children": "#81b29a",
        "mixed_children_students": "#3d405b",
        "elderly": "#6d6875",
        "unspecified": "#d8d8d8",
    }
    bar_cols = [palette.get(i, "#adb5bd") for i in vc.index]
    labels = [POP_PT.get(i, i) for i in vc.index]
    total = int(vc.sum())

    def _lab(p: float) -> str:
        v = int(round(p / 100.0 * total))
        return f"{p:.1f}%\n(n = {v})"

    fig, ax = plt.subplots(figsize=(6.8, 6.4))
    ax.pie(
        vc.values,
        labels=labels,
        autopct=_lab,
        colors=bar_cols,
        startangle=90,
        counterclock=False,
        wedgeprops={"linewidth": 1.0, "edgecolor": "white"},
        textprops={"fontsize": 9},
    )
    ax.set_title(f"Composição do corpus por tipo de população (N = {total} estudos)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_markers_bars_h(df: pd.DataFrame, path: Path) -> None:
    c = _marker_study_counter(df)
    if not c:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.text(0.5, 0.5, "Sem tags de marcadores", ha="center", va="center")
        ax.set_axis_off()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return
    items = sorted(c.items(), key=lambda x: -x[1])
    tags = [t for t, _ in items]
    counts = [n for _, n in items]
    labels = [MARKER_PT.get(t, t.replace("_", " ")) for t in tags]
    fig, ax = plt.subplots(figsize=(8, max(3.2, 0.45 * len(tags) + 1.2)))
    y = np.arange(len(tags))
    ax.barh(y, counts, color="#3d5a80", height=0.55, edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Número de estudos com a tag (coluna 5 normatizada)")
    k_any = int(df["amostra_marcadores_tags"].apply(lambda v: bool(_tags_from_cell(v))).sum())
    ax.set_title(f"Marcadores amostrais (amostra_marcadores_tags); estudos com ≥1 tag: k = {k_any}")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_markers_presence_donut(df: pd.DataFrame, path: Path) -> None:
    has = df["amostra_marcadores_tags"].apply(lambda v: bool(_tags_from_cell(v)))
    k_yes = int(has.sum())
    k_no = int((~has).sum())
    fig, ax = plt.subplots(figsize=(6.2, 6.2))
    if k_yes + k_no == 0:
        ax.text(0.5, 0.5, "Sem dados", ha="center", va="center")
        ax.set_axis_off()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return

    def _lab(pct: float) -> str:
        tot = k_yes + k_no
        v = int(round(pct / 100.0 * tot))
        return f"{pct:.1f}%\n(n = {v})"

    _, _, autotexts = ax.pie(
        [k_yes, k_no],
        labels=["Com ≥1 marcador", "Sem marcador codificado"],
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
    ax.text(
        0,
        0,
        f"N = {k_yes + k_no}\nestudos",
        ha="center",
        va="center",
        fontsize=11,
        linespacing=1.2,
    )
    ax.set_title("Cobertura de marcadores na coluna 5 (por estudo)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_summary(df: pd.DataFrame, md_path: Path) -> None:
    nrows = len(df)
    vc = _population_counts(df)
    mc = _marker_study_counter(df)
    k_tagged = int(df["amostra_marcadores_tags"].apply(lambda v: bool(_tags_from_cell(v))).sum())
    n_tag_instances = sum(mc.values())
    lines = [
        "# Q2 Bloco 2 — Resumo quantitativo",
        "",
        f"Fonte: `dados/tabela_normatizada.csv`. Estudos (linhas): **{nrows}**.",
        "",
        "## `amostra_population_type` (contagem por estudo)",
        "",
        "| Categoria (código) | Estudos | % |",
        "|---|---:|---:|",
    ]
    for cat, cnt in vc.items():
        lines.append(f"| `{cat}` | {int(cnt)} | {100 * cnt / nrows:.1f}% |")
    lines.extend(
        [
            "",
            "## `amostra_marcadores_tags`",
            "",
            f"| Métrica | Valor |",
            f"|---|---|",
            f"| Estudos com pelo menos uma tag | {k_tagged} |",
            f"| Estudos sem tag | {nrows - k_tagged} |",
            f"| Total de atribuições tag→estudo* | {n_tag_instances} |",
            "",
            "*Um estudo pode ter várias tags; cada tag conta uma vez por estudo em que aparece.",
            "",
            "### Frequência por tag (nº de estudos)",
            "",
        ]
    )
    if mc:
        lines.append("| Tag | Estudos |")
        lines.append("|---|---:|")
        for tag, cnt in sorted(mc.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"| `{tag}` | {cnt} |")
    else:
        lines.append("*(Nenhuma tag detectada.)*")
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
    plot_population_bars_h(df, OUT_FIG / "q2_b2_barras_population_type.png")
    plot_population_pie(df, OUT_FIG / "q2_b2_pizza_population_type.png")
    plot_markers_bars_h(df, OUT_FIG / "q2_b2_barras_marcadores.png")
    plot_markers_presence_donut(df, OUT_FIG / "q2_b2_rosca_marcadores_presenca.png")
    write_summary(df, OUT_TAB / "q2_b2_resumo.md")

    print(f"Figuras: {OUT_FIG}")
    print(f"Tabelas: {OUT_TAB}")


if __name__ == "__main__":
    main()
