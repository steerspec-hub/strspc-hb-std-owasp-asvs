"""Sentence splitting for ASVS requirement text.

A sentence ends at '.', '!' or '?' followed by whitespace and an upper-case letter
or a backtick, except after a known abbreviation. Text inside backticks is never split.
"""

import re

ABBREVIATIONS = ("e.g.", "i.e.", "etc.", "vs.", "cf.", "Fig.", "No.", "approx.")
_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z`\"'(])")


def split_sentences(text: str) -> list[str]:
    text = " ".join(text.split())
    parts, start = [], 0
    for m in _END.finditer(text):
        before = text[start : m.start()]
        if before.count("`") % 2:
            continue
        if before.endswith(ABBREVIATIONS):
            continue
        parts.append(before.strip())
        start = m.end()
    parts.append(text[start:].strip())
    return [p for p in parts if p]
