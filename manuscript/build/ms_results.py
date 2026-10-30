from msbase import B, O, strip_runin

# Statements below that the data must support; build.py evaluates them against numbers.csv and stops if one fails.
# N(key) returns the number (or text) computed from the repository outputs.
ASSERT = [
    ("all(N('glml.%s.Temp_Lag2.nsig' % d) > max(N('glml.%s.Temp_Avg.nsig' % d), N('glml.%s.Temp_Lag1.nsig' % d)) for d in ('DENV', 'CHIKV', 'ZIKV'))", "per-FU lagged models: lag 2 has the most significant FU for the three diseases"),
    ("N('natpeak_year.DENV') == 2024", "dengue incidence peaks in 2024"),
    ("N('natpeak_year.CHIKV') == 2024 and N('natsecond_year.CHIKV') == 2016", "chikungunya: 2024 first, 2016 second"),
    ("N('moran.DENV.p') < 0.05 and N('moran.CHIKV.p') < 0.05 and N('moran.ZIKV.p') >= 0.05", "global Moran: dengue and chikungunya significant, Zika not"),
    ("N('lisafdr_n.CHIKV.HH') == 0 and N('lisafdr_n.ZIKV.HH') == 0", "no chikungunya or Zika local cluster survives FDR"),
    ("N('mk_n.DENV.increasing') == 2 and N('mk_n.DENV.decreasing') == 0", "dengue: two increasing trends, none decreasing"),
    ("N('mk_n.CHIKV.increasing') == 3 and N('mk_n.CHIKV.decreasing') == 1", "chikungunya: three increasing, one decreasing"),
    ("N('mk_n.ZIKV.decreasing') >= 5 and N('mk_n.ZIKV.increasing') == 0", "Zika: decreasing trends only"),
    ("N('mkfdr_n.DENV.increasing') == 0 and N('mkfdr_n.DENV.decreasing') == 0", "no dengue trend survives FDR"),
    ("N('mkfdr_n.CHIKV.increasing') == 1 and N('mkfdr_n.CHIKV.decreasing') == 0", "one chikungunya trend survives FDR"),
    ("all(N('sp.%s.Temp.0.mean' % d) < 0 < N('sp.%s.Temp.2.mean' % d) for d in ('DENV', 'CHIKV'))", "temperature rho negative at lag 0 and positive at lag 2 (dengue, chikungunya)"),
    ("N('mkr.CHIKV.increasing.1.uf') == 'MS' and N('mk.CHIKV.MS.q') < 0.05", "the chikungunya trend that survives FDR is Mato Grosso do Sul"),
    ("N('lisa_n.DENV.HH') == 8 and N('lisa_n.CHIKV.HH') >= 1", "dengue has eight high-high units; chikungunya has high-high units"),
    ("set(N('lisa_uf.CHIKV.HH').split(',')) <= {'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA'}", "chikungunya high-high units are all in the Northeast"),
    ("all(N('glmpl.%s.Rain.maxlag' % d) == 2 for d in ('DENV', 'CHIKV', 'ZIKV'))", "largest single-lag rainfall coefficient at lag 2"),
    ("all(N('sp.%s.Rain.2.nneg' % d) == 0 and N('sp.%s.Rain.0.mean' % d) > 0 for d in ('DENV', 'CHIKV', 'ZIKV'))", "rainfall correlations positive"),
    ("all(N('sp.%s.Temp.2.reg.SE' % d) > 0 and N('sp.%s.Temp.2.reg.NE' % d) < 0 for d in ('DENV', 'CHIKV', 'ZIKV'))", "lag-2 temperature rho positive in the Southeast and negative in the Northeast"),
    ("N('glmp.DENV.Temp_Avg.p') < 0.05 and N('glmp.ZIKV.Temp_Avg.p') < 0.05 and N('glmp.CHIKV.Temp_Avg.p') >= 0.05", "pooled temperature: dengue and Zika significant, chikungunya not"),
    ("N('glmp.DENV.Rain_mm.p') < 0.05 and N('glmp.CHIKV.Rain_mm.p') >= 0.05 and N('glmp.ZIKV.Rain_mm.p') >= 0.05", "pooled rainfall: dengue significant, chikungunya and Zika not"),
    ("N('glmpl.DENV.Temp.maxlag') == 2 and N('glmpl.CHIKV.Temp.maxlag') == 2 and N('glmpl.ZIKV.Temp.maxlag') == 1", "pooled lagged model: largest temperature coefficient at lag 2 (dengue, chikungunya) and lag 1 (Zika)"),
    ("N('glmpl.DENV.Temp_Lag2.p') < 0.001 and 0.05 <= N('glmpl.CHIKV.Temp_Cum0_2.p') < 0.1 and N('glmpl.ZIKV.Temp_Cum0_2.p') >= 0.05", "pooled lagged: dengue lag 2 clear, chikungunya cumulative borderline, Zika cumulative not significant"),
    ("0.05 <= N('glmpl.CHIKV.Temp_Lag2.p') < 0.1 and N('glmpl.ZIKV.Temp_Lag1.p') < 0.01", "chikungunya lag-2 borderline; Zika lag-1 clear"),
    ("all(N('glmpl.%s.Rain_Cum0_2.p' % d) < 0.05 for d in ('DENV', 'CHIKV', 'ZIKV'))", "cumulative rainfall IRR significant in the pooled lagged model for the three diseases"),
]

