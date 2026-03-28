import pandas as pd
import re
import os
from pathlib import Path

# =========================
# CONFIGURAÇÃO DE CAMINHOS
# =========================
_REPO = Path(__file__).resolve().parent.parent
INPUT_FILE = str(_REPO / "dados" / "revisão-egg+math - Versão reduzida.csv")
OUTPUT_FILE = str(_REPO / "dados" / "tabela_normatizada.csv")

# =========================
# DICIONÁRIOS GLOBAIS
# =========================

DEVICE_DICT = {"BioSemi": ["biosemi"], "Brain Products": ["brain products", "brainamp"], "Neuroscan": ["neuroscan", "quik-cap"], "Emotiv": ["emotiv"], "Enobio": ["enobio"], "EGI": ["egi", "electrical geodesics", "geodesic"], "Biopac": ["biopac"], "Neurocom": ["neurocom"], "Encephalan": ["encephalan"], "ANT Neuro": ["ant neuro", "eego"], "Mitsar": ["mitsar"], "Nihon Kohden": ["nihon kohden", "neurofax"], "Brainno": ["brainno"]}
OTHER_DEVICES_DICT = {"Eye-Tracker": ["eye-tracker", "tobii"], "Oximeter": ["oximeter", "oxímetro"], "E-Prime": ["e-prime"], "PsychoPy": ["psychopy"], "HeartMath": ["heartmath"], "Sleep Tracker": ["sleep tracker"], "GSR Sensor": ["gsr"]}
ELECTRODE_TYPE_DICT = {"Ag/AgCl": ["ag/agcl"], "Silver": ["silver"], "Gold": ["gold"], "Dry": ["dry"], "Gel": ["gel"], "Saline": ["saline", "salina"], "Carbon": ["carbon"], "Sponge": ["sponge"]}
REFERENCE_DICT = {"Mastoids": ["mastoid"], "Linked Mastoids": ["linked mastoids"], "Average": ["average"], "Nose Bias": ["nose"], "Cz": ["cz"], "CPz": ["cpz"], "Earlobe": ["earlobe"]}

physio_map = {"EOG": ["eog", "eye movement"], "EMG": ["emg", "muscle"], "ECG": ["ecg", "ekg"], "HRV": ["hrv"], "Respiration": ["respiration", "breathing"], "GSR_EDA": ["gsr", "eda"], "Sleep": ["sleep"], "Pulse": ["pulse", "heart rate"], "Blood_pressure": ["blood pressure", "bp"], "Glucose": ["glucose"]}
psych_map = {
    "STAI": ["STAI"], "HAMA": ["HAMA"], "PSS": ["PSS"], "MARS": ["MARS"], "SMARS": ["SMARS"], "AMAS": ["AMAS"], "MASS": ["MASS"],
    "HAMD": ["HAMD"], "BDI": ["BDI"], "MMSE": ["MMSE"], "RAVLT": ["RAVLT"], "ACE": ["ACE"], "CDR": ["CDR"],
    "RAPM": ["RAPM"], "RPMT": ["RPMT"], "WAIS": ["WAIS"], "WISC": ["WISC"], "BIS": ["BIS"],
    "NEO": ["NEO"], "ASRS": ["ASRS"], "DISC": ["DISC"], "NASA": ["NASA"], "CBCL": ["CBCL"]
}
psych_domain_map = {
    "Anxiety": ["STAI", "HAMA", "MARS", "SMARS", "AMAS", "MASS"],
    "Stress": ["PSS", "NASA"],
    "Depression": ["HAMD", "BDI"],
    "Intelligence": ["RAPM", "RPMT", "WAIS", "WISC", "BIS"],
    "Cognition": ["MMSE", "RAVLT", "ACE", "CDR"],
    "Attention": ["ASRS"],
    "Personality": ["NEO"],
    "Diagnosis": ["DISC", "CBCL"]
}

behavior_map = {"Accuracy": ["accuracy", "correct", "acurácia", "acerto"], "Error_rate": ["error", "erro"], "Reaction_time": ["reaction time", "rt", "tempo de reação"], "Latency": ["latency"], "Throughput": ["per minute"], "Confidence": ["confidence"], "Difficulty": ["difficulty", "effort"], "Strategy": ["strategy"], "Self_report": ["self-report"], "Stress": ["stress"], "Happiness": ["happiness"], "Anxiety": ["anxiety"], "Cognitive_load": ["cognitive load", "workload"], "Drowsiness": ["drowsiness"], "Score": ["score", "exam", "nota"]}

region_map = {"Frontal": ["frontal", "fp", "f"], "Central": ["central", "c"], "Parietal": ["parietal", "p"], "Temporal": ["temporal", "t"], "Occipital": ["occipital", "o"], "Midline": ["fz", "cz", "pz", "midline"]}

# PREPROCESSING (15)
FILTER_DICT = {"High-pass": ["high-pass", "high pass"], "Low-pass": ["low-pass", "low pass"], "Band-pass": ["band-pass", "band pass"], "Notch": ["notch"], "Filtering": ["filtro", "filtering"]}
EPOCH_DICT = {"Segmentation": ["segmentation", "segmentação"], "Epoching": ["epoching"], "Windowing": ["windowing"]}
BASELINE_DICT = {"Baseline Correction": ["baseline correction"], "Baseline Pre-stimulus": ["prestimulus", "pre-stimulus"]}
ARTIFACT_DICT = {"ICA": ["ica"], "PCA": ["pca"], "Regression": ["regression"], "Rejection": ["rejection"], "EOG Correction": ["eog correction"]}
DOWNSAMPLE_DICT = {"Resampling": ["resampling", "amostragem"], "Decimation": ["decimation"], "Downsampling": ["downsampling"]}

