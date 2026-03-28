# Resultados — Questão de pesquisa 3, Bloco 2 (estrutura experimental)

A operacionalização da **comparação experimental** — a que condição a tarefa matemática é contrastada — foi sintetizada a partir do texto da **coluna 7** da revisão, via função `extract_comparison_from_text` em `scripts/normalize_eeg_math.py`. Os campos `comparison_type`, `comparison_detail` e `has_control_task` servem a agregações descritivas; o texto original da coluna 7 permanece a referência para nuances protocolares. Resultados exploratórios, sem inferência causal.

---

## Síntese quantitativa (tabela-resumo)

Valores de `tabelas/q3_b2_resumo.md`, gerados por `scripts/analyze_q3_bloco2.py`.

| Indicador | Valor |
|-----------|------:|
| Registros na base | 88 |
| Estudos `comparison_type` = `resting_state` | 42 (47,7%) |
| Estudos `unspecified` (col. 7 vazia ou «-») | 11 (12,5%) |
| Estudos `baseline_epoch` (pré-estímulo / ITI / fixação) | 9 (10,2%) |
| Estudos `control_verbal` | 7 (8,0%) |
| Estudos `mixed` (várias referências, ex. repouso + outra tarefa) | 6 (6,8%) |
| Estudos `within_task_only` | 5 (5,7%) |
| Estudos `control_perceptual` | 4 (4,5%) |
| Estudos `control_working_memory` | 2 (2,3%) |
| Estudos `control_simple_math` | 1 (1,1%) |
| Estudos `other_context` | 1 (1,1%) |
| Estudos com `comparison_detail` ocular preenchido | 12 |
| `has_control_task` = True | 72 (81,8%) |
| `has_control_task` = False | 16 (18,2%) |

A categoria **`resting_state`** domina: quase metade dos trabalhos menciona repouso, baseline de repouso, estado relaxado ou equivalente como referência. **`unspecified`** concentra-se em linhas sem texto útil na coluna 7. **`within_task_only`** e **`has_control_task` = False** alinham-se conceitualmente: cinco estudos descrevem apenas manipulações dentro da própria tarefa matemática (dificuldade, correto/incorreto, tempo em tarefa, etc.), sem tarefa de controlo externa normatizada como tal; os restantes `False` vêm sobretudo de `unspecified`.

---

## Leitura qualitativa e figuras

Entre os controlos **não matemáticos**, predominam rotas **verbais ou linguísticas** e **perceptivo-visuoespaciais** (incluindo fixação e correspondência de estímulos). **Memória de trabalho** aparece em dois estudos (ex.: n-back). **Misto** captura desenhos em que o texto explicita repouso conjuntamente com outra tarefa ou com variações internas de carga. **`control_simple_math`** isola o caso em que uma tarefa matemática complexa (ex. puzzle) é contrastada com uma tarefa aritmética mais simples no mesmo domínio — útil para não confundir com controlo “não numérico”.

O campo **`comparison_detail`** documenta **olhos fechados / abertos / ambos** quando o texto o permite; na maioria dos casos permanece vazio, porque a coluna 7 não detalha o estado ocular.

<!-- INSERIR FIGURA 1
Arquivo: figuras/q3_b2_barras_comparison_type.png
Legenda sugerida: Frequência de estudos por `comparison_type` (rótulos em português); percentagens relativas a N = 88.
-->

<!-- INSERIR FIGURA 2
Arquivo: figuras/q3_b2_pizza_comparison_type.png
Legenda sugerida: Composição percentual do corpus por tipo de comparação experimental.
-->

<!-- INSERIR FIGURA 3
Arquivo: figuras/q3_b2_rosca_has_control_task.png
Legenda sugerida: Estudos com referência externa normatizada (`has_control_task` True) versus desenhos só within-task ou não especificados (False).
-->

---

## Ressalvas metodológicas

A extração é **lexical**: sinónimos não listados, descrições implícitas ou comparações só na secção de métodos podem ficar **desalinhadas** da categoria escolhida. Estudos **`unspecified`** devem ser fila prioritária para revisão humana da coluna 7. A decisão de contar **repouso** como referência externa (`has_control_task` True) segue a prática comum de síntese em EEG, mas pode ser recodificada para análises que exijam estritamente **tarefa ativa de controlo**.

---

## Fechamento

O Bloco 2 descreve um corpus em que a **comparação a repouso** é a forma mais frequente de contextualizar a tarefa matemática, seguida de **intervalos basais curtos** e de **controlos verbais ou perceptivos**. Uma minoria explícita restringe-se a **variações dentro da tarefa**. A articulação com o Bloco 1 (`math_processes_tags`) e com medidas comportamentais (Bloco 4) pode ser explorada na discussão para relacionar **tipo de processo** com **tipo de desenho comparativo**.
