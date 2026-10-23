"""Replies of 'Claude for ERA' (round 2, 2026-10-22) to the threads of the manuscript, and the threads to close.

REPLIES_R2: root comment id -> reply text. Roots are the comments of the co-author (ids 3-22) and the assistant's own
queries (44-47); the user's instructions (ids 48-55) sit in these threads. Texts use the same tokens as the manuscript:
{n:key:fmt} numbers from the repository outputs, {F:key:A} figure numbers (by order of first citation).
"""

REPLIES_R2 = {
    3: "Rechecked after the rerun. Every incidence value in the text is computed from the repository files and logged with its source "
       "(docs/manuscript/SYNC_LOG.md). Mean annual incidence of dengue: {u:rank_minc.DENV.1:cap} {n:rank_minc_val.DENV.1:d1}, "
       "{u:rank_minc.DENV.2} {n:rank_minc_val.DENV.2:d1}, {u:rank_minc.DENV.3} {n:rank_minc_val.DENV.3:d1} per 100,000 (2016–2026, with "
       "2026 annualized from January–September).",
    4: "Reran as asked, on the corrected data. Moran’s I of the mean annual incidence with the new case definition: dengue "
       "{n:moran.DENV.I:d3} (p {n:moran.DENV.p:pv}), chikungunya {n:moran.CHIKV.I:d3} (p {n:moran.CHIKV.p:pv}; now significant, "
       "with high–high units in the Northeast) and Zika {n:moran.ZIKV.I:d3} (p {n:moran.ZIKV.p:pv}). The text and the legends take "
       "them from one file (outputs/geo_spatial_stats.xlsx, sheet Global_Moran). The mean annual incidence includes 2026, a partial "
       "year (January–September) annualized, and this is now stated wherever these statistics appear.",
    5: "Done. Figures are numbered by the order in which the text first cites them (main figures 1–8, supplementary S1–S7), the "
       "legends follow that order, and the cross-references inside the legends were renumbered. Figure citations were removed from the "
       "Methods and the annual maps were added to the Results (they had never been cited). The figure files are copied under the new "
       "numbers in docs/manuscript/figures/ (the repository keeps its own file names); the mapping is in docs/manuscript/SYNC_LOG.md.",
    6: "Went through each point. (1) Titles: the figures have no in-plot titles, only the panel names Dengue, Chikungunya and Zika. "
       "(2) Legend close to the figure: the keys sit inside each panel, next to the data. (3) Non-significant increases/decreases: in the maps "
       "and in the Kendall’s τ panel only p < 0.05 carries colour; in the Sen’s slope panel ({F:trend:B}) the non-significant bars "
       "were coloured and are now grey. (4) One colour per virus: defined once (R/utils.R) and used in every figure, dengue red, "
       "chikungunya green, Zika blue; chikungunya was orange in several figures and green in others. The maps keep their symbol shapes and "
       "class colours, which do not encode the virus.",
    9: "Updated with the new case definition: chikungunya incidence is highest in 2024 ({n:ann.CHIKV.BR.2024:d1} per 100,000) and second in "
       "2016 ({n:ann.CHIKV.BR.2016:d1}), and 2016 is included. The highest regional annual value is the {n:chik_regmax_region:s} in "
       "{n:chik_regmax_year:y} ({n:chik_regmax_val:d1}). The Ministry of Health data you mention are not part of this project, so the "
       "comparison with them could not be checked.",
    12: "Updated: {n:cl.CHIKV.sex.M:i} men (cases of 2016–2026, discarded notifications excluded; 2026 is January–September).",
    13: "Rechecked with the rebuilt tables (2016–2026): {n:cl.DENV.hosp.Positive:i} hospitalized + {n:cl.DENV.hosp.Negative:i} not "
        "hospitalized + {n:cl.DENV.hosp.IgnBlank:i} ignored or blank = {n:cl.DENV.hosp.total:i} dengue cases. The ignored/blank "
        "group is a separate category, not part of “not hospitalized”.",
    14: "Updated from the rebuilt tables (2016–2026): DENV-1 {n:cl.DENV.sero.DENV1:i}, DENV-2 {n:cl.DENV.sero.DENV2:i}, DENV-3 "
        "{n:cl.DENV.sero.DENV3:i}, DENV-4 {n:cl.DENV.sero.DENV4:i}; the serotype is missing in {n:fe.DENV.sero.pct:d1}% of the cases.",
    16: "Answer to “what should we do now”, which you approved: a pooled lagged model was added (FU and month fixed effects, lags "
        "0–2 jointly, FU-clustered SE) and Results report its IRR per lag and the IRR of a change sustained over lags 0–2. In it the "
        "dengue effect is concentrated at lag 2 (IRR {n:glmpl.DENV.Temp_Lag2.irr:d2}), chikungunya is borderline at lag 2 (p "
        "{n:glmpl.CHIKV.Temp_Lag2.p:pv}) and Zika peaks at lag 1. The per-FU lagged models stay as the description of the "
        "heterogeneity. Both are unconstrained lag models, not DLNMs, and the DLNM was removed from the manuscript.",
    18: "Applied as instructed: for the three diseases a case is now any notification not classified as discarded (confirmed + probable; "
        "inconclusive and under-investigation notifications are kept as probable). Dengue already worked this way. The pipeline was "
        "rerun (SINAN downloaded again on 2026-10-22; notifications dated after 2026-09-30 left out) and every number, figure and legend "
        "follows it. Chikungunya is now {n:disc.CHIKV.cases:i} cases and Zika {n:disc.ZIKV.cases:i} (discarded excluded: "
        "{n:disc.CHIKV.disc:i} and {n:disc.ZIKV.disc:i}); the counts per year are in clinical_tables/discarded_counts.csv.",
    19: "Done as you asked: discarded notifications are excluded from every analysis and table of the three diseases (chikungunya, code 5 "
        "and, in the early-2016 form, code 2; Zika, code 2, were the ones still included). The dengue files from 2022 on contain no "
        "discarded notifications. Excluding them leaves many empty state-months, so those are now zeros instead of missing months (the "
        "small Zika counts would otherwise have been annualized over the few months with cases); Espirito Santo 2021 (chikungunya and "
        "Zika), with no notification at all, stays missing. The classification panel of {F:chikzika} now shows confirmed, inconclusive "
        "and not yet classified (probable) cases.",
    21: "Clarified and relabeled: the panel previously called ELISA is the dengue NS1 antigen result (SINAN field RESUL_NS1, matched by "
        "yearly counts) and is now titled that way in the figure ({F:dengue:A}); {F:dengue:B} is the IgM serology (RESUL_SORO). RT-PCR "
        "results exist in the clinical tables but are not plotted. Please confirm.",
    45: "Removed. The DLNM no longer appears in the Methods, the Results or the Discussion; the pooled lagged model reports what it added. "
        "The analysis itself stays among the repository outputs. This thread is closed.",
    47: "Kept 2026 in the analyses as you asked, and every place that uses it now says so: the abstract, the Methods (2.1, 2.3 to 2.6, "
        "2.8), Results 3.1, 3.2 and 3.5, the Discussion, the limitations, the conclusion and the legends of the figures that include "
        "2026 state that 2026 is a partial year (January–September), annualized ×12/9, which overstates it. A check in the build "
        "fails if a paragraph mentions 2026 without that statement. This thread is closed.",
}

CLOSE_THREADS = ["dlnm", "ann2026"]   # anchor keys of the assistant's own query threads, closed after the reply

AUTHOR = "Claude for ERA"
INITIALS = "C"
