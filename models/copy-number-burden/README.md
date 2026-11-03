# Copy number and host burden — the Battle Royale model

**Stable ID:** `model.copy-number-burden.battle-royale`

Stable IDs are persistent and are not reused. Repository paths may change
without changing identity: if this directory moves, the ID does not.

The model: [`battle-royale.ipynb`](battle-royale.ipynb).

---

## What question does it answer?

**If twenty plasmid-bearing lineages compete in one flask, does raising copy
number help the plasmid, and under what conditions does it stop helping?**

Copy number raises gene dosage and raises burden at the same time. Those two
effects run in opposite directions, and which wins depends on how much growth
opportunity the culture has left, what the competitors are doing, and what is
being counted at the end. The notebook makes that trade-off executable: you
can turn the dial and watch the optimum move.

It is the computational companion to
[`more copies is not always better`](../../misconceptions/more-copy-is-always-better.md),
which argues the same point in prose. The page says copy number is a
trade-off variable rather than a performance dial; this model is where a
reader can turn the dial.

## What is measured or literature-anchored?

One input is calibrated. Everything else is chosen, assumed, or explored.

**The per-copy burden coefficient** comes from Rouches et al.
[@rouches2022tunable], who fit

> cost = *a* · *b* · *x* + *b*

where *x* is plasmid copy number, **a = 0.065% ± 0.006%** and
**b = 0.019 min⁻¹ ± 0.003 min⁻¹**, across **830 priming-promoter pUC19
variants** that are *"all with nearly identical origins of replications"*.

The coefficient is quoted here with its parameterisation rather than alone,
because alone it is not usable:

- ***a* is dimensionless.** *x* is a copy count and *b* carries min⁻¹, so *a*
  is a fraction — "0.065% per copy" is a fraction **of *b***, not an absolute
  rate.
- ***b* is never defined in words in the paper.** Its value and units are
  given; what it represents is not. No absolute per-copy rate appears in this
  model, because its baseline cannot be recovered from the source.
- **The authors interpret *a*** as the fraction of cellular growth resources
  one copy consumes, comparing 0.065% with pUC19's 0.058% of the *E. coli*
  genome length. That reading is theirs, and it is what gives the fraction
  meaning on its own.
- **The linear form is hedged by its authors**, who write that it only
  *"largely"* agrees with their data.

The paper's abstract gives 0.063% and its Results and Fig. 4E give
0.065% ± 0.006%; the model uses the Results value, which is the one
attributed to a specific figure. The fit population is the 830-variant
priming-promoter sub-library, not the full 1,194-variant library.

The *"nearly identical origins"* phrase is a scope condition, not decoration:
holding the origin near-constant while copy number varies is what makes this
a copy-number effect rather than an origin effect — and it is also what
bounds transfer to other origins.

**Used as reference points, not refitted:** single-cell copy-number
distributions [@shao2021singlecell; @jahn2016copynumber]; total exogenous DNA
as a burden axis [@akeno2014reducedgenome]; ColE1 host metabolism at low and
high copy number [@wang2006cole1]; growth-rate-dependent copy-number control
[@klumpp2011growthrate]; batch physiology in LB [@sezonov2007lb].

## What is assumed?