# ---------------------------------------------------------------- 3.1 distribution
ANNUAL = """
Between January 2016 and September 2026, SINAN recorded {n:cases.DENV.all:i} dengue cases, {n:cases.CHIKV.all:i}
chikungunya cases, and {n:cases.ZIKV.all:i} Zika cases in the 27 FU, counting confirmed and probable cases and
excluding notifications classified as discarded; 2026 is a partial year (January–September). Dengue incidence peaked in
2024, with {n:cases.DENV.y2024:i} cases ({n:ann.DENV.BR.2024:d0} per 100,000 inhabitants),
{n:natpeak_ratio_second.DENV:d1} times the incidence of 2023 ({n:ann.DENV.BR.2023:d0} per 100,000); the annualized incidence of the
partial year 2026 (January–September, annualized ×12/9) was {n:ann.DENV.BR.2026:d0} per 100,000 ({F:incid:A}).
{c9}Chikungunya incidence was also highest in 2024 ({n:ann.CHIKV.BR.2024:d1} per 100,000), followed by 2016
({n:ann.CHIKV.BR.2016:d1}). At regional level, the highest annual value was reached by the {n:chik_regmax_region:s} in
{n:chik_regmax_year:y} ({n:chik_regmax_val:d1} per 100,000).{/c9} Annual maps of incidence by FU are shown in {F:s_annual}.
"""

DISTRIBUTION = """
The absolute burden of dengue was concentrated in the Southeast, where {u:rank_cases.DENV.1:cap} recorded the largest
number of cases ({n:rank_cases_val.DENV.1:i}), followed by {u:rank_cases.DENV.2} ({n:rank_cases_val.DENV.2:i}). In contrast, the North
region reported substantially lower figures, ranging from {n:regmin.DENV.N:i} in {u:regmin_uf.DENV.N} to
{n:regmax.DENV.N:i} in {u:regmax_uf.DENV.N}, and the Northeast showed marked internal variation, from
{n:regmin.DENV.NE:i} in {u:regmin_uf.DENV.NE} to {n:regmax.DENV.NE:i} in {u:regmax_uf.DENV.NE}. Taken together, this
spatial gradient mirrors the demographic hierarchy of the country. It is interesting to note that the ranking changed
substantially when the population size was considered ({F:map}; mean of the annual incidence of 2016–2026, in which the value of
2026 is annualized from the partial year January–September). The highest mean annual incidence was observed in
{u:rank_minc.DENV.1} ({n:rank_minc_val.DENV.1:d1} per 100,000 inhabitants), followed by {u:rank_minc.DENV.2}
({n:rank_minc_val.DENV.2:d1}) and {u:rank_minc.DENV.3} ({n:rank_minc_val.DENV.3:d1}). The absolute burden of
chikungunya was concentrated in a few states of the Southeast and Northeast regions, where {u:rank_cases.CHIKV.1}
recorded the largest number of cases ({n:rank_cases_val.CHIKV.1:i}), followed by {u:rank_cases.CHIKV.2}
({n:rank_cases_val.CHIKV.2:i}), {u:rank_cases.CHIKV.3} ({n:rank_cases_val.CHIKV.3:i}), {u:rank_cases.CHIKV.4}
({n:rank_cases_val.CHIKV.4:i}), and {u:rank_cases.CHIKV.5} ({n:rank_cases_val.CHIKV.5:i}). On a per-capita basis, the
highest mean annual incidence was observed in {u:rank_minc.CHIKV.1} ({n:rank_minc_val.CHIKV.1:d1}), followed by
{u:rank_minc.CHIKV.2} ({n:rank_minc_val.CHIKV.2:d1}) and {u:rank_minc.CHIKV.3} ({n:rank_minc_val.CHIKV.3:d1}), whereas
{u:rank_cases.CHIKV.1} (which had the largest absolute number of cases) ranked {n:rank_of_topcases.CHIKV.1:ord}. The
absolute burden of Zika was highest in {u:rank_cases.ZIKV.1} ({n:rank_cases_val.ZIKV.1:i}) and
{u:rank_cases.ZIKV.2} ({n:rank_cases_val.ZIKV.2:i}), with counts in the South region ranging from {n:regmin.ZIKV.S:i} in
{u:regmin_uf.ZIKV.S} to {n:regmax.ZIKV.S:i} in {u:regmax_uf.ZIKV.S}. On a per-capita basis, the highest mean annual
incidence was observed in {u:rank_minc.ZIKV.1} ({n:rank_minc_val.ZIKV.1:d1}), {u:rank_minc.ZIKV.2}
({n:rank_minc_val.ZIKV.2:d1}), and {u:rank_minc.ZIKV.3} ({n:rank_minc_val.ZIKV.3:d1}); {u:rank_cases.ZIKV.1} and
{u:rank_cases.ZIKV.2}, the states with the largest absolute numbers, ranked {n:rank_of_topcases.ZIKV.1:ord} and
{n:rank_of_topcases.ZIKV.2:ord}, respectively ({F:map}).
"""

