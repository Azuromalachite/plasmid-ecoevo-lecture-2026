#!/usr/bin/env python3
"""Analytic figure: mean copy number against segregational loss rate.

Writes figures/output/copy-number-and-loss-rate.svg.

WHAT THIS FIGURE IS FOR. The textbook statement of random segregation gives
one number per copy number: a cell with c copies replicates to 2c, each
molecule goes to one daughter independently, and the chance a daughter gets
none is 2**(-2c). Drawn against copy number on a log axis that is a straight
line, and it is the line most people carry away.

It is also the wrong line for a population. Copy number varies cell to cell,
2**(-2c) is steeply convex, and a convex function averaged over a spread is
not the function at the mean. The rare low-copy cells carry essentially all
of the loss. At a mean of 10 copies the gap between a uniform population and
one with a CV of 0.6 is about three orders of magnitude; by a mean of 20 it
is eight. So the figure draws the straight line and then the curves that
peel away from it, and the point it teaches is that **a mean copy number
does not determine a loss rate**.

ANALYTIC, NOT ILLUSTRATIVE AND NOT CALIBRATED. The repository's other two
figures are badged illustrative because their points are synthetic. This one
has no points at all: every value is computed exactly from
`battle_royale.segregation`, which is the same module the notebook uses. So
nothing here is hand-placed or fitted -- but nothing here is measured
either. The curves are consequences of assumptions, and the assumptions are
printed on the figure:

  * Random segregation ONLY. No partition system, no multimer resolution, no
    clustering, no selection, no conjugation. These curves are a reference
    point and NOT a bound in either direction. Partition systems and multimer
    resolution put a real plasmid below them; multimerisation, clustering and
    fitness cost put one above. For ColE1-type vectors the net is five to
    eight orders of magnitude ABOVE: Summers & Sherratt (1984) measured
    1e-2 to 1e-5 per cell per generation where copy number predicts ~1e-9.
    concepts/random-segregation-is-not-a-floor.md has the evidence.
  * Copy number lognormal across cells, rounded to integers -- the same
    distribution the notebook's single-cell simulation samples from. It is a
    convenient positive, skewed choice. The LEFT TAIL drives every number
    here, and the left tail is what a lognormal is least entitled to claim
    it got right. Treat the vertical spacing between curves as an order of
    magnitude, not a value.
  * Loss is per daughter, averaged over carriers.

WHY THE REFERENCE LINE IS NOT `population_loss_rate(m, cv=0)`. At cv=0 that
function rounds the mean to an integer, so plotting it draws a staircase --
an artefact of the implementation. The smooth floor is `p_daughter_free(m)`
at real-valued m, which is what is drawn.

WHY THE X AXIS STARTS AT 3. Below about 3 copies the ordering of the curves
reverses, for two reasons that are properties of the model rather than bugs:
conditioning on carriers (a carrier holds at least one copy by definition),
and the upward bias of rounding a skewed distribution to integers. Both are
documented and asserted in `segregation.self_check`. Plotting that region
would show curve crossings that have nothing to do with the point being
made, so the figure stays inside the regime where the claim holds.

Standard library only: no numpy, no matplotlib, no network. Deterministic
output, so a rebuild produces a byte-identical file.

Usage (from the repository root):
    python figures/source/copy_number_and_loss_rate.py
"""

import importlib.util
import math
from pathlib import Path

import palette

# Keys for the footer, read by evidence/check_references.py.
SOURCE_KEYS = [
    "ilhan2019segregational",
    "nordstrom1989segregation",
    "paulsson2002multileveled",
    "summers1984multimerization",
]

# The model lives in the models tree and is imported by path rather than
# copied here. A second implementation of 2**(-2c) in this file would be a
# place for the figure and the module to drift apart silently.
_SEG = (Path(__file__).resolve().parents[2] / "models" / "copy-number-burden"
        / "battle_royale" / "segregation.py")
_spec = importlib.util.spec_from_file_location("_segregation", _SEG)
segregation = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(segregation)

W, H = 900, 640
PLOT = {"x0": 104, "y0": 118, "x1": 672, "y1": 452}

