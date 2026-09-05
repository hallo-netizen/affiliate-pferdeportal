#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
from typing import Dict, List, Tuple

OFFICIAL_CAMPUS_REF = "hobbyroom/project-memory-campus-v1-20260905"
PROJECT_MEMORY_ROOT = "protocol/PROJECT_MEMORY/"
CAPSULE_DIR = pathlib.Path(".paul-capsule")
ASSIGNMENT_MARKER = "PAUL_ASSIGNMENT_V1"

FORBIDDEN_WRITE_PREFIXES = (
    "protocol/PROJECT_MEMORY/",
    ".github/workflows/",
    "control/cloud-entry-gate/",
    "control/deterministic-entrance-gate/",
    "control/production-continuity/",
    "control/paul-scope-gate/",
)
FORBIDDEN_WRITE_EXACT = {"AGENTS.md"}


class Blocked(RuntimeError):
    pass


def git(*args: str, check: bool = True) -> str:
    p = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and p.returncode != 0:
        raise Blocked(f"GIT_BLOCKED:{' '.join(args)}:{p.stderr.strip()}")
    return p.stdout.strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch_official_campus() -> str:
    git(
        "fetch",
        "--no-tags",
        "origin",
        f"refs/heads/{OFFICIAL_CAMPUS_REF}",
    )
    return git("rev-parse", "FETCH_HEAD")


def show(ref: str, path: str) -> str:
    return git("show", f"{ref}:{path}")


def list_hobbyrooms(ref: str) -> List[str]:
    raw = git("ls-tree", "-r", "--name-only", ref, "--", PROJECT_MEMORY_ROOT)
    return [
        p for p in raw.splitlines()
        if p.startswith(PROJECT_MEMORY_ROOT) and p.endswith("/HOBBYRAUM.md")
    ]


def parse_kv_block(text: str, path: str) -> Dict[str, str] | None:
    pattern = re.compile(
        r"<!--\s*" + re.escape(ASSIGNMENT_MARKER) + r"\s*\n(?P<body>.*?)\n\s*-->",
        re.S,
    )
    matches = list(pattern.finditer(text))
    if not matches:
        return None
    if len(matches) != 1:
        raise Blocked(f"PAUL_ASSIGNMENT_INVALID:MULTIPLE_BLOCKS:{path}")
    data: Dict[str, str] = {}
    for line in matches[0].group("body").splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" not in line:
            raise Blocked(f"PAUL_ASSIGNMENT_INVALID:BAD_LINE:{path}:{line}")
        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()
        if not key or key in data:
            raise Blocked(f"PAUL_ASSIGNMENT_INVALID:DUPLICATE_OR_EMPTY_KEY:{path}:{key}")
        data[key] = value
    return data


def active_assignment(ref: str) -> Tuple[str, Dict[str, str]]:
    active: List[Tuple[str, Dict[str, str]]] = []
    malformed_active_markers: List[str] = []
    for path in list_hobbyrooms(ref):
        text = show(ref, path)
        if ASSIGNMENT_MARKER not in text:
            continue
        try:
            data = parse_kv_block(text, path)
        except Blocked:
            malformed_active_markers.append(path)
            continue
        if data and data.get("STATUS", "").upper() == "ACTIVE":
            active.append((path, data))
    if malformed_active_markers:
        raise Blocked("PAUL_ASSIGNMENT_INVALID:" + ",".join(sorted(malformed_active_markers)))
    if not active:
        raise Blocked("PAUL_NOT_ASSIGNED")
    if len(active) != 1:
        raise Blocked(
            "PAUL_MULTIPLE_ASSIGNMENTS_BLOCKED:" +
            ",".join(sorted(path for path, _ in active))
        )
    path, data = active[0]
    required = {
        "STATUS",
        "WORKER",
        "ASSIGNMENT_ID",
        "PAUL_BRANCH",
        "TECHNICAL_BASE_SHA",
        "WRITE_SCOPE",
        "TASK_SOURCE",
        "TARGET_SOURCE",
        "RULES_SOURCE",
    }
    missing = sorted(required.difference(data))
    if missing:
        raise Blocked("PAUL_ASSIGNMENT_INVALID:MISSING:" + ",".join(missing))
    if data["STATUS"].upper() != "ACTIVE" or data["WORKER"].upper() != "PAUL":
        raise Blocked("PAUL_NOT_ASSIGNED")
    if not re.fullmatch(r"[0-9a-fA-F]{40}", data["TECHNICAL_BASE_SHA"]):
        raise Blocked("PAUL_ASSIGNMENT_INVALID:TECHNICAL_BASE_SHA")
    if not data["PAUL_BRANCH"].startswith("paul/"):
        raise Blocked("PAUL_ASSIGNMENT_INVALID:PAUL_BRANCH")
    for key in ("TASK_SOURCE", "TARGET_SOURCE", "RULES_SOURCE"):
        if not data[key] or data[key].startswith("/") or ".." in pathlib.PurePosixPath(data[key]).parts:
            raise Blocked(f"PAUL_ASSIGNMENT_INVALID:{key}")
    validate_scope(data["WRITE_SCOPE"])
    return path, data


