# Adversarial review — repository, round 2

**Artifact:** `plasmid-ecoevo-lecture-2026` at `b4d08f5` (`main`).
**Reviewer:** Claude Opus 5, 3 November 2026.
**Method:** `adversarial-revision-review`, second round.

> **Conflict of interest, stated first because it changes how this should be
> read.** I wrote almost everything under review. Round 1 found seven defects
> in work I had not touched; this round examines three PRs of my own. An author
> reviewing their own revision is the case where adversarial review is least
> reliable — the blind spot that produced a defect is the same one that will
> skip over it — so this review leans on **constructed counterexamples and
> counting** rather than on reading, because those two do not care who wrote
> the code. Where a finding below rests on judgement rather than a measurement,
> treat it as weaker than a round-1 finding would be, and the "What is not
> covered" section at the end names what this method cannot reach.

Evidence labels: `[V]` verified verbatim · `[M]` measured by me · `[I]` inferred
from verified facts · `[U]` not verified, with the reason.

---

## 0. The rejection that holds

Round 1's draft for OF-3 proposed two marks and the repository kept three. That
decision holds, and **G3 below exists only because it held**: `CHECKABLE` and
`ATTESTED` both mean "take the author's word", so collapsing them would have
hidden nothing — but `CHECKED` is a promise of machine verification, and the
moment that promise is made, a clause whose scope exceeds its script becomes a
defect you can point at. The three-mark vocabulary is what makes G3 visible.
Two marks would have left it as prose nobody could falsify.

---

## 1. Disposition audit

Every round-1 finding, re-checked against `b4d08f5` rather than against its
closure note.

| ID | Closure claims | Measured | Verdict |
| --- | --- | --- | --- |
| F1 | anchored digest deleted, recipe self-checking | No digest or commit SHA in `figures/README.md`; rebuild reproduces `a626bbd3…`, tree clean `[M]` | Implemented |
| F2 | net direction at 8 of 8 prose sites | 8 content-page occurrences, 9 grep hits, the ninth a bare reference list `[M]` | Implemented |
| F3 | README separates reads from copies | Barcode framing and a 3-row misreading table present `[V]` | Implemented |
| F4 | registry wording at both sites | No "neutral or positive" on any content page `[M]` | Implemented |
| F5 | — | **Already corrected in-repo**: the "four keys" claim was wrong; it is three. Correction present in both the ledger and the review `[V]` | Corrected |
| F6 | NumPy floor stated, guard moved | Guard in configuration cell 4, absent from QA cell 44; floor stated with its reason `[V]` | Implemented |
| F7 | general optimum documented | `[U]` not re-checked this round | — |
| OF-1 | sensitivity domain replaces 59/59 | Check exits 0; `59/59` appears only as the record of what was replaced `[M]` | Implemented |
| OF-2 | committed checker, domain stated | Exits 0; 12-case mutation test passes `[M]`. **But see G2** | Implemented, and incomplete |
| OF-3 | every clause marked | Marks present on 16 clauses `[M]`. **But see G1** | Implemented, and miscounted |
| OF-6…OF-9 | four minors closed | Each verified in its own file `[V]` | Implemented |

No heading was dropped from `README.md` or the policy between `cb1a249` and
`b4d08f5` `[M]`. Nothing was silently reverted.

---

## 2. Findings

### G1 — the ratio sentence is wrong, in the document whose point is the ratio

**Severity: major.** `docs/participant-material-policy.md:207`,
`docs/open-findings.md:445`.

Both say `[V]`:

> Four clauses are **`CHECKED`**, two **`CHECKABLE`**, and the rest
> **`ATTESTED`**.

Counted `[M]`, excluding the three places that *define* the vocabulary and the
sentence itself:

| | Claimed | Measured |
| --- | --- | --- |
| `CHECKED` | 4 | **6** |
| `CHECKABLE` | 2 | 2 |
| `ATTESTED` | "the rest" | 8 |

The sentence was carried over from a draft that counted only the rows of the
**Never commit** table. Clauses were then marked in three further places — the
"on any branch" scope, the firewall block, and both halves of "Current state" —
and the count was never re-derived. It is a number written from the plan rather
than from the artifact after it: **the OF-5 class, in the changeset whose own
ledger entry says "The ratio is the finding."**

Two things make it worse than an arithmetic slip.

**The instrument you would reach for to recount also undercounts.** The badge is
written `**`ATTESTED`**` everywhere except the firewall block, where it is
`**`ATTESTED`.**` with the period inside the bold `[M]`. A grep for the badge
misses that one, so the obvious way to check the sentence agrees with the
sentence for the wrong reason.

