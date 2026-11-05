#!/usr/bin/env python3
"""Measured single-cell copy-number spread, and what it does not measure.

Writes figures/output/measured-copy-number-distributions.svg.

WHAT THIS FIGURE IS FOR. `copy-number-and-loss-rate.svg` has exactly one free
biological assumption: that copy number varies across cells, and by how much.
Everything else in it is arithmetic. This figure is the evidence for that
assumption, and the place where its limits are stated.

Shao et al. (2021) count plasmids in single living E. coli by labelling the
backbone with a PhlF-RFP fusion and calibrating spot intensity against the
single-plasmid step. Their Fig. 1e gives copy-number distributions across the
population for four origins. The numbers drawn here are the summary values
reported in their Results text, quoted in the figure and listed below.

WHY THIS DOES NOT REDRAW THEIR DISTRIBUTIONS. Their paper is open access
under CC BY 4.0, so their Fig. 1e may be reproduced with credit, and for a
talk that is the better option -- it shows the shapes. What must NOT be done
is to regenerate those shapes here from the reported mean and standard
deviation, because the companion figure's whole argument is that two moments
do not determine a distribution. Drawing a lognormal from Shao's mean and CV
and captioning it as their measurement would be the exact error that figure
exists to warn about. So this figure plots only what was reported: a mean, a
spread of the same order, and a plasmid-free fraction.

THE THREE THINGS THIS FIGURE EXISTS TO QUALIFY, all from the same paper:

  * A standing plasmid-free fraction is not a loss rate. Those cultures were
    grown under ampicillin and kanamycin selection, which acts against
    plasmid-free cells, so the standing fraction is not even an unbiased
    estimate of accumulated loss, let alone of the per-division rate.
  * The strain is NEB 10-beta, which the paper notes is deficient for
    non-specific nuclease and recombinase (recA1). Multimer formation by
    homologous recombination is therefore largely switched off. This is
    heterogeneity measured with the dimer-catastrophe route suppressed.
  * Their own model needed a fitted PARTITIONING COEFFICIENT alongside a
    replication-control sensitivity, and they note remaining prediction error
    that "could be due to additional sources of randomness in plasmid
    segregation". Plain random partitioning was not assumed and did not come
    out as a fitted conclusion either.

And one result that belongs with the companion figure's toxin-antitoxin
paragraph: adding hok/sok, a system used to minimise plasmid loss, gave the
SAME copy-number distribution. A TA system removes segregants; it does not
narrow the spread that produces them.

Standard library only, deterministic output.

Usage (from the repository root):
    python figures/source/measured_copy_number_distributions.py
"""

import math
from pathlib import Path

import palette

SOURCE_KEYS = ["shao2021singlecell"]

# Reported in the Results text of Shao et al. (2021), Nat Commun 12:1475.
# mean copy number; fraction of cells with no detectable plasmid; n cells.
# The standard deviations are given there as "on the order of the mean copy
# numbers", which is why the spread bar below is drawn as +/- one mean and
# labelled as an order-of-magnitude statement rather than a measured sigma.
BACKBONES = [
    ("pSC101", 4, 0.05, 858),
    ("p15A", 11, 0.03, 553),
    ("ColE1", 15, 0.01, 603),
    ("pUC", 60, 0.01, 355),
]

W, H = 900, 560
PLOT = {"x0": 150, "y0": 150, "x1": 610, "y1": 330}
X_MIN, X_MAX = 1.0, 140.0

ACCENT = palette.OKABE_ITO["blue"]
SPREAD = palette.OKABE_ITO["sky_blue"]

SUP = {"-": "⁻", "0": "⁰", "1": "¹", "2": "²",
       "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
       "7": "⁷", "8": "⁸", "9": "⁹"}


def superscript(n):
    return "".join(SUP[ch] for ch in str(n))


def sx(copies):
    t = ((math.log10(max(copies, X_MIN)) - math.log10(X_MIN))
         / (math.log10(X_MAX) - math.log10(X_MIN)))
    return PLOT["x0"] + t * (PLOT["x1"] - PLOT["x0"])


def text(x, y, s, size=13, colour=None, anchor="start", weight="normal"):
    colour = colour or palette.INK
    return (f'  <text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial,'
            f'sans-serif" font-size="{size}" fill="{colour}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')


