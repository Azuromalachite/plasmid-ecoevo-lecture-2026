#!/usr/bin/env python3
"""Settle whether the copy-number optimum is reachable, instead of asserting it.

Closes review finding F2, open since 17 October 2026. The lecture plan says
"always show [C_min, C_max] and ask whether C* exists inside it" and then never
asks. This script asks, and the answer is more interesting than either branch
of the question.

THE MODEL. Carriers after G0 generations with per-copy fractional growth cost
beta, and the isolated plasmid-molecule proxy:

    N(C)  proportional to  2 ** (G0 * (1 - beta * C))
    Q(C)  proportional to  C * N(C)

d(ln Q)/dC = 1/C - G0*beta*ln2 = 0 gives the interior stationary point

    C* = 1 / (beta * G0 * ln 2)

WHY THE EXISTENCE OF C* IS NOT A RESULT. For any positive beta and G0 this has
a stationary point, and it is always a maximum. A linear-in-C exponent times a
linear prefactor cannot do anything else. So "there is an optimal copy number"
is a property of the chosen functional form, not a finding about plasmids. The
only empirical content is WHERE C* sits relative to what a real vector can do,
which is what this script computes.

THE PARAMETER. beta is the fractional growth cost per plasmid copy. It is taken
from the authors' own interpretation of their fitted coefficient in
[@rouches2022tunable]: a = 0.065% +/- 0.006% of cellular growth resources per
copy, measured across 830 priming-promoter pUC19 variants with nearly identical
origins. `README.md` explains at length why the coefficient is only usable in
that reading -- the fitted `b` has no stated meaning, so no absolute per-copy
rate can be recovered. The scope conditions travel with it: one strain
background, pUC19-length plasmids, near-identical origins.

WHAT IS NOT TAKEN FROM THE COMPETITION. G0 and the feasible copy-number ranges
are swept, not assumed. The public rules do not state culture duration, and the
plan forbids inventing it, so this script reports the answer AS A FUNCTION of
G0 rather than picking one. The vector classes below are declared reference
ranges for common origin types, used the way the notebook uses its declared
competitor pool: to make a calculation concrete, never as a claim about what
anyone built.

Usage (from the repository root):
    uv run --no-project --with sympy python models/copy-number-burden/check_feasible_optimum.py

Exit status is 1 if a symbolic identity fails to reproduce.
"""

import math
import sys

try:
    import sympy as sp
except ImportError:
    sys.exit("needs sympy:  uv run --no-project --with sympy python "
             "models/copy-number-burden/check_feasible_optimum.py")

LN2 = math.log(2.0)

# The authors' interpretation of their own coefficient: fraction of cellular
# growth resources consumed per copy. Central value and stated uncertainty.
BETA = 6.5e-4
BETA_LO, BETA_HI = 5.9e-4, 7.1e-4

# Declared reference ranges for common origin classes. NOT Arena facts, and not
# a claim that any particular construct uses any of them. They exist so the
# question "is C* reachable?" has something concrete to be asked about.
VECTOR_CLASSES = [
    ("low-copy, p15A-like", 10, 15),
    ("medium, pBR322/pET-like", 20, 40),
    ("high-copy, pUC-like", 300, 500),
    ("tunable, wide range", 5, 500),
]

# Generation counts spanning a single batch to extended serial passage. Swept
# because the competition's culture duration is not public.
G0_VALUES = [5, 10, 15, 20, 30, 50, 100]


def c_star(beta, g0):
    return 1.0 / (beta * g0 * LN2)


def symbolic_checks():
    """Re-derive the three identities the lecture states, rather than trust them."""
    C, G0, beta = sp.symbols("C G_0 beta", positive=True)
    N = 2 ** (G0 * (1 - beta * C))
    Q = C * N

    solutions = sp.solve(sp.diff(sp.log(Q), C), C)
    derived = sp.simplify(solutions[0])
    expected = 1 / (beta * G0 * sp.log(2))
    ok_star = sp.simplify(derived - expected) == 0

    # It is a maximum, not just a stationary point.
    second = sp.diff(sp.log(Q), C, 2).subs(C, expected)
    ok_max = sp.simplify(second) < 0

    # The parameter-free invariant, which holds only at the unconstrained C*.
    invariant = sp.simplify((2 ** (-G0 * beta * expected)) - sp.exp(-1))
    ok_inv = invariant == 0

    return derived, ok_star, bool(ok_max), ok_inv


