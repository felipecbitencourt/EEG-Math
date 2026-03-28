
# Análise Topológica e Semântica: O Panorama de Pesquisa em EEG e Matemática

Esta análise explora a estrutura latente do campo de pesquisa através de técnicas de redução de dimensionalidade e processamento de linguagem natural aplicadas aos textos completos dos artigos revisados.

## 1. Metodologia de Mapeamento

Para transcender a categorização manual e revelar conexões empíricas, utilizamos um pipeline computacional composto por:

1.  **Extração de Features (TF-IDF):** Os artigos foram vetorizados usando *Term Frequency-Inverse Document Frequency* (n-grams 1-2), capturando não apenas palavras isoladas ("theta", "arithmetic"), mas conceitos compostos ("working memory", "power spectrum").
2.  **Redução de Dimensionalidade (UMAP vs t-SNE):** Optamos pelo algoritmo **UMAP** (Uniform Manifold Approximation and Projection) em detrimento do t-SNE e PCA.
    *   *Por que UMAP?* Enquanto o t-SNE prioriza apenas a preservação de vizinhanças locais (agrupando o que é muito similar), o UMAP preserva melhor a estrutura global dos dados. Isso é crucial para visualizar como grandes áreas temáticas (Megatópicos) se relacionam entre si, e não apenas ver ilhas isoladas.
    *   *Métrica:* Distância de Cosseno, ideal para espaços textuais de alta dimensão.

## 2. Clusterização Semântica e Coerência dos Tópicos

A projeção visual revela que a categorização teórica (Tópicos T1-T11) possui uma correspondência empírica variável. O **Silhouette Score de -0.05** indica que os limites entre os tópicos não são rígidos; não há "ilhas perfeitas", mas sim um *continuum* de pesquisa onde conceitos se entrelaçam.

### Tópicos Compactos (Alta Coerência)
Os tópicos com menor dispersão espacial (menor desvio padrão) são os mais terminologicamente consistentes:
*   **T2 – Ansiedade e Estresse (std ~0.43):** Forma um cluster muito denso. O vocabulário é altamente específico ("anxiety", "stress", "cortisol", "amygdala"), indicando uma subárea muito bem definida e pouco fragmentada.
*   **T1 – Transtornos/Clínica (std ~0.59):** Também coeso, sugerindo que artigos sobre discalculia e TDAH compartilham uma linguagem técnica distinta dos estudos com sujeitos neurotípicos.

### Tópicos Difusos (Alta Heterogeneidade)
Os tópicos com maior dispersão (std > 1.20) atuam como "guards-chuva" ou conectores:
*   **T10 – Análise Espectral:** É o tópico mais espalhado. Isso faz sentido intuitivamente: a análise espectral é uma *metodologia* aplicada a diversos problemas (ansiedade, carga, desempenho). Artigos deste tópico "viajam" pelo mapa em direção ao problema que estão investigando.
*   **T8 – Carga Cognitiva:** Aparece disperso pois "carga cognitiva" é um construto onipresente, estudado sob a ótica de redes, frequências ou tarefas educacionais.

## 3. Zonas Híbridas e Sobreposições

A análise de distância entre centroides revela quais tópicos são "vizinhos semânticos" imediatos, sugerindo áreas de fronteira fértil.

1.  **O "Triângulo Educacional" (T7 - T9 - T11):**
    *   Existe uma proximidade extrema entre **T7 (Desempenho)**, **T9 (Educação)** e **T11 (Contexto)**.
    *   *Interpretação:* A pesquisa aplicada em sala de aula (T9/T11) é semanticamente quase indistinguível dos estudos de desempenho (T7). Isso sugere que a distinção entre esses tópicos é mais contextual (onde o estudo foi feito) do que neurofisiológica (o que foi medido).

2.  **A Ponte Metodológica (T6 - T10):**
    *   **T6 (Conectividade)** e **T10 (Espectral)** formam outro eixo de proximidade. Ambos lidam com a "engenharia" do sinal EEG. Um artigo focado em coerência (Conectividade) usa termos muito similares a um focado em densidade espectral de potência (Espectral).

3.  **A "Ilha" do Aprendizado de Máquina (T5):**
    *   O tópico **T5 (Classificação/ML)** mantém uma distância maior dos tópicos puramente psicológicos (como T2 ou T8). Isso indica que a literatura de *Brain-Computer Interfaces* (BCI) e classificadores SVM/CNN introduz um léxico computacional ("accuracy", "classifier", "kernel") que a distingue fortemente da neurociência cognitiva clássica.

## 4. Conclusão: Fragmentação ou Integração?

O mapa não mostra um campo fragmentado em silos incomunicáveis. Pelo contrário, observa-se uma **Zona Central Densa** onde Carga Cognitiva (T8), Desempenho (T7) e Espectral (T10) se misturam. Esta é a "corrente principal" da literatura EEG-Matemática.

Nas periferias, temos as **Especializações**:
*   De um lado, a **Clínica/Ansiedade** (T1, T2) focada em patologia e emoção.
*   Do outro, a **Computação** (T5), focada em algoritmos.

Esta topologia sugere que a inovação no campo pode vir de **conectar as pontas**: aplicar os métodos avançados de T5 (ML) na ilha de T2 (Ansiedade), que hoje parecem distantes semanticamente.
