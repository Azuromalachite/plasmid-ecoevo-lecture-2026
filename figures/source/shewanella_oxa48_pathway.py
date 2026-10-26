#!/usr/bin/env python3
"""Conceptual figure: Shewanella chromosome -> Tn1999 -> IncL plasmid -> clinic.

Writes figures/output/shewanella-oxa48-pathway.svg.

This is an ILLUSTRATIVE diagram, not a scale drawing and not calibrated data.
It encodes no coordinates, lengths or frequencies from any dataset; positions
are chosen for legibility. Gene order in the Shewanella panel follows the
arrangement reported by Zong (2012); the plasmid is drawn as a circle of
arbitrary radius with no implied scale against the chromosome.

Standard library only: no matplotlib, no network access. Deterministic output,
so a rebuild produces a byte-identical file.

Usage (from the repository root):
    python figures/source/shewanella_oxa48_pathway.py
"""

from pathlib import Path

W, H = 1120, 620

# Colours chosen to stay legible on white and in greyscale print; the
# ancestral/environmental side is cool, the clinical side warm.
INK = "#1b1f23"
MUTED = "#5a6570"
ENV = "#2b6f8a"
ENV_FILL = "#dceaf1"
MOB = "#8a5a2b"
MOB_FILL = "#f2e4d2"
CLIN = "#96342f"
CLIN_FILL = "#f6dedc"
OPEN = "#6b6b6b"

FONT = "font-family=\"Helvetica,Arial,sans-serif\""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=13, fill=INK, anchor="start", weight="normal",
         style="normal"):
    return (f'<text x="{x}" y="{y}" {FONT} font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}">{esc(s)}</text>')


def box(x, y, w, h, stroke, fill, rx=6, dash=None, width=1.6):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"{d}/>')


def gene_arrow(x, y, w, h, fill, stroke, label, label_size=11, italic=False):
    """A block arrow pointing right, with a centred label."""
    tip = min(14, w * 0.3)
    pts = (f"{x},{y} {x + w - tip},{y} {x + w},{y + h / 2} "
           f"{x + w - tip},{y + h} {x},{y + h}")
    style = "italic" if italic else "normal"
    return (f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="1.4"/>'
            + text(x + (w - tip) / 2, y + h / 2 + 4, label, label_size, INK,
                   "middle", "normal", style))


def arrow(x1, y1, x2, y2, colour=INK, width=2.0, head=9, dashed=False):
    """Straight arrow with a filled triangular head (horizontal or vertical).

    dashed=True marks an arrow that orders CONTEXTS rather than asserting a
    reconstructed descent, so the visual grammar matches the caveat in the
    footer and in the case study's misreading table.
    """
    parts = []
    dash = ' stroke-dasharray="7 4"' if dashed else ""
    if y1 == y2:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2 - head}" y2="{y2}" '
                     f'stroke="{colour}" stroke-width="{width}"{dash}/>')
        parts.append(f'<polygon points="{x2},{y2} {x2 - head},{y2 - head * 0.6} '
                     f'{x2 - head},{y2 + head * 0.6}" fill="{colour}"/>')
    else:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2 - head}" '
                     f'stroke="{colour}" stroke-width="{width}"{dash}/>')
        parts.append(f'<polygon points="{x2},{y2} {x2 - head * 0.6},{y2 - head} '
                     f'{x2 + head * 0.6},{y2 - head}" fill="{colour}"/>')
    return "".join(parts)


