# The breakpoint that wasn't

A scaling threshold that replicated another lab's number to within a tenth of
a percentage point turns out to be a fact about which plasmid families exist,
not about plasmids.

> **This file is the argument. [`RESULTS.md`](RESULTS.md) is the record.**
> Every number below comes from [`receipt.json`](receipt.json) and regenerates
> by running [`reproduce.py`](reproduce.py); where the two files disagree,
> `RESULTS.md` and the receipt win and this one is stale.
>
> A version of this report laid out as a page, with the tables as charts, is
> published separately; it carries the same claims and the same ledger.

---

## The question

Plasmid copy number falls as plasmid size rises. Fit that across a few
thousand plasmids and the data prefer a bent line to a straight one, with the
bend at **1.73%** of chromosome length. Maddamsetti et al. (2025), working
from a different sample with a different coverage estimator, put their bend at
**1.84%**. Two labs, two pipelines, one number.

That agreement was the most quotable thing in `RESULTS.md` §3, and it is what
this report is about. Plasmids come in families; families have characteristic
sizes; families have characteristic copy numbers. A bend can appear in pooled
data simply because the families change over along the size axis, with no
threshold anywhere. The dataset already carries family labels, so the two
explanations can be told apart.

## The test

A real threshold is a **within-family** phenomenon: a family spanning it
should bend. A composition effect is purely **between-family**: remove each
family's own mean and the bend leaves with it.

![Bar chart of delta AIC. Pooled, the two-segment fit beats a single line by
148.1. Centred on plasmid family it beats it by 1.3. Three breaks of the
pooled magnitude planted into the centred data are recovered by the same test
at 45.2, 45.1 and 33.6.](../../figures/output/breakpoint-is-between-families.svg)

| fit | ΔAIC | slope below | slope above |
|---|---:|---:|---:|
| Pooled, as published | **−148.1** | −0.683 | −0.150 |
| Family-centred | **−1.3** | −0.356 | −0.598 |

The preference collapses. The single-slope exponent moves with it, from −0.620
pooled to **−0.399** once families are centred, so roughly a third of the
headline exponent in §1 is also a between-family effect.

## Why the planted breaks matter more than the observed one

A null is only worth reading if the test could have returned something else.
Centring strips out most of the variation in plasmid size — **95.3%** of the
variance in log relative size lies between families, only **4.7%** within —
so the first objection is that the test went blind.

It did not. A break of the pooled magnitude (a slope change of +0.533) was
planted into the centred data at three positions and the identical test
re-run:

| planted at | ΔAIC | |
|---|---:|---|
| 25th percentile | −45.2 | recovered |
| 50th percentile | −45.1 | recovered |
| 75th percentile | −33.6 | recovered |

With 4.7% of the variance left, a bend that size still registers at about −45.
We observed −1.3.

## What the families say one at a time

Nine families carry at least five plasmids on each side of the fitted
breakpoint. Three prefer a bend, their directions disagree with each other,
and only `PTU-FK` resembles the pooled shape. A shared physical threshold
would not produce that scatter; small-sample hinge fitting does. The full
table is in [`RESULTS.md`](RESULTS.md) §5.

## Why families do this

A plasmid family is not a size range that happens to be populated. It is a
replication and maintenance architecture, and that architecture largely fixes
both how big the plasmid is and how many copies it keeps. Pool several hundred
families whose sizes barely overlap, and the pooled curve has to bend wherever
the families hand over. Nothing in that bend is a property of any individual
plasmid.

## What it costs the headline

The arithmetic in `RESULTS.md` §4 is untouched. Below the bend the median
plasmid carries 5.59 copies and binomial segregation alone loses 0.043% of
daughters; above it the median is 1.48 and the same model loses 12.93%. That
301-fold step is why the bend looked mechanical: it sits almost exactly where
random inheritance stops being survivable.

It is still a boundary between kinds of plasmid rather than a point an
individual plasmid crosses as it grows. If the threshold means anything
biologically, it acts on families over evolutionary time — which families
exist, and which persist — not on a plasmid working its way up a size
gradient.

That reframes the agreement with Maddamsetti. Two enterobacteria-dominated
sequencing archives plausibly share a family composition. Two numbers agreeing
because the same families dominate both samples is a different claim from two
numbers agreeing because they measure the same constant, and only the second
would travel to a new sample.

**A number that replicates is not thereby a measurement of the same thing.**

## Claims ledger

| claim | status | the strongest version the evidence would not support |
|---|---|---|
| The segmented preference is between-family; centring takes ΔAIC from −148.1 to −1.3, and a planted break of the same size is recovered at −45 | supported | That no size threshold exists in plasmid biology. Scope is this dataset and these predicted families. |
| 95.3% of the variance in log relative size is between families | supported | That families are biologically discrete. It is a decomposition on predicted labels. |
| The PCN < 1 exclusion is a one-sided truncation that flattens the exponent monotonically | supported | That the authors' published exponent is wrong. It is conditional on a cut they stated. |
| 1.73% and 1.84% are two different measurements landing 0.1 points apart | narrowed | "The breakpoint replicates." Different sample, estimator and filters, and the finding above gives a reason they might agree without a shared threshold. |
| Median PCN 5.59 and 1.48 across the bend give 0.043% against 12.93% of daughters born plasmid-free | narrowed | That plasmid loss was measured. It is arithmetic on two medians of modelled point estimates, through a binomial model, with no interval available. |
| Nine genera share one scaling exponent | narrowed | The stated claim asserts the null. The data support "cannot be distinguished", restricted by the power of a nine-group test. |

## Methodology

The data are the curated modelling subset released by Ramiro-Martínez et al.
(2025) at `PaulaRamiro/NpAUREO`, file `Model/curateddataset.csv`, SHA-256
`23bee155…f78f`, 3,961 records, retrieved 6 November 2026 from the `main`
branch. `main` moves, and `reproduce.py` checks the hash and says so when it
differs. This is **not** the 6,327-plasmid set behind the paper's Figure 5A;
the two give visibly different slopes, and nothing here reproduces a published
panel.

Copy number is **modelled, not counted** — a sequencing-coverage ratio — and
ships as a point estimate with no uncertainty. No claim above turns on a
difference whose size could be swamped by an interval we cannot see. Plasmid
taxonomic unit and mobility are likewise the authors' predictions, as their
column names state. Noisy family assignment blurs families together and
*weakens* the between-family signal, so misassignment works against the
central finding rather than manufacturing it.

The analysis is ours, not the authors': per-genus slopes on PTU-level medians,
inverse-variance pooling with Cochran's Q, a continuous two-segment fit on
chromosome-normalised size, and a variance decomposition by predicted PTU.
Grouping is by PTU alone rather than by genus and PTU together, since a PTU is
already a plasmid taxonomic unit.

Every plasmid here was sequenced, assembled and binned, and copy number
affects all three. Whether the family-level pattern is itself selected, or
inherited from replicon architecture, these data cannot say.

## Figure

[`figures/source/breakpoint_is_between_families.py`](../../figures/source/breakpoint_is_between_families.py)
reads `receipt.json` at build time rather than holding its own copy of any
number, refuses to draw if the receipt records a run against an unexpected
input, and asserts its three series colours clear `palette.py`'s separability
threshold before writing anything.
