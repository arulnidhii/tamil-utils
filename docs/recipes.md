# Examples & Recipes

A few practical “copy-paste” workflows for `tamil-utils`.

---

## 1) Clean → Tokenize → Stopwords → N-grams → Frequency → Sort

### Python

```python
from tamil_utils import tokens, remove_stopwords, ngrams, word_counts, sort_tamil

text = "தமிழ் NLP தமிழ் பயன்பாடு தமிழ் NLP"

tok = tokens(text)
tok_nostop = remove_stopwords(tok, preset="ta")

# bigrams
bigs = [" ".join(g) for g in ngrams(tok_nostop, 2)]
print(bigs)

# top-2 bigrams by frequency
print(word_counts(text, n=2, top=2))

# sort Tamil words (lightweight collation)
print(sort_tamil(["இலங்கை", "ஆதி", "அடி"]))
```

### CLI

```bash
python -m tamil_utils.cli tokens --rmstop "தமிழ் NLP தமிழ் பயன்பாடு தமிழ் NLP"
python -m tamil_utils.cli ngrams -n 2 "தமிழ் NLP தமிழ் பயன்பாடு தமிழ் NLP"
python -m tamil_utils.cli freq -n 2 --top 2 "தமிழ் NLP தமிழ் பயன்பாடு தமிழ் NLP"
python -m tamil_utils.cli sort இலங்கை ஆதி அடி
```

---

## 2) Sentence splitting + numerals

```python
from tamil_utils import sents, to_arabic_numerals, to_tamil_numerals

print(sents("இது ஒன்று. இது இரண்டு? சரி!"))
print(to_arabic_numerals("௨௦௨௫"))  # -> "2025"
print(to_tamil_numerals("123"))    # -> "௧௨௩"
```

---

## 3) Script detection + transliteration

```python
from tamil_utils import tokens, token_scripts, transliterate_iso15919

print(token_scripts(tokens("கோட்123 hello")))
# Example output: [("கோட்123", "Mixed"), ("hello", "Latin")]

print(transliterate_iso15919("தமிழ்"))  # -> "tamiḻ"
print(transliterate_iso15919("ஆதி"))   # -> "ādi"
```

---

## 4) Syllables (approximate, grapheme-based)

```python
from tamil_utils import syllables

print(syllables("தமிழ்🙂 test 123"))  # Processes Tamil clusters; ignores non-Tamil
```

---

## 5) Simple text stats

```python
from tamil_utils import word_counts

text = "இது ஒரு சோதனை இது ஒரு சோதனை"
print(word_counts(text, rmstop=True, preset="ta", n=1))
# -> [("சோதனை", 2)]
```

---

## Notes & Tips

* **Collation**: `sort_tamil` uses a lightweight ISO-15919 key. For strict collation (ICU), keep ours as default and layer ICU in your app if needed.
* **Stopwords**: You can pass your own set to `remove_stopwords(tokens, stopwords=my_set)`.
* **Performance**: For large corpora, stream line-by-line and aggregate `word_counts` periodically.

---