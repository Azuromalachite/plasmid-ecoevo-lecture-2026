#!/usr/bin/env python3
"""Mutation test: prove `check_references.py` can go red, and for what.

A checker that has only ever reported clean is not known to work. It is known
to be quiet, and quiet is what a checker with a blind spot also looks like --
which is the whole of OF-2. This script copies the repository to a temporary
directory, breaks one thing at a time, and asserts that the checker notices.

Each case below names **the defect it is capable of catching**. That is the
property `models/copy-number-burden/README.md` calls for and defers: "every
important validation should state the defect it is capable of catching, and
ideally carry a deliberately constructed mutation that makes it fail."

The first case is the control: an unmutated copy must report clean. Without it
a bug that made the checker fail on everything would look like a perfect score.

The second case is OF-2's own defect, reproduced deliberately: `.ipynb` is
removed from the checker's domain, and the four keys cited only in the notebook
turn into orphans. That is exactly what the scratch tool did during the v0.2
cycle. It is here so the repository holds a reproduction of the failure it is
protecting against, rather than only a description of it.

Usage (from the repository root):
    uv run --no-project --with pyyaml python evidence/test_check_references.py

Exit status is 1 if any mutation goes unnoticed.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER = "evidence/check_references.py"


def cite(*keys):
    """Build a citation without writing one.

    This file would otherwise be a corpus of real-looking citations, and the
    checker reads every `.md`, `.yml`, `.py` and `.ipynb` in the tree --
    including this one, by design. Assembling the brackets at run time keeps
    the test out of the corpus without giving the checker a blind spot to
    arrange that. Excluding a file is how a check stops seeing things.
    """
    return "[" + "; ".join("@" + key for key in keys) + "]"


def replace_once(path, old, new):
    """Replace, and fail loudly if the target was not there.

    A mutation that silently fails to apply is a test case that reports on
    nothing. That is the same defect the checker exists to prevent, one level
    up, so it raises rather than returning quietly.
    """
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"mutation target not found in {path.name}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# ---------------------------------------------------------------------------
# Mutations. Each takes the temporary copy's root and breaks exactly one thing.
# ---------------------------------------------------------------------------

def mutate_nothing(root):
    """Control: an untouched copy must be clean."""


def mutate_drop_ipynb_from_domain(root):
    """OF-2's own defect: narrow the domain and watch real citations go orphan."""
    replace_once(root / CHECKER,
                 'READ_SUFFIXES = {".md", ".yml", ".py", ".ipynb"}',
                 'READ_SUFFIXES = {".md", ".yml", ".py"}')


def mutate_typo_in_prose(root):
    """A misspelt key in a bracketed citation on a content page."""
    replace_once(root / "concepts" / "copy-carry-spread.md",
                 cite("sanmillan2017costs"), cite("sanmillan2017cost"))


def mutate_typo_in_grouped_citation(root):
    """A misspelt key in the SECOND position of a grouped citation.

    Worth its own case: a reader of the regex can convince themselves the first
    key is checked without noticing whether the rest are.
    """
    replace_once(root / "concepts" / "plasmid-vs-host-fitness.md",
                 cite("sanmillan2017costs", "harrison2012coevolutionary"),
                 cite("sanmillan2017costs", "harrison2012coevolution"))


def mutate_typo_in_registry(root):
    """A misspelt key in a claims.yml `references:` list."""
    replace_once(root / "evidence" / "claims.yml",
                 "      - yin2014recycling", "      - yin2014recyling")


def mutate_typo_in_figure_footer(root):
    """A misspelt key in a figure's SOURCE_KEYS -- a dead reference in an SVG."""
    replace_once(root / "figures" / "source" / "shewanella_oxa48_pathway.py",
                 '"carattoli2015incl",', '"carattoli2015inc",')


def mutate_typo_in_notebook(root):
    """A misspelt key cited only in the notebook."""
    path = root / "models" / "copy-number-burden" / "battle-royale.ipynb"
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        source = cell.get("source", [])
        for i, line in enumerate(source):
            if "@jahn2016copynumber" in line:
                source[i] = line.replace("@jahn2016copynumber", "@jahn2016copynum")
                path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1),
                                encoding="utf-8")
                return
    raise RuntimeError("mutation target not found in the notebook")


def mutate_orphan_entry(root):
    """A bibliography entry nothing cites."""
    path = root / "evidence" / "references.bib"
    path.write_text(
        path.read_text(encoding="utf-8")
        + "\n@article{nobody2020uncited,\n  author = {Nobody},\n"
          "  title = {Uncited},\n  journal = {J},\n  year = {2020},\n"
          "  doi = {10.1234/uncited}\n}\n",
        encoding="utf-8")


