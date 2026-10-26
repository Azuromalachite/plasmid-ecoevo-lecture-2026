# Evidence levels

Every tracked claim in [`claims.yml`](claims.yml) carries a `status` from the
vocabulary below. The point of the vocabulary is to make the difference
between "we have evidence for this" and "this is a reasonable story" visible
in the file, rather than in the tone of a sentence.

## Status vocabulary

> **Open question.** v0.2 fixes seven learner-facing evidence states:
> supported, unresolved, unsupported, refuted, not tested, model-derived,
> illustrative (see
> [`../docs/pedagogy-conventions.md`](../docs/pedagogy-conventions.md)).
> This registry additionally uses `contested` and `definitional`, and
> currently lacks `not tested` and `illustrative`. Whether `contested` should
> map onto `unresolved` or become an eighth state, and whether `definitional`
> belongs on an evidence scale at all, is **awaiting a decision**; until then
> the two claims using them are left as they are. The states below are what
> the registry accepts today.

| Status | Meaning | Required to assign it |
| --- | --- | --- |
| `supported` | Published primary evidence directly tests the statement and is consistent with it. | At least one primary reference whose reported results bear on the statement as written. |
| `contested` | Published evidence exists on both sides, or authoritative sources disagree. | References on more than one side, named in `notes`. |
| `unsupported` | The statement is plausible but no cited evidence establishes it. This is **not** "false" — it marks a gap. | The gap stated explicitly in `notes`. |
| `refuted` | Published evidence is inconsistent with the statement. | A primary reference whose results contradict it. |
| `model-derived` | Follows from a stated model under stated assumptions; not an empirical observation. | The model, its assumptions and its regime named in `notes`. |
| `definitional` | A terminological or framing convention this project adopts, not a factual claim. | The convention stated; no empirical backing claimed. |

## Layer vocabulary

Separate from status, each claim records which of the project's four layers it
belongs to (see the principles in the [README](../README.md)):

- `source` — what a publication reports.
- `interpretation` — our synthesis across sources. Can be wrong even when
  every source is right.
- `model` — an implication of a stated model under stated assumptions.
- `observation` — data that tests a prediction.

A claim's layer and its status are independent: an `interpretation` can be
`supported`, and a `source`-layer claim can be `contested`.

## Rules

1. **Only reusable claims get tracked.** A statement that appears on one page
   and is cited there does not need an ID. Claims enter `claims.yml` when they
   are load-bearing across pages, when their status is likely to change, or
   when getting them wrong would propagate.
2. **A `supported` status needs a primary reference, not a review.** Reviews
   may be listed in addition, for context.
3. **Absence of evidence is `unsupported`, not `refuted`.** These are
   different situations and conflating them is how speculation becomes
   received wisdom.
4. **`notes` carries the caveat**, including what *is* established when the
   claim as written is not. The entry for
   `claim.shewanella.oxa_ancestral_selection` is the model: the native
   physiological context is supported; the historical selective agent is not.
5. **A status downgrade is normal.** Changing `supported` to `contested` when
   new work appears is maintenance, not failure.

## What this file does not do

It does not rank journals, weigh sample sizes, or grade study designs. It is a
bookkeeping convention for keeping interpretation visibly distinct from
evidence in a teaching repository — not an evidence-appraisal framework of the
kind used in clinical systematic review.

## Pending reconciliation

| v0.2 learner-facing state | In this registry today |
| --- | --- |
| supported | yes |
| unresolved | no — the nearest entry is `unsupported`, which means something narrower |
| unsupported | yes |
| refuted | yes |
| not tested | **missing** — currently indistinguishable from `unsupported`, which is exactly the distinction convention 4 says to preserve |
| model-derived | yes |
| illustrative | **missing** — used on figures in prose, but not as a claim status |
| — | `contested`: evidence on more than one side. Not in the v0.2 list |
| — | `definitional`: a project convention, arguably not an evidence state at all |

Adding `not tested` is the one change with a correctness argument behind it
rather than a tidiness argument: collapsing "nobody looked" into "nothing
establishes it" is the failure mode convention 4 exists to prevent.
