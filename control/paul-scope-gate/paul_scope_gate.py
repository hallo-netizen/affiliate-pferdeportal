#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from typing import Dict, List, Tuple

OFFICIAL_CAMPUS_REF = "hobbyroom/project-memory-campus-v1-20260905"
PROJECT_MEMORY_ROOT = "protocol/PROJECT_MEMORY/"
CAPSULE_DIR = pathlib.Path(".paul-capsule")
ASSIGNMENT_MARKER = "PAUL_ASSIGNMENT_V1"
WORK_LOCK_MARKER = "HOBBYROOM_WORK_LOCK_V1"

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
    p = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if p.returncode != 0:
        raise Blocked(f"GIT_BLOCKED:show {ref}:{path}:{p.stderr.strip()}")
    return p.stdout


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


def parse_work_lock(text: str, path: str) -> Dict[str, str] | None:
    pattern = re.compile(
        r"(?m)^" + re.escape(WORK_LOCK_MARKER) + r"\s*$\n(?P<body>.*?)\n^END_" + re.escape(WORK_LOCK_MARKER) + r"\s*$",
        re.S,
    )
    matches = list(pattern.finditer(text))
    if not matches:
        return None
    if len(matches) != 1:
        raise Blocked(f"HOBBYROOM_WORK_LOCK_INVALID:MULTIPLE_BLOCKS:{path}")
    data: Dict[str, str] = {}
    for line in matches[0].group("body").splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" not in line:
            raise Blocked(f"HOBBYROOM_WORK_LOCK_INVALID:BAD_LINE:{path}:{line}")
        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()
        if not key or key in data:
            raise Blocked(f"HOBBYROOM_WORK_LOCK_INVALID:DUPLICATE_OR_EMPTY_KEY:{path}:{key}")
        data[key] = value
    required = {
        "STATUS", "OFFICE", "MAIN_SHA", "ACTIVE_BLOCKER", "PLAN_PHASE",
        "CANDIDATE_BRANCH", "CANDIDATE_HEAD_SHA", "TECHNICAL_SCOPE_PREFIXES",
        "ALLOWED_PATH_PREFIXES", "CHECK_PAUL", "CHECK_HISTORY",
        "CHECK_LAST_GOOD", "CHECK_NEIGHBORS", "CHECK_REPEAT_CLASS",
        "CHECK_POS_NEG", "CHECK_INVARIANTS", "INTEGRATION_ALLOWED",
    }
    missing = sorted(required.difference(data))
    if missing:
        raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:MISSING:" + ",".join(missing))
    if not re.fullmatch(r"[0-9a-fA-F]{40}", data["MAIN_SHA"]):
        raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:MAIN_SHA")
    if data["STATUS"] == "FIX_ALLOWED_FOR_CODEX_TEST":
        proof_required = {
            "HISTORY_SOURCE_REF", "HISTORY_SOURCE_BLOB_SHA",
            "HISTORY_PROOF_RUNNER_REF", "HISTORY_PROOF_RUNNER_BLOB_SHA",
            "PAUL_SOURCE_REF", "PAUL_SOURCE_BLOB_SHA",
        }
        proof_missing = sorted(proof_required.difference(data))
        if proof_missing:
            raise Blocked(
                "HOBBYROOM_WORK_LOCK_INVALID:MACHINE_PROOF_MISSING:" +
                ",".join(proof_missing)
            )
        for key in ("HISTORY_SOURCE_REF", "HISTORY_PROOF_RUNNER_REF", "PAUL_SOURCE_REF"):
            value = data[key]
            if (
                not value
                or value.startswith("/")
                or ".." in pathlib.PurePosixPath(value).parts
            ):
                raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:" + key)
        for key in (
            "HISTORY_SOURCE_BLOB_SHA",
            "HISTORY_PROOF_RUNNER_BLOB_SHA",
            "PAUL_SOURCE_BLOB_SHA",
        ):
            if not re.fullmatch(r"[0-9a-fA-F]{40}", data[key]):
                raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:" + key)
    return data


def work_locks(ref: str) -> List[Tuple[str, Dict[str, str]]]:
    out: List[Tuple[str, Dict[str, str]]] = []
    for path in list_hobbyrooms(ref):
        text = show(ref, path)
        if WORK_LOCK_MARKER not in text:
            continue
        data = parse_work_lock(text, path)
        if data is not None:
            out.append((path, data))
    return out


