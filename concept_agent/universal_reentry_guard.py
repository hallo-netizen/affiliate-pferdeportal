#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from pathlib import Path

import progress_guard

CONTRACT = "CONCEPT_AGENT_UNIVERSAL_REENTRY_CHECKPOINT_V1"
CAPSULE_CONTRACT = "SYSTEM4_WORKSPACE_RECOVERY_CAPSULE_V1"
STATE_CONTRACT = "SYSTEM4_CANONICAL_ARTICLE_STATE_V1"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

INNER_PHASE_ACTIONS = {
    "RESEARCH_REQUIRED": "BOUND_RESEARCH_ONLY",
    "FACT_CHECK_REQUIRED": "BOUND_FACT_CHECK_ONLY",
    "CONTEXT_REQUIRED": "BOUND_CONTEXT_ONLY",
    "DRAFT_REQUIRED": "BOUND_DRAFT_ONLY",
    "CHECK_REQUIRED": "BOUND_FULLCHECK_ONLY",
    "REPAIR_REQUIRED": "BOUND_SAME_ARTICLE_REPAIR_ONLY",
    "OUTPUT_GATE_REQUIRED": "BOUND_OUTPUT_GATE_ONLY",
    "SIGNATURE_REQUIRED": "BOUND_SIGNATURE_GATE_ONLY",
    "RELEASED": "BOUND_ITEM_COMPLETE_ONLY",
}

INNER_TRANSITIONS = {
    "RESEARCH_REQUIRED": {"FACT_CHECK_REQUIRED"},
    "FACT_CHECK_REQUIRED": {"CONTEXT_REQUIRED"},
    "CONTEXT_REQUIRED": {"DRAFT_REQUIRED"},
    "DRAFT_REQUIRED": {"CHECK_REQUIRED"},
    "CHECK_REQUIRED": {"REPAIR_REQUIRED", "OUTPUT_GATE_REQUIRED"},
    "REPAIR_REQUIRED": {"CHECK_REQUIRED"},
    "OUTPUT_GATE_REQUIRED": {"SIGNATURE_REQUIRED", "RELEASED"},
    "SIGNATURE_REQUIRED": {"RELEASED"},
    "RELEASED": set(),
}

class Blocked(RuntimeError):
    pass

