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
      someone who never watched them?
- [ ] Nothing on the never-commit list is in the change, **on any branch**:
      transcripts, participant names, channel or contact data, identifying
      affiliations, internal transcription or judging notes, unpublished
      submissions, or verbatim participant speech. A public video is not
      permission to republish an identifiable transcript. Full policy:
      [`docs/participant-material-policy.md`](docs/participant-material-policy.md).
- [ ] No omission is written as a negative claim. "Not described in the
      presentation" and "not observable from the available source" are the
      available wordings; "the team did not consider X" is not.

## Running the checks

```bash
python evidence/check_claim_ids.py
python figures/source/palette.py
python figures/source/shewanella_oxa48_pathway.py && git status --porcelain
```

`check_claim_ids.py` also verifies that every `pages:` path exists and that
any `status:` or `layer:` written in a content page matches the registry.
Known unfixed defects are listed in
[`docs/open-findings.md`](docs/open-findings.md); add one there in the same
commit that discovers it.

The third should leave the working tree clean: a figure that changes without
its script changing means something is wrong.

There is no CI. These are run by hand, by whoever is editing.
