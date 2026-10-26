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
| **tipping point** | A threshold *plus* self-reinforcing change past it — the system keeps moving on its own. | Only with evidence of positive feedback driving the transition. |
| **bifurcation** | A qualitative change in the number or stability of equilibria of a specified dynamical system, as a named parameter crosses a value. | Only when you have the model, the parameter and the equilibria. |
| **bistability** | Two stable states coexist at the *same* parameter values; which one you are in depends on initial conditions. | Only with evidence that both states are stable under identical conditions. |
| **hysteresis** | Bistability *plus* path dependence: the forward and reverse transitions happen at different parameter values. | Only with evidence from a reversed sweep. |

**Threshold ≠ tipping point.** A threshold says the outcome changes. A tipping
point says the change becomes self-sustaining. Observing the first does not
license claiming the second.

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
