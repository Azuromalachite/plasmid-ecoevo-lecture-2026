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
2. **Which files it has decided carry no citations.** `UNCITED_SUFFIXES` and
   `UNCITED_NAMES` are that decision, written down. A file in neither set is a
   **failure**, not a skip: something nobody has ruled on has appeared, and the
   right response is to rule on it rather than to walk past it. Extensionless
   files are ruled on by name, because an empty suffix is not a type (OF-12).
3. **Which syntaxes it understands.** Citations in this repository are written
   three different ways, and a checker that knew only the obvious one would
   report the other two as orphans. Each extractor reports its own count, so an
   extractor that silently stops matching is visible as a zero rather than as
   an absence.
4. **Where the citation sits.** A key cited only from `reviews/` or `docs/` is
   kept alive by commentary about the repository, not by the material, and the
   orphan check cannot see the difference. The split is reported, with the keys
   named, and does not fail: whether a review citing a work it alone needs is a
   problem is a judgement, and this script does not make judgements (OF-11).

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
# the bibliography itself, the citation file, figure output and plain text.
UNCITED_SUFFIXES = {".bib", ".cff", ".svg", ".txt"}

# Extensionless files are ruled on by NAME. OF-12: `""` used to sit in the set
# above, where it read as a fifth decision and was in fact a standing exemption
# for every extensionless file that would ever exist here. Measured: a file
# named NOTES citing a key that does not exist produced "no problems", while an
# unruled `.tex` failed loudly -- the same checker enforcing its own rule in one
# direction only. Three names are a decision; `""` was a hole shaped like one.
UNCITED_NAMES = {"LICENSE", ".gitignore", ".gitattributes"}

# (4) Where a citation sits. OF-11: this checker had no split at all, so a
# bibliography entry kept alive only by commentary counted as cited and could
# never be reported as an orphan.
#
# This set is deliberately NOT the sibling's CONTENT_DIRS, and saying so is the
# point of this comment -- differing from it *silently* was the finding, not
# differing from it. `check_claim_ids.py` asks "is this claim ID surfaced to a
# reader on a page?", so figure scripts and README fall outside its content
# set. This script asks "is this source doing work in the public material?",
# and a figure footer citation is work: it ships inside the SVG. So the split
# here is material against commentary, and commentary is the two directories
# that talk ABOUT the repository rather than teach from it.
COMMENTARY_DIRS = {"reviews", "docs"}

# A BibTeX key in this repository: lowercase name, four-digit year, suffix.
KEY_SHAPE = r"[a-z][a-z-]*[0-9]{4}[a-z0-9]*"
KEY_SHAPE_RE = re.compile(r"\A" + KEY_SHAPE + r"\Z")

# Citation syntaxes. See the module docstring, point 3.
# Assembled rather than written whole: the pattern is itself a citation
# group, so a version written as one literal matched its own source and
# reported the regex as a malformed key.
PANDOC_GROUP = re.compile(r"\[" + r"@[^\]]*\]", re.S)

# G2: take whatever follows the `@` and judge it, rather than matching only
# things already shaped like a key. The earlier version extracted with
# KEY_SHAPE, so a key the shape did not fit was not reported as undefined -- it
# was not seen at all, and a bracketed `@Sanmillan2017costs` -- a capitalised
# real key and
# one of the commonest citation typos there is, passed silently. A checker
# whose extractor and whose validator are the same regex can only ever find
# what it already expected.
KEY_TOKEN_IN_GROUP = re.compile(r"@([^\s;,\]]+)")

