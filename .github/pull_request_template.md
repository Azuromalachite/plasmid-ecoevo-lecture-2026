<!--
This constrains rigour, not shape — the same stance CONTRIBUTING.md takes
when it says there is no page template. Delete any section that genuinely
does not apply, and say in one line why. A section deleted silently reads
as a section that passed.
-->

## What changed, and why

<!-- One paragraph. The why is the part a reader cannot reconstruct later. -->

## Open findings

<!--
docs/open-findings.md is updated in the same commit that closes or adds a
finding, so this list and that file should already agree.
-->

- Closes: <!-- OF-NN, or "none" -->
- Opens: <!-- OF-NN, or "none" -->
- Supersedes part of an existing entry: <!-- OF-NN and which sentence, or "none" -->

If this corrects something already public, say so here in one line — what
was claimed, and what replaces it.

## Numbers that changed

| number | was | is | reproduced by |
|---|---|---|---|
|  |  |  |  |

- [ ] Every changed number in prose matches the script output it came from.
- [ ] Every number still quoted at three significant figures has an interval
      that justifies them.

## Checks

Run by hand; there is no CI. **Paste the statuses, not a summary** — a
changeset here was once committed saying "all checkers exit 0" while one
test exited 1, because the reporting line read `$?` after a command
substitution had already reset it.

```bash
python evidence/check_claim_ids.py                  # status:
python evidence/check_references.py                 # status:
python evidence/check_participant_firewall.py       # status:
python evidence/check_math_delimiters.py            # status:
python figures/source/palette.py                    # status:
python figures/source/shewanella_oxa48_pathway.py && git status --porcelain
```

- [ ] The last one left the working tree clean. A figure that changes
      without its script changing means something is wrong.
- [ ] I confirmed the harness can propagate a failure at all:
      `uv run --no-project python -c "import sys; sys.exit(3)"` printed `3`.

## The control that could have failed

> A passing check without a demonstrated failing control is weak evidence of
> coverage — and that applies recursively to whatever executes the checks.

- Known-negative used: <!-- which one, and what it mutates -->
- [ ] I saw it go red, through the same execution path as the real run.
- [ ] It fails for the rule it was written for, not a different one. (Twelve
      reference-checker cases here once passed against the defect they were
      meant to cover, because each planted a key the extractor already
      matched.)
- If this change adds or widens a gate, a matching case was added: <!-- where -->

## Epistemic state

- [ ] Anything not plainly supported carries a marker: `MODEL`,
      `UNRESOLVED`, `NOT TESTED`, `CONTESTED`, `NOT COMPARABLE`, or
      `ILLUSTRATIVE`. Supported prose stays plain.
- [ ] Claim strength does not exceed design strength.
- [ ] No absence of evidence is written as evidence of absence; any absence
      claim carries its own evidence, not a neighbouring presence check's.
- [ ] No model output is presented as an observation.
- [ ] Two findings are only marked `contested` if they make the same claim
      under comparable scope.

## Public/private firewall

- [ ] `check_participant_firewall.py` passes over every branch in my clone.
      **Checked** clauses only — a clean run is the floor, not the policy.
- [ ] **Attested**, and no script can answer it: could this change have been
      written by someone who never watched the participant presentations?
      This includes **emphasis choices** — what is featured, ordered first,
      or given a callout.
- [ ] Nothing on the never-commit list is in the change, on any branch,
      including branches never pushed.
- [ ] No omission is written as a negative claim.

## What this does not establish

<!--
Required. Every substantial section of this repository carries one, and a
change that cannot name its own limits has usually not found them yet.
-->