# FEATURES (15)
SPECTRAL_DICT = {"PSD": ["psd"], "Power": ["power"], "Spectral Density": ["spectral density"], "FFT": ["fft"], "Wavelet": ["wavelet"], "TFR": ["tfr", "time-frequency"]}
CONNECTIVITY_DICT = {"Coherence": ["coherence"], "Phase Synchrony": ["phase synchrony"], "PLV": ["plv"], "PLI": ["pli"], "DTF": ["dtf"], "PDC": ["pdc"]}
ERP_DICT = {"ERP": ["erp", "event related potential"], "P300": ["p300"], "N400": ["n400"], "MMN": ["mmn"], "LPP": ["lpp"]}
NONLINEAR_DICT = {"Entropy": ["entropy"], "Lyapunov": ["lyapunov"], "Complexity": ["complexity"], "Fractal": ["fractal"], "Nonlinear": ["não linear"]}
ML_FEAT_DICT = {"Classification": ["classification"], "SVM": ["svm"], "Random Forest": ["random forest"], "Neural Network": ["neural network"], "Machine Learning": ["machine learning"], "Deep Learning": ["deep learning"], "LDA": ["lda"]}

# SOFTWARE (17)
languages_dict = {"Python": ["python"], "MATLAB": ["matlab"], "R": [" r ", ",r", "r-"], "Fortran": ["fortran"], "C/C++": ["c-program", "c++"]}
toolboxes_dict = {"EEGLAB": ["eeglab"], "Brainstorm": ["brainstorm"], "MNE": ["mne"], "Psychtoolbox": ["psychtoolbox"], "LIBSVM": ["libsvm"], "NoiseTools": ["noisetools"], "OpenMEEG": ["openmeeg"], "ERPLAB": ["erplab"], "BBCI": ["bbci"], "Brain Connectivity Toolbox": ["connectivity toolbox"], "Keras": ["keras"], "Pyunicorn": ["pyunicorn"]}
software_dict = {"BrainVision Analyzer": ["brainvision"], "Neuroscan Scan": ["scan"], "ActiView": ["actiview"], "NeuroGuide": ["neuroguide"], "WinEEG": ["wineeg"], "EEProbe": ["eeprobe"], "EEvoke": ["eevoke"], "Cartool": ["cartool"], "LORETA": ["loreta"], "SPSS": ["spss"], "STATISTICA": ["statistica"], "Excel": ["excel"], "E-Prime": ["e-prime"], "PsychoPy": ["psychopy"], "Presentation": ["presentation"]}

# STATS (18)
parametric_tests = {"t-test": ["t-test", "t test"], "ANOVA": ["anova"], "ANCOVA": ["ancova"], "Regression": ["regression"]}
nonparametric_tests = {"Wilcoxon": ["wilcoxon"], "Mann-Whitney": ["mann-whitney"], "Kruskal-Wallis": ["kruskal"], "Permutation test": ["permutation"], "Bootstrap": ["bootstrap"]}
corrections_dict = {"Bonferroni": ["bonferroni"], "FDR": ["fdr"], "Holm": ["holm"], "Greenhouse-Geisser": ["greenhouse"], "Huynh-Feldt": ["huynh"]}
correlation_dimred = {"Pearson": ["pearson"], "Spearman": ["spearman"], "PCA": ["pca", "principal component"], "Factor Analysis": ["factor analysis"]}
ml_methods = {"SVM": ["svm"], "LDA": ["lda"], "KNN": ["knn"], "Cross-validation": ["cross-validation"], "ROC/AUC": ["roc", "auc"], "Feature selection": ["feature selection", "rfe"]}
other_stats = {"Descriptive statistics": ["descriptive"], "Normality test": ["normality", "shapiro", "kolmogorov"], "Effect size": ["effect size"], "Bayesian": ["bayesian"]}

# CLASSIFICATION (19)
MODEL_MAP = {"SVM": ["svm", "support vector"], "kNN": ["knn", "k-nearest"], "LDA": ["lda", "linear discriminant"], "RF": ["random forest"], "DT": ["decision tree"], "NB": ["naive bayes"], "QDA": ["qda"], "ANN": ["ann", "neural"], "CNN": ["cnn"], "LSTM": ["lstm"], "GNN": ["gnn", "graph"], "LR": ["logistic regression"], "GB": ["gradient boosting"], "k-means": ["k-means"]}

# =========================
# FUNÇÕES DE EXTRAÇÃO GERAIS
# =========================

def find_from_dict(text, dictionary):
    if pd.isna(text) or not text: return []
    tl = str(text).lower()
    found = []
    for canonical, patterns in dictionary.items():
        if any(p.lower() in tl for p in patterns):
            found.append(canonical)
    return list(set(found))

def extract_n_channels(text):
    if not text or pd.isna(text): return None
    m = re.search(r'\b(\d+)\s*(?:channels|electrodes|sensors|-channel|canais|ch)\b', str(text), re.I)
    return int(m.group(1)) if m else None

def extract_eeg_system(text):
    if pd.isna(text) or not text: return None
    tl = str(text).lower()
    sm = {"10-20": ["10-20", "10/20"], "10-10": ["10-10"], "10-5": ["10-5"], "Extended_10-20": ["extended"]}
    for sys, pats in sm.items():
        if any(p in tl for p in pats): return sys
    return "Other/Specific" if len(re.findall(r'\b[FCPTAO][0-9zZ]{1,2}\b', tl)) > 0 else None

# =========================
# PARSING POR COLUNA
# =========================

_EN_NUM_UNITS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
_EN_NUM_TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}


def _parse_english_number_phrase(phrase: str):
    """Converte 'sixty', 'seven', 'twenty four', 'twenty-four' em inteiro (1–99)."""
    phrase = phrase.lower().strip().replace("-", " ")
    parts = phrase.split()
    if not parts:
        return None
    total = 0
    i = 0
    while i < len(parts):
        w = parts[i]
        if w in _EN_NUM_TENS:
            total += _EN_NUM_TENS[w]
            i += 1
            if i < len(parts) and parts[i] in _EN_NUM_UNITS and parts[i] not in _EN_NUM_TENS:
                total += _EN_NUM_UNITS[parts[i]]
                i += 1
        elif w in _EN_NUM_UNITS:
            total += _EN_NUM_UNITS[w]
            i += 1
        else:
            return None
    return total if total > 0 else None


