# JMV compliance checklist, open decisions, and removed text

Round 1 written 2026-10-21, **updated 2026-10-22 (round 2)** for `Alves ER et al JMV 2026.docx`.

**Status of the rules.** Wiley's author-guideline pages returned HTTP 403 to every automated request, and the search snippets that could be read disagree with each other. Every rule below marked **UNVERIFIED** was applied from common JMV/Wiley practice and the snippets, and must be checked on the live page (Journal of Medical Virology → Author Guidelines, https://onlinelibrary.wiley.com/page/journal/10969071/homepage/forauthors.html) before submission. The draft file name says "JVI"; its layout was that of ASM's *Journal of Virology*, not JMV.

## 1. Rules and how they were applied

| Item | Applied | Status |
|---|---|---|
| Article type | Original (research) article; retrospective ecological study of routinely collected data | author's choice |
| Abstract | One unstructured paragraph, no references, 182 words | UNVERIFIED limit: 200 (one source) or 250 (another); 182 words satisfies both |
| Keywords | 5 | UNVERIFIED: "3–6" and "up to 5" both appear |
| Main-text length | 6,792 words (Introduction to Conclusion, body paragraphs) | UNVERIFIED limit 4,000 words for a Research Article. **Over the limit.** The draft had about 4,800 and the 2026 qualifiers added more. Cutting is the authors' decision; not done |
| References | 70 (62 from the draft + new) | UNVERIFIED limit 50. **Over.** Not cut |
| Reference style | Numbered by first citation; NLM/AMA entries (`Authors. Title. Journal. Year;vol(issue):pages.`); more than 6 authors → first 3 + et al; superscript in-text numbers (one character style, `Citation Reference`, switches this) | UNVERIFIED (snippets say AMA-based) |
| Section order | 1 Introduction, 2 Materials and Methods, 3 Results, 4 Discussion, 5 Conclusion; numbered headings in the form `1 | INTRODUCTION`, `2.1 | Title` | UNVERIFIED (Wiley template convention); the draft had ASM order with Methods last |
| IMPORTANCE statement | Removed (ASM-only). Verbatim text in section 3 below | applied |
| Title page | Title, running title, authors, affiliations, two corresponding authors, ORCID iDs (placeholder), funding (placeholder), word counts | running-title length UNVERIFIED |
| Back matter | Author contributions, Acknowledgments, Funding, Conflict of interest, Data availability, Ethics, Supporting information | placeholders for what only the authors can state |
| Page layout | Times New Roman 12 pt, double spacing, 1-inch margins, US Letter, continuous line numbers (kept from the draft), page numbers | UNVERIFIED (A4?); the "St. Jude - Confidential" footers were never enabled and are removed |
| Figures | Separate files, never embedded; legends after the references, in order of citation (Figures 1–8, S1–S7); copies under the manuscript numbers in `manuscript/figures/` | file format and resolution UNVERIFIED (see section 4) |
| Partial year 2026 | Every paragraph and legend that uses 2026 states that it covers January–September and is annualized (build check); abstract, Methods 2.1/2.5, Results, Discussion, limitations and conclusion | author instruction (comment 51), not a journal rule |
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

**Round 2.** The sentences on the distributed lag non-linear model (DLNM) were deleted from Methods 2.9, Results 3.6 and the Discussion (comment 55); the pooled lagged model replaces them.

## 4. Figure files (copies in `manuscript/figures/`; the pipeline keeps its own names)

| Manuscript file | Pixels | Stored dpi |
|---|---|---|
| `Figure1.png` | 1890 × 1215 | 200 |
| `Figure2.png` | 1576 × 1411 | 200 |
| `Figure3.png` | 3169 × 966 | 200 |
| `Figure4.png` | 1860 × 1862 | 200 |
| `Figure5.png` | 1876 × 1338 | 200 |
| `Figure6.png` | 3624 × 1432 | 200 |
| `Figure7.png` | 2775 × 1778 | 200 |
| `Figure8.png` | 3662 × 1233 | 200 |
| `FigureS1_overview.png` | 4785 × 3286 | 200 |
| `FigureS1_2016.png` | 1576 × 1411 | 200 |
| `FigureS1_2017.png` | 1576 × 1411 | 200 |
| `FigureS1_2018.png` | 1576 × 1411 | 200 |
| `FigureS1_2019.png` | 1576 × 1411 | 200 |
| `FigureS1_2020.png` | 1576 × 1411 | 200 |
| `FigureS1_2021.png` | 1576 × 1411 | 200 |
| `FigureS1_2022.png` | 1576 × 1411 | 200 |
| `FigureS1_2023.png` | 1576 × 1411 | 200 |
| `FigureS1_2024.png` | 1576 × 1411 | 200 |
| `FigureS1_2025.png` | 1576 × 1411 | 200 |
| `FigureS1_2026.png` | 1576 × 1411 | 200 |
| `FigureS2.png` | 3210 × 1514 | 200 |
| `FigureS3.png` | 4200 × 1350 | 300 |
| `FigureS4.png` | 3600 × 1500 | 300 |
| `FigureS5.png` | 4200 × 2700 | 300 |
| `FigureS6.png` | 3900 × 3300 | 300 |
| `FigureS7.png` | 3600 × 1500 | 300 |

Journals usually ask for TIFF or EPS at 300 dpi or more (line art at higher resolution). **UNVERIFIED for JMV.** PNG was left as is.

## 5. Decisions for the authors

- Length: 6,792 words and 70 references against candidate limits of 4,000 and 50.
- Interpretation changes marked ⇄ in `SYNC_LOG.md`: chikungunya's global spatial autocorrelation is now significant; Zika's pooled temperature association is positive (borderline) and chikungunya's is not significant.
- The Zika lag signal differs between the pooled lagged model (lag 1) and the per-FU lagged models (lag 2); both are reported.
- The reading of the early-2016 chikungunya classification codes (code 2 discarded, code 1 confirmed) and the missing Espirito Santo 2021 notifications need confirmation from the data source.
- 2026 is kept with its qualifier; a sensitivity analysis restricted to 2016–2025 was not run.
- Serotype value 0 (Figure 7D) and the Espirito Santo counts: the author queries are still open.
- AI-use disclosure wording, ORCID, funding, contributions, conflicts, acknowledgments.
- Galileu's threads were answered but left open for him to close.

## 6. Structural changes that the redline does not track

Section reordering (Methods before Results), run-in headings turned into numbered heading styles, new styles and page layout, removal of the unused footer parts, reference renumbering and reformatting (the redline shows the text change of each entry), figure renumbering by order of citation, and the re-anchoring of comments to the rewritten sentences.
