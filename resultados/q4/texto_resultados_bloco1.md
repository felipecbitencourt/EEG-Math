# Resultados — Questao de pesquisa 4, Bloco 1 (regioes cerebrais)

Este bloco sintetiza a cobertura espacial das analises de EEG no corpus (N = 88), com base em `eeg_regions`, `eeg_specific_sites` e `eeg_scope`, e incorpora o cruzamento com `math_processes_tags` para discutir como o tipo de tarefa matematica se relaciona ao padrao regional reportado.

---

## Sintese quantitativa

Conforme `tabelas/q4_b1_resumo.md`, `eeg_regions` e `eeg_scope` apresentam alta cobertura (85/88; 96,6%), enquanto `eeg_specific_sites` aparece em 34/88 (38,6%). A mediana de regioes por estudo foi 5,0, sugerindo que os artigos frequentemente descrevem cobertura espacial ampla em termos regionais; para sitios especificos, a mediana no corpus total foi 0,0 (e 7,0 entre estudos com sitios detectados), indicando heterogeneidade no nivel de detalhamento de eletrodos.

As regioes mais frequentes foram `Temporal` (93,2%), `Occipital` (89,8%), `Frontal` (84,1%), `Parietal` (83,0%) e `Central` (79,5%), com `Midline` em menor proporcao (27,3%). Em `eeg_scope`, predominou `regional` (72,7%), seguido de `full_scalp` (23,9%).

<!-- INSERIR FIGURA 1
Arquivo: figuras/q4_b1_barras_eeg_regions.png
Legenda sugerida: Frequencia de estudos por regiao EEG (`eeg_regions`), com percentual sobre N = 88.
-->

<!-- INSERIR FIGURA 2
Arquivo: figuras/q4_b1_barras_eeg_scope.png
Legenda sugerida: Distribuicao de `eeg_scope` no corpus (regional, full scalp e vazio), com contagens e percentuais.
-->

<!-- INSERIR FIGURA 3
Arquivo: figuras/q4_b1_hist_n_regions.png
Legenda sugerida: Distribuicao do numero de regioes por estudo.
-->

<!-- INSERIR FIGURA 4
Arquivo: figuras/q4_b1_hist_n_sites.png
Legenda sugerida: Distribuicao do numero de sitios especificos por estudo, considerando apenas estudos com `eeg_specific_sites` > 0.
-->

<!-- INSERIR FIGURA 5
Arquivo: figuras/q4_b1_barras_top_sites.png
Legenda sugerida: Top sitios de eletrodos mais frequentes no subconjunto com `eeg_specific_sites` preenchido.
-->

---

## Achados do cruzamento tarefa x regiao

O cruzamento `math_processes_tags x eeg_regions` (`tabelas/q4_b1_tarefa_x_regiao.md`) mostrou um padrao robusto de coocorrencia entre tarefas aritmeticas centrais e cobertura regional ampla. Para `mental_arithmetic`, as maiores contagens ocorreram em `Occipital` (46), `Temporal` (45), `Parietal` (42), `Central` (40) e `Frontal` (39). Para `subtraction`, houve distribuicao semelhante (`Occipital` e `Temporal` com 27; `Parietal` com 24; `Central` e `Frontal` com 22).

Em tarefas de `addition`, o gradiente tambem permaneceu alto em `Occipital` e `Temporal` (23 cada), seguido de `Central` (21) e `Frontal`/`Parietal` (19 cada). Em termos descritivos, isso sugere que os paradigmas mais frequentes do corpus (especialmente calculo mental e subtracao) sao operacionalizados com cobertura envolvendo multiplos eixos regionais, em vez de foco exclusivo em um unico lobo.

<!-- INSERIR FIGURA 6
Arquivo: figuras/q4_b1_heatmap_tarefa_x_regiao.png
Legenda sugerida: Heatmap do cruzamento entre tags de tarefa matematica e regioes EEG. Cores normalizadas por linha (dentro de cada tarefa); numeros indicam contagens absolutas de estudos.
-->

O perfil de `eeg_scope` por tarefa (top tarefas) mostrou predominancia de `regional` em todos os grupos mais frequentes, com variacao secundaria de `full_scalp`, reforcando que a literatura tende a reportar redes regionais mesmo quando o registro cobre grande parte do escalpo.

<!-- INSERIR FIGURA 7
Arquivo: figuras/q4_b1_barras_scope_por_tarefa.png
Legenda sugerida: Percentual de `eeg_scope` por tarefa matematica nas tags mais frequentes.
-->

---

## Fechamento

Os achados do Q4-B1 indicam que a literatura analisada privilegia descricoes regionais amplas da atividade EEG e que esse padrao se mantem quando estratificado pelo tipo de tarefa matematica. Em termos de narrativa para artigo, o resultado central e que a relacao tarefa-regiao aparece como **distribuicao multirregional recorrente** (com destaque para temporal/occipital/frontal/parietal), mais do que como especializacao regional estreita.

