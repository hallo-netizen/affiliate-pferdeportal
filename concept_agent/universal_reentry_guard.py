#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from pathlib import Path

import full_workflow_gate
import progress_guard

CONTRACT = "CONCEPT_AGENT_UNIVERSAL_REENTRY_DECISION_V2"
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

def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value

def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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

def _research_payload_sha(binding: dict) -> str:
    rows = []
    for item in binding["items"]:
        research = item.get("research_bound")
        if not isinstance(research, dict):
            raise Blocked("RESEARCH_BOUND_ITEM_MISSING")
        rows.append({
            "item_index": item["item_index"],
            "plan_slot": item["identity"]["plan_slot"],
            "source_pool_sha256": research.get("source_pool_sha256"),
        })
    return stable(rows)

def _draft_row(binding: dict, checkpoint: dict, index: int) -> dict:
    rows = checkpoint.get("drafts")
    if not isinstance(rows, list):
        raise Blocked("DRAFTS_NOT_DURABLE")
    found = [x for x in rows if isinstance(x, dict) and x.get("item_index") == index]
    if len(found) != 1:
        raise Blocked("DRAFT_NOT_UNIQUE:" + str(index))
    row = found[0]
    item = binding["items"][index]
    if row.get("plan_slot") != item["identity"]["plan_slot"]:
        raise Blocked("DRAFT_SLOT_MISMATCH:" + str(index))
    content = row.get("content_utf8")
    if not isinstance(content, str) or not content:
        raise Blocked("DRAFT_BYTES_NOT_DURABLE:" + str(index))
    raw = content.encode("utf-8")
    if hashlib.sha256(raw).hexdigest() != row.get("draft_sha256"):
        raise Blocked("DRAFT_HASH_MISMATCH:" + str(index))
    if len(raw) != row.get("size_bytes"):
        raise Blocked("DRAFT_SIZE_MISMATCH:" + str(index))
    revision = row.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise Blocked("DRAFT_REVISION_INVALID:" + str(index))
    return row

def _validate_completed_articles(binding: dict, checkpoint: dict) -> str:
    count = binding["item_count"]
    completed = checkpoint.get("completed_items")
    if not isinstance(completed, list) or len(completed) != count:
        raise Blocked("ARTICLE_COMPLETION_COUNT_INVALID")
    bundle_rows = []
    for index, rec in enumerate(completed):
        if not isinstance(rec, dict) or rec.get("item_index") != index:
            raise Blocked("ARTICLE_COMPLETION_ORDER_INVALID:" + str(index))
        item = binding["items"][index]
        if rec.get("plan_slot") != item["identity"]["plan_slot"]:
            raise Blocked("ARTICLE_COMPLETION_SLOT_INVALID:" + str(index))
        if rec.get("lt68") != "PASS" or rec.get("ppm679") != "PASS":
            raise Blocked("ARTICLE_VALIDATOR_PASS_MISSING:" + str(index))
        row = _draft_row(binding, checkpoint, index)
        if rec.get("draft_sha256") != row.get("draft_sha256"):
            raise Blocked("ARTICLE_COMPLETION_DRAFT_HASH_MISMATCH:" + str(index))
        if rec.get("revision") != row.get("revision"):
            raise Blocked("ARTICLE_COMPLETION_REVISION_MISMATCH:" + str(index))
        bundle_rows.append({
            "item_index": index,
            "plan_slot": rec["plan_slot"],
            "draft_sha256": rec["draft_sha256"],
            "revision": rec["revision"],
        })
    return stable(bundle_rows)

