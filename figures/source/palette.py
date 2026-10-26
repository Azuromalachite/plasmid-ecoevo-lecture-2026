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
# Claims about this pool are relative to it; on all eight colours the picture
# differs, which is why the pool is named rather than assumed.
#
# NO NUMBERS IN THESE COMMENTS. Every quantity that used to be written here
# is now derived by measure() and printed by report_measurements(). A comment
# holding a second hand-maintained copy of a measurement is how this file
# came to assert two things that were false; run the module to see the
# current figures.
POOL = ("orange", "sky_blue", "bluish_green", "blue", "vermillion", "purple")

# --- Role assignments ----------------------------------------------------
# The three routes by which a plasmid lineage gains or loses copies.
# These keep the same colours in every figure, so a reader learns them once.
#
# COPY and SPREAD are both blues, which is a deliberate trade. Within POOL
# this assignment is among the best-separating options under BOTH simulated
# dichromacies, but it is NOT the only workable one — several alternatives
# also clear MIN_DISTANCE, so reassigning is possible if a later figure needs
# it. The two blues also differ in luminance, so they separate in greyscale,
# and ROUTE_DASH and ROUTE_MARK carry the distinction regardless of colour.
# For how many alternatives there are and how they score, run the module.
ROUTES = {
    "COPY":   OKABE_ITO["sky_blue"],
    "CARRY":  OKABE_ITO["orange"],
    "SPREAD": OKABE_ITO["blue"],
}

# Narrative stages, environmental through clinical.
#
# `environmental` reuses sky_blue, which ROUTES gives to COPY. Within POOL
# that reuse is forced: holding ROUTES fixed leaves exactly one candidate
# triple and it fails. Admitting black or yellow WOULD give disjoint triples
# that pass, so the constraint comes from the pool, not from Okabe-Ito. If
# the black/yellow exclusions above are ever relaxed, revisit this
# assignment; it is not a fact about the palette. report_measurements()
# prints both figures.
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

# A project convention, not a standard: a Euclidean distance in sRGB after
# simulation, chosen because it separated the cases we had. No external
# source defines it, and sRGB distance is not perceptually uniform, so it
# under-penalises some pairs and over-penalises others. Treat scores just
# above and just below it as the same answer: "close to the line, look".
MIN_DISTANCE = 60.0


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
    """Every pair within a palette group stays separable. Returns a problem list.

    What this DETECTS: two colours in the same group that collapse toward each
    other under a standard simulation of dichromacy, judged by a threshold we
    chose.

    What it CANNOT detect, and what therefore still needs a human:
      * whether colour is the only thing encoding a distinction. Rule 2 above
        is the stronger rule and nothing here enforces it -- a figure can pass
        this check and still be unreadable in greyscale;
      * anomalous trichromacy (mild red-green deficiency), which is far more
        common than the dichromacies simulated here, and monochromacy, which
        is not simulated at all;
      * whether the colours are legible against the background they are drawn
        on, or at the size and stroke width actually used;
      * whether a passing score means the pair looks different to a reader.
        sRGB distance is not perceptual, so it is a screen, not a verdict.
    """
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
    a property of Okabe-Ito rather than of our pool: no six-colour subset of
    the full palette clears MIN_DISTANCE, so six simultaneously separable
    categories are out of reach however they are assigned.
    report_measurements() prints the best achievable score, and
    verify_design_invariants() fails if that ever stops being true. Call this before mixing the vocabularies, and treat a failure
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


def _worst(names):
    """Lowest pairwise separation within a colour set, across all simulations."""
    cols = [OKABE_ITO[n] for n in names]
    w = float("inf")
    for vision in ("normal", "deuteranopia", "protanopia"):
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                a, b = cols[i], cols[j]
                if vision != "normal":
                    a, b = simulate(a, vision), simulate(b, vision)
                w = min(w, distance(a, b))
    return w


