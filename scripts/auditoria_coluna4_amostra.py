#!/usr/bin/env python3
"""
Auditoria: texto da coluna 4 (amostra) × campos amostra_* normatizados.
Gera CSV com flags por linha e relatório Markdown em resultados/q2/tabelas/.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "dados" / "tabela_normatizada.csv"
OUT_DIR = REPO / "resultados" / "q2" / "tabelas"
COL4 = "4. Amostra (número de participantes, idade)"
YEAR_COL = "Ano da primeria publicação"


def _num(s) -> float | None:
    if pd.isna(s):
        return None
    v = pd.to_numeric(s, errors="coerce")
    return float(v) if pd.notna(v) else None


def texto_sugere_media_idade(sl: str) -> bool:
    return bool(
        re.search(
            r"mean\s+age|average\s+age|median\s+age|idade\s+média|média\s+de\s+idade|media\s+de\s+idade",
            sl,
            re.I,
        )
    )


def texto_sugere_faixa_etaria(sl: str) -> bool:
    pats = [
        r"between\s+\d{1,3}\s+and\s+\d{1,3}\s*(?:years?|yrs?|year-old)",
        r"ages?\s+\d{1,3}\s*(?:to|[-–])\s*\d{1,3}",
        r"\d{1,3}\s*[-–]\s*\d{1,3}\s*years?\s*(?:old|of\s+age)?",
        r"entre\s+\d{1,3}\s+e\s+\d{1,3}\s*anos?",
    ]
    return any(re.search(p, sl, re.I) for p in pats)


def texto_sugere_sexo_mf(sl: str) -> bool:
    return bool(
        re.search(
            r"\d+\s*(?:men|women|males?|females?|homens?|mulheres?)\b|%\s*(?:were|was)?\s*(?:female|male)",
            sl,
            re.I,
        )
    )


def texto_sugere_lateralidade(sl: str) -> bool:
    return bool(
        re.search(
            r"right[- ]hand|left[- ]hand|destro|canhoto|ambidextr|manual\s+dominan",
            sl,
            re.I,
        )
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    titulo_col = df.columns[0]

    rows = []
    alertas_nmf = []
    alertas_idade = []
    alertas_sexo = []
    alertas_lat = []

    for i in range(len(df)):
        raw = df.loc[i, COL4]
        sl = "" if pd.isna(raw) else str(raw)
        sl_l = sl.lower()

        n = _num(df.loc[i, "amostra_n_total"])
        m = _num(df.loc[i, "amostra_n_male"])
        f = _num(df.loc[i, "amostra_n_female"])
        amean = _num(df.loc[i, "amostra_age_mean"])
        amin = _num(df.loc[i, "amostra_age_min"])
        amax = _num(df.loc[i, "amostra_age_max"])
        hand = df.loc[i, "amostra_handedness"]
        if pd.isna(hand):
            hand = ""

        f_vazio = len(sl.strip()) < 8
        f_mean_txt_sem = texto_sugere_media_idade(sl_l) and amean is None
        f_faixa_txt_sem = texto_sugere_faixa_etaria(sl_l) and (amin is None or amax is None)
        f_nmf = (
            n is not None
            and m is not None
            and f is not None
            and abs(n - (m + f)) > 0.51
        )
        f_sexo_txt_sem = texto_sugere_sexo_mf(sl_l) and m is None and f is None
        f_lat_txt_sem = texto_sugere_lateralidade(sl_l) and hand in ("", "unspecified")
        f_so_um_sexo = (m is not None) ^ (f is not None)
        f_n_faltante = n is None

        doi = str(df.loc[i, "DOI"]) if "DOI" in df.columns else ""
        tit = str(df.loc[i, titulo_col]).replace("\n", " ")[:90]

        row = {
            "idx": i,
            "DOI": doi[:120],
            "Titulo_curto": tit,
            "n_total": n,
            "n_male": m,
            "n_female": f,
            "age_mean": amean,
            "age_min": amin,
            "age_max": amax,
            "handedness": hand,
            "flag_texto_muito_curto": f_vazio,
            "flag_mean_idade_texto_sem_campo": f_mean_txt_sem,
            "flag_faixa_idade_texto_sem_campo": f_faixa_txt_sem,
            "flag_N_diferente_soma_MF": f_nmf,
            "flag_sexo_texto_sem_M_nem_F": f_sexo_txt_sem,
            "flag_lateralidade_texto_so_unspecified": f_lat_txt_sem,
            "flag_so_um_sexo_codificado": f_so_um_sexo,
            "flag_n_total_ausente": f_n_faltante,
            "trecho_col4": sl.replace("\n", " ").strip()[:280],
        }
        rows.append(row)

        if f_nmf:
            alertas_nmf.append(row)
        if f_mean_txt_sem or f_faixa_txt_sem:
            alertas_idade.append(row)
        if f_sexo_txt_sem or f_so_um_sexo:
            alertas_sexo.append(row)
        if f_lat_txt_sem:
            alertas_lat.append(row)

    out_csv = OUT_DIR / "auditoria_coluna4_flags.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False, encoding="utf-8")

    # Markdown
    n_linhas = len(df)
    n_mean_miss = sum(1 for r in rows if r["flag_mean_idade_texto_sem_campo"])
    n_range_miss = sum(1 for r in rows if r["flag_faixa_idade_texto_sem_campo"])
    n_nmf = sum(1 for r in rows if r["flag_N_diferente_soma_MF"])
    n_sexo = sum(1 for r in rows if r["flag_sexo_texto_sem_M_nem_F"])
    n_lat = sum(1 for r in rows if r["flag_lateralidade_texto_so_unspecified"])
    n_um_sexo = sum(1 for r in rows if r["flag_so_um_sexo_codificado"])

    def bloco_lista(titulo: str, lista: list, max_items: int = 25) -> str:
        if not lista:
            return f"### {titulo}\n\n*(nenhum caso nesta categoria)*\n\n"
        lines = [f"### {titulo}\n", f"*{len(lista)} caso(s).*\n\n"]
        for r in lista[:max_items]:
            lines.append(f"- **idx {r['idx']}** | {r['DOI'][:70]}\n")
            lines.append(f"  - {r['trecho_col4'][:220]}{'…' if len(r['trecho_col4']) >= 220 else ''}\n")
            lines.append(
                f"  - norm: N={r['n_total']} M={r['n_male']} F={r['n_female']} "
                f"idade_m={r['age_mean']} [{r['age_min']}-{r['age_max']}] hand={r['handedness']}\n\n"
            )
        if len(lista) > max_items:
            lines.append(f"\n*… e mais {len(lista) - max_items} linhas no CSV.*\n\n")
        return "".join(lines)

    md = f"""# Auditoria — coluna 4 (amostra) × normatização `amostra_*`

