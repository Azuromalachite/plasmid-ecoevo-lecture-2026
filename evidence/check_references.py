#!/usr/bin/env python3
"""Check that every citation resolves to a bibliography entry, and back.

Closes OF-2. The requirement that finding set is the reason for the first
section below: a checker **must enumerate the file types it reads and fail
visibly on types it does not**. During the v0.2 cycle a scratch tool reported
three real citations as orphans because it never opened `.ipynb`, and a
committed checker with the same blind spot would have reported clean on a file
it never read. A silent domain is the defect; the bibliography was fine.

So this script is explicit about three things it could otherwise be vague on:

1. **Which files it opens.** `READ_SUFFIXES` is the domain. Every run prints
   it, with a count. `.ipynb` is in it.
2. **Which files it has decided carry no citations.** `UNCITED_SUFFIXES` is
   that decision, written down. A suffix in neither set is a **failure**, not
   a skip: a file type nobody has ruled on has appeared, and the right response
   is to rule on it rather than to walk past it.
3. **Which syntaxes it understands.** Citations in this repository are written
   three different ways, and a checker that knew only the obvious one would
   report the other two as orphans. Each extractor reports its own count, so an
   extractor that silently stops matching is visible as a zero rather than as
   an absence.

WHAT IT DOES NOT DO. It does not resolve DOIs and does not check metadata
against the publisher: both need the network, and a check that is sometimes
skipped because a machine is offline is a check whose domain moves without
anyone deciding. It verifies that a `doi` field is present and plausibly
shaped. "Every reference has a resolving DOI whose metadata has been checked",
as `README.md` and `CITATION.cff` put it, remains a human claim about work done
by hand, and this script does not convert it into an automated one.

Usage (from the repository root):
    uv run --no-project --with pyyaml python evidence/check_references.py

Exit status is 1 if anything is wrong, so this can gate a commit later.
"""

import ast
import collections
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("needs pyyaml:  uv run --no-project --with pyyaml "
             "python evidence/check_references.py")

SKIP_DIRS = {".git", "__pycache__"}

# (1) The domain. Everything here is opened and searched for citations.
READ_SUFFIXES = {".md", ".yml", ".py", ".ipynb"}

# (2) The decision, written down. These carry no citations by their nature:
# the bibliography itself, the citation file, licence and figure output.
UNCITED_SUFFIXES = {".bib", ".cff", ".svg", ".txt", ""}

# A BibTeX key in this repository: lowercase name, four-digit year, suffix.
KEY_SHAPE = r"[a-z][a-z-]*[0-9]{4}[a-z0-9]*"

