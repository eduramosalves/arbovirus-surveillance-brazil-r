"""Generate manuscript/{SYNC_LOG,JMV_CHECKLIST,RECORD_CHECKLIST}.md (round 2, 2026-10-22).
Usage: python gen_logs.py <outdir> <destdir>"""
import csv
import json
import re
import struct
import sys
from pathlib import Path

WORK = Path(__file__).parent
out = Path(sys.argv[1])
dest = Path(sys.argv[2])
dest.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(WORK))
from msbase import ORIG  # noqa: E402

rep = json.load(open(out / "build_report.json", encoding="utf-8"))
calc = rep["calc"]
N = {r["key"]: r["value"] for r in csv.DictReader(open(WORK / "numbers.csv", encoding="utf-8"))}
PROJECT = WORK.parents[1]   # repository root (this file is manuscript/build/gen_logs.py)
MAIN_WORDS = "{:,}".format(calc["main_words"])
M = "\u2212"


def f(key, spec="d1"):
    v = float(N[key])
    if spec == "i":
        return "{:,.0f}".format(v)
    if spec.startswith("d"):
        return "{:,.{}f}".format(v, int(spec[1:])).replace("-", M)
    if spec == "pct1":
        return "{:.1f}%".format(v * 100)
    if spec == "pct0":
        return "{:.0f}%".format(v * 100)
    return N[key]


def uf(key):
    return N[key]


# =============================================================== SYNC_LOG
L = []
A = L.append
A("# Manuscript sync log: draft (2016\u20132025, Python) \u2192 round 1 (2016\u20132026, R) \u2192 round 2 (case definition, 2026 cap, figure order)")
A("")
A("Round 1 written 2026-10-21; **round 2 written 2026-10-22**, after the eight instructions tagged \"@claude for ERA\" in `Alves ER et al JMV 2026.docx`. "
  "Covers `Alves ER et al JMV 2026.docx` (clean) and `Alves ER et al JMV 2026 (redline).docx` (every text change tracked against the draft, author *Claude for ERA*), "
  "both built from `Alves ER et al JVI 2026.docx`, which was not modified. The file as edited by the authors before round 2 is kept in "
  "`manuscript/history/`.")
A("")
A("**How the numbers were produced.** Every number in the Abstract, Results, Discussion and Methods was computed from the repository files "
  "by `build/numbers.R` (R 4.6.1) into `numbers.csv`, and inserted into the text by key. The table in section 3 lists each inserted number "
  "with its source file. Legends are the text of `manuscript/FIGURE_CAPTIONS.md`. Statements the prose makes about the data (who trends, which model "
  "peaks at which lag, \"nearly half were discarded\") are checked at build time against `numbers.csv` (%d assertions), so the text cannot drift from the data. "
  "A second, independent computation in Python (section 6) reproduced 43 headline values from the raw tables." % calc.get("n_asserts", 34))
A("")
A("## 0. Round 2: what each instruction changed")
A("")
A("| Comment (author) | Instruction | What was done |")
A("|---|---|---|")
for r in [
    ("48 (ERA)", "\"need you to run this again\" (Moran's I)",
     "Whole pipeline rerun on the new case definition and data (ETL, 9 of 9 stages, source data). Moran's I: dengue %s (p %s), chikungunya %s (p %s; now significant), Zika %s (p %s)." % (
         f("moran.DENV.I", "d3"), f("moran.DENV.p", "d3"), f("moran.CHIKV.I", "d3"), f("moran.CHIKV.p", "d3"), f("moran.ZIKV.I", "d3"), f("moran.ZIKV.p", "d3"))),
    ("49, 50 (ERA)", "\"count total cases as the probables + confirmed, and exclude the discarded\"",
     "For all three diseases a case is any notification not classified as discarded (dengue code 5; chikungunya 5 and, in the early-2016 form, 2; Zika 2). "
     "Discarded and excluded: dengue %s of %s (%s; none from 2022 on), chikungunya %s of %s (%s), Zika %s of %s (%s). Counts per disease and year: `clinical_tables/discarded_counts.csv`." % (
         f("disc.DENV.disc", "i"), f("disc.DENV.notif", "i"), f("disc.DENV.share", "pct1"), f("disc.CHIKV.disc", "i"), f("disc.CHIKV.notif", "i"), f("disc.CHIKV.share", "pct1"),
         f("disc.ZIKV.disc", "i"), f("disc.ZIKV.notif", "i"), f("disc.ZIKV.share", "pct1"))),
    ("51 (ERA)", "\"keep 2026 on the analyses, but ALWAYS make it clear that this year has its limitations\"",
     "2026 kept. SINAN downloaded again on %s; the 2026 files (release of %s) were cut at notifications dated up to 2026-09-30, so 2026 is January\u2013September, annualized \u00d712/9. "
     "Every paragraph or legend that uses 2026 says so (a build check fails otherwise). Q4 holds %s / %s of dengue / Zika cases (2016\u20132025), so the annualized year is overstated." % (
         N["meta.sinan_access"].strip('"'), N["meta.sinan_release"].strip('"'), f("seas.DENV.q4_share", "pct1"), f("seas.ZIKV.q4_share", "pct1"))),
    ("52 (ERA)", "\"renumber and reorder everything having in mind the order that the images are cited\"",
     "Figures numbered by first citation (main 1\u20138, supplementary S1\u2013S7); legends reordered; cross-references inside legends renumbered; figure citations removed from Methods; the annual maps, never cited before, are now cited. "
     "Copies under the new numbers: `manuscript/figures/`; table in section 8."),
    ("53 (ERA)", "\"follow all the comments from Galileu\"",
     "Replies posted in each thread (threads left open for Galileu). Figure style (his comment 6): one colour per virus defined once in `R/utils.R` (dengue red, chikungunya green, Zika blue); "
     "grey bars for non-significant Sen's slopes (only significant trends carry colour); figures have no in-plot titles; keys sit next to the data."),
    ("54 (ERA)", "\"what should we do now?\" (lag model)",
     "You chose to add a pooled lagged model (FU and month fixed effects, lags 0\u20132 jointly, FU-clustered SE; `outputs/regression/glm_*_pooled_lagged.csv`). Results report the IRR per lag and the IRR of a change sustained over lags 0\u20132; the per-FU lagged models stay."),
    ("55 (ERA)", "\"you can delete it if it doesn't break the logic\" (DLNM)",
     "DLNM deleted from Methods, Results, Discussion and the author query (the logic holds); the analysis files stay in `outputs/`. A build check fails if \"DLNM\" reappears."),
    ("(not a comment)", "Figures 5, 7, 8 (your choice)",
     "Rebuilt from `clinical_tables/clinical_demographic_long.csv` (2016\u20132026, discarded excluded) instead of the GraphPad tables; NS1 panel relabelled; age bands and classification labels corrected in the ETL."),
]:
    A("| " + " | ".join(r) + " |")
