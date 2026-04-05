#!/usr/bin/env python3
"""Q3 Bloco 4: medidas observaveis — figuras e tabelas para artigo."""

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

MEASURE_PT = {
    "Accuracy": "Acuracia",
    "Reaction_time": "Tempo de reacao",
    "Score": "Score / nota",
    "Error_rate": "Taxa de erro",
    "Self_report": "Autorrelato",
    "Throughput": "Produtividade (itens/tempo)",
    "Difficulty": "Dificuldade percebida",
    "Anxiety": "Ansiedade",
    "Cognitive_load": "Carga cognitiva",
    "Latency": "Latencia",
    "Strategy": "Estrategia",
    "Confidence": "Confianca",
    "Drowsiness": "Sonolencia",
    "Happiness": "Humor positivo",
    "Stress": "Estresse",
}

FLAG_PT = {
    "has_behavioral": "Medida comportamental",
    "has_physio": "Variavel fisiologica adicional",
    "has_clinical_psych": "Variavel psicologica clinica",
}


def _load() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, encoding="utf-8")


def _split_measures(val) -> list[str]:
    if pd.isna(val):
        return []
    s = str(val).strip()
    if not s or s in ("-", "—", "nan"):
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def _measures_counter(df: pd.DataFrame) -> Counter[str]:
    c: Counter[str] = Counter()
    for val in df["behavioral_measures"]:
        for m in _split_measures(val):
            c[m] += 1
    return c


