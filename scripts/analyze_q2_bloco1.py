#!/usr/bin/env python3
"""Q2 Bloco 1: figuras e tabela-resumo a partir de dados/tabela_normatizada.csv."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_FIG = REPO / "resultados" / "q2" / "figuras"
OUT_TAB = REPO / "resultados" / "q2" / "tabelas"

YEAR_COL = "Ano da primeria publicação"

HAND_PT = {
    "right": "Destro",
    "left": "Canhoto",
    "unspecified": "Não especificado",
    "mixed": "Misto",
}


def _load() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, encoding="utf-8")


def _numeric_series(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce")


def plot_hist_n_total(df: pd.DataFrame, path: Path) -> None:
    """Histograma com eixo X em escala log (melhor para cauda à direita)."""
    n = _numeric_series(df, "amostra_n_total").dropna()
    n = n[n > 0]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if len(n) == 0:
        ax.text(0.5, 0.5, "Sem N total > 0", ha="center", va="center")
        ax.set_axis_off()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return
    lo, hi = float(n.min()), float(n.max())
    bins = np.logspace(np.log10(lo), np.log10(hi), min(18, max(8, int(len(n) ** 0.5) + 5)))
    ax.hist(n, bins=bins, color="#3d5a80", edgecolor="white", linewidth=0.6)
    med = float(n.median())
    ax.axvline(med, color="#ee6c4d", linestyle="--", linewidth=1.5, label=f"Mediana = {med:.0f}")
    ax.set_xscale("log")
    ax.set_xlabel("N total (participantes), escala log")
    ax.set_ylabel("Número de estudos (cada barra: estudos nessa faixa de N)")
    ax.set_title(f"Distribuição de amostra_n_total (k = {len(n)} estudos)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_violin_n_total(df: pd.DataFrame, path: Path) -> None:
    """Violino + pontos (cada estudo) para ver dispersão e outliers."""
    n = _numeric_series(df, "amostra_n_total").dropna().astype(float)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    if len(n) < 2:
        ax.text(0.5, 0.5, "Dados insuficientes para violino", ha="center", va="center")
        ax.set_axis_off()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return
    rng = np.random.default_rng(42)
    parts = ax.violinplot(
        [n.values],
        positions=[0],
        showmeans=False,
        showmedians=True,
        widths=0.55,
    )
    for b in parts["bodies"]:
        b.set_facecolor("#98c1d9")
        b.set_edgecolor("#3d5a80")
        b.set_alpha(0.55)
    for key in ("cbars", "cmins", "cmaxes", "cmedians"):
        if key in parts:
            parts[key].set_color("#3d5a80")
    jitter = rng.uniform(-0.28, 0.28, size=len(n))
    ax.scatter(jitter, n.values, alpha=0.55, s=32, c="#3d5a80", edgecolors="white", linewidths=0.35)
    ax.axhline(float(n.median()), color="#ee6c4d", linestyle="--", linewidth=1.2, label=f"Mediana = {n.median():.0f}")
    ax.set_xticks([0])
    ax.set_xticklabels([""])
    ax.set_ylabel("N total (participantes por estudo)")
    ax.set_title(f"amostra_n_total: violino + estudos individuais (k = {len(n)})")
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_handedness_bars_h(df: pd.DataFrame, path: Path) -> None:
    """Barras horizontais, rótulos em português (contagem por estudo)."""
    s = df["amostra_handedness"].fillna("unspecified").astype(str)
    vc = s.value_counts()
    order = ["right", "left", "mixed", "unspecified"]
    vc = vc.reindex([x for x in order if x in vc.index] + [x for x in vc.index if x not in order])
    pct = 100 * vc / vc.sum()
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    colors = {"right": "#3d5a80", "left": "#98c1d9", "unspecified": "#d8d8d8", "mixed": "#ee6c4d"}
    y = np.arange(len(vc))
    bar_cols = [colors.get(i, "#adb5bd") for i in vc.index]
    ax.barh(y, vc.values, color=bar_cols, height=0.62, edgecolor="white", linewidth=0.6)
    ax.set_yticks(y)
    labels_pt = [f"{HAND_PT.get(i, i)}\n({pct[i]:.1f}%)" for i in vc.index]
    ax.set_yticklabels(labels_pt, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Número de estudos")
    ax.set_title(f"Lateralidade relatada nos estudos (k = {len(df)})")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_handedness_pie(df: pd.DataFrame, path: Path) -> None:
    """Composição: cada fatia = fração dos estudos."""
    s = df["amostra_handedness"].fillna("unspecified").astype(str)
    vc = s.value_counts()
    order = ["right", "left", "mixed", "unspecified"]
    vc = vc.reindex([x for x in order if x in vc.index] + [x for x in vc.index if x not in order])
    colors = {"right": "#3d5a80", "left": "#98c1d9", "unspecified": "#d8d8d8", "mixed": "#ee6c4d"}
    bar_cols = [colors.get(i, "#adb5bd") for i in vc.index]
    labels = [HAND_PT.get(i, i) for i in vc.index]
    total = int(vc.sum())

    def _lab(pct: float) -> str:
        v = int(round(pct / 100.0 * total))
        return f"{pct:.1f}%\n(n = {v})"

    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    ax.pie(
        vc.values,
        labels=labels,
        autopct=_lab,
        colors=bar_cols,
        startangle=90,
        counterclock=False,
        wedgeprops={"linewidth": 1.0, "edgecolor": "white"},
        textprops={"fontsize": 10},
    )
    ax.set_title(f"Proporção de estudos por lateralidade (N = {total} estudos)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_gender_proportion_pie(df: pd.DataFrame, path: Path) -> None:
    """Rosca: participantes com M e F no mesmo estudo; centro com N e k."""
    m = _numeric_series(df, "amostra_n_male")
    f = _numeric_series(df, "amostra_n_female")
    mask = m.notna() & f.notna()
    m_sum = float(m[mask].sum())
    f_sum = float(f[mask].sum())
    total = m_sum + f_sum
    k = int(mask.sum())

    fig, ax = plt.subplots(figsize=(6.2, 6.2))
    if total <= 0:
        ax.text(0.5, 0.5, "Sem dados M/F pareados", ha="center", va="center")
        ax.set_axis_off()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return

    def _pct_label(pct: float) -> str:
        v = int(round(pct / 100.0 * total))
        return f"{pct:.1f}%\n(n = {v})"

    colors = ["#3d5a80", "#98c1d9"]
    _, texts, autotexts = ax.pie(
        [m_sum, f_sum],
        labels=["Masculino", "Feminino"],
        autopct=_pct_label,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops={"linewidth": 1.0, "edgecolor": "white", "width": 0.45},
        textprops={"fontsize": 11},
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight("bold")
    for t in texts:
        t.set_fontsize(11)

    ax.text(
        0,
        0,
        f"N = {int(total)}\n{k} estudos\n(M e F)",
        ha="center",
        va="center",
        fontsize=11,
        linespacing=1.25,
    )

    ax.set_title("Proporção de participantes por sexo (dados pareados)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_year_vs_n(df: pd.DataFrame, path: Path) -> None:
    y = _numeric_series(df, YEAR_COL)
    n = _numeric_series(df, "amostra_n_total")
    mask = y.notna() & n.notna() & (n > 0)
    yy = y[mask].to_numpy(dtype=float)
    nn = n[mask].to_numpy(dtype=float)
    rng = np.random.default_rng(43)
    nn_j = nn * (1.0 + rng.uniform(-0.04, 0.04, size=len(nn)))
    nn_j = np.maximum(nn_j, 0.8)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.scatter(yy, nn_j, alpha=0.55, c="#3d5a80", edgecolors="white", linewidths=0.4, s=38)
    if len(yy) >= 3 and np.nanstd(yy) > 0 and np.nanstd(np.log10(nn)) > 0:
        log_n = np.log10(np.maximum(nn, 1.0))
        coef = np.polyfit(yy, log_n, 1)
        xs = np.linspace(np.nanmin(yy), np.nanmax(yy), 80)
        ax.plot(xs, 10 ** np.poly1d(coef)(xs), color="#ee6c4d", linestyle="--", linewidth=1.6, label="Tendência (OLS em log₁₀ N)")
        ax.legend(frameon=False, loc="upper left")
    ax.set_yscale("log")
    ax.set_xlabel("Ano da primeira publicação")
    ax.set_ylabel("N total (escala log)")
    ax.set_title(f"Ano × tamanho amostral (k = {len(yy)}; jitter leve no N)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_summary(df: pd.DataFrame, md_path: Path, csv_path: Path) -> None:
    nrows = len(df)
    ntot = _numeric_series(df, "amostra_n_total")
    age_m = _numeric_series(df, "amostra_age_mean")
    age_min = _numeric_series(df, "amostra_age_min")
    age_max = _numeric_series(df, "amostra_age_max")
    m = _numeric_series(df, "amostra_n_male")
    f = _numeric_series(df, "amostra_n_female")
    excl = _numeric_series(df, "amostra_n_excluded") if "amostra_n_excluded" in df.columns else pd.Series(dtype=float)

    k_ntot = int(ntot.notna().sum())
    k_age_m = int(age_m.notna().sum())
    k_age_minmax = int((age_min.notna() & age_max.notna()).sum())
    k_mf = int((m.notna() & f.notna()).sum())
    m_sum = float(m[m.notna() & f.notna()].sum())
    f_sum = float(f[m.notna() & f.notna()].sum())
    total_g = m_sum + f_sum
    pct_m = 100 * m_sum / total_g if total_g else np.nan

    lines = [
        "# Q2 Bloco 1 — Resumo quantitativo",
        "",
        f"Fonte: `dados/tabela_normatizada.csv`. Estudos (linhas): **{nrows}**.",
        "",
        "| Métrica | Valor |",
        "|---|---|",
        f"| Estudos com `amostra_n_total` | {k_ntot} |",
    ]
    if k_ntot:
        nn = ntot.dropna()
        lines.append(f"| Média de N (DP) | {nn.mean():.1f} ({nn.std():.1f}) |")
        lines.append(f"| Mediana de N (IQR) | {nn.median():.0f} ({nn.quantile(0.25):.0f} – {nn.quantile(0.75):.0f}) |")
        lines.append(f"| Mín. – máx. N | {nn.min():.0f} – {nn.max():.0f} |")
    lines.append(f"| Estudos com `amostra_age_mean` | {k_age_m} |")
    if k_age_m:
        am = age_m.dropna()
        lines.append(f"| Média das médias de idade (entre estudos com dado) | {am.mean():.2f} |")
        lines.append(f"| Mín. – máx. média de idade | {am.min():.1f} – {am.max():.1f} |")
    lines.append(f"| Estudos com `amostra_age_min` e `amostra_age_max` | {k_age_minmax} |")
    lines.append(f"| Estudos com `amostra_n_male` e `amostra_n_female` | {k_mf} |")
    if k_mf and total_g:
        lines.append(f"| Soma M / F (participantes, estudos com ambos) | {int(m_sum)} / {int(f_sum)} |")
        lines.append(f"| % masculino (entre participantes codificados) | {pct_m:.1f}% |")
    lines.append(f"| Estudos com `amostra_handedness` preenchida | {int(df['amostra_handedness'].notna().sum())} |")
    if len(excl):
        k_ex = int(excl.notna().sum())
        lines.append(f"| Estudos com `amostra_n_excluded` | {k_ex} |")
        if k_ex:
            lines.append(f"| Soma de excluídos (onde informado) | {excl.dropna().sum():.0f} |")

    ynum = _numeric_series(df, YEAR_COL)
    mask_c = ynum.notna() & ntot.notna() & (ntot > 0)
    k_pairs = int(mask_c.sum())
    if k_pairs >= 3:
        yy = ynum[mask_c].to_numpy(dtype=float)
        nn_c = ntot[mask_c].to_numpy(dtype=float)
        r_log = float(np.corrcoef(yy, np.log10(nn_c))[0, 1])
        yr = pd.Series(yy).rank(method="average").to_numpy()
        nr = pd.Series(nn_c).rank(method="average").to_numpy()
        r_sp = float(np.corrcoef(yr, nr)[0, 1])
        lines.extend(
            [
                "",
                "## Exploratório: ano × N (*n* pareado = estudos com ano e N > 0)",
                "",
                "| Métrica | Valor |",
                "|---|---|",
                f"| Pares (ano, N) | {k_pairs} |",
                f"| Pearson: ano × log₁₀(N) | {r_log:.3f} |",
                f"| Spearman (postos): ano × N | {r_sp:.3f} |",
            ]
        )

    lines.extend(["", "## Lateralidade (contagem por estudo)", ""])
    vc = df["amostra_handedness"].fillna("(vazio)").astype(str).value_counts()
    for lab, c in vc.items():
        lines.append(f"- **{lab}:** {int(c)} ({100 * c / nrows:.1f}%)")
    lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")

    one_row = {
        "n_estudos": nrows,
        "k_n_total": k_ntot,
        "median_n_total": float(ntot.median()) if k_ntot else np.nan,
        "k_age_mean": k_age_m,
        "k_male_female": k_mf,
        "sum_male": m_sum if k_mf else np.nan,
        "sum_female": f_sum if k_mf else np.nan,
    }
    pd.DataFrame([one_row]).to_csv(csv_path, index=False)


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
    plot_hist_n_total(df, OUT_FIG / "q2_b1_hist_n_total.png")
    plot_violin_n_total(df, OUT_FIG / "q2_b1_violin_n_total.png")
    plot_handedness_bars_h(df, OUT_FIG / "q2_b1_barras_handedness.png")
    plot_handedness_pie(df, OUT_FIG / "q2_b1_pizza_handedness.png")
    plot_gender_proportion_pie(df, OUT_FIG / "q2_b1_sexo_participantes.png")
    plot_year_vs_n(df, OUT_FIG / "q2_b1_dispersao_ano_n.png")
    write_summary(df, OUT_TAB / "q2_b1_resumo.md", OUT_TAB / "q2_b1_resumo.csv")

    print(f"Figuras: {OUT_FIG}")
    print(f"Tabelas: {OUT_TAB}")


if __name__ == "__main__":
    main()
