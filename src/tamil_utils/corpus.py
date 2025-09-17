"""
Corpus utilities for Tamil-first text processing.

Includes:
- normalize_punct: quote/ellipsis/spacing harmonization
- dedup_lines: stable de-duplication of text lines
- filter_by_length: character / token length filters
- window_sents: sliding windows of sentences for RAG-style chunks
"""

from __future__ import annotations
from typing import Iterable, Iterator, List, Optional
import regex as re

from .core import normalize, tokens, sents

# --- Punctuation normalization ------------------------------------------------

# Map curly quotes / guillemets / ellipsis to simple ASCII
_PUNCT_MAP = str.maketrans({
    "“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
    "‘": "'", "’": "'", "‚": "'", "‹": "'", "›": "'",
    "…": "...",
})

# commas/periods/etc. where we want "no space before, one space after"
_AFTER_SPACE = r"[,\.\!\?\:\;]"
_BEFORE_SPACE = r"[\(\[\{]"     # openers need a space *after*? not always—leave as-is
_CLOSES = r"[\)\]\}]"

# collapse various whitespace to a single space (excluding newlines)
_WS_RE = re.compile(r"[^\S\r\n]+")

# spaces before/after punctuation
_SPACE_BEFORE_PUNCT_RE = re.compile(rf"\s+({_AFTER_SPACE})")
_SPACE_AFTER_PUNCT_RE = re.compile(rf"({_AFTER_SPACE})(\S)")

_SPACE_BEFORE_CLOSE_RE = re.compile(rf"\s+({_CLOSES})")


def normalize_punct(text: str) -> str:
    """
    Harmonize quotes/ellipsis and tidy common spacing issues around ASCII/Tamil punctuation.

    - Curly quotes/guillemets → straight quotes
    - Ellipsis (…) → "..."
    - Collapse internal whitespace
    - Remove spaces *before* .,!?:; and closers
    - Ensure a single space *after* .,!?:; (unless EOL)
    """
    if not text:
        return text
    s = normalize(text).translate(_PUNCT_MAP)

    # collapse internal spaces (leave newlines)
    s = _WS_RE.sub(" ", s)

    # no space before .,!?;: and closing brackets
    s = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", s)
    s = _SPACE_BEFORE_CLOSE_RE.sub(r"\1", s)

    # exactly one space after .,!?;: if not end of line
    s = _SPACE_AFTER_PUNCT_RE.sub(r"\1 \2", s)

    # trim ends
    return s.strip()


# --- De-duplication -----------------------------------------------------------

def dedup_lines(lines: Iterable[str], *, casefold: bool = True, strip: bool = True) -> List[str]:
    """
    Stable de-duplication of lines.

    Args:
        lines: iterable of text lines
        casefold: if True, casefold key (affects Latin)
        strip: if True, strip key

    Returns:
        List of unique lines preserving first occurrence order.
    """
    seen = set()
    out: List[str] = []
    for line in lines:
        key = line
        if strip:
            key = key.strip()
        if casefold:
            key = key.casefold()
        if key not in seen:
            seen.add(key)
            out.append(line)
    return out


# --- Length filters -----------------------------------------------------------

def filter_by_length(
    texts: Iterable[str],
    *,
    min_chars: Optional[int] = None,
    max_chars: Optional[int] = None,
    min_tokens: Optional[int] = None,
    max_tokens: Optional[int] = None,
) -> Iterator[str]:
    """
    Yield texts that satisfy character/token length constraints.

    Tokens use tamil_utils.tokens() on normalized text.
    """
    for t in texts:
        T = normalize(t)
        if min_chars is not None and len(T) < min_chars:
            continue
        if max_chars is not None and len(T) > max_chars:
            continue
        if min_tokens is not None or max_tokens is not None:
            n = len(tokens(T))
            if min_tokens is not None and n < min_tokens:
                continue
            if max_tokens is not None and n > max_tokens:
                continue
        yield t


# --- Sentence windows for RAG -------------------------------------------------

def window_sents(
    text: str,
    *,
    k: int = 3,
    stride: int = 1,
    join_with: str = " ",
) -> List[str]:
    """
    Slide over sentence list and join K sentences per window.

    Example:
        >>> window_sents("A. B. C. D.", k=2, stride=1)
        ['A. B.', 'B. C.', 'C. D.']
    """
    ss = sents(normalize(text))
    if not ss:
        return []
    out: List[str] = []
    i = 0
    while i + k <= len(ss):
        out.append(join_with.join(ss[i:i+k]))
        i += max(1, stride)
    return out
