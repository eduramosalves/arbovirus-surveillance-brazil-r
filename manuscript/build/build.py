"""Build the JMV manuscript (clean + tracked-change versions) from the block sources.

Usage: python build.py <outdir>
"""
import csv
import difflib
import json
import os
import random
import re
import shutil
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

WORK = Path(__file__).parent.resolve()
sys.path.insert(0, str(WORK))
# folder of the docx skill (comment.py); set DOCX_SKILL_DIR on another machine
SKILL = Path(os.environ.get("DOCX_SKILL_DIR", "C:/Users/Usuario/.claude/skills/synced/6d8e999c-5f17-479f-a00d-ae2a9687f861_77b8edd7-91ee-4c29-be3b-4d1cbe281602/docx/scripts"))
sys.path.insert(0, str(SKILL))

from lxml import etree  # noqa: E402

import comments_text  # noqa: E402
import figmap  # noqa: E402
import ms_back  # noqa: E402
import ms_discussion  # noqa: E402
import ms_front  # noqa: E402
import ms_methods  # noqa: E402
import ms_results  # noqa: E402
import refs as refmod  # noqa: E402
from msbase import ORIG, conv_cit, strip_runin  # noqa: E402

PROJECT = WORK.parents[1]   # repository root (this file is manuscript/build/build.py)
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DATE = "2026-10-21T12:00:00Z"
AUTHOR = comments_text.AUTHOR

