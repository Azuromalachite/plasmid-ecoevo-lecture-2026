#!/usr/bin/env python3
"""What a cell pays for is length TIMES copy number.

Every fit in this directory regresses copy number on relative plasmid
size and reports a slope. A slope of -0.62 is a number until you have
something to compare it against, and the comparison that matters is not
zero.

    load = size x copy number          (total plasmid DNA per cell)
    PCN proportional to size^b   =>    load proportional to size^(1+b)

    b = -1   load constant. Copy number cancels size exactly and every
             plasmid costs its host the same amount of DNA.
    b < -1   load falls with size. Bigger plasmids would cost less.
    b > -1   load rises with size. Copy number only partly compensates.

So -1 is the null worth stating, and the distance from it is the
biologically interpretable quantity. This script reports it, and the
decile table that shows the same thing without fitting anything.

The arithmetic is elementary and the slopes are already published; this
exists so the baseline is stated once, with a procedure, rather than left
for each reader to work out.

Usage:
    python -I dna_load.py curateddataset.csv [--json OUT]
"""
import argparse
import csv
import json
import math
import statistics as st
import sys
from pathlib import Path

import numpy as np


def sse(cols, y):
    M = np.column_stack(cols)
    b, *_ = np.linalg.lstsq(M, y, rcond=None)
    return float(((y - M @ b) ** 2).sum()), b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--knee", type=float, default=1.73,
                    help="breakpoint in %% of chromosome, for the split "
                         "report only; its location is not defended here")
    ap.add_argument("--json", help="write a payload for the figure")
    a = ap.parse_args()

    rows = []
    with Path(a.data).open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            try:
                bp = 10 ** float(r["Logsize"])
                pcn = float(r["PCN"])
                chrl = float(r["Length_chr"])
            except (TypeError, ValueError):
                continue
            if bp <= 0 or pcn <= 0 or chrl <= 0:
                continue
            rows.append({"bp": bp, "pcn": pcn, "chr": chrl,
                         "rel": 100 * bp / chrl, "load": bp * pcn})
    assert rows, "no usable rows; check the column names"
    print(f"{len(rows):,} plasmids\n")

    print("the two plasmids that make the point")
    print(f"   3 kb x 500 copies = {3_000*500/1e6:.1f} Mb of plasmid DNA")
    print(f"  30 kb x  10 copies = {30_000*10/1e6:.1f} Mb")
    print(f"  -> {3_000*500/(30_000*10):.0f}x the load from a plasmid "
          f"{30_000/3_000:.0f}x shorter\n")

    x = np.array([math.log10(r["rel"]) for r in rows])
    y = np.array([math.log10(r["pcn"]) for r in rows])
    lo = np.array([math.log10(r["load"]) for r in rows])
    # load as a FRACTION of the host chromosome. Everything else here is
    # regressed on relative size, and only this normalisation makes the
    # identity exact: log(rel x pcn) = log(rel) + log(pcn), so its slope is
    # 1 + the copy-number slope with nothing left over. Absolute load in bp
    # is reported too, because the intuition is easier in megabases, but
    # its slope carries a little chromosome-length covariation and is not
    # the one to assert on.
    lor = np.array([math.log10(r["rel"] * r["pcn"]) for r in rows])
    one = np.ones(len(x))
    _, b_pcn = sse([one, x], y)
    _, b_load = sse([one, x], lo)
    _, b_rel = sse([one, x], lor)

    print("fitted against relative size, pooled")
    print(f"  copy number slope            {b_pcn[1]:+.3f}")
    print(f"  load slope, % of chromosome  {b_rel[1]:+.3f}")
    print(f"  load slope, absolute bp      {b_load[1]:+.3f}")
    print(f"  constant load would be  -1.000  and  +0.000")
    assert abs((1 + b_pcn[1]) - b_rel[1]) < 1e-9, (
        f"load slope {b_rel[1]:.6f} is not 1 + pcn slope "
        f"{1+b_pcn[1]:.6f}; the identity this script rests on has broken")
    print(f"  (checked exactly: relative-load slope == 1 + "
          f"copy-number slope)")
    print(f"  the {abs(b_load[1]-b_rel[1]):.3f} gap between the two load "
          f"slopes is chromosome length covarying with relative size, "
          f"not an error")

    xc = math.log10(a.knee)
    z = np.maximum(0.0, x - xc)
    _, bs = sse([one, x, z], y)
    below, above = bs[1], bs[1] + bs[2]
    print(f"\nsplit at {a.knee}% of chromosome")
    print(f"  {'':<16}{'PCN slope':>11}{'load slope':>12}"
          f"{'size increase paid for':>24}")
    for lab, s in (("below", below), ("above", above)):
        print(f"  {lab:<16}{s:>+11.3f}{1+s:>+12.3f}{-s:>23.0%}")
    assert below < above, (
        "the fit is no longer flattening above the knee; the sentences "
        "below about weakening compensation would need rewriting")
    print("  -> compensation is partial everywhere, and weaker for the "
          "larger plasmids")

    # The bent load fit is NOT a second result. In relative units
    # log(rel x pcn) = log(rel) + log(pcn), so the load regression is the
    # copy-number regression with 1 added to one coefficient and the hinge
    # term untouched: identical residuals, identical knee, identical dAIC.
    # Check it rather than assert it in prose.
    _, bl = sse([one, x, z], lor)
    assert abs((1 + below) - bl[1]) < 1e-9 and abs(bs[2] - bl[2]) < 1e-9, (
        "the segmented load fit is no longer a reparametrisation of the "
        "segmented copy-number fit, which the write-up relies on")
    print("  (checked: the bent load fit is the bent copy-number fit with "
          "1 added to one slope -- same residuals, same knee, same dAIC, "
          "so it must not be quoted as independent evidence of a bend)")

    # absolute load IS a different fit, and lands somewhere else
    best = None
    for c in np.linspace(np.quantile(x, .08), np.quantile(x, .92), 300):
        s, b = sse([one, x, np.maximum(0.0, x - c)], lo)
        if best is None or s < best[0]:
            best = (s, b, c)
    print(f"  absolute load, knee searched: {10**best[2]:.2f}% against "
          f"{a.knee}% for copy number -- a factor of "
          f"{max(a.knee, 10**best[2])/min(a.knee, 10**best[2]):.1f} apart, "
          f"from two ways of writing the same burden")

    print("\nthe same thing without fitting anything, by size decile")
    qs = np.quantile([r["rel"] for r in rows], np.linspace(0, 1, 11))
    print(f"  {'relative size':<22}{'n':>6}{'med size':>11}{'med PCN':>9}"
          f"{'med load':>11}")
    first = last = None
    for i in range(10):
        sel = [r for r in rows if qs[i] <= r["rel"] <= qs[i + 1]]
        if not sel:
            continue
        m = (st.median([r["bp"] for r in sel]),
             st.median([r["pcn"] for r in sel]),
             st.median([r["load"] for r in sel]))
        first = first or m
        last = m
        print(f"  {f'{qs[i]:.3f}-{qs[i+1]:.3f}%':<22}{len(sel):>6}"
              f"{m[0]:>10,.0f}b{m[1]:>9.1f}{m[2]/1e6:>10.2f}M")
    print(f"\n  copy number falls {first[1]/last[1]:.0f}x across the range; "
          f"load still rises {last[2]/first[2]:.1f}x")
    assert last[2] > first[2], (
        "median load no longer rises with size, which contradicts the "
        "positive load slope above")

    loads = sorted(r["load"] for r in rows)
    over = sum(1 for v in loads if v > 1e6)
    medchr = st.median([r["chr"] for r in rows])
    print(f"  {over:,} plasmids ({100*over/len(rows):.1f}%) carry over 1 Mb "
          f"of plasmid DNA per cell")
    print(f"  the largest load is {loads[-1]/1e6:.1f} Mb, "
          f"{100*loads[-1]/medchr:.0f}% of a median chromosome here")

    if a.json:
        Path(a.json).write_text(json.dumps({
            "n": len(rows),
            "pts": [[round(float(p), 3), round(float(q), 3),
                     round(float(r_), 3)] for p, q, r_ in zip(x, lo, y)],
            "slope_pcn": round(float(b_pcn[1]), 4),
            "slope_load": round(float(b_load[1]), 4),
            "icpt_load": round(float(b_load[0]), 4),
            "below": round(float(below), 4), "above": round(float(above), 4),
            "knee": a.knee}, separators=(",", ":")), encoding="utf-8")
        print(f"\n  wrote {a.json}")
    print("\nall assertions passed")


if __name__ == "__main__":
    main()
