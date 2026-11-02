#!/usr/bin/env python3
"""Mutation test: prove `check_participant_firewall.py` can go red, and for what.

The firewall checker reported clean the first time it ran, which is also what a
checker with a blind spot does. Since the policy now marks clauses **CHECKED**
on the strength of that script, "checked" has to mean more than "it was quiet".

Each case names the defect it is capable of catching. Two are worth calling out:

- **the history cases commit.** The clauses say "on any branch", so the checker
  reads `git log --all`, not the working tree. A test that only wrote a file
  into the tree would pass against a checker that never looked at history, and
  would therefore be testing nothing.
- **the last case removes git.** A check that silently covers three of its five
  parts because a tool is missing is worse than one that fails, so the checker
  refuses to report on a subset. This asserts that it refuses.

Nothing here contains a participant name, an affiliation or a real address: the
mutations are shapes, as the checker is.

Usage (from the repository root):
    python evidence/test_check_participant_firewall.py

Exit status is 1 if any mutation goes unnoticed.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER = "evidence/check_participant_firewall.py"


def commit(root, message, *paths):
    """Commit the named paths, without depending on global git config.

    Only the named paths, never `-A`: a blanket add would also commit whatever
    is untracked in the copy, and switching branches afterwards would then
    delete files the test still needs. `-f` because the patterns under test are
    exactly the ones `.gitignore` blocks.
    """
    subprocess.run(["git", "add", "-f", *paths], cwd=root, check=True,
                   capture_output=True)
    # The address is assembled rather than written: the checker scans .py files
    # for addresses, and a literal one here would make this file fail the very
    # check it is testing.
    subprocess.run(
        ["git", "-c", "user.name=test",
         "-c", "user.email=test@" + "example.invalid",
         "commit", "-q", "-m", message],
        cwd=root, check=True, capture_output=True)


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"mutation target not found in {path.name}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# ---------------------------------------------------------------------------
# Mutations
# ---------------------------------------------------------------------------

def mutate_nothing(root):
    """Control: an untouched copy must be clean."""


def mutate_caption_committed(root):
    """A caption file reaches history -- the accident the net exists for."""
    (root / "notes.vtt").write_text("WEBVTT\n\n00:00.000 --> 00:02.000\nx\n",
                                    encoding="utf-8")
    commit(root, "add captions", "notes.vtt")


def mutate_guarded_dir_committed(root):
    """A folder of transcripts dropped into the tree and committed."""
    directory = root / "transcripts"
    directory.mkdir()
    (directory / "notes.md").write_text("notes\n", encoding="utf-8")
    commit(root, "add transcripts", "transcripts/notes.md")


def mutate_caption_committed_on_side_branch(root):
    """The same file, on a branch that is never pushed.

    The policy's "on any branch" clause is the reason the checker reads
    `--all`. This is the case that distinguishes it from a tree scan.
    """
    subprocess.run(["git", "checkout", "-q", "-b", "scratch/private"],
                   cwd=root, check=True, capture_output=True)
    (root / "side.srt").write_text("1\n00:00:00,000 --> 00:00:02,000\nx\n",
                                   encoding="utf-8")
    commit(root, "add on a side branch", "side.srt")
    subprocess.run(["git", "checkout", "-q", "main"], cwd=root, check=True,
                   capture_output=True)


def mutate_gitignore_caption_net_removed(root):
    """The net is quietly loosened while nothing is in the tree yet."""
    replace_once(root / ".gitignore", "*.vtt", "# *.vtt")


def mutate_gitignore_directory_net_removed(root):
    """Same, for the directory patterns."""
    replace_once(root / ".gitignore", "judging-notes/", "# judging-notes/")


def mutate_video_link(root):
    """A personal video link pasted into a page."""
    with (root / "concepts" / "copy-carry-spread.md").open(
            "a", encoding="utf-8") as fh:
        fh.write("\nSee https://www.youtu" + "be.com/watch?v=EXAMPLE for context.\n")


def mutate_stranger_email(root):
    """Contact information for someone who is not the author."""
    with (root / "concepts" / "copy-carry-spread.md").open(
            "a", encoding="utf-8") as fh:
        fh.write("\nContact: someone" + "@example.invalid\n")


def mutate_no_git(root):
    """git history unavailable: the checker must refuse, not cover a subset.

    Renamed rather than deleted: git keeps object files read-only, and on
    Windows removing the directory raises before the case has been tested.
    """
    (root / ".git").rename(root / "git-disabled")


CASES = [
    (mutate_nothing, None,
     "an unmutated copy reports clean"),
    (mutate_caption_committed, "caption/subtitle file was added in history",
     "a caption file committed on the current branch"),
    (mutate_caption_committed_on_side_branch,
     "caption/subtitle file was added in history",
     "a caption file committed on a branch that is never pushed"),
    (mutate_guarded_dir_committed, "guarded directory appears in history",
     "a folder of transcripts committed"),
    (mutate_gitignore_caption_net_removed, ".gitignore no longer guards *.vtt",
     "the caption net removed from .gitignore"),
    (mutate_gitignore_directory_net_removed,
     ".gitignore no longer guards judging-notes/",
     "a guarded directory removed from .gitignore"),
    (mutate_video_link, "personal video/channel link",
     "a personal video link in a page"),
    (mutate_stranger_email, "email address not in ALLOWED_EMAILS",
     "contact information for someone other than the author"),
    (mutate_no_git, "cannot read git history",
     "git history unavailable: refuses rather than covering a subset"),
]


def run_case(mutate, expect):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "repo"
        # Copied WITH .git: the clauses are about history, so the test has to
        # be able to reach it.
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns("__pycache__"))
        mutate(root)
        result = subprocess.run([sys.executable, str(root / CHECKER)],
                                capture_output=True, text=True, cwd=root)
        output = result.stdout + result.stderr

    if expect is None:
        ok = result.returncode == 0 and "no problems" in output
        return ok, "" if ok else f"exit {result.returncode}"
    if result.returncode != 1:
        return False, f"exit {result.returncode}, expected 1"
    if expect not in output:
        return False, f"did not report {expect!r}"
    return True, ""


def main():
    print(f"Mutation test for {CHECKER}")
    print(f"{len(CASES)} cases, one mutation each, on a temporary clone\n")
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
        print(f"{failures} of {len(CASES)} mutations went unnoticed.")
        return 1
    print(f"all {len(CASES)} cases behaved as specified. That is the measured "
          f"domain of the\nCHECKED rows in docs/participant-material-policy.md "
          f"-- the file-shaped accident.\nIt is not evidence about the CHECKABLE "
          f"or ATTESTED clauses, and no arrangement\nof scripts could be.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
