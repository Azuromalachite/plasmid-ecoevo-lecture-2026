#!/usr/bin/env python3
"""Reanalysis of the Ramiro-Martinez (2025) curated modelling dataset.

Writes receipt.json beside this file and prints a report.

WHAT THIS IS. An independent reanalysis of a public author dataset, not a
reproduction of any published figure. The input is the *curated modelling
subset* the authors ship for their machine-learning model, 3,961 records --
not the 6,327-plasmid set behind Fig. 5A. Those differ, and the difference is
visible: Klebsiella's slope here is -0.559 against roughly -0.63 in the
published figure. Nothing printed below should be described as reproducing a
published panel.

WHAT IT ESTABLISHES, and the reason it exists:

  1. Per-genus PTU-level slopes for ALL NINE genera, with standard errors, so
     that the spread between genera can be tested rather than eyeballed. It
     cannot be distinguished from zero: Q is below its degrees of freedom.
  2. The fitted exponent is strongly sensitive to the PCN floor. The authors
     excluded PCN < 1; raising the floor further flattens the slope
     monotonically and collapses R^2. The exclusion is a truncation of the
     dependent variable, not a neutral quality filter.
  3. On Maddamsetti's chromosome-normalised axis, THIS dataset prefers a
     segmented model by a large AIC margin and puts the breakpoint at ~1.7%
     of chromosome length, against Maddamsetti's published 1.84% -- derived
     from a different sample with a different coverage estimator. The
     authors' own paper fits a single power law and does not report this.

NETWORK. `figures/` is stdlib-only and offline by contract. This directory is
not: see ../README.md. The script never fetches silently -- without --fetch
it requires a local copy and says so.

Usage:
    python reproductions/ramiro-scaling/reproduce.py --fetch
    python reproductions/ramiro-scaling/reproduce.py --input path/to/file.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

SOURCE_URL = ("https://raw.githubusercontent.com/PaulaRamiro/NpAUREO/"
              "main/Model/curateddataset.csv")

#: The exact bytes this analysis was written against. `main` moves, so a
#: mismatch is not an error -- it is a notice that the input changed and the
#: numbers below may no longer be the ones in RESULTS.md.
EXPECTED_SHA256 = "23bee155b1c946bd565840c4cc0f5ac2e1fec6e4192578ba9f6752ee5f58f78f"
EXPECTED_ROWS = 3961

#: Published comparators, for the report only. Never used in a computation.
MADDAMSETTI = {"breakpoint_pct": 1.84, "slope_below": -0.880,
               "slope_above": -0.125, "doi": "10.1038/s41467-025-61205-2"}

# The segregation model is imported from the repository rather than
# reimplemented, for the reason the sibling figure script gives: a second
# copy of 2**(-2c) is a place for the two to drift apart. Loaded BY PATH, not
# as a package member -- battle_royale/__init__.py imports its scipy-backed
# siblings, and segregation.py itself is stdlib-only and should stay usable
# without them. The same trick is in figures/source/copy_number_and_loss_rate.py.
import importlib.util  # noqa: E402

_SEG_PATH = (REPO / "models" / "copy-number-burden" / "battle_royale"
             / "segregation.py")
_spec = importlib.util.spec_from_file_location("_segregation", _SEG_PATH)
segregation = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(segregation)


def load(path: Path):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(text.splitlines(), delimiter="\t"))
    recs = []
    for r in rows:
        try:
            pcn = float(r["PCN"])
            logsize = float(r["Logsize"])
            chrom = float(r["Length_chr"])
        except (KeyError, TypeError, ValueError):
            continue
        if pcn <= 0 or chrom <= 0:
            continue
        recs.append((r["Genus"].strip(), r["Predicted_ptu"].strip(),
                     logsize, pcn, chrom))
    return recs, digest, len(rows)


def ols(x, y):
    """Slope, standard error of the slope, and R^2."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    n = len(x)
    k, b = np.polyfit(x, y, 1)
    resid = y - (k * x + b)
    sse = float((resid ** 2).sum())
    sxx = float(((x - x.mean()) ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    se = math.sqrt(sse / (n - 2) / sxx) if n > 2 and sxx > 0 else float("nan")
    r2 = 1 - sse / sst if sst > 0 else float("nan")
    return k, se, r2


def ptu_points(recs):
    """Collapse records to one (median log size, log median PCN) per PTU."""
    g = defaultdict(list)
    for genus, ptu, logsize, pcn, _ in recs:
        g[(genus, ptu)].append((logsize, pcn))
    pts = {}
    for key, v in g.items():
        pts[key] = (float(np.median([a for a, _ in v])),
                    math.log10(float(np.median([b for _, b in v]))),
                    len(v))
    return pts


def hinge(x, y, c):
    """Continuous two-segment fit with the knee fixed at c."""
    M = np.column_stack([np.ones_like(x), x, np.maximum(x - c, 0.0)])
    beta, *_ = np.linalg.lstsq(M, y, rcond=None)
    return float(((y - M @ beta) ** 2).sum()), beta


def best_hinge(x, y, n_grid=400):
    grid = np.linspace(np.quantile(x, 0.05), np.quantile(x, 0.95), n_grid)
    sse, c = min((hinge(x, y, cc)[0], cc) for cc in grid)
    _, beta = hinge(x, y, c)
    return c, float(beta[1]), float(beta[1] + beta[2]), sse


def aic(sse, n, k):
    return n * math.log(sse / n) + 2 * k


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true",
                    help="download the source from the author's GitHub")
    ap.add_argument("--input", type=Path, default=HERE / "curateddataset.csv")
    args = ap.parse_args()

    if args.fetch and not args.input.exists():
        import urllib.request
        req = urllib.request.Request(
            SOURCE_URL, headers={"User-Agent": "plasmid-ecoevo-repro/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            args.input.write_bytes(r.read())

    if not args.input.exists():
        print(f"input not found: {args.input}\n"
              f"  re-run with --fetch, or pass --input <file>\n"
              f"  source: {SOURCE_URL}", file=sys.stderr)
        return 2

    recs, digest, n_raw = load(args.input)
    print(f"  input   {args.input.name}")
    print(f"  sha256  {digest}")
    if digest != EXPECTED_SHA256:
        print("  NOTE: input differs from the bytes this analysis was written"
              " against; numbers may not match RESULTS.md")
    print(f"  rows    {n_raw} parsed, {len(recs)} usable"
          f" (expected {EXPECTED_ROWS})")

    pcn = np.array([r[3] for r in recs])
    print(f"  PCN     min {pcn.min():.3f}  max {pcn.max():.1f}"
          f"  below 1: {int((pcn < 1).sum())}"
          "   <- the authors' stated exclusion, visible in the data")

    # --- 1. every genus -------------------------------------------------
    pts = ptu_points(recs)
    by_genus = defaultdict(list)
    for (genus, _), v in pts.items():
        by_genus[genus].append(v)

    print("\n  PER-GENUS PTU-LEVEL FIT")
    print(f"    {'genus':<16}{'PTUs':>5}{'recs':>7}{'slope':>9}"
          f"{'se':>8}{'R2':>8}")
    genus_rows = []
    for genus, v in sorted(by_genus.items(), key=lambda kv: -sum(p[2] for p in kv[1])):
        x = [p[0] for p in v]
        y = [p[1] for p in v]
        n_rec = sum(p[2] for p in v)
        if len(x) < 3:
            continue
        k, se, r2 = ols(x, y)
        genus_rows.append({"genus": genus, "ptus": len(x), "records": n_rec,
                           "slope": k, "se": se, "r2": r2})
        print(f"    {genus:<16}{len(x):>5}{n_rec:>7}{k:>9.3f}{se:>8.3f}{r2:>8.3f}")

    # --- 2. do the genera actually differ? ------------------------------
    k = np.array([g["slope"] for g in genus_rows])
    se = np.array([g["se"] for g in genus_rows])
    w = 1.0 / se ** 2
    pooled = float((w * k).sum() / w.sum())
    pooled_se = float(1.0 / math.sqrt(w.sum()))
    Q = float((w * (k - pooled) ** 2).sum())
    df = len(k) - 1
    i2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    print(f"\n  HOMOGENEITY  pooled {pooled:+.3f} +/- {pooled_se:.3f}"
          f"  (95% CI {pooled - 1.96 * pooled_se:+.3f}"
          f" to {pooled + 1.96 * pooled_se:+.3f})")
    print(f"    Q = {Q:.2f} on {df} df, I2 = {i2:.0f}%"
          f"   -> {'no detectable' if Q < df else 'some'} between-genus spread")

    # --- 3. sensitivity to the PCN floor --------------------------------
    L = np.array([r[2] for r in recs])
    Y = np.log10(pcn)
    print("\n  SENSITIVITY TO THE PCN FLOOR  (authors cut below 1)")
    print(f"    {'floor':>6}{'kept':>8}{'slope':>9}{'R2':>8}")
    floors = []
    for f in (1, 1.5, 2, 3, 5, 10):
        m = pcn >= f
        if m.sum() < 50:
            continue
        kk, _, rr = ols(L[m], Y[m])
        floors.append({"floor": f, "kept": int(m.sum()), "slope": kk, "r2": rr})
        print(f"    {f:>6}{int(m.sum()):>8}{kk:>9.3f}{rr:>8.3f}")

    # --- 4. the breakpoint, on Maddamsetti's axis -----------------------
    xn = np.log10(np.array([10 ** r[2] / r[4] for r in recs]))
    k1, _, _ = ols(xn, Y)
    sse1 = float(((Y - np.polyval(np.polyfit(xn, Y, 1), xn)) ** 2).sum())
    c, lo, hi, sse2 = best_hinge(xn, Y)
    n = len(xn)
    d_aic = aic(sse2, n, 4) - aic(sse1, n, 2)
    print("\n  SEGMENTED FIT ON CHROMOSOME-NORMALISED SIZE")
    print(f"    single line  slope {k1:+.3f}")
    print(f"    segmented    breakpoint {10 ** c * 100:.2f}% of chromosome,"
          f" slopes {lo:+.3f} then {hi:+.3f}")
    print(f"    dAIC {d_aic:+.1f}  ({'segmented' if d_aic < 0 else 'single'}"
          f" preferred)")
    print(f"    Maddamsetti published {MADDAMSETTI['breakpoint_pct']}%,"
          f" {MADDAMSETTI['slope_below']:+.3f} then"
          f" {MADDAMSETTI['slope_above']:+.3f}")

    # --- 5. what the breakpoint means for inheritance -------------------
    below = pcn[xn < c]
    above = pcn[xn >= c]
    m_lo, m_hi = float(np.median(below)), float(np.median(above))
    p_lo = segregation.p_daughter_free(m_lo)
    p_hi = segregation.p_daughter_free(m_hi)
    print("\n  WHAT THAT THRESHOLD COSTS  (via battle_royale.segregation)")
    print(f"    below  n={len(below):>5}  median PCN {m_lo:5.2f}"
          f"  -> {p_lo * 100:7.3f}% of daughters born plasmid-free")
    print(f"    above  n={len(above):>5}  median PCN {m_hi:5.2f}"
          f"  -> {p_hi * 100:7.3f}%")
    print(f"    ratio  {p_hi / p_lo:.0f}x"
          "   -- random segregation stops being survivable")
    print(f"    fraction with PCN<2:  below {float((below < 2).mean()):.1%},"
          f"  above {float((above < 2).mean()):.1%}"
          "   <- where the PCN floor bites")

    # --- 6. is the breakpoint a break, or a mixture of families? --------
    # RESULTS.md's own caveat: a segmented fit preferred by AIC on pooled
    # data is also what a mixture of replicon families with different
    # characteristic copy numbers produces. `Predicted_ptu` IS family-level
    # annotation, so the two are separable here.
    #
    # A real break is within-family: a family spanning the threshold kinks.
    # A mixture is between-family: remove the family means and it goes too.
    # Grouping is by PTU alone, not (genus, PTU) -- a PTU is already a
    # plasmid taxonomic unit, and splitting it by host would manufacture
    # families that do not exist.
    fam = defaultdict(list)
    for i, r in enumerate(recs):
        fam[r[1]].append(i)
    keep = {p: idx for p, idx in fam.items() if len(idx) >= 3}

    gm = xn.mean()
    tss_x = float(((xn - gm) ** 2).sum())
    within_x = 0.0
    cx, cy = [], []
    for idx in keep.values():
        xs, ys = xn[idx], Y[idx]
        within_x += float(((xs - xs.mean()) ** 2).sum())
        cx.extend(xs - xs.mean())
        cy.extend(ys - ys.mean())
    cx, cy = np.asarray(cx), np.asarray(cy)

    kc, _, _ = ols(cx, cy)
    sse1c = float(((cy - np.polyval(np.polyfit(cx, cy, 1), cx)) ** 2).sum())
    cc, loc, hic, sse2c = best_hinge(cx, cy)
    nc = len(cx)
    d_aic_c = aic(sse2c, nc, 4) - aic(sse1c, nc, 2)

    print("\n  BREAK, OR MIXTURE OF FAMILIES?")
    print(f"    families used            {len(keep)} PTUs with n>=3,"
          f" {nc} records")
    print(f"    variance in log size     {100 * within_x / tss_x:.1f}% within"
          f" family, {100 * (tss_x - within_x) / tss_x:.1f}% between")
    print(f"    pooled      dAIC {d_aic:+8.1f}   slopes"
          f" {lo:+.3f} then {hi:+.3f}")
    print(f"    family-centred dAIC {d_aic_c:+5.1f}   slopes"
          f" {loc:+.3f} then {hic:+.3f}   (single line {kc:+.3f})")

    # Could the centred test have SEEN a break? Centring removes most of the
    # x-range, so a null result might be blindness rather than absence.
    # Inject a break of exactly the pooled magnitude and try to recover it.
    delta = hi - lo
    power = []
    for q in (0.25, 0.50, 0.75):
        c0 = float(np.quantile(cx, q))
        inj = cy + delta * np.maximum(cx - c0, 0.0)
        s1 = float(((inj - np.polyval(np.polyfit(cx, inj, 1), cx)) ** 2).sum())
        _, _, _, s2 = best_hinge(cx, inj)
        power.append({"quantile": q, "knee": c0,
                      "delta_aic": aic(s2, nc, 4) - aic(s1, nc, 2)})
    print(f"    power check: inject the pooled break ({delta:+.3f}) into the"
          f" centred data")
    for p in power:
        print(f"      at q={p['quantile']:.2f}  dAIC {p['delta_aic']:+9.1f}"
              f"   {'recovered' if p['delta_aic'] < -10 else 'NOT recovered'}")

    # --- 6b. the test section 6 should have run ----------------------------
    # Centring x and y within PTU and then RESCANNING for a knee asks "is
    # there a kink anywhere in the within-family relationship". It does not
    # ask whether the kink AT the published breakpoint survives adjusting for
    # family: subtracting a different mean per family means a fixed plasmid
    # size no longer maps to one centred x. The second question is a
    # fixed-effects regression with c held FIXED, which by
    # Frisch-Waugh-Lovell is the within-transform applied to y, x and the
    # hinge term z = max(0, x - c). Demeaning z is the step section 6 omits.
    #
    # This matters: it is the difference between "the bend is between
    # families" and "most of the bend is between families". The second is
    # what the data support.
    zc = np.maximum(xn - c, 0.0)

    def _demean(v, g):
        out = np.empty_like(v)
        for p in np.unique(g):
            m = g == p
            out[m] = v[m] - v[m].mean()
        return out

    gk = np.array([recs[i][1] for i in range(len(recs))])
    inkeep = np.isin(gk, list(keep))
    gk, yk, xk, zk = gk[inkeep], Y[inkeep], xn[inkeep], zc[inkeep]
    yd2, xd2, zd2 = (_demean(yk, gk), _demean(xk, gk), _demean(zk, gk))
    nk = len(xk)

    def _sse(cols, yv):
        M = np.column_stack(cols)
        beta, *_ = np.linalg.lstsq(M, yv, rcond=None)
        return float(((yv - M @ beta) ** 2).sum()), beta

    sse_fe1, b_fe1 = _sse([xd2], yd2)
    sse_fe2, b_fe2 = _sse([xd2, zd2], yd2)
    n_ptu = len(np.unique(gk))
    d_fixed = (aic(sse_fe2, nk, n_ptu + 3) - aic(sse_fe1, nk, n_ptu + 2))

    straddle = [p for p in np.unique(gk)
                if (xk[gk == p] < c).any() and (xk[gk == p] >= c).any()]
    n_strad = int(sum((gk == p).sum() for p in straddle))

    print("\n  KNEE HELD AT THE PUBLISHED VALUE, PTU AS A FIXED EFFECT")
    print(f"    families straddling the knee  {len(straddle)} of {n_ptu},"
          f" holding {n_strad} of {nk} records")
    print(f"    slopes below / above          {b_fe2[0]:+.3f} /"
          f" {b_fe2[0] + b_fe2[1]:+.3f}   (change {b_fe2[1]:+.3f})")
    print(f"    dAIC                          {d_fixed:+.1f}"
          f"   vs {d_aic:+.1f} pooled and {d_aic_c:+.1f} when rescanned")

    # Where does the adjusted model want the knee?
    best_fe = None
    for cc in np.linspace(np.quantile(xk, 0.05), np.quantile(xk, 0.95), 400):
        s, b = _sse([xd2, _demean(np.maximum(xk - cc, 0.0), gk)], yd2)
        if best_fe is None or s < best_fe[0]:
            best_fe = (s, cc, b)
    sse_fe3, c_fe, b_fe3 = best_fe
    d_free = aic(sse_fe3, nk, n_ptu + 4) - aic(sse_fe1, nk, n_ptu + 2)
    print(f"    knee the adjusted model prefers  {10 ** c_fe * 100:.2f}% of"
          f" chromosome  (dAIC {d_free:+.1f})")
    print("    -- so the published 1.73% is not where the adjusted bend sits")

    loo = []
    for drop in ([], ["PTU-E1"], ["PTU-FE"], ["PTU-FK"],
                 ["PTU-E1", "PTU-FE", "PTU-FK"]):
        m = ~np.isin(gk, drop)
        g2, x2, y2 = gk[m], xk[m], yk[m]
        z2 = np.maximum(x2 - c, 0.0)
        a1, _ = _sse([_demean(x2, g2)], _demean(y2, g2))
        a2, ab = _sse([_demean(x2, g2), _demean(z2, g2)], _demean(y2, g2))
        n2, k2 = len(x2), len(np.unique(g2))
        loo.append({"excluded": drop, "n": n2,
                    "delta_aic": aic(a2, n2, k2 + 3) - aic(a1, n2, k2 + 2),
                    "slope_change": float(ab[1])})
    print("    leave-one-lineage-out:", ", ".join(
        f"{'none' if not r['excluded'] else '-'.join(s[4:] for s in r['excluded'])}"
        f" {r['delta_aic']:+.1f}" for r in loo))

    # Each family that spans the fitted breakpoint, on its own.
    print("\n    EACH SPANNING FAMILY")
    print(f"      {'PTU':<14}{'n':>5}{'below':>7}{'above':>7}"
          f"{'seg lo':>9}{'seg hi':>9}{'dAIC':>9}")
    per_family = []
    for p, idx in sorted(keep.items(), key=lambda kv: -len(kv[1])):
        xs, ys = xn[idx], Y[idx]
        nb, na = int((xs < c).sum()), int((xs >= c).sum())
        if nb < 5 or na < 5:
            continue
        s1 = float(((ys - np.polyval(np.polyfit(xs, ys, 1), xs)) ** 2).sum())
        _, flo, fhi, s2 = best_hinge(xs, ys)
        d = aic(s2, len(xs), 4) - aic(s1, len(xs), 2)
        per_family.append({"ptu": p, "n": len(idx), "below": nb, "above": na,
                           "slope_below": flo, "slope_above": fhi,
                           "delta_aic": d})
        print(f"      {p[:14]:<14}{len(idx):>5}{nb:>7}{na:>7}"
              f"{flo:>9.3f}{fhi:>9.3f}{d:>9.1f}")
    n_kink = sum(1 for f in per_family if f["delta_aic"] < -4)
    print(f"      {n_kink} of {len(per_family)} prefer a kink -- and the"
          f" directions disagree, which a shared threshold would not")

    receipt = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "COMPLETED",
        "scope": "independent reanalysis of a curated author subset; "
                 "NOT a reproduction of any published figure",
        "source": {"url": SOURCE_URL, "sha256": digest,
                   "sha256_expected": EXPECTED_SHA256,
                   "matches_expected": digest == EXPECTED_SHA256,
                   "rows_parsed": n_raw, "rows_used": len(recs)},
        "per_genus": genus_rows,
        "homogeneity": {"pooled_slope": pooled, "pooled_se": pooled_se,
                        "Q": Q, "df": df, "I2_percent": i2},
        "pcn_floor_sensitivity": floors,
        "segmented": {"single_slope": k1, "breakpoint_log10": c,
                      "breakpoint_percent_of_chromosome": 10 ** c * 100,
                      "slope_below": lo, "slope_above": hi,
                      "delta_aic_segmented_minus_single": d_aic,
                      "published_comparator": MADDAMSETTI},
        "inheritance": {"median_pcn_below": m_lo, "median_pcn_above": m_hi,
                        "p_daughter_free_below": p_lo,
                        "p_daughter_free_above": p_hi},
        "break_or_mixture": {
            "grouping": "Predicted_ptu alone, families with n>=3",
            "families": len(keep), "records": nc,
            "log_size_variance_within_family_percent":
                100 * within_x / tss_x,
            "pooled_delta_aic": d_aic,
            "family_centred_delta_aic": d_aic_c,
            "family_centred_single_slope": kc,
            "family_centred_slope_below": loc,
            "family_centred_slope_above": hic,
            "injected_break_magnitude": delta,
            "power_check": power,
            "per_family": per_family,
            "fixed_knee_ptu_fixed_effects": {
                "note": "knee HELD at the published breakpoint; PTU as a "
                        "fixed effect; the test section 6's rescan does not "
                        "perform",
                "families_straddling_knee": len(straddle),
                "records_straddling": n_strad,
                "slope_below": float(b_fe2[0]),
                "slope_above": float(b_fe2[0] + b_fe2[1]),
                "slope_change": float(b_fe2[1]),
                "delta_aic": d_fixed,
                "knee_preferred_by_adjusted_model_percent":
                    float(10 ** c_fe * 100),
                "delta_aic_free_knee": d_free,
                "leave_one_lineage_out": loo,
            },
        },
    }
    (HERE / "receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"\n  wrote {HERE / 'receipt.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
