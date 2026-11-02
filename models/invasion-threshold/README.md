# The plasmid invasion threshold — derivation and its sensitivity domain

**Stable ID:** `model.invasion-threshold.chemostat`

Stable IDs are persistent and are not reused. Repository paths may change
without changing identity: if this directory moves, the ID does not.

The check: [`check_invasion_threshold.py`](check_invasion_threshold.py).

---

## What question does it answer?

**When does a rare plasmid increase in a resource-limited continuous culture,
and over what range of conditions is that answer actually tested?**

The condition itself is short. In a well-mixed chemostat with mass-action
transfer and per-unit-time segregational loss, a rare plasmid-bearing class
increases when

> γ·n\* > c·ψ + τ

where *n*\* is the plasmid-free density at the plasmid-free equilibrium and ψ
there equals the dilution rate. It is the registry claim
`claim.model.plasmid_invasion_threshold` (`layer: model`,
`status: supported`), and it is used on
[`fitness-vs-persistence.md`](../../concepts/fitness-vs-persistence.md).

This directory exists for the second half of the question. A derivation can be
right and its verification worthless, and that is what happened here.

## Why it exists: OF-1

The previous verification drew parameter sets independently, discarded those
that happened to land within 5% of the threshold, and reported that the sign
of the invasion expression predicted the outcome in **59 of 59** of the rest.

Parameters drawn that way land far from the boundary almost surely. The script
measures the old design in its own terms: drawing transfer rates log-uniformly
over the range a plasmid study would consider gives a median distance from the
threshold of about **1.0** in relative terms, with **14%** of draws two or more
orders of magnitude away and only **1.1%** inside the 5% band the old test
discarded. A sign test over cases that far from a boundary cannot fail. The
number sounded discriminating and was a description of the sampler.

`59/59` is no longer offered as a verification result anywhere in this
repository. It survives only where it belongs — in this section, in the
registry entry's correction note, and in the ledger — as the record of what was
replaced. What replaced it is below.

## What the check does

**Symbolically**, with SymPy, two things are derived rather than asserted:

1. the total-cell balance cancels conjugation and segregation exactly
   (residual 0) — they move cells between classes and must not create or
   destroy any;
2. the plasmid row of the Jacobian at the plasmid-free equilibrium is `[0, 0]`
   off the diagonal, so the eigenvalue governing a rare plasmid-bearing class
   **is** γ·n\* − c·ψ − τ exactly, not to leading order. This is the step worth
   checking: it is what makes the condition a statement about the model rather
   than about an approximation to it.

**Numerically**, cases are *constructed from the invariant being tested*.
Everything except the transfer rate is held fixed, the critical transfer rate
is solved for, and γ is set to γ\_crit·(1 + ε) for a ladder of signed ε. The
predicted eigenvalue is then exactly ε·(c·D + τ), so ε is a dimensionless
signed distance from the threshold with a known consequence. The full nonlinear
system is integrated and the realised exponential rate is measured against it.

Integration uses ln *P* as a state variable. *P* spans many orders of magnitude
and stays positive by construction; in linear *P* a solver's absolute tolerance
would sit far above the effects being measured, and the measurement floor would
be the solver's rather than the model's.

## What is reported: a sensitivity domain, not a pass count

| | |
| --- | --- |
| **Rate recovered** | better than 6 × 10⁻⁶ relative error for \|ε\| ≤ 1 |
| **Sign recovered** | down to \|ε\| ≈ 10 × *P*₀/*n*\* |
| **Measured at** | \|ε\| = 1e-5, 1e-7, 1e-9, 1e-11, 1e-13 for inocula 1e-4, 1e-6, 1e-8, 1e-10, 1e-12 of *n*\* |
| **Upper edge** | the realised rate departs by 93% at ε = 10, and the plasmid-free state stops being the right reference entirely by ε = 100 |

**The lower edge is a property of the question, not of the arithmetic.** An
eigenvalue describes the limit of a vanishing plasmid-bearing class. Any class
you can simulate is not vanishing: a finite inoculum displaces the resident
state by order *P*₀/*n*\*, and that displacement is what sets how close to the
boundary the test can resolve. The evidence that this is the mechanism — rather
than a solver floor dressed up as physics — is that the edge tracks the
inoculum at a constant ratio across **eight orders of magnitude**, and the
measured rate error scales with *P*₀/*n*\* in the same way.

**The ladder reports when it has run out.** If the finest resolved ε sits at the
bottom of the ε ladder, the script fails rather than quoting it, because that
number would be the instrument's floor and not the system's resolution. The
run that produced the table above has two decades of headroom below its
deepest row.

## What this does *not* establish

- **That the condition holds empirically.** `status: supported` here means
  supported *within* the stated model. An experiment that disagreed would most
  likely show that an assumption fails, not that the algebra is wrong.
- **Anything about the assumptions themselves.** Mass-action transfer breaks
  above roughly 10⁶ cells·mL⁻¹ in liquid; the habitat is assumed well-mixed;
  segregation is per unit time, so the threshold must be re-derived under a
  per-division convention; transconjugants are assumed to transfer like donors;
  the cost is constant. These are listed with their sources in the registry
  entry and on the concept page, and none of them is tested here.
- **Displacement.** It is an invasion condition. It says a rare plasmid
  increases, not that it sweeps to fixation.
- **That the parameter values are anyone's measurements.** They are a
  physiologically ordinary chemostat, chosen so that the equilibrium exists and
  the critical transfer rate lands inside the range the literature reports.
  Nothing in the result depends on them: the quantity under test is ε, which is
  defined relative to whatever the parameters are.

## Running it

From the repository root:

```bash
uv run --no-project --with numpy --with scipy --with sympy python models/invasion-threshold/check_invasion_threshold.py
```

It needs NumPy, SciPy and SymPy, and exits 1 if any part disagrees with the
claim as stated. SymPy is required rather than optional: a symbolic check that
skips itself when an import fails is a check that reports clean on a domain it
never entered, which is the defect this directory exists to remove.

The script prints tables and no figures, writes nothing, and takes well under a
minute.
