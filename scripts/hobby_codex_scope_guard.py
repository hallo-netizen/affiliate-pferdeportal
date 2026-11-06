#!/usr/bin/env python3
"""Fail-closed write-scope audit for Hobby Depot Codex pilot PR #632."""
import os
import subprocess
import sys
from pathlib import Path

BASE = "hobbyroom/project-memory-campus-v1-20260905"
ALLOWED_PREFIXES = (
    "protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/",
    ".github/workflows/hobby-",
    "scripts/hobby_",
)
ALLOWED_EXACT = {
    "AGENTS.md",
    ".github/workflows/hd003-tile-images-audit-20261106.yml",
    "scripts/hd003_tile_images_audit_20261106.py",
}
FORBIDDEN = ("control/", "isolated_system4/", ".pferde-capsule/", "protocol/PROJECT_MEMORY/PROJEKTE/PFERDE", "K0/")


def cmd(*args):
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{args}: {p.stderr.strip() or p.stdout.strip()}")
    return p.stdout.strip()


def allowed(path):
    if path.startswith(FORBIDDEN):
        return False
    return path in ALLOWED_EXACT or path.startswith(ALLOWED_PREFIXES)


def main():
    try:
        repo = Path(cmd("git", "rev-parse", "--show-toplevel"))
        os.chdir(repo)
        branch = cmd("git", "branch", "--show-current")
        ref = os.environ.get("GITHUB_HEAD_REF") or os.environ.get("GITHUB_REF_NAME") or branch
        # GitHub Actions refs can be detached. They must still target this exact pilot branch.
        expected = "hobbyroom/hd003-category-tile-image-audit-20261106"
        if expected not in {branch, ref}:
            print(f"HOBBY_SCOPE_BLOCKED:WRONG_BRANCH:{branch}:{ref}")
            return 2
        cmd("git", "fetch", "--quiet", "--no-tags", "--depth=1", "origin", f"{BASE}:refs/remotes/origin/{BASE}")
        base = f"refs/remotes/origin/{BASE}"
        changed = [p for p in cmd("git", "diff", "--name-only", "--no-renames", base, "HEAD").splitlines() if p]
        changed += [p for p in cmd("git", "diff", "--name-only").splitlines() if p]
        # Untracked files from a Codex task are also checked. Ignore Python cache only.
        untracked = cmd("git", "ls-files", "--others", "--exclude-standard")
        changed += [p for p in untracked.splitlines() if p and "__pycache__/" not in p]
        illegal = sorted(set(p for p in changed if not allowed(p)))
        if illegal:
            print("HOBBY_SCOPE_BLOCKED:OUT_OF_SCOPE:" + ",".join(illegal))
            return 2
        # Exact unchanged original global gate in every base version.
        original = cmd("git", "show", f"{base}:AGENTS.md")
        actual = Path("AGENTS.md").read_text()
        if not actual.endswith(original):
            print("HOBBY_SCOPE_BLOCKED:ORIGINAL_PFERDE_AGENT_RULES_MUTATED")
            return 2
        # Exact K0-related contents cannot differ from the untouched base.
        for prefix in ("control/", "isolated_system4/"):
            diff = cmd("git", "diff", "--name-only", base, "HEAD", "--", prefix)
            if diff:
                print("HOBBY_SCOPE_BLOCKED:PFERDE_FILES_CHANGED:" + diff.replace("\n", ","))
                return 2
        print("HOBBY_SCOPE_PASS:branch=" + expected + ";files=" + str(len(set(changed))) + ";Pferde/K0 unchanged")
        return 0
    except Exception as e:
        print(f"HOBBY_SCOPE_BLOCKED:VERIFY_FAILED:{str(e)[:400]}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
