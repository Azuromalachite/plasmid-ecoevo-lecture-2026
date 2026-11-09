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


## 0. What the host pays for, and the baseline that gives the slope a meaning

Every fit below regresses copy number on relative plasmid size and reports
a slope. A slope of -0.62 is a number until there is something to compare
it against, and the comparison that matters is not zero.

A cell replicates, and pays for, **length x copy number** -- total plasmid
DNA. Two plasmids make the point: 3 kb at 500 copies is 1.5 Mb; 30 kb at
10 copies is 0.3 Mb. Five times the load from a plasmid ten times shorter.

That supplies the null:

    load = size x copy number,  so  PCN ~ size^b  =>  load ~ size^(1+b)

| copy-number slope | implied load slope | meaning |
|---|---|---|
| **-1** | **0** | copy number cancels size exactly; every plasmid costs the same |
| steeper than -1 | negative | bigger plasmids would cost less |
| shallower than -1 | positive | bigger plasmids cost more; compensation is partial |

**Nothing in this dataset is near -1.**

| | PCN slope | load slope | share of each size increase paid off |
|---|---:|---:|---:|
| pooled | -0.620 | +0.380 | 62% |
| below 1.73% of chromosome | -0.683 | +0.317 | 68% |
| above 1.73% | -0.149 | +0.851 | 15% |

The same thing without fitting anything, by size decile: median copy number
falls 15-fold across the range while median plasmid DNA per cell still
rises 7.1-fold, from 0.04 Mb to 0.31 Mb. Thirteen plasmids (0.3%) carry
over 1 Mb of plasmid DNA per cell; the largest load is 4.2 Mb, 84% of a
median chromosome in this file.

So the interpretable statement is **compensation is partial, and it weakens
as plasmids get bigger** -- about seven tenths of each size increase is
paid off at the small end and about one seventh at the large end. That does
not depend on there being a knee, or on where one sits, which is why it
survives everything in sections 9 and 14.

### The bent load fit is not a second result

Fitting a segmented model to load and quoting its dAIC alongside the
copy-number one would be counting the same result twice. In relative units
`log(load) = log(size) + log(copies)`, so the load regression is the
copy-number regression with 1 added to one coefficient and the hinge term
untouched: identical residuals (largest difference 1.5e-15), identical
knee, identical dAIC of -148.1. `dna_load.py` asserts this rather than
asserting it in prose.

Absolute load in base pairs *is* a different fit, because chromosome length
varies and the reparametrisation is no longer exact -- and its knee lands
at **0.70%** against 1.73% for copy number, a factor of 2.5 apart. Two ways
of writing down the same burden put the breakpoint in different places,
both inside the [0.41%, 2.05%] interval of section 9. One more reason not
to read a location off it.

Reproduced by `dna_load.py`.

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
| model preference | segmented | **ΔAIC = −148.1**, segmented (see §9: against a no-bend null a *searched* ΔAIC of this size has empirical p = 0.008 to 0.052, and a cubic at the same parameter count fits better) |

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
establish. Replicon PTU annotation turned out to be present already, and
§5 uses it; maintenance-gene annotation is still absent, and the mechanistic
half of the hypothesis still rests on it. What §5 changes is the level the
threshold would have to act on: PTUs over evolutionary time, not
plasmids along a size gradient.
See [`../../concepts/random-segregation-is-not-a-floor.md`](../../concepts/random-segregation-is-not-a-floor.md).

## 5. Most of the bend survives its PTUs

§3 and §4 both treat the breakpoint as a threshold on plasmid size. The
caveat below used to say that a mixture of replicon families with different
characteristic copy numbers would produce the same segmented preference, and
that separating the two needed PTU-level annotation.

The annotation is in the file. `Predicted_ptu` is a plasmid taxonomic unit,
139 of them. A PTU is **not** the same thing as a replicon family — the two
are correlated classifications built from different information, and the
authors assign replicon types to far more plasmids than they assign named
PTUs. A PTU is the nearest thing to a plasmid species, which is what this
test needs.