SPATIAL_AC = """
Spatial autocorrelation analysis showed significant global spatial structure for dengue
({c4}Moran’s I = {n:moran.DENV.I:d3}, p {n:moran.DENV.p:pv}{/c4}) and, more weakly, for chikungunya
(I = {n:moran.CHIKV.I:d3}, p {n:moran.CHIKV.p:pv}), but not for Zika (I = {n:moran.ZIKV.I:d3}, p {n:moran.ZIKV.p:pv};
{c5}{F:moran}{/c5}); these statistics use the mean annual incidence of 2016–2026, whose last year, 2026, is a partial year
(January–September) annualized ×12/9. For dengue, high–high clusters were observed across the Central-West and
Southeast and in Paraná ({n:lisa_names.DENV.HH:s}), and low–low clusters in {n:lisa_names.DENV.LL:s};
{u:lisa_uf.DENV.HL:cap} appeared as a high–low outlier and {u:lisa_uf.DENV.LH} as a low–high outlier
({c6}{F:s_lisa:A}{/c6}). For chikungunya, the high–high cluster was located in the Northeast ({n:lisa_names.CHIKV.HH:s}) and the
low–low units were {n:lisa_names.CHIKV.LL:s}. After Benjamini–Hochberg correction, only {n:lisafdr_names.DENV.HH:s}
(high–high) and {n:lisafdr_names.DENV.LH:s} (low–high) remained significant, for dengue; no local cluster of
chikungunya or Zika remained significant.
"""

# ---------------------------------------------------------------- 3.2 trends
TRENDS = """
Trends are based on 11 annual values of 2016–2026, the last of which (2026) is a partial year (January–September)
annualized ×12/9 and therefore overstated (see Limitations). Statistically significant increasing trends in dengue
incidence were observed in {u:mkr.DENV.increasing.1.uf:cap} (τ = {n:mkr.DENV.increasing.1.tau:d3}; Sen’s slope ≈
{n:mkr.DENV.increasing.1.slope:d0} cases per 100,000 per year) and {u:mkr.DENV.increasing.2.uf}
(τ = {n:mkr.DENV.increasing.2.tau:d3}; ≈{n:mkr.DENV.increasing.2.slope:d0}) ({c7}{F:trend}{/c7}). Three states displayed
statistically significant increasing trends for chikungunya: {u:mkr.CHIKV.increasing.1.uf:cap}
(τ = {n:mkr.CHIKV.increasing.1.tau:d3}; ≈{n:mkr.CHIKV.increasing.1.slope:d0} cases per 100,000 per year, the largest
Sen’s slope), {u:mkr.CHIKV.increasing.2.uf} (τ = {n:mkr.CHIKV.increasing.2.tau:d3}; ≈{n:mkr.CHIKV.increasing.2.slope:d0}), and
{u:mkr.CHIKV.increasing.3.uf} (τ = {n:mkr.CHIKV.increasing.3.tau:d3}; ≈{n:mkr.CHIKV.increasing.3.slope:d0}), and the
trend was decreasing in {u:mkr.CHIKV.decreasing.1.uf} (τ = {n:mkr.CHIKV.decreasing.1.tau:d3}). Zika was the only
arbovirus with a predominance of decreasing trends: they were significant in {n:mk_n.ZIKV.decreasing:words} states
(τ from {n:mk_taumin.ZIKV.decreasing:d3} to {n:mk_taumax.ZIKV.decreasing:d3}) and no state showed an increase
({c8}Figures {f:trend} and {f:s_lisa:B}{/c8}). After Benjamini–Hochberg correction, the increase of chikungunya in
{n:mkfdr_names.CHIKV.increasing:s} (q = {n:mk.CHIKV.MS.q:d3}) and the decrease of Zika in {n:mkfdr_n.ZIKV.decreasing:words} states
remained significant, whereas none of the dengue trends did (smallest q = {n:mk_minq.DENV:d3}).
"""