**The error inflates the verified half.** Saying four CHECKED where there are
six understates the claim — but the two uncounted ones are "on any branch" and
"DOI presence", both of which are the *weaker* halves of split marks. The
sentence is wrong in the direction that makes the policy sound more modest than
it is, which is the direction least likely to be challenged.

**Correction.** State 6 / 2 / 8, and normalise the badge spelling so one grep
finds every mark. Better: say "most of this policy is attested" and drop the
count — the sentence does not need a number, and a number in prose here has now
failed the same way twice in two rounds.

**Validation.** Count the marks excluding the definition table and the ratio
sentence; assert the sentence's numbers equal that count. This is three lines
in a script and would have caught it before the commit.

---

### G2 — the bibliography checker silently ignores any key that does not match its shape assumption

**Severity: major.** `evidence/check_references.py:65`.

`KEY_SHAPE = r"[a-z][a-z-]*[0-9]{4}[a-z0-9]*"`. A citation whose key does not
match is not reported as undefined — it is not seen at all.

Constructed on a copy outside the repository `[M]`:

| Planted citation | Checker says |
| --- | --- |
| `@Sanmillan2017costs` in brackets — the real key with a capital S | **no problems**, exit 0 |
| `@van_der2020thing` in brackets — an underscore | **no problems**, exit 0 |
| `@2020orphanyear` in brackets — digits first | **no problems**, exit 0 |

A capitalised key is one of the commonest citation typos there is, and it is
exactly the error this checker was committed to catch. **The checker that
closed OF-2 has an OF-2-shaped blind spot**: it opens the file, and cannot see
part of what is in it. The 12-case mutation test does not catch this because
every mutated key it plants still matches the shape — the test inherited the
assumption it was meant to challenge.

The direction matters. A capitalised key *in the bibliography* would be
reported as an orphan, which is noisy and visible. A capitalised key *in a
citation* is silent. The dangerous direction is the one that is unguarded.

**Correction.** Extract `@` plus a permissive token (`[^\s;,\]]+`) from inside
each group, then validate that token against `KEY_SHAPE` and report anything
that fails as a malformed key rather than discarding it. The group regex already
finds the right text; only the key regex throws it away.

**Validation.** Three mutation cases: a capitalised key, an underscore key, a
digits-first key. All three must go red. Note that this widens what the checker
covers, which `CONTRIBUTING.md` already says requires a new case.

---

### G3 — a `CHECKED` mark promises more than its script delivers

**Severity: minor,** rising to major if anyone relies on the mark.
`docs/participant-material-policy.md:24`.

The clause reads `[V]`: "personal YouTube or channel metadata, **or contact
information**", marked **`CHECKED`**.

`check_participant_firewall.py` covers `youtube.com`, `youtu.be`, `vimeo.com`
and email addresses. Constructed on a copy `[M]`: a page containing an
Instagram handle, a phone number and a Google Drive link produces **"no
problems"**, exit 0.

"Contact information" is broader than "an email address", and the mark does not
say so. This is the one defect class the marking vocabulary exists to prevent —
a reader being unable to tell what is actually verified — reappearing inside the
vocabulary itself.

**Correction.** Split the clause the way the "internal notes" clause is already
split: **`CHECKED`** for links and addresses, **`ATTESTED`** for the rest. The
pattern is in the file one bullet below, so this is a rearrangement rather than
an addition.

**Validation.** For each `CHECKED` clause, name the specific check that covers
it and confirm the clause says nothing the check does not cover. Three of the
six survive that test unchanged; this one does not.

---

### G4 — the OF-9 split was applied to one checker and not its sibling

**Severity: minor.** `evidence/check_references.py`.

OF-9 established that commentary in `reviews/` should not be counted as if it
were content, and `check_claim_ids.py` now reports "on content pages" and
"elsewhere" separately. `check_references.py` has no such split, so a key cited
only from a review counts as cited, and **a review can keep a dead reference
from being reported as an orphan**.

Latent today `[M]`: the round-1 review cites two keys (`jahn2016copynumber`,
`shao2021singlecell`), both also cited from content, so no key is currently
review-only. The exposure grows with each review round.

**Correction.** Either reuse `CONTENT_DIRS` to report the same split, or state
in the checker's docstring that commentary counts as a citation and why. Both
are defensible; silently differing from the sibling checker is not.

---

### G5 — one entry in `UNCITED_SUFFIXES` rules an open-ended class

**Severity: trivial.** `evidence/check_references.py:69`.