def build():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>']

    o.append(text(40, 44, "From an environmental chromosome to a clinical plasmid",
                  21, INK, "start", "bold"))
    o.append(text(40, 68, "blaOXA-48-like genes: one enzyme family in three "
                          "genetic contexts", 14, MUTED))

    # ---------------------------------------------------------------- panel 1
    o.append(box(40, 96, 310, 196, ENV, ENV_FILL))
    o.append(text(58, 122, "1 · ENVIRONMENTAL CHROMOSOME", 12, ENV, "start", "bold"))
    o.append(text(58, 142, "Shewanella spp., water and sediment", 12, MUTED,
                 "start", "normal", "italic"))

    # chromosome line with neighbouring housekeeping genes
    o.append(f'<line x1="58" y1="186" x2="332" y2="186" stroke="{ENV}" '
             f'stroke-width="3"/>')
    o.append(gene_arrow(58, 170, 54, 32, "#ffffff", ENV, "endA", 10, True))
    o.append(gene_arrow(118, 170, 54, 32, "#ffffff", ENV, "rsmE", 10, True))
    o.append(gene_arrow(178, 170, 72, 32, "#cfe3ec", ENV, "blaOXA", 10, True))
    o.append(gene_arrow(256, 170, 54, 32, "#ffffff", ENV, "lysR", 10, True))

    o.append(text(58, 228, "Chromosomal; inherited with the host lineage.", 12, INK))
    o.append(text(58, 246, "Expression wired into envelope physiology", 12, INK))
    o.append(text(58, 262, "(peptidoglycan recycling, PBP1a/LpoA).", 12, INK))
    o.append(text(58, 282, "Ancestral selective agent: unresolved.", 12, CLIN,
                 "start", "bold"))

    # ---------------------------------------------------------------- panel 2
    o.append(box(405, 96, 310, 196, MOB, MOB_FILL))
    o.append(text(423, 122, "2 · MOBILIZED ON Tn1999", 12, MOB, "start", "bold"))
    o.append(text(423, 142, "Composite transposon, two IS1999 copies", 12, MUTED,
                 "start", "normal", "italic"))

    o.append(box(423, 164, 274, 44, MOB, "#ffffff", 4))
    o.append(gene_arrow(431, 170, 70, 32, "#e6cfae", MOB, "IS1999", 10, False))
    o.append(gene_arrow(507, 170, 106, 32, "#cfe3ec", ENV, "blaOXA-48", 10, True))
    o.append(gene_arrow(619, 170, 70, 32, "#e6cfae", MOB, "IS1999", 10, False))

    o.append(text(423, 232, "IS1999 supplies the outward promoter Pout:", 12, INK))
    o.append(text(423, 248, "the gene is now read from the element's own", 12, INK))
    o.append(text(423, 264, "promoter, not its native one.", 12, INK))
    o.append(text(423, 284, "Location and expression context change together.", 12, MOB,
                 "start", "bold"))

    # ---------------------------------------------------------------- panel 3
    o.append(box(770, 96, 310, 196, CLIN, CLIN_FILL))
    o.append(text(788, 122, "3 · IncL PLASMID pOXA-48", 12, CLIN, "start", "bold"))
    o.append(text(788, 142, "~62 kb, self-transferable", 12, MUTED, "start",
                 "normal", "italic"))

    cx, cy, r = 862, 222, 56
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" '
             f'stroke="{CLIN}" stroke-width="3"/>')
    # Tn1999 drawn as an arc segment inserted into the backbone
    o.append(f'<path d="M {cx - 40} {cy - 39} A {r} {r} 0 0 1 {cx + 40} {cy - 39}" '
             f'fill="none" stroke="{MOB}" stroke-width="9" stroke-linecap="round"/>')
    o.append(text(cx, cy - 64, "Tn1999", 10, MOB, "middle", "bold"))
    o.append(text(cx, cy + 6, "pOXA-48", 12, INK, "middle", "bold"))
    o.append(text(cx, cy + 24, "IncL", 11, MUTED, "middle"))
    # the tir insertion marker
    o.append(f'<circle cx="{cx + 40}" cy="{cy - 39}" r="5" fill="{CLIN}"/>')
    o.append(text(cx + 54, cy - 40, "into tir", 11, CLIN, "start", "normal",
                 "italic"))

    o.append(text(962, 224, "No other", 11, INK))
    o.append(text(962, 240, "resistance gene", 11, INK))
    o.append(text(962, 256, "on the backbone.", 11, INK))
    o.append(text(788, 284, "tir insertion raises transfer frequency.", 12, CLIN,
                 "start", "bold"))

    # ------------------------------------------------------- arrows 1 -> 2 -> 3
    o.append(arrow(352, 194, 403, 194, MOB, dashed=True))
    o.append(text(377, 180, "mobilization", 11, MOB, "middle"))
    o.append(arrow(717, 194, 768, 194, CLIN, dashed=True))
    o.append(text(742, 180, "transposition", 11, CLIN, "middle"))

    # ---------------------------------------------------------------- panel 4
    o.append(arrow(925, 296, 925, 348, CLIN))
    o.append(box(40, 352, 1040, 118, CLIN, "#ffffff", 6))
    o.append(text(58, 378, "4 · NEW HOST, NEW PHENOTYPE, NEW EPIDEMIOLOGY",
                 12, CLIN, "start", "bold"))

    o.append(text(58, 404, "Enterobacteria (e.g. Klebsiella pneumoniae)", 12, INK,
                 "start", "bold"))
    o.append(text(58, 424, "High-level carbapenem resistance needs the enzyme", 12,
                 INK))
    o.append(text(58, 440, "AND reduced outer-membrane permeability.", 12, INK))

    o.append(f'<line x1="408" y1="392" x2="408" y2="452" stroke="#d8d8d8" '
             f'stroke-width="1.5"/>')
    o.append(text(430, 404, "Two routes, simultaneously", 12, INK, "start", "bold"))
    o.append(text(430, 424, "between patients: plasmid-carrying clones", 12, INK))
    o.append(text(430, 440, "within patients: plasmid transfer in the gut", 12, INK))

    o.append(f'<line x1="760" y1="392" x2="760" y2="452" stroke="#d8d8d8" '
             f'stroke-width="1.5"/>')
    o.append(text(782, 404, "And it keeps evolving", 12, INK, "start", "bold"))
    o.append(text(782, 424, "cost compensated within patients;", 12, INK))
    o.append(text(782, 440, "resistance level rises, with a trade-off.", 12, INK))

    # ------------------------------------------------------------- the message
    o.append(text(40, 506, "Same enzyme family.  Different cell.  Different meaning.",
                 17, INK, "start", "bold"))

    # ------------------------------------------------------------------ footer
    o.append(f'<line x1="40" y1="528" x2="1080" y2="528" stroke="#e2e2e2" '
             f'stroke-width="1"/>')
    o.append(text(40, 550, "Illustrative diagram — not to scale, no calibrated "
                           "quantities. Dashed arrows order contexts, not a dated "
                           "lineage. Panel 1 shows a subset of the neighbourhood, "
                           "order after Zong (2012).",
                 11, MUTED))
    o.append(text(40, 568, "Sources: potron2011oxa181 · zong2012oxa199 · "
                           "yin2014recycling · yin2015pbp1a · poirel2004progenitor "
                           "· aubert2006is1999 · poirel2004emergence",
                 11, MUTED))
    o.append(text(40, 584, "poirel2012genetic · poirel2012phantom · "
                           "carattoli2015incl · potron2014derepressed · "
                           "leonsampedro2021pervasive · delafuente2022withinpatient",
                 11, MUTED))
    o.append(text(40, 604, "The ancestral selective agent for chromosomal "
                           "blaOXA-48-like genes is not established "
                           "(claim.shewanella.oxa_ancestral_selection).",
                 11, OPEN, "start", "normal", "italic"))

    o.append("</svg>")
    return "\n".join(o) + "\n"


def main():
    out = Path(__file__).resolve().parents[1] / "output" / "shewanella-oxa48-pathway.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    # newline="\n" explicitly: text-mode writes would otherwise translate to
    # CRLF on Windows, so the same script would emit different bytes on
    # different platforms and the output would no longer be reproducible.
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