def extract_n_total_from_sample_text(t: str):
    """
    Extrai N total do texto livre da amostra. Ordem: regras mais específicas antes.
    Retorna int ou None.
    """
    if pd.isna(t) or not str(t).strip():
        return None
    s = str(t).strip()

    def _dig(m):
        return int(m.group(1)) if m else None

    # 1) Início numérico ou N + participante (padrão original, ampliado)
    m = re.search(r"^(\d+)", s) or re.search(
        r"(\d+)\s*(?:participants?|subjects?|volunteers?|students?|people)\b", s, re.I
    ) or re.search(r"(\d+)\s*(?:part|subj|stud)(?!ents)", s, re.I)
    if m:
        return int(m.group(1))

    # 2) Dois grupos balanceados típicos (experts/novices)
    m = re.search(r"(\d+)\s+math\s+experts?.*?(\d+)\s+math\s+novices?", s, re.I | re.DOTALL)
    if m:
        return int(m.group(1)) + int(m.group(2))

    # 3) Saudáveis + pacientes / MCI (dois tamanhos de grupo)
    m = re.search(
        r"(\d+)\s+healthy\s+volunteers?.*?(?:group\s+of\s+)?(\d+)\s+patients?",
        s,
        re.I | re.DOTALL,
    )
    if m:
        return int(m.group(1)) + int(m.group(2))

    # 4) Vários "group of N" (ex.: controle + pacientes)
    groups = [int(x) for x in re.findall(r"group\s+of\s+(\d+)\b", s, re.I)]
    if len(groups) >= 2:
        return sum(groups)

    # 5) "from N healthy" / dataset obtido
    for pat in (
        r"from\s+(\d{1,3})\s+healthy\b",
        r"obtained\s+from\s+(\d{1,3})\b",
        r"dataset\s+.*?from\s+(\d{1,3})\s+healthy\b",
    ):
        m = re.search(pat, s, re.I)
        if m:
            return int(m.group(1))

    # 6) "consisted of N …" / "volunteers were N …" / "sample consisted of N"
    for pat in (
        r"consisted\s+of\s+(\d{1,3})\s+right-handed\b",
        r"consisted\s+of\s+(\d{1,3})\s+(?:right-handed\s+)?participants?\b",
        r"sample\s+consisted\s+of\s+(\d{1,3})\s+",
        r"volunteers\s+were\s+(\d{1,3})\s+",
        r"study\s+utilized\s+.*?from\s+(\d{1,3})\s+healthy\b",
    ):
        m = re.search(pat, s, re.I)
        if m:
            return int(m.group(1))

    # 7) "included N healthy" / "study included seven healthy"
    m = re.search(r"study\s+included\s+(\d{1,3})\s+healthy\b", s, re.I)
    if m:
        return int(m.group(1))

    m = re.search(r"(?:The\s+)?study\s+included\s+([a-z]+(?:\s+[a-z\-]+)?)\s+healthy\b", s, re.I)
    if m:
        wn = _parse_english_number_phrase(m.group(1))
        if wn is not None:
            return wn

    # 8) "consisted of sixty healthy" (número por extenso)
    m = re.search(r"consisted\s+of\s+([a-z]+(?:\s+[a-z\-]+)?)\s+healthy\b", s, re.I)
    if m:
        wn = _parse_english_number_phrase(m.group(1))
        if wn is not None:
            return wn

    m = re.search(r"sample\s+consisted\s+of\s+([a-z]+(?:\s+[a-z\-]+)?)\s+healthy\b", s, re.I)
    if m:
        wn = _parse_english_number_phrase(m.group(1))
        if wn is not None:
            return wn

    # 9) Fallback: primeiro "N participants/volunteers/subjects" mais ao início do texto
    m = re.search(r"(\d{1,3})\s+(?:healthy\s+)?(?:volunteers?|participants?|subjects?)\b", s, re.I)
    if m:
        return int(m.group(1))

    return None


def extract_age_fields_from_sample_text(t: str):
    """
    Extrai idade média, DP e faixa etária do texto da amostra.
    Faixa: prioriza contextos com years/age/old/yrs para evitar 4–8 Hz, etc.
    """
    if pd.isna(t) or not str(t).strip():
        return None, None, None, None
    s = str(t)
    sl = s.lower()

    amean = None
    asd = None
    amin, amax = None, None

    for pat in (
        r"mean\s+age\s*(?:of|was|is)?\s*[:=]?\s*(\d+[\.,]\d+|\d+)(?=\s*(?:years?|yrs?|yo\b|months?|\(|,|\.|\s|$))",
        r"mean\s+age\s*(?:of|was|is)\s+(\d+[\.,]\d+|\d+)\b",
        r"average\s+age\s*(?:of|was|is)?\s*[:=]?\s*(\d+[\.,]\d+|\d+)\b",
        r"median\s+age\s*(?:of|was|is)?\s*[:=]?\s*(\d+[\.,]\d+|\d+)\b",
    ):
        m = re.search(pat, sl, re.I)
        if m:
            amean = float(m.group(1).replace(",", "."))
            break

    m_pm = re.search(r"(\d+[\.,]?\d*)\s*±\s*(\d+[\.,]?\d*)", s)
    if m_pm:
        try:
            asd = float(m_pm.group(2).replace(",", "."))
        except (TypeError, ValueError):
            asd = None
    else:
        m_single = re.search(r"\bSD\s*[=:]?\s*(\d+[\.,]?\d*)", s, re.I) or re.search(
            r"standard\s+deviation\s*(?:of|was|=)?\s*(\d+[\.,]?\d*)", sl, re.I
        )
        if m_single:
            try:
                asd = float(m_single.group(1).replace(",", "."))
            except (TypeError, ValueError):
                asd = None

    range_patterns = [
        r"(?:between|from)\s+(\d{1,3})\s+and\s+(\d{1,3})\s*(?:years?|yrs?|year-old|y\.?o\.?)",
        r"(?:between|from)\s+(\d{1,3})\s+and\s+(\d{1,3})\s+(?:years?\s+)?old",
        r"ages?\s+(?:ranging\s+from\s+)?(\d{1,3})\s*(?:to|[-–—])\s*(\d{1,3})\s*(?:years?|yrs?)?",
        r"(\d{1,3})\s*[-–]\s*(\d{1,3})\s*years?\s*(?:old|of\s+age)?",
        r"(\d{1,3})\s*[-–]\s*(\d{1,3})\s*yrs?\b",
        r"(\d{1,3})\s*[-–]\s*(\d{1,3})\s*(?:years?|yrs?)(?:\s+old)?",
        r"aged?\s+(\d{1,3})\s*[-–]\s*(\d{1,3})\b",
    ]
    for pat in range_patterns:
        m = re.search(pat, sl, re.I)
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        lo, hi = (a, b) if a <= b else (b, a)
        if 3 <= lo <= 120 and 3 <= hi <= 120 and (hi - lo) <= 95:
            amin, amax = lo, hi
            break

    return amean, asd, amin, amax


