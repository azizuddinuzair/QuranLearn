# Data Conversion

Use [convert_quran_md.py](convert_quran_md.py) to merge the downloaded Quran-MD train shards into app-friendly outputs.

## Prerequisites

1. If the shard files are Git LFS pointers, fetch the real blobs first:
   `git lfs install`
   `git lfs pull`
2. Install the Python packages used by the converter:
   `/Users/azizuddinson/Documents/GitHub/QuranLearn/.venv/bin/pip install pandas pyarrow`

## Run

Generate CSV, JSONL, and SQLite outputs in `data/processed`:

```bash
/Users/azizuddinson/Documents/GitHub/QuranLearn/.venv/bin/python workflow/scripts/convert_quran_md.py
```

Generate only JSONL and SQLite:

```bash
/Users/azizuddinson/Documents/GitHub/QuranLearn/.venv/bin/python workflow/scripts/convert_quran_md.py --formats jsonl sqlite
```

Keep the `audio` column for JSONL or SQLite exports:

```bash
/Users/azizuddinson/Documents/GitHub/QuranLearn/.venv/bin/python workflow/scripts/convert_quran_md.py --formats jsonl sqlite --keep-audio
```

## Outputs

- `data/processed/quran_words.csv`
- `data/processed/quran_words.jsonl`
- `data/processed/quran_words.sqlite`

The script prints row count, selected columns, and duplicate `word_id` count before writing files.