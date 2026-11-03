# Contributing

There is no page template, deliberately. The first principle is that the
subject generates the structure, and a template is a set of slots that invites
filling. What follows constrains **rigour**, not shape: two pages that look
nothing alike can both pass it.

## Checklist for any page

**Evidence**

- [ ] Every factual statement traces to an entry in
      [`evidence/references.bib`](evidence/references.bib).
- [ ] Every reference has a DOI that resolves, with metadata checked against
      the record — not against the title alone.
- [ ] Where prose paraphrases [`evidence/claims.yml`](evidence/claims.yml), the
      paraphrase preserves the claim's **scope**, **uncertainty** and
      **evidence state**. Word-for-word matching is neither required nor
      wanted. This one is a human check; no script can do it.
- [ ] `python evidence/check_claim_ids.py` passes. It checks that cited claim
      IDs exist and that every `layer` and `status` is in vocabulary; it does
      not and cannot check that a paraphrase is faithful.
- [ ] `python evidence/check_references.py` passes. Every `[@key]`, every key
      in a `references:` list and every key in a figure's `SOURCE_KEYS`
      resolves to an entry in `references.bib`, and every entry is cited
      somewhere. It does **not** resolve DOIs: that a DOI works, and that its
      metadata matches the entry, stays a human check.

**Epistemic state**

- [ ] Anything not plainly supported is marked: `MODEL`, `UNRESOLVED`,
      `NOT TESTED`, `CONTESTED`, `NOT COMPARABLE`, or `ILLUSTRATIVE` on a
      figure. Ordinary supported prose stays plain — marking everything turns
      the markers into wallpaper.
- [ ] Where a claim ID is cited, remember that **supported means supported at
      that claim's stated layer and scope**: `model / supported` is not
      empirical validation.
- [ ] A marker names a real inference problem. `NOT COMPARABLE` is never
      decoration.
- [ ] **Scope before status.** Two findings that disagree are only
      `contested` if they make the same claim under comparable host,
      environment, assay, estimator, timescale and definition. Otherwise it is
      context dependence, and the comparison is what needs marking.
- [ ] Absence of evidence is not written as evidence of absence. "Not tested"
      never reads as negative, and "unresolved" is never narrated as false.
- [ ] No model output is presented as an observation. If a number comes from a
      model, the same sentence says so.

**Claim strength**

- [ ] Claim strength does not exceed design strength. One strain is not a
      species; a mating assay is not environmental transfer; an endpoint is
      not a rate.
- [ ] Comparison sufficiency: one host does not establish host robustness, one
      environment does not establish ecological robustness, one endpoint does
      not establish dynamical stability. Where a comparison crosses
      incompatible hosts, assays, estimators, media, timescales or spatial
      regimes, it carries a visible context warning.
- [ ] No sentence fuses separately evidenced observations into a single
      historical event. Prefer describing the present configuration over
      narrating a sequence, unless the order is actually resolved.
- [ ] Lower bounds are not written as origins.
- [ ] A trailing qualifier after a list applies to every item in it. Check, and
      split the sentence where it does not.

**Figures**

- [ ] Generated from a committed script, standard library where possible, with
      `newline="\n"` so the output is byte-identical on any platform.
- [ ] Colours come from [`figures/source/palette.py`](figures/source/palette.py),
      and `python figures/source/palette.py` passes.
- [ ] Colour is never the only encoding. Labels, shapes, line styles or
      position carry the meaning too.
- [ ] The figure states whether it is illustrative or calibrated.
- [ ] An important figure carries a "how this can be misread" table.

**Teaching**

- [ ] An important case uses some version of predict → evidence → diagnose →
      reconstruct → transfer. Not every page needs every stage.
- [ ] A prediction prompt's answer is not visible directly below it. Use a
      `<details>` reveal.
- [ ] The prompt is worth asking: if the intuitive answer is right, it is not
      teaching anything.
- [ ] Nothing collects a learner's response.
- [ ] Instructor-facing facilitation notes are not in this repository.

**Public/private firewall**

- [ ] Nothing derives from Thai SynBio Challenge 2026 participant
      submissions or presentations. Could this page have been written by
      someone who never watched them? This one is **attested**: no script can
      answer it, which is why it is the working test rather than a check.
- [ ] `python evidence/check_participant_firewall.py` passes. It covers the
      **checked** clauses only — caption and subtitle formats, guarded
      directories, the `.gitignore` net, video links, stray addresses — over
      every branch in your clone. A clean run is the floor, not the policy.
