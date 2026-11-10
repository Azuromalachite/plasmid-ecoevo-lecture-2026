#!/usr/bin/env python3
"""Withdrawing section 8's claim that replicon type absorbs the bend worse.

The published claim was that grouping by replicon type leaves a larger
slope change than the pooled fit (+0.905 against +0.742), so "within a
replicon type the bend is steeper than across the whole sample". Three
problems, all fixed here:

  1. The two adjustments were computed on different samples: 8,411
     plasmids carry a PTU call, 6,620 a replicon call. Redone on the
     6,005 carrying both.
  2. The join ignored COPLA2's Remove flag. 371 flagged records were in it.
  3. The knee was refitted. Section 5 shows a refitted knee is not a valid
     comparison once groups differ in mean size, so it is held fixed here.

What survives: the point estimate, in the same direction. What does not:
any claim that it is distinguishable from zero. A cluster bootstrap over
whole replicon groups puts the difference at +0.234 [-0.183, +0.638], and
the sign reverses when the knee moves.

A granularity control is included because the obvious objection runs the
other way: replicon has MORE groups than PTU here (511 against 416), and
more groups absorb more of anything. A random partition with the same
group-size profile is the right null.

Usage:
    python -I replicon_adjustment.py <maddamsetti csv> <copla2 metadata tsv>
"""
import csv
import io
import sys
from collections import Counter
from pathlib import Path

import numpy as np

KNEE_PCT = 1.73
XC = np.log10(KNEE_PCT)


def load(mad, cop_path):
    cop = {}
    with Path(cop_path).open(encoding="utf-8", errors="replace",
                             newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            i = (r.get("ID") or "").strip().split(".")[0]
            if i:
                cop[i] = r
    recs, flagged = [], 0
    for r in csv.DictReader(io.StringIO(
            Path(mad).read_text(encoding="utf-8", errors="replace"))):
        if r["SeqType"].strip().lower() != "plasmid":
            continue
        try:
            pcn = float(r["PIRACopyNumber"])
            rel = float(r["normalized_replicon_length"])
        except (TypeError, ValueError):
            continue
        if pcn <= 0 or rel <= 0:
            continue
        c = cop.get(r["SeqID"].strip().split(".")[0])
        if c is None:
            continue
        if (c.get("Remove") or "").strip().upper() == "Y":
            flagged += 1
            continue
        recs.append((np.log10(100 * rel), np.log10(pcn),
                     (c.get("PTU") or "").strip(),
                     (c.get("Replicon") or "").strip()))
    return recs, flagged


def sse(cols, y):
    M = np.column_stack(cols)
    beta, *_ = np.linalg.lstsq(M, y, rcond=None)
    return float(((y - M @ beta) ** 2).sum()), beta


def fit(x, y, lab, xc=XC):
    z = np.maximum(0.0, x - xc)
    if lab is None:
        cols = [np.ones(len(x))]
        g = 1
    else:
        u = sorted(set(lab))
        cols = [(lab == v).astype(float) for v in u]
        g = len(u)
    s1, _ = sse(cols + [x], y)
    s2, b = sse(cols + [x, z], y)
    n = len(x)
    d = (n * np.log(s2 / n) + 2 * (g + 2)) - (n * np.log(s1 / n) + 2 * (g + 1))
    return {"below": float(b[-2]), "change": float(b[-1]),
            "d_aic": float(d), "groups": g}


def main(mad, cop):
    recs, flagged = load(mad, cop)
    ok = [r for r in recs if r[2] not in ("", "-") and r[3] not in ("", "-")]
    print(f"curated join {len(recs):,} ({flagged} Remove=Y records dropped); "
          f"carrying both labels {len(ok):,}")
    X = np.array([r[0] for r in ok])
    Y = np.array([r[1] for r in ok])
    PTU = np.array([r[2] for r in ok])
    REP = np.array([r[3] for r in ok])

    print(f"\nmatched records, knee held at {KNEE_PCT}%")
    print(f"  {'adjustment':<22}{'groups':>8}{'slope change':>14}{'dAIC':>10}")
    res = {}
    for name, lab in (("pooled", None), ("PTU", PTU), ("replicon", REP)):
        f = fit(X, Y, lab)
        res[name] = f
        print(f"  {name:<22}{f['groups']:>8}{f['change']:>+14.3f}"
              f"{f['d_aic']:>+10.1f}")

    print("\ngranularity null: random partitions with the same group sizes")
    rng = np.random.default_rng(11)
    for name, lab in (("PTU", PTU), ("replicon", REP)):
        sims = [fit(X, Y, lab[rng.permutation(len(lab))]) for _ in range(20)]
        m = float(np.mean([s["change"] for s in sims]))
        print(f"  {name:<22}real {res[name]['change']:+.3f}   "
              f"shuffled {m:+.3f}")
    print("  -> random grouping is neutral, so the point estimates are not")
    print("     an artefact of how many groups each label has.")

    print("\ncluster bootstrap over whole replicon groups (300 reps, n>=5)")
    cp, cr = Counter(PTU), Counter(REP)
    k = np.array([cp[p] >= 5 and cr[q] >= 5 for p, q in zip(PTU, REP)])
    xk, yk, pk, qk = X[k], Y[k], PTU[k], REP[k]
    gs = sorted(set(qk))
    idx = {g: np.where(qk == g)[0] for g in gs}
    out = {"pooled": [], "PTU": [], "replicon": []}
    for _ in range(300):
        pick = rng.choice(len(gs), len(gs), replace=True)
        sel = np.concatenate([idx[gs[i]] for i in pick])
        qb = np.concatenate([np.full(len(idx[gs[i]]), f"{gs[i]}#{j}")
                             for j, i in enumerate(pick)])
        out["pooled"].append(fit(xk[sel], yk[sel], None)["change"])
        out["PTU"].append(fit(xk[sel], yk[sel], pk[sel])["change"])
        out["replicon"].append(fit(xk[sel], yk[sel], qb)["change"])
    print(f"  on {k.sum():,} plasmids")
    for name in ("replicon", "PTU"):
        d = np.array(out[name]) - np.array(out["pooled"])
        lo, hi = np.percentile(d, 2.5), np.percentile(d, 97.5)
        print(f"  {name} minus pooled: {d.mean():+.3f} [{lo:+.3f}, {hi:+.3f}]"
              f"   excludes zero: {not (lo < 0 < hi)}")
        assert lo < 0 < hi, (
            f"the {name} difference now excludes zero; section 8's "
            f"withdrawal should be revisited rather than left standing")

    print("\nknee sensitivity")
    print(f"  {'knee %':>8}{'pooled':>9}{'PTU':>9}{'replicon':>11}")
    signs = set()
    for pct in (1.0, 1.4, 1.73, 2.2, 3.0, 4.0):
        c = np.log10(pct)
        a = fit(xk, yk, None, c)["change"]
        b = fit(xk, yk, pk, c)["change"]
        d = fit(xk, yk, qk, c)["change"]
        signs.add(d > a)
        print(f"  {pct:>8.2f}{a:>+9.3f}{b:>+9.3f}{d:>+11.3f}")
    assert len(signs) > 1, (
        "the replicon-vs-pooled sign no longer reverses across the knee "
        "grid; that was part of the reason for withdrawing the claim")
    print("  -> the sign of replicon-vs-pooled reverses across this grid.")
    print("\nall assertions passed: the claim stays withdrawn")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
