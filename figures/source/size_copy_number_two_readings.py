#!/usr/bin/env python3
"""Illustrative figure: one cloud, two laws.

Writes figures/output/size-copy-number-two-readings.svg.

WHAT THIS FIGURE IS FOR. The lecture plan asks for "one clean scaling-law
empirical figure". Clean is the risk: a single fitted line through plasmid
size against copy number is a contested claim drawn as a fact. Two published
studies fit a single power law; a 2026 preprint argues a segmented fit over
two strategies is the better model, and that the form and interpretation are
both disputed. A reader shown one line remembers one line.

So this draws the **model-form question**, not the data.

THE POINTS ARE SYNTHETIC AND SAY SO. Every point is generated here by a
deterministic generator with a fixed seed. Nothing is read from any dataset,
no published point is reproduced, and the axis values are plausible ranges
rather than measurements. The figure is badged ILLUSTRATIVE for exactly that
reason. **It does not replace the empirical figure the plan asks for and must
not be captioned as one.**

WHY BOTH LINES ARE FITTED, NOT DRAWN. Both the pooled line and the segmented
pair are least-squares fits computed here from the points that are plotted.
Hand-placing them would let the figure show a contrast its own data does not
support, which is the failure it exists to warn about.

WHY "NOT COMPARABLE" AND NOT "CONTESTED". Under scope before status in
evidence/evidence-levels.md, an apparent contradiction is only `contested`
when the findings make the same claim under comparable conditions. These do
not: the two 2025 studies use different estimators and different definitions
of copy number -- one is copies per cell, the other copies per longest
chromosome per cell. The first gate of that decision tree answers NO, so the
comparison is NOT COMPARABLE. That is the sharper teaching point anyway: the
studies are not disagreeing so much as measuring different quantities.

Standard library only: no numpy, no matplotlib, no network. Deterministic
output, so a rebuild produces a byte-identical file.

Usage (from the repository root):
    python figures/source/size_copy_number_two_readings.py
"""

import math
from pathlib import Path

import palette

# Keys for the footer, read by evidence/check_references.py. Declared rather
# than typed into the footer string, for the reason the sibling figure gives.
SOURCE_KEYS = [
    "ramiromartinez2025universal",
    "maddamsetti2025scaling",
    "shahzadi2026determinants",
    "shaw2026strategies",
]

# A fixed seed and an LCG written out in full. random.Random would almost
# certainly be stable too, but byte-identical rebuild is a promise this
# repository makes, and keeping the generator in the file makes that promise
# depend on this code rather than on a library's forward compatibility.
SEED = 20261103
_LCG_A, _LCG_C, _LCG_M = 1103515245, 12345, 2 ** 31


def _rng():
    state = SEED
    while True:
        state = (_LCG_A * state + _LCG_C) % _LCG_M
        yield state / _LCG_M


# Synthetic regimes. Plausible ranges, not measurements.
BREAK_KB = 20.0          # where the declared generator changes slope
SLOPE_SMALL = -0.95      # steep: inheritance depends on numbers
SLOPE_LARGE = -0.15      # shallow: active partition handles inheritance
N_POINTS = 150

W, H = 900, 580
PLOT = {"x0": 96, "y0": 78, "x1": 660, "y1": 430}
X_MIN_KB, X_MAX_KB = 1.0, 500.0
Y_MIN, Y_MAX = 0.8, 400.0


def generate():
    """Points, and the two fits, both computed from those points."""
    rnd = _rng()
    pts = []
    for _ in range(N_POINTS):
        u = next(rnd)
        size = X_MIN_KB * (X_MAX_KB / X_MIN_KB) ** u
        lb = math.log10(BREAK_KB)
        ls = math.log10(size)
        intercept_small = 2.35
        if ls <= lb:
            lp = intercept_small + SLOPE_SMALL * ls
        else:
            lp = intercept_small + SLOPE_SMALL * lb + SLOPE_LARGE * (ls - lb)
        noise = (next(rnd) + next(rnd) + next(rnd) - 1.5) * 0.30
        pcn = 10 ** (lp + noise)
        pts.append((size, min(max(pcn, Y_MIN), Y_MAX)))
    pts.sort()

    def ols(sample):
        n = len(sample)
        xs = [math.log10(s) for s, _ in sample]
        ys = [math.log10(p) for _, p in sample]
        mx, my = sum(xs) / n, sum(ys) / n
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        sxx = sum((x - mx) ** 2 for x in xs)
        slope = sxy / sxx
        return slope, my - slope * mx

    pooled = ols(pts)
    small = ols([p for p in pts if p[0] <= BREAK_KB])
    large = ols([p for p in pts if p[0] > BREAK_KB])
    return pts, pooled, small, large


