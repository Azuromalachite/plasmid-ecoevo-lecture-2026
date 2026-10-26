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

## Public/private firewall

This repository contains only material derived from published literature,
public competition rules, organizer-approved public protocol information,
generic models and independent teaching examples. It contains **nothing**
derived from Thai SynBio Challenge 2026 participant submissions or pitches: no
team strategies, no frequencies of approaches, no comparisons between teams,
and no emphasis chosen because of what teams presented. The test for every
page is: *could this page have been written by someone who never watched the
pitches?* If not, it does not belong here.

## Contents (v0.1)

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

Citations in pages use `[@key]`, where `key` is an entry in
`evidence/references.bib`.

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

v0.1, under development. No website, CI or DOI yet. Corrections with a
reference are welcome.

## Licence and citation

Content (prose, figures, `evidence/`) is under
[CC BY 4.0](LICENSES/CC-BY-4.0.txt); code (including `figures/source/`) is
under the [MIT licence](LICENSES/MIT.txt). What falls under which, and how to
attribute, is set out in [`LICENSE`](LICENSE).

To cite the project, see [`CITATION.cff`](CITATION.cff).
