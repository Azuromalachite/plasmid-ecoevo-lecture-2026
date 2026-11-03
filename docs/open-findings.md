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

### OF-13 — `q*` is solved and never checked against `[0, 1]`

**Severity:** major
**Location:** `models/gene-location/check_regime_boundary.py`

The script states "Plasmid localisation is favoured for q < q*, chromosomal
for q > q*". `q` is a frequency and lives in `[0, 1]`; `q*` is not constrained
to. Measured over a sweep of the four cost and rate parameters at `x_C = R/2`
(81 analyst-chosen grid cells, **not** a frequency over anything biological):
`q*` lies inside `[0, 1]` in 38, exceeds 1 in 28, and is negative in 15. In
**43 of 81** there is no boundary in range at all — one location wins at every
feasible ecology and the stated boundary is an extrapolation outside its own
variable.

This is OF-1/F2's defect in a new model. `check_feasible_optimum.py` exists
because `C*` was derived and never compared against `[C_min, C_max]`; the same
question was not asked of `q*` three directories away.

**Correction:** report `q*` against `[0, 1]` with a verdict per cell, and
solve the two boundary conditions in closed form as the copy-number script
does. The second is the interesting one: mobility can only repay a cost gap
smaller than the transfer rate itself.

### OF-14 — the nesting test binds to a transcription, not to the file it names

**Severity:** minor
**Location:** `models/gene-location/check_regime_boundary.py`

The nesting check compares against a local literal, `prior = -((c_p - c_c) +
delta * (2 * x_C - R))`, carrying the comment `# from check_priority_effect`.
The transcription is correct today — verified against that file's own
definitions — but nothing reads the file, so if the earlier model changes the
check still passes and still prints a claim about a file it never opened. A
comment is not a binding.

Same class as the firewall mutation target that broke on 3 November: a literal
copied from another file, correct when written, unguarded against the original
moving.

**Correction:** expose `w_P - w_C` at module level in
`check_priority_effect.py` and import it. Both modules are side-effect free at
import time.

### OF-15 — the two "controls" are algebraic consequences of one written line

**Severity:** minor
**Location:** `models/gene-location/check_regime_boundary.py`

`advantage` is written by hand in one statement. `gamma` occurs exactly once in
it, so substituting `gamma = 0` cannot fail to collapse it; `delta` is the only
coefficient on any `x_C` term, so `delta = 0` cannot fail to remove the `x_C`
dependence. Both are properties of how that line is typed. The script oversells
them — "if mobility were doing hidden work elsewhere in the expression this
would fail" is true only of an edit that moves `gamma`.

The algebra is right and the model is not wrong. The assurance is weaker than
the wording, in a repository whose subject is that gap. Contrast
`check_feasible_optimum.py`, which solves for `C*` and compares the solution to
an independently stated closed form.

**Correction:** derive `advantage` from the two fitness expressions rather than
writing the difference directly — then `gamma = 0` tests something — or relabel
them as consistency checks, which costs one word and is defensible.

### OF-16 — the firewall's own test breached the firewall

**Severity:** major
**Location:** `evidence/test_check_participant_firewall.py`
**Status:** occurred, contained, fix proposed in PR #15 (unmerged at the time
of writing)

The mutation test commits caption files on purpose — that is the mutation. It
is safe only because `shutil.copytree` is supposed to produce an isolated
copy, including `.git`, so the `git commit` calls touch the temporary tree and
nothing else.

**In a linked git worktree `.git` is not a directory. It is a one-line file
holding `gitdir: <main>/.git/worktrees/<name>`.** The copy inherits the
pointer, so every git command the mutations run operates on the **real
repository** from inside a temporary directory.

What happened, in this repository: a run from a linked worktree committed
`notes.vtt` to the working branch and `side.srt` to a newly created
`scratch/private` branch, and left `HEAD` on `scratch/private`.

Caption files in history are the first thing
`docs/participant-material-policy.md` forbids, and the first thing
`check_participant_firewall.py` looks for. **The test written to prove the
firewall works put the material the firewall excludes into the history it
guards.**

