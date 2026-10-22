import re
from msbase import B, O

ETHICS = O(93, ("This study used only secondary, anonymized, publicly available aggregate data, and no individual identifiers were accessed.",
                "This study used only secondary, publicly available, de-identified surveillance records, which were aggregated by FU "
                "and month, and no individual identifiers were accessed."))
ETHICS = re.sub(r"^\*\*Ethical considerations \*\*", "", ETHICS)

DATA_AVAIL = """
The surveillance notifications (SINAN), meteorological records (INMET), and population estimates (IBGE) analyzed in this
study are publicly available from the Brazilian federal open-data sources cited in the Methods; the SINAN 2026 files are
the release of October 6, 2026, and all raw files were downloaded and checked on October 8, 2026. The analysis code (R), the
cleaned analysis tables, the generated results, and the source data behind each figure are available at
https://github.com/eduramosalves/arbovirus-surveillance-brazil-r (MIT license; version 1.0.0). The raw files (about
1.7 GB) are not stored in the repository; a manifest with the size and SHA-256 checksum of each file used is provided.
{hl}A persistent identifier (DOI) for the repository has not been issued yet.{/hl}
"""

BACK = [
    B("H1", "AUTHOR CONTRIBUTIONS"),
    B("BackBody", "{hl}To be completed by the authors (contributor roles).{/hl}"),
    B("H1", "ACKNOWLEDGMENTS"),
    B("BackBody", "{hl}To be completed by the authors.{/hl}"),
    B("H1", "FUNDING"),
    B("BackBody", "{hl}To be completed by the authors.{/hl}"),
    B("H1", "CONFLICT OF INTEREST STATEMENT"),
    B("BackBody", "{hl}To be completed by the authors.{/hl}"),
    B("H1", "DATA AVAILABILITY STATEMENT"),
    B("BackBody", DATA_AVAIL),
    B("H1", "ETHICS STATEMENT"),
    B("BackBody", ETHICS, orig=[93], strip=True),
    B("H1", "SUPPORTING INFORMATION"),
    B("BackBody", "Supplementary Figures S1–S7 and the RECORD checklist are provided as supporting information. "
                  "{hl}Wording to be adjusted to the journal’s submission system.{/hl}"),
]


def legend_blocks(path):
    """Figure legends from docs/FIGURE_CAPTIONS.md, renumbered for the manuscript."""
    text = open(path, encoding="utf-8").read()
    start = text.index("## Main figures")
    end = text.index("## Methods and limitations")
    sec = text[start:end]
    pat = re.compile(r"\*\*((?:Supplementary Figure|GLM Figure|Figure)\s+[^*]+?)\*\*\s*\n(.*?)(?=\n\n|\n---|\Z)", re.S)
    out = []
    for m in pat.finditer(sec):
        title = " ".join(m.group(1).split())
        body = " ".join(m.group(2).split())
        mg = re.match(r"GLM Figure (\d)\.", title)
        if mg:
            title = "Supplementary Figure S%d." % (int(mg.group(1)) + 2) + title[mg.end():]
        body = re.sub(r"\s*Files: .*$", "", body)
        body = body.replace("`", "")
        for o, n in [("hospitalisation", "hospitalization"), ("standardised", "standardized"), ("coloured", "colored"),
                     ("neighbour", "neighbor"), ("annualised", "annualized"), ("colour", "color"),
                     ("Mann-Kendall Kendall\u2019s \u03c4", "Kendall\u2019s \u03c4 (Mann\u2013Kendall test)")]:
            body = body.replace(o, n)
            title = title.replace(o, n)
        body = re.sub(r"\bUFs\b", "FU", body)
        body = re.sub(r"\bUF\b", "FU", body)
        title = re.sub(r"\bUFs\b", "FU", title)
        title = re.sub(r"\bUF\b", "FU", title)
        head, _, rest = title.partition(". ")
        if head in ("Supplementary Figure S3.", "Supplementary Figure S4."):
            body += " Rainfall effects are drawn per 1 mm; the text reports them per 100 mm."
        out.append((head + ".", rest.rstrip("."), body))
    return out


# legend -> original legend paragraph (draft numbering), used only for the tracked-change comparison
LEGEND_ORIG = {"Figure 1.": 162, "Figure 2.": 172, "Figure 3.": 174, "Figure 4.": 164, "Figure 5.": 166,
               "Figure 6.": 160, "Figure 7.": 168, "Figure 8.": 170}

ABBREV = ("Abbreviations: FU, federative unit; IRR, incidence rate ratio; CI, confidence interval; FE, fixed effects; "
          "LISA, local indicator of spatial association; HH, high–high; LL, low–low; HL, high–low; LH, low–high.")


def legends(path):
    blocks = [B("H1", "FIGURE LEGENDS", orig=[159]), B("Legend", ABBREV)]
    for head, title, body in legend_blocks(path):
        orig = [LEGEND_ORIG[head]] if head in LEGEND_ORIG else []
        blocks.append(B("Legend", "**%s %s.** %s" % (head, title, body), orig=orig))
    return blocks
