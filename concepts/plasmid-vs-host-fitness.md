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

### 1. Horizontal transmission gives the plasmid a second route

A plasmid that can conjugate has a way to reproduce that does not require its
host to reproduce. It can therefore be maintained while imposing a cost that
pure vertical transmission would eliminate. This is the classical existence
condition: a conjugative plasmid can persist in a population even when
plasmid-bearing cells grow substantially more slowly than plasmid-free ones,
provided transfer is frequent enough relative to that cost and to segregational
loss [@stewart1977population].

Empirically, common conjugative plasmids do transfer fast enough to be
maintained without antibiotic selection despite being costly, across nine
plasmids from six incompatibility groups [@lopatkin2017persistence]. The
implication the authors draw is uncomfortable and important: reducing
antibiotic use alone need not reverse resistance.

The deeper point: **a trait that reduces host growth can still increase in
frequency if it raises transmission enough.** That is the logic of a
parasite, and it applies whether or not the plasmid is parasitic on balance.

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
  carry genes of clear host benefit, costs are frequently compensated, and in
  some wild-type hosts the measured effect of a clinical plasmid is neutral or
  positive [@alonsodelvalle2021variability]. Pure parasitism also fails as a
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
proposed and none is clearly sufficient [@carroll2018persistence;
@rodriguezbeltran2021beyond].

---

**Next.** If plasmid fitness and host fitness are different quantities, then
measuring either one does not settle what happens to the plasmid:
[`fitness-vs-persistence.md`](fitness-vs-persistence.md).