# ---------------------------------------------------------------- 3.3 seasonality
SEASON = """
Summed across the ten complete study years (2016–2025), dengue cases rose from {n:seas.DENV.m1:i} in January to
{n:seas.DENV.m2:i} in February, peaked in March–April (mean of {n:seas.DENV.marapr_mean:i} per month), and fell to
{n:seas.DENV.m6:i} in June; from July to December, monthly totals ranged from {n:seas.DENV.h2_min:i} to
{n:seas.DENV.h2_max:i}. Interannual variability was dominated by the 2024 epidemic, an extreme outlier in the series
({F:incid:A}). Chikungunya also showed a seasonal pattern, with monthly totals rising from {n:seas.CHIKV.m1:i} in January
to a peak of {n:seas.CHIKV.m5:i} in May and falling to {n:seas.CHIKV.m6:i} in June, and ranging from
{n:seas.CHIKV.h2_min:i} to {n:seas.CHIKV.h2_max:i} from July to December. The seasonal profile of ZIKV was similar to
those of dengue and chikungunya: monthly totals rose from {n:seas.ZIKV.m1:i} in January to a peak of
{n:seas.ZIKV.m3:i} in March, fell to {n:seas.ZIKV.m5:i} in May and {n:seas.ZIKV.m6:i} in June, and ranged from
{n:seas.ZIKV.h2_min:i} to {n:seas.ZIKV.h2_max:i} per month in the second half of the year. The annual series of ZIKV was
dominated by the 2016 epidemic, with {n:cases.ZIKV.y2016:i} cases nationally ({n:ann.ZIKV.BR.2016:d0} per
100,000), between {n:zika_ratio_min:d1} and {n:zika_ratio_max:d1} times the incidence of each later complete year.
"""

# ---------------------------------------------------------------- 3.4 climate correlations
CLIM1 = """
Correlations between monthly incidence and temperature depended on the lag ({c11}{F:corr}{/c11}). For dengue, the
mean Spearman correlation across the 27 FU was negative at lag 0 (ρ = {n:sp.DENV.Temp.0.mean:d3}), close to zero at
lag 1 ({n:sp.DENV.Temp.1.mean:d3}), and positive at lag 2 ({n:sp.DENV.Temp.2.mean:d3}); at lag 2, {n:sp.DENV.Temp.2.nsig:i}
of 27 FU ({n:sp.DENV.Temp.2.prop:pct0}) had p < 0.05, of which {n:sp.DENV.Temp.2.npos:i} were positive and
{n:sp.DENV.Temp.2.nneg:i} negative. The strongest lag-2 correlations were observed for {u:sp.DENV.Temp.2.top1.uf}
(ρ = {n:sp.DENV.Temp.2.top1.rho:d3}), {u:sp.DENV.Temp.2.top2.uf} ({n:sp.DENV.Temp.2.top2.rho:d3}),
{u:sp.DENV.Temp.2.top3.uf} ({n:sp.DENV.Temp.2.top3.rho:d3}), and {u:sp.DENV.Temp.2.top4.uf}
({n:sp.DENV.Temp.2.top4.rho:d3}). Chikungunya showed the same pattern (mean ρ = {n:sp.CHIKV.Temp.0.mean:d3},
{n:sp.CHIKV.Temp.1.mean:d3}, and {n:sp.CHIKV.Temp.2.mean:d3} at lags 0, 1, and 2; {n:sp.CHIKV.Temp.2.nsig:i} FU significant at
lag 2), with the strongest lag-2 correlations in {u:sp.CHIKV.Temp.2.top1.uf} (ρ = {n:sp.CHIKV.Temp.2.top1.rho:d3})
and {u:sp.CHIKV.Temp.2.top2.uf} ({n:sp.CHIKV.Temp.2.top2.rho:d3}). For Zika, the mean correlation with temperature was weak
(ρ = {n:sp.ZIKV.Temp.0.mean:d3}, {n:sp.ZIKV.Temp.1.mean:d3}, and {n:sp.ZIKV.Temp.2.mean:d3} at lags 0, 1, and 2), but some
states showed moderate positive correlations at lag 2, particularly {u:sp.ZIKV.Temp.2.top1.uf} (ρ = {n:sp.ZIKV.Temp.2.top1.rho:d3})
and {u:sp.ZIKV.Temp.2.top2.uf} ({n:sp.ZIKV.Temp.2.top2.rho:d3}). The national mean concealed a regional contrast: for all three
diseases, the mean lag-2 correlation with temperature was positive in the Southeast (dengue, {n:sp.DENV.Temp.2.reg.SE:d3};
chikungunya, {n:sp.CHIKV.Temp.2.reg.SE:d3}; Zika, {n:sp.ZIKV.Temp.2.reg.SE:d3}) and negative in the Northeast (dengue,
{n:sp.DENV.Temp.2.reg.NE:d3}; chikungunya, {n:sp.CHIKV.Temp.2.reg.NE:d3}; Zika, {n:sp.ZIKV.Temp.2.reg.NE:d3}).
"""

