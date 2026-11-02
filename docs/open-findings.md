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

## Closed in the minor-findings changeset

OF-6 through OF-9 were opened by the round-1 review and closed in the changeset
that followed it. Each is kept below with what it was, followed by what was
done. The one piece deliberately not done is named inside OF-6.

| ID | Fix |
| --- | --- |
| OF-6 | Both sites rewritten in the registry's wording; the misreading row no longer predicates "neutral or positive" of the reduction. The automated half is deliberately **not** done — see below |
| OF-7 | The checker now names the file types it reads and tallies, by extension, the ones it does not. Negative-tested outside the repository against three defects |
| OF-8 | `numpy>=2.0` stated in "Running it" with the reason; the guard moved from QA cell 44 into configuration cell 4, and verified to fire on a real NumPy 1.26.4 |
| OF-9 | The inline-citation count is split into "on content pages" and "elsewhere", which restores the content figure to 5 and keeps review commentary visible as commentary. Not fixed with `SKIP_DIRS` |

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

**Done:** both sites now carry the registry's wording — "an overall reduction
in fitness that was nonetheless small in most hosts and beneficial in several"
— and the misreading row predicates it of the plasmid rather than of the
reduction.

**Deliberately not done: the automated half.** The review proposed extending
`check_claim_ids.py` to assert that content-page renderings of a claim carry
the registry's own words. There is no honest way to do that with what the
registry has. `statement` is a paragraph, not a phrase, so it cannot be matched
against prose; making it work would mean adding a per-claim list of required
wordings, which is a new registry field, a new vocabulary, and a second place
for the canonical phrasing to live and drift from. It would also be the
semantic-fidelity check the module docstring says this tool must not pretend to
be. **What this leaves:** nothing automatic catches a paraphrase that keeps the
citation and loses the scope. That is the gap the review's F2 walked into and it
is still open as a *class*; the closing instrument named under F2 — enumerate
citation sites of the key, inspect each — is a human procedure and is currently
the only one. Revisit if a third instance appears, which would be evidence the
procedure is not enough.

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

**Done:** every run now opens with the number of files read and the types it
read them as, followed by a tally of what it skipped, by extension — currently
`(no suffix) x3, .bib x1, .cff x1, .ipynb x1, .svg x1, .txt x2`. `READ_SUFFIXES`
and `CONTENT_DIRS` are module constants rather than literals buried in two
loops.

`.ipynb` was **not** added to the read set. That is the separate and larger
decision OF-2 distinguishes: enumeration makes the blind spot legible, widening
the domain changes what the tool claims to cover, and the second should be
argued on its own. The tally is what makes it arguable.

**Negative-tested** on a copy outside the repository, against three constructed
defects: a bogus claim ID with a wrong `status:` planted in the notebook —
still reports "no problems", but the run now says `.ipynb x1` was not read, so
the silence is visible rather than mistakable for coverage; the same ID planted
in a content page — caught, exit 1; a `status:` desync on a content page —
caught, with the nearest-ID attribution naming the right claim.

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

**Done:** "Running it" states **NumPy ≥ 2.0** and says why, naming the two
cells and the 1.x spelling. The guard moved from QA cell 44 into configuration
cell 4, where it raises a `RuntimeError` that reports the version found and the
command to fix it, instead of a bare `assert` thirty cells downstream.

**Verified** by running the guard's condition under a real NumPy 1.26.4
(`uv run --python 3.11 --with numpy==1.26.4`): it fires, with the installed
version in the message. The notebook still executes end to end under NumPy 2.x.
The point is not that the assertion exists — it existed before — but that a
check downstream of its own subject cannot catch what it names.

### OF-9 — review documents in the tree perturb the checker

**Severity:** trivial
**Location:** `evidence/check_claim_ids.py`, `reviews/`

A review discusses claim IDs, so `reviews/review-repository-r1.md` raises the
reported "claim IDs cited inline" count from 5 to 7, and a literal placeholder
ID in it made the checker exit 1 until the placeholder was written in a form the
regex does not match. Neither is a defect in the repository's content.

