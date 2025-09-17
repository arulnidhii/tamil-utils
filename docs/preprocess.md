````markdown
# Dataset Preprocessor (JSONL-friendly)

The `preprocess` tools help you clean, segment, and tokenize Tamil text in a **stream-friendly** way for RAG/ML pipelines.

---

## What it does

- **Normalize** (NFC) and optionally harmonize **numerals**
- **Sentence split** (`sents`)
- **Tokenize** (`tokens`)
- Optional **stopword removal** (`tokens_nostop`, Tamil preset)

You get one **JSON object per input line** → ideal for JSONL.

---

## Python API

```python
from tamil_utils.preprocess import (
    PreprocessOptions, preprocess_record, preprocess_lines
)

opts = PreprocessOptions(numerals="ar", rmstop=True)
rec = preprocess_record("இது ஒரு சோதனை ௨௦௨௫", opts)
print(rec)
# {
#   "text": "இது ஒரு சோதனை 2025",
#   "sents": ["இது ஒரு சோதனை 2025"],
#   "tokens": ["இது","ஒரு","சோதனை","2025"],
#   "tokens_nostop": ["சோதனை","2025"]
# }

# Stream lines → records
with open("input.txt","r",encoding="utf-8") as f:
    for r in preprocess_lines(f, opts):
        print(r)
````

---

## CLI

```bash
# stdin → stdout (JSONL)
python -m tamil_utils.cli preprocess --numerals ar --rmstop < input.txt > out.jsonl

# select fields to emit (subset): text,sents,tokens,tokens_nostop
python -m tamil_utils.cli preprocess --emit text,tokens < input.txt > out.jsonl
```

### PowerShell note (Windows)

For correct Tamil I/O when **piping**, either use a UTF-8 file:

```powershell
Set-Content -Path in.txt -Value 'இது ஒரு சோதனை ௨௦௨௫' -Encoding UTF8
Get-Content -Raw -Encoding UTF8 .\in.txt | python -X utf8 -m tamil_utils.cli preprocess --numerals ar --rmstop
```

…or run `python -X utf8` directly when piping.

---

## Options

* `numerals`:

  * `ar` → Tamil digits → ASCII (`௨௦௨௫` → `2025`)
  * `ta` → ASCII → Tamil digits (`123` → `௧௨௩`)
* `rmstop`: also emit `tokens_nostop` (Tamil preset)
* `emit`: comma-separated fields to include (`text,sents,tokens,tokens_nostop`)

---

## When to use

* Prepping corpora for **RAG** / **LLM fine-tuning**
* Building **JSONL** datasets (one line per record)
* Quick, dependency-free preprocessing in data pipelines

```

Add this file, then say **next** and I’ll give you the tiny `mkdocs.yml` nav update + commit/deploy steps.
::contentReference[oaicite:0]{index=0}
```
