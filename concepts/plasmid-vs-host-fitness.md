# Plasmid fitness and host fitness are not the same quantity

A plasmid and its host cell share a body but not a reproductive accounting.
The host's fitness is measured in daughter cells. The plasmid's fitness is
measured in plasmid copies in future cells — including copies in cells that
are not descendants of this host. Those two currencies are convertible but not
identical, and the gap between them explains a large part of plasmid biology.

---

## Where the two agree

Vertical transmission aligns them. A plasmid copied into both daughters at
every division is a plasmid whose reproductive success *is* its host's
reproductive success. For a plasmid with perfect segregation and no transfer,
the alignment is total: anything that harms the host harms the plasmid by
exactly as much.

This is why the limiting case of a fully aligned plasmid is a chromosome.
Where gene mobility has no benefit and some cost, host-adaptive genes should,
over evolutionary time, end up in the chromosome rather than on a plasmid
[@bergstrom2000natural].

## Three ways the two come apart

**Predict first.** Two strains grow together. Plasmid-bearing cells grow 5%
more slowly than plasmid-free ones, but the plasmid transfers efficiently into
plasmid-free cells.

> **Is the plasmid necessarily becoming less fit?**

Commit to an answer before opening the reveal. Nothing records it.

### 1. Horizontal transmission gives the plasmid a second route

<details>
<summary>Evidence</summary>

**No — and the word "necessarily" is where the question turns.**

A plasmid that can conjugate has a way to reproduce that does not require its
host to reproduce. It can therefore be maintained while imposing a cost that
pure vertical transmission would eliminate. This is the classical existence
condition: a conjugative plasmid can persist in a population even when
plasmid-bearing cells grow substantially more slowly than plasmid-free ones,
provided transfer is frequent enough relative to that cost and to
segregational loss [@stewart1977population].

Empirically, common conjugative plasmids do transfer fast enough to be
maintained without antibiotic selection despite being costly, across nine
plasmids from six incompatibility groups [@lopatkin2017persistence]. The
implication the authors draw is uncomfortable and important: reducing
antibiotic use alone need not reverse resistance.

Note what the evidence does *not* say. It does not say the cost is irrelevant,
and it does not say this plasmid is increasing. It says host growth rate alone
does not settle the question.

</details>

**Diagnose.** If you answered yes, the assumption that did the work was almost
certainly this one:

> *I treated plasmid reproduction as if it occurred only through host
> reproduction.*

That assumption is not silly — it is exactly right for a chromosome, and for a
non-mobilisable plasmid. It fails here because conjugation gives the plasmid a
second route, and the question gave you that route in the same sentence as the
cost.

If you answered no, check whether you concluded it from the mechanism or
merely distrusted a question that looked like a trick. The second is a useful
instinct and not yet an understanding.

**Reconstruct.** The two accountings differ in what counts as a descendant:

| | Route that can contribute |
| --- | --- |
| **Host** | daughter cells |
| **Plasmid** | vertical descendants, **plus** lineages it colonises horizontally, **plus** its representation among copies inside a cell |

This is an accounting sketch, not a formula, and deliberately so. "Plasmid
fitness" has no single universal definition: which currency is right depends
on the question — invasion from rare, long-run frequency, or allele
representation within a cell — and each has its own formalisation. One of
them is worked through on the next page, where the invasion condition
γ·n\* > c·ψ + τ makes the same three terms explicit under stated assumptions
(`claim.model.plasmid_invasion_threshold`, **`MODEL`**). Read the table as
naming the routes, not as summing them.

**Transfer.** Change one variable and re-answer:

> Same 5% host cost, but the plasmid is **non-mobilisable** — no horizontal
> transfer at all. Does your answer change?

<details>
<summary>Why this one is different</summary>

Yes. With transfer removed, the plasmid's only route to future cells runs
through its host's division, so a sustained growth disadvantage plus any
segregational loss removes it. In the threshold on the next page, setting
γ = 0 makes the left side zero while cost and loss stay positive, so the
condition cannot be met at any host density.

The general relation, which is the thing worth keeping: **a host-level cost is
decisive exactly to the extent that the plasmid's reproduction is routed
through the host's.** The 5% was never the deciding number on its own.

Two honest caveats. Removing conjugation does not remove every route to
persistence — cargo that pays under selection, and compensatory evolution that
erodes the cost, both still apply, and are discussed below. And a
non-mobilisable plasmid is not an inert one: copy-number competition inside
the cell, route 2 below, does not need conjugation.

</details>

That is the logic of a parasite, and it applies whether or not the plasmid is
parasitic on balance — a question the last section returns to.

### 2. Intracellular competition gives the plasmid a third route

Within a single cell, plasmid copies are also in competition with each other.
A copy that replicates more than its share is more likely to be represented in
descendants — even though the cell carrying such copies is, on average, worse
off. Replication control is therefore under selection at two conflicting
levels at once, and several features of plasmid replication systems are
interpretable as the residue of that conflict [@paulsson2002multileveled].

