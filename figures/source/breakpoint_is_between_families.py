#!/usr/bin/env python3
"""The segmented preference survives pooling and does not survive families.

Writes figures/output/breakpoint-is-between-families.svg.

WHAT THIS FIGURE IS FOR. `reproductions/ramiro-scaling/RESULTS.md` reports a
segmented fit preferred over a single power law by dAIC -148.1, with the
breakpoint at 1.73% of chromosome length -- close to the 1.84% Maddamsetti et
al. publish from a different sample. Section 5 of that file shows the
preference is a property of how plasmid FAMILIES are distributed in size, not
a threshold individual plasmids cross: centring on predicted PTU takes dAIC to
-1.3.

A null is unreadable on its own. The reader cannot tell "no break" from "a
test that had stopped working", and centring removes 95.3% of the spread in
the predictor, which is exactly the circumstance where a test does stop
working. So the figure's job is not to show -1.3. It is to show -1.3 NEXT TO
three breaks of the pooled magnitude that were planted into the centred data
and recovered by the identical test. Those three bars are the figure.

WHAT THIS FIGURE MUST NOT IMPLY:
  * that the pooled segmented fit was wrong. It is in the data and it is
    where Maddamsetti says it is;
  * that the three planted bars are observations. They are synthetic, which
    is why their row labels say so ON the graphic rather than in a caption
    the screenshot leaves behind;
  * that copy number was counted. It is a coverage ratio the source ships
    without any uncertainty at all, stated in the figure's own footer.

NUMBERS COME FROM THE RECEIPT, NOT FROM HERE. Every value drawn is read out
of reproductions/ramiro-scaling/receipt.json at build time. A figure holding
its own copy of a number is how a figure comes to disagree with the analysis
that produced it; figures/source/palette.py carries the same rule for its own
measurements and says why.

COLOUR. The repository palette is Okabe-Ito with roles assigned in
palette.py, and this figure needs a categorical triple that neither existing
vocabulary (ROUTES, STAGES) supplies. The triple below was chosen by running
palette.py's own separability measure over POOL and taking a passing
combination; the assertion in build() re-runs that measure, so a future edit
that breaks it fails the build rather than shipping. sky_blue is also COPY in
ROUTES and `environmental` in STAGES: within POOL that reuse is forced, it is
the same compromise STAGES documents, and no figure mixes the vocabularies,
so nothing here asks a reader to hold two meanings at once.

Rule 2 of palette.py -- colour never carries meaning alone -- is met by the
row labels, which name every series in words, and by bar length, which is the
quantity itself.

Run:
    python figures/source/breakpoint_is_between_families.py
"""

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = REPO / "figures" / "output" / "breakpoint-is-between-families.svg"
RECEIPT = REPO / "reproductions" / "ramiro-scaling" / "receipt.json"

_spec = importlib.util.spec_from_file_location("_palette", HERE / "palette.py")
pal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pal)

#: Series roles for this figure. Verified against palette.py's own measure in
#: build(); see the module docstring for why these three.
POOLED = "sky_blue"
PLANTED = "bluish_green"
CENTRED = "vermillion"

W, H = 760, 348
X0, X1 = 250, 720          # plot area
TOP = 60
ROW_H, BAR_H = 38, 20


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def load():
    d = json.loads(RECEIPT.read_text(encoding="utf-8"))
    seg, mix = d["segmented"], d["break_or_mixture"]
    rows = [("Pooled, as published", mix["pooled_delta_aic"], POOLED, True)]
    for p in mix["power_check"]:
        pct = int(round(p["quantile"] * 100))
        rows.append((f"Planted break, {pct}th pct", p["delta_aic"], PLANTED,
                     False))
    rows.append(("Family-centred, observed", mix["family_centred_delta_aic"],
                 CENTRED, True))
    return d, seg, mix, rows