CLIM2 = """
Rainfall was positively correlated with incidence for all three arboviruses, and the correlation increased with lag
(mean ρ at lags 0, 1, and 2: dengue, {n:sp.DENV.Rain.0.mean:d3}, {n:sp.DENV.Rain.1.mean:d3}, and
{n:sp.DENV.Rain.2.mean:d3}; chikungunya, {n:sp.CHIKV.Rain.0.mean:d3}, {n:sp.CHIKV.Rain.1.mean:d3}, and
{n:sp.CHIKV.Rain.2.mean:d3}; Zika, {n:sp.ZIKV.Rain.0.mean:d3}, {n:sp.ZIKV.Rain.1.mean:d3}, and
{n:sp.ZIKV.Rain.2.mean:d3}). At lag 2, {n:sp.DENV.Rain.2.prop:pct0}, {n:sp.CHIKV.Rain.2.prop:pct0}, and
{n:sp.ZIKV.Rain.2.prop:pct0} of the FU had p < 0.05 for dengue, chikungunya, and Zika, respectively, and all significant
correlations were positive. Lag 2 was the lag with the largest absolute correlation with temperature in
{n:sp_bestlag.DENV.Temp.2:i}, {n:sp_bestlag.CHIKV.Temp.2:i}, and {n:sp_bestlag.ZIKV.Temp.2:i} of the 27 FU, and with
rainfall in {n:sp_bestlag.DENV.Rain.2:i}, {n:sp_bestlag.CHIKV.Rain.2:i}, and {n:sp_bestlag.ZIKV.Rain.2:i} FU
(dengue, chikungunya, and Zika); lags longer than two months were not examined.
"""

# ---------------------------------------------------------------- 3.5 demographic / clinical
DEMO = """
The demographic and clinical results refer to the cases of 2016–2026 defined in the Methods, with 2026 a partial year
(January–September). Dengue cases were concentrated among adults aged 20–59 years ({n:cl.DENV.age.20_59:i} of
{n:cl.DENV.age.known:i} cases with known age, {n:cl.DENV.age.20_59_share:pct1}), with lower frequencies among children and older
adults ({F:demo:A}). Most cases were recorded in women ({n:cl.DENV.sex.F:i}) when compared to men ({n:cl.DENV.sex.M:i}),
corresponding to a female-to-male ratio of {n:cl.DENV.sex.ratio:d2} ({F:demo:B}). The most affected age groups for chikungunya
were 20–39 years ({n:cl.CHIKV.age.20_39:i} cases) and 40–59 years ({n:cl.CHIKV.age.40_59:i} cases) ({F:demo:A}). Women
accounted for {n:cl.CHIKV.sex.F:i} cases, compared with {c12}{n:cl.CHIKV.sex.M:i}{/c12} cases in men, a ratio of
{n:cl.CHIKV.sex.ratio:d1}:1 ({F:demo:B}). For Zika, the most affected age groups were also 20–39 years
({n:cl.ZIKV.age.20_39:i} cases) and 40–59 years ({n:cl.ZIKV.age.40_59:i} cases), with progressively fewer cases among
adolescents, children, and older adults ({F:demo:A}). Women accounted for {n:cl.ZIKV.sex.F:i} cases when compared to men
({n:cl.ZIKV.sex.M:i}), a ratio of {n:cl.ZIKV.sex.ratio:d1}:1. A total of {n:cl.ZIKV.preg.tri_sum:i} cases occurred in pregnant
women, distributed across the first ({n:cl.ZIKV.preg.1Trimester:i}), second ({n:cl.ZIKV.preg.2Trimester:i}), and third
({n:cl.ZIKV.preg.3Trimester:i}) trimesters.
"""