Fonte: `{CSV_PATH.relative_to(REPO)}`. Total de registros: **{n_linhas}**.

## O que este relatório faz

Heurísticas **não** substituem leitura do PDF: servem para **priorizar** linhas em que o texto da coluna 4 sugere um dado (idade, sexo, lateralidade) ou em que **N ≠ M+F**, enquanto a normatização ficou vazia ou inconsistente.

## Resumo de flags

| Flag | Significado (heurístico) | Nº de linhas |
|------|---------------------------|-------------|
| `flag_N_diferente_soma_MF` | N, M e F preenchidos e \\|N − (M+F)\\| > 0,5 | **{n_nmf}** |
| `flag_mean_idade_texto_sem_campo` | Texto sugere média de idade, mas `amostra_age_mean` vazio | **{n_mean_miss}** |
| `flag_faixa_idade_texto_sem_campo` | Texto sugere faixa etária, mas min/max ausente | **{n_range_miss}** |
| `flag_sexo_texto_sem_M_nem_F` | Texto sugere contagens/% sexo, mas M e F vazios | **{n_sexo}** |
| `flag_so_um_sexo_codificado` | Só masculino **ou** só feminino preenchido | **{n_um_sexo}** |
| `flag_lateralidade_texto_so_unspecified` | Texto sugere lateralidade, mas campo = unspecified | **{n_lat}** |
| `flag_n_total_ausente` | `amostra_n_total` vazio | **{sum(1 for r in rows if r['flag_n_total_ausente'])}** |
| `flag_texto_muito_curto` | Coluna 4 com menos de 8 caracteres | **{sum(1 for r in rows if r['flag_texto_muito_curto'])}** |

## Arquivo para revisão linha a linha

- **`{out_csv.relative_to(REPO)}`** — todas as linhas, flags booleanas e trecho da coluna 4.

---

## Detalhes por tipo de alerta

{bloco_lista("N total ≠ soma M+F (revisar primeiro)", alertas_nmf)}
{bloco_lista("Idade: texto sugere média ou faixa, campo vazio", alertas_idade)}
{bloco_lista("Sexo: texto sugere M/F mas ambos vazios; ou só um sexo codificado", alertas_sexo)}
{bloco_lista("Lateralidade: texto sugere destro/canhoto mas normatizado unspecified", alertas_lat)}

## Próximos passos sugeridos

1. Corrigir prioritariamente os casos **N ≠ M+F** (interpretação de subgrupo vs total).
2. Para idade/sexo, usar o CSV para abrir o PDF só nas linhas com flag.
3. Ajustar `normalize_eeg_math.py` só depois de classificar *falso positivo* da heurística vs *falha real* do extrator.

"""
    out_md = OUT_DIR / "auditoria_coluna4_vs_normatizacao.md"
    out_md.write_text(md, encoding="utf-8")

    print(f"CSV:  {out_csv}")
    print(f"MD:   {out_md}")
    print(f"Flags N≠M+F: {n_nmf} | idade texto sem campo: {n_mean_miss + n_range_miss} | sexo: {n_sexo} | lat: {n_lat}")


if __name__ == "__main__":
    main()
