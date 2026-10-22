from msbase import B, O

D1 = O(58,
    ("was the only arbovirus with significant spatial clustering", "was the only arbovirus with significant global spatial clustering"),
    ("the Federal District and Goiás leading in incidence", "Goiás and the Federal District leading in incidence"),
    ("would underweight smaller populations that experience the highest transmission intensity.",
     "would underweight smaller populations that experience the highest transmission intensity. Only Goiás and Minas Gerais "
     "(high–high) and Rio de Janeiro (low–high) remained significant local clusters after correction for multiple "
     "testing, so the local cluster map should be read as exploratory."))

D2 = O(59,
    ("The significant increasing trends in Rio Grande do Sul, Santa Catarina, and São Paulo are consistent with the documented "
     "southward expansion of dengue and of *Ae. aegypti* [@r22,@r38].",
     "In the national SINAN records, DENV-3 rose from {n:ct.sero_share.DENV3.2024:pct1} of typed records in 2024 to "
     "{n:ct.sero_share.DENV3.2025:pct1} in 2025 and {n:ct.sero_share.DENV3.2026:pct1} in January–September 2026, in line with "
     "its detection in Ceará in July 2025 after no local detection since 2015 [@delima2026]. The significant increasing trends in "
     "Rio Grande do Sul and Santa Catarina are consistent with the documented southward expansion of dengue and of "
     "*Ae. aegypti* [@r22,@r38], but they rest on 11 annual values (2026 annualized from nine months) and did not remain "
     "significant after correction for multiple testing."))

D3 = O(60, ("(ratio 1.21)", "(ratio {n:cl.DENV.sex.ratio:d2})"))

D4 = O(61, ("(more than 97% of records lacked this information in most years)",
            "(more than 97% of records lacked this information in 2016–2025)"))

D5 = O(62,
    ("The highest per-capita incidence was observed in Mato Grosso, Mato Grosso do Sul, Ceará, Tocantins, and Rio Grande do Norte, "
     "and the significant increasing trends in Santa Catarina, Rio Grande do Sul, and Mato Grosso do Sul, together with the steep "
     "rise in the Central-West in 2025, suggest that chikungunya is expanding beyond its initial Northeastern foci into areas "
     "with largely susceptible populations.",
     "The highest per-capita incidence was observed in {u:rank_minc.CHIKV.1}, {u:rank_minc.CHIKV.2}, {u:rank_minc.CHIKV.3}, "
     "{u:rank_minc.CHIKV.4}, and {u:rank_minc.CHIKV.5}, and the increasing trends in {n:mk_names.CHIKV.increasing:s}, "
     "together with the steep rise in the Central-West in 2025, suggest that chikungunya may be expanding beyond its initial "
     "Northeastern foci into areas with largely susceptible populations, although none of these trends remained significant "
     "after correction for multiple testing."))

D6 = O(63)

D7 = O(64, ("More notifications were discarded than confirmed,",
            "More notifications were discarded than confirmed ({n:cl.ZIKV.disc:i} versus {n:cl.ZIKV.conf:i}),"))

D8 = O(65,
    ("from approximately 30% to 40%,",
     "from {n:cl.ZIKV.malesh_min:pct0} in {n:cl.ZIKV.malesh_minyear:y} to {n:cl.ZIKV.malesh_max:pct0} in {n:cl.ZIKV.malesh_maxyear:y},"),
    ("The 55,501 notifications", "The {n:cl.ZIKV.preg.tri_sum:i} notifications"))

D9 = """
The positive associations of temperature with dengue and Zika incidence in the pooled models, and the larger
correlations at a two-month lag, are biologically plausible. Higher temperatures shorten larval development and the
extrinsic incubation period and increase biting rates up to a thermal optimum [@r12,@r13,@r14], and the time required
for vector population growth, viral amplification, and case notification is consistent with a lag of one to two months
[@r16,@r17,@r18]; a two-month lag has also been reported as the best predictor of dengue cases in one study of the
temperature–dengue relationship [@liu2023]. The lag window of the present analysis ends at two months, so the
strongest association may lie at longer lags. The supplementary DLNM placed the dengue temperature optimum at
{n:dlnm.DENV.opt:d1} °C, within the 26–29 °C range estimated by mechanistic models [@r14]; this value is not
comparable with thresholds based on daily minimum or maximum temperature, such as the minimum of 14.8 °C and the
optimum maximum of 32–33 °C reported in a review [@liu2023], because the temperature used here is the monthly mean of
hourly readings averaged over the stations of each FU. The heterogeneity across states is also expected: the lag-2
correlations with temperature were positive in the Southeast, South, and Central-West and negative in the Northeast. In
the North and parts of the Northeast, temperatures are already close to or above the optimum for transmission, so
additional warming may have little effect or even reduce transmission, whereas in the South and Southeast warming
moves temperatures towards the optimum [@r14,@r23].
"""

