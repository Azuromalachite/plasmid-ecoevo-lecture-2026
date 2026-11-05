# Releases — what a version number means here

Adopted from the Arrowfield and ESPMap precedent in this account, because the
problem is the same one: a living repository keeps moving, and a version has
to freeze a state that is still meaningful after it has moved on.

> **Milestones are capability gates, not calendars.** A version is cut when
> its scientific contract is satisfied. Unfinished future work is listed as
> explicit non-goals rather than delaying the release indefinitely.

A minor version does not mean "enough commits accumulated". It means **a new
scientifically coherent capability**, with four conditions:

1. There is a **new question the repository can now answer**.
2. The evidence → model → figure chain for that question is **reproducible**.
3. Known limitations are **explicit enough that the release is safe to cite
   or teach from**.
4. The release boundary **can stay frozen** while `main` continues to move.

Condition 4 is the one that is easy to lose. A release is a contract about a
commit, not a pointer at the best current state.

## "Withheld" is repository state, not remembered intention

Earned in v0.3. The release note was drafted and deliberately **not**
committed, because its verification table was false until the findings it
declared closed actually closed. That decision existed only as an intention.
A `git add -A` on an unrelated branch swept the untracked file into a commit,
and `main` then carried a release note making false claims about a release
that had not happened — underneath this very document, which says a release
note cannot precede the state it describes.

Nobody was misled, because no tag pointed at it. That is luck. The fix is to
make the states physically distinct, so that the tooling cannot convert "I
meant not to publish this" into a repository fact merely because the file
exists in the working tree:

```text
exploratory draft      → scratch outside the repository, or a separate worktree
candidate release note → a release-prep branch
verified release note  → main
tag                    → immutable frozen boundary
```

No automation is needed and none is proposed. The rule is that **each state
has a location**, and a file's location is what says which state it is in. An
intention held in one person's head is not a state the repository can observe,
and `git add -A` cannot be taught to respect one.

The same reasoning governs the private-to-public promotion planned for v0.4:
it is a **reimplementation from a frozen export**, not a copy of whatever
currently looks good in the research repository. Copying working state carries
across exactly the hidden assumptions this episode showed the process does not
otherwise catch.

## Frozen artifacts stay frozen

A teaching artifact is tied to the release that produced it, including the
versions of the tools that produced it:

```text
release:          v0.4
renderer:         gbdraw 0.14.4
input accessions: frozen
render script:    frozen
```

**A newer renderer does not silently replace a historical figure.** If a
figure is deliberately refreshed under a newer tool, that is a *new artifact
in a new release context*, not an update of the old one. The same holds for a
model result: a study pinned to `v0.3` stays reproducible under `v0.3` even
after the model improves.

This matters here specifically because SVG output embeds full-precision
floats, so byte-identity is per-platform and per-version. A rebuild guarantee
is only meaningful against a pinned toolchain, and the pin belongs in the
release record.

## The ladder

| | Capability | State |
| --- | --- | --- |
| `v0.1` | scientific and intellectual spine | released |
| `v0.2` | evidence and pedagogy architecture | released |
| `v0.3` | **executable inference** | released |
| `v0.4` | evolution of genomic address | not started |
| `v0.5` | competing models of plasmid design space | future |
| `v0.6` | dynamical regimes and persistence landscapes | future |
| `v0.7` | mechanism-first design reasoning | future |
| `v1.0` | standalone reproducible resource | long term |

Each number is a different **inferential capability**, not a quantity of
content. The contracts below are deliberately short; the full notes live in
the per-release files.

### v0.3 — executable inference

*The repository no longer merely documents claims and pedagogy; it contains
executable models that can change or delimit the biological inference.*

See [`v0.3.md`](v0.3.md). It was withheld until the state it describes
existed — a release note is a claim about a frozen state, and its verification
table would have been false while findings it declares closed were still open.
Every number in that table was re-measured from the main checkout at the
tagged commit, and the table says so.

Non-goals already fixed for v0.3: comprehensive plasmid biology, an empirical
gene-location layer, scaling-law adjudication, lecture-complete enzymology,
and any website, DOI or research-software maturity.

The release verification table must also **say which checkout it was measured
from**. `evidence/test_check_participant_firewall.py` refuses to run in a
linked worktree — correctly, since it commits — so a table generated from a
worktree would record that refusal as a failure and be right to.

### v0.4 — evolution of genomic address

*What changes when an existing bacterial function moves from its native
chromosomal context into a mobile element?*

The theoretical partner already exists: `models/gene-location/` asks why a
gene might **stay** at one address, and finds that history and priority
effects can lock it there. v0.4 asks the complementary empirical question —
what actually changes when evolution **moves** it.

Three or four deliberately contrasting cases, not a catalogue. Candidates,
chosen because they differ in mechanism and in how strong the ancestry claim
is:

