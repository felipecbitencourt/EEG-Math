#!/usr/bin/env python3
"""Q4 Bloco 2: faixas de frequencia (coluna 16) e cruzamento com tarefa matematica."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_FIG = REPO / "resultados" / "q4" / "figuras"
OUT_TAB = REPO / "resultados" / "q4" / "tabelas"

BAND_MAP = {
    "delta": [r"\bdelta\b", r"\bδ\b"],
    "theta": [r"\btheta\b", r"\bteta\b", r"\bθ\b"],
    "alpha": [r"\balpha\b", r"\balfa\b", r"\bα\b"],
    "beta": [r"\bbeta\b", r"\bβ\b"],
    "gamma": [r"\bgamma\b", r"\bgama\b", r"\bγ\b"],
}

BAND_PT = {
    "delta": "Delta",
    "theta": "Teta",
    "alpha": "Alfa",
    "beta": "Beta",
    "gamma": "Gama",
    "wideband": "Banda larga (filtro amplo)",
}

TASK_PT = {
    "mental_arithmetic": "Calculo mental",
    "subtraction": "Subtracao",
    "addition": "Adicao",
    "multiplication": "Multiplicacao",
    "serial_subtraction": "Subtracao serial",
    "problem_solving": "Resolucao de problemas",
    "puzzles_games": "Puzzles / jogos",
}


def _freq_col(df: pd.DataFrame) -> str:
    cols = [c for c in df.columns if "16." in str(c)]
    if not cols:
        raise ValueError("Coluna 16 (faixas de frequencia) nao encontrada na tabela.")
    return cols[0]


def _load() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, encoding="utf-8")


def _split_tags(val) -> list[str]:
    if pd.isna(val):
        return []
    s = str(val).strip()
    if not s or s in ("-", "—", "nan"):
        return []
    return [x.strip() for x in s.split(";") if x.strip()]


def _should_skip_canonical_frequency(text: str) -> bool:
    """Evita false positives quando bandas aparecem so como exemplo negativo."""
    if not text:
        return True
    t = str(text).lower()
    if re.search(
        r"did\s+not.*explicitly.*analy[sz]e.*(canonical\s+)?(frequency\s+)?bands?",
        t,
        re.DOTALL,
    ):
        return True
    if re.search(r"nao\s+analisa(ram|mos)?\s+.*banda", t):
        return True
    if re.search(r"não\s+analisa(ram|mos)?\s+.*banda", t):
        return True
    return False


def _has_wideband_filter(text: str) -> bool:
    t = str(text).lower()
    if re.search(r"from\s+0[\.,]5\s+to\s+4\d", t):
        return True
    if re.search(r"from\s+0[\.,]5\s*[-–]\s*4\d", t):
        return True
    if "band-pass filtered from 0.5" in t or "band-pass filtered from 0,5" in t:
        return True
    if re.search(r"filtered\s+from\s+0[\.,]5\s+to\s+45", t):
        return True
    return False


def detect_bands(text) -> list[str]:
    if pd.isna(text):
        return []
    s = str(text).strip()
    if not s or s in ("-", "—", "nan", "(revisar)"):
        return []
    if _should_skip_canonical_frequency(s):
        return []
    tl = s.lower()
    found: list[str] = []
    for canonical, patterns in BAND_MAP.items():
        if any(re.search(p, tl, re.I) for p in patterns):
            found.append(canonical)
    if _has_wideband_filter(s) and not found:
        found.append("wideband")
    return sorted(set(found))


def _count_bands_series(df: pd.DataFrame, col: str) -> Counter[str]:
    c: Counter[str] = Counter()
    for v in df[col]:
        for b in detect_bands(v):
            c[b] += 1
    return c


def plot_bands_bars(df: pd.DataFrame, col: str, out_path: Path) -> None:
    bc = _count_bands_series(df, col)
    items = sorted(bc.items(), key=lambda x: x[1])
    labs, vals = zip(*items) if items else ([], [])
    n = len(df)
    fig, ax = plt.subplots(figsize=(8.2, max(3.8, 0.42 * len(labs) + 1.4)))
    if not items:
        ax.text(0.5, 0.5, "Nenhuma banda detectada", ha="center", va="center")
        ax.set_axis_off()
    else:
        y = np.arange(len(labs))
        ax.barh(y, vals, color="#3d5a80", height=0.55, edgecolor="white", linewidth=0.6)
        ax.set_yticks(y)
        ax.set_yticklabels([f"{BAND_PT.get(k, k)} ({100*v/n:.1f}%)" for k, v in zip(labs, vals)], fontsize=10)
        ax.invert_yaxis()
        ax.set_xlabel("Numero de estudos")
        ax.set_title(f"Mencoes a bandas de frequencia na coluna 16 (N = {n})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_hist_n_bands(df: pd.DataFrame, col: str, out_path: Path) -> None:
    arr = np.array([len(detect_bands(v)) for v in df[col]], dtype=int)
    mx = int(arr.max()) if len(arr) else 0
    bins = np.arange(-0.5, max(mx, 1) + 1.5, 1.0)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.hist(arr, bins=bins, color="#98c1d9", edgecolor="white", linewidth=0.8)
    ax.set_xticks(range(0, mx + 1))
    ax.set_xlabel("Numero de bandas canonicas detectadas por estudo")
    ax.set_ylabel("Numero de estudos")
    ax.set_title(f"Riqueza de bandas por estudo (mediana = {np.median(arr):.0f})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _top_tasks(df: pd.DataFrame, min_n: int = 5) -> list[str]:
    c: Counter[str] = Counter()
    for v in df["math_processes_tags"]:
        for t in _split_tags(v):
            c[t] += 1
    return [k for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0])) if v >= min_n]


def _task_band_matrix(df: pd.DataFrame, col: str, tasks: list[str], bands: list[str]) -> np.ndarray:
    m = np.zeros((len(tasks), len(bands)), dtype=int)
    it = {k: i for i, k in enumerate(tasks)}
    ib = {k: i for i, k in enumerate(bands)}
    for _, row in df.iterrows():
        ts = set(_split_tags(row["math_processes_tags"]))
        bs = set(detect_bands(row[col]))
        for t in ts:
            if t not in it:
                continue
            for b in bs:
                if b in ib:
                    m[it[t], ib[b]] += 1
    return m


def plot_task_band_heatmap(df: pd.DataFrame, col: str, out_path: Path) -> tuple[list[str], list[str], np.ndarray]:
    tasks = _top_tasks(df, min_n=5)
    bc = _count_bands_series(df, col)
    band_order = ["delta", "theta", "alpha", "beta", "gamma", "wideband"]
    bands = [b for b in band_order if b in bc]
    mat = _task_band_matrix(df, col, tasks, bands)
    if mat.size == 0:
        fig, ax = plt.subplots(figsize=(6.5, 3))
        ax.text(0.5, 0.5, "Sem dados para heatmap tarefa x banda", ha="center", va="center")
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        return tasks, bands, mat
    row_sums = mat.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        mat_norm = np.where(row_sums > 0, mat / row_sums, 0.0)
    fig, ax = plt.subplots(figsize=(max(7.5, 1.1 + 0.9 * len(bands)), max(4.8, 1.5 + 0.55 * len(tasks))))
    im = ax.imshow(mat_norm, cmap="Blues", aspect="auto", vmin=0, vmax=max(0.01, float(mat_norm.max())))
    ax.set_xticks(np.arange(len(bands)))
    ax.set_yticks(np.arange(len(tasks)))
    ax.set_xticklabels([BAND_PT.get(b, b) for b in bands], rotation=20, ha="right", fontsize=9)
    ax.set_yticklabels([TASK_PT.get(t, t.replace("_", " ")) for t in tasks], fontsize=9)
    ax.set_title("Cruzamento tarefa matematica x banda (normalizado por tarefa)")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] > 0:
                ax.text(j, i, str(int(mat[i, j])), ha="center", va="center", fontsize=8, color="#1b263b")
    cbar = fig.colorbar(im, ax=ax, shrink=0.82)
    cbar.set_label("Proporcao dentro de cada tarefa", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return tasks, bands, mat


def write_summary(df: pd.DataFrame, col: str, out_path: Path) -> None:
    n = len(df)
    nonempty = df[col].fillna("").astype(str).str.strip()
    elig = ~nonempty.isin(["", "-", "—", "nan", "(revisar)"])
    detected_any = np.array([len(detect_bands(v)) > 0 for v in df[col]], dtype=bool)
    bc = _count_bands_series(df, col)
    nb = np.array([len(detect_bands(v)) for v in df[col]], dtype=int)

    lines = [
        "# Q4 Bloco 2 — Resumo quantitativo (faixas de frequencia)",
        "",
        f"Fonte: coluna 16 em `dados/tabela_normatizada.csv`. Estudos: **{n}**.",
        "",
        "> **Nota metodologica:** bandas foram inferidas por padroes textuais (delta, theta, alpha, beta, gamma; mais `wideband` em alguns filtros largos). Textos que negam analise de bandas canonicas sao ignorados para contagens.",
        "",
        "| Indicador | Valor |",
        "|---|---:|",
        f"| Celulas da coluna 16 nao vazias (excl. marcador «(revisar)») | {int(elig.sum())} |",
        f"| Estudos com >=1 banda detectada | {int(detected_any.sum())} ({100*detected_any.mean():.1f}%) |",
        f"| Mediana de bandas por estudo (corpus) | {float(np.median(nb)):.1f} |",
        f"| Maximo de bandas num estudo | {int(nb.max())} |",
        "",
        "## Frequencia por banda",
        "",
        "| Banda | Estudos | % do corpus |",
        "|---|---:|---:|",
    ]
    for b, v in sorted(bc.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| `{b}` | {v} | {100*v/n:.1f}% |")
    if not bc:
        lines.append("| — | — | — |")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_task_band_table(tasks: list[str], bands: list[str], mat: np.ndarray, out_path: Path) -> None:
    lines = [
        "# Q4 Bloco 2 — Cruzamento tarefa x banda",
        "",
        "| Tarefa | Banda | Estudos |",
        "|---|---|---:|",
    ]
    if mat.size == 0:
        lines.append("| — | — | — |")
    else:
        rows = []
        for i, t in enumerate(tasks):
            for j, b in enumerate(bands):
                v = int(mat[i, j])
                if v > 0:
                    rows.append((t, b, v))
        rows.sort(key=lambda x: (-x[2], x[0], x[1]))
        for t, b, v in rows[:100]:
            lines.append(f"| `{t}` | `{b}` | {v} |")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    plt.rcParams.update({"font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11, "figure.facecolor": "white"})
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    OUT_TAB.mkdir(parents=True, exist_ok=True)

    df = _load()
    col = _freq_col(df)

    plot_bands_bars(df, col, OUT_FIG / "q4_b2_barras_bandas.png")
    plot_hist_n_bands(df, col, OUT_FIG / "q4_b2_hist_n_bandas.png")
    tasks, bands, mat = plot_task_band_heatmap(df, col, OUT_FIG / "q4_b2_heatmap_tarefa_x_banda.png")

    write_summary(df, col, OUT_TAB / "q4_b2_resumo.md")
    write_task_band_table(tasks, bands, mat, OUT_TAB / "q4_b2_tarefa_x_banda.md")

    print(f"Figuras: {OUT_FIG}")
    print(f"Tabelas: {OUT_TAB}")


if __name__ == "__main__":
    main()
