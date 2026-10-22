from msbase import B, O, strip_runin

# ---------------------------------------------------------------- 3.1 distribution
ANNUAL = """
Between January 2016 and September 2026, SINAN recorded {n:cases.DENV.all:i} probable dengue cases,
{n:cases.CHIKV.all:i} chikungunya notifications, and {n:cases.ZIKV.all:i} Zika notifications in the 27 FU. Dengue incidence peaked in 2024, with
{n:cases.DENV.y2024:i} cases ({n:ann.DENV.BR.2024:d0} per 100,000 inhabitants), {n:natpeak_ratio_second.DENV:d1} times
the incidence of 2023 ({n:ann.DENV.BR.2023:d0} per 100,000); the annualized incidence for 2026 (January–September) was
{n:ann.DENV.BR.2026:d0} per 100,000 (Figure 1A). {c9}Chikungunya incidence was also highest in 2024
({n:ann.CHIKV.BR.2024:d1} per 100,000), followed by 2016 ({n:ann.CHIKV.BR.2016:d1}). At regional level, the highest
annual value was reached by the Central-West in 2025 ({n:chik_regmax_val:d1} per 100,000), driven by Mato Grosso do Sul
({n:ann_state.CHIKV.MS.2025:d0}) and Mato Grosso ({n:ann_state.CHIKV.MT.2025:d0}).{/c9}
"""

DISTRIBUTION = """
The absolute burden of dengue was concentrated in the Southeast, where {u:rank_cases.DENV.1:cap} recorded the largest
number of cases ({n:rank_cases_val.DENV.1:i}), followed by {u:rank_cases.DENV.2} ({n:rank_cases_val.DENV.2:i}). In contrast, the North
region reported substantially lower figures, ranging from {n:regmin.DENV.N:i} in {u:regmin_uf.DENV.N} to
{n:regmax.DENV.N:i} in {u:regmax_uf.DENV.N}, and the Northeast showed marked internal variation, from
{n:regmin.DENV.NE:i} in {u:regmin_uf.DENV.NE} to {n:regmax.DENV.NE:i} in {u:regmax_uf.DENV.NE}. Taken together, this
spatial gradient mirrors the demographic hierarchy of the country. It is interesting to note that the ranking changed
substantially when the population size was considered (Figure 6). The highest mean annual incidence was observed in
{u:rank_minc.DENV.1} ({n:rank_minc_val.DENV.1:d1} per 100,000 inhabitants), followed by {u:rank_minc.DENV.2}
({n:rank_minc_val.DENV.2:d1}) and {u:rank_minc.DENV.3} ({n:rank_minc_val.DENV.3:d1}). The absolute burden of
chikungunya was concentrated in a few states of the Southeast and Northeast regions, where {u:rank_cases.CHIKV.1}
recorded the largest number of cases ({n:rank_cases_val.CHIKV.1:i}), followed by {u:rank_cases.CHIKV.2}
({n:rank_cases_val.CHIKV.2:i}), {u:rank_cases.CHIKV.3} ({n:rank_cases_val.CHIKV.3:i}), {u:rank_cases.CHIKV.4}
({n:rank_cases_val.CHIKV.4:i}), and {u:rank_cases.CHIKV.5} ({n:rank_cases_val.CHIKV.5:i}). On a per-capita basis, the
highest mean annual incidence was observed in {u:rank_minc.CHIKV.1} ({n:rank_minc_val.CHIKV.1:d1}), Central-West region,
followed by {u:rank_minc.CHIKV.2} ({n:rank_minc_val.CHIKV.2:d1}) and {u:rank_minc.CHIKV.3} ({n:rank_minc_val.CHIKV.3:d1}),
while {u:rank_cases.CHIKV.1} (which had the largest absolute number of cases) ranked {n:rank_of_topcases.CHIKV.1:ord}
(Figure 6). The absolute burden of Zika was highest in {u:rank_cases.ZIKV.1} ({n:rank_cases_val.ZIKV.1:i}) and
{u:rank_cases.ZIKV.2} ({n:rank_cases_val.ZIKV.2:i}), with counts in the South region ranging from {n:regmin.ZIKV.S:i} in
{u:regmin_uf.ZIKV.S} to {n:regmax.ZIKV.S:i} in {u:regmax_uf.ZIKV.S}. On a per-capita basis, the highest mean annual
incidence was observed in {u:rank_minc.ZIKV.1} ({n:rank_minc_val.ZIKV.1:d1}) and {u:rank_minc.ZIKV.2}
({n:rank_minc_val.ZIKV.2:d1}), whereas {u:rank_cases.ZIKV.1} and {u:rank_cases.ZIKV.2} ranked
{n:rank_of_topcases.ZIKV.1:ord} and {n:rank_of_topcases.ZIKV.2:ord}, respectively (Figure 6).
"""

