# Figure captions

Captions for the figures in `figures/`, written to be pasted into the manuscript. Generated on 2026-10-22 by
`docs/manuscript/build/gen_captions.py` from the regenerated outputs (`outputs/figure_caption_values.csv`,
`outputs/figure_exclusions_captions.txt`, `numbers.csv`): SINAN downloaded 2026-10-22, 2026 files = release of 2026-10-20,
notifications up to 2026-09-30, cases = every notification not classified as discarded. If the pipeline is rerun, regenerate
this file. The numbering of the supplementary figures (S1, S2, GLM Figures 1-5) is the repository's; the manuscript numbers
figures by order of citation (see `docs/manuscript/SYNC_LOG.md`).

Abbreviations used throughout: UF, federative unit (state); IRR, incidence rate ratio; CI, confidence
interval; FE, fixed effects; LISA, local indicator of spatial association.

---

## Main figures

**Figure 1. Annual and monthly incidence of dengue, chikungunya and Zika in Brazil, 2016–2026.**
(A) Annual incidence per 100,000 inhabitants for Brazil (solid line, population-weighted mean of
the 27 UFs) and for each macro-region (dashed lines). (B) Distribution of monthly incidence per
100,000 inhabitants across UF-months, by macro-region; boxes show the median and interquartile
range, whiskers 1.5 × IQR; the y axis, shared by the three panels, is cropped at 1.05 × the
largest 99th percentile of the three diseases. 2026 is a partial year (January–September): its annual values are annualized (×12/9) from the months reported, which overstates the year.

**Figure 2. Temporal trends in annual incidence by state, 2016–2026.**
(A) Mann-Kendall Kendall’s τ for each UF; coloured bars indicate p < 0.05 (dengue 2/27,
chikungunya 4/27, Zika 13/27 states). (B) Sen’s slope of annual incidence (cases per 100,000
per year) by UF and disease; bars of trends with p < 0.05 are coloured by disease, the others grey. The last annual value of the series is the
partial year 2026 (January–September), annualized (×12/9), which overstates it.

**Figure 3. Correlation between monthly incidence and climate.**
(A) Mean Spearman’s ρ across the 27 UFs between monthly incidence and mean temperature or rainfall
at lags of 0, 1 and 2 months; * marks combinations in which at least 50% of states had p < 0.05.
(B) Mean ρ by macro-region and lag for temperature and rainfall. Climate: INMET automatic
stations aggregated to UF-month.

**Figure 4. Spatial autocorrelation of mean annual incidence.**
Moran scatterplots of standardised population-weighted mean annual incidence (z) against its
spatial lag (Wz), with the fitted line, using row-standardised k-nearest-neighbour weights (k = 5).
Global Moran’s I (999 permutations): dengue 0.516 (p = 0.001), chikungunya 0.231 (p = 0.017), Zika −0.105 (p = 0.243). The mean annual incidence is the mean of the annual values of 2016–2026, whose last year
is the partial year 2026 (January–September), annualized (×12/9).

**Figure 5. Age and sex of cases, 2016–2026.**
Confirmed and probable cases (notifications classified as discarded excluded). (A) Distribution of patient age by year. Violins are reconstructed from age-band counts (ages
drawn uniformly within each band); inner lines mark the quartiles and the white dot the median;
n = cases with known age. (B) Percentage of male and female cases by year. Percentages and age distributions are calculated on records with a known value; records with ignored/blank values were excluded: A, Dengue age group: n = 28,887 of 16,802,619 (0.2%); A, Chikungunya age group: n = 110 of 1,599,784 (<0.1%); A, Zika age group: n = 0 of 295,639 (<0.1%); B, Dengue sex: n = 22,153 of 16,802,619 (0.1%); B, Chikungunya sex: n = 1,983 of 1,599,784 (0.1%); B, Zika sex: n = 387 of 295,639 (0.1%). 2026 covers January–September only (a partial year); percentages are not annualized.