def _outer_state(binding: dict, checkpoint: dict) -> dict:
    progress_guard.verify_binding(binding)
    progress_guard.verify_checkpoint(binding, checkpoint)
    batch = binding["batch_sha256"]
    count = binding["item_count"]

    intake_sha = str(binding.get("source_intake_sha256") or "")
    research_binding_sha = str(binding.get("source_research_binding_sha256") or "")
    authoring_binding_sha = str(binding.get("binding_sha256") or "")
    for name, value in (
        ("INTAKE", intake_sha),
        ("RESEARCH_BOUND", research_binding_sha),
        ("AUTHORING_BOUND", authoring_binding_sha),
    ):
        if not SHA_RE.fullmatch(value):
            raise Blocked("OUTER_BINDING_HASH_INVALID:" + name)

    research_payload_sha = _research_payload_sha(binding)
    state = full_workflow_gate.initial_state(batch, count)
    state = full_workflow_gate.complete_stage(state, "INTAKE", {
        "batch_sha256": batch,
        "item_count": count,
        "intake_status": "PASS",
        "intake_sha256": intake_sha,
        "publish_allowed": False,
    })
    state = full_workflow_gate.complete_stage(state, "RESEARCH", {
        "batch_sha256": batch,
        "item_count": count,
        "research_status": "COMPLETE",
        "research_payload_sha256": research_payload_sha,
        "publish_allowed": False,
    })
    state = full_workflow_gate.complete_stage(state, "RESEARCH_BOUND", {
        "batch_sha256": batch,
        "item_count": count,
        "research_binding_status": "PASS",
        "research_payload_sha256": research_payload_sha,
        "research_binding_sha256": research_binding_sha,
        "publish_allowed": False,
    })
    state = full_workflow_gate.complete_stage(state, "AUTHORING_BOUND", {
        "batch_sha256": batch,
        "item_count": count,
        "authoring_binding_status": "PASS",
        "research_binding_sha256": research_binding_sha,
        "authoring_binding_sha256": authoring_binding_sha,
        "publish_allowed": False,
    })

    phase = checkpoint["phase"]
    article_complete_phases = {
        "ALL_ARTICLES_LT_PPM_PASS",
        "PSERC_PASS_ENDSTEMPEL_REQUIRED",
        "ENDSTEMPEL_PASS_STOP",
    }
    article_bundle_sha = None
    if phase in article_complete_phases:
        article_bundle_sha = _validate_completed_articles(binding, checkpoint)
        state = full_workflow_gate.complete_stage(state, "ARTICLE_PRODUCTION", {
            "batch_sha256": batch,
            "item_count": count,
            "article_status": "PASS",
            "authoring_binding_sha256": authoring_binding_sha,
            "article_pass_count": count,
            "article_bundle_sha256": article_bundle_sha,
            "lt68_all_pass": True,
            "ppm679_all_pass": True,
            "publish_allowed": False,
        })

    if phase in {"PSERC_PASS_ENDSTEMPEL_REQUIRED", "ENDSTEMPEL_PASS_STOP"}:
        pserc_sha = str(checkpoint.get("pserc_package_sha256") or "")
        if not SHA_RE.fullmatch(pserc_sha):
            raise Blocked("PSERC_PACKAGE_SHA_MISSING")
        state = full_workflow_gate.complete_stage(state, "PSERC_PACKAGE", {
            "batch_sha256": batch,
            "item_count": count,
            "pserc_status": "PASS",
            "article_bundle_sha256": article_bundle_sha,
            "pserc_package_sha256": pserc_sha,
            "publish_allowed": False,
        })

    if phase == "ENDSTEMPEL_PASS_STOP":
        final_sha = str(checkpoint.get("endstempel_final_file_sha256") or "")
        pserc_sha = str(checkpoint.get("pserc_package_sha256") or "")
        if not SHA_RE.fullmatch(final_sha):
            raise Blocked("ENDSTEMPEL_FINAL_FILE_SHA_MISSING")
        state = full_workflow_gate.complete_stage(state, "ENDSTEMPEL", {
            "batch_sha256": batch,
            "item_count": count,
            "endstempel_status": "ENDSTEMPEL_PASS",
            "pserc_package_sha256": pserc_sha,
            "final_file_sha256": final_sha,
            "publish_allowed": False,
        })
    return state

