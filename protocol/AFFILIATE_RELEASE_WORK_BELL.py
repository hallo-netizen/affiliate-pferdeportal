#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

WORKSTREAM = "AFFILIATE_ZENTRALE"
BRANCH = "affiliate-release-current"
CODEX_EPHEMERAL_BRANCH = "work"
EXPECTED_MANIFEST_SHA256 = "5a7409487432b460921312380b975e40328615298bdbc5f5485e13ed507d933c"
EXPECTED_FILE_COUNT = 26
CANDIDATE_NAME = "affiliate-zentrale_v6.64.2_LIVE_CANDIDATE_26FILE.zip"
RELEASE_JSON = Path("control/release-governance/CURRENT_RELEASE.json")
MANIFEST = Path("release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt")
SOURCE_ROOT = Path("release/affiliate-zentrale/current")
PLUGIN_ROOT = SOURCE_ROOT / "affiliate-portal-router"
WORK_ROOT = Path(".affiliate-work-bell")
CANDIDATE = WORK_ROOT / CANDIDATE_NAME
STATE_FILE = WORK_ROOT / "state.json"

FORBIDDEN_RUNTIME_PREFIXES = (
    "control/cloud-entry-gate/",
    "control/startmaster",
    ".pferde-capsule/",
    ".pferde-quarantine/",
)


def die(code: str, detail: str, exit_code: int = 2) -> None:
    print("WORK_BELL: BLOCKED")
    print(f"CODE: {code}")
    print(f"DETAIL: {detail}")
    raise SystemExit(exit_code)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_checked(cmd: list[str]) -> str:
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if p.returncode != 0:
        die("BOUND_COMMAND_FAILED", f"{' '.join(cmd)}\n{p.stdout.strip()}")
    return p.stdout.strip()


def ensure_repo_root() -> None:
    if not RELEASE_JSON.is_file() or not MANIFEST.is_file() or not PLUGIN_ROOT.is_dir():
        die("WRONG_WORKSPACE", "Affiliate release authority files are missing; run from repository root.")


def ensure_no_startmaster_navigation() -> None:
    argv = " ".join(sys.argv).lower()
    for prefix in FORBIDDEN_RUNTIME_PREFIXES:
        if prefix.lower() in argv:
            die("STARTMASTER_FORBIDDEN", f"Affiliate work may not navigate through {prefix}")


