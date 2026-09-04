#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import fnmatch
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / ".runs"

class Blocked(RuntimeError):
    pass

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_task(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {"task_id","image","inputs","writable","command","tests","timeout_seconds"}
    if set(data) != required:
        raise Blocked("TASK_FIELDS_INVALID")
    if not data["task_id"] or "/" in data["task_id"] or ".." in data["task_id"]:
        raise Blocked("TASK_ID_INVALID")
    if not isinstance(data["inputs"], list) or not data["inputs"]:
        raise Blocked("INPUTS_REQUIRED")
    if not isinstance(data["writable"], list):
        raise Blocked("WRITABLE_INVALID")
    if not isinstance(data["tests"], list):
        raise Blocked("TESTS_INVALID")
    if not isinstance(data["command"], str) or not data["command"].strip():
        raise Blocked("COMMAND_REQUIRED")
    return data

def safe_rel(value: str) -> Path:
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or not str(p):
        raise Blocked("DEST_INVALID:" + value)
    return p

def assert_safe_source(src: Path) -> None:
    if src.is_symlink():
        raise Blocked("SYMLINK_INPUT_FORBIDDEN:" + str(src))
    if ".git" in src.parts:
        raise Blocked("GIT_METADATA_FORBIDDEN:" + str(src))
    if src.is_dir():
        for p in src.rglob("*"):
            if ".git" in p.parts:
                raise Blocked("GIT_METADATA_FORBIDDEN:" + str(p))
            if p.is_symlink():
                raise Blocked("SYMLINK_INPUT_FORBIDDEN:" + str(p))

def prepare(task: dict, task_file: Path) -> Path:
    run = RUNS / task["task_id"]
    if run.exists():
        shutil.rmtree(run)
    workspace = run / "workspace"
    baseline = run / "baseline"
    out = run / "out"
    workspace.mkdir(parents=True)
    baseline.mkdir(parents=True)
    out.mkdir(parents=True)

    base = task_file.parent.resolve()
    for row in task["inputs"]:
        if not isinstance(row, dict) or set(row) != {"src","dest"}:
            raise Blocked("INPUT_ROW_INVALID")
        src = Path(row["src"])
        if not src.is_absolute():
            src = (base / src).resolve()
        dest_rel = safe_rel(str(row["dest"]))
        if not src.exists():
            raise Blocked("INPUT_MISSING:" + str(src))
        assert_safe_source(src)
        if ".git" in dest_rel.parts:
            raise Blocked("GIT_METADATA_DEST_FORBIDDEN:" + str(dest_rel))
        dest = workspace / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)

    shutil.copytree(workspace, baseline, dirs_exist_ok=True)
    (run / "TASK.json").write_text(json.dumps(task, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return run

def engine() -> str:
    for name in ("docker","podman"):
        if shutil.which(name):
            return name
    raise Blocked("DOCKER_OR_PODMAN_REQUIRED")

def allowed(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)

def snapshot(root: Path) -> dict[str, str]:
    result = {}
    if not root.exists():
        return result
    for p in sorted(root.rglob("*")):
        if p.is_file():
            result[p.relative_to(root).as_posix()] = sha256(p)
    return result

def run_in_container(task: dict, run: Path, command: str) -> subprocess.CompletedProcess:
    eng = engine()
    workspace = (run / "workspace").resolve()
    cmd = [
        eng, "run", "--rm", "--pull=never",
        "--network", "none",
        "--read-only",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--pids-limit", "256",
        "--user", f"{os.getuid()}:{os.getgid()}",
        "--env", "HOME=/tmp",
        "--env", "TMPDIR=/tmp",
        "--env", "XDG_CACHE_HOME=/tmp/.cache",
        "--env", "PYTHONDONTWRITEBYTECODE=1",
        "--tmpfs", "/tmp:rw,nosuid,nodev,size=256m",
        "-v", f"{workspace}:/workspace:rw",
        "-w", "/workspace",
        task["image"],
        "/bin/sh", "-lc", command
    ]
    return subprocess.run(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=int(task["timeout_seconds"]),
    )

def diff_and_export(task: dict, run: Path) -> dict:
    before = snapshot(run / "baseline")
    after = snapshot(run / "workspace")
    paths = sorted(set(before) | set(after))
    changed = [p for p in paths if before.get(p) != after.get(p)]
    forbidden = [p for p in changed if not allowed(p, task["writable"])]
    if forbidden:
        raise Blocked("WRITE_OUTSIDE_ALLOWLIST:" + ",".join(forbidden))

    patch_parts = []
    out = run / "out"
    for rel in changed:
        src = run / "workspace" / rel
        old = run / "baseline" / rel
        if src.exists():
            dst = out / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        try:
            old_text = old.read_text(encoding="utf-8").splitlines(True) if old.exists() else []
            new_text = src.read_text(encoding="utf-8").splitlines(True) if src.exists() else []
            patch_parts.extend(difflib.unified_diff(old_text, new_text, fromfile="a/"+rel, tofile="b/"+rel))
        except UnicodeDecodeError:
            patch_parts.append(f"BINARY_CHANGED {rel}\n")

    patch = "".join(patch_parts)
    (run / "PATCH.diff").write_text(patch, encoding="utf-8")
    result = {"status":"PASS","changed":changed,"forbidden":[],"patch_ref":str(run / "PATCH.diff"),"out_ref":str(out)}
    (run / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return result

def execute(task: dict, task_file: Path) -> dict:
    run = prepare(task, task_file)

    work = run_in_container(task, run, task["command"])
    (run / "COMMAND.stdout.txt").write_text(work.stdout or "", encoding="utf-8")
    (run / "COMMAND.stderr.txt").write_text(work.stderr or "", encoding="utf-8")
    if work.returncode != 0:
        detail = ((work.stderr or "") + "\n" + (work.stdout or "")).strip().replace("\n", " ")[:600]
        raise Blocked("TASK_COMMAND_FAILED:" + str(work.returncode) + ":" + detail)

    for idx, test in enumerate(task["tests"], start=1):
        if not isinstance(test, str) or not test.strip():
            raise Blocked("TEST_INVALID:" + str(idx))
        proc = run_in_container(task, run, test)
        (run / f"TEST_{idx}.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
        (run / f"TEST_{idx}.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
        if proc.returncode != 0:
            detail = ((proc.stderr or "") + "\n" + (proc.stdout or "")).strip().replace("\n", " ")[:600]
            raise Blocked("TEST_FAILED:" + str(idx) + ":" + str(proc.returncode) + ":" + detail)

    return diff_and_export(task, run)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    args = ap.parse_args()
    try:
        task_file = Path(args.task).resolve()
        task = load_task(task_file)
        result = execute(task, task_file)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (Blocked, OSError, ValueError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        print(json.dumps({"status":"BLOCKED","reason":str(exc)}, ensure_ascii=False, indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