CLIN = """
{c13}Hospitalization status was recorded for {n:cl.DENV.hosp.known:i} of the {n:cl.DENV.hosp.total:i} dengue cases:
{n:cl.DENV.hosp.Positive:i} patients ({n:cl.DENV.hosp.share_known:pct1} of those with known status) were admitted for
inpatient care and {n:cl.DENV.hosp.Negative:i} were not, whereas the information was ignored or blank in
{n:cl.DENV.hosp.IgnBlank:i} cases ({n:fe.DENV.hosp.pct:d1}%) ({F:dengue:C}).{/c13} {q:code0}Serotype was recorded for only
{n:cl.DENV.sero.typed:i} cases ({n:cl.DENV.sero.typed_share:pct1}){/q}: {c14}DENV-1 was detected in
{n:cl.DENV.sero.DENV1:i} cases, followed by DENV-2 ({n:cl.DENV.sero.DENV2:i}), DENV-3 ({n:cl.DENV.sero.DENV3:i}), and DENV-4
({n:cl.DENV.sero.DENV4:i}){/c14} ({F:dengue:D}). {n:fe.DENV.sero.pct:d1}% of the records lacked serotype information, and DENV-2 and
DENV-3 began to reappear visibly in 2024–2025: among typed records, DENV-2 rose from
{n:cl.DENV.sero_share.DENV2.2023:pct1} in 2023 to {n:cl.DENV.sero_share.DENV2.2024:pct1} in 2024 and
{n:cl.DENV.sero_share.DENV2.2025:pct1} in 2025, and DENV-3 from {n:cl.DENV.sero_share.DENV3.2023:pct1} to
{n:cl.DENV.sero_share.DENV3.2024:pct1} and {n:cl.DENV.sero_share.DENV3.2025:pct1}; in the partial year 2026
(January–September), {n:cl.DENV.sero_share.DENV3.2026:pct1} of the typed records were DENV-3 and
{n:cl.DENV.sero_share.DENV2.2026:pct1} DENV-2. Of the {n:cl.CHIKV.class.total:i} chikungunya cases, {n:cl.CHIKV.class.Chikungunya:i} were
classified as confirmed, {n:cl.CHIKV.class.Inconclusive:i} as inconclusive, and {n:cl.CHIKV.class.Unclassified:i} had no
classification yet (probable cases) ({F:chikzika:A}); cases under investigation by confirmation criterion numbered
{n:cl.CHIKV.crit.Ininvestigation:i}. The outcome of chikungunya was overwhelmingly cure ({n:cl.CHIKV.evo.Cure:i} patients), and
{n:cl.CHIKV.evo.Death:i} deaths from chikungunya were recorded. Of the {n:cl.ZIKV.class.total:i} Zika cases,
{n:cl.ZIKV.class.Confirmed:i} were confirmed, {n:cl.ZIKV.class.Inconclusive:i} remained inconclusive, and
{n:cl.ZIKV.class.Unclassified:i} had no classification yet ({F:chikzika:B}).
"""

