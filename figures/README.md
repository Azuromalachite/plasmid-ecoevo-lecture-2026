# Figures

Every figure here is generated from a script in [`source/`](source/). The
rendered output in [`output/`](output/) is committed so the repository can be
read without running anything, but **the script is the source of truth**: fix
the script, rebuild, commit both.

## Rebuilding

From the repository root:

```bash
python figures/source/shewanella_oxa48_pathway.py
```

The scripts use the Python standard library only — no matplotlib, no network
access — and write SVG directly. Output is deterministic: rebuilding without
editing the script produces a byte-identical file, so a diff in `output/`
always corresponds to a diff in `source/`.

On Windows, if a script ever prints non-ASCII to the console, set
`PYTHONUTF8=1` first.

## What makes the output byte-identical

Two things, and both are load-bearing:

1. **The scripts write `newline="\n"` explicitly.** Python's text mode would
   otherwise translate newlines to CRLF on Windows, so the same script would
   emit different bytes on different platforms.
2. **`.gitattributes` enforces LF** for text, SVG and Python files, so a
   checkout cannot reintroduce CRLF.

Without the first, git's own normalisation *hides* the problem: the working
tree still looks clean after a rebuild even though the bytes on disk changed.
Give any new figure script the same explicit newline.

## Verifying it yourself

The claim above is checkable from a clean machine, and does not depend on
trusting this file:

```bash
git clone https://github.com/Azuromalachite/plasmid-ecoevo-lecture-2026
cd plasmid-ecoevo-lecture-2026
md5sum figures/output/shewanella-oxa48-pathway.svg
python figures/source/shewanella_oxa48_pathway.py
md5sum figures/output/shewanella-oxa48-pathway.svg   # same digest
git status --porcelain                               # no output
```

Last checked at commit `e85bb22` on Windows: both digests
`01b91795f4084009ecebf59ce3237c95`, working tree clean.

## Figures

### `shewanella-oxa48-pathway.svg`

From an environmental *Shewanella* chromosome to a clinical IncL plasmid:
chromosomal context → Tn*1999* → pOXA-48 → new host and clinical spread.

- **Source:** [`source/shewanella_oxa48_pathway.py`](source/shewanella_oxa48_pathway.py)
- **Used by:** [`../case-studies/shewanella-oxa48.md`](../case-studies/shewanella-oxa48.md)
- **Status: illustrative, not calibrated.** No coordinate, length, copy number
  or frequency in the drawing comes from data. The plasmid circle has an
  arbitrary radius and no scale relationship to the chromosome line; the gene
  blocks are not to scale in either panel.
- **What *is* taken from sources:** the relative order of the genes *shown*
  flanking the chromosomal *bla*<sub>OXA-48</sub>-like gene in panel 1 follows
  Zong (2012); other reported neighbours (a peptidase ORF and *sprT*
  upstream, the acetyl-CoA carboxylase locus downstream) are omitted for
  legibility, so the panel is a subset of that neighbourhood rather than a
  complete map of it. The
  two-IS*1999* composite structure, the P<sub>out</sub> promoter, the IncL
  backbone and the Tn*1999* insertion into *tir* follow the references listed
  in the figure footer and cited in the case study.
- **What the figure deliberately marks as open:** the ancestral selective
  agent for the chromosomal gene (claim
  `claim.shewanella.oxa_ancestral_selection` in
  [`../evidence/claims.yml`](../evidence/claims.yml)).

## Colour

[`source/palette.py`](source/palette.py) holds the shared palette and its
accessibility self-test. Run it:

```bash
python figures/source/palette.py
```

Two rules:

1. Colours stay distinguishable under simulated deuteranopia and protanopia.
   The self-test enforces this and fails loudly.
2. **Colour never carries meaning alone.** Every distinction is also carried
   by a label, shape, line style or position. Rule 1 limits the damage when
   colour fails; rule 2 is what makes a figure survive greyscale printing and
   a reader who sees no colour at all.

The module records two measured constraints rather than hiding them: COPY and
SPREAD are both blues because that is the only assignment of Okabe-Ito colours
to those three roles that clears the threshold under *both* simulations, and
the route and stage vocabularies share a colour because six Okabe-Ito colours
cannot supply two fully separable triples. A figure needing both must call
`check_union()`, which fails by design.

### The v0.1 figure predates this

`shewanella-oxa48-pathway.svg` uses its original colours, in which the brown
and the red collapse under deuteranopia (RGB distance 14; 36 under
protanopia). It is **not** being reissued: colour is not load-bearing there,
since the panels are numbered, titled and ordered left to right, so the figure
reads correctly in greyscale and under any colour vision. New figures use the
palette module.

## Conventions for new figures

1. One script per figure, standard library only where possible, deterministic
   output.
2. The figure states on its face whether it is **illustrative** or
   **calibrated**. A calibrated figure additionally names its data source,
   parameters and regime, either in the figure or in this file.
3. Source keys in the figure footer are BibTeX keys from
   [`../evidence/references.bib`](../evidence/references.bib).
4. SVG for diagrams. Raster output only when a figure genuinely needs it.
