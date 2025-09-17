# spaCy Tokenizer Hook (optional)

`tamil-utils` can install a **Tamil-aware spaCy tokenizer** so tokenization matches `tamil_utils.tokens`.
It also normalizes input to **Unicode NFC**.

---

## Quick start

```python
import spacy
from tamil_utils.spacy_hook import install_tamil_tokenizer

nlp = spacy.blank("xx")           # use spaCy's multi-language pipeline
install_tamil_tokenizer(nlp)      # replaces nlp.tokenizer; normalizes to NFC

doc = nlp("இது ஒரு சோதனை 2025")
print([t.text for t in doc])      # ['இது','ஒரு','சோதனை','2025']
```

---

## Install

```bash
pip install "spacy>=3.6,<4"
# or, if you've enabled extras in your pyproject:
pip install "tamil-utils[spacy]"
```

---

## Notes

* **Language**: `spacy.blank("xx")` (multi-language) is recommended.
  If you already have a pipeline (e.g., `en_core_web_sm`), call `install_tamil_tokenizer(nlp)` **after** loading it to replace its tokenizer.
* **What it changes**: Only `nlp.tokenizer` is replaced. Other pipeline components (tagger, parser, etc.) are untouched.
* **Normalization**: Text is normalized to NFC before tokenization to ensure consistent Tamil segmentation.

---

## Restore default tokenizer (optional)

If you need to revert to spaCy’s default tokenizer:

```python
from spacy.tokenizer import Tokenizer
nlp.tokenizer = Tokenizer(nlp.vocab)
```
