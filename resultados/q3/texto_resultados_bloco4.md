# Resultados — Questao de pesquisa 3, Bloco 4 (medidas observaveis)

Este bloco sintetiza como os estudos operacionalizam os desfechos observaveis a partir de `behavioral_measures`, `behavioral_count`, `has_behavioral`, `has_physio` e `has_clinical_psych`. A analise utiliza `dados/tabela_normatizada.csv` (N = 88) e os artefatos gerados por `scripts/analyze_q3_bloco4.py`.

---

## Sintese quantitativa do corpus

Conforme `tabelas/q3_b4_resumo.md`, houve predominio de estudos com medida comportamental explicita (`has_behavioral` = 78/88; 88,6%), enquanto variaveis fisiologicas adicionais (`has_physio`) apareceram em 40/88 (45,5%) e variaveis psicologicas clinicas (`has_clinical_psych`) em 28/88 (31,8%). A riqueza de medidas comportamentais por estudo foi moderada (`behavioral_count` medio = 2,03; mediana = 2; maximo = 5), indicando que a maior parte dos protocolos nao se limita a um unico desfecho comportamental.

---

## Medidas comportamentais mais frequentes

As medidas mais recorrentes foram **`Accuracy`** (54 estudos; 61,4%) e **`Reaction_time`** (46; 52,3%), seguidas por **`Score`** (22; 25,0%) e **`Error_rate`** (14; 15,9%). Medidas de autorrelato/metacognitivas (p.ex., `Self_report`, `Difficulty`, `Confidence`) apareceram com menor frequencia, sugerindo que o corpus privilegia indicadores de desempenho e velocidade em detrimento de fenomenologia subjetiva.

<!-- INSERIR FIGURA 1
Arquivo: figuras/q3_b4_barras_behavioral_measures.png
Legenda sugerida: Frequencia de medidas comportamentais observaveis por estudo (N = 88). As porcentagens referem-se ao total do corpus; multiplas medidas podem ocorrer no mesmo estudo.
-->

Essa distribuicao reforca que os desfechos comportamentais centrais da literatura analisada sao de natureza **psicometrica-operacional** (acuracia e tempo de resposta), com menor representacao de desfechos afetivos ou de fadiga.

---

## Riqueza de mensuracao por estudo

A distribuicao de `behavioral_count` mostrou concentracao em **2 medidas por estudo** (33 estudos), seguida de 1 medida (19 estudos) e 3 medidas (14 estudos). Foram identificados 10 estudos com `behavioral_count = 0`, o que sinaliza ausencia de medida comportamental detectada na codificacao automatica para esse subconjunto.

<!-- INSERIR FIGURA 2
Arquivo: figuras/q3_b4_hist_behavioral_count.png
Legenda sugerida: Distribuicao do numero de medidas comportamentais por estudo (`behavioral_count`), com mediana indicada no titulo.
-->

Do ponto de vista metodologico, esse padrao e compatível com protocolos que tipicamente combinam acuracia + tempo de reacao, enquanto baterias mais extensas (4-5 medidas) aparecem como minoria.

---

## Integracao entre eixos observaveis (comportamental, fisio, psicologico clinico)

A prevalencia isolada de cada eixo confirma gradiente de cobertura: comportamental > fisiologico adicional > psicologico clinico. Em termos de perfis combinados, o arranjo mais frequente foi **`1-0-0`** (apenas comportamental; 31 estudos; 35,2%), seguido de **`1-1-0`** (comportamental + fisio; 20; 22,7%). A combinacao completa **`1-1-1`** ocorreu em 14 estudos (15,9%), indicando multimodalidade plena em aproximadamente um sexto do corpus.

<!-- INSERIR FIGURA 3
Arquivo: figuras/q3_b4_barras_prevalencia_flags.png
Legenda sugerida: Prevalencia dos tres eixos observaveis no corpus (`has_behavioral`, `has_physio`, `has_clinical_psych`), com contagem e porcentagem por barra.
-->

<!-- INSERIR FIGURA 4
Arquivo: figuras/q3_b4_barras_combo_flags.png
Legenda sugerida: Composicao dos perfis de mensuracao combinada. Codigo B-P-C: B=`has_behavioral`, P=`has_physio`, C=`has_clinical_psych` (1=True; 0=False).
-->

---

## Fechamento da secao

No Bloco 4, os achados apontam para um corpus com forte ancoragem em medidas comportamentais classicas, especialmente acuracia e tempo de reacao, e com multimodalidade parcial em parcela relevante dos estudos. Para discussao no artigo, esse perfil sustenta a interpretacao de que a operacionalizacao de processos matematicos em EEG tende a priorizar desfechos de desempenho, enquanto a integracao sistematica com indicadores fisiologicos adicionais e clinico-psicologicos permanece menos disseminada.

