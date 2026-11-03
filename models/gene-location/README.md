# Gene location — why a plasmid rather than the chromosome?

Supports the lecture's regulation-versus-mobility slide, which asserts its
central distinction rather than deriving it.

## The question

> If the chromosome is a reliable storage system that can also regulate a
> conditionally useful gene, why put the gene on a plasmid at all?

The weak answer — *conditionally useful genes belong on plasmids because you
can switch them off* — is wrong, and the lecture already refuses it: a
chromosome can stockpile and regulate too. What replaces it has to be a
mechanism that is **not** about expression.

## What this model says

[`check_priority_effect.py`](check_priority_effect.py) derives one threshold
and checks one control. It is a reduction of a single mechanism from
[@lehtinen2021location], not a reproduction of their model.

Four states exist — sensitive, chromosomal, plasmid-borne, dual — and the
mechanism is that the **dual** state costs more and gains nothing:

```text
w_C = b − c_c − δ·x_P      chromosomal cell acquires a resistant plasmid
w_P = b − c_p − δ·x_C      plasmid-bearing cell acquires the chromosomal form
```

Three results, all machine-checked:

**1. The benefit cancels.** `b` does not appear in `w_C − w_P`. Under this
mechanism, *how useful the gene is cannot predict where it sits.* That is the
formal version of the lecture's refusal of the weak answer.

**2. Positive frequency dependence**, slope `2δ`: the commoner location gains
as it becomes commoner, because transfer into an already-resistant cell is
wasted. This is the direction the source reports, and getting it right matters
— the naive model, in which the plasmid's advantage is horizontal transfer
into non-carriers, gives the *opposite* sign.

**3. A priority effect, with a condition:**

```text
threshold   x_C* = (Rδ + c_c − c_p) / (2δ)

exists in (0, R)  ⟺  |c_c − c_p| < δ·R
```

Both pure states are locally stable, so whichever form arrives first is hard
to displace — **but only when the two locations differ in cost by less than
the redundancy penalty.** If one location is clearly cheaper than carrying
both is wasteful, it simply wins and history does not matter. History matters
precisely when the locations are close.

## The control

Setting `δ = 0` makes dual carriage exactly as good as single carriage. The
frequency dependence must then vanish and the cheaper location must win
outright. The script checks this first and **fails if it does not hold**.

This matters because the structure could manufacture a priority effect on its
own. The source says the dual-carrier penalty is "the only crucial assumption"
for the result; switching it off and watching the result disappear is how that
claim gets tested rather than repeated.

**The control reproduces a published sensitivity analysis, not merely a
sensible null.** `[L]` Verified in the published text:

> *"eliminating the additional cost from dual resistance, or increasing the
> benefit of dual resistance so much that it outweighs this additional cost,
> abolishes the region of bistability"* — [@lehtinen2021location]

That is exactly what `δ = 0` does and exactly what the script asserts happens.
The control was designed before this sentence was found, which makes the
agreement worth more than if it had been copied.

### The assumption that makes the benefit cancel

The derived result that `b` cancels — *how useful the gene is cannot predict
where it sits* — rests on an assumption the authors state and bound:

> `[L]` *"Throughout the work, we have made the assumption that the effect of
> the gene of interest … is the same on the chromosome and the plasmid: when
> this assumption does not hold, location can be trivially explained by the
> fitness difference."*

So the cancellation is a consequence of equal effects, not a general truth, and
the paper names where equal effects fails first:

> `[L]` *"the equal effects assumption would not hold for high copy number
> plasmids if gene expression levels increase with copy number"*

**That links this model to [`../copy-number-burden/`](../copy-number-burden/).**
The gene-location argument assumes equal effects; the copy-number model is
about precisely the regime where that assumption breaks. A lecture that uses
both must not let the audience carry the `b`-cancels conclusion into the
high-copy discussion — there, location is not neutral with respect to
usefulness, and the paper says so.

## Reading the literature lineage correctly

The lecture plan lists three papers as a *"useful literature lineage"*:
Eberhard 1989 → Svara & Rankin 2011 → Lehtinen et al. 2021. Presented as a
sequence, that implies accumulation. It is not one:

> `[L]` *"in presence of the non-beneficial plasmid, local adaptation does not
> explain why some genes are plasmid-borne"* — [@lehtinen2021location]

Local adaptation is [@eberhard1989genes]'s explanation. The third paper tests
it inside their model structure and reports that it fails there, replacing it
with frequency dependence and a priority effect. The scope condition matters —
this is a result about their model with a non-beneficial plasmid present, not
a general refutation — but a slide that presents the three as a cumulative
lineage is presenting a disagreement as a progression.

