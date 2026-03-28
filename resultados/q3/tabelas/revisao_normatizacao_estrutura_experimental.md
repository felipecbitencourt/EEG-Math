# Revisão da normatização — Q3 Bloco 2 (estrutura experimental)

Fonte: `dados/tabela_normatizada.csv`. *N* = 88 estudos.

Campos derivados da **coluna 7** (*«Durante a tarefa, a tarefa matemática é comparada a quê?»*) por `extract_comparison_from_text` em `scripts/normalize_eeg_math.py`.

- **`comparison_type`:** categoria principal da comparação.
- **`comparison_detail`:** subtipo ocular quando aplicável (`eyes_closed`, `eyes_open`, `eyes_open_and_closed`).
- **`has_control_task`:** `False` só para `within_task_only` ou `unspecified` (repouso conta como referência externa, `True`).

## `comparison_type`

| Código | Estudos | % | Rótulo (PT) |
|---|---:|---:|---|
| `resting_state` | 42 | 47.7% | Repouso / baseline de repouso |
| `unspecified` | 11 | 12.5% | Não especificado / texto vazio |
| `baseline_epoch` | 9 | 10.2% | Intervalo pré-estímulo / ITI / fixação |
| `control_verbal` | 7 | 8.0% | Controlo verbal / linguístico |
| `mixed` | 6 | 6.8% | Várias condições de referência (ex.: repouso + outra tarefa) |
| `within_task_only` | 5 | 5.7% | Só manipulações dentro da tarefa matemática |
| `control_perceptual` | 4 | 4.5% | Controlo perceptivo / visuoespacial |
| `control_working_memory` | 2 | 2.3% | Controlo de memória de trabalho (ex.: n-back) |
| `control_simple_math` | 1 | 1.1% | Controlo com tarefa matemática mais simples (mesmo domínio) |
| `other_context` | 1 | 1.1% | Contexto experimental atípico (ex.: gravidade) |

## `comparison_detail`

| Valor | Estudos |
|---|---:|
| (vazio) | 76 |
| eyes_closed | 5 |
| eyes_open | 4 |
| eyes_open_and_closed | 3 |

## `has_control_task`

| Valor | Estudos |
|---|---:|
| `True` | 72 |
| `False` | 16 |

## Estudos `unspecified` (*n* = 11)

Revisar texto da coluna 7 ou alargar padrões em `extract_comparison_from_text`.

### Índice 21

- **Título:** Can Music Support Calculation Skills? A Pilot Study Using Electrophysiological Measures…

- **Col. 7:**   …


### Índice 23

- **Título:** The neural differences of arithmetic verification performance depend on math skill: Evid…

- **Col. 7:** -…


### Índice 27

- **Título:** SOME CHANGES OF MATH ANXIETY GROUPS BASED ON TWO MEASUREMENTS, MASS & EEG…

- **Col. 7:** -…


### Índice 36

- **Título:** The Impact of Math Anxiety on Working Memory: A Cortical Activations and Cortical Functi…

- **Col. 7:** -…


### Índice 40

- **Título:** EEG-based discrimination of different cognitive workload levels from mental arithmetic…

- **Col. 7:** -…


### Índice 41

- **Título:** Stereotype-based stressors facilitate emotional memory neural network connectivity and e…

- **Col. 7:** -…


### Índice 42

- **Título:** Math anxiety and the shifting function: An event-related potential study of arithmetic t…

- **Col. 7:** -…


### Índice 75

- **Título:** Oscillatory EEG correlates of arithmetic strategy use in addition and subtraction…

- **Col. 7:** -…


### Índice 85

- **Título:** The analysis of EEG coherence reflects middle childhood differences in mathematical achi…

- **Col. 7:** nan…


### Índice 86

- **Título:** Towards Predicting Attention and Workload During Math Problem Solving…

- **Col. 7:** -…


### Índice 87

- **Título:** Training Machine Learning Models to Detect Group Differences in Neurophysiological Data …

- **Col. 7:** -…


## Regeneração

`python3 scripts/normalize_eeg_math.py`