def _assert_route_matches_checkpoint(route: dict, checkpoint: dict) -> None:
    stage = route.get("next_stage")
    action = checkpoint.get("allowed_action")
    if not isinstance(action, dict):
        raise Blocked("CHECKPOINT_ALLOWED_ACTION_MISSING")
    name = action.get("action")
    if stage == "ARTICLE_PRODUCTION":
        if name not in {"WRITE_DRAFT", "RUN_CHECKER", "REPAIR_DRAFT"}:
            raise Blocked("ARTICLE_ROUTE_ACTION_MISMATCH:" + str(name))
    elif stage == "PSERC_PACKAGE":
        if name != "RUN_PSERC":
            raise Blocked("PSERC_ROUTE_ACTION_MISMATCH:" + str(name))
    elif stage == "ENDSTEMPEL":
        if name != "RUN_ENDSTEMPEL":
            raise Blocked("ENDSTEMPEL_ROUTE_ACTION_MISMATCH:" + str(name))
    elif stage == "COMPLETE":
        if name != "STOP":
            raise Blocked("COMPLETE_ROUTE_ACTION_MISMATCH:" + str(name))
    else:
        raise Blocked("UNEXPECTED_REENTRY_STAGE:" + str(stage))

def build(binding: dict, checkpoint: dict, capsule: dict | None = None, previous: dict | None = None) -> dict:
    outer_state = _outer_state(binding, checkpoint)
    entry = full_workflow_gate.enter(outer_state)
    route = full_workflow_gate.stage_route_from_entry_proof(entry)
    _assert_route_matches_checkpoint(route, checkpoint)

    workspace = None
    workspace_capsule = None
    workspace_action = None
    previous_workspace_sha = None

    if previous is not None:
        verify(binding, checkpoint, previous)
        previous_workspace_sha = previous.get("decision_sha256")

    if capsule is not None:
        cap, state = verify_capsule(capsule)
        current = verify_state_against_current_item(binding, checkpoint, state)
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
        workspace_capsule = json.loads(json.dumps(cap))
        workspace_action = {
            "action": "CONTINUE_BOUND_ARTICLE_WORKER",
            "item_index": current["item_index"],
            "plan_slot": current["plan_slot"],
            "inner_phase": current["phase"],
            "inner_action": current["inner_action"],
        }
        if current.get("draft_sha256"):
            workspace_action["draft_sha256"] = current["draft_sha256"]
        workspace_action["revision"] = current.get("revision")
    elif checkpoint["allowed_action"].get("action") in {"RUN_CHECKER", "REPAIR_DRAFT"}:
        raise Blocked("WORKSPACE_CAPSULE_REQUIRED_FOR_ACTIVE_ARTICLE")

    decision = {
        "contract": CONTRACT,
        "status": "PASS",
        "batch_sha256": binding["batch_sha256"],
        "production_binding_sha256": binding["binding_sha256"],
        "checkpoint_sha256": checkpoint["checkpoint_sha256"],
        "outer_state_sha256": outer_state["state_sha256"],
        "outer_entry_proof_sha256": entry["proof_sha256"],
        "outer_route_sha256": route["route_sha256"],
        "outer_stage": route["next_stage"],
        "outer_authority": route["authority"],
        "outer_entry_ref": route["entry_ref"],
        "outer_allowed_operation": route["allowed_operation"],
        "allowed_action": checkpoint["allowed_action"],
        "workspace": workspace,
        "workspace_capsule": workspace_capsule,
        "workspace_action": workspace_action,
        "previous_workspace_decision_sha256": previous_workspace_sha,
        "policy": {
            "always_enter_at_stage_0": True,
            "fast_forward_validate_only": True,
            "chat_may_choose_stage": False,
            "chat_may_choose_article": False,
            "free_chat_execution": False,
            "free_repo_search": False,
            "free_binary_lookup": False,
            "alternate_route_allowed": False,
            "missing_canonical_execution_environment": "STOP",
            "resume_from_exact_checkpoint_only": True,
        },
        "publish_allowed": False,
    }
    decision["decision_sha256"] = stable(decision)
    if previous is not None and workspace is not None:
        validate_transition(previous, decision)
    return decision