**Why it was nearly invisible.** It surfaced only because that run exited
non-zero for an unrelated reason and the output was read. For this test the
dangerous outcome is a **pass**: a pass means every mutation ran, and under
this defect "ran" meant "committed to the real repository". A clean run would
have been silent, and the next clean run of the checker would have reported
the caption files as a genuine policy violation with no explanation of where
they came from.

**Contained, verified independently** rather than accepted on report: nothing
was pushed; `scratch/private` does not exist locally or on the remote;
`git log --all --diff-filter=A` over 69 commits and 50 added paths contains no
caption or subtitle file; `check_participant_firewall.py` exits 0. The
matcher used for that search was first shown able to find a caption filename,
because a negative from an unexercised matcher is worth nothing — see
`CONTRIBUTING.md`.

**Fix (PR #15):** the test **fails closed** when `.git` is a file, naming the
cause and the remedy, rather than repairing the pointer. A test that can write
to the repository it tests should refuse, not attempt surgery. Demonstrated
both ways: exits 1 from a linked worktree, still passes 11 of 11 from the main
checkout.

**What this finding is not.** It is not "a test had a bug". The repository's
only *mechanical* guarantee about participant material — the one thing in the
policy marked `CHECKED` rather than `CHECKABLE` or `ATTESTED` — was enforced
by a script whose own test could violate that guarantee undetectably. And it
happened under a workflow adopted the same day **specifically to be safer**.
Isolation was assumed by the test rather than checked by it, which is the
same defect class as a control that cannot fail, with the sign reversed.

**Residue.**

- The fix closes the linked-worktree case by name. It does not establish that
  no other test can write outside its sandbox. `test_check_references.py`
  copies with `ignore_patterns(".git")` and is unaffected, but that is a
  property of that file, not a rule anything enforces.
- A clean `check_participant_firewall.py` run still speaks only for the
  clones it can see. That limit was already stated in the policy; this
  incident is the first time it mattered.

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
currently missed — but three bibliography keys are cited *only* there
(`jambor2025checklist`, `midway2020visualization`, `wong2010datafigures`).

**CORRECTED while closing OF-2.** This entry, and the review finding behind it,
said **four** keys and added `jahn2016copynumber`, concluding that "OF-2
recorded three; the blind spot has grown". That was wrong twice over.
`jahn2016copynumber` is also cited in `models/copy-number-burden/README.md`,
inside the grouped citation `[@shao2021singlecell; @jahn2016copynumber]`, and
the count was taken with a `grep` that matches `[@` and therefore reads a
group as a single citation, silently dropping every key after the first. OF-2's
original three was right, and the blind spot had not grown.

The instrument that produced the wrong number was the one being criticised for
having a blind spot, used without checking whether it had one. The committed
checker does read grouped citations, and `test_check_references.py` carries a
case for the second position of a group specifically because that is where
this was lost.

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

---

## Closed: OF-2 — no committed bibliography-key checker

**Was:** citation keys were cross-checked only by an uncommitted scratch tool.
The correction required that a committed checker **enumerate the file types it
reads and fail visibly on types it does not** — during the v0.2 cycle a scratch
checker silently reported three real citations as orphans because it did not
open `.ipynb`, and a committed checker with the same blind spot would have
reported clean on a file it never read.

**Done:** [`../evidence/check_references.py`](../evidence/check_references.py),
with a mutation test beside it,
[`../evidence/test_check_references.py`](../evidence/test_check_references.py).

### The domain is stated, and an unruled type is a failure

`READ_SUFFIXES` is what the checker opens — `.md`, `.yml`, `.py`, `.ipynb` —
and every run prints it with a count. `UNCITED_SUFFIXES` is the decision that
the bibliography, the citation file, licences and figure output carry no
citations, written down rather than implied by omission. **A suffix in neither
set fails the run.** That is the "fail visibly" half: a file type nobody has
ruled on has appeared, and the response is to rule on it, not to walk past it.
Adding a `.tex` draft to the tree turns the checker red until someone decides
whether it can carry citations.

### Three citation syntaxes, each reporting its own count

A checker that knew only the obvious one would have reported the other two as
orphans:

| Syntax | Where | Distinct keys |
| --- | --- | --- |
| `[@key]` and `[@a; @b]`, including groups wrapping across lines | prose, the notebook | 51 |
| bare keys in `references:` lists | `claims.yml` | 33 |
| `SOURCE_KEYS` | figure scripts | 13 |

Each extractor prints its own count, so one that silently stops matching shows
up as a zero rather than as an absence.

The third of those needed a change to the figure. `figures/README.md` states
that footer keys are BibTeX keys from `references.bib`, and nothing checked it:
a typo would have shipped a dead reference inside an SVG. The footer is now
built from a module-level `SOURCE_KEYS` list that the checker reads by parsing
the script, so the printed footer and the checked list cannot disagree. The
refactor is output-neutral — the SVG rebuilds to the same digest it had before.

### What it does not do

It does not resolve DOIs and does not check metadata against publishers. Both
need the network, and a check that is sometimes skipped because a machine is
offline is a check whose domain moves without anyone deciding. It verifies that
a `doi` field is present and shaped like a DOI. "Every reference has a resolving
DOI whose metadata has been checked", as `README.md` and `CITATION.cff` put it,
stays a human claim about work done by hand, and the script says so in its own
output rather than leaving the reader to assume.

### The checker is known to go red, and for what

It reported clean the first time it ran, which is also what a checker with a
blind spot does. So 15 mutations are applied to a temporary copy, one at a
time, and each must be caught: a clean control, OF-2's own defect reproduced by
narrowing the domain, misspelt keys in prose, in the second position of a
group, in `claims.yml`, in a figure footer and in the notebook, an orphan entry,
a duplicate entry, a missing `doi`, a malformed `doi`, and an unruled file type.
The mutation helpers assemble citations at run time rather than containing them,
so the test does not become part of the corpus — excluding it would have been
the other option, and excluding a file is how a check stops seeing things.

**Residue.** 15 cases is a measured domain of sensitivity, not a proof that
no blind spot remains. It says these defects are not among them.

---

## Closed: OF-3 — the participant policy does not distinguish checks from attestations

**Was:** some clauses are verifiable against an artifact — no transcripts in
Git, no participant names. Others cannot be: "no emphasis chosen because of
what teams presented" has no diff to measure, nothing that could falsify it,
and no procedure that would catch a violation. All clauses were presented in
the same declarative voice, so a reader could not tell which was which.

**Done:** every clause in `docs/participant-material-policy.md` now carries a
mark, and the README's firewall paragraph does too — it held the finding's own
example, so leaving it out would have put the hole exactly where OF-3 pointed.

### Three marks, not two

The finding says checked or attested. There are three, and the third is forced
by a trap worth recording. "No participant names" *is* mechanically checkable:
grep the tree against the participant list. But that list is the material the
policy excludes, so **the check cannot be committed without violating the
clause it checks**. That is not "no transcripts in Git", which any stranger can
verify, and not a judgement nobody can. So: **`CHECKED`** (anyone who clones
can verify), **`CHECKABLE`** (a real procedure whose input cannot live here),
**`ATTESTED`** (nothing could falsify it).

From a reader's position the last two are identical — they take the author's
word. The distinction is about what the author can do, not what the reader
gets, and the policy says so rather than letting `CHECKABLE` read as a weaker
`CHECKED`.

The marks are a local vocabulary for that one file, explicitly unrelated to the
`layer` and `status` axes in `evidence-levels.md`. Those describe claims about
nature; these describe who is in a position to check a promise.

### `CHECKED` had to be made true first

Marking a clause `CHECKED` on the strength of a grep someone ran once would be
an attestation wearing a check's clothes — OF-2's defect, relocated. So the
checked clauses are now run by a committed script,
[`../evidence/check_participant_firewall.py`](../evidence/check_participant_firewall.py):
caption and subtitle formats and guarded directories never added in any
reachable commit on any branch in the clone, the `.gitignore` net for both
still present *and uncommented*, no personal video or channel link in the tree,
no email address outside an explicit allowlist. It reports what it does not
cover in its own output.

11 mutations in
[`../evidence/test_check_participant_firewall.py`](../evidence/test_check_participant_firewall.py)
confirm it goes red for each, including a caption file committed on a branch
that is never pushed — the case that distinguishes a history check from a tree
scan — and confirm it refuses to run rather than cover part of its 5 checks
when git is unavailable.

Two defects were found by writing that test rather than by reading the code.
The `.gitignore` check used a substring search, so commenting a pattern out
left `# *.vtt` still containing `*.vtt` and the check passed on exactly the
thing it existed to catch. And the test's own git-config email was a literal
address, which the checker correctly flagged — fixed by assembling it at run
time, the same move `test_check_references.py` uses, rather than by excluding
the file.

### The ratio is the finding

Four clauses are `CHECKED`, two `CHECKABLE`, the rest `ATTESTED`. OF-3 did not
ask for the policy to be made checkable and it has not been. A firewall against
*judgement* being contaminated cannot be reduced to a grep; a policy containing
only its greppable parts would be a smaller policy, not a better-verified one.
What was wrong was the uniform voice. Publishing the ratio is the honest
version of a promise most of which rests on one person's word.

**Residue.** The checked clauses are a floor: they catch a folder of captions
dropped into the tree. They say nothing about a page written by someone who
watched the presentations and did not notice they were remembering one. Nothing
in this changeset moves that, and nothing could.

---

## Closed in the round-2 review changeset

Round-2 adversarial review of `b4d08f5`:
[`../reviews/review-repository-r2.md`](../reviews/review-repository-r2.md). It
found five defects, all of them in the checking apparatus added to close round
one, and **none in work the review's author had not written** — the review
states that conflict of interest in its own opening and leans on constructed
counterexamples rather than reading, because those do not care who wrote the
code. G1 and G2 are closed here; G3 to G5 are open above as OF-10 to OF-12.

| ID | Was | Fix |
| --- | --- | --- |
| G2 | `check_references.py` extracted citation keys with the same regex it validated them against, so a key that did not already look like a key was not reported — it was not seen. A bracketed `@Sanmillan2017costs`, the real key with a capital S, passed silently, as did underscore and digits-first keys | Extraction now takes any token after an `@` inside a citation group and validates it, reporting a malformed key rather than discarding it. Three mutation cases added, one per shape |
| G1 | The policy and this file both said "Four clauses are `CHECKED`, two `CHECKABLE`". Counted: six, two, eight | The sentence now states 6 / 2 / 8 **and is checked**: `check_participant_firewall.py` counts the badges outside the definition table and fails if they disagree. Two mutation cases added |

### Why G2 survived a mutation test

`test_check_references.py` had twelve cases and every one of them planted a key
that still matched `KEY_SHAPE`. The test inherited the assumption it existed to
challenge, which is the sharpest available demonstration that mutation testing
finds what its author thought to plant and nothing else. The fix is three more
cases; the lesson is that the cases have to attack the *shape* of the
extractor, not only its subject matter.

Two smaller things fell out of the fix. The pandoc group regex, written as one
literal, **matched its own source** and reported itself as a malformed key; it
is now assembled from two pieces, the same move the mutation tests use for
their citations. And citations inside code spans are now stripped before
extraction, because documentation *about* citation syntax is not a corpus of
citations — which also removes the hazard that made two test files fail the
checker during development.

### Why G1 is the fifth of its kind

OF-5, F1, OF-1, F5 and now G1 are all one defect: a number in prose that drifted
from the thing it described. Each was fixed where it was found. G1 is the first
one introduced by the person who had just written that pattern down — the
sentence was carried from a working draft that counted one section, and never
re-derived after three further sections were marked.

So this time the number is not corrected, it is **removed as a separate claim**:
the policy states the ratio in a form a script parses, and the script counts the
marks and fails on disagreement. That is the only move in this sequence that
does not depend on the author remembering. The counts in `CONTRIBUTING.md` and
in this file were re-derived by measurement in the same changeset rather than
retyped, and three of them had already gone stale.

**Residue.** Every other count asserted anywhere in the repository was verified
by measurement this round and is correct, but only the policy ratio is
*enforced*. The mutation-case counts, the bibliography totals and the model's
sensitivity figures are still prose, and still rely on someone re-deriving them.

---

## Closed in the minors changeset

OF-10, OF-11 and OF-12 — the three findings round 2 recorded rather than
fixed. All three were in the checking apparatus or in the document that
describes it, which is where round 2 found everything.

### OF-10 — closed by splitting the clause, which moved the vocabulary

The contact clause now reads **`CHECKED`** for video and channel links and for
email addresses, **`ATTESTED`** for contact information in any other form. The
script's own output gained a line saying the same thing, because the script is
what the first mark means and it was not stating this limit.

The part worth recording is what the split cost. `ATTESTED` was defined as
"nothing could falsify it". "No contact information in any other form" does not
fit that: it **is** falsifiable — find a phone number in the tree and it is
false — but no list of what counts as contact information is complete, so no
committable check decides it. That is a third situation, and the definition was
widened to hold it: *no committable check decides it, either because nothing
could falsify it or because nothing enumerates what would*.

Widening a definition to fit a case is the move that turns a vocabulary into
decoration, so it is stated in the policy under "What the third mark had to
absorb" rather than made quietly. The alternative was available and worse: keep
the single `CHECKED` mark and let the gap between "contact information" and "an
email address" stay invisible. The three marks still separate the same thing —
who can decide a clause — and the first two are untouched.

**Ratio moved** from 6/2/8 to **6 checked, 2 checkable, 9 attested**, and
`check_participant_firewall.py` confirmed the stated line and the marks agree.
That is the G1 enforcement doing its job on the first change after it was
written, which is the only evidence worth having about it.

**No new mutation case.** The fix narrows a claim; it does not widen a check.
The consequence that *is* checkable — the ratio — is already covered by
`mutate_ratio_drift`. A case asserting that the script fails to catch a phone
number would be a test that the repository has a limitation, which the policy
states in words.

### OF-11 — closed, and its own measurement was wrong by the time it was read

The finding said: "the round-1 review cites two keys, both also cited from
content". **Measured on `main` before fixing: `reviews/` contributes zero
citations.** Both bracketed citations in the round-1 review sit inside
backticks, and the G2 fix in the same changeset began stripping code spans
before extraction — correctly, since they are discussion of citation syntax,
not citations. The finding's premise was overtaken by its sibling fix.

The live instance is elsewhere: `docs/open-findings.md` carries one genuine
bracketed citation, so this file is the only commentary citing anything. That
key is also cited from content, so the count today is still zero.

Making it the sixth instance of a number in prose drifting from what it
describes — after OF-5, F1, OF-1, F5 and G1 — except that this one was in the
ledger entry *recording* the pattern.

**Fixed by** splitting the reported count: `COMMENTARY_DIRS = {"reviews",
"docs"}`, keys cited only from commentary counted and **named** in the output.

**Not by reusing `CONTENT_DIRS`**, which is what the correction drafted. The
sibling asks "is this claim ID surfaced to a reader on a page?", so figure
scripts and README fall outside its content set. This checker asks "is this
source doing work in the public material?", and a figure footer citation is
work: it ships inside the SVG. Reusing the set verbatim would have filed all 13
figure-footer citations as commentary — a new inaccuracy introduced by a fix,
which is the defect class round 2 was about. The difference between the two
sets is now a comment in the file. OF-11's complaint was the *silence*, not the
difference.

**Reported, not failed.** A review may legitimately cite a work the teaching
material does not; whether a given case is that or a dead reference is a
judgement, and the script does not make judgements. This matches OF-9, which
also split a count without changing a rule.

### OF-12 — closed by naming the three files

`""` is gone from `UNCITED_SUFFIXES`. Extensionless files are ruled on by name
in a new `UNCITED_NAMES = {"LICENSE", ".gitignore", ".gitattributes"}`, and
anything else extensionless fails as unruled, with a message that names the
file and the set to add it to. An empty suffix is not a type, and the entry
that treated it as one was a standing exemption that read like a decision.

### Both new cases were checked against the unfixed checker

Each fix was reverted on its own in a scratch copy, and the matching case went
red: the OF-12 case exits 0 with `""` restored, and the OF-11 case stays green
without the reporting line. This is the control G2 did not have — twelve
mutation cases passed against the defect they were written to cover — and it is
now written into `CONTRIBUTING.md` as a requirement for new cases rather than
left as a lesson.

The references test gained a third kind of assertion for the OF-11 case:
green **and** saying the thing. Asserting it as a failure would push a
non-defect into exit 1; asserting it as the control would check "no problems"
and ignore the sentence entirely. 17 cases: 1 control, 15 red, 1 noted.

### What these three leave behind

`CONTENT_DIRS` and `COMMENTARY_DIRS` are now two sets in two checkers
partitioning the same tree for different questions, and nothing checks that
every directory falls on one side of each. A new top-level directory is
material to one and invisible to the other, silently. Not filed as a finding
because no such directory exists and inventing a third mechanism to watch two
sets would cost more than it protects — but it is the shape of the next one.

---

## Closed: the ratio mutation carried a copy of the number it was testing

Found on `main` after merging #5 and #6, by running the suite and reading the
exit codes correctly for the first time in that cycle.

### What broke

`mutate_ratio_unparseable` in `evidence/test_check_participant_firewall.py`
named its target in full: `**6 checked, 2 checkable, 8 attested.**`. OF-10's
clause split moved the ratio to nine, and `replace_once` raised. That raise is
not contained to one case — it aborts the run, so **ten other cases stopped
executing**, including every history check. The firewall mutation test on
`main` was not failing one assertion; it was not testing anything.

This is the seventh instance of the defect recorded under OF-5, F1, OF-1, F5,
G1 and OF-11: a number living in prose, copied from somewhere else, drifting
when the original moved. It is the first instance **inside the apparatus built
to catch it**. The test that exists because the policy's ratio had already
drifted once kept its own copy of that ratio.

**Fixed** by matching the shape (`RATIO_RE`) rather than the digits, so a
future ratio change cannot break the case. That is the same correction the
policy received under G1, applied one level up.

### The verification claim in #5 was false

`[M]` The commit message and pull-request body for #5 both state that all four
checkers and both mutation tests exit 0. Measured at `5d3c1d1`, the branch tip
that was merged: `test_check_participant_firewall.py` **exits 1**. The claim
was untrue when it was written.

The cause was not the checker. The verification loop printed its result with

```bash
echo "$(printf '%-50s' "$s") exit $?"
```

where `$?` is evaluated **after** the command substitution, so it reports the
status of `printf` — always 0 — and never the checker's. Every line of that
run read `exit 0` because no other value could be produced. The later runs in
the same cycle used `printf "... exit %s\n" "$s" "$?"`, where the status is
expanded as an argument before `printf` runs, and those were correct; that is
why the merge caught it.

Nothing else in #5 or #6 was wrong: re-run correctly on `main`, the other six
scripts exit 0 and the figure digest is unchanged.

**Recorded rather than quietly corrected**, for the same reason the F5 "four
keys" error was annotated in place rather than edited away. A repository whose
subject is checks that cannot fail should keep the instance where its own
verification could not fail, especially when the instance is its author's.

**Left behind:** the suite is still run by hand, so nothing prevents the next
harness from having the same shape. `CONTRIBUTING.md` now warns about it, which
is an instruction, not a check — in this file's own vocabulary, an attestation.
A committed runner that reports each status itself would make it CHECKED. Not
filed as an open finding because the remedy is a build step this repository has
deliberately not taken, but it is the shape of the next one.
