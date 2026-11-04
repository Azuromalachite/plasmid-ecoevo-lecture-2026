"""Random segregation: what loss rate does a given copy number imply?

The notebook treats `LOSS_PER_DIVISION` as a declared scenario parameter, and
says so: it is "not a fitted pUC segregation law". That is the honest
treatment, because real plasmid loss depends on multimerisation, clustering,
partition systems and replication timing, none of which this models.

What this module adds is the floor. Under random segregation with no active
partition, copy number alone sets a loss rate, and that number is useful when
choosing the scenario parameter — it says what loss would be if nothing but
chance were operating.

The factor of two
-----------------
Two probabilities live here and they differ by exactly two. Conflating them is
the commonest error in this calculation, and it is a factor-of-two error in
whatever headline follows.

With c copies in a newborn cell, replicating to 2c independently segregating
molecules before division:

    p_division_loses(c) = 2 ** (1 - 2c)
        A division produces a plasmid-free daughter. Either daughter counts,
        hence the leading 2. Denominator: divisions.

    p_daughter_free(c) = 2 ** (-2c)
        A randomly chosen daughter is plasmid-free. A loss event yields one
        empty daughter out of two, so this is half the above.
        Denominator: daughters.

Propagating a *cell* fraction across generations uses the per-daughter form,
because each generation replaces the population with daughters. Quoting "how
often does a division go wrong" uses the per-division form. At c = 3 the
plasmid-bearing fraction after 100 generations is 20.7% with the correct form
and 4.2% with the other: both are right answers, to different questions.

Standard library only, so the checks run anywhere.
"""
from __future__ import annotations

import math

__all__ = [
    "p_division_loses",
    "p_daughter_free",
    "bearing_fraction_after",
    "copies_for_retention",
    "loss_table",
    "self_check",
]


def p_division_loses(copies: float) -> float:
    """Fraction of divisions producing a plasmid-free daughter: 2**(1-2c)."""
    if copies <= 0:
        raise ValueError("copies must be positive")
    return 2.0 ** (1.0 - 2.0 * copies)


def p_daughter_free(copies: float) -> float:
    """Fraction of daughters that are plasmid-free: 2**(-2c).

    Use this one when propagating a population fraction.
    """
    if copies <= 0:
        raise ValueError("copies must be positive")
    return 2.0 ** (-2.0 * copies)


def bearing_fraction_after(copies: float, generations: int) -> float:
    """Plasmid-bearing fraction after n generations, random segregation only.

    Assumes every cell starts as a carrier, equal growth for carriers and
    non-carriers, no transfer and no selection -- so the only process is
    segregational loss. Any real culture with a fitness cost loses the plasmid
    faster than this, because plasmid-free cells then outgrow carriers; this
    is the floor, not a prediction.
    """
    if generations < 0:
        raise ValueError("generations must be non-negative")
    return (1.0 - p_daughter_free(copies)) ** generations


def copies_for_retention(target: float, generations: int) -> int:
    """Smallest integer copy number retaining `target` fraction after n gens.

    Example: holding 99% of cells over 100 generations needs how many copies?
    """
    if not 0.0 < target < 1.0:
        raise ValueError("target must be strictly between 0 and 1")
    c = 1
    while bearing_fraction_after(c, generations) < target:
        c += 1
        if c > 200:
            raise RuntimeError("no copy number under 200 reaches that target")
    return c


def loss_table(copy_numbers=(3, 5, 6, 8, 10), generations=100):
    """Rows of (copies, per-division, per-daughter, bearing after n gens)."""
    return [(c, p_division_loses(c), p_daughter_free(c),
             bearing_fraction_after(c, generations)) for c in copy_numbers]


def self_check(verbose: bool = True) -> int:
    """Checks that can fail. Returns the failure count.

    Mutation-tested: removing the factor of two, swapping which probability
    `bearing_fraction_after` uses, or dropping the input validation each makes
    this report a failure.
    """
    fails = []

    for c in (1, 3, 5, 10, 40):
        if not math.isclose(p_division_loses(c), 2.0 * p_daughter_free(c)):
            fails.append(f"the two probabilities are not a factor of 2 apart "
                         f"at c={c}")

    # the published pair of numbers this module exists to keep straight
    if not math.isclose(bearing_fraction_after(3, 100), 0.20704, abs_tol=1e-5):
        fails.append(f"c=3 over 100 generations should be ~20.7%, got "
                     f"{bearing_fraction_after(3, 100)*100:.3f}% -- this is "
                     f"the per-daughter/per-division confusion")

    if bearing_fraction_after(10, 0) != 1.0:
        fails.append("zero generations should lose nobody")

    # monotone in both arguments
    vals = [bearing_fraction_after(c, 50) for c in range(2, 12)]
    if any(b < a for a, b in zip(vals, vals[1:])):
        fails.append("retention should not fall as copy number rises")
    vals = [bearing_fraction_after(5, g) for g in range(0, 200, 10)]
    if any(b > a for a, b in zip(vals, vals[1:])):
        fails.append("retention should not rise with more generations")

    # 6 copies gives 97.6%, which is short of 99%; 7 is the answer. Written
    # down because the first version of this check asserted 6 and failed.
    if copies_for_retention(0.99, 100) != 7:
        fails.append(f"99% over 100 generations should need 7 copies, got "
                     f"{copies_for_retention(0.99, 100)}")

    for bad, arg in ((0, "copies"), (-1, "copies")):
        try:
            p_daughter_free(bad)
            fails.append(f"{arg}={bad} should have raised")
        except ValueError:
            pass

    if verbose:
        for f in fails:
            print(f"  FAIL  {f}")
        print(f"  segregation.self_check: "
              f"{'all groups passed' if not fails else f'{len(fails)} failure(s)'}")
    return len(fails)


if __name__ == "__main__":
    print("Random segregation floor\n")
    failures = self_check()
    print(f"\n  {'c':>3}  {'per division':>14}  {'per daughter':>14}  "
          f"{'bearing @100 gen':>17}")
    for c, pd_, pdt, keep in loss_table():
        print(f"  {c:>3}  {pd_*100:13.6f}%  {pdt*100:13.6f}%  "
              f"{keep*100:16.3f}%")
    print("\n  Retention targets over 100 generations:")
    for t in (0.90, 0.99, 0.999):
        print(f"    {t:.1%} of cells still carrying needs "
              f"{copies_for_retention(t, 100)} copies")
    raise SystemExit(1 if failures else 0)
