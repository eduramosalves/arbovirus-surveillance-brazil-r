import re
from msbase import B, O

ETHICS = O(93, ("This study used only secondary, anonymized, publicly available aggregate data, and no individual identifiers were accessed.",
                "This study used only secondary, publicly available, de-identified surveillance records, which were aggregated by FU "
                "and month, and no individual identifiers were accessed."))
ETHICS = re.sub(r"^\*\*Ethical considerations \*\*", "", ETHICS)

DATA_AVAIL = """
The surveillance notifications (SINAN), meteorological records (INMET), and population estimates (IBGE) analyzed in this
study are publicly available from the Brazilian federal open-data sources cited in the Methods. The SINAN files were
downloaded from OpenDataSUS on {n:meta.sinan_access:s}; the 2026 files are the release of {n:meta.sinan_release:s}, from which
only notifications dated up to September 30, 2026 were used. The analysis code (R), the cleaned analysis tables, the
generated results, and the source data behind each figure are available at
https://github.com/eduramosalves/arbovirus-surveillance-brazil-r (MIT license). The raw files (about 1.7 GB) are not stored
in the repository; a manifest with the size and SHA-256 checksum of each file used is provided.
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
    B("BackBody", "Supplementary Figures {f:first_supp}–{f:last_supp} and the RECORD checklist are provided as supporting "
                  "information. {hl}Wording to be adjusted to the journal’s submission system.{/hl}"),
]

_HEAD = re.compile(r"\*\*((?:Supplementary Figure|GLM Figure|Figure)\s+[^*]+?)\*\*\s*\n(.*?)(?=\n\n|\n---|\Z)", re.S)
_FIXES = [("hospitalisation", "hospitalization"), ("standardised", "standardized"), ("coloured", "colored"),
          ("neighbour", "neighbor"), ("annualised", "annualized"), ("colour", "color"),
          ("Mann-Kendall Kendall’s τ", "Kendall’s τ (Mann–Kendall test)")]


def legend_blocks(path):
    """Figure legends of manuscript/FIGURE_CAPTIONS.md as (repository label, title, body); the repository label is the
    heading used there ('Figure 6', 'GLM Figure 3')."""
    text = open(path, encoding="utf-8").read()
    sec = text[text.index("## Main figures"):text.index("## Methods and limitations")]
    out = []
    for m in _HEAD.finditer(sec):
        title = " ".join(m.group(1).split())
        body = " ".join(m.group(2).split())
        body = re.sub(r"\s*Files: .*$", "", body).replace("`", "")
        for o, n in _FIXES:
            body, title = body.replace(o, n), title.replace(o, n)
        body, title = re.sub(r"\bUFs?\b", "FU", body), re.sub(r"\bUFs?\b", "FU", title)
        head, _, rest = title.partition(". ")
        if head in ("GLM Figure 1", "GLM Figure 2"):
            body += " Rainfall effects are drawn per 1 mm; the text reports them per 100 mm."
        out.append((head, rest.rstrip("."), body))
    return out


# repository legend label -> paragraph of the draft's legend, used only for the tracked-change comparison
LEGEND_ORIG = {"Figure 1": 162, "Figure 2": 172, "Figure 3": 174, "Figure 4": 164, "Figure 5": 166,
               "Figure 6": 160, "Figure 7": 168, "Figure 8": 170}

ABBREV = ("Abbreviations: FU, federative unit; IRR, incidence rate ratio; CI, confidence interval; FE, fixed effects; "
          "LISA, local indicator of spatial association; HH, high–high; LL, low–low; HL, high–low; LH, low–high.")


def legends(path, num):
    """Legend blocks in manuscript order (main figures, then supplementary) with the manuscript numbers; `num` maps
    figure keys to numbers (figmap.numbering)."""
    import figmap
    items = []
    for head, title, body in legend_blocks(path):
        key = figmap.LABEL_TO_KEY[head]
        if key not in num:
            raise KeyError("there is a legend for %s but the figure is never cited in the text" % head)
        items.append((key, head, title, figmap.renumber_legend_refs(body, num)))
    items.sort(key=lambda it: (num[it[0]].startswith("S"), int(num[it[0]].lstrip("S"))))
    blocks = [B("H1", "FIGURE LEGENDS", orig=[159]), B("Legend", ABBREV)]
    for key, head, title, body in items:
        label = ("Supplementary Figure " if num[key].startswith("S") else "Figure ") + num[key]
        blocks.append(B("Legend", "**%s. %s.** %s" % (label, title, body), orig=[LEGEND_ORIG[head]] if head in LEGEND_ORIG else []))
    return blocks