def sx(size_kb):
    t = (math.log10(size_kb) - math.log10(X_MIN_KB)) / (
        math.log10(X_MAX_KB) - math.log10(X_MIN_KB))
    return PLOT["x0"] + t * (PLOT["x1"] - PLOT["x0"])


def sy(pcn):
    t = (math.log10(pcn) - math.log10(Y_MIN)) / (
        math.log10(Y_MAX) - math.log10(Y_MIN))
    return PLOT["y1"] - t * (PLOT["y1"] - PLOT["y0"])


def fit_line(slope, intercept, lo_kb, hi_kb, colour, dash, width=2.4):
    x1, x2 = sx(lo_kb), sx(hi_kb)
    y1 = sy(10 ** (intercept + slope * math.log10(lo_kb)))
    y2 = sy(10 ** (intercept + slope * math.log10(hi_kb)))
    return (f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{colour}" stroke-width="{width}" '
            f'stroke-dasharray="{dash}" stroke-linecap="round"/>')


def text(x, y, s, size=13, colour=None, anchor="start", weight="normal"):
    colour = colour or palette.INK
    return (f'  <text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial,'
            f'sans-serif" font-size="{size}" fill="{colour}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')


def build():
    pts, pooled, small, large = generate()
    c_small = palette.OKABE_ITO["vermillion"]
    c_large = palette.OKABE_ITO["blue"]
    c_pooled = palette.INK

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         f'  <rect width="{W}" height="{H}" fill="{palette.PAPER}"/>']

    o.append(text(48, 36, "Plasmid size against copy number: one cloud, two laws",
                  size=19, weight="bold"))
    o.append(text(48, 58, "Synthetic points. The question is which model form "
                          "the data supports, not where the line sits.",
                  size=13, colour=palette.MUTED))

    # axes
    o.append(f'  <line x1="{PLOT["x0"]}" y1="{PLOT["y1"]}" x2="{PLOT["x1"]}" '
             f'y2="{PLOT["y1"]}" stroke="{palette.INK}" stroke-width="1.2"/>')
    o.append(f'  <line x1="{PLOT["x0"]}" y1="{PLOT["y0"]}" x2="{PLOT["x0"]}" '
             f'y2="{PLOT["y1"]}" stroke="{palette.INK}" stroke-width="1.2"/>')
    for kb in (1, 10, 100, 500):
        x = sx(kb)
        o.append(f'  <line x1="{x:.1f}" y1="{PLOT["y1"]}" x2="{x:.1f}" '
                 f'y2="{PLOT["y1"]+5}" stroke="{palette.INK}" stroke-width="1"/>')
        o.append(text(x, PLOT["y1"] + 20, f"{kb}", size=12, anchor="middle",
                      colour=palette.MUTED))
    for pcn in (1, 10, 100):
        y = sy(pcn)
        o.append(f'  <line x1="{PLOT["x0"]-5}" y1="{y:.1f}" x2="{PLOT["x0"]}" '
                 f'y2="{y:.1f}" stroke="{palette.INK}" stroke-width="1"/>')
        o.append(text(PLOT["x0"] - 11, y + 4, f"{pcn}", size=12, anchor="end",
                      colour=palette.MUTED))
    o.append(text((PLOT["x0"] + PLOT["x1"]) / 2, PLOT["y1"] + 44,
                  "plasmid size (kb, log scale)", size=13, anchor="middle"))
    o.append(f'  <text x="34" y="{(PLOT["y0"]+PLOT["y1"])/2:.1f}" '
             f'font-family="Helvetica,Arial,sans-serif" font-size="13" '
             f'fill="{palette.INK}" text-anchor="middle" '
             f'transform="rotate(-90 34 {(PLOT["y0"]+PLOT["y1"])/2:.1f})">'
             f'copies per cell (log scale)</text>')

    # breakpoint guide
    xb = sx(BREAK_KB)
    o.append(f'  <line x1="{xb:.1f}" y1="{PLOT["y0"]}" x2="{xb:.1f}" '
             f'y2="{PLOT["y1"]}" stroke="{palette.RULE}" stroke-width="1" '
             f'stroke-dasharray="3 4"/>')

    # points
    for size, pcn in pts:
        col = c_small if size <= BREAK_KB else c_large
        o.append(f'  <circle cx="{sx(size):.1f}" cy="{sy(pcn):.1f}" r="3.1" '
                 f'fill="{col}" fill-opacity="0.42"/>')

    # fits, computed above from these points
    o.append(fit_line(*pooled, X_MIN_KB, X_MAX_KB, c_pooled, "none", 2.8))
    o.append(fit_line(*small, X_MIN_KB, BREAK_KB, c_small, "7 4"))
    o.append(fit_line(*large, BREAK_KB, X_MAX_KB, c_large, "7 4"))

    # legend
    lx, ly = PLOT["x1"] + 26, PLOT["y0"] + 6
    o.append(text(lx, ly, "TWO READINGS", size=12, weight="bold",
                  colour=palette.MUTED))
    o.append(f'  <line x1="{lx}" y1="{ly+20}" x2="{lx+28}" y2="{ly+20}" '
             f'stroke="{c_pooled}" stroke-width="2.8"/>')
    o.append(text(lx + 36, ly + 24, "one law", size=12, weight="bold"))
    o.append(text(lx, ly + 42, f"pooled slope {pooled[0]:+.2f}", size=11,
                  colour=palette.MUTED))
    o.append(f'  <line x1="{lx}" y1="{ly+70}" x2="{lx+28}" y2="{ly+70}" '
             f'stroke="{c_small}" stroke-width="2.4" stroke-dasharray="7 4"/>')
    o.append(text(lx + 36, ly + 74, "two regimes", size=12, weight="bold"))
    o.append(text(lx, ly + 92, f"small  {small[0]:+.2f}", size=11,
                  colour=c_small))
    o.append(text(lx, ly + 108, f"large  {large[0]:+.2f}", size=11,
                  colour=c_large))

    o.append(text(lx, ly + 142, "many copies", size=11, colour=c_small))
    o.append(text(lx, ly + 157, "= redundancy", size=11, colour=c_small))
    o.append(text(lx, ly + 180, "few copies +", size=11, colour=c_large))
    o.append(text(lx, ly + 195, "active partition", size=11, colour=c_large))

    # badges
    bx, by = 48, PLOT["y1"] + 76
    for i, (label, note) in enumerate([
        ("ILLUSTRATIVE", "points are synthetic; no dataset is plotted"),
        ("NOT COMPARABLE", "the two studies define copy number differently"),
    ]):
        y = by + i * 26
        o.append(f'  <rect x="{bx}" y="{y-13}" width="128" height="19" rx="3" '
                 f'fill="none" stroke="{palette.MUTED}" stroke-width="1"/>')
        o.append(text(bx + 8, y + 1, label, size=11, weight="bold",
                      colour=palette.MUTED))
        o.append(text(bx + 144, y + 1, note, size=12, colour=palette.MUTED))

    o.append(text(48, H - 56,
                  "A single line and a breakpoint fit the same cloud. Which is "
                  "right is open; one line drawn alone decides it silently.",
                  size=13))
    o.append(text(48, H - 20, "sources: " + " · ".join(SOURCE_KEYS), size=10,
                  colour=palette.MUTED))
    o.append("</svg>")
    return "\n".join(o) + "\n"


def main():
    out = Path(__file__).resolve().parent.parent / "output" / \
        "size-copy-number-two-readings.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    # newline="\n" explicitly, so a rebuild on Windows matches one elsewhere.
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build())
    pts, pooled, small, large = generate()
    print(f"wrote {out.name}")
    print(f"  {len(pts)} synthetic points, seed {SEED}")
    print(f"  pooled slope   {pooled[0]:+.3f}")
    print(f"  small-plasmid  {small[0]:+.3f}   large-plasmid {large[0]:+.3f}")
    print("  ILLUSTRATIVE: no dataset is plotted and no published point is "
          "reproduced.")


if __name__ == "__main__":
    main()
