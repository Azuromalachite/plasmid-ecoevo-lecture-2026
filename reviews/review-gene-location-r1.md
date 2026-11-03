# Adversarial review — gene-location model, round 1

**Artifact:** `models/gene-location/` on `main` at `29c92ec` (PRs #10 and #12)
**Reviewer:** Reviewer 3 (this session). The model's author is the forked
session, so for once in this project the reviewer did not write the artifact.
**Method:** read, re-derivation, and a feasibility sweep the scripts do not run.
**Committed 3 November 2026**, after the forked session released the shared
checkout. Findings 1 to 3 are recorded in
[`../docs/open-findings.md`](../docs/open-findings.md) as OF-13 to OF-15,
because unlike the lecture-plan review these are defects in committed public
content.

**Claim labels:** `[V]` verbatim · `[M]` measured by me · `[I]` inferred

**Headline:** the central result holds and I verified it independently — the
earlier model really is the `q → 1` corner of the later one. The defect is that
the boundary it solves for is never checked for **reachability**, which is the
exact finding this repository closed as F2 three hours ago, one model over.

---

## Finding 1 — `q*` is solved and never checked against `[0, 1]`

**Severity: high.** `[M]`

`[V]` The script states: *"Plasmid localisation is favoured for q < q\*,
chromosomal for q > q\*."* `q` is a frequency, so it lives in `[0, 1]`. `q*` is
not constrained to.

`[M]` Sweeping the four cost and rate parameters over three values each
(`c_c, c_p, δ, γ`), at `x_C = R/2`:

| | cells |
|---|---|
| `q*` inside `[0, 1]` | 38 of 81 |
| `q* > 1` — plasmid favoured at **every** feasible ecology | 28 of 81 |
| `q* < 0` — chromosome favoured at **every** feasible ecology | 15 of 81 |
| **no boundary in range** | **43 of 81** |

*Grid count, not a frequency — my denominator, chosen by me, no claim about
real systems. Applying the rule the script itself now applies.*

`[I]` So for a large part of parameter space there is no trade-off between the
two positions at all: one location wins regardless of the ecology, and `q*` is
an extrapolation outside its own variable's range. The sign of the two
out-of-range cases is opposite, exactly as in the copy-number result — `q* > 1`
when plasmid carriage is cheap relative to transfer, `q* < 0` when the cost gap
exceeds what mobility can repay.

**This is F2's defect in a new model.** `check_feasible_optimum.py` exists
because `C*` was derived and never compared with `[C_min, C_max]`. The same
script is three directories away and the same question was not asked of `q*`.

**Correction:** add a feasibility section. Report `q*` against `[0, 1]` with a
verdict per cell — `PLASMID ALWAYS` / `INTERIOR` / `CHROMOSOME ALWAYS` — and
solve the two boundary conditions in closed form as the copy-number script
does: `q* ≥ 1 ⟺ c_c − c_p ≥ 2δx_C − δR`, and `q* ≤ 0 ⟺ c_p − c_c ≥ γ + δR −
2δx_C`. The second is the more interesting statement: **mobility can only repay
a cost gap smaller than the transfer rate itself.**

**Validation:** if the script can print a parameter set where it claims a
boundary at `q* = 1.4`, the finding is unaddressed.

---

## Finding 2 — the nesting test binds to a transcription, not to the other file

**Severity: medium.** `[M]`

`[V]` The nesting check compares against a locally written literal:

```python
prior = -((c_p - c_c) + delta * (2 * x_C - R))      # from check_priority_effect
```

`[M]` That transcription is **correct today**: `check_priority_effect.py`
defines `w_C = b - c_c - delta*x_P` and `w_P = b - c_p - delta*x_C`, whose
difference is `-(c_p - c_c) - delta*(x_C - x_P)`, and `x_C - x_P = 2x_C - R`.

`[I]` But the test does not read that file. If the earlier model changes, this
check still passes and still prints *"the earlier script is this one's q → 1
limit"* — a claim about a file it never opened. The comment `# from
check_priority_effect` is the entire binding, and a comment is not a binding.

**This is the defect that broke the firewall mutation test this morning**: a
literal copied from another file, correct when written, unguarded against the
original moving. Seventh instance, now eighth.

**Correction:** import it. Both are plain modules with no side effects at
import time; `w_P - w_C` can be exposed as a module-level expression in
`check_priority_effect.py` and consumed here. Then the nesting claim is
checked against the thing it names.

---

## Finding 3 — the two "controls" are algebraic consequences of one written line

**Severity: medium.** `[I]`

`advantage` is written once, by hand:

```python
advantage = gamma * (1 - q) - (c_p - c_c) - delta * (x_C - x_P)
```

`[I]` `gamma` occurs exactly once in it, so substituting `gamma = 0` **cannot
fail** to collapse to the remaining terms. `delta` is the only coefficient on
any `x_C` term, so `delta = 0` **cannot fail** to remove the `x_C` dependence.
Both controls are properties of how that line is typed, visible by inspection.

`[V]` The script oversells them: *"If mobility were doing hidden work elsewhere
in the expression this would fail."* True only of an edit that puts `gamma`
somewhere else — which is a regression test on one line, not a control on a
model.

**The contrast is in this repository.** `check_feasible_optimum.py` *solves*
`d(ln Q)/dC = 0` and compares the solution to an independently stated closed
form, and checks the second derivative so "stationary point" is not standing in
for "maximum". Nothing is derived here; an expression is asserted and its own
shape is read back.

`[I]` This does not make the model wrong — the algebra is right and I checked
`q*` by hand. It means the script's assurance is weaker than its wording, in a
repository whose subject is exactly that gap.

**Correction:** either derive `advantage` from the two fitness expressions
rather than writing the difference directly — then `gamma = 0` tests something
— or relabel them honestly as consistency checks. The second costs one word
and is defensible.

---

## What it got right

**1. Making the disagreement the specification.** `[V]` *"one model, two
regimes, and the parameter that separates them."* The alternative — build one
mechanism, then add a caveat about the other paper — was easier and would have
buried the finding in prose. This is the hardest correct decision in the
artifact.

**2. The nesting result, which I verified independently.** `[M]` `q = 1` does
reduce exactly to the earlier model. A corner of a larger model, shown
symbolically, is far stronger evidence than two models that merely agree — and
it retires the question of which is right.

**3. The teaching line is in the mathematics, not beside it.** `[V]` *"Mobility
is rented from the ecology, not owned by the plasmid"* — because `γ` is
multiplied by `(1 − q)`, and `q` is set outside the niche. A sentence that
reads off the first term of an equation is worth more than a slide bullet.

**4. The float-rounding catch.** `[V]` A worked corner sat algebraically on the
boundary and was being decided by binary representation — `0.010` is not
`1/100` — and reported as a plasmid win. Exact rationals, an `ON BOUNDARY`
label, count moved 11 → 10. **A verdict produced by rounding is
indistinguishable from a verdict produced by the model.** That is the
instrument rule found independently, one level below where I found it.

**5. Scope attached at the point of use.** `[V]` The grid count prints its own
caveat, and *"What this settles, and what it does not"* names `q` as an
ecological measurement nobody has made. Findings 1 and 3 are about assurance,
not honesty; this artifact is unusually honest.

**6. Declining to cite `svara2011plasmidcarried` to clear the commentary-only
line.** Adding a citation to quiet a checker is the failure mode the checker
exists to expose. Leaving it is correct.

---

## The one thing to do first

**Ask `q*` the question this repository already asks `C*`.**

It is the same defect, the same shape, and the fix is a direct transcription of
a script three directories away — a verdict per cell against `[0, 1]` and the
two boundary conditions in closed form. `[M]` In my sweep that converts 43 of
81 cells from an unremarked extrapolation into a stated result: *for these
ecologies there is no trade-off, and which location wins does not depend on q
at all.*

That is also the better teaching outcome, and it is the same sentence the
copy-number model ended up with. Two independent models in this repository now
both say: the interesting question is not where the optimum or the boundary
is, but whether you can reach it.

Findings 2 and 3 are assurance debt. They can wait for a round 2, but Finding 2
should not wait long — it is an unguarded copy of another file's contents, and
this project has now been bitten by that eight times.
