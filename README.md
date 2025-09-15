# tamil-utils

Tiny **Tamil** text utilities: `normalize`, `tokens`, `remove_stopwords`, `graphemes`.

```python
from tamil_utils import normalize, tokens, remove_stopwords, graphemes

s = "இது ஒரு சோதனை 👋🏽"
print(tokens(s))                        # ['இது', 'ஒரு', 'சோதனை']
print(remove_stopwords(tokens(s)))      # ['சோதனை']
print(graphemes("👩🏽‍💻"))               # ['👩🏽‍💻']

```

## Installation
pip install tamil-utils
# Windows CLI (module form avoids PATH issues)
python -m tamil_utils.cli tokens "இது ஒரு சோதனை"

[![PyPI version](https://img.shields.io/pypi/v/tamil-utils)](https://pypi.org/project/tamil-utils/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tamil-utils)