def verdict(cs, lo, hi):
    if cs < lo:
        return "PUSH DOWN", "floor optimal for both objectives"
    if cs > hi:
        return "PUSH UP  ", "ceiling optimal for both objectives"
    return "INTERIOR ", "a real trade-off exists"


def main():
    derived, ok_star, ok_max, ok_inv = symbolic_checks()
    print("SYMBOLIC")
    print(f"  C* derived            : {derived}")
    print(f"  matches 1/(beta G0 ln2): {ok_star}")
    print(f"  second derivative < 0  : {ok_max}  (a maximum, for ALL beta, G0)")
    print(f"  2^(-G0 beta C*) = 1/e  : {ok_inv}")
    if not (ok_star and ok_max and ok_inv):
        print("\nPROBLEM: a stated identity did not reproduce.")
        return 1

    print(f"\nPARAMETER\n  beta = {BETA:.1e} per copy "
          f"(range {BETA_LO:.1e} to {BETA_HI:.1e}), from the authors' reading")
    print(f"  1/beta = {1/BETA:.0f} copies is where the model predicts zero")
    print("  growth; it is outside any range below, so the form is not being")
    print("  evaluated where it breaks.")

    print("\nC* AS A FUNCTION OF GENERATIONS (culture duration is not public)")
    print(f"  {'G0':>5}  {'C* (copies/cell)':>18}   {'C* range over beta':>24}")
    for g0 in G0_VALUES:
        print(f"  {g0:>5}  {c_star(BETA, g0):>18.0f}   "
              f"{c_star(BETA_HI, g0):>10.0f} to {c_star(BETA_LO, g0):<10.0f}")

    print("\nIS C* REACHABLE? verdict per declared vector class")
    print(f"  {'G0':>4}  " + "  ".join(f"{name:<24}" for name, _, _ in VECTOR_CLASSES))
    interior = 0
    total = 0
    for g0 in G0_VALUES:
        cs = c_star(BETA, g0)
        cells = []
        for _, lo, hi in VECTOR_CLASSES:
            tag, _ = verdict(cs, lo, hi)
            total += 1
            if tag.strip() == "INTERIOR":
                interior += 1
            cells.append(f"{tag:<24}")
        print(f"  {g0:>4}  " + "  ".join(cells))

    print(f"\n  interior optima: {interior} of {total} grid cells")
    print("  GRID COUNT, NOT A FREQUENCY. The four ranges and seven generation")
    print("  counts are analyst-chosen probes of parameter space, not a sample")
    print("  from any population of plasmids. This is not 'a third of cases'")
    print("  and must never be quoted as a percentage of anything biological.")

    print("\nTHE BOUNDARY, SOLVED RATHER THAN SWEPT")
    print("  C* <= C_min  <=>  G0 >= 1/(beta * C_min * ln2)")
    print("  C* >= C_max  <=>  G0 <= 1/(beta * C_max * ln2)")
    print(f"  {'vector class':<26} {'G0 below which':>15} {'G0 above which':>15}")
    print(f"  {'':<26} {'ceiling wins':>15} {'floor wins':>15}")
    for name, lo, hi in VECTOR_CLASSES:
        print(f"  {name:<26} {1/(BETA*hi*LN2):>15.1f} {1/(BETA*lo*LN2):>15.1f}")

    print("\nDENSITY PENALTY AT C*, against the lowest feasible copy number")
    print("  N(C*)/N(C_min) = 2^(-G0 beta (C* - C_min)); only defined where")
    print("  C* > C_min, i.e. where a trade-off exists at all.")
    for name, lo, hi in VECTOR_CLASSES:
        rows = []
        for g0 in G0_VALUES:
            cs = c_star(BETA, g0)
            if lo < cs < hi:
                rows.append(f"G0={g0}: {100*(1-2**(-g0*BETA*(cs-lo))):.0f}%")
        print(f"  {name:<26} {', '.join(rows) if rows else 'no interior optimum at any swept G0'}")

    print("\nVERDICT")
    print("  The trade-off is not a property of a plasmid. It is a property of")
    print("  how long the culture runs, and for most origin classes at most")
    print("  generation counts it does not exist: the optimum sits outside the")
    print("  reachable range and both objectives agree on the same boundary.")
    print("  Crucially they do not agree on WHICH boundary -- a medium-copy")
    print("  vector is told to go up and a high-copy vector to come down, by")
    print("  the same model with the same parameter.")
    print("\n  Not checked here: that burden is linear in copy number (the")
    print("  source hedges it), that the coefficient transfers off pUC19-length")
    print("  plasmids and near-identical origins, or that retention is")
    print("  independent of copy number. Each would move C*.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
