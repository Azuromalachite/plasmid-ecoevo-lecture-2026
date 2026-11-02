#!/usr/bin/env python3
"""Run the checkable floor of the participant-material policy.

`docs/participant-material-policy.md` marks each of its clauses **CHECKED**,
**CHECKABLE** or **ATTESTED**. This script is what the first of those words
means. Without it, "checked" would mean "the author ran a grep once", which is
an attestation wearing a check's clothes -- and is the defect OF-2 was opened
for, in a different file.

WHAT IT CHECKS. Six things, all of them *shapes* or counts, none of them names:

  1. no caption or subtitle file was ever added, on any branch in this clone;
  2. no guarded directory was ever added, on any branch in this clone;
  3. the `.gitignore` net for both is still present, so it cannot be removed
     quietly while this script keeps reporting clean;
  4. no personal video or channel link is in the working tree;
  5. no email address is in the working tree except those explicitly allowed;
  6. the ratio of marks the policy states matches the marks it actually
     carries, because that sentence had already drifted once.

WHAT IT CANNOT CHECK, and the policy says so in its own voice:

  - **names and affiliations.** The check is a grep against the participant
    list, and that list is the material the policy excludes. Committing it to
    make this script complete would violate the clause the script exists to
    support. The policy marks those clauses CHECKABLE for exactly this reason:
    the procedure is real, the input cannot live here.
  - **contact information that is not an email address or a video link.** A
    phone number, a social handle, a file-sharing link, a personal site. The
    class has no edge to enumerate, so check 4 and check 5 are the whole of
    what "contact information" means here. The policy clause carries two marks
    for this reason (OF-10): CHECKED for the two shapes below, ATTESTED for
    the rest. Measured before the split: a page carrying a handle, a phone
    number and a drive link produced "no problems", exit 0.
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

    # The policy states a ratio of marks. A count in prose is an unversioned
    # copy of a computation, and this one had already drifted once -- it said
    # four checked when there were six, carried from a draft and never
    # re-derived. Counting it here is what stops the sentence and the file from
    # being two different things.
    #
    # The rule the policy commits to: outside the definition table, a badge
    # marks a clause and never explains one. So clause marks are badge
    # occurrences on lines that are not table rows.
    policy = (root / "docs" / "participant-material-policy.md")
    policy_lines = policy.read_text(encoding="utf-8").splitlines()
    badge = re.compile(r"\*\*`(CHECKED|CHECKABLE|ATTESTED)`\*\*")
    counted = {"CHECKED": 0, "CHECKABLE": 0, "ATTESTED": 0}
    for line in policy_lines:
        if line.lstrip().startswith("|"):
            continue
        for found in badge.findall(line):
            counted[found] += 1

    stated = re.search(r"\*\*(\d+) checked, (\d+) checkable, (\d+) attested\.\*\*",
                       "\n".join(policy_lines))
    if not stated:
        problems.append("the policy no longer states its ratio in a countable "
                        "form ('**N checked, N checkable, N attested.**')")
    else:
        want = dict(zip(("CHECKED", "CHECKABLE", "ATTESTED"),
                        (int(n) for n in stated.groups())))
        if want != counted:
            problems.append(
                f"the policy's stated ratio {want} does not match the badges "
                f"counted outside its definition table {counted}")

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
    print(f"policy clause marks   : {counted['CHECKED']} checked, "
          f"{counted['CHECKABLE']} checkable, {counted['ATTESTED']} attested "
          f"({'matches' if stated and want == counted else 'DISAGREES WITH'} "
          f"the ratio the policy states)")

    print("\nNOT checked here, and marked CHECKABLE or ATTESTED in the policy:")
    print("  names and affiliations -- the grep needs the participant list as")
    print("  input, and that list is the material the policy excludes.")
    print("  Contact information other than an email address or a video link:")
    print("  a phone number, a social handle, a file-sharing link. The class has")
    print("  no edge to enumerate, so the clause is marked CHECKED for the two")
    print("  shapes above and ATTESTED for the rest.")
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