**Figure 6. Mean annual incidence of dengue, chikungunya and Zika by state, 2016–2026.**
One symbol per UF and disease (circle, dengue; triangle, chikungunya; square, Zika), filled by
the natural-breaks (Jenks, k = 5) class of the population-weighted mean annual incidence, computed
separately for each disease. Class bounds (cases per 100,000; class 1 → 5): dengue 71–130, 130–397, 397–761, 761–1,212, 1,212–1,784; chikungunya 2–18, 18–62, 62–100, 100–156, 156–228; Zika 0–5, 5–15, 15–25, 25–43, 43–73.
Symbols for RN, PB, PE, AL, SE, ES and RJ are drawn offshore, with a leader line to the state. Global Moran’s I: dengue 0.516 (p = 0.001), chikungunya 0.231 (p = 0.017), Zika −0.105 (p = 0.243). The mean annual incidence includes the
partial year 2026 (January–September), annualized (×12/9), which overstates it.

**Figure 7. Laboratory testing, hospitalisation and serotype of dengue cases, 2016–2026.**
Dengue cases (notifications classified as discarded excluded). Percentage of records with a known value in each category by year: (A) NS1 antigen result, (B) IgM
result, (C) hospitalisation, (D) serotype; the number of records with a known value is shown
under each year. Percentages are calculated on records with a known value; records with ignored/blank values were excluded: A, Dengue NS1 antigen: n = 7,462,409 of 16,802,619 (44.4%); B, Dengue IgM: n = 7,996,515 of 16,802,619 (47.6%); C, Dengue hospitalization: n = 5,263,231 of 16,802,619 (31.3%); D, Dengue serotype: n = 16,432,924 of 16,802,619 (97.8%). Serotype percentages describe typed cases only (547–189,583 per year in 2016–2025). In 2025, 98% of the NS1 and
IgM records were ignored/blank. 2026 covers January–September only (a partial year); percentages are not annualized.

**Figure 8. Classification, confirmation criterion, outcome and pregnancy status of chikungunya
and Zika cases, 2016–2026.**
Confirmed and probable cases (notifications classified as discarded excluded). Percentage of records with a known value in each category by year, with the number of such
records under each year. (A) Chikungunya: final classification, confirmation
criterion and outcome. (B) Zika: final classification, confirmation criterion,
outcome and pregnancy status. “Under investigation or blank” is a probable case that has not been classified yet. Percentages are calculated on records with a known value; records with ignored/blank values were excluded: A, Chikungunya classification: n = 554 of 1,599,784 (<0.1%); A, Chikungunya criteria: n = 287,292 of 1,599,784 (18.0%); A, Chikungunya evolution: n = 409,684 of 1,599,784 (25.6%); B, Zika classification: n = 175 of 295,639 (<0.1%); B, Zika criteria: n = 115,246 of 295,639 (39.0%); B, Zika evolution: n = 125,208 of 295,639 (42.4%); B, Zika pregnancy: n = 43,090 of 295,639 (14.6%). 2026 covers January–September only (a partial year); percentages are not annualized.

---

## Supplementary figures

**Supplementary Figure S1. Annual incidence of dengue, chikungunya and Zika by state, 2016–2026
(one map per year).**
One symbol per UF and disease (circle, dengue; triangle, chikungunya; square, Zika), filled by
the natural-breaks (Jenks, k = 5) class of annual incidence, computed per disease over all
state-years so that each colour denotes the same incidence range in every year. Class bounds
(cases per 100,000; class 1 → 5): dengue 1–505, 505–1,363, 1,363–2,868, 2,868–5,477, 5,477–9,354; chikungunya 0–69, 69–235, 235–477, 477–782, 782–1,285; Zika 0–26, 26–76, 76–201, 201–432, 432–671. 2026 is a partial year (January–September): its annual values are annualized (×12/9) from the months reported, which overstates the year. No symbol is drawn for
Espirito Santo 2021 (Chikungunya); Espirito Santo 2021 (Zika): the national SINAN files contain no notification
for that state-year (see Limitations). Files: `FigureS1_2016.png` … `FigureS1_2026.png`;
`FigureS1_overview.png` shows all years.