def extract_sex_counts_from_sample_text(t: str):
    """
    Contagens M/F a partir do texto. Inglês e português; pares explícitos primeiro.
    Retorna (n_male, n_female) ou (None, None) se não houver padrão seguro.
    """
    if pd.isna(t) or not str(t).strip():
        return None, None
    s = str(t)
    sl = s.lower()

    # (regex, swap): swap=True quando grupo1=feminino e grupo2=masculino
    pair_specs = [
        (r"(\d+)\s*(?:men|males?|boys?)\s*(?:and|,)\s*(\d+)\s*(?:women|females?|girls?)", False),
        (r"(\d+)\s*(?:women|females?|girls?)\s*(?:and|,)\s*(\d+)\s*(?:men|males?|boys?)", True),
        (r"(\d+)\s*homens?\s+e\s+(\d+)\s+mulheres?", False),
        (r"(\d+)\s+mulheres?\s+e\s+(\d+)\s+homens?", True),
        (r"(\d+)\s*masculinos?\s+e\s+(\d+)\s+femininos?", False),
        (r"\(\s*(\d+)\s*(?:men|males?)\s+and\s+(\d+)\s*(?:women|females?)\s*\)", False),
        (r"(\d+)\s*male[s]?\s+and\s+(\d+)\s+female[s]?", False),
        (r"(\d+)\s*female[s]?\s+and\s+(\d+)\s+male[s]?", True),
    ]
    for pat, swap in pair_specs:
        m = re.search(pat, sl, re.I)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            return (b, a) if swap else (a, b)

    nm = nf = None
    m_m = re.search(
        r"(\d+)\s*(?:men|males?|boys?)\b(?:\s*(?:\(|,|and)\s*)?",
        sl,
        re.I,
    )
    m_f = re.search(
        r"(\d+)\s*(?:women|females?|girls?)\b",
        sl,
        re.I,
    )
    if m_m:
        nm = int(m_m.group(1))
    if m_f:
        nf = int(m_f.group(1))

    if nm is None:
        m2 = re.search(r"(\d+)\s*males?\b(?:\s+(?:and|,)\s+\d+\s*females?)?", sl, re.I)
        if m2:
            nm = int(m2.group(1))
    if nf is None:
        m3 = re.search(r"(\d+)\s*females?\b(?:\s+(?:and|,)\s+\d+\s*males?)?", sl, re.I)
        if m3:
            nf = int(m3.group(1))

    if nm is None:
        m4 = re.search(r"\(\s*(\d+)\s*M\s*,\s*(\d+)\s*F\s*\)", s, re.I)
        if m4:
            nm, nf = int(m4.group(1)), int(m4.group(2))
            return nm, nf

    return nm, nf


def extract_handedness_from_sample_text(t: str):
    """
    Lateralidade ao nível do relato: right / left / mixed / unspecified.
    """
    if pd.isna(t) or not str(t).strip():
        return "unspecified"
    sl = str(t).lower()

    if re.search(r"ambidextr|ambi\s*dexter|mixed\s+handedness|heterogeneous\s+handedness", sl):
        return "mixed"

    neg_left = bool(re.search(r"no\s+left[-\s]?hand|non[- ]?left[-\s]?hand|without\s+left[-\s]?hand", sl))
    neg_right = bool(re.search(r"no\s+right[-\s]?hand|non[- ]?right[-\s]?hand|without\s+right[-\s]?hand", sl))

    has_left = not neg_left and bool(
        re.search(r"left[- ]handed|left[- ]hand\b|canhoto|sinistr(?:al)?", sl)
    )
    has_right = not neg_right and bool(
        re.search(r"right[- ]handed|right[- ]hand\b|destro", sl)
    )
    if has_left and has_right:
        return "mixed"
    if has_left:
        return "left"
    if has_right:
        return "right"
    return "unspecified"


# Marcadores (pergunta 5) → tags canônicas para Bloco 2 / síntese
MARKER_KEYWORDS = {
    "math_anxiety": ["math anxiety", "mars", "smars", "amas", "stereotype threat", "math anxious"],
    "dyscalculia": ["dyscalculia", "discalculia", "developmental dyscalculia"],
    "gifted": ["gifted", "high ability", "high math", "math-gifted", "mathematically precocious"],
    "experts_novices": ["math expert", "experts and novices", "expert group", "novice group", "professional mathematician"],
    "mci_dementia": ["mci", "alzheimer", "dementia", "mild cognitive impairment", "cognitive impairment"],
    "schizophrenia": ["schizophren", "schizoaffective"],
    "autism": ["autism", " asd", "asd,"],
    "adhd": [" adhd", "adhd,"],
    "epilepsy": ["epilepsy", "epileptic"],
    "stroke": ["stroke", "cva"],
    "meditators": ["meditat", "mindfulness"],
    "teachers": ["teacher", "in-service teacher"],
}