**Done:** the count is split. The checker now reports
`claim IDs cited inline: 5 on content pages, 2 elsewhere`, which restores the
content figure to what it was before `reviews/` existed and keeps the
commentary visible as commentary. The split uses `CONTENT_DIRS`, the same
constant the registry↔page sync check uses, so the two cannot disagree about
what a content page is.

**Deliberately not `SKIP_DIRS`.** Skipping a directory is how a check acquires
a domain it cannot see, which is the defect OF-7 is about; a count that is
wrong is better than a file that is invisible. Reviews stay in the tree and
stay read — a bogus claim ID written in one is still reported, as it should be.

---

## Closed: OF-1 — the 59/59 validation is not discriminating

**Was:** the invasion threshold's verification note reported that the sign of
γ·n\* − c·ψ − τ predicted invasion in 59 of 59 sampled parameter sets outside a
5% band. Parameter sets were drawn independently and *then* observed to fall
mostly far from the boundary, so the test could hardly have failed. The number
sounded discriminating and was not.

**Done:** the check is now a committed script,
[`../models/invasion-threshold/check_invasion_threshold.py`](../models/invasion-threshold/check_invasion_threshold.py),
with [a README](../models/invasion-threshold/README.md) stating what it does
and does not establish. Three things changed, and the first is the one the
finding was about.

**1. The cases are constructed from the invariant, not sampled near it.**
Everything except the transfer rate is fixed, γ\_crit is solved for, and γ is
set to γ\_crit·(1 + ε) for a ladder of signed ε. The predicted eigenvalue is
then exactly ε·(c·D + τ), so ε is a dimensionless signed distance from the
threshold with a known consequence, and the full nonlinear system is integrated
in ln *P* to measure the realised rate against it.

**2. A sensitivity domain replaces the pass count.** The predicted rate is
recovered to better than 6 × 10⁻⁶ relative for |ε| ≤ 1. The *sign* — which is
what the condition asserts — is recovered down to |ε| ≈ 10 × *P*₀/*n*\*,
measured at 1e-5, 1e-7, 1e-9, 1e-11 and 1e-13 for inocula of 1e-4 through
1e-12 of *n*\*. The lower edge is a property of the question rather than of the
arithmetic: an eigenvalue describes a vanishing class, and a class you can
simulate is not vanishing. The evidence for that reading, rather than a solver
floor dressed as physics, is that the edge tracks the inoculum at a constant
ratio across eight orders of magnitude and the rate error scales the same way.
Above |ε| ≈ 10 the linearisation stops describing the system, as it should.

**3. The derivation became a derivation.** The symbolic half now *derives* the
eigenvalue instead of asserting it, and checks the step that matters: the
plasmid row of the Jacobian is `[0, 0]` off the diagonal at the plasmid-free
equilibrium, so the eigenvalue is γ·n\* − c·ψ − τ exactly and not to leading
order. The note previously claimed "symbolic residual 0" with nothing committed
that computed it — the same gap as a bibliography checked only by a scratch
tool (OF-2).

**The old design is measured rather than just criticised.** The script
reconstructs independent log-uniform sampling of the transfer rate and reports
what it explored: a median |ε| of about 1.0, 14% of draws two or more orders
from the boundary, and 1.1% inside the 5% band the old test discarded. That is
the quantitative form of "could hardly have failed", and it is what makes the
replacement worth its length.

**What this leaves.** `status: supported` still means supported *within* the
model. None of the model's assumptions — mass action, well-mixedness,
per-unit-time segregation, transconjugants transferring like donors, constant
cost — is tested by any of this, and the README says so in its own section
rather than leaving it to be inferred.

**Residue: the ladder can still run out.** The script fails rather than quoting
a resolution that sits at the bottom of its own ε ladder, because that number
would be the instrument's floor and not the system's. This fired once during
development, at *P*₀/*n*\* = 1e-12, and the ladder was deepened until the row
had headroom. The guard is the durable part; the current depth is not.
