# Manuscript sync log: draft (2016–2025, Python) → round 1 (2016–2026, R) → round 2 (case definition, 2026 cap, figure order)

Round 1 written 2026-10-21; **round 2 written 2026-10-22**, after the eight instructions tagged "@claude for ERA" in `Alves ER et al JMV 2026.docx`. Covers `Alves ER et al JMV 2026.docx` (clean) and `Alves ER et al JMV 2026 (redline).docx` (every text change tracked against the draft, author *Claude for ERA*), both built from `Alves ER et al JVI 2026.docx`, which was not modified. The file as edited by the authors before round 2 is kept in `docs/manuscript/history/`.

**How the numbers were produced.** Every number in the Abstract, Results, Discussion and Methods was computed from the repository files by `build/numbers.R` (R 4.6.1) into `numbers.csv`, and inserted into the text by key. The table in section 3 lists each inserted number with its source file. Legends are the text of `docs/FIGURE_CAPTIONS.md`. Statements the prose makes about the data (who trends, which model peaks at which lag, "nearly half were discarded") are checked at build time against `numbers.csv` (34 assertions), so the text cannot drift from the data. A second, independent computation in Python (section 6) reproduced 43 headline values from the raw tables.

## 0. Round 2: what each instruction changed

| Comment (author) | Instruction | What was done |
|---|---|---|
| 48 (ERA) | "need you to run this again" (Moran's I) | Whole pipeline rerun on the new case definition and data (ETL, 9 of 9 stages, source data). Moran's I: dengue 0.516 (p 0.001), chikungunya 0.231 (p 0.017; now significant), Zika −0.105 (p 0.243). |
| 49, 50 (ERA) | "count total cases as the probables + confirmed, and exclude the discarded" | For all three diseases a case is any notification not classified as discarded (dengue code 5; chikungunya 5 and, in the early-2016 form, 2; Zika 2). Discarded and excluded: dengue 3,002,212 of 19,804,831 (15.2%; none from 2022 on), chikungunya 846,972 of 2,446,756 (34.6%), Zika 263,816 of 559,455 (47.2%). Counts per disease and year: `clinical_tables/discarded_counts.csv`. |
| 51 (ERA) | "keep 2026 on the analyses, but ALWAYS make it clear that this year has its limitations" | 2026 kept. SINAN downloaded again on October 22, 2026; the 2026 files (release of October 20, 2026) were cut at notifications dated up to 2026-09-30, so 2026 is January–September, annualized ×12/9. Every paragraph or legend that uses 2026 says so (a build check fails otherwise). Q4 holds 4.8% / 4.2% of dengue / Zika cases (2016–2025), so the annualized year is overstated. |
| 52 (ERA) | "renumber and reorder everything having in mind the order that the images are cited" | Figures numbered by first citation (main 1–8, supplementary S1–S7); legends reordered; cross-references inside legends renumbered; figure citations removed from Methods; the annual maps, never cited before, are now cited. Copies under the new numbers: `docs/manuscript/figures/`; table in section 8. |
| 53 (ERA) | "follow all the comments from Galileu" | Replies posted in each thread (threads left open for Galileu). Figure style (his comment 6): one colour per virus defined once in `R/utils.R` (dengue red, chikungunya green, Zika blue); grey bars for non-significant Sen's slopes (only significant trends carry colour); figures have no in-plot titles; keys sit next to the data. |
| 54 (ERA) | "what should we do now?" (lag model) | You chose to add a pooled lagged model (FU and month fixed effects, lags 0–2 jointly, FU-clustered SE; `outputs/glm_*_pooled_lagged.csv`). Results report the IRR per lag and the IRR of a change sustained over lags 0–2; the per-FU lagged models stay. |
| 55 (ERA) | "you can delete it if it doesn't break the logic" (DLNM) | DLNM deleted from Methods, Results, Discussion and the author query (the logic holds); the analysis files stay in `outputs/`. A build check fails if "DLNM" reappears. |
| (not a comment) | Figures 5, 7, 8 (your choice) | Rebuilt from `clinical_tables/clinical_demographic_long.csv` (2016–2026, discarded excluded) instead of the GraphPad tables; NS1 panel relabelled; age bands and classification labels corrected in the ETL. |

## 1. Headline changes in the claims

Draft = `Alves ER et al JVI 2026.docx` (Python, 2016–2025). Round 1 = manuscript of 2026-10-21 (R, 2016–2026, chikungunya and Zika with discarded notifications, 2026 up to the 2026-10-06 release). Round 2 = this manuscript. Items marked **⇄** change the interpretation and need the co-authors' attention.

| | Draft | Round 1 | Round 2 | Source |
|---|---|---|---|---|
| Cases 2016–2026 (dengue / chikungunya / Zika) | — | — | 16,802,619 / 1,599,784 / 295,639 | `db/normalized_fact_cases.csv` |
| Moran's I, dengue / chikungunya / Zika | 0.562 (p = 0.001) / −0.036 (0.460) / −0.008 (0.352) | 0.516 / 0.004 / −0.006 (p 0.001 / 0.285 / 0.326) | 0.516 / 0.231 / −0.105 (p 0.001 / 0.017 / 0.243) | `outputs/geo_spatial_stats.xlsx`, Global_Moran |
| Mean annual incidence, dengue top 3 | DF 1,825.6; GO 1,742.7; MG 1,647.7 | GO 1,782.4; DF 1,693.7; MG 1,538.7 | GO 1,783.7; DF 1,693.6; MG 1,539.0 | `geo_spatial_stats.xlsx`, Mean_Incidence |
| Chikungunya top mean incidence | MS 421.8 | MS 498.4; CE 324.9; MT 294.5 | MT 227.8; CE 215.0; RN 202.5 | same |
| Zika top mean incidence | TO 145.7; MT 106.7 | TO 136.9; MT 98.4 | MT 72.7; RJ 42.7; BA 41.3 | same |
| ⇄ Dengue increasing trends | RS, SC, SP | RS (τ 0.600), SC (τ 0.491); SP not significant (p = 0.161) | RS (τ 0.600), SC (τ 0.491); SP not significant | `py_statistical_results.xlsx`, Mann_Kendall |
| ⇄ Chikungunya increasing trends | SC, RS, MS | MS, MG, GO; SC (p = 0.119) and RS (p = 0.161) not significant | MS (τ 0.782), GO (0.600), MG (0.564); CE decreasing | same |
| ⇄ Zika decreasing trends | AL, PI, DF (3 states) | 6 states (DF, PI, MG, RJ, AL, PR) | 13 states, none increasing | same |
| ⇄ Multiple testing | "no adjustment" | BH q-values reported; no trend survives (minimum q: dengue 0.344, chikungunya 0.137, Zika 0.110) | BH q-values reported; minimum q: dengue 0.344, chikungunya 0.029 (MS), Zika 0.002 (12 states remain significant) | Mann_Kendall, q_value |
| Dengue LISA high–high, after BH | Central-West and Southeast | also Paraná; after BH only GO, MG (HH) and RJ (LH) | also Paraná; after BH only Goiás and Minas Gerais (HH) and Rio de Janeiro (LH) | `geo_spatial_stats.xlsx`, LISA_Clusters |
| Zika 2016 vs later years | "roughly 8–10 times" | 6.8–14.9 times (complete years 2017–2025) | 12.2–62.6 times (complete years 2017–2025) | `source_data/Figure1.xlsx` |
| ⇄ Pooled temperature IRR, dengue | 2.10 (1.96–2.26) | 1.10 (1.02–1.19) | 1.11 (1.03–1.19) | `outputs/glm_negbin_pooled_fe.csv` |
| ⇄ Pooled temperature IRR, chikungunya | 1.32 (1.24–1.41), significant | 1.05 (0.99–1.12), **not significant** | 1.03 (0.95–1.12), **not significant** | same |
| ⇄ Pooled temperature IRR, Zika | 0.90 (0.84–0.97), inverse | 1.09 (1.01–1.18), **positive** | 1.11 (1.00–1.22), **positive** (p 0.047) | same |
| ⇄ Rainfall | IRR 1.007 per mm; Spearman ρ ≈ 0 | IRR per 100 mm 1.30 / 1.18 / 1.16; mean ρ at lag 2 0.433 / 0.355 / 0.347 | IRR per 100 mm 1.30 / 1.16 / 1.11; mean ρ at lag 2 0.432 / 0.295 / 0.243 | glm CSVs; `Spearman_Lag` |
| Temperature Spearman ρ (national mean, dengue) | 0.16 → 0.19, "positive at all lags" | −0.147 / −0.018 / 0.137 at lags 0 / 1 / 2 | −0.146 / −0.016 / 0.137 at lags 0 / 1 / 2 | `Spearman_Lag` |
| NB2 dispersion α (pooled) | 1.69 / 1.45 / 1.55 | 1.23 / 1.20 / 1.21 | 1.25 / 1.71 / 2.21 | pooled CSV |
| Per-FU temperature, significant FU | 16 / 12 / 10 | 14 / 9 / 7 | 14 / 11 / 5 | `glm_negbin_per_state.csv` |
| Per-FU lagged models, lag-2 temperature, significant FU | 11 / 4 / 7 | 11 / 7 / 8 | 11 / 8 / 8 | `glm_negbin_lagged.csv` |
| **New** pooled lagged model, temperature IRR per °C | — | — | dengue lag 2 1.37, sustained 0–2 1.33; chikungunya lag 2 borderline (p 0.056); Zika peaks at lag 1 (1.09) | `outputs/glm_negbin_pooled_lagged.csv` |
| Hospitalization (comment 13) | 15,788,792 not hospitalized; 529,203 hospitalized | 529,203 hospitalized; 10,642,808 not; 5,145,984 ignored/blank (sum 16,317,995) | 559,539 hospitalized; 10,979,849 not; 5,263,231 ignored/blank (sum 16,802,619) | `source_data/Figure7.xlsx` |
| Placeholders | [X], xxxxx, [REF IBGE??] | chikungunya men 800,258; DENV-2 117,958; DENV-3 8,766; DENV-4 747 | chikungunya men 624,457; DENV-2 139,603; DENV-3 18,805; DENV-4 860 | Figure 5/7 source data |
| Chikungunya peak year | (comment 9) | 2024 (200.5 per 100,000), second 2016 (155.3) | 2024 (124.2 per 100,000), second 2016 (117.3); highest regional value: Northeast 2016 (380.5) | `Figure1.xlsx` |

## 2. Methods statements rewritten to what the code does

| Draft statement | Manuscript statement | Evidence in the repository |
|---|---|---|
| Analyses in Python 3.12 (pandas, statsmodels, GeoPandas…) | R 4.6.1; data.table, readxl, sf, spdep, classInt, ggplot2, patchwork | `R_SESSION_INFO.txt`; `docs/R_PORT_NOTES.md` |
| Temperature from CPC/NCEP grid; rainfall from INMET and CPTEC/INPE | INMET hourly automatic stations, ≥240 (temperature) / ≥360 (rainfall) valid hourly readings per station-month, unweighted mean per FU | `etl/build_climate.R` |
| Spatial weights: Queen contiguity with kNN fallback | Row-standardized kNN (k = 5) on polygon centroids only | `pipelines/data_loader.R`; `R/stats.R` |
| "No adjustment for multiple comparisons" | Raw p reported with Benjamini–Hochberg q-values | `R/utils.R` (`p.adjust(method = "BH")`); `Significant_FDR` columns |
| Pooled distributed-lag model (comment 16) | Four specifications: pooled, per-FU, per-FU lagged (unconstrained), and **pooled lagged** (new, round 2); no DLNM in the manuscript | `pipelines/glm_common.R` `SPECS`; `FORMULA_LAGGED_FE` |
| "Overdispersion assessed by testing α > 0" (comment 22) | Pearson dispersion of the Poisson fit and ML α; no formal test | `glm_common.R`; no `lrtest` anywhere |
| State fixed effects only; model-based SE | Pooled: FU + calendar-month FE, FU-clustered SE; per-FU and per-FU lagged: month FE, Newey–West (3 lags) | `glm_common.R` |
| Discarded and under-investigation cases excluded; FU of residence | **All three diseases**: every notification not classified as discarded (confirmed + probable, inconclusive and under investigation kept); FU/month of notification | `etl/build_cases_clinical.R` (`DISCARD`, `MAP_CLASSI_BY`); `README.md` |
| Population: 2022 Census and intercensal estimates [REF] | IBGE projections (2024 revision) 2016–2023; DOU 1-July estimates 2024–2026 | `etl/build_population.R`; `docs/DATA_SOURCES.md` |
| Study period to December 31, 2025 | To September 30, 2026 (SINAN download of 2026-10-22; 2026 annualized ×12/9) | `etl/build_cases_clinical.R` (`CAP_YEAR`, `LAST_NOTIFICATION_DATE`); `pipelines/data_loader.R` |
| (not stated) | State-months without a notification are zeros inside the observed span of a state-year; a state-year with no notification at all (Espirito Santo 2021, chikungunya and Zika) is missing, not zero | `etl/build_cases_clinical.R` (zero-fill); `outputs/figure_exclusions_state_years.csv` |

## 3. Every number inserted into the text, with its source

`key` is the entry in `build/numbers.csv`. Formats: `i` integer, `dN` N decimals, `pct` percent, `pv` p-value, `s` text, `ord`/`words` spelled.

| Key | Format | Text | Source |
|---|---|---|---|
| `ann.CHIKV.BR.2016` | d1 | 117.3 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.CHIKV.BR.2024` | d1 | 124.2 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.DENV.BR.2023` | d0 | 778 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.DENV.BR.2024` | d0 | 3,088 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.DENV.BR.2026` | d0 | 292 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.ZIKV.BR.2016` | d0 | 108 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `cases.CHIKV.all` | i | 1,599,784 | `db/normalized_fact_cases.csv` |
| `cases.DENV.all` | i | 16,802,619 | `db/normalized_fact_cases.csv` |
| `cases.DENV.y2024` | i | 6,564,924 | `db/normalized_fact_cases.csv` |
| `cases.DENV.y2024` | mil2 | 6.56 | `db/normalized_fact_cases.csv` |
| `cases.ZIKV.all` | i | 295,639 | `db/normalized_fact_cases.csv` |
| `cases.ZIKV.y2016` | i | 219,266 | `db/normalized_fact_cases.csv` |
| `chik_regmax_region` | s | Northeast | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `chik_regmax_val` | d1 | 380.5 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `chik_regmax_year` | y | 2016 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `cl.CHIKV.age.20_39` | i | 536,330 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.CHIKV.age.40_59` | i | 496,275 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.CHIKV.class.Chikungunya` | i | 1,295,927 | `source_data/Figure8.xlsx / Fig8A1_Chik_Classifi` |
| `cl.CHIKV.class.Inconclusive` | i | 37,493 | `source_data/Figure8.xlsx / Fig8A1_Chik_Classifi` |
| `cl.CHIKV.class.Unclassified` | i | 265,810 | `source_data/Figure8.xlsx / Fig8A1_Chik_Classifi` |
| `cl.CHIKV.class.total` | i | 1,599,784 | `source_data/Figure8.xlsx / Fig8A1_Chik_Classifi` |
| `cl.CHIKV.crit.Ininvestigation` | i | 34,298 | `source_data/Figure8.xlsx / Fig8A2_Chik_Criteria` |
| `cl.CHIKV.evo.Cure` | i | 1,187,793 | `source_data/Figure8.xlsx / Fig8A3_Chik_Evolutio` |
| `cl.CHIKV.evo.Death` | i | 1,492 | `source_data/Figure8.xlsx / Fig8A3_Chik_Evolutio` |
| `cl.CHIKV.sex.F` | i | 973,344 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.CHIKV.sex.M` | i | 624,457 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.CHIKV.sex.ratio` | d1 | 1.6 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.DENV.age.20_59` | i | 10,477,652 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.DENV.age.20_59_share` | pct1 | 62.5% | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.DENV.age.known` | i | 16,773,732 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.DENV.hosp.IgnBlank` | i | 5,263,231 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.Negative` | i | 10,979,849 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.Positive` | i | 559,539 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.known` | i | 11,539,388 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.share_known` | pct1 | 4.8% | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.total` | i | 16,802,619 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.sero.DENV1` | i | 210,427 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.DENV2` | i | 139,603 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.DENV3` | i | 18,805 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.DENV4` | i | 860 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.typed` | i | 369,695 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.typed_share` | pct1 | 2.2% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV2.2023` | pct1 | 12.8% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV2.2024` | pct1 | 30.5% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV2.2025` | pct1 | 73.8% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV2.2026` | pct1 | 64.2% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV3.2023` | pct1 | 0.2% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV3.2024` | pct1 | 0.9% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV3.2025` | pct1 | 14.0% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV3.2026` | pct1 | 29.8% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sex.F` | i | 9,191,414 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.DENV.sex.M` | i | 7,589,052 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.DENV.sex.ratio` | d2 | 1.21 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.age.20_39` | i | 121,604 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.ZIKV.age.40_59` | i | 70,910 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.ZIKV.class.Confirmed` | i | 179,642 | `source_data/Figure8.xlsx / Fig8B1_Zika_Classifi` |
| `cl.ZIKV.class.Inconclusive` | i | 103,094 | `source_data/Figure8.xlsx / Fig8B1_Zika_Classifi` |
| `cl.ZIKV.class.Unclassified` | i | 12,728 | `source_data/Figure8.xlsx / Fig8B1_Zika_Classifi` |
| `cl.ZIKV.class.total` | i | 295,639 | `source_data/Figure8.xlsx / Fig8B1_Zika_Classifi` |
| `cl.ZIKV.crit.Clinicepidemiological` | i | 151,662 | `source_data/Figure8.xlsx / Fig8B2_Zika_Criteria` |
| `cl.ZIKV.crit.Laboratorial` | i | 28,731 | `source_data/Figure8.xlsx / Fig8B2_Zika_Criteria` |
| `cl.ZIKV.malesh_max` | pct0 | 42% | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.malesh_maxyear` | y | 2026 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.malesh_min` | pct0 | 32% | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.malesh_minyear` | y | 2017 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.preg.1Trimester` | i | 5,794 | `source_data/Figure8.xlsx / Fig8B4_Zika_Pregnanc` |
| `cl.ZIKV.preg.2Trimester` | i | 9,014 | `source_data/Figure8.xlsx / Fig8B4_Zika_Pregnanc` |
| `cl.ZIKV.preg.3Trimester` | i | 7,965 | `source_data/Figure8.xlsx / Fig8B4_Zika_Pregnanc` |
| `cl.ZIKV.preg.tri_sum` | i | 22,773 | `source_data/Figure8.xlsx / Fig8B4_Zika_Pregnanc` |
| `cl.ZIKV.sex.F` | i | 195,779 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.sex.M` | i | 99,473 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.sex.ratio` | d1 | 2.0 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `clim.n_states_2026` |  | 26 | `db/normalized_fact_climate.csv` |
| `clim.rain_sd` | d0 | 100 | `db/normalized_fact_climate.csv` |
| `ct.sero_share.DENV3.2024` | pct1 | 0.9% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_share.DENV3.2025` | pct1 | 14.0% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_share.DENV3.2026` | pct1 | 29.8% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_typed_pct.2026` | pct1 | 7.1% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_typed_pct_max` | pct1 | 3.0% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_typed_pct_min` | pct1 | 0.2% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `disc.CHIKV.cases` | i | 1,599,784 | `clinical_tables/discarded_counts.csv` |
| `disc.CHIKV.disc` | i | 846,972 | `clinical_tables/discarded_counts.csv` |
| `disc.CHIKV.notif` | i | 2,446,756 | `clinical_tables/discarded_counts.csv` |
| `disc.CHIKV.share` | pct0 | 35% | `clinical_tables/discarded_counts.csv` |
| `disc.CHIKV.share` | pct1 | 34.6% | `clinical_tables/discarded_counts.csv` |
| `disc.DENV.disc` | i | 3,002,212 | `clinical_tables/discarded_counts.csv` |
| `disc.DENV.notif` | i | 19,804,831 | `clinical_tables/discarded_counts.csv` |
| `disc.DENV.share` | pct0 | 15% | `clinical_tables/discarded_counts.csv` |
| `disc.DENV.share` | pct1 | 15.2% | `clinical_tables/discarded_counts.csv` |
| `disc.ZIKV.cases` | i | 295,639 | `clinical_tables/discarded_counts.csv` |
| `disc.ZIKV.disc` | i | 263,816 | `clinical_tables/discarded_counts.csv` |
| `disc.ZIKV.notif` | i | 559,455 | `clinical_tables/discarded_counts.csv` |
| `disc.ZIKV.share` | pct0 | 47% | `clinical_tables/discarded_counts.csv` |
| `disc.ZIKV.share` | pct1 | 47.2% | `clinical_tables/discarded_counts.csv` |
| `fe.DENV.elisa.pct2025` | d0 | 98 | `outputs/figure_exclusions.csv` |
| `fe.DENV.elisa.pctmax1624` | d0 | 53 | `outputs/figure_exclusions.csv` |
| `fe.DENV.elisa.pctmin1624` | d0 | 35 | `outputs/figure_exclusions.csv` |
| `fe.DENV.hosp.pct` | d1 | 31.3 | `outputs/figure_exclusions.csv` |
| `fe.DENV.igm.pct2025` | d0 | 98 | `outputs/figure_exclusions.csv` |
| `fe.DENV.igm.pctmax1624` | d0 | 49 | `outputs/figure_exclusions.csv` |
| `fe.DENV.igm.pctmin1624` | d0 | 33 | `outputs/figure_exclusions.csv` |
| `fe.DENV.sero.pct` | d1 | 97.8 | `outputs/figure_exclusions.csv` |
| `gap.text` | s | The national SINAN files contain no chikungunya and Zika notification for Espírito Santo in 2021, so these sta | `outputs/figure_exclusions_state_years.csv` |
| `glml.CHIKV.Rain_Lag2.nsig` | i | 7 | `outputs/glm_negbin_lagged.csv` |
| `glml.CHIKV.Temp_Avg.nsig` | i | 7 | `outputs/glm_negbin_lagged.csv` |
| `glml.CHIKV.Temp_Lag1.nsig` | i | 3 | `outputs/glm_negbin_lagged.csv` |
| `glml.CHIKV.Temp_Lag2.npos` | i | 5 | `outputs/glm_negbin_lagged.csv` |
| `glml.CHIKV.Temp_Lag2.nsig` | i | 8 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Rain_Lag2.nsig` | i | 13 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Avg.nsig` | i | 9 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Lag1.nsig` | i | 9 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Lag2.nfdr` | i | 11 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Lag2.npos` | i | 9 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Lag2.nsig` | i | 11 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Rain_Lag2.nsig` | i | 6 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Temp_Avg.nsig` | i | 3 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Temp_Lag1.nsig` | i | 0 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Temp_Lag2.nsig` | i | 8 | `outputs/glm_negbin_lagged.csv` |
| `glmp.CHIKV.Rain_mm.hi100` | d2 | 1.37 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef + crit x SE)))` |
| `glmp.CHIKV.Rain_mm.irr100` | d2 | 1.16 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x Coef))` |
| `glmp.CHIKV.Rain_mm.lo100` | d2 | 0.97 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef - crit x SE)))` |
| `glmp.CHIKV.Temp_Avg.hi` | d2 | 1.12 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.CHIKV.Temp_Avg.irr` | d2 | 1.03 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.CHIKV.Temp_Avg.lo` | d2 | 0.95 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.CHIKV.Temp_Avg.p` | pv | = 0.493 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.CHIKV.alpha` | d2 | 1.71 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.Rain_mm.hi100` | d2 | 1.48 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef + crit x SE)))` |
| `glmp.DENV.Rain_mm.irr100` | d2 | 1.30 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x Coef))` |
| `glmp.DENV.Rain_mm.lo100` | d2 | 1.13 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef - crit x SE)))` |
| `glmp.DENV.Temp_Avg.hi` | d2 | 1.19 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.Temp_Avg.irr` | d2 | 1.11 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.Temp_Avg.lo` | d2 | 1.03 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.Temp_Avg.p` | pv | = 0.008 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.aic` | i | 55,747 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.alpha` | d2 | 1.25 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.Rain_mm.hi100` | d2 | 1.26 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef + crit x SE)))` |
| `glmp.ZIKV.Rain_mm.irr100` | d2 | 1.11 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x Coef))` |
| `glmp.ZIKV.Rain_mm.lo100` | d2 | 0.97 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef - crit x SE)))` |
| `glmp.ZIKV.Temp_Avg.hi` | d2 | 1.22 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.Temp_Avg.irr` | d2 | 1.11 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.Temp_Avg.lo` | d2 | 1.00 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.Temp_Avg.p` | pv | = 0.047 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.alpha` | d2 | 2.21 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmpl.CHIKV.Rain_Cum0_2.irr100` | d2 | 1.53 | `outputs/glm_negbin_pooled_lagged.csv (exp(100 x Coef))` |
| `glmpl.CHIKV.Temp_Cum0_2.hi` | d2 | 1.22 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.CHIKV.Temp_Cum0_2.irr` | d2 | 1.10 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.CHIKV.Temp_Cum0_2.lo` | d2 | 1.00 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.CHIKV.Temp_Cum0_2.p` | pv | = 0.053 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.CHIKV.Temp_Lag2.hi` | d2 | 1.20 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.CHIKV.Temp_Lag2.irr` | d2 | 1.09 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.CHIKV.Temp_Lag2.lo` | d2 | 1.00 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.CHIKV.Temp_Lag2.p` | pv | = 0.056 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.DENV.Rain_Cum0_2.irr100` | d2 | 1.80 | `outputs/glm_negbin_pooled_lagged.csv (exp(100 x Coef))` |
| `glmpl.DENV.Temp_Avg.irr` | d2 | 0.95 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.DENV.Temp_Cum0_2.hi` | d2 | 1.44 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.DENV.Temp_Cum0_2.irr` | d2 | 1.33 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.DENV.Temp_Cum0_2.lo` | d2 | 1.23 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.DENV.Temp_Lag1.irr` | d2 | 1.02 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.DENV.Temp_Lag2.hi` | d2 | 1.48 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.DENV.Temp_Lag2.irr` | d2 | 1.37 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.DENV.Temp_Lag2.lo` | d2 | 1.26 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.ZIKV.Rain_Cum0_2.irr100` | d2 | 1.29 | `outputs/glm_negbin_pooled_lagged.csv (exp(100 x Coef))` |
| `glmpl.ZIKV.Temp_Cum0_2.hi` | d2 | 1.12 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.ZIKV.Temp_Cum0_2.irr` | d2 | 1.04 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.ZIKV.Temp_Cum0_2.lo` | d2 | 0.96 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.ZIKV.Temp_Lag1.hi` | d2 | 1.15 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.ZIKV.Temp_Lag1.irr` | d2 | 1.09 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpl.ZIKV.Temp_Lag1.lo` | d2 | 1.04 | `outputs/glm_negbin_pooled_lagged.csv` |
| `glmpois.CHIKV.Temp_Avg.irr` | d2 | 1.21 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.CHIKV.disp` | i | 1,597 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.DENV.Temp_Avg.irr` | d2 | 1.48 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.DENV.aic` | i | 22,341,710 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.DENV.disp` | i | 9,873 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.ZIKV.Temp_Avg.irr` | d2 | 1.50 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.ZIKV.disp` | i | 635 | `outputs/glm_poisson_pooled_fe.csv` |
| `glms.CHIKV.Rain_mm.npos` | i | 3 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Rain_mm.nsig` | i | 5 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Temp_Avg.medirr_sigpos` | d2 | 1.65 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Temp_Avg.nfdr` | i | 8 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Temp_Avg.npos` | i | 7 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Temp_Avg.nsig` | i | 11 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Rain_mm.npos` | i | 10 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Rain_mm.nsig` | i | 10 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.medirr_sigpos` | d2 | 1.82 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.nfdr` | i | 13 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.nneg` | i | 2 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.npos` | i | 12 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.nsig` | i | 14 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Rain_mm.nneg` | i | 4 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Rain_mm.nsig` | i | 6 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Temp_Avg.medirr_sigpos` | d2 | 2.50 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Temp_Avg.nfdr` | i | 2 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Temp_Avg.npos` | i | 3 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Temp_Avg.nsig` | i | 5 | `outputs/glm_negbin_per_state.csv` |
| `lisa_names.CHIKV.HH` | s | Alagoas, Ceará, Paraíba, Pernambuco, Rio Grande do Norte and Sergipe | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.CHIKV.LL` | s | Paraná and Roraima | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.DENV.HH` | s | the Federal District, Espírito Santo, Goiás, Mato Grosso, Mato Grosso do Sul, Minas Gerais, Paraná and São Pau | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.DENV.LL` | s | Amapá, Maranhão, Rio Grande do Norte and Roraima | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_uf.DENV.HL` | ucap | Acre | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_uf.DENV.LH` | u | Rio de Janeiro | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisafdr_names.DENV.HH` | s | Goiás and Minas Gerais | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisafdr_names.DENV.LH` | s | Rio de Janeiro | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `meta.sinan_access` | s | October 22, 2026 | `raw/sources_manifest.csv` |
| `meta.sinan_release` | s | October 20, 2026 | `raw/sources_manifest.csv (latest Last-Modified of the 2026 files)` |
| `mk.CHIKV.MS.q` | d3 | 0.029 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_all_names.CHIKV.decreasing` | s | Ceará | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_all_names.CHIKV.increasing` | s | Mato Grosso do Sul, Goiás and Minas Gerais | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_minq.DENV` | d3 | 0.344 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_n.ZIKV.decreasing` | words | 13 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_taumax.ZIKV.decreasing` | d3 | −0.491 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_taumin.ZIKV.decreasing` | d3 | −0.945 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkfdr_n.ZIKV.decreasing` | words | twelve | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkfdr_names.CHIKV.increasing` | s | Mato Grosso do Sul | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.decreasing.1.tau` | d3 | −0.564 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.decreasing.1.uf` | u | Ceará | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.1.slope` | d0 | 16 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.1.tau` | d3 | 0.782 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.1.uf` | ucap | Mato Grosso do Sul | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.2.slope` | d0 | 9 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.2.tau` | d3 | 0.600 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.2.uf` | u | Goiás | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.3.slope` | d0 | 10 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.3.tau` | d3 | 0.564 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.3.uf` | u | Minas Gerais | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.1.slope` | d0 | 54 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.1.tau` | d3 | 0.600 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.1.uf` | ucap | Rio Grande do Sul | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.2.slope` | d0 | 52 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.2.tau` | d3 | 0.491 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.2.uf` | u | Santa Catarina | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `moran.CHIKV.I` | d3 | 0.231 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.CHIKV.p` | pv | = 0.017 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.DENV.I` | d3 | 0.516 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.DENV.p` | pv | = 0.001 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.ZIKV.I` | d3 | −0.105 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.ZIKV.p` | pv | = 0.243 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `n_months` | i | 129 | `db/normalized_fact_cases.csv` |
| `natpeak_ratio_second.DENV` | d1 | 4.0 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `rank_cases.CHIKV.1` | u | Minas Gerais | `db/normalized_fact_cases.csv` |
| `rank_cases.CHIKV.2` | u | Ceará | `db/normalized_fact_cases.csv` |
| `rank_cases.CHIKV.3` | u | Bahia | `db/normalized_fact_cases.csv` |
| `rank_cases.CHIKV.4` | u | Rio de Janeiro | `db/normalized_fact_cases.csv` |
| `rank_cases.CHIKV.5` | u | Pernambuco | `db/normalized_fact_cases.csv` |
| `rank_cases.DENV.1` | ucap | São Paulo | `db/normalized_fact_cases.csv` |
| `rank_cases.DENV.2` | u | Minas Gerais | `db/normalized_fact_cases.csv` |
| `rank_cases.ZIKV.1` | u | Rio de Janeiro | `db/normalized_fact_cases.csv` |
| `rank_cases.ZIKV.2` | u | Bahia | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.1` | i | 356,101 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.2` | i | 215,187 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.3` | i | 196,092 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.4` | i | 165,519 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.5` | i | 102,841 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.DENV.1` | i | 4,873,681 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.DENV.2` | i | 3,545,693 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.ZIKV.1` | i | 80,648 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.ZIKV.2` | i | 66,976 | `db/normalized_fact_cases.csv` |
| `rank_minc.CHIKV.1` | u | Mato Grosso | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.CHIKV.2` | u | Ceará | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.CHIKV.3` | u | Rio Grande do Norte | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.CHIKV.4` | u | Minas Gerais | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.CHIKV.5` | u | Paraíba | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.DENV.1` | u | Goiás | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.DENV.1` | ucap | Goiás | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.DENV.2` | u | the Federal District | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.DENV.3` | u | Minas Gerais | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.ZIKV.1` | u | Mato Grosso | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.ZIKV.2` | u | Rio de Janeiro | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.ZIKV.3` | u | Bahia | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.CHIKV.1` | d1 | 227.8 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.CHIKV.2` | d1 | 215.0 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.CHIKV.3` | d1 | 202.5 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.DENV.1` | d1 | 1,783.7 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.DENV.2` | d1 | 1,693.6 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.DENV.3` | d1 | 1,539.0 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.ZIKV.1` | d1 | 72.7 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.ZIKV.2` | d1 | 42.7 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.ZIKV.3` | d1 | 41.3 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_of_topcases.CHIKV.1` | ord | fourth | `outputs/geo_spatial_stats.xlsx / Mean_Incidence (rank of the state with the k-th largest case total)` |
| `rank_of_topcases.ZIKV.1` | ord | second | `outputs/geo_spatial_stats.xlsx / Mean_Incidence (rank of the state with the k-th largest case total)` |
| `rank_of_topcases.ZIKV.2` | ord | third | `outputs/geo_spatial_stats.xlsx / Mean_Incidence (rank of the state with the k-th largest case total)` |
| `regmax.DENV.N` | i | 95,753 | `db/normalized_fact_cases.csv` |
| `regmax.DENV.NE` | i | 636,339 | `db/normalized_fact_cases.csv` |
| `regmax.ZIKV.S` | i | 830 | `db/normalized_fact_cases.csv` |
| `regmax_uf.DENV.N` | u | Pará | `db/normalized_fact_cases.csv` |
| `regmax_uf.DENV.NE` | u | Bahia | `db/normalized_fact_cases.csv` |
| `regmax_uf.ZIKV.S` | u | Paraná | `db/normalized_fact_cases.csv` |
| `regmin.DENV.N` | i | 4,867 | `db/normalized_fact_cases.csv` |
| `regmin.DENV.NE` | i | 25,362 | `db/normalized_fact_cases.csv` |
| `regmin.ZIKV.S` | i | 249 | `db/normalized_fact_cases.csv` |
| `regmin_uf.DENV.N` | u | Roraima | `db/normalized_fact_cases.csv` |
| `regmin_uf.DENV.NE` | u | Sergipe | `db/normalized_fact_cases.csv` |
| `regmin_uf.ZIKV.S` | u | Santa Catarina | `db/normalized_fact_cases.csv` |
| `seas.CHIKV.h2_max` | i | 109,102 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.h2_min` | i | 28,639 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.m1` | i | 100,946 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.m5` | i | 271,538 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.m6` | i | 170,494 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.q4_share` | pct1 | 6.4% | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.h2_max` | i | 460,755 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.h2_min` | i | 187,670 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.m1` | i | 1,066,320 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.m2` | i | 2,246,788 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.m6` | i | 1,075,374 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.marapr_mean` | i | 3,678,888 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.q4_share` | pct1 | 4.8% | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.h2_max` | i | 10,110 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.h2_min` | i | 4,016 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.m1` | i | 34,312 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.m3` | i | 70,710 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.m5` | i | 29,333 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.m6` | i | 15,804 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.q4_share` | pct1 | 4.2% | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `sp.CHIKV.Rain.0.mean` | d3 | 0.094 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Rain.1.mean` | d3 | 0.226 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Rain.2.mean` | d3 | 0.295 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Rain.2.prop` | pct0 | 85% | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.0.mean` | d3 | −0.128 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.1.mean` | d3 | −0.044 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.mean` | d3 | 0.058 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.nsig` | i | 17 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.reg.NE` | d3 | −0.149 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.reg.SE` | d3 | 0.360 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.top1.rho` | d3 | 0.531 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.top1.uf` | u | Paraná | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.top2.rho` | d3 | 0.528 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.top2.uf` | u | Santa Catarina | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Rain.0.mean` | d3 | 0.218 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Rain.1.mean` | d3 | 0.376 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Rain.2.mean` | d3 | 0.432 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Rain.2.prop` | pct0 | 85% | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.0.mean` | d3 | −0.146 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.1.mean` | d3 | −0.016 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.mean` | d3 | 0.137 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.nneg` | i | 5 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.npos` | i | 13 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.nsig` | i | 18 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.prop` | pct0 | 67% | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.reg.NE` | d3 | −0.126 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.reg.SE` | d3 | 0.546 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top1.rho` | d3 | 0.607 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top1.uf` | u | Minas Gerais | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top2.rho` | d3 | 0.591 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top2.uf` | u | Rio de Janeiro | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top3.rho` | d3 | 0.555 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top3.uf` | u | São Paulo | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top4.rho` | d3 | 0.538 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top4.uf` | u | Paraná | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Rain.0.mean` | d3 | 0.120 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Rain.1.mean` | d3 | 0.206 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Rain.2.mean` | d3 | 0.243 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Rain.2.prop` | pct0 | 67% | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.0.mean` | d3 | −0.117 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.1.mean` | d3 | −0.074 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.mean` | d3 | −0.016 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.reg.NE` | d3 | −0.151 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.reg.SE` | d3 | 0.191 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.top1.rho` | d3 | 0.303 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.top1.uf` | u | Espírito Santo | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.top2.rho` | d3 | 0.295 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.top2.uf` | u | Minas Gerais | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.CHIKV.Rain.2` | i | 23 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.CHIKV.Temp.2` | i | 12 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.DENV.Rain.2` | i | 19 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.DENV.Temp.2` | i | 12 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.ZIKV.Rain.2` | i | 19 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.ZIKV.Temp.2` | i | 10 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `zika_ratio_max` | d1 | 62.6 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `zika_ratio_min` | d1 | 12.2 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |

