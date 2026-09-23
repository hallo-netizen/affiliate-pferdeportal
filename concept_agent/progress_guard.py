#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, re, sys
from pathlib import Path

BINDING_CONTRACT = "CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1"
CHECKPOINT_CONTRACT = "CONCEPT_AGENT_CURRENT_PROGRESS_V1"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

class Blocked(RuntimeError):
    pass

def canon(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def stable(value) -> str:
    return hashlib.sha256(canon(value)).hexdigest()

def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value

def verify_binding(binding: dict) -> None:
    if binding.get("contract") != BINDING_CONTRACT:
        raise Blocked("BINDING_CONTRACT_INVALID")
    core = dict(binding)
    declared = core.pop("binding_sha256", None)
    if not isinstance(declared, str) or declared != stable(core):
        raise Blocked("BINDING_HASH_MISMATCH")
    if binding.get("publish_allowed") is not False:
        raise Blocked("BINDING_PUBLISH_INVALID")

def verify_checkpoint(binding: dict, state: dict) -> None:
    verify_binding(binding)
    if state.get("contract") != CHECKPOINT_CONTRACT:
        raise Blocked("CHECKPOINT_CONTRACT_INVALID")
    core = dict(state)
    declared = core.pop("checkpoint_sha256", None)
    if not isinstance(declared, str) or declared != stable(core):
        raise Blocked("CHECKPOINT_HASH_MISMATCH")
    if state.get("batch_sha256") != binding.get("batch_sha256"):
        raise Blocked("CHECKPOINT_BATCH_MISMATCH")
    if state.get("production_binding_sha256") != binding.get("binding_sha256"):
        raise Blocked("CHECKPOINT_BINDING_MISMATCH")
    if state.get("item_count") != binding.get("item_count"):
        raise Blocked("CHECKPOINT_COUNT_MISMATCH")
    if state.get("publish_allowed") is not False:
        raise Blocked("CHECKPOINT_PUBLISH_INVALID")

def reseal(previous: dict, new: dict) -> dict:
    prev_sha = previous.get("checkpoint_sha256")
    if not isinstance(prev_sha, str) or not SHA_RE.fullmatch(prev_sha):
        raise Blocked("PREVIOUS_CHECKPOINT_SHA_INVALID")
    out = json.loads(json.dumps(new))
    out["previous_checkpoint_sha256"] = prev_sha
    out.pop("checkpoint_sha256", None)
    out["checkpoint_sha256"] = stable(out)
    return out

def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def _draft_path(draft_dir: Path, index: int, slot: str) -> Path:
    candidates = [draft_dir / f"{index:02d}_{slot}.md", draft_dir / f"{index}_{slot}.md"]
    existing = [p for p in candidates if p.is_file()]
    if len(existing) != 1:
        raise Blocked(f"DRAFT_FILE_NOT_EXACT:{index}")
    return existing[0]

def _find_draft(state: dict, index: int) -> dict:
    rows = state.get("drafts")
    if not isinstance(rows, list):
        raise Blocked("DRAFT_MANIFEST_MISSING")
    matches = [row for row in rows if isinstance(row, dict) and row.get("item_index") == index]
    if len(matches) != 1:
        raise Blocked(f"DRAFT_MANIFEST_ITEM_INVALID:{index}")
    return matches[0]

def attach_drafts(binding: dict, state: dict, draft_dir: Path) -> dict:
    verify_checkpoint(binding, state)
    if state.get("phase") != "AUTHORING_READY" or state.get("completed_items") != [] or state.get("current_item") is not None:
        raise Blocked("ATTACH_DRAFTS_PHASE_INVALID")
    rows = []
    for item in binding["items"]:
        idx = item["item_index"]
        slot = item["identity"]["plan_slot"]
        path = _draft_path(draft_dir, idx, slot)
        raw = path.read_bytes()
        if not raw.strip():
            raise Blocked(f"DRAFT_EMPTY:{idx}")
        rows.append({
            "item_index": idx,
            "plan_slot": slot,
            "filename": path.name,
            "draft_sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
            "revision": 1,
            "lt68": "PENDING",
            "ppm679": "PENDING",
        })
    out = dict(state)
    out["phase"] = "DRAFTS_SECURED_PENDING_LT"
    out["drafts"] = rows
    out["next_item_index"] = 0
    out["status"] = "IN_PROGRESS"
    return reseal(state, out)

def _check_result(result: dict, draft_sha: str) -> str:
    status = str(result.get("status") or "")
    if status not in {"PASS", "REPAIR_REQUIRED"}:
        raise Blocked("CHECK_RESULT_STATUS_INVALID")
    content_sha = str(result.get("content_sha256") or result.get("checked_draft_sha256") or "")
    if content_sha != draft_sha:
        raise Blocked("CHECK_RESULT_DRAFT_HASH_MISMATCH")
    return status

def record_check(binding: dict, state: dict, index: int, checker: str, result: dict, draft_path: Path) -> dict:
    verify_checkpoint(binding, state)
    if state.get("phase") not in {"DRAFTS_SECURED_PENDING_LT", "CHECKING", "REPAIR_REQUIRED"}:
        raise Blocked("RECORD_CHECK_PHASE_INVALID")
    if state.get("next_item_index") != index:
        raise Blocked("RECORD_CHECK_WRONG_ITEM")
    row = _find_draft(state, index)
    if file_sha(draft_path) != row["draft_sha256"]:
        raise Blocked("RECORD_CHECK_DRAFT_BYTES_CHANGED")
    status = _check_result(result, row["draft_sha256"])
    out = json.loads(json.dumps(state))
    target = _find_draft(out, index)
    checker = checker.upper()
    if checker == "LT68":
        if target.get("lt68") not in {"PENDING", "REPAIR_REQUIRED"} or target.get("ppm679") != "PENDING":
            raise Blocked("LT68_ORDER_INVALID")
        target["lt68"] = status
    elif checker == "PPM679":
        if target.get("lt68") != "PASS" or target.get("ppm679") not in {"PENDING", "REPAIR_REQUIRED"}:
            raise Blocked("PPM679_ORDER_INVALID")
        target["ppm679"] = status
    else:
        raise Blocked("CHECKER_INVALID")
    target["last_check_sha256"] = stable(result)
    if status == "REPAIR_REQUIRED":
        out["phase"] = "REPAIR_REQUIRED"
        out["current_item"] = {
            "item_index": index,
            "checker": checker,
            "draft_sha256": target["draft_sha256"],
            "finding_sha256": stable(result),
        }
    elif checker == "LT68":
        out["phase"] = "CHECKING"
        out["current_item"] = {
            "item_index": index,
            "next_checker": "PPM679",
            "draft_sha256": target["draft_sha256"],
        }
    else:
        completed = list(out.get("completed_items") or [])
        completed.append({
            "item_index": index,
            "plan_slot": target["plan_slot"],
            "draft_sha256": target["draft_sha256"],
            "revision": target["revision"],
            "lt68": "PASS",
            "ppm679": "PASS",
        })
        out["completed_items"] = completed
        out["current_item"] = None
        out["next_item_index"] = index + 1
        if out["next_item_index"] == out["item_count"]:
            out["phase"] = "ALL_ARTICLES_LT_PPM_PASS"
            out["status"] = "PASS"
        else:
            out["phase"] = "DRAFTS_SECURED_PENDING_LT"
    return reseal(state, out)

def replace_draft(binding: dict, state: dict, index: int, draft_path: Path) -> dict:
    verify_checkpoint(binding, state)
    if state.get("phase") != "REPAIR_REQUIRED" or state.get("next_item_index") != index:
        raise Blocked("REPAIR_DRAFT_PHASE_INVALID")
    current = state.get("current_item")
    if not isinstance(current, dict) or current.get("item_index") != index:
        raise Blocked("REPAIR_CURRENT_ITEM_INVALID")
    out = json.loads(json.dumps(state))
    target = _find_draft(out, index)
    new_sha = file_sha(draft_path)
    if new_sha == target["draft_sha256"]:
        raise Blocked("REPAIR_DRAFT_UNCHANGED")
    target["draft_sha256"] = new_sha
    target["size_bytes"] = draft_path.stat().st_size
    target["filename"] = draft_path.name
    target["revision"] = int(target.get("revision") or 1) + 1
    target["lt68"] = "PENDING"
    target["ppm679"] = "PENDING"
    target.pop("last_check_sha256", None)
    out["phase"] = "DRAFTS_SECURED_PENDING_LT"
    out["current_item"] = None
    return reseal(state, out)

def main(argv: list[str]) -> int:
    try:
        if len(argv) < 2:
            raise Blocked("COMMAND_REQUIRED")
        cmd = argv[1]
        if cmd == "attach-drafts" and len(argv) == 6:
            binding, state = load(Path(argv[2])), load(Path(argv[3]))
            result = attach_drafts(binding, state, Path(argv[4]))
            write(Path(argv[5]), result)
        elif cmd == "record-check" and len(argv) == 9:
            binding, state = load(Path(argv[2])), load(Path(argv[3]))
            result = record_check(binding, state, int(argv[4]), argv[5], load(Path(argv[6])), Path(argv[7]))
            write(Path(argv[8]), result)
        elif cmd == "replace-draft" and len(argv) == 7:
            binding, state = load(Path(argv[2])), load(Path(argv[3]))
            result = replace_draft(binding, state, int(argv[4]), Path(argv[5]))
            write(Path(argv[6]), result)
        else:
            raise Blocked(
                "USE: progress_guard.py attach-drafts BINDING CHECKPOINT DRAFT_DIR OUT | "
                "record-check BINDING CHECKPOINT INDEX LT68|PPM679 RESULT_JSON DRAFT OUT | "
                "replace-draft BINDING CHECKPOINT INDEX DRAFT OUT"
            )
        print(json.dumps({
            "status": result["phase"],
            "next_item_index": result["next_item_index"],
            "checkpoint_sha256": result["checkpoint_sha256"],
            "publish_allowed": False,
        }, sort_keys=True))
        return 0
    except Exception as exc:
        print("CONCEPT_AGENT_PROGRESS_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