SPATIAL_AC = """
Spatial autocorrelation analysis identified dengue as the only arbovirus with significant global spatial structure
({c4}Moran’s I = {n:moran.DENV.I:d3}, p {n:moran.DENV.p:pv}{/c4}; chikungunya, I = {n:moran.CHIKV.I:d3},
p {n:moran.CHIKV.p:pv}; Zika, I = {n:moran.ZIKV.I:d3}, p {n:moran.ZIKV.p:pv}; {c5}Figure 4{/c5}). For dengue, high–high
clusters were observed across the Central-West and Southeast and in Paraná ({n:lisa_names.DENV.HH:s}), and low–low
clusters in {n:lisa_names.DENV.LL:s}; {u:lisa_uf.DENV.HL:cap} appeared as a high–low outlier and
{u:lisa_uf.DENV.LH} as a low–high outlier ({c6}Figure S2A{/c6}). After Benjamini–Hochberg correction, only
{n:lisafdr_names.DENV.HH:s} (high–high) and {n:lisafdr_names.DENV.LH:s} (low–high) remained significant. Only isolated
local clusters were detected for chikungunya (high–high, {n:lisa_names.CHIKV.HH:s}; high–low,
{n:lisa_names.CHIKV.HL:s}; low–high, {n:lisa_names.CHIKV.LH:s}) and Zika (high–high, {n:lisa_names.ZIKV.HH:s}; low–low,
{n:lisa_names.ZIKV.LL:s}; low–high, {n:lisa_names.ZIKV.LH:s}), and none remained significant after correction.
"""

# ---------------------------------------------------------------- 3.2 trends
TRENDS = """
Statistically significant increasing trends in dengue incidence were observed in
{u:mkr.DENV.increasing.1.uf:cap} (τ = {n:mkr.DENV.increasing.1.tau:d3}; Sen’s slope ≈ {n:mkr.DENV.increasing.1.slope:d0} cases per 100,000 per
year) and {u:mkr.DENV.increasing.2.uf} (τ = {n:mkr.DENV.increasing.2.tau:d3}; ≈{n:mkr.DENV.increasing.2.slope:d0}) ({c7}Figure 2{/c7}).
Three states displayed statistically significant increasing trends for chikungunya: {u:mkr.CHIKV.increasing.1.uf:cap}
(τ = {n:mkr.CHIKV.increasing.1.tau:d3}; ≈{n:mkr.CHIKV.increasing.1.slope:d0} cases per 100,000 per year, the largest Sen’s slope),
{u:mkr.CHIKV.increasing.2.uf} (τ = {n:mkr.CHIKV.increasing.2.tau:d3}; ≈{n:mkr.CHIKV.increasing.2.slope:d0}), and
{u:mkr.CHIKV.increasing.3.uf} (τ = {n:mkr.CHIKV.increasing.3.tau:d3}; ≈{n:mkr.CHIKV.increasing.3.slope:d0}). Zika was the only arbovirus with
significant decreasing trends, observed in {n:mk_n.ZIKV.decreasing:words} states ({n:mk_names.ZIKV.decreasing:s}; τ from
{n:mk_taumin.ZIKV.decreasing:d3} to {n:mk_taumax.ZIKV.decreasing:d3}) ({c8}Figures S2B and 2{/c8}). None of these trends remained
significant after Benjamini–Hochberg correction (smallest q-values: dengue {n:mk_minq.DENV:d3}, chikungunya
{n:mk_minq.CHIKV:d3}, Zika {n:mk_minq.ZIKV:d3}).
"""

