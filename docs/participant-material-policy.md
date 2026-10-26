# Participant-material policy

**Participant-derived material is excluded from this public repository by
default.**

This policy exists because the project draws on a teaching context in which
real people presented their own work. They presented to an audience, not to a
permanent public archive with their name attached, and the difference matters.

## Never commit

The following must not enter Git **on any branch** — including temporary,
draft and unpublished branches, and including branches that are never pushed:

- raw or cleaned transcripts;
- participant names or other directly identifying personal data;
- personal YouTube or channel metadata, or contact information;
- schools, universities or affiliations, where these identify individuals;
- internal transcription, correction, judging or curation notes;
- unpublished submissions or presentation material;
- verbatim participant speech, unless separately and explicitly authorised.

**This applies even when the original presentation or video is publicly
accessible.** A public source is not, by itself, permission to redistribute an
identifiable transcript. Findability and republication are different acts, and
the second attaches a person's words to this repository's name and lifetime.

Git makes this close to irreversible: a commit on a local branch can be
pushed later by someone who did not know what was in it, and history is not
meaningfully editable once shared. "Only on a draft branch" is not a
mitigation.

## What may eventually be included

Participant-derived *scientific* content may enter only when there is
**documented, scoped permission** covering the intended reuse.

The preferred public form is a **minimised, paraphrased strategy summary** —
not a transcript. Such a summary might describe:

- replication and origin choice;
- copy-number strategy;
- burden mitigation;
- maintenance strategy;
- mobility and transfer assumptions;
- selection regime;
- ecological assumptions;
- which components were experimentally tested and which were proposed.

Include only what the educational comparison needs. Where it would serve the
reader, **link to the original public presentation rather than reproducing
it**.

## Permission is scoped, and the scopes are separate

Before publishing anything participant-derived, record what the permission
actually covers. These are distinct permissions:

| Scope | Covers |
| --- | --- |
| Paraphrased scientific strategies | A minimised summary in our words |
| Official team names | Naming the team |
| Links to public presentations | Pointing at the original |
| Quotations | Verbatim speech or text |
| Figures and slides | Reproducing their visual material |
| Comparison across teams | Setting teams side by side |

**Permission for one category is not permission for another.** Agreement to a
paraphrased summary is not agreement to be quoted, and agreement to be named
is not agreement to be compared.

## Inference discipline

A presentation is an **incomplete observation** of a team's design process.
People leave things out for time, for emphasis, or because they assumed the
audience knew.

> **Not mentioned in the presentation ≠ not considered by the team.**

Never convert an omission into a negative claim. Write:

- "not described in the presentation";
- "not observable from the available source";
- "not assessed from this material".

**Absence from a presentation is a limitation of the available source, not an
evidence state of the underlying scientific claim.** "Not mentioned", "not
observable from the available material" and "not assessed" must not be
converted automatically into `not_tested`, `unsupported` or `refuted`.

These are different questions, and collapsing them would reintroduce the
error the registry exists to prevent:

| Source limitation | Evidence state |
| --- | --- |
| "the presentation did not mention X" | "X has not been tested" |

From silence we usually know only that something was **not observed in this
source**. The team may well have tested it and not mentioned it — time,
emphasis, or an assumption about the audience. Silence is evidence about the
presentation, not about the work.

So a source limitation gets recorded as what it is, in words, and does not
receive a registry status at all. See
[`../evidence/evidence-levels.md`](../evidence/evidence-levels.md).

**`NOT COMPARABLE`** is likewise used where the available presentations
*genuinely prevent* a comparison — different experimental context,
measurement, or evidence — and **not** automatically wherever presentation
detail happens to differ. Two teams described at different levels of detail
have not been shown to differ in design; they have been shown to differ in
what they said, and whether that blocks a particular comparison is a judgement
to make and state, not a default.

## The firewall

Until appropriate permission is documented, the repository-wide firewall
stands:

> No participant-derived scientific strategy, and no identifiable participant
> material, enters the public repository.

The working test is unchanged: **could this page have been written by someone
who never watched the presentations?**

If permission is later obtained, the firewall is **changed deliberately into a
permission-gated boundary** — recording which scopes are covered, for whom,
and by what evidence. It is not removed. A boundary that dissolves the first
time someone says yes was never a boundary.

## Governance principle

**When the educational objective can be achieved with less participant data,
use less participant data.**

The public educational object is the curated scientific abstraction, not the
source corpus. If a concept can be taught from the published literature — and
in this repository it almost always can — then it should be, because that
version is reusable, checkable and carries no one's name.

## Current state

Nothing in this repository is participant-derived. Every page is built from
published literature with DOI-checked references. This policy is written down
so that stays true by decision rather than by accident.
