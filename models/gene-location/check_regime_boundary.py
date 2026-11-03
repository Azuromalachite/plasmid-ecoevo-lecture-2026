#!/usr/bin/env python3
r"""Both gene-location regimes from one model, and the boundary between them.

[`check_priority_effect.py`](check_priority_effect.py) reproduced the
redundancy mechanism of [@lehtinen2021location]. It did not represent the
position that paper argues against, so it could state the disagreement in
prose but not locate it. This script makes the disagreement the specification:
one model, two regimes, and the parameter that separates them.

THE TWO POSITIONS, as the later paper characterises the earlier one.

[@eberhard1989genes], local adaptation: a gene useful only in a local niche
does better on a plasmid, because the plasmid carries it horizontally into
immigrant lineages that lack it. [@lehtinen2021location] states the assumption
this rests on -- "outside the local niche with the beneficial gene, plasmids
would not persist" -- and then removes it.

Removing it reverses the argument. If the gene-free ("sensitive") version of
the same plasmid already persists outside the niche, immigrants mostly arrive
carrying the backbone already. The resistant plasmid then has few plasmid-free
recipients to colonise, and the cells it does enter become dual carriers, which
pay for two copies of a function they need once. The verified finding: "Plasmid
-borne resistance benefits from the sensitive plasmid being rare."

THE PARAMETER THAT SEPARATES THEM is therefore q, the frequency of the
gene-free plasmid among potential recipients. It is a property of the ecology
outside the niche, not of the plasmid or the gene.

    w_P - w_C = gamma*(1 - q) - (c_p - c_c) - delta*(x_C - x_P)
                \__________/   \___________/  \_________________/
                 mobility        carriage       redundancy
                 is rented       cost gap       (the priority effect)

gamma is the transfer rate into plasmid-free recipients, delta the extra cost
of dual carriage for no extra benefit, c_c and c_p the carriage costs, and
x_C + x_P = R the resistant fraction.

The mobility term is the whole of Eberhard's advantage, and it is multiplied by
the fraction of recipients that are still plasmid-free. **Mobility is rented
from the ecology, not owned by the plasmid.**

Usage (from the repository root):
    uv run --no-project --with sympy python models/gene-location/check_regime_boundary.py

Exit status is 1 if a derivation or a control does not reproduce.
"""

import sys

try:
    import sympy as sp
except ImportError:
    sys.exit("needs sympy:  uv run --no-project --with sympy python "
             "models/gene-location/check_regime_boundary.py")


