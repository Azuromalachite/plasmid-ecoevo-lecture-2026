# Adversarial review — repository, round 1 (post-v0.2 changeset)

**Artifact:** `plasmid-ecoevo-lecture-2026` at `cb1a249` (`main`), 7,461 lines
across 23 content files plus a 3,010-line notebook.
**Reviewer:** Claude Opus 5, 2 November 2026.
**Method:** `adversarial-revision-review`. This is a revision review: the prior
round's findings (B3–B9, A2, A3, A6) are dispositioned in
`docs/open-findings.md`, so most of the yield should be in the seams between
what changed and what did not.

**Containment.** Nothing in this file is participant-derived. No team name,
affiliation, submission, transcript or aggregate appears, and nothing from the
private longitudinal analysis framework is reproduced. Competition facts used
below are taken from the public competition site, which is the same source the
`README` already cites.

Evidence labels: `[V]` verified verbatim in the artifact · `[M]` measured by me
· `[L]` verified against external primary documentation I retrieved · `[I]`
inferred from verified facts · `[U]` not verified, with the reason.

---

## 0. No retraction to make, and one rejection that holds

This is my first round on this artifact, so I have no prior recommendation to
withdraw. The disposition that most deserves crediting before anything else is
a **refusal**:

**OF-4 declines to delete the unused `CONTESTED` badge row, and is right.**
`[V]` The reasoning given — the status stays valid in the registry, so removing
the badge while keeping the status would make the two inconsistent — is
correct, and the obvious reviewer move (delete the dead row, the vocabulary is
smaller) would have introduced the desync that `A2`'s checker was written to
catch. I went looking for a second defined-and-unused badge to show the
enumeration was incomplete. There isn't one: `NOT COMPARABLE` is used at
`case-studies/shewanella-oxa48.md:58` `[M]`, and `UNRESOLVED`, `NOT TESTED`,
`MODEL` and `ILLUSTRATIVE` all have content-page sites `[M]`. OF-4's count of
one is right.

---

## 1. Disposition audit

Every prior finding, checked against the repository rather than against the
ledger's own claim.

| ID | Ledger says | Measured | Verdict |
| --- | --- | --- | --- |
| B3 | Re-attributed to Rodríguez-Beltrán 2018 | `claim.copy_number.evolution_not_proportional` cites `rodriguezbeltran2018tradeoffs`, keeps San Millán's dual mechanism separate `[V]` | Implemented |
| B4 | Mechanism clause replaced, two sites | No "precursors, polymerase and ribosomes" anywhere `[M]` | Implemented |
| B5 | VanA only shown functional | `claims.yml` and `case-studies/shewanella-oxa48.md:125–132` both carry the VanA-only restriction `[V]` | Implemented |
| B6 | Net direction restored at **seven** sites | Seven content-page occurrences of "overall reduction", whitespace-normalised `[M]`. **An eighth citation site has none** | **Partially implemented — see F2** |
| B7 | Four of five steps evidenced, two not | `claim.transfer_is_not_spread` names which `[V]` | Implemented |
| B8 | Eleven source-scope defects corrected | Spot-checked four (Poirel/AmpR, Simonsen estimator-only, Kahan provenance, Rodríguez-Beltrán 2021 removed from the paradox sentence) `[V]` | Implemented |
| B9 | Mass-action limit sourced to `rodriguezgrande2025encounter` | Entry present with DOI `10.1371/journal.pgen.1011560`, registered `[M]`; the quoted T/D-saturation sentence not retrieved `[U]` | Implemented, one quote unverified |
| A2 | `pages:` and status/layer sync validated both ways | Checker contains both loops; runs clean on `main` `[M]` | Implemented |
| A3 | `UNRESOLVED`, `NOT TESTED`, `ILLUSTRATIVE` given real sites | All three present on content pages `[M]` | Implemented |
| A6 | 10⁸ vs the 10⁶ boundary made explicit | `concepts/fitness-vs-persistence.md:153–156` states the term is used outside its regime and overstates transfer `[V]` | Implemented |
| OF-5 | B6 closed at five, claimed seven; now seven | Seven confirmed `[M]` | Implemented, and the class is still open — F2 |

