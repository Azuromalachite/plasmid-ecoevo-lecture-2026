# Open findings

Known, specific, unfixed defects in this repository, and what the correction
would be. Updated in the same commit that closes or adds one.

This file exists because the deferral it replaces named a *category*. A
reader of `main` could not previously learn that identified defects with
drafted corrections were outstanding, which is the same failure as a check
with a domain it cannot see: the finding was visible, the tracking was not.

Not an issue tracker, not a schema, not a new vocabulary. One block per
finding.

---

## Open

### OF-1 — the 59/59 validation is not discriminating

**Severity:** major
**Location:** `claim.model.plasmid_invasion_threshold` (`evidence/claims.yml`),
`concepts/fitness-vs-persistence.md`

The invasion threshold's verification note reports that the sign of
γ·n\* − c·ψ − τ predicted invasion in 59 of 59 sampled parameter sets outside
a 5% band. Parameter sets were drawn independently and *then* observed to
fall mostly far from the boundary, so the test could hardly have failed. The
number sounds discriminating and is not.

**Correction:** redesign so the challenge cases are *derived from the
invariant being tested* — generate parameter sets at controlled distances
from the boundary — rather than sampled and hoped over. Report the
sensitivity domain, not the pass count.

### OF-2 — no committed bibliography-key checker

**Severity:** minor
**Location:** repository-wide

Citation keys are cross-checked only by an uncommitted scratch tool.

**Correction:** commit one. It **must enumerate the file types it reads and
fail visibly on types it does not**: during the v0.2 cycle a scratch checker
silently reported three real citations as orphans because it did not open
`.ipynb`, and a committed checker with the same blind spot would have
reported clean on a file it never read.

### OF-3 — the participant policy does not distinguish checks from attestations

**Severity:** minor
**Location:** `docs/participant-material-policy.md`

Some clauses are verifiable against an artifact — no transcripts in Git, no
participant names. Others cannot be: "no emphasis chosen because of what
teams presented" has no diff to measure, nothing that could falsify it, and
no procedure that would catch a violation. It is an attestation by someone
who knows what they did. All clauses are currently presented in the same
declarative voice, so a reader cannot tell which is which.

**Correction:** mark each clause as checked or attested. Knowing which of the
two you are holding is most of the discipline.

### OF-4 — `CONTESTED` has no site on any content page

**Severity:** trivial
**Location:** `evidence/evidence-levels.md` badge table

No registry claim currently carries `status: contested`, which is intended —
under scope-before-status most apparent contradictions turn out to be context
dependence. So the badge is defined and unused.

**Correction:** none yet. Deliberately *not* deleted: `contested` remains a
valid registry status, and removing the badge row while keeping the status
would make the two inconsistent. Revisit if a genuinely contested claim
appears, or if the status itself is retired.

---

## Closed in this changeset