def main():
    c_c, c_p, delta, R, gamma = sp.symbols("c_c c_p delta R gamma", positive=True)
    q = sp.Symbol("q", nonnegative=True)
    x_C = sp.Symbol("x_C", nonnegative=True)
    x_P = R - x_C

    advantage = gamma * (1 - q) - (c_p - c_c) - delta * (x_C - x_P)
    advantage = sp.expand(advantage)

    print("THE COMBINED MODEL")
    print(f"  w_P - w_C = {advantage}")
    print("  positive means plasmid localisation is favoured.")

    ok = []

    # 1. NESTING. At q = 1 the mobility term vanishes and the model must reduce
    #    exactly to the redundancy-only expression already committed.
    prior = -((c_p - c_c) + delta * (2 * x_C - R))      # from check_priority_effect
    nests = sp.simplify(advantage.subs(q, 1) - prior) == 0
    ok.append(nests)
    print(f"\n1. NESTING at q = 1 (gene-free plasmid everywhere)")
    print(f"   reduces to the committed redundancy model : {nests}")
    print("   So the earlier script is this one's q -> 1 limit, not a rival to")
    print("   it. The Lehtinen regime is the saturated-recipient corner.")

    # 2. The Eberhard regime is the opposite corner.
    eberhard = sp.simplify(advantage.subs(q, 0))
    print(f"\n2. EBERHARD CORNER at q = 0 (no gene-free plasmid outside)")
    print(f"   w_P - w_C = {eberhard}")
    print("   The full transfer rate is available, so local adaptation plus")
    print("   mobility can favour the plasmid -- the original argument, intact")
    print("   inside its own assumption.")

    # 3. The boundary, solved in q.
    q_star = sp.simplify(sp.solve(sp.Eq(advantage, 0), q)[0])
    print(f"\n3. THE BOUNDARY")
    print(f"   q* = {q_star}")
    print("   Plasmid localisation is favoured for q < q*, chromosomal for")
    print("   q > q*. At the symmetric point x_C = R/2:")
    q_sym = sp.simplify(q_star.subs(x_C, R / 2))
    print(f"   q*|sym = {q_sym}")
    print("   The two positions are the two sides of one inequality. Neither")
    print("   is wrong; they describe different ecologies.")

    # 4. CONTROL A -- no mobility. gamma -> 0 must leave only the priority
    #    effect, for every q. If mobility were doing hidden work elsewhere in
    #    the expression this would fail.
    no_mobility = sp.simplify(advantage.subs(gamma, 0) - prior) == 0
    ok.append(no_mobility)
    print(f"\n4. CONTROL A, gamma = 0 (no horizontal transfer at all)")
    print(f"   collapses to the redundancy model for every q : {no_mobility}")

    # 5. CONTROL B -- no redundancy penalty. delta = 0 must remove the
    #    frequency dependence, leaving a boundary that does not depend on how
    #    common either form already is.
    flat = sp.simplify(sp.diff(advantage.subs(delta, 0), x_C)) == 0
    q_star_flat = sp.simplify(q_star.subs(delta, 0))
    indep = sp.simplify(sp.diff(q_star_flat, x_C)) == 0
    ok.extend([flat, indep])
    print(f"\n5. CONTROL B, delta = 0 (dual carriage costs nothing extra)")
    print(f"   no dependence on x_C                      : {flat}")
    print(f"   q* = {q_star_flat}")
    print(f"   boundary independent of current frequencies: {indep}")
    print("   Without the redundancy penalty there is no priority effect and")
    print("   the outcome is set by ecology and cost alone -- history stops")
    print("   mattering, which is the right behaviour for this control.")

    if not all(ok):
        print("\nPROBLEM: a derivation or control did not reproduce.")
        return 1

    # 6. Worked corners. Counts below are over analyst-chosen probes.
    print("\n6. WORKED CORNERS (illustrative parameter choices)")
    # Exact rationals, not floats: one corner sits algebraically on the
    # boundary and 0.010 is not 1/100 in binary, so a float base would decide
    # that corner by rounding error.
    base = {c_c: sp.Rational(1, 100), c_p: sp.Rational(3, 200),
            delta: sp.Rational(1, 25), R: sp.Rational(1, 2),
            gamma: sp.Rational(1, 50)}
    print("   c_c=0.010  c_p=0.015  delta=0.040  R=0.5  gamma=0.020")
    print(f"   {'q':>6}  {'x_C':>6}  {'w_P - w_C':>12}   favoured")
    # Exact rationals, then a tolerance band: one of these corners sits
    # algebraically ON the boundary, and deciding it by float sign would be a
    # verdict produced by rounding rather than by the model.
    probes = 0
    plasmid_wins = 0
    on_boundary = 0
    for qv in (0, sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), 1):
        for xv in (sp.Rational(3, 20), sp.Rational(1, 4), sp.Rational(7, 20)):
            exact = sp.simplify(advantage.subs(base).subs({q: qv, x_C: xv}))
            val = float(exact)
            probes += 1
            if exact == 0:
                label, on_boundary = "ON BOUNDARY", on_boundary + 1
            elif exact > 0:
                label, plasmid_wins = "plasmid", plasmid_wins + 1
            else:
                label = "chromosome"
            print(f"   {float(qv):>6.2f}  {float(xv):>6.2f}  {val:>+12.5f}   {label}")
    print(f"\n   plasmid favoured in {plasmid_wins} of {probes} grid cells, "
          f"{on_boundary} exactly on the boundary.")
    print("   GRID COUNT, NOT A FREQUENCY. Five q values and three x_C values")
    print("   are probes chosen to span the corners, not a sample from any")
    print("   population of plasmids or niches. This number must never be")
    print("   quoted as a proportion of anything biological.")

    print("\nWHAT THIS SETTLES, AND WHAT IT DOES NOT")
    print("  Settles: the two published positions are corners of one")
    print("  inequality, separated by q, and the earlier model is recovered")
    print("  exactly as the q -> 1 limit of the later mechanism.")
    print("  Does not settle: which regime any real system is in. q is an")
    print("  ecological measurement nobody has made here. Nor does it")
    print("  reproduce either paper's dynamics -- transfer, loss and mutation")
    print("  rates are folded into gamma, delta and the costs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