A("")
A("## 1. Headline changes in the claims")
A("")
A("Draft = `Alves ER et al JVI 2026.docx` (Python, 2016\u20132025). Round 1 = manuscript of 2026-10-21 (R, 2016\u20132026, chikungunya and Zika with discarded notifications, 2026 up to the 2026-10-06 release). "
  "Round 2 = this manuscript. Items marked **\u21c4** change the interpretation and need the co-authors' attention.")
A("")
A("| | Draft | Round 1 | Round 2 | Source |")
A("|---|---|---|---|---|")
rows = [
    ("Cases 2016\u20132026 (dengue / chikungunya / Zika)", "\u2014", "\u2014",
     "%s / %s / %s" % (f("disc.DENV.cases", "i"), f("disc.CHIKV.cases", "i"), f("disc.ZIKV.cases", "i")), "`db/normalized_fact_cases.csv`"),
    ("Moran's I, dengue / chikungunya / Zika", "0.562 (p = 0.001) / \u22120.036 (0.460) / \u22120.008 (0.352)", "0.516 / 0.004 / \u22120.006 (p 0.001 / 0.285 / 0.326)",
     "%s / %s / %s (p %s / %s / %s)" % (f("moran.DENV.I", "d3"), f("moran.CHIKV.I", "d3"), f("moran.ZIKV.I", "d3"), f("moran.DENV.p", "d3"), f("moran.CHIKV.p", "d3"), f("moran.ZIKV.p", "d3")),
     "`outputs/spatial/geo_spatial_stats.xlsx`, Global_Moran"),
    ("Mean annual incidence, dengue top 3", "DF 1,825.6; GO 1,742.7; MG 1,647.7", "GO 1,782.4; DF 1,693.7; MG 1,538.7",
     "%s %s; %s %s; %s %s" % tuple(x for k in (1, 2, 3) for x in (uf("rank_minc.DENV.%d" % k), f("rank_minc_val.DENV.%d" % k))), "`geo_spatial_stats.xlsx`, Mean_Incidence"),
    ("Chikungunya top mean incidence", "MS 421.8", "MS 498.4; CE 324.9; MT 294.5",
     "%s %s; %s %s; %s %s" % tuple(x for k in (1, 2, 3) for x in (uf("rank_minc.CHIKV.%d" % k), f("rank_minc_val.CHIKV.%d" % k))), "same"),
    ("Zika top mean incidence", "TO 145.7; MT 106.7", "TO 136.9; MT 98.4",
     "%s %s; %s %s; %s %s" % tuple(x for k in (1, 2, 3) for x in (uf("rank_minc.ZIKV.%d" % k), f("rank_minc_val.ZIKV.%d" % k))), "same"),
    ("\u21c4 Dengue increasing trends", "RS, SC, SP", "RS (\u03c4 0.600), SC (\u03c4 0.491); SP not significant (p = 0.161)",
     "RS (\u03c4 %s), SC (\u03c4 %s); SP not significant" % (f("mk.DENV.RS.tau", "d3"), f("mk.DENV.SC.tau", "d3")), "`py_statistical_results.xlsx`, Mann_Kendall"),
    ("\u21c4 Chikungunya increasing trends", "SC, RS, MS", "MS, MG, GO; SC (p = 0.119) and RS (p = 0.161) not significant",
     "MS (\u03c4 %s), GO (%s), MG (%s); CE decreasing" % (f("mk.CHIKV.MS.tau", "d3"), f("mk.CHIKV.GO.tau", "d3"), f("mk.CHIKV.MG.tau", "d3")), "same"),
    ("\u21c4 Zika decreasing trends", "AL, PI, DF (3 states)", "6 states (DF, PI, MG, RJ, AL, PR)", "%s states, none increasing" % f("mk_n.ZIKV.decreasing", "i"), "same"),
    ("\u21c4 Multiple testing", "\"no adjustment\"", "BH q-values reported; no trend survives (minimum q: dengue 0.344, chikungunya 0.137, Zika 0.110)",
     "BH q-values reported; minimum q: dengue %s, chikungunya %s (MS), Zika %s (%s states remain significant)" % (f("mk_minq.DENV", "d3"), f("mk_minq.CHIKV", "d3"), f("mk_minq.ZIKV", "d3"), f("mkfdr_n.ZIKV.decreasing", "i")), "Mann_Kendall, q_value"),
    ("Dengue LISA high\u2013high, after BH", "Central-West and Southeast", "also Paran\u00e1; after BH only GO, MG (HH) and RJ (LH)",
     "also Paran\u00e1; after BH only %s (HH) and %s (LH)" % (N["lisafdr_names.DENV.HH"], N["lisafdr_names.DENV.LH"]), "`geo_spatial_stats.xlsx`, LISA_Clusters"),
    ("Zika 2016 vs later years", "\"roughly 8\u201310 times\"", "6.8\u201314.9 times (complete years 2017\u20132025)",
     "%s\u2013%s times (complete years 2017\u20132025)" % (f("zika_ratio_min"), f("zika_ratio_max")), "`source_data/Figure1.xlsx`"),
    ("\u21c4 Pooled temperature IRR, dengue", "2.10 (1.96\u20132.26)", "1.10 (1.02\u20131.19)",
     "%s (%s\u2013%s)" % (f("glmp.DENV.Temp_Avg.irr", "d2"), f("glmp.DENV.Temp_Avg.lo", "d2"), f("glmp.DENV.Temp_Avg.hi", "d2")), "`outputs/regression/glm_negbin_pooled_fe.csv`"),
    ("\u21c4 Pooled temperature IRR, chikungunya", "1.32 (1.24\u20131.41), significant", "1.05 (0.99\u20131.12), **not significant**",
     "%s (%s\u2013%s), **not significant**" % (f("glmp.CHIKV.Temp_Avg.irr", "d2"), f("glmp.CHIKV.Temp_Avg.lo", "d2"), f("glmp.CHIKV.Temp_Avg.hi", "d2")), "same"),
    ("\u21c4 Pooled temperature IRR, Zika", "0.90 (0.84\u20130.97), inverse", "1.09 (1.01\u20131.18), **positive**",
     "%s (%s\u2013%s), **positive** (p %s)" % (f("glmp.ZIKV.Temp_Avg.irr", "d2"), f("glmp.ZIKV.Temp_Avg.lo", "d2"), f("glmp.ZIKV.Temp_Avg.hi", "d2"), f("glmp.ZIKV.Temp_Avg.p", "d3")), "same"),
    ("\u21c4 Rainfall", "IRR 1.007 per mm; Spearman \u03c1 \u2248 0", "IRR per 100 mm 1.30 / 1.18 / 1.16; mean \u03c1 at lag 2 0.433 / 0.355 / 0.347",
     "IRR per 100 mm %s / %s / %s; mean \u03c1 at lag 2 %s / %s / %s" % (f("glmp.DENV.Rain_mm.irr100", "d2"), f("glmp.CHIKV.Rain_mm.irr100", "d2"), f("glmp.ZIKV.Rain_mm.irr100", "d2"), f("sp.DENV.Rain.2.mean", "d3"), f("sp.CHIKV.Rain.2.mean", "d3"), f("sp.ZIKV.Rain.2.mean", "d3")), "glm CSVs; `Spearman_Lag`"),
    ("Temperature Spearman \u03c1 (national mean, dengue)", "0.16 \u2192 0.19, \"positive at all lags\"", "\u22120.147 / \u22120.018 / 0.137 at lags 0 / 1 / 2",
     "%s / %s / %s at lags 0 / 1 / 2" % (f("sp.DENV.Temp.0.mean", "d3"), f("sp.DENV.Temp.1.mean", "d3"), f("sp.DENV.Temp.2.mean", "d3")), "`Spearman_Lag`"),
    ("NB2 dispersion \u03b1 (pooled)", "1.69 / 1.45 / 1.55", "1.23 / 1.20 / 1.21",
     "%s / %s / %s" % (f("glmp.DENV.alpha", "d2"), f("glmp.CHIKV.alpha", "d2"), f("glmp.ZIKV.alpha", "d2")), "pooled CSV"),
    ("Per-FU temperature, significant FU", "16 / 12 / 10", "14 / 9 / 7",
     "%s / %s / %s" % (f("glms.DENV.Temp_Avg.nsig", "i"), f("glms.CHIKV.Temp_Avg.nsig", "i"), f("glms.ZIKV.Temp_Avg.nsig", "i")), "`glm_negbin_per_state.csv`"),
    ("Per-FU lagged models, lag-2 temperature, significant FU", "11 / 4 / 7", "11 / 7 / 8",
     "%s / %s / %s" % (f("glml.DENV.Temp_Lag2.nsig", "i"), f("glml.CHIKV.Temp_Lag2.nsig", "i"), f("glml.ZIKV.Temp_Lag2.nsig", "i")), "`glm_negbin_lagged.csv`"),
    ("**New** pooled lagged model, temperature IRR per \u00b0C", "\u2014", "\u2014",
     "dengue lag 2 %s, sustained 0\u20132 %s; chikungunya lag 2 borderline (p %s); Zika peaks at lag 1 (%s)" % (
         f("glmpl.DENV.Temp_Lag2.irr", "d2"), f("glmpl.DENV.Temp_Cum0_2.irr", "d2"), f("glmpl.CHIKV.Temp_Lag2.p", "d3"), f("glmpl.ZIKV.Temp_Lag1.irr", "d2")), "`outputs/regression/glm_negbin_pooled_lagged.csv`"),
    ("Hospitalization (comment 13)", "15,788,792 not hospitalized; 529,203 hospitalized", "529,203 hospitalized; 10,642,808 not; 5,145,984 ignored/blank (sum 16,317,995)",
     "%s hospitalized; %s not; %s ignored/blank (sum %s)" % (f("cl.DENV.hosp.Positive", "i"), f("cl.DENV.hosp.Negative", "i"), f("cl.DENV.hosp.IgnBlank", "i"), f("cl.DENV.hosp.total", "i")), "`source_data/Figure7.xlsx`"),
    ("Placeholders", "[X], xxxxx, [REF IBGE??]", "chikungunya men 800,258; DENV-2 117,958; DENV-3 8,766; DENV-4 747",
     "chikungunya men %s; DENV-2 %s; DENV-3 %s; DENV-4 %s" % (f("cl.CHIKV.sex.M", "i"), f("cl.DENV.sero.DENV2", "i"), f("cl.DENV.sero.DENV3", "i"), f("cl.DENV.sero.DENV4", "i")), "Figure 5/7 source data"),
    ("Chikungunya peak year", "(comment 9)", "2024 (200.5 per 100,000), second 2016 (155.3)",
     "2024 (%s per 100,000), second 2016 (%s); highest regional value: %s %s (%s)" % (f("ann.CHIKV.BR.2024"), f("ann.CHIKV.BR.2016"), N["chik_regmax_region"], N["chik_regmax_year"], f("chik_regmax_val")), "`Figure1.xlsx`"),
]
for r in rows:
    A("| " + " | ".join(r) + " |")