Selection below the level of the cell has no reason to produce host benefit.

### 3. Post-segregational killing makes loss worse than carriage

Toxin–antitoxin and related addiction systems do not make the plasmid cheaper
to carry. They make *losing* it lethal, so cells that segregate the plasmid
away are removed from the population [@nordstrom1989segregation]. The
population-level effect is high plasmid retention; the cell-level effect for a
cell that loses the plasmid is death. This stabilises the plasmid by
penalising the host, which is the clearest possible demonstration that the two
fitnesses are separate quantities.

## Why the gap is not usually as wide as it could be

Three forces narrow it.

**Compensatory evolution.** Costs are not fixed. Mutations in host or plasmid
reduce burden over time, often rapidly, and this is a major reason plasmids
persist [@sanmillan2017costs]. Within hospitalised patients, pOXA-48 showed
compensatory evolution of its fitness cost alongside evolution of higher
resistance, with a trade-off between the two
[@delafuente2022withinpatient].

**Cargo that pays.** When the plasmid carries a gene the host needs — a
resistance gene under antibiotic exposure, a catabolic operon on a novel
carbon source — the two fitnesses align for as long as the environment holds.
This alignment is conditional and can disappear overnight.

**Host–plasmid coevolution.** Plasmid and host adapt to each other, so the
interaction is not a fixed cost but a coevolutionary process whose outcome
depends on the history of the pairing [@harrison2012coevolutionary].

## The consequence for how we talk about plasmids

Two framings are each incomplete:

- *"Plasmids are genetic parasites."* This over-reads the gap. Many plasmids
  carry genes of clear host benefit, costs are frequently compensated, and
  across wild-type gut enterobacteria a clinical plasmid's effect was an
  overall reduction in fitness that was nonetheless neutral or positive in
  several hosts [@alonsodelvalle2021variability]. Those hosts are the ones
  that bear on parasitism, and they are exceptions inside a net cost, not the
  central tendency. Pure parasitism also fails as a
  general explanation: empirically, transfer rates are often too low for
  plasmids to be maintained as parasites alone [@bergstrom2000natural].
- *"Plasmids are accessory genomes that help their hosts."* This ignores the
  gap. It cannot explain addiction systems, copy-number conflict, or
  persistence of costly plasmids in the absence of selection for their cargo.

The usable framing is **conditional alignment**: plasmid and host interests
coincide to the degree that the plasmid's reproduction runs through the host's
reproduction, and they diverge to the degree that it does not. Horizontal
transfer, intracellular replication competition and addiction systems are
exactly the mechanisms that let plasmid reproduction bypass host reproduction.

That there is no single resolution of this tension is itself a live research
question — the "plasmid paradox", for which several explanations have been
proposed and none is clearly sufficient [@carroll2018persistence]. (The
Rodríguez-Beltrán review previously cited here does not raise the paradox; it
covers plasmid polyploidy, genetic dominance and segregational drift, and has
been removed from this sentence rather than re-purposed.)

## How this can be misread

Status vocabulary:
[`../docs/pedagogy-conventions.md`](../docs/pedagogy-conventions.md).

| Tempting reading | Status | Better model |
| --- | --- | --- |
| A plasmid that slows its host has low plasmid fitness. | **Misleading** | Host and plasmid reproductive accounting can diverge. A cost is decisive only to the extent the plasmid's reproduction runs through the host's [@stewart1977population; @lopatkin2017persistence]. |
| Horizontal transfer makes host cost irrelevant. | **False** | The cost still enters every generation of carriage. Transfer adds a route; it does not delete a term, and it has to outpace cost *plus* segregational loss [@sanmillan2017costs]. |
| Addiction systems benefit plasmids because they benefit their hosts. | **False** | They stabilise carriage by making plasmid *loss* costly to the host: cells that segregate the plasmid away are killed [@nordstrom1989segregation]. Population-level retention, cell-level harm. |
| Plasmids are therefore parasites. | **Overgeneralised** | Alignment is conditional. Cargo that pays, compensatory evolution and host–plasmid coevolution all realign interests [@sanmillan2017costs; @harrison2012coevolutionary]; a clinical plasmid's overall reduction in host fitness was neutral or positive in several wild-type hosts [@alonsodelvalle2021variability]; and transfer rates are often too low for plasmids to persist as parasites alone [@bergstrom2000natural]. |

The first and last rows fail in opposite directions, which is the useful
thing about seeing them together: one under-reads the gap between the two
accountings, the other over-reads it. The page is about the conditions that
set its width (`claim.fitness.conditional_alignment`).

---

**Next.** If plasmid fitness and host fitness are different quantities, then
measuring either one does not settle what happens to the plasmid:
[`fitness-vs-persistence.md`](fitness-vs-persistence.md).
