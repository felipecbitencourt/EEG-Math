# Revisão da normatização — Q3 Bloco 1 (processos matemáticos)

Fonte: `dados/tabela_normatizada.csv`. *N* = 88 estudos.

O campo **`math_processes`** reproduz o texto livre da coluna 6 da revisão. O campo **`math_processes_tags`** agrega etiquetas canónicas derivadas por palavras-chave (`MATH_PROCESS_KEYWORDS` em `scripts/normalize_eeg_math.py`).

## Cobertura das tags

| Métrica | Valor |
|---|---:|
| Estudos com pelo menos uma tag | 86 |
| Estudos sem tag detectada | 2 |

## Frequência por tag (nº de estudos)

| Tag | Estudos |
|---|---:|
| `mental_arithmetic` | 46 |
| `subtraction` | 28 |
| `addition` | 24 |
| `serial_subtraction` | 15 |
| `multiplication` | 11 |
| `problem_solving` | 6 |
| `puzzles_games` | 5 |
| `division` | 4 |
| `deductive_reasoning` | 4 |
| `arithmetic_mixed_ops` | 4 |
| `algebra` | 4 |
| `magnitude_comparison` | 4 |
| `executive_mixed_task` | 4 |
| `learning_demonstration` | 3 |
| `arithmetic_general` | 2 |
| `fractions_ratios` | 2 |
| `verification_task` | 2 |
| `geometry_spatial` | 2 |
| `functions_representations` | 2 |
| `word_problems` | 2 |
| `modulo` | 1 |
| `standardized_test` | 1 |
| `written_mode` | 1 |
| `inductive_reasoning` | 1 |
| `broad_math_battery` | 1 |

## Estudos sem tag (*n* = 2)

Útil para revisão manual ou extensão do dicionário `MATH_PROCESS_KEYWORDS`.

### Índice 85

- **Título:** The analysis of EEG coherence reflects middle childhood differences in mathematical achiev…

- **Col. 6 (processos):** -…


### Índice 86

- **Título:** Towards Predicting Attention and Workload During Math Problem Solving…

- **Col. 6 (processos):** Internal comparison to past mental state values/events…



## Referência de implementação

- `extract_math_process_tags_from_text` e `MATH_PROCESS_KEYWORDS` em `scripts/normalize_eeg_math.py`.
- Regenerar: `python3 scripts/normalize_eeg_math.py`.