The two hypotheses differ in one place: **a real break is a within-PTU
phenomenon**, and a PTU spanning the threshold should kink. A mixture is
purely between-PTU.

| fit | ΔAIC | slopes |
|---|---:|---|
| pooled, as in §3 | **−148.1** | −0.683 then −0.150 |
| **knee held at 1.73%, PTU as a fixed effect** | **−19.4** | **−0.499 then −0.119** |
| PTU-centred, knee rescanned | −1.3 | −0.356 then −0.598 |

**The second row is the one that answers the question, and an earlier version
of this section reported only the third.** Centring *x* and *y* within PTU and
then rescanning for a knee asks whether there is a kink anywhere in the
within-PTU relationship. It does not ask whether the kink at 1.73% of
chromosome length survives adjusting for PTU, because subtracting a
different mean from each PTU means a fixed plasmid size no longer maps to
one centred *x*. Holding the knee fixed and absorbing PTU intercepts — the
within-transform applied to *y*, *x* **and** the hinge term, which is the step
the rescan omits — gives ΔAIC −19.4, not −1.3.

Thirty-eight of the 116 PTUs straddle the knee, holding 1,677 records, so
the hinge is identified within PTUs rather than being an artefact of
collinearity.

The preference weakens by most of its magnitude and does not disappear. The single-slope exponent moves with it, from
−0.620 pooled to **−0.399** once PTUs are centred — so a third of the
headline exponent in §1 is also a between-PTU effect.

**Those two reductions are not the same quantity, and an earlier version of
this section leaned on the wrong one.** ΔAIC falls 87%, but ΔAIC is a
model-comparison statistic, not a share of anything: the adjusted fit also
is not a share of anything. An earlier version of this file explained the
drop by saying the adjusted fit "spends 116 parameters on intercepts". That
is wrong: both models in that comparison carry the same PTU intercepts, so
their penalties cancel exactly and the two differ by a single parameter
(`n_ptu + 3` against `n_ptu + 2`, `reproduce.py:403`). The drop is real, and
it is a drop in *evidence* for a hinge once between-PTU variation is removed
-- a different question from how large the hinge is. The quantity that measures the bend is the change in slope, and it
falls from **+0.533** to **+0.380** — a **29%** reduction. Roughly seven
tenths of the bend's magnitude survives adjusting for PTU.

So the honest summary is close to the opposite of what this section first
said. PTUs account for something like a third of the bend, not most of
it; what collapses under adjustment is the *evidence*, not the *effect*.

Two things still qualify it. Allowed to choose, the adjusted model puts its
knee at **0.84%** of chromosome length rather than 1.73%. And the residual
does not survive narrowing the data: restricted to *Escherichia* it is
**+0.6**, and with the PCN floor raised to three it is **−0.1**. Dropping
the three most abundant lineages one at a time leaves ΔAIC between −16.4
and −22.1, so what survives is at least not one lineage's doing.

**The rescanned test is uninformative, and an earlier version of this
section claimed the opposite.** It argued that a near-null rescan was an
absence rather than blindness, on the strength of breaks injected into the
centred data and recovered at ΔAIC ≈ −45. But those breaks were injected at
a common *centred* coordinate. A real shared threshold sits at a common
*original* size, which centring scatters across PTUs, so the controls
validated the detection of something no biological threshold would look
like.

`reproduce.py` now simulates data that genuinely has a shared threshold —
116 PTUs in narrow size bands, a true bend at the fitted knee — and runs
the rescan on it. The rescan returns a **positive** ΔAIC: it misses a bend
that is really there, where the fixed-effects test with the knee held at the
truth finds it. A near-null rescan therefore says nothing either way, and
the −1.3 below should be read as a test that cannot answer the question
rather than as an answer.

The injected-break figures are kept here only because they were published:

| injected at | ΔAIC | |
|---|---:|---|
| 25th percentile | −45.2 | recovered |
| 50th percentile | −45.1 | recovered |
| 75th percentile | −33.6 | recovered |

