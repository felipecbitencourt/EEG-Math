# Auditoria — coluna 4 (amostra) × normatização `amostra_*`

Fonte: `dados/tabela_normatizada.csv`. Total de registros: **88**.

## O que este relatório faz

Heurísticas **não** substituem leitura do PDF: servem para **priorizar** linhas em que o texto da coluna 4 sugere um dado (idade, sexo, lateralidade) ou em que **N ≠ M+F**, enquanto a normatização ficou vazia ou inconsistente.

## Resumo de flags

| Flag | Significado (heurístico) | Nº de linhas |
|------|---------------------------|-------------|
| `flag_N_diferente_soma_MF` | N, M e F preenchidos e \|N − (M+F)\| > 0,5 | **4** |
| `flag_mean_idade_texto_sem_campo` | Texto sugere média de idade, mas `amostra_age_mean` vazio | **2** |
| `flag_faixa_idade_texto_sem_campo` | Texto sugere faixa etária, mas min/max ausente | **1** |
| `flag_sexo_texto_sem_M_nem_F` | Texto sugere contagens/% sexo, mas M e F vazios | **0** |
| `flag_so_um_sexo_codificado` | Só masculino **ou** só feminino preenchido | **5** |
| `flag_lateralidade_texto_so_unspecified` | Texto sugere lateralidade, mas campo = unspecified | **0** |
| `flag_n_total_ausente` | `amostra_n_total` vazio | **0** |
| `flag_texto_muito_curto` | Coluna 4 com menos de 8 caracteres | **0** |

## Arquivo para revisão linha a linha

- **`resultados/q2/tabelas/auditoria_coluna4_flags.csv`** — todas as linhas, flags booleanas e trecho da coluna 4.

---

## Detalhes por tipo de alerta

### N total ≠ soma M+F (revisar primeiro)
*4 caso(s).*

- **idx 10** | doi: 10.3389/fnhum.2014.00430
  - 24 participants. Math-gifted group: 11 adolescents (8 males, 3 females), ages 15–18 years old (mean age 16.3 ± 0.6). Control group: 13 adolescents (8 males, 5 females), ages 15–18 years old (mean age 15.9 ± 0.7).
  - norm: N=24.0 M=8.0 F=3.0 idade_m=16.3 [15.0-18.0] hand=unspecified

- **idx 26** | https://doi.org/10.1007/s11571-017-9467-8
  - The study was conducted with a control group of 27 healthy volunteers (15 men and 12 women) and a group of 13 patients with mild cognitive impairment (six men and seven women). All participants were between 50 and 80 yea…
  - norm: N=40.0 M=15.0 F=12.0 idade_m=None [50.0-80.0] hand=unspecified

- **idx 43** | 10.1093/cercor/bhae025
  - Two right-handed groups: 22 math experts, (5 female and 17 male, 19 to 24 years), and 22 math novices (7 female and 15 male, 19 to 35 years). ANOVA age effect that would have to be controlled along the study
  - norm: N=44.0 M=17.0 F=5.0 idade_m=None [None-None] hand=right

- **idx 56** | 10.1016/j.physbeh.2012.03.034
  - 81 healthy children, 44 girls // 37 boys.Experimental group (Fed group): 40 children (18 boys and 22 girls) , aged 8–11 years  (M = 9.78 years) .Control group (Fasting group): 41 children (19 boys and 22 girls) , aged 8–…
  - norm: N=81.0 M=18.0 F=22.0 idade_m=None [8.0-11.0] hand=unspecified


### Idade: texto sugere média ou faixa, campo vazio
*3 caso(s).*

- **idx 31** | 10.1109/ICMULT.2010.5629620
  - 22 right-handed healthy university males (1 excluded), average age is about 22.6
  - norm: N=22.0 M=None F=None idade_m=None [None-None] hand=right

- **idx 36** | 10.1109/ACCESS.2019.2892808
  - (2) groups of 16 students of the Aristotle University of Thessaloniki, namely LMA (Low Math Anxiety), and HMA (High Math Anxiety) according to their AMAS scores; mean ages were 22.5 ± 2.3 (LMA) and 22.21 ± 2.43 (HMA)
  - norm: N=16.0 M=None F=None idade_m=None [None-None] hand=unspecified

- **idx 86** | 10.1007/978-3-030-22244-4_27
  - 17 alunos (10 F, 7 M). Idade: entre 9 e 11 anos (M=10,05; DP=0,42).
  - norm: N=17.0 M=None F=None idade_m=None [None-None] hand=unspecified


### Sexo: texto sugere M/F mas ambos vazios; ou só um sexo codificado
*5 caso(s).*

- **idx 28** | https://doi.org/10.1007/s11517-024-03028-9 
  - The study sample consisted of sixty healthy volunteers with a mean age of 21.9 years and a standard deviation 29 males,and the sample demonstrated good overall performance on the math task, achieving a median score of 7.…
  - norm: N=60.0 M=29.0 F=None idade_m=21.9 [None-None] hand=unspecified

- **idx 41** | doi: 10.1093/scan/nsy043
  - 160 white paid participants (87 women) aware of the negative female math stereotype,  sample randomized into 2 groups with different interventions: 1) stereotype threat/DMT condition or 2) control/problem-solving (PST) c…
  - norm: N=160.0 M=None F=87.0 idade_m=None [None-None] hand=unspecified

- **idx 47** | 10.1007/s10339-021-01038-1
  - 36 female undergraduate students. High Performers: 18 participants, mean age 21 years and 3 months. Low Performers: 18 participants, mean age 20 years and 8 months.
  - norm: N=36.0 M=None F=36.0 idade_m=21.0 [None-None] hand=unspecified

- **idx 53** | 10.1016/0013-4694(77)90022-0
  - 21 boys in total. Experimental group: 10 boys with learning disabilities, aged 10.1–12.6 years (M = 11.3). Control group: 11 normal boys, aged 10.6–11.7 years (M = 11.2).
  - norm: N=21.0 M=21.0 F=None idade_m=None [None-None] hand=unspecified

- **idx 85** | 10.1016/j.bandc.2018.04.006
  - 40 children, all aged 8-to-9 years old. High Achievement (HA) Group: 20 children (6 females), mean age 9.1 years. Low Achievement (LA) Group: 20 children (10 females), mean age 9.1 years.
  - norm: N=40.0 M=None F=6.0 idade_m=9.1 [None-None] hand=unspecified


### Lateralidade: texto sugere destro/canhoto mas normatizado unspecified

*(nenhum caso nesta categoria)*



## Próximos passos sugeridos

1. Corrigir prioritariamente os casos **N ≠ M+F** (interpretação de subgrupo vs total).
2. Para idade/sexo, usar o CSV para abrir o PDF só nas linhas com flag.
3. Ajustar `normalize_eeg_math.py` só depois de classificar *falso positivo* da heurística vs *falha real* do extrator.

