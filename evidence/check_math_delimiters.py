#!/usr/bin/env python3
"""Refuse LaTeX-style maths delimiters that markdown destroys before MathJax.

WHY THIS EXISTS. Jupyter, Colab and GitHub all run markdown through a
CommonMark parser before any maths renderer sees it, and that parser treats a
backslash before ASCII punctuation as an escape. So `\\[` is emitted as a
literal `[` and the delimiter is gone one stage before the thing that would
have used it. The reader sees raw LaTeX.

Measured through nbconvert's own renderer, on this repository's notebook:

    \\[ r(C)=1-\\beta C \\]   ->   <p>[ r(C)=1-\\beta C ]</p>
    $$ r(C)=1-\\beta C $$   ->   <p>$$ r(C)=1-\\beta C $$</p>

Dollar delimiters survive because `$` is not escapable punctuation. Eighteen
display equations and twenty-four inline ones shipped broken in
`battle-royale.ipynb` and were visible to anyone who opened it; one equation
in the same file used `$$` and had been rendering correctly the whole time.

This will recur without a check, because `\\[...\\]` is correct LaTeX and is
what Overleaf, papers and most assistants emit. It is only wrong once the
LaTeX is embedded in markdown.

WHY IT LIVES IN `evidence/`. Not because it checks evidence, but because
this is where the checkers that scan the whole tree live. The alternative was
a new top-level directory for one file.

DOMAIN. Markdown only: `.md` files, and the markdown cells of `.ipynb`.
Code cells are never read, and neither is any other file type — a backslash
before a bracket is ordinary in Python, and flagging it there would make the
check untrustworthy rather than stricter.

WHAT IT DELIBERATELY DOES NOT FLAG. Fenced code blocks and inline code spans
inside markdown, because documenting a regex is not writing an equation.
`check_references.py` and this file both contain `\\(` in prose about
patterns; stripping code first is what lets this check coexist with writing
about the problem it detects.

Usage:
    python evidence/check_math_delimiters.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

#: Display and inline LaTeX delimiters. The pair that markdown eats.
BAD = {
    r"\[": "display open",
    r"\]": "display close",
    r"\(": "inline open",
    r"\)": "inline close",
}

FENCE = re.compile(r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$", re.M | re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(text: str) -> str:
    """Blank out code, preserving line structure so line numbers stay true."""
    def blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))
    return INLINE_CODE.sub(blank, FENCE.sub(blank, text))


def scan(text: str, where: str) -> list[str]:
    hits = []
    for lineno, line in enumerate(strip_code(text).splitlines(), 1):
        for token, kind in BAD.items():
            if token in line:
                hits.append(f"{where}:{lineno}  {kind} `{token}`  "
                            f"{line.strip()[:64]}")
    return hits


def tracked(*patterns: str) -> list[Path]:
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", *patterns],
                         capture_output=True, text=True, check=True)
    return [REPO / p for p in out.stdout.split("\n") if p.strip()]


def main() -> int:
    problems: list[str] = []
    md_files = tracked("*.md")
    nb_files = tracked("*.ipynb")

    for p in md_files:
        problems += scan(p.read_text(encoding="utf-8"),
                         p.relative_to(REPO).as_posix())

    cells_read = 0
    for p in nb_files:
        nb = json.loads(p.read_text(encoding="utf-8"))
        for i, cell in enumerate(nb.get("cells", [])):
            if cell.get("cell_type") != "markdown":
                continue
            cells_read += 1
            src = "".join(cell.get("source", []))
            problems += scan(src, f"{p.relative_to(REPO).as_posix()}[cell {i}]")

    print(f"markdown scanned: {len(md_files)} .md files, "
          f"{cells_read} markdown cells in {len(nb_files)} notebooks")
    print("code fences and inline code spans excluded; code cells never read")

    if problems:
        print("\nPROBLEMS: markdown will eat these before MathJax sees them.")
        for q in problems:
            print(f"  {q}")
        print(f"\n{len(problems)} occurrence(s). Use $...$ and $$...$$ "
              "instead; `$` is not escapable punctuation and survives.")
        return 1

    print("\nno problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
