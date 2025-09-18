from .core import (
    normalize,
    tokens,
    remove_stopwords,
    graphemes,
    sents,
    to_arabic_numerals,
    to_tamil_numerals,
    stopwords_preset,
    script_of,
    token_scripts,
    transliterate_iso15919,
    syllables,          # v0.2
    sort_tamil,         # v0.2
)

# --- v0.2: counts / n-grams (kept in a separate module to keep core lean) ---
from .v02_counts import (
    ngrams,
    bigrams,
    trigrams,
    word_counts,
)

# --- v0.3: preprocess pipeline (JSONL-friendly record) ---
from .preprocess import (
    PreprocessOptions,
    preprocess_record,
)

# --- v0.4: corpus helpers (lightweight, no heavy deps) ---
from .corpus import (
    normalize_punct,
    window_sents,       # sentence windows for RAG
)

# --- v0.5: Tanglish (dependency-free detection; optional translit plugin at call time) ---
from .tanglish import (
    detect_tanglish,
    normalize_tanglish,
    tanglish_to_tamil,
)

__all__ = [
    # core
    "normalize",
    "tokens",
    "remove_stopwords",
    "graphemes",
    "sents",
    "to_arabic_numerals",
    "to_tamil_numerals",
    "stopwords_preset",
    "script_of",
    "token_scripts",
    "transliterate_iso15919",
    "syllables",
    "sort_tamil",
    # v0.2 counts / n-grams
    "ngrams",
    "bigrams",
    "trigrams",
    "word_counts",
    # v0.3 preprocess
    "PreprocessOptions",
    "preprocess_record",
    # v0.4 corpus
    "normalize_punct",
    "window_sents",
    # v0.5 tanglish
    "detect_tanglish",
    "normalize_tanglish",
    "tanglish_to_tamil",
]
