# Literature context

How four recent papers relate to the results of this project, and what the project can and cannot say
against them. Written 2026-10-21 for the 2016–2026 analysis; **numbers updated 2026-10-22** after the rerun (SINAN
downloaded again on 2026-10-22, 2026 limited to notifications up to 2026-09-30; a case is any notification not
classified as discarded, for the three diseases).

**Numbers from this project come from the regenerated outputs** (`outputs/`, `clinical_tables/`,
`outputs/2026-10-08/additional/`), never from [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md), which describes the
older 2016–2025 run. Each statement is tagged:

- **Consistent**: the project's result points the same way as the paper.
- **Qualifies**: the paper limits how the project's result should be read.
- **Hypothesis**: a possible link the data here do not test.
- **Gap**: something the paper covers that the project does not.

Of the four papers, Liu, Lim and De Lima were checked against the paper's text. Moura was checked against its
abstract only (no open full text), so only abstract-level facts are used from it.

---

## 1. Liu et al. 2023, temperature and dengue transmission (review)

*What it reports.* Temperature shapes *Aedes* survival and distribution, the dengue virus itself, and vector
competence. It gives a minimum suitable temperature for transmission of 14.8 °C and an optimum maximum of
32–33 °C, and reports a two-month lag as the best predictor of dengue cases in one Delhi study. It also
discusses the daily temperature range (DTR) and *Aedes* spread into colder areas under warming.

*Against this project.*
- **Consistent.** Dengue has a positive temperature association: the regenerated pooled NegBin model (state and
  month fixed effects, cluster-robust SEs) gives an IRR of 1.106 per +1 °C (95% CI 1.026–1.191, p = 0.008).
  Chikungunya is 1.029 (0.948–1.117, p = 0.493, not significant); Zika is 1.106 (1.001–1.221, p = 0.047)
  (`outputs/glm_negbin_pooled_fe.csv`).
- **Consistent, with a caveat.** The response is non-linear. The DLNM puts the dengue temperature optimum at
  27.5 °C (IRR 1.19); chikungunya (25.1 °C, IRR 1.01) and Zika (25.6 °C, IRR 1.00) are flat
  (`dlnm_summary.csv`; the DLNM is not part of the manuscript). Do not read this
  as agreement or disagreement with Liu's 32–33 °C: Liu's thresholds mix mean, minimum and maximum temperatures,
  while this project uses the monthly mean of hourly readings, averaged over each state's stations.
- **Gap.** The lag dimension covers 0–2 months only, there is no humidity, and there is no Tmin, Tmax or DTR.
  The Delhi study's two-month optimum sits at the edge of this project's lag window; in the pooled lagged model
  the dengue coefficient is largest at lag 2 (IRR 1.37), so a longer window could show a stronger association.
- **Hypothesis.** Liu (and Lim, below) point to *Aedes* spread into colder, higher-latitude areas. Whether the
  southern states' dengue and chikungunya trends reflect this is untested here. The regenerated Figure S2B marks
  two states for dengue (Rio Grande do Sul, Santa Catarina) and three for chikungunya (Mato Grosso do Sul, Goiás,
  Minas Gerais) with a significant increasing trend (raw p < 0.05). After Benjamini–Hochberg correction only the
  chikungunya increase in Mato Grosso do Sul remains (q = 0.029); no dengue trend does (smallest q = 0.344)
  (`outputs/py_statistical_results.xlsx`). The chikungunya states are in the Central-West and Southeast.

## 2. Moura et al. 2020, *Aedes* oviposition in Natal, Rio Grande do Norte (abstract only)

*What it reports.* 307 oviposition traps across the city, checked weekly from 2016 to 2018. The median
oviposition positivity was 60.5% and the egg density 45.4 eggs per trap. Temperature and humidity correlated only
weakly and very weakly with oviposition. Positivity was highest in the second quarter (71.1%). Oviposition was
spatially segregated, with persistent areas along a strip of the north and west districts.

*Against this project.*
- **Qualifies.** The project works at state level with monthly climate. Moura works at street level with weekly
  vector counts. A state-level climate association says nothing about where in a city transmission is
  concentrated.
