from msbase import B, O, strip_runin

EPI = """
Notified cases of dengue, chikungunya, and Zika were obtained from the open SINAN microdata published by the Brazilian
Ministry of Health through OpenDataSUS (files DENGBR, CHIKBR, and ZIKABR for 2016–2026; the 2026 files are the
release of October 6, 2026) [@r56]. The cases are classified as confirmed, discarded, inconclusive, or under
investigation, using either {c17}laboratory criteria (RT-PCR, NS1 antigen detection, or IgM/IgG ELISA){/c17} or
clinical-epidemiological criteria defined by the Brazilian Ministry of Health (BMoH) [@r52]. The case definition
follows the original series and differs by disease. {c18}Dengue counts probable cases, that is, all notifications
except those classified as discarded.{/c18} {c19}Chikungunya and Zika count all notifications, including discarded,
inconclusive, and under-investigation records{/c19}: in the clinical tables, discarded records were
{n:cl.CHIKV.disc:i} of {n:cl.CHIKV.class.all:i} chikungunya notifications ({n:cl.CHIKV.disc_share:pct1}; 2017–2025)
and {n:cl.ZIKV.disc:i} of {n:cl.ZIKV.class.all:i} Zika notifications ({n:cl.ZIKV.disc_share:pct1}; 2016–2025).
Cases were assigned to the FU of notification, to the year of the SINAN annual file, and to the month of the
notification date, not to the FU of residence, and notifications without a valid FU or notification month were not
counted [@r52]. The national SINAN files contain no chikungunya or Zika notification for Espírito Santo in 2021, so
that state-year is missing, not zero. Notifications with missing values for other attributes such as sex, age,
serotype, or laboratory results were used only for incidence and trend analyses (which is consistent with the BMoH
reporting practice). In the descriptive analyses of proportions, records with ignored or blank values were excluded
from numerators and denominators, and the number excluded is given in each figure legend. {c20}Annual resident
population{/c20} estimates by FU were obtained from the Brazilian Institute of Geography and Statistics (IBGE): the
Population Projections, 2024 revision, which are consistent with the 2022 Demographic Census, for 2016–2023
[@ibge2024], and the official estimates of July 1 published in the Diário Oficial da União for 2024–2026
[@ibgedou].
"""

CLIMATE = """
Climate data came from the hourly records of the automatic weather stations of the Brazilian National Institute of
Meteorology (INMET) for 2016–2026 [@inmet]. For each station and month, mean air temperature (°C) was computed
from the hourly readings and accumulated rainfall (mm) as the sum of the hourly values, keeping only station-months
with at least 240 valid hourly temperature readings or at least 360 valid hourly rainfall readings, respectively.
Sentinel values (−9999) and temperatures outside −50 to 60 °C were set to missing. The value for each FU
and month is the unweighted mean across the stations of that FU. Climate data are available for
{n:clim.n_states_2026} of the 27 FU in 2026 (none for Roraima). To account for the delay between climatic
conditions, vector proliferation, viral incubation, and symptom onset and notification, we derived one- and two-month
lagged versions of each variable (Temp_Lag1, Temp_Lag2, Rain_Lag1, and Rain_Lag2) [@r13,@r16] as shifts within the
monthly series of each FU. Official boundary polygons of the 27 FU were obtained from the IBGE territorial mesh and
stored in GeoJSON format. Identifiers were harmonized across data sources using IBGE numerical codes and a
name-to-abbreviation lookup table, so that the epidemiological, climatic, and geographical layers could be joined
using a single state-level key.
"""

VARIABLES = """
Data were stratified by calendar year, calendar month, FU, macro-region, sex, and age group. Age bands followed the
SINAN standard reporting structure (<1, 1–4, 5–9, 10–14, 15–19, 20–39, 40–59, 60–64,
65–69, 70–79, and ≥80 years). Clinical and laboratory variables included {c21}the dengue NS1 antigen
result (labeled “ELISA” in Figure 7A) and the IgM serology result{/c21} (positive, negative, inconclusive,
or not performed), final classification (confirmed, discarded, inconclusive, and under investigation), confirmation
criterion (laboratory or clinical-epidemiological), clinical outcome, and hospitalization. Dengue cases were
additionally stratified by serotype (DENV-1 to DENV-4), and Zika cases by pregnancy status and trimester. The
clinical and demographic figures (Figures 5, 7, and 8) were built from tables that end in 2025, and therefore refer
to 2016–2025 for dengue and Zika and to 2017–2025 for chikungunya.
"""

SPATIAL = """
Spatial analyses were performed at the FU level using the population-weighted mean annual incidence over
2016–2026, with 2026 annualized. Spatial weights were defined as row-standardized k-nearest-neighbor weights
(k = 5) computed from the centroids of the FU polygons (planar longitude–latitude coordinates). Global spatial
autocorrelation was assessed using Moran’s I test [@r60], with inference based on 999 random permutations with a
fixed seed. Local spatial autocorrelation was assessed using the Local Moran’s I test (Local Indicator of
Spatial Association [LISA]) [@r61] with 999 permutations, and units with p < 0.05 were classified as high–high
(hotspot), low–low (cold spot), high–low, or low–high (spatial outliers); the classification after
Benjamini–Hochberg correction across the 27 FU is also reported. Mean incidence was mapped as one symbol per FU
and disease, filled by the natural-breaks (Jenks) class of the mean annual incidence, computed separately for each
disease. Year-by-year maps, LISA cluster maps, and maps of Mann–Kendall trend categories were also produced.
"""

