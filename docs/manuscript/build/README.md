# Manuscript build tools

These scripts built `Alves ER et al JMV 2026.docx` (and its tracked-change version) from the draft
`Alves ER et al JVI 2026.docx` and the repository outputs. They are kept so that the content can be
re-synchronised if the analysis changes (for example if the pipeline is rerun without discarded
chikungunya and Zika notifications). They are session tools, not part of the analysis pipeline, and several
paths are absolute for this machine (`PROJECT`, `SKILL` in `build.py`; `ROOT` in `numbers.R` and `recompute.py`).

## What is where

| File | Role |
|---|---|
| `numbers.R` | Computes every number quoted in the text from `db/`, `outputs/`, `source_data/`, `clinical_tables/` into `numbers.csv` (key, value, source). |
| `ms_front.py`, `ms_methods.py`, `ms_results.py`, `ms_discussion.py`, `ms_back.py` | The manuscript text as blocks. Numbers are `{n:key:format}`, state names `{u:key}`, citations `[@r12]`, comment anchors `{c17}...{/c17}`. Unchanged sentences are taken from the draft by paragraph index, so the tracked-change version shows only real edits. |
| `refs.py` | Converts the draft's ASM-style references to NLM/AMA style and holds the new references. |
| `comments_text.py` | Replies to the 20 co-author comments and the author queries (author "Claude for ERA"). |
| `build.py` | Resolves the markup, numbers citations by first appearance, renders the clean and tracked-change documents, assembles the package. |
| `audit.py`, `number_audit.py`, `recompute.py` | Checks: structure, comments, citations, redline = clean; numbers without a source; independent recomputation (Python/numpy) of 40 headline values. |
| `gen_logs.py` | Writes `SYNC_LOG.md`, `JMV_CHECKLIST.md`, `RECORD_CHECKLIST.md`. |
| `extract_markup.py` | Dumps the draft's paragraphs as markup (`orig_markup.txt`). |

## Run order

```powershell
# 0. once: a Python environment with lxml and defusedxml (the docx skill's validator needs them)
uv venv venv ; uv pip install --python venv\Scripts\python.exe lxml defusedxml

# 1. unpack the draft next to the scripts and dump it as markup
python -c "import zipfile; zipfile.ZipFile(r'..\..\..\Alves ER et al JVI 2026.docx').extractall('orig')"
venv\Scripts\python.exe extract_markup.py orig orig_markup.txt

# 2. numbers (R 4.6.1; readxl and data.table are used)
& "C:\Program Files\R\R-4.6.1\bin\Rscript.exe" numbers.R

# 3. build, audit, logs
venv\Scripts\python.exe build.py out
venv\Scripts\python.exe audit.py out
python number_audit.py out
python recompute.py "out\Alves ER et al JMV 2026.docx"      # needs numpy
python gen_logs.py out ..
```

`build.py` imports `comment.py` from the docx skill (`SKILL` path) to write the threaded replies.
The draft's SHA-256, checked at the end of `audit.py`, is `e8e68cf28b2f2074fa27218eb20ce86dc1ab050faab0bb8023174137f6866869`.
