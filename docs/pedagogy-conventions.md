# Pedagogy conventions

Conventions, not machinery. Nothing here needs a build step; all of it is
about how pages are written. The checklist that applies them page by page is
[`../CONTRIBUTING.md`](../CONTRIBUTING.md).

The project's fifth principle is to **teach inference control and model
updating, not merely facts or surprise**. A page that leaves a reader with a
memorable fact has done part of the job. A page that changes how they reason
about the next case has done the job.

This completes three layers of provenance:

| Layer | Question it answers | Where it lives |
| --- | --- | --- |
| Scientific | Where did this claim come from? | `evidence/references.bib`, `evidence/claims.yml` |
| Computational | Where did this figure come from? | `figures/source/`, the rebuild recipe |
| Pedagogical | What observation licenses this interpretation? | these conventions |

### A note on justification

The justification for all of this is **educational evidence**: prediction
before instruction, retrieval practice, spaced revisiting, and the finding
that errors help when they are diagnosed rather than merely corrected.

Neuroscience offers plausible mechanisms and boundary conditions, nothing
more. This is **not** "brain-based teaching", and no page should sell it that
way. If a page cites learning-science literature, that reference is verified
exactly like any other: a resolving DOI, checked metadata, and a claim no
stronger than the study's design.

---

## The learning cycle

```
ACTIVATE → PREDICT → EVIDENCE → DIAGNOSE → RECONSTRUCT → CONTRAST/TRANSFER → RETRIEVE LATER
```

- **Activate.** Surface what the reader already believes, in their own terms,
  before introducing any machinery.
- **Predict.** Low-stakes and private, with an optional low/medium/high
  confidence rating. Nothing is collected.
- **Evidence.** Never a gotcha. The point is not that the reader was wrong;
  often the intuitive answer is right under conditions the prompt did not
  state, and saying so is part of the teaching.
- **Diagnose.** Which assumption made the prediction succeed or fail? This is
  the step that does the work and the one most often skipped. A corrected
  answer with an undiagnosed assumption leaves the reasoning intact to fail
  again.
- **Reconstruct.** Give the wider causal model the diagnosis implies.
- **Contrast / transfer.** Apply it to a nearby, non-identical case. Identical
  cases test recall; nearby ones test the model.
- **Retrieve later.** Bring the principle back elsewhere in the repository,
  days or weeks later in reading time.

The worked example is in
[`../concepts/fitness-vs-persistence.md`](../concepts/fitness-vs-persistence.md):
"a plasmid imposes a 5% growth cost — does it disappear?"

---

## Five conventions

### 1. Important cases use some version of the cycle

Predict → evidence → diagnose → reconstruct → transfer. **Not every page needs
every stage**, and a page that mechanically performs all seven is worse than
one that uses three well.

Selection rule for a prompt: **if the intuitive answer is right, the prompt is
not teaching the boundary.** The 5% cost prompt qualifies because both
confident answers — "yes, it disappears" and "no, plasmids persist" — are
wrong as stated, and the diagnosis is the same either way: a missing term.

When retrofitting the cycle into an existing page, expect it to displace
exposition: move or remove prose that now reveals the answer too early or
merely repeats what the learner has just derived. The test is duplication of
function, not line count — exposition that still does a different job stays.

### 2. Important figures and models carry a "How this can be misread" table

Three columns: **tempting reading**, **status**, **better interpretation**.
Written from the figure's own likely misreadings, not from generic caveats.

Traps worth covering where they apply:

- fitness cost ≠ fate;
- transfer ≠ spread;
- copy number ≠ evolutionary success;
- threshold ≠ automatically a tipping point;
- one host ≠ host robustness.

Current example: the table in
[`../case-studies/shewanella-oxa48.md`](../case-studies/shewanella-oxa48.md).

### 3. A visible context warning wherever quantities are not comparable

Whenever numbers sit side by side across incompatible **host**, **assay**,
**estimator**, **medium**, **timescale** or **spatial regime**, the page says
so where the comparison appears.

`NOT COMPARABLE` must mark a real inference problem — a case where reading the
numbers against each other would license a wrong conclusion. Used
decoratively, it trains readers to skip it.

Three specific insufficiencies:

- one host cannot establish host robustness;
- one environment cannot establish ecological robustness;
- a single endpoint cannot establish dynamical stability.

