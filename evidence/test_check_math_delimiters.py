#!/usr/bin/env python3
"""Known-negatives for check_math_delimiters: it must go red, and stay green.

A checker that has only ever reported clean is not known to work. Each case
below is a small synthetic tree scanned by the real `scan` function, with the
verdict it must produce. Half assert a failure and half assert silence,
because a check that flags everything is as useless as one that flags
nothing — and the silent cases are the ones that would make the check
untrustworthy enough to be switched off.

Usage:
    python evidence/test_check_math_delimiters.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_math_delimiters import scan  # noqa: E402

D = chr(36)

#: (label, markdown source, must this be flagged?)
CASES: list[tuple[str, str, bool]] = [
    ("display delimiters in prose",
     r"The growth law is \[ \mu = \mu_{max} S/(K+S) \] for a Monod term.",
     True),
    ("inline delimiters in prose",
     r"with carrying capacity \(K\) fixed at one million.",
     True),
    ("both on separate lines",
     "Resource dynamics:\n\n" + r"\[ b = \beta C \]" + "\n\nand so on.",
     True),
    ("only the closing delimiter survives an edit",
     r"The term is $$ \beta C \] which is half converted.",
     True),

    ("dollar delimiters are the fix, not a problem",
     f"The growth law is {D}{D} \\mu = S/(K+S) {D}{D} for a Monod term.",
     False),
    ("inline dollars",
     f"with carrying capacity {D}K{D} fixed.",
     False),
    ("a regex in a fenced code block",
     "Strip them first:\n\n```python\n"
     r"FENCE = re.compile(r'\[|\(')" + "\n```\n\nas above.",
     False),
    ("a regex in an inline code span",
     "The pattern `re.findall(r'\\(')` finds open parens.",
     False),
    ("a literal escaped dollar in prose",
     f"It costs \\{D}5 per reaction.",
     False),
    ("ordinary brackets and parens, unescaped",
     "See Table [3] and the note (above) for details.",
     False),
]


def main() -> int:
    failures = []
    for label, source, should_flag in CASES:
        hits = scan(source, "probe.md")
        flagged = bool(hits)
        if flagged != should_flag:
            want = "flagged" if should_flag else "silent"
            got = "flagged" if flagged else "silent"
            failures.append(f"{label}: expected {want}, got {got}"
                            + (f" ({hits[0]})" if hits else ""))
        verdict = "red " if flagged else "green"
        want_s = "must be red " if should_flag else "must be green"
        mark = "ok" if flagged == should_flag else "WRONG"
        print(f"  {verdict}  {want_s}  {mark:5s}  {label}")

    n_red = sum(1 for _, _, f in CASES if f)
    print(f"\n  {len(CASES)} cases: {n_red} assert a failure, "
          f"{len(CASES) - n_red} assert silence")

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("  the checker responds correctly to all of them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
