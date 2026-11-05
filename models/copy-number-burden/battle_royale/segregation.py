"""Random segregation: what loss rate does a given copy number imply?

The notebook treats `LOSS_PER_DIVISION` as a declared scenario parameter, and
says so: it is "not a fitted pUC segregation law". That is the honest
treatment, because real plasmid loss depends on multimerisation, clustering,
partition systems and replication timing, none of which this models.

What this module adds is the reference point. Under random segregation with
no active partition, copy number alone sets a loss rate, and that number is
useful when choosing the scenario parameter — it says what loss would be if
nothing but chance were operating on molecules that are genuinely independent
and genuinely as numerous as the measured copy number.

It is NOT a floor, and earlier versions of this file called it one. Measured
loss rates fall on both sides. Partition systems, multimer resolution and
toxin-antitoxin push below it; multimerisation, clustering and fitness cost
push above it, and for ColE1-type vectors the net is five to eight orders of
magnitude ABOVE: Summers & Sherratt (1984, PMID 6323019) report loss at
1e-2 to 1e-5 per cell per generation for plasmids whose copy number would
predict about 1e-9. The gap is not a modelling detail; it is the subject.
See concepts/random-segregation-is-not-a-floor.md.

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

Mean copy number does not determine the loss rate
------------------------------------------------
Everything above assumes every cell carries the same number of copies. Real
populations do not: copy number varies cell to cell, and 2**(-2c) is steeply
convex, so the rare low-copy cells dominate the loss rate entirely. Averaging
the loss rate over a distribution is therefore NOT the loss rate at the mean,
and the gap grows with both the mean and the spread.

`population_loss_rate` does that average. At a mean of 20 copies, a CV of 0.6
raises the loss rate about eight orders of magnitude above the uniform value,
so quoting a loss rate from a mean copy number alone is not a small
approximation. It is the wrong calculation.

Standard library only, so the checks run anywhere.
"""
from __future__ import annotations

import math

