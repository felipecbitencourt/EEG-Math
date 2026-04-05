#!/usr/bin/env python3
"""Q3 Bloco 3: dimensoes cognitivas associadas — figuras e tabelas."""

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

AXES = {
    "psych_domains": "Dominios psicologicos",
    "behavioral_domains": "Dominios comportamentais",
    "physio_list": "Variaveis fisiologicas adicionais",
}

LABELS_PT = {
    "Anxiety": "Ansiedade",
    "Stress": "Estresse",
    "Depression": "Depressao",
    "Intelligence": "Inteligencia",
    "Cognition": "Cognicao",
    "Attention": "Atencao",
    "Personality": "Personalidade",
    "Diagnosis": "Diagnostico",
    "Self_concept": "Autoconceito",
    "performance": "Desempenho",
    "speed": "Velocidade",
    "efficiency": "Eficiencia",
    "metacognition": "Metacognicao",
    "affective": "Afetivo",
    "cognitive_load": "Carga cognitiva",
    "attention": "Atencao",
    "learning": "Aprendizagem",
    "EOG": "EOG",
    "EMG": "EMG",
    "ECG": "ECG",
    "HRV": "HRV",
    "Respiration": "Respiracao",
    "GSR_EDA": "GSR/EDA",
    "Sleep": "Sono",
    "Pulse": "Pulso",
    "Blood_pressure": "Pressao arterial",
    "Glucose": "Glicose",
}


def _load() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, encoding="utf-8")


def _split_items(val) -> list[str]:
    if pd.isna(val):
        return []
    s = str(val).strip()
    if not s or s in ("-", "—", "nan"):
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def _is_source_eligible(series: pd.Series) -> pd.Series:
    s = series.fillna("").astype(str).str.strip()
    return ~s.isin(["", "-", "—", "nan"])


def _counter_for_col(df: pd.DataFrame, col: str) -> Counter[str]:
    c: Counter[str] = Counter()
    for v in df[col]:
        for item in _split_items(v):
            c[item] += 1
    return c


def _n_items_per_study(df: pd.DataFrame, col: str) -> np.ndarray:
    return np.array([len(_split_items(v)) for v in df[col]], dtype=int)


def _pt_label(code: str) -> str:
    return LABELS_PT.get(code, code.replace("_", " "))


