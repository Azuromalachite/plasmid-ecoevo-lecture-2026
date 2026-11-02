#!/usr/bin/env python3
"""Run the checkable floor of the participant-material policy.

`docs/participant-material-policy.md` marks each of its clauses **CHECKED**,
**CHECKABLE** or **ATTESTED**. This script is what the first of those words
means. Without it, "checked" would mean "the author ran a grep once", which is
an attestation wearing a check's clothes -- and is the defect OF-2 was opened
for, in a different file.

WHAT IT CHECKS. Five things, all of them *shapes*, none of them names:

  1. no caption or subtitle file was ever added, on any branch in this clone;
  2. no guarded directory was ever added, on any branch in this clone;
  3. the `.gitignore` net for both is still present, so it cannot be removed
     quietly while this script keeps reporting clean;
  4. no personal video or channel link is in the working tree;
  5. no email address is in the working tree except those explicitly allowed.

WHAT IT CANNOT CHECK, and the policy says so in its own voice:

  - **names and affiliations.** The check is a grep against the participant
    list, and that list is the material the policy excludes. Committing it to
    make this script complete would violate the clause the script exists to
    support. The policy marks those clauses CHECKABLE for exactly this reason:
    the procedure is real, the input cannot live here.
  - **anything requiring judgement.** Whether a paraphrase came from a
    presentation, whether an emphasis was chosen because of what was presented,
    whether prose began life as someone's unpublished submission. These have no
    signature to search for. The policy marks them ATTESTED. A script that
    appeared to cover them would make the firewall look verified when the part
    that matters is a person's word.

So a clean run here is a **floor**, not the policy. It catches the file-shaped
accident -- a folder of captions dropped into the tree -- and says nothing about
a page written by someone who watched the presentations and did not notice they
were remembering one.

Usage (from the repository root):
    python evidence/check_participant_firewall.py

Exit status is 1 if anything is wrong.
"""

import re
import subprocess
import sys
from pathlib import Path

# Shapes, not names. Nothing in this file identifies anyone.
CAPTION_SUFFIXES = (".vtt", ".srt", ".sbv", ".ttml")
GUARDED_DIRS = ("transcripts", "participant-data", "judging-notes",
                "curation-notes", "submissions")
LINK_RE = re.compile(r"(?:youtube\.com|youtu\.be|vimeo\.com)/\S*")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# The repository's own addresses. An address here is a deliberate decision,
# not an exception that accumulated: anything else in the tree fails the run.
ALLOWED_EMAILS = {
    "austinwongsatit@kaist.ac.kr",   # the author, in CITATION.cff
    "noreply@anthropic.com",         # commit co-author trailer
}

SCANNED_SUFFIXES = {".md", ".yml", ".py", ".ipynb", ".cff", ".bib"}
SKIP_DIRS = {".git", "__pycache__"}


def git(root, *args):
    result = subprocess.run(("git",) + args, cwd=root,
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def paths_ever_added(root):
    """Every path ever added in any reachable commit, on any branch here.

    `--all` is the point: the policy forbids this material on branches that are
    never pushed, so checking the working tree would miss the case the clause
    is most worried about. It still cannot see a branch that exists only in
    somebody else's clone, which is why the policy's branch clause is marked
    CHECKED for shapes and ATTESTED for content.
    """
    out = git(root, "log", "--all", "--diff-filter=A", "--name-only",
              "--pretty=format:")
    return sorted({line.strip() for line in out.splitlines() if line.strip()})


def tree_files(root):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or set(path.parts) & SKIP_DIRS:
            continue
        if path.suffix in SCANNED_SUFFIXES:
            yield path


def main():
    root = Path(__file__).resolve().parent.parent
    problems = []

    try:
        added = paths_ever_added(root)
    except (RuntimeError, FileNotFoundError) as exc:
        # Not a skip. Without git the history checks do not run, and a run that
        # quietly covered three of five checks would be the worst outcome here.
        print(f"cannot read git history: {exc}")
        print("This check is not meaningful without it. Failing rather than "
              "reporting on a subset.")
        return 1

    captions = [p for p in added if p.lower().endswith(CAPTION_SUFFIXES)]
    for path in captions:
        problems.append(f"caption/subtitle file was added in history: {path}")

    guarded = [p for p in added
               if any(part in GUARDED_DIRS for part in p.split("/"))]
    for path in guarded:
        problems.append(f"guarded directory appears in history: {path}")

    # Active patterns only. A commented-out pattern still contains its own
    # text, so a substring search would read `# *.vtt` as the net being intact
    # -- a check that passes on the thing it is meant to catch.
    active = {line.strip() for line in
              (root / ".gitignore").read_text(encoding="utf-8").splitlines()
              if line.strip() and not line.lstrip().startswith("#")}
    for suffix in CAPTION_SUFFIXES:
        if f"*{suffix}" not in active:
            problems.append(f".gitignore no longer guards *{suffix}")
    for directory in GUARDED_DIRS:
        if not {f"{directory}/", f"**/{directory}/"} & active:
            problems.append(f".gitignore no longer guards {directory}/")

    links, emails = [], []
    for path in tree_files(root):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        for match in LINK_RE.findall(text):
            links.append((rel, match))
        for match in EMAIL_RE.findall(text):
            if match not in ALLOWED_EMAILS:
                emails.append((rel, match))

    for rel, match in links:
        problems.append(f"personal video/channel link in {rel}: {match}")
    for rel, match in emails:
        problems.append(f"email address not in ALLOWED_EMAILS, in {rel}: {match}")

    print(f"commits searched: {len(git(root, 'rev-list', '--all').split())} "
          f"(every branch in this clone)")
    print(f"paths ever added: {len(added)}")
    print(f"  caption/subtitle files: {len(captions)}")
    print(f"  guarded directories   : {len(guarded)}")
    print(f".gitignore guards {len(CAPTION_SUFFIXES)} caption formats and "
          f"{len(GUARDED_DIRS)} directories")
    print(f"working tree scanned: {sum(1 for _ in tree_files(root))} files "
          f"({', '.join(sorted(SCANNED_SUFFIXES))})")
    print(f"  video/channel links   : {len(links)}")
    print(f"  unexpected emails     : {len(emails)}")

    print("\nNOT checked here, and marked CHECKABLE or ATTESTED in the policy:")
    print("  names and affiliations -- the grep needs the participant list as")
    print("  input, and that list is the material the policy excludes.")
    print("  Anything needing judgement: whether a paraphrase, an emphasis or a")
    print("  framing came from a presentation. No signature exists to search for.")

    if problems:
        print("\nPROBLEMS:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print("\nno problems (this is the floor, not the policy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
