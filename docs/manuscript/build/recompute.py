"""Independent recomputation of headline numbers (second code path: Python/numpy from the repo's db/ and source tables).
Compares each value with the text of the built manuscript. Usage: python recompute.py <clean.docx>"""
import csv
import json
import math
import re
import sys
import zipfile
from collections import defaultdict
from xml.etree import ElementTree as ET

import numpy as np

ROOT = "C:/Users/Usuario/arbovirus-surveillance-brazil-r-eduardo/"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

doc = zipfile.ZipFile(sys.argv[1])
root = ET.fromstring(doc.read("word/document.xml"))
TEXT = "\n".join("".join(t.text or "" for t in p.iter(W + "t")) for p in root.iter(W + "p"))
results = []


def check(label, value_str, ctx=None):
    found = value_str in TEXT
    results.append(found)
    print(("PASS " if found else "FAIL ") + label + " -> " + value_str)


def fmt_i(x):
    return "{:,.0f}".format(x)


# ---------- minimal xlsx reader
def read_xlsx(path, sheet):
    z = zipfile.ZipFile(path)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = None
    for s in wb.find("m:sheets", NS):
        if s.get("name") == sheet:
            rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    target = [r.get("Target") for r in rels if r.get("Id") == rid][0].lstrip("/")
    target = target if target.startswith("xl/") else "xl/" + target
    sst = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            sst.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    rows = []
    for row in ET.fromstring(z.read(target)).find("m:sheetData", NS):
        vals = {}
        for c in row:
            ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
            v = c.find("m:v", NS)
            if v is None:
                is_ = c.find("m:is", NS)
                vals[ref] = "".join(t.text or "" for t in is_.iter("{%s}t" % NS["m"])) if is_ is not None else None
            elif c.get("t") == "s":
                vals[ref] = sst[int(v.text)]
            else:
                vals[ref] = v.text
        rows.append(vals)
    hdr = rows[0]
    return [{hdr[k]: v for k, v in r.items() if k in hdr} for r in rows[1:]]


# ---------- data
loc = {r["Location_ID"]: r["State_Code"] for r in csv.DictReader(open(ROOT + "db/normalized_dim_location.csv", encoding="utf-8"))}
pop = {(r["Location_ID"], int(r["Year"])): float(r["Population"]) for r in csv.DictReader(open(ROOT + "db/normalized_fact_population.csv"))}
cases = defaultdict(float)       # (disease, uf, year, month) -> n
for r in csv.DictReader(open(ROOT + "db/normalized_fact_cases.csv")):
    cases[(r["Disease"], loc[r["Location_ID"]], int(r["Year"]), int(r["Month"]))] += float(r["Cases"])
uf_id = {v: k for k, v in loc.items()}
months_rep = defaultdict(set)
for (d, u, y, m) in cases:
    months_rep[(d, u, y)].add(m)

# 1-2 totals
for d, exp in (("DENV", None), ("CHIKV", None), ("ZIKV", None)):
    tot = sum(v for (dd, u, y, m), v in cases.items() if dd == d)
    check("total cases 2016-2026 %s" % d, fmt_i(tot))
check("dengue cases 2024", fmt_i(sum(v for (d, u, y, m), v in cases.items() if d == "DENV" and y == 2024)))
check("Zika cases 2016", fmt_i(sum(v for (d, u, y, m), v in cases.items() if d == "ZIKV" and y == 2016)))
for d, u in (("DENV", "SP"), ("DENV", "MG"), ("CHIKV", "MG"), ("ZIKV", "RJ")):
    check("state total %s %s" % (d, u), fmt_i(sum(v for (dd, uu, y, m), v in cases.items() if dd == d and uu == u)))


# 3-4 national annual incidence
def nat_inc(d, y):
    c = sum(v for (dd, u, yy, m), v in cases.items() if dd == d and yy == y)
    p = sum(pop[(uf_id[u], y)] for u in loc.values())
    return c / p * 1e5


check("dengue 2024 incidence", fmt_i(nat_inc("DENV", 2024)))
check("Zika 2016 incidence", fmt_i(nat_inc("ZIKV", 2016)))
check("chikungunya 2024 incidence", "{:.1f}".format(nat_inc("CHIKV", 2024)))
check("chikungunya 2016 incidence", "{:.1f}".format(nat_inc("CHIKV", 2016)))


# annual state incidence with 2026 annualized
def annual_inc(d, u, y):
    c = sum(cases.get((d, u, y, m), 0) for m in range(1, 13))
    mr = len(months_rep.get((d, u, y), ()))
    if mr == 0:
        return None
    return c * 12.0 / mr / pop[(uf_id[u], y)] * 1e5


def mean_inc(d, u):
    num = den = 0.0
    for y in range(2016, 2027):
        v = annual_inc(d, u, y)
        if v is not None:
            p = pop[(uf_id[u], y)]
            num += v * p
            den += p
    return num / den


