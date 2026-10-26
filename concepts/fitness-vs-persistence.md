# Fitness is a measurement; persistence is an outcome

A competition assay returns a number: the relative fitness of plasmid-bearing
cells against plasmid-free cells, usually written *w* or as a cost *c* = 1 − *w*.
It is a real measurement of a real quantity. It is also not, on its own, an
answer to the question people usually want answered, which is: **will this
plasmid still be here?**

> **Measuring fitness does not by itself predict fate.**

---

## The chain from cost to fate

A fitness cost enters the outcome through three channels, and the other two
can overturn it.

```
         fitness cost (c)
                │
    ┌───────────┼─────────────────┐
    ▼           ▼                 ▼
growth      segregational     horizontal
difference      loss            transfer
    │           │                 │
    └───────────┴─────────────────┘
                │
                ▼
     persistence or extinction
```

1. **Growth difference.** The cost compounds per generation. Alone, a cost
   drives the plasmid out.
2. **Segregational loss.** Plasmid-free cells are generated from
   plasmid-bearing ones at some rate per division, independent of the cost.
   Alone, this also drives the plasmid out, and faster at low copy number
   without partition systems [@nordstrom1989segregation].
3. **Horizontal transfer.** Plasmid-bearing cells are generated from
   plasmid-free ones. This is the only term with the opposite sign.

Persistence is the balance of the three, and this has been the structure of
plasmid population models since the beginning [@stewart1977population]. The
classical result is that a conjugative plasmid can be maintained despite a
substantial growth disadvantage when transfer is sufficiently frequent
[@stewart1977population], and the corresponding empirical result is that
common conjugative plasmids do transfer fast enough for this to happen without
antibiotic selection [@lopatkin2017persistence]. A review of this model family
is available [@hernandezbeltran2021models].

## Worked example: a plasmid imposes a 5% growth cost. Does it disappear?

This is the one fully worked example in the repository, and it runs the whole
cycle described in
[`../docs/pedagogy-conventions.md`](../docs/pedagogy-conventions.md).

### Predict

A conjugative plasmid costs its host 5% of its growth rate. No antibiotic is
present. **Over a few hundred generations, does the plasmid disappear from the
population?**

Commit to yes or no before reading on, and optionally note whether your
confidence is low, medium or high. Nothing records your answer.

<details>
<summary>Evidence</summary>

**It depends, and the condition is not about the cost alone.**

Empirically: common conjugative plasmids, including costly ones, are
maintained in *E. coli* without antibiotic selection — demonstrated across
nine plasmids from six incompatibility groups [@lopatkin2017persistence].
So "a costly plasmid is eliminated" is wrong as a general claim.

But the opposite claim is equally wrong. The same literature's starting point
is that a cost, acting alone, does remove a plasmid
[@stewart1977population]. Both outcomes are reachable.

</details>

### Diagnose

If you predicted extinction, the assumption that did the work was almost
certainly that **plasmid-bearing cells only come from other plasmid-bearing
cells.** Under vertical inheritance alone that prediction is right: a 5% cost
compounds every generation and segregational loss only adds to it.

The omitted term is horizontal transmission. Plasmid-bearing cells are also
produced *from plasmid-free ones*, and that is the only term in the balance
with the opposite sign.

If you predicted persistence, check whether you assumed it rather than derived
it — the conditions below are what it actually requires.

### Reconstruct

Three processes, two of which remove the plasmid:

| Process | Direction | Parameter |
| --- | --- | --- |
| Growth difference (the cost) | removes | *c* |
| Segregational loss | removes | *τ* |
| Conjugative transfer | adds | *γ* |

**`MODEL`** — what follows is derived, not measured. In a resource-limited
continuous culture with mass-action transfer and per-unit-time segregational
loss, a rare plasmid increases when

> **γ·n\* > c·ψ + τ**

where *n\** is the density of plasmid-free cells, *ψ* the steady-state growth
rate, *c* the fractional cost and *τ* the segregational loss rate. Transfer
has to outpace cost **plus** loss, and it is the *product* γ·n\* that competes
with the cost, so the same plasmid flips outcome with host density.

<details>
<summary>Where this comes from, and what it assumes</summary>

The plasmid-free equilibrium of the resource-explicit chemostat model is
isolated, its Jacobian there is upper triangular, and the eigenvalue governing
a rare plasmid-bearing class is γ·n\* − c·ψ − τ. Derived symbolically and
checked numerically: the cell balance cancels conjugation and segregation
exactly, and the sign of that expression predicted invasion in 59 of 59
simulated parameter sets outside a 5% band around the threshold.

It assumes mass-action transfer, which is itself a modelling choice that
fails above roughly 10⁶ cells·mL⁻¹ in liquid, where transfer saturates; a
well-mixed habitat, so no spatial structure; per-unit-time segregation, which
is a convention — the threshold has to be re-derived if you switch to
per-division; transconjugants that transfer like donors; and a constant cost.

It is an **invasion** condition, not a displacement condition. It says a rare
plasmid increases, not that it sweeps to fixation.

</details>

### Contrast

Hold the 5% cost fixed and lower the transfer rate. With a plasmid-free
density of 10⁸ cells·mL⁻¹, a growth rate of 0.5 h⁻¹ and segregational loss of
10⁻⁴ h⁻¹, the cost-plus-loss side of the balance is about 0.025 h⁻¹. A
transfer rate of 10⁻⁹ mL·cell⁻¹·h⁻¹ gives γ·n\* ≈ 0.1 h⁻¹ and the plasmid
invades; 10⁻¹¹ gives 0.001 h⁻¹ and it is lost. Same cost, same host, opposite
fate, from a parameter the cost measurement never touched. **`MODEL`** — these
are illustrative parameter values, not measurements of any real plasmid.