A("")
A("## 2. Methods statements rewritten to what the code does")
A("")
A("| Draft statement | Manuscript statement | Evidence in the repository |")
A("|---|---|---|")
for r in [
    ("Analyses in Python 3.12 (pandas, statsmodels, GeoPandas\u2026)", "R 4.6.1; data.table, readxl, sf, spdep, classInt, ggplot2, patchwork", "`docs/R_SESSION_INFO.txt`; `docs/R_PORT_NOTES.md`"),
    ("Temperature from CPC/NCEP grid; rainfall from INMET and CPTEC/INPE", "INMET hourly automatic stations, \u2265240 (temperature) / \u2265360 (rainfall) valid hourly readings per station-month, unweighted mean per FU", "`etl/build_climate.R`"),
    ("Spatial weights: Queen contiguity with kNN fallback", "Row-standardized kNN (k = 5) on polygon centroids only", "`pipelines/data_loader.R`; `R/stats.R`"),
    ("\"No adjustment for multiple comparisons\"", "Raw p reported with Benjamini\u2013Hochberg q-values", "`R/utils.R` (`p.adjust(method = \"BH\")`); `Significant_FDR` columns"),
    ("Pooled distributed-lag model (comment 16)", "Four specifications: pooled, per-FU, per-FU lagged (unconstrained), and **pooled lagged** (new, round 2); no DLNM in the manuscript", "`pipelines/glm_common.R` `SPECS`; `FORMULA_LAGGED_FE`"),
    ("\"Overdispersion assessed by testing \u03b1 > 0\" (comment 22)", "Pearson dispersion of the Poisson fit and ML \u03b1; no formal test", "`glm_common.R`; no `lrtest` anywhere"),
    ("State fixed effects only; model-based SE", "Pooled: FU + calendar-month FE, FU-clustered SE; per-FU and per-FU lagged: month FE, Newey\u2013West (3 lags)", "`glm_common.R`"),
    ("Discarded and under-investigation cases excluded; FU of residence", "**All three diseases**: every notification not classified as discarded (confirmed + probable, inconclusive and under investigation kept); FU/month of notification", "`etl/build_cases_clinical.R` (`DISCARD`, `MAP_CLASSI_BY`); `README.md`"),
    ("Population: 2022 Census and intercensal estimates [REF]", "IBGE projections (2024 revision) 2016\u20132023; DOU 1-July estimates 2024\u20132026", "`etl/build_population.R`; `docs/DATA_SOURCES.md`"),
    ("Study period to December 31, 2025", "To September 30, 2026 (SINAN download of 2026-10-22; 2026 annualized \u00d712/9)", "`etl/build_cases_clinical.R` (`CAP_YEAR`, `LAST_NOTIFICATION_DATE`); `pipelines/data_loader.R`"),
    ("(not stated)", "State-months without a notification are zeros inside the observed span of a state-year; a state-year with no notification at all (Espirito Santo 2021, chikungunya and Zika) is missing, not zero", "`etl/build_cases_clinical.R` (zero-fill); `outputs/figure_notes/figure_exclusions_state_years.csv`"),
]:
    A("| " + " | ".join(r) + " |")
