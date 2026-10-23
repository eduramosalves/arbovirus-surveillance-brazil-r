from msbase import B, O

ASSERT = [
    ("N('chik_regmax_region') == 'Northeast' and N('chik_regmax_year') == 2016", "the highest regional chikungunya value is the Northeast in 2016"),
    ("0.4 < N('disc.ZIKV.share') < 0.5", "nearly half of the Zika notifications were discarded"),
    ("N('glml.ZIKV.Temp_Lag2.nsig') > N('glml.ZIKV.Temp_Lag1.nsig') and N('glmpl.ZIKV.Temp.maxlag') == 1", "Zika: per-FU models point to lag 2 and the pooled model to lag 1"),
    ("N('gap.n') == 2", "only Espirito Santo 2021 (chikungunya and Zika) is missing"),
    ("N('cl.ZIKV.malesh_maxyear') > N('cl.ZIKV.malesh_minyear')", "the male share of Zika cases rises over time"),
    ("N('fe.DENV.sero.pct') > 97", "more than 97% of dengue records lack the serotype"),
    ("N('disc.ZIKV.share') > N('disc.CHIKV.share') > N('disc.DENV.share')", "discarded share: Zika > chikungunya > dengue"),
    ("N('glms.ZIKV.Temp_Avg.nfdr') <= 4", "Zika per-FU temperature associations: few survive FDR"),
]

D1 = O(58,
    ("was the only arbovirus with significant spatial clustering, concentrated in a high-incidence corridor across the Central-West, Southeast, and South.",
     "showed the strongest global spatial clustering, concentrated in a high-incidence corridor across the Central-West, Southeast, and South; "
     "chikungunya showed significant but weaker clustering (Moran’s I = {n:moran.CHIKV.I:d3}), with a group of high-incidence "
     "states in the Northeast, and Zika showed none."),
    ("the Federal District and Goiás leading in incidence", "Goiás and the Federal District leading in incidence"),
    ("would underweight smaller populations that experience the highest transmission intensity.",
     "would underweight smaller populations that experience the highest transmission intensity. Only Goiás and Minas Gerais "
     "(high–high) and Rio de Janeiro (low–high) remained significant local clusters after correction for multiple "
     "testing, so the local cluster map should be read as exploratory. These spatial statistics use the mean annual incidence of "
     "2016–2026, whose last year is a partial year (January–September 2026) annualized and therefore overstated."))

D2 = O(59,
    ("The significant increasing trends in Rio Grande do Sul, Santa Catarina, and São Paulo are consistent with the documented "
     "southward expansion of dengue and of *Ae. aegypti* [@r22,@r38].",
     "In the national SINAN records, DENV-3 rose from {n:ct.sero_share.DENV3.2024:pct1} of typed records in 2024 to "
     "{n:ct.sero_share.DENV3.2025:pct1} in 2025 and {n:ct.sero_share.DENV3.2026:pct1} in the partial year January–September 2026, "
     "in line with its detection in Ceará in July 2025 after no local detection since 2015 [@delima2026]. The significant increasing "
     "trends in Rio Grande do Sul and Santa Catarina are consistent with the documented southward expansion of dengue and of "
     "*Ae. aegypti* [@r22,@r38], but they rest on 11 annual values whose last one is the partial year January–September 2026, "
     "annualized, and they did not remain significant after correction for multiple testing."))

D3 = O(60, ("(ratio 1.21)", "(ratio {n:cl.DENV.sex.ratio:d2})"))

D4 = O(61, ("(more than 97% of records lacked this information in most years)",
            "({n:fe.DENV.sero.pct:d1}% of the records lacked this information over the study period)"))

