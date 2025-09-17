# Recipes

Copy-pasteable pipelines for apps, data prep, and RAG.

---

## 1) Quick clean → JSONL (CLI)

```bash
# Normalize punctuation, then preprocess to JSONL with numerals harmonized
# One record per line: {"text","sents","tokens","tokens_nostop"}
python -m tamil_utils.cli preprocess --numerals ar --rmstop < input.txt > out.jsonl
```

**Tip (Windows PowerShell, UTF-8):**

```powershell
Set-Content in.txt -Value '“இது”  ஒரு  சோதனை …  சரி!' -Encoding UTF8
Get-Content -Raw -Encoding UTF8 .\in.txt | python -X utf8 -m tamil_utils.cli preprocess --numerals ar --rmstop
```

---

## 2) Deduplicate + filter before preprocessing (CLI)

```bash
# Remove duplicates (stable order)
python -m tamil_utils.cli corpus-dedup --file raw.txt > uniq.txt

# Keep medium-sized lines (2–50 tokens)
python -m tamil_utils.cli corpus-filter --file uniq.txt --min-tokens 2 --max-tokens 50 > kept.txt

# Convert to JSONL records
python -m tamil_utils.cli preprocess --numerals ar --rmstop < kept.txt > data.jsonl
```

---

## 3) RAG chunks via sentence windows (CLI)

```bash
# Windows of 3 sentences with stride 1 (overlapping chunks)
python -m tamil_utils.cli corpus-windows --k 3 --stride 1 --file doc.txt > chunks.txt

# (optional) Further normalize / tokenize per chunk
python -m tamil_utils.cli preprocess --numerals ar --rmstop < chunks.txt > chunks.jsonl
```

---

## 4) End-to-end in Python: clean → window → HF Dataset

```python
import json
from tamil_utils.corpus import normalize_punct, window_sents
from tamil_utils.preprocess import PreprocessOptions, preprocess_record
from tamil_utils.hf_export import to_hf_dataset  # pip install datasets

text = ' “இது”  ஒரு  சோதனை …  சரி! இது இரண்டாம்? '
clean = normalize_punct(text)
wins = window_sents(clean, k=2, stride=1)     # sentence windows

opts = PreprocessOptions(numerals="ar", rmstop=True, emit=["text","tokens","tokens_nostop"])
records = [preprocess_record(w, opts) for w in wins]

ds = to_hf_dataset(records)
print(ds)
# save to disk for training later:
#   from tamil_utils.hf_export import save_hf_dataset
#   save_hf_dataset(ds, "out_ds")
```

---

## 5) Minimal training JSONL (keep only `"text"`)

If you only need `text` for LM/RAG ingestion:

```bash
python -m tamil_utils.cli preprocess --numerals ar --emit text < input.txt > text_only.jsonl
```

Each line:

```json
{"text": "இது ஒரு சோதனை 2025"}
```

---

## 6) spaCy tokenizer hook (optional)

Mirror `tamil_utils.tokens` inside spaCy:

```python
import spacy
from tamil_utils.spacy_hook import install_tamil_tokenizer

nlp = spacy.blank("xx")            # language-agnostic
install_tamil_tokenizer(nlp)       # NFC-normalizes and replaces tokenizer
doc = nlp("இது ஒரு சோதனை 2025")
print([t.text for t in doc])       # ['இது','ஒரு','சோதனை','2025']
```

Install:

```bash
pip install "tamil-utils[spacy]"
```

---

## 7) N-gram counts for quick analysis

```bash
python -m tamil_utils.cli freq -n 1 --top 20 "தமிழ் NLP தமிழ் பயன்பாடு"
python -m tamil_utils.cli freq -n 2 --top 10 "தமிழ் NLP தமிழ் NLP"
```

Programmatically:

```python
from tamil_utils import word_counts
print(word_counts("தமிழ் NLP தமிழ் NLP", n=2, top=3))
```

---

## 8) Sorting titles in Tamil order

```python
from tamil_utils import sort_tamil
titles = ["இலங்கை", "ஆதி", "அடி"]
print(sort_tamil(titles))  # ['அடி', 'ஆதி', 'இலங்கை']
```

For strict, locale-aware collation (libraries, catalogs), use ICU (`PyICU`) and **fallback** to `sort_tamil`.

---

## 9) Common gotchas

* **Encoding:** prefer UTF-8 files and `python -X utf8` when piping on Windows.
* **Normalization:** mixed corpora benefit from `normalize_punct` before `sents`/`window_sents`.
* **Stopwords:** Tamil preset is pragmatic, not exhaustive—tune for your domain.

---

## 10) Tiny checklists

**RAG prep (docs → chunks → JSONL):**

1. `normalize_punct(doc)`
2. `window_sents(..., k=3, stride=1)`
3. `preprocess_record(chunk, numerals='ar', rmstop=True)`
4. (optional) `to_hf_dataset(records)`

**Corpus cleanup (CLI):**

```bash
python -m tamil_utils.cli corpus-dedup --file raw.txt \
| python -m tamil_utils.cli corpus-filter --min-tokens 2 --max-tokens 50 \
| python -m tamil_utils.cli preprocess --numerals ar --rmstop > data.jsonl
```
