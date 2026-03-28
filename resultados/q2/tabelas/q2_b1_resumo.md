# Q2 Bloco 1 — Resumo quantitativo

Fonte: `dados/tabela_normatizada.csv`. Estudos (linhas): **88**.

| Métrica | Valor |
|---|---|
| Estudos com `amostra_n_total` | 88 |
| Média de N (DP) | 31.5 (25.9) |
| Mediana de N (IQR) | 24 (16 – 36) |
| Mín. – máx. N | 1 – 160 |
| Estudos com `amostra_age_mean` | 21 |
| Média das médias de idade (entre estudos com dado) | 21.33 |
| Mín. – máx. média de idade | 9.1 – 28.5 |
| Estudos com `amostra_age_min` e `amostra_age_max` | 18 |
| Estudos com `amostra_n_male` e `amostra_n_female` | 31 |
| Soma M / F (participantes, estudos com ambos) | 437 / 482 |
| % masculino (entre participantes codificados) | 47.6% |
| Estudos com `amostra_handedness` preenchida | 88 |
| Estudos com `amostra_n_excluded` | 2 |
| Soma de excluídos (onde informado) | 9 |

## Exploratório: ano × N (*n* pareado = estudos com ano e N > 0)

| Métrica | Valor |
|---|---|
| Pares (ano, N) | 88 |
| Pearson: ano × log₁₀(N) | 0.344 |
| Spearman (postos): ano × N | 0.460 |

## Lateralidade (contagem por estudo)

- **unspecified:** 67 (76.1%)
- **right:** 20 (22.7%)
- **left:** 1 (1.1%)
