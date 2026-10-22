# Manuscript sync log: draft (2016–2025, Python) → JMV manuscript (2016–2026, R)

Written 2026-10-21. Covers `Alves ER et al JMV 2026.docx` (clean) and `Alves ER et al JMV 2026 (redline).docx` (every text change tracked, author *Claude for ERA*), both built from `Alves ER et al JVI 2026.docx`, which was not modified.

**How the numbers were produced.** Every number in the Abstract, Results, Discussion and Methods was computed from the repository files by `build/numbers.R` (R 4.6.1) into `numbers.csv`, and inserted into the text by key. The table in section 3 lists each inserted number with its source file. Legends are the text of `docs/FIGURE_CAPTIONS.md`. A second, independent computation in Python (section 6) reproduced 40 headline values from the raw tables.

## 1. Headline changes in the claims

The regenerated results (R, 2016–2026) reverse several statements of the draft (Python, 2016–2025). The manuscript text was rewritten to what the regenerated outputs show. Items marked **⇄** change the interpretation and need the co-authors' attention.

| | Draft | Manuscript | Source |
|---|---|---|---|
| Moran's I, dengue / chikungunya / Zika | 0.562 (p = 0.001) / −0.036 (0.460) / −0.008 (0.352) | 0.516 / 0.004 / −0.006 (p 0.001 / 0.285 / 0.326) | `outputs/geo_spatial_stats.xlsx`, Global_Moran |
| Mean annual incidence, dengue top 3 | DF 1,825.6; GO 1,742.7; MG 1,647.7 | GO 1,782.4; DF 1,693.7; MG 1,538.7 | `geo_spatial_stats.xlsx`, Mean_Incidence |
| Chikungunya top mean incidence | MS 421.8 | MS 498.4; CE 324.9; MT 294.5 | same |
| Zika top mean incidence | TO 145.7; MT 106.7 | TO 136.9; MT 98.4 | same |
| ⇄ Dengue increasing trends | RS, SC, SP | RS (τ 0.600), SC (τ 0.491); SP not significant (p = 0.161) | `py_statistical_results.xlsx`, Mann_Kendall |
| ⇄ Chikungunya increasing trends | SC, RS, MS | MS, MG, GO; SC (p = 0.119) and RS (p = 0.161) not significant | same |
| ⇄ Zika decreasing trends | AL, PI, DF (3 states) | 6 states (DF, PI, MG, RJ, AL, PR) | same |
| ⇄ Multiple testing | "no adjustment" | Benjamini–Hochberg q-values reported; no trend survives (minimum q: dengue 0.344, chikungunya 0.137, Zika 0.110) | Mann_Kendall, q_value |
| Dengue LISA high–high | Central-West and Southeast | also Paraná; after BH correction only GO, MG (HH) and RJ (LH) | `geo_spatial_stats.xlsx`, LISA_Clusters |
| Zika 2016 vs later years | "roughly 8–10 times" | 6.8–14.9 times (complete years 2017–2025) | `source_data/Figure1.xlsx` |
| ⇄ Pooled temperature IRR, dengue | 2.10 (1.96–2.26) | 1.10 (1.02–1.19) | `outputs/glm_negbin_pooled_fe.csv` |
| ⇄ Pooled temperature IRR, chikungunya | 1.32 (1.24–1.41), significant | 1.05 (0.99–1.12), **not significant** | same |
| ⇄ Pooled temperature IRR, Zika | 0.90 (0.84–0.97), inverse | 1.09 (1.01–1.18), **positive** | same |
| ⇄ Rainfall | IRR 1.007 per mm; Spearman ρ ≈ 0 | IRR per 100 mm 1.30 / 1.18 / 1.16; mean ρ at lag 2 0.433 / 0.355 / 0.347 | glm CSVs; `Spearman_Lag` |
| Temperature Spearman ρ (national mean) | dengue 0.16 → 0.19, "positive at all lags" | dengue −0.147 / −0.018 / 0.137 at lags 0 / 1 / 2 (negative, ~0, positive) | `Spearman_Lag` |
| NB2 dispersion α | 1.69 / 1.45 / 1.55 | 1.23 / 1.20 / 1.21 | pooled CSV |
| Per-state temperature, significant FU | 16 / 12 / 10 | 14 / 9 / 7 | `glm_negbin_per_state.csv` |
| Lag-2 temperature, significant FU | 11 / 4 / 7 | 11 / 7 / 8 | `glm_negbin_lagged.csv` |
| Hospitalization (comment 13) | 15,788,792 not hospitalized; 529,203 hospitalized | 529,203 hospitalized; 10,642,808 not; 5,145,984 ignored/blank (sum 16,317,995) | `source_data/Figure7.xlsx` |
| Placeholders | [X], xxxxx, [REF IBGE??] | chikungunya men 800,258; DENV-2 117,958; DENV-3 8,766; DENV-4 747; IBGE references added | Figure 5/7 source data |
| Chikungunya peak year | (comment 9) | 2024 (200.5 per 100,000), second 2016 (155.3); Central-West 2025 702.5 | `Figure1.xlsx` |

