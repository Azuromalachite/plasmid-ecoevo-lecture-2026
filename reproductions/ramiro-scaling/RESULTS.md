# Ramiro-Martinez (2025): what the curated dataset says

Run [`reproduce.py`](reproduce.py) to regenerate every number below;
[`receipt.json`](receipt.json) records the run.

| | |
|---|---|
| **Source** | `PaulaRamiro/NpAUREO`, `Model/curateddataset.csv`, SHA-256 `23bee155…f78f`, 3,961 records |
| **Analysis** | ours, applied to their data — PTU-level medians, OLS, inverse-variance pooling, a continuous two-segment fit |
| **Execution** | `COMPLETED` |
| **Scope** | **not** a reproduction of published Fig. 5A. This is the curated *modelling* subset the authors ship for their ML model, not the 6,327-plasmid figure set. The two differ, visibly: Klebsiella is −0.559 here against roughly −0.63 in the paper. |

---

## 1. The nine genera cannot be told apart

| genus | PTUs | records | slope | ± se | R² |
|---|---:|---:|---:|---:|---:|
| Escherichia | 57 | 1613 | −0.645 | 0.026 | 0.916 |
| Klebsiella | 59 | 1060 | −0.559 | 0.052 | 0.672 |
| Salmonella | 35 | 282 | −0.692 | 0.052 | 0.842 |
| Staphylococcus | 15 | 282 | −0.796 | 0.116 | 0.785 |
| Enterococcus | 12 | 243 | −0.677 | 0.105 | 0.806 |
| Enterobacter | 33 | 193 | −0.667 | 0.062 | 0.790 |
| Acinetobacter | 9 | 157 | −0.689 | 0.126 | 0.811 |
| Bacillus | 20 | 123 | −0.529 | 0.111 | 0.555 |
| Pseudomonas | 3 | 8 | −0.569 | 0.133 | 0.948 |

Inverse-variance pooled: **−0.643 ± 0.019** (95% CI −0.680 to −0.606).
Heterogeneity **Q = 7.06 on 8 df, I² = 0%** — Q *below* its degrees of
freedom, so there is less spread between genera than chance alone predicts.
Not one genus slope falls outside the pooled interval, and the two extremes
(Staphylococcus −0.796, Bacillus −0.529) are 1.66 standard errors apart.

A per-genus panel without error bars invites "different taxa scale
differently". These data do not support that. They support something
stronger and more surprising: one exponent near −0.64 across Escherichia,
Bacillus and Staphylococcus alike.

Two cautions. Pseudomonas has **3 PTUs and 8 records** — its R² of 0.948 is
the highest in the table and the least informative, because three points fit
a line almost regardless. And the sample is not broad: Escherichia and
Klebsiella alone are 67.5% of records, the four Enterobacteriaceae 79.5%. The
pooled value is mostly an *E. coli* and *Klebsiella* number wearing nine
labels.

## 2. The PCN floor is a truncation, not a filter

The authors excluded plasmids with PCN below 1, and the data show it —
minimum PCN is exactly 1.000, with zero records beneath. Raising that floor
further flattens the exponent monotonically and collapses the fit:

| floor | kept | slope | R² |
|---:|---:|---:|---:|
| 1 (theirs) | 3961 | −0.608 | 0.663 |
| 1.5 | 2999 | −0.577 | 0.621 |
| 2 | 2355 | −0.539 | 0.527 |
| 3 | 1789 | −0.459 | 0.344 |
| 5 | 1427 | −0.359 | 0.184 |
| 10 | 988 | −0.196 | 0.053 |

So the published exponent is conditional on where the cut sits. And the cut
is not evenly distributed: **80.9%** of plasmids above the breakpoint in §3
have PCN below 2, against 22.0% below it. The exclusion removes the
large-plasmid arm almost exclusively — which is the regime Maddamsetti et al.
describe as a plateau and where their retained 20.7% with PCN below 1 live.

