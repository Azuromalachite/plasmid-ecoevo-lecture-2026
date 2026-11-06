#!/usr/bin/env python3
"""Replicate the central finding on an independent, accession-keyed dataset.

WHY THIS EXISTS. Everything in RESULTS.md rests on one file: the Ramiro
modelling subset, 3,961 plasmids, no accession of any kind, copy numbers
below one already removed, and a family label whose relationship to
replication machinery the report had to concede was unmeasured. Three
separate limitations, all of them traceable to that one file.

COPLA2's RefSeq 224 reference database removes all three at once. It carries
`ID` (a RefSeq accession), `PTU`, `Replicon`, `MOB` and a host-range grade
for 89,393 plasmids, and Maddamsetti's Supplementary Data 1 carries RefSeq
accessions beside its copy numbers. The two join.

WHAT IT ANSWERS:

  1. Does the pooled bend replicate on a different, larger sample?
  2. Does the residual after absorbing family replicate?
  3. Does REPLICON TYPE absorb the bend better than PTU does? The report
     states that a PTU is not a replicon family and that nothing available
     measured the difference. This measures it.

WHAT IT DOES NOT ANSWER. Copy number is still modelled from coverage with no
published uncertainty, plasmids within a family are still related by descent,
and a replicon type is still an annotation rather than an experiment. A
larger sample does not repair any of that.

NETWORK. Two downloads, both hash-checked, both into --work. The COPLA2
metadata is about 46 MB.

Usage:
    python reproductions/ramiro-scaling/copla_replication.py --work /tmp/j
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

SOURCES = {
    "maddamsetti": {
        "url": ("https://static-content.springer.com/esm/"
                "art%3A10.1038%2Fs41467-025-61205-2/MediaObjects/"
                "41467_2025_61205_MOESM3_ESM.csv"),
        "sha256": "131faa58f5528d814877cca9ffa8c3e56b41e92518385d740c1b7e530f2bc3a7",
        "name": "41467_2025_61205_MOESM3_ESM.csv",
    },
    "copla2": {
        "url": "https://castillo.dicom.unican.es/copla2/data/refseq_224/metadata.tsv",
        "sha256": "ef2bc2a0bfecd08b",      # prefix; full value recorded on first run
        "name": "copla2_refseq224_metadata.tsv",
    },
}


def fetch(spec, work: Path, exploratory: bool):
    dest = work / spec["name"]
    if not dest.exists():
        req = urllib.request.Request(
            spec["url"], headers={"User-Agent": "plasmid-ecoevo-repro/1.0"})
        with urllib.request.urlopen(req, timeout=600) as r:
            dest.write_bytes(r.read())
    raw = dest.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    want = spec["sha256"]
    ok = got.startswith(want) if len(want) < 64 else got == want
    print(f"  {spec['name']:<42} {len(raw):>12,} bytes  "
          f"{'hash ok' if ok else 'HASH DIFFERS'}")
    if not ok and not exploratory:
        sys.exit(f"{spec['name']}: expected {want}, got {got}. "
                 "Re-run with --exploratory to proceed anyway.")
    return raw, got


def ols_seg(x, y, grid=400):
    def f(cols, yv):
        M = np.column_stack(cols)
        b, *_ = np.linalg.lstsq(M, yv, rcond=None)
        return float(((yv - M @ b) ** 2).sum()), b
    s1, b1 = f([np.ones_like(x), x], y)
    best = None
    for c in np.linspace(np.quantile(x, .05), np.quantile(x, .95), grid):
        s, b = f([np.ones_like(x), x, np.maximum(x - c, 0)], y)
        if best is None or s < best[0]:
            best = (s, c, b)
    return s1, b1, best, f


def check_percent(v):
    """x is log10 of a PERCENTAGE, so 10**c IS the percentage.

    Multiplying by 100 again reports a plasmid longer than its chromosome.
    That mistake has been made three times in this analysis -- in the
    notebook, in a scratch test, and here -- so it is now an assertion
    rather than a convention.
    """
    assert 0 < v < 100, f"bend of {v:.2f}% of a chromosome is not possible"
    return v


def aic(sse, n, k):
    return n * math.log(sse / n) + 2 * k


def absorb(x, y, lab, knee, f):
    """Knee held fixed, one intercept per group with at least three members."""
    cnt = Counter(lab)
    keep = np.array([cnt[v] >= 3 and v not in ("-", "", "NA") for v in lab])
    if keep.sum() < 200:
        return None
    x, y, g = x[keep], y[keep], lab[keep]
    z = np.maximum(x - knee, 0.0)

    def dm(v):
        o = np.empty_like(v, dtype=float)
        for p in np.unique(g):
            m = g == p
            o[m] = v[m] - v[m].mean()
        return o

    yd, xd, zd = dm(y), dm(x), dm(z)
    s1, _ = f([xd], yd)
    s2, b = f([xd, zd], yd)
    n, npt = len(x), len(np.unique(g))
    straddle = sum(1 for p in np.unique(g)
                   if (x[g == p] < knee).any() and (x[g == p] >= knee).any())
    return {"n": int(n), "groups": int(npt), "straddling": int(straddle),
            "slope_below": float(b[0]), "slope_above": float(b[0] + b[1]),
            "slope_change": float(b[1]),
            "delta_aic": aic(s2, n, npt + 3) - aic(s1, n, npt + 2)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", type=Path, required=True,
                    help="directory for the two downloads (its own, empty)")
    ap.add_argument("--exploratory", action="store_true",
                    help="continue when an input hash differs")
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)

    print("inputs")
    mad_raw, mad_sha = fetch(SOURCES["maddamsetti"], a.work, a.exploratory)
    cop_raw, cop_sha = fetch(SOURCES["copla2"], a.work, a.exploratory)

    csv.field_size_limit(10_000_000)
    cop = {}
    for r in csv.DictReader(
            io.StringIO(cop_raw.decode("utf-8", "replace")), delimiter="\t"):
        cop[r["ID"].strip()] = r

    rows = []
    for r in csv.DictReader(io.StringIO(mad_raw.decode("utf-8", "replace"))):
        if r["SeqType"].strip().lower() != "plasmid":
            continue
        try:
            pcn = float(r["PIRACopyNumber"])
            rel = float(r["normalized_replicon_length"])
        except (TypeError, ValueError):
            continue
        c = cop.get(r["SeqID"].strip())
        if c is None or pcn <= 0 or rel <= 0:
            continue
        rows.append({"x": math.log10(100 * rel), "y": math.log10(pcn),
                     "pcn": pcn, "ptu": c["PTU"], "rep": c["Replicon"],
                     "genus": (r.get("Genus") or "?").strip()})

    print(f"\nCOPLA2 RefSeq 224 {len(cop):,} plasmids; "
          f"joined to Maddamsetti on accession: {len(rows):,}")

    # how often does one PTU carry several replicon types?
    byptu = defaultdict(Counter)
    for r in rows:
        if r["ptu"] not in ("-", "", "NA") and r["rep"] not in ("-", "", "NA"):
            byptu[r["ptu"]][r["rep"]] += 1
    multi = sum(1 for v in byptu.values() if len(v) > 1)
    print(f"PTUs carrying more than one replicon type: {multi:,} of "
          f"{len(byptu):,}  -- a PTU is not a replicon family, measured")

    out = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "sources": {"maddamsetti_sha256": mad_sha, "copla2_sha256": cop_sha,
                       "copla2_release": "RefSeq 224"},
           "joined": len(rows), "copla2_records": len(cop),
           "ptus_with_multiple_replicon_types": multi,
           "ptus_compared": len(byptu), "subsets": {}}

    for name, sub in (("all", rows),
                      ("pcn_ge_1", [r for r in rows if r["pcn"] >= 1])):
        x = np.array([r["x"] for r in sub])
        y = np.array([r["y"] for r in sub])
        s1, b1, (s2, c, b2), f = ols_seg(x, y)
        d = aic(s2, len(x), 4) - aic(s1, len(x), 2)
        check_percent(10 ** c)
        print(f"\n{name}  n={len(sub):,}")
        print(f"  pooled  bend {10 ** c:.2f}% of chromosome, "
              f"slopes {b2[1]:+.3f}/{b2[1] + b2[2]:+.3f}, "
              f"change {b2[2]:+.3f}, dAIC {d:+.1f}")
        rec = {"n": len(sub), "bend_percent": float(10 ** c),
               "slope_below": float(b2[1]), "slope_above": float(b2[1] + b2[2]),
               "slope_change": float(b2[2]), "delta_aic": d, "absorbed": {}}
        for field, label in (("ptu", "PTU"), ("rep", "replicon type"),
                             ("genus", "genus")):
            r_ = absorb(x, y, np.array([s[field] for s in sub]), c, f)
            rec["absorbed"][field] = r_
            if r_:
                print(f"    {label:<16} groups {r_['groups']:>4}  "
                      f"straddling {r_['straddling']:>4}  "
                      f"change {r_['slope_change']:+.3f}  "
                      f"dAIC {r_['delta_aic']:+9.1f}")
        out["subsets"][name] = rec

    (HERE / "copla_receipt.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"\nwrote {HERE / 'copla_receipt.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