def build():
    rows = len(BACKBONES)
    step = (PLOT["y1"] - PLOT["y0"]) / rows
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         f'  <rect width="{W}" height="{H}" fill="{palette.PAPER}"/>']

    o.append(text(48, 42, "The spread is as large as the mean",
                  size=20, weight="bold"))
    o.append(text(48, 66, "Single-cell plasmid counts in E. coli for four "
                          "origins. Standard deviations are on the order of "
                          "the means, so the",
                  size=13, colour=palette.MUTED))
    o.append(text(48, 84, "copy-number heterogeneity the companion figure "
                          "assumes is measured, and larger than most of the "
                          "curves it draws.",
                  size=13, colour=palette.MUTED))

    # --- gridlines at the decades ---
    for e in (0, 1, 2):
        x = sx(10 ** e)
        if x > PLOT["x1"]:
            continue
        o.append(f'  <line x1="{x:.1f}" y1="{PLOT["y0"] - 14}" x2="{x:.1f}" '
                 f'y2="{PLOT["y1"] + 6}" stroke="{palette.RULE}" '
                 f'stroke-width="1"/>')
        o.append(text(x, PLOT["y1"] + 24, f"10{superscript(e)}", size=12,
                      colour=palette.MUTED, anchor="middle"))
    o.append(text((PLOT["x0"] + PLOT["x1"]) / 2, PLOT["y1"] + 48,
                  "Plasmid copies per cell", size=14, anchor="middle"))

    # --- column headings ---
    o.append(text(PLOT["x0"] - 16, PLOT["y0"] - 20, "origin", size=12,
                  colour=palette.MUTED, anchor="end", weight="bold"))
    o.append(text(PLOT["x1"] + 40, PLOT["y0"] - 20, "mean", size=12,
                  colour=palette.MUTED, anchor="middle", weight="bold"))
    o.append(text(PLOT["x1"] + 150, PLOT["y0"] - 34, "cells with", size=12,
                  colour=palette.MUTED, anchor="middle", weight="bold"))
    o.append(text(PLOT["x1"] + 150, PLOT["y0"] - 20, "no plasmid", size=12,
                  colour=palette.MUTED, anchor="middle", weight="bold"))

    # --- one row per backbone ---
    for i, (name, mean, free, n) in enumerate(BACKBONES):
        y = PLOT["y0"] + step * (i + 0.5)
        # Spread bar: mean +/- one mean, since sigma is reported only as
        # being of that order. Drawn hollow so it cannot be read as a
        # measured interval.
        x_lo, x_hi = sx(max(mean - mean, X_MIN)), sx(mean + mean)
        o.append(f'  <rect x="{x_lo:.1f}" y="{y - 9:.1f}" '
                 f'width="{x_hi - x_lo:.1f}" height="18" rx="2" '
                 f'fill="none" stroke="{SPREAD}" stroke-width="1.6" '
                 f'stroke-dasharray="4 3"/>')
        o.append(f'  <circle cx="{sx(mean):.1f}" cy="{y:.1f}" r="6" '
                 f'fill="{ACCENT}"/>')
        o.append(text(PLOT["x0"] - 16, y + 5, name, size=13, anchor="end",
                      weight="bold"))
        o.append(text(PLOT["x1"] + 40, y + 5, str(mean), size=13,
                      anchor="middle"))
        o.append(text(PLOT["x1"] + 150, y + 5, f"{free:.0%}", size=13,
                      anchor="middle", weight="bold"))
        o.append(text(PLOT["x1"] + 214, y + 5, f"n = {n}", size=11,
                      colour=palette.MUTED))

    o.append(text(PLOT["x0"], PLOT["y1"] + 74,
                  "Dashed box spans the mean ± one mean: the paper "
                  "reports the standard deviations only as being of that "
                  "order, so it is a", size=11, colour=palette.MUTED))
    o.append(text(PLOT["x0"], PLOT["y1"] + 90,
                  "statement about scale, not a measured interval. Many "
                  "cells carried four times the mean or more.",
                  size=11, colour=palette.MUTED))

    # --- what this does not measure ---
    y0 = PLOT["y1"] + 122
    o.append(f'  <rect x="48" y="{y0 - 16}" width="186" height="22" rx="3" '
             f'fill="{palette.INK}"/>')
    o.append(text(141, y0 - 1, "WHAT IT DOES NOT SHOW", size=12,
                  colour=palette.PAPER, anchor="middle", weight="bold"))
    notes = [
        ("A loss rate.", " Those are standing plasmid-free fractions, under "
         "ampicillin and kanamycin selection, which acts against exactly "
         "the cells being counted."),
        ("Multimerisation.", " The strain is NEB 10-beta, deficient for "
         "recombinase, so the dimer route to plasmid-free cells is largely "
         "switched off here."),
        ("Random partitioning.", " Their model fits a partitioning "
         "coefficient, and they attribute residual error to further "
         "randomness in segregation."),
    ]
    # Tails share one left edge rather than being offset by the width of each
    # heading, which made the block visibly ragged.
    for j, (head, tail) in enumerate(notes):
        yy = y0 + 20 + j * 17
        o.append(text(48, yy, head, size=11, weight="bold"))
        o.append(text(176, yy, tail.lstrip(), size=11, colour=palette.MUTED))

    o.append(text(48, y0 + 20 + len(notes) * 17 + 6,
                  "Adding the hok/sok toxin-antitoxin system gave the same "
                  "distribution: it removes segregants, it does not narrow "
                  "the spread that makes them.",
                  size=11, weight="bold"))
    o.append(text(48, y0 + 20 + len(notes) * 17 + 24,
                  "Values from the Results text of Shao et al. 2021, Nat "
                  "Commun 12:1475 (CC BY 4.0); their Fig. 1e has the "
                  "distribution shapes.  Source: " + ", ".join(SOURCE_KEYS),
                  size=11, colour=palette.MUTED))

    o.append("</svg>")
    return "\n".join(o) + "\n"


def main():
    out = (Path(__file__).resolve().parents[1] / "output"
           / "measured-copy-number-distributions.svg")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