def verify(binding: dict, checkpoint: dict, decision: dict) -> dict:
    capsule = decision.get("workspace_capsule") if isinstance(decision, dict) else None
    previous = None
    expected = build(binding, checkpoint, capsule, previous)
    # previous_workspace_decision_sha256 is chaining metadata and cannot be rebuilt
    # without the preceding decision object; all other bytes must be exact.
    actual = json.loads(json.dumps(decision))
    expected_previous = actual.get("previous_workspace_decision_sha256")
    expected["previous_workspace_decision_sha256"] = expected_previous
    expected.pop("decision_sha256", None)
    expected["decision_sha256"] = stable(expected)
    if actual != expected:
        raise Blocked("REENTRY_DECISION_NOT_EXACT_CURRENT_DERIVATION")
    return {
        "status": "UNIVERSAL_REENTRY_ALLOWED",
        "batch_sha256": decision["batch_sha256"],
        "checkpoint_sha256": decision["checkpoint_sha256"],
        "outer_stage": decision["outer_stage"],
        "allowed_action": decision["allowed_action"],
        "workspace": decision.get("workspace"),
        "workspace_action": decision.get("workspace_action"),
        "decision_sha256": decision["decision_sha256"],
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
    if current.get("previous_workspace_decision_sha256") != previous.get("decision_sha256"):
        raise Blocked("REENTRY_CHAIN_BROKEN")

def main(argv: list[str]) -> int:
    try:
        if len(argv) == 5 and argv[1] == "build":
            result = build(load(Path(argv[2])), load(Path(argv[3])))
            write(Path(argv[4]), result)
            print(json.dumps({
                "status": "UNIVERSAL_REENTRY_DECISION_READY",
                "outer_stage": result["outer_stage"],
                "allowed_action": result["allowed_action"],
                "decision_sha256": result["decision_sha256"],
                "publish_allowed": False,
            }, ensure_ascii=False, sort_keys=True))
            return 0
        if len(argv) == 6 and argv[1] == "build-capsule":
            result = build(load(Path(argv[2])), load(Path(argv[3])), load(Path(argv[4])))
            write(Path(argv[5]), result)
            print(json.dumps({
                "status": "UNIVERSAL_REENTRY_DECISION_READY",
                "outer_stage": result["outer_stage"],
                "allowed_action": result["allowed_action"],
                "workspace_action": result["workspace_action"],
                "decision_sha256": result["decision_sha256"],
                "publish_allowed": False,
            }, ensure_ascii=False, sort_keys=True))
            return 0
        if len(argv) == 7 and argv[1] == "advance-capsule":
            binding = load(Path(argv[2]))
            checkpoint = load(Path(argv[3]))
            previous = load(Path(argv[4]))
            result = build(binding, checkpoint, load(Path(argv[5])), previous)
            write(Path(argv[6]), result)
            print(json.dumps({
                "status": "UNIVERSAL_REENTRY_DECISION_READY",
                "workspace_action": result["workspace_action"],
                "decision_sha256": result["decision_sha256"],
                "publish_allowed": False,
            }, ensure_ascii=False, sort_keys=True))
            return 0
        if len(argv) == 5 and argv[1] == "verify":
            result = verify(load(Path(argv[2])), load(Path(argv[3])), load(Path(argv[4])))
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        raise Blocked(
            "USE: universal_reentry_guard.py build BINDING CHECKPOINT OUT | "
            "build-capsule BINDING CHECKPOINT CAPSULE OUT | "
            "advance-capsule BINDING CHECKPOINT PREVIOUS CAPSULE OUT | "
            "verify BINDING CHECKPOINT DECISION"
        )
    except Exception as exc:
        print("CONCEPT_AGENT_UNIVERSAL_REENTRY_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
