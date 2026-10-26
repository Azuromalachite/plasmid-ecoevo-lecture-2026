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
| B6 | Alonso-del Valle's "overall reduction in bacterial fitness" clause dropped | Restored at **seven** sites, enumerated rather than listed. "overall reduction" previously appeared zero times in the repo |
| B7 | The registry asserted each of five spread steps is independently evidenced | False for two. Note now names which four are evidenced and which two are not; the uncited restriction/CRISPR mechanism is marked unsourced in prose |
| B8 | Eleven source-scope defects | All eleven corrected: Zong (two ORFs split, IS*Shes2* downstream, WCJ25 clinical), Tacão (PCR clone libraries, authors decline the attribution), AmpR vs AmpC, sufficiency→necessity at three sites, Aubert (which promoter, not how much), Dimitriu (RP4 did not evolve), León-Sampedro ("suggesting", not observed), Simonsen (estimator only; the variation claim flagged unsourced), Paulsson (hedged to match the other page), Rodríguez-Beltrán 2021 (removed from the paradox sentence), Kahan (class-name provenance) |
| B9 | "Mass action fails above roughly 10⁶ cells·mL⁻¹" with no citation anywhere | Sourced to [@rodriguezgrande2025encounter], verified: *"T/D ratios saturated at cell densities >10⁶ cells/ml"* — plasmid R64 in LB broth, supplementary figure. Scope carried; figure kept as an order of magnitude, not a boundary |
| A6 | The worked Contrast example runs at 10⁸ cells·mL⁻¹, two orders above that boundary | Made explicit rather than hidden: the mass-action term is used outside its regime there and overstates transfer, so the contrast shows the balance deciding the outcome, not a prediction for a real culture |
| A2 | `pages:` and prose status/layer strings validated in neither direction, which is how a `status: contested` desync survived every check | `check_claim_ids.py` now verifies that every `pages:` path exists and that status/layer strings in content prose match the registry. Negative-tested on a copy **outside** the repo against both defect types |
| A3 | `UNRESOLVED`, `NOT TESTED` and `ILLUSTRATIVE` defined but never used; `evidence-levels.md` claimed the ancestral-selection question "reads as UNRESOLVED on the page" when no page carried the badge | All three given real sites; the claim about the page is now true. `CONTESTED` remains unused — see OF-4 |
| A4 | Misreading status column undefined | Closed before this changeset, in `docs/pedagogy-conventions.md` |
