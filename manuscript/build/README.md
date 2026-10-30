# Manuscript build tools

These scripts built `Alves ER et al JMV 2026.docx` (and its tracked-change version) from the draft
`Alves ER et al JVI 2026.docx`, the file as the authors edited it on 2026-10-22 (their comments and their
deletions are kept), and the repository outputs. They are kept so that the content can be re-synchronised if the
analysis changes. They are manual tools, not part of the analysis pipeline. Paths inside the repository are derived from the
location of the scripts (`manuscript/build/`); the only machine-specific path left is the docx skill that writes the comments
(`SKILL` in `build.py`; set the environment variable `DOCX_SKILL_DIR` on another machine).

Round 1 (2026-10-21) formatted the draft for the Journal of Medical Virology and synchronised it with the 2016–2026
analysis. Round 2 (2026-10-22) applied the eight instructions tagged "@claude for ERA": case definition (all
notifications not classified as discarded, for the three diseases), SINAN downloaded again with 2026 capped at
2026-09-30, a pooled lagged model, DLNM removed, figures numbered by order of citation, 2026 qualified wherever it is used.

## What is where

| File | Role |
|---|---|
| `numbers.R` | Computes every number quoted in the text from `db/`, `outputs/<topic>/`, `source_data/`, `clinical_tables/`, `raw/sources_manifest.csv` into `numbers.csv` (key, value, source). |
| `ms_front.py`, `ms_methods.py`, `ms_results.py`, `ms_discussion.py`, `ms_back.py` | The manuscript text as blocks. Numbers are `{n:key:format}`, state names `{u:key}`, figure numbers `{F:key}` (capitalized "Figure N") and `{f:key}` (number only), citations `[@r12]`, comment anchors `{c17}...{/c17}`. Unchanged sentences are taken from the draft by paragraph index, so the tracked-change version shows only real edits. Each module also holds an `ASSERT` list: statements the prose makes about the data (who trends, which model peaks at which lag), evaluated against `numbers.csv` at build time. |
| `figmap.py` | Numbers the figures by order of first citation in the text and checks that the order is monotonic; maps each manuscript number to the repository files. |
| `refs.py` | Converts the draft's ASM-style references to NLM/AMA style and holds the new references. |
| `comments_text.py` | Round-2 replies of "Claude for ERA" inside the threads (the authors' instructions sit in the same threads) and the threads to close. |
| `build.py` | Resolves the markup, numbers citations and figures by first appearance, runs the build-time checks (assertions; every paragraph that mentions 2026 must say January–September and annualized/partial; no DLNM), renders the clean and tracked-change documents, assembles the package. |
| `audit.py`, `number_audit.py`, `recompute.py` | Checks: structure; all comments of the authors' edited file kept unchanged and the deleted ones not restored; citations; redline accepted = clean; numbers without a source; independent recomputation (Python/numpy) of 43 headline values. |
| `gen_captions.py` | Writes `manuscript/FIGURE_CAPTIONS.md` from `outputs/figure_notes/figure_caption_values.csv`, `figure_exclusions_captions.txt` and `numbers.csv`. |
| `gen_logs.py` | Writes `SYNC_LOG.md`, `JMV_CHECKLIST.md`, `RECORD_CHECKLIST.md` (and the figure map). |
| `extract_markup.py` | Dumps the draft's paragraphs as markup (`orig_markup.txt`). |
| `export_figures.py` | Copies the final figures under their manuscript numbers into `manuscript/figures/` (mapping from `build_report.json`). |

## Run order

```powershell
# 0. once: a Python environment with lxml and defusedxml (the docx skill's validator needs them)
uv venv venv ; uv pip install --python venv\Scripts\python.exe lxml defusedxml pymupdf numpy

# 1. unpack the inputs next to the scripts
# the original draft is in manuscript/ (audit.py also accepts it at the repository root)
python -c "import zipfile; zipfile.ZipFile(r'..\Alves ER et al JVI 2026.docx').extractall('orig')"
copy ..\"Alves ER et al JVI 2026.docx" original.docx
python -c "import zipfile,glob; zipfile.ZipFile(glob.glob(r'..\history\*authors edit*.docx')[0]).extractall('user')"
venv\Scripts\python.exe extract_markup.py orig orig_markup.txt

# 2. numbers (R 4.6.1; readxl and data.table are used), then the legends
& "C:\Program Files\R\R-4.6.1\bin\Rscript.exe" numbers.R
python gen_captions.py ..\.. numbers.csv

# 3. build, audit, logs
venv\Scripts\python.exe build.py out
venv\Scripts\python.exe audit.py out
python number_audit.py out
python recompute.py "out\Alves ER et al JMV 2026.docx"      # needs numpy
python gen_logs.py out ..
python export_figures.py out                                  # refresh manuscript\figures
```

`orig/`, `user/`, `out/`, `venv/`, `orig_markup.txt` and `original.docx` are scratch files; `.gitignore` keeps them out of git.

`build.py` imports `comment.py` from the docx skill (`SKILL` path) to write the threaded replies and builds on the comment
parts of the `user/` folder (the authors' edited file), so their comments and deletions are preserved. The draft's
SHA-256, checked at the start of `audit.py`, is `e8e68cf28b2f2074fa27218eb20ce86dc1ab050faab0bb8023174137f6866869`.

The renamed figure copies in `../figures/` (written by `export_figures.py`) are `Figure<N>.png` for the manuscript number N (mapping in `../SYNC_LOG.md`, section 8);
the pipeline keeps its own file names in `figures/`.
