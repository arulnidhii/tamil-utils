# Hugging Face Datasets (optional)

`tamil-utils` can convert your preprocessed JSONL-like records into a Hugging Face **`datasets.Dataset`** and save/reload it for RAG/ML pipelines.

> Install when needed:
>
> ```bash
> pip install datasets
> ```

---

## From Python records

```python
from tamil_utils.hf_export import to_hf_dataset, save_hf_dataset

records = [
    {"text": "இது ஒரு சோதனை 2025", "tokens": ["இது", "ஒரு", "சோதனை", "2025"]},
    {"text": "தமிழ் NLP", "tokens": ["தமிழ்", "NLP"]},
]

ds = to_hf_dataset(records)     # -> datasets.Dataset
save_hf_dataset(ds, "out_ds")   # saves Arrow dataset to disk

# later:
import datasets
reloaded = datasets.load_from_disk("out_ds")
print(len(reloaded), reloaded[0]["text"])
```

---

## From a JSONL preprocess stream

First, build JSONL with the `tamil-utils` preprocessor:

```bash
python -m tamil_utils.cli preprocess --numerals ar --rmstop < input.txt > out.jsonl
```

Then load the JSONL into a Dataset:

```python
import json
from tamil_utils.hf_export import to_hf_dataset

with open("out.jsonl", "r", encoding="utf-8") as f:
    records = (json.loads(line) for line in f if line.strip())

ds = to_hf_dataset(records)
print(ds)
```

---

### Tips

* Keep only the fields you need for training (e.g., `text`, `tokens`) to reduce disk/memory footprint.
* Keys in your JSON/records become **columns** in the resulting `datasets.Dataset`.
