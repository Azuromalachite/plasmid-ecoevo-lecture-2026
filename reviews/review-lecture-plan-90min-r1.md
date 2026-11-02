# Adversarial review — 90-minute lecture plan, round 1

**Artifact:** unpublished 90-minute overall lecture plan, 3 November 2026
**Reviewer:** Reviewer 3
**Method:** adversarial revision review
**Repository state consulted:** `main` at `f079aca`
**Scope:** scientific accuracy, prior-finding disposition, timing,
pedagogical architecture, and consistency with the public repository.

**Containment.**
This review contains no participant-derived strategies, team identities,
submission content, or aggregate analysis. It was produced without consulting
participant materials.

---

## What this review is not

It reviews an **unpublished** planning document, not `main`. That distinction
governs what follows it:

- Findings here are defects in a lecture plan. They are **not** entries for
  [`../docs/open-findings.md`](../docs/open-findings.md), which records defects
  in committed public artifacts. Nothing in this review is promoted to that
  ledger.
- Two findings describe a qualification that public repository content *would*
  need if the corresponding material were ever added. Those are recorded under
  [Promotion conditions](#promotion-conditions) with the trigger that would
  make them repository findings.

The other reviews in this directory open with a conflict-of-interest statement
because their author wrote the code under review. The same applies here: the
plan under review and this review have the same author. The mitigation is the
same one round 2 used — the findings below lean on arithmetic, enumeration and
retrieved primary sources rather than on reading, because those do not care who
wrote the document.

**Claim labels:** `[V]` verbatim · `[M]` measured · `[L]` verified against a
retrieved primary source · `[I]` inferred · `[U]` unverified

**Headline:** the revision closed four of seven prior findings cleanly and the
1/e correction has fully propagated. `[L]` The one claim in the new material
that is actively disputed in the literature — the size–plasmid-copy-number
scaling law — is presented as settled, and **the dissenting account is already
written into the plan, two movements earlier**. That is a rearrangement, not
new work.

---

## 1. Disposition audit

`[M]` Each prior finding checked against the text, not against any claim of
having fixed it. The prior round reviewed the previous 60-minute plan on
17 October 2026 and raised seven findings plus one retraction.

| Prior finding | Disposition | Evidence |
|---|---|---|
| **Retraction** — "a 63.2 % sacrifice, always" was wrong | **Implemented and strengthened** | `[V]` The quantitative section names five reasons not to say it; the claims-to-avoid list repeats it |
| **F1** (high) — quantitative section states 12–14 min, schedule gives 9 | **Dissolved, not fixed** | `[M]` The model still has **9 min**. The prose budget that created the mismatch is gone; the only prose minute-figures left both agree with the table |
| **F2** (med-high) — the feasibility escape is correct but unevaluated | **Still open** | `[V]` The plan asks whether \(C^*\) lies inside the feasible range; the production list schedules a re-render; nothing evaluates it |
| **F3** (medium) — stops sit after accumulated overrun, buffer downstream | **Worse** | `[M]` See Finding 3 |
| **F4** (medium) — cut ladder ordered by reluctance, not minutes freed | **Still open** | `[V]` Two unordered lists, no minute attached to any rung |
| **F5** (medium) — SPREAD defined narrowly first | **Implemented** | `[V]` The definition now leads with establishment in a new cellular lineage, then occupied recipients; the `transfer ≠ establishment ≠ persistence ≠ spread` correction now **precedes** it |
| **F6** (low-med) — regime table lacks the segregation-flux mechanism | **Implemented** | `[V]` The protocol-regime gate now carries plasmid-free recipient supply as a small flux |
| **F7** (low) — artifact integrity | **Implemented** | `[M]` Header date matches filename; display math balanced 17/17; inline 11/11; no broken arrow macro |

**Four implemented, two still open, one worse, one dissolved.**

### F1 closed by deletion, which is worth naming

`[M]` The prior finding was a disagreement between a prose budget and a
schedule table. The disagreement is gone because **one side of it was
deleted**. The allocation it concerned did not move: the copy-number model had
9 minutes then and has 9 minutes now, and it now also absorbs the
burden-is-not-one-coefficient material, which has no schedule item of its own.

`[I]` Nine minutes may well be right — the envelope grew from 60 to 90 around
it. But nothing in the document now states what the quantitative core
*requires*, so the next revision has nothing to check the table against. A
budget that can no longer disagree with the schedule is not a budget.

**Correction:** one line stating what the quantitative sections need. If the
answer is 9, the finding closes honestly and stays closed.

---

## 2. Finding 1 — A contested scaling law presented as settled, with the dissent already in the plan

**Severity: high.** The only finding that changes what goes on a slide.

`[L]` The plan's scaling-law section presents two 2025 studies and represents
their contents accurately. But a 2026 preprint by **Liam P. Shaw**, *Plasmid
copy numbers reflect distinct evolutionary strategies* (bioRxiv, doi
`10.64898/2026.06.10.731345`, **not peer reviewed**), names both papers and
argues:

> `[L]` *"both the form and the interpretation of this law are contested"*

> `[L]` *"not through a scaling law, but through the lens of two dominant
> evolutionary strategies"*

> `[L]` *"need not be governed by a universal constraint"*

`[L]` Its technical claim is about **model form**: *"A segmented regression is
a better model"*. Small plasmids lacking active segregation show the inverse
relationship through an inheritance-versus-cost trade-off; larger plasmids with
active partition show *"a much weaker relationship"*, their costs dominated by
the expression of specific genes rather than by size.

### Why this is not a missing citation

`[V]` The plan's own critical lesson is *scaling law = useful null model, not
complete mechanism*. That is the right instinct and a **different claim**.
"Useful null model with residuals" concedes unexplained variance *within* one
functional form. The dissent says the functional form is wrong — that two
regimes with different mechanisms are being averaged into one exponent.

`[I]` A lecture teaching the residual framing has taught the audience to look
for better predictors. A lecture teaching the form dispute has taught them to
ask whether a single law should have been fitted at all. The second is the
transferable skill, and it is what the plan's own Layer 2 exists to deliver.

### The correction is a rearrangement of the author's own material

The plan already teaches, in the movement on how different plasmids solve the
same problems:

```text
Solution A: many copies → redundancy
Solution B: few copies + active partition → deliberate inheritance
```

and already teaches, in the scaling-law section itself:

```text
small plasmid → many copies can be feasible
large plasmid → numerical redundancy becomes expensive
             → low copy + active inheritance becomes more plausible
```

**Those are the same two strategies, and they are the dissent's thesis.** The
plan states the dissenting position twice, `[M]` in movements II and III and
about twenty lecture-minutes apart, without noticing it is the live alternative
to the law presented in between.

The teaching move this makes available is the one the repository is built
around — predict, show the evidence, diagnose the assumption, reconstruct:

```text
single global scaling law
        ↓
tempting interpretation:
"one universal constraint"

but

segmented / two-strategy interpretation
        ↓
many copies + redundancy
versus
few copies + active inheritance
```

**Correction:** extend the boxed lesson to the form question and draw the arrow
back explicitly — *the two solutions you met earlier are what a segmented fit
sees; the single exponent is what a pooled fit sees; which is right is open.*
Nothing new has to be learned; the audience already holds both halves.

**Validation:** if the planned scaling-law figure can be drawn as a single
straight line with no breakpoint and no stated model-form question, the finding
is unaddressed.

---

## 3. Finding 2 — Three quantities are all called copy number

**Severity: high.** `[L]` Primary-source verified; a one-line fix.

The plan places three quantities beside each other and calls them all PCN:

| Where | Quantity |
|---|---|
| The toy model | \(C\) = plasmid copies **per cell / per carrier** |
| Ramiro-Martínez et al. 2025 | PCN from read-depth ratio, nine genera |
| Maddamsetti et al. 2025 | `[L]` *"the number of plasmid copies per the longest chromosome per cell"* |

`[I]` The third is a **ratio to chromosome**, not a per-cell count. Under fast
growth with multifork replication there are several chromosome equivalents per
cell, so the two differ by a growth-rate-dependent factor — and in a growth
competition, that factor is itself under selection.

`[V]` The plan already builds exactly the right apparatus for this, in its
measurement-chain section:

```text
PCN ≠ carrier abundance ≠ total molecules ≠ barcode count
    ≠ host fitness ≠ plasmid fitness
```

That list is the correct slide and is missing the one distinction the new
scaling-law material introduces.

**Correction:** add `copies per cell ≠ copies per chromosome` to that chain,
and state which quantity each study measured when the figure goes up.
`[I]` Without it, the lecture spends one movement teaching that measurement
layers must not be conflated and then conflates two in the next.

---

## 4. Finding 3 — Seven stops declared, three budgeted, and the unbudgeted ones are all late

**Severity: medium-high.** `[M]` The prior F3, recurring and worse.

`[M]` Measured from the architecture:

| Budgeted stop | Cumulative minute |
|---|---|
| first | 18 |
| second | 32 |
| third | 55 |
| — | *nothing from 55 to 85* |

`[V]` The discussion-stop section declares **seven** stops and says *"Use ~4–5
as true pauses and the rest as rhetorical prompts."* `[M]` The schedule budgets
**three**, at 2 minutes each.

`[M]` Stops 5, 6 and 7 — occupied hosts, game theory, dynamics — map to
movements IV and V, i.e. **minutes 55–85, where no stop time exists**. Running
4–5 true pauses therefore costs an unbudgeted 2–4 minutes drawn from a
5-minute reserve, and the overrun lands in the stretch containing the entire
participant-facing payoff.

`[I]` Movements I–III are paced for a lecture with pauses; IV–V are paced for
one without; the stop section assumes they are spread throughout. The three
budgeted stops are also the three easiest to skip, because they fall before
anyone is tired.

**Correction:** decide which four are true pauses, write them into the
architecture as items with minutes, and take the time from the compression list
rather than from the reserve. If movements IV–V genuinely have no pauses, say
so, and rewrite Stop 7 — the sharpest question in the list — as a statement.

---

## 5. Finding 4 — "Two independent studies" overstates the independence

**Severity: medium-high.** `[L]`

`[V]` The section is headed as two *independent* large-scale scaling studies,
and its rhetorical work is their agreement: two datasets, same inverse scaling,
therefore a real constraint.

`[L]` The **datasets** are independent — one covers nine genera and 95 species;
the other 12,006 plasmids across 4,644 genomes including archaea. **The
estimators are not.** Both infer copy number from short-read depth ratios, and
the dissent devotes a section to problems with sequencing-based copy-number
estimates before reaching its interpretation argument. `[I]` Two studies
sharing a method family with a known systematic concern do not validate each
other against that concern; they reproduce it. This is the same independence
question the repository's own checkers are written around — independence has to
be established per shared component, not asserted per artifact.

`[L]` The sampling frames are also not comparable. The nine-genus study
selected genera *"with biotechnological and clinical interest, such as all
members of the ESKAPEE group"*. `[I]` That is a relevance-selected sample: the
right one for the organisms in question, the wrong one to support a universal
statement about natural plasmid diversity, which is what the plan's second
thesis and sixth take-home assert.

**Correction:** retitle to name the difference — two large-scale studies,
different sampling frames, same estimator family — and give each frame a
clause. This **strengthens** the existing "useful null model" lesson by making
it concrete.

> **Added 3 November 2026, from authoritative metadata.** `[L]` The plan
> presents the 2026 theory-and-machine-learning work as a later, separate line
> of support. It is not separate from one of the two 2025 studies:
> [@shahzadi2026determinants] and [@maddamsetti2025scaling] **share two
> authors**, R. Maddamsetti and L. You, and their datasets are close in size
> (11,338 plasmids from 4,317 genomes against 12,006 from 4,644). Taken from
> the CSL-JSON author lists returned by `doi.org`, not inferred.
>
> `[I]` So the section's structure — two independent studies, then independent
> later confirmation — is one research group appearing twice in a sequence of
> three. That does not make any of the work wrong, and the third paper's
> machine-learning approach is genuinely different from the second's
> regression. It does mean the agreement carries less weight than three
> separate entries on a slide imply, and it is worth one clause.

---

## 6. Finding 5 — The designated payoff shares three minutes and is first on the cut list

**Severity: medium.** `[M]`

`[V]` The plan designates a three-part thread spanning the whole lecture —
opening, middle, and a **late payoff** in which cargo leaves the plasmid
vehicle, whose stated purpose is that gene, transposon, plasmid and host can
have different evolutionary fates. `[V]` That statement is also the fourth
take-home.

`[M]` In the schedule, entry exclusion, antiplasmid conflict and cargo escape
**share one 3-minute item**. `[V]` The compression list then names detailed
conflict mechanisms as the **first** thing to compress.

`[I]` So the payoff of the only thread spanning all five movements is allotted
about a minute and is first in line to be cut. The compression list is right
that the first two are expendable — they are examples. The third is not; it is
where \(W_{\rm gene} \neq W_{\rm transposon} \neq W_{\rm plasmid} \neq
W_{\rm host}\) stops being a claim and becomes a story.

**Correction:** name the two expendable subsections in the cut rung instead of
the whole section, and give the payoff its own minute. `[I]` The prior round's
cut list already did exactly this for the plasmid-paradox synthesis, with a
stated reason.

---

## 7. Finding 6 — Two sections have no slot, and one is on the compression list

**Severity: medium.** `[M]`

`[M]` Mapping every numbered subsection to a schedule item leaves two without
one:

- **The small cast of named plasmids** (the high-copy, low-copy-with-partition
  and broad-host-range contrasts). Its movement's items are the success
  framework, multilevel fitness, Arena objectives and a stop. There is no item
  for it. `[V]` A later section develops the same material again, and `[V]` the
  compression list names *extra named plasmid examples* as compressible.
- **Burden is not one universal coefficient**, which must sit inside the model
  item.

`[I]` The first is the prior F4 in a new place: **a cut-list rung that frees
nothing, because what it names was never allotted time.** It is also the
section carrying the dissent's thesis (Finding 1) — so the one section with no
slot is the one the most important finding depends on.

**Correction:** give it a named item. `[M]` Its movement is the thinnest at 14
of 85 minutes, and the success framework recurs throughout the lecture anyway,
so two minutes can come from there.

---

## 8. Finding 7 — Layer 3 is declared the main gap and allocated 14 %

**Severity: medium.** `[M]`

`[V]` The plan states that Layer 3 — using the principles to interrogate a
design — *"was the main gap in earlier versions and is now explicitly included
near the end."*

`[M]` Measured density:

| Content | Minutes | Per unit |
|---|---|---|
| Design audit, 10 subsections | 7 | **42 s** |
| Game theory, 3 subsections | 3 | 60 s |
| Synthesis, 12 questions | 2 | **10 s** |
| **Movement V total** | **12 / 85 = 14 %** | |
| Quantitative movement | 23 / 85 = 27 % | |

`[I]` Closing a gap by adding a section is not the same as closing it by giving
the section time. At 42 seconds a subsection the audit can be read aloud but
not practised, and twelve questions at ten seconds each is a slide to
photograph rather than work through.

`[M]` The 90-minute envelope is confirmed, so the compression path is
contingency rather than the expected case — which makes the fix available from
rungs the plan has already nominated.

**Correction:** either move 3–4 minutes into the audit from those rungs, or
demote the later subsections explicitly to a handout and say so, so the section
promises what the clock can deliver.

---

## 9. Finding 8 — Unresolvable sources, and none of the new material's sources are in the bibliography

**Severity: medium.** `[M]`

`[M]` The literature-cluster section has 29 bullets. Six name design-engineering
schools and are legitimately not papers. Of the remaining 23, **10 cannot be
resolved to a specific paper** — including the theory paper that founds the
scaling-law arc and the evolvability work supporting the sixth take-home.
`[I]` Both are load-bearing and neither names an author.

`[M]` Cross-checking the named sources against this repository's 51-entry,
DOI-verified `evidence/references.bib`:

| Named in the plan | In the bibliography? |
|---|---|
| The three gene-location papers | **absent** |
| The three scaling-law papers | **absent** |
| Rouches 2022; Stewart; Levin; Lopatkin | present |

`[I]` Both blocks of genuinely new content rest on sources outside the only
verified source set the project has. `[V]` The production list schedules a
scaling-law empirical figure; `[M]` in this repository a figure declares
`SOURCE_KEYS` that `evidence/check_references.py` checks against the
bibliography, so **that figure cannot be built to the project's own standard**
until roughly six entries are added and DOI-verified.

`[M]` When this review was written it demonstrated the constraint rather than
describing it: its sources were plain text and URLs, not `references.bib` keys,
because citing them as keys would have made `check_references.py` exit 1 — the
checker working exactly as intended.

> **Closed, 3 November 2026.** Seven entries were added to `references.bib`:
> the three gene-location papers, the three scaling-law papers, and the
> dissenting preprint. `[M]` All seven DOIs were resolved by content
> negotiation against `doi.org`, every one returning HTTP 200, and each
> entry's authors, year, volume and pages were taken from the returned
> CSL-JSON rather than transcribed from a search result. The Sources section
> below now cites them as keys.
>
> `[M]` They are cited **only from this review**, so `check_references.py`
> reports all seven under its commentary-only line — the OF-11 reporting added
> the same day, which until now had nothing to report. That is the correct
> state for a verified source staged for content that does not exist yet, and
> it will clear itself when a page or figure cites them.
>
> One part of the finding does **not** close: the unnamed 2024 theory paper and
> the unnamed evolvability work still cannot be resolved, so they cannot be
> added. `[U]` Naming them is the author's to do.

---

## 10. Finding 9 — The emphasis-confidentiality review is scheduled where it cannot act

**Severity: low-medium, but asymmetric.** `[V]`

`[V]` The production list places *run confidentiality-through-emphasis review*
**fifteenth of sixteen** items, after the slides are built. `[V]` The plan's
own firewall clause forbids participant-derived material in *emphasis choices*
as well as in content.

`[I]` A check scheduled after the work it governs can only produce a choice
between shipping and rework. The material it should examine exists now: the
revision summary lists twelve changes, several of which are emphasis decisions
in exactly that sense — what gets a slide, what recurs, what was demoted. Those
twelve lines are a cheaper and better audit target than a finished deck.

`[I]` It is also the only check in the plan with no stated output. The firewall
clause supplies a test sentence; the production item names no criterion and no
artifact. In this repository's vocabulary that makes it an attestation, which
is fine — but an attestation that was never recorded as having been made is not
yet even that.

**Correction:** apply the test to the revision summary and the running order
now, and record the answer in the plan.

---

## Promotion conditions

`[I]` Nothing above is a defect in committed public content, so nothing above
enters [`../docs/open-findings.md`](../docs/open-findings.md). Two findings
become repository findings on a specific trigger:

| Finding | Trigger | What would then be the defect |
|---|---|---|
| **1** — contested scaling law | A page or figure presenting the size–PCN scaling law is added to the repository | Presenting a single power law without the segmented / two-strategy reading, or without a `status` reflecting that the form is disputed |
| **2** — PCN units | Repository content places a scaling-law PCN beside the toy model's \(C\) | The two quantities set side by side without the per-cell / per-chromosome qualification |

`[M]` Finding 1's trigger would also be the first genuine site for the
`CONTESTED` badge, which `docs/open-findings.md` **OF-4** records as defined
and unused on any content page. OF-4 is not closed by this review — no content
page carries the status yet — but the candidate is now identified, which is
what OF-4 asks for: *"Revisit if a genuinely contested claim appears."*

---

## Summary

| # | Finding | Severity | Basis |
|---|---|---|---|
| 1 | Size–PCN scaling presented as settled; a 2026 preprint disputes the model form, and its thesis is already in the plan | High | `[L]` + `[V]` |
| 2 | Three quantities called PCN; one is per-chromosome, not per-cell; the measurement chain omits it | High | `[L]` |
| 3 | Seven stops declared, three budgeted; the unbudgeted ones fall in the stopless final third | Med-high | `[M]` |
| 4 | "Two independent studies" — independent datasets, shared estimator family, non-comparable frames | Med-high | `[L]` |
| 5 | The designated payoff shares three minutes and is first on the cut list | Medium | `[M]` |
| 6 | Two sections have no slot; one is a cut rung that frees nothing | Medium | `[M]` |
| 7 | Layer 3 declared the main gap, allocated 14 % | Medium | `[M]` |
| 8 | 10 of 23 source bullets unresolvable; none of the new material's sources in the bibliography | Medium | `[M]` |
| 9 | Emphasis-confidentiality review scheduled fifteenth of sixteen | Low-med | `[V]` + `[I]` |
| — | **F1 dissolved:** the prose budget that disagreed with the schedule was deleted; the allocation did not move | — | `[M]` |

---

## What it got right

**1. `[V]` The plan refuses an answer that would have taught well and been
wrong.** This is the hardest correct decision in the document. It names the
weak answer — that conditionally useful genes belong on plasmids because they
can be switched off when not needed — and rejects it, because *a chromosome can
also stockpile genes and regulate them*. The replacement is sharper: regulation
changes **when** a lineage expresses a gene; mobility changes **which** lineage
possesses it. Then it undercuts its own framing further — *gene location itself
is an evolving trait*, and genes do not intrinsically belong anywhere. An
intuitive wrong answer an audience supplies unprompted is the most expensive
kind to displace, and this displaces it with a distinction rather than a
correction.

**2. `[V]` The 1/e retraction propagated completely.** The invariant is kept
and labelled an elegant property of the toy model only, with five reasons it is
not a result about the density award: zero copy number is infeasible, the
comparator is \(C_{\min}\), retention may depend on copy number, the pooled
score is relative, and the optimum may lie outside the feasible range. The
claims-to-avoid list repeats it. `[M]` The prior round's retraction stands and
the surviving statement is the useful one.

**3. `[V]` The feasibility escape is stated in the imperative.** *Always show*
\([C_{\min},C_{\max}]\) *and ask whether* \(C^*\) *exists inside it*, and *a
mathematically valid interior optimum may disappear biologically*. `[M]` I
re-derived the model: \(Q = C\,2^{G_0(1-\beta C)}\) has a stationary point at
\(C^{*} = 1/(\beta G_0 \ln 2)\) for **any** positive \(\beta, G_0\), so the
existence of an interior optimum is a property of the functional form, not a
result. The plan never claims otherwise, and the feasibility question is
precisely what keeps the model falsifiable rather than tautological. F2 is
still unevaluated, but the document says the right thing about it.

**4. `[V]` An unknown protocol is converted into a design criterion.** Both
antibiotic regimes get consequences, then: *do not guess — ask which regime the
design is robust to*. Turning missing information into a robustness question
gives participants something to do with it, which a caveat does not.

**5. `[V]` Terminology discipline, with a discussion stop as its test.**
Threshold, bifurcation, bistability, hysteresis and tipping are separated, with
*tipping* reserved for evidence of abrupt disproportionate change — and then a
stop asks whether observing a sharp persistence threshold justifies calling it
a tipping point. Teaching a vocabulary and simultaneously teaching the
discipline for not over-claiming with it is rare; most treatments do the first
and create the problem.

**6. `[V]` The claims-to-avoid list has sixteen specific entries**, not a
general caution — *all recipients are plasmid-free*, *a threshold is
automatically a tipping point*, *bifurcation, bistability and hysteresis are
synonyms*. `[M]` Every entry I checked corresponds to a claim made somewhere in
the body, so the list is derived from the lecture rather than from generic
prudence.

**7. `[V]` The measurement chain, with a modelling error named in advance** —
*if the abundance term already counts carriers, do not multiply by the carrier
fraction twice*. `[I]` This apparatus is why Finding 2 costs one line instead
of a new slide.

**8. `[V]` Eleven unknown protocol details are enumerated** rather than
gestured at. An enumerated unknown can be checked off when the rules clarify;
an unenumerated one cannot.

**9. `[V]` The scaling-law section already refuses the strong reading** —
*useful null model, not complete mechanism*, with a workflow ending in
residual → mechanism. Finding 1 asks it to go one step further, to the form
question; it builds on this instinct rather than correcting it.

---

## The one thing to do first

**Settle the scaling-law framing before the figure is drawn.**

`[V]` The production list schedules one clean scaling-law empirical figure plus
a mechanism/residual slide. `[L]` If that figure is a single line of slope
−0.65, the lecture presents a contested claim as a constraint, in the movement
this revision was built around.

The fix is not research. It is three sentences and an arrow back to the
two-solutions diagram already in the plan. `[I]` It also converts the weakest
moment in the new material into the strongest available teaching moment: an
audience watching a presenter locate the alternative hypothesis *inside their
own earlier slide* learns more about how inference works than any amount of
"models are conditional".

Then, in order of minutes per unit of benefit:

1. **One line** adding `copies per cell ≠ copies per chromosome` to the
   measurement chain (Finding 2).
2. **Five minutes** deciding which four stops are real and writing them into
   the architecture (Finding 3).
3. **Ten minutes** applying the emphasis test to the revision summary now,
   rather than after the deck exists (Finding 9).
4. **Twenty minutes** adding the six missing bibliography entries, without
   which the scaling-law figure cannot be built to this repository's standard
   (Finding 8).

`[M]` Findings 5, 6 and 7 are rearrangements of existing material and cost no
net minutes; they can wait until a rehearsal shows where the time actually
goes.

---

## Sources

Cited as bibliography keys since 3 November 2026 — see the annotation under
Finding 8 for why they were plain text when this review was written, and for
how the seven entries were verified.

**The scaling-law material.**

- [@ramiromartinez2025universal] — verified verbatim: *"The overall slope was
  k = −0.65 (95% CI: −0.66, −0.63)"*; sampling frame *"nine different bacterial
  genera from two distinct phyla"* and *"95 species with biotechnological and
  clinical interest, such as all members of the ESKAPEE group"*; replicon
  dominance *"Higher copy number replicons were generally recessive … (6 of 22
  cases)"*.