X_MIN, X_MAX = 2.0, 20.0
LOG_Y_MIN, LOG_Y_MAX = -13.0, 0.0
N_SAMPLES = 240

# Ordered variable, so the curves are distinguished by position and by a
# label at the end of each line, not by hue. One colour, varying dash.
CVS = [
    (0.1, "2 3"),
    (0.2, "4 3"),
    (0.4, "9 4"),
    (0.6, "none"),
    # Shao et al. (2021) measured standard deviations on the order of the
    # means for pSC101, p15A, ColE1 and pUC, so CV near 1 is the measured
    # regime rather than an extreme. Note what the curve does there: across
    # the whole axis it falls about two decades, while the uniform line falls
    # twelve. At the measured spread, copy number nearly stops mattering.
    (1.0, "1 4"),
]
CURVE = palette.OKABE_ITO["blue"]

# Two populations with the SAME mean copy number at division (40, so 20 at
# birth) and the SAME variance (16, CV 0.10), whose loss rates differ by a
# factor of about 2600. Counts are copies at division. They are plotted as
# marks rather than curves because they are exact distributions, not members
# of the lognormal family the curves sweep -- and they are on the figure
# because (mean, CV) does not determine the answer, which the curves alone
# would quietly imply.
COUNTEREXAMPLES = [
    ("A", [(36, 0.5), (44, 0.5)]),
    ("B", [(20, 0.02), (40, 0.96), (60, 0.02)]),
]
COUNTER_BIRTH_MEAN = 20.0
COUNTER_COLOUR = palette.OKABE_ITO["vermillion"]

# Where the bracket is drawn. Read from the model below, not written here.
CALLOUT_MEAN = 10.0

SUP = {"-": "⁻", "0": "⁰", "1": "¹", "2": "²",
       "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
       "7": "⁷", "8": "⁸", "9": "⁹"}


def superscript(n):
    return "".join(SUP[ch] for ch in str(n))


def sx(mean_copies):
    t = (mean_copies - X_MIN) / (X_MAX - X_MIN)
    return PLOT["x0"] + t * (PLOT["x1"] - PLOT["x0"])


def sy(p):
    t = (math.log10(p) - LOG_Y_MIN) / (LOG_Y_MAX - LOG_Y_MIN)
    return PLOT["y1"] - t * (PLOT["y1"] - PLOT["y0"])


def text(x, y, s, size=13, colour=None, anchor="start", weight="normal"):
    colour = colour or palette.INK
    return (f'  <text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial,'
            f'sans-serif" font-size="{size}" fill="{colour}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')