## 2. Methods statements rewritten to what the code does

| Draft statement | Manuscript statement | Evidence in the repository |
|---|---|---|
| Analyses in Python 3.12 (pandas, statsmodels, GeoPandas…) | R 4.6.1; data.table, readxl, sf, spdep, classInt, ggplot2, patchwork | `R_SESSION_INFO.txt`; `docs/R_PORT_NOTES.md` |
| Temperature from CPC/NCEP grid; rainfall from INMET and CPTEC/INPE | INMET hourly automatic stations, ≥240 (temperature) / ≥360 (rainfall) valid hourly readings per station-month, unweighted mean per FU | `etl/build_climate.R` lines 4, 30, 106–108, 134–135 |
| Spatial weights: Queen contiguity with kNN fallback | Row-standardized kNN (k = 5) on polygon centroids only | `pipelines/data_loader.R` 141–142; `R/stats.R` 70–73 |
| "No adjustment for multiple comparisons" | Raw p reported with Benjamini–Hochberg q-values | `R/utils.R` 84 (`p.adjust(method = "BH")`); `Significant_FDR` columns |
| Pooled distributed-lag model (comment 16) | Per-FU unconstrained lag model (lags 0–2 jointly); separate pooled constrained DLNM | `pipelines/glm_common.R` `SPECS` 48–51; `pipelines/additional/adv_dlnm.R` |
| "Overdispersion assessed by testing α > 0" (comment 22) | Pearson dispersion of the Poisson fit and ML α; no formal test | `glm_common.R` 156–180; no `lrtest` anywhere |
| State fixed effects only; model-based SE | Pooled: FU + calendar-month FE, FU-clustered SE; per-FU and lagged: month FE, Newey–West (3 lags) | `glm_common.R` 6–21, 38, 44–51, 183–200 |
| Discarded and under-investigation cases excluded; FU of residence | Dengue = notifications minus discarded; chikungunya and Zika = all notifications; FU/month of notification | `etl/build_cases_clinical.R` 88, 116–130; `README.md` 156–160 |
| Population: 2022 Census and intercensal estimates [REF] | IBGE projections (2024 revision) 2016–2023; DOU 1-July estimates 2024–2026 | `etl/build_population.R` 1–6; `docs/DATA_SOURCES.md` 21–28 |
| Study period to December 31, 2025 | To September 30, 2026; 2026 annualized as cases × 12 / months | `pipelines/data_loader.R` 77–90 |

## 3. Every number inserted into the text, with its source

`key` is the entry in `build/numbers.csv`. Formats: `i` integer, `dN` N decimals, `pct` percent, `pv` p-value, `s` text, `ord`/`words` spelled.