Those numbers are real and they mean less than they appear to. They show the
rescan can find a break placed where centring leaves it, not that it could
find a biological threshold.

**Sign convention.** ΔAIC here is AIC(segmented) − AIC(single line), so a
negative value favours the segmented model. The receipt records it under
`delta_aic_segmented_minus_single`, and the single line is fitted with two
parameters against the hinge's four.

**How nine PTUs were arrived at.** The file holds 3,961 records across 139
PTU labels. 116 PTUs hold at least three records and supply the 3,930 used for
centring; 23 hold one or two, 15 of them singletons, and the median PTU holds
ten. Nine PTUs hold at least five records on **each** side of the fitted
breakpoint, and those nine hold 943 records — 23.8% of the file. The nine are
therefore the largest, best-sampled, mostly Enterobacterales-associated
lineages, not a sample of plasmid diversity.

The per-PTU test is weak where it matters most. Taking the thinner side of
each PTU: PTU-E64 has 6, PTU-E42 8, PTU-FK and PTU-FS 9 each, PTU-B/O/K/Z
and PTU-Bac45 11, PTU-I1 22, PTU-E5 38 and PTU-FE 101. A hinge fitted across a
side holding six points is nearly unconstrained, which is the likeliest reading
of the disagreeing directions below. Records within a PTU are also related by
descent, so they are not independent observations and the nominal AIC
comparison flatters itself.

Nine PTUs have at least five records on each side of the fitted
breakpoint. Three prefer a kink, and **all three flatten**, in the same direction as the
pooled fit: PTU-FK +0.561, PTU-Bac45 +1.111, PTU-E64 +0.812, against a pooled
+0.533. An earlier version of this section said their directions disagreed
and cited PTU-FS and PTU-E5 as the evidence. Those two score −3.7 and −2.0
and are not among the three; the sentence compared the wrong PTUs. The
correction runs against the reading this document reaches, which is why it is
stated plainly: within the PTUs large enough to test it, the bend goes
the same way it goes in the pooled data.

### What this means for §3 and §4

The arithmetic in §4 is untouched: median PCN really is 5.59 below the break
and 1.48 above, a 301-fold step in daughters born plasmid-free.

What changes is how much of the break is a property of plasmids and how much
of the catalogue. Most of it is composition — small-plasmid PTUs carry
high copy number, large-plasmid PTUs low, and each sits in its own narrow
band. A residual bend survives that adjustment, and these data do not
distinguish it from within-lineage curvature, PTU misclassification, the
PCN ≥ 1 truncation or sampling bias. It is not evidence of a replication-size
transition; it is a reason not to have closed the question.

The consequence for §3 is sharper, and it cuts against the most quotable
claim in this document. A breakpoint agreeing with Maddamsetti's to within
0.1 percentage points reads as independent confirmation of a physical
constant. If both datasets are assembled from similar PTU compositions —
and both are enterobacteria-dominated sequencing archives — then the
agreement may be reporting a shared taxonomic makeup rather than a shared
threshold. Distinguishing those needs the PTU composition of
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

## 7. The two tails

> **Units correction, 7 November 2026.** `PIRASequencingCoverage` in the
> Maddamsetti supplement is **mapped reads per base**, not base depth: it
> equals `PIRAReadCount / replicon_length` exactly, for all 16,861 rows, to
> a relative error of 1.5e-10 (implied read length 1.0000). Earlier versions
> of this file read "0.6x" as base coverage and argued that the low tail was
> partly a measurement artefact. **That argument is withdrawn.** A value of
> 0.57 on a 111,773 bp plasmid is 63,279 mapped reads, and not one of the
> 2,487 sub-one-copy plasmids was called from fewer than 1,000 reads. The
> units cancel in the copy-number ratio, so no fitted result anywhere in
> this document changes -- only the interpretation of measurement quality.
> Checked by `coverage_units.py`.


