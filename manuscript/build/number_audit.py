"""List every number in Abstract/Results/Discussion that is NOT produced by a sourced {n:...} key. Usage: python number_audit.py <outdir>"""
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
out = Path(sys.argv[1])
rep = json.load(open(out / "build_report.json", encoding="utf-8"))
NUM = re.compile(r"[−-]?\d+(?:,\d{3})*(?:\.\d+)?%?")
sourced = set()
for u in rep["used"]:
    for m in NUM.finditer(u["text"]):
        sourced.add(m.group(0).rstrip("%"))
z = zipfile.ZipFile(out / "Alves ER et al JMV 2026.docx")
root = ET.fromstring(z.read("word/document.xml"))
paras = []
for p in root.find(W + "body").findall(W + "p"):
    st = p.find(W + "pPr/" + W + "pStyle")
    txt = []
    for r in p.iter(W + "r"):
        rs = r.find(W + "rPr/" + W + "rStyle")
        if rs is not None and rs.get(W + "val") == "CitationRef":
            continue
        txt.append("".join(t.text or "" for t in r.iter(W + "t")))
    paras.append((st.get(W + "val") if st is not None else "", "".join(txt)))
sections, cur = {}, None
for st, t in paras:
    if st == "Ttulo1":
        cur = t
    if st == "Abstract":
        cur = "ABSTRACT"
    if cur:
        sections.setdefault(cur, []).append((st, t))
SKIP_PAT = [
    r"Figures? S?\d+[A-D]?(?: and S?\d+[A-D]?)?", r"Figures? \d+[A-D]?", r"Supplementary Figures? S\d+", r"\b20[12]\d\b", r"\b\d{1,2}\.\d \| ",
    r"p < 0\.05", r"\b27\b", r"\b\d{1,2}[–-]\d{1,2} °C\b", r"lags? \d", r"lags of \d", r"\bCOVID-19\b", r"DENV-\d", r"\bat lags? 0, 1, and 2\b",
]
found = {}
for sec in ("ABSTRACT", "3 | RESULTS", "4 | DISCUSSION", "5 | CONCLUSION"):
    for st, t in sections.get(sec, []):
        if st in ("Ttulo1", "Ttulo2"):
            continue
        s = t
        for pat in SKIP_PAT:
            s = re.sub(pat, " ", s)
        s = re.sub(r"\[\d+[^\]]*\]", " ", s)
        for m in NUM.finditer(s):
            tok = m.group(0).rstrip("%")
            if tok not in sourced:
                ctx = s[max(0, m.start() - 40): m.end() + 30].replace("\n", " ")
                found.setdefault(sec, []).append((tok, ctx))
for sec, items in found.items():
    print("==", sec, len(items))
    for tok, ctx in items:
        print("   %-8s ...%s..." % (tok, ctx))
if not found:
    print("every number in the audited sections is sourced")