| Candidate | Contrast it provides |
| --- | --- |
| OXA-23 | a near-replicate of the OXA-48 transition in a different genus and vehicle |
| OXA-48-like | same enzyme class, different reservoir, plural source lineages |
| *qnrA* | target protection rather than drug destruction |
| *tmexCD–toprJ* | an entire efflux **module**, not a single enzyme |
| *tet*(X) | a weaker ancestry inference, useful precisely because it is weaker |

**`[U]` None of these has been source-verified in this repository.** They are
reading notes, and they enter `main` only through the normal route: a claim
with a `layer` and a `status`, a DOI-resolved reference, and the scope the
source actually supports. Two scope conditions are already known and must
survive:

- evidence levels differ across the cases and must not be flattened — an
  *identified progenitor* is not a *potential ancestral source*;
- **do not frame this as a universal "environmental resistome → clinic"
  pathway.** Several of these source organisms span environmental and
  clinical niches. The defensible invariant is *native chromosomal context →
  mobile context, often with a major ecological transition*.

Kill criterion, Arrowfield-style: **if stable accession → replicon →
neighbourhood provenance cannot be made explicit, do not release a
quantitative chromosome/plasmid claim.** Fall back to a bounded curated case
study and say so.

#### Release-defining, and supporting

The two are kept apart on purpose, because a milestone is defined by **the new
question the repository can answer** — not by every good artefact made while
reaching it. A version whose contract absorbs each worthwhile side result
stops meaning "evolution of genomic address" and starts meaning "things we
improved after v0.3".

**Release-defining — v0.4 does not ship without these:**

- a verified OXA capture-history case;
- explicit accession → replicon → neighbourhood provenance;
- at least two further contrasting address-transition cases;
- comparable context figures from frozen inputs;
- the model and the empirical work brought together **without either being
  offered as evidence for the other**;
- an adversarial review.

**Supporting, explicitly non-blocking:**

- a PBP / β-lactam mechanism figure built on the ESPMap → frozen-record →
  exported-fixture route, carrying **both** panels: local reaction-site
  similarity, *and* the PBP5 result showing recruitment happening away from
  the active site with stem peptide and β-lactam able to bind at once. A
  version with only the first panel would teach the oversimplification the
  figure exists to correct;
- mechanistic refinement of the lecture's opening arc.

`[I]` The supporting artefacts answer a different question — *what molecular
feature makes a β-lactam enter the PBP reaction pathway, and why is "it looks
like D-Ala-D-Ala" not a sufficient answer* — and they strengthen the teaching
material considerably. They are still not what the version is about. **If the
empirical genomic-address work runs slow, the figure must not be allowed to
stand in for the capability v0.4 names.**

The scientific connection runs the other way, and is worth stating because it
is the reason both belong in the same era:

```text
MOLECULAR    β-lactam → acyl-enzyme chemistry; OXA can hydrolyse it
                 ↓
GENOMIC      chromosomal blaOXA-like → mobilised onto an MGE
                 ↓
ECOLOGICAL   new host, regulation, dosage, transmission
                 ↓
             clinical resistance determinant
```

That chain blocks a common collapse — *"the gene became a resistance gene when
it entered a plasmid"*. The protein chemistry may already have existed. What
changed was the address, and everything the address brings with it.

### v0.5 — competing models of plasmid design space

*Which explanatory model of the size–copy-number relationship survives
comparison?* Single power law against segmented regression against a
two-strategy mixture, with the measurement definitions made explicit and the
published dissent treated as a competing model rather than a footnote.

A bounded negative result — *current data do not identify one mechanism
uniquely* — is a valid release under this framework, because it is a resolved
scientific question.

### v0.6 — dynamical regimes and persistence landscapes

*Can we classify the dynamical regime a plasmid occupies, rather than
estimate a fitness value?* Persistence boundaries, introduction thresholds,
bistability and hysteresis where genuinely supported, recipient depletion,
host × environment dependence — and the discipline that a threshold is not
automatically a tipping point.

### v0.7 — mechanism-first design reasoning

*Objective → mechanism → design lever → cost → failure mode → prediction,
under uncertainty.* The synthetic-biology-facing layer. This stays a teaching
and reasoning resource; the exploratory research machinery lives elsewhere.

### v1.0 — defined by independence, not completeness

*A user who did not participate in the project can reproduce the major
claims, understand their scope, and navigate evidence → model → figure →
interpretation without oral project history.*

Not "all plasmid biology finished". Criteria: several independent case
studies; a stable evidence vocabulary; a stable release procedure;
deterministic or explicitly bounded builds; every relied-upon gate
demonstrated capable of failing; frozen release manifests; version-pinned
examples still reproducible; and no need to know the founding lecture's
context to use the repository.

## Scope boundary

This repository is a teaching and reasoning resource that happens to contain
research-grade checks. Exploratory work — large comparative atlases, sequence
discovery pipelines, model experiments — enters only when it has crystallised
into a small, auditable teaching result. The machinery for producing such
results belongs in the projects that do that work.