# ---------------------------------------------------------------- 3.6 regression
REG1 = """
All three series showed substantial overdispersion (Pearson dispersion of the Poisson models {n:glmpois.DENV.disp:i},
{n:glmpois.CHIKV.disp:i}, and {n:glmpois.ZIKV.disp:i} for dengue, chikungunya, and Zika; NB2 dispersion parameter
α = {n:glmp.DENV.alpha:d2}, {n:glmp.CHIKV.alpha:d2}, and {n:glmp.ZIKV.alpha:d2}), and the NB2 models had far lower AIC
values than the Poisson models (for dengue, {n:glmp.DENV.aic:i} versus {n:glmpois.DENV.aic:i}; {F:glm_aic}). In the pooled
NB2 models with FU and calendar-month fixed effects ({F:glm_pooled}), each 1 °C increase in monthly mean temperature was
associated with higher dengue incidence (IRR {n:glmp.DENV.Temp_Avg.irr:d2}; 95% CI {n:glmp.DENV.Temp_Avg.lo:d2}–{n:glmp.DENV.Temp_Avg.hi:d2};
p {n:glmp.DENV.Temp_Avg.p:pv}) and higher Zika incidence (IRR {n:glmp.ZIKV.Temp_Avg.irr:d2}; 95% CI
{n:glmp.ZIKV.Temp_Avg.lo:d2}–{n:glmp.ZIKV.Temp_Avg.hi:d2}; p {n:glmp.ZIKV.Temp_Avg.p:pv}), whereas the association with
chikungunya incidence was not significant (IRR {n:glmp.CHIKV.Temp_Avg.irr:d2}; 95% CI
{n:glmp.CHIKV.Temp_Avg.lo:d2}–{n:glmp.CHIKV.Temp_Avg.hi:d2}; p {n:glmp.CHIKV.Temp_Avg.p:pv}). Each 100 mm increase in monthly rainfall was
associated with higher dengue incidence (IRR {n:glmp.DENV.Rain_mm.irr100:d2}; 95% CI
{n:glmp.DENV.Rain_mm.lo100:d2}–{n:glmp.DENV.Rain_mm.hi100:d2}), but not significantly with chikungunya
({n:glmp.CHIKV.Rain_mm.irr100:d2}; {n:glmp.CHIKV.Rain_mm.lo100:d2}–{n:glmp.CHIKV.Rain_mm.hi100:d2}) or Zika
({n:glmp.ZIKV.Rain_mm.irr100:d2}; {n:glmp.ZIKV.Rain_mm.lo100:d2}–{n:glmp.ZIKV.Rain_mm.hi100:d2}). Poisson models with
the same specification gave larger temperature IRRs (dengue, {n:glmpois.DENV.Temp_Avg.irr:d2}; chikungunya,
{n:glmpois.CHIKV.Temp_Avg.irr:d2}; Zika, {n:glmpois.ZIKV.Temp_Avg.irr:d2}), which shows that these estimates depend on how
overdispersion is handled.
"""

REG2 = """
At the FU level, the climatic signal varied considerably in both magnitude and direction across Brazil
({c15}Figures {f:glm_state} and {f:glm_forest}{/c15}). Temperature was significantly associated with dengue incidence in
{n:glms.DENV.Temp_Avg.nsig:i} of 27 FU ({n:glms.DENV.Temp_Avg.npos:i} positive and {n:glms.DENV.Temp_Avg.nneg:i}
negative), with chikungunya incidence in {n:glms.CHIKV.Temp_Avg.nsig:i} ({n:glms.CHIKV.Temp_Avg.npos:i} positive), and with
Zika incidence in {n:glms.ZIKV.Temp_Avg.nsig:i} ({n:glms.ZIKV.Temp_Avg.npos:i} positive); after Benjamini–Hochberg
correction, {n:glms.DENV.Temp_Avg.nfdr:i}, {n:glms.CHIKV.Temp_Avg.nfdr:i}, and {n:glms.ZIKV.Temp_Avg.nfdr:i} FU remained
significant. Among the FU with a significant positive association, the median IRR per °C was
{n:glms.DENV.Temp_Avg.medirr_sigpos:d2} for dengue, {n:glms.CHIKV.Temp_Avg.medirr_sigpos:d2} for chikungunya, and
{n:glms.ZIKV.Temp_Avg.medirr_sigpos:d2} for Zika. Rainfall was significantly associated with dengue incidence in
{n:glms.DENV.Rain_mm.nsig:i} FU ({n:glms.DENV.Rain_mm.npos:i} positive), with chikungunya incidence in
{n:glms.CHIKV.Rain_mm.nsig:i} ({n:glms.CHIKV.Rain_mm.npos:i} positive), and with Zika incidence in
{n:glms.ZIKV.Rain_mm.nsig:i} ({n:glms.ZIKV.Rain_mm.nneg:i} negative).
"""