| Key | Format | Text | Source |
|---|---|---|---|
| `ann.CHIKV.BR.2016` | d1 | 155.3 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.CHIKV.BR.2024` | d1 | 200.5 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.DENV.BR.2023` | d0 | 778 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.DENV.BR.2024` | d0 | 3,088 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.DENV.BR.2026` | d0 | 290 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann.ZIKV.BR.2016` | d0 | 138 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `ann_state.CHIKV.MS.2025` | d0 | 1,726 | `outputs/py_statistical_results.xlsx / Annual_Incidence` |
| `ann_state.CHIKV.MT.2025` | d0 | 1,709 | `outputs/py_statistical_results.xlsx / Annual_Incidence` |
| `cases.CHIKV.all` | i | 2,445,247 | `db/normalized_fact_cases.csv` |
| `cases.DENV.all` | i | 16,799,392 | `db/normalized_fact_cases.csv` |
| `cases.DENV.y2024` | i | 6,564,924 | `db/normalized_fact_cases.csv` |
| `cases.DENV.y2024` | mil2 | 6.56 | `db/normalized_fact_cases.csv` |
| `cases.ZIKV.all` | i | 559,043 | `db/normalized_fact_cases.csv` |
| `cases.ZIKV.y2016` | i | 281,464 | `db/normalized_fact_cases.csv` |
| `chik_regmax_val` | d1 | 702.5 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `cl.CHIKV.age.20_39` | i | 690,798 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.CHIKV.age.40_59` | i | 599,167 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.CHIKV.class.IgnBlank` | i | 214,989 | `source_data/Figure8.xlsx / Fig8A1_Chik_Classfic` |
| `cl.CHIKV.class.all` | i | 1,994,043 | `source_data/Figure8.xlsx / Fig8A1_Chik_Classfic` |
| `cl.CHIKV.conf` | i | 1,078,333 | `source_data/Figure8.xlsx / Fig8A1_Chik_Classfic` |
| `cl.CHIKV.crit.Ininvestigation` | i | 29,962 | `source_data/Figure8.xlsx / Fig8A2_Chik_Criteria` |
| `cl.CHIKV.disc` | i | 700,721 | `source_data/Figure8.xlsx / Fig8A1_Chik_Classfic` |
| `cl.CHIKV.disc_share` | pct1 | 35.1% | `source_data/Figure8.xlsx / Fig8A1_Chik_Classfic` |
| `cl.CHIKV.evo.Cure` | i | 1,553,880 | `source_data/Figure8.xlsx / Fig8A3_Chik_Evolutio` |
| `cl.CHIKV.evo.Death` | i | 1,106 | `source_data/Figure8.xlsx / Fig8A3_Chik_Evolutio` |
| `cl.CHIKV.sex.F` | i | 1,191,567 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.CHIKV.sex.M` | i | 800,258 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.CHIKV.sex.ratio` | d1 | 1.5 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.DENV.age.20_59` | i | 10,190,286 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.DENV.age.20_59_share` | pct1 | 62.5% | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.DENV.age.known` | i | 16,299,054 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.DENV.hosp.IgnBlank` | i | 5,145,984 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.Negative` | i | 10,642,808 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.Positive` | i | 529,203 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.known` | i | 11,172,011 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.share_known` | pct1 | 4.7% | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.hosp.total` | i | 16,317,995 | `source_data/Figure7.xlsx / Fig7C_Hospitalization` |
| `cl.DENV.sero.DENV1` | i | 208,452 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.DENV2` | i | 117,958 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.DENV3` | i | 8,766 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.DENV4` | i | 747 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.typed` | i | 335,923 | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero.typed_share` | pct1 | 2.1% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV2.2023` | pct1 | 12.8% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV2.2024` | pct1 | 30.5% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV2.2025` | pct1 | 73.8% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV3.2023` | pct1 | 0.2% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV3.2024` | pct1 | 0.9% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sero_share.DENV3.2025` | pct1 | 13.9% | `source_data/Figure7.xlsx / Fig7D_Serotype` |
| `cl.DENV.sex.F` | i | 8,930,141 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.DENV.sex.M` | i | 7,366,070 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.DENV.sex.ratio` | d2 | 1.21 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.age.20_39` | i | 227,790 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.ZIKV.age.40_59` | i | 125,131 | `source_data/Figure5.xlsx / Fig5A_age_group_counts` |
| `cl.ZIKV.class.all` | i | 545,864 | `source_data/Figure8.xlsx / Fig8B1_Zika_Classifi` |
| `cl.ZIKV.conf` | i | 178,938 | `source_data/Figure8.xlsx / Fig8B1_Zika_Classifi` |
| `cl.ZIKV.disc` | i | 252,266 | `source_data/Figure8.xlsx / Fig8B1_Zika_Classifi` |
| `cl.ZIKV.disc_share` | pct1 | 46.2% | `source_data/Figure8.xlsx / Fig8B1_Zika_Classifi` |
| `cl.ZIKV.incl` | i | 102,483 | `source_data/Figure8.xlsx / Fig8B1_Zika_Classifi` |
| `cl.ZIKV.malesh_max` | pct0 | 41% | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.malesh_maxyear` | y | 2023 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.malesh_min` | pct0 | 30% | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.malesh_minyear` | y | 2017 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.preg.1Trimester` | i | 14,583 | `source_data/Figure8.xlsx / Fig8B4_Zika_Pregnanc` |
| `cl.ZIKV.preg.2Trimester` | i | 20,976 | `source_data/Figure8.xlsx / Fig8B4_Zika_Pregnanc` |
| `cl.ZIKV.preg.3Trimester` | i | 19,942 | `source_data/Figure8.xlsx / Fig8B4_Zika_Pregnanc` |
| `cl.ZIKV.preg.tri_sum` | i | 55,501 | `source_data/Figure8.xlsx / Fig8B4_Zika_Pregnanc` |
| `cl.ZIKV.sex.F` | i | 357,840 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.sex.M` | i | 188,209 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `cl.ZIKV.sex.ratio` | d1 | 1.9 | `source_data/Figure5.xlsx / Fig5B_sex` |
| `clim.n_states_2026` |  | 26 | `db/normalized_fact_climate.csv` |
| `clim.rain_sd` | d0 | 100 | `db/normalized_fact_climate.csv` |
| `ct.sero_share.DENV2.2026` | pct1 | 64.2% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_share.DENV3.2024` | pct1 | 0.9% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_share.DENV3.2025` | pct1 | 14.0% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_share.DENV3.2026` | pct1 | 29.9% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_typed_pct.2026` | pct1 | 7.1% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_typed_pct_max` | pct1 | 3.0% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `ct.sero_typed_pct_min` | pct1 | 0.2% | `clinical_tables/clinical_demographic_long.csv (serotype)` |
| `dlnm.CHIKV.opt` | d1 | 25.6 | `outputs/2026-10-08/additional/dlnm_summary.csv` |
| `dlnm.DENV.irr` | d2 | 1.18 | `outputs/2026-10-08/additional/dlnm_summary.csv` |
| `dlnm.DENV.opt` | d1 | 27.2 | `outputs/2026-10-08/additional/dlnm_summary.csv` |
| `dlnm.ZIKV.irr` | d2 | 1.34 | `outputs/2026-10-08/additional/dlnm_summary.csv` |
| `dlnm.ZIKV.opt` | d1 | 29.6 | `outputs/2026-10-08/additional/dlnm_summary.csv` |
| `dlnm.ref.Temp` | d1 | 25.4 | `outputs/2026-10-08/additional/dlnm_exposure_response.csv` |
| `fe.DENV.elisa.pct2025` | d0 | 98 | `outputs/figure_exclusions.csv` |
| `fe.DENV.elisa.pctmax1624` | d0 | 53 | `outputs/figure_exclusions.csv` |
| `fe.DENV.elisa.pctmin1624` | d0 | 35 | `outputs/figure_exclusions.csv` |
| `fe.DENV.hosp.pct` | d1 | 31.5 | `outputs/figure_exclusions.csv` |
| `fe.DENV.igm.pctmax1624` | d0 | 49 | `outputs/figure_exclusions.csv` |
| `fe.DENV.igm.pctmin1624` | d0 | 34 | `outputs/figure_exclusions.csv` |
| `fe.DENV.sero.pct` | d1 | 97.9 | `outputs/figure_exclusions.csv` |
| `glml.CHIKV.Rain_Lag2.nsig` | i | 7 | `outputs/glm_negbin_lagged.csv` |
| `glml.CHIKV.Temp_Avg.nsig` | i | 3 | `outputs/glm_negbin_lagged.csv` |
| `glml.CHIKV.Temp_Lag1.nsig` | i | 4 | `outputs/glm_negbin_lagged.csv` |
| `glml.CHIKV.Temp_Lag2.medirr_sigpos` | d2 | 1.52 | `outputs/glm_negbin_lagged.csv` |
| `glml.CHIKV.Temp_Lag2.npos` | i | 4 | `outputs/glm_negbin_lagged.csv` |
| `glml.CHIKV.Temp_Lag2.nsig` | i | 7 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Rain_Lag2.nsig` | i | 13 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Avg.nsig` | i | 10 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Lag1.nsig` | i | 9 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Lag2.medirr_sigpos` | d2 | 1.62 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Lag2.nfdr` | i | 10 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Lag2.npos` | i | 9 | `outputs/glm_negbin_lagged.csv` |
| `glml.DENV.Temp_Lag2.nsig` | i | 11 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Rain_Lag2.nsig` | i | 10 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Temp_Avg.nsig` | i | 3 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Temp_Lag1.nsig` | i | 1 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Temp_Lag2.medirr_sigpos` | d2 | 1.30 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Temp_Lag2.npos` | i | 6 | `outputs/glm_negbin_lagged.csv` |
| `glml.ZIKV.Temp_Lag2.nsig` | i | 8 | `outputs/glm_negbin_lagged.csv` |
| `glmp.CHIKV.Rain_mm.hi100` | d2 | 1.33 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef + crit x SE)))` |
| `glmp.CHIKV.Rain_mm.irr100` | d2 | 1.18 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x Coef))` |
| `glmp.CHIKV.Rain_mm.lo100` | d2 | 1.06 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef - crit x SE)))` |
| `glmp.CHIKV.Temp_Avg.hi` | d2 | 1.12 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.CHIKV.Temp_Avg.irr` | d2 | 1.05 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.CHIKV.Temp_Avg.lo` | d2 | 0.99 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.CHIKV.Temp_Avg.p` | pv | = 0.103 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.CHIKV.alpha` | d2 | 1.20 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.Rain_mm.hi100` | d2 | 1.48 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef + crit x SE)))` |
| `glmp.DENV.Rain_mm.irr100` | d2 | 1.30 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x Coef))` |
| `glmp.DENV.Rain_mm.lo100` | d2 | 1.13 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef - crit x SE)))` |
| `glmp.DENV.Temp_Avg.hi` | d2 | 1.19 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.Temp_Avg.irr` | d2 | 1.10 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.Temp_Avg.lo` | d2 | 1.02 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.Temp_Avg.p` | pv | = 0.009 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.aic` | i | 55,643 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.DENV.alpha` | d2 | 1.23 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.Rain_mm.hi100` | d2 | 1.30 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef + crit x SE)))` |
| `glmp.ZIKV.Rain_mm.irr100` | d2 | 1.16 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x Coef))` |
| `glmp.ZIKV.Rain_mm.lo100` | d2 | 1.04 | `outputs/glm_negbin_pooled_fe.csv (exp(100 x (Coef - crit x SE)))` |
| `glmp.ZIKV.Temp_Avg.hi` | d2 | 1.18 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.Temp_Avg.irr` | d2 | 1.09 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.Temp_Avg.lo` | d2 | 1.01 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.Temp_Avg.p` | pv | = 0.035 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmp.ZIKV.alpha` | d2 | 1.21 | `outputs/glm_negbin_pooled_fe.csv` |
| `glmpois.CHIKV.Temp_Avg.irr` | d2 | 1.20 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.CHIKV.disp` | i | 1,794 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.DENV.Temp_Avg.irr` | d2 | 1.48 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.DENV.aic` | i | 22,299,664 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.DENV.disp` | i | 9,884 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.ZIKV.Temp_Avg.irr` | d2 | 1.33 | `outputs/glm_poisson_pooled_fe.csv` |
| `glmpois.ZIKV.disp` | i | 762 | `outputs/glm_poisson_pooled_fe.csv` |
| `glms.CHIKV.Rain_mm.npos` | i | 4 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Rain_mm.nsig` | i | 6 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Temp_Avg.medirr_sigpos` | d2 | 1.55 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Temp_Avg.nfdr` | i | 6 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Temp_Avg.npos` | i | 6 | `outputs/glm_negbin_per_state.csv` |
| `glms.CHIKV.Temp_Avg.nsig` | i | 9 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Rain_mm.npos` | i | 10 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Rain_mm.nsig` | i | 10 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.medirr_sigpos` | d2 | 1.79 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.nfdr` | i | 12 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.nneg` | i | 2 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.npos` | i | 12 | `outputs/glm_negbin_per_state.csv` |
| `glms.DENV.Temp_Avg.nsig` | i | 14 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Rain_mm.nneg` | i | 3 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Rain_mm.nsig` | i | 3 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Temp_Avg.medirr_sigpos` | d2 | 1.51 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Temp_Avg.nfdr` | i | 0 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Temp_Avg.nfdr` | nz | no | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Temp_Avg.npos` | i | 5 | `outputs/glm_negbin_per_state.csv` |
| `glms.ZIKV.Temp_Avg.nsig` | i | 7 | `outputs/glm_negbin_per_state.csv` |
| `lisa_names.CHIKV.HH` | s | Paraíba | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.CHIKV.HL` | s | Roraima | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.CHIKV.LH` | s | Alagoas | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.DENV.HH` | s | the Federal District, Espírito Santo, Goiás, Mato Grosso, Mato Grosso do Sul, Minas Gerais, Paraná and São Pau | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.DENV.LL` | s | Amapá, Maranhão, Rio Grande do Norte and Roraima | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.ZIKV.HH` | s | Mato Grosso | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.ZIKV.LH` | s | Pará | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_names.ZIKV.LL` | s | Paraná | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_uf.DENV.HL` | ucap | Acre | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisa_uf.DENV.LH` | u | Rio de Janeiro | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisafdr_names.DENV.HH` | s | Goiás and Minas Gerais | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `lisafdr_names.DENV.LH` | s | Rio de Janeiro | `outputs/geo_spatial_stats.xlsx / LISA_Clusters` |
| `mk_minq.CHIKV` | d3 | 0.137 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_minq.DENV` | d3 | 0.344 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_minq.ZIKV` | d3 | 0.110 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_n.ZIKV.decreasing` | words | six | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_names.CHIKV.increasing` | s | Mato Grosso do Sul, Minas Gerais and Goiás | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_names.ZIKV.decreasing` | s | the Federal District, Piauí, Minas Gerais, Rio de Janeiro, Alagoas and Paraná | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_taumax.ZIKV.decreasing` | d3 | −0.527 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mk_taumin.ZIKV.decreasing` | d3 | −0.636 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.1.slope` | d0 | 158 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.1.tau` | d3 | 0.673 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.1.uf` | ucap | Mato Grosso do Sul | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.2.slope` | d0 | 13 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.2.tau` | d3 | 0.564 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.2.uf` | u | Minas Gerais | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.3.slope` | d0 | 12 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.3.tau` | d3 | 0.527 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.CHIKV.increasing.3.uf` | u | Goiás | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.1.slope` | d0 | 54 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.1.tau` | d3 | 0.600 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.1.uf` | ucap | Rio Grande do Sul | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.2.slope` | d0 | 52 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.2.tau` | d3 | 0.491 | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `mkr.DENV.increasing.2.uf` | u | Santa Catarina | `outputs/py_statistical_results.xlsx / Mann_Kendall` |
| `moran.CHIKV.I` | d3 | 0.004 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.CHIKV.p` | pv | = 0.285 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.DENV.I` | d3 | 0.516 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.DENV.p` | pv | = 0.001 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.ZIKV.I` | d3 | −0.006 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `moran.ZIKV.p` | pv | = 0.326 | `outputs/geo_spatial_stats.xlsx / Global_Moran` |
| `n_months` | i | 129 | `db/normalized_fact_cases.csv` |
| `natpeak_ratio_second.DENV` | d1 | 4.0 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `rank_cases.CHIKV.1` | u | Minas Gerais | `db/normalized_fact_cases.csv` |
| `rank_cases.CHIKV.2` | u | Ceará | `db/normalized_fact_cases.csv` |
| `rank_cases.CHIKV.3` | u | Bahia | `db/normalized_fact_cases.csv` |
| `rank_cases.CHIKV.4` | u | Pernambuco | `db/normalized_fact_cases.csv` |
| `rank_cases.CHIKV.5` | u | Rio de Janeiro | `db/normalized_fact_cases.csv` |
| `rank_cases.DENV.1` | ucap | São Paulo | `db/normalized_fact_cases.csv` |
| `rank_cases.DENV.2` | u | Minas Gerais | `db/normalized_fact_cases.csv` |
| `rank_cases.ZIKV.1` | u | Rio de Janeiro | `db/normalized_fact_cases.csv` |
| `rank_cases.ZIKV.2` | u | Bahia | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.1` | i | 448,370 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.2` | i | 323,351 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.3` | i | 244,512 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.4` | i | 199,691 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.CHIKV.5` | i | 198,626 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.DENV.1` | i | 4,873,074 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.DENV.2` | i | 3,545,139 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.ZIKV.1` | i | 95,934 | `db/normalized_fact_cases.csv` |
| `rank_cases_val.ZIKV.2` | i | 87,328 | `db/normalized_fact_cases.csv` |
| `rank_minc.CHIKV.1` | u | Mato Grosso do Sul | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.CHIKV.2` | u | Ceará | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.CHIKV.3` | u | Mato Grosso | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.CHIKV.4` | u | Rio Grande do Norte | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.CHIKV.5` | u | Tocantins | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.DENV.1` | u | Goiás | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.DENV.2` | u | the Federal District | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.DENV.3` | u | Minas Gerais | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.ZIKV.1` | u | Tocantins | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc.ZIKV.2` | u | Mato Grosso | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.CHIKV.1` | d1 | 498.4 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.CHIKV.2` | d1 | 324.9 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.CHIKV.3` | d1 | 294.5 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.DENV.1` | d1 | 1,782.4 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.DENV.2` | d1 | 1,693.7 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.DENV.3` | d1 | 1,538.7 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.ZIKV.1` | d1 | 136.9 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_minc_val.ZIKV.2` | d1 | 98.4 | `outputs/geo_spatial_stats.xlsx / Mean_Incidence` |
| `rank_of_topcases.CHIKV.1` | ord | sixth | `outputs/geo_spatial_stats.xlsx / Mean_Incidence (rank of the state with the k-th largest case total)` |
| `rank_of_topcases.ZIKV.1` | ord | ninth | `outputs/geo_spatial_stats.xlsx / Mean_Incidence (rank of the state with the k-th largest case total)` |
| `rank_of_topcases.ZIKV.2` | ord | seventh | `outputs/geo_spatial_stats.xlsx / Mean_Incidence (rank of the state with the k-th largest case total)` |
| `regmax.DENV.N` | i | 95,597 | `db/normalized_fact_cases.csv` |
| `regmax.DENV.NE` | i | 635,912 | `db/normalized_fact_cases.csv` |
| `regmax.ZIKV.S` | i | 5,977 | `db/normalized_fact_cases.csv` |
| `regmax_uf.DENV.N` | u | Pará | `db/normalized_fact_cases.csv` |
| `regmax_uf.DENV.NE` | u | Bahia | `db/normalized_fact_cases.csv` |
| `regmax_uf.ZIKV.S` | u | Paraná | `db/normalized_fact_cases.csv` |
| `regmin.DENV.N` | i | 4,860 | `db/normalized_fact_cases.csv` |
| `regmin.DENV.NE` | i | 25,323 | `db/normalized_fact_cases.csv` |
| `regmin.ZIKV.S` | i | 2,405 | `db/normalized_fact_cases.csv` |
| `regmin_uf.DENV.N` | u | Roraima | `db/normalized_fact_cases.csv` |
| `regmin_uf.DENV.NE` | u | Sergipe | `db/normalized_fact_cases.csv` |
| `regmin_uf.ZIKV.S` | u | Santa Catarina | `db/normalized_fact_cases.csv` |
| `seas.CHIKV.h2_max` | i | 159,484 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.h2_min` | i | 53,192 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.m1` | i | 154,677 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.m5` | i | 389,863 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.m6` | i | 243,725 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.CHIKV.q4_share` | pct1 | 7.4% | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.h2_max` | i | 460,755 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.h2_min` | i | 187,670 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.m1` | i | 1,066,320 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.m2` | i | 2,246,788 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.m6` | i | 1,075,374 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.marapr_mean` | i | 3,678,888 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.DENV.q4_share` | pct1 | 4.8% | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.h2_max` | i | 25,371 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.h2_min` | i | 10,943 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.m1` | i | 56,176 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.m3` | i | 116,101 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.m5` | i | 62,434 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.m6` | i | 37,573 | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `seas.ZIKV.q4_share` | pct1 | 6.3% | `db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)` |
| `sp.CHIKV.Rain.0.mean` | d3 | 0.145 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Rain.1.mean` | d3 | 0.288 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Rain.2.mean` | d3 | 0.355 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Rain.2.prop` | pct0 | 96% | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.0.mean` | d3 | −0.121 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.1.mean` | d3 | −0.033 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.mean` | d3 | 0.077 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.nsig` | i | 18 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.reg.NE` | d3 | −0.120 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.top1.rho` | d3 | 0.660 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.top1.uf` | u | Santa Catarina | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.top2.rho` | d3 | 0.601 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.CHIKV.Temp.2.top2.uf` | u | Rio Grande do Sul | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Rain.0.mean` | d3 | 0.218 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Rain.1.mean` | d3 | 0.376 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Rain.2.mean` | d3 | 0.433 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Rain.2.prop` | pct0 | 85% | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.0.mean` | d3 | −0.147 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.1.mean` | d3 | −0.018 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.mean` | d3 | 0.137 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.nneg` | i | 5 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.npos` | i | 13 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.nsig` | i | 18 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.prop` | pct0 | 67% | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.reg.CO` | d3 | 0.306 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.reg.NE` | d3 | −0.126 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.reg.S` | d3 | 0.465 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.reg.SE` | d3 | 0.545 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top1.rho` | d3 | 0.607 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top1.uf` | u | Minas Gerais | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top2.rho` | d3 | 0.589 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top2.uf` | u | Rio de Janeiro | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top3.rho` | d3 | 0.556 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top3.uf` | u | São Paulo | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top4.rho` | d3 | 0.539 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.DENV.Temp.2.top4.uf` | u | Paraná | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Rain.0.mean` | d3 | 0.161 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Rain.1.mean` | d3 | 0.296 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Rain.2.mean` | d3 | 0.347 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Rain.2.prop` | pct0 | 81% | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.0.mean` | d3 | −0.105 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.1.mean` | d3 | −0.024 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.mean` | d3 | 0.079 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.reg.NE` | d3 | −0.101 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.top1.rho` | d3 | 0.589 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.top1.uf` | u | São Paulo | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.top2.rho` | d3 | 0.554 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp.ZIKV.Temp.2.top2.uf` | u | Santa Catarina | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.CHIKV.Rain.2` | i | 23 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.CHIKV.Temp.2` | i | 12 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.DENV.Rain.2` | i | 19 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.DENV.Temp.2` | i | 12 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.ZIKV.Rain.2` | i | 23 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `sp_bestlag.ZIKV.Temp.2` | i | 15 | `outputs/py_statistical_results.xlsx / Spearman_Lag` |
| `zika_ratio_max` | d1 | 14.9 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |
| `zika_ratio_min` | d1 | 6.8 | `source_data/Figure1.xlsx / Fig1A_annual_incidence` |

