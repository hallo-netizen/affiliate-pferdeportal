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
        "RECOVERY_BASE_SHA", "HISTORY_EXPECTED_FAIL",
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
    if not re.fullmatch(r"[0-9a-fA-F]{40}", data["RECOVERY_BASE_SHA"]):
        raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:RECOVERY_BASE_SHA")
    if data["HISTORY_EXPECTED_FAIL"] != "NONE" and not re.fullmatch(
        r"M[0-9]{2,}", data["HISTORY_EXPECTED_FAIL"]
    ):
        raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:HISTORY_EXPECTED_FAIL")
    if data["PLAN_PHASE"] == "HISTORY_AUTHORITY_MAINTENANCE":
        if data["HISTORY_EXPECTED_FAIL"] == "NONE":
            raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:HISTORY_EXPECTED_FAIL_REQUIRED")
    elif data["HISTORY_EXPECTED_FAIL"] != "NONE":
        raise Blocked("HOBBYROOM_WORK_LOCK_INVALID:HISTORY_EXPECTED_FAIL_OUTSIDE_MAINTENANCE")
    if data["STATUS"] == "FIX_ALLOWED_FOR_CODEX_TEST":
        proof_required = {
            "HISTORY_SOURCE_REF", "HISTORY_SOURCE_BLOB_SHA",
            "HISTORY_PROOF_RUNNER_REF", "HISTORY_PROOF_RUNNER_BLOB_SHA",
            "PAUL_SOURCE_REF", "PAUL_SOURCE_BLOB_SHA",
            "ERROR_SOURCE_REF", "ERROR_SOURCE_BLOB_SHA",
            "CURRENT_STATE_REF", "CURRENT_STATE_BLOB_SHA",
            "DECISION_SOURCE_REF", "DECISION_SOURCE_BLOB_SHA",
            "STANDARD_SOURCE_REF", "STANDARD_SOURCE_BLOB_SHA",
            "PROTOCOL_SOURCE_REF", "PROTOCOL_SOURCE_BLOB_SHA",
        }
        proof_missing = sorted(proof_required.difference(data))
        if proof_missing:
            raise Blocked(
                "HOBBYROOM_WORK_LOCK_INVALID:MACHINE_PROOF_MISSING:" +
                ",".join(proof_missing)
            )
        for key in (
            "HISTORY_SOURCE_REF", "HISTORY_PROOF_RUNNER_REF", "PAUL_SOURCE_REF",
            "ERROR_SOURCE_REF", "CURRENT_STATE_REF", "DECISION_SOURCE_REF",
            "STANDARD_SOURCE_REF", "PROTOCOL_SOURCE_REF",
        ):
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
            "ERROR_SOURCE_BLOB_SHA",
            "CURRENT_STATE_BLOB_SHA",
            "DECISION_SOURCE_BLOB_SHA",
            "STANDARD_SOURCE_BLOB_SHA",
            "PROTOCOL_SOURCE_BLOB_SHA",
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
    return sorted(set(re.findall(r"(?m)^M(\d{2,})\s+[–-]", text)))


def _history_ids_from_runner(text: str) -> List[str]:
    pairs = re.findall(r'\("M(\d{2,})",\s*m\d+\)', text)
    return sorted(set(pairs))


def _error_ids_from_authoritative(text: str) -> List[str]:
    return sorted(set(re.findall(r"(?m)^\|\s*M(\d{2,})\s*\|", text)))


def _normalized_history_ids(ids: List[str], label: str) -> List[str]:
    if not ids:
        raise Blocked("HOBBYROOM_HISTORY_COVERAGE_EMPTY:" + label)
    nums = sorted(set(int(x) for x in ids))
    if nums[-1] < 33:
        raise Blocked("HOBBYROOM_HISTORY_BASELINE_M01_M33_MISSING:" + label)
    expected = list(range(1, nums[-1] + 1))
    if nums != expected:
        raise Blocked("HOBBYROOM_HISTORY_COVERAGE_NOT_CONTIGUOUS:" + label)
    return [f"{n:02d}" if n < 100 else str(n) for n in nums]


