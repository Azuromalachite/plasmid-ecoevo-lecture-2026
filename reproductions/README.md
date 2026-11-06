# Reproductions

Independent reanalyses of **other people's published data**. One directory per
study, each with a script, an execution receipt, and a results file.

This is not [`figures/`](../figures/), and the separation is deliberate.

| | `figures/` | `reproductions/` |
|---|---|---|
| input | none — everything is generated | somebody else's dataset |
| dependencies | standard library only | numpy and friends are allowed |
| network | never | required, and explicit |
| determinism | byte-identical rebuild | depends on an input that can move |
| output | a teaching figure | a number, with a receipt |

A reproduction cannot satisfy the figure contract, because it depends on a
file hosted somewhere else that can change under it. Letting one into
`figures/` would silently weaken a stated invariant — "the scripts use the
Python standard library only, no matplotlib, no network access" — for every
figure, in order to accommodate one script. So they live here instead, and
`figures/` is untouched.

## Four statements, not one badge

The repository badges figures `ILLUSTRATIVE`, `CALIBRATED` or `ANALYTIC`.
A reanalysis does not fit any of them, and adding `REPRODUCED` as a fourth
would paper over the distinction that actually matters: *which part* was
reproduced. Every directory here states four things separately.

- **Source** — the exact URL, the SHA-256 of the bytes used, and the row
  count. Not "the author's data": *these* bytes.
- **Analysis** — whose method. Theirs re-run, or ours applied to their data.
  These are different claims and only one of them is a reproduction.
- **Execution** — `COMPLETED` only after a real run against a real file. A
  receipt written by a script that did not read the input is worth nothing,
  and is the specific failure this directory was created in response to.
- **Scope** — what the result does *not* establish. Usually the most
  important line.

## What a reproduction here must do

Three acceptance tests, all cheap, all required. They exist because an
earlier candidate for this directory failed all three while looking correct:
its figure was a plot of thirty-one numbers typed into the script, its
manifest said `NOT RUN`, and its numbers were nonetheless exactly right. A
verified calculation is not a reproducible artifact.

1. **Read the input.** Perturbing values in the source file must change the
   output. Demonstrate it, don't assert it.
2. **Fail loudly without it.** No input, no silent fallback, no cached
   constants — a clear message naming the source, and a non-zero exit.
3. **Pin the bytes.** Record the SHA-256 the analysis was written against and
   say so when the input no longer matches. Upstream `main` moves.

## Why not just cite the paper

Because the interesting results are the ones the authors did not report. The
first reproduction here finds that the dataset prefers a segmented model its
own paper does not fit, and that the published exclusion of PCN below 1 is a
truncation of the dependent variable rather than a quality filter. Neither is
visible from the abstract, and neither is a criticism — they are consequences
of choices the papers state plainly and that nobody had followed through.

## Contents

| directory | study | what it establishes |
|---|---|---|
| [`ramiro-scaling/`](ramiro-scaling/) | Ramiro-Martinez et al. (2025) | per-genus scaling across all nine genera; the genera are not distinguishable; the breakpoint replicates on a second dataset, but is a between-family feature rather than a threshold on size ([report](ramiro-scaling/REPORT.md), [explorer](ramiro-scaling/explore.ipynb)) |