__all__ = [
    "p_division_loses",
    "p_daughter_free",
    "daughter_distribution",
    "bearing_fraction_after",
    "copy_number_pmf",
    "population_loss_rate",
    "carrier_mean",
    "loss_rate_from_division_counts",
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


def daughter_distribution(copies: int) -> list[float]:
    """Probability a daughter inherits k of the 2c molecules, for k = 0..2c.

    This is the textbook segregation picture: a cell with `copies` plasmids
    replicates to 2c, then each molecule goes to one daughter or the other
    independently. Nothing here is simulated. One division of independently
    segregating molecules is a binomial draw, so the whole distribution is
    closed form, and sampling it would add noise to an exact answer.

    Both probabilities this module exists to keep apart are visible in the
    returned list, which is the reason it is worth drawing:

        dist[0]              this daughter is empty
        dist[0] + dist[-1]   the division produced an empty daughter, either one

    That is the factor of two, as a picture rather than as an exponent.

    `copies` must be a whole number; you cannot count subsets of half a
    molecule.
    """
    if copies != int(copies) or copies <= 0:
        raise ValueError("copies must be a positive whole number")
    n = 2 * int(copies)
    return [math.comb(n, k) * 0.5 ** n for k in range(n + 1)]


def bearing_fraction_after(copies: float, generations: int) -> float:
    """Plasmid-bearing fraction after n generations, random segregation only.

    Assumes every cell starts as a carrier, equal growth for carriers and
    non-carriers, no transfer and no selection -- so the only process is
    segregational loss.

    Against a fitness cost alone this is a CEILING on retention, not a floor:
    plasmid-free cells outgrow carriers, so a real culture keeps less than
    this. But several mechanisms run the other way -- partition systems,
    multimer resolution, conjugation re-infecting free cells -- and others,
    such as multimerisation and clustering, make retention worse still. The
    returned number bounds nothing in general. It is the retention you would
    see if segregation were the only process, which it never is.
    See concepts/random-segregation-is-not-a-floor.md.
    """
    if generations < 0:
        raise ValueError("generations must be non-negative")
    return (1.0 - p_daughter_free(copies)) ** generations


def _normal_cdf(x: float) -> float:
    """Standard normal CDF, via math.erf so this file stays stdlib-only."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _default_kmax(mean_copies: float, cv: float) -> int:
    """A ceiling far enough out that the truncated tail is negligible."""
    if cv <= 0.0:
        return max(1, int(round(mean_copies)))
    sigma = math.sqrt(math.log(1.0 + cv * cv))
    return int(math.ceil(mean_copies * math.exp(6.0 * sigma))) + 20


def copy_number_pmf(mean_copies: float, cv: float = 0.0, kmax=None):
    """P(c = k) for k = 0..kmax, copy number lognormal and rounded to integers.

    The same distribution the notebook's single-cell simulation draws from
    (`_lognormal_integer_sample`), written as a probability mass function so
    it can be summed exactly rather than sampled.  `cv` is the coefficient of
    variation of copy number across cells at birth.

    This distribution is an ASSUMPTION, not a measurement.  Lognormal is a
    convenient positive, right-skewed choice; the left tail is what drives
    every number downstream, and that is the part a lognormal is least
    entitled to claim it got right.
    """
    if mean_copies <= 0:
        raise ValueError("mean_copies must be positive")
    if cv < 0:
        raise ValueError("cv must be non-negative")
    if kmax is None:
        kmax = _default_kmax(mean_copies, cv)
    if kmax < 1:
        raise ValueError("kmax must be at least 1")
    if cv == 0.0:
        k = int(round(mean_copies))
        if k > kmax:
            # This used to clamp with min(), which returned a pmf putting all
            # its mass at kmax -- a confident, silent, wrong answer. A caller
            # asking for mean 10 with kmax 5 got "every cell has 5 copies".
            raise ValueError(
                f"kmax={kmax} is too small for a mean of {mean_copies}: "
                f"the distribution needs index {k}")
        pmf = [0.0] * (kmax + 1)
        pmf[k] = 1.0
        return pmf
    sigma2 = math.log(1.0 + cv * cv)
    sigma = math.sqrt(sigma2)
    mu = math.log(mean_copies) - 0.5 * sigma2

    def cdf(x):
        return 0.0 if x <= 0.0 else _normal_cdf((math.log(x) - mu) / sigma)

    return [cdf(k + 0.5) - cdf(k - 0.5) for k in range(kmax + 1)]


def population_loss_rate(mean_copies: float, cv: float = 0.0, kmax=None):
    """Per-daughter loss rate across a population with varying copy number.

    The average of `p_daughter_free` over the copy-number distribution,
    conditioned on carriers, since a cell that already has no plasmid cannot
    lose one.

    With `cv=0` this reduces to `p_daughter_free(round(mean_copies))`.  Note
    the `round`: at cv=0 this function is a staircase in `mean_copies`, not a
    curve.  The smooth reference to plot a spread curve against is therefore
    `p_daughter_free(m)` at real-valued m, not this function at cv=0, which
    would draw the rounding rather than the biology.

    From a mean of about 3 copies upward, any spread makes the rate strictly
    larger, because 2**(-2c) is convex: Jensen's inequality, and it is not a
    small correction.  That is the regime the figure plots and the only one
    the self-check asserts.

    BELOW it the inequality fails, and two earlier versions of this docstring
    claimed otherwise -- first for all means, then for means above 2.  Two
    effects compete with convexity down there:

      * conditioning on carriers.  A carrier holds at least one copy by
        definition, so at a mean near 1 spread raises the copy number *among
        carriers* rather than exposing a low tail, and the rate falls with
        cv instead of rising.
      * skew plus rounding.  A lognormal rounded to integers puts more mass
        above the mean than below it, and at small cv that asymmetry is
        larger than the convexity gain.  At mean 2, cv 0.1 the rate lands
        just under the floor -- 6.241e-02 against 6.250e-02.

    Neither is a bug; both are properties of the model as specified.  They
    are recorded here because "more spread means more loss" is the sentence
    the figure teaches, and it is only true away from the boundary.

    Same scope as the rest of this module: random segregation only.  No
    partition system, no multimer resolution, no clustering, no selection.

    A low-copy plasmid with an active partition system lives far BELOW this
    curve, and that distance measures what partitioning is doing.  A
    multimerising or clustering high-copy vector lives far ABOVE it, because
    neither the segregating unit nor its count is what the formula assumes.
    Do not read a gap in either direction as an error.
    See concepts/random-segregation-is-not-a-floor.md.
    """
    if kmax is None:
        kmax = _default_kmax(mean_copies, cv)
    pmf = copy_number_pmf(mean_copies, cv, kmax)
    carriers = math.fsum(pmf[1:])
    if carriers <= 0.0:
        raise ValueError("distribution puts no mass on carriers")
    weighted = math.fsum(p * 2.0 ** (-2 * k)
                         for k, p in enumerate(pmf) if k >= 1)
    return weighted / carriers


def carrier_mean(mean_copies: float, cv: float = 0.0, kmax=None) -> float:
    """Mean copy number among carriers: the x value a loss rate belongs at.

    `population_loss_rate` conditions on carriers, so the distribution it
    averages over is NOT the one `mean_copies` names -- dropping the
    zero-copy cells raises the mean.  At a nominal mean of 10 the difference
    is invisible; at a nominal mean of 1 with cv 1.0 the carriers average
    1.46 copies.

    This is the whole explanation of the apparent curve crossings at low
    mean, and it is worth stating precisely, because Jensen's inequality is
    unconditional:

        E[2**(-2c)]  >=  2**(-2 E[c])      for ANY distribution of c

    So a spread population can never fall below the uniform line when both
    are read at the SAME mean.  If a plot shows one doing so, the two means
    are not the same, and the fix is to plot against this function rather
    than against the nominal mean.  Nothing biological is happening.
    """
    if kmax is None:
        kmax = _default_kmax(mean_copies, cv)
    pmf = copy_number_pmf(mean_copies, cv, kmax)
    carriers = math.fsum(pmf[1:])
    if carriers <= 0.0:
        raise ValueError("distribution puts no mass on carriers")
    return math.fsum(k * p for k, p in enumerate(pmf) if k >= 1) / carriers


def loss_rate_from_division_counts(pairs) -> float:
    """Per-daughter loss rate for an ARBITRARY distribution of copies.

    `pairs` is an iterable of (N, probability) where N is the number of
    independently segregating copies present at division -- twice the birth
    copy number in the idealised picture the rest of this module uses.
    Returns E[2**-N] conditioned on N >= 1.

    This exists because mean and CV do not determine the loss rate, and
    `copy_number_pmf` cannot show that, having only those two knobs.  Two
    distributions can share a mean AND a variance and still sit three orders
    of magnitude apart, because the answer is set by the shape of the
    low-copy tail and neither moment describes it.  `self_check` carries such
    a pair, so no curve in this repository can quietly start implying that
    (mean, cv) is enough.
    """
    items = [(int(n), float(p)) for n, p in pairs]
    if any(n < 0 for n, _ in items):
        raise ValueError("copy counts must be non-negative")
    if any(p < 0 for _, p in items):
        raise ValueError("probabilities must be non-negative")
    total = math.fsum(p for _, p in items)
    if not math.isclose(total, 1.0, abs_tol=1e-9):
        raise ValueError(f"probabilities must sum to 1; got {total}")
    carriers = math.fsum(p for n, p in items if n >= 1)
    if carriers <= 0.0:
        raise ValueError("distribution puts no mass on carriers")
    return math.fsum(p * 2.0 ** (-n) for n, p in items if n >= 1) / carriers


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

    # The distribution is the picture: one division drawn as 2c+1 outcomes.
    for c in (1, 2, 3, 6):
        dist = daughter_distribution(c)
        if not math.isclose(sum(dist), 1.0, abs_tol=1e-12):
            fails.append(f"daughter_distribution({c}) sums to {sum(dist)}, not 1")
        if not math.isclose(dist[0], p_daughter_free(c)):
            fails.append(f"dist[0] should be p_daughter_free({c}): "
                         f"{dist[0]} vs {p_daughter_free(c)}")
        if not math.isclose(dist[0] + dist[-1], p_division_loses(c)):
            fails.append(f"dist[0]+dist[-1] should be p_division_loses({c}) -- "
                         f"both ends of the distribution are a lost division")
        if any(not math.isclose(a, b) for a, b in zip(dist, reversed(dist))):
            fails.append(f"daughter_distribution({c}) is not symmetric")
        if len(dist) != 2 * c + 1:
            fails.append(f"daughter_distribution({c}) has {len(dist)} outcomes, "
                         f"expected {2 * c + 1}")

    # c=2 is the figure every textbook draws: 4 molecules, 1:4:6:4:1 in 16ths
    if [round(p * 16) for p in daughter_distribution(2)] != [1, 4, 6, 4, 1]:
        fails.append(f"c=2 should give 1:4:6:4:1 in sixteenths, got "
                     f"{[round(p * 16) for p in daughter_distribution(2)]}")

    for bad in (2.5, 0, -1):
        try:
            daughter_distribution(bad)
            fails.append(f"daughter_distribution({bad}) should have raised")
        except ValueError:
            pass

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

    # A copy-number distribution is a distribution.
    for m, cv in ((3, 0.2), (10, 0.4), (20, 0.6), (7, 1.0)):
        total = math.fsum(copy_number_pmf(m, cv))
        if not math.isclose(total, 1.0, abs_tol=1e-9):
            fails.append(f"copy_number_pmf({m}, {cv}) sums to {total}, not 1 -- "
                         f"the tail is being truncated too early")

    # No spread: the population rate must collapse to the single-cell one.
    for m in (2, 5, 10, 20):
        if not math.isclose(population_loss_rate(m, 0.0), p_daughter_free(m),
                            rel_tol=1e-12):
            fails.append(f"population_loss_rate({m}, cv=0) should equal "
                         f"p_daughter_free({m})")

    # Jensen: 2**(-2c) is convex, so spread raises the average -- but only
    # where convexity dominates. Tested from mean 3 upward; at mean 2 with
    # cv 0.1 it fails by 0.1%, for the reason the docstring gives.
    for m in (3, 5, 10, 20):
        floor = p_daughter_free(m)
        for cv in (0.1, 0.3, 0.6):
            got = population_loss_rate(m, cv)
            if got <= floor:
                fails.append(f"population_loss_rate({m}, cv={cv}) = {got:.3e} "
                             f"is not above the uniform floor {floor:.3e}; "
                             f"convexity says it must be")

    # carrier_mean needs checking in its own right: the Jensen check below
    # only bites when it comes out too SMALL, so a mean that drifts upward
    # would sail through. With no spread it must be exactly the rounded mean.
    for m in (2.0, 5.0, 10.0, 20.0):
        if carrier_mean(m, 0.0) != float(round(m)):
            fails.append(f"carrier_mean({m}, 0) should be {float(round(m))}, "
                         f"got {carrier_mean(m, 0.0)}")
    # Conditioning removes the lowest bin, so it must raise the mean -- but
    # relative to the pmf's OWN mean, not the nominal one. Rounding a skewed
    # distribution to integers already moves the pmf's mean off the nominal
    # value (at mean 2, cv 0.4 the pmf averages 1.9946), and an earlier
    # version of this check compared against the nominal mean and failed on
    # correct code.
    for m in (1.0, 2.0, 5.0, 20.0):
        for cv in (0.1, 0.4, 1.0):
            pmf = copy_number_pmf(m, cv)
            raw = math.fsum(k * p for k, p in enumerate(pmf))
            if pmf[0] > 1e-12 and not carrier_mean(m, cv) > raw:
                fails.append(f"carrier_mean({m}, {cv}) = "
                             f"{carrier_mean(m, cv)} does not exceed the "
                             f"unconditioned mean {raw}, though {pmf[0]:.3e} "
                             f"of cells carry nothing; conditioning is not "
                             f"happening")

    # Jensen stated the way it is actually true: against the CONDITIONED
    # mean. In that form it is unconditional and admits no regime boundary,
    # which makes it a far better check than the boundary assertions it
    # replaces -- those tested where my x axis was wrong, not where the
    # mathematics changes.
    for m in (1.0, 1.5, 2.0, 2.5, 3.0, 5.0, 10.0, 20.0):
        for cv in (0.1, 0.2, 0.4, 0.6, 1.0):
            got = population_loss_rate(m, cv)
            cm = carrier_mean(m, cv)
            ref = p_daughter_free(cm)
            if got < ref * (1.0 - 1e-12):
                fails.append(f"Jensen violated at nominal mean {m}, cv {cv}: "
                             f"{got:.4e} < {ref:.4e} at carrier mean "
                             f"{cm:.4f} -- convexity cannot be beaten, so "
                             f"this is an arithmetic error, not a regime")

    # The apparent crossings against the NOMINAL mean are still real, and
    # still worth pinning down, but they are now diagnosed rather than
    # described: conditioning moved the mean. Both of these hold because
    # carrier_mean(m, cv) > m, not because spread helps.
    for m, cv in ((1.0, 0.6), (2.0, 0.1)):
        if not population_loss_rate(m, cv) < p_daughter_free(m):
            fails.append(f"expected an apparent crossing at nominal mean {m},"
                         f" cv {cv}")
        if not carrier_mean(m, cv) > m:
            fails.append(f"the crossing at mean {m}, cv {cv} should be "
                         f"explained by carrier_mean exceeding {m}; it is "
                         f"{carrier_mean(m, cv)}")

    # Mean and CV do not determine the loss rate, and no curve labelled by
    # those two numbers can. These populations share a mean of 40 copies at
    # division AND a variance of 16, and sit ~2600x apart.
    pop_a = [(36, 0.5), (44, 0.5)]
    pop_b = [(20, 0.02), (40, 0.96), (60, 0.02)]
    for name, dist in (("A", pop_a), ("B", pop_b)):
        mu = math.fsum(n * p for n, p in dist)
        variance = math.fsum(p * (n - mu) ** 2 for n, p in dist)
        if not (math.isclose(mu, 40.0) and math.isclose(variance, 16.0)):
            fails.append(f"counterexample {name} should have mean 40 and "
                         f"variance 16; got {mu} and {variance}")
    ratio = (loss_rate_from_division_counts(pop_b)
             / loss_rate_from_division_counts(pop_a))
    if not 2000.0 < ratio < 3500.0:
        fails.append(f"two populations sharing a mean and a variance should "
                     f"differ by roughly 2600x here; got {ratio:.0f}")

    # ...and the uniform case must agree with the single-cell formula.
    if not math.isclose(loss_rate_from_division_counts([(40, 1.0)]),
                        p_daughter_free(20), rel_tol=1e-12):
        fails.append("loss_rate_from_division_counts disagrees with "
                     "p_daughter_free on a uniform population")

    # Half the cells carry nothing: the answer is the rate among the half
    # that do, 2**-2, not half of it. Without this the conditioning in
    # loss_rate_from_division_counts is untested, because every other
    # distribution here puts no mass at zero.
    if not math.isclose(loss_rate_from_division_counts([(0, 0.5), (2, 0.5)]),
                        0.25, rel_tol=1e-12):
        fails.append("loss_rate_from_division_counts is not conditioning on "
                     "carriers: plasmid-free cells are being averaged in")

    for bad in ([(10, 0.5)], [(-1, 1.0)], [(0, 1.0)], [(10, 2.0)]):
        try:
            loss_rate_from_division_counts(bad)
            fails.append(f"loss_rate_from_division_counts({bad}) should have "
                         f"raised")
        except ValueError:
            pass

    # Monotone: more spread is worse, more copies are better.
    for m in (5, 10, 20):
        series = [population_loss_rate(m, cv) for cv in (0.0, 0.2, 0.4, 0.6)]
        if any(b <= a for a, b in zip(series, series[1:])):
            fails.append(f"loss rate at mean {m} is not increasing in CV: "
                         f"{series}")
    for cv in (0.0, 0.3, 0.6):
        series = [population_loss_rate(m, cv) for m in (3, 5, 8, 12, 20)]
        if any(b >= a for a, b in zip(series, series[1:])):
            fails.append(f"loss rate at CV {cv} is not decreasing in mean copy "
                         f"number: {series}")

    # The headline the figure rests on, as a check rather than a caption.
    spread = population_loss_rate(20, 0.6) / p_daughter_free(20)
    if not 1e7 < spread < 1e9:
        fails.append(f"mean 20 at CV 0.6 should sit 7-9 orders above the "
                     f"uniform floor; got {spread:.3e}")

    # The distribution must have the mean it was asked for. This is what
    # catches a dropped lognormal median correction, which leaves every other
    # property of the pmf intact and so slips past all the checks above.
    # The tolerance is loose at low mean because rounding to integers biases
    # a skewed distribution upward, and that bias is real, not a bug.
    for m, cv, tol in ((5, 0.3, 1e-4), (10, 0.4, 1e-4), (20, 0.6, 1e-4),
                       (10, 1.0, 1e-3), (2, 0.2, 2e-2)):
        got = math.fsum(k * p for k, p in enumerate(copy_number_pmf(m, cv)))
        if abs(got - m) / m > tol:
            fails.append(f"copy_number_pmf({m}, {cv}) has mean {got:.4f}, not "
                         f"{m} (rel err {abs(got - m) / m:.2e} > {tol})")

    # Conditioning on carriers is load-bearing, but only visible where a large
    # share of cells hold nothing. At mean 1 and CV 3 the conditioned rate is
    # about 2.6x the unconditioned one; at mean 20 they agree to five figures,
    # which is why every other case here misses this.
    low = population_loss_rate(1.0, 3.0)
    if not low > 0.12:
        fails.append(f"population_loss_rate(1.0, 3.0) = {low:.4f}; a rate "
                     f"averaged over carriers alone cannot be that low, so "
                     f"plasmid-free cells are being counted as carriers")

    # A kmax too small to hold the distribution must refuse, not truncate.
    try:
        copy_number_pmf(10, 0.0, kmax=5)
        fails.append("copy_number_pmf(10, 0.0, kmax=5) silently reported 5 "
                     "copies instead of refusing")
    except ValueError:
        pass

    # The cv=0 cases matter: with cv>0 an absent guard is masked by math.log
    # raising on its own, so those inputs test nothing.
    for bad_m, bad_cv in ((0, 0.3), (-1, 0.3), (10, -0.1),
                          (0, 0.0), (-1, 0.0)):
        try:
            copy_number_pmf(bad_m, bad_cv)
            fails.append(f"copy_number_pmf({bad_m}, {bad_cv}) should have raised")
        except ValueError:
            pass

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
    print()
    print("  One division, c = 2 (the four-molecule picture):")
    for k, p in enumerate(daughter_distribution(2)):
        bar = "#" * round(p * 48)
        print(f"    daughter gets {k}/4  {p * 100:6.2f}%  {bar}")
    print("    top bar alone = this daughter is empty;"
          " top + bottom = the division lost one")
    print("\n  Retention targets over 100 generations:")
    for t in (0.90, 0.99, 0.999):
        print(f"    {t:.1%} of cells still carrying needs "
              f"{copies_for_retention(t, 100)} copies")
    print()
    print("  Loss rate per daughter vs MEAN copy number, by spread:")
    cvs = (0.0, 0.2, 0.4, 0.6)
    header = "".join(("CV=" + str(c)).rjust(14) for c in cvs)
    print("      mean" + header)
    for m in (3, 5, 8, 10, 15, 20):
        row = "".join(f"{population_loss_rate(m, c):14.3e}" for c in cvs)
        print(f"    {m:6d}" + row)
    print("    Same mean, different spread, up to eight orders apart.")
    raise SystemExit(1 if failures else 0)
