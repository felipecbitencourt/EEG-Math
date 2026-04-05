# Resultados — Questão de pesquisa 4, Bloco 2 (faixas de frequência)

A coluna **16** da revisão («Quais faixas de frequência foram analisadas?») está **presente** em `dados/tabela_normatizada.csv` (cópia do CSV original; não existe hoje campo derivado dedicado no `normalize_eeg_math.py`). A síntese abaixo usa deteção lexical automatizada (`scripts/analyze_q4_bloco2.py`), com heurística conservadora quando o texto **nega** análise explícita de bandas canónicas.

---

## Síntese quantitativa

Segundo `tabelas/q4_b2_resumo.md`, entre 88 estudos havia **79** células úteis na coluna 16 (excluindo apenas o marcador «(revisar)»). Em **67** estudos (76,1%) foi possível identificar pelo menos uma banda canónica (delta, theta, alpha, beta, gamma). A **mediana** de bandas detectadas por estudo foi **3** (máximo 5), compatível com descrições que listam várias faixas no mesmo protocolo.

As menções mais frequentes foram **theta** (58; 65,9%), **alpha** (55; 62,5%) e **beta** (43; 48,9%), seguidas de **delta** (31; 35,2%) e **gamma** (29; 33,0%).

<!-- INSERIR FIGURA 1
Arquivo: figuras/q4_b2_barras_bandas.png
Legenda sugerida: Frequência de estudos com menção a cada banda canónica na coluna 16 (N = 88); percentagens relativas ao corpus total; um estudo pode contribuir para várias bandas.
-->

<!-- INSERIR FIGURA 2
Arquivo: figuras/q4_b2_hist_n_bandas.png
Legenda sugerida: Distribuição do número de bandas canónicas detectadas por estudo (mediana no título).
-->

---

## Cruzamento com a tarefa matemática

Na tabela `tabelas/q4_b2_tarefa_x_banda.md`, **`mental_arithmetic`** apresentou as maiores coocorrências com **alpha** e **theta** (31 cada), seguidas de **beta** (25), **delta** (19) e **gamma** (16). **`subtraction`** manteve perfil semelhante (alpha 21; theta 20; beta 16). **`serial_subtraction`** e **`addition`** repetiram a combinação alpha/theta entre as contagens mais altas do seu grupo.

<!-- INSERIR FIGURA 3
Arquivo: figuras/q4_b2_heatmap_tarefa_x_banda.png
Legenda sugerida: Heatmap tarefa (`math_processes_tags`) × banda; intensidade normalizada por linha (dentro de cada tarefa); números = contagens absolutas de estudos.
-->

Em linguagem de artigo, isso apoia a ideia de que os paradigmas matemáticos mais centrais do corpus tendem a reportar análise em **faixas lentas e médias** (theta/alpha) e **beta**, com **gamma** e **delta** como componentes secundários mas não negligenciáveis.

---

## Ressalvas metodológicas

1. A codificação depende do **texto da coluna 16**: estudos que só descrevem filtro largo sem rotular bandas podem ficar sob-representados ou sem etiqueta, consoante o texto.
2. Frases do tipo *«did not explicitly analyze canonical frequency bands (e.g., alpha, beta)»* são **excluídas** da contagem canónica para reduzir falsos positivos por exemplificação.
3. Para revisão fina, convém cruzar manualmente os **9** estudos com coluna vazia e os **12** com texto mas sem banda detectada.

---

## Fechamento

O Bloco 2 descreve um corpus em que **theta, alpha e beta** concentram a maior parte das menções explícitas a bandas, com distribuição multibanda frequente ao nível do estudo. O cruzamento com tags de tarefa reforça consistência desse padrão nos agrupamentos de cálculo mental, subtração e adição.
