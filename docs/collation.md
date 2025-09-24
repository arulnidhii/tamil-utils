# Collation (Sorting) for Tamil

`tamil-utils` provides a lightweight collation via `sort_tamil()`.  
It builds a stable sort key from ISO-15919 transliteration so words sort *roughly* as native Tamil order:

a < ā < i < ī < u < ū < e < ē < ai < o < ō < au


This is **deterministic** and **dependency-free**, suitable for most app and data tasks.  
It is **not** a full Tamil Collation Algorithm (TCA) and does not depend on ICU.

---

## Quick usage

```python
from tamil_utils import sort_tamil

words = ["இலங்கை", "ஆதி", "அடி"]
print(sort_tamil(words))   # ['அடி', 'ஆதி', 'இலங்கை']

Yes. That section **is part of `docs/collation.md`** right after “Quick usage”.

Here’s the exact block to paste (properly fenced):

````markdown
## When you need strict, locale-aware collation

If your product requires exact linguistic collation for Tamil (e.g., official indexes, libraries), use **ICU** where available and fall back to `sort_tamil()`.

### Python (PyICU) with fallback

```python
def sort_tamil_strict(words):
    try:
        from icu import Collator, Locale
        coll = Collator.createInstance(Locale("ta_IN"))
        return sorted(words, key=coll.getSortKey)
    except Exception:
        from tamil_utils import sort_tamil
        return sort_tamil(words)

words = ["இலங்கை", "ஆதி", "அடி"]
print(sort_tamil_strict(words))
````

> Install: `pip install PyICU` (platform-specific wheels may apply).
> Keep `tamil-utils` default lightweight; add ICU only if your deployment needs it.

```