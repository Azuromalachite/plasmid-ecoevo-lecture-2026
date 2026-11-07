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
    leave-one-PTU-out CV predicts unseen LINEAGES, which is the question
                         "is the bend shared?" actually asks

Plus a cluster bootstrap interval on the knee itself. A threshold quoted
to three significant figures should have an interval narrow enough to
justify them.

Usage:
    python -I smooth_vs_hinge.py curateddataset.csv [--boot 400]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--boot", type=int, default=400)
    a = ap.parse_args()

    rows = []
    with Path(a.data).open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            try:
                xx, pcn = float(r["Logsize"]), float(r["PCN"])
                chrl = float(r["Length_chr"])
            except (TypeError, ValueError):
                continue
            if pcn <= 0 or chrl <= 0:
                continue
            rows.append((np.log10(100 * (10 ** xx) / chrl), np.log10(pcn),
                         (r.get("Predicted_ptu") or "-").strip() or "-"))
    X = np.array([r[0] for r in rows])
    Y = np.array([r[1] for r in rows])
    G = np.array([r[2] for r in rows])
    n = len(X)
    grid = np.linspace(np.quantile(X, .08), np.quantile(X, .92), GRID_N)
    print(f"{n:,} plasmids, {len(set(G))} PTU labels\n")

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
    print(f"\n  {'model':<16}{'random 5-fold MSE':>20}{'leave-PTU-out MSE':>20}")
    for name in MODELS:
        print(f"  {name:<16}{r_cv[name]:>20.5f}{g_cv[name]:>20.5f}")
    bestr = min(r_cv, key=r_cv.get)
    bestg = min(g_cv, key=g_cv.get)
    print(f"\n  random split prefers    {bestr}")
    print(f"  leave-PTU-out prefers   {bestg}")
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
    print(f"  cluster bootstrap over PTUs, {a.boot} reps: "
          f"95% interval [{lo:.2f}%, {hi:.2f}%]")
    print(f"  that interval spans a factor of {hi/lo:.1f}")
    assert hi > lo, "degenerate bootstrap interval"
    if hi / lo > 2:
        print("  -> too wide to justify quoting the knee to three "
              "significant figures")


if __name__ == "__main__":
    main()