The honest framing is that the question *why is this gene here?* has at least
two live answers with different consequences: an adaptive one, under which
location is informative about the environment, and a historical one, under
which location is partly an accident locked in by priority. The second is the
more useful thing to teach, because it tells a designer that **observed gene
location is weak evidence about what is optimal**.

## Both regimes from one model

[`check_regime_boundary.py`](check_regime_boundary.py) goes further than
noting the disagreement: it makes the disagreement the specification. One
inequality, two corners, and the parameter that separates them.

The later paper states the assumption the earlier argument rests on —
*"outside the local niche with the beneficial gene, plasmids would not
persist"* — and then removes it. Removing it reverses the conclusion, because
if the gene-free version of the same plasmid already persists outside, the
resistant plasmid has few plasmid-free recipients left to colonise, and the
cells it does enter become dual carriers. Verified: *"Plasmid-borne resistance
benefits from the sensitive plasmid being rare."*

So the separating parameter is **q, the frequency of the gene-free plasmid
among potential recipients**:

```text
w_P − w_C  =  γ(1−q)  −  (c_p − c_c)  −  δ(x_C − x_P)
              mobility    carriage        redundancy
              is rented   cost gap        (priority effect)
```

| Corner | Regime | Outcome |
| --- | --- | --- |
| `q → 0` | Eberhard: no gene-free plasmid outside the niche | full transfer rate available; plasmid localisation can win |
| `q → 1` | Lehtinen: backbone persists everywhere without the gene | mobility term vanishes; the redundancy model remains |

**The earlier script is this one's `q → 1` limit**, checked symbolically — not
a rival to it. The boundary is `q* = (Rδ + c_c − c_p − 2δx_C + γ)/γ`, which at
the symmetric point is `1 − (c_p − c_c)/γ`.

The teaching line is in the first term: **mobility is rented from the ecology,
not owned by the plasmid.** Its value is multiplied by the fraction of
recipients still plasmid-free, and that fraction is a property of the world
outside the niche. Neither paper is wrong; they describe different ecologies.

Two controls, both failing the script if they break: `γ = 0` must collapse to
the redundancy model for every `q`, and `δ = 0` must remove the frequency
dependence so the boundary no longer depends on how common either form already
is — history stops mattering, which is correct for that control.

What it does not settle: which regime any real system is in. `q` is an
ecological measurement nobody has made here.

## What it does not show

- Not that real gene location is set this way.
- Not the published model's dynamics: transfer, loss and mutation rates are
  folded into `δ` and the costs, so nothing here speaks about rates.
- Not anything about this competition's constructs.

## Running it

```bash
uv run --no-project --with sympy python models/gene-location/check_priority_effect.py
```

Exit status is 1 if a derivation stops reproducing.

## Source provenance — which version the quotations come from

Every sentence quoted on this page was checked against the **published**
Evolution Letters text at `10.1002/evl3.226`. The published Discussion
contains the cleanest single statement of the boundary this directory models:

> *"Thus, local adaptation only favors plasmid-borne resistance if the
> frequency of the sensitive plasmid is low outside the local niche."*

**Quote the published text and cite the DOI**, because that is the version of
record and its wording is what a reader will find.

### A correction, kept rather than edited away

The first version of this section said that sentence was *"not present in the
bioRxiv version"*. **That was false.** `[M]` It is present in bioRxiv v2
(`10.1101/2020.08.04.236455`), differing by one letter — the preprint has
British *"favours"* where the copy-edited published text has *"favors"*:

> *"Thus, local adaptation only **favours** plasmid-borne resistance if the
> frequency of the sensitive plasmid is low outside the local niche."*

The claim was made because a case-insensitive, whitespace-normalised search of
the preprint returned nothing — the variant axis was **orthography**, which
that search did not defeat. It is the third false negative of its kind in one
day: whitespace, then case, then en-GB against en-US.

`[I]` Worth keeping because of what it was: an **absence claim** published in
the same changeset that added the rule *"an absence claim is a claim; it needs
its own evidence"*. The rule was right and its author was its first casualty.

**For retrieval from published text, defeat at least:** whitespace, case,
British/American spelling, hyphenation, and smart versus straight quotes. The
practical form is to search a distinctive fragment containing none of them —
`plasmid-borne resistance if the frequency of the sensitive plasmid is low`
matches both documents on the first attempt.

## References

Held centrally in
[`evidence/references.bib`](../../evidence/references.bib) and cited by key.