## 4. Values taken verbatim from other repository documents

- Figure legends: `docs/FIGURE_CAPTIONS.md` (generated by `build/gen_captions.py` from `outputs/figure_caption_values.csv`, `figure_exclusions*.csv`). Renumbered by order of citation; "UF" becomes "FU"; American spelling; legends of S4 and S5 note that rainfall is drawn per 1 mm while the text uses 100 mm.
- Literature thresholds (Liu 2023: 14.8 °C minimum, 32–33 °C optimum maximum; Lim 2025; Moura 2020 at abstract level; de Lima 2026: DENV-3 detection in Ceará in July 2025): `docs/LITERATURE_CONTEXT.md` (its numbers predate round 2 and are not used).
- Not verified against the original source: the Espirito Santo 2021 counts (2,901 chikungunya, 872 Zika) quoted in the old caption file; the cited page could not be read, so the numbers are left out of the manuscript (author query attached, still open).

## 5. Derived values (not in any output file)

- Rainfall IRR per 10 and per 100 mm = exp(k × Coef) and exp(k × (Coef ± c × SE)) from `glm_negbin_pooled_fe.csv`, with c = 1.96 (the critical value implied by the exported CI). 100 mm ≈ 1 SD of monthly rainfall (100 mm).
- Pooled lagged model: the IRR of a change sustained over lags 0–2 is exp(sum of the three lag coefficients) with the variance taken from the FU-clustered covariance matrix (columns `Temp_Cum0_2`, `Rain_Cum0_2` of the pooled lagged CSV).
- Seasonal totals: sums of `db/normalized_fact_cases.csv` by calendar month over 2016–2025 (complete years). Ratios of Zika 2016 incidence to later years from `Figure1.xlsx`.
- Hospitalization, serotype and discard shares: ratios of the counts in `source_data/Figure5/7/8.xlsx` and `clinical_tables/discarded_counts.csv`.

