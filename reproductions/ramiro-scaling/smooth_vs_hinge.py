#!/usr/bin/env python3
"""A hinge beating a straight line is not evidence of a threshold.

RESULTS.md compares a segmented fit against a single line and reads the
win as a breakpoint at 1.73% of chromosome. But a smoothly curving
relationship also beats a straight line, and the comparison that was never
run is hinge against smooth at the same number of parameters.

Fitted here, all on the same records:

    line                     k=2
    quadratic                k=3
    hinge, knee searched     k=4   (intercept, slope, slope change, knee)
    cubic                    k=4
    natural spline, 4 knots  k=4
    natural spline, 5 knots  k=5

Three ways of choosing between them, because AIC alone is what this
document over-relied on:

    AIC and BIC          in-sample, two different complexity penalties
    5-fold random CV     predicts unseen plasmids
    leave-one-group-out  predicts unseen LINEAGES, which is the question
                         "is the bend shared?" actually asks

Plus a cluster bootstrap interval on the knee itself. A threshold quoted
to three significant figures should have an interval narrow enough to
justify them.

Both files are accepted. Running the second one as it ships reverses every
answer, and that reversal is an artefact of two things the comparison was
not controlling: the two files cover different domains, and their natural
cluster units hold 28.5 and 2.6 plasmids respectively, so one bootstrap is
far more conservative than the other. --max-x, --min-pcn and --group exist
to match those, and matched, the two files agree. See OF-28.

Usage:
    python -I smooth_vs_hinge.py curateddataset.csv [--boot 400]
    python -I smooth_vs_hinge.py maddamsetti_supplementary_table_3.csv \\
        --group genus --max-x 10.13 --min-pcn 1
"""
import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

GRID_N = 200


def lstsq(M, y):
    beta, *_ = np.linalg.lstsq(M, y, rcond=None)
    return beta


def rcs(x, knots):
    """Harrell's restricted cubic spline basis: intercept + x + K-2 terms."""
    t = np.asarray(knots, float)
    K = len(t)
    den = (t[-1] - t[0]) ** 2
    cols = [np.ones(len(x)), x]
    for j in range(K - 2):
        a = np.maximum(0.0, x - t[j]) ** 3
        b = (np.maximum(0.0, x - t[K - 2]) ** 3
             * (t[K - 1] - t[j]) / (t[K - 1] - t[K - 2]))
        c = (np.maximum(0.0, x - t[K - 1]) ** 3
             * (t[K - 2] - t[j]) / (t[K - 1] - t[K - 2]))
        cols.append((a - b + c) / den)
    return np.column_stack(cols)


def design(name, x, fitted=None):
    """Return (matrix, k, state). state carries anything learned on train."""
    if name == "line":
        return np.column_stack([np.ones(len(x)), x]), 2, None
    if name == "quadratic":
        return np.column_stack([np.ones(len(x)), x, x ** 2]), 3, None
    if name == "cubic":
        return np.column_stack([np.ones(len(x)), x, x ** 2, x ** 3]), 4, None
    if name.startswith("spline"):
        nk = int(name.split("-")[1])
        t = fitted if fitted is not None else np.quantile(
            x, np.linspace(0.05, 0.95, nk))
        return rcs(x, t), nk, t
    raise ValueError(name)


def hinge_design(x, c):
    return np.column_stack([np.ones(len(x)), x, np.maximum(0.0, x - c)])


def search_knee(x, y, grid):
    best = None
    for c in grid:
        M = hinge_design(x, c)
        r = y - M @ lstsq(M, y)
        s = float((r * r).sum())
        if best is None or s < best[0]:
            best = (s, c)
    return best[1]


def ic(sse_, n, k):
    ll = -0.5 * n * (np.log(2 * np.pi * sse_ / n) + 1)
    return -2 * ll + 2 * k, -2 * ll + k * np.log(n), ll


MODELS = ["line", "quadratic", "hinge", "cubic", "spline-4", "spline-5"]