A("")
A("## 3. Every number inserted into the text, with its source")
A("")
A("`key` is the entry in `build/numbers.csv`. Formats: `i` integer, `dN` N decimals, `pct` percent, `pv` p-value, `s` text, `ord`/`words` spelled.")
A("")
A("| Key | Format | Text | Source |")
A("|---|---|---|---|")
for u in rep["used"]:
    A("| `%s` | %s | %s | %s |" % (u["key"], u["fmt"] or "", str(u["text"]).replace("|", "/")[:110], ("`%s`" % u["src"]) if u["src"] else ""))
A("")
A("## 4. Values taken verbatim from other repository documents")
A("")
A("- Figure legends: `manuscript/FIGURE_CAPTIONS.md` (generated by `build/gen_captions.py` from `outputs/figure_notes/figure_caption_values.csv`, `figure_exclusions*.csv`). Renumbered by order of citation; "
  "\"UF\" becomes \"FU\"; American spelling; legends of S4 and S5 note that rainfall is drawn per 1 mm while the text uses 100 mm.")
A("- Literature thresholds (Liu 2023: 14.8 \u00b0C minimum, 32\u201333 \u00b0C optimum maximum; Lim 2025; Moura 2020 at abstract level; de Lima 2026: DENV-3 detection in Cear\u00e1 in July 2025): `docs/LITERATURE_CONTEXT.md` (its numbers predate round 2 and are not used).")
A("- Not verified against the original source: the Espirito Santo 2021 counts (2,901 chikungunya, 872 Zika) quoted in the old caption file; the cited page could not be read, so the numbers are left out of the manuscript (author query attached, still open).")
A("")
A("## 5. Derived values (not in any output file)")
A("")
A("- Rainfall IRR per 10 and per 100 mm = exp(k \u00d7 Coef) and exp(k \u00d7 (Coef \u00b1 c \u00d7 SE)) from `glm_negbin_pooled_fe.csv`, with c = 1.96 (the critical value implied by the exported CI). 100 mm \u2248 1 SD of monthly rainfall (%s mm)." % f("clim.rain_sd", "d0"))
A("- Pooled lagged model: the IRR of a change sustained over lags 0\u20132 is exp(sum of the three lag coefficients) with the variance taken from the FU-clustered covariance matrix (columns `Temp_Cum0_2`, `Rain_Cum0_2` of the pooled lagged CSV).")
A("- Seasonal totals: sums of `db/normalized_fact_cases.csv` by calendar month over 2016\u20132025 (complete years). Ratios of Zika 2016 incidence to later years from `Figure1.xlsx`.")
A("- Hospitalization, serotype and discard shares: ratios of the counts in `source_data/Figure5/7/8.xlsx` and `clinical_tables/discarded_counts.csv`.")
A("")
A("## 6. Independent verification")
A("")
A("`build/recompute.py` recomputes, from `db/` and the source tables and without using `numbers.csv` or the R outputs, and looks for the result in the manuscript text: "
  "case totals, 2024 dengue and 2016 Zika, state totals, national incidence, population-weighted mean incidence (GO, DF, MT, CE, RJ), "
  "Mann\u2013Kendall \u03c4 and Sen's slope (dengue RS, chikungunya MS), Spearman \u03c1 (dengue MG, RJ; national means of dengue and chikungunya temperature, Zika), global Moran's I for the three diseases from polygon centroids, "
  "the pooled Poisson and NB2 temperature IRRs and the rainfall IRR per 100 mm by refitting the model by IRLS, the hospitalization and serotype counts, chikungunya men, "
  "and the pooled January and May totals. **Result: 43 of 43 matched.** The stored monthly incidence in `db/` is rounded to 2 decimals; the independent Spearman uses the same rounding "
  "(without it the dengue MG value differs in the third decimal, 0.608 instead of 0.607).")