def build():
    worst = pal._worst((POOLED, PLANTED, CENTRED))
    if worst < pal.MIN_DISTANCE:
        sys.exit(f"palette: {POOLED}/{PLANTED}/{CENTRED} separate by only "
                 f"{worst:.1f}, below MIN_DISTANCE {pal.MIN_DISTANCE}")

    d, seg, mix, rows = load()
    if not d["source"]["matches_expected"]:
        sys.exit("receipt records a run against an unexpected input; "
                 "re-run reproduce.py before building this figure")

    span = max(abs(v) for _, v, _, _ in rows)
    top = 40 * (int(span // 40) + 1)          # round the axis up to a tick
    def x(v):
        return X0 + abs(v) / top * (X1 - X0)

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif" '
         f'role="img" aria-labelledby="t d">',
         f'<title id="t">The segmented preference is between families, not '
         f'within them</title>',
         f'<desc id="d">Pooled, the two-segment fit beats a single line by '
         f'dAIC {mix["pooled_delta_aic"]:.1f}. Centred on plasmid family it '
         f'beats it by only {mix["family_centred_delta_aic"]:.1f}. Three '
         f'breaks of the pooled magnitude planted into the centred data were '
         f'recovered by the same test at around dAIC -45, so the near-zero '
         f'observed value is an absence rather than a test without '
         f'power.</desc>',
         f'<rect width="{W}" height="{H}" fill="{pal.PAPER}"/>']

    s.append(f'<text x="24" y="30" font-size="15" font-weight="bold" '
             f'fill="{pal.INK}">Removing the family means removes the bend</text>')
    s.append(f'<text x="24" y="48" font-size="12" fill="{pal.MUTED}">'
             f'&#916;AIC, two segments minus one line. More negative is '
             f'stronger evidence for a bend.</text>')

    # gridlines, zero emphasised
    for t in range(0, top + 1, 40):
        gx = X0 + t / top * (X1 - X0)
        s.append(f'<line x1="{gx:.1f}" y1="{TOP - 10}" x2="{gx:.1f}" '
                 f'y2="{TOP + len(rows) * ROW_H - 4}" stroke="{pal.RULE}" '
                 f'stroke-width="1"/>')
        s.append(f'<text x="{gx:.1f}" y="{TOP + len(rows) * ROW_H + 14}" '
                 f'font-size="11" fill="{pal.MUTED}" text-anchor="middle">'
                 f'{"0" if t == 0 else "&#8722;" + str(t)}</text>')
    s.append(f'<line x1="{X0}" y1="{TOP - 10}" x2="{X0}" '
             f'y2="{TOP + len(rows) * ROW_H - 4}" stroke="{pal.MUTED}" '
             f'stroke-width="2"/>')

    for i, (label, val, role, strong) in enumerate(rows):
        cy = TOP + i * ROW_H
        w = x(val) - X0
        s.append(f'<text x="{X0 - 12}" y="{cy + 14}" font-size="12" '
                 f'text-anchor="end" fill="{pal.INK}"'
                 f'{" font-weight=\"bold\"" if strong else ""}>'
                 f'{esc(label)}</text>')
        s.append(f'<rect x="{X0}" y="{cy}" width="{max(w, 2):.1f}" '
                 f'height="{BAR_H}" rx="3" fill="{pal.OKABE_ITO[role]}"/>')
        # value label: inside the bar when it fits, otherwise just past its end
        txt = f'&#8722;{abs(val):.1f}'
        if w > 60:
            s.append(f'<text x="{X0 + w - 8:.1f}" y="{cy + 14}" font-size="12" '
                     f'text-anchor="end" fill="#ffffff" font-weight="bold">'
                     f'{txt}</text>')
        else:
            s.append(f'<text x="{X0 + w + 8:.1f}" y="{cy + 14}" font-size="12" '
                     f'fill="{pal.INK}" font-weight="bold">{txt}</text>')

    base = TOP + len(rows) * ROW_H - 4
    s.append(f'<line x1="{X0}" y1="{base}" x2="{X1}" y2="{base}" '
             f'stroke="{pal.MUTED}" stroke-width="1"/>')

    # Three short lines rather than two long ones: at 11px the single-line
    # version ran past the 760px canvas, which no check here would have
    # caught -- SVG text does not wrap and does not report overflow.
    within = mix["log_size_variance_within_family_percent"]
    foot = [
        f'Pooled breakpoint {seg["breakpoint_percent_of_chromosome"]:.2f}% of '
        f'chromosome length. Variance in log relative size: {within:.1f}% '
        f'within families, {100 - within:.1f}% between.',
        'Copy number is estimated from sequencing coverage, not counted; the '
        'source publishes no uncertainty for it.',
        'Planted breaks are synthetic controls, not observations.',
    ]
    for k, line in enumerate(foot):
        s.append(f'<text x="24" y="{H - 52 + k * 16}" font-size="11" '
                 f'fill="{pal.MUTED}">{esc(line)}</text>')
    s.append('</svg>')

    OUT.write_text("\n".join(s) + "\n", encoding="utf-8", newline="\n")
    print(f"  palette: {POOLED}/{PLANTED}/{CENTRED} separate by "
          f"{worst:.1f} (>= {pal.MIN_DISTANCE})")
    print(f"  drawn from receipt sha256 {d['source']['sha256'][:12]}")
    for label, val, _, _ in rows:
        print(f"    {label:<26} {val:+8.1f}")
    print(f"  wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