def extract_marker_tags_from_text(text) -> str:
    """Lista semicolon-separada de marcadores detectados na coluna 5 (ou texto combinado)."""
    if pd.isna(text) or not str(text).strip() or str(text).strip() in ("-", "—"):
        return ""
    tl = str(text).lower()
    found = []
    for tag, pats in MARKER_KEYWORDS.items():
        if any(p in tl for p in pats):
            found.append(tag)
    return "; ".join(sorted(set(found)))


# Coluna 6 (processos matemáticos) → tags canônicas para Q3 Bloco 1 / síntese
MATH_PROCESS_KEYWORDS = {
    "addition": [
        "addition", "adição", "summation", "mental addition", "serial summation",
        "serial additions", "additions and subtractions", "addition and subtraction",
        "addition operations", "simple addition", "two-digit additions",
    ],
    "subtraction": [
        "subtraction", "subtração", "subtractions", "subtract", "continuous subtraction",
    ],
    "multiplication": [
        "multiplication", "multiplicação", "multiplications", "two-digit multiplication",
        "written multiplication",
    ],
    "division": ["division", "divisão", "divisions"],
    "mental_arithmetic": [
        "mental arithmetic", "mental math", "cálculo mental", "mental calculation",
        "numerical mental calculation", "mental arith", "artihmetic", "arithmetical addition",
        "mat (", "human computation", "numerical skills",
    ],
    "serial_subtraction": [
        "serial subtraction", "serial subtractions", "kraepelin", "subtracting the number 7",
        "subtract 7", "−7 from", "-7 from", "from 1000", "from 200",
    ],
    "fractions_ratios": ["fraction", "fractions", "proportional math", "ratios", "proportional"],
    "algebra": ["algebraic", " algebra", "algebra ", "algebra.", "algebra and", "quadratic functions", "attribute substitution"],
    "magnitude_comparison": [
        "digit comparison", "compare problems", "arithmetic comparisons", "arithmetic comparison",
        "comparison of four-digit", "comparison of two-digit", "visual digit comparison",
    ],
    "word_problems": ["word problem", "word problems"],
    "problem_solving": [
        "problem solving", "problem-solving", "math problem-solving", "mathematical problem solving",
        "math problem solving", "mathematical problem-solving",
    ],
    "deductive_reasoning": ["deductive", "syllogism", "categorical syllogism"],
    "inductive_reasoning": ["inductive reasoning", "rule induction", "rule application", "numerical inductive"],
    "geometry_spatial": [
        "geometric", "figural", "imagery strategy", "spatial", "symbolic and geometric",
    ],
    "functions_representations": [
        "graphical", "symbolic representation", "translate between", "representations of functions",
        "graphical (g)", "algebraic (f)",
    ],
    "standardized_test": ["sat items", "sat problem"],
    "puzzles_games": [
        "puzzle", "math24", "24 puzzle", "twenty-four", "tower of hanoi", "toh task",
        "hanoi ",
    ],
    "verification_task": ["verification paradigm", "verification task", "arithmetic verification"],
    "learning_demonstration": [
        "learning mathematics", "demonstrations", "learning-based mathematical", "math demonstrations",
    ],
    "modulo": ["mod problems", " mod ", " modulo"],
    "broad_math_battery": [
        "math fluency", "applied problems", "math calculation", "subtests", "broad math",
        "general math skills", "math abilities",
    ],
    "written_mode": ["written multiplication", "written arithmetic", "not purely mental"],
    "arithmetic_mixed_ops": [
        "simple arithmetic operations", "numerical operations:", "basic arithmetical",
        "additions, subtractions, multiplications", "addition, subtraction, fraction",
        "simple arithmetic calcul", "perform simple arithmetic", "repeatedly perform simple",
    ],
    "arithmetic_general": [
        "arithmetic processing",
        "arithmetic and probably",
    ],
    "executive_mixed_task": ["tower of hanoi", "executive function", "convergent thinking"],
}


def extract_math_process_tags_from_text(text) -> str:
    """Tags derivadas do texto livre da coluna 6 (processos matemáticos)."""
    if pd.isna(text) or not str(text).strip() or str(text).strip() in ("-", "—"):
        return ""
    tl = str(text).lower()
    found = []
    for tag, pats in MATH_PROCESS_KEYWORDS.items():
        if any(p in tl for p in pats):
            found.append(tag)
    return "; ".join(sorted(set(found)))


