#!/usr/bin/env python3
"""Why gene location can be an accident: redundancy, not local adaptation.

Supports the lecture's regulation-versus-mobility slide, which currently
asserts its distinction rather than deriving it. This script derives the one
threshold the argument needs and checks the control that makes it meaningful.

WHAT THIS IS NOT. It is not a reproduction of the model in
[@lehtinen2021location]. It is the smallest system that reproduces **one
mechanism they state**, so that the mechanism can be checked rather than
quoted. Their full treatment has four genotypes with explicit transfer, loss,
mutation and antibiotic exposure, analysed by simulation as well as algebra.
Anything here that goes beyond the single mechanism below is not theirs.

THE MECHANISM, in their words: gene location is under *positive*
frequency-dependent selection, and this "arises because dually resistant cells
are less fit than cells with either form of single resistance: dual resistance
incurs an additional fitness cost but provides no additional fitness benefit."
They add that this is "the only crucial assumption" for the result.

THE REDUCTION. Four states -- sensitive, chromosomal, plasmid-borne, dual --
but the invasion question only needs the two resistant forms and the rate at
which each is converted into the wasteful dual state:

    w_C = b - c_c - delta * x_P     a chromosomal cell meets a resistant plasmid
    w_P = b - c_p - delta * x_C     a plasmid-bearing cell meets a chromosomal one

b is the benefit of resistance, identical for both locations and for the dual
state: that identity IS the assumption. c_c and c_p are the carriage costs of
each location. delta is the extra cost of carrying both and gaining nothing.

WHY THE BENEFIT CANCELS, AND WHY THAT IS THE POINT. b does not appear in
w_C - w_P. Under this mechanism, **how useful the gene is cannot explain where
it sits.** That is the formal version of the lecture's refusal of the weak
answer -- a chromosome can also stockpile and regulate a conditionally useful
gene, so usefulness alone predicts nothing about location.

THE CONTROL. Setting delta = 0 makes dual carriage exactly as good as single
carriage. The frequency dependence must then vanish and the cheaper location
must win outright. A model that still produced a priority effect at delta = 0
would be producing it from its own structure, not from the mechanism. That
check runs first and the script fails if it does not hold.

Usage (from the repository root):
    uv run --no-project --with sympy python models/gene-location/check_priority_effect.py

Exit status is 1 if a derivation does not reproduce.
"""

import sys

try:
    import sympy as sp
except ImportError:
    sys.exit("needs sympy:  uv run --no-project --with sympy python "
             "models/gene-location/check_priority_effect.py")


def fitness(b, c_c, c_p, delta, R, x_C):
    """(w_C, w_P) for the redundancy-only model, built from first principles.

    Module level and side-effect free so that `check_regime_boundary.py` can
    IMPORT it rather than transcribe the difference into a literal (OF-14). A
    comment saying "from check_priority_effect" is not a binding: it keeps
    passing after this file changes. The import is.
    """
    x_P = R - x_C
    w_C = b - c_c - delta * x_P
    w_P = b - c_p - delta * x_C
    return w_C, w_P


def advantage_expr(b, c_c, c_p, delta, R, x_C):
    """w_P - w_C for this model. The sign convention matches the sibling:
    positive means plasmid localisation is favoured."""
    w_C, w_P = fitness(b, c_c, c_p, delta, R, x_C)
    return sp.expand(w_P - w_C)