def _relative_luminance(hex_colour):
    r, g, b = (_srgb_to_lin(v) for v in _hex2rgb(hex_colour))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def measure():
    """Derive every quantity this module's design rests on. Single source.

    Nothing here is hard-coded from a previous run, and no comment above
    repeats these numbers. Earlier versions kept the figures in three places
    at once -- a comment, a literal in the checker, and the real measurement
    -- and two of the comment copies were false while the checker passed.
    """
    import itertools

    route_names = tuple(k for k in POOL if OKABE_ITO[k] in ROUTES.values())
    stage_names = tuple(k for k in OKABE_ITO if OKABE_ITO[k] in STAGES.values())
    pool_triples = [(c, _worst(c)) for c in itertools.combinations(POOL, 3)]
    passing = sorted([x for x in pool_triples if x[1] >= MIN_DISTANCE],
                     key=lambda x: -x[1])
    disjoint_pool = [(c, _worst(c)) for c in itertools.combinations(
        [n for n in POOL if n not in route_names], 3)]
    disjoint_full = sorted([(c, _worst(c)) for c in itertools.combinations(
        [n for n in OKABE_ITO if n not in route_names], 3)
        if _worst(c) >= MIN_DISTANCE], key=lambda x: -x[1])
    best_six = max((_worst(c) for c in itertools.combinations(OKABE_ITO, 6)))
    lum = sorted(_relative_luminance(v) for v in
                 (ROUTES["COPY"], ROUTES["SPREAD"]))
    return {
        "pool_triples_total": len(pool_triples),
        "pool_triples_passing": passing,
        "routes_names": route_names,
        "routes_score": _worst(route_names),
        "stages_score": _worst(stage_names),
        "disjoint_within_pool": disjoint_pool,
        "disjoint_with_black_yellow": disjoint_full,
        "best_six_colour_set": best_six,
        "copy_spread_luminance_ratio": (lum[1] + 0.05) / (lum[0] + 0.05),
    }


def report_measurements(m=None):
    """Print the derived figures. These are the numbers; comments defer here."""
    m = m or measure()
    passing = m["pool_triples_passing"]
    print(f"POOL = {', '.join(POOL)}")
    print(f"  triples clearing MIN_DISTANCE: {len(passing)} of "
          f"{m['pool_triples_total']}")
    for c, s in passing:
        mark = "  <-- ROUTES" if set(c) == set(m["routes_names"]) else ""
        print(f"    {s:7.2f}  {', '.join(c)}{mark}")
    print(f"  ROUTES score {m['routes_score']:.2f}; "
          f"STAGES score {m['stages_score']:.2f}")
    print(f"  COPY/SPREAD luminance ratio: "
          f"{m['copy_spread_luminance_ratio']:.2f}:1")
    print(f"  disjoint STAGES options within POOL: "
          f"{len(m['disjoint_within_pool'])} candidate(s), "
          f"best {max(s for _, s in m['disjoint_within_pool']):.2f} "
          f"-- none clear {MIN_DISTANCE}")
    dj = m["disjoint_with_black_yellow"]
    print(f"  disjoint STAGES options if black/yellow are admitted: {len(dj)}"
          + (f", best {dj[0][1]:.2f} ({', '.join(dj[0][0])})" if dj else ""))
    print(f"  best six-colour set over all eight: "
          f"{m['best_six_colour_set']:.2f}")


def verify_design_invariants(verbose=True):
    """Assert only the properties the design actually depends on.

    Deliberately NOT a comparison against expected numbers. Counts and scores
    drift for legitimate reasons; what must stay true is structural.

    What this DETECTS: a ROUTES or STAGES assignment that stops being
    separable, and a union that silently becomes separable (which would mean
    the never-mix rule could be dropped).

    What it CANNOT detect: a false statement written in a comment. No check
    in Python validates prose. The defence is that the comments no longer
    carry numbers -- they point here instead -- so there is nothing in them
    left to drift out of date.
    """
    m = measure()
    problems = []
    if m["routes_score"] < MIN_DISTANCE:
        problems.append(f"ROUTES no longer separable: {m['routes_score']:.2f}")
    if m["stages_score"] < MIN_DISTANCE:
        problems.append(f"STAGES no longer separable: {m['stages_score']:.2f}")
    if not any(set(c) == set(m["routes_names"])
               for c, _ in m["pool_triples_passing"]):
        problems.append("ROUTES is not among the passing triples of POOL")
    if m["best_six_colour_set"] >= MIN_DISTANCE:
        problems.append(
            f"six categories are now separable ({m['best_six_colour_set']:.2f}); "
            "the never-mix rule and check_union() need revisiting")
    if verbose:
        print(f"design invariants: {len(problems)} violation(s)")
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
    report_measurements()
    print()
    if verify_design_invariants():
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