# ---------------------------------------------------------------- 3.3 seasonality
SEASON = """
Summed across the ten complete study years (2016–2025), dengue cases rose from {n:seas.DENV.m1:i} in January to
{n:seas.DENV.m2:i} in February, peaked in March–April (mean of {n:seas.DENV.marapr_mean:i} per month), and fell to
{n:seas.DENV.m6:i} in June; from July to December, monthly totals ranged from {n:seas.DENV.h2_min:i} to
{n:seas.DENV.h2_max:i}. Interannual variability was dominated by the 2024 epidemic, an extreme outlier in the series
(Figure 1A). Chikungunya also showed a seasonal pattern, with monthly totals rising from {n:seas.CHIKV.m1:i} in January
to a peak of {n:seas.CHIKV.m5:i} in May and falling to {n:seas.CHIKV.m6:i} in June, and ranging from
{n:seas.CHIKV.h2_min:i} to {n:seas.CHIKV.h2_max:i} from July to December. The seasonal profile of ZIKV was similar to
those of dengue and chikungunya: monthly totals rose from {n:seas.ZIKV.m1:i} in January to a peak of
{n:seas.ZIKV.m3:i} in March, fell to {n:seas.ZIKV.m5:i} in May and {n:seas.ZIKV.m6:i} in June, and ranged from
{n:seas.ZIKV.h2_min:i} to {n:seas.ZIKV.h2_max:i} per month in the second half of the year. The annual series of ZIKV was
dominated by the 2016 epidemic (Figure 1A), with {n:cases.ZIKV.y2016:i} cases nationally ({n:ann.ZIKV.BR.2016:d0} per
100,000), between {n:zika_ratio_min:d1} and {n:zika_ratio_max:d1} times the incidence of each later complete year.
"""

