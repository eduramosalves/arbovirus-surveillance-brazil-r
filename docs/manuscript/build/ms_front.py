from msbase import B, O, strip_runin

ABSTRACT = """
Dengue virus (DENV), chikungunya virus (CHIKV), and Zika virus (ZIKV) share *Aedes* vectors and climatic determinants,
yet their epidemiological trajectories in Brazil differ markedly. We compared their spatial, temporal, demographic, and
climatic profiles in a nationwide ecological study of notified cases in the 27 federative units (January 2016 to
September 2026), combined with population and station-based climate data. Dengue carried the highest
burden and peaked in 2024 ({n:cases.DENV.y2024:mil2} million cases; {n:ann.DENV.BR.2024:d0} per 100,000);
only dengue showed significant global spatial autocorrelation (Moran's I = {n:moran.DENV.I:d3}; p {n:moran.DENV.p:pv}), with
high–high clusters in the Central-West, Southeast, and Paraná. Increasing trends were significant for dengue in two
southern states and for chikungunya in three states of the Central-West and Southeast, and Zika declined in six states; none
remained significant after false discovery rate correction. In pooled negative binomial models, temperature was positively
associated with dengue (incidence rate ratio [IRR] {n:glmp.DENV.Temp_Avg.irr:d2} per °C; 95% CI
{n:glmp.DENV.Temp_Avg.lo:d2}–{n:glmp.DENV.Temp_Avg.hi:d2}) and Zika ({n:glmp.ZIKV.Temp_Avg.irr:d2};
{n:glmp.ZIKV.Temp_Avg.lo:d2}–{n:glmp.ZIKV.Temp_Avg.hi:d2}) but not significantly with chikungunya
({n:glmp.CHIKV.Temp_Avg.irr:d2}; {n:glmp.CHIKV.Temp_Avg.lo:d2}–{n:glmp.CHIKV.Temp_Avg.hi:d2}), and rainfall was positively
associated with all three. State-level correlations with temperature were strongest at a two-month lag and differed in
sign between regions. These patterns support regionalized, climate-informed surveillance based on
population-adjusted burden.
"""

FRONT = [
    B("Title", O(0, ("2016–2025", "2016–2026")).replace("**", ""), orig=[0]),
    B("RunningTitle", "Running title: Dengue, chikungunya, and Zika in Brazil, 2016–2026"),
    B("Authors", O(2), orig=[2]),
    B("Affil", O(4), orig=[4]),
    B("Affil", O(5), orig=[5]),
    B("Affil", O(6), orig=[6]),
    B("Affil", O(7), orig=[7]),
    B("Affil", O(8), orig=[8]),
    B("Corr", O(10), orig=[10]),
    B("Corr", "ORCID iDs: {hl}to be provided by each author{/hl}"),
    B("Corr", "Funding information: {hl}to be provided by the authors{/hl}"),
    B("Corr", "Word counts: abstract, {calc:abstract_words}; main text, {calc:main_words}. References: {calc:n_refs}. "
              "Figures: 8 main and 7 supplementary. Tables: none."),
    B("Label", "ABSTRACT"),
    B("Abstract", ABSTRACT, orig=[19]),
    B("Keywords", "**Keywords:** dengue; chikungunya; Zika virus; climate; spatial analysis", orig=[26]),
]

INTRO = [
    B("H1", "1 | INTRODUCTION"),
    B("Body", O(33), orig=[33]),
    B("Body", O(34), orig=[34]),
    B("Body", O(35), orig=[35]),
    B("Body", O(36), orig=[36]),
    B("Body", O(37), orig=[37]),
    B("Body", O(38), orig=[38]),
    B("Body", O(39, ("in Brazil during 2016–2025,", "in Brazil from January 2016 to September 2026,")), orig=[39]),
]
