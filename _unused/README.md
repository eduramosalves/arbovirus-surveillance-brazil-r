# Unused files

Files that no script, document or figure uses any more. Nothing was deleted: each file sits here under the path it had in the
repository, so putting it back is one command, for example

```bash
git mv "_unused/docs/RESULTS_SUMMARY.md" docs/RESULTS_SUMMARY.md
```

Moved on 2026-10-22 (full old → new list of the reorganisation: [`docs/CLEANUP_2026-10-22.md`](../docs/CLEANUP_2026-10-22.md)).

| Path under `_unused/` | What it is | Why it is here |
|---|---|---|
| `Claude outputs/RELATORIO_REVISAO_SOFIA.docx` | Copy of the co-author review report | Byte-identical to `docs/RELATORIO_REVISAO_SOFIA.docx`; nothing read the folder |
| `Claude outputs/build_docx.js` | Node script that wrote that report | Writes to a sandbox path (`/mnt/user-data/outputs/`) and cites scripts that no longer exist |
| `docs/RELATORIO_REVISAO_SOFIA.docx`, `docs/RELATORIO_REVISAO_SOFIA.R`, `docs/VERIFICACAO_RELATORIO_SOFIA.md` | The co-author review of the earlier results and the check of its flagged items | Record of a past review; no script or document uses them |
| `docs/RESULTS_SUMMARY.md`, `docs/RESULTS_SUMMARY.html` | Narrative of the original 2016–2025 analysis | Superseded by the regenerated results; the HTML gallery pointed at figure names that no longer exist |
| `docs/README_original.md` | README of the Python-era project | Historical; its links were already broken |
| `outputs/Dengue_02_ELISA.png` | Old "ELISA" figure, 2016–2025 | Replaced by `outputs/clinical/Dengue_02_NS1.png` (the panel is the NS1 antigen result, 2016–2026) |
| `outputs/Dengue_00_general_data.csv` | 74-column "General Data" sheet of the GraphPad file | No current script writes it; the clinical tables have no such sheet |
| `reference/graphpad_data/*.pzfx`, `db/graphpad_data/*.pzfx` | The three GraphPad Prism files that fed the clinical figures until 2026-10-22 | Figures 5, 7, 8 now come from `clinical_tables/`; the reader and the copy step were removed from the code |

The GraphPad files are the only input of the old clinical figures. Keep them if you want to compare the old and new clinical
numbers; they are not needed to run the project.