D10 = """
The pooled estimates should be interpreted with caution. They depended on how overdispersion was handled (the Poisson
model gave a dengue IRR of {n:glmpois.DENV.Temp_Avg.irr:d2} against {n:glmp.DENV.Temp_Avg.irr:d2} for the NB2 model), and
the Zika association was small and imprecise (IRR {n:glmp.ZIKV.Temp_Avg.irr:d2}; lower confidence limit
{n:glmp.ZIKV.Temp_Avg.lo:d2}), with {n:glms.ZIKV.Temp_Avg.nfdr:nz} FU remaining significant in the per-FU models after
Benjamini–Hochberg correction. The Zika series is dominated by a single epidemic in early 2016, after which incidence
collapsed largely because of population immunity, so that the pooled coefficient may reflect the timing of this epidemic
relative to temperature rather than a causal relationship. Rainfall was positively associated with incidence in the pooled
models and in the correlation analysis, whereas the per-FU rainfall coefficients were positive for dengue
({n:glms.DENV.Rain_mm.npos:i} of {n:glms.DENV.Rain_mm.nsig:i} significant FU) and negative for Zika
({n:glms.ZIKV.Rain_mm.nneg:i} of {n:glms.ZIKV.Rain_mm.nsig:i}); rainfall–dengue relationships are known to be non-linear,
with both excess rainfall and drought increasing risk [@r15]. The supplementary DLNM is a first step towards modelling
these relationships [@r50], but it is limited to lags of 0–2 months and to a linear lag–response. Distributed lag
non-linear models with longer lag windows and explicit control of seasonality and long-term trends would provide more
robust estimates of the exposure–lag–response relationships.
"""

D11 = O(68,
    ("which would draw attention to the Central-West and to Southern states where dengue and chikungunya are increasing.",
     "which would draw attention to Goás and the Federal District, to the Southern states where dengue is increasing, and to the "
     "Central-West and Southeast where chikungunya is increasing."),
    ("Second, the consistency of the lagged temperature signal supports",
     "Second, the lagged association between temperature and incidence, which was strongest at the longest lag tested and "
     "differed in direction between regions, supports"))

LIMITS1 = """
Our study has several limitations. First, SINAN data are subject to under-reporting, heterogeneous application of
case-confirmation criteria across FU, misclassification among the three diseases, and substantial missing information
[@r31,@r52]. Notifications are not incidence: reporting and diagnosis vary between FU and between diseases, and
surveillance capability is higher in richer and more accessible places [@lim2025], so differences between FU in Figure 6
and Figure S2A may partly reflect who is tested and reported. Second, the case definition differs by disease (dengue,
probable cases; chikungunya and Zika, all notifications, including discarded ones), and cases are assigned to the FU of
notification; published laboratory-confirmed dengue series count different cases and are not comparable in absolute
numbers or incidence [@delima2026]. Third, 2026 covers January to September and was annualized from the months reported;
because October to December accounted for only {n:seas.DENV.q4_share:pct1}, {n:seas.CHIKV.q4_share:pct1}, and
{n:seas.ZIKV.q4_share:pct1} of the dengue, chikungunya, and Zika cases of 2016–2025, this overstates the incidence of 2026,
which enters the trends, the mean incidence, and the spatial statistics. Fourth, the national SINAN files contain no
chikungunya or Zika record for Espírito Santo in 2021, although the state reported cases of both diseases that year through its
own notification system {q:esdata}[@esgov2021]{/q}; that state-year is therefore missing, not zero.
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
dengue notifications per year in 2016–2025 and {n:ct.sero_typed_pct.2026:pct1} in 2026. Finally, the clinical and demographic
figures end in 2025, and in 2025 {n:fe.DENV.elisa.pct2025:d0}% of the dengue NS1 and IgM results were ignored or blank,
compared with {n:fe.DENV.elisa.pctmin1624:d0}–{n:fe.DENV.elisa.pctmax1624:d0}% (NS1) and
{n:fe.DENV.igm.pctmin1624:d0}–{n:fe.DENV.igm.pctmax1624:d0}% (IgM) in 2016–2024, which suggests a change in how test
results were recorded.
"""

CONCL = """
In conclusion, our findings suggest that, despite sharing *Aedes* vectors and ecological determinants, dengue,
chikungunya, and Zika follow distinct spatial, temporal, and climatic dynamics that should not be addressed by uniform
surveillance strategies. Dengue alone showed significant global spatial clustering, and temperature was positively
associated with dengue incidence, with state-level correlations strongest at the longest lag tested and opposite in
direction between regions. The heterogeneous per-capita rankings, together with the increasing trends of dengue in the
South and of chikungunya in the Central-West and Southeast (which were not robust to correction for multiple testing),
argue for regionalized prioritization that goes beyond absolute case counts. Strengthening laboratory capacity, reducing
missing information in surveillance records, and integrating climatic, demographic, and entomological data at finer
spatial scales remain priorities for refining the public-health response to the arboviral burden to human health.
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
