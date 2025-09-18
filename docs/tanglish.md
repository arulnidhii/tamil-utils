````markdown
# Tanglish (Tamil in Latin script)

Many real-world texts mix Tamil script with **Tamil written in Latin letters** (a.k.a. *Tanglish*):  
> “enna solra idhu sariyaa? Tamil ok-aa?”

`tamil-utils` provides:
- **Detection/tagging** of Tanglish tokens (dependency-free)
- **Optional transliteration** of Tanglish → Tamil (via plugin)

This improves downstream **NER, search, RAG, and analytics** by normalizing noisy inputs.

---

## Install

```bash
# Core library (no heavy deps)
pip install tamil-utils

# Optional: enable Tanglish → Tamil transliteration
pip install aksharamukha-transliterate   # plugin used by tamil-utils
````

> If the plugin is missing, transliteration silently falls back to a no-op.
> Detection/tagging works without any extra packages.

---

## Quick start (CLI)

### Detect/mark Tanglish tokens

```bash
python -m tamil_utils.cli tanglish-tag "enna solra? தமிழ் ok-aa?"
# → ⟪enna⟫ ⟪solra⟫? தமிழ் ⟪ok⟫-⟪aa⟫?
```

### Transliterate Tanglish → Tamil (if plugin installed)

```bash
python -m tamil_utils.cli tanglish-2ta "enna solra idhu sariyaa?"
# → என்ன சொல்ற இது சரியா?   (best-effort; depends on input style)
```

**Windows UTF-8 tip for pipes**

```powershell
chcp 65001 > $null; [Console]::InputEncoding=[Text.Encoding]::UTF8; [Console]::OutputEncoding=[Text.Encoding]::UTF8
$env:PYTHONIOENCODING="utf-8"
```

---

## Python API

```python
from tamil_utils.tanglish import detect_tanglish, normalize_tanglish, tanglish_to_tamil

txt = "enna solra? தமிழ் ok-aa?"
tags = detect_tanglish(txt)
# [("enna","Tanglish"), (" ","Other"), ("solra","Tanglish"), ("?","Other"), (" ","Other"),
#  ("தமிழ்","Tamil"), (" ","Other"), ("ok","Tanglish"), ("-","Other"), ("aa","Tanglish"), ("?","Other")]

# Debug/tag mode (wrap Tanglish tokens with ⟪ ⟫)
print(normalize_tanglish(txt, mode="tag"))
# ⟪enna⟫ ⟪solra⟫? தமிழ் ⟪ok⟫-⟪aa⟫?

# Transliterate Tanglish → Tamil (requires aksharamukha-transliterate)
print(tanglish_to_tamil("enna solra idhu sariyaa?"))
```

---

## Modes

* **`mode="tag"`**: Non-destructive; wraps Tanglish tokens as `⟪token⟫`.
  Use for inspection or to branch pipeline logic.

* **`mode="transliterate"`**: Converts Tanglish tokens to Tamil using a plugin
  (default: **Aksharamukha**, if installed). Tokens not recognized or plugin-less inputs are left as-is.

---

## Heuristics (detection)

A token is marked **Tanglish** if:

* It is **pure Latin** (no Tamil codepoints), **contains a vowel**, and
* Matches **common romanization cues**: `aa` `ee` `oo` `uu`, `zh` (ழ), `ng`, `ny`, `th`/`dh`, `ai`, `au`, etc.

These rules are intentionally conservative and **language-aware** (Tamil vs generic Latin).

---

## Quality & caveats

* Transliteration is **best-effort**. Colloquial spellings vary; perfect 1-1 mapping isn’t guaranteed.
* Acronyms, brand names, or English words in Latin remain **Latin** (not Tanglish) unless they look like Tamil romanization.
* Keep a human review loop for high-stakes pipelines (e.g., legal/government documents).

---

## Recipes

### 1) Clean → detect → transliterate → preprocess

```bash
# Example: sentence windows with normalized Tanglish, then NER
cat docs.txt \
| python -m tamil_utils.cli tanglish-2ta \
| python -m tamil_utils.cli corpus-windows --k 3 --stride 1 \
| python -m tamil_utils.cli ner --device -1 \
> windows_ner.jsonl
```

### 2) Branch by tag density (Python)

```python
from tamil_utils.tanglish import detect_tanglish, tanglish_to_tamil
from tamil_utils import preprocess

s = "enna solra? இது ஒரு சோதனை"
pairs = detect_tanglish(s)
tanglish_ratio = sum(1 for _, t in pairs if t=="Tanglish") / max(1, sum(1 for _, t in pairs if _.strip()))
if tanglish_ratio > 0.2:
    s = tanglish_to_tamil(s)  # normalize only if heavy Tanglish
rec = preprocess.preprocess_record(s)
```

---

## Troubleshooting

* **Transliteration didn’t change text** → install plugin:

  ```bash
  pip install aksharamukha-transliterate
  ```
* **Mixed Tamil+Latin words** may be tagged `Other` (not transliterated).
  Consider splitting punctuation and retrying, or rely on `preprocess` tokens.

---

## See also

* [Preprocess](./preprocess.md) – normalization → sentences → tokens → numerals/stopwords
* [NER](./ner.md) – entity extraction for Tamil (IndicNER wrapper)

````