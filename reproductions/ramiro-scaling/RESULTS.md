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

The lower slopes differ (−0.68 against −0.88) and the PCN floor does **not**
explain it: the floor barely touches small plasmids, where that segment
lives. Multimapping treatment is a candidate — `pseuPIRA` incorporates
ambiguous reads where `CoverM` trims — but settling it needs accession-matched
comparison, which these data cannot provide.

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

## 5. The breakpoint is between families, not within them

§3 and §4 both treat the breakpoint as a threshold on plasmid size. The
caveat below used to say that a mixture of replicon families with different
characteristic copy numbers would produce the same segmented preference, and
that separating the two needed family-level annotation.

The annotation is in the file. `Predicted_ptu` is a plasmid taxonomic unit
— 139 of them — and a PTU is a replicon family. So the two hypotheses can be
told apart, because they differ in one place: **a real break is a
within-family phenomenon**, and a family spanning the threshold should kink.
A mixture is purely between-family, and removing the family means removes
it.

| fit | ΔAIC | slopes |
|---|---:|---|
| pooled, as in §3 | **−148.1** | −0.683 then −0.150 |
| family-centred | **−1.3** | −0.356 then −0.598 |

The preference disappears. The single-slope exponent moves with it, from
−0.620 pooled to **−0.399** once families are centred — so a third of the
headline exponent in §1 is also a between-family effect.

**This is absence, not blindness.** Centring removes most of the range in
the predictor: 95.3% of the variance in log relative size lies between
families, only 4.7% within, because families occupy narrow size bands. A
null result on 4.7% of the variance invites the obvious objection. So the
pooled break (a slope change of +0.533) was injected into the centred data
and the same test re-run:

| injected at | ΔAIC | |
|---|---:|---|
| 25th percentile | −45.2 | recovered |
| 50th percentile | −45.1 | recovered |
| 75th percentile | −33.6 | recovered |

A break of that size would have been seen at ΔAIC ≈ −45. The observed value
is −1.3.

Nine families have at least five records on each side of the fitted
breakpoint. Three prefer a kink, and the directions disagree — PTU-FS runs
+0.63 then −3.41, PTU-E5 −1.10 then +0.84, PTU-E64 −0.74 then +0.07. Only
PTU-FK (n = 227) resembles the pooled shape. A shared physical threshold
would not produce that scatter; small-sample hinge fitting does.

### What this means for §3 and §4

The arithmetic in §4 is untouched: median PCN really is 5.59 below the break
and 1.48 above, a 301-fold step in daughters born plasmid-free. What changes
is what the break *is*. Not a size at which an individual plasmid's
inheritance stops working, but the point where the **composition of families
changes over** — small-plasmid families carry high copy number, large-plasmid
families low, and each sits in its own narrow band.

The consequence for §3 is sharper, and it cuts against the most quotable
claim in this document. A breakpoint agreeing with Maddamsetti's to within
0.1 percentage points reads as independent confirmation of a physical
constant. If both datasets are assembled from similar family compositions —
and both are enterobacteria-dominated sequencing archives — then the
agreement may be reporting a shared taxonomic makeup rather than a shared
threshold. Distinguishing those needs the family composition of
Maddamsetti's sample, which is not in these data.

## What this does not establish

- Nothing about Fig. 5A, which uses a different and larger dataset.
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