**Transfer is not the only route to persistence**, and presenting it as the
answer would be its own overclaim. A costly plasmid can also persist through
**compensatory evolution** that reduces the cost
[@sanmillan2017costs; @delafuente2022withinpatient], through **positive
selection** whenever the cargo pays, and through **spatial structure**, which
can let a plasmid invade on a surface while the same plasmid fails in liquid
[@fox2008spatial]. The honest summary is that a cost is one term among
several.

### Retrieve later

This returns in [`copy-carry-spread.md`](copy-carry-spread.md), where γ·n\* is
the SPREAD side of the same balance and *c* and *τ* are the CARRY side, and
again in the pOXA-48 discussion below, where a plasmid's cost turns out to be
small or even negative in many wild-type hosts — which moves the left-hand
side of the inequality rather than the right.

---

## Four reasons a cost measurement under-determines the outcome

**1. The missing terms.** A cost of 3% per generation sounds decisive until
you learn the conjugation rate, and then it may not be. Neither number alone
settles anything.

**2. Context dependence of the cost itself.** Cost is measured in a host, a
medium and a growth regime. The same plasmid, pOXA-48_K8, measured across
wild-type enterobacteria from the human gut, showed mostly small effects and
beneficial effects in several isolates, varying with host phylogeny
[@alonsodelvalle2021variability]. A single-host cost is a single point in a
distribution.

**3. The distribution matters, not just its mean.** In that same study, the
*variability* of fitness effects across hosts was itself what changed the
persistence conditions: in a population model, plasmid persistence increased
with community diversity and became less dependent on conjugation
[@alonsodelvalle2021variability]. A community where the plasmid is neutral in
one member behaves differently from a uniform community with the same mean
cost.

**4. Costs change.** Compensatory evolution reduces cost over time
[@sanmillan2017costs], including within individual patients
[@delafuente2022withinpatient], and transfer rates evolve too
[@dimitriu2021copy]. A cost measured at *t* = 0 may not describe *t* = 200
generations. Spatial structure and nutrient supply shift the outcome without
changing the cost at all [@fox2008spatial].

That no single one of these resolves the general question of why costly
plasmids are so common is the "plasmid paradox", which remains open
[@carroll2018persistence].

## What to report

For a fitness measurement to be usable by someone else, it needs:

- the host strain and the competitor;
- the medium, growth regime and whether structure was present;
- what was measured (exponential growth rate, lag, yield, or a composite like
  relative fitness over a passage);
- the number of generations;
- whether segregational loss was measured separately or folded in;
- whether transfer was blocked, measured, or neither.

A conjugation rate should be reported as a rate constant estimated under a
stated model, not as a ratio of transconjugants to donors at an arbitrary time
point, which depends on growth and on when you looked
[@simonsen1990endpoint].

## Terminology discipline

Plasmid persistence has threshold-like behaviour, and the vocabulary of
dynamical systems is attractive for describing it. Most of that vocabulary
carries commitments that a persistence study rarely tests. This project uses
the following discipline.

| Term | What it commits you to | Use it when |
| --- | --- | --- |
| **threshold** | A value of a parameter above/below which the outcome differs. | Almost always safe. |
| **tipping point** | A small or gradual change in conditions produces a disproportionately large, abrupt and often hard-to-reverse change in state. | Only with evidence that the response is abrupt and disproportionate — not merely that the outcome differs across a threshold. |
| **bifurcation** | A qualitative change in the number or stability of equilibria of a specified dynamical system, as a named parameter crosses a value. | Only when you have the model, the parameter and the equilibria. |
| **bistability** | Two stable states coexist at the *same* parameter values; which one you are in depends on initial conditions. | Only with evidence that both states are stable under identical conditions. |
| **hysteresis** | Bistability *plus* path dependence: the forward and reverse transitions happen at different parameter values. | Only with evidence from a reversed sweep. |

**Threshold ≠ tipping point.** A threshold says the outcome differs on either
side of some value. A tipping point says the response is abrupt and
disproportionate to the change that triggered it, and usually hard to reverse.
Observing the first does not license claiming the second.

A caution about the mechanism, because it is easy to over-specify: tipping is
*not* defined by positive feedback. The dynamical-systems literature
distinguishes at least bifurcation-induced, noise-induced and rate-induced
tipping, and in the rate-induced case a system can tip because conditions
change too *fast*, even though the equilibrium it was tracking never loses
stability [@ashwin2012tipping]. So "there must be a self-reinforcing loop" is
one usage, not the definition. The practical consequence for this project is
unchanged: do not call a persistence threshold a tipping point without
evidence of an abrupt, disproportionate response, and do not assert a
particular mechanism you have not identified.

**Bifurcation ≠ bistability ≠ hysteresis.** A bifurcation is a statement about
a model's equilibrium structure; not every bifurcation produces bistability,
and bistability does not imply hysteresis has been shown. Each is a stronger
claim than the last, and each needs its own evidence.

**Preferred default wording.** Absent evidence for the stronger claims, say
**persistence boundary** for the parameter combination separating persistence
from loss, and **stability landscape** for the qualitative picture of which
states the system settles into. Both are descriptive and commit you to nothing
you have not shown. Upgrade the wording when the evidence arrives, and say what
the evidence was.

---

**See also.** The three routes whose balance this page describes:
[`copy-carry-spread.md`](copy-carry-spread.md). Why cost exists at all and
whom it is paid by: [`plasmid-vs-host-fitness.md`](plasmid-vs-host-fitness.md).
