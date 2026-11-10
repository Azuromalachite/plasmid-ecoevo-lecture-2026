#!/usr/bin/env python3
"""What unit is PIRASequencingCoverage in?

RESULTS.md section 7 originally read that column as base depth and argued
from "0.6x coverage" that the sub-one-copy tail was partly a measurement
artefact. This script is the check that withdrew the argument.

The column is mapped READS PER BASE: it equals PIRAReadCount divided by
replicon_length, exactly, for every row. A value of 0.57 on a 111,773 bp
plasmid is 63,279 mapped reads, not a sixth of a read per base.

The units cancel in the copy-number ratio, so no fitted result changes --
only the interpretation of measurement quality.

Usage:
    python -I coverage_units.py <maddamsetti supplementary csv>
"""
import csv
import io
import math
import statistics as st
import sys
from pathlib import Path


def main(path):
    rows = list(csv.DictReader(io.StringIO(
        Path(path).read_text(encoding="utf-8", errors="replace"))))

    def num(r, k):
        try:
            return float(r[k])
        except (TypeError, ValueError, KeyError):
            return None

    # --- the unit test -----------------------------------------------
    checked = bad = 0
    worst = 0.0
    for r in rows:
        rc, ln = num(r, "PIRAReadCount"), num(r, "replicon_length")
        cv = num(r, "PIRASequencingCoverage")
        if not rc or not ln or not cv or ln <= 0 or cv <= 0:
            continue
        checked += 1
        err = abs(rc / ln - cv) / cv
        worst = max(worst, err)
        if err > 1e-6:
            bad += 1
    print(f"coverage == PIRAReadCount / replicon_length ?")
    print(f"  {checked:,} rows checked, {bad} deviating by more than 1e-6, "
          f"worst {worst:.2e}")
    assert checked > 10_000, "too few rows checked to conclude anything"
    assert bad == 0, (
        f"{bad} rows break the identity; the column is NOT reads per base "
        f"and the units note in RESULTS.md section 7 must be revisited")
    print("  -> the column is MAPPED READS PER BASE, not base depth.\n")

    # --- what that means for the low tail -----------------------------
    plas = []
    for r in rows:
        if r["SeqType"].strip().lower() != "plasmid":
            continue
        pcn, ln = num(r, "PIRACopyNumber"), num(r, "replicon_length")
        rc, cv = num(r, "PIRAReadCount"), num(r, "PIRASequencingCoverage")
        cc = num(r, "PIRALongestRepliconCoverage")
        if not all((pcn, ln, rc, cv, cc)) or min(pcn, ln, rc, cv, cc) <= 0:
            continue
        plas.append({"pcn": pcn, "len": ln, "rc": rc, "cv": cv, "cc": cc})

    def band(r):
        return ("below one copy" if r["pcn"] < 1
                else "132 and up" if r["pcn"] >= 132 else "1 to 132")

    print(f"  {'group':<16}{'n':>7}{'med reads/base':>16}"
          f"{'med read count':>16}{'Poisson rel SE':>16}")
    for g in ("below one copy", "1 to 132", "132 and up"):
        v = [r for r in plas if band(r) == g]
        rc = st.median([r["rc"] for r in v])
        print(f"  {g:<16}{len(v):>7}{st.median([r['cv'] for r in v]):>16.2f}"
              f"{rc:>16,.0f}{100/math.sqrt(rc):>15.2f}%")

    # The file has a hard floor at 10,000 mapped reads, so asking whether
    # any row falls under 1,000 is unfalsifiable -- it reports the upstream
    # selection, not the sequencing. Detect the floor instead, and fail if
    # it ever moves, which is a thing that can happen.
    allrc = sorted(r["rc"] for r in plas)
    floor = allrc[0]
    near = sum(1 for v in allrc if v < floor * 1.01)
    print(f"\n  lowest mapped-read count in the file: {floor:,.0f}")
    print(f"  rows within 1% of it: {near}")
    assert 9_000 <= floor <= 11_000, (
        f"the read floor has moved to {floor:,.0f}; the selection this file "
        f"was published under has changed and \u00a77's framing needs "
        f"revisiting")
    print("  -> a floor at 10,000 with a pile-up just above it is an "
          "upstream")
    print("     filter. Any statement that no row is short of reads "
          "describes")
    print("     that selection, not the sequencing (OF-24).")

    # --- which half of the ratio drives the tails ---------------------
    def corr(a, b):
        ma, mb = st.mean(a), st.mean(b)
        num_ = sum((x - ma) * (y - mb) for x, y in zip(a, b))
        den = math.sqrt(sum((x - ma) ** 2 for x in a)
                        * sum((y - mb) ** 2 for y in b))
        return num_ / den

    lp = [math.log10(r["pcn"]) for r in plas]
    print(f"\n  corr(log copy number, log numerator)   = "
          f"{corr(lp, [math.log10(r['cv']) for r in plas]):+.3f}")
    print(f"  corr(log copy number, log denominator) = "
          f"{corr(lp, [math.log10(r['cc']) for r in plas]):+.3f}")
    print("  -> the tails are made in the numerator.")
    print("\nall assertions passed")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
