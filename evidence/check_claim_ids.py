#!/usr/bin/env python3
"""Check cited claim IDs, the layer/status vocabulary, and registry<->page sync.

This checks EXISTENCE ONLY. It cannot tell whether a paraphrase preserved a
claim's scope, uncertainty or evidence state, and it does not try: a check
that appeared to police semantic fidelity would license exactly the drift it
seemed to prevent. Humans do that part. See docs/pedagogy-conventions.md.

Also reports claims whose `pages:` list names a file that does not exist, and
claims never cited anywhere, which are usually a rename left half-finished.

Every run states the file types it read and tallies the ones it did not, so a
clean report cannot be mistaken for coverage of a type the check never opens.
`.ipynb` is currently among the types it does not read; the tally says so.

Usage (from the repository root):
    python evidence/check_claim_ids.py

Exit status is 1 if anything is wrong, so this can gate a commit later.
"""

import collections
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("needs pyyaml:  uv run --no-project --with pyyaml python evidence/check_claim_ids.py")

CLAIM_RE = re.compile(r"\bclaim\.[a-z0-9_]+(?:\.[a-z0-9_]+)+")
SKIP_DIRS = {".git", "__pycache__"}

# OF-7: the file types this check can read, named rather than inlined, and
# reported on every run alongside a tally of the types it skipped. A check that
# does not say what it opened can report clean on a domain it never saw -- which
# is how a scratch bibliography checker once called three real citations orphans
# because it did not open `.ipynb`. Enumerating the domain does not widen it;
# it stops the silence from looking like a pass.
READ_SUFFIXES = {".md", ".yml", ".py"}

# Content pages, as opposed to the files that DEFINE the vocabulary (evidence/,
# docs/) and the files that comment on it (reviews/). Used by the registry<->page
# sync check below, and to split the citation counts: a claim ID mentioned in a
# review is not the same fact as one cited on a page, and reporting them in one
# number makes the page count drift upward with every review round (OF-9).
CONTENT_DIRS = {"case-studies", "concepts", "misconceptions", "models"}

# The two axes. See evidence/evidence-levels.md.
LAYERS = {"source", "interpretation", "model", "observation", "convention"}
STATUSES = {"supported", "contested", "unsupported", "refuted",
            "not_tested", "not_applicable"}
CHECKED_AGAINST = {"full_text", "abstract", "own_derivation"}


