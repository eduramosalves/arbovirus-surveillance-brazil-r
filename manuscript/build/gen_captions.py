"""Write manuscript/FIGURE_CAPTIONS.md from the regenerated outputs (figure_caption_values.csv, figure_exclusions_captions.txt,
numbers.csv). Usage: python gen_captions.py <project root> <numbers.csv>"""
import csv
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
N = {r["key"]: r["value"] for r in csv.DictReader(open(sys.argv[2], encoding="utf-8"))}
cv = list(csv.DictReader(open(root / "outputs" / "figure_notes" / "figure_caption_values.csv", encoding="utf-8")))


def val(figure, item, panel=None, start=None):
    for r in cv:
        if r["Figure"] == figure and r["Item"].startswith(item) and (panel is None or r["Panel"] == panel):
            return r["Value"]
    raise KeyError((figure, item, panel))


def i(k):
    return "{:,.0f}".format(float(N[k]))


def exc(fig):
    for line in open(root / "outputs" / "figure_notes" / "figure_exclusions_captions.txt", encoding="utf-8"):
        if line.startswith(fig + "."):
            return line[len(fig) + 2:].strip()
    raise KeyError(fig)


moran = {p: val("Figure 4", "Global Moran", p).replace("-", "−") for p in ("Dengue", "Chikungunya", "Zika")}
moran_txt = "dengue %s, chikungunya %s, Zika %s" % tuple(moran[p].replace("(p =", "(p =") for p in ("Dengue", "Chikungunya", "Zika"))
sig = {p: val("Figure 2A", "Significant states", p) for p in ("Dengue", "Chikungunya", "Zika")}
b6 = {p: val("Figure 6", "Class bounds", p).replace("  |  ", ", ").replace(" | ", ", ") for p in ("Dengue", "Chikungunya", "Zika")}
b1 = {p: val("Figure S1", "Class bounds", p).replace("  |  ", ", ").replace(" | ", ", ") for p in ("Dengue", "Chikungunya", "Zika")}
lisa = {p: val("Figure S2A", "States per category", p) for p in ("Dengue", "Chikungunya", "Zika")}
trend = {p: val("Figure S2B", "States per category", p) for p in ("Dengue", "Chikungunya", "Zika")}
gaps = val("Figure S1", "No symbol")
typed = [float(N["ct.sero_typed.%d" % y]) for y in range(2016, 2026)]
P26 = ("2026 is a partial year (January–September): its annual values are annualized (×12/9) from the months reported, "
       "which overstates the year.")
P26c = "2026 covers January–September only (a partial year); percentages are not annualized."