A("")
A("## 7. Data-quality findings and open points")
A("")
for t in [
    "**Discarded notifications: handled.** All three diseases now exclude them (section 0). Judgement to confirm: the early-2016 chikungunya form codes confirmed / discarded as 1 / 2 (like the Zika form), the later form as 13 / 5. On the 2016 file codes 1 and 2 follow the same January–April pattern and the same 2.2 : 1 ratio as 13 and 5, and code 2 has almost no deaths from the disease (4 of 28,500, against 0 for code 5), while code 1 behaves as confirmed; so codes 2 and 5 are treated as discarded for chikungunya. Please confirm with the BMoH data dictionary.",
    "**Annualized 2026.** \u00d712/9 overstates 2026 because October\u2013December hold %s / %s / %s of the cases (dengue / chikungunya / Zika, 2016\u20132025). 2026 enters the trends, mean incidence, Moran's I and LISA, with the qualifier required by comment 51. No sensitivity analysis without 2026 was run (not requested)." % (f("seas.DENV.q4_share", "pct1"), f("seas.CHIKV.q4_share", "pct1"), f("seas.ZIKV.q4_share", "pct1")),
    "**Zero months.** Excluding discarded notifications leaves many state-months without cases; they are zeros inside the observed span (otherwise annualization and the models would use only the months with cases). Espirito Santo 2021 (chikungunya and Zika) has no notification at all in the national files and stays missing; the national totals of those two diseases are therefore slightly low for 2021. Source of the gap unverified.",
    "**Clinical tables.** Figures 5, 7, 8 now come from `clinical_tables/clinical_demographic_long.csv`. Fixes in the ETL: age parsing (the 2016–2020 files store age as a float string such as \"4003.0\", so every age of those files was read as unknown), SINAN age bands, disease-specific classification labels with an `Unclassified` (not yet classified) category. The old GraphPad tables (`_unused/reference/graphpad_data`) are kept for comparison only.",
    "**Serotype value 0** (not a valid serotype; 134,407 records in 2023) is folded into Ign/Blank in Figure 7D. The author query remains open; Methods do not yet describe it.",
    "**Figure 7A/7B labels**: the panel previously called \"ELISA\" is the NS1 antigen result (SINAN field RESUL_NS1, matched by yearly counts); 7B is the IgM serology. Now labelled so. Please confirm.",
    "**Zika lag**: the pooled lagged model peaks at lag 1 while the per-FU lagged models have most significant FU at lag 2 (the text says both).",
    "**Espirito Santo counts** (2,901 chikungunya and 872 Zika, January\u2013October 2021) are still unverified.",
]:
    A("- " + t)