- **Consistent.** Weak climate–vector correlation fits the modest climate effects in the regenerated models.
- **Gap.** The project has no vector indicator and no humidity.
- **Hypothesis.** The original 2016–2025 summary listed Rio Grande do Norte among the dengue low-low clusters,
  although Natal showed abundant oviposition. If that cluster holds in the regenerated LISA output, vector
  presence and notified incidence need not move together. This has not been checked in the current outputs.

## 3. Lim et al. 2025, overlapping distribution of dengue, chikungunya, Zika and yellow fever

*What it reports.* A joint niche model with a surveillance-capability model for the four viruses. Suitability is
the probability that one or more cases ever occurred up to 2024, given average environmental conditions over
2010–2020. It estimates 5.66 billion people in areas suitable for dengue, chikungunya and Zika, and 1.54 billion
for yellow fever. Recent chikungunya and Zika spread lies inside areas already suitable for dengue. Surveillance
capability is higher in richer and more accessible places, and it varies within countries, with urban areas above
rural ones, "particularly evident in countries like Brazil and India". The authors note a high potential for
misdiagnosis and under-reporting of Zika and chikungunya and call for integrated arbovirus responses.

*Against this project.*
- **Qualifies.** SINAN notifications are treated here as incidence. State differences in the maps (Figure 6,
  Figure S2A) can reflect who gets tested and reported as well as who gets infected. The case definition is the
  same for the three diseases (every notification not classified as discarded), but the share discarded differs
  (dengue 15%, chikungunya 35%, Zika 47%), which limits comparisons across diseases.