UFNAME = {"AC": "Acre", "AL": "Alagoas", "AP": "Amap\u00e1", "AM": "Amazonas", "BA": "Bahia", "CE": "Cear\u00e1",
          "DF": "the Federal District", "ES": "Esp\u00edrito Santo", "GO": "Goi\u00e1s", "MA": "Maranh\u00e3o", "MT": "Mato Grosso",
          "MS": "Mato Grosso do Sul", "MG": "Minas Gerais", "PA": "Par\u00e1", "PB": "Para\u00edba", "PR": "Paran\u00e1",
          "PE": "Pernambuco", "PI": "Piau\u00ed", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
          "RO": "Rond\u00f4nia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "S\u00e3o Paulo", "SE": "Sergipe", "TO": "Tocantins"}
ORD = ["zeroth", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]

NUMS = {}
SRC = {}
for r in csv.DictReader(open(WORK / "numbers.csv", encoding="utf-8")):
    NUMS[r["key"]] = r["value"]
    SRC[r["key"]] = r["src"]
USED = {}  # key -> (display values, spec)


def minus(s):
    return s.replace("-", "\u2212")


def fmt_value(key, spec):
    if key not in NUMS:
        raise KeyError("missing number key: %s" % key)
    v = NUMS[key]
    if spec in ("s", None):
        return v
    x = float(v)
    if spec == "i":
        return minus("{:,.0f}".format(x))
    if spec == "y":
        return str(int(x))
    m = re.fullmatch(r"d(\d)", spec)
    if m:
        return minus("{:,.{}f}".format(x, int(m.group(1))))
    if spec == "pct0":
        return minus("{:.0f}%".format(x * 100))
    if spec == "pct1":
        return minus("{:.1f}%".format(x * 100))
    if spec == "pv":
        return "< 0.001" if x < 0.001 else "= {:.3f}".format(x)
    if spec == "mil2":
        return "{:.2f}".format(x / 1e6)
    if spec == "nz":
        return "no" if x == 0 else minus("{:,.0f}".format(x))
    if spec == "ord":
        n = int(round(x))
        return ORD[n] if n < len(ORD) else "%dth" % n
    if spec == "words":
        n = int(round(x))
        return WORDS[n] if n < len(WORDS) else str(n)
    raise ValueError("unknown format %s" % spec)


def resolve_numbers(text):
    def num(m):
        key, spec = m.group(1), m.group(2)
        out = fmt_value(key, spec)
        USED[(key, spec)] = out
        return out

    def uf(m):
        key, mod = m.group(1), m.group(2)
        if key not in NUMS:
            raise KeyError("missing uf key: %s" % key)
        codes = [c.strip() for c in NUMS[key].split(",") if c.strip()]
        names = [UFNAME[c] for c in codes]
        s = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
        USED[(key, "u" + (mod or ""))] = s
        return s[0].upper() + s[1:] if mod == "cap" else s

    text = re.sub(r"\{n:([^:{}]+)(?::([a-z0-9]+))?\}", num, text)
    text = re.sub(r"\{u:([^:{}]+)(?::(cap))?\}", uf, text)
    return text


# ------------------------------------------------------------------ tokens
TOKRE = re.compile(r"(\{c\d+\}|\{/c\d+\}|\{q:[a-z0-9]+\}|\{/q\}|\{hl\}|\{/hl\}|\[@[^\]]+\]|\*\*|\*|\^|~)")


def tokenize(text):
    """markup -> tokens: ('t', text, flags) | ('cite', keys) | ('cs', id) | ('ce', id)"""
    text = text.replace("\\*", "\ue000")
    out = []
    flags = {"b": False, "i": False, "sup": False, "sub": False, "hl": False}
    qstack = []
    for piece in TOKRE.split(text):
        if not piece:
            continue
        if piece == "**":
            flags["b"] = not flags["b"]
        elif piece == "*":
            flags["i"] = not flags["i"]
        elif piece == "^":
            flags["sup"] = not flags["sup"]
        elif piece == "~":
            flags["sub"] = not flags["sub"]
        elif piece == "{hl}":
            flags["hl"] = True
        elif piece == "{/hl}":
            flags["hl"] = False
        elif re.fullmatch(r"\{c\d+\}", piece):
            out.append(("cs", piece[2:-1]))
        elif re.fullmatch(r"\{/c\d+\}", piece):
            out.append(("ce", piece[3:-1]))
        elif piece.startswith("{q:"):
            qstack.append("q:" + piece[3:-1])
            out.append(("cs", qstack[-1]))
        elif piece == "{/q}":
            out.append(("ce", qstack.pop()))
        elif piece.startswith("[@"):
            keys = [k.strip().lstrip("@") for k in piece[1:-1].split(",")]
            out.append(("cite", tuple(keys)))
        else:
            t = piece.replace("\ue000", "*").replace("'", "\u2019")
            out.append(("t", t, tuple(sorted(k for k, v in flags.items() if v))))
    return out


def plain(tokens):
    return "".join(t[1] for t in tokens if t[0] == "t")


# ------------------------------------------------------------------ assemble blocks
def assemble():
    return ms_front.FRONT + ms_front.INTRO + ms_methods.METHODS + ms_results.RESULTS + ms_discussion.DISCUSSION + ms_back.BACK


def number_citations(blocks):
    order = {}
    for b in blocks:
        for t in b["tokens"]:
            if t[0] == "cite":
                for k in t[1]:
                    if k not in order:
                        order[k] = len(order) + 1
    return order


def cite_text(keys, order):
    nums = sorted(order[k] for k in keys)
    parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        if j - i >= 2:
            parts.append("%d\u2013%d" % (nums[i], nums[j]))
        else:
            parts.extend(str(n) for n in nums[i:j + 1])
        i = j + 1
    return ",".join(parts)


# ------------------------------------------------------------------ XML rendering
_ids = {"n": 1000}


def next_id():
    _ids["n"] += 1
    return _ids["n"]


def rpr(flags, cite=False, extra=""):
    s = ""
    if cite:
        s += '<w:rStyle w:val="CitationRef"/>'
    if "b" in flags:
        s += "<w:b/>"
    if "i" in flags:
        s += "<w:i/>"
    if "hl" in flags:
        s += '<w:highlight w:val="yellow"/>'
    if "sup" in flags:
        s += '<w:vertAlign w:val="superscript"/>'
    elif "sub" in flags:
        s += '<w:vertAlign w:val="subscript"/>'
    return "<w:rPr>%s</w:rPr>" % s if s else ""


def run_xml(text, flags, cite=False, deleted=False):
    parts = re.split(r"(\t)", text)
    inner = ""
    for p in parts:
        if p == "\t":
            inner += "<w:tab/>"
        elif p:
            tag = "w:delText" if deleted else "w:t"
            inner += '<%s xml:space="preserve">%s</%s>' % (tag, escape(p), tag)
    return "<w:r>%s%s</w:r>" % (rpr(flags, cite), inner)


class Ctx:
    def __init__(self, order, cid_map, replies):
        self.order = order          # citation key -> number
        self.cid = cid_map          # anchor id ('17' / 'q:code0') -> numeric comment id
        self.replies = replies      # numeric parent id -> [reply numeric ids]


def marker_xml(tok, ctx):
    kind, cid = tok
    nid = ctx.cid[cid]
    reps = ctx.replies.get(nid, [])
    if kind == "cs":
        return '<w:commentRangeStart w:id="%d"/>' % nid + "".join('<w:commentRangeStart w:id="%d"/>' % r for r in reps)
    ref = lambda i: '<w:r><w:rPr><w:rStyle w:val="Refdecomentrio"/></w:rPr><w:commentReference w:id="%d"/></w:r>' % i
    return ("".join('<w:commentRangeEnd w:id="%d"/>' % r for r in reps) + '<w:commentRangeEnd w:id="%d"/>' % nid
            + ref(nid) + "".join(ref(r) for r in reps))


def atoms_of(tokens, order=None):
    """Tokens -> flat atoms for diffing/rendering. Atom: (kind, payload, flags)"""
    out = []
    for t in tokens:
        if t[0] == "t":
            for a in re.findall(r"\s+|\w+|[^\w\s]", t[1]):
                out.append(("t", a, t[2]))
        elif t[0] == "cite":
            out.append(("cite", t[1], ()))
        else:
            out.append((t[0], t[1], ()))
    return out


def akey(a):
    if a[0] == "t":
        return " " if a[1].isspace() else a[1]
    if a[0] == "cite":
        return ("cite", frozenset(a[1]))
    return None


def emit_runs(events, ctx):
    """events: ('run', atom, mode) | ('marker', atom). Returns XML for paragraph content."""
    xml = []
    cur = None  # [mode, [(text, flags, cite)]]

    def flush():
        nonlocal cur
        if not cur:
            return
        mode, items = cur
        # merge adjacent runs with same flags/cite
        merged = []
        for text, flags, cite in items:
            if merged and merged[-1][1] == flags and merged[-1][2] == cite:
                merged[-1][0] += text
            else:
                merged.append([text, flags, cite])
        runs = "".join(run_xml(t, f, c, deleted=(mode == "del")) for t, f, c in merged)
        if mode == "eq":
            xml.append(runs)
        else:
            tag = "w:ins" if mode == "ins" else "w:del"
            xml.append('<%s w:id="%d" w:author="%s" w:date="%s">%s</%s>' % (tag, next_id(), escape(AUTHOR), DATE, runs, tag))
        cur = None

    for ev in events:
        if ev[0] == "marker":
            flush()
            xml.append(marker_xml((ev[1][0], ev[1][1]), ctx))
            continue
        _, atom, mode = ev
        if atom[0] == "cite":
            text, flags, cite = cite_text(atom[1], ctx.order), (), True
        else:
            text, flags, cite = atom[1], atom[2], False
        if cur is None or cur[0] != mode:
            flush()
            cur = [mode, []]
        cur[1].append((text, flags, cite))
    flush()
    return "".join(xml)


def para_xml(style, content, mark=None):
    ppr = '<w:pStyle w:val="%s"/>' % style
    if mark == "ins":
        ppr += '<w:rPr><w:ins w:id="%d" w:author="%s" w:date="%s"/></w:rPr>' % (next_id(), escape(AUTHOR), DATE)
    elif mark == "del":
        ppr += '<w:rPr><w:del w:id="%d" w:author="%s" w:date="%s"/></w:rPr>' % (next_id(), escape(AUTHOR), DATE)
    return "<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (ppr, content)


STYLE_ID = {"Title": "Ttulo", "H1": "Ttulo1", "H2": "Ttulo2"}


def sid(style):
    return STYLE_ID.get(style, style)


def old_tokens(block):
    """Tokens of the original paragraph(s) mapped to this block, for the tracked-change comparison."""
    toks = []
    for k, i in enumerate(block["orig"]):
        t = ORIG[i]
        if block["strip"] and k == 0:
            t = strip_runin(t)
        t = conv_cit(t)
        t = re.sub(r"\{/?c\d+\}", "", t)
        t = t.replace("'", "\u2019")
        # old bracket citations -> cite tokens
        pieces = tokenize(t)
        if k:
            pieces = [("t", " ", ())] + pieces
        toks.extend(pieces)
    return toks


def render_block(block, ctx, tracked):
    style = sid(block["style"])
    new_t = block["tokens"]
    if not tracked or not block["orig"] and False:
        pass
    if not tracked:
        events = []
        for a in atoms_of(new_t):
            events.append(("marker", a) if a[0] in ("cs", "ce") else ("run", a, "eq"))
        return para_xml(style, emit_runs(events, ctx))
    if not block["orig"]:
        events = []
        for a in atoms_of(new_t):
            events.append(("marker", a) if a[0] in ("cs", "ce") else ("run", a, "ins"))
        return para_xml(style, emit_runs(events, ctx), mark="ins")
    N = atoms_of(new_t)
    O = atoms_of(old_tokens(block))
    nm = [i for i, a in enumerate(N) if a[0] in ("t", "cite")]
    nkeys = [akey(N[i]) for i in nm]
    okeys = [akey(a) for a in O]
    sm = difflib.SequenceMatcher(None, okeys, nkeys, autojunk=False)
    events, start = [], 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        end = nm[j2] if j2 < len(nm) else len(N)
        region = N[start:end]
        start = end
        if op == "equal":
            for a in region:
                events.append(("marker", a) if a[0] in ("cs", "ce") else ("run", a, "eq"))
        else:
            for a in O[i1:i2]:
                events.append(("run", a, "del"))
            for a in region:
                events.append(("marker", a) if a[0] in ("cs", "ce") else ("run", a, "ins"))
    for a in N[start:]:
        events.append(("marker", a) if a[0] in ("cs", "ce") else ("run", a, "eq"))
    return para_xml(style, emit_runs(events, ctx))


def deleted_para_xml(i):
    t = conv_cit(ORIG[i])
    t = re.sub(r"\{/?c\d+\}", "", t).replace("'", "\u2019")
    events = [("run", a, "del") for a in atoms_of(tokenize(t))]
    return para_xml("Body", emit_runs(events, Ctx({}, {}, {})), mark="del")


# ------------------------------------------------------------------ package
def patch_styles(path):
    tree = etree.parse(str(path))
    root = tree.getroot()
    q = lambda t: "{%s}%s" % (W_NS, t)
    E = lambda xml: etree.fromstring('<root xmlns:w="%s">%s</root>' % (W_NS, xml))[0]
    dd = root.find(q("docDefaults"))
    root.replace(dd, E(
        '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" '
        'w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/>'
        '<w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
        '<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="480" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'))
    styles = {s.get(q("styleId")): s for s in root.findall(q("style"))}

    def redefine(sid_, name, ppr="", rp="", based="Normal", nxt="Normal", link=None, qf=True):
        old = styles.get(sid_)
        xml = ('<w:style w:type="paragraph" w:styleId="%s"><w:name w:val="%s"/><w:basedOn w:val="%s"/><w:next w:val="%s"/>%s%s'
               '<w:pPr>%s</w:pPr><w:rPr>%s</w:rPr></w:style>') % (
            sid_, name, based, nxt, '<w:link w:val="%s"/>' % link if link else "", "<w:qFormat/>" if qf else "", ppr, rp)
        new = E(xml)
        if old is not None:
            root.replace(old, new)
        else:
            root.append(new)

    TNR = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    redefine("Ttulo", "Title", ppr='<w:keepNext/><w:spacing w:after="240" w:line="480" w:lineRule="auto"/>', rp=TNR + '<w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/>', link=None)
    redefine("Ttulo1", "heading 1", ppr='<w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="0"/><w:outlineLvl w:val="0"/>',
             rp=TNR + '<w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/>')
    redefine("Ttulo2", "heading 2", ppr='<w:keepNext/><w:keepLines/><w:spacing w:before="120" w:after="0"/><w:outlineLvl w:val="1"/>',
             rp=TNR + '<w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/>')
    redefine("RunningTitle", "Running Title", ppr="", rp="<w:i/>")
    redefine("Authors", "Authors", ppr='<w:spacing w:after="120" w:line="360" w:lineRule="auto"/>')
    redefine("Affil", "Affiliation", ppr='<w:spacing w:after="60" w:line="240" w:lineRule="auto"/>')
    redefine("Corr", "Correspondence", ppr='<w:spacing w:before="60" w:after="120" w:line="240" w:lineRule="auto"/>')
    redefine("Label", "Section Label", ppr='<w:keepNext/><w:spacing w:before="240" w:after="0"/>', rp="<w:b/><w:bCs/>")
    redefine("Abstract", "Abstract", ppr="")
    redefine("Keywords", "Keywords", ppr='<w:spacing w:before="120"/>')
    redefine("Body", "Body Text Indent", ppr='<w:ind w:firstLine="720"/>')
    redefine("BackBody", "Back Matter Text", ppr='')
    redefine("Legend", "Figure Legend", ppr='<w:spacing w:after="120" w:line="360" w:lineRule="auto"/>')
    redefine("Reference", "Reference Entry", ppr='<w:spacing w:after="60" w:line="276" w:lineRule="auto"/><w:ind w:left="360" w:hanging="360"/>')
    root.append(E('<w:style w:type="character" w:customStyle="1" w:styleId="CitationRef"><w:name w:val="Citation Reference"/>'
                  '<w:basedOn w:val="Fontepargpadro"/><w:qFormat/><w:rPr><w:vertAlign w:val="superscript"/></w:rPr></w:style>'))
    tree.write(str(path), xml_declaration=True, encoding="UTF-8", standalone=True)


def main(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    head = assemble()
    run_assertions()
    # figures are numbered by the order of their first citation in the text (main and supplementary separately)
    order_keys = figmap.cited_order([b["text"] for b in head])
    uncited = [k for k in figmap.FIGURES if k not in order_keys]
    assert not uncited, "figures never cited in the text: %s" % uncited
    fignum = figmap.numbering(order_keys)
    for b in head:
        b["text"] = figmap.resolve(b["text"], fignum)
    legends = ms_back.legends(str(PROJECT / "manuscript" / "FIGURE_CAPTIONS.md"), fignum)
    # tokens (numbers resolved first; citation numbers need the whole document)
    allblocks = head + legends
    for b in allblocks:
        b["tokens"] = tokenize(resolve_numbers(b["text"]))
    order = number_citations(head)
    entries = refmod.all_entries()
    unknown = [k for k in order if k not in entries]
    assert not unknown, "unknown reference keys: %s" % unknown
    # calc counts
    abstract_words = sum(len(plain(b["tokens"]).split()) for b in head if b["style"] == "Abstract")
    in_main, main_words = False, 0
    for b in head:
        if b["style"] == "H1":
            txt = plain(b["tokens"])
            in_main = txt.startswith(("1 |", "2 |", "3 |", "4 |", "5 |"))
        if in_main and b["style"] == "Body":
            main_words += len(plain(b["tokens"]).split())
    calc = {"abstract_words": abstract_words, "main_words": main_words, "n_refs": len(order)}
    check_text(head + legends)
    for b in allblocks:
        newt = []
        for t in b["tokens"]:
            if t[0] == "t" and "{calc:" in t[1]:
                t = ("t", re.sub(r"\{calc:(\w+)\}", lambda m: "{:,}".format(calc[m.group(1)]), t[1]), t[2])
            newt.append(t)
        b["tokens"] = newt
    # reference blocks
    ref_blocks = [{"style": "H1", "text": "REFERENCES", "orig": [95], "strip": False,
                   "tokens": tokenize("REFERENCES")}]
    inv = sorted(order.items(), key=lambda kv: kv[1])
    for key, n in inv:
        orig = [95 + int(key[1:])] if re.fullmatch(r"r\d+", key) else []
        ref_blocks.append({"style": "Reference", "text": "", "orig": orig, "strip": False,
                           "tokens": tokenize("%d. %s" % (n, entries[key]))})
    full = head + ref_blocks + legends
    # ---- comments
    random.seed(20261021)
    results = {}
    for tracked in (False, True):
        bdir = WORK / ("build_redline" if tracked else "build_clean")
        if bdir.exists():
            shutil.rmtree(bdir)
        shutil.copytree(WORK / "orig", bdir)
        # the comment parts come from the file as edited in Word (the co-author's comments, the user's
        # instructions and the user's deletions); only the body, styles and footer are rebuilt
        for part in ("comments.xml", "commentsExtended.xml", "commentsIds.xml", "commentsExtensible.xml", "people.xml"):
            shutil.copy(USER_DIR / "word" / part, bdir / "word" / part)
        from comment import add_comment  # skill helper
        cid_map, replies = comment_threads()
        new_ids = []
        for pid, text in comments_text.REPLIES_R2.items():
            text = figmap.resolve(resolve_numbers(text), fignum)
            if pid not in replies and pid not in {v for v in cid_map.values()}:
                raise KeyError("no comment %s to reply to" % pid)
            cid, _, _ = add_comment(bdir, text, author=AUTHOR, initials=comments_text.INITIALS, parent_id=pid)
            replies.setdefault(pid, []).append(cid)
            new_ids.append((pid, cid))
        fix_reply_parents(bdir, {pid: [cid] for pid, cid in new_ids})
        close_threads(bdir, replies, [cid_map["q:" + k] for k in comments_text.CLOSE_THREADS])
        ctx = Ctx(order, cid_map, replies)
        # anchors check (anchors of comments the user deleted are dropped from the text)
        anchors = [t[1] for b in full for t in b["tokens"] if t[0] == "cs"]
        unknown = sorted({a for a in anchors if a not in cid_map})
        if unknown:
            print("note: anchors without a comment in the file (dropped): %s" % unknown)
            for b in full:
                b["tokens"] = [t for t in b["tokens"] if not (t[0] in ("cs", "ce") and t[1] in unknown)]
        anchors = [t[1] for b in full for t in b["tokens"] if t[0] == "cs"]
        missing = [c for c in cid_map if c not in anchors]
        dup = [c for c in set(anchors) if anchors.count(c) != 1]
        assert not missing, "comment anchors missing in the text: %s" % missing
        assert not dup, "comment anchors duplicated: %s" % dup
        # ---- body
        _ids["n"] = 1000
        body = []
        mapped = {i for b in full for i in b["orig"]}
        unmapped = sorted(i for i in ORIG if i not in mapped and ORIG[i].strip())
        attach = {}
        if tracked:
            mapped_sorted = sorted(mapped)
            for i in unmapped:
                prev = [m for m in mapped_sorted if m < i]
                attach.setdefault(prev[-1] if prev else -1, []).append(i)
        last_orig_for_block = lambda b: max(b["orig"]) if b["orig"] else None
        pending = list(attach.get(-1, []))
        for b in full:
            body.append(render_block(b, ctx, tracked))
            for i in b["orig"]:
                for j in attach.pop(i, []):
                    body.append(deleted_para_xml(j))
        for j in sum(attach.values(), []):
            body.append(deleted_para_xml(j))
        sect = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdFtr1"/><w:pgSz w:w="12240" w:h="15840" w:code="1"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
                '<w:lnNumType w:countBy="1" w:restart="continuous"/><w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>')
        orig_doc = (WORK / "orig" / "word" / "document.xml").read_text(encoding="utf-8")
        root_open = re.search(r"<w:document[^>]*>", orig_doc).group(0)
        doc = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + root_open + "<w:body>" + "".join(body) + sect + "</w:body></w:document>"
        etree.fromstring(doc.encode("utf-8"))  # well-formedness
        (bdir / "word" / "document.xml").write_text(doc, encoding="utf-8")
        finish_package(bdir)
        name = "Alves ER et al JMV 2026 (redline).docx" if tracked else "Alves ER et al JMV 2026.docx"
        zpath = out / name
        zip_dir(bdir, zpath)
        results[name] = str(zpath)
    # ---- reports
    used = [{"key": k, "fmt": s, "text": v, "src": SRC.get(k, "")} for (k, s), v in sorted(USED.items())]
    figures = [{"key": k, "repo_label": figmap.FIGURES[k][0], "number": n, "files": figmap.FIGURES[k][2]}
               for k, n in sorted(fignum.items(), key=lambda kv: (kv[1].startswith("S"), int(kv[1].lstrip("S"))))]
    json.dump({"calc": calc, "citation_order": order, "figures": figures, "used": used},
              open(out / "build_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plain_all = []
    for b in full:
        plain_all.append("[%s] %s" % (b["style"], plain(b["tokens"]).replace("\t", " ")))
    (out / "manuscript_plain.txt").write_text("\n\n".join(plain_all), encoding="utf-8")
    print(json.dumps(calc), len(used), "numbers used;", len(order), "references")
    return results


USER_DIR = WORK / "user"   # unpacked copy of the manuscript as edited in Word on 2026-10-22
# the keys are phrases of the authors' existing comments (they still say docs/FIGURE_CAPTIONS.md); do not rename
QUERY_KEYS = {"Figure 7D folds": "code0", "The supplementary DLNM": "dlnm", "docs/FIGURE_CAPTIONS.md quotes": "esdata",
              "2026 is annualized": "ann2026"}


def comment_threads():
    """(cid_map, replies) of the comments in USER_DIR: cid_map maps anchor keys ('17', 'q:dlnm') to comment ids;
    replies maps each thread root to the ids of its replies (in id order)."""
    W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
    W15 = "http://schemas.microsoft.com/office/word/2012/wordml"
    cm = etree.parse(str(USER_DIR / "word" / "comments.xml")).getroot()
    ext = etree.parse(str(USER_DIR / "word" / "commentsExtended.xml")).getroot()
    para2id, info = {}, {}
    for c in cm:
        cid = int(c.get("{%s}id" % W_NS))
        paras = [p.get("{%s}paraId" % W14) for p in c.iter("{%s}p" % W_NS)]
        text = "\n".join("".join(t.text or "" for t in p.iter("{%s}t" % W_NS)) for p in c.iter("{%s}p" % W_NS))
        for p in paras:
            para2id[p] = cid
        info[cid] = {"author": c.get("{%s}author" % W_NS), "text": text}
    parent = {}
    for e in ext:
        pp = e.get("{%s}paraIdParent" % W15)
        if pp:
            parent[para2id[e.get("{%s}paraId" % W15)]] = para2id[pp]
    cid_map, replies = {}, {}
    for cid in sorted(info):
        if cid in parent:
            replies.setdefault(parent[cid], []).append(cid)
        elif info[cid]["author"] == AUTHOR:
            key = [k for pre, k in QUERY_KEYS.items() if info[cid]["text"].startswith(pre)]
            assert key, "unrecognised query of the assistant: %r" % info[cid]["text"][:60]
            cid_map["q:" + key[0]] = cid
        else:
            cid_map[str(cid)] = cid
    return cid_map, replies


def close_threads(bdir, replies, roots):
    """Mark whole threads as resolved (w15:done) in commentsExtended.xml."""
    W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
    W15 = "http://schemas.microsoft.com/office/word/2012/wordml"
    cm = etree.parse(str(bdir / "word" / "comments.xml")).getroot()
    last = {int(c.get("{%s}id" % W_NS)): [p.get("{%s}paraId" % W14) for p in c.iter("{%s}p" % W_NS)] for c in cm}
    ext_path = bdir / "word" / "commentsExtended.xml"
    ext = etree.parse(str(ext_path))
    by_para = {e.get("{%s}paraId" % W15): e for e in ext.getroot()}
    for root in roots:
        for cid in [root] + replies.get(root, []):
            for pid in last[cid]:
                if pid in by_para:
                    by_para[pid].set("{%s}done" % W15, "1")
    ext.write(str(ext_path), xml_declaration=True, encoding="UTF-8", standalone=True)


def run_assertions():
    """Evaluate the ASSERT lists of the text modules against numbers.csv: statements the prose makes about the data."""
    def N(key):
        v = NUMS[key]
        try:
            return float(v)
        except ValueError:
            return v
    failed = []
    for mod in (ms_front, ms_methods, ms_results, ms_discussion):
        for expr, why in getattr(mod, "ASSERT", []):
            try:
                ok = bool(eval(expr, {"N": N, "set": set}))
            except Exception as e:  # noqa: BLE001
                ok, why = False, "%s [%s]" % (why, e)
            if not ok:
                failed.append("%s  ::  %s" % (why, expr))
    if failed:
        raise SystemExit("DATA ASSERTIONS FAILED (the text says something the data no longer support):\n  " + "\n  ".join(failed))
    print("data assertions passed:", sum(len(getattr(m, "ASSERT", [])) for m in (ms_front, ms_methods, ms_results, ms_discussion)))


WINDOW = re.compile(r"January(?:\s+to\s+|\s*[–-]\s*)September")


def check_text(blocks):
    """Build-time rules of the text: every paragraph that mentions 2026 must say that 2026 is a partial,
    annualized year (January-September), and the DLNM must not be described."""
    bad = []
    for b in blocks:
        if b["style"] not in ("Abstract", "Body", "Legend"):
            continue
        t = plain(b["tokens"])
        if "2026" in t and not (WINDOW.search(t) and re.search(r"annualized|partial", t)):
            bad.append("2026 without the January-September / annualized qualifier: " + t[:90])
        if re.search(r"DLNM", t):
            bad.append("DLNM still in the text: " + t[:90])
    if bad:
        raise SystemExit("TEXT CHECK FAILED:\n  " + "\n  ".join(bad))


def fix_reply_parents(bdir, replies):
    """Word links a reply to the LAST paragraph of its parent comment; add_comment used the first."""
    cm = etree.parse(str(bdir / "word" / "comments.xml")).getroot()
    W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
    W15 = "http://schemas.microsoft.com/office/word/2012/wordml"
    last_para, para_of = {}, {}
    for c in cm:
        cid = int(c.get("{%s}id" % W_NS))
        ps = [p.get("{%s}paraId" % W14) for p in c.iter("{%s}p" % W_NS)]
        last_para[cid] = ps[-1]
        para_of[cid] = ps[-1]
    ext_path = bdir / "word" / "commentsExtended.xml"
    ext = etree.parse(str(ext_path))
    by_para = {e.get("{%s}paraId" % W15): e for e in ext.getroot()}
    for pid, rids in replies.items():
        for rid in rids:
            e = by_para[para_of[rid]]
            e.set("{%s}paraIdParent" % W15, last_para[pid])
    ext.write(str(ext_path), xml_declaration=True, encoding="UTF-8", standalone=True)
    # comment content uses the style id of this document
    p = bdir / "word" / "comments.xml"
    p.write_text(p.read_text(encoding="utf-8").replace('w:val="CommentReference"', 'w:val="Refdecomentrio"'), encoding="utf-8")


def finish_package(bdir):
    # footer: page number only (the draft's footer parts were never shown)
    for n in ("footer1.xml", "footer2.xml"):
        f = bdir / "word" / n
        if f.exists():
            f.unlink()
    (bdir / "word" / "footer3.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:ftr xmlns:w="%s" xmlns:r="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships"><w:p><w:pPr><w:pStyle w:val="Rodap"/><w:jc w:val="center"/></w:pPr><w:r><w:fldChar '
        'w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar '
        'w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>' % W_NS,
        encoding="utf-8")
    rels = bdir / "word" / "_rels" / "document.xml.rels"
    t = rels.read_text(encoding="utf-8")
    t = re.sub(r'<Relationship Id="rId1[12]"[^>]*footer[^>]*/>', "", t)
    t = t.replace("</Relationships>", '<Relationship Id="rIdFtr1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                                      'relationships/footer" Target="footer3.xml"/></Relationships>')
    rels.write_text(t, encoding="utf-8")
    ct = bdir / "[Content_Types].xml"
    c = ct.read_text(encoding="utf-8")
    c = re.sub(r'<Override PartName="/word/footer[12]\.xml"[^>]*/>', "", c)
    c = c.replace('<Override PartName="/word/fontTable.xml"', '<Override PartName="/word/footer3.xml" ContentType="application/vnd.'
                  'openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/word/fontTable.xml"')
    ct.write_text(c, encoding="utf-8")
    patch_styles(bdir / "word" / "styles.xml")
    core = bdir / "docProps" / "core.xml"
    s = core.read_text(encoding="utf-8")
    s = s.replace("<dc:title></dc:title>", "<dc:title>Spatiotemporal Dynamics and Climatic Correlates of Dengue, Chikungunya, and Zika in Brazil during 2016\u20132026</dc:title>")
    core.write_text(s, encoding="utf-8")


def zip_dir(bdir, zpath):
    if Path(zpath).exists():
        Path(zpath).unlink()
    files = [p for p in bdir.rglob("*") if p.is_file()]
    files.sort(key=lambda p: (str(p.relative_to(bdir)) != "[Content_Types].xml", str(p.relative_to(bdir))))
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, str(p.relative_to(bdir)).replace("\\", "/"))


if __name__ == "__main__":
    main(sys.argv[1])
