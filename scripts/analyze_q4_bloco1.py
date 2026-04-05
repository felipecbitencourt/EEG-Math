#!/usr/bin/env python3
"""Q4 Bloco 1: regioes cerebrais e cruzamento com tarefa matematica."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_FIG = REPO / "resultados" / "q4" / "figuras"
OUT_TAB = REPO / "resultados" / "q4" / "tabelas"

REGION_PT = {
    "Frontal": "Frontal",
    "Parietal": "Parietal",
    "Temporal": "Temporal",
    "Occipital": "Occipital",
    "Central": "Central",
    "Midline": "Linha media",
}

SCOPE_PT = {
    "full_scalp": "Full scalp",
    "regional": "Regional",
    "specific_sites": "Sitios especificos",
    "": "Vazio",
}

TASK_PT = {
    "mental_arithmetic": "Calculo mental",
    "subtraction": "Subtracao",
    "addition": "Adicao",
    "multiplication": "Multiplicacao",
    "division": "Divisao",
    "problem_solving": "Resolucao de problemas",
    "deductive_reasoning": "Raciocinio dedutivo",
    "puzzles_games": "Puzzles / jogos",
}


def _load() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, encoding="utf-8")


def _split_csv(val) -> list[str]:
    if pd.isna(val):
        return []
    s = str(val).strip()
    if not s or s in ("-", "—", "nan"):
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def _split_tags(val) -> list[str]:
    if pd.isna(val):
        return []
    s = str(val).strip()
    if not s or s in ("-", "—", "nan"):
        return []
    return [x.strip() for x in s.split(";") if x.strip()]


def _count_items(df: pd.DataFrame, col: str, splitter) -> Counter[str]:
    c: Counter[str] = Counter()
    for v in df[col]:
        for it in splitter(v):
            c[it] += 1
    return c


def plot_regions_bars(df: pd.DataFrame, out_path: Path) -> None:
    c = _count_items(df, "eeg_regions", _split_csv)
    items = sorted(c.items(), key=lambda x: x[1])
    labs, vals = zip(*items) if items else ([], [])
    n = len(df)
    fig, ax = plt.subplots(figsize=(8.8, max(4.0, 0.42 * len(labs) + 1.6)))
    if not items:
        ax.text(0.5, 0.5, "Sem regioes detectadas", ha="center", va="center")
        ax.set_axis_off()
    else:
        y = np.arange(len(labs))
        ax.barh(y, vals, color="#3d5a80", height=0.56, edgecolor="white", linewidth=0.6)
        ax.set_yticks(y)
        ax.set_yticklabels([f"{REGION_PT.get(k, k)} ({100*v/n:.1f}%)" for k, v in zip(labs, vals)], fontsize=10)
        ax.invert_yaxis()
        ax.set_xlabel("Numero de estudos")
        ax.set_title(f"Frequencia de regioes EEG analisadas (N = {n})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_scope_bars(df: pd.DataFrame, out_path: Path) -> None:
    s = df["eeg_scope"].fillna("").astype(str).str.strip()
    vc = s.value_counts().sort_values(ascending=False)
    labs = [SCOPE_PT.get(k, k if k else "Vazio") for k in vc.index]
    vals = vc.values
    n = len(df)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    x = np.arange(len(labs))
    bars = ax.bar(x, vals, color="#4f6d7a", width=0.62, edgecolor="white", linewidth=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(labs, fontsize=10)
    ax.set_ylabel("Numero de estudos")
    ax.set_title(f"Distribuicao do escopo espacial (eeg_scope; N = {n})")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.4, f"{int(v)}\n({100*v/n:.1f}%)", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_hist_n_regions(df: pd.DataFrame, out_path: Path) -> None:
    arr = np.array([len(_split_csv(v)) for v in df["eeg_regions"]], dtype=int)
    mx = int(arr.max()) if len(arr) else 0
    bins = np.arange(-0.5, max(mx, 1) + 1.5, 1.0)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.hist(arr, bins=bins, color="#98c1d9", edgecolor="white", linewidth=0.8)
    ax.set_xticks(range(0, mx + 1))
    ax.set_xlabel("Numero de regioes por estudo")
    ax.set_ylabel("Numero de estudos")
    ax.set_title(f"Riqueza regional por estudo (mediana = {np.median(arr):.0f})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_hist_n_sites(df: pd.DataFrame, out_path: Path) -> None:
    arr = np.array([len(_split_csv(v)) for v in df["eeg_specific_sites"]], dtype=int)
    arr = arr[arr > 0]
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    if len(arr) == 0:
        ax.text(0.5, 0.5, "Sem sitios especificos detectados", ha="center", va="center")
        ax.set_axis_off()
    else:
        mx = int(arr.max())
        bins = np.arange(0.5, mx + 1.5, 1.0)
        ax.hist(arr, bins=bins, color="#c2dfe3", edgecolor="white", linewidth=0.8)
        ax.set_xticks(range(1, mx + 1))
        ax.set_xlabel("Numero de sitios por estudo (somente estudos com >0)")
        ax.set_ylabel("Numero de estudos")
        ax.set_title(f"Granularidade de sitios especificos (mediana = {np.median(arr):.0f})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_top_sites(df: pd.DataFrame, out_path: Path, top_k: int = 15) -> None:
    c = _count_items(df, "eeg_specific_sites", _split_csv)
    items = sorted(c.items(), key=lambda x: (-x[1], x[0]))[:top_k]
    fig, ax = plt.subplots(figsize=(8.6, max(4.0, 0.38 * max(len(items), 1) + 1.6)))
    if not items:
        ax.text(0.5, 0.5, "Sem sitios especificos detectados", ha="center", va="center")
        ax.set_axis_off()
    else:
        labs = [k for k, _ in items][::-1]
        vals = [v for _, v in items][::-1]
        ax.barh(np.arange(len(labs)), vals, color="#3d5a80", edgecolor="white", linewidth=0.6)
        ax.set_yticks(np.arange(len(labs)))
        ax.set_yticklabels(labs, fontsize=10)
        ax.set_xlabel("Numero de estudos")
        ax.set_title(f"Top-{top_k} sitios EEG mais reportados")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _top_tasks(df: pd.DataFrame, min_n: int = 5) -> list[str]:
    c = _count_items(df, "math_processes_tags", _split_tags)
    return [k for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0])) if v >= min_n]


def _task_region_matrix(df: pd.DataFrame, tasks: list[str], regions: list[str]) -> np.ndarray:
    m = np.zeros((len(tasks), len(regions)), dtype=int)
    idx_t = {k: i for i, k in enumerate(tasks)}
    idx_r = {k: i for i, k in enumerate(regions)}
    for _, row in df.iterrows():
        ts = set(_split_tags(row["math_processes_tags"]))
        rs = set(_split_csv(row["eeg_regions"]))
        for t in ts:
            if t not in idx_t:
                continue
            for r in rs:
                if r in idx_r:
                    m[idx_t[t], idx_r[r]] += 1
    return m


def plot_task_region_heatmap(df: pd.DataFrame, out_path: Path) -> tuple[list[str], list[str], np.ndarray]:
    tasks = _top_tasks(df, min_n=5)
    region_counts = _count_items(df, "eeg_regions", _split_csv)
    regions = [k for k, _ in sorted(region_counts.items(), key=lambda x: (-x[1], x[0]))]
    mat = _task_region_matrix(df, tasks, regions)
    if mat.size == 0:
        fig, ax = plt.subplots(figsize=(6.5, 3))
        ax.text(0.5, 0.5, "Sem dados para cruzamento tarefa x regiao", ha="center", va="center")
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        return tasks, regions, mat

    # normalizacao por linha para leitura relativa entre tarefas
    row_sums = mat.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        mat_norm = np.where(row_sums > 0, mat / row_sums, 0.0)

    fig_w = max(8.0, 1.4 + 0.95 * len(regions))
    fig_h = max(4.8, 1.6 + 0.62 * len(tasks))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    im = ax.imshow(mat_norm, cmap="Blues", aspect="auto", vmin=0, vmax=max(0.01, float(mat_norm.max())))
    ax.set_xticks(np.arange(len(regions)))
    ax.set_yticks(np.arange(len(tasks)))
    ax.set_xticklabels([REGION_PT.get(r, r) for r in regions], rotation=30, ha="right", fontsize=9)
    ax.set_yticklabels([TASK_PT.get(t, t.replace("_", " ")) for t in tasks], fontsize=9)
    ax.set_title("Cruzamento tarefa matematica x regiao EEG (normalizado por tarefa)")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] > 0:
                ax.text(j, i, str(int(mat[i, j])), ha="center", va="center", fontsize=8, color="#1b263b")
    cbar = fig.colorbar(im, ax=ax, shrink=0.82)
    cbar.set_label("Proporcao dentro de cada tarefa", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return tasks, regions, mat


def plot_scope_by_task(df: pd.DataFrame, out_path: Path) -> None:
    tasks = _top_tasks(df, min_n=8)[:6]
    scopes = ["full_scalp", "regional", "specific_sites", ""]
    if not tasks:
        fig, ax = plt.subplots(figsize=(6.5, 3))
        ax.text(0.5, 0.5, "Sem tarefas com n minimo para comparar escopo", ha="center", va="center")
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        return

    rows = []
    for t in tasks:
        has_t = df["math_processes_tags"].apply(lambda x: t in set(_split_tags(x)))
        sub = df.loc[has_t, "eeg_scope"].fillna("").astype(str).str.strip()
        vc = sub.value_counts()
        n = int(has_t.sum())
        row = {"task": t, "n": n}
        for s in scopes:
            row[s] = int(vc.get(s, 0))
        rows.append(row)
    p = pd.DataFrame(rows)

    x = np.arange(len(tasks))
    width = 0.18
    fig, ax = plt.subplots(figsize=(10.0, 4.8))
    for i, s in enumerate(scopes):
        vals = p[s].to_numpy()
        pct = np.where(p["n"].to_numpy() > 0, 100 * vals / p["n"].to_numpy(), 0.0)
        ax.bar(x + (i - 1.5) * width, pct, width=width, label=SCOPE_PT.get(s, s if s else "Vazio"))
    ax.set_xticks(x)
    ax.set_xticklabels([TASK_PT.get(t, t.replace("_", " ")) for t in tasks], rotation=15, ha="right")
    ax.set_ylabel("% dentro da tarefa")
    ax.set_title("Perfil de eeg_scope por tarefa matematica (top tarefas)")
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def write_summary(df: pd.DataFrame, out_path: Path) -> None:
    n = len(df)
    col12_nonempty = (df["eeg_regions"].fillna("").astype(str).str.strip() != "").sum()
    n_regions = np.array([len(_split_csv(v)) for v in df["eeg_regions"]], dtype=int)
    n_sites = np.array([len(_split_csv(v)) for v in df["eeg_specific_sites"]], dtype=int)
    scope_vc = df["eeg_scope"].fillna("").astype(str).str.strip().value_counts()
    reg_counts = _count_items(df, "eeg_regions", _split_csv)

    lines = [
        "# Q4 Bloco 1 — Resumo quantitativo (regioes cerebrais)",
        "",
        f"Fonte: `dados/tabela_normatizada.csv`. Estudos: **{n}**.",
        "",
        "| Indicador | Valor |",
        "|---|---:|",
        f"| Estudos com `eeg_regions` preenchido | {int((n_regions > 0).sum())} ({100*(n_regions>0).mean():.1f}%) |",
        f"| Estudos com `eeg_specific_sites` preenchido | {int((n_sites > 0).sum())} ({100*(n_sites>0).mean():.1f}%) |",
        f"| Estudos com `eeg_scope` preenchido | {int((df['eeg_scope'].fillna('').astype(str).str.strip()!='').sum())} ({100*(df['eeg_scope'].fillna('').astype(str).str.strip()!='').mean():.1f}%) |",
        f"| Mediana de n de regioes por estudo | {float(np.median(n_regions)):.1f} |",
        f"| Mediana de n de sitios por estudo (todos) | {float(np.median(n_sites)):.1f} |",
        (
            f"| Mediana de n de sitios (apenas >0) | {float(np.median(n_sites[n_sites>0])):.1f} |"
            if int((n_sites > 0).sum())
            else "| Mediana de n de sitios (apenas >0) | — |"
        ),
        "",
        "## Frequencia por regiao",
        "",
        "| Regiao | Estudos | % do corpus |",
        "|---|---:|---:|",
    ]
    for r, v in sorted(reg_counts.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| `{r}` | {v} | {100*v/n:.1f}% |")

    lines.extend(["", "## Distribuicao de eeg_scope", "", "| eeg_scope | Estudos | % |", "|---|---:|---:|"])
    for s, v in scope_vc.items():
        key = s if s else "(vazio)"
        lines.append(f"| `{key}` | {int(v)} | {100*v/n:.1f}% |")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_task_region_table(tasks: list[str], regions: list[str], mat: np.ndarray, out_path: Path) -> None:
    lines = [
        "# Q4 Bloco 1 — Cruzamento tarefa x regiao",
        "",
        "Contagens brutas de coocorrencia estudo->(tag de tarefa, regiao).",
        "",
        "| Tarefa (`math_processes_tags`) | Regiao (`eeg_regions`) | Estudos |",
        "|---|---|---:|",
    ]
    if mat.size == 0:
        lines.append("| — | — | — |")
    else:
        rows = []
        for i, t in enumerate(tasks):
            for j, r in enumerate(regions):
                v = int(mat[i, j])
                if v > 0:
                    rows.append((t, r, v))
        rows.sort(key=lambda x: (-x[2], x[0], x[1]))
        for t, r, v in rows[:120]:
            lines.append(f"| `{t}` | `{r}` | {v} |")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    plt.rcParams.update({"font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11, "figure.facecolor": "white"})
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    OUT_TAB.mkdir(parents=True, exist_ok=True)
    df = _load()

    plot_regions_bars(df, OUT_FIG / "q4_b1_barras_eeg_regions.png")
    plot_scope_bars(df, OUT_FIG / "q4_b1_barras_eeg_scope.png")
    plot_hist_n_regions(df, OUT_FIG / "q4_b1_hist_n_regions.png")
    plot_hist_n_sites(df, OUT_FIG / "q4_b1_hist_n_sites.png")
    plot_top_sites(df, OUT_FIG / "q4_b1_barras_top_sites.png", top_k=15)
    tasks, regions, mat = plot_task_region_heatmap(df, OUT_FIG / "q4_b1_heatmap_tarefa_x_regiao.png")
    plot_scope_by_task(df, OUT_FIG / "q4_b1_barras_scope_por_tarefa.png")

    write_summary(df, OUT_TAB / "q4_b1_resumo.md")
    write_task_region_table(tasks, regions, mat, OUT_TAB / "q4_b1_tarefa_x_regiao.md")

    print(f"Figuras: {OUT_FIG}")
    print(f"Tabelas: {OUT_TAB}")


if __name__ == "__main__":
    main()