- **Hypothesis.** Dengue shows strong spatial clustering (global Moran's I = 0.516, p = 0.001), chikungunya a
  weaker one (0.231, p = 0.017) and Zika none (−0.105, p = 0.243), although Lim finds all three share a suitability
  niche. Differential reporting or diagnosis is one candidate explanation. Epidemic timing and introduction
  history are others. The data here cannot separate them.
- **Consistent.** The co-circulation analysis (`adv_cocirculation.R`) treats the three diseases together, in line
  with the call for an integrated approach.
- **Gap.** Yellow fever is not covered. Lim's maps are suitability, not circulation, and they cannot be compared
  with notification counts directly.

## 4. De Lima et al. 2026, dengue in Ceará, 2010–2025 (Emerging Infectious Diseases, early release)

*What it reports.* National laboratory-confirmed dengue: 1,657,046 cases, in 98.9% of municipalities,
13 major epidemic waves, and a test positivity of 18.2% to 57.1%. In Ceará: 131,961 confirmed cases
(cumulative incidence 1,500 per 100,000), in all 184 municipalities. National epidemics ran February–June and
peaked in March–April; in Ceará they ran March–August and typically peaked in May. The female-to-male ratio was
1.6, and cumulative incidence was higher at ages 10–39 than above 70. In Ceará, DENV-1 predominated in 2014–2019
and 2023–2025, DENV-2 re-emerged in 2019, and DENV-3 (lineage III_B3.2) was detected again in July 2025 after no
local detection since 2015, clustering with São Paulo sequences from 2024–2025. The authors sequenced 243 genomes
from February 2024 to July 2025, and their conclusions point to future dengue immunization programs in Brazil
using Qdenga (TAK-003) and Butantan-DV.

*Against this project.*
- **Consistent.** The national SINAN serotype records show DENV-3 rising. Among typed dengue records
  (DENV-1 to DENV-4 only), DENV-3 never exceeded 1.6% in 2016–2023 (0.2% in 2023), then reached 0.9% in 2024
  (1,789 records), 14.0% in 2025 (6,857) and 29.8% in 2026, January–September (9,977).
- **Qualifies.** These are national typed records, not Ceará. Nationally, DENV-2 holds most typed records in
  2025 (73.8%) and 2026 (64.2%), while the paper reports DENV-1 as predominant in Ceará. Where the typed
  records come from geographically is not known here. Typing covers 0.2–3.0% of notifications per year in
  2016–2025 and 7.1% in 2026.
- **Qualifies.** A SOROTIPO value of `0`, which is not a serotype, appears under the label `codigo_0` in
  `clinical_tables/clinical_demographic_long.csv` from 2021: 134,407 records in 2023 (about three times all valid
  typed records that year), 131,058 in 2024, 33,493 in 2025 and 17,700 in 2026. These are not counted as typed
  above. Figure 7D folds them into "Ign/Blank"; the manuscript carries an author query on this treatment.
- **Qualifies.** The paper counts laboratory-confirmed cases. This project counts probable dengue cases
  (all notifications except discarded). Absolute counts and incidence are not comparable.
- **Gap.** No seasonality metric (peak month, season length) per state or region, for comparison with the paper's
  national and Ceará pattern. No sex-ratio or age-band comment. Severity (warning signs, severe dengue, deaths) is
  tabulated in `clinical_tables/` but not analysed. There is no vaccination, genomic-lineage or test-positivity
  information.

---

## Limitations these papers add to the manuscript text

These are mirrored in the limitations block of [`FIGURE_CAPTIONS.md`](FIGURE_CAPTIONS.md).

1. Notifications are not incidence: reporting and diagnosis vary between states and between diseases (Lim).
2. Cases are confirmed plus probable (discarded notifications excluded) for the three diseases, and published
   laboratory-confirmed series are not comparable in size (De Lima).
3. Climate is a monthly state mean of hourly readings, with lags up to two months, and no humidity or daily range
   (Liu, Moura).
4. State-level associations do not describe vector abundance or transmission inside a city (Moura).
5. No vaccination data for 2024–2026, no genomic lineages, and serotype typing is partial (De Lima).

## Open checks before any of the "Hypothesis" items is written up as a result

- Whether the strongest climate association lies at the longest lag tested (lag 2). The pooled lagged model puts the
  dengue maximum at lag 2 (Zika at lag 1); only a model with a longer window can test it.
- Which states carry the dengue and chikungunya increasing trends, and whether any survives FDR: answered above
  (dengue RS and SC, none after correction; chikungunya MS, GO and MG, MS after correction).
- Whether Rio Grande do Norte is still a dengue low-low state in the regenerated LISA output: yes (raw p < 0.05);
  none of the local clusters except Goiás, Minas Gerais and Rio de Janeiro remains after correction.
- How Figure 7D treats the `codigo_0` serotype records: folded into "Ign/Blank" (author query open).

## References

1. Liu Z, Zhang Q, Li L, He J, Guo J, Wang Z, Huang Y, Xi Z, Yuan F, Li Y, Li T. The effect of temperature on
   dengue virus transmission by *Aedes* mosquitoes. *Front Cell Infect Microbiol*. 2023;13:1242173.
   [doi:10.3389/fcimb.2023.1242173](https://doi.org/10.3389/fcimb.2023.1242173). PMID 37808907.
2. Moura MCBM, de Oliveira JV, Pedreira RM, Tavares AM, de Souza TA, de Lima KC, Barbosa IR. Spatio-temporal
   dynamics of *Aedes aegypti* and *Aedes albopictus* oviposition in an urban area of northeastern Brazil.
   *Trop Med Int Health*. 2020;25(12):1510–1521.
   [doi:10.1111/tmi.13491](https://doi.org/10.1111/tmi.13491). PMID 32959943.
3. Lim A, Shearer FM, Sewalk K, et al. The overlapping global distribution of dengue, chikungunya, Zika and
   yellow fever. *Nat Commun*. 2025;16(1):3418.
   [doi:10.1038/s41467-025-58609-5](https://doi.org/10.1038/s41467-025-58609-5). PMID 40210848.
4. de Lima STS, Claro IM, Hua X, et al. Transmission dynamics of dengue virus, Ceará State, Brazil, 2010–2025.
   *Emerg Infect Dis*. 2026;32(11). Early release 15 October 2026.
   [doi:10.3201/eid3211.260609](https://doi.org/10.3201/eid3211.260609).