## 4. Values taken verbatim from other repository documents

- Figure legends: `docs/FIGURE_CAPTIONS.md` (generated from `outputs/figure_caption_values.csv`, `figure_exclusions*.csv`). Renumbered: the five GLM figures become Supplementary Figures S3–S7; "UF" becomes "FU"; American spelling; legends of S3 and S4 note that rainfall is drawn per 1 mm while the text uses 100 mm.
- Literature thresholds (Liu 2023: 14.8 °C minimum, 32–33 °C optimum maximum; Lim 2025; Moura 2020 at abstract level; de Lima 2026: DENV-3 detection in Ceará in July 2025): `docs/LITERATURE_CONTEXT.md`.
- Not verified against the original source: the Espirito Santo 2021 counts (2,901 chikungunya, 872 Zika) quoted in `docs/FIGURE_CAPTIONS.md`; the cited page could not be read, so the numbers are left out of the manuscript (author query attached).

## 5. Derived values (not in any output file)

- Rainfall IRR per 10 and per 100 mm = exp(k × Coef) and exp(k × (Coef ± c × SE)) from `glm_negbin_pooled_fe.csv`, with c = 1.96 (the critical value implied by the exported CI). 100 mm ≈ 1 SD of monthly rainfall (100 mm).
- Seasonal totals: sums of `db/normalized_fact_cases.csv` by calendar month over 2016–2025 (complete years). Ratios of Zika 2016 incidence to later years from `Figure1.xlsx`.
- Hospitalization, serotype and discard shares: ratios of the counts in `source_data/Figure5/7/8.xlsx`.