- [@maddamsetti2025scaling] — verified verbatim: *"we define the plasmid copy
  number (PCN) as the number of plasmid copies per the longest chromosome per
  cell"*; 12,006 plasmids across 4,644 genomes.
- [@shahzadi2026determinants] — the plan's 2026 theory-plus-machine-learning
  citation, **now confirmed** by title and DOI rather than inferred, which
  retires the `[U]` this review carried. 11,338 plasmids from 4,317 genomes;
  idealised theoretical exponent −1 with empirical fits near −0.71. Shares two
  authors with the entry above (Finding 4 annotation).
- [@shaw2026strategies] — **preprint, not certified by peer review.** Verified
  verbatim: *"both the form and the interpretation of this law are contested"*;
  *"not through a scaling law, but through the lens of two dominant
  evolutionary strategies"*; *"A segmented regression is a better model"*;
  *"need not be governed by a universal constraint"*.

**The gene-location lineage**, named in the plan and absent from the
bibliography until this changeset. `[L]` Identified by title and DOI; not read
in full for this review, so nothing above rests on their contents.

- [@eberhard1989genes]
- [@svara2011plasmidcarried]
- [@lehtinen2021location]

**This repository:** `evidence/references.bib` (58 entries since this
changeset, all with DOI fields), `evidence/check_references.py`, and
[`../docs/open-findings.md`](../docs/open-findings.md) (OF-4, the unused
`CONTESTED` badge).