def validate_scope(scope: str) -> List[str]:
    if scope == "READ_ONLY":
        return []
    parts = [p.strip() for p in scope.split(";") if p.strip()]
    if not parts:
        raise Blocked("PAUL_ASSIGNMENT_INVALID:WRITE_SCOPE")
    for p in parts:
        if p.startswith("/") or ".." in pathlib.PurePosixPath(p).parts:
            raise Blocked("PAUL_ASSIGNMENT_INVALID:WRITE_SCOPE")
        if p in FORBIDDEN_WRITE_EXACT or any(p.startswith(x) for x in FORBIDDEN_WRITE_PREFIXES):
            raise Blocked(f"PAUL_ASSIGNMENT_INVALID:FORBIDDEN_SCOPE:{p}")
    return parts


def path_allowed(path: str, scope: str) -> bool:
    if path in FORBIDDEN_WRITE_EXACT or any(path.startswith(x) for x in FORBIDDEN_WRITE_PREFIXES):
        return False
    allowed = validate_scope(scope)
    if not allowed:
        return False
    for item in allowed:
        if item.endswith("/"):
            if path.startswith(item):
                return True
        elif path == item:
            return True
    return False


def ensure_branch_and_base(data: Dict[str, str], branch: str | None = None, head: str | None = None) -> Tuple[str, str]:
    branch = branch or git("branch", "--show-current")
    head = head or git("rev-parse", "HEAD")
    if branch != data["PAUL_BRANCH"]:
        raise Blocked(f"PAUL_BRANCH_MISMATCH_BLOCKED:EXPECTED={data['PAUL_BRANCH']}:GOT={branch}")
    base = data["TECHNICAL_BASE_SHA"].lower()
    git("fetch", "--no-tags", "origin", base)
    p = subprocess.run(
        ["git", "merge-base", "--is-ancestor", base, head],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if p.returncode != 0:
        raise Blocked(f"PAUL_BASE_MISMATCH_BLOCKED:{base}")
    return branch, head


def changed_paths(base: str, head: str) -> List[str]:
    paths = set(filter(None, git("diff", "--name-only", base, head).splitlines()))
    if head == git("rev-parse", "HEAD"):
        paths.update(filter(None, git("diff", "--name-only").splitlines()))
        paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
        paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    paths.discard("")
    return sorted(paths)


def enforce_scope(data: Dict[str, str], paths: List[str]) -> None:
    scope = data["WRITE_SCOPE"]
    if scope == "READ_ONLY" and paths:
        raise Blocked("PAUL_WRITE_SCOPE_BLOCKED:READ_ONLY:" + ",".join(paths))
    bad = [p for p in paths if not path_allowed(p, scope)]
    if bad:
        raise Blocked("PAUL_WRITE_SCOPE_BLOCKED:" + ",".join(bad))


def source_paths(hobbyroom: str, data: Dict[str, str]) -> List[str]:
    office = str(pathlib.PurePosixPath(hobbyroom).parent)
    candidates = [
        "protocol/PROJECT_MEMORY/START_HERE.md",
        f"{office}/START_HERE.md",
        f"{office}/CURRENT_STATE.md",
        hobbyroom,
        "protocol/PROJECT_MEMORY/FEHLERREGISTER.md",
        "protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md",
        "protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md",
        "protocol/PROJECT_MEMORY/HANDLUNGSVERZEICHNIS.md",
        data["TASK_SOURCE"],
        data["TARGET_SOURCE"],
        data["RULES_SOURCE"],
    ]
    out: List[str] = []
    for p in candidates:
        if p not in out:
            out.append(p)
    return out


def critical_source_paths(hobbyroom: str, data: Dict[str, str]) -> List[str]:
    office = str(pathlib.PurePosixPath(hobbyroom).parent)
    candidates = [
        f"{office}/CURRENT_STATE.md",
        hobbyroom,
        data["TASK_SOURCE"],
        data["TARGET_SOURCE"],
        data["RULES_SOURCE"],
    ]
    out: List[str] = []
    for p in candidates:
        if p not in out:
            out.append(p)
    return out


def snapshot_sources(ref: str, paths: List[str]) -> Dict[str, Dict[str, str]]:
    snap: Dict[str, Dict[str, str]] = {}
    for path in paths:
        text = show(ref, path)
        snap[path] = {"sha256": sha256_text(text), "content": text}
    return snap


def add_local_exclude() -> None:
    p = pathlib.Path(".git/info/exclude")
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    if ".paul-capsule/" not in text.splitlines():
        with p.open("a", encoding="utf-8") as fh:
            if text and not text.endswith("\n"):
                fh.write("\n")
            fh.write(".paul-capsule/\n")


def write_capsule(campus_head: str, hobbyroom: str, data: Dict[str, str], snap: Dict[str, Dict[str, str]]) -> None:
    if CAPSULE_DIR.exists():
        for child in sorted(CAPSULE_DIR.rglob("*"), reverse=True):
            if child.is_file() or child.is_symlink():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
    CAPSULE_DIR.mkdir(parents=True, exist_ok=True)
    src_root = CAPSULE_DIR / "sources"
    src_root.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema": "PAUL_CAPSULE_V1",
        "authority": "READ_ONLY_SNAPSHOT_OFFICIAL_CAMPUS",
        "official_campus_ref": OFFICIAL_CAMPUS_REF,
        "campus_head": campus_head,
        "hobbyroom": hobbyroom,
        "assignment": data,
        "sources": {p: {"sha256": v["sha256"]} for p, v in snap.items()},
        "critical_sources": critical_source_paths(hobbyroom, data),
    }
    (CAPSULE_DIR / "ASSIGNMENT.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    for path, item in snap.items():
        dest = src_root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(item["content"], encoding="utf-8")
    boundary = f"""# PAUL CAPSULE – READ ONLY

AUTHORITY:
Official campus ref \`{OFFICIAL_CAMPUS_REF}\` at \`{campus_head}\`.

ASSIGNMENT_ID:
\`{data['ASSIGNMENT_ID']}\`

PAUL_BRANCH:
\`{data['PAUL_BRANCH']}\`

TECHNICAL_BASE_SHA:
\`{data['TECHNICAL_BASE_SHA']}\`

WRITE_SCOPE:
\`{data['WRITE_SCOPE']}\`

This capsule is a temporary hashed snapshot, not a second truth.
The cloud capsule remains the workflow instruction.
This Paul capsule only proves current worker assignment, context and write boundary.
"""
    (CAPSULE_DIR / "BOUNDARY.md").write_text(boundary, encoding="utf-8")


def load_capsule() -> Dict:
    p = CAPSULE_DIR / "ASSIGNMENT.json"
    if not p.is_file():
        raise Blocked("PAUL_CAPSULE_MISSING")
    return json.loads(p.read_text(encoding="utf-8"))


def start() -> None:
    add_local_exclude()
    campus_head = fetch_official_campus()
    hobbyroom, data = active_assignment(campus_head)
    branch, head = ensure_branch_and_base(data)
    paths = changed_paths(data["TECHNICAL_BASE_SHA"], head)
    enforce_scope(data, paths)
    snap = snapshot_sources(campus_head, source_paths(hobbyroom, data))
    write_capsule(campus_head, hobbyroom, data, snap)
    print(f"PAUL_BOOTSTRAP_PASS:{data['ASSIGNMENT_ID']}:{campus_head}")


def verify() -> None:
    capsule = load_capsule()
    campus_head = fetch_official_campus()
    hobbyroom, data = active_assignment(campus_head)
    old = capsule["assignment"]
    stable_keys = [
        "ASSIGNMENT_ID",
        "PAUL_BRANCH",
        "TECHNICAL_BASE_SHA",
        "WRITE_SCOPE",
        "TASK_SOURCE",
        "TARGET_SOURCE",
        "RULES_SOURCE",
    ]
    if hobbyroom != capsule["hobbyroom"]:
        raise Blocked("STALE_ASSIGNMENT_BLOCKED:HOBBYRAUM_CHANGED")
    for key in stable_keys:
        if data.get(key) != old.get(key):
            raise Blocked(f"STALE_ASSIGNMENT_BLOCKED:{key}")
    branch, head = ensure_branch_and_base(data)
    enforce_scope(data, changed_paths(data["TECHNICAL_BASE_SHA"], head))

    critical = list(capsule.get("critical_sources") or [])
    current = snapshot_sources(campus_head, critical)
    for path in critical:
        if current[path]["sha256"] != capsule["sources"][path]["sha256"]:
            raise Blocked(f"STALE_ASSIGNMENT_BLOCKED:SOURCE_CHANGED:{path}")
    print(f"PAUL_VERIFY_PASS:{data['ASSIGNMENT_ID']}:{campus_head}")


def verify_pr(branch: str, head: str, pr_base: str) -> None:
    campus_head = fetch_official_campus()
    try:
        hobbyroom, data = active_assignment(campus_head)
    except Blocked as exc:
        if str(exc) == "PAUL_NOT_ASSIGNED" and not branch.startswith("paul/"):
            print("PAUL_SCOPE_NOT_APPLICABLE")
            return
        raise

    if branch == data["PAUL_BRANCH"]:
        ensure_branch_and_base(data, branch=branch, head=head)
        enforce_scope(data, changed_paths(data["TECHNICAL_BASE_SHA"], head))
        print(f"PAUL_PR_SCOPE_PASS:{data['ASSIGNMENT_ID']}:{hobbyroom}:{campus_head}")
        return

    if branch.startswith("paul/"):
        raise Blocked(
            f"PAUL_BRANCH_MISMATCH_BLOCKED:EXPECTED={data['PAUL_BRANCH']}:GOT={branch}"
        )

    # Single Writer: while Paul owns a technical write scope, every other PR
    # is barred from touching that same scope.
    locked = [
        p for p in changed_paths(pr_base, head)
        if path_allowed(p, data["WRITE_SCOPE"])
    ]
    if locked:
        raise Blocked(
            "PAUL_EXCLUSIVE_SCOPE_LOCKED:" + ",".join(locked)
        )
    print(f"PAUL_EXCLUSIVE_SCOPE_PASS:{data['ASSIGNMENT_ID']}")


def selftest() -> None:
    valid = """<!-- PAUL_ASSIGNMENT_V1
STATUS: ACTIVE
WORKER: PAUL
ASSIGNMENT_ID: T-1
PAUL_BRANCH: paul/t-1
TECHNICAL_BASE_SHA: 0123456789012345678901234567890123456789
WRITE_SCOPE: src/a.py;src/pkg/
TASK_SOURCE: protocol/task.md
TARGET_SOURCE: protocol/target.md
RULES_SOURCE: protocol/rules.md
-->"""
    d = parse_kv_block(valid, "x/HOBBYRAUM.md")
    assert d and d["ASSIGNMENT_ID"] == "T-1"
    assert path_allowed("src/a.py", d["WRITE_SCOPE"])
    assert path_allowed("src/pkg/x.py", d["WRITE_SCOPE"])
    assert not path_allowed("src/b.py", d["WRITE_SCOPE"])
    assert not path_allowed("protocol/PROJECT_MEMORY/X.md", d["WRITE_SCOPE"])
    assert not path_allowed("AGENTS.md", d["WRITE_SCOPE"])
    try:
        validate_scope("protocol/PROJECT_MEMORY/")
        raise AssertionError("forbidden scope accepted")
    except Blocked:
        pass
    try:
        validate_scope("READ_ONLY")
    except Blocked:
        raise AssertionError("READ_ONLY rejected")
    assert parse_kv_block("no assignment", "x") is None
    critical = critical_source_paths(
        "protocol/PROJECT_MEMORY/PROJEKTE/X/TEXT/HOBBYRAUM.md", d
    )
    assert "protocol/PROJECT_MEMORY/PROJEKTE/X/TEXT/CURRENT_STATE.md" in critical
    assert "protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md" not in critical
    print("PAUL_SCOPE_GATE_SELFTEST_PASS:11/11")


def main() -> int:
    try:
        if len(sys.argv) < 2:
            raise Blocked("USAGE:paul_scope_gate.py start|verify|verify-pr|selftest")
        cmd = sys.argv[1]
        if cmd == "start":
            start()
        elif cmd == "verify":
            verify()
        elif cmd == "verify-pr":
            if len(sys.argv) != 5:
                raise Blocked("USAGE:paul_scope_gate.py verify-pr <branch> <head_sha> <pr_base_sha>")
            verify_pr(sys.argv[2], sys.argv[3], sys.argv[4])
        elif cmd == "selftest":
            selftest()
        else:
            raise Blocked(f"UNKNOWN_COMMAND:{cmd}")
        return 0
    except Blocked as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