REGRESSION = """
Generalized linear models (GLMs) with a log link were fitted to monthly case counts for each arbovirus, with the
logarithm of the resident population as an offset so that coefficients could be interpreted as incidence rate
ratios (IRRs). Calendar-month fixed effects absorbed the seasonal cycle, so that the climatic coefficients describe
departures from the usual seasonal pattern. Poisson, quasi-Poisson, and negative binomial (NB2) models were fitted
[@r62]. {c22}Overdispersion was quantified by the Pearson dispersion statistic of the Poisson fit and by the
maximum-likelihood estimate of the NB2 dispersion parameter α, and the models were compared with the Akaike
information criterion (AIC); no formal test of α > 0 was performed.{/c22} Inference is based on the NB2 models, which
had the lowest AIC in all three series. Three specifications were fitted: (1) a pooled model including concurrent
mean temperature and accumulated rainfall, with FU and calendar-month fixed effects and standard errors clustered by
FU; (2) per-FU models fitting the same two covariates separately for each FU, with calendar-month fixed effects and
heteroskedasticity- and autocorrelation-consistent (Newey–West, three lags) standard errors; and (3) per-FU lagged
models, in which concurrent temperature and rainfall and their one- and two-month lags entered jointly, without a lag
constraint. IRRs are reported per 1 °C increase in temperature and {c23}per 100 mm increase in rainfall{/c23} (about one
standard deviation of monthly rainfall, {n:clim.rain_sd:d0} mm), with 95% Wald confidence intervals.
Benjamini–Hochberg q-values were computed within each disease and model term across the 27 FU. A supplementary
distributed-lag non-linear model (DLNM) [@r50] was fitted as a pooled NB2 model with FU and calendar-month fixed
effects, a natural-spline exposure–response function (four degrees of freedom for temperature and three for
rainfall), and a linear lag–response over lags 0–2.
"""

SOFTWARE = """
All analyses were performed in R 4.6.1, using data.table and readxl (data handling), sf and spdep (geographical
data, nearest-neighbor weights, and spatial statistics), classInt (Jenks classification), and ggplot2 and patchwork
(visualization). The Mann–Kendall test, Sen’s slope, Spearman tests, and the GLM engine were implemented in the project code. The clinical and demographic panels (Figures 5, 7, and 8) were drawn in R from
tables prepared in GraphPad Prism (version 8.0.1). All tests were two-sided with α = 0.05. Raw p-values are
reported together with Benjamini–Hochberg q-values, and state-level results are interpreted as exploratory.
Permutation tests and bootstrap resampling used fixed seeds. The code and derived datasets are available as described
in the Data Availability Statement.
"""

METHODS = [
    B("H1", "2 | MATERIALS AND METHODS"),
    B("H2", "2.1 | Study design and setting"),
    B("Body", strip_runin(O(73,
        ("the 27 Brazilian FU (26 states", "the 27 Brazilian federative units (FU; 26 states"),
        ("to December 31^st^, 2025.", "to September 30^th^, 2026 ({n:n_months:i} months; {q:ann2026}2026 covers January to September{/q}, "
                                       "the period available in the SINAN release of October 6, 2026)."))), orig=[73], strip=True),
    B("H2", "2.2 | Epidemiological data"),
    B("Body", EPI, orig=[75], strip=True),
    B("H2", "2.3 | Meteorological and geographical data"),
    B("Body", CLIMATE, orig=[77], strip=True),
    B("H2", "2.4 | Variables"),
    B("Body", VARIABLES, orig=[79], strip=True),
    B("H2", "2.5 | Descriptive analysis"),
    B("Body", strip_runin(O(81,
        ("Annual incidence per 100,000 inhabitants was calculated for each arbovirus and FU.",
         "Annual incidence per 100,000 inhabitants was calculated for each arbovirus and FU; incidence for 2026, which covers "
         "January to September, was annualized as the cases reported multiplied by 12 and divided by the number of months "
         "reported."),
        ("which is equivalent to a population-weighted mean of state-level rates.",
         "which is equivalent to a population-weighted mean of state-level rates. The mean annual incidence of each FU is "
         "the population-weighted mean of its annual values for 2016–2026."),
        ("1,000 bootstrap samples were drawn with replacement", "1,000 bootstrap samples (fixed seed) were drawn with replacement"))),
      orig=[81], strip=True),
    B("H2", "2.6 | Temporal trend analysis"),
    B("Body", strip_runin(O(83,
        ("requiring a minimum of four annual observations.",
         "requiring a minimum of four annual observations (11 annual values for 2016–2026, with 2026 annualized)."),
        ("at α = 0.05.", "at α = 0.05; Benjamini–Hochberg q-values across the 27 FU were also computed for each "
                              "disease."))), orig=[83], strip=True),
    B("H2", "2.7 | Climatic correlation analysis"),
    B("Body", strip_runin(O(85,
        ("together with the proportion of states reaching statistical significance.",
         "together with the proportion of states reaching statistical significance (raw p < 0.05). Benjamini–Hochberg "
         "q-values were computed within each virus and climatic variable across the 81 state–lag tests."),
        ("A complementary lag-profile analysis at the macro-regional level identified the lag at which each climatic variable "
         "showed the strongest correlation with incidence.",
         "A complementary lag-profile analysis described the mean ρ by macro-region and lag."))),
      orig=[85], strip=True),
    B("H2", "2.8 | Spatial analysis"),
    B("Body", SPATIAL, orig=[87], strip=True),
    B("H2", "2.9 | Regression modelling of climatic variables"),
    B("Body", REGRESSION, orig=[89], strip=True),
    B("H2", "2.10 | Software"),
    B("Body", SOFTWARE, orig=[91], strip=True),
]