def main():
    b, c_c, c_p, delta, R = sp.symbols("b c_c c_p delta R", positive=True)
    x_C = sp.Symbol("x_C", nonnegative=True)

    # The two resistant forms partition the resistant fraction R.
    w_C, w_P = fitness(b, c_c, c_p, delta, R, x_C)
    x_P = R - x_C
    diff = sp.simplify(w_C - w_P)

    print("THE REDUCTION")
    print(f"  w_C - w_P = {diff}")

    # 1. The benefit cancels.
    benefit_cancels = sp.simplify(sp.diff(diff, b)) == 0
    print(f"\n1. benefit b cancels                     : {benefit_cancels}")
    print("   How useful the gene is does not predict where it sits.")

    # 2. Positive frequency dependence: the commoner form gains.
    slope = sp.simplify(sp.diff(diff, x_C))
    positive_fd = sp.simplify(slope - 2 * delta) == 0
    print(f"\n2. d(w_C - w_P)/dx_C = {slope}")
    print(f"   positive for delta > 0                 : {positive_fd}")
    print("   The commoner location gains relative fitness as it becomes")
    print("   commoner. That is the published direction, and the reason is")
    print("   that transfer into an already-resistant cell is wasted.")

    # 3. THE CONTROL. delta = 0 must remove the frequency dependence entirely.
    diff0 = sp.simplify(diff.subs(delta, 0))
    control_flat = sp.simplify(sp.diff(diff0, x_C)) == 0
    control_cost_only = sp.simplify(diff0 - (c_p - c_c)) == 0
    print(f"\n3. CONTROL, delta = 0")
    print(f"   w_C - w_P = {diff0}")
    print(f"   no dependence on frequency             : {control_flat}")
    print(f"   reduces to the cost difference alone   : {control_cost_only}")
    print("   With no redundancy penalty the cheaper location simply wins and")
    print("   there is no priority effect. The mechanism is doing the work,")
    print("   not the algebra.")

    if not (benefit_cancels and positive_fd and control_flat and control_cost_only):
        print("\nPROBLEM: a derivation did not reproduce.")
        return 1

    # 4. The interior threshold, and when it exists.
    threshold = sp.solve(sp.Eq(diff, 0), x_C)[0]
    threshold = sp.simplify(threshold)
    print(f"\n4. INTERIOR THRESHOLD")
    print(f"   w_C = w_P at x_C = {threshold}")
    print(f"   expanded           = {sp.simplify(sp.expand(threshold))}")
    print("   Above it the chromosomal form wins, below it the plasmid form")
    print("   does, and the point itself is unstable -- so both pure states")
    print("   are locally stable. That is the priority effect: whichever form")
    print("   arrives first is hard to displace.")

    # 5. The condition for the threshold to lie inside [0, R] -- i.e. for a
    #    priority effect to exist at all rather than one location winning.
    print(f"\n5. WHEN DOES A PRIORITY EFFECT EXIST?")
    print("   The threshold must lie strictly inside (0, R).")
    lo = sp.simplify(threshold > 0)
    hi = sp.simplify(threshold < R)
    print(f"   x_C* > 0  <=>  {lo}")
    print(f"   x_C* < R  <=>  {hi}")
    print("\n   Together, writing the cost gap as |c_c - c_p|:")
    print("       |c_c - c_p|  <  delta * R")
    print("\n   A priority effect exists only when the two locations differ in")
    print("   cost by LESS than the redundancy penalty across the resistant")
    print("   fraction. If one location is clearly cheaper than carrying both")
    print("   is wasteful, that location simply wins and history does not")
    print("   matter. History matters precisely when the locations are close.")

    # 6. Numeric illustration of the bistability, as a sanity check on signs.
    print(f"\n6. NUMERIC CHECK (b=0.10, c_c=0.010, c_p=0.015, delta=0.040, R=0.5)")
    subs = {b: 0.10, c_c: 0.010, c_p: 0.015, delta: 0.040, R: 0.5}
    t = float(threshold.subs(subs))
    print(f"   cost gap |c_c - c_p| = 0.005   delta*R = {0.040*0.5}")
    print(f"   priority effect expected       : {abs(0.010-0.015) < 0.040*0.5}")
    print(f"   threshold x_C*                 : {t:.4f}  (inside 0 to 0.5)")
    for probe in (0.10, 0.25, 0.40):
        d = float(diff.subs(subs).subs(x_C, probe))
        winner = "chromosome" if d > 0 else "plasmid"
        print(f"     x_C = {probe:.2f} -> w_C - w_P = {d:+.5f}  ->  {winner} gains")
    print("   Both ends run away from the threshold: bistable, as stated.")

    print("\n  WHAT THIS DOES NOT SHOW. Not that real gene location is set this")
    print("  way; not the published model's full dynamics; not anything about")
    print("  rates, since transfer and loss are folded into delta and the")
    print("  costs. It shows that one stated mechanism yields the published")
    print("  direction of frequency dependence and a priority effect, and")
    print("  that both disappear when the mechanism is switched off.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
