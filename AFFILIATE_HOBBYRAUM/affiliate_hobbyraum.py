#!/usr/bin/env python3
from __future__ import annotations

import argparse, difflib, fnmatch, hashlib, json, os, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / ".runs"
CONTRACT = "AFFILIATE_HOBBYRAUM_V1"
FORBIDDEN_TOKENS = ("STARTMASTER", "TEXTMASCHINE", "HOBBYRAUM/")

class Blocked(RuntimeError):
    pass

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_rel(value: str) -> Path:
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or not str(p):
        raise Blocked("PATH_INVALID:" + value)
    return p

def reject_foreign(value: str) -> None:
    upper = value.upper()
    for token in FORBIDDEN_TOKENS:
        if token in upper:
            raise Blocked("FOREIGN_WORKSTREAM_FORBIDDEN:" + value)

def load_task(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {"contract","task_id","goal","image","inputs","writable","command","tests","timeout_seconds"}
    if set(data) != required:
        raise Blocked("TASK_FIELDS_INVALID")
    if data["contract"] != CONTRACT:
        raise Blocked("WRONG_CONTRACT")
    if not isinstance(data["goal"], str) or not data["goal"].strip():
        raise Blocked("ONE_GOAL_REQUIRED")
    if "\n" in data["goal"] or len(data["goal"]) > 300:
        raise Blocked("GOAL_NOT_SINGLE_AND_COMPACT")
    if not isinstance(data["inputs"], list) or not data["inputs"]:
        raise Blocked("INPUTS_REQUIRED")
    if len(data["inputs"]) > 20:
        raise Blocked("TOO_MANY_INPUTS")
    if not isinstance(data["writable"], list):
        raise Blocked("WRITABLE_INVALID")
    if not isinstance(data["tests"], list):
        raise Blocked("TESTS_INVALID")
    if not isinstance(data["command"], str) or not data["command"].strip():
        raise Blocked("COMMAND_REQUIRED")
    reject_foreign(data["goal"])
    reject_foreign(data["command"])
    for test in data["tests"]:
        if not isinstance(test, str) or not test.strip():
            raise Blocked("TEST_INVALID")
        reject_foreign(test)
    return data

def assert_safe_source(src: Path) -> None:
    if src.is_symlink():
        raise Blocked("SYMLINK_INPUT_FORBIDDEN:" + str(src))
    if ".git" in src.parts:
        raise Blocked("GIT_METADATA_FORBIDDEN:" + str(src))

def prepare(task: dict, task_file: Path) -> Path:
    run = RUNS / task["task_id"]
    if run.exists():
        shutil.rmtree(run)
    workspace, baseline, out = run/"workspace", run/"baseline", run/"out"
    workspace.mkdir(parents=True)
    baseline.mkdir(parents=True)
    out.mkdir(parents=True)

    base = task_file.parent.resolve()
    seen_dest = set()
    for row in task["inputs"]:
        if not isinstance(row, dict) or set(row) != {"src","dest"}:
            raise Blocked("INPUT_ROW_INVALID")
        reject_foreign(str(row["src"]))
        reject_foreign(str(row["dest"]))
        src = Path(row["src"])
        if not src.is_absolute():
            src = (base / src).resolve()
        dest_rel = safe_rel(str(row["dest"]))
        if str(dest_rel) in seen_dest:
            raise Blocked("DUPLICATE_INPUT_DEST:" + str(dest_rel))
        seen_dest.add(str(dest_rel))
        if not src.exists() or not src.is_file():
            raise Blocked("INPUT_FILE_MISSING:" + str(src))
        assert_safe_source(src)
        dest = workspace / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    for w in task["writable"]:
        reject_foreign(str(w))
        safe_rel(str(w))

    shutil.copytree(workspace, baseline, dirs_exist_ok=True)
    (run/"TASK.json").write_text(json.dumps(task, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return run

def engine() -> str:
    for name in ("docker","podman"):
        if shutil.which(name):
            return name
    raise Blocked("DOCKER_OR_PODMAN_REQUIRED")

def snapshot(root: Path) -> dict[str,str]:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[p.relative_to(root).as_posix()] = sha256(p)
    return out

def allowed(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)

def run_cmd(task: dict, run: Path, command: str) -> subprocess.CompletedProcess:
    eng = engine()
    workspace = (run/"workspace").resolve()
    cmd = [
        eng,"run","--rm","--pull=never",
        "--network","none","--read-only",
        "--cap-drop","ALL","--security-opt","no-new-privileges",
        "--pids-limit","256",
        "--user",f"{os.getuid()}:{os.getgid()}",
        "--env","HOME=/tmp","--env","TMPDIR=/tmp",
        "--tmpfs","/tmp:rw,nosuid,nodev,size=256m",
        "-v",f"{workspace}:/workspace:rw","-w","/workspace",
        task["image"],"/bin/sh","-lc",command
    ]
    return subprocess.run(
        cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=int(task["timeout_seconds"])
    )

def export(task: dict, run: Path) -> dict:
    before, after = snapshot(run/"baseline"), snapshot(run/"workspace")
    changed = sorted(p for p in set(before)|set(after) if before.get(p) != after.get(p))
    forbidden = [p for p in changed if not allowed(p, task["writable"])]
    if forbidden:
        raise Blocked("WRITE_OUTSIDE_ALLOWLIST:" + ",".join(forbidden))

    patch_parts = []
    for rel in changed:
        src, old = run/"workspace"/rel, run/"baseline"/rel
        dst = run/"out"/rel
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        try:
            old_text = old.read_text(encoding="utf-8").splitlines(True) if old.exists() else []
            new_text = src.read_text(encoding="utf-8").splitlines(True) if src.exists() else []
            patch_parts.extend(difflib.unified_diff(old_text,new_text,fromfile="a/"+rel,tofile="b/"+rel))
        except UnicodeDecodeError:
            patch_parts.append(f"BINARY_CHANGED {rel}\n")
    (run/"PATCH.diff").write_text("".join(patch_parts), encoding="utf-8")
    result = {
        "status":"PASS",
        "contract":CONTRACT,
        "goal":task["goal"],
        "changed":changed,
        "patch_ref":str(run/"PATCH.diff"),
        "out_ref":str(run/"out")
    }
    (run/"RESULT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return result

def execute(task: dict, task_file: Path) -> dict:
    run = prepare(task, task_file)
    p = run_cmd(task, run, task["command"])
    (run/"COMMAND.stdout.txt").write_text(p.stdout or "",encoding="utf-8")
    (run/"COMMAND.stderr.txt").write_text(p.stderr or "",encoding="utf-8")
    if p.returncode != 0:
        detail = ((p.stderr or "")+" "+(p.stdout or "")).replace("\n"," ")[:500]
        raise Blocked("TASK_COMMAND_FAILED:"+str(p.returncode)+":"+detail)

    for i,test in enumerate(task["tests"],1):
        p = run_cmd(task, run, test)
        (run/f"TEST_{i}.stdout.txt").write_text(p.stdout or "",encoding="utf-8")
        (run/f"TEST_{i}.stderr.txt").write_text(p.stderr or "",encoding="utf-8")
        if p.returncode != 0:
            detail = ((p.stderr or "")+" "+(p.stdout or "")).replace("\n"," ")[:500]
            raise Blocked("TEST_FAILED:"+str(i)+":"+detail)
    return export(task, run)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    args = ap.parse_args()
    try:
        task_file = Path(args.task).resolve()
        task = load_task(task_file)
        print(json.dumps(execute(task, task_file),ensure_ascii=False,indent=2))
        return 0
    except (Blocked,OSError,ValueError,subprocess.TimeoutExpired,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"BLOCKED","contract":CONTRACT,"reason":str(exc)},ensure_ascii=False,indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
