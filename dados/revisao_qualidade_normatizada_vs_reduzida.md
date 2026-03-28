# Revisão de qualidade: `tabela_normatizada.csv` em relação à base reduzida

**Base de referência:** `revisão-egg+math - Versão reduzida.csv`  
**Derivado:** `tabela_normatizada.csv` (pipeline em `normalize_eeg_math.py`)  
**Data da checagem automatizada:** linhas e colunas comparadas programaticamente (mesmo repositório).

---

## 1. Integridade estrutural

| Critério | Resultado |
|----------|-----------|
| Número de linhas (estudos) | **88** em ambos os arquivos |
| Colunas da reduzida preservadas | **Todas** as 28 colunas da versão reduzida aparecem na normatizada; nenhuma coluna da base foi perdida |
| Colunas adicionais na normatizada | **55** campos derivados (ex.: `amostra_*`, `eeg_*`, `stats_*`, `ml_*`, flags `has_*`, etc.) |
| Ordem e alinhamento das linhas | **100%** de coincidência de DOI e de título (1ª coluna), linha a linha |
| Alteração do texto das colunas originais | **Nenhuma** divergência entre reduzida e normatizada ao comparar, célula a célula, todas as colunas compartilhadas (após normalizar `NaN` e *strip*) |

**Conclusão:** a normatização é uma **extensão não destrutiva** da tabela reduzida: mesmos registros, mesma ordem, conteúdo textual idêntico nas colunas comuns.

---

## 2. Qualidade dos campos derivados (`amostra_*` e demais)

A extração automática de metadados de amostra depende de `parse_sample()` (expressões regulares sobre o texto da pergunta 4). Isso implica **limites previsíveis**:

### 2.1 Cobertura observada (normatizada, *n* = 88)

- `amostra_n_total`: **88** com valor após a atualização do extrator (antes: 81; **7** falhas corrigidas por regras adicionais — ver anexo).
- `amostra_n_male` / `amostra_n_female`: **33** / **34** (só quando o texto casa com padrões do tipo `N male` / `N female`).
- Idade (`amostra_age_mean`, mín/máx): **7** / **12** com média ou faixa — cobertura baixa frente ao potencial informativo do texto livre.
- `amostra_handedness`: **88** preenchidos (rótulo sempre presente; em muitos casos será `unspecified` por regra conservadora).
- `amostra_population_type`: **88** preenchidos (`unspecified`, `students`, `healthy`, `children`, … conforme palavras-chave).
- `amostra_n_excluded`: **2** estudos — reflexo raro do padrão “*n* excluded/removed” no texto.

### 2.2 Inconsistência puntual (M + F vs. N total)

Há **pelo menos um** caso em que `amostra_n_male` e `amostra_n_female` estão ambos informados e **não somam** `amostra_n_total` (diferença maior que 0,5): DOI `10.3389/fnhum.2014.00430` (*N* = 24 vs. 8 M + 3 F). Isso costuma indicar **subgrupos** no texto (ex.: apenas um grupo sexo reportado), **erro de parsing** ou **N total de outra etapa** do estudo — não necessariamente erro da tabela reduzida.

**Recomendação:** regras de validação (alerta quando M+F ≠ N e ambos existem) ou revisão manual desses casos.

### 2.3 Duplicidade de estudos

- **Nenhum** DOI não vazio aparece duplicado nas 88 linhas (checagem simples de duplicatas).

---

## 3. Limitações do pipeline de normatização (relevantes para “qualidade”)

1. **`amostra_n_total`:** o extrator foi expandido (vide função dedicada no script), mas relatos muito atípicos ou ambíguos (vários números sem contexto claro) ainda podem exigir revisão manual.
2. **Sexo:** padrões em inglês (`male`, `female`, `M`/`F` com contexto); relatos só em português ou tabelas pode não ser capturado.
3. **Lateralidade:** depende de frases com `right-hand` / `left-hand`; omissão vira `unspecified` (alto percentual é esperado se o original não citar lateralidade de forma explícita).
4. **Tipo de população:** dicionário reduzido (`child`, `student`, `healthy`, `patient`, `elder`); outras populações tendem a `unspecified`.
5. **Demais colunas derivadas** (EEG, estatística, ML): baseadas em *keyword matching*; falsos positivos/negativos são possíveis e não foram auditados linha a linha neste relatório.