def _scope_items(spec: str) -> List[str]:
    if spec == "NONE":
        return []
    parts = [p.strip() for p in spec.split(";") if p.strip()]
    for p in parts:
        if p.startswith("/") or ".." in pathlib.PurePosixPath(p).parts:
            raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:SCOPE")
    return parts


def _matches_scope(path: str, spec: str) -> bool:
    for item in _scope_items(spec):
        if item.endswith("/"):
            if path.startswith(item):
                return True
        elif path == item:
            return True
    return False


def _blob_at(ref: str, path: str, label: str) -> str:
    try:
        value = git("rev-parse", f"{ref}:{path}")
    except Blocked as exc:
        raise Blocked(f"HOBBYROOM_MACHINE_PROOF_SOURCE_MISSING:{label}:{path}") from exc
    if not re.fullmatch(r"[0-9a-fA-F]{40}", value):
        raise Blocked(f"HOBBYROOM_MACHINE_PROOF_BLOB_INVALID:{label}:{path}")
    return value.lower()


def _history_ids_from_matrix(text: str) -> List[str]:
    return sorted(set(re.findall(r"(?m)^M(\d{2})\s+[–-]", text)))


def _history_ids_from_runner(text: str) -> List[str]:
    pairs = re.findall(r'\("M(\d{2})",\s*m\d{2}\)', text)
    return sorted(set(pairs))