def plot_bars_h(df: pd.DataFrame, col: str, out_path: Path) -> None:
    c = _counter_for_col(df, col)
    if not c:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.text(0.5, 0.5, "Sem categorias detectadas", ha="center", va="center")
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        return
    items = sorted(c.items(), key=lambda x: x[1])
    cats, counts = zip(*items)
    n = len(df)
    pct = [100 * k / n for k in counts]
    fig, ax = plt.subplots(figsize=(9, max(4.0, 0.40 * len(cats) + 1.6)))
    y = np.arange(len(cats))
    ax.barh(y, counts, color="#3d5a80", height=0.55, edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    labels = [f"{_pt_label(cat)}\n({p:.1f}% dos estudos)" for cat, p in zip(cats, pct)]
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Numero de estudos")
    ax.set_title(f"{AXES[col]} (N = {n})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_coverage_donut(df: pd.DataFrame, col: str, out_path: Path) -> None:
    has_data = df[col].apply(lambda x: bool(_split_items(x)))
    k_yes = int(has_data.sum())
    k_no = int((~has_data).sum())
    fig, ax = plt.subplots(figsize=(6.0, 6.0))

    def _lab(pct: float) -> str:
        tot = k_yes + k_no
        val = int(round(pct / 100.0 * tot))
        return f"{pct:.1f}%\n(n = {val})"

    _, _, autotexts = ax.pie(
        [k_yes, k_no],
        labels=["Preenchido", "Vazio"],
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
    ax.set_title(f"Cobertura de {col}")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _cooccurrence_matrix(df: pd.DataFrame, col_a: str, col_b: str) -> tuple[list[str], list[str], np.ndarray]:
    ca = _counter_for_col(df, col_a)
    cb = _counter_for_col(df, col_b)
    labs_a = [k for k, _ in sorted(ca.items(), key=lambda x: (-x[1], x[0]))]
    labs_b = [k for k, _ in sorted(cb.items(), key=lambda x: (-x[1], x[0]))]
    arr = np.zeros((len(labs_a), len(labs_b)), dtype=int)
    ia = {k: i for i, k in enumerate(labs_a)}
    ib = {k: i for i, k in enumerate(labs_b)}
    for _, row in df.iterrows():
        aa = set(_split_items(row[col_a]))
        bb = set(_split_items(row[col_b]))
        for a in aa:
            for b in bb:
                arr[ia[a], ib[b]] += 1
    return labs_a, labs_b, arr


def plot_heatmap(df: pd.DataFrame, col_a: str, col_b: str, out_path: Path) -> None:
    labs_a, labs_b, arr = _cooccurrence_matrix(df, col_a, col_b)
    if arr.size == 0:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.text(0.5, 0.5, "Sem coocorrencias", ha="center", va="center")
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        return

    # Limita para manter legibilidade visual.
    max_rows = 10
    max_cols = 10
    labs_a = labs_a[:max_rows]
    labs_b = labs_b[:max_cols]
    arr = arr[:max_rows, :max_cols]

    fig_w = max(6.8, 1.0 + 0.60 * len(labs_b))
    fig_h = max(5.2, 1.4 + 0.45 * len(labs_a))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    im = ax.imshow(arr, cmap="Blues", aspect="auto")
    ax.set_xticks(np.arange(len(labs_b)))
    ax.set_yticks(np.arange(len(labs_a)))
    ax.set_xticklabels([_pt_label(x) for x in labs_b], rotation=35, ha="right", fontsize=8)
    ax.set_yticklabels([_pt_label(x) for x in labs_a], fontsize=8)
    ax.set_title(f"Coocorrencia: {col_a} x {col_b}")
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            v = int(arr[i, j])
            if v > 0:
                ax.text(j, i, str(v), ha="center", va="center", fontsize=8, color="#1b263b")
    cbar = fig.colorbar(im, ax=ax, shrink=0.85)
    cbar.set_label("Numero de estudos", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_n_axes(df: pd.DataFrame, out_path: Path) -> None:
    n_axes = (
        df["psych_domains"].apply(lambda x: bool(_split_items(x))).astype(int)
        + df["behavioral_domains"].apply(lambda x: bool(_split_items(x))).astype(int)
        + df["physio_list"].apply(lambda x: bool(_split_items(x))).astype(int)
    )
    vc = n_axes.value_counts().sort_index()
    x = np.array([0, 1, 2, 3], dtype=int)
    y = np.array([int(vc.get(i, 0)) for i in x], dtype=int)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.bar(x, y, color="#3d5a80", width=0.65, edgecolor="white", linewidth=0.7)
    for xi, yi in zip(x, y):
        ax.text(xi, yi + 0.4, str(yi), ha="center", va="bottom", fontsize=10)
    ax.set_xticks(x)
    ax.set_xlabel("Numero de eixos preenchidos (psych, behavioral, physio)")
    ax.set_ylabel("Numero de estudos")
    ax.set_title("Perfil de multimodalidade (3 eixos do Bloco 3)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def write_summary(df: pd.DataFrame, md_path: Path) -> None:
    n = len(df)
    lines = [
        "# Q3 Bloco 3 — Resumo quantitativo (dimensoes cognitivas associadas)",
        "",
        f"Fonte: `dados/tabela_normatizada.csv`. Estudos: **{n}**.",
        "",
        "| Eixo | Preenchido (n/N) | % do corpus | Elegiveis com texto na origem | Cobertura entre elegiveis |",
        "|---|---:|---:|---:|---:|",
    ]
    for col in ("psych_domains", "behavioral_domains", "physio_list"):
        filled = int(df[col].apply(lambda x: bool(_split_items(x))).sum())
        elig = int(_is_source_eligible(df[col]).sum())
        cov = (100 * filled / elig) if elig else 0.0
        lines.append(f"| `{col}` | {filled}/{n} | {100 * filled / n:.1f}% | {elig} | {cov:.1f}% |")

    lines.extend(
        [
            "",
            "## Frequencias por eixo",
            "",
        ]
    )
    for col in ("psych_domains", "behavioral_domains", "physio_list"):
        c = _counter_for_col(df, col)
        lines.extend([f"### `{col}`", "", "| Categoria | Estudos | % do corpus |", "|---|---:|---:|"])
        for cat, cnt in sorted(c.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"| `{cat}` | {cnt} | {100 * cnt / n:.1f}% |")
        if not c:
            lines.append("| — | — | — |")
        ni = _n_items_per_study(df, col)
        lines.extend(
            [
                "",
                f"- Estudos com >=1 categoria: {int((ni > 0).sum())}",
                f"- Media de categorias por estudo (corpus): {float(ni.mean()):.2f}",
                (
                    f"- Media de categorias (apenas preenchidos): {float(ni[ni > 0].mean()):.2f}"
                    if int((ni > 0).sum())
                    else "- Media de categorias (apenas preenchidos): —"
                ),
                f"- Mediana de categorias por estudo (corpus): {float(np.median(ni)):.1f}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def write_cooccurrence_table(df: pd.DataFrame, md_path: Path) -> None:
    pairs = [
        ("psych_domains", "behavioral_domains"),
        ("psych_domains", "physio_list"),
        ("behavioral_domains", "physio_list"),
    ]
    lines = [
        "# Q3 Bloco 3 — Coocorrencias entre eixos",
        "",
        "Contagens de estudos em que a categoria A e a categoria B aparecem juntas no mesmo artigo.",
        "",
    ]
    for a, b in pairs:
        labs_a, labs_b, arr = _cooccurrence_matrix(df, a, b)
        flat = []
        for i, la in enumerate(labs_a):
            for j, lb in enumerate(labs_b):
                v = int(arr[i, j])
                if v > 0:
                    flat.append((la, lb, v))
        flat.sort(key=lambda x: (-x[2], x[0], x[1]))
        lines.extend([f"## `{a}` x `{b}`", "", "| Categoria A | Categoria B | Estudos |", "|---|---|---:|"])
        for la, lb, v in flat[:30]:
            lines.append(f"| `{la}` | `{lb}` | {v} |")
        if not flat:
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

    plot_bars_h(df, "psych_domains", OUT_FIG / "q3_b3_barras_psych_domains.png")
    plot_bars_h(df, "behavioral_domains", OUT_FIG / "q3_b3_barras_behavioral_domains.png")
    plot_bars_h(df, "physio_list", OUT_FIG / "q3_b3_barras_physio_list.png")

    plot_coverage_donut(df, "psych_domains", OUT_FIG / "q3_b3_rosca_cobertura_psych.png")
    plot_coverage_donut(df, "behavioral_domains", OUT_FIG / "q3_b3_rosca_cobertura_behavioral.png")
    plot_coverage_donut(df, "physio_list", OUT_FIG / "q3_b3_rosca_cobertura_physio.png")

    plot_heatmap(df, "psych_domains", "behavioral_domains", OUT_FIG / "q3_b3_heatmap_psych_x_behavioral.png")
    plot_heatmap(df, "psych_domains", "physio_list", OUT_FIG / "q3_b3_heatmap_psych_x_physio.png")
    plot_heatmap(df, "behavioral_domains", "physio_list", OUT_FIG / "q3_b3_heatmap_behavioral_x_physio.png")

    plot_n_axes(df, OUT_FIG / "q3_b3_barras_n_eixos_preenchidos.png")

    write_summary(df, OUT_TAB / "q3_b3_resumo.md")
    write_cooccurrence_table(df, OUT_TAB / "q3_b3_coocorrencias.md")

    print(f"Figuras: {OUT_FIG}")
    print(f"Tabelas: {OUT_TAB}")


if __name__ == "__main__":
    main()

