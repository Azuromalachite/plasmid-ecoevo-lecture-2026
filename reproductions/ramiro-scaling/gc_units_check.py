#!/usr/bin/env python3
"""The gc column of curateddataset.csv is in mixed units.

2,155 of the 3,961 rows are fractions and 1,806 are percentages, with no
values at all between 1 and 25. Both halves have the same underlying GC,
so it is a unit mix and not two populations.

Nothing in this repository reads that column, so no result here is
affected. This script exists so that the defect is recorded with a
procedure rather than only as prose, and so that anyone reusing the file
can see it in one run.

Usage:
    python -I gc_units_check.py reproductions/ramiro-scaling/curateddataset.csv
"""
import csv
import statistics as st
import sys
from pathlib import Path


def main(path):
    v = []
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            try:
                v.append(float(r["gc"]))
            except (TypeError, ValueError, KeyError):
                pass
    assert v, "no gc values parsed; has the column been renamed?"
    v.sort()
    frac = [x for x in v if x <= 1.0]
    pct = [x for x in v if x > 1.0]
    middle = [x for x in v if 1.0 < x < 25.0]

    print(f"{len(v):,} gc values")
    print(f"  at or below 1.0 : {len(frac):>5}  median {st.median(frac):.3f}")
    print(f"  above 1.0       : {len(pct):>5}  median {st.median(pct):.2f}")
    print(f"  between 1 and 25: {len(middle):>5}")
    print(f"  raw mean {st.mean(v):.2f}, sd {st.pstdev(v):.2f}  "
          f"<- not a GC distribution")

    assert len(frac) > 100 and len(pct) > 100, (
        "the mixed-unit pattern is gone; if the upstream file has been "
        "fixed, delete this script and the note in RESULTS.md")
    assert not middle, (
        f"{len(middle)} values sit between 1 and 25, which the two-unit "
        f"reading does not allow; re-examine before trusting the fix")

    # the two halves describe the same quantity
    a, b = st.median([x * 100 for x in frac]), st.median(pct)
    print(f"\n  fractions rescaled to percent: median {a:.2f}")
    print(f"  values already in percent    : median {b:.2f}")
    print(f"  difference {abs(a-b):.2f} points -> one quantity, two units")
    assert abs(a - b) < 5, (
        "the two halves differ too much to be the same quantity in "
        "different units; the mixed-unit reading may be wrong")

    fixed = [x * 100 if x <= 1.0 else x for x in v]
    print(f"\n  normalised: mean {st.mean(fixed):.2f}%, "
          f"sd {st.pstdev(fixed):.2f}, range {min(fixed):.2f}-{max(fixed):.2f}")
    assert 20 < st.mean(fixed) < 75, "normalised GC is still not plausible"
    print("\nall assertions passed")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