## 6. Independent verification

`build/recompute.py` recomputes, from `db/` and the source tables and without using `numbers.csv` or the R outputs, and looks for the result in the manuscript text: case totals, 2024 dengue and 2016 Zika, state totals, national incidence, population-weighted mean incidence (GO, DF, MT, CE, RJ), Mann–Kendall τ and Sen's slope (dengue RS, chikungunya MS), Spearman ρ (dengue MG, RJ; national means of dengue and chikungunya temperature, Zika), global Moran's I for the three diseases from polygon centroids, the pooled Poisson and NB2 temperature IRRs and the rainfall IRR per 100 mm by refitting the model by IRLS, the hospitalization and serotype counts, chikungunya men, and the pooled January and May totals. **Result: 43 of 43 matched.** The stored monthly incidence in `db/` is rounded to 2 decimals; the independent Spearman uses the same rounding (without it the dengue MG value differs in the third decimal, 0.608 instead of 0.607).

## 7. Data-quality findings and open points

- **Discarded notifications: handled.** All three diseases now exclude them (section 0). Judgement to confirm: the early-2016 chikungunya form codes confirmed / discarded as 1 / 2 (like the Zika form), the later form as 13 / 5. On the 2016 file codes 1 and 2 follow the same January–April pattern and the same 2.2 : 1 ratio as 13 and 5, and code 2 has almost no deaths from the disease (4 of 28,500, against 0 for code 5), while code 1 behaves as confirmed; so codes 2 and 5 are treated as discarded for chikungunya. Please confirm with the BMoH data dictionary.
- **Annualized 2026.** ×12/9 overstates 2026 because October–December hold 4.8% / 6.4% / 4.2% of the cases (dengue / chikungunya / Zika, 2016–2025). 2026 enters the trends, mean incidence, Moran's I and LISA, with the qualifier required by comment 51. No sensitivity analysis without 2026 was run (not requested).
- **Zero months.** Excluding discarded notifications leaves many state-months without cases; they are zeros inside the observed span (otherwise annualization and the models would use only the months with cases). Espirito Santo 2021 (chikungunya and Zika) has no notification at all in the national files and stays missing; the national totals of those two diseases are therefore slightly low for 2021. Source of the gap unverified.
- **Clinical tables.** Figures 5, 7, 8 now come from `clinical_tables/clinical_demographic_long.csv`. Fixes in the ETL: age parsing (the 2016–2020 files store age as a float string such as "4003.0", so every age of those files was read as unknown), SINAN age bands, disease-specific classification labels with an `Unclassified` (not yet classified) category. The old GraphPad tables (`reference/graphpad_data`) are kept for comparison only.
- **Serotype value 0** (not a valid serotype; 134,407 records in 2023) is folded into Ign/Blank in Figure 7D. The author query remains open; Methods do not yet describe it.
- **Figure 7A/7B labels**: the panel previously called "ELISA" is the NS1 antigen result (SINAN field RESUL_NS1, matched by yearly counts); 7B is the IgM serology. Now labelled so. Please confirm.
- **Zika lag**: the pooled lagged model peaks at lag 1 while the per-FU lagged models have most significant FU at lag 2 (the text says both).
- **Espirito Santo counts** (2,901 chikungunya and 872 Zika, January–October 2021) are still unverified.