def extract_population_type_from_text(col4_text, col5_text=None) -> str:
    """
    Tipo populacional primário para Bloco 2. Usa coluna 4 + (opcional) coluna 5.
    Ordem: clínico > expertise matemática > misto crianças+estudantes > crianças > idosos > estudantes > saudável > não especificado.
    """
    parts = [str(col4_text or ""), str(col5_text or "")]
    t = " ".join(parts).lower()
    if not t.strip():
        return "unspecified"

    def _has(pat: str) -> bool:
        return bool(re.search(pat, t, re.I))

    def _looks_pediatric_context() -> bool:
        return bool(
            re.search(
                r"\bchild|\bchildren|infant|preschool|elementary\s+school|"
                r"primary\s+school|middle\s+school\b(?!\s+children\s+and)",
                t,
                re.I,
            )
        )

    # 1) Populações clínicas / neurológicas
    if _has(
        r"schizophren|schizoaffective|alzheimer|dementia|\bmci\b|mild cognitive impairment|"
        r"autism|\basd\b| adhd|epilepsy|stroke|brain injury|tumor|lesion|"
        r"dyscalculia|dyslexia|"
        r"patients?\s+with|patient group|clinical group|hospitalized|diagnos"
    ):
        return "clinical"

    # 2) Expertise / talento em matemática (antes de “student” genérico)
    if _has(r"math\s+experts?|experts?\s+and\s+novices|gifted|math-gifted|professional\s+mathematician"):
        return "experts_maths"

    # Idade escolar explícita (PT): “entre 9 e 11 anos” → crianças antes de “alunos” genérico
    m_pt_age = re.search(r"entre\s+(\d+)\s+e\s+(\d+)\s+anos", t, re.I)
    if m_pt_age and max(int(m_pt_age.group(1)), int(m_pt_age.group(2))) <= 14:
        return "children"

    has_children = bool(re.search(r"\bchildren\b|\bchild\s+(participant|subject|volunteer)?s?\b", t))
    has_students = (
        "student" in t
        or "undergraduate" in t
        or ("university" in t and "volunteer" in t)
        or "college" in t
        or bool(re.search(r"\b(alunos?|estudantes?|universit[aá]ri[oa]s?)\b", t))
    )
    if has_children and has_students:
        return "mixed_children_students"

    if has_children or (
        "adolescent" in t and "university" not in t and "college" not in t
    ):
        return "children"

    if _has(r"older adults?|elderly|seniors?|aged\s+6[5-9]|age[ds]?\s+7[0-9]|>\s*6[05]\s*years"):
        return "elderly"

    if has_students or "pupils" in t or "schoolchildren" in t:
        return "students"

    # Faixa etária típica de graduação sem a palavra “student”
    if _has(
        r"aged?\s+between\s+16\s+and\s+26\b|"
        r"\bages?\s+20\s+to\s+31\b|"
        r"\b21\s+to\s+25\s+years?\b|"
        r"\bag(?:e|es)d?\s+20\s+to\s+23\b|"
        r"\baged\s+20\s+to\s+23\b"
    ):
        return "students"

    m_mean = re.search(r"mean\s+age[^0-9]{0,28}(\d+(?:\.\d+)?)", t, re.I)
    if m_mean and _has(r"\bparticipants?\b"):
        ag = float(m_mean.group(1))
        if 18.0 <= ag <= 26.0:
            return "students"

    if "healthy" in t or "control group" in t or "volunteers" in t:
        return "healthy"

    # Amostras de conveniência adultas (laboratório / cognição), após exclusões acima
    if not _looks_pediatric_context():
        if _has(
            r"\badults?\b|\badult\s+subject|"
            r"single\s+participants?|\bone\s+participant\b|\b1\s+single\s+participant|"
            r"meditat|meditators?"
        ):
            return "healthy"
        if _has(r"\b\d+\s+adults?\b"):
            return "healthy"
        if _has(
            r"\(\s*\d+\s*males?|\(\d+\s*males?,\s*\d+\s*females?|"
            r"\bparticipants?\s*\(\s*\d+\s*(?:male|female)|"
            r"\d+\s*(?:males?|females?),\s*\d+\s*(?:males?|females?)"
        ):
            return "healthy"
        if _has(r"\d+\s*w\s+\d+\s*m\b|\d+\s*m\s+\d+\s*w\b|\d+\s*men\s+and\s+\d+\s+women"):
            return "healthy"
        if _has(r"\bindividuals?\b.*\b(?:were|was)\s+(?:selected|recruited|subdivided)"):
            return "healthy"
        if _has(r"\bpaid\s+participants?\b"):
            return "healthy"
        if _has(r"\b\d+\s+subjects?\b.*\b(?:high|low)\s+math|math\s+ability\s+group"):
            return "healthy"
        if _has(r"\b\d+\s+subjects?\b.*;\s*age\s+not\s+specified"):
            return "healthy"
        if _has(r"\b(?:1[0-9]|[2-9]\d|\d{3})\s+subjects?\b"):
            return "healthy"
        if _has(r"\b(?:1[0-9]|[2-9]\d|\d{3})\s+participants?\b"):
            return "healthy"

    if "elder" in t:
        return "elderly"

    return "unspecified"


def parse_sample_row(col4_text, col5_text=None):
    """Uma linha: coluna 4 obrigatória; coluna 5 opcional para população e marcadores."""
    t = str(col4_text)
    c5s = (
        ""
        if col5_text is None or (isinstance(col5_text, float) and pd.isna(col5_text))
        else str(col5_text)
    )

    ntot = extract_n_total_from_sample_text(col4_text)
    m_ex = re.search(r"(\d+)\s*(excluded|removed|discarded)", t, re.I)
    n_ex = int(m_ex.group(1)) if m_ex else None

    amean, asd, amin, amax = extract_age_fields_from_sample_text(col4_text)
    nm, nf = extract_sex_counts_from_sample_text(col4_text)
    handedness = extract_handedness_from_sample_text(col4_text)

    p_type = extract_population_type_from_text(col4_text, c5s)
    marcadores = extract_marker_tags_from_text(c5s)

    return pd.Series({
        "amostra_n_total": ntot, "amostra_n_excluded": n_ex, "amostra_age_mean": amean, "amostra_age_sd": asd,
        "amostra_age_min": amin, "amostra_age_max": amax, "amostra_n_male": nm, "amostra_n_female": nf,
        "amostra_population_type": p_type, "amostra_handedness": handedness,
        "amostra_marcadores_tags": marcadores,
    })


def parse_sample(text):
    """Compatibilidade: só coluna 4 (sem marcadores da Q5)."""
    return parse_sample_row(text, None)