text = f"""# Figure captions

Captions for the figures in `figures/` (`main/`, `supplementary/`, `glm/`), written to be pasted into the manuscript. Generated on 2026-10-22 by
`manuscript/build/gen_captions.py` from the regenerated outputs (`outputs/figure_notes/figure_caption_values.csv`,
`outputs/figure_notes/figure_exclusions_captions.txt`, `numbers.csv`): SINAN downloaded 2026-10-22, 2026 files = release of 2026-10-20,
notifications up to 2026-09-30, cases = every notification not classified as discarded. If the pipeline is rerun, regenerate
this file. The numbering of the supplementary figures (S1, S2, GLM Figures 1-5) is the repository's; the manuscript numbers
figures by order of citation (see `manuscript/SYNC_LOG.md`).

Abbreviations used throughout: UF, federative unit (state); IRR, incidence rate ratio; CI, confidence
interval; FE, fixed effects; LISA, local indicator of spatial association.

---

## Main figures

**Figure 1. Annual and monthly incidence of dengue, chikungunya and Zika in Brazil, 2016–2026.**
(A) Annual incidence per 100,000 inhabitants for Brazil (solid line, population-weighted mean of
the 27 UFs) and for each macro-region (dashed lines). (B) Distribution of monthly incidence per
100,000 inhabitants across UF-months, by macro-region; boxes show the median and interquartile
range, whiskers 1.5 × IQR; the y axis, shared by the three panels, is cropped at 1.05 × the
largest 99th percentile of the three diseases. {P26}

**Figure 2. Temporal trends in annual incidence by state, 2016–2026.**
(A) Mann-Kendall Kendall’s τ for each UF; coloured bars indicate p < 0.05 (dengue {sig['Dengue']},
chikungunya {sig['Chikungunya']}, Zika {sig['Zika']} states). (B) Sen’s slope of annual incidence (cases per 100,000
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
Global Moran’s I (999 permutations): {moran_txt}. The mean annual incidence is the mean of the annual values of 2016–2026, whose last year
is the partial year 2026 (January–September), annualized (×12/9).

**Figure 5. Age and sex of cases, 2016–2026.**
Confirmed and probable cases (notifications classified as discarded excluded). (A) Distribution of patient age by year. Violins are reconstructed from age-band counts (ages
drawn uniformly within each band); inner lines mark the quartiles and the white dot the median;
n = cases with known age. (B) Percentage of male and female cases by year. {exc('Figure 5')} {P26c}

**Figure 6. Mean annual incidence of dengue, chikungunya and Zika by state, 2016–2026.**
One symbol per UF and disease (circle, dengue; triangle, chikungunya; square, Zika), filled by
the natural-breaks (Jenks, k = 5) class of the population-weighted mean annual incidence, computed
separately for each disease. Class bounds (cases per 100,000; class 1 → 5): dengue {b6['Dengue']}; chikungunya {b6['Chikungunya']}; Zika {b6['Zika']}.
Symbols for RN, PB, PE, AL, SE, ES and RJ are drawn offshore, with a leader line to the state. Global Moran’s I: {moran_txt}. The mean annual incidence includes the
partial year 2026 (January–September), annualized (×12/9), which overstates it.

**Figure 7. Laboratory testing, hospitalisation and serotype of dengue cases, 2016–2026.**
Dengue cases (notifications classified as discarded excluded). Percentage of records with a known value in each category by year: (A) NS1 antigen result, (B) IgM
result, (C) hospitalisation, (D) serotype; the number of records with a known value is shown
under each year. {exc('Figure 7')} Serotype percentages describe typed cases only ({i('ct.sero_typed.2017')}–{max(typed):,.0f} per year in 2016–2025). In 2025, {float(N['fe.DENV.elisa.pct2025']):.0f}% of the NS1 and
IgM records were ignored/blank. {P26c}

**Figure 8. Classification, confirmation criterion, outcome and pregnancy status of chikungunya
and Zika cases, 2016–2026.**
Confirmed and probable cases (notifications classified as discarded excluded). Percentage of records with a known value in each category by year, with the number of such
records under each year. (A) Chikungunya: final classification, confirmation
criterion and outcome. (B) Zika: final classification, confirmation criterion,
outcome and pregnancy status. “Under investigation or blank” is a probable case that has not been classified yet. {exc('Figure 8')} {P26c}

---

## Supplementary figures

**Supplementary Figure S1. Annual incidence of dengue, chikungunya and Zika by state, 2016–2026
(one map per year).**
One symbol per UF and disease (circle, dengue; triangle, chikungunya; square, Zika), filled by
the natural-breaks (Jenks, k = 5) class of annual incidence, computed per disease over all
state-years so that each colour denotes the same incidence range in every year. Class bounds
(cases per 100,000; class 1 → 5): dengue {b1['Dengue']}; chikungunya {b1['Chikungunya']}; Zika {b1['Zika']}. {P26} No symbol is drawn for
{gaps}: the national SINAN files contain no notification
for that state-year (see Limitations). Files: `FigureS1_2016.png` … `FigureS1_2026.png`;
`FigureS1_overview.png` shows all years.

**Supplementary Figure S2. Local spatial clusters and temporal trends by state.**
(A) LISA category of the population-weighted mean annual incidence (k-nearest-neighbour
weights, k = 5; 999 permutations; p < 0.05): HH and LL, high-high and low-low clusters; HL and
LH, spatial outliers; white, not significant (dengue {lisa['Dengue']}; chikungunya {lisa['Chikungunya']}; Zika {lisa['Zika']}). (B) Mann-Kendall trend of annual incidence, 2016–2026
(p < 0.05): {trend['Dengue']} for dengue, {trend['Chikungunya']} for chikungunya, {trend['Zika']} for Zika; white, no significant trend. Symbols as in Figure 6. The mean annual incidence and the trends include the
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
(`manuscript/`). Points specific to the figures:

- **Case definition.** For the three diseases a case is every notification not classified as discarded (confirmed and probable).
  The discarded notifications excluded are {i('disc.DENV.disc')} (dengue), {i('disc.CHIKV.disc')} (chikungunya) and {i('disc.ZIKV.disc')} (Zika),
  of {i('disc.DENV.notif')}, {i('disc.CHIKV.notif')} and {i('disc.ZIKV.notif')} notifications.
- **Missing values.** In the clinical figures (5, 7, 8) percentages and distributions are calculated on records with a known value.
  Records coded as ignored or blank in SINAN were excluded from numerators and denominators, except the blank classification of chikungunya and Zika
  (a notification not yet classified, drawn as its own category). Recorded answers such as "not performed" or "inconclusive" were kept as
  categories. The number and percentage excluded for each figure and year are in `outputs/figure_notes/figure_exclusions.csv`.
- **2026.** 2026 covers January–September (notifications dated up to 2026-09-30) and its annual values are annualized (×12/9), which overstates
  the year because October–December carry {float(N['seas.DENV.q4_share'])*100:.1f}% (dengue), {float(N['seas.CHIKV.q4_share'])*100:.1f}% (chikungunya) and
  {float(N['seas.ZIKV.q4_share'])*100:.1f}% (Zika) of the cases of 2016–2025. It is kept in the trends, mean incidence, Moran’s I and LISA.
- **Missing state-years.** The national SINAN files contain no chikungunya or Zika notification for Espírito Santo in 2021 ({gaps}); that state-year is missing,
  not zero. A state-month without a case is a zero for every state with notifications in that year’s file.
- **Serotype.** Dengue serotype was recorded for {float(N['ct.sero_typed_pct_min'])*100:.1f}–{float(N['ct.sero_typed_pct_max'])*100:.1f}% of the cases per year in 2016–2025
  and {float(N['ct.sero_typed_pct.2026'])*100:.1f}% in the partial year 2026. A SINAN serotype value of `0`, which is not a serotype, is labelled `codigo_0` in `clinical_tables/`
  and counted as not typed.
- **Supplementary Figure S1.** Classes are pooled over all years so that colours are comparable across years; years with low incidence therefore fall mostly in class 1.
"""
(root / "manuscript" / "FIGURE_CAPTIONS.md").write_text(text, encoding="utf-8")
print("written", len(text), "characters")
