## Core API

```python
from tamil_utils import (
    normalize, tokens, remove_stopwords, graphemes, sents,
    to_arabic_numerals, to_tamil_numerals, syllables, sort_tamil, word_counts
)

s = "இது ஒரு சோதனை 👩🏽‍💻 ௨௦௨௫"

print(tokens(s))                                # ['இது','ஒரு','சோதனை','👩🏽‍💻','௨௦௨௫']
print(remove_stopwords(tokens(s), preset="ta")) # ['சோதனை','👩🏽‍💻','௨௦௨௫']
print(graphemes("👩🏽‍💻"))                       # ['👩🏽‍💻']
print(sents("இது ஒன்று. இது இரண்டு? சரி!"))      # ['இது ஒன்று.', 'இது இரண்டு?', 'சரி!']
print(to_arabic_numerals("௨௦௨௫"))                 # "2025"
print(to_tamil_numerals("123"))                  # "௧௨௩"
print(syllables("தமிழ்"))                         # approx syllables
print(sort_tamil(["இலங்கை","ஆதி","அடி"]))         # ['அடி','ஆதி','இலங்கை']
```

---

## Useful CLIs

```bash
# n-gram counts (unigram/bigram/trigram)
python -m tamil_utils.cli freq -n 2 --top 5 "தமிழ் NLP தமிழ் NLP"

# Tamil collation via ISO-15919 key
python -m tamil_utils.cli sort "இலங்கை" "ஆதி" "அடி"
```

---

## Preprocess (JSONL)

```bash
python -m tamil_utils.cli preprocess --numerals ar --rmstop < input.txt > out.jsonl
```

### Windows PowerShell

Use UTF-8 when piping:

```powershell
Set-Content in.txt -Value 'இது ஒரு சோதனை ௨௦௨௫' -Encoding UTF8
Get-Content -Raw -Encoding UTF8 .\in.txt | python -X utf8 -m tamil_utils.cli preprocess --numerals ar --rmstop
```

---

## Optional integrations

### spaCy tokenizer hook

```python
import spacy
from tamil_utils.spacy_hook import install_tamil_tokenizer

nlp = spacy.blank("xx")
install_tamil_tokenizer(nlp)
[t.text for t in nlp("இது ஒரு சோதனை 2025")]  # ['இது','ஒரு','சோதனை','2025']
```

### Hugging Face Datasets

```python
from tamil_utils.hf_export import to_hf_dataset  # pip install datasets

records = [{"text": "இது ஒரு சோதனை 2025",
            "tokens": ["இது","ஒரு","சோதனை","2025"]}]
ds = to_hf_dataset(records)
print(ds)
```
