"""Generate the ASVS 5.0.0 Standard Realm from OWASP's machine-readable release.

Usage:
    python3 tools/generate.py [--source source/<file>.flat.json] [--dir rules] [--strspc strspc]

The script only runs strspc commands; it never writes rule JSON itself, so every
hash is computed by strspc.

- One entity per chapter (V1 -> V01) and one sub-entity per section (V1.2 -> V01S02).
  EUIDs have 3 to 18 characters, and zero-padding keeps them in the standard's order.
- Each requirement becomes one rule per sentence, in the standard's order, with
  `clause` set to the requirement number (V1.2.2) and `profiles` set from its
  minimum level: levels are cumulative, so L1 -> L1,L2,L3, L2 -> L2,L3, L3 -> L3.
- Rule bodies are the standard's text. Only Markdown escapes of punctuation are
  removed (`\\*` -> `*`, `\\_` -> `_`), so `Sec-Fetch-\\*` reads `Sec-Fetch-*` as the
  standard shows it. Escapes such as `\\t`, `\\0` and `\\r\\n`, which the standard
  writes literally, are kept.

Regeneration starts from an empty realm: delete the entity files under rules/
(keep realm.json and _schema/) and rerun. Once rules are Published, a fix is a
`strspc rule supersede`, never a regeneration, because rule IDs are never reused.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sentences import split_sentences  # noqa: E402

DEFAULT_SOURCE = "source/OWASP_Application_Security_Verification_Standard_5.0.0_en.flat.json"
ADDED_BY = "github:pleberre"
PROFILES = {"1": "L1,L2,L3", "2": "L2,L3", "3": "L3"}
MD_ESCAPE = re.compile(r"\\([*_`\[\]#])")


def chapter_euid(chapter_id: str) -> str:
    return f"V{int(chapter_id[1:]):02d}"


def section_euid(section_id: str) -> str:
    chapter, section = section_id[1:].split(".")
    return f"V{int(chapter):02d}S{int(section):02d}"


def body_text(text: str) -> str:
    return MD_ESCAPE.sub(r"\1", text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    ap.add_argument("--dir", default="rules")
    ap.add_argument("--strspc", default="strspc")
    ap.add_argument("--chapter", help="generate only this chapter, for example V1")
    args = ap.parse_args()

    reqs = json.loads(Path(args.source).read_text(encoding="utf-8"))["requirements"]
    if args.chapter:
        reqs = [r for r in reqs if r["chapter_id"] == args.chapter]

    env = dict(os.environ, STRSPC_ADDED_BY=ADDED_BY)

    def run(*cmd: str) -> None:
        subprocess.run([args.strspc, *cmd, "--dir", args.dir], check=True, env=env, stdout=subprocess.DEVNULL)

    chapters, sections, rules = set(), set(), 0
    for r in reqs:
        ch, sec = chapter_euid(r["chapter_id"]), section_euid(r["section_id"])
        if ch not in chapters:
            run("realm", "add", ch, "--title", r["chapter_name"])
            chapters.add(ch)
        if sec not in sections:
            run("entity", "add", sec, "--parent", ch, "--title", r["section_name"])
            sections.add(sec)
        for sentence in split_sentences(body_text(r["req_description"])):
            run("rule", "add", sec, "--body", sentence, "--clause", r["req_id"], "--profiles", PROFILES[r["L"]])
            rules += 1
    print(f"{len(chapters)} chapters, {len(sections)} sections, {len(reqs)} requirements, {rules} rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