Nothing was silently dropped. `[M]` Ten of eleven are implemented as claimed;
the one exception is the finding the ledger itself re-opened.

---

## 2. Findings

### F1 — the figure provenance attestation is stale, and a reader following the documented recipe will conclude the build is broken

**Severity: major.** `figures/README.md`, "Verifying it yourself".

The file gives a five-command recipe for a reader to verify determinism from a
fresh clone, and anchors it:

> Last checked at commit `e85bb22` on Windows: both digests
> `01b91795f4084009ecebf59ce3237c95`, working tree clean. `[V]`

Measured `[M]`:

| | |
| --- | --- |
| `e85bb22` exists | yes — "Scientific hardening: four claim corrections before a tagged release" |
| `figures/` changed since `e85bb22` | yes — SVG ±14 lines, script ±33 lines, `palette.py` added (354 lines), README +65 |
| digest of the shipped SVG at `cb1a249` | `a626bbd391a524ca338d627b90bb4c2c` |
| digest after rebuild | `a626bbd391a524ca338d627b90bb4c2c` — identical |
| `git status --porcelain` after rebuild | empty |

So the **property holds** and the **attestation does not**. A reader who runs
the documented recipe gets `a626bbd3…` where the file promises `01b91795…`,
and the honest conclusion available to them is that the determinism claim has
failed — on the one page in the repository whose job is to let a stranger check
a provenance claim without trusting the author.

This is the defect class OF-5 names in its own closing paragraph — "a number in
prose: an unversioned copy of a computation, and it drifted from the thing it
described" — recurring in the file next door, in the same release cycle.

**Correction.** Either re-measure and update both the commit and the digest at
`cb1a249`, or — better, and available in the repository's own materials —
delete the anchored pair and replace it with the self-checking form the recipe
already implies: *rebuild, then `git status --porcelain`; no output is the
check.* That form cannot go stale, because it compares the build against the
commit the reader is standing on rather than against a remembered number.

**Validation.** `md5sum`, rebuild, `md5sum`, `git status --porcelain` from a
fresh clone at `cb1a249`. If the attestation is kept in anchored form, it needs
a release-checklist line, because it is now the third kind of number in this
repository that has drifted from what it describes.

---

### F2 — B6's class is not closed: the flagship case study still uses the paper without its net direction

**Severity: major.** `case-studies/shewanella-oxa48.md:239–243`.

The page currently reads `[V]`:

> Fitness effects of pOXA-48_K8 across wild-type gut enterobacteria were mostly
> small, and beneficial in several isolates; in a population model, that
> variability itself widened the conditions for plasmid persistence…

The paper's abstract says `[L]`:

> "although pOXA-48_K8 produced an overall reduction in bacterial fitness, it
> produced small effects in most bacterial hosts, and even beneficial effects
> in several isolates"

The subordinating "although" is the sentence's whole structure, and the page
keeps the concession while dropping the main clause. Measured `[M]`: nine
citation sites of `alonsodelvalle2021variability` across content pages; seven
carry the net direction; this one does not; the remaining one is a bare
reference list.

Two things make this the worst of the eight to have missed, and they are the
same two OF-5 gave for its own pair. First, the omission is doing argumentative
work: the sentence sits in the case study's spread section, where the reader is
being shown why pOXA-48 is an epidemic plasmid, and "mostly small, and
beneficial in several" reads as a favourable link in that chain. Second, this is
the page the `README` singles out — "If you read one thing, read this."

The deeper point is about how the previous fix was verified. OF-5 found its two
missed sites by counting the restored clause and finding the count short. A
count of the clause can only find sites that *have* the clause; it is
structurally incapable of finding a site that cites the paper and never mentions
the net direction at all. The instrument that closed B6 could not see the case
that remained — which is, once again, the defect class the repository says it
keeps rediscovering, this time inside the method used to close it.

**Correction.** Add the net direction at `:239`, in the registry's own wording —
`claim.fitness.cost_is_host_dependent` already states it as "an overall
reduction in fitness that is nonetheless small in most hosts and beneficial in
several" `[V]`. No new sentence is needed.

**Validation.** Change the closing instrument: enumerate *citation sites of the
key* and assert each carries the net direction, rather than counting the clause.
`grep -n alonsodelvalle2021variability` over content pages returns nine lines;
eight are prose sites and each should be inspected. Re-run after the fix and
record the denominator, not the count.