def main():
    root = Path(__file__).resolve().parent.parent
    claims_path = root / "evidence" / "claims.yml"
    data = yaml.safe_load(claims_path.read_text(encoding="utf-8"))
    defined = {c["id"] for c in data["claims"]}

    cited = {}
    files_read = 0
    skipped_suffixes = collections.Counter()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or set(path.parts) & SKIP_DIRS:
            continue
        if path.suffix not in READ_SUFFIXES:
            skipped_suffixes[path.suffix or "(no suffix)"] += 1
            continue
        if path.name == "claims.yml":
            continue
        files_read += 1
        for cid in CLAIM_RE.findall(path.read_text(encoding="utf-8")):
            cited.setdefault(cid, set()).add(path.relative_to(root).as_posix())

    problems = []

    for cid in sorted(set(cited) - defined):
        problems.append(f"cited but not defined: {cid}  "
                        f"(in {', '.join(sorted(cited[cid]))})")

    # A2: the registry<->page link is hand-maintained and was unvalidated in
    # both directions, which is how a `status: contested` desync survived
    # every check. These two loops close that.
    status_re = re.compile(r"`?status:\s*([a-z_]+)`?")
    layer_re = re.compile(r"`?layer:\s*([a-z_]+)`?")
    by_id = {c["id"]: c for c in data["claims"]}
    # Content pages only. evidence/ and docs/ DEFINE the vocabulary, so every
    # status and layer string appears there legitimately; running the sync
    # check over them produced a false positive on the badge mapping table,
    # and a check that fires on its own dictionary gets ignored.
    for path in sorted(root.rglob("*.md")):
        if set(path.parts) & SKIP_DIRS or not (set(path.parts) & CONTENT_DIRS):
            continue
        text = path.read_text(encoding="utf-8")
        # Attribute each stated status/layer to the NEAREST claim ID, not to
        # every ID within a window. A first version used a 400-character
        # window and fired on a passage that correctly states two claims with
        # different statuses side by side -- the window overlapped, so each
        # was checked against the other's registry entry.
        ids = [(m.start(), m.group(0)) for m in CLAIM_RE.finditer(text)
               if m.group(0) in by_id]
        if not ids:
            continue
        for rex, field, vocab in ((status_re, "status", STATUSES),
                                  (layer_re, "layer", LAYERS)):
            for m in rex.finditer(text):
                stated = m.group(1)
                if stated not in vocab:
                    continue
                pos, cid = min(ids, key=lambda p: abs(p[0] - m.start()))
                if abs(pos - m.start()) > 300:
                    continue
                if stated != by_id[cid].get(field):
                    problems.append(
                        f"{path.relative_to(root).as_posix()}: states "
                        f"{field} '{stated}' nearest to {cid}, registry says "
                        f"'{by_id[cid].get(field)}'")

    for claim in data["claims"]:
        cid = claim["id"]
        if claim.get("layer") not in LAYERS:
            problems.append(f"{cid}: layer {claim.get('layer')!r} not in vocabulary")
        if claim.get("status") not in STATUSES:
            problems.append(f"{cid}: status {claim.get('status')!r} not in vocabulary")
        # A convention is a house rule, so no evidential status applies to it.
        if claim.get("layer") == "convention" and claim.get("status") != "not_applicable":
            problems.append(f"{cid}: layer 'convention' should carry status "
                            f"'not_applicable', not {claim.get('status')!r}")
        v = claim.get("verification")
        if v and v.get("checked_against") not in CHECKED_AGAINST:
            problems.append(f"{cid}: verification.checked_against "
                            f"{v.get('checked_against')!r} not in vocabulary")
        for page in claim.get("pages") or []:
            if not (root / page).exists():
                problems.append(f"{claim['id']}: pages names a missing file: {page}")

    # A claim is normally linked to prose by its `pages:` list, not by having
    # its ID written out in the text; citing the ID inline is reserved for
    # claims whose status the reader needs to see. So "no ID citation" is not
    # the signal. "Neither an ID citation nor a page" is.
    orphaned = sorted(cid for cid in defined - set(cited)
                      if not next(c for c in data["claims"] if c["id"] == cid).get("pages"))

    # OF-9: split the inline-citation count by where the citation is. A claim ID
    # written on a content page is a page telling a reader to check a status; the
    # same ID in a review or a release note is commentary. Reported as one number
    # they are indistinguishable, and the page figure rises every review round.
    on_content = {cid for cid in set(cited) & defined
                  if any(set(Path(p).parts) & CONTENT_DIRS for p in cited[cid])}
    elsewhere = (set(cited) & defined) - on_content

    by_layer = collections.Counter(c.get("layer") for c in data["claims"])
    by_status = collections.Counter(c.get("status") for c in data["claims"])
    print(f"files read: {files_read}  "
          f"({', '.join(sorted(READ_SUFFIXES))})")
    if skipped_suffixes:
        tally = ", ".join(f"{suffix} x{n}"
                          for suffix, n in sorted(skipped_suffixes.items()))
        print(f"  not read, by type: {tally}")
    print(f"claims defined: {len(defined)}")
    print(f"  layer : {dict(by_layer)}")
    print(f"  status: {dict(by_status)}")
    print(f"claim IDs cited inline: {len(on_content)} on content pages, "
          f"{len(elsewhere)} elsewhere")
    print(f"claims linked to a page: "
          f"{sum(1 for c in data['claims'] if c.get('pages'))}")
    if orphaned:
        print("\nattached to nothing (no inline citation and no pages entry):")
        for cid in orphaned:
            print(f"  {cid}")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(f"  {p}")
        return 1
    print("\nno problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