def _flags_df(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    for col in ("has_behavioral", "has_physio", "has_clinical_psych"):
        out[col] = df[col].fillna(False).astype(bool)
    return out


def plot_measures_bars(df: pd.DataFrame, out_path: Path) -> None:
    c = _measures_counter(df)
    if not c:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.text(0.5, 0.5, "Sem medidas comportamentais detectadas", ha="center", va="center")
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        return
    items = sorted(c.items(), key=lambda x: x[1])
    labs, vals = zip(*items)
    n = len(df)
    pcts = [100 * v / n for v in vals]
    fig, ax = plt.subplots(figsize=(9.2, max(4.5, 0.42 * len(labs) + 1.8)))
    y = np.arange(len(labs))
    ax.barh(y, vals, color="#3d5a80", height=0.56, edgecolor="white", linewidth=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{MEASURE_PT.get(k, k)}\n({p:.1f}% dos estudos)" for k, p in zip(labs, pcts)], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Numero de estudos")
    ax.set_title(f"Frequencia de medidas comportamentais observaveis (N = {n})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_behavioral_count_hist(df: pd.DataFrame, out_path: Path) -> None:
    arr = df["behavioral_count"].fillna(0).astype(int).to_numpy()
    max_k = int(arr.max()) if len(arr) else 0
    bins = np.arange(-0.5, max(max_k, 1) + 1.5, 1.0)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.hist(arr, bins=bins, color="#98c1d9", edgecolor="white", linewidth=0.8)
    ax.set_xticks(range(0, max_k + 1))
    ax.set_xlabel("Numero de medidas comportamentais por estudo (behavioral_count)")
    ax.set_ylabel("Numero de estudos")
    ax.set_title(f"Distribuicao da riqueza comportamental (mediana = {np.median(arr):.0f})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_flags_prevalence(df: pd.DataFrame, out_path: Path) -> None:
    f = _flags_df(df)
    n = len(df)
    cols = ["has_behavioral", "has_physio", "has_clinical_psych"]
    vals = [int(f[c].sum()) for c in cols]
    pcts = [100 * v / n for v in vals]

    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    x = np.arange(len(cols))
    bars = ax.bar(x, vals, color=["#3d5a80", "#4f6d7a", "#6b8e9f"], width=0.62, edgecolor="white", linewidth=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels([FLAG_PT[c] for c in cols], fontsize=10)
    ax.set_ylabel("Numero de estudos")
    ax.set_title(f"Prevalencia dos eixos observaveis no corpus (N = {n})")
    for b, v, p in zip(bars, vals, pcts):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.5, f"{v}\n({p:.1f}%)", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _combo_counts(df: pd.DataFrame) -> pd.Series:
    f = _flags_df(df)
    code = (
        f["has_behavioral"].astype(int).astype(str)
        + "-"
        + f["has_physio"].astype(int).astype(str)
        + "-"
        + f["has_clinical_psych"].astype(int).astype(str)
    )
    return code.value_counts().sort_values(ascending=False)


def plot_combo_bars(df: pd.DataFrame, out_path: Path) -> None:
    vc = _combo_counts(df)
    n = len(df)
    fig, ax = plt.subplots(figsize=(8.8, max(4.2, 0.46 * len(vc) + 1.6)))
    y = np.arange(len(vc))
    ax.barh(y, vc.values, color="#3d5a80", height=0.58, edgecolor="white", linewidth=0.6)
    ax.set_yticks(y)
    labels = [f"{k}  (B-P-C)" for k in vc.index]
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Numero de estudos")
    ax.set_title(f"Perfis de combinacao das flags (B=behavioral, P=physio, C=clinical psych; N = {n})")
    for yi, v in zip(y, vc.values):
        ax.text(v + 0.3, yi, f"{v} ({100*v/n:.1f}%)", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def write_summary(df: pd.DataFrame, out_path: Path) -> None:
    n = len(df)
    f = _flags_df(df)
    m = _measures_counter(df)
    bc = df["behavioral_count"].fillna(0).astype(int)
    lines = [
        "# Q3 Bloco 4 — Resumo quantitativo (medidas observaveis)",
        "",
        f"Fonte: `dados/tabela_normatizada.csv`. Estudos: **{n}**.",
        "",
        "| Indicador | Valor |",
        "|---|---:|",
        f"| Estudos com `has_behavioral` = True | {int(f['has_behavioral'].sum())} ({100*f['has_behavioral'].mean():.1f}%) |",
        f"| Estudos com `has_physio` = True | {int(f['has_physio'].sum())} ({100*f['has_physio'].mean():.1f}%) |",
        f"| Estudos com `has_clinical_psych` = True | {int(f['has_clinical_psych'].sum())} ({100*f['has_clinical_psych'].mean():.1f}%) |",
        f"| Media de `behavioral_count` (corpus) | {bc.mean():.2f} |",
        f"| Mediana de `behavioral_count` | {bc.median():.1f} |",
        f"| Maximo de `behavioral_count` | {int(bc.max())} |",
        "",
        "## Frequencia por medida comportamental",
        "",
        "| Medida (codigo) | Estudos | % do corpus |",
        "|---|---:|---:|",
    ]
    for k, v in sorted(m.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| `{k}` | {v} | {100*v/n:.1f}% |")
    if not m:
        lines.append("| — | — | — |")

    dist = bc.value_counts().sort_index()
    lines.extend(["", "## Distribuicao de behavioral_count", "", "| behavioral_count | Estudos |", "|---:|---:|"])
    for k, v in dist.items():
        lines.append(f"| {int(k)} | {int(v)} |")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_flag_combos(df: pd.DataFrame, out_path: Path) -> None:
    vc = _combo_counts(df)
    n = len(df)
    lines = [
        "# Q3 Bloco 4 — Combinacoes das flags",
        "",
        "Codigo: `has_behavioral-has_physio-has_clinical_psych` (1=True, 0=False).",
        "",
        "| Perfil | Estudos | % do corpus |",
        "|---|---:|---:|",
    ]
    for k, v in vc.items():
        lines.append(f"| `{k}` | {int(v)} | {100*v/n:.1f}% |")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


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
    plot_measures_bars(df, OUT_FIG / "q3_b4_barras_behavioral_measures.png")
    plot_behavioral_count_hist(df, OUT_FIG / "q3_b4_hist_behavioral_count.png")
    plot_flags_prevalence(df, OUT_FIG / "q3_b4_barras_prevalencia_flags.png")
    plot_combo_bars(df, OUT_FIG / "q3_b4_barras_combo_flags.png")
    write_summary(df, OUT_TAB / "q3_b4_resumo.md")
    write_flag_combos(df, OUT_TAB / "q3_b4_combinacoes_flags.md")
    print(f"Figuras: {OUT_FIG}")
    print(f"Tabelas: {OUT_TAB}")


if __name__ == "__main__":
    main()