D5 = """
Chikungunya shared the seasonal profile of dengue. Its spatial structure was weaker, with a group of high-incidence
states in the Northeast ({n:lisa_names.CHIKV.HH:s}) but no local cluster surviving correction for multiple testing, which is
consistent with the recurrent, spatially discontinuous epidemic waves described for CHIKV in Brazil, in which large outbreaks occur
where susceptible populations remain after earlier waves, rather than spreading along a contiguous corridor [@r24,@r43]. The highest
per-capita incidence was observed in {u:rank_minc.CHIKV.1}, {u:rank_minc.CHIKV.2}, {u:rank_minc.CHIKV.3}, {u:rank_minc.CHIKV.4}, and
{u:rank_minc.CHIKV.5}. The highest regional annual value was reached by the {n:chik_regmax_region:s} in {n:chik_regmax_year:y}, in the
early epidemic. The increasing trends in {n:mk_all_names.CHIKV.increasing:s}, together with the decrease in
{n:mk_all_names.CHIKV.decreasing:s}, suggest that the burden has expanded beyond the initial Northeastern foci into areas with largely
susceptible populations; only the increase in
{n:mkfdr_names.CHIKV.increasing:s} was robust to correction for multiple testing, and the last annual value of these trends is the partial
year January–September 2026, annualized.
"""

D6 = O(63, ("A relatively few deaths from Chikungunya were recorded,",
            "A relatively few deaths from chikungunya were recorded ({n:cl.CHIKV.evo.Death:i} deaths among {n:cl.CHIKV.class.total:i} cases),"))

D7 = """
The Zika time series was dominated by the 2016 epidemic, followed by a sharp and sustained decline, which was significant in
{n:mk_n.ZIKV.decreasing:words} states. This pattern is consistent with the rapid accumulation of population immunity during the
2015–2016 epidemic, which serosurveys estimated to exceed 60% in some Northeastern cities and which was predicted to limit further
transmission for years [@r27,@r28]. Pre-existing dengue immunity may also have contributed to the decline of ZIKV transmission [@r29].
However, the post-2016 surveillance data must be interpreted with caution. Nearly half of the Zika notifications were discarded
({n:disc.ZIKV.disc:i} of {n:disc.ZIKV.notif:i}, {n:disc.ZIKV.share:pct0}), and the cases kept include {n:cl.ZIKV.class.Inconclusive:i}
inconclusive ones and {n:cl.ZIKV.class.Unclassified:i} not yet classified; the clinical-epidemiological criterion was recorded for
{n:cl.ZIKV.crit.Clinicepidemiological:i} cases and the laboratory criterion for {n:cl.ZIKV.crit.Laboratorial:i}, and the overlap in
clinical presentation and serological cross-reactivity with DENV makes misclassification likely in both directions [@r31,@r32]. Many
ZIKV infections are also asymptomatic or mild and therefore never notified [@r47].
"""

D8 = O(65,
    ("from approximately 30% to 40%,",
     "from {n:cl.ZIKV.malesh_min:pct0} in {n:cl.ZIKV.malesh_minyear:y} to {n:cl.ZIKV.malesh_max:pct0} in {n:cl.ZIKV.malesh_maxyear:y} "
     "(2026 being a partial year, January–September),"),
    ("The 55,501 notifications", "The {n:cl.ZIKV.preg.tri_sum:i} cases"),
    ("(1.9:1)", "({n:cl.ZIKV.sex.ratio:d1}:1)"))

D9 = """
The positive associations of temperature with dengue and Zika incidence in the pooled models are biologically plausible. Higher
temperatures shorten larval development and the extrinsic incubation period and increase biting rates up to a thermal optimum
[@r12,@r13,@r14], and the time required for vector population growth, viral amplification, and case notification is consistent with a lag
of one to two months [@r16,@r17,@r18]. In the pooled lagged model the dengue association was concentrated at a two-month lag, in line with
the two-month lag reported as the best predictor of dengue cases in one study of the temperature–dengue relationship [@liu2023]; for
chikungunya the lag-2 estimate was borderline, and for Zika the pooled estimate peaked at one month whereas the per-FU models pointed to two months. The lag window of the present analysis ends at two
months, so the strongest association may lie at longer lags. The temperature used here is the monthly mean of hourly readings averaged
over the stations of each FU, so these results cannot be compared with thresholds based on daily minimum or maximum temperature, such as
the minimum of 14.8 °C and the optimum maximum of 32–33 °C reported in a review [@liu2023]. The heterogeneity across states is also
expected: the lag-2 correlations with temperature were positive in the Southeast and negative in the Northeast. In the North and parts of the
Northeast, temperatures are already close to or above the optimum for transmission, so additional warming may have little effect or even
reduce transmission, whereas in the South and Southeast warming moves temperatures towards the optimum [@r14,@r23].
"""