def _require_tokens(text: str, tokens: Tuple[str, ...], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        raise Blocked(
            "HOBBYROOM_EVIDENCE_SEMANTIC_MISSING:" + label + ":" +
            ",".join(missing)
        )


def _validate_bound_evidence_texts(
    data: Dict[str, str],
    *,
    history_text: str,
    runner_text: str,
    paul_text: str,
    error_text: str,
    current_state_text: str,
    decision_text: str,
    standard_text: str,
    protocol_text: str,
) -> Tuple[List[str], List[str]]:
    matrix_ids = _normalized_history_ids(
        _history_ids_from_matrix(history_text), "MATRIX"
    )
    runner_ids = _normalized_history_ids(
        _history_ids_from_runner(runner_text), "RUNNER"
    )
    error_ids = _normalized_history_ids(
        _error_ids_from_authoritative(error_text), "ERROR_SOURCE"
    )
    if runner_ids != matrix_ids:
        raise Blocked("HOBBYROOM_HISTORY_RUNNER_MATRIX_MISMATCH")

    maintenance = data["PLAN_PHASE"] == "HISTORY_AUTHORITY_MAINTENANCE"
    if maintenance:
        if not set(matrix_ids).issubset(set(error_ids)):
            raise Blocked("HOBBYROOM_HISTORY_BASE_NOT_SUBSET_OF_ERROR_SOURCE")
    elif error_ids != matrix_ids:
        raise Blocked("HOBBYROOM_ERROR_SOURCE_HISTORY_MISMATCH")

    blocker = data["ACTIVE_BLOCKER"]
    if blocker not in error_text:
        raise Blocked("HOBBYROOM_ACTIVE_BLOCKER_NOT_IN_AUTHORITATIVE_ERROR_SOURCE")
    if blocker not in current_state_text:
        raise Blocked("HOBBYROOM_ACTIVE_BLOCKER_NOT_IN_CURRENT_STATE")
    if data["MAIN_SHA"] not in current_state_text:
        raise Blocked("HOBBYROOM_MAIN_SHA_NOT_IN_CURRENT_STATE")
    if data["RECOVERY_BASE_SHA"] not in current_state_text:
        raise Blocked("HOBBYROOM_LAST_GOOD_NOT_IN_CURRENT_STATE")
    if blocker not in protocol_text:
        raise Blocked("HOBBYROOM_ACTIVE_BLOCKER_NOT_IN_PROTOCOL")
    if data["MAIN_SHA"] not in protocol_text:
        raise Blocked("HOBBYROOM_MAIN_SHA_NOT_IN_PROTOCOL")
    if data["RECOVERY_BASE_SHA"] not in protocol_text:
        raise Blocked("HOBBYROOM_LAST_GOOD_NOT_IN_PROTOCOL")
    _require_tokens(
        protocol_text,
        (
            "Realtest",
            "PASS",
            "FAIL",
            "Kein Publish",
        ),
        "PROTOCOL",
    )

    _require_tokens(
        paul_text,
        (
            "Kein 41-Punkte-Sammelfix.",
            "Historische Fehlerquelle gegenprüfen.",
            "Bestehender Regressionstest danach.",
            "Echter 7/7-Lauf bleibt Produktionsbeweis.",
            "Unerfüllbarer technischer Vertrag",
            "Artefaktzustands-Parität",
            "Hash-Semantik",
            "Pre-/Post-Transformation-Gate-Reihenfolge",
        ),
        "PAUL",
    )
    _require_tokens(
        decision_text,
        (
            "TEXT-TECH-20260907-CORRIDOR",
            "TEXT-TECH-20260908-FROZEN-RECOVERY",
            "TEXT-TECH-20260908-HISTORY-MACHINE-PROOF",
            "Kein zweites Reparaturkonzept",
            "kein Fix auf einen fehlgeschlagenen Fix",
        ),
        "DECISIONS",
    )
    _require_tokens(
        standard_text,
        (
            "Verbindlicher Pre-Fix-Ablauf für technische Hobbyräume",
            "gesamte bekannte Fehlerhistorie prüfen",
            "letzten funktionierenden Stand vergleichen",
            "unmittelbare Vor- und Nachstufe",
            "Wiederholungsfehlerklasse prüfen",
            "Positiv- und Negativtest des Kandidaten",
            "keine Reparatur im laufenden Test",
        ),
        "HOBBYROOM_STANDARD",
    )
    return matrix_ids, error_ids


def _run_history_runner(
    runner_text: str,
    *,
    candidate: pathlib.Path,
    label: str,
    expected_fail: str | None = None,
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
        if expected_fail is None:
            if p.returncode != 0 or '"status": "GESAMT PASS"' not in output:
                raise Blocked(
                    f"HOBBYROOM_HISTORY_FULL_PASS_BLOCKED:{label}:" + output[-2200:]
                )
            return

        if p.returncode == 0:
            raise Blocked(
                f"HOBBYROOM_HISTORY_REPRODUCTION_DID_NOT_FAIL:{expected_fail}:" +
                output[-2200:]
            )
        required = (
            '"status": "REGRESSION_FAIL"',
            '"first_fail": "' + expected_fail + '"',
        )
        if any(token not in output for token in required):
            raise Blocked(
                f"HOBBYROOM_HISTORY_WRONG_REPRODUCTION_FAIL:EXPECTED={expected_fail}:" +
                output[-2200:]
            )
        print("HOBBYROOM_HISTORY_REPRODUCTION_PASS:" + expected_fail)
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
        ("ERROR_SOURCE", campus_head, data["ERROR_SOURCE_REF"], data["ERROR_SOURCE_BLOB_SHA"]),
        ("CURRENT_STATE", campus_head, data["CURRENT_STATE_REF"], data["CURRENT_STATE_BLOB_SHA"]),
        ("DECISION_SOURCE", campus_head, data["DECISION_SOURCE_REF"], data["DECISION_SOURCE_BLOB_SHA"]),
        ("STANDARD_SOURCE", campus_head, data["STANDARD_SOURCE_REF"], data["STANDARD_SOURCE_BLOB_SHA"]),
        ("PROTOCOL_SOURCE", campus_head, data["PROTOCOL_SOURCE_REF"], data["PROTOCOL_SOURCE_BLOB_SHA"]),
    )
    for label, ref, path, expected in bindings:
        actual = _blob_at(ref, path, label)
        if actual != expected.lower():
            raise Blocked(
                f"HOBBYROOM_MACHINE_PROOF_SOURCE_STALE:{label}:EXPECTED={expected}:GOT={actual}"
            )

    history_ref = data["HISTORY_SOURCE_REF"]
    runner_ref = data["HISTORY_PROOF_RUNNER_REF"]
    base_matrix = show(pr_base, history_ref)
    base_runner = show(pr_base, runner_ref)
    paul_text = show(campus_head, data["PAUL_SOURCE_REF"])
    error_text = show(campus_head, data["ERROR_SOURCE_REF"])
    current_state_text = show(campus_head, data["CURRENT_STATE_REF"])
    decision_text = show(campus_head, data["DECISION_SOURCE_REF"])
    standard_text = show(campus_head, data["STANDARD_SOURCE_REF"])
    protocol_text = show(campus_head, data["PROTOCOL_SOURCE_REF"])
    base_ids, error_ids = _validate_bound_evidence_texts(
        data,
        history_text=base_matrix,
        runner_text=base_runner,
        paul_text=paul_text,
        error_text=error_text,
        current_state_text=current_state_text,
        decision_text=decision_text,
        standard_text=standard_text,
        protocol_text=protocol_text,
    )

    authority_changes = [p for p in changed if p in {history_ref, runner_ref}]
    other_changes = [p for p in changed if p not in {history_ref, runner_ref}]

    with tempfile.TemporaryDirectory(prefix="hobbyroom-history-proof-") as td:
        candidate = pathlib.Path(td) / "candidate"
        git("worktree", "add", "--detach", str(candidate), head)
        try:
            if authority_changes:
                if data["PLAN_PHASE"] != "HISTORY_AUTHORITY_MAINTENANCE":
                    raise Blocked("HOBBYROOM_HISTORY_AUTHORITY_CHANGE_BLOCKED")
                if other_changes:
                    raise Blocked(
                        "HOBBYROOM_HISTORY_MAINTENANCE_MIXED_WITH_PRODUCT_CHANGE:" +
                        ",".join(sorted(other_changes))
                    )
                _run_history_runner(
                    base_runner, candidate=candidate, label="TRUSTED_BASE"
                )
                candidate_matrix = (candidate / history_ref).read_text(encoding="utf-8")
                candidate_runner = (candidate / runner_ref).read_text(encoding="utf-8")
                candidate_ids = _normalized_history_ids(
                    _history_ids_from_matrix(candidate_matrix), "CANDIDATE_MATRIX"
                )
                candidate_runner_ids = _normalized_history_ids(
                    _history_ids_from_runner(candidate_runner), "CANDIDATE_RUNNER"
                )
                if candidate_runner_ids != candidate_ids:
                    raise Blocked("HOBBYROOM_HISTORY_CANDIDATE_RUNNER_MATRIX_MISMATCH")
                if candidate_ids != error_ids:
                    raise Blocked("HOBBYROOM_HISTORY_CANDIDATE_ERROR_SOURCE_MISMATCH")
                if not set(base_ids).issubset(set(candidate_ids)):
                    raise Blocked("HOBBYROOM_HISTORY_CANDIDATE_REMOVED_OLD_ERROR")
                _run_history_runner(
                    candidate_runner,
                    candidate=candidate,
                    label="CANDIDATE_AUTHORITY",
                    expected_fail=data["HISTORY_EXPECTED_FAIL"],
                )
            else:
                if data["PLAN_PHASE"] == "HISTORY_AUTHORITY_MAINTENANCE":
                    raise Blocked("HOBBYROOM_HISTORY_MAINTENANCE_WITHOUT_AUTHORITY_CHANGE")
                _run_history_runner(
                    base_runner, candidate=candidate, label="TRUSTED_BASE"
                )
        finally:
            git("worktree", "remove", "--force", str(candidate), check=False)
            git("worktree", "prune", check=False)

    print("HOBBYROOM_HISTORY_MACHINE_PROOF_PASS")


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
    # Self-test the gate's invariant semantics on every server-side PR check.
    work_lock_selftest()
    evidence_semantic_selftest()
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
RECOVERY_BASE_SHA: 7777777777777777777777777777777777777777
HISTORY_EXPECTED_FAIL: NONE
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
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md
ERROR_SOURCE_BLOB_SHA: 5555555555555555555555555555555555555555
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 6666666666666666666666666666666666666666
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 8888888888888888888888888888888888888888
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: 9999999999999999999999999999999999999999
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
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
    notes = dict(data)
    notes["CHECK_HISTORY"] = "PENDING"
    notes["CHECK_POS_NEG"] = "PENDING"
    assert evaluate_work_lock_pr(
        "hobbyroom/test", head, base,
        ["control/startmaster0107/file.py"], [("X/HOBBYRAUM.md", notes)]
    ).startswith("HOBBYROOM_WORK_LOCK_PR_PASS:")
    print("HOBBYROOM_WORK_LOCK_SELFTEST_PASS:8/8")


def evidence_semantic_selftest() -> None:
    ids = [f"{i:02d}" for i in range(1, 34)]
    history = "\n".join("M" + i + " – test" for i in ids)
    runner = "CASES=[" + ",".join('("M' + i + '",m' + i + ')' for i in ids) + "]"
    error = "\n".join("| M" + i + " | test |" for i in ids) + "\nBLOCK_X"
    current = (
        "AKTUELLER REALTEST\nBLOCK_X\n" + "0" * 40 + "\n" + "7" * 40
    )
    paul = "\n".join((
        "Kein 41-Punkte-Sammelfix.",
        "Historische Fehlerquelle gegenprüfen.",
        "Bestehender Regressionstest danach.",
        "Echter 7/7-Lauf bleibt Produktionsbeweis.",
        "Unerfüllbarer technischer Vertrag",
        "Artefaktzustands-Parität",
        "Hash-Semantik",
        "Pre-/Post-Transformation-Gate-Reihenfolge",
    ))
    decisions = "\n".join((
        "TEXT-TECH-20260907-CORRIDOR",
        "TEXT-TECH-20260908-FROZEN-RECOVERY",
        "TEXT-TECH-20260908-HISTORY-MACHINE-PROOF",
        "Kein zweites Reparaturkonzept",
        "kein Fix auf einen fehlgeschlagenen Fix",
    ))
    standard = "\n".join((
        "Verbindlicher Pre-Fix-Ablauf für technische Hobbyräume",
        "gesamte bekannte Fehlerhistorie prüfen",
        "letzten funktionierenden Stand vergleichen",
        "unmittelbare Vor- und Nachstufe",
        "Wiederholungsfehlerklasse prüfen",
        "Positiv- und Negativtest des Kandidaten",
        "keine Reparatur im laufenden Test",
    ))
    protocol = (
        "Realtest PASS FAIL Kein Publish\nBLOCK_X\n" +
        "0" * 40 + "\n" + "7" * 40
    )
    data = {
        "ACTIVE_BLOCKER": "BLOCK_X",
        "MAIN_SHA": "0" * 40,
        "RECOVERY_BASE_SHA": "7" * 40,
        "PLAN_PHASE": "PRODUCT_FIX",
    }
    def check(**overrides):
        payload = {
            "history_text": history,
            "runner_text": runner,
            "paul_text": paul,
            "error_text": error,
            "current_state_text": current,
            "decision_text": decisions,
            "standard_text": standard,
            "protocol_text": protocol,
        }
        payload.update(overrides)
        return _validate_bound_evidence_texts(data, **payload)

    check()
    negatives = (
        ("M33_MATRIX", {"history_text": history.replace("M33 – test", "")}),
        ("M33_RUNNER", {"runner_text": runner.replace('("M33",m33)', "")}),
        ("M33_ERROR", {"error_text": error.replace("| M33 | test |", "")}),
        ("GAP", {"history_text": history.replace("M17 – test", "")}),
        ("PAUL", {"paul_text": paul.replace("Artefaktzustands-Parität", "")}),
        ("DECISIONS", {"decision_text": decisions.replace("kein Fix auf einen fehlgeschlagenen Fix", "")}),
        ("STANDARD", {"standard_text": standard.replace("letzten funktionierenden Stand vergleichen", "")}),
        ("LAST_GOOD", {"current_state_text": current.replace("7" * 40, "")}),
        ("PROTOCOL_MAIN", {"protocol_text": protocol.replace("0" * 40, "")}),
    )
    for label, override in negatives:
        try:
            check(**override)
            raise AssertionError(label + " not blocked")
        except Blocked:
            pass

    grown_history = history + "\nM34 – future"
    grown_runner = runner[:-1] + ',("M34",m34)]'
    grown_error = error + "\n| M34 | future |"
    check(
        history_text=grown_history,
        runner_text=grown_runner,
        error_text=grown_error,
    )
    print("HOBBYROOM_EVIDENCE_SELFTEST_PASS:10/10")


def selftest() -> None:
    work_lock_selftest()
    evidence_semantic_selftest()
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