- [ ] Nothing on the never-commit list is in the change, **on any branch**:
      transcripts, participant names, channel or contact data, identifying
      affiliations, internal transcription or judging notes, unpublished
      submissions, or verbatim participant speech. The name and affiliation
      clauses are **checkable** but not checked here: the grep needs the
      participant list, which must never enter this repository, so run it
      against your own copy. A public video is not permission to republish an
      identifiable transcript. Full policy, with every clause marked checked,
      checkable or attested:
      [`docs/participant-material-policy.md`](docs/participant-material-policy.md).
- [ ] No omission is written as a negative claim. "Not described in the
      presentation" and "not observable from the available source" are the
      available wordings; "the team did not consider X" is not.

## Running the checks

```bash
python evidence/check_claim_ids.py
python evidence/check_references.py
python evidence/check_participant_firewall.py
python figures/source/palette.py
python figures/source/shewanella_oxa48_pathway.py && git status --porcelain
```

Both checkers need PyYAML, so from a bare machine:
`uv run --no-project --with pyyaml python evidence/check_references.py`.

`check_claim_ids.py` also verifies that every `pages:` path exists and that
any `status:` or `layer:` written in a content page matches the registry.

**Read the exit status directly.** If you wrap a run in a loop that formats its
own output, check that the status you print is the checker's and not the
formatter's. A changeset in this repository was committed with "all checkers
exit 0" in its message while one mutation test exited 1, because the reporting
line evaluated `$?` after a command substitution had already reset it. A
verification harness that cannot report a failure is the same defect as a
checker that cannot fail, one level up, and it is harder to see because its
output looks like success.

Each checker states the file types it reads and refuses to pass when a file
type appears that nobody has ruled on. If you add a format — `.tex`, `.qmd`,
`.json` — `check_references.py` will fail until you decide whether it can
carry citations. That is deliberate: the alternative is a check that quietly
stops covering part of the repository. The same applies to a file with **no**
extension: those are ruled on by name, in `UNCITED_NAMES`, so adding a
`NOTES` or a `Makefile` fails until you say which it is.

The two `test_check_*.py` scripts are not part of the routine run. Each mutates
a temporary copy — 17 ways for the references checker, 11 for the
firewall checker — and asserts the checker responds. Sixteen of the references
cases assert a failure; one asserts that the checker stays green and still
reports what it found, because not everything worth saying is an error. Run
the matching test after changing a checker, and add a case when you widen what
it covers: a checker that has only ever reported clean is not known to work.

When you add a case, check that it **fails against the unfixed checker**. A
case that passes either way tests nothing, and that is not hypothetical here:
twelve of the references cases passed against a defect they were written to
cover, because every one of them planted a key that already matched the
pattern the extractor used (G2).

## Every instrument needs evidence that it can fail

The rule the defects in this repository keep arriving at:

> **A passing check without a demonstrated failing control is weak evidence of
> coverage — and that applies recursively to whatever executes the checks.**

Not every script needs a mutation suite. But every gate anyone relies on should
have **at least one known-negative that travels the same execution path** as
the real run, and you should have seen it go red.

This is not incidental hygiene. It is the same discipline the teaching material
asks of an experiment:

```text
biological assay
  signal observed      ≠  measurement system shown able to detect failure

repository check
  exit 0 observed      ≠  harness shown able to propagate failure
```

Both failures look identical to success from the outside, which is why neither
can be settled by reading. Before quoting a screen of zeros, push a deliberate
failure through the same loop:

```bash
uv run --no-project python -c "import sys; sys.exit(3)"
```

If that does not print `3`, nothing else the loop printed means anything.

### A control on other inputs is not a control on this one

The rule above is necessary and not sufficient, and the sharper version was
earned three times in one day — twice by searching published text for a
sentence that was there.

A whitespace-insensitive search missed a sentence because `innerText` inserts
line breaks. The fix was to normalise whitespace. The *next* search, already
whitespace-normalised and returning four hits out of six, still produced one
false negative: the quarry began a sentence and the matcher was
case-sensitive. That matcher had been demonstrated able to return positives —
on five other strings in the same document — and it was still wrong about the
sixth.

> **A control exercises one failure mode. Passing it says nothing about the
> others.** Before reporting that something is absent, ask which way *this*
> search could be wrong, and defeat that specific way.

For text retrieval that means normalising whitespace **and** case, and
preferring a regex over `includes` for anything whose capitalisation depends
on where a sentence starts. For a numerical verdict it means exact arithmetic
where a value can land on a boundary: a float base once labelled an
algebraically-zero cell a win, and a verdict produced by rounding is
indistinguishable from one produced by the model.

An absence claim is a claim. It needs its own evidence, not the evidence that
a neighbouring presence claim passed.

Known unfixed defects are listed in
[`docs/open-findings.md`](docs/open-findings.md); add one there in the same
commit that discovers it.

The third should leave the working tree clean: a figure that changes without
its script changing means something is wrong.

There is no CI. These are run by hand, by whoever is editing.
