from __future__ import annotations

import base64
import hashlib
import json
import shutil
import sys
from pathlib import Path

CONTRACT = "SYSTEM4_WORKSPACE_RECOVERY_CAPSULE_V1"


class RecoveryCapsuleError(RuntimeError):
    pass


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canon(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _safe_rel(value: str) -> Path:
    p = Path(str(value or ""))
    if not value or p.is_absolute() or ".." in p.parts:
        raise RecoveryCapsuleError("RECOVERY_CAPSULE_PATH_INVALID")
    return p


def _identity(state: dict) -> dict:
    article = state.get("article") or {}
    checks = state.get("checks") or {}
    return {
        "canonical_article_id": article.get("canonical_article_id"),
        "plan_slot": article.get("plan_slot"),
        "title": article.get("title"),
        "target_keyword": article.get("target_keyword"),
        "phase": state.get("phase"),
        "revision": state.get("revision"),
        "draft_sha256": state.get("draft_sha256"),
        "checks_sha256": _sha_bytes(_canon(checks)),
        "last_error": state.get("last_error"),
    }


def _tree_hash(rows: list[dict]) -> str:
    h = hashlib.sha256()
    for row in rows:
        h.update(str(row["path"]).encode("utf-8"))
        h.update(b"\0")
        h.update(str(row["sha256"]).encode("ascii"))
        h.update(b"\0")
        h.update(str(row["size"]).encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def create_capsule(workspace: Path, output: Path) -> dict:
    workspace = Path(workspace).resolve()
    output = Path(output).resolve()
    if not workspace.is_dir():
        raise RecoveryCapsuleError("RECOVERY_WORKSPACE_MISSING")
    state_path = workspace / "state.json"
    if not state_path.is_file():
        raise RecoveryCapsuleError("RECOVERY_STATE_MISSING")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    rows: list[dict] = []
    for path in sorted(workspace.rglob("*")):
        if path.is_symlink():
            raise RecoveryCapsuleError("RECOVERY_SYMLINK_FORBIDDEN")
        if not path.is_file():
            continue
        rel = path.relative_to(workspace).as_posix()
        raw = path.read_bytes()
        rows.append({
            "path": rel,
            "size": len(raw),
            "sha256": _sha_bytes(raw),
            "base64": base64.b64encode(raw).decode("ascii"),
        })
    if not rows:
        raise RecoveryCapsuleError("RECOVERY_WORKSPACE_EMPTY")
    manifest = {
        "contract": CONTRACT,
        "status": "RECOVERY_CAPSULE_READY",
        "workspace_identity": _identity(state),
        "file_count": len(rows),
        "tree_sha256": _tree_hash(rows),
        "files": rows,
        "publish_allowed": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    tmp.write_bytes(_canon(manifest))
    tmp.replace(output)
    verify_capsule(output)
    return manifest


def verify_capsule(capsule: Path) -> dict:
    capsule = Path(capsule).resolve()
    try:
        value = json.loads(capsule.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RecoveryCapsuleError("RECOVERY_CAPSULE_JSON_INVALID") from exc
    if value.get("contract") != CONTRACT or value.get("status") != "RECOVERY_CAPSULE_READY":
        raise RecoveryCapsuleError("RECOVERY_CAPSULE_CONTRACT_INVALID")
    rows = value.get("files")
    if not isinstance(rows, list) or not rows or value.get("file_count") != len(rows):
        raise RecoveryCapsuleError("RECOVERY_CAPSULE_FILESET_INVALID")
    seen: set[str] = set()
    normalized: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            raise RecoveryCapsuleError("RECOVERY_CAPSULE_FILE_INVALID")
        rel = _safe_rel(str(row.get("path") or "")).as_posix()
        if rel in seen:
            raise RecoveryCapsuleError("RECOVERY_CAPSULE_DUPLICATE_PATH")
        seen.add(rel)
        try:
            raw = base64.b64decode(str(row.get("base64") or ""), validate=True)
        except Exception as exc:
            raise RecoveryCapsuleError("RECOVERY_CAPSULE_BASE64_INVALID:" + rel) from exc
        if len(raw) != int(row.get("size", -1)):
            raise RecoveryCapsuleError("RECOVERY_CAPSULE_SIZE_MISMATCH:" + rel)
        if _sha_bytes(raw) != row.get("sha256"):
            raise RecoveryCapsuleError("RECOVERY_CAPSULE_HASH_MISMATCH:" + rel)
        normalized.append({"path": rel, "size": len(raw), "sha256": row["sha256"]})
    if value.get("tree_sha256") != _tree_hash(normalized):
        raise RecoveryCapsuleError("RECOVERY_CAPSULE_TREE_HASH_MISMATCH")
    state_rows = [row for row in rows if row.get("path") == "state.json"]
    if len(state_rows) != 1:
        raise RecoveryCapsuleError("RECOVERY_CAPSULE_STATE_FILE_INVALID")
    state = json.loads(base64.b64decode(state_rows[0]["base64"]).decode("utf-8"))
    if value.get("workspace_identity") != _identity(state):
        raise RecoveryCapsuleError("RECOVERY_CAPSULE_IDENTITY_MISMATCH")
    if value.get("publish_allowed") is not False:
        raise RecoveryCapsuleError("RECOVERY_CAPSULE_PUBLISH_INVALID")
    return value


def restore_capsule(capsule: Path, destination: Path) -> dict:
    value = verify_capsule(capsule)
    destination = Path(destination).resolve()
    if destination.exists() and any(destination.iterdir()):
        raise RecoveryCapsuleError("RECOVERY_DESTINATION_NOT_EMPTY")
    destination.mkdir(parents=True, exist_ok=True)
    for row in value["files"]:
        rel = _safe_rel(row["path"])
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = base64.b64decode(row["base64"])
        target.write_bytes(raw)
    restored = create_capsule(destination, destination.parent / (destination.name + ".verify.json"))
    (destination.parent / (destination.name + ".verify.json")).unlink(missing_ok=True)
    if restored["tree_sha256"] != value["tree_sha256"]:
        shutil.rmtree(destination, ignore_errors=True)
        raise RecoveryCapsuleError("RECOVERY_RESTORE_TREE_MISMATCH")
    if restored["workspace_identity"] != value["workspace_identity"]:
        shutil.rmtree(destination, ignore_errors=True)
        raise RecoveryCapsuleError("RECOVERY_RESTORE_IDENTITY_MISMATCH")
    return {
        "contract": CONTRACT,
        "status": "RECOVERY_RESTORE_PASS",
        "tree_sha256": value["tree_sha256"],
        "workspace_identity": value["workspace_identity"],
        "file_count": value["file_count"],
        "publish_allowed": False,
    }


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 4 and argv[1] == "create":
            result = create_capsule(Path(argv[2]), Path(argv[3]))
        elif len(argv) == 3 and argv[1] == "verify":
            result = verify_capsule(Path(argv[2]))
        elif len(argv) == 4 and argv[1] == "restore":
            result = restore_capsule(Path(argv[2]), Path(argv[3]))
        else:
            raise RecoveryCapsuleError(
                "USE: workspace_recovery_capsule.py create WORKSPACE CAPSULE | "
                "verify CAPSULE | restore CAPSULE DESTINATION"
            )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "status": "RECOVERY_CAPSULE_BLOCKED",
            "reason": str(exc),
            "publish_allowed": False,
        }, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
