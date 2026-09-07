#!/usr/bin/env python3
"""Technical handoff for proofs emitted by the unchanged Fachworkflow.

This module has no content or quality authority.  It only verifies that every
required stage left identity-bound, hash-bound evidence of a real execution and
then writes the aggregate pass and the item receipt expected by step 107007.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

REPO = Path(__file__).resolve().parents[2]
CONTRACT = "PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1"
PASS_CONTRACT = "PFERDE_ATELIER_FACHWORKFLOW_PASS_V1"
STAGE_CONTRACT = "PFERDE_ATELIER_FACHWORKFLOW_STAGE_EXECUTION_PROOF_V1"
RECEIPT_CONTRACT = "PFERDE_ATELIER_BOUND_ITEM_EXECUTION_RECEIPT_V1"
STAGES = ["research_fact_pack", "textmachine_article_type_structure", "table_contract",
          "internal_links", "languagetool", "ppm", "pserc", "pste",
          "duplicate_cannibalization", "seo", "design_format", "publish_safety"]


class Blocked(RuntimeError):
    pass


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED")
    return value


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _path(repo: Path, ref: str, root: str) -> Path:
    if not ref.startswith(root):
        raise Blocked("PROOF_REF_OUTSIDE_BOUND_OUTPUT_ROOT")
    relative = Path(ref)
    if relative.is_absolute() or ".." in relative.parts:
        raise Blocked("INVALID_RELATIVE_REF")
    result = (repo / relative).resolve()
    base = (repo / root).resolve()
    if result != base and base not in result.parents:
        raise Blocked("PROOF_REF_ESCAPE")
    return result


def _write(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def materialize(repo: Path, request_ref: str) -> dict:
    repo = Path(repo).resolve()
    relative_request = Path(request_ref)
    if not request_ref or relative_request.is_absolute() or ".." in relative_request.parts:
        raise Blocked("INVALID_HANDOFF_REQUEST_REF")
    request_path = (repo / relative_request).resolve()
    if repo not in request_path.parents:
        raise Blocked("HANDOFF_REQUEST_REF_ESCAPE")
    request = _load(request_path)
    required = {"contract", "room_token", "batch_sha256", "canonical_article_id", "plan_slot",
                "allowed_output_root", "item_receipt_ref", "fachworkflow_pass_ref",
                "contract_binding_ref", "contract_binding_sha256", "stage_proofs",
                "fact_pack", "production_plan_item", "production_plan_header",
                "workflow_release_item", "workflow_release_metadata"}
    if set(request) != required or request.get("contract") != CONTRACT:
        raise Blocked("HANDOFF_REQUEST_FIELDS_OR_CONTRACT_INVALID")
    batch = str(request["batch_sha256"]); slot = str(request["plan_slot"])
    if not re.fullmatch(r"[0-9a-f]{64}", batch) or not re.fullmatch(r"[0-9a-f]{64}", slot):
        raise Blocked("HANDOFF_IDENTITY_HASH_INVALID")
    root = str(request["allowed_output_root"])
    if not root.endswith("/") or request_ref.startswith(root) is False:
        raise Blocked("HANDOFF_REQUEST_NOT_IN_BOUND_OUTPUT_ROOT")
    binding = (repo / str(request["contract_binding_ref"])).resolve()
    if not binding.is_file() or _sha(binding) != request["contract_binding_sha256"]:
        raise Blocked("HANDOFF_CONTRACT_BINDING_HASH_MISMATCH")
    rows = request["stage_proofs"]
    if not isinstance(rows, list) or len(rows) != len(STAGES):
        raise Blocked("FACH_STAGE_COUNT_INVALID")
    verified = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"stage", "ref", "sha256"}:
            raise Blocked("FACH_STAGE_ROW_INVALID")
        stage = row["stage"]
        if stage in seen or stage not in STAGES:
            raise Blocked("FACH_STAGE_SET_INVALID")
        seen.add(stage)
        proof_path = _path(repo, str(row["ref"]), root)
        if not proof_path.is_file() or _sha(proof_path) != row["sha256"]:
            raise Blocked("FACH_STAGE_HASH_MISMATCH:" + str(stage))
        proof = _load(proof_path)
        expected = {"contract": STAGE_CONTRACT, "status": "PASS", "batch_sha256": batch,
                    "canonical_article_id": request["canonical_article_id"], "plan_slot": slot,
                    "stage": stage, "execution_performed": True,
                    "content_or_quality_rules_changed": False, "publish_allowed": False}
        if any(proof.get(key) != value for key, value in expected.items()):
            raise Blocked("FACH_STAGE_EXECUTION_BINDING_INVALID:" + str(stage))
        if not re.fullmatch(r"[0-9a-f]{64}", str(proof.get("input_sha256", ""))):
            raise Blocked("FACH_STAGE_INPUT_HASH_INVALID:" + str(stage))
        evidence = proof.get("execution_evidence")
        artifacts = proof.get("artifacts")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x.strip() for x in evidence):
            raise Blocked("FACH_STAGE_EXECUTION_EVIDENCE_MISSING:" + str(stage))
        if not isinstance(artifacts, list) or not artifacts:
            raise Blocked("FACH_STAGE_ARTIFACTS_MISSING:" + str(stage))
        for artifact in artifacts:
            if not isinstance(artifact, dict) or set(artifact) != {"ref", "sha256"}:
                raise Blocked("FACH_STAGE_ARTIFACT_ROW_INVALID:" + str(stage))
            artifact_path = _path(repo, str(artifact["ref"]), root)
            if not artifact_path.is_file() or _sha(artifact_path) != artifact["sha256"]:
                raise Blocked("FACH_STAGE_ARTIFACT_HASH_MISMATCH:" + str(stage))
        verified.append(dict(row))
    if seen != set(STAGES):
        raise Blocked("FACH_STAGE_SET_INVALID")
    passed = {"contract": PASS_CONTRACT, "status": "PASS", "batch_sha256": batch,
              "canonical_article_id": request["canonical_article_id"], "plan_slot": slot,
              "contract_binding_ref": request["contract_binding_ref"],
              "contract_binding_sha256": request["contract_binding_sha256"],
              "required_stage_proofs": verified, "fact_pack": request["fact_pack"],
              "production_plan_item": request["production_plan_item"],
              "production_plan_header": request["production_plan_header"],
              "workflow_release_item": request["workflow_release_item"],
              "workflow_release_metadata": request["workflow_release_metadata"],
              "content_or_quality_rules_changed": False, "publish_allowed": False}
    pass_path = _path(repo, str(request["fachworkflow_pass_ref"]), root)
    _write(pass_path, passed)
    output_rows = verified + [{"stage": "fachworkflow_pass", "ref": request["fachworkflow_pass_ref"], "sha256": _sha(pass_path)}]
    outputs = [{"ref": row["ref"], "sha256": row["sha256"]} for row in output_rows]
    receipt = {"contract": RECEIPT_CONTRACT, "room_token": request["room_token"],
               "canonical_article_id": request["canonical_article_id"], "plan_slot": slot,
               "status": "PASS", "workflow_pass": True, "navigation_decision": False,
               "state_write_requested": False, "workflow_change_requested": False,
               "content_or_quality_rules_changed": False, "outputs": outputs,
               "evidence": ["REAL_FACHWORKFLOW_STAGE_EXECUTION_PROOFS_HASH_VERIFIED"],
               "fachworkflow_pass_ref": request["fachworkflow_pass_ref"],
               "fachworkflow_pass_sha256": _sha(pass_path)}
    receipt_path = _path(repo, str(request["item_receipt_ref"]), root)
    _write(receipt_path, receipt)
    return {"ok": True, "status": "FACHWORKFLOW_PROOF_HANDOFF_PASS",
            "item_receipt_ref": request["item_receipt_ref"], "item_receipt_sha256": _sha(receipt_path),
            "publish_allowed": False}


def main(argv: list[str]) -> int:
    try:
        if len(argv) != 2 or argv[0] != "materialize":
            raise Blocked("USAGE: materialize HANDOFF_REQUEST.json")
        result = materialize(REPO, argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "status": "FACHWORKFLOW_PROOF_HANDOFF_BLOCKED",
                          "error": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2)); return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
