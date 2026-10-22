# Data sources and Source Data

Provenance for every raw input of the 2016–2026 arbovirus analysis, and an index of the
journal-style Source Data files. Raw files were re-downloaded from the official sources on
**2026-10-08** and checked against the archived copies the results were built from
(`data/updated_data.rar`, `data/metereologicos.rar`). **The 33 SINAN files were downloaded again on
2026-10-22** (OpenDataSUS had republished the 2026 files on 2026-10-20); everything below about SINAN
refers to that download unless a date says otherwise.

## 1. Raw sources

| Dataset | Publisher | Files | URL pattern |
|---|---|---|---|
| Arbovirus notifications (SINAN) | Ministério da Saúde, OpenDataSUS | `DENGBR16–26`, `CHIKBR16–26`, `ZIKABR16–26` `.csv.zip` (33) | `https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/{Dengue,Chikungunya,Zikavirus}/csv/{DENG,CHIK,ZIKA}BR{yy}.csv.zip` |
| Weather stations (hourly, automatic) | INMET, Banco de Dados Históricos | `2016.zip`–`2026.zip` (11) | `https://portal.inmet.gov.br/uploads/dadoshistoricos/{year}.zip` |
| Population estimates 2016–2021, 2024–2026 | IBGE, Estimativas da População | `estimativa_dou_*`, `estimativa_TCU_2016_*`, `POP20xx_*`, `serie_2001_20xx_TCU` (26) | `https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_{year}/{file}` |
| Population 2022–2023 | IBGE, Projeções da População, Revisão 2024 | `projecoes_2024_tab1_idade_simples.xlsx`, `projecoes_2024_tab4_indicadores.xlsx` | `https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/{file}` |
| State boundaries | IBGE, API de Malhas v3 | `uf_{code}.geojson` (27) | `https://servicodados.ibge.gov.br/api/v3/malhas/estados/{code}?formato=application/vnd.geo+json&qualidade=intermediaria` |

All of these are Brazilian federal open data, published under the Política de Dados Abertos
(Decreto 8.777/2016). Cite the publisher and the access date.

**Population.** `etl/build_population.R` builds the series from the raw IBGE files:
- **2016–2023:** Projeções 2024 revision, `projecoes_2024_tab4_indicadores.xlsx` column `POP_T`.
  IBGE published no estimates for 2022–2023 (census year). The earlier copied series turned out to
  be exactly this file for 2016–2023 (27/27 states every year).
- **2024–2026:** official DOU 1-July estimates, `estimativa_dou_<year>`. 2024–2025 equal the
  earlier series.
- **Not used:** the pre-census DOU estimates for 2016–2021. They sit 1–1.5% above the projections
  nationally and up to 11% above for single states (Amapá), and would break the series at 2022.

**Local copy:** `raw/` is not committed to the git repository; only `raw/MANIFEST.csv` is. The full set
was 99 files (about 1.7 GB). On 2026-10-22 only the 33 SINAN files (about 0.6 GB) were downloaded again, with
`Rscript tools/fetch_raw_sources.R --only sinan`; the INMET, IBGE and boundary files were not, and `db/`
climate, population and boundaries were not rebuilt (their hashes in `reference/expected_hashes.csv` still
match). The SINAN rows of `raw/MANIFEST.csv` now list the bytes and sha256 of the 2026-10-22 download; `raw/sources_manifest.csv`
(git-ignored) adds the URL, `Last-Modified` and access time of each file. The 2026 SINAN files are the **release of 2026-10-20**
(the 2026-10-06 release used before cannot be fetched any more); the 2016–2024 files, and the 2025 files, have the
same content as before.

## 2. Fresh downloads vs the archived inputs

| Result | Files |
|---|---|
| Byte-identical (CRC32) | 64 of 72: all INMET years, all IBGE files, and SINAN 2016–2024 |
| Re-zipped, same CSV content | `DENGBR25`, `CHIKBR25`, `ZIKABR25` (inner CSV CRC identical) |
| Newer data | `DENGBR26` 460,356 → 465,323 records; `CHIKBR26` 130,003 → 131,830; `ZIKABR26` 12,682 → 12,971 |

The 2026 SINAN files are preliminary, and OpenDataSUS republishes them weekly. State the release date in the methods.

**2026-10-22 download.** 27 of the 33 SINAN files are byte-identical to the 2026-10-08 build (all of 2016–2024). The
2025 files were re-zipped (`Last-Modified` 2026-10-20; same size) and the 2026 files have new content:

| 2026 file | Records, release 2026-10-06 | Records, release 2026-10-20 |
|---|---|---|
| `DENGBR26` | 465,323 | 470,451 |
| `CHIKBR26` | 131,830 | 133,490 |
| `ZIKABR26` | 12,971 | 13,384 |

The newer files reach into October. **Only notifications dated up to 2026-09-30 are used** (`LAST_NOTIFICATION_DATE` in
`etl/build_cases_clinical.R`; 1,901 dengue, 151 chikungunya and 1 Zika notifications are left out), so 2026 still covers
January–September, now with late notifications of those months filled in. Earlier results (2026-10-05, 2026-10-08)
used the releases of 2026-09-26 and 2026-10-06.