def mutate_duplicate_entry(root):
    """The same key defined twice."""
    path = root / "evidence" / "references.bib"
    text = path.read_text(encoding="utf-8")
    entry = re.search(r"@article\{bergstrom2000natural.*?\n\}\n", text, re.S)
    path.write_text(text + "\n" + entry.group(0), encoding="utf-8")


def mutate_missing_doi(root):
    """An entry with no doi field."""
    path = root / "evidence" / "references.bib"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("  doi = {10.1093/genetics/155.4.1505}\n", "", 1),
                    encoding="utf-8")


def mutate_malformed_doi(root):
    """A doi field holding something that is not a DOI."""
    path = root / "evidence" / "references.bib"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("doi = {10.1093/genetics/155.4.1505}",
                     "doi = {https://doi.org/10.1093/genetics/155.4.1505}", 1),
        encoding="utf-8")


def mutate_unruled_file_type(root):
    """A file type nobody has ruled on appears in the tree."""
    (root / "concepts" / "draft.tex").write_text(
        "A citation the checker cannot see: \\cite{sanmillan2017costs}\n",
        encoding="utf-8")


CASES = [
    (mutate_nothing, None,
     "an unmutated copy reports clean"),
    # jambor2025checklist is one of the three keys cited ONLY in the notebook.
    # Three, not four: a grep that reads `[@a; @b]` as one citation undercounts
    # the rest of the group, and that is how an earlier audit of this very
    # question got the number wrong. See the OF-7 correction note.
    (mutate_drop_ipynb_from_domain,
     "in references.bib but cited nowhere: jambor2025checklist",
     "OF-2's defect: a narrowed domain turns notebook-only citations into orphans"),
    (mutate_typo_in_prose, "cited but not in references.bib: sanmillan2017cost",
     "a misspelt key in prose"),
    (mutate_typo_in_grouped_citation, "cited but not in references.bib: harrison2012coevolution",
     "a misspelt key in the second position of a [@a; @b] group"),
    (mutate_typo_in_registry, "cited but not in references.bib: yin2014recyling",
     "a misspelt key in a claims.yml references: list"),
    (mutate_typo_in_figure_footer, "cited but not in references.bib: carattoli2015inc",
     "a misspelt key in a figure footer"),
    (mutate_typo_in_notebook, "cited but not in references.bib: jahn2016copynum",
     "a misspelt key cited only in the notebook"),
    (mutate_orphan_entry, "in references.bib but cited nowhere: nobody2020uncited",
     "a bibliography entry nothing cites"),
    (mutate_duplicate_entry, "duplicate entry in references.bib: bergstrom2000natural",
     "the same key defined twice"),
    (mutate_missing_doi, "no doi field: bergstrom2000natural",
     "an entry with no doi field"),
    (mutate_malformed_doi, "doi is not shaped like a DOI",
     "a doi field holding a URL instead of a DOI"),
    (mutate_unruled_file_type, "unruled file type '.tex'",
     "a file type nobody has ruled on"),
]


def run_case(mutate, expect):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "repo"
        shutil.copytree(ROOT, root,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))
        mutate(root)
        result = subprocess.run(
            [sys.executable, str(root / CHECKER)],
            capture_output=True, text=True, cwd=root)
        output = result.stdout + result.stderr

    if expect is None:
        ok = result.returncode == 0 and "no problems" in output
        detail = "" if ok else f"exit {result.returncode}"
    else:
        ok = result.returncode == 1 and expect in output
        if result.returncode != 1:
            detail = f"exit {result.returncode}, expected 1"
        elif expect not in output:
            detail = f"did not report {expect!r}"
        else:
            detail = ""
    return ok, detail


def main():
    print(f"Mutation test for {CHECKER}")
    print(f"{len(CASES)} cases, one mutation each, on a temporary copy\n")
    failures = 0
    for mutate, expect, description in CASES:
        ok, detail = run_case(mutate, expect)
        mark = "caught " if expect else "clean  "
        if not ok:
            mark = "MISSED "
            failures += 1
        print(f"  {mark} {description}" + (f"  [{detail}]" if detail else ""))

    print()
    if failures:
        print(f"{failures} of {len(CASES)} mutations went unnoticed. The checker's "
              f"domain is narrower than it claims.")
        return 1
    print(f"all {len(CASES)} cases behaved as specified: the checker reports clean "
          f"on a clean tree\nand red on each defect above. That is its measured "
          f"domain of sensitivity, not\nan argument that it has no blind spots -- "
          f"only that these are not among them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