def extract_comparison_from_text(comp_txt):
    """
    Q3 Bloco 2: tipo de comparação experimental (coluna 7), detalhe ocular (se aplicável),
    e se existe referência externa à tarefa matemática (repouso, outra tarefa, baseline longa).

    has_control_task = False apenas para within_task_only (só manipulações dentro da tarefa matemática)
    ou texto vazio; repouso conta como condição de referência (True).
    """
    if pd.isna(comp_txt):
        return "unspecified", None, False
    s = str(comp_txt).strip()
    if not s or s in ("-", "—"):
        return "unspecified", None, False

    tl = s.lower()

    def _eyes_detail():
        ec = "eyes closed" in tl or "eyes-closed" in tl
        eo = "eyes open" in tl or "eyes-open" in tl or bool(re.search(r"\beyes\s+opened\b", tl))
        if ec and eo:
            return "eyes_open_and_closed"
        if ec:
            return "eyes_closed"
        if eo:
            return "eyes_open"
        return None

    has_rest = bool(
        re.search(
            r"\bresting(?:\s+state|\s+baseline|\s+condition|\s+phase|\s+baseline\s+recording)?\b|"
            r"\brest(?:ing)?\s+state\b|\brest\s+state\b|\bresting\s+baseline\b|"
            r"\bestado\s+de\s+repouso\b|\brepouso\b|\bresting\s+period\b|"
            r"\bbaseline\s+rest|\brest\s+baseline\b|\brelax(?:ed)?\s+state\b|\brelax\s+state\b|"
            r"\bidle\s+state\b|\bnon-task\s+idle\b|\bbefore\s+task\s+condition\b|"
            r"\brest with eyes\b|\bempty mind\b|\bmeditative state\b|"
            r"\brest condition\b|\bat rest\b|\brest\s*\(\s*while\b|"
            r"\beyes-closed state\b|\b(relaxed|still).{0,55}eyes-closed\b|"
            r"\bbaseline conditions\b",
            tl,
        )
    )
    has_pre_stim_short = bool(
        re.search(
            r"pre-stimulus|prestimulus|inter-trial|intertrial|iti\b|"
            r"\b500\s*ms\b.*baseline|baseline\s*period\s*\(\s*500|"
            r"fixation\s+period|reference\s+trials|reference\s+interval",
            tl,
        )
    )
    has_within_phrase = bool(
        re.search(
            r"different difficulty levels within the task|"
            r"within the task itself|"
            r"do not compare the mathematical task with (a )?non-mathematical|"
            r"does not compare the mathematical task with another|"
            r"authors do not compare the mathematical task|"
            r"does not compare.*mathematical task with another control|"
            r"comparison is not with a task of a different nature|"
            r"not between different tasks.*arithmetic|"
            r"primary comparison is not between different tasks|"
            r"only comparisons? (made|reported) (are|is) (of )?two types.*within|"
            r"between-groups comparison.*(same|math)|"
            r"gifted vs\.? normal|gifted versus normal|"
            r"time on task|first \d+\s*minutes vs",
            tl,
        )
    )
    has_correct_incorrect = bool(re.search(r"correct (versus|vs\.?) incorrect|incorrect solution", tl))
    has_wm_control = bool(
        re.search(
            r"\bn-back\b|\bn back\b|sternberg|multi-object tracking|\bmot\b|"
            r"working memory task",
            tl,
        )
    )
    has_verbal_control = bool(
        re.search(
            r"verbal task|verbal tasks|anagram|general knowledge|"
            r"language training|reading, spelling|listen(ed)? to letters|a-l\)|"
            r"non-numeric verbal|verbal-logical|verbal image-matching|categorical syllogism|"
            r"academic discipline|different discipline",
            tl,
        )
    )
    has_perceptual_control = bool(
        re.search(
            r"pattern matching|image-matching|part-to-whole|watch(ed)? or listened|v-l\)|"
            r"visual fixation|fixation \(control|number looking|"
            r"figural-spatial|spatial part|perceptual control|watching.*letters",
            tl,
        )
    )
    has_addition_baseline = bool(re.search(r"basic addition task|addition task.*baseline", tl))

    if has_rest and (has_within_phrase or has_wm_control or has_verbal_control or has_perceptual_control or has_addition_baseline or "warm-up" in tl or "immediate recall" in tl):
        return "mixed", _eyes_detail(), True

    if has_within_phrase or (has_correct_incorrect and not has_rest and not has_wm_control and not has_verbal_control):
        return "within_task_only", None, False

    if has_rest:
        return "resting_state", _eyes_detail(), True

    if has_wm_control:
        return "control_working_memory", None, True

    if has_verbal_control:
        return "control_verbal", None, True

    if has_perceptual_control:
        return "control_perceptual", None, True

    if has_pre_stim_short and not has_rest:
        return "baseline_epoch", None, True

    if "anticipation period" in tl or "pre-problem" in tl:
        return "baseline_epoch", None, True

    if re.search(r"normal gravity|parabola|\b1g\b", tl):
        return "other_context", None, True

    if "compared to off-task" in tl or "no-task" in tl:
        return "mixed", None, True

    if re.search(r"basic addition task|serves as the study'?s baseline", tl) and re.search(
        r"puzzle|math24|math 24", tl
    ):
        return "control_simple_math", None, True

    return "other", _eyes_detail(), True


def parse_math(proc_txt, comp_txt):
    ct, cd, hct = extract_comparison_from_text(comp_txt)
    proc_tags = extract_math_process_tags_from_text(proc_txt)
    return pd.Series({
        "math_processes": proc_txt,
        "math_processes_tags": proc_tags,
        "comparison_type": ct,
        "comparison_detail": cd,
        "has_control_task": hct,
    })

def parse_vars(phys_txt, psych_txt):
    p_lst = find_from_dict(phys_txt, physio_map)
    m_lst = find_from_dict(psych_txt, psych_map)
    d_lst = find_from_dict(psych_txt, psych_domain_map)
    return pd.Series({
        "physio_list": ", ".join(p_lst), "has_physio": len(p_lst) > 0,
        "psych_measures": ", ".join(m_lst), "psych_domains": ", ".join(d_lst), "has_clinical_psych": len(m_lst) > 0
    })

def parse_behavior(text):
    f = find_from_dict(text, behavior_map)
    doms = list(set([next((dom for dom, ms in {"performance": ["Accuracy", "Error_rate"], "speed": ["Reaction_time", "Latency"], "efficiency": ["Throughput"], "metacognition": ["Confidence", "Difficulty", "Strategy", "Self_report"], "affective": ["Stress", "Happiness", "Anxiety"], "cognitive_load": ["Cognitive_load"], "attention": ["Drowsiness"], "learning": ["Score"]}.items() if k in ms), "other") for k in f]))
    return pd.Series({"behavioral_measures": ", ".join(f), "behavioral_domains": ", ".join(doms), "has_behavioral": len(f) > 0, "behavioral_count": len(f)})

