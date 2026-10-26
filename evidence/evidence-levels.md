# Evidence levels

Every tracked claim in [`claims.yml`](claims.yml) carries two fields on two
**independent axes**:

- **`layer`** — what sort of statement this is.
- **`status`** — what the evidence currently says about it.

Keeping them apart is the whole point. The earlier vocabulary mixed them:
`model-derived` and `definitional` sat in `status` alongside `supported` and
`refuted`, which answer a different question. A model result was then stuck at
"model-derived" and could never be recorded as well-established *within its
model*, or as disputed *between* models.

## `layer` — what sort of statement

| Layer | Means |
| --- | --- |
| `source` | What a publication reports. |
| `interpretation` | Our synthesis across sources. Can be wrong even when every source is right. |
| `model` | Follows from a stated model under stated assumptions. |
| `observation` | Data that tests a prediction. |
| `convention` | A house rule this project adopts, not a claim about nature. |

## `status` — what the evidence says

**Supported means supported at the claim's stated layer and scope.** It is
not a general endorsement. `model / supported` says the derivation and its
checks hold under the model's assumptions; it implies no empirical
validation. `interpretation / supported` says our synthesis follows from the
cited sources; it is not a directly observed fact. Read the two fields
together or the word means more than it should.

| Status | Means |
| --- | --- |
| `supported` | Evidence directly tests the statement, within its stated scope, and is consistent with it. |
| `contested` | Credible evidence or interpretations both support and challenge the same scoped claim under comparable conditions. |
| `unsupported` | Relevant evidence exists or has been examined, but does not establish the claim. **Not** "false". |
| `refuted` | Evidence gives affirmative reason to reject the claim within its stated scope. |
| `not_tested` | The claim has not been directly tested; no identified evidence bears on it discriminatingly. |
| `not_applicable` | No evidential status applies — the normal case for `layer: convention`. |

### The three that are easy to collapse

```
not_tested    "We haven't asked."
unsupported   "We've looked, and this conclusion isn't established."
refuted       "We have evidence against it."
```

These are scientifically different, and collapsing the first two produces
exactly the inference error this repository exists to teach. The registry
carries a worked pair:

- `claim.shewanella.oxa_ancestral_selection` — "the historical selective agent
  is known" → **unsupported**. Evidence has been examined (ancient resistance,
  native regulation, environmental reservoirs) and none of it establishes the
  agent.
- `claim.shewanella.oxa_betalactam_hypothesis` — "environmental β-lactams were
  the agent" → **not_tested**. A specific hypothesis that no identified study
  tests discriminatingly.

"We don't know the answer" and "this particular answer is untested" are
different facts, and the registry can now record both.

**A source limitation is not an evidence state.** "The paper does not mention
it", "not observable from the available material", "not assessed from this
source" describe what we could see, not what is true of the claim. None of
them licenses `not_tested`, which asserts something about the world: that
nobody has tested it. An author who did not mention a control may still have
run it. Record source limitations in words, and leave the status to evidence
about the claim itself.

## Scope before status

**Before marking anything `contested`, check that the findings make the same
claim under comparable conditions.** Context dependence is not disagreement.

```
apparent contradiction
        ↓
same host / environment / assay / estimator / timescale / definition?
        ↓
       NO  →  scope or context mismatch; mark the comparison NOT COMPARABLE
        ↓
       YES
        ↓
credible evidence genuinely disagrees?
        ↓
       YES →  contested
```

Plasmid X costly in host A and beneficial in host B is **host dependence**.
High conjugation on a filter and low conjugation in liquid is **ecological
context dependence**. Neither is a controversy, and filing them as `contested`
would turn that label into a dumping ground for biological heterogeneity —
which, in a field whose central finding is that context decides, would empty
it of meaning.

The rule has already changed a classification.
`claim.shewanella.blaa_regulation_not_uniform` was `contested`: Poirel could
not demonstrate induction by imipenem or cefoxitin, while Yin reports strong
induction by high-dose ampicillin. Different inducers, different assays, so
not comparable, so not contested. It is now an `interpretation` that is
`supported` — the reports do not establish a disagreement. Whether one exists
under matched conditions is itself untested.

