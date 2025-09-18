# src/tamil_utils/tanglish.py
"""
Tanglish (Tamil written in Latin script) detection + optional normalization.

- `detect_tanglish(text)` → list[(token, tag)] where tag ∈ {"Tamil","Latin","Tanglish","Digit","Other"}
- `normalize_tanglish(text, mode="tag"|"transliterate", plugin="aksharamukha")` → str
- `tanglish_to_tamil(text, plugin="aksharamukha")` → str

Heuristics:
- Pure Latin tokens that contain patterns common in informal Tamil romanization
  (e.g., aa, ee, oo, uu for long vowels; zh for ழ; ng/ny; th/dh clusters; ai/au).
- At least one Latin vowel to avoid acronyms.

Optional transliteration plugin:
- If `aksharamukha` is installed (`pip install aksharamukha`), Tanglish tokens
  can be transliterated to Tamil using its “Roman (Colloquial)” → “Tamil” map.
  Falls back gracefully if the package is missing.

Note: We keep this dependency optional to keep tamil-utils lightweight.
"""
from __future__ import annotations

from typing import Iterable, List, Tuple
import regex as re

from .core import normalize, script_of

# --- Tokenization that preserves whitespace & punctuation so we can reassemble ---
#   - words (letters/digits/_), whitespace runs, or a single other char
_SPLIT_RE = re.compile(r"\w+|\s+|[^\w\s]", re.UNICODE)

# Basic shapes
_LATIN_WORD = re.compile(r"^[A-Za-z](?:[A-Za-z'\-]*[A-Za-z])?$")  # allow ' and -
_DIGITS = re.compile(r"^\d+$")

# Heuristic “Tanglish” cues often seen in colloquial Tamil romanization
# (double vowels for length; zh for ழ; ng/ny; th/dh; ai/au diphthongs)
_TANGLISH_HINTS = re.compile(
    r"(aa|ee|oo|uu|zh|ng|ny|nth|th|dh|ai|au)",
    re.IGNORECASE,
)

# Ensure it’s not just consonant clusters; require at least one Latin vowel
_HAS_LATIN_VOWEL = re.compile(r"[aeiou]", re.IGNORECASE)


def _is_tanglish_word(tok: str) -> bool:
    """Return True if token *looks* like Tanglish (Tamil in Latin letters)."""
    if not _LATIN_WORD.match(tok):
        return False
    if not _HAS_LATIN_VOWEL.search(tok):
        return False
    return bool(_TANGLISH_HINTS.search(tok))


def _shape_tag(tok: str) -> str:
    """Classify a single token: Tamil/Latin/Tanglish/Digit/Other."""
    s = tok
    if _DIGITS.match(s):
        return "Digit"
    # Use existing Tamil-vs-Latin detector first
    base = script_of(s)  # "Tamil", "Latin", "Mixed", "Other"
    if base == "Tamil":
        return "Tamil"
    if base == "Latin":
        return "Tanglish" if _is_tanglish_word(s) else "Latin"
    # Mixed or symbols
    return "Other"


def detect_tanglish(text: str) -> List[Tuple[str, str]]:
    """
    Tokenize while preserving separators and tag each piece.
    Returns list of (token, tag) where separators will be tagged as 'Other'.
    """
    text = normalize(text)
    parts = _SPLIT_RE.findall(text)
    out: List[Tuple[str, str]] = []
    for p in parts:
        tag = _shape_tag(p) if p.strip() else "Other"
        out.append((p, tag))
    return out


# ----------------- Optional transliteration backend (plugin) -----------------

def _aksharamukha_transliterate_word(word: str) -> str:
    """
    Transliterate a single *Tanglish* word to Tamil using Aksharamukha, if available.
    We try 'Roman (Colloquial)' → 'Tamil' first, then fall back to 'ISO' → 'Tamil'.
    Returns original word on failure/missing dependency.
    """
    try:
        # Import lazily so the core package stays dependency-free
        from aksharamukha.transliterate import process  # type: ignore
    except Exception:
        return word

    w = normalize(word)
    try:
        # Many users type colloquial romanization; this mapping handles that reasonably well.
        out = process("Roman (Colloquial)", "Tamil", w)  # source, target
        if out and any("\p{Tamil}" in g for g in re.findall(r"\X", out)):
            return out
        # Fallback to ISO if colloquial didn’t convert
        out2 = process("ISO", "Tamil", w)
        return out2 or word
    except Exception:
        return word


def tanglish_to_tamil(text: str, plugin: str = "aksharamukha") -> str:
    """
    Convert Tanglish words in `text` to Tamil using the chosen plugin.
    Unknown plugin or missing dependency → returns original for those tokens.
    """
    parts = detect_tanglish(text)
    out: List[str] = []
    for tok, tag in parts:
        if tag == "Tanglish" and plugin == "aksharamukha":
            out.append(_aksharamukha_transliterate_word(tok))
        else:
            out.append(tok)
    return "".join(out)


# ------------------- User-facing normalization helper -------------------

def normalize_tanglish(
    text: str,
    mode: str = "tag",
    plugin: str = "aksharamukha",
    tag_open: str = "⟪",
    tag_close: str = "⟫",
) -> str:
    """
    If mode == "tag": wrap Tanglish tokens (debug/inspection), leave others unchanged.
    If mode == "transliterate": convert Tanglish tokens to Tamil via `plugin`.
    """
    if mode not in {"tag", "transliterate"}:
        raise ValueError('mode must be "tag" or "transliterate"')

    if mode == "transliterate":
        return tanglish_to_tamil(text, plugin=plugin)

    # mode == "tag"
    parts = detect_tanglish(text)
    out: List[str] = []
    for tok, tag in parts:
        if tag == "Tanglish":
            out.append(f"{tag_open}{tok}{tag_close}")
        else:
            out.append(tok)
    return "".join(out)


# ------------------- Tiny convenience for CLI wiring -------------------

def tag_tanglish(text: str) -> str:
    """Debug helper to mark Tanglish tokens with ⟪…⟫."""
    return normalize_tanglish(text, mode="tag")


def transliterate_tanglish(text: str, plugin: str = "aksharamukha") -> str:
    """Convenience alias for transliteration mode."""
    return normalize_tanglish(text, mode="transliterate", plugin=plugin)