## 3. From raw files to `db/`

`etl/build_db.R` runs the whole build (population, cases + clinical tables, climate, checks).
The field decodes are in `etl/build_cases_clinical.R`. In short:
- **Cases:** counted by notification state (`SG_UF_NOT`) and month of `DT_NOTIFIC`. **One definition for the three
  diseases (since 2026-10-22): every notification except those classified as discarded**, that is, confirmed plus
  probable (inconclusive and under-investigation notifications stay in). Discarded `CLASSI_FIN` codes: dengue 5; chikungunya 5,
  and 2 in the early-2016 form (which coded confirmed / discarded as 1 / 2, like the Zika form; checked on the 2016 file: same
  seasonal shape and 2.2 : 1 ratio as codes 13 / 5, and code 2 has almost no deaths from the disease); Zika 2. The dengue files
  from 2022 on contain no discarded notifications at all. `clinical_tables/discarded_counts.csv` gives, per disease and
  year, the notifications, those dropped by the 2026 date cap, the discarded ones excluded, and the cases kept.
  Before 2026-10-22 only dengue was filtered, and chikungunya and Zika counted every notification.
  **Zero months:** a state-month without a case is written as 0 (`normalized_fact_cases.csv` is a complete
  state × month grid) for every state that has notifications in that year's file, counted before the discarded ones
  are dropped; a state with no notification at all in the file (Espírito Santo 2021, chikungunya and Zika) is left
  absent, that is, missing. Before this, absent months were treated as not reported and annual totals were annualized
  over the months present, which would have inflated the small Zika counts.
- **Climate:** INMET hourly data. −9999 values are masked. A station-month counts only with ≥ 240 valid
  temperature readings or ≥ 360 valid rain readings. State values are the mean across stations.
  When a year zip holds several cumulative snapshots of one station (`2026.zip` has files ending
  31-08-2026 and 30-09-2026 for each station), only the latest is used.
- **Incidence:** cases / population × 100,000.

## 4. Source Data (`source_data/`)

`pipelines/build_source_data.R` writes one workbook per figure, with one sheet per panel. Each
workbook has a `README` sheet naming the code each panel comes from. Numbers are recomputed with
the pipelines' own functions, then cross-checked against the saved results. All checks pass:
annual incidence, Mann-Kendall, Spearman, global Moran, mean incidence, LISA, and the national monthly series.

| Workbook | Contents |
|---|---|
| `Figure1` | A: national and regional pop-weighted annual incidence. B: box statistics and all 10,364 state-month rows |
| `Figure2` | A: Kendall τ per state. B: Sen's slope |
| `Figure3` | A: mean ρ and % significant by variable × lag. B: regional lag profile. Plus all state-level tests |
| `Figure4` | Moran scatter z / Wz per state, with I, p and the fitted line |
| `Figure5` | A: age-band counts and the plotted violin quartiles. B: sex counts and % |
| `Figure6` | Combined map: mean incidence and natural-breaks class per state × disease, symbol positions, class bounds and Moran's I |
| `Figure7`, `Figure8` | Clinical/laboratory counts and the plotted % (DENV; CHIKV and ZIKV) |
| `GLM_Figures` | glm_fig1–5 |
| `Additional_Figures` | DLNM, co-circulation, spatial regression, ITS, forecast, epidemic threshold |
| `Supplementary_Figures` | S1: incidence per state-year and its natural-breaks class (all years pooled), class bounds. S2: LISA and MK trend classes. py_02, py_03b, py_06b/c, py_07, clinical monthly and state totals, alt_results |
| `Tables` | Bootstrap CIs, global Moran, clinical breakdowns for 2016–2026 |

**Caveats:**
- **Figures 5, 7 and 8 are drawn from `clinical_tables/clinical_demographic_long.csv`** (2016–2026, discarded
  notifications excluded, SINAN standard age bands). Until 2026-10-22 they came from hand-made GraphPad `.pzfx` tables
  that ended in 2025, counted discarded chikungunya and Zika notifications and had no chikungunya for 2016; those files are kept
  in `reference/graphpad_data/` and `parse_pzfx()` in `pipelines/graphpad_pipeline.R` only to compare the two sources.
  The 2016–2020 ages were unreadable in the clinical tables before the same date (the old files store ages as `"4003.0"`).
- **The age violins are resampled.** They draw 6,000 synthetic ages per year from the binned counts
  (seed 42). The Source Data gives the bin counts plus the plotted quartiles.
- **2026 is annualised.** All 2026 annual incidence is annualised from January–September.

## 5. Reproduce

```bash
Rscript tools/fetch_raw_sources.R                      # re-download + manifest (resumable)
Rscript tools/compare_with_archive.R --data <folder>    # compare with updated_data.rar / metereologicos.rar
Rscript pipelines/build_source_data.R                   # source_data/*.xlsx + consistency checks
```
