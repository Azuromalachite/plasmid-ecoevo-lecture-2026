# Pedagogy conventions

Conventions, not machinery. Nothing here needs a build step; all of it is
about how pages are written.

The project's fifth principle is that we **teach the boundary between
observation and inference, not only the biological fact**. That completes
three layers of provenance:

| Layer | Question it answers | Where it lives |
| --- | --- | --- |
| Scientific | Where did this claim come from? | `evidence/references.bib`, `evidence/claims.yml` |
| Computational | Where did this figure come from? | `figures/source/`, the rebuild recipe |
| Pedagogical | What observation licenses this interpretation? | these conventions |

A learner who finishes a page should be able to say not only what is true,
but which sentence was measured and which was inferred.

---

## 1. Important case studies run predict → commit → evidence → interpretation → limits

The teaching rhythm is **intuition → commitment → counterexample or data →
revised model**. The commitment step is what makes the rest work: a reader who
has not committed to an answer experiences the evidence as information, and a
reader who has committed experiences it as a correction. Only the second
changes a model.

Commitment prompts currently in use:

- An OXA-like enzyme sits on a *Shewanella* chromosome. What phenotype do you
  expect?
- A plasmid imposes a 5% fitness cost. Does it disappear?
- The conjugation rate rises tenfold. Does prevalence necessarily rise?
- Plasmid copy number doubles. Does evolutionary success necessarily improve?

Every one of these has an intuitive answer that is wrong, or wrong without
conditions. That is the selection criterion for a good prompt: **if the
intuitive answer is right, the prompt is not teaching the boundary.**

The **limits** step is not optional. A case study that ends at interpretation
has taught a conclusion; one that ends at limits has taught where the
conclusion stops.

## 2. Important figures carry a "How this can be misread" table

Three columns: **tempting reading**, **status**, **better interpretation**.

A figure compresses, and compression invites inference the evidence does not
support. The table is written from the figure's own most likely misreadings,
not from generic caveats, and it names the status of each misreading using the
vocabulary below.

Current example: the table in
[`../case-studies/shewanella-oxa48.md`](../case-studies/shewanella-oxa48.md),
which covers the pathway figure.

## 3. Five evidence states stay visibly distinct

| State | Means |
| --- | --- |
| **Supported** | Primary evidence directly tests the statement and is consistent with it |
| **Unresolved** | The question is open; no cited evidence settles it |
| **Model-derived** | Follows from a stated model under stated assumptions; not an observation |
| **Illustrative** | Chosen for legibility; carries no calibrated quantity |
| **Not tested** | Nobody has looked, as far as we know |

**Absence of evidence is never presented as evidence of absence.** "Unresolved"
and "not tested" are different from "refuted", and both are different from
each other: unresolved means the question has been asked, not tested means it
has not. Collapsing any of these into "no" is the most common way a teaching
page becomes wrong while every sentence in it stays defensible.

The status vocabulary used in `claims.yml` is defined in
[`../evidence/evidence-levels.md`](../evidence/evidence-levels.md); these five
are the learner-facing projection of it.

## 4. Comparison sufficiency

Before a comparison is used to support a general claim, check it against these
three. Where it fails, mark the page with a **context-mismatch flag** saying
which condition is unmet.

- **One host cannot establish host robustness.** A fitness cost, a transfer
  rate or a phenotype measured in one strain is a point, not a distribution.
- **One environment cannot establish ecological robustness.** Rich medium,
  well mixed, one temperature is a condition, not a world.
- **A single endpoint cannot establish dynamical stability.** One timepoint
  tells you where the system was, not where it settles or whether it stays.

These are deliberately about *sufficiency*, not validity. A single-host study
is good evidence about that host.

## 5. Model output is never silently presented as observation

In learner-facing material, any number or conclusion produced by a model
carries a word saying so, in the same sentence. Not a footnote, not a methods
line further down.

This is the rule most easily broken by accurate writing. A paper that measures
a fitness distribution and then derives persistence conditions from a model
has produced two different kinds of result, and a page that reports both in
one voice has quietly promoted the second.

---

## Claims and prose

Prose **may paraphrase** `claims.yml`. It must preserve three things: the
claim's **scope**, its **uncertainty**, and its **evidence state**. Word-for-word
matching is not required and is not wanted; a page that reads like a YAML
file teaches nothing.

What is automated: a check that every claim ID cited in prose **exists** in
`claims.yml` (`evidence/check_claim_ids.py`). Semantic fidelity is a human
job, because a machine cannot tell whether a paraphrase has quietly widened a
scope, and a check that pretends otherwise would license exactly the drift it
appears to prevent.

### Verification blocks

Load-bearing supported claims — the ones other pages rest on — carry a light
block recording that someone read the source:

```yaml
verification:
  source_checked: true
  checked_against: full_text   # or: abstract
  note: "Fig. 3 / Results"
```

This goes on load-bearing claims only. Adding it everywhere converts a useful
signal into boilerplate, and boilerplate is not read.

## Teaching objects

Three kinds, and they are not interchangeable:

1. **Learner-facing prompt** — a question the reader answers before seeing the
   evidence. Public.
2. **Public explanation** — the page itself. Public.
3. **Instructor-only facilitation notes** — what the common wrong answers
   reveal, how long to leave a silence, when to let an error stand. These may
   not belong in a public repository, and the current recommendation is that
   they stay out of it: a facilitation note that says "most students will
   answer X" is read very differently by a student who finds it than by the
   instructor it was written for.

### A prediction exercise must not show its answer directly below it

Options considered: `<details>` reveals, a separate instructor file, or no
formal answer key.

**Recommended, and implemented in the case study: `<details>` reveals.**
Reasons: the commitment step survives, since the answer is one deliberate
click away rather than in peripheral vision; it works on GitHub without a
build step; it keeps the learner-facing object in one file; and it degrades
honestly — in a plain-text or printed rendering the answer is visible, which
is a known limitation rather than a silent failure.

A separate instructor file would hide answers better but splits the learner
object across two files and pushes the repository toward instructor material
it may not want to host publicly. No answer key at all is defensible for a
live lecture and poor for a self-study reader, which is this repository's
main audience.

### Learner predictions are ephemeral

Predictions a learner writes are **not collected** unless there is an explicit
reason to keep them, a consent model, and a plan for who holds them and for
how long. The default is that a prediction exists in the learner's head and
nowhere else. This repository collects nothing.
