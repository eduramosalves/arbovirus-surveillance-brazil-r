"""Dump the original docx body as lightweight markup, one line per body element.

Markup: *italic*  **bold**  ^superscript^  {cN}..{/cN} comment anchors  {hl}..{/hl} highlight.
Usage: python extract_markup.py <unzipped dir> <out file>
"""
import sys
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
q = lambda t: "{%s}%s" % (W, t)


def run_flags(r):
    rp = r.find(q("rPr"))
    f = {"b": False, "i": False, "sup": False, "hl": False}
    if rp is not None:
        if rp.find(q("b")) is not None:
            f["b"] = True
        if rp.find(q("i")) is not None:
            f["i"] = True
        va = rp.find(q("vertAlign"))
        if va is not None and va.get(q("val")) == "superscript":
            f["sup"] = True
        if rp.find(q("highlight")) is not None:
            f["hl"] = True
    return f


def para_markup(p):
    out = []
    state = {"b": False, "i": False, "sup": False, "hl": False}
    mark = {"b": "**", "i": "*", "sup": "^", "hl": None}

    def close_all():
        for k in ("hl", "sup", "i", "b"):
            if state[k]:
                out.append("{/hl}" if k == "hl" else mark[k])
                state[k] = False

    for ch in p.iter():
        tag = etree.QName(ch).localname
        if tag == "commentRangeStart":
            close_all()
            out.append("{c%s}" % ch.get(q("id")))
        elif tag == "commentRangeEnd":
            close_all()
            out.append("{/c%s}" % ch.get(q("id")))
        elif tag == "r":
            txt = "".join((x.text or "") for x in ch.findall(q("t")))
            if ch.find(q("tab")) is not None:
                txt = "\t" + txt
            if not txt:
                continue
            txt = txt.replace("*", "\*")
            f = run_flags(ch)
            for k in ("b", "i", "sup", "hl"):
                if f[k] != state[k]:
                    if f[k]:
                        out.append("{hl}" if k == "hl" else mark[k])
                    else:
                        out.append("{/hl}" if k == "hl" else mark[k])
                    state[k] = f[k]
            out.append(txt)
    close_all()
    return "".join(out)


root = etree.parse(sys.argv[1] + "/word/document.xml").getroot()
body = root.find(q("body"))
lines = []
for i, el in enumerate(body):
    if etree.QName(el).localname == "p":
        lines.append("[%d] %s" % (i, para_markup(el)))
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(lines))
print(len(lines), "paragraphs written")