This dataset therefore cannot see the phenomenon the other study reports, and
the two exponents should not be compared as though they estimated the same
quantity on the same support.

## 3. The breakpoint replicates on a second dataset

Putting these data on Maddamsetti's chromosome-normalised axis:

| | Maddamsetti et al. (2025) | this dataset |
|---|---|---|
| breakpoint | 1.84% of chromosome | **1.73%** |
| slope below | −0.880 | −0.683 |
| slope above | −0.125 | −0.152 |
| model preference | segmented | **ΔAIC = −148.1**, segmented |

Different sample, different coverage estimator, different filters — and the
breakpoint lands within 0.1 percentage points. The upper slope agrees
closely. **The authors' own data prefer the segmented model by a wide margin,
and their paper fits a single power law.**

The lower slopes differ, −0.683 here against −0.880 there. An earlier
version of this section argued that the PCN floor could not explain the gap,
because the floor barely touches small plasmids, where that segment lives.
That was an argument from the shape of *our* data, and it is wrong.

Maddamsetti's Supplementary Data 1 is downloadable (§6) and keeps the
plasmids below one copy that this subset excludes, so the floor can simply be
applied to their file:

| subset | n | bend | slope below | slope above |
|---|---:|---:|---:|---:|
| theirs, all plasmids | 12,006 | 1.84% | −0.879 | −0.125 |
| **theirs, PCN ≥ 1 (our floor)** | 9,519 | **1.68%** | **−0.796** | **−0.143** |
| ours, PCN ≥ 1 | 3,961 | 1.73% | −0.683 | −0.150 |

The floor closes **about 42%** of the lower-slope gap and moves the bend and
the upper slope toward ours as well. It does not close all of it, so
something else — multimapping treatment is still a candidate, since `pseuPIRA`
incorporates ambiguous reads where `CoverM` trims — accounts for the rest. But
the first-order answer is the filter, not the estimator.

This also deflates the agreement in the table above. Under a common floor
their bend sits at 1.68% and ours at 1.73%, which is closer than the headline
comparison; under no floor theirs is 1.84%. The two numbers being a tenth of
a point apart was partly a coincidence of differing exclusions.

**Read §5 before citing this section.** The breakpoint is real in the pooled
data and it does land where Maddamsetti's does. It is not, however, a
threshold that individual plasmids cross, and that changes what the
agreement between two datasets is evidence for.

## 4. What the threshold costs, in inheritance

Computed through [`battle_royale.segregation`](../../models/copy-number-burden/battle_royale/segregation.py)
so the two stay consistent:

| | median PCN | daughters born plasmid-free |
|---|---:|---:|
| below the breakpoint (n = 2713) | 5.59 | **0.043%** |
| above it (n = 1248) | 1.48 | **12.93%** |

A **301-fold** step. 1.8% of a 5 Mb chromosome is roughly 90 kb — about the
size of the F plasmid. Below that, copy number alone makes random segregation
safe: four daughters in ten thousand. Above it, one in eight is born without
the plasmid, which no lineage survives.

So the breakpoint is plausibly the size at which **numbers stop working and
machinery has to take over** — and that is the same threshold Effe et al.
(2025) approach from the mechanistic side, taking a 43-generation half-life
to 549 with ParAB plus a toxin-antitoxin system.

This is a hypothesis the coincidence suggests, not a result these data
establish. Replicon family annotation turned out to be present already, and
§5 uses it; maintenance-gene annotation is still absent, and the mechanistic
half of the hypothesis still rests on it. What §5 changes is the level the
threshold would have to act on: families over evolutionary time, not
plasmids along a size gradient.
See [`../../concepts/random-segregation-is-not-a-floor.md`](../../concepts/random-segregation-is-not-a-floor.md).

## 5. Most of the breakpoint is between families — but not all of it

§3 and §4 both treat the breakpoint as a threshold on plasmid size. The
caveat below used to say that a mixture of replicon families with different
characteristic copy numbers would produce the same segmented preference, and
that separating the two needed family-level annotation.

