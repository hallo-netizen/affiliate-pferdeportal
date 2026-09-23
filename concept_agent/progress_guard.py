#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, re, sys
from pathlib import Path

BINDING_CONTRACT = "CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1"
CHECKPOINT_CONTRACT = "CONCEPT_AGENT_CURRENT_PROGRESS_V1"
BATCH_STAGE_RESULT_CONTRACT = "CONCEPT_AGENT_BOUND_BATCH_STAGE_RESULT_V1"
REENTRY_GATE = "CONCEPT_AGENT_UNIVERSAL_REENTRY_CHECKPOINT_V1"
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
    items = binding.get("items")
    if not isinstance(items, list) or not items or binding.get("item_count") != len(items):
        raise Blocked("BINDING_ITEMS_INVALID")
    for index, item in enumerate(items):
        if not isinstance(item, dict) or item.get("item_index") != index:
            raise Blocked(f"BINDING_ITEM_ORDER_INVALID:{index}")
        identity = item.get("identity")
        if not isinstance(identity, dict) or not SHA_RE.fullmatch(str(identity.get("plan_slot") or "")):
            raise Blocked(f"BINDING_ITEM_IDENTITY_INVALID:{index}")

def _binding_item(binding: dict, index: int) -> dict:
    verify_binding(binding)
    items = binding["items"]
    if index < 0 or index >= len(items):
        raise Blocked("ITEM_INDEX_INVALID")
    return items[index]

def _find_draft(state: dict, index: int) -> dict:
    rows = state.get("drafts")
    if not isinstance(rows, list):
        raise Blocked("DRAFT_MANIFEST_MISSING")
    matches = [row for row in rows if isinstance(row, dict) and row.get("item_index") == index]
    if len(matches) != 1:
        raise Blocked(f"DRAFT_MANIFEST_ITEM_INVALID:{index}")
    return matches[0]

def _gated(action: dict) -> dict:
    out = dict(action)
    out["reentry_gate"] = REENTRY_GATE
    out["canonical_bound_worker_only"] = True
    out["free_chat_execution"] = False
    out["fallback_route"] = "STOP"
    return out

def expected_action(binding: dict, state: dict) -> dict:
    phase = str(state.get("phase") or "")
    index = state.get("next_item_index")
    count = binding.get("item_count")
    if not isinstance(index, int) or isinstance(index, bool) or not isinstance(count, int):
        raise Blocked("CHECKPOINT_INDEX_INVALID")
    if phase == "AUTHORING_REQUIRED":
        item = _binding_item(binding, index)
        return _gated({
            "action": "WRITE_DRAFT",
            "item_index": index,
            "plan_slot": item["identity"]["plan_slot"],
        })
    if phase == "LT68_REQUIRED":
        row = _find_draft(state, index)
        return _gated({
            "action": "RUN_CHECKER",
            "checker": "LT68",
            "item_index": index,
            "draft_sha256": row["draft_sha256"],
        })
    if phase == "PPM679_REQUIRED":
        row = _find_draft(state, index)
        return _gated({
            "action": "RUN_CHECKER",
            "checker": "PPM679",
            "item_index": index,
            "draft_sha256": row["draft_sha256"],
        })
    if phase == "REPAIR_REQUIRED":
        row = _find_draft(state, index)
        current = state.get("current_item")
        if not isinstance(current, dict) or current.get("item_index") != index:
            raise Blocked("REPAIR_CURRENT_ITEM_INVALID")
        checker = str(current.get("checker") or "")
        if checker not in {"LT68", "PPM679"}:
            raise Blocked("REPAIR_CHECKER_INVALID")
        return _gated({
            "action": "REPAIR_DRAFT",
            "item_index": index,
            "checker": checker,
            "draft_sha256": row["draft_sha256"],
            "finding_sha256": current.get("finding_sha256"),
        })
    if phase == "ALL_ARTICLES_LT_PPM_PASS":
        if index != count or state.get("status") != "PASS":
            raise Blocked("COMPLETE_CHECKPOINT_INVALID")
        return _gated({
            "action": "RUN_PSERC",
            "item_count": count,
        })
    if phase == "PSERC_PASS_ENDSTEMPEL_REQUIRED":
        if index != count:
            raise Blocked("PSERC_PASS_INDEX_INVALID")
        return _gated({
            "action": "RUN_ENDSTEMPEL",
            "item_count": count,
        })
    if phase == "ENDSTEMPEL_PASS_STOP":
        if index != count or state.get("status") != "PASS":
            raise Blocked("ENDSTEMPEL_STOP_STATE_INVALID")
        return _gated({
            "action": "STOP",
            "reason": "BATCH_COMPLETE_ENDSTEMPEL_PASS",
        })
    raise Blocked("CHECKPOINT_PHASE_NOT_RESUMABLE:" + phase)

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
    if state.get("allowed_action") != expected_action(binding, state):
        raise Blocked("CHECKPOINT_ALLOWED_ACTION_MISMATCH")