These are about *sufficiency*, not validity: a single-host study is good
evidence about that host.

### 4. Two axes in the registry, a small badge vocabulary on the page

The registry records two independent things: **`layer`** (what sort of
statement this is: source, interpretation, model, observation, convention) and
**`status`** (what the evidence says: supported, contested, unsupported,
refuted, not_tested, not_applicable). Full definitions in
[`../evidence/evidence-levels.md`](../evidence/evidence-levels.md).

Separating them is what lets a derived result be recorded honestly. The
invasion threshold in the worked example is `layer: model`, `status:
supported` — the derivation and its numerical checks hold *within* the model —
and the layer is what stops anyone reading it as an empirical law.

Three states are easy to collapse and must not be:

```
not_tested    "We haven't asked."
unsupported   "We've looked, and this conclusion isn't established."
refuted       "We have evidence against it."
```

**"Not tested" never looks negative, and "unresolved" is never narrated as
false.** These are the failure modes that make a page wrong while every
sentence in it stays individually defensible.

**Scope before status.** Before calling anything contested, check the findings
make the same claim under comparable host, environment, assay, estimator,
timescale and definition. Context dependence is not disagreement — and in a
field whose central finding is that context decides, letting `contested`
absorb biological heterogeneity would empty the label of meaning.

**Supported means supported at the claim's stated layer and scope.**
`model / supported` implies no empirical validation, and
`interpretation / supported` is not a directly observed fact.

On the page, a reader sees a small badge vocabulary derived from the two
fields rather than equal to them: **MODEL**, **UNRESOLVED**, **NOT TESTED**,
**CONTESTED**, **NOT COMPARABLE**, and **ILLUSTRATIVE** on figures. Pages show
only the exceptions that matter for teaching — metadata on every sentence
trains readers to skip it. Ordinary supported prose carries no badge. The
mapping is in `evidence-levels.md`.

The vocabulary is **frozen for v0.2**: add no layer or status unless a real
claim cannot be represented correctly.

### 5. Deliberate retrieval across reading paths

A concept introduced in one place returns in another. The *Shewanella* story's
context-dependence returns under COPY/CARRY/SPREAD and again under
persistence; the cost-versus-transfer balance from the worked example returns
in the pOXA-48 discussion.

The aim is learning that survives days and weeks, so a concept should reappear
*after* the reader has moved on, where it has to be recognised rather than
recalled from the paragraph above. The [reading paths](../README.md) are the
structure that makes this schedulable.

---

## Claims and prose

Prose **may paraphrase** `claims.yml`. It must preserve the claim's **scope**,
its **uncertainty** and its **evidence state**. Word-for-word matching is not
required and is not wanted.

Automated: that every claim ID cited in prose **exists and is valid**
(`evidence/check_claim_ids.py`). Semantic fidelity is a human job — a machine
cannot tell whether a paraphrase quietly widened a scope, and a check that
pretended to would license the drift it appeared to prevent.

Load-bearing supported claims carry a light record that a human read the
source:

```yaml
verification:
  source_checked: true
  checked_against: full_text   # or: abstract
  note: "Fig. 3 / Results"
```

Load-bearing claims only. Applied everywhere it becomes boilerplate, and
boilerplate is not read.

## Student material

Decide explicitly, for every piece, whether it is **learner-facing** or
**instructor-facing**.

- **Learner-facing**: prediction prompts, explanations, figures. Public.
- **Instructor-facing**: facilitation notes — what the common wrong answers
  reveal, how long to leave a silence, when to let an error stand. The current
  recommendation is that these stay **out of this public repository**: a note
  saying "most students will answer X" is read very differently by a student
  who finds it than by the instructor it was written for.

**Public prediction exercises never retain responses.** No forms, no
analytics, no storage. A prediction exists in the reader's head and nowhere
else.

**When an immediate answer would spoil the exercise**, use a `<details>`
collapsible reveal, or move the answer to a separate facilitation note.
`<details>` is what the worked example and the case study use: the commitment
step survives because the answer is a deliberate click away rather than in
peripheral vision, it works on GitHub with no build step, and it degrades
honestly — in printed or plain-text rendering the answer is visible, which is
a known limitation rather than a silent failure.
