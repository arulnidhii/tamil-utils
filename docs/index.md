# tamil-utils

Small, production-ready **Tamil-first** text layer.

* Normalization & graphemes
* Tamil-aware tokens
* Stopwords preset, sentence splitter, numerals
* Syllables (approx), Tamil collation (ISO-15919 key)
* **v0.1** adds: script detection, ISO-15919 transliteration
* **v0.3 (alpha)** adds: **JSONL preprocessor**, **spaCy tokenizer hook** (optional), **Hugging Face Datasets** export (optional)

---

## Install

```bash
pip install tamil-utils

# optional extras
pip install "tamil-utils[spacy]"   # spaCy tokenizer hook
pip install datasets               # Hugging Face helper
```

---

## CLI quickstart

```bash
# sentence split
python -m tamil_utils.cli sents "இது ஒரு வாக்கியம். இது இரண்டாம்? சரி!"

# Tamil ↔ ASCII numerals
python -m tamil_utils.cli to-arabic "௨௦௨௫"   # -> 2025
python -m tamil_utils.cli to-tamil "123"     # -> ௧௨௩

# word/n-gram counts
python -m tamil_utils.cli freq -n 2 --top 5 "தமிழ் NLP தமிழ் NLP"

# JSONL preprocessor (one record per line)
python -m tamil_utils.cli preprocess --numerals ar --rmstop < input.txt > out.jsonl
```

### Windows note

When piping Tamil text in PowerShell, prefer UTF-8 files or run with `python -X utf8`. See **Preprocess** page for examples.

---

## Links

* **Usage** – examples of the core API & CLI → [`usage.md`](./usage.md)
* **API** – functions and signatures → [`api.md`](./api.md)
* **Recipes** – common tasks for apps & data → [`recipes.md`](./recipes.md)
* **Collation** – how `sort_tamil` orders words → [`collation.md`](./collation.md)
* **Preprocess** – JSONL pipeline for RAG/ML → [`preprocess.md`](./preprocess.md)
* **spaCy** – optional tokenizer hook → [`spacy.md`](./spacy.md)
* **Hugging Face** – optional dataset helper → [`hf.md`](./hf.md)
