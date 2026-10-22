# JMV compliance checklist, open decisions, and removed text

Written 2026-10-21 for `Alves ER et al JMV 2026.docx`.

**Status of the rules.** Wiley's author-guideline pages returned HTTP 403 to every automated request, and the search snippets that could be read disagree with each other. Every rule below marked **UNVERIFIED** was applied from common JMV/Wiley practice and the snippets, and must be checked on the live page (Journal of Medical Virology → Author Guidelines, https://onlinelibrary.wiley.com/page/journal/10969071/homepage/forauthors.html) before submission. The draft file name says "JVI"; its layout was that of ASM's *Journal of Virology*, not JMV.

## 1. Rules and how they were applied

| Item | Applied | Status |
|---|---|---|
| Article type | Original (research) article; retrospective ecological study of routinely collected data | author's choice |
| Abstract | One unstructured paragraph, no references, 197 words | UNVERIFIED limit: 200 (one source) or 250 (another); 197 words satisfies both |
| Keywords | 5 | UNVERIFIED: "3–6" and "up to 5" both appear |
| Main-text length | 6,274 words (Introduction to Conclusion, body paragraphs) | UNVERIFIED limit 4,000 words for a Research Article. **Over the limit.** The draft had about 4,800. Cutting is the authors' decision; not done |
| References | 70 (62 from the draft + 8 new) | UNVERIFIED limit 50. **Over.** Not cut |
| Reference style | Numbered by first citation; NLM/AMA entries (`Authors. Title. Journal. Year;vol(issue):pages.`); more than 6 authors → first 3 + et al; superscript in-text numbers (one character style, `Citation Reference`, switches this) | UNVERIFIED (snippets say AMA-based) |
| Section order | 1 Introduction, 2 Materials and Methods, 3 Results, 4 Discussion, 5 Conclusion; numbered headings in the form `1 | INTRODUCTION`, `2.1 | Title` | UNVERIFIED (Wiley template convention); the draft had ASM order with Methods last |
| IMPORTANCE statement | Removed (ASM-only). Verbatim text in section 3 below | applied |
| Title page | Title, running title, authors, affiliations, two corresponding authors, ORCID iDs (placeholder), funding (placeholder), word counts | running-title length UNVERIFIED |
| Back matter | Author contributions, Acknowledgments, Funding, Conflict of interest, Data availability, Ethics, Supporting information | placeholders for what only the authors can state |
| Page layout | Times New Roman 12 pt, double spacing, 1-inch margins, US Letter, continuous line numbers (kept from the draft), page numbers | UNVERIFIED (A4?); the "St. Jude - Confidential" footers were never enabled and are removed |
| Figures | Separate files, never embedded; legends after the references, in figure order (Figures 1–8, S1–S7) | file format and resolution UNVERIFIED (see section 4) |
| Tables | None |  |
| Reporting guideline | RECORD (STROBE extension), cited in Methods; checklist in `RECORD_CHECKLIST.md` | UNVERIFIED whether JMV requires the checklist |
| Generative-AI disclosure | Not stated in the manuscript | UNVERIFIED: publisher policies usually ask authors to disclose AI-assisted work; the authors decide the wording |
| Submission route | Not applicable | UNVERIFIED: JMV may accept a free-format first submission, with formatting required at revision |

## 2. Placeholders still in the manuscript (highlighted yellow)

- ORCID iDs of all authors
- Funding information (title page and the FUNDING section)
- Author contributions
- Acknowledgments
- Conflict of interest statement
- DOI for the repository (none issued; confirm the repository is public)
- Wording of the Supporting Information sentence

## 3. Text removed or replaced

**IMPORTANCE block (ASM only), verbatim from the draft.** It contains claims that the regenerated results no longer support (a southward expansion of chikungunya; a lagged temperature association shared by the three viruses):

> Dengue, chikungunya, and Zika remain among the most important public health threats in Brazil, and their geographic distribution is shifting as temperatures rise and cities expand. This study is one of the few nationwide comparisons of the three arboviruses that uses a single analytical framework across all 27 federative units. It covers a decade that includes the 2016 Zika epidemic, the COVID-19 pandemic, and the record 2024 dengue epidemic. The three viruses follow distinct spatial, temporal, and climatic patterns despite sharing the same vector, which argues against uniform national control strategies. The study identifies expanding transmission in southern and central-western states, shows that the states with the most cases are not those with the highest incidence per capita, and finds a lagged association between temperature and incidence. Together, these findings can guide regional prioritization, support stronger laboratory surveillance, and inform climate-based early warning systems in Brazil.

## 4. Figure files (not changed)

| File | Pixels | Stored dpi |
|---|---|---|
| `Figure1_incidence_regional.png` | 1890 × 1215 | 200 |
| `Figure2_trend_analysis.png` | 1860 × 1862 | 200 |
| `Figure3_climate_correlations.png` | 1876 × 1338 | 200 |
| `Figure4_spatial_autocorrelation.png` | 3169 × 966 | 200 |
| `Figure5_demographics.png` | 3624 × 1477 | 200 |
| `Figure6_combined_map.png` | 1576 × 1411 | 200 |
| `Figure7_dengue_clinical.png` | 2771 × 1778 | 200 |
| `Figure8_chikv_zika_clinical.png` | 3660 × 1233 | 200 |
| `FigureS2_lisa_trend.png` | 3210 × 1514 | 200 |
| `FigureS1_overview.png` | 4785 × 3286 | 200 |
| `glm_fig1_pooled_climate_irr.png` | 3600 × 1500 | 300 |
| `glm_fig2_per_state_heatmap.png` | 4200 × 2700 | 300 |
| `glm_fig3_lag_profile.png` | 3600 × 1500 | 300 |
| `glm_fig4_aic_comparison.png` | 4200 × 1350 | 300 |
| `glm_fig5_forest_significant.png` | 3900 × 3300 | 300 |

Journals usually ask for TIFF or EPS at 300 dpi or more (line art at higher resolution). **UNVERIFIED for JMV.** PNG at 200–300 dpi was left as is.

## 5. Decisions for the authors

- Discarded chikungunya and Zika notifications are in the counts (comments 18–19): keep and document (as written) or rerun without them.
- Annualized 2026 enters the trends, means, Moran's I and LISA: keep, or restrict the main analyses to 2016–2025.
- Length: 6,274 words and 70 references against candidate limits of 4,000 and 50.
- Figure numbers follow the repository set; first citations are not sequential (Figure 6 before 1 and 4). Renumber or reorder if the journal requires it.
- Figure style (comment 6): no titles, legend placement, one colour per virus (for example chikungunya in green), removal of non-significant increasing/decreasing labels.
- The supplementary DLNM has no numbered figure (author query attached).
- Regenerate the figures built from the GraphPad tables (5, 7, 8) to 2026, and the former state-total and seasonal figures, if the text should match the full window.
- Interpretation changes marked ⇄ in `SYNC_LOG.md`, in particular that Zika's pooled temperature association is now positive and chikungunya's is not significant.
- Whether to report a pooled lagged model (none exists in the outputs).
- AI-use disclosure wording, ORCID, funding, contributions, conflicts, acknowledgments.

## 6. Structural changes that the redline does not track

Section reordering (Methods before Results), run-in headings turned into numbered heading styles, new styles and page layout, removal of the unused footer parts, reference renumbering and reformatting (the redline shows the text change of each entry), and the re-anchoring of comments to the rewritten sentences.
