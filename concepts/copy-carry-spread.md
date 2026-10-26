# COPY, CARRY, SPREAD

A plasmid lineage can gain or lose copies in three ways, operating on three
different timescales and under three different selective regimes:

| | Process | Unit that changes | Timescale |
| --- | --- | --- | --- |
| **COPY** | replication inside one cell | copies per cell | minutes |
| **CARRY** | the host cell divides, or does not | plasmid-bearing cells | generations |
| **SPREAD** | transfer to a cell that did not have it | host lineages | generations to outbreaks |

The three are not independent, and a change that helps one can hurt another.
That is the point of separating them.

---

## COPY — replication inside the cell

**What it is.** A plasmid replicates within its host independently of the
chromosome, to a copy number set by its own control system.

**Benefit of more copies.** Gene dosage. More copies of a resistance gene
generally means more enzyme and a higher resistance level. More copies also
mean a larger mutational supply per cell, which can speed adaptation: in
*Escherichia coli*, a multicopy plasmid accelerated the evolution of a new
β-lactamase activity [@sanmillan2016multicopy], and multicopy carriage allowed
escape from fitness trade-offs during evolutionary innovation, because
variants with different alleles can coexist in one cell
[@rodriguezbeltran2018tradeoffs].

**Burden of more copies.** Replication and expression consume resources.
Plasmid fitness cost arises across the whole plasmid life cycle — replication,
transcription, translation, and interference with host regulation — and is the
main constraint on both vertical and horizontal replication
[@sanmillan2017costs].

**Segregation.** Copies are distributed to daughter cells at division. For
multicopy plasmids without active partition, that distribution is a random
sample, which has two consequences. A cell can receive zero copies
(segregational loss). And alleles within a heterogeneous plasmid population
drift: *segregational drift* means the evolutionary rate of a multicopy
plasmid does **not** rise in proportion to its copy number, because new
variants are lost or take longer to fix [@ilhan2019segregational].
Low-copy plasmids counter loss with active partition and post-segregational
killing systems [@nordstrom1989segregation].

**Copy-number control and intracellular selection.** Replication control is
itself under selection at two conflicting levels: a plasmid copy that
over-replicates relative to its cell-mates is more likely to be inherited, but
the cell carrying such copies is less competitive [@paulsson2002multileveled].
This is the clearest case in plasmid biology of selection acting *below* the
level of the cell. Copy-number control genes are also what incompatibility
acts through: two plasmids sharing a replication control system cannot be
stably co-inherited [@novick1987incompatibility].

**Dynamic, not fixed.** Treating copy number as a constant of the plasmid is a
modelling convenience, not a fact. Copy number responds to host physiology and
growth state, and it evolves: in experimental evolution, the most common
mutations in plasmid R1 were in *copA*, the copy-number control gene, and the
resulting higher copy number raised both transfer rate and resistance level
[@dimitriu2021copy].

> **COPY is a dial with a cost on both ends, and the dial moves on its own.**

## CARRY — vertical transmission

**What it is.** A plasmid-bearing cell divides and both daughters carry the
plasmid. This is how most plasmid copies are actually produced; conjugation is
the rarer event.

**What determines it.**

- **Growth.** The relative growth rate of plasmid-bearing versus plasmid-free
  cells. A cost here compounds every generation.
- **Lag and yield.** Growth rate is not the whole fitness effect. A plasmid
  can lengthen lag phase or lower final yield without changing exponential
  rate, and competition outcomes depend on which the environment rewards.
- **Retention.** Segregational loss rate per division, which depends on copy
  number, partition systems and addiction systems
  [@nordstrom1989segregation].
- **Burden and its compensation.** Costs can be reduced by compensatory
  mutation in host or plasmid over time [@sanmillan2017costs], and this has
  been observed within patients for pOXA-48 [@delafuente2022withinpatient].
- **Host state and host identity.** The *same* plasmid has different costs in
  different hosts. For pOXA-48_K8 in wild-type gut enterobacteria the effect
  was usually small and sometimes beneficial, and it tracked host phylogeny
  [@alonsodelvalle2021variability].

> **CARRY is where cost is paid, every generation, and where it is
> renegotiated.**

