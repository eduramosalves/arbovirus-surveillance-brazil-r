"""Helpers shared by the manuscript source files.

Markup used in block text:
  *italic*  **bold**  ^superscript^  ~subscript~  \\* literal asterisk
  [@r1,@r2]  [@r16-@r18]  [@liu2023]    citations by reference key
  {n:key:fmt}   number from numbers.csv      {u:key[:cap]}  state name from a UF code in numbers.csv
  {cN}..{/cN}   anchor of original comment N   {q:KEY}..{/q} anchor of a new author query
  {hl}..{/hl}   highlighted placeholder        {calc:name}  computed count (abstract_words, main_words, n_refs)
"""
import re

ORIG = {}
for _l in open("orig_markup.txt", encoding="utf-8").read().split("\n"):
    _m = re.match(r"\[(\d+)\] ?(.*)", _l)
    if _m:
        ORIG[int(_m.group(1))] = _m.group(2)

_CIT = re.compile(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]")


def _expand(s):
    out = []
    for part in re.split(r"\s*,\s*", s.strip()):
        m = re.match(r"(\d+)\s*[–-]\s*(\d+)$", part)
        if m:
            out.extend(range(int(m.group(1)), int(m.group(2)) + 1))
        else:
            out.append(int(part))
    return out


def conv_cit(text):
    """[1,2] / [16–18] -> [@r1,@r2] / [@r16,@r17,@r18]"""
    return _CIT.sub(lambda m: "[" + ",".join("@r%d" % n for n in _expand(m.group(1))) + "]", text)


def O(i, *repl):
    """Original paragraph i as markup with converted citations; optional (old, new) replacements, each must match."""
    t = conv_cit(ORIG[i])
    for old, new in repl:
        if old not in t:
            raise ValueError("replacement not found in original [%d]: %r" % (i, old))
        t = t.replace(old, new, 1)
    return t


def strip_runin(t):
    """Drop a leading **run-in heading** (used when the heading becomes its own H2 block)."""
    m = re.match(r"\*\*[^*]+\*\*\s*", t)
    return t[m.end():] if m else t


def B(style, text, orig=None, strip=False, id=None):
    return {"style": style, "text": " ".join(text.split()) if style != "Keep" else text,
            "orig": orig or [], "strip": strip, "id": id}
