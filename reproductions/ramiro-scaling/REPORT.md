# Mostly the catalogue, not the plasmids

A scaling threshold that replicated another lab's number to within a tenth of
a percentage point turns out to be *mostly* a fact about which plasmid
families exist. Mostly, not entirely — and an earlier version of this report
said entirely, on a test that could not have shown otherwise.

> **Correction, 6 November 2026.** This report first claimed the breakpoint
> was a between-family effect and nothing more. The test behind that claim
> centred plasmid size within each family and then searched for a *new* bend,
> which is a different question. Holding the bend where the pooled fit put it
> and absorbing family intercepts leaves ΔAIC −19.4, not −1.3. Most of the
> signal is composition; a weaker bend survives. The claims ledger and
> §5 of `RESULTS.md` carry the corrected numbers.

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
| **Bend held at 1.73%, family as a fixed effect** | **−19.4** | **−0.499** | **−0.119** |
| Family-centred, bend re-fitted | −1.3 | −0.356 | −0.598 |

ΔAIC is AIC(segmented) − AIC(single line), so negative favours the bend.

The middle row is the test that answers the question. Centring size within
each family moves the 1.73% mark to a different coordinate for every family,
so re-fitting a bend afterwards asks whether *any* kink hides inside
families — a reasonable question, answered no, and not the one the headline
was making. Holding the bend fixed and absorbing one intercept per family
keeps the mark where it was. Thirty-eight of the 116 families straddle it,
holding 1,677 plasmids, so the test has something to work with.

The slope change falls from **+0.533** pooled to **+0.380** adjusted. ΔAIC
falls by 87%. Neither reaches zero.

The single-slope exponent moves too, from −0.620 pooled to **−0.399** once
families are absorbed, so roughly a third of the headline exponent is also a
between-family effect.

Two further things the adjusted model says. Allowed to choose its own bend,
it puts it at **0.84%** of chromosome length, not 1.73% — an argument against
treating either number as a constant. And dropping the three most abundant
lineages one at a time leaves ΔAIC between −16.4 and −22.1, so what survives
is not one lineage's doing.

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

Those nine are not a sample of plasmid diversity, and the arithmetic says so:

| step | PTUs | records |
|---|---:|---:|
| in the file | 139 | 3,961 |
| holding ≥ 3 records, used for centring | 116 | 3,930 |
| holding ≥ 5 records **each side** of the break | **9** | **943** |

The thinner side of each of the nine holds between 6 and 101 records — six for
PTU-E64, nine for PTU-FK and PTU-FS. A hinge fitted across six points is
nearly unconstrained, and plasmids within a PTU are related by descent rather
than independent, so the nominal comparison flatters itself in both
directions. The disagreement among those three bends is better read as
small-sample noise than as nine lineages behaving differently.

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

And a test that cannot return the other answer is not thereby evidence.

## Claims ledger

| claim | status | the strongest version the evidence would not support |
|---|---|---|
| Most of the segmented preference is between-family: holding the bend at 1.73% and absorbing family intercepts takes ΔAIC from −148.1 to −19.4 | supported | That the bend is *entirely* between families. An earlier version of this report claimed that, on a test that re-fitted the bend in centred coordinates and so could not have shown otherwise. |
| No second bend hides inside families once their means are removed: ΔAIC −1.3, where a planted break of the pooled size is recovered at −45 | supported | That the bend at 1.73% disappears under adjustment. It does not; this is a different question. |
| The residual bend is evidence of a replication-size transition | **not supported** | These data cannot separate it from within-lineage curvature, PTU misclassification, the PCN ≥ 1 truncation or sampling bias. The adjusted model prefers a bend at 0.84%. |
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

The modelling subset is curated further than the PCN floor, in ways the
authors document and the file does not show: unassigned PTUs removed,
redundant variables dropped, copy numbers above 100 excluded. The file is
consistent with all three — every record carries a named PTU where COPLA
would write `-` or `PTU-?`, and the maximum PCN is 99.50 with nothing at or
above 100. An earlier version of this report called the PTU filtering an
undisclosed selection; that was wrong, and this is the correction. It is
disclosed in the paper and merely invisible in the CSV. It still runs toward
well-sampled lineages.

A PTU is also **not** a replicon family, and an earlier version of this
report said it was. They are correlated classifications built from different
information — whole-plasmid relatedness against replication machinery — and
the authors assign replicon types to far more plasmids than named PTUs.
Shared PTU is not proof of shared replication control.

The file carries **no accession, assembly or strain identifier**: ten
columns, none of which names a record. So nothing in *this CSV* can be joined
to PTU membership tables, replicon typing or any external annotation. That is
a limit of the modelling subset, not of the authors' release: their
repository ships seven supplementary datasets, and whether every modelling
record can be recovered from them is an open question and the obvious next
check.

Every plasmid here was sequenced, assembled and binned, and copy number
affects all three. Whether the family-level pattern is itself selected, or
inherited from replicon architecture, these data cannot say.

## Figure

[`figures/source/breakpoint_is_between_families.py`](../../figures/source/breakpoint_is_between_families.py)
reads `receipt.json` at build time rather than holding its own copy of any
number, refuses to draw if the receipt records a run against an unexpected
input, and asserts its three series colours clear `palette.py`'s separability
threshold before writing anything.
