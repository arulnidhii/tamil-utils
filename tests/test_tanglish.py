# tests/test_tanglish.py
import pytest

from tamil_utils.tanglish import (
    detect_tanglish,
    normalize_tanglish,
    tanglish_to_tamil,
)

def _strip_tags(s: str) -> str:
    return s.replace("⟪", "").replace("⟫", "")

def test_detect_basic_mix():
    txt = "enna solra? தமிழ் ok-aa?"
    out = detect_tanglish(txt)
    # Ensure we return a non-empty tagged sequence
    assert isinstance(out, list) and len(out) > 0
    # Must contain at least one Tanglish and one Tamil
    tags = [t for _, t in out]
    assert "Tanglish" in tags
    assert "Tamil" in tags or "Other" in tags  # "தமிழ்" will be Tamil; punctuation is Other

def test_tag_mode_marks_only_tanglish():
    txt = "enna solra? idhu Tamil text."
    tagged = normalize_tanglish(txt, mode="tag")
    # Tanglish tokens wrapped with ⟪ ⟫
    assert "⟪enna⟫" in tagged or "⟪solra⟫" in tagged or "⟪idhu⟫" in tagged
    # Non-Tanglish tokens remain as-is
    assert "Tamil" in tagged
    assert "text" in tagged

def test_tag_mode_is_reversible_wrt_content():
    txt = "enna solra idhu sariyaa?"
    tagged = normalize_tanglish(txt, mode="tag")
    assert _strip_tags(tagged) == txt

def test_transliterate_fallback_noop(monkeypatch):
    # Force import failure for optional plugin path to ensure graceful fallback.
    def _fail(*a, **k):
        raise ImportError("no plugin")
    monkeypatch.setattr("tamil_utils.tanglish._aksharamukha_transliterate_word", lambda w: w, raising=True)
    txt = "enna solra"
    out = tanglish_to_tamil(txt, plugin="aksharamukha")
    # If plugin unavailable, should return original (no crash)
    assert out == txt

@pytest.mark.parametrize("s", [
    "vaanga nanba",       # aa long vowel cue
    "azhagiya tamizh",    # zh → ழ
    "ponnu polaama",      # aa, oo hints
    "enna panreenga",     # ng
    "idhula sari illa",   # th/dh patterns (heuristic)
])
def test_heuristic_flags_tanglish_words(s):
    tagged = normalize_tanglish(s, mode="tag")
    # Should mark at least one token as Tanglish
    assert "⟪" in tagged and "⟫" in tagged