D10 = """
The pooled estimates should be interpreted with caution. They depended on how overdispersion was handled (the Poisson model gave a dengue
IRR of {n:glmpois.DENV.Temp_Avg.irr:d2} against {n:glmp.DENV.Temp_Avg.irr:d2} for the NB2 model), and the Zika association was small and
imprecise (IRR {n:glmp.ZIKV.Temp_Avg.irr:d2}; lower confidence limit {n:glmp.ZIKV.Temp_Avg.lo:d2}), with {n:glms.ZIKV.Temp_Avg.nfdr:i} FU
remaining significant in the per-FU models after Benjamini–Hochberg correction. The Zika series is dominated by a single epidemic in 2016,
after which incidence collapsed largely because of population immunity, so that the pooled coefficient may reflect the timing of this
epidemic relative to temperature rather than a causal relationship. Rainfall was positively associated with dengue incidence in the pooled
model but not with chikungunya or Zika, whereas the correlation analysis and the cumulative effect in the pooled lagged model were
positive for the three diseases; the per-FU rainfall coefficients were positive for dengue ({n:glms.DENV.Rain_mm.npos:i} of
{n:glms.DENV.Rain_mm.nsig:i} significant FU) and mostly negative for Zika ({n:glms.ZIKV.Rain_mm.nneg:i} of {n:glms.ZIKV.Rain_mm.nsig:i}).
Rainfall–dengue relationships are known to be non-linear, with both excess rainfall and drought increasing risk [@r15]. Distributed lag
non-linear models with longer lag windows and explicit control of seasonality and long-term trends [@r50] would provide more robust
estimates of the exposure–lag–response relationships.
"""

D11 = O(68,
    ("which would draw attention to the Central-West and to Southern states where dengue and chikungunya are increasing.",
     "which would draw attention to Goiás and the Federal District for dengue, to the Southern states where dengue is increasing, "
     "to the Northeastern states with the highest chikungunya incidence, and to {n:mkfdr_names.CHIKV.increasing:s}, where chikungunya "
     "increased significantly even after correction for multiple testing."),
    ("Second, the consistency of the lagged temperature signal supports",
     "Second, the lagged association between temperature and incidence, which was concentrated at the longest lag tested for dengue and "
     "differed in direction between regions, supports"))

LIMITS1 = """
Our study has several limitations. First, SINAN data are subject to under-reporting, heterogeneous application of
case-confirmation criteria across FU, misclassification among the three diseases, and substantial missing information
[@r31,@r52]. Notifications are not incidence: reporting and diagnosis vary between FU and between diseases, and
surveillance capability is higher in richer and more accessible places [@lim2025], so differences between FU in {F:map}
and {F:s_lisa:A} may partly reflect who is tested and reported. Second, a case was any notification not classified as discarded
(confirmed and probable cases); the share of discarded notifications differs between diseases ({n:disc.DENV.share:pct0}, {n:disc.CHIKV.share:pct0},
and {n:disc.ZIKV.share:pct0} of the dengue, chikungunya, and Zika notifications) and the dengue files for 2022–2026 contain none, which
points to different practices of classification and publication, and published laboratory-confirmed dengue series count different
cases and are not comparable in absolute numbers or incidence [@delima2026]. Third, 2026 is a partial year (January–September) that
was annualized from the months reported; because October to December accounted for only {n:seas.DENV.q4_share:pct1},
{n:seas.CHIKV.q4_share:pct1}, and {n:seas.ZIKV.q4_share:pct1} of the dengue, chikungunya, and Zika cases of 2016–2025, this overstates the
incidence of 2026, which was nevertheless kept in the trends, the mean incidence, and the spatial statistics; the trends, in particular, rest on
a last annual value that is partial. Fourth, the national SINAN files contain no chikungunya or Zika notification for Espírito Santo in
2021, although the state reported cases of both diseases that year through its own notification system {q:esdata}[@esgov2021]{/q}; that
state-year is therefore missing, not zero.
"""