---

## 4. Síntese

| Aspecto | Avaliação |
|---------|------------|
| Fidelidade à base reduzida | **Excelente** — cópia literal das colunas originais, sem perda nem troca de linhas |
| Completude da normatização | **Parcial** — `amostra_n_total` com cobertura total nos 88 registros após refinamento do parser; idade e pareamento M/F seguem esparsos |
| Consistência interna derivada | **Boa com ressalvas** — pelo menos um caso M+F ≠ *N* merece revisão |
| Uso recomendado | Análises agregadas e figuras com **transparência de cobertura**; campos críticos podem exigir **segunda passagem manual** ou refinamento de `parse_sample()` |

Para repetir as verificações estruturais após atualizar qualquer um dos CSVs, basta rodar de novo o script de comparação (ou reexecutar `normalize_eeg_math.py` a partir da reduzida e diffar o resultado com uma versão congelada, se desejar controle de versão).

---

## Anexo: os 7 registros que falhavam em `amostra_n_total` (extração antiga)

**Atualização:** o `normalize_eeg_math.py` foi ampliado com `extract_n_total_from_sample_text()` (padrões `from N healthy`, `N participants/volunteers`, soma de dois grupos saudáveis + pacientes, experts + novices, múltiplos “group of N”, e números por extenso em inglês até 99). Após regenerar o CSV, esses sete registros passam a receber `amostra_n_total` automaticamente (36, 40, 60, 44, 7, 16, 24, respectivamente) e o corpus atinge **88/88** linhas com N preenchido — sujeito a nova auditoria se o texto da coluna 4 mudar.

A tabela abaixo documenta a **lógica histórica** da falha (versão anterior do parser) e os valores esperados para conferência manual.

| Índice¹ | DOI | *N* sugerido (manual) | Por que o parser falhou (resumo) |
|--------|-----|----------------------|-----------------------------------|
| 25 | `doi:10.1088/1742-6596/2949/1/012004` | 36 | Frase começa com “The study…”; número aparece em “from **36** healthy volunteers”. |
| 26 | `10.1007/s11571-017-9467-8` | 40 (27+13) | Dois grupos; início não é numérico. Definir convênio (N total vs. por grupo). |
| 28 | `10.1007/s11517-024-03028-9` | 60 | “**sixty**” por extenso em inglês. |
| 43 | `10.1093/cercor/bhae025` | 44 (22+22) | Início “Two right-handed groups”; totais nos subgrupos. |
| 55 | `10.1109/NER.2013.6696049` | 7 | “**seven** … subjects” por extenso. |
| 57 | `10.1016/0301-0511(81)90040-5` | 16 | “The volunteers were **16**…” — falta de token `participant/subject` imediatamente após o número no padrão atual. |
| 62 | — (sem DOI na base) | 24 | “**24** right-handed participants” após prefixo “The study's sample consisted of”. |

### Trechos da pergunta 4 (amostra), arquivo normatizado

1. **Índice 25:** “The study utilized an EEG dataset obtained from **36** healthy volunteers…”

2. **Índice 26:** “…a control group of **27** healthy volunteers… and a group of **13** patients…”

3. **Índice 28:** “The study sample consisted of **sixty** healthy volunteers with a mean age of 21.9…”

4. **Índice 43:** “**Two** right-handed groups: **22** math experts… and **22** math novices…”

5. **Índice 55:** “The study included **seven** healthy subjects (2 females and 5 males)…”

6. **Índice 57:** “The volunteers were **16** right-handed male students between the ages of 18 and 30.”

7. **Índice 62:** “The study's sample consisted of **24** right-handed participants divided into two groups of twelve.”

¹ Índice da linha no `DataFrame` carregado com `pd.read_csv` (0 = primeira linha de dados após o cabeçalho). Útil para localizar o registro em scripts; em planilha Excel o número da linha costuma ser índice + 2.