The annotation is in the file. `Predicted_ptu` is a plasmid taxonomic unit,
139 of them. A PTU is **not** the same thing as a replicon family — the two
are correlated classifications built from different information, and the
authors assign replicon types to far more plasmids than they assign named
PTUs. A PTU is the nearest thing to a plasmid species, which is what this
test needs.

The two hypotheses differ in one place: **a real break is a within-family
phenomenon**, and a family spanning the threshold should kink. A mixture is
purely between-family.

| fit | ΔAIC | slopes |
|---|---:|---|
| pooled, as in §3 | **−148.1** | −0.683 then −0.150 |
| **knee held at 1.73%, PTU as a fixed effect** | **−19.4** | **−0.499 then −0.119** |
| family-centred, knee rescanned | −1.3 | −0.356 then −0.598 |

**The second row is the one that answers the question, and an earlier version
of this section reported only the third.** Centring *x* and *y* within PTU and
then rescanning for a knee asks whether there is a kink anywhere in the
within-family relationship. It does not ask whether the kink at 1.73% of
chromosome length survives adjusting for family, because subtracting a
different mean from each family means a fixed plasmid size no longer maps to
one centred *x*. Holding the knee fixed and absorbing PTU intercepts — the
within-transform applied to *y*, *x* **and** the hinge term, which is the step
the rescan omits — gives ΔAIC −19.4, not −1.3.

Thirty-eight of the 116 families straddle the knee, holding 1,677 records, so
the hinge is identified within families rather than being an artefact of
collinearity.

The preference weakens by most of its magnitude and does not disappear. The single-slope exponent moves with it, from
−0.620 pooled to **−0.399** once families are centred — so a third of the
headline exponent in §1 is also a between-family effect.

The slope change falls from **+0.533** pooled to **+0.380** adjusted — about
a 29% reduction, against an 87% reduction in ΔAIC. And the adjusted model,
allowed to choose, puts its knee at **0.84%** of chromosome length rather than
1.73%, which is its own argument against treating either number as a
constant. Dropping the three most abundant lineages one at a time leaves
ΔAIC between −16.4 and −22.1, so the residual bend is not one lineage's
doing.

**On the rescanned test, the null is at least readable.** Centring removes
most of the range in the predictor: 95.3% of the variance in log relative
size lies between families, only 4.7% within. So the pooled break (a slope
change of +0.533) was injected into the centred data and the same test
re-run:

| injected at | ΔAIC | |
|---|---:|---|
| 25th percentile | −45.2 | recovered |
| 50th percentile | −45.1 | recovered |
| 75th percentile | −33.6 | recovered |

A break of that size would have been seen at ΔAIC ≈ −45. The rescanned value
is −1.3. That still says there is no second kink hiding inside families once
their means are gone; it is simply not the same statement as "the bend at
1.73% is entirely between families", which is what this section used to
claim.

**Sign convention.** ΔAIC here is AIC(segmented) − AIC(single line), so a
negative value favours the segmented model. The receipt records it under
`delta_aic_segmented_minus_single`, and the single line is fitted with two
parameters against the hinge's four.

**How nine families were arrived at.** The file holds 3,961 records across 139
PTU labels. 116 PTUs hold at least three records and supply the 3,930 used for
centring; 23 hold one or two, 15 of them singletons, and the median PTU holds
ten. Nine PTUs hold at least five records on **each** side of the fitted
breakpoint, and those nine hold 943 records — 23.8% of the file. The nine are
therefore the largest, best-sampled, mostly Enterobacterales-associated
lineages, not a sample of plasmid diversity.

The per-family test is weak where it matters most. Taking the thinner side of
each family: PTU-E64 has 6, PTU-E42 8, PTU-FK and PTU-FS 9 each, PTU-B/O/K/Z
and PTU-Bac45 11, PTU-I1 22, PTU-E5 38 and PTU-FE 101. A hinge fitted across a
side holding six points is nearly unconstrained, which is the likeliest reading
of the disagreeing directions below. Records within a PTU are also related by
descent, so they are not independent observations and the nominal AIC
comparison flatters itself.