`UNCITED_SUFFIXES` is described as "the decision, written down". Four of its
entries name a format. The fifth, `""`, covers every extensionless file that
will ever exist in the tree. Constructed `[M]`: a file named `NOTES` citing a key
that does not exist (`notarealkey2099x`) produces "no problems", exit 0.

Today the extensionless files are `LICENSE`, `.gitignore` and `.gitattributes`,
for which the rule is right. It is the open-endedness that is the defect: the
checker fails loudly on an unruled `.tex` while silently accepting an unruled
`NOTES`.

A note on how this file is written, because it bears on G2 and G5 both. The
planted keys above are named without their brackets. An earlier draft wrote
them as real citations and `check_references.py` flagged one of them — the one
whose key happens to match `KEY_SHAPE`. The other three went through unseen,
which is G2 demonstrating itself inside the document reporting it. Review
documents are part of the corpus the checker reads, and the fix is to write
about citations without writing citations, as the mutation tests already do.

**Correction.** Replace `""` with the three filenames, so a new extensionless
file is unruled and fails like any other unruled type.

---

## 3. What it got right

Verified, not assumed.

**Every other number in the new material is correct** `[M]`. Bibliography 51
entries; 51 pandoc keys, 33 registry keys, 13 footer keys as the OF-2 table
states; 12 and 9 mutation cases as claimed in four separate places. G1 is the
only count that drifted, which is what makes it worth a finding rather than a
pattern.

**The new documentation is itself covered by the checks.**
`models/invasion-threshold/README.md` cites a claim ID and states its `layer`
and `status`; `models/` is in `CONTENT_DIRS`, so the registry↔page sync check
validates those strings, and does `[M]`. The document asserting the model's
status cannot drift from the registry without the checker noticing.

**The firewall checker's refusal is real.** Removing git makes it exit 1 with
"cannot read git history" rather than reporting on the two of five checks that
do not need it `[M]`. This is the rarer discipline: most tools degrade quietly.

**The mutation tests found four defects that reading did not** — a `.gitignore`
substring search that passed on the exact case it existed to catch, two test
files polluting their own corpus, and a miscount in the round-1 review. G2 is
evidence that mutation testing is necessary, not that it is sufficient: the
tests found everything their authors thought to plant, and nothing they did not.

**F5's correction was handled well.** The wrong number was corrected in the
ledger, annotated in place in the review rather than edited away, and the
mutation test carries a case for the specific position where the miscount
happened. That is the right shape for a correction.

---

## 4. Summary

| ID | Severity | Finding | Where |
| --- | --- | --- | --- |
| G1 | major | Ratio sentence says 4 CHECKED; there are 6. Badge spelling makes the recount agree wrongly | `participant-material-policy.md:207`, `open-findings.md:445` |
| G2 | major | Citations whose key fails `KEY_SHAPE` are silently invisible, including capitalised keys | `check_references.py:65` |
| G3 | minor | `CHECKED` on a clause covering "contact information" that the script does not cover | `participant-material-policy.md:24` |
| G4 | minor | OF-9's content/commentary split applied to one checker, not its sibling | `check_references.py` |
| G5 | trivial | `""` in `UNCITED_SUFFIXES` rules an open-ended class | `check_references.py:69` |

Two majors, both in work added to close round-1 findings. Neither touches the
scientific content: the claims registry, the bibliography, the invasion
threshold and the figure build are all unaffected.

---

## 5. The one thing to do first

**G2.** G1 is more embarrassing and is two lines to fix; G2 is the one that
leaves a gate unable to catch what it was built for. A bibliography checker that
cannot see a capitalised key is quiet in exactly the circumstance that matters,
and nothing in the repository would reveal it — the mutation test that exists to
prove the checker can go red inherited the assumption that makes it stay green.

---

## 6. What this review did not cover

Named so the clean sections are not read as cleared.

- **F7** was not re-checked.
- **The scientific content** — claims, sources, the case study, the model's
  biology — was reviewed in round 1 and not re-examined here. This round looked
  almost entirely at the checking apparatus.
- **The `ATTESTED` clauses**, necessarily. No review can reach them.
- **Whether the three-mark vocabulary is the right vocabulary.** I proposed it
  and the author chose it; I am not a useful judge of it.
- **The structural item raised twice and still unfiled**: every round so far has
  produced at least one defect of the form "a number in prose drifted from what
  it describes" — OF-5, F1, OF-1, F5, and now G1. Five instances across two
  rounds, each fixed where it was found. Nothing in `CONTRIBUTING.md` or the
  release process re-derives such numbers. G1 is the fifth instance and the
  first one I introduced myself, which is the strongest evidence available that
  the discipline does not survive contact with a motivated author.
