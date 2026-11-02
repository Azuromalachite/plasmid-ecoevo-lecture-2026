# Plasmid Eco-Evo

**Educational ecology and evolution of plasmids and mobile DNA**

Plasmid Eco-Evo is an educational project about the ecology and evolution of
plasmids and mobile DNA. It began around a 2026 lecture on plasmid fitness but
is being developed as a reusable collection of biological case studies,
conceptual frameworks, quantitative models and teaching figures. The central
idea is simple: plasmid success is not a property of DNA sequence alone.
Replication, host physiology, horizontal transmission, ecological
interactions, environmental context and evolutionary history jointly determine
whether a plasmid persists, spreads or disappears. The project therefore treats
plasmids not only as molecular vectors, but as evolving ecological entities.

## What success looks like

A reader who works through this material should move from

> "a plasmid is a circular DNA vector"

to

> "a plasmid is an evolving lineage whose fate emerges from replication, host
> reproduction, horizontal transmission, ecological interactions and
> environmental context."

## Principles

1. **The subject generates the structure.** Pages, directories and models
   exist because the biology needs them, not because a template had a slot.
   Directories stay empty until there is something worth putting in them.
2. **Preserve provenance.** Every factual statement traces to a published
   source in [`evidence/references.bib`](evidence/references.bib), and every
   reference there has a resolving DOI whose metadata has been checked.
3. **Separate evidence from interpretation.** Pages keep four layers apart:
   **Source** (what a paper reports), **Interpretation** (our synthesis),
   **Model / prediction** (what a stated model implies under stated
   assumptions) and **Observation** (data that tests a prediction). Reusable
   claims are tracked with a status in [`evidence/claims.yml`](evidence/claims.yml);
   the status vocabulary is in [`evidence/evidence-levels.md`](evidence/evidence-levels.md).
4. **Formalize gradually.** Prose first, then diagrams, then equations, then
   simulations, and only when the earlier layer has shown what the later one
   should answer. Every model and figure declares its assumptions, parameters,
   regime, and whether it is illustrative or calibrated.
5. **Teach inference control and model updating, not merely facts or
   surprise.** A reader should finish a page reasoning differently about the
   next case, not just holding one more fact. This is the third layer of
   provenance: scientific provenance asks where a claim came from,
   computational provenance asks where a figure came from, and pedagogical
   provenance asks what observation licenses an interpretation. The
   conventions that implement it — predict before evidence, diagnose the
   assumption rather than just correcting the answer, a
   "how this can be misread" table on important figures, seven distinct
   evidence states, comparison sufficiency, and never passing a model output
   off as an observation — are in
   [`docs/pedagogy-conventions.md`](docs/pedagogy-conventions.md), with the
   page-by-page checklist in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Context: the Thai SynBio Challenge 2026

