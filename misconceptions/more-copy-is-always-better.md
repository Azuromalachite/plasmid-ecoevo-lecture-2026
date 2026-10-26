# Misconception: more copies is always better

## The tempting intuition

More copies of the plasmid means more copies of the gene, which means more
protein, which means a stronger phenotype — more resistance, more product,
more of whatever the plasmid encodes. Higher copy number also means more
targets for mutation, so the plasmid should evolve faster. Copy number looks
like a dial where "up" is simply "more".

The intuition is reinforced by laboratory practice: cloning vectors are chosen
for high copy number precisely to get more DNA and more product.

## Why it fails

**1. Copies cost.** Replication and expression of every copy consume
precursors, polymerase and ribosomes. Fitness cost arises throughout the
plasmid life cycle and is the main constraint on plasmid replication, both
vertical and horizontal [@sanmillan2017costs]. A dosage benefit is bought with
a growth cost, and whether the trade is favourable depends on whether the
environment is paying for the dosage.

**2. More copies does not give proportionally faster evolution.** This is the
least intuitive part. Multicopy plasmids do have an increased mutational
supply, but when the plasmid population within a cell is genetically
heterogeneous, random distribution of copies at cell division — *segregational
drift* — loses new variants and lengthens the time to fixation. In
experimental evolution of low- and high-copy plasmids in *E. coli*, the
evolutionary rate of the multicopy plasmid did **not** reflect the increased
mutational supply expected from its copy number [@ilhan2019segregational].

What multicopy carriage does give is something different and genuinely useful:
*heterozygosity*. Different alleles can coexist in one cell, which allows
escape from fitness trade-offs during evolutionary innovation
[@rodriguezbeltran2018tradeoffs], and multicopy plasmids can potentiate the
evolution of resistance [@sanmillan2016multicopy]. "Faster" and "able to hold
two alleles at once" are not the same advantage.

**3. Selection inside the cell is not aligned with the cell.** Copy number
control is under selection at two levels: a copy that over-replicates wins
against its cell-mates, while the cell loses against other cells
[@paulsson2002multileveled]. The copy number a plasmid settles at is a product
of that conflict, not an optimum for the host.

**4. Copy number has side effects beyond dosage.** Elevated copy number can
raise conjugative transfer rate as well: evolved *copA* variants of plasmid R1
had higher copy number, up to 1000-fold higher transfer, *and* higher
resistance, at a cost to the host [@dimitriu2021copy]. Copy number is coupled
to spread, not only to dosage. Whether that is "better" depends on whose
fitness you are asking about.

**5. Low copy number buys stability by other means.** Low-copy plasmids are
not simply deficient. They use active partition systems and post-segregational
killing to achieve retention that random distribution could not provide
[@nordstrom1989segregation]. These are solutions to a problem high copy number
solves differently, not failures to reach high copy number.

## A better model

Copy number is a **trade-off variable under multilevel selection**, not a
performance dial:

| Raising copy number | Effect |
| --- | --- |
| Gene dosage | ↑ |
| Mutational supply per cell | ↑ |
| Allelic heterozygosity within a cell | ↑ |
| Conjugative transfer (sometimes) | ↑ |
| Metabolic burden | ↑ (cost) |
| Retention of a *new* beneficial allele | ↓ (segregational drift) |
| Alignment with host interest | ↓ |
| Loss by random segregation | ↓ (benefit) |

The useful question is not "is copy number high?" but **"what is copy number
being selected by, at which level, in this environment?"** And since copy
number evolves [@dimitriu2021copy], it is a variable of the system, not a
parameter of the plasmid.

## Example

Plasmid R1 evolving in the presence of susceptible, plasmid-free recipients
accumulated mutations in *copA*, the copy-number control gene. The resulting
higher-copy variants transferred up to 1000-fold better and conferred higher
antibiotic resistance — and imposed a cost on their hosts. Both host
availability and antibiotics were each sufficient on their own to select these
plasmids [@dimitriu2021copy]. The copy number went up, and whether that was
"better" has a different answer for the plasmid and for the cell.

Contrast: in the segregational drift experiments, the high-copy plasmid's
extra mutational supply did not translate into a proportionally higher
evolutionary rate, because drift at division removed new variants
[@ilhan2019segregational].

## References

[@sanmillan2017costs; @ilhan2019segregational; @rodriguezbeltran2018tradeoffs;
@sanmillan2016multicopy; @paulsson2002multileveled; @dimitriu2021copy;
@nordstrom1989segregation]

See also [`../concepts/copy-carry-spread.md`](../concepts/copy-carry-spread.md),
section COPY.