**Supplementary Figure S2. Local spatial clusters and temporal trends by state.**
(A) LISA category of the population-weighted mean annual incidence (k-nearest-neighbour
weights, k = 5; 999 permutations; p < 0.05): HH and LL, high-high and low-low clusters; HL and
LH, spatial outliers; white, not significant (dengue HH 8 | LL 4 | HL 1 | LH 1 | NS 13; chikungunya HH 6 | LL 2 | HL 0 | LH 0 | NS 19; Zika HH 0 | LL 0 | HL 1 | LH 0 | NS 26). (B) Mann-Kendall trend of annual incidence, 2016–2026
(p < 0.05): increasing 2 | decreasing 0 | no trend 25 for dengue, increasing 3 | decreasing 1 | no trend 23 for chikungunya, increasing 0 | decreasing 13 | no trend 14 for Zika; white, no significant trend. Symbols as in Figure 6. The mean annual incidence and the trends include the
partial year 2026 (January–September), annualized (×12/9), which overstates it.

**GLM Figure 1. Climate effects from pooled models with state and month fixed effects.**
IRR per +1 °C of mean temperature and per +1 mm of rainfall, by disease and model family
(Poisson, quasi-Poisson, negative binomial), with 95% CI (cluster-robust standard errors for the
Poisson and negative binomial models); * p < 0.05.

**GLM Figure 2. Per-state climate effects (negative binomial models).**
IRR per +1 °C of mean temperature and per +1 mm of rainfall for each UF and disease, from
per-state negative binomial models with month fixed effects and HAC standard errors; colour =
log₂(IRR) (red, positive; blue, negative); * p < 0.05.

**GLM Figure 3. Lag profile of climate effects.**
Median IRR across states (line) and interquartile range (shaded) for temperature and rainfall at
lags of 0, 1 and 2 months, from per-state negative binomial models with lagged climate predictors
and month fixed effects; diamonds with bars are the IRR and 95% CI of each lag in the pooled negative binomial model with
state and month fixed effects, in which the lags are entered jointly.

**GLM Figure 4. Model fit comparison.**
Median AIC across states (log scale; lower is better) by model family and specification
(per-state, per-state lagged, pooled fixed effects, pooled fixed effects with lags). The negative binomial models fit the overdispersed
monthly counts far better than the Poisson models.

**GLM Figure 5. Statistically significant per-state climate effects.**
Forest plot of log₂(IRR) with 95% CI for the state–disease combinations with p < 0.05 in the
per-state negative binomial models, for temperature and rainfall (right of zero, positive
association; left, negative).

---

## Methods and limitations (text for the manuscript)

The Methods and limitations of the manuscript are in `Alves ER et al JMV 2026.docx` and are built from the repository outputs
(`docs/manuscript/`). Points specific to the figures:

- **Case definition.** For the three diseases a case is every notification not classified as discarded (confirmed and probable).
  The discarded notifications excluded are 3,002,212 (dengue), 846,972 (chikungunya) and 263,816 (Zika),
  of 19,804,831, 2,446,756 and 559,455 notifications.
- **Missing values.** In the clinical figures (5, 7, 8) percentages and distributions are calculated on records with a known value.
  Records coded as ignored or blank in SINAN were excluded from numerators and denominators, except the blank classification of chikungunya and Zika
  (a notification not yet classified, drawn as its own category). Recorded answers such as "not performed" or "inconclusive" were kept as
  categories. The number and percentage excluded for each figure and year are in `outputs/figure_exclusions.csv`.
- **2026.** 2026 covers January–September (notifications dated up to 2026-09-30) and its annual values are annualized (×12/9), which overstates
  the year because October–December carry 4.8% (dengue), 6.4% (chikungunya) and
  4.2% (Zika) of the cases of 2016–2025. It is kept in the trends, mean incidence, Moran’s I and LISA.
- **Missing state-years.** The national SINAN files contain no chikungunya or Zika notification for Espírito Santo in 2021 (Espirito Santo 2021 (Chikungunya); Espirito Santo 2021 (Zika)); that state-year is missing,
  not zero. A state-month without a case is a zero for every state with notifications in that year’s file.
- **Serotype.** Dengue serotype was recorded for 0.2–3.0% of the cases per year in 2016–2025
  and 7.1% in the partial year 2026. A SINAN serotype value of `0`, which is not a serotype, is labelled `codigo_0` in `clinical_tables/`
  and counted as not typed.
- **Supplementary Figure S1.** Classes are pooled over all years so that colours are comparable across years; years with low incidence therefore fall mostly in class 1.
