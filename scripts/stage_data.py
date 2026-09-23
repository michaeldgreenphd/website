#!/usr/bin/env python3
"""
Stage the fetched data files for publishing, and check what gets committed.

The data workflow (.github/workflows/update-scholar.yml) runs in two jobs.
The fetch job runs the third-party packages with a read-only token and
hands over only the five data files, as an artifact. The publish job holds
the write token and runs nothing but this script and render_snapshot.py
from its own checkout (standard library only):

    python3 scripts/stage_data.py import DIR   # before rendering
    python3 scripts/stage_data.py check        # after rendering

import: copy each data file from DIR into the repository. A JSON file must
decode to an object and a PNG must start with the PNG signature; a file
that fails is skipped (the committed version stays) and the step exits 1
with an ::error:: line after copying the others.

check: refuse the commit unless only the data files and index.html differ
from HEAD, and index.html only between its <!-- data:NAME --> markers.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
JSON_FILES = ["scholar_stats.json", "substack_posts.json", "orcid_works.json"]
PNG_FILES = ["citations_over_time.png", "citations_over_time_dark.png"]
ALLOWED_CHANGES = set(JSON_FILES + PNG_FILES + ["index.html"])
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
DATA_BLOCK_RE = re.compile(r"(<!-- data:([\w-]+) -->).*?(<!-- /data:\2 -->)", re.S)


def problem_with(name, data):
    """Why this data file must not be published, or None if it is fine."""
    if name in PNG_FILES:
        return None if data.startswith(PNG_SIGNATURE) else "not a PNG file"
    try:
        value = json.loads(data.decode("utf-8"))
    except (ValueError, RecursionError) as err:
        return f"not valid JSON ({err})"
    return None if isinstance(value, dict) else "not a JSON object"


def import_files(source_dir):
    failed = False
    for name in JSON_FILES + PNG_FILES:
        src = Path(source_dir) / name
        try:
            data = src.read_bytes()
        except OSError as err:
            print(f"::error::stage_data: {name} is missing from the fetch job's files ({err})")
            failed = True
            continue
        reason = problem_with(name, data)
        if reason:
            print(f"::error::stage_data: {name} is {reason}; keeping the committed version")
            failed = True
            continue
        shutil.copyfile(src, REPO_ROOT / name)
    return 1 if failed else 0


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True
    ).stdout


def outside_data_blocks(doc):
    return DATA_BLOCK_RE.sub(r"\1\3", doc)


def check():
    entries = git("status", "--porcelain=v1", "-z", "--untracked-files=all").split(b"\0")
    changed = {entry[3:].decode("utf-8", "replace") for entry in entries if entry}
    unexpected = sorted(changed - ALLOWED_CHANGES)
    if unexpected:
        print(f"::error::stage_data: unexpected changes, not committing: {', '.join(unexpected)}")
        return 1
    if "index.html" in changed:
        before = git("show", "HEAD:index.html").decode("utf-8")
        after = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        if outside_data_blocks(before) != outside_data_blocks(after):
            print("::error::stage_data: index.html changed outside its data blocks, not committing")
            return 1
    print(f"Changes are limited to the data files: {', '.join(sorted(changed)) or 'none'}")
    return 0


def main(argv):
    if len(argv) == 3 and argv[1] == "import":
        return import_files(argv[2])
    if len(argv) == 2 and argv[1] == "check":
        return check()
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