## 8. Figure map (numbers by order of first citation)

| Manuscript | Draft (old numbering) | Repository files | Copy in `docs/manuscript/figures/` |
|---|---|---|---|
| Figure 1 | Fig 2 incidence | `Figure1_incidence_regional.png` | `Figure1.png` |
| Figure 2 | Fig 1A–B maps | `Figure6_combined_map.png` | `Figure2.png` |
| Figure 3 | Fig 3 Moran scatter | `Figure4_spatial_autocorrelation.png` | `Figure3.png` |
| Figure 4 | Fig 7 trends | `Figure2_trend_analysis.png` | `Figure4.png` |
| Figure 5 | Fig 8 correlations | `Figure3_climate_correlations.png` | `Figure5.png` |
| Figure 6 | Fig 4 age and sex | `Figure5_demographics.png` | `Figure6.png` |
| Figure 7 | Fig 5 dengue clinical | `Figure7_dengue_clinical.png` | `Figure7.png` |
| Figure 8 | Fig 6 chikungunya and Zika clinical | `Figure8_chikv_zika_clinical.png` | `Figure8.png` |
| Supplementary Figure S1 | Fig 1C annual maps | `FigureS1_overview.png`, `FigureS1_2016.png`, `FigureS1_2017.png`, `FigureS1_2018.png`, `FigureS1_2019.png`, `FigureS1_2020.png`, `FigureS1_2021.png`, `FigureS1_2022.png`, `FigureS1_2023.png`, `FigureS1_2024.png`, `FigureS1_2025.png`, `FigureS1_2026.png` | `FigureS1_overview.png`, `FigureS1_2016.png`, `FigureS1_2017.png`, `FigureS1_2018.png`, `FigureS1_2019.png`, `FigureS1_2020.png`, `FigureS1_2021.png`, `FigureS1_2022.png`, `FigureS1_2023.png`, `FigureS1_2024.png`, `FigureS1_2025.png`, `FigureS1_2026.png` |
| Supplementary Figure S2 | Fig 1D LISA and trend maps | `FigureS2_lisa_trend.png` | `FigureS2.png` |
| Supplementary Figure S3 | S5 AIC | `glm_fig4_aic_comparison.png` | `FigureS3.png` |
| Supplementary Figure S4 | S6 pooled | `glm_fig1_pooled_climate_irr.png` | `FigureS4.png` |
| Supplementary Figure S5 | S7/S8 per-state | `glm_fig2_per_state_heatmap.png` | `FigureS5.png` |
| Supplementary Figure S6 | S7/S8 per-state | `glm_fig5_forest_significant.png` | `FigureS6.png` |
| Supplementary Figure S7 | S9 lag profile | `glm_fig3_lag_profile.png` | `FigureS7.png` |
| not cited | S1A–C state totals, S2A–C seasonal heatmaps, Table S11 | `outputs/*_05_federative_unit_totals.png`, `*_01b_monthly_heatmap.png`, `outputs/glm_*_results.xlsx` | |

## 9. Reference list

70 references: the 62 of the draft, converted from ASM to NLM/AMA style and renumbered by order of first citation (the Methods precede the Results), plus new entries (Liu 2023, Moura 2020, Lim 2025, de Lima 2026, IBGE projections and DOU estimates, INMET, Governo do Espírito Santo 2021). No DOIs were added except those already in the draft or given in `docs/LITERATURE_CONTEXT.md`; journal abbreviations are those of the draft. Rule used for authors: more than 6 → first 3 + et al (AMA); **unverified for JMV**.
