from msbase import B, O, strip_runin

ASSERT = [
    ("N('mk_n.DENV.increasing') == 2 and N('mk_n.CHIKV.increasing') == 3", "abstract: two dengue and three chikungunya increasing trends"),
    ("N('mkfdr_n.CHIKV.increasing') == 1", "abstract: one chikungunya trend robust to multiple testing"),
    ("N('lisa_n.DENV.HH') == 8", "abstract: dengue high-high units"),
]

ABSTRACT = """
Dengue virus (DENV), chikungunya virus (CHIKV), and Zika virus (ZIKV) share *Aedes* vectors and climatic determinants, yet their
epidemiological trajectories in Brazil differ markedly. We compared their spatial, temporal, and climatic profiles in a nationwide
ecological study of confirmed and probable cases (discarded notifications excluded) in the 27 federative units, from January 2016
to September 2026, with population and station-based climate data; 2026 is a partial year (January–September), annualized in
the annual analyses. Dengue carried the highest burden and peaked in 2024 ({n:cases.DENV.y2024:mil2} million cases;
{n:ann.DENV.BR.2024:d0} per 100,000). Global spatial autocorrelation was significant for dengue (Moran's I = {n:moran.DENV.I:d3})
and, more weakly, chikungunya ({n:moran.CHIKV.I:d3}), but not Zika. Dengue increased in two southern states and chikungunya in
three states of the Central-West and Southeast (one robust to multiple testing), and Zika declined in {n:mk_n.ZIKV.decreasing:words}
states. In pooled negative binomial models, temperature was positively associated with dengue (incidence rate ratio [IRR]
{n:glmp.DENV.Temp_Avg.irr:d2} per °C; 95% CI {n:glmp.DENV.Temp_Avg.lo:d2}–{n:glmp.DENV.Temp_Avg.hi:d2}) and Zika
({n:glmp.ZIKV.Temp_Avg.irr:d2}; {n:glmp.ZIKV.Temp_Avg.lo:d2}–{n:glmp.ZIKV.Temp_Avg.hi:d2}) but not chikungunya, and the dengue
association was concentrated at a two-month lag. These patterns support regionalized, climate-informed surveillance based on
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
    B("Body", O(39, ("in Brazil during 2016–2025,",
                     "in Brazil from January 2016 to September 2026 (2026 being a partial year, January–September),")), orig=[39]),
]
