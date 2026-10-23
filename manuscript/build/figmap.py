"""Figures of the manuscript: repository numbering -> keys. The manuscript number of a figure is the order of
its first citation in the text (main and supplementary figures are numbered separately).

In the text a figure is cited as {F:key} -> "Figure 3", {F:key:A} -> "Figure 3A", {f:key} -> "3" (number only),
{f:key:B} -> "3B". Supplementary figures read "Figure S2".
"""
import re

# key: (label used by docs/FIGURE_CAPTIONS.md, supplementary?, repository files)
FIGURES = {
    "incid":   ("Figure 1", False, ["Figure1_incidence_regional.png"]),
    "trend":   ("Figure 2", False, ["Figure2_trend_analysis.png"]),
    "corr":    ("Figure 3", False, ["Figure3_climate_correlations.png"]),
    "moran":   ("Figure 4", False, ["Figure4_spatial_autocorrelation.png"]),
    "demo":    ("Figure 5", False, ["Figure5_demographics.png"]),
    "map":     ("Figure 6", False, ["Figure6_combined_map.png"]),
    "dengue":  ("Figure 7", False, ["Figure7_dengue_clinical.png"]),
    "chikzika": ("Figure 8", False, ["Figure8_chikv_zika_clinical.png"]),
    "s_annual": ("Supplementary Figure S1", True, ["FigureS1_overview.png"] + ["FigureS1_%d.png" % y for y in range(2016, 2027)]),
    "s_lisa":  ("Supplementary Figure S2", True, ["FigureS2_lisa_trend.png"]),
    "glm_pooled": ("GLM Figure 1", True, ["glm_fig1_pooled_climate_irr.png"]),
    "glm_state": ("GLM Figure 2", True, ["glm_fig2_per_state_heatmap.png"]),
    "glm_lag": ("GLM Figure 3", True, ["glm_fig3_lag_profile.png"]),
    "glm_aic": ("GLM Figure 4", True, ["glm_fig4_aic_comparison.png"]),
    "glm_forest": ("GLM Figure 5", True, ["glm_fig5_forest_significant.png"]),
}
LABEL_TO_KEY = {v[0]: k for k, v in FIGURES.items()}

SPECIAL = ("first_supp", "last_supp")   # {f:first_supp} / {f:last_supp}: first and last supplementary figure numbers
TOKEN = re.compile(r"\{([Ff]):([a-z0-9_]+)(?::([A-Z]))?\}")


def cited_order(texts):
    """Keys in order of first citation over the given texts (in document order)."""
    seen = []
    for t in texts:
        for m in TOKEN.finditer(t):
            if m.group(2) in SPECIAL:
                continue
            if m.group(2) not in FIGURES:
                raise KeyError("unknown figure key %r" % m.group(2))
            if m.group(2) not in seen:
                seen.append(m.group(2))
    return seen


def numbering(order):
    """key -> manuscript label ('1', '2', ..., 'S1', ...) from the order of first citation."""
    num, main_n, supp_n = {}, 0, 0
    for k in order:
        if FIGURES[k][1]:
            supp_n += 1
            num[k] = "S%d" % supp_n
        else:
            main_n += 1
            num[k] = str(main_n)
    return num


def resolve(text, num):
    def rep(m):
        kind, key, panel = m.groups()
        if key in SPECIAL:
            supp = [v for v in num.values() if v.startswith("S")]
            return "S1" if key == "first_supp" else "S%d" % len(supp)
        label = num[key] + (panel or "")
        return ("Figure " + label) if kind == "F" else label
    return TOKEN.sub(rep, text)


_LEGEND_REF = re.compile(r"(Supplementary Figure S\d+|GLM Figure \d+|Figure \d+)")


def renumber_legend_refs(text, num):
    """Rewrite the repository figure labels quoted inside a legend ('Symbols as in Figure 6') to the manuscript numbers."""
    def rep(m):
        key = LABEL_TO_KEY.get(m.group(1))
        if key is None:
            return m.group(1)
        return "Figure " + num[key]
    return _LEGEND_REF.sub(rep, text)