The twenty-lineage Arena is a **declared synthetic scenario**. Competitor
copy numbers, cargo parameters and plasmid architectures are invented for the
model and are **not** inferred from participant materials. Also chosen rather
than measured: equal inoculation at *f*ᵢ(0) = 0.05, a 19-member PCN-100
reference pool, *K*/*N*₀, and culture duration.

Beyond those, four mechanisms are **exploratory** — hypothesis generators,
not calibrated relationships: linear transfer of the burden coefficient along
plasmid length, saturating cargo burden, dynamic copy-number feedback, and
PCN-dependent loss.

## What are the model layers?

Each layer answers a different question and carries a different evidential
weight. Reading a result without knowing its layer is the main way to misuse
this notebook.

| Layer | What it does | Evidence status |
| --- | --- | --- |
| Analytic fixed-PCN | Closed-form intuition and exact checks | Calibrated coefficient inside a declared scenario |
| Shared-resource batch | Competition for one carrying capacity, with plasmid loss | Declared scenario |
| Length / cargo extension | Separates DNA amount from cargo expression burden | Exploratory |
| Dynamic PCN | Substrate depletion with copy-number–growth feedback | Exploratory |
| Single-cell | Stochastic copy control and partitioning | Exploratory, with distributions anchored to [@shao2021singlecell] |

## What must *not* be inferred from its outputs?

- **The actual distribution of participant designs.** The competitor pool is
  invented. Nothing here is evidence about what anyone submitted.
- **A BL21(DE3)-specific winning copy number.** The coefficient is fitted in
  one strain background on pUC19-length plasmids with near-identical origins.
- **The competition winner.** Every optimum is a scenario calculation.
- **An exact mapping from simulated plasmid abundance to barcode read count.**
  The notebook deliberately declines to promote either candidate proxy to the
  scoring observable, because library-input normalisation is not specified.
- **That burden is linear in copy number.** The authors of the source hedge
  this, and the model inherits the hedge.

## Quality assurance — what was and was not validated

Stating which is more useful than "tests passed", because a passing test says
nothing about what it was capable of catching.

**Validated:**

- the numerical implementation agrees with the analytic model in a low-noise
  regime, at a 5% tolerance chosen to catch divergences a 20% tolerance
  missed;
- deterministic and stochastic paths agree where they should, and are
  checked separately in two regimes rather than averaged into one;
- results are invariant to the plotting grid, which removes a software
  artefact where a prediction changed when the analyst changed the grid;
- invalid copy numbers, invalid mechanistic states, and burden-domain
  violations are rejected rather than silently computed;
- the PCN-dependent loss model recovers the constant-loss model at zero
  exponent.

**Not validated:**

- **empirical applicability to BL21(DE3)** — no measurement in this host
  background was made or reproduced here;
- **realism of the synthetic competitor distribution** — it is declared, and
  no claim is made that real designs resemble it;
- **the exploratory mechanisms** — length transfer, cargo saturation, dynamic
  feedback and single-cell noise are structurally reasonable and not
  independently tested;
- **the mapping to barcode read counts**, for the reason above.

A direction for later rounds, not yet implemented: every important validation
should state the defect it is capable of catching, and ideally carry a
deliberately constructed mutation that makes it fail. A test whose domain of
sensitivity is not legible can pass for the wrong reason.

## Is the optimum reachable? — the question the model kept deferring

[`check_feasible_optimum.py`](check_feasible_optimum.py) answers it, and the
answer is not the one the question implies.

The analytic layer gives an interior optimum at

```text
C* = 1 / (beta · G0 · ln 2)
```

**That there is an optimum is not a result.** For any positive `beta` and `G0`,
a linear-in-C exponent times a linear prefactor has a stationary point, and it
is always a maximum. The script confirms this symbolically — including the
second derivative, so "stationary point" is not doing quiet work for
"maximum". The only empirical content is *where* `C*` sits relative to what a
real vector can reach.

Using the authors' own reading of the fitted coefficient — 0.065% of growth
resources per copy — and sweeping generation count, because the competition's
culture duration is not public and must not be invented:

| G0 (doublings) | 5 | 10 | 20 | 30 | 50 | 100 |
| --- | --- | --- | --- | --- | --- | --- |
| C* (copies/cell) | 444 | 222 | 111 | 74 | 44 | 22 |

Against declared reference ranges for common origin classes — **not** claims
about any construct in the competition:

| Origin class | At G0 = 10–30 |
| --- | --- |
| low-copy, p15A-like (10–15) | `C*` **above** the ceiling → raise copy number |
| medium, pBR322/pET-like (20–40) | `C*` **above** the ceiling → raise copy number |
| high-copy, pUC-like (300–500) | `C*` **below** the floor → lower copy number |
| tunable, wide range (5–500) | interior — a real trade-off |

**For the two commonest fixed-origin classes there is no trade-off at
realistic batch durations, and they are told to move in opposite
directions.** Only a vector whose reachable range straddles `C*` faces the
compromise the model is usually quoted for. Across the swept grid, 9 of 28
cells have an interior optimum.

> **Grid count, not frequency.** The four reference ranges and seven generation
> counts are deliberately chosen probes of parameter space, not a sample from
> any population of plasmids. "9 of 28" is not "about a third of cases" and
> carries no claim about how often real plasmids face this trade-off. The
> number has exactly the shape of a statistic that later loses its denominator,
> which is why the script prints the caveat beside it.

The boundary is solved rather than sampled:

```text
C* ≤ C_min   ⟺   G0 ≥ 1 / (beta · C_min · ln 2)     floor wins
C* ≥ C_max   ⟺   G0 ≤ 1 / (beta · C_max · ln 2)     ceiling wins
```

so whether the trade-off exists is a property of **how long the culture runs**,
not of the plasmid.

This also locates the 1 − 1/e invariant correctly. The density penalty at `C*`
against the lowest feasible copy number approaches 63% only as `C_min` → 0; in
the swept wide-range class it runs 54–63%, and in the medium class, where an
interior optimum appears only at G0 = 100, it is 9%. The invariant is the
zero-floor limit of a quantity that is otherwise much smaller — which is why it
must not be quoted as a fixed cost.

**Not settled by this script:** that burden is linear in copy number (the
source hedges it), that the coefficient transfers off pUC19-length plasmids
with near-identical origins, or that retention is independent of copy number.
Each would move `C*`, and the first would change the shape of the argument
rather than its value.

## Running it

Open [`battle-royale.ipynb`](battle-royale.ipynb) in Jupyter or Colab and run
top to bottom. It needs **NumPy ≥ 2.0**, SciPy, pandas and Matplotlib.

The feasibility check is separate and needs only SymPy:

```bash
uv run --no-project --with sympy python models/copy-number-burden/check_feasible_optimum.py
```

The NumPy floor is not cosmetic: two cells integrate with `np.trapezoid`, which
was added in NumPy 2.0 and is spelled `np.trapz` in 1.x. On a 1.x kernel —
which a hosted notebook may still be running — the failure used to surface as
an `AttributeError` midway through the shared-flask section, thirty cells
before the assertion that names the requirement. That assertion now lives in
the configuration cell, so the environment is checked before anything depends
on it.

Outputs are stripped in version control and `SAVE_FIGURES` defaults to
`False`, so running it does not write files into the repository. Notebook
figures are **exploratory**. A figure promoted into the educational material
becomes a separate hardened artifact under [`figures/`](../../figures/),
which is built from a committed script and rebuilds byte-identically — a
guarantee this notebook's plots do not meet and are not intended to meet.

## References

Held centrally in
[`evidence/references.bib`](../../evidence/references.bib) and cited by key.
Every entry has a DOI that resolves, with the full record checked field by
field.