check("mean annual incidence GO dengue", "{:,.1f}".format(mean_inc("DENV", "GO")))
check("mean annual incidence DF dengue", "{:,.1f}".format(mean_inc("DENV", "DF")))
check("mean annual incidence MS chikungunya", "{:,.1f}".format(mean_inc("CHIKV", "MS")))
check("mean annual incidence TO Zika", "{:,.1f}".format(mean_inc("ZIKV", "TO")))

# 5 Mann-Kendall + Sen (dengue RS, chikungunya MS)
def mk(series):
    n = len(series)
    s = sum(np.sign(series[j] - series[i]) for i in range(n - 1) for j in range(i + 1, n))
    ties = defaultdict(int)
    for v in series:
        ties[v] += 1
    n0 = n * (n - 1) / 2
    n1 = sum(t * (t - 1) / 2 for t in ties.values())
    tau = s / math.sqrt(n0 * n0 - n1 * n0) if n1 else s / n0
    slopes = [(series[j] - series[i]) / (j - i) for i in range(n - 1) for j in range(i + 1, n)]
    return tau, float(np.median(slopes))


for d, u in (("DENV", "RS"), ("CHIKV", "MS")):
    ser = [annual_inc(d, u, y) for y in range(2016, 2027)]
    tau, sl = mk(ser)
    check("Mann-Kendall tau %s %s" % (d, u), "{:.3f}".format(tau))
    check("Sen slope %s %s" % (d, u), "{:.0f}".format(sl))

# 6 Spearman dengue MG temperature lag 2
clim = {}
for r in csv.DictReader(open(ROOT + "db/normalized_fact_climate.csv")):
    clim[(loc[r["Location_ID"]], int(r["Year"]), int(r["Month"]))] = r


def rank(a):
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a))
    ranks[order] = np.arange(len(a))
    for v in set(a):
        idx = [i for i, x in enumerate(a) if x == v]
        if len(idx) > 1:
            ranks[idx] = np.mean(ranks[idx])
    return ranks


def spearman(d, u, col):
    xs, ys = [], []
    for (dd, uu, y, m), c in sorted(cases.items()):
        if dd != d or uu != u:
            continue
        cr = clim.get((u, y, m))
        if cr is None or cr[col] in ("", None):
            continue
        xs.append(c / pop[(uf_id[u], y)] * 1e5)
        ys.append(float(cr[col]))
    return float(np.corrcoef(rank(xs), rank(ys))[0, 1])


check("Spearman dengue MG temperature lag 2", "{:.3f}".format(spearman("DENV", "MG", "Temp_Lag2")))
check("Spearman dengue RJ temperature lag 2", "{:.3f}".format(spearman("DENV", "RJ", "Temp_Lag2")))
mean_l2 = np.mean([spearman("DENV", u, "Temp_Lag2") for u in loc.values()])
check("mean Spearman dengue temperature lag 2", "{:.3f}".format(mean_l2))
mean_r2 = np.mean([spearman("CHIKV", u, "Rain_Lag2") for u in loc.values()])
check("mean Spearman chikungunya rainfall lag 2", "{:.3f}".format(mean_r2))

# 7 Moran's I dengue (kNN k=5 on planar polygon centroids)
gj = json.load(open(ROOT + "db/brazil_states.geojson", encoding="utf-8")) if False else json.load(open(ROOT + "reference/brazil_states.geojson", encoding="utf-8"))


def ring_cent(r):
    r = np.array(r)
    x, y = r[:, 0], r[:, 1]
    a = x[:-1] * y[1:] - x[1:] * y[:-1]
    A = a.sum() / 2
    return A, ((x[:-1] + x[1:]) * a).sum() / (6 * A), ((y[:-1] + y[1:]) * a).sum() / (6 * A)


def geom_centroid(g):
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    A = cx = cy = 0.0
    for poly in polys:
        for k, ring in enumerate(poly):
            a, x, y = ring_cent(ring)
            sgn = 1 if k == 0 else -1
            a = abs(a) * sgn
            A += a; cx += a * x; cy += a * y
    return cx / A, cy / A


names = {}
cent = {}
for f in gj["features"]:
    p = f["properties"]
    IBGE = {"11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO", "21": "MA", "22": "PI", "23": "CE",
            "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA", "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
            "41": "PR", "42": "SC", "43": "RS", "50": "MS", "51": "MT", "52": "GO", "53": "DF"}
    cent[IBGE[p["codarea"]]] = geom_centroid(f["geometry"])
ufs = sorted(u for u in cent if u in loc.values())
if len(ufs) == 27:
    pts = np.array([cent[u] for u in ufs])
    n = len(ufs)
    Wm = np.zeros((n, n))
    for i in range(n):
        d2 = ((pts - pts[i]) ** 2).sum(1)
        d2[i] = np.inf
        for j in np.argsort(d2)[:5]:
            Wm[i, j] = 1 / 5
    z = np.array([mean_inc("DENV", u) for u in ufs]); z = z - z.mean()
    I = float((Wm * np.outer(z, z)).sum() / (z ** 2).sum())
    check("global Moran's I dengue (kNN k=5)", "{:.3f}".format(I))
    for d in ("CHIKV", "ZIKV"):
        z = np.array([mean_inc(d, u) for u in ufs]); z = z - z.mean()
        check("global Moran's I %s" % d, "{:.3f}".format(float((Wm * np.outer(z, z)).sum() / (z ** 2).sum())).replace("-", "\u2212"))