This project grew up alongside the [Thai SynBio Challenge 2026](https://thaisynbiogc.web.app/),
subtitled "The Arena", organised in collaboration with the Thailand Synthetic
Biology Consortium, SIAT and Naresuan University. Its design task is unusually
well matched to this material: teams design a 5 kb plasmid carrying a unique
DNA barcode, the finalists' constructs are then grown together in one shared
*E. coli* BL21(DE3) population, and the Arena is scored by sequencing those
barcodes at the endpoint. A distinctive rule makes it a game as well as an
experiment: after finalists are announced, strategy videos are released to the
whole cohort, so teams can revise their designs against their rivals' before
synthesis. The final is hosted at BMB 2027 in May 2027.

The Arena deliberately makes an endpoint barcode count the winning criterion
under a defined experimental regime. That makes it useful to read alongside
[more copies is not always better](misconceptions/more-copy-is-always-better.md):
the competition asks which design maximises a specified quantity in a shared
flask, whereas the concept page asks when higher copy number improves, or
harms, the longer-term success of a plasmid lineage. Neither question
invalidates the other; they operate at different scopes.

That is worth sitting with, because the apparent clash is a good test of
scope discipline. A reader may reasonably object: *this repository says more
copies is not always better, and the competition says highest copy number
wins.* Both are true, and the way to see it is to ask the question neither
statement carries on its face — **better according to which objective, over
what timescale, in which environment?** An optimisation target defined for a
scoring regime is not a general criterion of biological fitness, and noticing
that difference is most of what this repository is trying to teach.

There is a second collapse to notice, and it is about **measurement** rather
than objective. The organisers describe the winner as "the plasmid with the
highest copy number — counted by DNA barcode sequencing". That names two
quantities and treats them as one. Copies per carrier cell, total plasmid
molecules in the flask, and barcode read fraction are three different things:
reads at the endpoint reflect carrier abundance, retention, copies per carrier
*and* library normalisation, and the public rules do not specify the last of
those. This repository therefore describes the Arena as scored on a barcode
read count and does not call that readout a copy-number measurement — the same
refusal the model makes explicitly in
[`models/copy-number-burden/`](models/copy-number-burden/), which declines to
promote either candidate proxy to the scoring observable. Keeping cells,
plasmids and reads apart is the same discipline as
[transfer is not spread](misconceptions/transfer-is-not-spread.md), applied to
an instrument instead of a process.

**How this can be misread.**

| Tempting reading | Status | Better model |
| --- | --- | --- |
| The Arena measures plasmid copy number. | **Misleading** | It measures barcode reads at the endpoint. Reads reflect carrier abundance × retention × copies per carrier × library normalisation. Copy number is one factor among four, and the normalisation is not specified in the public rules. |
| A higher endpoint barcode share means a higher copy number per cell. | **False** | A lineage can win on carrier abundance or retention at a lower copy number, which is the trade-off [more copies is not always better](misconceptions/more-copy-is-always-better.md) describes and the model computes. |
| The constructs competing in the Arena are the 5 kb designs. | **Unsupported** | The 5 kb limit is stated for the design submission. The public rules do not establish that it describes the constructs that reach the Arena, so this repository does not assert it either way. |

## Public/private firewall

This repository contains only material derived from published literature,
public competition rules, organizer-approved public protocol information,
generic models and independent teaching examples. It contains **nothing**
derived from Thai SynBio Challenge 2026 participant submissions or
presentations: no team strategies, no frequencies of approaches, no
comparisons between teams, and no emphasis chosen because of what teams
presented. The test for every page is: *could this page have been written by
someone who never watched the presentations?* If not, it does not belong here.

**Those last three are attestations, not checks.** "No frequencies of
approaches", "no comparisons between teams" and "no emphasis chosen because of
what teams presented" have no diff to measure, nothing that could falsify
them, and no procedure that would catch a violation. They are statements by
the author about their own conduct, and saying so is the point: the clauses
either side of them *are* machine-checked, and a reader should not have to
guess which is which.

Participant-derived material is excluded **by default and on every branch**,
draft and unpublished branches included, and a publicly accessible video is
not by itself permission to republish an identifiable transcript. The
file-shaped half of that is checked by
[`evidence/check_participant_firewall.py`](evidence/check_participant_firewall.py)
over every branch in the clone. What may eventually be included, how
permission is scoped, why an omission in a presentation is never evidence of
absence, and which clause carries which mark, are all set out in
[`docs/participant-material-policy.md`](docs/participant-material-policy.md).

## Contents

| Path | What it is |
| --- | --- |
| [`case-studies/shewanella-oxa48.md`](case-studies/shewanella-oxa48.md) | From an environmental *Shewanella* chromosome to a clinical carbapenemase plasmid |
| [`concepts/copy-carry-spread.md`](concepts/copy-carry-spread.md) | Three routes by which a plasmid lineage gains or loses copies |
| [`concepts/plasmid-vs-host-fitness.md`](concepts/plasmid-vs-host-fitness.md) | Why what is good for the plasmid and what is good for the cell diverge |
| [`concepts/fitness-vs-persistence.md`](concepts/fitness-vs-persistence.md) | Why a measured fitness cost does not by itself predict fate |
| [`misconceptions/more-copy-is-always-better.md`](misconceptions/more-copy-is-always-better.md) | Copy number has costs, not just benefits |
| [`misconceptions/transfer-is-not-spread.md`](misconceptions/transfer-is-not-spread.md) | A transfer event is not a spreading lineage |
| [`evidence/`](evidence/) | Bibliography, tracked claims, evidence levels |
| [`figures/`](figures/) | Figures generated from source; see [`figures/README.md`](figures/README.md) |
| [`docs/pedagogy-conventions.md`](docs/pedagogy-conventions.md) | How pages teach inference control and model updating |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Rigour checklist for any new or edited page |
| [`models/copy-number-burden/`](models/copy-number-burden/) | Executable copy-number/burden model; the Battle Royale scenario |
| [`models/invasion-threshold/`](models/invasion-threshold/) | The invasion condition γ·n\* > c·ψ + τ, derived symbolically and tested against cases built at known distances from the boundary |
| [`docs/participant-material-policy.md`](docs/participant-material-policy.md) | What participant-derived material may never enter Git, and on what terms anything could |

Citations in pages use `[@key]`, where `key` is an entry in
`evidence/references.bib`.

## Reading paths

Light navigation, not a curriculum. Each path is an order to read existing
pages in; none is a prerequisite for another.

**Start here — about 15 minutes.**
[The *Shewanella* → OXA-48 case study](case-studies/shewanella-oxa48.md),
including the prediction prompt at the top and the "how this can be misread"
table at the bottom. If you read one thing, read this.

**Plasmid fitness → persistence.**
[Plasmid vs host fitness](concepts/plasmid-vs-host-fitness.md) →
[fitness vs persistence](concepts/fitness-vs-persistence.md), including the
worked example "a plasmid imposes a 5% cost: does it disappear?" →
[more copies is not always better](misconceptions/more-copy-is-always-better.md).
Why a measured cost does not tell you what happens next.

**Mobility and AMR.**
[The case study](case-studies/shewanella-oxa48.md) →
[COPY, CARRY, SPREAD](concepts/copy-carry-spread.md) →
[transfer is not spread](misconceptions/transfer-is-not-spread.md). How a gene
becomes a clinical problem without its chemistry changing.

**Dynamical landscapes.** *(Later — not all of the pages this path will
connect exist yet.)* The terminology discipline in
[fitness vs persistence](concepts/fitness-vs-persistence.md) is the seed:
persistence boundaries, what a threshold does and does not license, and why
"tipping point" is a stronger claim than it looks.

## Provenance, including of the build

Principle 2 asks where a *claim* came from. The same question applies to the
artefacts: a figure whose provenance cannot be checked is as weak as a
sentence without a citation. Supply-chain provenance is the computational
counterpart of the claims-and-evidence system.

What holds today: every figure is generated from a committed script, with no
network access and no non-standard-library dependency, and the output is
byte-identical on rebuild — verifiable from a fresh clone with the recipe in
[`figures/README.md`](figures/README.md).

On the roadmap, each step only when the project actually reaches it: build
attestations ([GitHub Artifact Attestations](https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds),
SLSA v1 provenance via Sigstore) once there is a release workflow to attest;
a reusable build-and-attest workflow if this becomes a regularly released
resource; SBOMs, pinned Actions and Zenodo archiving only if datasets or
software here become research outputs in their own right.

## Status

Latest tagged release: v0.2. No website, CI or DOI yet. Corrections with a
reference are welcome.

## Licence and citation

Content (prose, figures, `evidence/`) is under
[CC BY 4.0](LICENSES/CC-BY-4.0.txt); code (including `figures/source/`) is
under the [MIT licence](LICENSES/MIT.txt). What falls under which, and how to
attribute, is set out in [`LICENSE`](LICENSE).

To cite the project, see [`CITATION.cff`](CITATION.cff).