def canon(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def stable(value) -> str:
    return hashlib.sha256(canon(value)).hexdigest()

def _safe_rel(value: str) -> Path:
    p = Path(str(value or ""))
    if not value or p.is_absolute() or ".." in p.parts:
        raise Blocked("CAPSULE_PATH_INVALID")
    return p

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

def _binding_item(binding: dict, index: int) -> dict:
    progress_guard.verify_binding(binding)
    items = binding["items"]
    if not isinstance(index, int) or isinstance(index, bool) or index < 0 or index >= len(items):
        raise Blocked("ITEM_INDEX_INVALID")
    return items[index]

def _checks_sha(state: dict) -> str:
    return hashlib.sha256(canon(state.get("checks") or {}) + b"\n").hexdigest()

def _capsule_identity(state: dict) -> dict:
    article = state.get("article") or {}
    return {
        "canonical_article_id": article.get("canonical_article_id"),
        "plan_slot": article.get("plan_slot"),
        "title": article.get("title"),
        "target_keyword": article.get("target_keyword"),
        "phase": state.get("phase"),
        "revision": state.get("revision"),
        "draft_sha256": state.get("draft_sha256"),
        "checks_sha256": _checks_sha(state),
        "last_error": state.get("last_error"),
    }

def _verify_state_integrity(state: dict) -> None:
    if state.get("contract") != STATE_CONTRACT:
        raise Blocked("WORKSPACE_STATE_CONTRACT_INVALID")
    article = state.get("article")
    if not isinstance(article, dict):
        raise Blocked("WORKSPACE_ARTICLE_INVALID")
    immutable = {
        "contract": state.get("contract"),
        "source_snapshot_sha256": state.get("source_snapshot_sha256"),
        "batch_sha256": state.get("batch_sha256"),
        "article": article,
    }
    if state.get("immutable_core_sha256") != stable(immutable):
        raise Blocked("WORKSPACE_IMMUTABLE_CORE_TAMPERED")
    if state.get("publish_allowed") is not False:
        raise Blocked("WORKSPACE_STATE_PUBLISH_INVALID")

    for field in ("research", "facts"):
        value = state.get(field)
        if value is not None:
            if not isinstance(value, dict) or not isinstance(value.get("text"), str):
                raise Blocked("WORKSPACE_" + field.upper() + "_INVALID")
            if hashlib.sha256(value["text"].encode("utf-8")).hexdigest() != value.get("sha256"):
                raise Blocked("WORKSPACE_" + field.upper() + "_HASH_MISMATCH")

    draft = state.get("draft_markdown")
    if draft is not None:
        if not isinstance(draft, str):
            raise Blocked("WORKSPACE_DRAFT_INVALID")
        if hashlib.sha256(draft.encode("utf-8")).hexdigest() != state.get("draft_sha256"):
            raise Blocked("WORKSPACE_DRAFT_HASH_MISMATCH")

    context = state.get("production_context")
    if context is not None:
        if not isinstance(context, dict) or set(context) != {"fact_pack", "production_plan_item", "sha256"}:
            raise Blocked("WORKSPACE_CONTEXT_INVALID")
        if stable({
            "fact_pack": context["fact_pack"],
            "production_plan_item": context["production_plan_item"],
        }) != context.get("sha256"):
            raise Blocked("WORKSPACE_CONTEXT_HASH_MISMATCH")

    phase = str(state.get("phase") or "")
    if phase not in INNER_PHASE_ACTIONS:
        raise Blocked("WORKSPACE_PHASE_INVALID")
    if phase == "FACT_CHECK_REQUIRED" and state.get("research") is None:
        raise Blocked("WORKSPACE_PHASE_STATE_MISMATCH")
    if phase in {"CONTEXT_REQUIRED","DRAFT_REQUIRED","CHECK_REQUIRED","REPAIR_REQUIRED","OUTPUT_GATE_REQUIRED","SIGNATURE_REQUIRED","RELEASED"}:
        if state.get("research") is None or state.get("facts") is None:
            raise Blocked("WORKSPACE_PHASE_STATE_MISMATCH")
    if phase in {"DRAFT_REQUIRED","CHECK_REQUIRED","REPAIR_REQUIRED","OUTPUT_GATE_REQUIRED","SIGNATURE_REQUIRED","RELEASED"}:
        if state.get("production_context") is None or not isinstance(state.get("authoring_contract"), dict):
            raise Blocked("WORKSPACE_PHASE_STATE_MISMATCH")
    if phase in {"CHECK_REQUIRED","REPAIR_REQUIRED","OUTPUT_GATE_REQUIRED","SIGNATURE_REQUIRED","RELEASED"} and not draft:
        raise Blocked("WORKSPACE_PHASE_STATE_MISMATCH")
    if phase == "REPAIR_REQUIRED":
        checks = state.get("checks") or {}
        if checks.get("status") != "FAIL" or not state.get("last_error"):
            raise Blocked("WORKSPACE_REPAIR_STATE_MISMATCH")
    if phase in {"OUTPUT_GATE_REQUIRED","SIGNATURE_REQUIRED","RELEASED"}:
        checks = state.get("checks") or {}
        if checks.get("status") != "PASS" or checks.get("checked_draft_sha256") != state.get("draft_sha256"):
            raise Blocked("WORKSPACE_PASS_STATE_MISMATCH")
    if phase == "SIGNATURE_REQUIRED" and not isinstance(state.get("release_prepared"), dict):
        raise Blocked("WORKSPACE_SIGNATURE_STATE_MISMATCH")
    if phase == "RELEASED" and state.get("released") is not True:
        raise Blocked("WORKSPACE_RELEASE_STATE_MISMATCH")

def verify_capsule(capsule: dict) -> tuple[dict, dict]:
    if not isinstance(capsule, dict) or capsule.get("contract") != CAPSULE_CONTRACT:
        raise Blocked("CAPSULE_CONTRACT_INVALID")
    if capsule.get("status") != "RECOVERY_CAPSULE_READY":
        raise Blocked("CAPSULE_STATUS_INVALID")
    if capsule.get("publish_allowed") is not False:
        raise Blocked("CAPSULE_PUBLISH_INVALID")
    rows = capsule.get("files")
    if not isinstance(rows, list) or not rows or capsule.get("file_count") != len(rows):
        raise Blocked("CAPSULE_FILESET_INVALID")
    seen = set()
    normalized = []
    state = None
    for row in rows:
        if not isinstance(row, dict):
            raise Blocked("CAPSULE_FILE_INVALID")
        rel = _safe_rel(str(row.get("path") or "")).as_posix()
        if rel in seen:
            raise Blocked("CAPSULE_DUPLICATE_PATH")
        seen.add(rel)
        try:
            raw = base64.b64decode(str(row.get("base64") or ""), validate=True)
        except Exception as exc:
            raise Blocked("CAPSULE_BASE64_INVALID:" + rel) from exc
        size = row.get("size")
        if not isinstance(size, int) or isinstance(size, bool) or size != len(raw):
            raise Blocked("CAPSULE_SIZE_MISMATCH:" + rel)
        digest = hashlib.sha256(raw).hexdigest()
        if digest != row.get("sha256"):
            raise Blocked("CAPSULE_HASH_MISMATCH:" + rel)
        normalized.append({"path": rel, "size": len(raw), "sha256": digest})
        if rel == "state.json":
            try:
                state = json.loads(raw.decode("utf-8"))
            except Exception as exc:
                raise Blocked("CAPSULE_STATE_JSON_INVALID") from exc
    if capsule.get("tree_sha256") != _tree_hash(normalized):
        raise Blocked("CAPSULE_TREE_HASH_MISMATCH")
    if not isinstance(state, dict):
        raise Blocked("CAPSULE_STATE_MISSING")
    identity = capsule.get("workspace_identity")
    if not isinstance(identity, dict):
        raise Blocked("CAPSULE_IDENTITY_MISSING")
    _verify_state_integrity(state)
    if identity != _capsule_identity(state):
        raise Blocked("CAPSULE_IDENTITY_MISMATCH")
    return capsule, state

def verify_state_against_current_item(binding: dict, outer: dict, state: dict) -> dict:
    progress_guard.verify_checkpoint(binding, outer)
    index = outer.get("next_item_index")
    if not isinstance(index, int) or isinstance(index, bool):
        raise Blocked("OUTER_INDEX_INVALID")
    item = _binding_item(binding, index)
    identity = item.get("identity")
    article = state.get("article")
    _verify_state_integrity(state)
    if state.get("batch_sha256") != binding.get("batch_sha256"):
        raise Blocked("WORKSPACE_BATCH_MISMATCH")
    if not isinstance(identity, dict) or not isinstance(article, dict):
        raise Blocked("WORKSPACE_ARTICLE_IDENTITY_MISSING")
    for key in ("title", "target_keyword", "category", "article_type", "plan_slot"):
        if article.get(key) != identity.get(key):
            raise Blocked("WORKSPACE_ARTICLE_IDENTITY_MISMATCH:" + key)
    phase = str(state.get("phase") or "")
    if phase not in INNER_PHASE_ACTIONS:
        raise Blocked("WORKSPACE_PHASE_INVALID")
    if phase in {"CHECK_REQUIRED", "REPAIR_REQUIRED", "OUTPUT_GATE_REQUIRED", "SIGNATURE_REQUIRED", "RELEASED"}:
        draft_sha = str(state.get("draft_sha256") or "")
        if not SHA_RE.fullmatch(draft_sha):
            raise Blocked("WORKSPACE_DRAFT_HASH_MISSING")
    return {
        "item_index": index,
        "plan_slot": identity["plan_slot"],
        "phase": phase,
        "inner_action": INNER_PHASE_ACTIONS[phase],
        "draft_sha256": state.get("draft_sha256"),
        "revision": state.get("revision"),
        "last_error": state.get("last_error"),
    }

def _outer_action(binding: dict, outer: dict) -> dict:
    progress_guard.verify_checkpoint(binding, outer)
    action = outer["allowed_action"]
    name = action.get("action")
    if name == "WRITE_DRAFT":
        return {
            "action": "START_BOUND_ARTICLE_WORKER",
            "item_index": action["item_index"],
            "plan_slot": action["plan_slot"],
        }
    if name in {"RUN_CHECKER", "REPAIR_DRAFT"}:
        raise Blocked("WORKSPACE_CAPSULE_REQUIRED_FOR_ACTIVE_ARTICLE")
    if name == "RUN_PSERC":
        return {
            "action": "RUN_BOUND_PSERC",
            "item_count": action["item_count"],
        }
    if name == "RUN_ENDSTEMPEL":
        return {
            "action": "RUN_BOUND_ENDSTEMPEL",
            "item_count": action["item_count"],
        }
    if name == "STOP":
        return {
            "action": "STOP",
            "reason": action.get("reason"),
        }
    raise Blocked("OUTER_ACTION_NOT_SUPPORTED")

def build(binding: dict, outer: dict, capsule: dict | None = None, previous: dict | None = None) -> dict:
    progress_guard.verify_checkpoint(binding, outer)
    previous_sha = None
    if previous is not None:
        verify(binding, outer, previous)
        previous_sha = previous["reentry_checkpoint_sha256"]

    if capsule is None:
        allowed = _outer_action(binding, outer)
        workspace = None
    else:
        cap, state = verify_capsule(capsule)
        current = verify_state_against_current_item(binding, outer, state)
        allowed = {
            "action": "CONTINUE_BOUND_ARTICLE_WORKER",
            "item_index": current["item_index"],
            "plan_slot": current["plan_slot"],
            "inner_phase": current["phase"],
            "inner_action": current["inner_action"],
        }
        if current.get("draft_sha256"):
            allowed["draft_sha256"] = current["draft_sha256"]
        allowed["revision"] = current.get("revision")
        workspace = {
            "capsule_sha256": stable(cap),
            "tree_sha256": cap["tree_sha256"],
            "workspace_identity": cap["workspace_identity"],
            "state_phase": current["phase"],
            "item_index": current["item_index"],
            "plan_slot": current["plan_slot"],
            "draft_sha256": current.get("draft_sha256"),
            "revision": current.get("revision"),
            "last_error": current.get("last_error"),
        }

    result = {
        "contract": CONTRACT,
        "batch_sha256": binding["batch_sha256"],
        "production_binding_sha256": binding["binding_sha256"],
        "outer_checkpoint_sha256": outer["checkpoint_sha256"],
        "previous_reentry_checkpoint_sha256": previous_sha,
        "workspace": workspace,
        "allowed_action": allowed,
        "execution_policy": {
            "canonical_bound_worker_only": True,
            "free_chat_execution": False,
            "free_repo_search": False,
            "free_binary_lookup": False,
            "fallback_route": "STOP",
            "resume_from_this_checkpoint_only": True,
        },
        "publish_allowed": False,
    }
    result["reentry_checkpoint_sha256"] = stable(result)
    return result

def verify(binding: dict, outer: dict, reentry: dict) -> dict:
    progress_guard.verify_checkpoint(binding, outer)
    if not isinstance(reentry, dict) or reentry.get("contract") != CONTRACT:
        raise Blocked("REENTRY_CONTRACT_INVALID")
    core = dict(reentry)
    declared = core.pop("reentry_checkpoint_sha256", None)
    if not isinstance(declared, str) or declared != stable(core):
        raise Blocked("REENTRY_HASH_MISMATCH")
    if reentry.get("batch_sha256") != binding.get("batch_sha256"):
        raise Blocked("REENTRY_BATCH_MISMATCH")
    if reentry.get("production_binding_sha256") != binding.get("binding_sha256"):
        raise Blocked("REENTRY_BINDING_MISMATCH")
    if reentry.get("outer_checkpoint_sha256") != outer.get("checkpoint_sha256"):
        raise Blocked("REENTRY_OUTER_CHECKPOINT_MISMATCH")
    if reentry.get("publish_allowed") is not False:
        raise Blocked("REENTRY_PUBLISH_INVALID")
    policy = reentry.get("execution_policy")
    expected_policy = {
        "canonical_bound_worker_only": True,
        "free_chat_execution": False,
        "free_repo_search": False,
        "free_binary_lookup": False,
        "fallback_route": "STOP",
        "resume_from_this_checkpoint_only": True,
    }
    if policy != expected_policy:
        raise Blocked("REENTRY_EXECUTION_POLICY_INVALID")
    allowed = reentry.get("allowed_action")
    if not isinstance(allowed, dict):
        raise Blocked("REENTRY_ALLOWED_ACTION_INVALID")
    workspace = reentry.get("workspace")
    if workspace is None:
        expected = _outer_action(binding, outer)
        if allowed != expected:
            raise Blocked("REENTRY_ALLOWED_ACTION_MISMATCH")
    else:
        if not isinstance(workspace, dict):
            raise Blocked("REENTRY_WORKSPACE_INVALID")
        phase = workspace.get("state_phase")
        if phase not in INNER_PHASE_ACTIONS:
            raise Blocked("REENTRY_WORKSPACE_PHASE_INVALID")
        expected = {
            "action": "CONTINUE_BOUND_ARTICLE_WORKER",
            "item_index": workspace.get("item_index"),
            "plan_slot": workspace.get("plan_slot"),
            "inner_phase": phase,
            "inner_action": INNER_PHASE_ACTIONS[phase],
        }
        if workspace.get("draft_sha256"):
            expected["draft_sha256"] = workspace["draft_sha256"]
        expected["revision"] = workspace.get("revision")
        if allowed != expected:
            raise Blocked("REENTRY_ALLOWED_ACTION_MISMATCH")
    return {
        "status": "UNIVERSAL_REENTRY_ALLOWED",
        "batch_sha256": reentry["batch_sha256"],
        "reentry_checkpoint_sha256": declared,
        "allowed_action": allowed,
        "publish_allowed": False,
    }

def validate_transition(previous: dict, current: dict) -> None:
    pw = previous.get("workspace")
    cw = current.get("workspace")
    if not isinstance(pw, dict) or not isinstance(cw, dict):
        raise Blocked("WORKSPACE_TRANSITION_REQUIRES_TWO_CAPSULES")
    if previous.get("batch_sha256") != current.get("batch_sha256"):
        raise Blocked("TRANSITION_BATCH_CHANGED")
    if previous.get("production_binding_sha256") != current.get("production_binding_sha256"):
        raise Blocked("TRANSITION_BINDING_CHANGED")
    if pw.get("item_index") != cw.get("item_index") or pw.get("plan_slot") != cw.get("plan_slot"):
        raise Blocked("TRANSITION_ARTICLE_CHANGED")
    before = str(pw.get("state_phase") or "")
    after = str(cw.get("state_phase") or "")
    if after not in INNER_TRANSITIONS.get(before, set()):
        raise Blocked("WORKSPACE_PHASE_JUMP_FORBIDDEN:" + before + "->" + after)
    if current.get("previous_reentry_checkpoint_sha256") != previous.get("reentry_checkpoint_sha256"):
        raise Blocked("REENTRY_CHAIN_BROKEN")

def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED")
    return value

def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main(argv: list[str]) -> int:
    try:
        if len(argv) == 5 and argv[1] == "build":
            result = build(load(Path(argv[2])), load(Path(argv[3])), None)
            write(Path(argv[4]), result)
        elif len(argv) == 6 and argv[1] == "build-capsule":
            result = build(load(Path(argv[2])), load(Path(argv[3])), load(Path(argv[4])))
            write(Path(argv[5]), result)
        elif len(argv) == 7 and argv[1] == "advance-capsule":
            binding = load(Path(argv[2]))
            outer = load(Path(argv[3]))
            previous = load(Path(argv[4]))
            result = build(binding, outer, load(Path(argv[5])), previous)
            validate_transition(previous, result)
            write(Path(argv[6]), result)
        elif len(argv) == 5 and argv[1] == "resume":
            result = verify(load(Path(argv[2])), load(Path(argv[3])), load(Path(argv[4])))
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        else:
            raise Blocked(
                "USE: universal_reentry_guard.py build BINDING OUTER OUT | "
                "build-capsule BINDING OUTER CAPSULE OUT | "
                "advance-capsule BINDING OUTER PREVIOUS CAPSULE OUT | "
                "resume BINDING OUTER REENTRY"
            )
        print(json.dumps({
            "status": "UNIVERSAL_REENTRY_CHECKPOINT_READY",
            "reentry_checkpoint_sha256": result["reentry_checkpoint_sha256"],
            "allowed_action": result["allowed_action"],
            "publish_allowed": False,
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print("CONCEPT_AGENT_UNIVERSAL_REENTRY_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
