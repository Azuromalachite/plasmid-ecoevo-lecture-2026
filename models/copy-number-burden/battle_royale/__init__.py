"""Battle Royale: importable pieces of the copy-number/burden model.

`battle-royale.ipynb` is the model. This package is where its functions move
as they are extracted, so that they can be imported, tested and reused without
executing a 46-cell notebook.

The extraction is deliberately incremental, and additive-first: a new module
can be added without touching the notebook, whereas moving existing code out
of it changes behaviour until proven otherwise. The order below is the planned
one; modules appear here only once their contents have been migrated AND the
notebook has been shown to produce identical output.

    config       BETA, LOSS_PER_DIVISION, PCN bounds, the validators
    analytic     relative_growth, log2_score, analytic_optimal_pcn, score_ratio
    dynamic      dynamic_copy_profile
    shared_flask simulate_shared_batch
    mechanistic  substrate depletion and dynamic C(t)
    single_cell  the particle simulation
    figures      new_fig, seq_colors, font and colormap setup
    checks       the QA audit, runnable outside the notebook

How to migrate one of them safely
---------------------------------
1. Run the notebook and capture every stream output (15 cells currently
   produce one). That is the baseline.
2. Move one section's functions into a module; have the notebook import them
   instead of defining them.
3. Re-run and diff the streams. Identical output is the only evidence the
   move preserved behaviour; "it still runs" is not.

Two things resist extraction and should stay in the notebook: the `# @title`
and `# @param` annotations, which are Colab form widgets rather than Python,
and the interleaved prose, which is the teaching.

Extracted so far: `config`, `analytic`, `dynamic`, `shared_flask`,
`mechanistic`, `single_cell` and `segregation`. Each move was verified by the
before/after stream diff above; the notebook's 15 output-producing cells were
byte-identical every time.

Still in the notebook, deliberately: the figure helpers, because nearly every
plotting cell uses them and moving them buys import churn rather than clarity;
and the QA audit, which is narrative as much as test.

`segregation` is the one module that was never in the notebook. It was written
here directly, since nothing depended on it and adding it could not change
existing output.
"""

from . import (analytic, config, dynamic, mechanistic,  # noqa: F401
               segregation, shared_flask, single_cell)

__all__ = ["analytic", "config", "dynamic", "mechanistic",
           "segregation", "shared_flask", "single_cell"]