Maddamsetti's file keeps the plasmids below one copy that this subset
excludes, and carries the coverage each estimate came from, so it is the one
that can say what lives at the extremes. The two tails are nothing like each
other.

| | top 1% (n = 121, >= 132 copies) | below one copy (n = 2,487) |
|---|---|---|
| median length | 2,505 bp | 111,773 bp |
| median % of chromosome | 0.056% | 2.566% |
| median mapped read count | 269,374 | 63,279 |
| called from under 1,000 reads | 0 | 0 |
| enriched genera | *Salmonella* 3.7x | *Agrobacterium* **25x**, *Paracoccus* 6.0x, *Pantoea* 5.6x, *Rhizobium* 5.1x |

**The extreme top of the high tail is a library artefact.** A reader asked
whether the two top rows, both *Chlamydia psittaci* at 7,553 bp, were one
record entered twice. They are not -- different accessions, different
assemblies, **both from horses**, one from fetal tissue and one from
placental tissue. (An earlier version of this file said parrot; the parrot
is a different, low-copy row in the same table.) No plasmid accession
appears twice anywhere in the file.

An earlier version also ran all eight rows together as one plasmid. They are
**three species**, so the comparison to make is within *C. psittaci*:

| accession | species | copies | reads/base | chr reads/base | isolate |
|---|---|---:|---:|---:|---|
| `NZ_CP110212.1` | *C. psittaci* | 1.7 | 29.9 | 17.54 | Amazon parrot, faeces |
| `NZ_CP047320.1` | *C. psittaci* | 4.0 | 4.0 | 0.99 | goat |
| `NZ_CP092198.1` | *C. psittaci* | **2,268** | **4,721.6** | 2.08 | horse, placental tissue |
| `NZ_CP092200.1` | *C. psittaci* | **2,423** | **4,615.4** | 1.90 | horse, fetal tissue |
| `NZ_OU508368.1` | *C. abortus* | 3.9 | 5.5 | 1.44 | magpie, cloacal swab |
| `NZ_CP018053.1` | *C. trachomatis* | 7.9 | 7.3 | 0.92 | human |
| `NZ_CP015297.1` | *C. trachomatis* | 14.5 | 33.2 | 2.29 | human |
| `NZ_CP015299.1` | *C. trachomatis* | 30.0 | 46.2 | 1.54 | human |

Within *C. psittaci* the same 7,553 bp element is called at 1.7, 4.0, 2,268
and 2,423 copies.

It is worth being exact about which half of the ratio fails, because this
document got it wrong on first writing. Copy number is plasmid coverage
divided by chromosome coverage. The two horse rows have chromosome coverage
of 1.90 and 2.08 reads per base -- the 75th and 77th percentile of the file,
**better** than the median of 0.84. The denominator is unremarkable; the
numerator is at the 100th percentile. Across all 12,006 rows copy number
correlates +0.77 with the numerator and only -0.10 with the denominator.

**And 23.5% of the file is not independent.** 2,818 of 12,006 rows share an
organism and an exact plasmid length with another row -- the same plasmid in a
different isolate. Within the top 200 by copy number, 20 such groups cover 47
rows; collapsing every organism-and-length group to its median leaves 10,005
distinct pairs. Every AIC comparison in this document counts those as separate
evidence, so every dAIC here is larger than it should be.

**The high tail is small and well measured**, and sits where the scaling
relationship predicts rather than off it. Its extreme top is where to be most
sceptical: two independent *Chlamydia psittaci* genomes put a 7.55 kb plasmid
above 2,000 copies at more than 4,000x coverage, where that plasmid is
normally described at single-digit copy number. Copy number is a ratio, and
anything that depresses the chromosomal denominator inflates it.

**The low tail is one population, not two.** An earlier version of this
file split it into a measurement artefact and real biology. With the units
corrected the artefact half is withdrawn: the median sub-one-copy plasmid
carries 63,279 mapped reads and the Poisson relative standard error on that
count is 0.40%. What is left is real biology -- *Agrobacterium*, *Rhizobium*,
*Paracoccus* and *Pantoea* carry large, genuinely low-copy secondary
replicons, and a value slightly below one is what the measurement should give
for a replicon held at one per chromosome in most of a culture.