def fit_predict(name, xtr, ytr, xte, grid):
    """Fit on train, return predictions on test and the parameter count."""
    if name == "hinge":
        c = search_knee(xtr, ytr, grid)
        b = lstsq(hinge_design(xtr, c), ytr)
        return hinge_design(xte, c) @ b, 4
    M, k, st = design(name, xtr)
    b = lstsq(M, ytr)
    Mte, _, _ = design(name, xte, fitted=st)
    return Mte @ b, k


def load(path, max_x=None, min_pcn=None, group=None):
    """Either file. Returns x, y, group label, and what the group is.

    max_x and min_pcn exist to ask one specific question: the two files do
    not cover the same domain, so a disagreement between them might be
    about the data or merely about where each one looks. Restricting the
    larger file to the smaller one's domain separates those.

    Ramiro publishes Logsize, PCN, Length_chr and a PTU call, so the
    natural held-out unit is the PTU. Maddamsetti publishes a normalised
    length and a copy number but no PTU, and its rows share a chromosome
    coverage per assembly, so the natural held-out unit is the assembly --
    which is also the sharper clustering of the two, since every plasmid in
    a genome shares one denominator exactly rather than approximately.
    """
    head = Path(path).open(encoding="utf-8-sig", newline="").readline()
    ramiro = "Logsize" in head
    rows = []
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f, delimiter="\t" if ramiro else ",")
        for r in rd:
            try:
                if ramiro:
                    rel = (10 ** float(r["Logsize"])) / float(r["Length_chr"])
                    pcn = float(r["PCN"])
                    g = (r.get("Predicted_ptu") or "-").strip() or "-"
                else:
                    if r["SeqType"].strip().lower() != "plasmid":
                        continue
                    rel = float(r["normalized_replicon_length"])
                    pcn = float(r["PIRACopyNumber"])
                    col = {"organism": "Organism", "genus": "Genus"}.get(
                        group, "AnnotationAccession")
                    g = r[col].strip() or "-"
            except (TypeError, ValueError, KeyError):
                continue
            if pcn <= 0 or rel <= 0:
                continue
            if max_x is not None and 100 * rel > max_x:
                continue
            if min_pcn is not None and pcn < min_pcn:
                continue
            rows.append((np.log10(100 * rel), np.log10(pcn), g))
    assert rows, "no usable rows; is this one of the two expected files?"
    return (np.array([r[0] for r in rows]), np.array([r[1] for r in rows]),
            np.array([r[2] for r in rows]),
            "PTU" if ramiro else (group or "assembly"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--boot", type=int, default=400)
    ap.add_argument("--max-x", type=float, default=None,
                    help="drop plasmids above this %% of chromosome")
    ap.add_argument("--min-pcn", type=float, default=None,
                    help="drop plasmids below this copy number")
    ap.add_argument("--group", choices=("assembly", "organism", "genus"),
                    default="assembly",
                    help="held-out and bootstrap unit (Maddamsetti only; "
                         "Ramiro always uses the PTU)")
    a = ap.parse_args()

    X, Y, G, unit = load(a.data, a.max_x, a.min_pcn, a.group)
    n = len(X)
    grid = np.linspace(np.quantile(X, .08), np.quantile(X, .92), GRID_N)
    lim = []
    if a.max_x is not None:
        lim.append(f"x <= {a.max_x}% of chromosome")
    if a.min_pcn is not None:
        lim.append(f"PCN >= {a.min_pcn}")
    print(f"{n:,} plasmids, {len(set(G)):,} {unit} labels "
          f"({n/len(set(G)):.1f} per block), held out by {unit}")
    if lim:
        print("  restricted to " + " and ".join(lim))
    print()

    # ---- in sample -----------------------------------------------------
    print(f"  {'model':<16}{'k':>3}{'AIC':>12}{'BIC':>12}"
          f"{'dAIC vs line':>14}{'dBIC vs line':>14}")
    base = None
    insample = {}
    for name in MODELS:
        if name == "hinge":
            c = search_knee(X, Y, grid)
            M = hinge_design(X, c)
            k = 4
        else:
            M, k, _ = design(name, X)
        r = Y - M @ lstsq(M, Y)
        s = float((r * r).sum())
        A, B, _ = ic(s, n, k)
        insample[name] = (A, B, k)
        if base is None:
            base = (A, B)
        print(f"  {name:<16}{k:>3}{A:>12.1f}{B:>12.1f}"
              f"{A-base[0]:>+14.1f}{B-base[1]:>+14.1f}")

    hA = insample["hinge"][0]
    print("\n  hinge against the matched-k smooths:")
    for alt in ("cubic", "spline-4"):
        d = insample[alt][0] - hA
        who = "hinge" if d > 0 else alt
        print(f"    vs {alt:<12} dAIC {d:+7.1f}  -> {who} preferred"
              f"{'  (both k=4)' if insample[alt][2] == 4 else ''}")

    # ---- cross-validation ----------------------------------------------
    rng = np.random.default_rng(7)

    def cv(folds):
        out = defaultdict(list)
        for tr, te in folds:
            for name in MODELS:
                p, _ = fit_predict(name, X[tr], Y[tr], X[te], grid)
                out[name].append(float(((Y[te] - p) ** 2).mean()))
        return {k: float(np.mean(v)) for k, v in out.items()}

    order = rng.permutation(n)
    rand_folds = [(np.setdiff1d(order, f), f) for f in np.array_split(order, 5)]
    gl = sorted(set(G))
    rng.shuffle(gl)
    gchunks = np.array_split(np.array(gl, dtype=object), 5)
    grp_folds = []
    for ch in gchunks:
        te = np.where(np.isin(G, ch))[0]
        grp_folds.append((np.setdiff1d(np.arange(n), te), te))

    r_cv, g_cv = cv(rand_folds), cv(grp_folds)
    print(f"\n  {'model':<16}{'random 5-fold MSE':>20}"
          f"{'leave-' + unit + '-out MSE':>24}")
    for name in MODELS:
        print(f"  {name:<16}{r_cv[name]:>20.5f}{g_cv[name]:>24.5f}")
    bestr = min(r_cv, key=r_cv.get)
    bestg = min(g_cv, key=g_cv.get)
    print(f"\n  random split prefers    {bestr}")
    print(f"  leave-{unit}-out prefers   {bestg}")
    print(f"  hinge is {100*(r_cv['hinge']/r_cv[bestr]-1):+.2f}% off the best "
          f"on random folds and "
          f"{100*(g_cv['hinge']/g_cv[bestg]-1):+.2f}% on held-out lineages")

    # ---- the knee, with an interval -------------------------------------
    c_hat = search_knee(X, Y, grid)
    idx = defaultdict(list)
    for i, g in enumerate(G):
        idx[g].append(i)
    keys = list(idx)
    knees = []
    for _ in range(a.boot):
        pick = rng.choice(len(keys), len(keys), replace=True)
        sel = np.concatenate([idx[keys[i]] for i in pick])
        knees.append(search_knee(X[sel], Y[sel], grid))
    kn = 10 ** np.array(knees)
    lo, hi = np.percentile(kn, [2.5, 97.5])
    print(f"\n  knee {10**c_hat:.2f}% of chromosome")
    plural = {"assembly": "assemblies", "genus": "genera"}.get(
        unit, unit + "s")
    print(f"  cluster bootstrap over {plural}, {a.boot} reps: "
          f"95% interval [{lo:.2f}%, {hi:.2f}%]")
    print(f"  that interval spans a factor of {hi/lo:.1f}")
    assert hi > lo, "degenerate bootstrap interval"
    if hi / lo > 2:
        print("  -> too wide to justify quoting the knee to three "
              "significant figures")


if __name__ == "__main__":
    main()