def _seal_new_state(binding: dict, previous: dict, new: dict) -> dict:
    prev_sha = previous.get("checkpoint_sha256")
    if not isinstance(prev_sha, str) or not SHA_RE.fullmatch(prev_sha):
        raise Blocked("PREVIOUS_CHECKPOINT_SHA_INVALID")
    out = json.loads(json.dumps(new))
    out["previous_checkpoint_sha256"] = prev_sha
    out["allowed_action"] = expected_action(binding, out)
    out.pop("checkpoint_sha256", None)
    out["checkpoint_sha256"] = stable(out)
    return out

def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def attach_drafts(binding: dict, state: dict, draft_dir: Path) -> dict:
    verify_checkpoint(binding, state)
    raise Blocked("BATCH_DRAFT_ATTACH_FORBIDDEN")

def record_draft(binding: dict, state: dict, index: int, draft_path: Path) -> dict:
    verify_checkpoint(binding, state)
    action = state["allowed_action"]
    if action.get("action") != "WRITE_DRAFT" or action.get("item_index") != index:
        raise Blocked("RECORD_DRAFT_NOT_ALLOWED")
    item = _binding_item(binding, index)
    slot = item["identity"]["plan_slot"]
    if draft_path.name != f"{index:02d}_{slot}.md":
        raise Blocked("DRAFT_FILENAME_NOT_EXACT")
    raw = draft_path.read_bytes()
    if not raw.strip():
        raise Blocked("DRAFT_EMPTY")
    rows = state.get("drafts")
    if rows is None:
        rows = []
    if not isinstance(rows, list):
        raise Blocked("DRAFT_MANIFEST_INVALID")
    if any(isinstance(row, dict) and row.get("item_index") == index for row in rows):
        raise Blocked("DRAFT_ALREADY_RECORDED")
    out = json.loads(json.dumps(state))
    out["drafts"] = list(rows) + [{
        "item_index": index,
        "plan_slot": slot,
        "filename": draft_path.name,
        "draft_sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
        "revision": 1,
        "lt68": "PENDING",
        "ppm679": "PENDING",
    }]
    out["phase"] = "LT68_REQUIRED"
    out["status"] = "IN_PROGRESS"
    out["current_item"] = {
        "item_index": index,
        "draft_sha256": out["drafts"][-1]["draft_sha256"],
    }
    return _seal_new_state(binding, state, out)

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
    checker = checker.upper()
    action = state["allowed_action"]
    if (
        action.get("action") != "RUN_CHECKER"
        or action.get("item_index") != index
        or action.get("checker") != checker
    ):
        raise Blocked("RECORD_CHECK_NOT_ALLOWED")
    row = _find_draft(state, index)
    if file_sha(draft_path) != row["draft_sha256"]:
        raise Blocked("RECORD_CHECK_DRAFT_BYTES_CHANGED")
    status = _check_result(result, row["draft_sha256"])
    out = json.loads(json.dumps(state))
    target = _find_draft(out, index)
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
        out["phase"] = "PPM679_REQUIRED"
        out["current_item"] = {
            "item_index": index,
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
            out["phase"] = "AUTHORING_REQUIRED"
    return _seal_new_state(binding, state, out)

def replace_draft(binding: dict, state: dict, index: int, draft_path: Path) -> dict:
    verify_checkpoint(binding, state)
    action = state["allowed_action"]
    if action.get("action") != "REPAIR_DRAFT" or action.get("item_index") != index:
        raise Blocked("REPAIR_DRAFT_NOT_ALLOWED")
    target0 = _find_draft(state, index)
    if draft_path.name != target0["filename"]:
        raise Blocked("REPAIR_DRAFT_FILENAME_MISMATCH")
    out = json.loads(json.dumps(state))
    target = _find_draft(out, index)
    new_sha = file_sha(draft_path)
    if new_sha == target["draft_sha256"]:
        raise Blocked("REPAIR_DRAFT_UNCHANGED")
    target["draft_sha256"] = new_sha
    target["size_bytes"] = draft_path.stat().st_size
    target["revision"] = int(target.get("revision") or 1) + 1
    target["lt68"] = "PENDING"
    target["ppm679"] = "PENDING"
    target.pop("last_check_sha256", None)
    out["phase"] = "LT68_REQUIRED"
    out["current_item"] = {
        "item_index": index,
        "draft_sha256": new_sha,
    }
    return _seal_new_state(binding, state, out)

def _validate_batch_stage_result(state: dict, stage: str, result: dict) -> None:
    if result.get("contract") != BATCH_STAGE_RESULT_CONTRACT:
        raise Blocked("BATCH_STAGE_RESULT_CONTRACT_INVALID")
    if result.get("stage") != stage:
        raise Blocked("BATCH_STAGE_RESULT_STAGE_MISMATCH")
    if result.get("status") != "PASS":
        raise Blocked("BATCH_STAGE_RESULT_NOT_PASS")
    if result.get("batch_sha256") != state.get("batch_sha256"):
        raise Blocked("BATCH_STAGE_RESULT_BATCH_MISMATCH")
    if result.get("source_checkpoint_sha256") != state.get("checkpoint_sha256"):
        raise Blocked("BATCH_STAGE_RESULT_CHECKPOINT_MISMATCH")
    if result.get("publish_allowed") is not False:
        raise Blocked("BATCH_STAGE_RESULT_PUBLISH_INVALID")
    evidence = str(result.get("evidence_sha256") or "")
    if not SHA_RE.fullmatch(evidence):
        raise Blocked("BATCH_STAGE_RESULT_EVIDENCE_HASH_INVALID")

def record_batch_stage(binding: dict, state: dict, stage: str, result: dict) -> dict:
    verify_checkpoint(binding, state)
    stage = stage.upper()
    action = state["allowed_action"]
    if stage == "PSERC":
        if action.get("action") != "RUN_PSERC" or state.get("phase") != "ALL_ARTICLES_LT_PPM_PASS":
            raise Blocked("PSERC_NOT_ALLOWED")
        _validate_batch_stage_result(state, stage, result)
        out = json.loads(json.dumps(state))
        out["phase"] = "PSERC_PASS_ENDSTEMPEL_REQUIRED"
        out["status"] = "IN_PROGRESS"
        out["pserc_result_sha256"] = stable(result)
        return _seal_new_state(binding, state, out)
    if stage == "ENDSTEMPEL":
        if action.get("action") != "RUN_ENDSTEMPEL" or state.get("phase") != "PSERC_PASS_ENDSTEMPEL_REQUIRED":
            raise Blocked("ENDSTEMPEL_NOT_ALLOWED")
        _validate_batch_stage_result(state, stage, result)
        out = json.loads(json.dumps(state))
        out["phase"] = "ENDSTEMPEL_PASS_STOP"
        out["status"] = "PASS"
        out["endstempel_result_sha256"] = stable(result)
        return _seal_new_state(binding, state, out)
    raise Blocked("BATCH_STAGE_INVALID")

def resume(binding: dict, state: dict) -> dict:
    verify_checkpoint(binding, state)
    return {
        "status": "RESUME_ALLOWED",
        "batch_sha256": state["batch_sha256"],
        "checkpoint_sha256": state["checkpoint_sha256"],
        "allowed_action": state["allowed_action"],
        "publish_allowed": False,
    }

def main(argv: list[str]) -> int:
    try:
        if len(argv) < 2:
            raise Blocked("COMMAND_REQUIRED")
        cmd = argv[1]
        if cmd == "resume" and len(argv) == 4:
            result = resume(load(Path(argv[2])), load(Path(argv[3])))
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        if cmd == "attach-drafts":
            raise Blocked("BATCH_DRAFT_ATTACH_FORBIDDEN")
        if cmd == "record-draft" and len(argv) == 7:
            binding, state = load(Path(argv[2])), load(Path(argv[3]))
            result = record_draft(binding, state, int(argv[4]), Path(argv[5]))
            write(Path(argv[6]), result)
        elif cmd == "record-check" and len(argv) == 9:
            binding, state = load(Path(argv[2])), load(Path(argv[3]))
            result = record_check(binding, state, int(argv[4]), argv[5], load(Path(argv[6])), Path(argv[7]))
            write(Path(argv[8]), result)
        elif cmd == "replace-draft" and len(argv) == 7:
            binding, state = load(Path(argv[2])), load(Path(argv[3]))
            result = replace_draft(binding, state, int(argv[4]), Path(argv[5]))
            write(Path(argv[6]), result)
        elif cmd == "record-batch-stage" and len(argv) == 7:
            binding, state = load(Path(argv[2])), load(Path(argv[3]))
            result = record_batch_stage(binding, state, argv[4], load(Path(argv[5])))
            write(Path(argv[6]), result)
        else:
            raise Blocked(
                "USE: progress_guard.py resume BINDING CHECKPOINT | "
                "record-draft BINDING CHECKPOINT INDEX DRAFT OUT | "
                "record-check BINDING CHECKPOINT INDEX LT68|PPM679 RESULT_JSON DRAFT OUT | "
                "replace-draft BINDING CHECKPOINT INDEX DRAFT OUT | "
                "record-batch-stage BINDING CHECKPOINT PSERC|ENDSTEMPEL RESULT_JSON OUT"
            )
        print(json.dumps({
            "status": result["phase"],
            "next_item_index": result["next_item_index"],
            "allowed_action": result["allowed_action"],
            "checkpoint_sha256": result["checkpoint_sha256"],
            "publish_allowed": False,
        }, sort_keys=True))
        return 0
    except Exception as exc:
        print("CONCEPT_AGENT_PROGRESS_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