---

### F3 — the README states the competition's criterion in the exact terms the repository exists to separate

**Severity: major.** `README.md`, "Context: the Thai SynBio Challenge 2026".

The README says `[V]`:

> teams engineer a 5 kb plasmid carrying a unique DNA barcode, all the
> finalists' plasmids are then grown together in one shared *E. coli* BL21(DE3)
> population, and **the plasmid reaching the highest copy number — counted by
> barcode sequencing — wins**.

The public competition site says `[L]`: "The plasmid with the highest copy
number — counted by DNA barcode sequencing … wins the Arena." So the README is a
faithful paraphrase of the organisers' public framing. That is the problem.

The repository's own model documentation says the opposite `[V]`, twice:

- `models/copy-number-burden/README.md`, what must not be inferred: "**An exact
  mapping from simulated plasmid abundance to barcode read count.** The notebook
  deliberately declines to promote either candidate proxy to the scoring
  observable, because library-input normalisation is not specified."
- the notebook's MODEL STATUS carries the same item under **NOT CLAIMED** `[V]`.

And the notebook's QA audit enforces the distinction in code `[M]`: it asserts
`absolute_plasmids == carrier_cells * 100` and separately that
`0 < barcode_fraction < 1`, under the comment "Measurement readouts are
intentionally distinct APIs". The repository draws the line everywhere except on
its front page, where it reproduces the collapse as fact — copy number per cell,
total plasmid molecules and barcode read fraction are three quantities, and
"highest copy number counted by barcode sequencing" is two of them asserted to
be one.

What makes this hard to see is that the README *looks* like it has handled it.
The next two paragraphs run a scope-discipline argument — "better according to
which objective, over what timescale, in which environment?" — and resolve a
real tension between the competition's objective and the more-copies page. But
that argument is about **objectives**, and the conflation here is about
**observables**. The section that appears to do the work does a different job,
which is why the defect survived a changeset that corrected eleven source-scope
errors elsewhere.

A second, smaller inaccuracy sits in the same sentence `[I]`: read as a
sequence, "teams engineer a 5 kb plasmid … all the finalists' plasmids are then
grown together" states that ≤5 kb constructs are what compete. The size cap
applies to the initial design and synthesis phase; the constructs that reach the
Arena have been through an upgrade phase. `[U]` I could not find this on the
public site — `https://thaisynbiogc.web.app/rules` serves the same single-page
content as the root, with no rules document `[M]` — so the repository does not
currently have a public citation for it.

**Correction.** Two edits, both small.

1. Separate the observable from the quantity, in the repository's own
   vocabulary: *the Arena's endpoint is a barcode read count, which is not the
   same quantity as copies per cell or as plasmid molecules in the flask; the
   organisers' framing collapses them, and keeping them apart is the point of
   `transfer-is-not-spread` and of the model's measurement section.* This is not
   a correction of the organisers — it is the repository declining to inherit a
   conflation, which is exactly what the misreading tables do elsewhere.