LIMITS2 = """
Fifth, climate is the monthly mean of hourly INMET readings averaged over the stations of each FU, with lags of zero to
two months and without humidity, minimum, maximum, or daily-range variables; the lag window ends where a two-month optimum
has been reported [@liu2023]. Sixth, the ecological design precludes individual-level inference, and state-level results do
not describe vector abundance or transmission within cities, where oviposition is spatially concentrated and only weakly
related to temperature and humidity [@moura2020]. Seventh, the regression models included FU and calendar-month fixed
effects but no socioeconomic, entomological, or long-term trend terms, so the climatic associations should be interpreted
as exploratory rather than causal. Eighth, we have no data on dengue vaccination (Qdenga/TAK-003 and Butantan-DV) for
2024–2026 or on viral lineages, and serotype was recorded for {n:ct.sero_typed_pct_min:pct1}–{n:ct.sero_typed_pct_max:pct1} of the
dengue cases per year in 2016–2025 and {n:ct.sero_typed_pct.2026:pct1} in the partial year January–September 2026. Finally,
{n:fe.DENV.elisa.pct2025:d0}% of the dengue NS1 results and {n:fe.DENV.igm.pct2025:d0}% of the IgM results of 2025 were ignored or blank,
compared with {n:fe.DENV.elisa.pctmin1624:d0}–{n:fe.DENV.elisa.pctmax1624:d0}% (NS1) and
{n:fe.DENV.igm.pctmin1624:d0}–{n:fe.DENV.igm.pctmax1624:d0}% (IgM) in 2016–2024, which suggests a change in how test
results were recorded.
"""

CONCL = """
In conclusion, our findings suggest that, despite sharing *Aedes* vectors and ecological determinants, dengue,
chikungunya, and Zika follow distinct spatial, temporal, and climatic dynamics that should not be addressed by uniform
surveillance strategies. Dengue showed the strongest global spatial clustering and chikungunya a weaker one centred on the Northeast,
whereas Zika showed none; temperature was positively associated with dengue incidence, with the association concentrated at a
two-month lag, and state-level correlations differed in direction between regions. The heterogeneous per-capita rankings, together with the
decline of Zika, the increase of chikungunya in {n:mkfdr_names.CHIKV.increasing:s}, and the increase of dengue in the South (not robust to
correction for multiple testing), argue for regionalized prioritization that goes beyond absolute case counts; all trends rest on a last annual
value that is a partial year (January–September 2026) annualized. Strengthening laboratory capacity, reducing missing information in
surveillance records, and integrating climatic, demographic, and entomological data at finer spatial scales remain priorities for refining
the public-health response to the arboviral burden to human health.
"""

DISCUSSION = [
    B("H1", "4 | DISCUSSION", orig=[57]),
    B("Body", D1, orig=[58]), B("Body", D2, orig=[59]), B("Body", D3, orig=[60]), B("Body", D4, orig=[61]),
    B("Body", D5, orig=[62]), B("Body", D6, orig=[63]), B("Body", D7, orig=[64]), B("Body", D8, orig=[65]),
    B("Body", D9, orig=[66]), B("Body", D10, orig=[67]), B("Body", D11, orig=[68]),
    B("Body", LIMITS1, orig=[69]), B("Body", LIMITS2),
    B("H1", "5 | CONCLUSION"),
    B("Body", CONCL, orig=[70]),
]