def polyline(points, colour, dash, width=2.3):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (f'  <polyline points="{pts}" fill="none" stroke="{colour}" '
            f'stroke-width="{width}" stroke-dasharray="{dash}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def sample(point_at):
    """Points across the sweep, dropped where they fall outside the axes.

    `point_at(m)` returns the (x, y) a nominal mean of m belongs at. For the
    spread curves x is the CARRIER mean, not m, which is why this sweeps a
    parameter rather than the axis: see carrier_mean in segregation.py.
    """
    out = []
    lo, hi = 0.8 * X_MIN, X_MAX
    for i in range(N_SAMPLES + 1):
        m = lo + (hi - lo) * i / N_SAMPLES
        x, y = point_at(m)
        if X_MIN <= x <= X_MAX and 10 ** LOG_Y_MIN <= y <= 10 ** LOG_Y_MAX:
            out.append((sx(x), sy(y)))
    return out


def build():
    floor = segregation.p_daughter_free
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         f'  <rect width="{W}" height="{H}" fill="{palette.PAPER}"/>']

    o.append(text(48, 42, "Mean copy number does not determine the loss rate",
                  size=20, weight="bold"))
    o.append(text(48, 66, "Random segregation only. Each curve is one spread "
                          "in copy number across cells; the straight line is "
                          "the textbook formula,", size=13,
                  colour=palette.MUTED))
    o.append(text(48, 84, "which assumes every cell carries the same number. "
                          "A and B show that the curves' two parameters are "
                          "not enough.", size=13, colour=palette.MUTED))

    # --- gridlines, every other decade ---
    for e in range(-12, 1, 2):
        y = sy(10.0 ** e)
        o.append(f'  <line x1="{PLOT["x0"]}" y1="{y:.1f}" x2="{PLOT["x1"]}" '
                 f'y2="{y:.1f}" stroke="{palette.RULE}" stroke-width="1"/>')
        o.append(text(PLOT["x0"] - 12, y + 4.5,
                      f"10{superscript(e)}", size=12,
                      colour=palette.MUTED, anchor="end"))

    # --- axes ---
    o.append(f'  <line x1="{PLOT["x0"]}" y1="{PLOT["y1"]}" x2="{PLOT["x1"]}" '
             f'y2="{PLOT["y1"]}" stroke="{palette.INK}" stroke-width="1.2"/>')
    o.append(f'  <line x1="{PLOT["x0"]}" y1="{PLOT["y0"]}" x2="{PLOT["x0"]}" '
             f'y2="{PLOT["y1"]}" stroke="{palette.INK}" stroke-width="1.2"/>')
    for m in (2, 5, 10, 15, 20):
        x = sx(m)
        o.append(f'  <line x1="{x:.1f}" y1="{PLOT["y1"]}" x2="{x:.1f}" '
                 f'y2="{PLOT["y1"] + 6}" stroke="{palette.INK}" '
                 f'stroke-width="1.2"/>')
        o.append(text(x, PLOT["y1"] + 24, str(m), size=12, anchor="middle"))
    o.append(text((PLOT["x0"] + PLOT["x1"]) / 2, PLOT["y1"] + 50,
                  "Mean copy number among plasmid-bearing cells", size=14,
                  anchor="middle"))
    o.append(f'  <text x="34" y="{(PLOT["y0"] + PLOT["y1"]) / 2:.1f}" '
             f'font-family="Helvetica,Arial,sans-serif" font-size="14" '
             f'fill="{palette.INK}" text-anchor="middle" '
             f'transform="rotate(-90 34 '
             f'{(PLOT["y0"] + PLOT["y1"]) / 2:.1f})">'
             f'Chance a daughter is born plasmid-free</text>')

    # --- the callout bracket, before the curves so lines sit on top ---
    x_call = sx(CALLOUT_MEAN)
    top = sy(segregation.population_loss_rate(CALLOUT_MEAN, 0.6))
    bot = sy(floor(CALLOUT_MEAN))
    ratio = (segregation.population_loss_rate(CALLOUT_MEAN, 0.6)
             / floor(CALLOUT_MEAN))
    o.append(f'  <line x1="{x_call:.1f}" y1="{top:.1f}" x2="{x_call:.1f}" '
             f'y2="{bot:.1f}" stroke="{palette.MUTED}" stroke-width="1.4" '
             f'stroke-dasharray="3 3"/>')
    for y in (top, bot):
        o.append(f'  <line x1="{x_call - 6:.1f}" y1="{y:.1f}" '
                 f'x2="{x_call + 6:.1f}" y2="{y:.1f}" '
                 f'stroke="{palette.MUTED}" stroke-width="1.4"/>')
    # The caption sits in the empty lower-left quadrant rather than beside
    # the bracket: next to it, it is painted over three curves. The axis tick
    # at 10 and the words "a mean of 10" do the linking instead of a leader
    # line, which would have to cross the floor to get there.
    y_note = PLOT["y1"] - 104
    o.append(text(sx(2.6), y_note,
                  "At a mean of 10 copies, a spread of CV 0.6",
                  size=13, colour=palette.MUTED))
    o.append(text(sx(2.6), y_note + 18,
                  f"raises the loss rate {round(ratio, -2):,.0f}×",
                  size=13, weight="bold"))
    counter = {k: segregation.loss_rate_from_division_counts(v)
               for k, v in COUNTEREXAMPLES}
    o.append(text(sx(2.6), y_note + 46,
                  "A and B: same mean (20) and same CV (0.10),",
                  size=13, colour=COUNTER_COLOUR))
    o.append(text(sx(2.6), y_note + 64,
                  f"{round(counter['B'] / counter['A'], -2):,.0f}× apart. "
                  f"Two moments are not enough.",
                  size=13, colour=COUNTER_COLOUR, weight="bold"))

    # --- the uniform reference line ---
    o.append(polyline(sample(lambda m: (m, floor(m))),
                      palette.INK, "none", width=2.8))
    y_end = sy(floor(X_MAX))
    o.append(text(PLOT["x1"] + 12, y_end + 4, "uniform copy number",
                  size=12, weight="bold"))
    o.append(text(PLOT["x1"] + 12, y_end + 21, "(the textbook line)",
                  size=11, colour=palette.MUTED))

    # --- one curve per spread ---
    # x is the CARRIER mean, not the nominal one. Read at the same mean,
    # Jensen's inequality forbids a spread curve from dipping below the
    # uniform line; plotted against the nominal mean these curves appear to
    # cross it below about 3 copies, which is an artefact of the x value and
    # not biology. segregation.carrier_mean carries the argument.
    for cv, dash in CVS:
        pts = sample(lambda m, c=cv: (segregation.carrier_mean(m, c),
                                      segregation.population_loss_rate(m, c)))
        o.append(polyline(pts, CURVE, dash))
        y_lab = sy(segregation.population_loss_rate(X_MAX, cv))
        o.append(text(PLOT["x1"] + 12, y_lab + 4, f"CV = {cv}", size=12,
                      colour=CURVE, weight="bold"))
        if cv == 1.0:
            o.append(text(PLOT["x1"] + 12, y_lab + 20, "measured range",
                          size=11, colour=palette.MUTED))

    # --- the two counterexample populations ---
    for label, dist in COUNTEREXAMPLES:
        y = sy(segregation.loss_rate_from_division_counts(dist))
        x = sx(COUNTER_BIRTH_MEAN)
        o.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" '
                 f'fill="{COUNTER_COLOUR}" stroke="{palette.PAPER}" '
                 f'stroke-width="1.5"/>')
        o.append(text(x - 11, y + 4, label, size=13,
                      colour=COUNTER_COLOUR, anchor="end", weight="bold"))

    # --- badge and assumptions ---
    o.append(f'  <rect x="48" y="{PLOT["y1"] + 68}" width="116" height="22" '
             f'rx="3" fill="{palette.INK}"/>')
    o.append(text(106, PLOT["y1"] + 83, "ANALYTIC", size=12,
                  colour=palette.PAPER, anchor="middle", weight="bold"))
    o.append(text(176, PLOT["y1"] + 83,
                  "No data and no fit: every value is computed from "
                  "models/copy-number-burden/battle_royale/segregation.py",
                  size=11, colour=palette.MUTED))
    o.append(text(48, PLOT["y1"] + 104,
                  "Assumes random segregation with no partition system, no "
                  "multimer resolution and no selection, and a lognormal "
                  "copy-number distribution across cells.", size=11,
                  colour=palette.MUTED))
    o.append(text(48, PLOT["y1"] + 120,
                  "The left tail of that distribution sets every value here, "
                  "so read the gaps as orders of magnitude rather than as "
                  "numbers.", size=11, colour=palette.MUTED))
    # A slide gets separated from its README, so the correction that matters
    # most travels on the figure itself: these curves bound nothing.
    o.append(text(48, PLOT["y1"] + 137,
                  "A reference point, not a bound: partition systems put a "
                  "plasmid below these curves, multimerisation and clustering "
                  "put one above.", size=11, weight="bold"))
    o.append(text(48, PLOT["y1"] + 153,
                  "Measured loss for ColE1-type vectors runs five to eight "
                  "orders of magnitude higher than their copy number predicts "
                  "(Summers & Sherratt 1984).", size=11,
                  colour=palette.MUTED))
    o.append(text(48, PLOT["y1"] + 172, "Sources: " + ", ".join(SOURCE_KEYS),
                  size=11, colour=palette.MUTED))

    o.append("</svg>")
    return "\n".join(o) + "\n"


def main():
    out = (Path(__file__).resolve().parents[1] / "output"
           / "copy-number-and-loss-rate.svg")
    # newline="\n" explicitly, so a rebuild on Windows matches one elsewhere.
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