| ID | Was | Fix |
| --- | --- | --- |
| B3 | Heterozygosity attributed to San Millán 2016, whose abstract never uses the word | Attributed to Rodríguez-Beltrán 2018; San Millán's own dual mechanism (mutational supply then gene dosage, "necessary and sufficient") stated separately. Ilhan reconciled by scope, using the paper's own "depending on the selection pressure on newly emerging variants" |
| B4 | Cost mechanism given as "precursors, polymerase and ribosomes", citing a review whose abstract says the mechanisms "remain poorly understood" | Mechanism clause replaced with the review's own position; its supported claim — cost as the main constraint on vertical and horizontal replication — kept. Two sites |
| B5 | "Functional β-lactam, tetracycline and glycopeptide resistance determinants" from permafrost | Genes for three classes *identified*; structure and function shown for **VanA only**. Two sites |
| B6 | Alonso-del Valle's "overall reduction in bacterial fitness" clause dropped | Restored at **seven** content sites, enumerated rather than listed. "overall reduction" previously appeared zero times in the repo. Five landed in the changeset as written; the two parasitism rebuttals in `plasmid-vs-host-fitness.md` were added at merge — see OF-5 |
| B7 | The registry asserted each of five spread steps is independently evidenced | False for two. Note now names which four are evidenced and which two are not; the uncited restriction/CRISPR mechanism is marked unsourced in prose |
| B8 | Eleven source-scope defects | All eleven corrected: Zong (two ORFs split, IS*Shes2* downstream, WCJ25 clinical), Tacão (PCR clone libraries, authors decline the attribution), AmpR vs AmpC, sufficiency→necessity at three sites, Aubert (which promoter, not how much), Dimitriu (RP4 did not evolve), León-Sampedro ("suggesting", not observed), Simonsen (estimator only; the variation claim flagged unsourced), Paulsson (hedged to match the other page), Rodríguez-Beltrán 2021 (removed from the paradox sentence), Kahan (class-name provenance) |
| B9 | "Mass action fails above roughly 10⁶ cells·mL⁻¹" with no citation anywhere | Sourced to [@rodriguezgrande2025encounter], verified: *"T/D ratios saturated at cell densities >10⁶ cells/ml"* — plasmid R64 in LB broth, supplementary figure. Scope carried; figure kept as an order of magnitude, not a boundary |
| A6 | The worked Contrast example runs at 10⁸ cells·mL⁻¹, two orders above that boundary | Made explicit rather than hidden: the mass-action term is used outside its regime there and overstates transfer, so the contrast shows the balance deciding the outcome, not a prediction for a real culture |
| A2 | `pages:` and prose status/layer strings validated in neither direction, which is how a `status: contested` desync survived every check | `check_claim_ids.py` now verifies that every `pages:` path exists and that status/layer strings in content prose match the registry. Negative-tested on a copy **outside** the repo against both defect types |
| A3 | `UNRESOLVED`, `NOT TESTED` and `ILLUSTRATIVE` defined but never used; `evidence-levels.md` claimed the ancestral-selection question "reads as UNRESOLVED on the page" when no page carried the badge | All three given real sites; the claim about the page is now true. `CONTESTED` remains unused — see OF-4 |
| A4 | Misreading status column undefined | Closed before this changeset, in `docs/pedagogy-conventions.md` |

### OF-5 — B6 was recorded as closed at seven sites while it was closed at five

The changeset restored Alonso-del Valle's net-direction clause at five sites
and its own entry claimed seven. The two it missed were the places where the
paper is used to rebut *"plasmids are genetic parasites"*: a bullet and a
misreading-table row in `plasmid-vs-host-fitness.md`. Both stated something
true — the effect is neutral or positive in several wild-type hosts — while
omitting that the overall effect was a reduction. That is the worst place to
drop it, because there the omission is doing the argumentative work. Both now
carry the net direction, and the table row no longer cites the paper for
Bergström's low-transfer-rate claim.

Two things are worth keeping from how this was found.

**The entry was checked against a count, and the count was wrong twice.**
`grep -c` and `grep -oh | wc -l` are line-based, and the clause wraps across a
line break at two of the seven sites, so both instruments reported fewer sites
than exist. The count that settled it normalises whitespace before matching.
A fix verified by an instrument that cannot see part of its domain is the
defect class this repository keeps rediscovering; this time it appeared inside
the document that exists to track it.

**A tracking entry is a claim and needs the same discipline as a page.** "Seven
sites" was written from the enumeration made while planning the fix, not from
the repository after it. A count in a findings table is a number in prose: an
unversioned copy of a computation, and it drifted from the thing it described
in the same commit that introduced it.

---

## Closed in the round-1 review changeset

Adversarial review of the repository at `cb1a249`:
[`../reviews/review-repository-r1.md`](../reviews/review-repository-r1.md). Its
seven findings are F1–F7; the three majors are closed here and the four minors
are carried below as OF-6 through OF-9.

| ID | Was | Fix |
| --- | --- | --- |
| F1 | `figures/README.md` anchored its determinism check to commit `e85bb22` and digest `01b91795…`. The figure changed after that commit, so the shipped digest is `a626bbd3…` and a reader running the documented recipe got a mismatch on a build that is in fact byte-identical | The anchored pair is deleted rather than re-measured. The recipe now compares its two `md5sum` lines with each other and the rebuild against the reader's own commit, so it has nothing that can drift. Why it drifted is recorded in place |
| F2 | B6's eighth site: the case study used Alonso-del Valle with "mostly small, and beneficial in several isolates" and no net direction, in the spread section where the omission does argumentative work — on the page the README calls "if you read one thing, read this" | Rewritten in the registry's wording. Measured after the fix: eight content-page occurrences across eight prose citation sites of the key, whitespace-normalised |
| F3 | The README stated "the plasmid reaching the highest copy number — counted by barcode sequencing — wins", collapsing copies per cell into barcode reads, which `models/copy-number-burden/` explicitly refuses to do and the notebook's QA audit enforces apart in code | The Arena is now described as scored on an endpoint barcode count, with a three-row misreading table separating reads from copy number and from the 5 kb design limit |

