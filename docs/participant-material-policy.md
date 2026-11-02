# Participant-material policy

**Participant-derived material is excluded from this public repository by
default.**

This policy exists because the project draws on a teaching context in which
real people presented their own work. They presented to an audience, not to a
permanent public archive with their name attached, and the difference matters.

## Never commit

The following must not enter Git **on any branch** — including temporary,
draft and unpublished branches, and including branches that are never pushed:

Each clause carries a mark, defined under
[Checked or attested](#checked-or-attested). The short version: the mark says
who is in a position to verify the clause — anyone, only someone holding
material this policy excludes, or the author alone.

Outside the definition table below, a badge always marks a clause and never
explains one. That is what makes the clauses countable, and the count is
checked — see [The ratio](#the-ratio).

- **`CHECKED`** — raw or cleaned transcripts;
- **`CHECKABLE`** — participant names or other directly identifying personal
  data;
- **`CHECKED`** for video and channel links and for email addresses,
  **`ATTESTED`** for contact information in any other form — personal YouTube
  or channel metadata, or contact information;
- **`CHECKABLE`** — schools, universities or affiliations, where these
  identify individuals;
- **`CHECKED`** for the directory shapes, **`ATTESTED`** for the content —
  internal transcription, correction, judging or curation notes;
- **`ATTESTED`** — unpublished submissions or presentation material;
- **`ATTESTED`** — verbatim participant speech, unless separately and
  explicitly authorised.

**This applies even when the original presentation or video is publicly
accessible.** A public source is not, by itself, permission to redistribute an
identifiable transcript. Findability and republication are different acts, and
the second attaches a person's words to this repository's name and lifetime.

Git makes this close to irreversible: a commit on a local branch can be
pushed later by someone who did not know what was in it, and history is not
meaningfully editable once shared. "Only on a draft branch" is not a
mitigation.

The **on any branch** scope is **`CHECKED`** for the file shapes and
**`ATTESTED`** for content. The checker reads `git log --all`, so it covers
every branch in the clone it runs in, including ones never pushed — but it
cannot see a branch that exists only in somebody else's working tree, which is
the case this clause worries about most.

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

**`ATTESTED`** — every checked clause above is a consequence of this one that
happens to leave a trace. The firewall itself is broader than all of them
together, and nothing could falsify it.

The working test is unchanged: **could this page have been written by someone
who never watched the presentations?** **`ATTESTED`**, necessarily — it is a
judgement, which is what makes it a usable test and what makes it unverifiable
by anyone else.

If permission is later obtained, the firewall is **changed deliberately into a
permission-gated boundary** — recording which scopes are covered, for whom,
and by what evidence. It is not removed. A boundary that dissolves the first
time someone says yes was never a boundary.

## Checked or attested

The clauses in this policy are not all the same kind of statement, and
presenting them in one declarative voice hid that: a reader could not tell
which ones they were being asked to take on trust. Each now carries one of
three marks.

| Mark | Means | Who can verify it |
| --- | --- | --- |
| **`CHECKED`** | A committed script verifies it. | Anyone who clones. |
| **`CHECKABLE`** | A procedure exists and has been run, but its input is material this policy excludes, so the check cannot be committed. | Only someone holding that input. |
| **`ATTESTED`** | No committable check decides it — either nothing could falsify it, or nothing enumerates what would. A statement by the author about their own conduct. | No one. |

These are a **separate, local vocabulary** for this file. They are not
evidence badges and have no relationship to the `layer` and `status` axes in
[`../evidence/evidence-levels.md`](../evidence/evidence-levels.md), which
describe claims about nature. These describe who is in a position to check a
promise.

### Why the middle mark exists

"No participant names" *is* mechanically checkable: grep the tree for the
names. But the check needs the list of names as its input, and committing that
list would commit precisely the identifying data the clause forbids. **The
check cannot be committed without violating the clause it checks.** That is
not the same as "no transcripts in Git", which any stranger can verify, and
not the same as a judgement nobody can. Both reductions lose something true,
so the policy carries three marks rather than two.

From a reader's position the second and third marks are the same: they take
the author's word. The distinction is about what the author can do, not what
the reader gets.

### What the third mark had to absorb

`ATTESTED` first meant "nothing could falsify it". Splitting the contact
clause (OF-10) produced a statement that does not fit that: "no contact
information in any other form" **is** falsifiable — find a phone number in the
tree and it is false — but no list of what counts as contact information is
complete, so no committable check decides it. That is a third situation, and
the mark's definition was widened to hold it rather than filed under the
nearest existing one.

This is worth stating because the alternative was available and tempting: the
clause could have kept its single `CHECKED` mark, and the gap between "contact
information" and "an email address" would have stayed invisible. A vocabulary
whose categories are never strained is usually a vocabulary nobody has tried to
use.

What the three marks now separate is who can decide a clause: anyone with a
clone, only someone holding excluded material, or no one. The widening does not
touch the first two.

### What `CHECKED` is worth

[`../evidence/check_participant_firewall.py`](../evidence/check_participant_firewall.py)
runs the checked clauses: caption and subtitle formats and guarded directories
never added in any reachable commit on any branch in the clone, the
`.gitignore` net for both still present and uncommented, no personal video or
channel link in the tree, and no email address outside an explicit allowlist.
Those last two are the whole of what it knows about contact information: a
phone number, a social handle or a file-sharing link is not in its domain,
which is why the clause above carries two marks instead of one. It states in
its own output what it does not cover. 11 mutations in
[`../evidence/test_check_participant_firewall.py`](../evidence/test_check_participant_firewall.py)
confirm it goes red for each of those, including one committed on a branch
that is never pushed, and that it refuses to run rather than cover a subset
when git is unavailable.

**The checked clauses are the floor, not the policy.** They catch the
file-shaped accident — a folder of captions dropped into the tree. They say
nothing about a page written by someone who watched the presentations and did
not notice they were remembering one.

### The ratio

Counted in this file: **6 checked, 2 checkable, 9 attested.**

Most of this policy is attested, and that is not a defect to be engineered
away. A firewall against *judgement* being contaminated cannot be reduced to a
grep, and a policy containing only its greppable parts would be a smaller
policy, not a better-verified one. Publishing the ratio is the honest version
of a promise most of which rests on one person's word.

The line above is itself checked. `check_participant_firewall.py` counts the
badges outside the definition table and fails if they disagree with it, because
the first version of this sentence said four checked when there were six: it
was carried over from a working draft that counted one section's clauses, and
never re-derived after three more sections were marked. A count in prose is an
unversioned copy of a computation — the defect recorded under OF-5 and found
again here — and the only durable answer is to make the prose and the
computation the same thing.

## Governance principle

**When the educational objective can be achieved with less participant data,
use less participant data.**

The public educational object is the curated scientific abstraction, not the
source corpus. If a concept can be taught from the published literature — and
in this repository it almost always can — then it should be, because that
version is reusable, checkable and carries no one's name.

## Current state

Nothing in this repository is participant-derived. **`ATTESTED`** — it is the
conjunction of everything above, and while some of its conjuncts are checked,
the statement is not.

Every page is built from published literature **`CHECKED`** — every citation
resolves to an entry in the bibliography and every entry is cited, verified by
[`../evidence/check_references.py`](../evidence/check_references.py) — with
DOI-checked references, **`CHECKED`** for the presence and shape of each
`doi` field and **`ATTESTED`** for resolution: that a DOI works, and that its
metadata matches the entry, is hand-checking the script declines to imitate.

This policy is written down so that stays true by decision rather than by
accident, and marked so that a reader can tell which half of it rests on a
command and which on a person.
