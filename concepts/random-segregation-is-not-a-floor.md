# Random segregation is a reference point, not a floor

The standard formula for segregational loss is one line. A cell carrying *c*
plasmid copies replicates them to 2*c*, each molecule goes to one daughter or
the other independently, and the chance a given daughter is born plasmid-free
is

```
    p = (1/2)^(2c)
```

[Nordström & Gerdes (2003)](https://pubmed.ncbi.nlm.nih.gov/12932735/) state
it in exactly this form — plasmid-free daughters at a frequency of
`(1/2)^2n` per cell per generation, where `2n` is the average copy number *at
cell division* — and conclude that **the unit of segregation is one plasmid
copy**.

[`../models/copy-number-burden/battle_royale/segregation.py`](../models/copy-number-burden/battle_royale/segregation.py)
implements that, and
[`../figures/output/copy-number-and-loss-rate.svg`](../figures/output/copy-number-and-loss-rate.svg)
draws it. Both originally described the result as a **floor** — the loss rate
you would get if nothing but chance were operating, with real plasmids living
below it.

> **That framing is wrong, and this file exists because the measured numbers
> say so. Real loss rates sit on both sides of the line, and for the plasmids
> the model describes best they sit far above it.**

---

## The number that settles it

[Summers & Sherratt (1984)](https://pubmed.ncbi.nlm.nih.gov/6323019/), in
*Cell*, report that ColE1-related cloning vectors are lost at **10⁻² to 10⁻⁵
per cell per generation**.

pBR322-class vectors run at roughly 15–20 copies. The model at *c* = 15 gives
2⁻³⁰ ≈ 9 × 10⁻¹⁰.

```
    measured      10⁻²  ──────────────  10⁻⁵
    predicted                                        ~10⁻⁹
                  └──────── five to eight orders ────────┘
```

So the observed rate is **five to eight orders of magnitude above** what
random segregation at that copy number predicts. The same paper says these
plasmids *are* "partitioned randomly at cell division" — so this is not a
failure of the random-segregation idea. It is a failure of the assumption
that *c* in the formula equals the copy number you measured.

A caveat that matters: "ColE1-related cloning vectors" is a class, their copy
numbers vary, and the 10⁻²–10⁻⁵ range spans constructs and conditions. This
is an order-of-magnitude comparison, not a matched measurement on one
plasmid. It is still far too large a gap to be a modelling detail.

---

## What pushes measured loss ABOVE the line

### Multimerisation — the same argument the figure makes, about a different variable

Summers & Sherratt found plasmid stability **inversely correlated with
multimerisation**, and gave the mechanism: multimers are maintained at lower
copy number than monomers, because copy-number control counts origins. A
dimer is *one segregating unit carrying two origins*. Form dimers and the
effective *c* falls even though the number of plasmid *molecules* has not.

[Summers, Beton & Withers (1993)](https://pubmed.ncbi.nlm.nih.gov/8361350/)
pushed this into the "dimer catastrophe" hypothesis, and the finding is worth
reading carefully:

- dimers replicate at **twice** the rate of monomers, so they take over
  whichever cell has them;
- dimer distribution across the population is **heterogeneous**, not even —
  in a rec⁺ culture where **4% of pBR322 molecules are dimers, more than half
  of those dimers sit in dimer-only cells**;
- plasmid-free daughters arise from that small subpopulation at high
  frequency.

**This is structurally the same claim as the figure.** The figure says: a
mean copy number hides a low-copy minority that does nearly all of the
losing. Summers et al. say: a 4% dimer fraction hides a dimer-only minority
that does nearly all of the losing. Same shape, different variable — and
theirs was published in 1993. An average over a convex loss function is not
the loss at the average, whichever quantity is doing the varying.

**Status: partly confirmed, quantitatively contested.**
[Boe et al. (1997)](https://pubmed.ncbi.nlm.nih.gov/9044259/) tested it on a
pBR322 derivative. They confirmed most of the theory and the heterogeneous
distribution, measured the monomer-to-dimer loss-rate difference at **13–14×**
and monomer-to-trimer at **14–50×**, but could *not* detect the difference in
growth inhibition between monomeric, dimeric and trimeric states that Summers
had proposed as the brake on runaway multimerisation. What stops runaway is
left open.

### Clustering — the unit of segregation may not be the molecule

If plasmids travel in clusters, the segregating unit is the cluster, and
effective *c* is the number of clusters rather than the copy number.
Fluorescence work on RK2 and on oriR1 repeatedly finds **fewer foci per cell
than copies per cell**.

This one is genuinely unsettled, and the sources disagree in an interesting
way:

- Nordström & Gerdes (2003) name it a paradox and propose a resolution that
  **rescues** random segregation: one copy at a time is recruited from the
  cluster to a central replication factory, the daughter copies then diffuse
  freely, so segregation is coupled to *replication* and happens continuously
  through the cycle rather than at division. The unit stays the copy.
- [Reyes-Lamothe et al. (2014)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3902917/),
  *NAR* 42:1042–1051, support random partitioning for ColE1-type high-copy
  plasmids: individual molecules diffuse in nucleoid-free space, replicate
  stochastically and are randomly partitioned.
- [Million-Weaver & Camps (2014)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4163524),
  *Plasmid*, doi 10.1016/j.plasmid.2014.07.002, question the
  random-distribution model and argue for a mechanism moving high-copy
  plasmids to the poles.

Do not present clustering as a settled correction. Present it as the open
question it is.

### Fitness cost, which the model switches off entirely

`bearing_fraction_after` assumes carriers and non-carriers grow at the same
rate. They do not. A plasmid-free segregant founds a lineage that outgrows
the carriers, so the carrier fraction falls faster than segregation alone
accounts for.

This matters for reading any experiment: a loss rate from a serial-passage
assay is **segregation and selection together**, and the model computes only
the first. See
[`fitness-vs-persistence.md`](fitness-vs-persistence.md).

---

## What pushes measured loss BELOW the line

### Active partition

Three mechanistic classes, named for the motor NTPase:

| Type | System | Motor |
|---|---|---|
| I | ParABS | Walker-type ATPase (ParA), ParB, *parS* |
| II | ParMRC | actin-like ParM filament pushing two copies apart |
| III | TubZRC | tubulin-like GTPase |

Low-copy plasmids carry these *because* the formula is unaffordable down
there: at *c* = 2, 6.25% of daughters are born free, and at *c* = 1 it is
25%. Partition converts a stochastic process into a near-deterministic one.
See also [Paulsson et al. (2000)](https://pubmed.ncbi.nlm.nih.gov/10704315/),
"Molecular clocks reduce plasmid loss rates: the R1 case".

This is why pOXA-48 — large, IncL, low copy — is not a counterexample to the
figure. It is living far below the curve on purpose, and the distance is the
measure of what its partition system is doing.

### Multimer resolution

ColE1's *cer* site, resolved by XerCD with the host factors ArgR and PepA,
converts multimers back to monomers and so **maximises the number of
independently segregating units**. Summers & Sherratt localised the
monomerising determinant to a 0.38 kb region whose addition greatly increased
vector stability.

### Toxin–antitoxin systems

These do not change segregation at all. They remove the segregants
afterwards, so the *apparent* loss rate falls while the actual rate of
producing plasmid-free daughters is untouched. Whether the mechanism is
killing or growth inhibition is disputed — see
[Song & Wood (2018)](https://www.frontiersin.org/articles/10.3389/fmicb.2018.00814/pdf),
who argue the evidence for post-segregational *killing* is weaker than
usually assumed.

Worth saying out loud in a lecture: a stability mechanism that works by
removing the evidence is not the same kind of thing as one that prevents the
event.

---

## The correction, stated plainly

```
                        partition systems
                        multimer resolution        measured loss
                        toxin-antitoxin            BELOW the line
                               ▲
    ───────────────  (1/2)^(2c)  ───────────────
                               ▼
                        multimerisation            measured loss
                        clustering                 ABOVE the line
                        fitness cost
```

The line is a **reference point**: the rate you would see if the only thing
happening were independent coin flips over molecules that are genuinely
independent, genuinely equal in number to the measured copy number, in cells
that grow at the same rate whether or not they carry the plasmid. Nothing
guarantees a real plasmid falls on either side of it.

What the figure still teaches correctly, and what no mechanism above
overturns: **averaging a convex loss function over a distribution is not that
function at the mean.** The dimer catastrophe is that statement about dimer
fraction; the figure is that statement about copy number.

---

## Two different things are called "the plasmid paradox"

Worth keeping straight, because this lecture touches both:

- **Nordström & Gerdes (2003)** — plasmids cluster, yet segregate as though
  the unit were a single copy. A paradox about *mechanism*.
- **The persistence paradox** — costly plasmids ought to be purged by
  selection, yet they persist. A paradox about *evolution*. See
  [Brockhurst & Harrison (2022)](https://pubmed.ncbi.nlm.nih.gov/34848115/),
  "Ecological and evolutionary solutions to the plasmid paradox", *Trends
  Microbiol*.

They share a name and nothing else.

---

## References

Every entry below was checked against its PubMed record; PMIDs are given so
the check is repeatable.

| Work | Venue | PMID |
|---|---|---|
| Summers & Sherratt, multimerisation causes instability; *cer* | *Cell*, 1984 | [6323019](https://pubmed.ncbi.nlm.nih.gov/6323019/) |
| Summers, Beton & Withers, dimer catastrophe hypothesis | *Mol Microbiol*, 1993 | [8361350](https://pubmed.ncbi.nlm.nih.gov/8361350/) |
| Boe et al., comments on the dimer catastrophe hypothesis | *Mol Microbiol*, 1997 | [9044259](https://pubmed.ncbi.nlm.nih.gov/9044259/) |
| Paulsson et al., molecular clocks reduce plasmid loss rates | *J Mol Biol*, 2000 | [10704315](https://pubmed.ncbi.nlm.nih.gov/10704315/) |
| Nordström & Gerdes, clustering versus random segregation | *Plasmid*, 2003 | [12932735](https://pubmed.ncbi.nlm.nih.gov/12932735/) |
| Reyes-Lamothe et al., high-copy plasmids randomly partitioned | *NAR*, 2014 | [24137005](https://pubmed.ncbi.nlm.nih.gov/24137005/) |
| Million-Weaver & Camps, mechanisms of plasmid segregation | *Plasmid*, 2014 | [25107339](https://pubmed.ncbi.nlm.nih.gov/25107339/) |
| Field & Summers, revisiting the dimer catastrophe | *J Theor Biol*, 2011 | [21945338](https://pubmed.ncbi.nlm.nih.gov/21945338/) |
| Song & Wood, post-segregational killing evidence is weak | *Front Microbiol*, 2018 | — |
| Brockhurst & Harrison, solutions to the plasmid paradox | *Trends Microbiol*, 2022 | [34848115](https://pubmed.ncbi.nlm.nih.gov/34848115/) |

Not yet verified to the same standard, and flagged rather than cited as
settled: the RK2 and oriR1 clustering microscopy, which reached this file
through a literature search rather than a read of the primary papers, and the
Song & Wood PMID.
