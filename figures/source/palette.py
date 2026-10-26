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

# --- The working pool ----------------------------------------------------
# Categorical roles below are drawn from SIX of the eight Okabe-Ito colours.
# Excluded, and this exclusion is a design choice rather than a measurement:
#   black  (#000000) is visually indistinguishable from INK, the body-text
#          colour, so a category in black reads as a label, not a series;
#   yellow (#F0E442) has too little contrast on the white figure background
#          to carry a line, a small mark or text.
# Every count below is relative to that six-colour pool. On all eight colours
# the numbers are different and better, which is why the pool has to be
# stated rather than assumed.
POOL = ("orange", "sky_blue", "bluish_green", "blue", "vermillion", "purple")

# --- Role assignments ----------------------------------------------------
# The three routes by which a plasmid lineage gains or loses copies.
# These keep the same colours in every figure, so a reader learns them once.
#
# COPY and SPREAD are both blues, which is a deliberate trade. Measured over
# the pool above: 6 of the 20 possible triples clear MIN_DISTANCE under BOTH
# simulated deuteranopia and protanopia. This one scores 103.40, tied for
# best with (sky_blue, blue, vermillion); the rest score 100.50, 100.50,
# 86.01 and 75.26. So it is a joint-best choice, NOT the only workable one —
# reassigning is possible if a later figure needs it, at a documented cost.
# The two blues differ in relative luminance by 2.25:1, so they also separate
# in greyscale, and ROUTE_DASH and ROUTE_MARK carry the distinction anyway.
ROUTES = {
    "COPY":   OKABE_ITO["sky_blue"],
    "CARRY":  OKABE_ITO["orange"],
    "SPREAD": OKABE_ITO["blue"],
}

# Narrative stages, environmental through clinical.
#
# `environmental` reuses sky_blue, which ROUTES gives to COPY. Within the
# six-colour pool that reuse is forced: holding ROUTES fixed leaves only
# (bluish_green, vermillion, purple), which scores 56.71 and fails. Admitting
# black or yellow WOULD give disjoint triples that pass — the best is
# (black, bluish_green, vermillion) at 124.65 — so the constraint comes from
# the pool, not from Okabe-Ito. If the black/yellow exclusions above are ever
# relaxed, revisit this assignment; it is not a fact about the palette.
#
# Since a figure uses one vocabulary or the other, separability WITHIN a
# group is the operative constraint. A figure needing both must call
# check_union(), which fails.
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

    Expected to fail. Unlike the single-group constraints, this one really is
    a property of Okabe-Ito rather than of our pool: over all eight colours
    the best six-colour set scores 56.71, below MIN_DISTANCE, so six
    simultaneously separable categories are out of reach however they are
    assigned. Call this before mixing the vocabularies, and treat a failure
    as a sign to split the figure or use fewer categories, never to lower
    MIN_DISTANCE.
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


def verify_documented_claims(verbose=True):
    """Re-derive every count stated in the comments above.

    These numbers were wrong once: an earlier version claimed the ROUTES
    triple was "the only one" that passed and that no disjoint STAGES triple
    existed. Both were false, and both were stated over an unstated colour
    pool. A comment cannot be trusted to stay true, so it is checked here.
    """
    import itertools

    def worst(names):
        cols = [OKABE_ITO[n] for n in names]
        w = float("inf")
        for vision in ("normal", "deuteranopia", "protanopia"):
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    x, y = cols[i], cols[j]
                    if vision != "normal":
                        x, y = simulate(x, vision), simulate(y, vision)
                    w = min(w, distance(x, y))
        return w

    problems = []
    passing = [c for c in itertools.combinations(POOL, 3) if worst(c) >= MIN_DISTANCE]
    if len(passing) != 6:
        problems.append(f"comment says 6 of 20 pool triples pass; measured {len(passing)}")
    routes = tuple(k for k in POOL if OKABE_ITO[k] in ROUTES.values())
    top = max(worst(c) for c in passing)
    if abs(worst(routes) - 103.40) > 0.01 or abs(top - 103.40) > 0.01:
        problems.append(f"comment says ROUTES ties for best at 103.40; measured "
                        f"{worst(routes):.2f}, best {top:.2f}")
    rest = tuple(n for n in POOL if n not in routes)
    if worst(rest) >= MIN_DISTANCE:
        problems.append(f"comment says the disjoint pool option fails at 56.71; "
                        f"measured {worst(rest):.2f}, which passes")
    best6 = max(worst(c) for c in itertools.combinations(OKABE_ITO, 6))
    if best6 >= MIN_DISTANCE:
        problems.append(f"comment says six categories are unreachable; best "
                        f"six-colour set scores {best6:.2f}")
    if verbose:
        print(f"documented-claim check: {len(problems)} stale claim(s)")
        for q in problems:
            print(f"    {q}")
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
    print()
    if verify_documented_claims():
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
