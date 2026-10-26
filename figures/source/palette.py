#!/usr/bin/env python3
"""Shared figure palette and accessibility self-test.

Every v0.2 figure imports its colours from here. The v0.1 pathway figure
predates this module and is deliberately not being reissued; it keeps its
original colours, whose defect is recorded in figures/README.md.

Two rules, and the second is the one that actually protects a reader:

1. Colours must stay distinguishable under simulated deuteranopia and
   protanopia. `check()` enforces this, and it fails loudly.
2. **Colour never carries meaning alone.** Every encoded distinction is also
   carried by a label, a shape, a line style or a position. Rule 1 reduces the
   damage when colour fails; rule 2 is what makes a figure survive greyscale
   printing, a bad projector and a reader who never sees colour at all.

The base colours are the Okabe-Ito qualitative palette, which was designed for
colour-vision deficiency. The choice of which Okabe-Ito colour plays which
role is ours, and is what `check()` verifies.

Run the self-test:
    python figures/source/palette.py
"""

import sys

# --- Okabe & Ito qualitative palette -------------------------------------
OKABE_ITO = {
    "black":        "#000000",
    "orange":       "#E69F00",
    "sky_blue":     "#56B4E9",
    "bluish_green": "#009E73",
    "yellow":       "#F0E442",
    "blue":         "#0072B2",
    "vermillion":   "#D55E00",
    "purple":       "#CC79A7",
}

# --- Role assignments ----------------------------------------------------
# The three routes by which a plasmid lineage gains or loses copies.
# These keep the same colours in every figure, so a reader learns them once.
# COPY and SPREAD are both blues. That is a measured trade, not an oversight:
# of every assignment of Okabe-Ito colours to these three roles, this is the
# only one whose worst-case separation stays above MIN_DISTANCE under BOTH
# simulated deuteranopia and protanopia (103.4; the runners-up fail at 38-55).
# The two blues differ in relative luminance by 2.25:1, so they also separate
# in greyscale, and ROUTE_DASH and ROUTE_MARK carry the distinction anyway.
ROUTES = {
    "COPY":   OKABE_ITO["sky_blue"],
    "CARRY":  OKABE_ITO["orange"],
    "SPREAD": OKABE_ITO["blue"],
}

# Narrative stages, environmental through clinical.
#
# `environmental` deliberately reuses sky_blue, which ROUTES gives to COPY.
# Six Okabe-Ito colours cannot supply two fully disjoint separable triples:
# the best disjoint pair tops out at 56.7, below MIN_DISTANCE. Since a figure
# uses one vocabulary or the other, separability WITHIN a group is the real
# constraint. A figure that needs both must call check_union(), which fails.
STAGES = {
    "environmental": OKABE_ITO["sky_blue"],
    "mobile":        OKABE_ITO["purple"],
    "clinical":      OKABE_ITO["vermillion"],
}

# Non-categorical roles.
INK = "#1b1f23"
MUTED = "#5a6570"
RULE = "#d8d8d8"
PAPER = "#ffffff"      # explicit background: dark text on transparent is
                       # invisible against a dark viewer background.

# Redundant encodings to pair with colour (rule 2).
ROUTE_DASH = {"COPY": "none", "CARRY": "6 3", "SPREAD": "2 3"}
ROUTE_MARK = {"COPY": "circle", "CARRY": "square", "SPREAD": "triangle"}

MIN_DISTANCE = 60.0    # RGB distance under simulation; below this, two
                       # colours are not reliably separable.


# --- colour-vision simulation -------------------------------------------
_M = {
    "deuteranopia": [[0.625, 0.375, 0.0], [0.70, 0.30, 0.0], [0.0, 0.30, 0.70]],
    "protanopia":   [[0.1115, 0.8885, 0.0], [0.1115, 0.8885, 0.0], [0.0, 0.0, 1.0]],
}


def _hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _srgb_to_lin(v):
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def _lin_to_srgb(v):
    v = max(0.0, min(1.0, v))
    return round(255 * (12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055))


def simulate(hex_colour, kind):
    """Approximate how a colour appears under dichromacy (Vienot et al.)."""
    r, g, b = (_srgb_to_lin(v) for v in _hex2rgb(hex_colour))
    m = _M[kind]
    return "#%02x%02x%02x" % tuple(
        _lin_to_srgb(m[i][0] * r + m[i][1] * g + m[i][2] * b) for i in range(3))


def distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(_hex2rgb(a), _hex2rgb(b))) ** 0.5


def check(verbose=True):
    """Every pair within a palette group stays separable. Returns a problem list."""
    problems = []
    for name, group in (("ROUTES", ROUTES), ("STAGES", STAGES)):
        keys = list(group)
        for vision in ("normal", "deuteranopia", "protanopia"):
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    a, b = group[keys[i]], group[keys[j]]
                    if vision != "normal":
                        a, b = simulate(a, vision), simulate(b, vision)
                    d = distance(a, b)
                    ok = d >= MIN_DISTANCE
                    if verbose:
                        print(f"  {name:7s} {vision:13s} {keys[i]:>13s} vs "
                              f"{keys[j]:<13s} {d:6.1f}  {'ok' if ok else 'TOO CLOSE'}")
                    if not ok:
                        problems.append(
                            f"{name}: {keys[i]} vs {keys[j]} under {vision} "
                            f"(distance {d:.1f} < {MIN_DISTANCE})")
    return problems


def check_union(verbose=True):
    """Separability when ROUTES and STAGES appear in ONE figure.

    Expected to fail: the two groups share a colour and the palette cannot
    support six simultaneously separable categories. Call it before mixing
    the vocabularies, and treat a failure as a sign to split the figure or
    drop to fewer categories rather than to lower MIN_DISTANCE.
    """
    merged = {f"ROUTE:{k}": v for k, v in ROUTES.items()}
    merged.update({f"STAGE:{k}": v for k, v in STAGES.items()})
    problems, keys = [], list(merged)
    for vision in ("normal", "deuteranopia", "protanopia"):
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = merged[keys[i]], merged[keys[j]]
                if vision != "normal":
                    a, b = simulate(a, vision), simulate(b, vision)
                d = distance(a, b)
                if d < MIN_DISTANCE:
                    problems.append(f"{keys[i]} vs {keys[j]} under {vision}: {d:.1f}")
    if verbose:
        print(f"union check: {len(problems)} unseparable pair(s)")
        for p in problems:
            print(f"    {p}")
    return problems


def main():
    print("Palette accessibility self-test")
    print(f"minimum acceptable RGB distance: {MIN_DISTANCE}\n")
    problems = check()
    if problems:
        print("\nFAILED:")
        for p in problems:
            print(f"  {p}")
        return 1
    print("\nall pairs separable under normal, deuteranopic and protanopic vision")
    print("\nReminder: colour must never be the only encoding. Pair it with "
          "ROUTE_DASH, ROUTE_MARK, a label or position.")
    print("\nFor reference, the two vocabularies cannot be mixed in one figure:")
    check_union()
    return 0


if __name__ == "__main__":
    sys.exit(main())
