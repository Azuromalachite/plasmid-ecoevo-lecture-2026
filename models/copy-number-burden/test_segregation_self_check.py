#!/usr/bin/env python3
"""Mutation test: break `segregation.py`, confirm its self-check notices.

`segregation.self_check()` prints "all groups passed" and exits 0. That is
worth nothing on its own -- a function that always passes also prints that.
This asserts the other half: each of the mutations below, applied one at a
time, must make it exit non-zero.

WHY THIS FILE EXISTS. Three commit messages on `main` claim mutation results
("fourteen deliberate breakages, fourteen caught"; "20/20 mutants caught").
Those were true when written and the repository could not support them,
which is the defect class OF-1 recorded: a validation reported as passing
without evidence it discriminates. The harness ran in a scratch directory
and was discarded. This is it, kept.

ISOLATION. Every mutant is written to a fresh temporary directory and run
there, never in the working tree. OF-16 is a mutation test in this
repository that wrote into real history from a linked worktree; the cheapest
way not to repeat it is never to mutate a tracked file. `segregation.py`
imports only `math`, so a copy runs correctly anywhere.

THE PROBE NEEDS A PROBE. The unmutated copy is run first and must pass. If
it does not, every mutant would "fail" for the wrong reason and a report of
20/20 would be meaningless. A baseline failure is reported as such and is
itself a failure of this test.

Usage:
    python models/copy-number-burden/test_segregation_self_check.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TARGET = Path(__file__).resolve().parent / "battle_royale" / "segregation.py"

#: (label, exact source text, replacement). Each must match exactly once;
#: a pattern that stops matching after a refactor is reported as SKIP rather
#: than silently passing, because an unapplied mutation proves nothing.
MUTANTS: list[tuple[str, str, str]] = [
    # --- daughter_distribution ---
    ("dist: replication dropped (n = c, not 2c)",
     "n = 2 * int(copies)", "n = int(copies)"),
    ("dist: normalisation off by a factor of 2",
     "math.comb(n, k) * 0.5 ** n", "math.comb(n, k) * 0.5 ** (n - 1)"),
    ("dist: last outcome omitted",
     "for k in range(n + 1)", "for k in range(n)"),
    ("dist: binomial coefficient dropped (flat)",
     "math.comb(n, k) * 0.5 ** n", "0.5 ** n"),
    ("dist: input validation removed",
     'raise ValueError("copies must be a positive whole number")', "pass"),
    ("dist: asymmetric, k counted from the wrong end",
     "math.comb(n, k) * 0.5 ** n",
     "math.comb(n, k) * 0.5 ** n * (1 + 0.1 * k)"),
    # --- copy_number_pmf / population_loss_rate ---
    ("pop: tail truncated too early",
     "math.exp(6.0 * sigma)", "math.exp(1.5 * sigma)"),
    ("pop: per-division instead of per-daughter",
     "p * 2.0 ** (-2 * k)", "p * 2.0 ** (1 - 2 * k)"),
    ("pop: carrier conditioning dropped",
     "return weighted / carriers", "return weighted"),
    ("pop: lognormal median correction dropped",
     "mu = math.log(mean_copies) - 0.5 * sigma2",
     "mu = math.log(mean_copies)"),
    ("pop: convexity destroyed (loss evaluated at the mean)",
     "p * 2.0 ** (-2 * k)", "p * 2.0 ** (-2 * mean_copies)"),
    ("pop: zero-copy cells counted as carriers",
     'carriers = math.fsum(pmf[1:])\n    if carriers <= 0.0:\n'
     '        raise ValueError("distribution puts no mass on carriers")\n'
     '    weighted',
     'carriers = math.fsum(pmf)\n    if carriers <= 0.0:\n'
     '        raise ValueError("distribution puts no mass on carriers")\n'
     '    weighted'),
    ("pop: cv=0 shortcut puts mass at the wrong copy number",
     "pmf[k] = 1.0", "pmf[k - 1] = 1.0"),
    ("pop: input validation removed",
     'raise ValueError("mean_copies must be positive")', "pass"),
    # --- carrier_mean / loss_rate_from_division_counts ---
    ("carrier_mean: conditioning dropped",
     "    return math.fsum(k * p for k, p in enumerate(pmf) if k >= 1)"
     " / carriers",
     "    return math.fsum(k * p for k, p in enumerate(pmf))"),
    ("carrier_mean: off by one copy",
     "return math.fsum(k * p for k, p in enumerate(pmf) if k >= 1) / carriers",
     "return math.fsum((k + 1) * p for k, p in enumerate(pmf) if k >= 1)"
     " / carriers"),
    ("arbitrary: per-division instead of per-daughter",
     "return math.fsum(p * 2.0 ** (-n) for n, p in items if n >= 1) / carriers",
     "return math.fsum(p * 2.0 ** (1 - n) for n, p in items if n >= 1)"
     " / carriers"),
    ("arbitrary: carrier conditioning dropped",
     "return math.fsum(p * 2.0 ** (-n) for n, p in items if n >= 1) / carriers",
     "return math.fsum(p * 2.0 ** (-n) for n, p in items if n >= 1)"),
    ("arbitrary: normalisation check removed",
     '        raise ValueError(f"probabilities must sum to 1; got {total}")',
     "        pass"),
    ("arbitrary: treats counts as birth copies, not division copies",
     "return math.fsum(p * 2.0 ** (-n) for n, p in items if n >= 1) / carriers",
     "return math.fsum(p * 2.0 ** (-2 * n) for n, p in items if n >= 1)"
     " / carriers"),
]


def run(source: str, workdir: Path) -> tuple[int, str]:
    """Run a copy of the module in an isolated directory."""
    f = workdir / "segregation_under_test.py"
    f.write_text(source, encoding="utf-8", newline="\n")
    p = subprocess.run([sys.executable, str(f)],
                       capture_output=True, text=True, cwd=workdir)
    first = next((l.strip() for l in p.stdout.splitlines() if "FAIL" in l), "")
    return p.returncode, first


def main() -> int:
    good = TARGET.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="segregation-mutants-") as tmp:
        work = Path(tmp)

        rc, _ = run(good, work)
        if rc != 0:
            print("  BASELINE FAILED: the unmutated module does not pass its "
                  "own self-check.\n  Every mutant below would 'fail' for "
                  "that reason instead of the intended one,\n  so no mutation "
                  "result from this run means anything.", file=sys.stderr)
            return 1
        print("  baseline: unmutated module passes (so a failure below is "
              "attributable to the mutation)\n")

        rows = []
        for label, old, new in MUTANTS:
            hits = good.count(old)
            if hits != 1:
                rows.append((label, "SKIP", f"pattern matched {hits}x"))
                continue
            rc, first = run(good.replace(old, new, 1), work)
            rows.append((label, "caught" if rc != 0 else "SURVIVED",
                         first[:70]))

    width = max(len(r[0]) for r in rows)
    bad = 0
    for label, verdict, detail in rows:
        if verdict != "caught":
            bad += 1
        print(f"  {verdict:9s} {label:{width}s}  {detail}")

    print(f"\n  {len(rows) - bad}/{len(rows)} mutants caught")
    if bad:
        print("  A SURVIVED mutant is a hole in self_check; a SKIP is a "
              "pattern that no\n  longer matches the source and proves "
              "nothing either way. Both are failures.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