A("")
A("## 8. Figure map (numbers by order of first citation)")
A("")
A("| Manuscript | Draft (old numbering) | Repository files | Copy in `manuscript/figures/` |")
A("|---|---|---|---|")
DRAFT = {"Figure 6": "Fig 1A\u2013B maps", "Supplementary Figure S1": "Fig 1C annual maps", "Supplementary Figure S2": "Fig 1D LISA and trend maps",
         "Figure 1": "Fig 2 incidence", "Figure 4": "Fig 3 Moran scatter", "Figure 5": "Fig 4 age and sex", "Figure 7": "Fig 5 dengue clinical",
         "Figure 8": "Fig 6 chikungunya and Zika clinical", "Figure 2": "Fig 7 trends", "Figure 3": "Fig 8 correlations", "GLM Figure 4": "S5 AIC",
         "GLM Figure 1": "S6 pooled", "GLM Figure 2": "S7/S8 per-state", "GLM Figure 5": "S7/S8 per-state", "GLM Figure 3": "S9 lag profile"}
for fg in rep["figures"]:
    num = fg["number"]
    label = ("Supplementary Figure " + num) if num.startswith("S") else ("Figure " + num)
    files = fg["files"]
    copies = ["Figure%s.png" % num] if len(files) == 1 else ["Figure%s_%s.png" % (num, Path(x).stem.split("_", 1)[1]) for x in files]
    A("| %s | %s | %s | %s |" % (label, DRAFT.get(fg["repo_label"], "(new)"), ", ".join("`%s`" % x for x in files), ", ".join("`%s`" % x for x in copies)))
A("| not cited | S1A\u2013C state totals, S2A\u2013C seasonal heatmaps, Table S11 | `outputs/clinical/*_05_federative_unit_totals.png`, `outputs/clinical/*_01b_monthly_heatmap.png`, `outputs/regression/glm_*_results.xlsx` | |")
A("")
A("## 9. Reference list")
A("")
A("%d references: the 62 of the draft, converted from ASM to NLM/AMA style and renumbered by order of first citation (the Methods precede the Results), plus new entries (Liu 2023, Moura 2020, Lim 2025, de Lima 2026, IBGE projections and DOU estimates, INMET, Governo do Esp\u00edrito Santo 2021). "
  "No DOIs were added except those already in the draft or given in `docs/LITERATURE_CONTEXT.md`; journal abbreviations are those of the draft. "
  "Rule used for authors: more than 6 \u2192 first 3 + et al (AMA); **unverified for JMV**." % calc["n_refs"])