### Why B6 reopened, and what the closing instrument has to be

OF-5 closed B6 by counting the restored clause and finding the count short. A
count of the clause can only find sites that *have* the clause. It is
structurally incapable of finding a site that cites the paper and never mentions
the net direction at all, which is what F2 was. The instrument that closed the
finding could not see the case that remained — the same class as the line-based
`grep` above, one level up.

**So the closing instrument for a propagation fix is an enumeration of citation
sites of the key, not a count of the clause.** `grep -n` on
`alonsodelvalle2021variability` over content pages returns nine lines: eight
prose sites, each of which now carries the net direction, and one bare reference
list. Report the denominator, not the count.

---

## Open — added by the round-1 review

### OF-6 — "neutral or positive" drifts from the source and from the registry

**Severity:** minor
**Location:** `concepts/plasmid-vs-host-fitness.md`, the parasitism bullet and
the parasitism misreading row

Both sites render the non-negative hosts as "neutral or positive". The paper
says "even beneficial effects in several isolates"; the registry says
"beneficial in several", as do the three other content pages. "Neutral or
positive" admits hosts where the effect was zero, which the source does not
assert for that set. The misreading row additionally predicates "neutral or
positive" of the *reduction*, which cannot be either.

**Correction:** the registry wording, verbatim, at both sites. Then extend
`check_claim_ids.py` to assert that content-page renderings of
`claim.fitness.cost_is_host_dependent` carry the registry's own words — the
nearest-ID attribution it already does for `status:` and `layer:` is the
mechanism.

### OF-7 — the committed checker does not enumerate the file types it reads

**Severity:** minor
**Location:** `evidence/check_claim_ids.py`

OF-2 requires of a bibliography checker that it "must enumerate the file types
it reads and fail visibly on types it does not". The checker that *is*
committed filters on `.md`, `.yml`, `.py` and says nothing about what it
skipped. `models/copy-number-burden/battle-royale.ipynb` is 3,010 lines inside
a directory the sync check's own `content_dirs` set includes, and is invisible
to it. The notebook carries no claim IDs or status strings today, so nothing is
currently missed — but four bibliography keys are cited *only* there
(`jahn2016copynumber`, `jambor2025checklist`, `midway2020visualization`,
`wong2010datafigures`). OF-2 recorded three; the blind spot has grown.

**Correction:** print the suffix set and a count of skipped files in the summary
block. Adding `.ipynb` to the set is a separate and smaller decision; the
enumeration is what OF-2 asked for.

### OF-8 — the notebook requires NumPy ≥ 2.0 and does not say so

**Severity:** minor
**Location:** `models/copy-number-burden/README.md`, "Running it";
`battle-royale.ipynb` cells 14, 16 and 44

`np.trapezoid` is called in cells 14 and 16. It was added in NumPy 2.0. The
README states no version floor and tells the reader to run top to bottom in
Colab, whose NumPy version they do not choose. The guard that exists —
`assert hasattr(np, 'trapezoid')` — is in cell 44, after both uses, so on
NumPy 1.x the reader meets an `AttributeError` thirty cells before the
assertion that names the requirement.

**Correction:** state `numpy>=2.0`, and move the guard into the configuration
cell so it fires before anything depends on it.

### OF-9 — review documents in the tree perturb the checker

**Severity:** trivial
**Location:** `evidence/check_claim_ids.py`, `reviews/`

A review discusses claim IDs, so `reviews/review-repository-r1.md` raises the
reported "claim IDs cited inline" count from 5 to 7, and a literal placeholder
ID in it made the checker exit 1 until the placeholder was written in a form the
regex does not match. Neither is a defect in the repository's content.

**Correction:** none yet, and deliberately not `SKIP_DIRS`. Skipping a directory
is how a check acquires a domain it cannot see, which is the defect class OF-7
is about. The options worth weighing are reporting content and non-content
counts separately, or keeping review documents outside the tree. Decide once
there is a second round to decide it for.
