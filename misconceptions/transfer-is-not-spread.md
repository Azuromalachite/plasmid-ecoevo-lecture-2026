# Misconception: a transfer event means the plasmid is spreading

## The tempting intuition

Conjugation was detected. Transconjugants were counted. The plasmid moved from
one cell to another, therefore the plasmid is spreading, and the higher the
transfer rate the faster it spreads.

This intuition is built into how transfer is often reported: a ratio of
transconjugants to donors or recipients at the end of a mating, treated as if
it were a property of the plasmid.

## Why it fails

**Transfer is one step in a chain of five, and the chain usually breaks.**

```
CONTACT → TRANSFER → ESTABLISHMENT → PERSISTENCE → SECONDARY SPREAD
```

A transconjugant on a plate is evidence for step 2 only.

**1. CONTACT is not the plasmid's property.** Whether donor and recipient meet
depends on density, mixing and spatial structure. Plasmid pB10 in *E. coli*
invaded a population from an initial frequency as low as 10⁻⁷ when cells grew
on filters with daily transfer to fresh medium, nearly completely invaded when
the structure was disturbed daily, and **could not invade in liquid at all**
[@fox2008spatial]. Same plasmid, same host, opposite outcomes — decided by the
habitat.

**2. ESTABLISHMENT can fail after a successful transfer.** The recipient is
not an empty vessel. Restriction and other defences may destroy the incoming
DNA. The plasmid may replicate poorly in an unfamiliar host. A resident
plasmid sharing the same replication control system makes stable
co-inheritance impossible [@novick1987incompatibility]. And recipients
carrying a related plasmid actively reduce further transfer from the same
backbone through entry exclusion, which is a near-universal feature of
conjugative plasmids [@garcillan2008entry].

**3. PERSISTENCE is a separate question with its own answer.** A
transconjugant lineage faces the full CARRY balance: fitness cost and
segregational loss, in a host that may never have carried this plasmid before.
The cost of the same plasmid varies substantially between wild-type hosts and
is an overall reduction that is small in most hosts and beneficial in
several [@alonsodelvalle2021variability]. A
transfer into a host where the plasmid is costly and poorly retained is a dead
end.

**4. SECONDARY SPREAD requires the new host to become a donor.** Only then is
there a transmission chain rather than an isolated event. This depends on the
transfer machinery being expressed in the new host and on that host meeting
further recipients.

**5. The number you measured may not be the number you think.** A
transconjugant count at a single time point confounds transfer with growth of
donors, recipients and transconjugants during the mating, and with when you
chose to look. A conjugation rate should be estimated as a rate constant under
a stated population model [@simonsen1990endpoint]. Two experiments reporting
"transfer frequency" without the model behind it are not comparable.

## A better model

Treat spread as a **chain with a probability at every link**, and the
realised rate of spread as the product of them, under conditions that must be
stated:

| Link | What limits it | Property of |
| --- | --- | --- |
| CONTACT | density, structure, mixing | the habitat |
| TRANSFER | conjugation machinery, repression, recipient receptivity | plasmid × host pair |
| ESTABLISHMENT | defences, replication in new host, incompatibility, entry exclusion | the recipient |
| PERSISTENCE | cost, segregational loss, selection for cargo | new host × environment |
| SECONDARY SPREAD | expression of transfer in the new host, further contacts | new host × habitat |

Consequences for interpretation:

- A measured transfer rate is a statement about link 2 under one set of
  conditions. It is not a prediction of spread.
- Failure to spread does not imply failure to transfer, and detecting transfer
  does not imply spread.
- Interventions can target any link. Blocking conjugation targets link 2;
  changing spatial structure or nutrient supply targets link 1
  [@fox2008spatial]; a resident incompatible plasmid targets link 3.

## Example

**Transfer without spread.** pB10 in well-mixed liquid culture: conjugation
occurs, but the plasmid does not invade the population, because the structure
that would let transconjugant microcolonies grow and transfer onward is
absent. On filters with nutrient replenishment, the same plasmid invades from
extreme rarity [@fox2008spatial].

**Spread as a chain, in a hospital.** For pOXA-48 the chain completes
repeatedly and at two different levels at once. Combining epidemiological data
from over 9,000 patients with 250 enterobacterial genomes over two years
showed frequent between-patient transmission of plasmid-carrying clones
*and* within-patient horizontal transfer of the plasmid occurring in
essentially every colonised patient's gut — an inference the authors draw
from their sequence analysis and models, phrased as "suggesting that", rather
than a direct observation [@leonsampedro2021pervasive]. What
makes this spread rather than transfer is that the later links hold too: the
plasmid's fitness effects in wild-type gut enterobacteria are an overall
reduction that is nonetheless small in most hosts and beneficial in several
[@alonsodelvalle2021variability], and its cost is compensated
within patients over time [@delafuente2022withinpatient]. Note also that the
transfer link itself was raised by a genetic accident — the Tn*1999* insertion
into the transfer-inhibition gene *tir* [@potron2014derepressed]. Several
links are favourable simultaneously; that is what an epidemic plasmid looks
like.

## References

[@fox2008spatial; @novick1987incompatibility; @garcillan2008entry;
@alonsodelvalle2021variability; @simonsen1990endpoint;
@leonsampedro2021pervasive; @delafuente2022withinpatient;
@potron2014derepressed]

See also [`../concepts/copy-carry-spread.md`](../concepts/copy-carry-spread.md),
section SPREAD.