def parse_eeg_areas(text):
    es = list(set([m.upper() for m in re.findall(r'\b([FCPTAO][0-9zZ]{1,2})\b', str(text))]))
    rs = find_from_dict(text, region_map)
    sys = extract_eeg_system(text)
    scope = "full_scalp" if any(x in str(text).lower() for x in ["full", "all", "total"]) else ("regional" if len(rs) > 0 else ("specific_sites" if len(es) > 0 else None))
    return pd.Series({"eeg_regions": ", ".join(rs), "eeg_specific_sites": ", ".join(es), "eeg_system": sys, "eeg_scope": scope})

def parse_tech(c13, c14):
    ds = find_from_dict(c13, DEVICE_DICT)
    ods = find_from_dict(c13, OTHER_DEVICES_DICT)
    nch = extract_n_channels(c14) or extract_n_channels(c13)
    etyp = find_from_dict(c14, ELECTRODE_TYPE_DICT)
    ref = find_from_dict(c14, REFERENCE_DICT)
    return pd.Series({
        "eeg_device": ", ".join(ds), "other_devices": ", ".join(ods), "tech_n_channels": nch,
        "electrode_type": ", ".join(etyp), "reference_reference": ", ".join(ref)
    })

def parse_prep(text):
    return pd.Series({
        "filtering": ", ".join(find_from_dict(text, FILTER_DICT)), "re_reference": ", ".join(find_from_dict(text, REFERENCE_DICT)),
        "epoching": ", ".join(find_from_dict(text, EPOCH_DICT)), "baseline": ", ".join(find_from_dict(text, BASELINE_DICT)),
        "artifact_removal": ", ".join(find_from_dict(text, ARTIFACT_DICT)), "downsampling": ", ".join(find_from_dict(text, DOWNSAMPLE_DICT)),
        "spectral_features": ", ".join(find_from_dict(text, SPECTRAL_DICT)), "connectivity_features": ", ".join(find_from_dict(text, CONNECTIVITY_DICT)),
        "erp_features": ", ".join(find_from_dict(text, ERP_DICT)), "nonlinear_features": ", ".join(find_from_dict(text, NONLINEAR_DICT)),
        "ml_features": ", ".join(find_from_dict(text, ML_FEAT_DICT))
    })

def parse_software(text):
    return pd.Series({"soft_language": "; ".join(find_from_dict(text, languages_dict)), "soft_toolbox": "; ".join(find_from_dict(text, toolboxes_dict)), "soft_software": "; ".join(find_from_dict(text, software_dict))})

def parse_stats(text):
    return pd.Series({
        "stats_parametric": "; ".join(find_from_dict(text, parametric_tests)),
        "stats_nonparametric": "; ".join(find_from_dict(text, nonparametric_tests)),
        "stats_corrections": "; ".join(find_from_dict(text, corrections_dict)),
        "stats_ml": "; ".join(find_from_dict(text, ml_methods)),
        "stats_other": "; ".join(find_from_dict(text, other_stats))
    })

def parse_ml(text):
    if pd.isna(text) or text.strip() in ["-", "No"]: return pd.Series({"ml_used": "no", "ml_models": None, "ml_validation": None, "ml_metrics": None})
    t = str(text).lower()
    models = find_from_dict(t, MODEL_MAP)
    valid = []
    if "fold" in t:
        m = re.search(r'(\d+)[-\s]?fold', t)
        valid.append(f"{m.group(1)}-fold" if m else "k-fold")
    if "cross-validation" in t: valid.append("CV")
    if "split" in t: valid.append("split")
    if "loso" in t: valid.append("LOSO")
    metrics = [m for m in ["accuracy", "auc", "f1", "precision", "recall", "kappa"] if m in t]
    return pd.Series({"ml_used": "yes", "ml_models": "; ".join(models), "ml_validation": "; ".join(valid), "ml_metrics": "; ".join(metrics)})

# =========================
# EXECUÇÃO DO PROCESSO
# =========================

def main():
    print(f"📖 Lendo arquivo: {INPUT_FILE}")
    if not os.path.exists(INPUT_FILE): return
    df = pd.read_csv(INPUT_FILE)

    # PROCESSAMENTO POR COLUNA
    c4n = "4. Amostra (número de participantes, idade)"
    c5n = [c for c in df.columns if c.strip().startswith("5.")][0]
    df_amostra = df.apply(lambda r: parse_sample_row(r[c4n], r[c5n]), axis=1)
    
    c7 = [c for c in df.columns if "7." in c][0]
    df_math = df.apply(lambda r: parse_math(r["6. Quais processos matemáticos são investigados?"], r[c7]), axis=1)
    
    c9, c10 = [c for c in df.columns if "9." in c][0], [c for c in df.columns if "10." in c][0]
    df_vars = df.apply(lambda r: parse_vars(r[c9], r[c10]), axis=1)
    
    c11 = [c for c in df.columns if "11." in c][0]
    df_behavior = df[c11].apply(parse_behavior)
    
    c12 = [c for c in df.columns if "12." in c][0]
    df_eeg = df[c12].apply(parse_eeg_areas)
    
    c13, c14 = [c for c in df.columns if "13." in c][0], [c for c in df.columns if "14." in c][0]
    df_tech = df.apply(lambda r: parse_tech(r[c13], r[c14]), axis=1)
    
    c15 = [c for c in df.columns if "15." in c][0]
    df_prep = df[c15].apply(parse_prep)
    
    c17 = [c for c in df.columns if "17." in c][0]
    df_soft = df[c17].apply(parse_software)
    
    c18 = [c for c in df.columns if "18." in c][0]
    df_stat = df[c18].apply(parse_stats)
    
    c19 = [c for c in df.columns if "19." in c][0]
    df_ml = df[c19].apply(parse_ml)

    # FINALIZAR
    df_final = pd.concat([df, df_amostra, df_math, df_vars, df_behavior, df_eeg, df_tech, df_prep, df_soft, df_stat, df_ml], axis=1)
    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Sucesso! Tabela consolidada com {len(df_final.columns)} colunas.")

if __name__ == "__main__":
    main()