# ---------------------------------------------------------------- 3.4 climate correlations
CLIM1 = """
Correlations between monthly incidence and temperature depended on the lag ({c11}Figure 3{/c11}). For dengue, the
mean Spearman correlation across the 27 FU was negative at lag 0 (ρ = {n:sp.DENV.Temp.0.mean:d3}), close to zero at
lag 1 ({n:sp.DENV.Temp.1.mean:d3}), and positive at lag 2 ({n:sp.DENV.Temp.2.mean:d3}); at lag 2, {n:sp.DENV.Temp.2.nsig:i}
of 27 FU ({n:sp.DENV.Temp.2.prop:pct0}) had p < 0.05, of which {n:sp.DENV.Temp.2.npos:i} were positive and
{n:sp.DENV.Temp.2.nneg:i} negative. The strongest lag-2 correlations were observed for {u:sp.DENV.Temp.2.top1.uf}
(ρ = {n:sp.DENV.Temp.2.top1.rho:d3}), {u:sp.DENV.Temp.2.top2.uf} ({n:sp.DENV.Temp.2.top2.rho:d3}),
{u:sp.DENV.Temp.2.top3.uf} ({n:sp.DENV.Temp.2.top3.rho:d3}), and {u:sp.DENV.Temp.2.top4.uf}
({n:sp.DENV.Temp.2.top4.rho:d3}). Chikungunya showed the same pattern (mean ρ = {n:sp.CHIKV.Temp.0.mean:d3},
{n:sp.CHIKV.Temp.1.mean:d3}, and {n:sp.CHIKV.Temp.2.mean:d3} at lags 0, 1, and 2; {n:sp.CHIKV.Temp.2.nsig:i} FU significant at
lag 2), with the strongest lag-2 correlations in {u:sp.CHIKV.Temp.2.top1.uf} (ρ = {n:sp.CHIKV.Temp.2.top1.rho:d3})
and {u:sp.CHIKV.Temp.2.top2.uf} ({n:sp.CHIKV.Temp.2.top2.rho:d3}). For Zika, the mean correlation with temperature was weak (ρ = {n:sp.ZIKV.Temp.0.mean:d3},
{n:sp.ZIKV.Temp.1.mean:d3}, and {n:sp.ZIKV.Temp.2.mean:d3} at lags 0, 1, and 2), but some states showed strong correlations
at lag 2, particularly {u:sp.ZIKV.Temp.2.top1.uf} (ρ = {n:sp.ZIKV.Temp.2.top1.rho:d3})
and {u:sp.ZIKV.Temp.2.top2.uf} ({n:sp.ZIKV.Temp.2.top2.rho:d3}). The national mean concealed a regional contrast: for all three diseases, the mean
lag-2 correlation with temperature was positive in the Southeast, South, and Central-West (dengue, {n:sp.DENV.Temp.2.reg.SE:d3},
{n:sp.DENV.Temp.2.reg.S:d3}, and {n:sp.DENV.Temp.2.reg.CO:d3}) and negative in the Northeast (dengue,
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
The demographic and clinical results refer to 2016–2025 for dengue and Zika and to 2017–2025 for chikungunya.
Dengue cases were concentrated among adults aged 20–59 years ({n:cl.DENV.age.20_59:i} of {n:cl.DENV.age.known:i} cases
with known age, {n:cl.DENV.age.20_59_share:pct1}), with lower frequencies among children and older adults (Figure 5A).
Most cases were recorded in women ({n:cl.DENV.sex.F:i}) when compared to men ({n:cl.DENV.sex.M:i}), corresponding to a
female-to-male ratio of {n:cl.DENV.sex.ratio:d2} (Figure 5B). The most affected age groups for chikungunya were 20–39
years ({n:cl.CHIKV.age.20_39:i} cases) and 40–59 years ({n:cl.CHIKV.age.40_59:i} cases) (Figure 5A). Women accounted for
{n:cl.CHIKV.sex.F:i} cases, compared with {c12}{n:cl.CHIKV.sex.M:i}{/c12} cases in men, a ratio of {n:cl.CHIKV.sex.ratio:d1}:1 (Figure 5B). For Zika, the most
affected age groups were also 20–39 years ({n:cl.ZIKV.age.20_39:i} cases) and 40–59 years ({n:cl.ZIKV.age.40_59:i}
cases), with progressively fewer cases among adolescents, children, and older adults (Figure 5A). Women accounted for
{n:cl.ZIKV.sex.F:i} cases when compared to men ({n:cl.ZIKV.sex.M:i}), a ratio of {n:cl.ZIKV.sex.ratio:d1}:1. A total of
{n:cl.ZIKV.preg.tri_sum:i} cases occurred in pregnant women, distributed across the first ({n:cl.ZIKV.preg.1Trimester:i}),
second ({n:cl.ZIKV.preg.2Trimester:i}), and third ({n:cl.ZIKV.preg.3Trimester:i}) trimesters.
"""