## 6. Independent verification

`build/recompute.py` recomputes, from `db/` and the source tables and without using `numbers.csv` or the R outputs, and looks for the result in the manuscript text: case totals, 2024 dengue and 2016 Zika, state totals, national incidence, population-weighted mean incidence (GO, DF, MS, TO), Mann–Kendall τ and Sen's slope (dengue RS, chikungunya MS), Spearman ρ (dengue MG, RJ; national means), global Moran's I for the three diseases from polygon centroids, the pooled Poisson and NB2 temperature IRRs and the rainfall IRR per 100 mm by refitting the model by IRLS, the hospitalization and serotype counts, chikungunya men, and the pooled January and May totals. **Result: 40 of 40 matched.**

## 7. Data-quality findings that need a decision (not fixed here)

- **Discarded notifications.** Chikungunya and Zika include discarded notifications (comments 18–19). Dengue excludes them. Changing this means rerunning the pipeline: the Zika discard code is 2, not 5 (2016: 62,198 records, equal to the GraphPad "Discarded" count), and chikungunya 2016 has 102,858 records with legacy classification codes 1 and 2 (shown as "Dengue classico" and "Dengue c/ complicacoes") whose meaning is not documented.
- **Annualized 2026.** ×12/9 overstates 2026 because October–December hold 4.8% / 7.4% / 6.3% of the cases (dengue / chikungunya / Zika, 2016–2025). 2026 enters the trends, mean incidence, Moran's I and LISA.
- **GraphPad tables (Figures 5, 7, 8)** end in 2025. Their yearly dengue totals are below `clinical_tables/` by 3,954 (2020), 8,238 (2021), 10,563 (2022) and 998 (2023); the 2021–2022 gaps are close to the Espírito Santo notifications in `clinical_tables/` (8,726 and 11,218). The former state-total and monthly-heatmap figures end in 2025 as well and are not cited.
- **`clinical_tables/clinical_demographic_long.csv`**: age is 100% ignored for dengue 2016–2019 and chikungunya 2017–2020; classification labels are the dengue labels for every disease (Zika code 1 is shown as "Dengue classico" but is confirmed); SINAN serotype value 0 appears as `codigo_0` (134,407 in 2023).
- **Figure 7A/7B labels**: "ELISA" matches the NS1 antigen field and "IgM" the IgM serology field by yearly counts (e.g. 2016 positives 97,530 vs 97,528). Confirm.
- **Pooled lagged model**: none exists in the outputs, so the manuscript reports the per-FU lagged models. Add a `pooled = TRUE` lagged entry to `SPECS` in `pipelines/glm_common.R` if the authors want it reported.