def _run_history_runner(
    runner_text: str,
    *,
    candidate: pathlib.Path,
    label: str,
) -> None:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".py", encoding="utf-8", delete=False
    ) as fh:
        fh.write(runner_text)
        runner_path = pathlib.Path(fh.name)
    try:
        env = dict(os.environ)
        env["HOBBYROOM_TARGET_ROOT"] = str(candidate)
        p = subprocess.run(
            [sys.executable, str(runner_path)],
            cwd=str(candidate),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        output = (p.stdout + p.stderr).strip()
        if p.returncode != 0 or '"status": "GESAMT PASS"' not in output:
            raise Blocked(
                f"HOBBYROOM_HISTORY_M01_M33_BLOCKED:{label}:" + output[-2200:]
            )
    finally:
        runner_path.unlink(missing_ok=True)


def enforce_history_machine_proof(
    data: Dict[str, str],
    *,
    head: str,
    pr_base: str,
    campus_head: str,
    changed: List[str],
) -> None:
    bindings = (
        ("HISTORY_SOURCE", pr_base, data["HISTORY_SOURCE_REF"], data["HISTORY_SOURCE_BLOB_SHA"]),
        ("HISTORY_PROOF_RUNNER", pr_base, data["HISTORY_PROOF_RUNNER_REF"], data["HISTORY_PROOF_RUNNER_BLOB_SHA"]),
        ("PAUL_SOURCE", campus_head, data["PAUL_SOURCE_REF"], data["PAUL_SOURCE_BLOB_SHA"]),
    )
    for label, ref, path, expected in bindings:
        actual = _blob_at(ref, path, label)
        if actual != expected.lower():
            raise Blocked(
                f"HOBBYROOM_MACHINE_PROOF_SOURCE_STALE:{label}:EXPECTED={expected}:GOT={actual}"
            )

    history_ref = data["HISTORY_SOURCE_REF"]
    runner_ref = data["HISTORY_PROOF_RUNNER_REF"]
    expected_ids = [f"{i:02d}" for i in range(1, 34)]

    base_matrix = show(pr_base, history_ref)
    base_runner = show(pr_base, runner_ref)
    if _history_ids_from_matrix(base_matrix) != expected_ids:
        raise Blocked("HOBBYROOM_HISTORY_MATRIX_COVERAGE_INVALID:BASE")
    if _history_ids_from_runner(base_runner) != expected_ids:
        raise Blocked("HOBBYROOM_HISTORY_RUNNER_COVERAGE_INVALID:BASE")

    authority_changes = [p for p in changed if p in {history_ref, runner_ref}]
    other_changes = [p for p in changed if p not in {history_ref, runner_ref}]

    with tempfile.TemporaryDirectory(prefix="hobbyroom-history-proof-") as td:
        candidate = pathlib.Path(td) / "candidate"
        git("worktree", "add", "--detach", str(candidate), head)
        try:
            _run_history_runner(base_runner, candidate=candidate, label="TRUSTED_BASE")

            if authority_changes:
                if data["PLAN_PHASE"] != "HISTORY_AUTHORITY_MAINTENANCE":
                    raise Blocked("HOBBYROOM_HISTORY_AUTHORITY_CHANGE_BLOCKED")
                if other_changes:
                    raise Blocked(
                        "HOBBYROOM_HISTORY_MAINTENANCE_MIXED_WITH_PRODUCT_CHANGE:" +
                        ",".join(sorted(other_changes))
                    )
                candidate_matrix = (candidate / history_ref).read_text(encoding="utf-8")
                candidate_runner = (candidate / runner_ref).read_text(encoding="utf-8")
                if _history_ids_from_matrix(candidate_matrix) != expected_ids:
                    raise Blocked("HOBBYROOM_HISTORY_MATRIX_COVERAGE_INVALID:CANDIDATE")
                if _history_ids_from_runner(candidate_runner) != expected_ids:
                    raise Blocked("HOBBYROOM_HISTORY_RUNNER_COVERAGE_INVALID:CANDIDATE")
                _run_history_runner(
                    candidate_runner,
                    candidate=candidate,
                    label="CANDIDATE_AUTHORITY",
                )
        finally:
            git("worktree", "remove", "--force", str(candidate), check=False)
            git("worktree", "prune", check=False)

    print("HOBBYROOM_HISTORY_M01_M33_MACHINE_PROOF_PASS")


def evaluate_work_lock_pr(
    branch: str,
    head: str,
    pr_base: str,
    changed: List[str],
    locks: List[Tuple[str, Dict[str, str]]],
) -> str:
    relevant: List[Tuple[str, Dict[str, str]]] = []
    for path, data in locks:
        if any(_matches_scope(p, data["TECHNICAL_SCOPE_PREFIXES"]) for p in changed):
            relevant.append((path, data))
    if not relevant:
        return "HOBBYROOM_WORK_LOCK_NOT_APPLICABLE"
    if len(relevant) != 1:
        raise Blocked(
            "HOBBYROOM_MULTIPLE_WORK_LOCKS_BLOCKED:" +
            ",".join(sorted(path for path, _ in relevant))
        )

    hobbyroom, data = relevant[0]
    if data["STATUS"] != "FIX_ALLOWED_FOR_CODEX_TEST":
        raise Blocked(f"HOBBYROOM_WORK_LOCK_BLOCKED:{data['STATUS']}:{hobbyroom}")
    if data["INTEGRATION_ALLOWED"].casefold() != "true":
        raise Blocked(f"HOBBYROOM_INTEGRATION_NOT_ALLOWED:{hobbyroom}")
    if branch != data["CANDIDATE_BRANCH"]:
        raise Blocked(
            f"HOBBYROOM_CANDIDATE_BRANCH_MISMATCH:EXPECTED={data['CANDIDATE_BRANCH']}:GOT={branch}"
        )
    if not re.fullmatch(r"[0-9a-fA-F]{40}", data["CANDIDATE_HEAD_SHA"]):
        raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:CANDIDATE_HEAD_SHA")
    if head.lower() != data["CANDIDATE_HEAD_SHA"].lower():
        raise Blocked(
            f"HOBBYROOM_CANDIDATE_HEAD_MISMATCH:EXPECTED={data['CANDIDATE_HEAD_SHA']}:GOT={head}"
        )
    if pr_base.lower() != data["MAIN_SHA"].lower():
        raise Blocked(
            f"HOBBYROOM_MAIN_BASE_MISMATCH:EXPECTED={data['MAIN_SHA']}:GOT={pr_base}"
        )

    for key in (
        "CHECK_PAUL", "CHECK_HISTORY", "CHECK_LAST_GOOD", "CHECK_NEIGHBORS",
        "CHECK_REPEAT_CLASS", "CHECK_POS_NEG", "CHECK_INVARIANTS",
    ):
        if data[key] != "PASS":
            raise Blocked(f"HOBBYROOM_REQUIRED_CHECK_NOT_PASS:{key}:{data[key]}")

    allowed = data["ALLOWED_PATH_PREFIXES"]
    if not _scope_items(allowed):
        raise Blocked("HOBBYROOM_ALLOWED_PATHS_MISSING")
    relevant_changed = [
        p for p in changed
        if _matches_scope(p, data["TECHNICAL_SCOPE_PREFIXES"])
    ]
    bad = [p for p in relevant_changed if not _matches_scope(p, allowed)]
    if bad:
        raise Blocked("HOBBYROOM_ALLOWED_PATHS_BLOCKED:" + ",".join(sorted(bad)))
    return f"HOBBYROOM_WORK_LOCK_PR_PASS:{hobbyroom}"


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
Official campus ref `{OFFICIAL_CAMPUS_REF}` at `{campus_head}`.

ASSIGNMENT_ID:
`{data['ASSIGNMENT_ID']}`

PAUL_BRANCH:
`{data['PAUL_BRANCH']}`

TECHNICAL_BASE_SHA:
`{data['TECHNICAL_BASE_SHA']}`

WRITE_SCOPE:
`{data['WRITE_SCOPE']}`

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
    changed = changed_paths(pr_base, head)
    locks = work_locks(campus_head)
    work_result = evaluate_work_lock_pr(
        branch, head, pr_base, changed, locks
    )
    print(work_result)
    if work_result.startswith("HOBBYROOM_WORK_LOCK_PR_PASS:"):
        relevant = [
            data for _, data in locks
            if any(
                _matches_scope(p, data["TECHNICAL_SCOPE_PREFIXES"])
                for p in changed
            )
        ]
        if len(relevant) != 1:
            raise Blocked("HOBBYROOM_MACHINE_PROOF_LOCK_RESOLUTION_FAILED")
        enforce_history_machine_proof(
            relevant[0],
            head=head,
            pr_base=pr_base,
            campus_head=campus_head,
            changed=changed,
        )
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


def work_lock_selftest() -> None:
    base = "0" * 40
    head = "1" * 40
    valid = """HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 0000000000000000000000000000000000000000
ACTIVE_BLOCKER: X
PLAN_PHASE: E
CANDIDATE_BRANCH: hobbyroom/test
CANDIDATE_HEAD_SHA: 1111111111111111111111111111111111111111
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/;control/single-door-boundary/
ALLOWED_PATH_PREFIXES: control/startmaster0107/file.py
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PASS
CHECK_INVARIANTS: PASS
HISTORY_SOURCE_REF: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md
HISTORY_SOURCE_BLOB_SHA: 2222222222222222222222222222222222222222
HISTORY_PROOF_RUNNER_REF: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
HISTORY_PROOF_RUNNER_BLOB_SHA: 3333333333333333333333333333333333333333
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 4444444444444444444444444444444444444444
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1"""
    data = parse_work_lock(valid, "X/HOBBYRAUM.md")
    assert data is not None
    locks = [("X/HOBBYRAUM.md", data)]
    assert evaluate_work_lock_pr(
        "feature/x", head, base, ["README.md"], locks
    ) == "HOBBYROOM_WORK_LOCK_NOT_APPLICABLE"
    assert evaluate_work_lock_pr(
        "hobbyroom/test", head, base,
        ["control/startmaster0107/file.py"], locks
    ).startswith("HOBBYROOM_WORK_LOCK_PR_PASS:")
    for label, mutate, expected in (
        ("STATUS", ("STATUS", "FIX_FORBIDDEN"), "HOBBYROOM_WORK_LOCK_BLOCKED"),
        ("BRANCH", ("CANDIDATE_BRANCH", "hobbyroom/other"), "HOBBYROOM_CANDIDATE_BRANCH_MISMATCH"),
        ("HEAD", ("CANDIDATE_HEAD_SHA", "2" * 40), "HOBBYROOM_CANDIDATE_HEAD_MISMATCH"),
        ("POSNEG", ("CHECK_POS_NEG", "PENDING"), "HOBBYROOM_REQUIRED_CHECK_NOT_PASS"),
        ("INVARIANTS", ("CHECK_INVARIANTS", "PENDING"), "HOBBYROOM_REQUIRED_CHECK_NOT_PASS"),
        ("INTEGRATION", ("INTEGRATION_ALLOWED", "false"), "HOBBYROOM_INTEGRATION_NOT_ALLOWED"),
        ("PATH", ("ALLOWED_PATH_PREFIXES", "control/startmaster0107/other.py"), "HOBBYROOM_ALLOWED_PATHS_BLOCKED"),
    ):
        bad = dict(data)
        bad[mutate[0]] = mutate[1]
        try:
            evaluate_work_lock_pr(
                "hobbyroom/test", head, base,
                ["control/startmaster0107/file.py"],
                [("X/HOBBYRAUM.md", bad)],
            )
            raise AssertionError(label + " not blocked")
        except Blocked as exc:
            assert str(exc).startswith(expected), (label, str(exc))
    print("HOBBYROOM_WORK_LOCK_SELFTEST_PASS:9/9")


def selftest() -> None:
    work_lock_selftest()
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