CLIN = """
{c13}Hospitalization status was recorded for {n:cl.DENV.hosp.known:i} of the {n:cl.DENV.hosp.total:i} dengue
notifications: {n:cl.DENV.hosp.Positive:i} patients ({n:cl.DENV.hosp.share_known:pct1} of those with known status) were
admitted for inpatient care and {n:cl.DENV.hosp.Negative:i} were not, whereas the information was ignored or blank in
{n:cl.DENV.hosp.IgnBlank:i} notifications ({n:fe.DENV.hosp.pct:d1}%) (Figure 7C).{/c13} Serotype was recorded for only
{n:cl.DENV.sero.typed:i} notifications ({n:cl.DENV.sero.typed_share:pct1}): {c14}DENV-1 was detected in
{n:cl.DENV.sero.DENV1:i} cases, followed by DENV-2 ({n:cl.DENV.sero.DENV2:i}), DENV-3 ({n:cl.DENV.sero.DENV3:i}), and DENV-4
({n:cl.DENV.sero.DENV4:i}){/c14} (Figure 7D). {n:fe.DENV.sero.pct:d1}% of the records lacked serotype information, and DENV-2 and
DENV-3 began to reappear visibly in 2024–2025: among typed records, DENV-2 rose from
{n:cl.DENV.sero_share.DENV2.2023:pct1} in 2023 to {n:cl.DENV.sero_share.DENV2.2024:pct1} in 2024 and
{n:cl.DENV.sero_share.DENV2.2025:pct1} in 2025, and DENV-3 from {n:cl.DENV.sero_share.DENV3.2023:pct1} to
{n:cl.DENV.sero_share.DENV3.2024:pct1} and {n:cl.DENV.sero_share.DENV3.2025:pct1}. In the SINAN records through
September 2026, which Figure 7 does not include, {q:code0}{n:ct.sero_typed_pct.2026:pct1} of notifications were typed{/q}, and DENV-3 accounted for
{n:ct.sero_share.DENV3.2026:pct1} and DENV-2 for {n:ct.sero_share.DENV2.2026:pct1} of the typed records.
Of the {n:cl.CHIKV.class.all:i} chikungunya notifications, {n:cl.CHIKV.conf:i} were classified as confirmed and
{n:cl.CHIKV.disc:i} as discarded, and the classification was ignored or blank in {n:cl.CHIKV.class.IgnBlank:i}
(Figure 8A); cases under investigation remained rare ({n:cl.CHIKV.crit.Ininvestigation:i} notifications by confirmation
criterion). The outcome of chikungunya was overwhelmingly cure ({n:cl.CHIKV.evo.Cure:i} patients), and
{n:cl.CHIKV.evo.Death:i} deaths from chikungunya were recorded. Of the {n:cl.ZIKV.class.all:i} Zika notifications,
{n:cl.ZIKV.conf:i} were confirmed, {n:cl.ZIKV.incl:i} remained inconclusive, and {n:cl.ZIKV.disc:i} were discarded
(Figure 8B).
"""

# ---------------------------------------------------------------- 3.6 regression
REG1 = """
All three series showed substantial overdispersion (Pearson dispersion of the Poisson models {n:glmpois.DENV.disp:i},
{n:glmpois.CHIKV.disp:i}, and {n:glmpois.ZIKV.disp:i} for dengue, chikungunya, and Zika; NB2 dispersion parameter
α = {n:glmp.DENV.alpha:d2}, {n:glmp.CHIKV.alpha:d2}, and {n:glmp.ZIKV.alpha:d2}), and the NB2 models had far lower AIC
values than the Poisson models (for dengue, {n:glmp.DENV.aic:i} versus {n:glmpois.DENV.aic:i}; Figure S6). In the pooled
NB2 models with FU and calendar-month fixed effects (Figure S3), each 1 °C increase in monthly mean temperature was
associated with higher dengue incidence (IRR {n:glmp.DENV.Temp_Avg.irr:d2}; 95% CI {n:glmp.DENV.Temp_Avg.lo:d2}–{n:glmp.DENV.Temp_Avg.hi:d2};
p {n:glmp.DENV.Temp_Avg.p:pv}) and higher Zika incidence (IRR {n:glmp.ZIKV.Temp_Avg.irr:d2}; 95% CI
{n:glmp.ZIKV.Temp_Avg.lo:d2}–{n:glmp.ZIKV.Temp_Avg.hi:d2}; p {n:glmp.ZIKV.Temp_Avg.p:pv}), whereas the association with
chikungunya incidence was not significant (IRR {n:glmp.CHIKV.Temp_Avg.irr:d2}; 95% CI
{n:glmp.CHIKV.Temp_Avg.lo:d2}–{n:glmp.CHIKV.Temp_Avg.hi:d2}; p {n:glmp.CHIKV.Temp_Avg.p:pv}). Rainfall was positively associated
with incidence for all three diseases: each 100 mm increase was associated with an IRR of
{n:glmp.DENV.Rain_mm.irr100:d2} (95% CI {n:glmp.DENV.Rain_mm.lo100:d2}–{n:glmp.DENV.Rain_mm.hi100:d2}) for dengue,
{n:glmp.CHIKV.Rain_mm.irr100:d2} ({n:glmp.CHIKV.Rain_mm.lo100:d2}–{n:glmp.CHIKV.Rain_mm.hi100:d2}) for chikungunya, and
{n:glmp.ZIKV.Rain_mm.irr100:d2} ({n:glmp.ZIKV.Rain_mm.lo100:d2}–{n:glmp.ZIKV.Rain_mm.hi100:d2}) for Zika. Poisson models with
the same specification gave larger temperature IRRs (dengue, {n:glmpois.DENV.Temp_Avg.irr:d2}; chikungunya,
{n:glmpois.CHIKV.Temp_Avg.irr:d2}; Zika, {n:glmpois.ZIKV.Temp_Avg.irr:d2}), which shows that these estimates depend on how
overdispersion is handled.
"""

