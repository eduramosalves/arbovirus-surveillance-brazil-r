"""Generate docs/manuscript/{SYNC_LOG,JMV_CHECKLIST,RECORD_CHECKLIST}.md. Usage: python gen_logs.py <outdir> <destdir>"""
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
PROJECT = Path("C:/Users/Usuario/arbovirus-surveillance-brazil-r-eduardo")


def f(key, spec="d1"):
    v = float(N[key])
    if spec == "i":
        return "{:,.0f}".format(v)
    if spec.startswith("d"):
        return "{:,.{}f}".format(v, int(spec[1:])).replace("-", "\u2212")
    if spec == "pct1":
        return "{:.1f}%".format(v * 100)
    return N[key]


UF = {"AC": "Acre", "AL": "Alagoas", "AP": "Amap\u00e1", "AM": "Amazonas", "BA": "Bahia", "CE": "Cear\u00e1", "DF": "Federal District",
      "ES": "Esp\u00edrito Santo", "GO": "Goi\u00e1s", "MA": "Maranh\u00e3o", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
      "PA": "Par\u00e1", "PB": "Para\u00edba", "PR": "Paran\u00e1", "PE": "Pernambuco", "PI": "Piau\u00ed", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
      "RS": "Rio Grande do Sul", "RO": "Rond\u00f4nia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "S\u00e3o Paulo", "SE": "Sergipe", "TO": "Tocantins"}

# =============================================================== SYNC_LOG
L = []
A = L.append
A("# Manuscript sync log: draft (2016\u20132025, Python) \u2192 JMV manuscript (2016\u20132026, R)")
A("")
A("Written 2026-10-21. Covers `Alves ER et al JMV 2026.docx` (clean) and `Alves ER et al JMV 2026 (redline).docx` (every text change "
  "tracked, author *Claude for ERA*), both built from `Alves ER et al JVI 2026.docx`, which was not modified.")
A("")
A("**How the numbers were produced.** Every number in the Abstract, Results, Discussion and Methods was computed from the repository files "
  "by `build/numbers.R` (R 4.6.1) into `numbers.csv`, and inserted into the text by key. The table in section 3 lists each inserted number "
  "with its source file. Legends are the text of `docs/FIGURE_CAPTIONS.md`. A second, independent computation in Python (section 6) "
  "reproduced 40 headline values from the raw tables.")
A("")
A("## 1. Headline changes in the claims")
A("")
A("The regenerated results (R, 2016\u20132026) reverse several statements of the draft (Python, 2016\u20132025). The manuscript text was rewritten to what "
  "the regenerated outputs show. Items marked **\u21c4** change the interpretation and need the co-authors' attention.")
A("")
A("| | Draft | Manuscript | Source |")
A("|---|---|---|---|")
rows = [
    ("Moran's I, dengue / chikungunya / Zika", "0.562 (p = 0.001) / \u22120.036 (0.460) / \u22120.008 (0.352)",
     "%s / %s / %s (p %s / %s / %s)" % (f("moran.DENV.I", "d3"), f("moran.CHIKV.I", "d3"), f("moran.ZIKV.I", "d3"), f("moran.DENV.p", "d3"), f("moran.CHIKV.p", "d3"), f("moran.ZIKV.p", "d3")),
     "`outputs/geo_spatial_stats.xlsx`, Global_Moran"),
    ("Mean annual incidence, dengue top 3", "DF 1,825.6; GO 1,742.7; MG 1,647.7",
     "GO %s; DF %s; MG %s" % (f("rank_minc_val.DENV.1"), f("rank_minc_val.DENV.2"), f("rank_minc_val.DENV.3")), "`geo_spatial_stats.xlsx`, Mean_Incidence"),
    ("Chikungunya top mean incidence", "MS 421.8", "MS %s; CE %s; MT %s" % (f("rank_minc_val.CHIKV.1"), f("rank_minc_val.CHIKV.2"), f("rank_minc_val.CHIKV.3")), "same"),
    ("Zika top mean incidence", "TO 145.7; MT 106.7", "TO %s; MT %s" % (f("rank_minc_val.ZIKV.1"), f("rank_minc_val.ZIKV.2")), "same"),
    ("\u21c4 Dengue increasing trends", "RS, SC, SP", "RS (\u03c4 %s), SC (\u03c4 %s); SP not significant (p = %s)" % (f("mk.DENV.RS.tau", "d3"), f("mk.DENV.SC.tau", "d3"), f("mk.DENV.SP.p", "d3")), "`py_statistical_results.xlsx`, Mann_Kendall"),
    ("\u21c4 Chikungunya increasing trends", "SC, RS, MS", "MS, MG, GO; SC (p = %s) and RS (p = %s) not significant" % (f("mk.CHIKV.SC.p", "d3"), f("mk.CHIKV.RS.p", "d3")), "same"),
    ("\u21c4 Zika decreasing trends", "AL, PI, DF (3 states)", "6 states (DF, PI, MG, RJ, AL, PR)", "same"),
    ("\u21c4 Multiple testing", "\"no adjustment\"", "Benjamini\u2013Hochberg q-values reported; no trend survives (minimum q: dengue %s, chikungunya %s, Zika %s)" % (f("mk_minq.DENV", "d3"), f("mk_minq.CHIKV", "d3"), f("mk_minq.ZIKV", "d3")), "Mann_Kendall, q_value"),
    ("Dengue LISA high\u2013high", "Central-West and Southeast", "also Paran\u00e1; after BH correction only GO, MG (HH) and RJ (LH)", "`geo_spatial_stats.xlsx`, LISA_Clusters"),
    ("Zika 2016 vs later years", "\"roughly 8\u201310 times\"", "%s\u2013%s times (complete years 2017\u20132025)" % (f("zika_ratio_min"), f("zika_ratio_max")), "`source_data/Figure1.xlsx`"),
    ("\u21c4 Pooled temperature IRR, dengue", "2.10 (1.96\u20132.26)", "%s (%s\u2013%s)" % (f("glmp.DENV.Temp_Avg.irr", "d2"), f("glmp.DENV.Temp_Avg.lo", "d2"), f("glmp.DENV.Temp_Avg.hi", "d2")), "`outputs/glm_negbin_pooled_fe.csv`"),
    ("\u21c4 Pooled temperature IRR, chikungunya", "1.32 (1.24\u20131.41), significant", "%s (%s\u2013%s), **not significant**" % (f("glmp.CHIKV.Temp_Avg.irr", "d2"), f("glmp.CHIKV.Temp_Avg.lo", "d2"), f("glmp.CHIKV.Temp_Avg.hi", "d2")), "same"),
    ("\u21c4 Pooled temperature IRR, Zika", "0.90 (0.84\u20130.97), inverse", "%s (%s\u2013%s), **positive**" % (f("glmp.ZIKV.Temp_Avg.irr", "d2"), f("glmp.ZIKV.Temp_Avg.lo", "d2"), f("glmp.ZIKV.Temp_Avg.hi", "d2")), "same"),
    ("\u21c4 Rainfall", "IRR 1.007 per mm; Spearman \u03c1 \u2248 0", "IRR per 100 mm %s / %s / %s; mean \u03c1 at lag 2 %s / %s / %s" % (f("glmp.DENV.Rain_mm.irr100", "d2"), f("glmp.CHIKV.Rain_mm.irr100", "d2"), f("glmp.ZIKV.Rain_mm.irr100", "d2"), f("sp.DENV.Rain.2.mean", "d3"), f("sp.CHIKV.Rain.2.mean", "d3"), f("sp.ZIKV.Rain.2.mean", "d3")), "glm CSVs; `Spearman_Lag`"),
    ("Temperature Spearman \u03c1 (national mean)", "dengue 0.16 \u2192 0.19, \"positive at all lags\"", "dengue %s / %s / %s at lags 0 / 1 / 2 (negative, ~0, positive)" % (f("sp.DENV.Temp.0.mean", "d3"), f("sp.DENV.Temp.1.mean", "d3"), f("sp.DENV.Temp.2.mean", "d3")), "`Spearman_Lag`"),
    ("NB2 dispersion \u03b1", "1.69 / 1.45 / 1.55", "%s / %s / %s" % (f("glmp.DENV.alpha", "d2"), f("glmp.CHIKV.alpha", "d2"), f("glmp.ZIKV.alpha", "d2")), "pooled CSV"),
    ("Per-state temperature, significant FU", "16 / 12 / 10", "%s / %s / %s" % (f("glms.DENV.Temp_Avg.nsig", "i"), f("glms.CHIKV.Temp_Avg.nsig", "i"), f("glms.ZIKV.Temp_Avg.nsig", "i")), "`glm_negbin_per_state.csv`"),
    ("Lag-2 temperature, significant FU", "11 / 4 / 7", "%s / %s / %s" % (f("glml.DENV.Temp_Lag2.nsig", "i"), f("glml.CHIKV.Temp_Lag2.nsig", "i"), f("glml.ZIKV.Temp_Lag2.nsig", "i")), "`glm_negbin_lagged.csv`"),
    ("Hospitalization (comment 13)", "15,788,792 not hospitalized; 529,203 hospitalized", "%s hospitalized; %s not; %s ignored/blank (sum %s)" % (f("cl.DENV.hosp.Positive", "i"), f("cl.DENV.hosp.Negative", "i"), f("cl.DENV.hosp.IgnBlank", "i"), f("cl.DENV.hosp.total", "i")), "`source_data/Figure7.xlsx`"),
    ("Placeholders", "[X], xxxxx, [REF IBGE??]", "chikungunya men %s; DENV-2 %s; DENV-3 %s; DENV-4 %s; IBGE references added" % (f("cl.CHIKV.sex.M", "i"), f("cl.DENV.sero.DENV2", "i"), f("cl.DENV.sero.DENV3", "i"), f("cl.DENV.sero.DENV4", "i")), "Figure 5/7 source data"),
    ("Chikungunya peak year", "(comment 9)", "2024 (%s per 100,000), second 2016 (%s); Central-West 2025 %s" % (f("ann.CHIKV.BR.2024"), f("ann.CHIKV.BR.2016"), f("chik_regmax_val")), "`Figure1.xlsx`"),
]
for r in rows:
    A("| " + " | ".join(r) + " |")
A("")
A("## 2. Methods statements rewritten to what the code does")
A("")
A("| Draft statement | Manuscript statement | Evidence in the repository |")
A("|---|---|---|")
for r in [
    ("Analyses in Python 3.12 (pandas, statsmodels, GeoPandas\u2026)", "R 4.6.1; data.table, readxl, sf, spdep, classInt, ggplot2, patchwork", "`R_SESSION_INFO.txt`; `docs/R_PORT_NOTES.md`"),
    ("Temperature from CPC/NCEP grid; rainfall from INMET and CPTEC/INPE", "INMET hourly automatic stations, \u2265240 (temperature) / \u2265360 (rainfall) valid hourly readings per station-month, unweighted mean per FU", "`etl/build_climate.R` lines 4, 30, 106\u2013108, 134\u2013135"),
    ("Spatial weights: Queen contiguity with kNN fallback", "Row-standardized kNN (k = 5) on polygon centroids only", "`pipelines/data_loader.R` 141\u2013142; `R/stats.R` 70\u201373"),
    ("\"No adjustment for multiple comparisons\"", "Raw p reported with Benjamini\u2013Hochberg q-values", "`R/utils.R` 84 (`p.adjust(method = \"BH\")`); `Significant_FDR` columns"),
    ("Pooled distributed-lag model (comment 16)", "Per-FU unconstrained lag model (lags 0\u20132 jointly); separate pooled constrained DLNM", "`pipelines/glm_common.R` `SPECS` 48\u201351; `pipelines/additional/adv_dlnm.R`"),
    ("\"Overdispersion assessed by testing \u03b1 > 0\" (comment 22)", "Pearson dispersion of the Poisson fit and ML \u03b1; no formal test", "`glm_common.R` 156\u2013180; no `lrtest` anywhere"),
    ("State fixed effects only; model-based SE", "Pooled: FU + calendar-month FE, FU-clustered SE; per-FU and lagged: month FE, Newey\u2013West (3 lags)", "`glm_common.R` 6\u201321, 38, 44\u201351, 183\u2013200"),
    ("Discarded and under-investigation cases excluded; FU of residence", "Dengue = notifications minus discarded; chikungunya and Zika = all notifications; FU/month of notification", "`etl/build_cases_clinical.R` 88, 116\u2013130; `README.md` 156\u2013160"),
    ("Population: 2022 Census and intercensal estimates [REF]", "IBGE projections (2024 revision) 2016\u20132023; DOU 1-July estimates 2024\u20132026", "`etl/build_population.R` 1\u20136; `docs/DATA_SOURCES.md` 21\u201328"),
    ("Study period to December 31, 2025", "To September 30, 2026; 2026 annualized as cases \u00d7 12 / months", "`pipelines/data_loader.R` 77\u201390"),
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
A("- Figure legends: `docs/FIGURE_CAPTIONS.md` (generated from `outputs/figure_caption_values.csv`, `figure_exclusions*.csv`). Renumbered: the five GLM figures become "
  "Supplementary Figures S3\u2013S7; \"UF\" becomes \"FU\"; American spelling; legends of S3 and S4 note that rainfall is drawn per 1 mm while the text uses 100 mm.")
A("- Literature thresholds (Liu 2023: 14.8 \u00b0C minimum, 32\u201333 \u00b0C optimum maximum; Lim 2025; Moura 2020 at abstract level; de Lima 2026: DENV-3 detection in Cear\u00e1 in July 2025): `docs/LITERATURE_CONTEXT.md`.")
A("- Not verified against the original source: the Espirito Santo 2021 counts (2,901 chikungunya, 872 Zika) quoted in `docs/FIGURE_CAPTIONS.md`; the cited page could not be read, so the numbers are left out of the manuscript (author query attached).")
A("")
A("## 5. Derived values (not in any output file)")
A("")
A("- Rainfall IRR per 10 and per 100 mm = exp(k \u00d7 Coef) and exp(k \u00d7 (Coef \u00b1 c \u00d7 SE)) from `glm_negbin_pooled_fe.csv`, with c = 1.96 (the critical value implied by the exported CI). 100 mm \u2248 1 SD of monthly rainfall (%s mm)." % f("clim.rain_sd", "d0"))
A("- Seasonal totals: sums of `db/normalized_fact_cases.csv` by calendar month over 2016\u20132025 (complete years). Ratios of Zika 2016 incidence to later years from `Figure1.xlsx`.")
A("- Hospitalization, serotype and discard shares: ratios of the counts in `source_data/Figure5/7/8.xlsx`.")
A("")
A("## 6. Independent verification")
A("")
A("`build/recompute.py` recomputes, from `db/` and the source tables and without using `numbers.csv` or the R outputs, and looks for the result in the manuscript text: "
  "case totals, 2024 dengue and 2016 Zika, state totals, national incidence, population-weighted mean incidence (GO, DF, MS, TO), "
  "Mann\u2013Kendall \u03c4 and Sen's slope (dengue RS, chikungunya MS), Spearman \u03c1 (dengue MG, RJ; national means), global Moran's I for the three diseases from polygon centroids, "
  "the pooled Poisson and NB2 temperature IRRs and the rainfall IRR per 100 mm by refitting the model by IRLS, the hospitalization and serotype counts, chikungunya men, "
  "and the pooled January and May totals. **Result: 40 of 40 matched.**")
A("")
A("## 7. Data-quality findings that need a decision (not fixed here)")
A("")
for t in [
    "**Discarded notifications.** Chikungunya and Zika include discarded notifications (comments 18\u201319). Dengue excludes them. Changing this means rerunning the pipeline: the Zika discard code is 2, not 5 (2016: 62,198 records, equal to the GraphPad \"Discarded\" count), and chikungunya 2016 has 102,858 records with legacy classification codes 1 and 2 (shown as \"Dengue classico\" and \"Dengue c/ complicacoes\") whose meaning is not documented.",
    "**Annualized 2026.** \u00d712/9 overstates 2026 because October\u2013December hold %s / %s / %s of the cases (dengue / chikungunya / Zika, 2016\u20132025). 2026 enters the trends, mean incidence, Moran's I and LISA." % (f("seas.DENV.q4_share", "pct1"), f("seas.CHIKV.q4_share", "pct1"), f("seas.ZIKV.q4_share", "pct1")),
    "**GraphPad tables (Figures 5, 7, 8)** end in 2025. Their yearly dengue totals are below `clinical_tables/` by 3,954 (2020), 8,238 (2021), 10,563 (2022) and 998 (2023); the 2021\u20132022 gaps are close to the Esp\u00edrito Santo notifications in `clinical_tables/` (8,726 and 11,218). The former state-total and monthly-heatmap figures end in 2025 as well and are not cited.",
    "**`clinical_tables/clinical_demographic_long.csv`**: age is 100% ignored for dengue 2016\u20132019 and chikungunya 2017\u20132020; classification labels are the dengue labels for every disease (Zika code 1 is shown as \"Dengue classico\" but is confirmed); SINAN serotype value 0 appears as `codigo_0` (134,407 in 2023).",
    "**Figure 7A/7B labels**: \"ELISA\" matches the NS1 antigen field and \"IgM\" the IgM serology field by yearly counts (e.g. 2016 positives 97,530 vs 97,528). Confirm.",
    "**Pooled lagged model**: none exists in the outputs, so the manuscript reports the per-FU lagged models. Add a `pooled = TRUE` lagged entry to `SPECS` in `pipelines/glm_common.R` if the authors want it reported.",
]:
    A("- " + t)
A("")
A("## 8. Figure map")
A("")
A("| Draft (old numbering) | Manuscript | Repository file |")
A("|---|---|---|")
for r in [("Fig 1A\u2013B maps", "Figure 6", "`figures/Figure6_combined_map.png`"), ("Fig 1C annual maps", "Supplementary Figure S1", "`FigureS1_2016\u20132026.png`, `FigureS1_overview.png`"),
          ("Fig 1D LISA and trend maps", "Supplementary Figure S2", "`FigureS2_lisa_trend.png`"), ("Fig 2 incidence", "Figure 1", "`Figure1_incidence_regional.png`"),
          ("Fig 3 Moran scatter", "Figure 4", "`Figure4_spatial_autocorrelation.png`"), ("Fig 4 age and sex", "Figure 5", "`Figure5_demographics.png`"),
          ("Fig 5 dengue clinical", "Figure 7", "`Figure7_dengue_clinical.png`"), ("Fig 6 chikungunya and Zika clinical", "Figure 8", "`Figure8_chikv_zika_clinical.png`"),
          ("Fig 7 trends", "Figure 2", "`Figure2_trend_analysis.png`"), ("Fig 8 correlations", "Figure 3", "`Figure3_climate_correlations.png`"),
          ("S5 AIC", "Supplementary Figure S6", "`glm_fig4_aic_comparison.png`"), ("S6 pooled", "Supplementary Figure S3", "`glm_fig1_pooled_climate_irr.png`"),
          ("S7/S8 per-state", "Supplementary Figures S4 and S7", "`glm_fig2_per_state_heatmap.png`, `glm_fig5_forest_significant.png`"),
          ("S9 lag profile", "Supplementary Figure S5", "`glm_fig3_lag_profile.png`"),
          ("S1A\u2013C state totals, S2A\u2013C seasonal heatmaps", "not cited", "`outputs/*_05_federative_unit_totals.png`, `*_01b_monthly_heatmap.png` (end in 2025)"),
          ("Table S11", "not cited", "`outputs/glm_*_results.xlsx`")]:
    A("| " + " | ".join(r) + " |")
A("")
A("## 9. Reference list")
A("")
A("62 references converted from ASM to NLM/AMA style and renumbered by order of first citation (the Methods now precede the Results). New entries: Liu 2023, Moura 2020, Lim 2025, de Lima 2026, IBGE (projections; DOU estimates), INMET, Governo do Esp\u00edrito Santo 2021. "
  "No DOIs were added except those already in the draft or given in `docs/LITERATURE_CONTEXT.md`; journal abbreviations are those of the draft. "
  "Rule used for authors: more than 6 \u2192 first 3 + et al (AMA); **unverified for JMV**.")
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
B("Written 2026-10-21 for `Alves ER et al JMV 2026.docx`.")
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
    ("Abstract", "One unstructured paragraph, no references, %d words" % calc["abstract_words"], "UNVERIFIED limit: 200 (one source) or 250 (another); 197 words satisfies both"),
    ("Keywords", "5", "UNVERIFIED: \"3\u20136\" and \"up to 5\" both appear"),
    ("Main-text length", "%s words (Introduction to Conclusion, body paragraphs)" % "{:,}".format(calc["main_words"]), "UNVERIFIED limit 4,000 words for a Research Article. **Over the limit.** The draft had about 4,800. Cutting is the authors' decision; not done"),
    ("References", "%d (62 from the draft + 8 new)" % calc["n_refs"], "UNVERIFIED limit 50. **Over.** Not cut"),
    ("Reference style", "Numbered by first citation; NLM/AMA entries (`Authors. Title. Journal. Year;vol(issue):pages.`); more than 6 authors \u2192 first 3 + et al; superscript in-text numbers (one character style, `Citation Reference`, switches this)", "UNVERIFIED (snippets say AMA-based)"),
    ("Section order", "1 Introduction, 2 Materials and Methods, 3 Results, 4 Discussion, 5 Conclusion; numbered headings in the form `1 | INTRODUCTION`, `2.1 | Title`", "UNVERIFIED (Wiley template convention); the draft had ASM order with Methods last"),
    ("IMPORTANCE statement", "Removed (ASM-only). Verbatim text in section 3 below", "applied"),
    ("Title page", "Title, running title, authors, affiliations, two corresponding authors, ORCID iDs (placeholder), funding (placeholder), word counts", "running-title length UNVERIFIED"),
    ("Back matter", "Author contributions, Acknowledgments, Funding, Conflict of interest, Data availability, Ethics, Supporting information", "placeholders for what only the authors can state"),
    ("Page layout", "Times New Roman 12 pt, double spacing, 1-inch margins, US Letter, continuous line numbers (kept from the draft), page numbers", "UNVERIFIED (A4?); the \"St. Jude - Confidential\" footers were never enabled and are removed"),
    ("Figures", "Separate files, never embedded; legends after the references, in figure order (Figures 1\u20138, S1\u2013S7)", "file format and resolution UNVERIFIED (see section 4)"),
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
B("## 4. Figure files (not changed)")
B("")
B("| File | Pixels | Stored dpi |")
B("|---|---|---|")
for p in sorted((PROJECT / "figures").glob("Figure[0-9]*.png")) + [PROJECT / "figures" / "FigureS2_lisa_trend.png", PROJECT / "figures" / "FigureS1_overview.png"] + sorted((PROJECT / "figures").glob("glm_fig*.png")):
    w, h, dpi = png_info(p)
    B("| `%s` | %d \u00d7 %d | %s |" % (p.name, w, h, dpi or "n/a"))
B("")
B("Journals usually ask for TIFF or EPS at 300 dpi or more (line art at higher resolution). **UNVERIFIED for JMV.** PNG at 200\u2013300 dpi was left as is.")
B("")
B("## 5. Decisions for the authors")
B("")
for t in [
    "Discarded chikungunya and Zika notifications are in the counts (comments 18\u201319): keep and document (as written) or rerun without them.",
    "Annualized 2026 enters the trends, means, Moran's I and LISA: keep, or restrict the main analyses to 2016\u20132025.",
    "Length: %s words and %d references against candidate limits of 4,000 and 50." % ("{:,}".format(calc["main_words"]), calc["n_refs"]),
    "Figure numbers follow the repository set; first citations are not sequential (Figure 6 before 1 and 4). Renumber or reorder if the journal requires it.",
    "Figure style (comment 6): no titles, legend placement, one colour per virus (for example chikungunya in green), removal of non-significant increasing/decreasing labels.",
    "The supplementary DLNM has no numbered figure (author query attached).",
    "Regenerate the figures built from the GraphPad tables (5, 7, 8) to 2026, and the former state-total and seasonal figures, if the text should match the full window.",
    "Interpretation changes marked \u21c4 in `SYNC_LOG.md`, in particular that Zika's pooled temperature association is now positive and chikungunya's is not significant.",
    "Whether to report a pooled lagged model (none exists in the outputs).",
    "AI-use disclosure wording, ORCID, funding, contributions, conflicts, acknowledgments.",
]:
    B("- " + t)
B("")
B("## 6. Structural changes that the redline does not track")
B("")
B("Section reordering (Methods before Results), run-in headings turned into numbered heading styles, new styles and page layout, removal of the unused footer parts, "
  "reference renumbering and reformatting (the redline shows the text change of each entry), and the re-anchoring of comments to the rewritten sentences.")
(dest / "JMV_CHECKLIST.md").write_text("\n".join(C) + "\n", encoding="utf-8")

# =============================================================== RECORD_CHECKLIST
R = []
Q = R.append
Q("# RECORD checklist (STROBE extension for routinely collected health data)")
Q("")
Q("Written 2026-10-21. Section numbers refer to `Alves ER et al JMV 2026.docx`. \"Author\" means the authors must complete or confirm it. "
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
    ("5", "Setting, locations, dates", "2.1, 2.2", "Addressed"),
    ("6 / R6.1\u20136.3", "Study population and selection (codes, algorithms; validation; flow)", "2.2 (case definition per disease, FU and month assignment)", "Partly: no code validation study; no flow diagram"),
    ("7 / R7.1", "Variables and the codes or algorithms for them", "2.2\u20132.4", "Partly: SINAN field names are given in `docs/`, not in the text"),
    ("8", "Data sources and measurement", "2.2, 2.3", "Addressed"),
    ("9", "Bias", "4 (limitations): under-reporting, misclassification, differing definitions, annualized 2026, missing Esp\u00edrito Santo 2021", "Addressed"),
    ("10", "Study size", "2.1 (27 FU, 129 months); 3.1 (notifications)", "Addressed"),
    ("11", "Quantitative variables", "2.5\u20132.9 (incidence per 100,000, IRR per 1 \u00b0C and per 100 mm)", "Addressed"),
    ("12 / R12.1\u201312.3", "Statistical methods; access to the database; data cleaning; linkage", "2.5\u20132.10", "Partly: access to the database population and cleaning are described in `docs/DATA_SOURCES.md`; summarize in 2.2 if required"),
    ("13 / R13.1", "Participants at each stage; flow", "2.2, figure legends (records excluded per figure)", "Partly: aggregate data, no individual flow"),
    ("14", "Descriptive data", "3.1, 3.5", "Addressed"),
    ("15", "Outcome data", "3.1\u20133.3", "Addressed"),
    ("16", "Main results with precision", "3.6 (IRR with 95% CI)", "Addressed"),
    ("17", "Other analyses", "3.4, 3.6 (lagged, DLNM)", "Addressed"),
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
