# Arbovirus Surveillance in Brazil — 2016–2026 (updated, self-contained)

Reproducible statistical and geospatial analysis of **Dengue, Chikungunya, and Zika**
notifications across the **27 Brazilian federative units**, monthly, **2016–2026**.

A reproducible **R** project: the code that turns the raw official files into every table and
figure, the cleaned analysis tables (`db/`), and the generated results. Clone it anywhere and run
one script; no paths need editing. **New here? Start with [`docs/GUIDE.md`](docs/GUIDE.md).**

> **Raw data are not stored in this repository** (`raw/`, about 1.7 GB). On a fresh clone, run with
> `--skip-etl`: it rebuilds every result from the committed `db/`. To rebuild `db/` itself, see
> [Raw data](#raw-data) below.

## Quick start
The project is written in **R** (R ≥ 4.5; https://cloud.r-project.org). No Rtools or Python needed.
```powershell
# Windows
powershell -ExecutionPolicy Bypass -File run_all.ps1
```
```bash
# macOS / Linux / Git Bash
bash run_all.sh
```
```r
# or from any R session / RStudio
system("Rscript run_all.R")      # run_all.R accepts --skip-etl and --skip-install
```
The script installs any missing CRAN packages (`R/install_packages.R`, binary builds; the
versions used are recorded in `docs/R_SESSION_INFO.txt`), then runs:

| Step | Command | Produces |
|---|---|---|
| 1 | `etl/build_db.R` | `db/` + `clinical_tables/` from `raw/` (checked against `reference/expected_hashes.csv`) |
| 2 | `pipelines/run_all.R` | 9 core stages → `outputs/<topic>/`, `figures/<kind>/` |
| 3 | `pipelines/additional/run_additional_analyses.R` | `outputs/additional/` |
| 4 | `pipelines/alt_results.R` | `figures/alternatives/` |
| 5 | `pipelines/build_source_data.R` | `source_data/` (one xlsx per figure) |

Flags: `-SkipEtl` / `--skip-etl` reuse an existing `db/`; `-SkipInstall` / `--skip-install`
skip the package check. Step 1 streams ~5.8 GB of uncompressed SINAN records and ~1.1 GB of
INMET zips (about 3 minutes); the whole run takes about 7 minutes.

The project was ported from Python to R on 2026-10-09. The rebuilt `db/` is byte-identical to the
Python build, and the statistics match the Python results; the few expected differences
(permutation p-values, bootstrap draws, …) are listed in [`docs/R_PORT_NOTES.md`](docs/R_PORT_NOTES.md).

- **Data window:** 2016–2026 (CHIKV now includes 2016; 2026 is season-to-date, Jan–Sep, annualised in the annual results)
- **Spatial unit:** 27 federative units (UF) · **Temporal unit:** monthly
- **Generated:** 2026-10-22 (SINAN downloaded 2026-10-22; 2026 files = release of 2026-10-20, notifications up to 2026-09-30)

The repository ships with the results already generated (`db/`, `clinical_tables/`, `outputs/`,
`figures/`, `source_data/`). `run_all.R --skip-etl` regenerates them from `db/`; the full run first
rebuilds `db/` from `raw/`. Output file names
keep their original names (e.g. `py_statistical_results.xlsx`, `py_01_*.png`) so references in
the papers and older notes stay valid. They are grouped in sub-folders by topic (see [Folder layout](#folder-layout)).

## What changed on 2026-10-22
The repository was also reorganised that day: results grouped by topic (`outputs/<topic>/`, `figures/<kind>/`), the manuscript
material gathered in `manuscript/`, and everything unused moved to `_unused/`. Nothing was deleted; the old-to-new path list is in
[`docs/CLEANUP_2026-10-22.md`](docs/CLEANUP_2026-10-22.md).

| Item | Before | Now |
|---|---|---|
| Case definition | dengue: all notifications minus discarded; chikungunya and Zika: **all notifications, discarded included** | **all three: all notifications minus discarded** (confirmed + probable). Chikungunya totals fall by 749,047 and Zika by 252,573 in 2016–2025 (`clinical_tables/discarded_counts.csv`) |
| SINAN 2026 | release 2026-10-06 | release 2026-10-20, notifications dated up to 2026-09-30 only |
| Clinical figures 5, 7, 8 | GraphPad `.pzfx` tables, 2016–2025, no chikungunya 2016, discarded included | `clinical_tables/`, 2016–2026, discarded excluded, SINAN standard age bands (ages of 2016–2020 were unreadable before: `"4003.0"`) |
| GLM | per-state, per-state lagged, pooled | + pooled lagged model (`glm_*_pooled_lagged.csv`, terms `Temp_Cum0_2`, `Rain_Cum0_2`) |
| Figure colours | chikungunya orange or green depending on the figure | one palette (`VIRUS_COLOR` in `R/utils.R`): dengue red, chikungunya green, Zika blue |
| Sen's slope panel | all bars in the virus colour | only trends with p < 0.05 in colour, the others grey |

## What changed vs the 2026-10-05 results (`arbovirus-surveillance-brazil-2026`)
| Input | Before | Now |
|---|---|---|
| SINAN 2026 | release 2026-09-26 (notifications to Sep 18–20) | release 2026-10-06 (to Sep 25–27) |
| 2026 cases | DENV 460,356 · CHIKV 130,003 · ZIKV 12,682 | DENV 465,323 · CHIKV 131,830 · ZIKV 12,971 |
| Population | copied series | parsed from raw IBGE files (identical values, see below) |
| INMET 2026 | each station counted twice for Jan–Aug (two snapshots in `2026.zip`) | latest snapshot per station only; 10/233 temperature and 16/232 rain cells changed (max 0.05 °C, 17 mm) |

SINAN 2016–2025, all climate before 2026, and population are unchanged, so every difference in
the results comes from the 2026 data.

---

## Folder layout
Data flows one way: `raw/` → (`etl/`) → `db/` + `clinical_tables/` → (`pipelines/`) → `outputs/` → `figures/` → `source_data/`.
```
arbovirus-surveillance-brazil-r-eduardo/
├── README.md  LICENSE  CITATION.cff  .gitignore  .github/workflows/pipeline.yml   # manual CI run of the core pipeline
├── run_all.R                 # one-command rebuild (packages + all steps)
├── run_all.ps1 / run_all.sh  # wrappers that find Rscript and run run_all.R
│
├── R/                        # CODE: shared helpers (utils.R holds the output-folder layout), stats.R, install_packages.R
├── etl/                      # raw → db/ + clinical_tables/ (build_db.R runs it all)
├── pipelines/                # all analysis code
│   ├── run_all.R             # core 9-stage orchestrator
│   └── additional/           # advanced analyses (DLNM, forecast, spatial reg, ITS, …)
├── tools/                    # raw-source re-download + archive comparison (see docs/DATA_SOURCES.md)
│
├── raw/                      # DATA: RAW official files (not in git; only MANIFEST.csv is committed)
│   ├── sinan/                # DENGBR/CHIKBR/ZIKABR 16–26 .csv.zip (OpenDataSUS)
│   ├── inmet/                # 2016.zip … 2026.zip hourly station data
│   ├── ibge/                 # population: DOU estimates + Projeções 2024
│   ├── geo/                  # IBGE state boundaries (uf_*.geojson)
│   └── MANIFEST.csv          # bytes + sha256 of the exact files the results were built from
├── reference/                # fixed inputs not rebuilt from raw
│   ├── dim_location.csv          # 27 UF ids/names
│   ├── brazil_states.geojson     # merged state polygons used by the maps
│   ├── original_db/              # original 2016–2025 series, for calibration printouts only
│   └── expected_hashes.csv       # sha256 of the db/ + clinical_tables/ these results came from
├── db/                       # normalized analysis inputs
├── clinical_tables/          # clinical/demographic breakdowns 2016–2026 + discarded_counts.csv
│
├── outputs/                  # RESULTS: tables and plots, by topic
│   ├── descriptive/          # incidence, Mann–Kendall trends, Spearman correlations (py_*)
│   ├── spatial/              # maps, Moran's I, LISA (geo_*)
│   ├── clinical/             # clinical and demographic plots per disease (Dengue_*, Chikungunya_*, Zika_*)
│   ├── regression/           # GLM tables (glm_*)
│   ├── bootstrap/            # bootstrap confidence intervals
│   ├── additional/           # advanced analyses (DLNM, co-circulation, forecast, ITS, thresholds, spatial regression)
│   └── figure_notes/         # caption values and records excluded per figure
├── figures/                  # composite publication figures
│   ├── main/                 # Figure 1–8
│   ├── supplementary/        # Figure S1 (maps by year + overview) and Figure S2
│   ├── glm/                  # regression figures (glm_fig1–5)
│   └── alternatives/         # 3 alternative-view figures (+ README)
├── source_data/              # one xlsx per figure, one sheet per panel
│
├── manuscript/               # PAPER (Journal of Medical Virology): build tools, legends, logs
│   ├── build/                # scripts that build the .docx from the repository outputs (see its README)
│   ├── figures/              # the figures renamed by order of citation (Figure1.png … FigureS7.png)
│   ├── history/              # the manuscript as the authors edited it before round 2
│   ├── FIGURE_CAPTIONS.md  SYNC_LOG.md  JMV_CHECKLIST.md  RECORD_CHECKLIST.md
│   ├── Alves ER et al JVI 2026.docx              # the original draft (never edited)
│   └── Alves ER et al JMV 2026.docx  (+ "(redline)" copy with tracked changes)   # the manuscript
├── docs/
│   ├── GUIDE.md                  # start here: what to open, what each folder holds
│   ├── DATA_SOURCES.md           # raw-data URLs, access date, checksums, Source Data index
│   ├── LITERATURE_CONTEXT.md     # results set against four recent papers + references
│   ├── R_PORT_NOTES.md           # Python → R port: method mapping, verification, known differences
│   ├── R_SESSION_INFO.txt        # R + package versions of the last install
│   └── CLEANUP_2026-10-22.md     # every file that moved in the reorganisation (old path → new path)
└── _unused/                  # files nothing uses any more, kept under their old paths (see _unused/README.md)
```

## Raw data
`raw/` is not committed (about 1.7 GB of SINAN, INMET and IBGE downloads). `raw/MANIFEST.csv` is:
it lists the size and sha256 of the 99 files the results were built from; the source URLs are in
[`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md). To rebuild `db/` from raw, download them into `raw/`
and run the full pipeline:
```bash
Rscript tools/fetch_raw_sources.R     # all official sources (resumable); --only sinan,inmet,ibge,geo
Rscript run_all.R                     # ETL + everything; etl/check_db.R compares db/ with reference/expected_hashes.csv
```
OpenDataSUS republishes the 2026 SINAN files weekly, so a fresh download is newer than the
**2026-10-20 release** these results use and changes the 2026 counts (and the `check_db.R` hashes), although
only notifications up to 2026-09-30 are used. The 2026-10-08 re-download matched the archived inputs byte for byte
for all INMET and IBGE files and SINAN 2016–2024; the 2025 SINAN zips were re-packed with identical content
(details in `docs/DATA_SOURCES.md`). On 2026-10-22 only the SINAN files were downloaded again.

## Figures
Main figures are in `figures/main/` (Figure 1–8), supplementary maps in `figures/supplementary/` (`FigureS1_<year>.png`,
2016–2026, plus `FigureS1_overview.png`, and `FigureS2_lisa_trend.png`), regression figures in `figures/glm/`, and the numbers
behind each panel in `source_data/`. Every map uses one design: a single map of Brazil with one symbol per state
and disease (circle = dengue, triangle = chikungunya, square = Zika), filled by the mapped category.
Figures carry no in-plot titles. Text for the captions is generated with them:
- `outputs/figure_notes/figure_caption_values.csv`: statistics, colour keys and class bounds per figure panel;
- `outputs/figure_notes/figure_exclusions.csv` and `figure_exclusions_captions.txt`: records with ignored/blank
  values left out of each clinical figure (n and %), plus ready-to-use caption sentences;
- `outputs/figure_notes/figure_exclusions_state_years.csv`: state-years without SINAN records.

Draft captions for every figure, with a methods/limitations paragraph, are in
[`manuscript/FIGURE_CAPTIONS.md`](manuscript/FIGURE_CAPTIONS.md). How the results relate to recent literature
(temperature and dengue transmission, *Aedes* oviposition, reporting bias across arboviruses, dengue
serotype turnover) is in [`docs/LITERATURE_CONTEXT.md`](docs/LITERATURE_CONTEXT.md).

## License and data
The code is released under the [MIT License](LICENSE); see [`CITATION.cff`](CITATION.cff) to cite it.
The tables in `db/` and `clinical_tables/`, and the results and figures, are derived from Brazilian
federal open data (SINAN/OpenDataSUS, INMET, IBGE), published under the Política de Dados Abertos
(Decreto 8.777/2016). Cite those publishers and the access date (see
[`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md)).

---

## How the data was built (provenance & definitions)

All inputs were rebuilt from the raw official sources and **calibrated to reproduce the original
series** (full detail in `clinical_tables/` companion notes and below).

**Cases** — SINAN notification microdata (DENGBR/CHIKBR/ZIKABR, 2016–2026). Counted by
notification state (`SG_UF_NOT`) and month of notification (`DT_NOTIFIC`). **One case definition for
the three diseases (since 2026-10-22): every notification except those classified as discarded**,
that is, confirmed plus probable cases (inconclusive and under-investigation notifications are kept).
Discarded `CLASSI_FIN` codes: dengue 5; chikungunya 5 (and 2 in the early-2016 form); Zika 2. The dengue
files from 2022 on contain no discarded notifications. `clinical_tables/discarded_counts.csv` lists, per
disease and year, the notifications, the discarded ones excluded and the cases kept. Notifications of the
2026 file dated after 2026-09-30 are left out, so 2026 always covers January–September. A state-month without a
case is a **zero** (not missing) for every state that has notifications in that year's file; a state with no
notification at all in the file (Espírito Santo 2021, chikungunya and Zika) stays missing. This matters because
excluding discarded notifications leaves many empty state-months.

Before 2026-10-22 only dengue was filtered and chikungunya and Zika counted every notification (discarded
ones too: 749,047 and 252,573 in 2016–2025); the earlier series were validated against the original `db/`
on that basis (25 of 29 overlapping state-years within 1%). The new chikungunya and Zika totals are
therefore not comparable with the old ones. `Monthly_Inc_per100k = Cases / Population × 100000`.

**Population** — parsed from the raw IBGE files by `etl/build_population.R`:
2016–2023 from the census-consistent *Projeções da População, Revisão 2024*
(`projecoes_2024_tab4_indicadores.xlsx`; IBGE published no estimates for 2022–2023), and
2024–2026 from the official 1-July estimates published in the DOU (`estimativa_dou_<year>`;
2026 Brazil total 214.2 M). The pre-census DOU estimates for 2016–2021 are not used: they overstate
several states (Amapá +11%) and would create a ~2.4 M drop between 2021 and 2022.

**Climate** — INMET automatic weather stations aggregated to state × month (−9999 sentinels
masked; coverage thresholds applied). `Temp_Avg` reproduces the original series well (corr 0.83).
⚠ **Rainfall** is on a different, physically-correct scale (~115 mm/month, realistic seasonality)
than the original `Rain_mm` (~36 mm/month) and is **not continuous** with it — the whole climate
series was rebuilt uniformly for all years, so climate-dependent results below are computed on
this consistent INMET series, **not** comparable in absolute rain scale to the original writeup.

**Clinical/demographic** (`clinical_tables/`) — tidy breakdowns (sex, age, classification,
criterion, evolution, hospitalization, serotype, lab results, pregnancy, UF totals) derived from
the same case population, 2016–2026.

---

## Reproducing the results
Use `run_all.ps1` / `run_all.sh` / `run_all.R` (see Quick start), or run the steps by hand from
any folder:
```bash
Rscript R/install_packages.R                         # once: CRAN packages
Rscript etl/build_db.R                               # raw -> db/ + clinical_tables/
Rscript pipelines/run_all.R                          # core 9 stages -> outputs/ + figures/
Rscript pipelines/additional/run_additional_analyses.R
Rscript pipelines/alt_results.R
Rscript pipelines/build_source_data.R
```
Every script finds the project root by itself, so they also run from RStudio (`source()` the file,
or open it and press *Source*). `etl/check_db.R` (run by `build_db.R`) confirms the rebuilt `db/`
CSVs are byte-identical to the ones the published results used. Permutation tests and the
bootstrap use fixed seeds, so reruns reproduce the numbers. Re-downloading with
`tools/fetch_raw_sources.R` pulls the newest 2026 SINAN release, which changes the 2026 counts
(see `docs/DATA_SOURCES.md`).

---

## Important notes
- **2026 is season-to-date** (cases Jan–Sep; climate Jan–Sep, late months partial; climate present
  for 26/27 states). Annual-incidence values for 2026 are annualised from reported months.
- **CHIKV 2016 is new** vs the original series (which began CHIKV in 2017).
- **The old `RESULTS_SUMMARY.*` (now in `_unused/docs/`) describes the ORIGINAL 2016–2025 analysis.** The figures/tables in
  `outputs/` and `figures/` here are the regenerated 2016–2026 results; where climate (esp. rain)
  is involved, re-read the numbers from these regenerated outputs rather than the old narrative.
- **Clinical figures** (Figures 5, 7, 8 and `outputs/clinical/`) are drawn from
  `clinical_tables/clinical_demographic_long.csv` (2016–2026, discarded notifications excluded). Until
  2026-10-22 they came from hand-made GraphPad `.pzfx` tables that ended in 2025 (kept in
  `_unused/reference/graphpad_data/` for comparison only).
- **2026 limitations.** 2026 covers January–September and its annual values are annualised (× 12 / 9),
  which overstates the year because October–December carry a small share of the cases. It is kept in the
  trends, mean incidence, Moran's I and LISA; read every 2026-dependent result with that in mind.