REG3 = """
{c16}In the per-FU lagged models (concurrent temperature and rainfall and their one- and two-month lags entered jointly,
without a lag constraint){/c16}, the two-month temperature lag (Temp_Lag2) had the largest number of significant FU for
the three diseases: dengue ({n:glml.DENV.Temp_Lag2.nsig:i}; {n:glml.DENV.Temp_Lag2.npos:i} positive; {n:glml.DENV.Temp_Lag2.nfdr:i} after
Benjamini–Hochberg correction, compared with {n:glml.DENV.Temp_Avg.nsig:i} at lag 0 and {n:glml.DENV.Temp_Lag1.nsig:i} at
lag 1), chikungunya ({n:glml.CHIKV.Temp_Lag2.nsig:i}, {n:glml.CHIKV.Temp_Lag2.npos:i} positive, against
{n:glml.CHIKV.Temp_Avg.nsig:i} at lag 0 and {n:glml.CHIKV.Temp_Lag1.nsig:i} at lag 1), and Zika
({n:glml.ZIKV.Temp_Lag2.nsig:i} at lag 2, {n:glml.ZIKV.Temp_Avg.nsig:i} at lag 0, and {n:glml.ZIKV.Temp_Lag1.nsig:i} at lag 1). The
lag-2 rainfall coefficient was significant in {n:glml.DENV.Rain_Lag2.nsig:i}, {n:glml.CHIKV.Rain_Lag2.nsig:i}, and
{n:glml.ZIKV.Rain_Lag2.nsig:i} FU, respectively. {q:dlnm}In the pooled lagged model ({F:glm_lag}), the IRR per °C of dengue incidence was
{n:glmpl.DENV.Temp_Lag2.irr:d2} (95% CI {n:glmpl.DENV.Temp_Lag2.lo:d2}–{n:glmpl.DENV.Temp_Lag2.hi:d2}) at lag 2, against
{n:glmpl.DENV.Temp_Avg.irr:d2} at lag 0 and {n:glmpl.DENV.Temp_Lag1.irr:d2} at lag 1{/q}, and a temperature increase sustained over
lags 0–2 was associated with an IRR of {n:glmpl.DENV.Temp_Cum0_2.irr:d2} ({n:glmpl.DENV.Temp_Cum0_2.lo:d2}–{n:glmpl.DENV.Temp_Cum0_2.hi:d2}).
For chikungunya the lag-2 IRR was borderline ({n:glmpl.CHIKV.Temp_Lag2.irr:d2}; {n:glmpl.CHIKV.Temp_Lag2.lo:d2}–{n:glmpl.CHIKV.Temp_Lag2.hi:d2};
p {n:glmpl.CHIKV.Temp_Lag2.p:pv}), as was the sustained 0–2 month IRR ({n:glmpl.CHIKV.Temp_Cum0_2.irr:d2};
{n:glmpl.CHIKV.Temp_Cum0_2.lo:d2}–{n:glmpl.CHIKV.Temp_Cum0_2.hi:d2}; p {n:glmpl.CHIKV.Temp_Cum0_2.p:pv}). For Zika the largest coefficient was at lag 1
(IRR {n:glmpl.ZIKV.Temp_Lag1.irr:d2}; {n:glmpl.ZIKV.Temp_Lag1.lo:d2}–{n:glmpl.ZIKV.Temp_Lag1.hi:d2}) and the sustained 0–2 month IRR was
not significant ({n:glmpl.ZIKV.Temp_Cum0_2.irr:d2}; {n:glmpl.ZIKV.Temp_Cum0_2.lo:d2}–{n:glmpl.ZIKV.Temp_Cum0_2.hi:d2}). Rainfall sustained over
lags 0–2 was associated with higher incidence of the three diseases (IRR per 100 mm: dengue, {n:glmpl.DENV.Rain_Cum0_2.irr100:d2};
chikungunya, {n:glmpl.CHIKV.Rain_Cum0_2.irr100:d2}; Zika, {n:glmpl.ZIKV.Rain_Cum0_2.irr100:d2}), with the largest single-lag coefficients
at lag 2.
"""

RESULTS = [
    B("H1", "{c3}3 | RESULTS{/c3}"),
    B("H2", "3.1 | Spatiotemporal distribution"),
    B("Body", ANNUAL),
    B("Body", DISTRIBUTION, orig=[42], strip=True),
    B("Body", SPATIAL_AC),
    B("H2", "3.2 | Temporal trends"),
    B("Body", TRENDS, orig=[44], strip=True),
    B("H2", "3.3 | Seasonal variation"),
    B("Body", SEASON, orig=[46], strip=True),
    B("H2", "3.4 | Climatic correlations"),
    B("Body", CLIM1, orig=[48], strip=True),
    B("Body", CLIM2),
    B("H2", "3.5 | Demographic, clinical, and laboratory profile"),
    B("Body", DEMO, orig=[50], strip=True),
    B("Body", CLIN, orig=[51]),
    B("H2", "3.6 | Regression models"),
    B("Body", REG1, orig=[53], strip=True),
    B("Body", REG2, orig=[54]),
    B("Body", REG3, orig=[55]),
]
