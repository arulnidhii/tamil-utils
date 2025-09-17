# Dataset Preprocessor (JSONL-friendly)

The `preprocess` tools help you clean, segment, and tokenize Tamil text in a **stream-friendly** way for RAG/ML pipelines.

---

## What it does

* **Normalize** text to NFC and optionally harmonize **numerals**
* **Sentence split** (`sents`)
* **Tokenize** (`tokens`)
* Optional **stopword removal** (`tokens_nostop`, Tamil preset)

**One JSON object per input line** → ideal for JSONL.

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
with open("input.txt", "r", encoding="utf-8") as f:
    for r in preprocess_lines(f, opts):
        print(r)
```

**Example record (JSON):**

```json
{
  "text": "இது ஒரு சோதனை 2025",
  "sents": ["இது ஒரு சோதனை 2025"],
  "tokens": ["இது", "ஒரு", "சோதனை", "2025"],
  "tokens_nostop": ["சோதனை", "2025"]
}
```

---

## CLI

```bash
# stdin → stdout (JSONL)
python -m tamil_utils.cli preprocess --numerals ar --rmstop < input.txt > out.jsonl

# Select fields to emit (subset of: text,sents,tokens,tokens_nostop)
python -m tamil_utils.cli preprocess --emit text,tokens < input.txt > out.jsonl
```

### PowerShell note (Windows)

When piping Tamil text, prefer a UTF-8 file or use `python -X utf8`:

```powershell
Set-Content -Path in.txt -Value 'இது ஒரு சோதனை ௨௦௨௫' -Encoding UTF8
Get-Content -Raw -Encoding UTF8 .\in.txt | python -X utf8 -m tamil_utils.cli preprocess --numerals ar --rmstop
```

---

## Options

* `numerals`

  * `ar` → Tamil digits → ASCII (e.g., ௨௦௨௫ → 2025)
  * `ta` → ASCII → Tamil digits (e.g., 123 → ௧௨௩)
* `rmstop` – also emit `tokens_nostop` (Tamil preset)
* `emit` – comma-separated fields to include (`text,sents,tokens,tokens_nostop`)

---

## Output Schema

Each processed record is a JSON object:

| Field           | Type             | Description                                         |
| --------------- | ---------------- | --------------------------------------------------- |
| `text`          | string           | Normalized (NFC) text with optional numeral mapping |
| `sents`         | string\[]        | Sentence segments                                   |
| `tokens`        | string\[]        | Word tokens                                         |
| `tokens_nostop` | string\[] (opt.) | Tokens with Tamil stopwords removed (if `rmstop`)   |

---

## When to use

* Preparing corpora for **RAG / LLM fine-tuning**
* Building **JSONL datasets** (one line per record)
* **Quick, dependency-free** preprocessing in data pipelines