# Citation syntaxes. See the module docstring, point 3.
PANDOC_GROUP = re.compile(r"\[@[^\]]*\]", re.S)   # [@a] and [@a; @b] across lines
KEY_IN_GROUP = re.compile(r"@(" + KEY_SHAPE + r")")
BIB_ENTRY = re.compile(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,", re.M)
BIB_DOI = re.compile(r"\bdoi\s*=\s*\{([^}]*)\}")
DOI_SHAPE = re.compile(r"^10\.\d{4,9}/\S+$")


def read_text(path):
    """Text of a file, with notebooks flattened to their cell sources."""
    raw = path.read_text(encoding="utf-8")
    if path.suffix != ".ipynb":
        return raw
    notebook = json.loads(raw)
    return "\n".join("".join(cell.get("source", []))
                     for cell in notebook.get("cells", []))


def walk(root):
    """Yield readable files; return the skip tally and any unruled suffixes."""
    skipped = collections.Counter()
    unruled = collections.Counter()
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or set(path.parts) & SKIP_DIRS:
            continue
        suffix = path.suffix
        if suffix in READ_SUFFIXES:
            files.append(path)
        elif suffix in UNCITED_SUFFIXES:
            skipped[suffix or "(no suffix)"] += 1
        else:
            unruled[suffix] += 1
    return files, skipped, unruled


# ---------------------------------------------------------------------------
# The bibliography
# ---------------------------------------------------------------------------

def parse_bibliography(path):
    text = path.read_text(encoding="utf-8")
    keys = [m.group(2) for m in BIB_ENTRY.finditer(text)]
    duplicates = [k for k, n in collections.Counter(keys).items() if n > 1]

    # Split on entry starts so each key is paired with its own body.
    starts = [m.start() for m in BIB_ENTRY.finditer(text)] + [len(text)]
    bodies = {keys[i]: text[starts[i]:starts[i + 1]] for i in range(len(keys))}

    dois = {}
    for key, body in bodies.items():
        m = BIB_DOI.search(body)
        dois[key] = m.group(1).strip() if m else None
    return set(keys), duplicates, dois


# ---------------------------------------------------------------------------
# The three citation syntaxes
# ---------------------------------------------------------------------------

def cites_pandoc(files, root):
    """`[@key]` and `[@a; @b]`, including groups that wrap across lines."""
    found = {}
    for path in files:
        text = read_text(path)
        for group in PANDOC_GROUP.findall(text):
            for key in KEY_IN_GROUP.findall(group):
                found.setdefault(key, set()).add(path.relative_to(root).as_posix())
    return found


def cites_registry(root):
    """`references:` lists in evidence/claims.yml, which are bare keys."""
    path = root / "evidence" / "claims.yml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    found = {}
    for claim in data["claims"]:
        for key in claim.get("references") or []:
            found.setdefault(key, set()).add(
                f"claims.yml:{claim['id']}")
    return found


def cites_figure_footers(root):
    """`SOURCE_KEYS` in a figure script.

    Figure footers print their sources, and `figures/README.md` states those
    are BibTeX keys. That was an assertion nothing checked: a typo in a footer
    shipped a dead reference inside an SVG. The scripts now declare the keys in
    a module-level `SOURCE_KEYS` list and build the footer text from it, so the
    printed footer and the checked list cannot disagree.
    """
    found = {}
    for path in sorted((root / "figures" / "source").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            targets = getattr(node, "targets", [])
            if not (isinstance(node, ast.Assign) and len(targets) == 1):
                continue
            if getattr(targets[0], "id", None) != "SOURCE_KEYS":
                continue
            for element in node.value.elts:
                found.setdefault(element.value, set()).add(
                    path.relative_to(root).as_posix())
    return found


def merge(*sources):
    merged = {}
    for source in sources:
        for key, where in source.items():
            merged.setdefault(key, set()).update(where)
    return merged


def main():
    root = Path(__file__).resolve().parent.parent
    defined, duplicates, dois = parse_bibliography(root / "evidence" / "references.bib")
    files, skipped, unruled = walk(root)

    extractors = {
        "pandoc  [@key] / [@a; @b]": cites_pandoc(files, root),
        "registry  references:": cites_registry(root),
        "figure footer  SOURCE_KEYS": cites_figure_footers(root),
    }
    cited = merge(*extractors.values())

    problems = []

    for key in sorted(k for k in cited if k not in defined):
        problems.append(f"cited but not in references.bib: {key}  "
                        f"(in {', '.join(sorted(cited[key]))})")
    for key in sorted(defined - set(cited)):
        problems.append(f"in references.bib but cited nowhere: {key}")
    for key in sorted(duplicates):
        problems.append(f"duplicate entry in references.bib: {key}")
    for key in sorted(k for k, v in dois.items() if v is None):
        problems.append(f"no doi field: {key}")
    for key, doi in sorted((k, v) for k, v in dois.items() if v):
        if not DOI_SHAPE.match(doi):
            problems.append(f"doi is not shaped like a DOI: {key} -> {doi!r}")
    for suffix, n in sorted(unruled.items()):
        problems.append(
            f"unruled file type {suffix!r} ({n} file(s)): decide whether it can "
            f"carry citations, then add it to READ_SUFFIXES or UNCITED_SUFFIXES")
    for name, found in extractors.items():
        if not found:
            problems.append(f"extractor matched nothing: {name!r} -- either the "
                            f"syntax left the repository or the extractor broke")

    print(f"bibliography: {len(defined)} entries, "
          f"{sum(1 for v in dois.values() if v)} with a doi field")
    print(f"files read: {len(files)}  ({', '.join(sorted(READ_SUFFIXES))})")
    if skipped:
        print("  ruled as carrying no citations: "
              + ", ".join(f"{s} x{n}" for s, n in sorted(skipped.items())))
    if unruled:
        print("  UNRULED types present: "
              + ", ".join(f"{s} x{n}" for s, n in sorted(unruled.items())))
    print("citations found, by syntax:")
    for name, found in extractors.items():
        print(f"  {len(found):3d} distinct keys   {name}")
    print(f"distinct keys cited overall: {len(cited)}")
    print("\nnot checked here: that a DOI resolves, or that its metadata "
          "matches the entry.\nBoth need the network and stay a human step.")

    if problems:
        print("\nPROBLEMS:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print("\nno problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