else:
    print("SKIP Moran: could not map %d state polygons" % len(ufs))

# 8 pooled GLM: Poisson and NB (alpha fixed at the exported ML value) with state + month FE and population offset
rowsD = []
for (dd, u, y, m), c in sorted(cases.items()):
    if dd != "DENV":
        continue
    cr = clim.get((u, y, m))
    if cr is None or cr["Temp_Avg"] in ("", None) or cr["Rain_mm"] in ("", None):
        continue
    rowsD.append((u, m, c, pop[(uf_id[u], y)], float(cr["Temp_Avg"]), float(cr["Rain_mm"])))
ufl = sorted({r[0] for r in rowsD})
X = np.zeros((len(rowsD), 2 + (len(ufl) - 1) + 11))
y_ = np.array([r[2] for r in rowsD]); off = np.log(np.array([r[3] for r in rowsD]))
# first column order: Temp, Rain, state dummies (drop first), month dummies (drop 1), intercept
cols = []
for i, r in enumerate(rowsD):
    X[i, 0] = r[4]; X[i, 1] = r[5]
    k = 2
    if r[0] != ufl[0]:
        X[i, 2 + ufl.index(r[0]) - 1] = 1
    if r[1] != 1:
        X[i, 2 + len(ufl) - 1 + r[1] - 2] = 1
X = np.hstack([X, np.ones((len(rowsD), 1))])


def irls(alpha):
    beta = np.zeros(X.shape[1]); beta[-1] = np.log(y_.sum() / np.exp(off).sum())
    for _ in range(200):
        eta = X @ beta + off; mu = np.exp(eta)
        w = mu / (1 + alpha * mu)
        z = eta - off + (y_ - mu) / mu
        XtW = X.T * w
        new = np.linalg.solve(XtW @ X, XtW @ z)
        if np.max(np.abs(new - beta)) < 1e-10:
            beta = new; break
        beta = new
    return beta


bp = irls(0.0)
check("pooled Poisson IRR dengue temperature", "{:.2f}".format(math.exp(bp[0])))
nums = json.load(open(sys.argv[1].replace("Alves ER et al JMV 2026.docx", "build_report.json")))
alpha = None
for r in csv.DictReader(open(ROOT + "outputs/glm_negbin_pooled_fe.csv")):
    if r["Virus"] == "Dengue" and r["Term"] == "Temp_Avg":
        alpha = float(r["alpha"]); n_exp = int(r["n"])
print("   (n observations: %d independent vs %d exported)" % (len(rowsD), n_exp))
bn = irls(alpha)
check("pooled NB2 IRR dengue temperature (alpha from export)", "{:.2f}".format(math.exp(bn[0])))
check("pooled NB2 IRR dengue rainfall per 100 mm", "{:.2f}".format(math.exp(100 * bn[1])))

# 9 clinical tables (xlsx)
def sumcat(path, sheet, cat_col, val_col, cat):
    return sum(float(r[val_col]) for r in read_xlsx(ROOT + path, sheet) if r[cat_col] == cat)


check("hospitalized", fmt_i(sumcat("source_data/Figure7.xlsx", "Fig7C_Hospitalization", "Category", "Count", "Positive")))
check("not hospitalized", fmt_i(sumcat("source_data/Figure7.xlsx", "Fig7C_Hospitalization", "Category", "Count", "Negative")))
check("hospitalization ignored/blank", fmt_i(sumcat("source_data/Figure7.xlsx", "Fig7C_Hospitalization", "Category", "Count", "Ign/Blank")))
check("DENV-2", fmt_i(sumcat("source_data/Figure7.xlsx", "Fig7D_Serotype", "Category", "Count", "DENV 2")))
check("DENV-3", fmt_i(sumcat("source_data/Figure7.xlsx", "Fig7D_Serotype", "Category", "Count", "DENV 3")))
check("chikungunya men", fmt_i(sum(float(r["Count"]) for r in read_xlsx(ROOT + "source_data/Figure5.xlsx", "Fig5B_sex")
                                  if r["Virus"] == "Chikungunya" and r["Category"] == "M")))
check("dengue women", fmt_i(sum(float(r["Count"]) for r in read_xlsx(ROOT + "source_data/Figure5.xlsx", "Fig5B_sex")
                               if r["Virus"] == "Dengue" and r["Category"] == "F")))

# 10 seasonality (2016-2025 pooled by month)
jan = sum(v for (d, u, y, m), v in cases.items() if d == "DENV" and y <= 2025 and m == 1)
check("dengue January pooled 2016-2025", fmt_i(jan))
may_c = sum(v for (d, u, y, m), v in cases.items() if d == "CHIKV" and y <= 2025 and m == 5)
check("chikungunya May pooled 2016-2025", fmt_i(may_c))

print("%d/%d independent checks matched the manuscript" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
