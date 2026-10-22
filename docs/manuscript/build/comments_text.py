"""Replies to the 20 original co-author comments and new author queries (author 'Claude for ERA')."""

# original comment id -> reply text (None = no reply)
REPLIES = {
    3: "All incidence values in the text were recomputed from the regenerated 2016–2026 outputs and are logged with their "
       "source file in docs/manuscript/SYNC_LOG.md. Rankings changed: Goiás (1,782.4 per 100,000) now exceeds the Federal "
       "District (1,693.7) once 2026 (annualized) is included.",
    4: "Moran’s I now comes from one source (outputs/geo_spatial_stats.xlsx, sheet Global_Moran): dengue 0.516 (p = 0.001), "
       "chikungunya 0.004 (p = 0.285), Zika −0.006 (p = 0.326). The same values appear in the text and in the legends of "
       "Figures 4 and 6. The earlier 0.562, −0.036 and −0.008 came from the previous Python run and cannot be reproduced "
       "from the current data.",
    5: "Figure numbers now follow the repository set (Figures 1–8; Supplementary Figures S1–S2; the five GLM figures are "
       "renamed S3–S7). The order of first citation in the text is not sequential (Figure 6 is cited before Figures 1 and 4). "
       "Renumbering or reordering is left to the authors if the journal requires sequential citation.",
    6: "Not changed: this is figure work, outside this edit. The regenerated figures carry no in-plot titles. The colour code per "
       "virus (for example CHIKV in green) and the removal of non-significant increasing/decreasing labels remain to be decided.",
    7: "Updated: the Mann–Kendall figure is now Figure 2.",
    8: "Updated: the trend map is now Figure S2B and the Mann–Kendall figure is Figure 2.",
    9: "Described in Section 3.1: the Central-West reached 702.5 per 100,000 in 2025 (Mato Grosso do Sul 1,726 and Mato Grosso "
       "1,709). In the SINAN series used here, chikungunya incidence is highest nationally in 2024 (200.5) and second in 2016 "
       "(155.3); 2016 is now included. The Ministry of Health data mentioned are not part of this project, so the statement "
       "that 2016 exceeded 2024 could not be checked.",
    11: "Updated: the Spearman correlations are now Figure 3.",
    12: "Added: 800,258 men (data of Figure 5B, 2017–2025).",
    13: "Corrected. 5,145,984 is the number of notifications with ignored or blank hospitalization status, not a separate count "
        "of non-hospitalized patients: 529,203 hospitalized + 10,642,808 not hospitalized + 5,145,984 ignored/blank = "
        "16,317,995 dengue notifications. Hospitalization is now reported among those with known status (4.7%).",
    14: "Filled from the tables behind Figure 7D (2016–2025): DENV-2, 117,958; DENV-3, 8,766; DENV-4, 747. Serotype is missing in "
        "97.9% of the notifications.",
    15: "The missing reference is now Figures S4 (per-FU estimates) and S7 (significant per-FU estimates).",
    16: "Agreed on both points. The lagged model is per FU and unconstrained (lags 0–2 entered jointly); no pooled lagged model "
        "exists in the outputs, and it is not a DLNM. Methods and Results now say so. A separate pooled DLNM with a linear "
        "lag–response over lags 0–2 is reported as a supplementary analysis.",
    17: "Clarified: Section 2.2 gives the national definition (RT-PCR, NS1 antigen, IgM/IgG ELISA, or clinical-epidemiological "
        "criterion), and Section 2.4 lists the results actually analyzed: the NS1 antigen and IgM serology results shown in "
        "Figure 7. RT-PCR results exist in the clinical tables but are not plotted.",
    18: "Left open for the authors. The pipeline counts dengue as probable cases (all notifications except discarded); the Methods "
        "now state this. Restricting the analyses to confirmed cases would change every incidence, trend, Moran and GLM "
        "result and requires rerunning the pipeline.",
    19: "Documented, not changed. Dengue excludes discarded notifications; chikungunya and Zika include all notifications, "
        "discarded ones too (700,721 chikungunya and 252,266 Zika in the tables behind the figures), so your reading is right. "
        "The Methods now say so. Excluding them needs a pipeline rerun (the Zika discard code is 2, not 5, and chikungunya 2016 "
        "has 102,858 records with legacy classification codes). Decision for the authors.",
    20: "IBGE, not SINAN: Population Projections (2024 revision) for 2016–2023 and the official 1 July estimates published in "
        "the DOU for 2024–2026. References added.",
    21: "Clarified: Figure 7A is the dengue NS1 antigen result and Figure 7B the IgM serology result. This was established by "
        "matching yearly counts with the SINAN fields, not from the GraphPad labels; please confirm.",
    22: "Corrected. No formal test of α > 0 was run, and the NB2 parameter α is not the quasi-Poisson φ. The Methods now report "
        "the Pearson dispersion of the Poisson fit and the maximum-likelihood estimate of α, and state that no formal test was "
        "performed. A likelihood-ratio test could be added from the log-likelihoods in glm_negbin_results.xlsx.",
    23: "Done: rainfall is reported per 100 mm (about one SD of monthly rainfall), an exact transformation of the exported "
        "coefficient. Note that the rebuilt INMET rainfall (about 115 mm/month) is not on the scale of the original series, "
        "so the per-mm IRRs of the earlier draft are not comparable.",
}

# new author queries: key -> text
QUERIES = {
    "code0": "Figure 7D folds the SINAN serotype value 0 (not a valid serotype; 134,407 records in 2023) into “Ign/Blank”. "
             "Please confirm this treatment and describe it in the Methods if it is kept.",
    "dlnm": "The supplementary DLNM has no numbered figure. Add outputs/2026-10-08/additional/dlnm_exposure_response.png as a "
            "supplementary figure, or delete this sentence.",
    "esdata": "docs/FIGURE_CAPTIONS.md quotes 2,901 chikungunya and 872 Zika cases reported by Espírito Santo for January–October "
              "2021, but the cited page could not be read, so the numbers were left out. Please verify them (or cite the SESA-ES "
              "bulletin) before adding them.",
    "ann2026": "2026 is annualized as cases × 12 / months reported. This inflates 2026 because October–December carry a small "
               "share of annual cases (see Discussion), and 2026 enters the trends, mean incidence, Moran’s I and LISA. "
               "Decide whether to keep 2026 in these analyses.",
}

AUTHOR = "Claude for ERA"
INITIALS = "C"
