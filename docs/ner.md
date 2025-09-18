# Named Entity Recognition (NER)

`tamil-utils` includes a thin, Unicode-safe wrapper around a Hugging Face
token-classification model (defaults to **ai4bharat/IndicNER**) and a tiny
evaluation harness for quick checks on public datasets.

> **Why this wrapper?**  
> You get NFC normalization, simple batch APIs, and consistent JSON outputs without
> touching transformers code. It’s optional—install only if you need NER.

---

## Installation

```bash
# core library
pip install tamil-utils

# add NER extras (requires PyPI wheels for transformers/torch on your platform)
pip install "tamil-utils[hf]"
# or explicitly:
# pip install transformers datasets accelerate torch seqeval
````

---

## Python API

```python
from tamil_utils.ner import NERTagger

tagger = NERTagger()  # defaults to ai4bharat/IndicNER
spans = tagger.predict_spans("தமிழ்நாடு அரசு அறிவிப்பு சென்னை இன்று வெளியானது.")
for s in spans:
    print(s.label, s.text, s.start, s.end, f"{s.score:.3f}")

# Or JSON-ready:
print(tagger.predict_json("ராமு TCS நிறுவனத்தில் சென்னை அலுவலகத்தில் உள்ளார்."))
```

**Batching**

```python
texts = [
    "தமிழ்நாடு அரசு அறிவிப்பு சென்னை இன்று வெளியானது.",
    "ராமு TCS நிறுவனத்தில் சென்னை அலுவலகத்தில் உள்ளார்.",
]
batched = tagger.predict_spans_batch(texts)
```

---

## CLI

```bash
# Single input (or pipe via stdin)
python -m tamil_utils.cli ner "தமிழ்நாடு அரசு அறிவிப்பு சென்னை இன்று வெளியானது."

# Use a different model, or force CPU with --device -1
python -m tamil_utils.cli ner --model ai4bharat/IndicNER --device -1 "ராமு TCS நிறுவனத்தில் ..."

# Quick evaluation harness (Naamapadam sample; prints JSONL to stdout)
python -m tamil_utils.cli eval-ner --limit 50 --split validation --lang ta
# save predictions
python -m tamil_utils.cli eval-ner --limit 50 --save-jsonl preds.jsonl
```

**Outputs** (example)

```json
[
  {"label":"LOC","text":"தமிழ்நாடு","start":0,"end":9,"score":0.98},
  {"label":"LOC","text":"சென்னை","start":24,"end":31,"score":0.97},
  {"label":"ORG","text":"TCS","start":6,"end":9,"score":0.95}
]
```

---

## Notes & tips

* **Models & data**
  Default model is **ai4bharat/IndicNER** (multilingual Indic NER). The evaluation
  harness samples from **Naamapadam** (large Indic NER dataset).
* **Normalization**
  The wrapper runs `normalize()` before inference to avoid Unicode edge-cases.
* **Performance**
  For CPU-only environments, set `--device -1`. For GPU, pass CUDA index (e.g., `--device 0`).
* **Licensing & usage**
  Check model/data cards for licenses before shipping to production.

---

## Troubleshooting

* `transformers` not found → install extras: `pip install "tamil-utils[hf]"`.
* Torch/accelerate wheels missing → install a version compatible with your Python/OS/CPU/GPU.
* Slow cold start → first run downloads model weights; reuse the same environment to avoid re-downloads.

---

## Minimal recipe: NER → RAG

1. Preprocess a corpus (normalize, sentence-split),
2. Run `ner` to extract entities per sentence,
3. Store `{text, entities}` in an index (e.g., JSONL → FAISS/Chroma/HF Datasets),
4. Use entities as **filters** or **boosts** for retrieval.

```bash
# toy example: one document per line; get top entities per sentence window
python -m tamil_utils.cli corpus-windows --k 3 --stride 1 --file docs.txt \
| python -m tamil_utils.cli ner --device -1 \
> windows_ner.jsonl
```
