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

## References

Held centrally in
[`evidence/references.bib`](../../evidence/references.bib) and cited by key.