That bears directly on §3. The PCN >= 1 cut removes this whole population,
and it accounts for about 42% of the slope difference between the two labs.
What it removes is now easier to name than it was: a real low-copy biology
concentrated in the genera that carry large secondary replicons.

## 8. The same test on an independent, accession-keyed dataset

> **Defect found 7 November 2026: the COPLA2 `Remove` flag was never
> consulted.** COPLA2 RefSeq 224 marks 25,363 of its 89,393 entries
> `Remove=Y`, with a stated reason -- Borreliaceae sequences, sub-1500 bp
> fragments, and oversized entries. Every sequence above 1.5 Mb is flagged,
> up to an 11,850,240 bp "plasmid". `copla_replication.py` did not filter on
> it, so **371 of this section's 11,381 joined plasmids (3.3%) should not
> have been there**. The script now honours the flag; the numbers in the
> tables below predate that fix and are marked where they are affected.


Everything above rests on one file, and three of its limitations trace to
that single fact: no accession, so no join to anything; copy numbers below
one already removed; and a PTU label whose relation to replication
machinery this document had to concede was unmeasured.

[COPLA2's RefSeq 224 reference database](https://castillo.dicom.unican.es/copla2/databases)
removes all three at once. It carries a RefSeq accession, a PTU, a
**replicon type**, a MOB class and a host-range grade for 89,393 plasmids,
and Maddamsetti's Supplementary Data 1 carries RefSeq accessions beside its
copy numbers. **94.8% of his plasmids join**, giving 11,379 with copy number,
size, PTU and replicon type together — nearly three times the Ramiro
subset, and keeping the 2,359 plasmids below one copy.
[`copla_replication.py`](copla_replication.py) regenerates all of it and
writes [`copla_receipt.json`](copla_receipt.json).

### The bend replicates, and PTUs absorb even less of it

| | pooled | PTU absorbed | replicon absorbed | genus absorbed |
|---|---:|---:|---:|---:|
| **all 11,379** ΔAIC | −1392.2 | −66.1 | −145.6 | −1325.6 |
| slope change | +0.742 | +0.678 | +0.905 | +0.807 |
| **9,020 at PCN ≥ 1** ΔAIC | −824.0 | −35.2 | −102.5 | −743.1 |
| slope change | +0.656 | +0.550 | +0.822 | +0.688 |

The pooled bend sits at **1.76%** of chromosome length on the full set and
**1.62%** under the Ramiro copy-number filter, against 1.73% in the Ramiro
subset and 1.84% published. Absorbing the PTU leaves ΔAIC at −66.1 and
−35.2 — the same sign, the same conclusion.

What changes is the magnitude, and it moves **against** the composition
reading. In the Ramiro subset the slope change fell 29% under PTU
adjustment. Here it falls **9%** on the full set and **16%** under the same
copy-number filter. On the larger, accession-keyed sample, PTUs account
for less of the bend than §5 estimated, not more.

### A PTU is not a replicon family, now measured

§5 states this and could not support it. Of the 416 PTUs in the joined set
that carry replicon annotations, **182 carry more than one replicon type**.
PTU-FE spans IncFII, Col156;IncFIA and others; PTU-E3 is 52% Col(pHAD28) and
27% a Col(pHAD28);Col440 combination. The two classifications are correlated
and not interchangeable, which is what the correction asserted.

~~And replicon type is the **worse** absorber of the two ... within a
replicon type the bend is steeper than across the whole sample.~~
**Withdrawn, 7 November 2026.** That comparison was computed on two
different samples -- 8,411 plasmids carry a PTU call and 6,620 a replicon
call -- and on a join that included the 371 curator-flagged records. Redone
on the 6,005 records carrying **both** labels, curated, with the knee held
fixed (§5 shows a refitted knee is not comparable once groups differ in mean
size), the point estimates are pooled +0.758, PTU +0.686, replicon +0.923.
The direction of the original claim survives as a point estimate, but it
does not survive being tested:

| | difference from pooled | 95% interval | excludes zero |
|---|---:|---|---|
| replicon - pooled | +0.212 | [-0.217, +0.625] | no |
| PTU - pooled | -0.063 | [-0.366, +0.245] | no |

That is a cluster bootstrap resampling whole replicon groups, which is the
right unit because plasmids within a group are not independent. Neither
adjustment's effect on the bend is resolvable from zero. The sign also
reverses with the knee: replicon exceeds pooled at knees of 1.0-2.2% and
falls below it at 3.0-4.0%.

A granularity control rules out the obvious objection in the other
direction: a random partition with the same 511 groups and the same group
sizes gives +0.761, essentially the pooled value, so random grouping is
neutral and the replicon point estimate is not an artefact of group count.
The estimate is real; its *uncertainty* is what defeats it.

**So this section cannot say which annotation absorbs the bend better, and
no hypothesis about distinct replication strategies can rest on it.**
Reproduced by `replicon_adjustment.py`.

Grouping by genus barely touches the bend at all (ΔAIC −1325.6 of −1392.2),
so it is not host taxonomy either -- that comparison has the same
unmatched-sample and flag problems and has not been redone.

### What this does not fix

Copy number is still modelled from coverage with no published uncertainty.
Plasmids within a PTU are still related by descent, so the AIC comparisons
still flatter themselves. Only 88 of 529 PTUs straddle the knee, so the
within-PTU hinge rests on a minority as it did before. And a replicon type
is an annotation, not an experiment — 58.3% of the joined plasmids carry one
at all.

One result here is odd enough to flag rather than interpret: after absorbing
either grouping, the slope *above* the bend turns positive (+0.133 for PTU,
+0.151 for replicon), meaning copy number rising with size among large
plasmids within a PTU. That is not something this analysis predicted and
it is not something these data explain.



## 9. What a searched ΔAIC is worth, and whether a hinge is the right shape

Two checks this document should have run before leaning on ΔAIC at all.
Both bear on numbers quoted above. Neither changes a fitted coefficient;
both change what the coefficients are worth.

### A searched breakpoint is not a two-parameter model

The pooled ΔAIC of −148.1 was earned by scanning a 200-point grid of
breakpoints and keeping the best, then charged as four parameters against
two, as though the knee had been named in advance. Under the null of no
bend the breakpoint does not exist as a parameter at all, so the usual
regularity conditions behind AIC and the likelihood-ratio test fail. This
is the Davies problem and nothing here corrected for it.

It cannot be corrected analytically, but it can be calibrated: generate
data with **no bend**, keep the real x values and the real PTU structure,
run the same search, and see what the search alone returns.

| null | statistic | median | 5% crit | min | observed | empirical p |
|---|---|---:|---:|---:|---:|---:|
| parametric | pooled, knee **searched** | −23.1 | −92.9 | −233.6 | −148.1 | **0.008** |
| parametric | PTU FE, knee fixed | +1.5 | −2.5 | −9.8 | −19.5 | **0.000** |
| block | pooled, knee **searched** | −28.6 | −148.3 | −505.2 | −148.1 | **0.052** |
| block | PTU FE, knee fixed | +1.5 | −2.5 | −8.9 | −19.5 | **0.000** |

The parametric null adds a PTU random intercept and Gaussian noise with
the variance decomposition of the real residuals. The block null resamples
residuals from the *segmented* fit in whole PTU blocks onto a straight
line, so the real residual shape and within-PTU correlation survive and
the bend is not recycled into its own null.

**The conventional bar of −4 is reached by 88–93% of no-bend datasets when
the knee is searched**, and by 2% when it is fixed. So −4 means nothing
here.

**The headline number is the weak one.** −148.1 reads as overwhelming
against a textbook −4 and is ordinary against its own null: p = 0.008
under the parametric null and **p = 0.052 under the block null**, which is
to say not significant at 5% once realistic within-PTU correlation is
allowed. Meanwhile −19.5, which looks modest, is beyond the entire null
range under both (p = 0.000) because that fit searched nothing.

Every ΔAIC in this document that came from a knee search should be read
against this table rather than against −4. The fixed-knee results are
unaffected. Reproduced by `aic_calibration.py`.

### A hinge beating a line is not evidence of a threshold

A smoothly curving relationship also beats a straight line. The comparison
never run here is hinge against smooth **at the same number of
parameters**.

| model | k | AIC | ΔAIC vs line |
|---|---:|---:|---:|
| line | 2 | 1437.2 | +0.0 |
| quadratic | 3 | 1325.9 | −111.2 |
| hinge, knee searched | 4 | 1289.0 | −148.1 |
| **cubic** | **4** | **1270.0** | **−167.1** |
| natural spline, 4 knots | 4 | 1278.4 | −158.8 |
| natural spline, 5 knots | 5 | 1273.1 | −164.0 |

At matched complexity a plain cubic beats the hinge by 19.0 AIC units and
a natural spline beats it by 10.6. Cross-validation agrees on both
designs:

| model | random 5-fold MSE | leave-one-PTU-out MSE |
|---|---:|---:|
| line | 0.08416 | 0.08536 |
| quadratic | 0.08180 | 0.08313 |
| hinge | 0.08116 | 0.08213 |
| **cubic** | **0.08071** | **0.08185** |
| natural spline, 4 knots | 0.08086 | 0.08228 |

The differences among the curved models are small -- the hinge is 0.55%
off the best on random folds and 0.34% on held-out lineages -- and that is
the finding. **The data support curvature. They do not single out a
hinge**, and a hinge is the only one of these shapes that implies a
threshold.

Worth noting what the leave-one-PTU-out column does say: every model
predicts unseen *lineages* almost as well as unseen *plasmids*
(0.08185 against 0.08071 for the cubic). The size--copy-number
relationship does transfer across PTUs. That supports a shared
relationship; it does not support a shared discontinuity.

### The knee does not survive an interval

| | estimate | 95% interval |
|---|---:|---|
| breakpoint, % of chromosome | 1.71% | **[0.41%, 2.05%]** |

Cluster bootstrap over PTUs, 400 resamples. The interval spans a factor of
5.0. **Quoting a threshold at "1.73%" to three significant figures is not
supported**, and statements elsewhere in this document that treat the
breakpoint location as a measured quantity should be read with that
interval attached.

Reproduced by `smooth_vs_hinge.py`.

## Defects in the input files

Two problems in data this repository ships or downloads, recorded so that
anyone reusing them starts from a known state.

### `curateddataset.csv`, the `gc` column, is in mixed units

2,155 of the 3,961 rows are fractions (median 0.485); 1,806 are percentages
(median 49.81); there are **no values at all between 1 and 25**. Both halves
have the same underlying GC, so it is a unit mix, not two populations.

Taken raw it gives a mean "GC content" of 22.8% with a standard deviation of
24.5. Normalised to percent it is 46.6% with a standard deviation of 7.7.
Nothing in this repository reads that column -- neither `reproduce.py` nor
any section above -- so no result here is affected, but anyone else using it
should normalise first. Checked by `gc_units_check.py`.

### COPLA2 RefSeq 224 ships a curation flag that must be applied

25,363 of 89,393 entries are marked `Remove=Y`. See the note in §8.

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
  whether the PTU-level pattern — small PTUs with high copy number,
  large PTUs with low — is itself selected or merely inherited from
  replicon architecture.
- That genera truly share an exponent. Q has modest power at nine groups;
  "no detected heterogeneity" is not proof of none.
- Any causal direction. Larger plasmids having lower copy number is a
  correlation in a sample assembled from sequencing archives, with whatever
  selection that implies about which plasmids get sequenced at all.