REG2 = """
At the FU level, the climatic signal varied considerably in both magnitude and direction across Brazil
({c15}Figures S4 and S7{/c15}). Temperature was significantly associated with dengue incidence in
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
without a lag constraint; Figure S5){/c16}, the two-month temperature lag (Temp_Lag2) had the largest number of
significant FU for all three diseases. The lag-2 coefficient was significant in {n:glml.DENV.Temp_Lag2.nsig:i} FU for
dengue ({n:glml.DENV.Temp_Lag2.npos:i} positive; {n:glml.DENV.Temp_Lag2.nfdr:i} after Benjamini–Hochberg correction),
{n:glml.CHIKV.Temp_Lag2.nsig:i} for chikungunya ({n:glml.CHIKV.Temp_Lag2.npos:i} positive), and
{n:glml.ZIKV.Temp_Lag2.nsig:i} for Zika ({n:glml.ZIKV.Temp_Lag2.npos:i} positive), compared with
{n:glml.DENV.Temp_Avg.nsig:i}, {n:glml.CHIKV.Temp_Avg.nsig:i}, and {n:glml.ZIKV.Temp_Avg.nsig:i} FU at lag 0 and
{n:glml.DENV.Temp_Lag1.nsig:i}, {n:glml.CHIKV.Temp_Lag1.nsig:i}, and {n:glml.ZIKV.Temp_Lag1.nsig:i} FU at lag 1; for
dengue, the margin over lags 0 and 1 was small. Among the FU with a significant positive lag-2 coefficient, the median IRR
per °C was {n:glml.DENV.Temp_Lag2.medirr_sigpos:d2} for dengue, {n:glml.CHIKV.Temp_Lag2.medirr_sigpos:d2} for
chikungunya, and {n:glml.ZIKV.Temp_Lag2.medirr_sigpos:d2} for Zika. The lag-2 rainfall coefficient was significant in
{n:glml.DENV.Rain_Lag2.nsig:i}, {n:glml.CHIKV.Rain_Lag2.nsig:i}, and {n:glml.ZIKV.Rain_Lag2.nsig:i} FU, respectively. In
the supplementary DLNM, {q:dlnm}the temperature optimum for dengue was {n:dlnm.DENV.opt:d1} °C (cumulative IRR
{n:dlnm.DENV.irr:d2} relative to {n:dlnm.ref.Temp:d1} °C){/q}; the Zika curve increased up to the upper end of the observed
range ({n:dlnm.ZIKV.opt:d1} °C; IRR {n:dlnm.ZIKV.irr:d2}), and the chikungunya curve rose up to about
{n:dlnm.CHIKV.opt:d1} °C with no further increase at higher temperatures.
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
