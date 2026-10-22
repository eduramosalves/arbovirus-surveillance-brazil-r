"""Structural audit of the built manuscripts. Usage: python audit.py <outdir>"""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
W15 = "http://schemas.microsoft.com/office/word/2012/wordml"
q = lambda t: "{%s}%s" % (W, t)
out = Path(sys.argv[1])
CLEAN = out / "Alves ER et al JMV 2026.docx"
RED = out / "Alves ER et al JMV 2026 (redline).docx"
ORIG = Path("C:/Users/Usuario/arbovirus-surveillance-brazil-r-eduardo/Alves ER et al JVI 2026.docx")
ok = True


def check(name, cond, detail=""):
    global ok
    ok = ok and bool(cond)
    print(("PASS " if cond else "FAIL ") + name + (" :: " + str(detail) if detail else ""))


def load(path):
    z = zipfile.ZipFile(path)
    return z, etree.fromstring(z.read("word/document.xml"))


def ptext(p, drop_del=True, only_new=True):
    s = []
    for r in p.iter():
        if r.tag == q("t"):
            s.append(r.text or "")
        elif r.tag == q("tab"):
            s.append("\t")
        elif r.tag == q("delText") and not drop_del:
            s.append(r.text or "")
    return "".join(s)


zc, dc = load(CLEAN)
zr, dr = load(RED)

# ---- original untouched
sha = hashlib.sha256(ORIG.read_bytes()).hexdigest()
check("original file hash unchanged", sha == "e8e68cf28b2f2074fa27218eb20ce86dc1ab050faab0bb8023174137f6866869", sha[:16])

for label, z, d in (("clean", zc, dc), ("redline", zr, dr)):
    # ---- comments
    cm = etree.fromstring(z.read("word/comments.xml"))
    ids = [int(c.get(q("id"))) for c in cm]
    orig_ids = [3, 4, 5, 6, 7, 8, 9] + list(range(11, 24))
    check(label + ": all 20 original comments kept", all(i in ids for i in orig_ids), len(ids))
    starts = [int(e.get(q("id"))) for e in d.iter(q("commentRangeStart"))]
    ends = [int(e.get(q("id"))) for e in d.iter(q("commentRangeEnd"))]
    refs = [int(e.get(q("id"))) for e in d.iter(q("commentReference"))]
    check(label + ": every comment anchored (start/end/reference)", sorted(ids) == sorted(starts) == sorted(ends) == sorted(refs),
          "%d comments, %d/%d/%d markers" % (len(ids), len(starts), len(ends), len(refs)))
    authors = {}
    for c in cm:
        authors[c.get(q("author"))] = authors.get(c.get(q("author")), 0) + 1
    print("   authors:", authors)
    ext = etree.fromstring(z.read("word/commentsExtended.xml"))
    para_ids = {p.get("{%s}paraId" % W14) for c in cm for p in c.iter(q("p"))}
    parents = [e.get("{%s}paraIdParent" % W15) for e in ext if e.get("{%s}paraIdParent" % W15)]
    check(label + ": reply parents resolve", all(p in para_ids for p in parents), "%d replies" % len(parents))
    # ---- text
    body = d.find(q("body"))
    paras = [p for p in body if p.tag == q("p")]
    full = "\n".join(ptext(p) for p in paras)
    if label == "clean":
        for bad in ("xxxxx", "[X]", "REF IBGE", "St. Jude - Confidential", "Python", "CPC/NCEP", "Queen contiguity"):
            check("clean: no '%s'" % bad, bad not in full)
        hl = []
        for r in d.iter(q("r")):
            if r.find(q("rPr") + "/" + q("highlight")) is not None:
                hl.append("".join(t.text or "" for t in r.iter(q("t"))))
        print("   highlighted placeholders:", hl)
        # ---- citations
        cites = []
        for r in d.iter(q("r")):
            st = r.find(q("rPr") + "/" + q("rStyle"))
            if st is not None and st.get(q("val")) == "CitationRef":
                cites.append("".join(t.text or "" for t in r.iter(q("t"))))
        seen, mono = 0, True
        used = set()
        for c in cites:
            nums = []
            for part in c.split(","):
                m = re.fullmatch(r"(\d+)\u2013(\d+)", part)
                nums += list(range(int(m.group(1)), int(m.group(2)) + 1)) if m else [int(part)]
            for n in nums:
                used.add(n)
                if n > seen + 1:
                    mono = False
                seen = max(seen, n)
        reflist = [ptext(p) for p in paras if p.find(q("pPr") + "/" + q("pStyle")) is not None
                   and p.find(q("pPr") + "/" + q("pStyle")).get(q("val")) == "Reference"]
        refnums = [int(re.match(r"(\d+)\.", t).group(1)) for t in reflist]
        check("clean: citation numbers appear in order of first citation", mono, "max %d" % seen)
        check("clean: every reference is cited and every citation resolves", used == set(refnums) == set(range(1, len(refnums) + 1)),
              "%d refs, %d cited" % (len(refnums), len(used)))
        # ---- limits
        ab = [ptext(p) for p in paras if p.find(q("pPr") + "/" + q("pStyle")) is not None
              and p.find(q("pPr") + "/" + q("pStyle")).get(q("val")) == "Abstract"]
        words = sum(len(t.split()) for t in ab)
        check("clean: abstract <= 200 words", words <= 200, words)
        kw = [ptext(p) for p in paras if p.find(q("pPr") + "/" + q("pStyle")) is not None
              and p.find(q("pPr") + "/" + q("pStyle")).get(q("val")) == "Keywords"][0]
        n_kw = len([k for k in kw.split(":", 1)[1].split(";") if k.strip()])
        check("clean: 5 keywords", n_kw == 5, n_kw)
        sect = d.find(q("body")).find(q("sectPr"))
        check("clean: line numbering kept", sect.find(q("lnNumType")) is not None)

# ---- redline accepted == clean
def accepted_paras(d):
    out = []
    for p in d.find(q("body")).findall(q("p")):
        mark_del = p.find(q("pPr") + "/" + q("rPr") + "/" + q("del")) is not None
        t = []
        for r in p.iter(q("t")):
            # skip text inside w:del (it is delText anyway)
            t.append(r.text or "")
        txt = "".join(t)
        if mark_del and not txt.strip():
            continue
        out.append(txt)
    return out


a = accepted_paras(dr)
b = accepted_paras(dc)
check("redline with all changes accepted == clean text", a == b, "%d vs %d paragraphs" % (len(a), len(b)))
if a != b:
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            print("   first difference at paragraph", i, repr(x[:120]), "|", repr(y[:120]))
            break
n_ins = len(list(dr.iter(q("ins")))); n_del = len(list(dr.iter(q("del"))))
print("   tracked insertions: %d, deletions: %d" % (n_ins, n_del))
print("ALL OK" if ok else "SOME CHECKS FAILED")