Nine families have at least five records on each side of the fitted
breakpoint. Three prefer a kink, and the directions disagree — PTU-FS runs
+0.63 then −3.41, PTU-E5 −1.10 then +0.84, PTU-E64 −0.74 then +0.07. Only
PTU-FK (n = 227) resembles the pooled shape. A shared physical threshold
would not produce that scatter; small-sample hinge fitting does.

### What this means for §3 and §4

The arithmetic in §4 is untouched: median PCN really is 5.59 below the break
and 1.48 above, a 301-fold step in daughters born plasmid-free.

What changes is how much of the break is a property of plasmids and how much
of the catalogue. Most of it is composition — small-plasmid families carry
high copy number, large-plasmid families low, and each sits in its own narrow
band. A residual bend survives that adjustment, and these data do not
distinguish it from within-lineage curvature, PTU misclassification, the
PCN ≥ 1 truncation or sampling bias. It is not evidence of a replication-size
transition; it is a reason not to have closed the question.

The consequence for §3 is sharper, and it cuts against the most quotable
claim in this document. A breakpoint agreeing with Maddamsetti's to within
0.1 percentage points reads as independent confirmation of a physical
constant. If both datasets are assembled from similar family compositions —
and both are enterobacteria-dominated sequencing archives — then the
agreement may be reporting a shared taxonomic makeup rather than a shared
threshold. Distinguishing those needs the family composition of
Maddamsetti's sample, which is not in these data.

## 6. The comparator dataset, and how to get it

Maddamsetti's per-plasmid table is **Supplementary Data 1**, served by the
publisher at `static-content.springer.com`:

```
41467_2025_61205_MOESM3_ESM.csv     4,334,409 bytes
sha256 131faa58f5528d814877cca9ffa8c3e56b41e92518385d740c1b7e530f2bc3a7
16,861 replicons -> 12,006 plasmids, 22 columns
```

It carries `AnnotationAccession` and `SeqID`, so unlike the Ramiro modelling
subset it can be joined to external annotation. PMC serves the same file
behind a "Preparing to download" page that an automated request cannot pass;
the publisher's own host does not. [`explore.ipynb`](explore.ipynb) fetches
it, checks that hash, and reproduces their published figure from it: bend at
1.84%, slopes −0.879 and −0.125, against their published 1.84%, −0.880 and
−0.125.

The single power law on the same file gives −0.717, which is the −0.71
Shahzadi et al. (2026) report — they reuse these plasmids and these copy
numbers, so the two papers are not independent samples and their agreement
is not corroboration.

## What this does not establish

- Nothing about Fig. 5A, which uses a different and larger dataset.
- That these plasmids represent plasmids. Beyond the PCN floor in §2, the
  modelling subset carries further curation **which the authors document and
  this file does not show**: unassigned PTUs removed, redundant variables
  dropped, and copy numbers above 100 excluded. The file is consistent with
  all three — every one of the 3,961 records carries a named PTU where COPLA
  would write `-` or `PTU-?`, and the maximum PCN is 99.50 with nothing at or
  above 100. An earlier version of this list called the PTU filtering an
  undisclosed selection. That was wrong: it is disclosed in the paper, and
  only invisible in the CSV. It still runs toward well-sampled lineages, and
  it is still upstream of every number here.
- That the breakpoint is biological. This was listed here as untested; §5
  now tests it, and the mixture reading wins. What remains untested is
  whether the family-level pattern — small families with high copy number,
  large families with low — is itself selected or merely inherited from
  replicon architecture.
- That genera truly share an exponent. Q has modest power at nine groups;
  "no detected heterogeneity" is not proof of none.
- Any causal direction. Larger plasmids having lower copy number is a
  correlation in a sample assembled from sequencing archives, with whatever
  selection that implies about which plasmids get sequenced at all.