## 8. Figure map

| Draft (old numbering) | Manuscript | Repository file |
|---|---|---|
| Fig 1A–B maps | Figure 6 | `figures/Figure6_combined_map.png` |
| Fig 1C annual maps | Supplementary Figure S1 | `FigureS1_2016–2026.png`, `FigureS1_overview.png` |
| Fig 1D LISA and trend maps | Supplementary Figure S2 | `FigureS2_lisa_trend.png` |
| Fig 2 incidence | Figure 1 | `Figure1_incidence_regional.png` |
| Fig 3 Moran scatter | Figure 4 | `Figure4_spatial_autocorrelation.png` |
| Fig 4 age and sex | Figure 5 | `Figure5_demographics.png` |
| Fig 5 dengue clinical | Figure 7 | `Figure7_dengue_clinical.png` |
| Fig 6 chikungunya and Zika clinical | Figure 8 | `Figure8_chikv_zika_clinical.png` |
| Fig 7 trends | Figure 2 | `Figure2_trend_analysis.png` |
| Fig 8 correlations | Figure 3 | `Figure3_climate_correlations.png` |
| S5 AIC | Supplementary Figure S6 | `glm_fig4_aic_comparison.png` |
| S6 pooled | Supplementary Figure S3 | `glm_fig1_pooled_climate_irr.png` |
| S7/S8 per-state | Supplementary Figures S4 and S7 | `glm_fig2_per_state_heatmap.png`, `glm_fig5_forest_significant.png` |
| S9 lag profile | Supplementary Figure S5 | `glm_fig3_lag_profile.png` |
| S1A–C state totals, S2A–C seasonal heatmaps | not cited | `outputs/*_05_federative_unit_totals.png`, `*_01b_monthly_heatmap.png` (end in 2025) |
| Table S11 | not cited | `outputs/glm_*_results.xlsx` |

## 9. Reference list

62 references converted from ASM to NLM/AMA style and renumbered by order of first citation (the Methods now precede the Results). New entries: Liu 2023, Moura 2020, Lim 2025, de Lima 2026, IBGE (projections; DOU estimates), INMET, Governo do Espírito Santo 2021. No DOIs were added except those already in the draft or given in `docs/LITERATURE_CONTEXT.md`; journal abbreviations are those of the draft. Rule used for authors: more than 6 → first 3 + et al (AMA); **unverified for JMV**.
