# Resultados — Questão de pesquisa 3, Bloco 1 (processos matemáticos)

A caracterização dos **processos matemáticos** investigados tomou como referência o texto livre da coluna 6 da revisão, tal como exportado em `math_processes`, e a camada normatizada **`math_processes_tags`**, obtida por correspondência lexical (`MATH_PROCESS_KEYWORDS` em `scripts/normalize_eeg_math.py`). A redação abaixo apresenta síntese numérica, leitura descritiva e referências às figuras; trata-se de resultados exploratórios, sem inferência causal sobre a literatura além do recorte normatizado.

---

## Síntese quantitativa do corpus (tabela-resumo)

Os valores reproduzem `tabelas/q3_b1_resumo.md`, gerado por `scripts/analyze_q3_bloco1.py` a partir de `dados/tabela_normatizada.csv`.

| Indicador | Valor |
|-----------|------:|
| Registros na base | 88 |
| Texto da col. 6 vazio ou «-» | 1 |
| Comprimento médio do texto (excl. «-») | 75,4 caracteres |
| Estudos com ≥1 tag (`math_processes_tags`) | 86 (97,7%) |
| Estudos sem tag detectada | 2 (2,3%) |
| Total de atribuições estudo→tag | 179 |
| Média de tags por estudo (corpus inteiro) | 2,03 |
| Média de tags (só entre estudos com tag) | 2,08 |
| Máximo de tags num único estudo | 6 |

Dois aspectos emergem. Primeiro, o **texto qualitativo** está quase sempre preenchido, mas a **síntese automática** ainda deixa dois registros sem etiqueta — um por ausência de conteúdo na coluna 6 e outro por descrição não alinhada a processos matemáticos (vide `tabelas/revisao_normatizacao_processos_matematicos.md`). Segundo, a **multiplicidade de tags** por estudo (média ≈2) reflete a natureza composta das descrições (várias operações ou tarefas no mesmo protocolo); as percentagens por tag **não somam 100%** ao nível do corpus, porque cada estudo pode contribuir para várias categorias simultaneamente.

---

## Perfil das tags: predominância do cálculo mental e das operações básicas

Entre as etiquetas mais frequentes, **`mental_arithmetic`** surge em 46 estudos (52,3%), seguida de **`subtraction`** (28; 31,8%) e **`addition`** (24; 27,3%). **`serial_subtraction`** aparece em 15 trabalhos (17,0%), configurando um subconjunto claro de paradigmas tipo Kraepelin ou subtração contínua. Operações de **`multiplication`** e **`division`** são menos centrais no agregado (11 e 4 estudos, respectivamente), o que é compatível com um campo em que a **subtração serial** e a **adição** dominam os desenhos de tarefa relatados.

Tags que captam **raciocínio lógico**, **resolução de problemas**, **puzzles** ou **tarefas executivas** (`deductive_reasoning`, `problem_solving`, `puzzles_games`, `executive_mixed_task`) aparecem com contagens modestas (cerca de 4–6 estudos cada), assinalando uma cauda temática relevante mas minoritária face ao núcleo aritmético-mental. Categorias mais específicas (`fractions_ratios`, `functions_representations`, `standardized_test`, `modulo`, etc.) concentram-se em **um ou dois** trabalhos no presente recorte — úteis para localizar nichos, mas insuficientes sozinhas para sínteses quantitativas finas.

<!-- INSERIR FIGURA 1
Arquivo: figuras/q3_b1_barras_processos_tags.png
Legenda sugerida: Frequência de estudos por tag canónica de processo matemático (`math_processes_tags`); rótulos em português; percentagens referem-se ao total de 88 estudos.
-->

<!-- INSERIR FIGURA 2
Arquivo: figuras/q3_b1_rosca_cobertura_tags.png
Legenda sugerida: Proporção de estudos com pelo menos uma tag normatizada versus estudos sem tag; rosca com N total no centro.
-->

<!-- INSERIR FIGURA 3
Arquivo: figuras/q3_b1_hist_n_tags_por_estudo.png
Legenda sugerida: Distribuição do número de tags por estudo (histograma); mediana indicada no título.
-->

---

## Riqueza de codificação e leitura qualitativa

O histograma do número de tags por estudo complementa a tabela-resumo: a maioria dos trabalhos recebe **duas ou três** etiquetas compatíveis com descrições que mencionam, por exemplo, cálculo mental conjuntamente com adição e subtração. Estudos com **cinco ou seis** tags tendem a corresponder a protocolos verbalmente densos (várias operações, verificação, raciocínio ou representações múltiplas). Em linguagem de resultados, a normatização por palavras-chave **expande** o texto livre em dimensões comparáveis entre papers, à custa de **ambiguidade residual** (sinónimos não listados, tarefas mistas descritas de forma idiossincrática).

---

## Fechamento da seção de resultados

Em conjunto, o Bloco 1 descreve um corpus centrado em **cálculo mental** e **operações aritméticas básicas**, com subtração serial como paradigma recorrente, e uma **cauda** de processos ligados a problemas, puzzles, álgebra, comparação de magnitudes e raciocínio dedutivo. A cobertura das tags é alta, mas **dois estudos** carecem de etiquetas até revisão lexical ou correcção da coluna 6. Discussão posterior pode contrastar este perfil com a diversidade cognitiva declarada nos títulos ou abstracts e com a operacionalização nas colunas de tarefa comparativa (Bloco 2 da Q3).
