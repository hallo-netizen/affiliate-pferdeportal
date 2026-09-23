#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import full_workflow_gate
import progress_guard
import runtime_environment_guard

CONTRACT = "CONCEPT_AGENT_UNIVERSAL_REENTRY_DECISION_V2"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

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

def build(binding: dict, checkpoint: dict) -> dict:
    runtime_binding = runtime_environment_guard.current_binding()
    outer_state = _outer_state(binding, checkpoint)
    entry = full_workflow_gate.enter(outer_state)
    route = full_workflow_gate.stage_route_from_entry_proof(entry)
    _assert_route_matches_checkpoint(route, checkpoint)
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
        "runtime_binding": runtime_binding,
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
    return decision

def verify(binding: dict, checkpoint: dict, decision: dict) -> dict:
    expected = build(binding, checkpoint)
    if decision != expected:
        raise Blocked("REENTRY_DECISION_NOT_EXACT_CURRENT_DERIVATION")
    return {
        "status": "UNIVERSAL_REENTRY_ALLOWED",
        "batch_sha256": decision["batch_sha256"],
        "checkpoint_sha256": decision["checkpoint_sha256"],
        "outer_stage": decision["outer_stage"],
        "allowed_action": decision["allowed_action"],
        "decision_sha256": decision["decision_sha256"],
        "publish_allowed": False,
    }

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
        if len(argv) == 5 and argv[1] == "verify":
            result = verify(load(Path(argv[2])), load(Path(argv[3])), load(Path(argv[4])))
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        raise Blocked(
            "USE: universal_reentry_guard.py build BINDING CHECKPOINT OUT | "
            "verify BINDING CHECKPOINT DECISION"
        )
    except Exception as exc:
        print("CONCEPT_AGENT_UNIVERSAL_REENTRY_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
