# Resultados — Questao de pesquisa 3, Bloco 3 (dimensoes cognitivas associadas)

A sintese do Bloco 3 usa tres eixos complementares da tabela normatizada: `psych_domains`, `behavioral_domains` e `physio_list`. O objetivo e descrever como o corpus distribui dimensoes psicologicas, comportamentais e fisiologicas adicionais no contexto das tarefas matematicas com EEG. Os resultados abaixo sao descritivos e baseiam-se em `dados/tabela_normatizada.csv`, com outputs de `scripts/analyze_q3_bloco3.py`.

---

## Sintese quantitativa (tabela-resumo)

Valores de `tabelas/q3_b3_resumo.md`:

| Indicador | Valor |
|-----------|------:|
| Registros na base | 88 |
| Estudos com `psych_domains` preenchido | 29 (33,0%) |
| Estudos com `behavioral_domains` preenchido | 78 (88,6%) |
| Estudos com `physio_list` preenchido | 40 (45,5%) |
| Cobertura entre elegiveis (`psych_domains`) | 29/29 (100,0%) |
| Cobertura entre elegiveis (`behavioral_domains`) | 78/78 (100,0%) |
| Cobertura entre elegiveis (`physio_list`) | 40/40 (100,0%) |

No eixo psicologico, as categorias mais frequentes sao **`Intelligence`** (12 estudos; 13,6% do corpus) e **`Anxiety`** (10; 11,4%), enquanto as demais aparecem como cauda de baixa frequencia (`Stress`, `Diagnosis`, `Attention`, `Cognition`, `Depression`, `Personality`, `Self_concept`). No eixo comportamental, predominam **`performance`** (57; 64,8%) e **`speed`** (48; 54,5%), seguidos por **`learning`** (22; 25,0%) e **`metacognition`** (14; 15,9%). Em `physio_list`, **`EOG`** domina claramente (34; 38,6%), com menor presenca de `ECG` (7; 8,0%) e `EMG` (4; 4,5%).

---

## Coocorrencias entre eixos

As coocorrencias extraidas em `tabelas/q3_b3_coocorrencias.md` mostram padroes consistentes com a literatura do corpus:

- `psych_domains` x `behavioral_domains`:
  - `Intelligence` com `speed` (9) e `performance` (8);
  - `Anxiety` com `performance` (7), `speed` (7) e `affective` (5).
- `psych_domains` x `physio_list`:
  - `Intelligence` com `EOG` (8);
  - `Anxiety` com `EOG` (6).
- `behavioral_domains` x `physio_list`:
  - `performance` com `EOG` (25);
  - `speed` com `EOG` (20).

Esse perfil sugere que os estudos com avaliacao psicologica/clinica tendem a se articular com desfechos comportamentais classicos (desempenho e velocidade), enquanto a instrumentacao fisiologica adicional e majoritariamente centrada em controle ocular (EOG), com menor diversidade de sinais autonomicos complementares.

---

## Leitura por cobertura e multimodalidade

A distribuicao por numero de eixos preenchidos (0/1/2/3) indica heterogeneidade de profundidade de caracterizacao entre estudos: parte relevante cobre um unico eixo (tipicamente comportamental), e subconjuntos menores combinam dois ou tres eixos simultaneamente. Em termos de interpretacao de resultados, isso recomenda distinguir:

1. estudos com foco em desempenho/tempo de resposta;
2. estudos com triangulacao comportamento + fisiologia adicional;
3. estudos com caracterizacao psicologica explicita.

<!-- INSERIR FIGURA 1
Arquivo: figuras/q3_b3_barras_psych_domains.png
Legenda sugerida: Frequencia de estudos por dominio psicologico (`psych_domains`), percentual sobre N = 88.
-->

<!-- INSERIR FIGURA 2
Arquivo: figuras/q3_b3_barras_behavioral_domains.png
Legenda sugerida: Frequencia de estudos por dominio comportamental (`behavioral_domains`), percentual sobre N = 88.
-->

<!-- INSERIR FIGURA 3
Arquivo: figuras/q3_b3_barras_physio_list.png
Legenda sugerida: Frequencia de variaveis fisiologicas adicionais (`physio_list`) por estudo, percentual sobre N = 88.
-->

<!-- INSERIR FIGURA 4
Arquivo: figuras/q3_b3_rosca_cobertura_psych.png
Legenda sugerida: Cobertura de preenchimento de `psych_domains`.
-->

<!-- INSERIR FIGURA 5
Arquivo: figuras/q3_b3_rosca_cobertura_behavioral.png
Legenda sugerida: Cobertura de preenchimento de `behavioral_domains`.
-->

<!-- INSERIR FIGURA 6
Arquivo: figuras/q3_b3_rosca_cobertura_physio.png
Legenda sugerida: Cobertura de preenchimento de `physio_list`.
-->

<!-- INSERIR FIGURA 7
Arquivo: figuras/q3_b3_heatmap_psych_x_behavioral.png
Legenda sugerida: Heatmap de coocorrencia entre dominios psicologicos e comportamentais (contagem de estudos).
-->

<!-- INSERIR FIGURA 8
Arquivo: figuras/q3_b3_heatmap_psych_x_physio.png
Legenda sugerida: Heatmap de coocorrencia entre dominios psicologicos e variaveis fisiologicas adicionais.
-->

<!-- INSERIR FIGURA 9
Arquivo: figuras/q3_b3_heatmap_behavioral_x_physio.png
Legenda sugerida: Heatmap de coocorrencia entre dominios comportamentais e variaveis fisiologicas adicionais.
-->

<!-- INSERIR FIGURA 10
Arquivo: figuras/q3_b3_barras_n_eixos_preenchidos.png
Legenda sugerida: Numero de estudos por quantidade de eixos preenchidos no Bloco 3 (0 a 3).
-->

---

## Fechamento

No recorte do Bloco 3, o corpus e fortemente orientado a medidas comportamentais (especialmente desempenho e velocidade), com cobertura psicologica mais seletiva e fisiologia adicional dominada por EOG. Em termos de uso na secao de resultados, essa composicao apoia uma narrativa de **predominio comportamental com multimodalidade parcial**, em que coocorrencias entre inteligencia/ansiedade e desempenho/velocidade aparecem como padroes recorrentes.