2. For the size cap, attribute what the public site supports ("design a 5 kb
   plasmid") and do not extend it to the Arena, or hedge the phase explicitly
   until a citable public rules document exists.

**Validation.** Apply the page checklist in `CONTRIBUTING.md` to `README.md`.
`[M]` The repository has six content pages and two misreading tables; the README
is not treated as a content page and is the single most-read surface in the
repository. A one-row misreading table under that paragraph — *tempting reading:
"the Arena measures copy number" · status: misleading · better model: it
measures barcode reads, which depend on carriers × retention × copies × library
normalisation* — would settle it and costs four lines.

---

### F4 — the net-direction clause drifted while it was being propagated

**Severity: minor,** but it is a scope defect in the sentence that was added to
fix a scope defect. `concepts/plasmid-vs-host-fitness.md:168–170` and `:202`.

Both sites in this file render the non-negative hosts as "**neutral or
positive**" `[V]`. The paper says "even **beneficial** effects in several
isolates" `[L]`, and the registry's own canonical statement says "beneficial in
several" `[V]`, as do the three other content pages `[M]`. "Neutral or positive"
is a different and weaker claim than "beneficial": it admits hosts where the
effect was zero, which the source does not assert for that set.

The table row at `:202` is additionally broken as a sentence `[V]`:

> a clinical plasmid's overall reduction in host fitness was neutral or positive
> in several wild-type hosts

This predicates "neutral or positive" of the *reduction*, which cannot be
either. The prose site thirty lines above gets the grammar right — "an overall
reduction in fitness that was nonetheless neutral or positive in several hosts"
— so the table row looks like the merge-time addition recorded in OF-5 carrying
the wording across without the sentence frame it needed.

**Correction.** Use the registry wording verbatim at both sites.

**Validation.** `[M]` One wording per claim: assert that every content-page
rendering of `claim.fitness.cost_is_host_dependent` matches the registry
`statement` on the words "beneficial" and "overall reduction". This is in reach
of `check_claim_ids.py`, which already does nearest-ID attribution for `status:`
and `layer:` strings.

---

### F5 — the committed checker has the blind spot OF-2 was written to prevent, and the blind spot is already occupied

**Severity: minor.** `evidence/check_claim_ids.py:48–52`.

OF-2 says a committed bibliography checker "**must enumerate the file types it
reads and fail visibly on types it does not**", and gives the reason: a scratch
checker reported three real citations as orphans because it did not open
`.ipynb` `[V]`.

The checker that *is* committed does not meet that standard `[V]`. It filters on
`path.suffix not in {".md", ".yml", ".py"}` and reports nothing about what it
skipped. `models/copy-number-burden/battle-royale.ipynb` is 3,010 lines of
content inside a directory the checker's own `content_dirs` set includes — so
the registry↔page sync loop covers `models/` for Markdown and is blind to the
notebook that is the directory's actual content.

Measured `[M]`:

- the notebook contains **0** `claim.*` IDs and **0** `status:`/`layer:` strings
  today, so nothing is currently being missed by the sync check;
- but **4** bibliography keys are cited *only* in the notebook —
  `jahn2016copynumber`, `jambor2025checklist`, `midway2020visualization`,
  `wong2010datafigures`. OF-2 recorded three; it is four now. The blind spot has
  grown since it was described.

> **Correction, added when OF-2 was closed.** The number above is wrong: it is
> **three**, and OF-2's original count was right. `jahn2016copynumber` is also
> cited in `models/copy-number-burden/README.md`, inside the grouped citation
> `[@shao2021singlecell; @jahn2016copynumber]`. The measurement was taken with
> a `grep` anchored on `[@`, which reads a group as one citation and drops
> every key after the first — so this reviewer criticised an instrument for
> having a blind spot using an instrument with a blind spot, and did not check.
> The finding itself stands; only its illustration was overstated. Left in
> place rather than edited away, because the error is more instructive than the
> finding.

So the risk is latent for claim IDs and live for citations: the notebook is a
file type that the repository's one committed checker cannot see, and content is
accumulating in it.

For the record, the bibliography itself is currently clean `[M]`: 51 entries
defined, 51 distinct keys cited across `.md`, `.yml`, `.py` and `.ipynb`, zero
cited-but-undefined, zero defined-but-uncited. OF-2's defect is the missing
*instrument*, not a missing fix.

**Correction.** Two lines, available now: make the suffix set a module constant
and print it in the summary block alongside `claims defined:`, and have the walk
count files whose suffix is not in the set and print that count. A checker that
says "read 23 files (.md, .yml, .py); skipped 1 (.ipynb)" cannot report clean on
a domain it never opened. Adding `.ipynb` to the set is a separate decision and a
smaller one — the enumeration is what OF-2 actually asked for.

**Validation.** Negative-test it the way A2 was negative-tested: on a copy
outside the repository, put a `claim.<nonexistent>.id` and a wrong `status:` string
in the notebook, confirm the checker still reports clean, then confirm the
skipped-type line makes that silence visible.

---

### F6 — the notebook requires NumPy ≥ 2.0, says it needs "NumPy", and guards the requirement thirty cells after the first use

**Severity: minor.** `models/copy-number-burden/battle-royale.ipynb`, cells 14,
16 and 44; `models/copy-number-burden/README.md`, "Running it".

`np.trapezoid` is called in cell 14 (`host_doublings`) and cell 16 (the
shared-flask gross-growth integral) `[M]`. It was added in NumPy 2.0; the 1.x
spelling is `np.trapz`. The README says only "It needs NumPy, SciPy, pandas and
Matplotlib" `[V]` — no floor — and the instruction is "Open in Jupyter or Colab
and run top to bottom", on a platform whose NumPy version the reader does not
choose.

The guard that exists, `assert hasattr(np, 'trapezoid')`, is in cell 44 `[V]` —
after both uses. On NumPy 1.x the reader meets an `AttributeError` in the middle
of the shared-flask section; the assertion that names the real requirement never
runs. A check placed downstream of the thing it checks cannot catch it.

Verified working as shipped `[M]`: executed end to end under `nbconvert` with
NumPy 2.x — **0 errors across 46 cells**, every QA assertion passing, no
`RuntimeWarning` for PCN outside the calibrated range, and `SAVE_FIGURES=False`
leaving the working tree clean.

**Correction.** State `numpy>=2.0` in "Running it", and move the `hasattr` guard
into the configuration cell where it will fire before anything depends on it.

**Validation.** Execute under NumPy 1.26 and confirm the failure is now the
stated assertion in cell 4 rather than an `AttributeError` in cell 14.

---

### F7 — the documented optimum is the ℓ = 0 special case; the code and the QA assertion use the general one

**Severity: trivial,** reported with its effect size so it can be dismissed on
the numbers rather than on the description.

Cell 6 gives `[V]`:

> When ℓ = 0, the analytic optimum is C\* = 1/(βG₀ ln 2).

`analytic_optimal_pcn` implements `1/(β·g₀·ln(2(1−ℓ)))` `[V]`, and the QA audit
asserts the optimum *increases* with loss `[V]`. I re-derived the general form
and it is correct `[M]`: maximising `G₀(1−βC)·ln(2(1−ℓ)) + ln C` over `C` gives
`C* = 1/(βG₀ ln(2(1−ℓ)))`.

The asserted direction is real but negligible at the shipped parameters `[M]`:
at `G₀ = 10`, `C*` runs 222.0 → 222.3 → 225.2 for ℓ = 0, 0.001, 0.01 — a 1.4%
move across a tenfold change in loss. So there is no misreading risk worth a
table row; there is a documentation gap. A reader who reads only the markdown
has the wrong formula, and a reader who reads only the QA cell has a direction
with no magnitude.

**Correction.** Put the general form in cell 6 with the ℓ = 0 case as its
corollary, and print the three numbers above where the assertion runs.

**Validation.** None needed beyond the existing assertion; it already holds.

---

## 3. What it got right

Verified, not assumed, and ordered by how easy the wrong choice would have been.

**The QA audit places its checks off the inert reference point** `[V]`. The
length law is `β·p·(bp/2686)`, so any test at `bp = 2686` multiplies by one and
passes under almost any bug. The audit says so in a comment — "Fault-sensitive
length-law checks away from the inert ratio=1 reference point" — and then tests
at 3,500 bp and at twice the reference, asserting the burden exactly doubles.
This is the single hardest correct decision in the artifact: the obvious test is
the one that cannot fail, and it was identified as such and replaced.

**The notebook refuses to name a scoring observable** `[V]`, declining to
promote either candidate proxy to the barcode readout because library-input
normalisation is unspecified. The entire model would be more quotable with that
mapping and would be wrong in a way nobody downstream could see. (F3 is the cost
of that discipline not reaching the front page.)

**The Rouches coefficient is quoted with its parameterisation, and the
parameterisation is the point** `[V]`. Four things are recorded that almost
nobody records: that *a* is dimensionless and therefore a fraction *of b*; that
*b* is never defined in words by its own authors, so no absolute per-copy rate
can be quoted; that the authors' resource interpretation is theirs; and that the
abstract's 0.063% and the Results' 0.065% differ, with the Results value chosen
because it is attributable to a figure. The fit population is given as the
830-variant sub-library, not the 1,194-variant library.

**The one calibrated input is kept inside its range by construction** `[M]`.
Cell 10 starts the sweep at `G₀ = 3` with the comment that this keeps the
analytic optimum inside the measured range; at β = 0.00065 the optimum crosses
800 copies at `G₀ ≈ 2.77`, so the bound is tight and deliberate. The table
carries a "Within ~1–800-copy library range" column rather than leaving the
reader to check. Executing the notebook produced no out-of-range warning.

**The firewall holds, measured rather than asserted** `[M]`. No private-framework
vocabulary, no participant-derived content, no team names or affiliations appear
anywhere in the repository. The `.gitignore` is targeted on directory and format
patterns and explicitly refuses the wider `*transcript*` net, with the reason
recorded: a net wide enough to catch the accident would also block a legitimate
page about transcription.

**The determinism property is real** `[M]`: standard-library-only scripts, no
network, byte-identical rebuild, clean tree. The palette self-test passes and
publishes its own failures — `check_union()` reports five unseparable pairs and
"fails by design", and the module records *why* COPY and SPREAD are both blues
rather than hiding the constraint.

**Every DOI resolves** `[M]`: 51 of 51 registered at `doi.org`, confirmed by
content negotiation. Worth recording how that was measured, because my first
instrument was wrong in the repository's own characteristic way: following
redirects through to the publisher returned 25 of 51 as `403`, which is
publisher bot-blocking, not DOI failure. An instrument that could not see part of
its domain reported a 49% failure rate on a bibliography that is clean.

**The worked example's arithmetic is correct** `[M]`: c·ψ + τ = 0.05 × 0.5 +
10⁻⁴ = 0.0251 h⁻¹; γ·n\* = 10⁻⁹ × 10⁸ = 0.1 h⁻¹ and 10⁻¹¹ × 10⁸ = 0.001 h⁻¹.
The invasion condition γn\* > cψ + τ also follows correctly from the stated
model `[M]`, and A6's fix states on the page that the example runs two orders
above the mass-action regime and therefore overstates transfer.

**OF-1 is honest about a check that could hardly have failed** `[V]`, and names
the right correction — derive challenge cases from the invariant, report the
sensitivity domain rather than the pass count. It remains the most valuable open
item in the ledger and nothing in this review displaces it.

---

## 4. Summary

| ID | Severity | Finding | Where |
| --- | --- | --- | --- |
| F1 | major | Stale provenance attestation; documented recipe now reports a mismatch | `figures/README.md` |
| F2 | major | B6's class still open at an eighth, load-bearing site | `case-studies/shewanella-oxa48.md:239` |
| F3 | major | README collapses copy number into barcode count; ≤5 kb extended past its phase | `README.md` |
| F4 | minor | "neutral or positive" drifts from the source and the registry; one row ungrammatical | `concepts/plasmid-vs-host-fitness.md:168, 202` |
| F5 | minor | Committed checker does not enumerate the file types it reads; 4 keys live only in the blind spot | `evidence/check_claim_ids.py` |
| F6 | minor | Undeclared NumPy ≥ 2.0; guard sits downstream of first use | `models/copy-number-burden/` |
| F7 | trivial | Documented optimum is the ℓ = 0 case only (effect size 1.4%) | notebook cell 6 |

Three majors, none of which touches the scientific architecture. F2 and F4 are
sentence-level; F1 is two lines; F3 is a paragraph and a four-line table. The
evidence system, the claim registry, the figure build and the model's internal
discipline all survive this review intact.

---

## 5. The one thing to do first

**F1.** Not because it is the most interesting — F3 is — but because it is the
only finding that makes a correct thing look broken to a stranger. Every other
defect here is visible to someone who already trusts the repository; F1 is
visible to someone deciding whether to.

---

## Sources

- Alonso-del Valle et al. 2021, *Nat Commun* 12:2653 —
  https://www.nature.com/articles/s41467-021-22849-y (abstract retrieved and
  quoted verbatim in F2 and F4)
- Rodríguez-Grande et al. 2025, *PLOS Genet* 21(2):e1011560 —
  https://doi.org/10.1371/journal.pgen.1011560 (registration confirmed; the
  T/D-saturation sentence not retrieved — `[U]`)
- Thai SynBio Challenge 2026 public site — https://thaisynbiogc.web.app/
  (public framing quoted in F3; no rules document served at `/rules`)
- NumPy 2.0 release notes, `np.trapezoid` (F6)
