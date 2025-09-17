````markdown
# Corpus Utilities

Utilities to tidy large Tamil corpora before training / RAG.

---

## 1) Punctuation normalization

```python
from tamil_utils.corpus import normalize_punct

s = ' “இது”  ஒரு  சோதனை …  சரி  !  இது  இரண்டாம்  ? '
print(normalize_punct(s))
# -> "இது" ஒரு சோதனை ... சரி! இது இரண்டாம்?
````

* Curly quotes → straight quotes
* Ellipsis `…` → `...` (kept atomic)
* Collapses whitespace
* No space **before** `. ! ? : ;` and closers
* Exactly one space **after** punctuation (unless end of line)

---

## 2) Stable de-duplication

```python
from tamil_utils.corpus import dedup_lines

lines = ["தமிழ் NLP\n", "தமிழ் nlp\n", "  தமிழ் NLP\n", "Tamil nlp\n"]
print(dedup_lines(lines))
# -> ['தமிழ் NLP\n', 'Tamil nlp\n']
```

* First occurrence wins
* `casefold=True`, `strip=True` by default (affects Latin; preserves originals)

---

## 3) Length filters (chars & tokens)

```python
from tamil_utils.corpus import filter_by_length

data = ["இது", "இது ஒரு", "இது ஒரு சோதனை", "சரி!"]
print(list(filter_by_length(data, min_tokens=2, max_tokens=3)))
# -> ['இது ஒரு', 'இது ஒரு சோதனை']
```

* Tokenization uses `tamil_utils.tokens` after NFC normalize
* Combine character and token bounds as needed

---

## 4) Sentence windows for RAG

```python
from tamil_utils.corpus import window_sents

txt = "இது ஒன்று. இது இரண்டு? சரி! முடிந்தது."
print(window_sents(txt, k=2, stride=1))
# -> ['இது ஒன்று. இது இரண்டு?', 'இது இரண்டு? சரி!', 'சரி! முடிந்தது.']
```

* Join `k` sentences per window with a sliding `stride`
* Great for chunking long docs for retrieval pipelines

---

## Tips

* Use `normalize_punct` → `sents` → `window_sents` for clean, chunked inputs.
* For PowerShell piping, prefer UTF-8 files or run `python -X utf8`.

````

---

### Apply & publish
```powershell
git add docs/corpus.md
# add to nav
# mkdocs.yml -> nav:
#   - Corpus: corpus.md
git add mkdocs.yml
git commit -m "docs: add corpus utilities page (normalize_punct, dedup, length filter, windows)"
git push origin main
python -m mkdocs gh-deploy --force
````

Say **next** if you want the optional **CLI shims** (`corpus-dedup`, `corpus-filter`, `corpus-windows`) or we can jump to packaging a **v0.4.0a1** preview release.