(dest / "SYNC_LOG.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# =============================================================== JMV_CHECKLIST
def png_info(p):
    d = open(p, "rb").read(200000)
    w, h = struct.unpack(">II", d[16:24])
    dpi = None
    i = d.find(b"pHYs")
    if i > 0:
        px, py, u = struct.unpack(">IIB", d[i + 4:i + 13])
        dpi = round(px * 0.0254) if u == 1 else None
    return w, h, dpi


imp = re.sub(r"\{/?c\d+\}", "", ORIG[24])
C = []
B = C.append
B("# JMV compliance checklist, open decisions, and removed text")
B("")
B("Round 1 written 2026-10-21, **updated 2026-10-22 (round 2)** for `Alves ER et al JMV 2026.docx`.")
B("")
B("**Status of the rules.** Wiley's author-guideline pages returned HTTP 403 to every automated request, and the search snippets that could be read disagree with each other. "
  "Every rule below marked **UNVERIFIED** was applied from common JMV/Wiley practice and the snippets, and must be checked on the live page "
  "(Journal of Medical Virology \u2192 Author Guidelines, https://onlinelibrary.wiley.com/page/journal/10969071/homepage/forauthors.html) before submission. "
  "The draft file name says \"JVI\"; its layout was that of ASM's *Journal of Virology*, not JMV.")
B("")
B("## 1. Rules and how they were applied")
B("")
B("| Item | Applied | Status |")
B("|---|---|---|")
for r in [
    ("Article type", "Original (research) article; retrospective ecological study of routinely collected data", "author's choice"),
    ("Abstract", "One unstructured paragraph, no references, %d words" % calc["abstract_words"], "UNVERIFIED limit: 200 (one source) or 250 (another); %d words satisfies both" % calc["abstract_words"]),
    ("Keywords", "5", "UNVERIFIED: \"3\u20136\" and \"up to 5\" both appear"),
    ("Main-text length", "%s words (Introduction to Conclusion, body paragraphs)" % MAIN_WORDS, "UNVERIFIED limit 4,000 words for a Research Article. **Over the limit.** The draft had about 4,800 and the 2026 qualifiers added more. Cutting is the authors' decision; not done"),
    ("References", "%d (62 from the draft + new)" % calc["n_refs"], "UNVERIFIED limit 50. **Over.** Not cut"),
    ("Reference style", "Numbered by first citation; NLM/AMA entries (`Authors. Title. Journal. Year;vol(issue):pages.`); more than 6 authors \u2192 first 3 + et al; superscript in-text numbers (one character style, `Citation Reference`, switches this)", "UNVERIFIED (snippets say AMA-based)"),
    ("Section order", "1 Introduction, 2 Materials and Methods, 3 Results, 4 Discussion, 5 Conclusion; numbered headings in the form `1 | INTRODUCTION`, `2.1 | Title`", "UNVERIFIED (Wiley template convention); the draft had ASM order with Methods last"),
    ("IMPORTANCE statement", "Removed (ASM-only). Verbatim text in section 3 below", "applied"),
    ("Title page", "Title, running title, authors, affiliations, two corresponding authors, ORCID iDs (placeholder), funding (placeholder), word counts", "running-title length UNVERIFIED"),
    ("Back matter", "Author contributions, Acknowledgments, Funding, Conflict of interest, Data availability, Ethics, Supporting information", "placeholders for what only the authors can state"),
    ("Page layout", "Times New Roman 12 pt, double spacing, 1-inch margins, US Letter, continuous line numbers (kept from the draft), page numbers", "UNVERIFIED (A4?); the \"St. Jude - Confidential\" footers were never enabled and are removed"),
    ("Figures", "Separate files, never embedded; legends after the references, in order of citation (Figures 1\u20138, S1\u2013S7); copies under the manuscript numbers in `manuscript/figures/`", "file format and resolution UNVERIFIED (see section 4)"),
    ("Partial year 2026", "Every paragraph and legend that uses 2026 states that it covers January\u2013September and is annualized (build check); abstract, Methods 2.1/2.5, Results, Discussion, limitations and conclusion", "author instruction (comment 51), not a journal rule"),
    ("Tables", "None", ""),
    ("Reporting guideline", "RECORD (STROBE extension), cited in Methods; checklist in `RECORD_CHECKLIST.md`", "UNVERIFIED whether JMV requires the checklist"),
    ("Generative-AI disclosure", "Not stated in the manuscript", "UNVERIFIED: publisher policies usually ask authors to disclose AI-assisted work; the authors decide the wording"),
    ("Submission route", "Not applicable", "UNVERIFIED: JMV may accept a free-format first submission, with formatting required at revision"),
]:
    B("| " + " | ".join(r) + " |")
B("")
B("## 2. Placeholders still in the manuscript (highlighted yellow)")
B("")
for t in ["ORCID iDs of all authors", "Funding information (title page and the FUNDING section)", "Author contributions", "Acknowledgments", "Conflict of interest statement",
          "DOI for the repository (none issued; confirm the repository is public)", "Wording of the Supporting Information sentence"]:
    B("- " + t)
B("")
B("## 3. Text removed or replaced")
B("")
B("**IMPORTANCE block (ASM only), verbatim from the draft.** It contains claims that the regenerated results no longer support (a southward expansion of chikungunya; a lagged "
  "temperature association shared by the three viruses):")
B("")
B("> " + imp)
B("")
B("**Round 2.** The sentences on the distributed lag non-linear model (DLNM) were deleted from Methods 2.9, Results 3.6 and the Discussion (comment 55); the pooled lagged model replaces them.")
B("")
B("## 4. Figure files (copies in `manuscript/figures/`; the pipeline keeps its own names)")
B("")
B("| Manuscript file | Pixels | Stored dpi |")
B("|---|---|---|")
for fg in rep["figures"]:
    num = fg["number"]
    files = fg["files"]
    for x in files:
        name = ("Figure%s.png" % num) if len(files) == 1 else ("Figure%s_%s.png" % (num, Path(x).stem.split("_", 1)[1]))
        w, h, dpi = png_info(next((PROJECT / "figures").rglob(x)))
        B("| `%s` | %d \u00d7 %d | %s |" % (name, w, h, dpi or "n/a"))
B("")
B("Journals usually ask for TIFF or EPS at 300 dpi or more (line art at higher resolution). **UNVERIFIED for JMV.** PNG was left as is.")
B("")
B("## 5. Decisions for the authors")
B("")
for t in [
    "Length: %s words and %d references against candidate limits of 4,000 and 50." % (MAIN_WORDS, calc["n_refs"]),
    "Interpretation changes marked \u21c4 in `SYNC_LOG.md`: chikungunya's global spatial autocorrelation is now significant; Zika's pooled temperature association is positive (borderline) and chikungunya's is not significant.",
    "The Zika lag signal differs between the pooled lagged model (lag 1) and the per-FU lagged models (lag 2); both are reported.",
    "The reading of the early-2016 chikungunya classification codes (code 2 discarded, code 1 confirmed) and the missing Espirito Santo 2021 notifications need confirmation from the data source.",
    "2026 is kept with its qualifier; a sensitivity analysis restricted to 2016\u20132025 was not run.",
    "Serotype value 0 (Figure 7D) and the Espirito Santo counts: the author queries are still open.",
    "AI-use disclosure wording, ORCID, funding, contributions, conflicts, acknowledgments.",
    "Galileu's threads were answered but left open for him to close.",
]:
    B("- " + t)
B("")
B("## 6. Structural changes that the redline does not track")
B("")
B("Section reordering (Methods before Results), run-in headings turned into numbered heading styles, new styles and page layout, removal of the unused footer parts, "
  "reference renumbering and reformatting (the redline shows the text change of each entry), figure renumbering by order of citation, and the re-anchoring of comments to the rewritten sentences.")
(dest / "JMV_CHECKLIST.md").write_text("\n".join(C) + "\n", encoding="utf-8")

# =============================================================== RECORD_CHECKLIST
R = []
Q = R.append
Q("# RECORD checklist (STROBE extension for routinely collected health data)")
Q("")
Q("Round 1 written 2026-10-21, updated 2026-10-22. Section numbers refer to `Alves ER et al JMV 2026.docx`. \"Author\" means the authors must complete or confirm it. "
  "Item wording is abbreviated; use the official checklist (Benchimol et al., PLoS Med 2015;12:e1001885) for submission.")
Q("")
Q("| Item | Requirement (abbreviated) | Where | Status |")
Q("|---|---|---|---|")
for r in [
    ("1a / R1.1", "Study design in the title or abstract; name of the database", "Abstract; title (SINAN is named in Methods 2.2, not in the abstract)", "Partly: add \"SINAN\" to the abstract"),
    ("R1.2", "Geographic region and timeframe in the title or abstract", "Title; Abstract", "Addressed"),
    ("R1.3", "Linkage between databases stated", "2.2, 2.3, 2.1 (notifications, climate and population joined by FU and month)", "Addressed"),
    ("2", "Scientific background and rationale", "1", "Addressed"),
    ("3", "Objectives", "1 (last paragraph)", "Addressed"),
    ("4", "Key elements of the design", "2.1", "Addressed"),
    ("5", "Setting, locations, dates", "2.1, 2.2 (notifications up to September 30, 2026)", "Addressed"),
    ("6 / R6.1\u20136.3", "Study population and selection (codes, algorithms; validation; flow)", "2.2 (case definition: all notifications not classified as discarded; classification codes; discarded counts per disease; FU and month assignment)", "Partly: no code validation study; no flow diagram"),
    ("7 / R7.1", "Variables and the codes or algorithms for them", "2.2\u20132.4", "Partly: SINAN field names are given in `docs/`, not in the text"),
    ("8", "Data sources and measurement", "2.2, 2.3", "Addressed"),
    ("9", "Bias", "4 (limitations): under-reporting, misclassification, differing definitions, discarded notifications, annualized 2026, missing Esp\u00edrito Santo 2021", "Addressed"),
    ("10", "Study size", "2.1 (27 FU, %d months); 3.1 (cases)" % int(float(N["n_months"])), "Addressed"),
    ("11", "Quantitative variables", "2.5\u20132.9 (incidence per 100,000, IRR per 1 \u00b0C and per 100 mm)", "Addressed"),
    ("12 / R12.1\u201312.3", "Statistical methods; access to the database; data cleaning; linkage", "2.5\u20132.10", "Partly: access to the database population and cleaning are described in `docs/DATA_SOURCES.md`; summarize in 2.2 if required"),
    ("13 / R13.1", "Participants at each stage; flow", "2.2 (notifications, discarded, cases), figure legends (records excluded per figure)", "Partly: aggregate data, no individual flow diagram"),
    ("14", "Descriptive data", "3.1, 3.5", "Addressed"),
    ("15", "Outcome data", "3.1\u20133.3", "Addressed"),
    ("16", "Main results with precision", "3.6 (IRR with 95% CI)", "Addressed"),
    ("17", "Other analyses", "3.4, 3.6 (per-FU lagged and pooled lagged models)", "Addressed"),
    ("18", "Key results", "4, 5", "Addressed"),
    ("19 / R19.1", "Limitations; implications of using data not created for the question", "4 (limitations)", "Addressed"),
    ("20", "Interpretation", "4", "Addressed"),
    ("21", "Generalisability", "4 (limitations: FU level, ecological design)", "Partly: no explicit statement beyond Brazil"),
    ("22", "Funding", "Title page, FUNDING", "Author"),
    ("R22.1", "How to access supplemental information, raw data, code", "DATA AVAILABILITY STATEMENT", "Addressed; confirm the repository is public"),
]:
    Q("| " + " | ".join(r) + " |")
(dest / "RECORD_CHECKLIST.md").write_text("\n".join(R) + "\n", encoding="utf-8")
print("written to", dest)