## SPREAD — horizontal transmission

Spread is not one event. It is a chain, and the chain breaks more often than
it completes.

```
CONTACT → TRANSFER → ESTABLISHMENT → PERSISTENCE → SECONDARY SPREAD
```

1. **CONTACT.** Donor and recipient must physically meet. This is a function
   of density, spatial structure and mixing, not of the plasmid. In
   *E. coli*, plasmid pB10 could invade from a very rare start on filters with
   daily nutrient replenishment, but not in liquid culture
   [@fox2008spatial].
2. **TRANSFER.** The conjugative machinery must work and the recipient must be
   receptive. Transfer rates vary over orders of magnitude and are a property
   of plasmid *and* host pair, measured as a rate constant rather than a count
   [@simonsen1990endpoint]. Transfer can also be derepressed by genetic
   accident: the Tn*1999* insertion into *tir* raised pOXA-48a transfer
   frequency [@potron2014derepressed].
3. **ESTABLISHMENT.** The arriving plasmid must survive in the new cell:
   restriction and CRISPR defences, replication in an unfamiliar host, and
   incompatibility with a resident plasmid sharing its replication control
   [@novick1987incompatibility]. Entry exclusion systems in the recipient
   actively reduce redundant transfer from identical backbones
   [@garcillan2008entry].
4. **PERSISTENCE.** The new transconjugant lineage must not be outcompeted or
   lose the plasmid, which puts us back in CARRY.
5. **SECONDARY SPREAD.** The new host must itself become a donor. Only here
   does the plasmid have a transmission chain rather than a transmission
   event.

> **Transfer alone is not spread.** A detected transconjugant tells you step 2
> happened. It tells you nothing about steps 3–5. See
> [`../misconceptions/transfer-is-not-spread.md`](../misconceptions/transfer-is-not-spread.md).

**Recipients are not empty.** A recipient in nature is already a cell with a
genome, a physiology, often a resident plasmid and often defences. Resident
plasmids matter in both directions: an incompatible resident blocks
establishment [@novick1987incompatibility], and entry exclusion encoded by a
resident reduces repeat transfer of its own kind [@garcillan2008entry].

## Ecological context: what the three processes are conditional on

None of COPY, CARRY or SPREAD has a value independent of context. A plasmid
"cost" or "transfer rate" quoted without its context is incomplete.

- **Resources.** Nutrient level sets growth rate, and the cost of carriage is
  partly a cost of biosynthesis. Nutrient replenishment was necessary for
  plasmid invasion in structured populations [@fox2008spatial].
- **Competitors.** Fitness is relative. What matters is the cost against the
  competitor actually present.
- **Antibiotics.** Selection for the cargo can reverse the sign of the net
  effect, and its concentration and timing matter.
- **Space.** Spatial structure concentrates donors next to recipients and
  shelters transconjugant microcolonies [@fox2008spatial].
- **Host state.** Growth phase, stress response and physiology change both
  copy number and cost.
- **Resident plasmids.** Incompatibility and exclusion
  [@novick1987incompatibility; @garcillan2008entry].
- **Time.** Costs are compensated; transfer rates evolve
  [@sanmillan2017costs; @dimitriu2021copy].
- **History.** Which hosts the plasmid has already adapted to, and what the
  population has already been exposed to.

> **Same plasmid. Different context. Different fate.**

## How the three interact

The processes are coupled, often in ways that frustrate simple predictions.

- Higher copy number raises dosage and mutational supply (COPY benefit), but
  raises burden (CARRY cost) and dilutes new alleles through segregational
  drift (COPY cost) [@ilhan2019segregational; @sanmillan2017costs].
- Higher copy number can also raise transfer rate, coupling COPY to SPREAD:
  evolved *copA* variants of plasmid R1 had both higher copy number and up to
  1000-fold higher transfer, at a cost to the host [@dimitriu2021copy].
- High transfer can sustain a plasmid whose CARRY balance is negative, which
  is why costly plasmids persist without antibiotic selection
  [@lopatkin2017persistence].

The next page asks why these couplings so often leave plasmid interest and
host interest pointing in different directions:
[`plasmid-vs-host-fitness.md`](plasmid-vs-host-fitness.md).