# Citations written INSIDE code spans or fences are being discussed, not made:
# a bracketed `@key` in a sentence about citation syntax, the examples in this
# file's own
# docstring, the planted keys in the mutation test. They are removed before
# extraction so that documentation about citations does not become a corpus of
# them -- the same reason the mutation tests assemble their brackets at run
# time. A real citation never needs backticks.
CODE_SPAN = re.compile(r"`{1,3}.*?`{1,3}", re.S)
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
    """Yield readable files, the skip tally, and anything unruled.

    Unruled things come back in two tallies because they are ruled on in two
    ways: a type by its suffix, an extensionless file by its name. Collapsing
    them would report a new `NOTES` as unruled file type '', which names
    neither the file nor the set to add it to.
    """
    skipped = collections.Counter()
    unruled_suffixes = collections.Counter()
    unruled_names = collections.Counter()
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or set(path.parts) & SKIP_DIRS:
            continue
        suffix = path.suffix
        if suffix in READ_SUFFIXES:
            files.append(path)
        elif suffix in UNCITED_SUFFIXES:
            skipped[suffix] += 1
        elif not suffix and path.name in UNCITED_NAMES:
            skipped[path.name] += 1
        elif not suffix:
            unruled_names[path.name] += 1
        else:
            unruled_suffixes[suffix] += 1
    return files, skipped, unruled_suffixes, unruled_names


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
    """Bracketed citations, including groups that wrap across lines.

    Returns (found, malformed). Every token after an `@` inside a citation
    group is extracted; those that are not shaped like a key are returned as
    malformed rather than dropped, because a key the extractor cannot parse is
    a defect to report, not an absence of a citation.
    """
    found, malformed = {}, {}
    for path in files:
        text = CODE_SPAN.sub(" ", read_text(path))
        where = path.relative_to(root).as_posix()
        for group in PANDOC_GROUP.findall(text):
            for token in KEY_TOKEN_IN_GROUP.findall(group):
                target = found if KEY_SHAPE_RE.match(token) else malformed
                target.setdefault(token, set()).add(where)
    return found, malformed


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
    files, skipped, unruled_suffixes, unruled_names = walk(root)

    pandoc, malformed = cites_pandoc(files, root)
    extractors = {
        "pandoc  bracketed citations": pandoc,
        "registry  references:": cites_registry(root),
        "figure footer  SOURCE_KEYS": cites_figure_footers(root),
    }
    cited = merge(*extractors.values())

    # OF-11. A key every one of whose citation sites is commentary. Registry
    # sites are spelled "claims.yml:<id>" rather than as paths, which have no
    # directory part and so never count as commentary -- correct, since the
    # registry is material.
    commentary_only = sorted(
        key for key, where in cited.items()
        if where and all(set(Path(site).parts) & COMMENTARY_DIRS
                         for site in where))

    problems = []

    for token in sorted(malformed):
        problems.append(
            f"malformed citation key: {token!r}  "
            f"(in {', '.join(sorted(malformed[token]))}). Keys are lowercase, "
            f"a four-digit year, then a suffix -- e.g. sanmillan2017costs")

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
    for suffix, n in sorted(unruled_suffixes.items()):
        problems.append(
            f"unruled file type {suffix!r} ({n} file(s)): decide whether it can "
            f"carry citations, then add it to READ_SUFFIXES or UNCITED_SUFFIXES")
    for name, n in sorted(unruled_names.items()):
        problems.append(
            f"unruled extensionless file {name!r}: decide whether it can carry "
            f"citations, then add its name to UNCITED_NAMES -- or, if it can, "
            f"give it a suffix in READ_SUFFIXES")
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
    if unruled_suffixes or unruled_names:
        print("  UNRULED present: "
              + ", ".join([f"{s} x{n}" for s, n in sorted(unruled_suffixes.items())]
                          + [f"{n_} (no suffix)" for n_ in sorted(unruled_names)]))
    print("citations found, by syntax:")
    for name, found in extractors.items():
        print(f"  {len(found):3d} distinct keys   {name}")
    print(f"distinct keys cited overall: {len(cited)}  "
          f"({len(cited) - len(commentary_only)} from the material, "
          f"{len(commentary_only)} only from commentary)")
    if commentary_only:
        print("  cited only from " + "/".join(sorted(COMMENTARY_DIRS)) + ": "
              + ", ".join(commentary_only))
        print("  Not an error: a review may cite a work the teaching material "
              "does not.\n  Reported because such a key cannot be caught by "
              "the orphan check -- commentary\n  about the repository keeps "
              "its bibliography entry alive.")
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