def load_release() -> dict:
    try:
        data = json.loads(RELEASE_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        die("CURRENT_RELEASE_INVALID", repr(exc))
    if data.get("workstream") != WORKSTREAM:
        die("WRONG_WORKSTREAM", f"expected {WORKSTREAM}, got {data.get('workstream')}")
    lock = data.get("user_scope_lock") or {}
    if lock.get("status") != "ACTIVE" or lock.get("decision") != "MANUAL_SINGLE_UPLOAD_MULTI_PROVIDER_IMPORT":
        die("USER_SCOPE_LOCK_MISMATCH", "Manual single-upload multi-provider import is not the active scope lock.")
    src = data.get("source_authority") or {}
    if src.get("manifest_sha256") != EXPECTED_MANIFEST_SHA256 or src.get("source_file_count") != EXPECTED_FILE_COUNT:
        die("SOURCE_AUTHORITY_MISMATCH", f"expected manifest {EXPECTED_MANIFEST_SHA256} / {EXPECTED_FILE_COUNT} files")
    return data


def ensure_branch() -> str:
    branch = run_checked(["git", "branch", "--show-current"]).strip()
    if branch == BRANCH:
        return branch
    if branch == CODEX_EPHEMERAL_BRANCH:
        # Codex Cloud executes tasks on its own ephemeral local branch named "work".
        # The branch name is therefore not release authority. Safety is enforced below
        # by CURRENT_RELEASE binding + exact manifest hash + exact 26-file byte identity.
        return branch
    die("WRONG_BRANCH", f"expected {BRANCH} or Codex ephemeral {CODEX_EPHEMERAL_BRANCH}, got {branch or '<detached>'}")
    return branch


def run_release_guards() -> tuple[str, str]:
    gov = run_checked(["python3", "control/release-governance/release_guard.py", "governance-check"])
    # release_guard's --branch value is the bound release-policy identity, not the
    # ephemeral local Codex checkout name.
    start = run_checked(["python3", "control/release-governance/release_guard.py", "start", "--branch", BRANCH])
    return gov, start


def parse_manifest() -> list[tuple[str, str]]:
    actual_manifest_sha = sha256_file(MANIFEST)
    if actual_manifest_sha != EXPECTED_MANIFEST_SHA256:
        die("MANIFEST_SHA_MISMATCH", f"expected {EXPECTED_MANIFEST_SHA256}, got {actual_manifest_sha}")
    rows: list[tuple[str, str]] = []
    for n, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or len(parts[0]) != 64:
            die("MANIFEST_ROW_INVALID", f"line {n}: {raw!r}")
        expected, rel = parts[0].lower(), parts[1].strip()
        p = PurePosixPath(rel)
        if p.is_absolute() or ".." in p.parts or not rel.startswith("affiliate-portal-router/"):
            die("MANIFEST_PATH_INVALID", rel)
        rows.append((expected, rel))
    if len(rows) != EXPECTED_FILE_COUNT:
        die("MANIFEST_FILE_COUNT_MISMATCH", f"expected {EXPECTED_FILE_COUNT}, got {len(rows)}")
    if len({rel for _, rel in rows}) != len(rows):
        die("MANIFEST_DUPLICATE_PATH", "Manifest contains duplicate paths")
    return rows


def verify_source(rows: list[tuple[str, str]]) -> None:
    expected_paths = {rel for _, rel in rows}
    actual_paths = {
        p.relative_to(SOURCE_ROOT).as_posix()
        for p in PLUGIN_ROOT.rglob("*")
        if p.is_file()
    }
    if actual_paths != expected_paths:
        missing = sorted(expected_paths - actual_paths)
        extra = sorted(actual_paths - expected_paths)
        die("SOURCE_FILESET_MISMATCH", f"missing={missing} extra={extra}")
    for expected, rel in rows:
        path = SOURCE_ROOT / rel
        actual = sha256_file(path)
        if actual != expected:
            die("SOURCE_HASH_MISMATCH", f"{rel}: expected {expected}, got {actual}")


def deterministic_zip(rows: list[tuple[str, str]]) -> None:
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    tmp = CANDIDATE.with_suffix(".tmp.zip")
    if tmp.exists():
        tmp.unlink()
    if CANDIDATE.exists():
        CANDIDATE.unlink()
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for _, rel in sorted(rows, key=lambda x: x[1]):
            src = SOURCE_ROOT / rel
            data = src.read_bytes()
            zi = zipfile.ZipInfo(rel)
            zi.date_time = (2026, 9, 2, 0, 0, 0)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o100644 << 16
            zf.writestr(zi, data)
    os.replace(tmp, CANDIDATE)


def verify_fresh_unpack(rows: list[tuple[str, str]]) -> None:
    expected = {rel: digest for digest, rel in rows}
    with tempfile.TemporaryDirectory(prefix="affiliate-live-candidate-") as td:
        root = Path(td)
        with zipfile.ZipFile(CANDIDATE, "r") as zf:
            names = [n for n in zf.namelist() if not n.endswith("/")]
            if len(names) != EXPECTED_FILE_COUNT or set(names) != set(expected):
                die("ZIP_FILESET_MISMATCH", f"expected 26 exact manifest files, got {len(names)}")
            for n in names:
                p = PurePosixPath(n)
                if p.is_absolute() or ".." in p.parts:
                    die("ZIP_PATH_INVALID", n)
            zf.extractall(root)
        for rel, digest in expected.items():
            actual = sha256_file(root / rel)
            if actual != digest:
                die("FRESH_UNPACK_HASH_MISMATCH", f"{rel}: expected {digest}, got {actual}")


def write_state(status: str, zip_sha: str | None = None, local_branch: str | None = None) -> None:
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    payload = {
        "contract": "AFFILIATE_RELEASE_WORK_BELL_V2_CODEX_EPHEMERAL_BRANCH_SAFE",
        "workstream": WORKSTREAM,
        "release_branch_identity": BRANCH,
        "local_execution_branch": local_branch,
        "manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "source_file_count": EXPECTED_FILE_COUNT,
        "status": status,
        "next_allowed_action": "WORDPRESS_INSTALL_LIVE_CANDIDATE" if status == "LIVE_CANDIDATE_READY" else "BUILD_LIVE_CANDIDATE",
        "forbidden": [
            "STARTMASTER_NAVIGATION",
            "CLOUD_ENTRY_GATE",
            "NEW_ARCHITECTURE",
            "DS24_AUTOMATIC_DISCOVERY",
            "REPEAT_HASH_IDENTICAL_PASS_GATES",
            "HISTORICAL_ZIP_RECONSTRUCTION",
        ],
        "candidate": str(CANDIDATE) if zip_sha else None,
        "candidate_sha256": zip_sha,
    }
    STATE_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def current() -> None:
    ensure_repo_root()
    ensure_no_startmaster_navigation()
    release = load_release()
    local_branch = ensure_branch()
    status = "BUILD_LIVE_CANDIDATE"
    if CANDIDATE.is_file() and STATE_FILE.is_file():
        try:
            st = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            if st.get("status") == "LIVE_CANDIDATE_READY" and st.get("candidate_sha256") == sha256_file(CANDIDATE):
                status = "WORDPRESS_INSTALL_LIVE_CANDIDATE"
        except Exception:
            pass
    print("WORK_BELL: PASS")
    print(f"WORKSTREAM: {WORKSTREAM}")
    print(f"LOCAL_EXECUTION_BRANCH: {local_branch}")
    print(f"RELEASE_BRANCH_IDENTITY: {BRANCH}")
    print(f"AUTHORIZED_NEXT_ACTION: {status}")
    print(f"RELEASE_STATE: {(release.get('execution_state') or {}).get('state')}")


def run_build() -> None:
    ensure_repo_root()
    ensure_no_startmaster_navigation()
    load_release()
    local_branch = ensure_branch()
    write_state("BUILD_LIVE_CANDIDATE", local_branch=local_branch)
    run_release_guards()
    rows = parse_manifest()
    verify_source(rows)
    deterministic_zip(rows)
    verify_fresh_unpack(rows)
    zip_sha = sha256_file(CANDIDATE)
    write_state("LIVE_CANDIDATE_READY", zip_sha, local_branch)
    print("WORK_BELL: PASS")
    print("GOVERNANCE_CHECK: PASS")
    print("START_CHECK: PASS")
    print(f"LOCAL_EXECUTION_BRANCH: {local_branch}")
    print(f"RELEASE_BRANCH_IDENTITY: {BRANCH}")
    print(f"SOURCE_MANIFEST_SHA256: {EXPECTED_MANIFEST_SHA256}")
    print(f"SOURCE_FILE_COUNT: {EXPECTED_FILE_COUNT}")
    print("SOURCE_BYTE_IDENTITY: PASS")
    print(f"FRESH_UNPACK_FILE_COUNT: {EXPECTED_FILE_COUNT}")
    print("FRESH_UNPACK_BYTE_IDENTITY: PASS")
    print(f"LIVE_CANDIDATE_ZIP_SHA256: {zip_sha}")
    print(f"LIVE_CANDIDATE_PATH: {CANDIDATE}")
    print("USER_ACTION_REQUIRED: WordPress -> Plugins -> Installieren -> Plugin hochladen; danach Affiliate-Zentrale -> Anbieter & APIs -> vorhandene DS24-CSV importieren.")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "current"
    if cmd == "current":
        current()
    elif cmd in {"run", "build"}:
        run_build()
    else:
        die("UNKNOWN_COMMAND", "Allowed commands: current, run")


if __name__ == "__main__":
    main()
