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

## Conventions for new figures

1. One script per figure, standard library only where possible, deterministic
   output.
2. The figure states on its face whether it is **illustrative** or
   **calibrated**. A calibrated figure additionally names its data source,
   parameters and regime, either in the figure or in this file.
3. Source keys in the figure footer are BibTeX keys from
   [`../evidence/references.bib`](../evidence/references.bib).
4. SVG for diagrams. Raster output only when a figure genuinely needs it.