## Badges are not statuses

Pages carry a small learner-facing vocabulary, derived from these two fields
rather than equal to them. The registry can be precise without making every
page read like an evidence dashboard.

| Registry | Rendered on a page as |
| --- | --- |
| an open question, often spanning several registry entries | **UNRESOLVED** |
| `status: not_tested`, pointing at one specific untested claim | **NOT TESTED** |
| `layer: model`, any status | **MODEL** |
| `layer: convention` | *(no badge)* |
| any layer, `status: contested` | **CONTESTED** |
| a figure or value chosen for legibility | **ILLUSTRATIVE** |
| quantities not comparable across host, assay, estimator, medium, timescale or spatial regime | **NOT COMPARABLE** |

`ILLUSTRATIVE` and `NOT COMPARABLE` describe a figure or a comparison rather
than a claim, which is why they have no registry row. Ordinary supported prose
carries no badge at all.

**UNRESOLVED or NOT TESTED?** Use `NOT TESTED` when the page is pointing at
one specific claim nobody has tested, because that is the more informative
label. Use `UNRESOLVED` when the open question is broader than any single
registry entry — several competing hypotheses, or a mix of untested and
unestablished. The ancestral-selection question takes `UNRESOLVED`; the
β-lactam hypothesis on its own would take `NOT TESTED`.

Pages show only the exceptions that matter for teaching. Metadata on every
sentence trains readers to skip it, which costs more than it buys.

**UNRESOLVED is not a registry status, and is not identical to any one of
them.** It is the reader-facing label for a question that is open. Internally
that can arise in more than one way: a claim nobody has tested, a claim where
the evidence does not establish the conclusion, or a cluster of competing
hypotheses that are individually untested or weakly supported. The badge says
"the answer is not settled"; the registry says which of those situations
produced it. The *Shewanella* ancestral-selection question is badged UNRESOLVED
on the page and is carried by two registry entries with different statuses —
`unsupported` for "the agent is known", `not_tested` for the specific
β-lactam hypothesis.

`model-derived` and `illustrative` are **provenance and type markers**, not
verdicts, which is why they sit on the `layer` axis (or on a figure) rather
than in `status`. A model result then still gets a real evidence state:
the invasion condition displays **MODEL** on the page, and its derivation and
numerical checks make it `supported` *within the model's stated assumptions*.

## Verification blocks

Load-bearing claims carry a light record that a human checked the source:

```yaml
verification:
  source_checked: true
  checked_against: full_text   # or: abstract, own_derivation
  note: "Fig. 3 / Results"
```

`own_derivation` is for `layer: model` claims, where what was checked is the
derivation and its numerical verification rather than someone else's paper.

## The ontology is frozen for v0.2

Five layers, six statuses. **Add nothing unless a real claim cannot be
represented correctly** — not because a new shade would be tidier. The cost of
a larger vocabulary is paid by every future reader deciding between two
near-identical labels, and by every page that then needs re-marking.

`contested` being unused is intended, not a gap. Under scope before status it
should stay rare: most apparent contradictions in this field are context
dependence, and a `contested` that fills up has stopped meaning anything.

## Rules

1. **Only reusable claims get tracked.** A statement cited on one page does
   not need an ID. Claims enter the registry when they are load-bearing across
   pages, when their status is likely to change, or when getting them wrong
   would propagate.
2. **`supported` needs a primary reference**, not a review — except for
   `layer: model`, where it means supported *within* the model, and the
   derivation plus its verification is the evidence.
3. **Absence of evidence is `not_tested` or `unsupported`, never `refuted`.**
4. **`notes` carries the caveat**, including what *is* established when the
   claim as written is not.
5. **A status change is normal.** Reclassifying as new work appears, or as a
   rule like scope-before-status is applied, is maintenance, not failure.

## What this file does not do

It does not rank journals, weigh sample sizes or grade study designs. It is a
bookkeeping convention for keeping interpretation visibly distinct from
evidence in a teaching repository — not an evidence-appraisal framework of the
kind used in clinical systematic review.
