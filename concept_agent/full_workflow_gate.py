#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

FULL_STATE_CONTRACT = "CONCEPT_AGENT_FULL_WORKFLOW_STATE_V1"
ENTRY_PROOF_CONTRACT = "CONCEPT_AGENT_FULL_REENTRY_PROOF_V1"
STAGES = [
    "INTAKE",
    "RESEARCH",
    "RESEARCH_BOUND",
    "AUTHORING_BOUND",
    "ARTICLE_PRODUCTION",
    "PSERC_PACKAGE",
    "ENDSTEMPEL",
]
SHA_RE = __import__("re").compile(r"^[0-9a-f]{64}$")


class Blocked(RuntimeError):
    pass


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def seal_record(stage: str, payload: dict[str, Any]) -> dict[str, Any]:
    rec = {"stage": stage, "payload": payload}
    rec["payload_sha256"] = stable(payload)
    rec["record_sha256"] = stable(rec)
    return rec


def validate_record(rec: Any, expected_stage: str) -> None:
    if not isinstance(rec, dict) or rec.get("stage") != expected_stage:
        raise Blocked("STAGE_RECORD_INVALID:" + expected_stage)
    payload = rec.get("payload")
    if not isinstance(payload, dict):
        raise Blocked("STAGE_PAYLOAD_INVALID:" + expected_stage)
    if rec.get("payload_sha256") != stable(payload):
        raise Blocked("STAGE_PAYLOAD_HASH_MISMATCH:" + expected_stage)
    copy = dict(rec)
    declared = copy.pop("record_sha256", None)
    if declared != stable(copy):
        raise Blocked("STAGE_RECORD_HASH_MISMATCH:" + expected_stage)


def initial_state(batch_sha256: str, item_count: int) -> dict[str, Any]:
    if not SHA_RE.fullmatch(batch_sha256):
        raise Blocked("BATCH_SHA_INVALID")
    if isinstance(item_count, bool) or not isinstance(item_count, int) or item_count < 1:
        raise Blocked("ITEM_COUNT_INVALID")
    state = {
        "contract": FULL_STATE_CONTRACT,
        "batch_sha256": batch_sha256,
        "item_count": item_count,
        "next_stage_index": 0,
        "completed_stages": [],
        "status": "IN_PROGRESS",
        "publish_allowed": False,
    }
    state["state_sha256"] = stable(state)
    return state


def validate_state(state: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(state, dict) or state.get("contract") != FULL_STATE_CONTRACT:
        raise Blocked("FULL_STATE_CONTRACT_INVALID")
    if state.get("publish_allowed") is not False:
        raise Blocked("PUBLISH_MUST_BE_FALSE")
    copy = dict(state)
    declared = copy.pop("state_sha256", None)
    if declared != stable(copy):
        raise Blocked("FULL_STATE_HASH_MISMATCH")
    batch = state.get("batch_sha256")
    if not isinstance(batch, str) or not SHA_RE.fullmatch(batch):
        raise Blocked("FULL_STATE_BATCH_INVALID")
    count = state.get("item_count")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise Blocked("FULL_STATE_ITEM_COUNT_INVALID")
    completed = state.get("completed_stages")
    if not isinstance(completed, list):
        raise Blocked("FULL_STATE_COMPLETED_INVALID")
    idx = state.get("next_stage_index")
    if not isinstance(idx, int) or idx != len(completed) or idx < 0 or idx > len(STAGES):
        raise Blocked("FULL_STATE_STAGE_SEQUENCE_INVALID")
    for pos, rec in enumerate(completed):
        validate_record(rec, STAGES[pos])
        p = rec["payload"]
        if p.get("batch_sha256") != batch:
            raise Blocked("STAGE_BATCH_MISMATCH:" + STAGES[pos])
        if p.get("item_count") != count:
            raise Blocked("STAGE_ITEM_COUNT_MISMATCH:" + STAGES[pos])
        if p.get("publish_allowed") is not False:
            raise Blocked("STAGE_PUBLISH_INVALID:" + STAGES[pos])
    if idx == len(STAGES):
        if state.get("status") != "PASS":
            raise Blocked("FULL_STATE_FINAL_STATUS_INVALID")
    elif state.get("status") != "IN_PROGRESS":
        raise Blocked("FULL_STATE_PROGRESS_STATUS_INVALID")
    _validate_cross_stage_bindings(state)
    return state


def _validate_cross_stage_bindings(state: dict[str, Any]) -> None:
    rows = state["completed_stages"]
    if not rows:
        return
    by = {r["stage"]: r["payload"] for r in rows}
    batch = state["batch_sha256"]

    if "INTAKE" in by:
        p = by["INTAKE"]
        if p.get("intake_status") != "PASS" or not SHA_RE.fullmatch(str(p.get("intake_sha256") or "")):
            raise Blocked("INTAKE_NOT_BOUND")

    if "RESEARCH" in by:
        p = by["RESEARCH"]
        if p.get("research_status") != "COMPLETE" or not SHA_RE.fullmatch(str(p.get("research_payload_sha256") or "")):
            raise Blocked("RESEARCH_NOT_COMPLETE")

    if "RESEARCH_BOUND" in by:
        p = by["RESEARCH_BOUND"]
        if p.get("research_binding_status") != "PASS":
            raise Blocked("RESEARCH_BINDING_NOT_PASS")
        if p.get("research_payload_sha256") != by["RESEARCH"]["research_payload_sha256"]:
            raise Blocked("RESEARCH_BINDING_SOURCE_HASH_MISMATCH")
        if not SHA_RE.fullmatch(str(p.get("research_binding_sha256") or "")):
            raise Blocked("RESEARCH_BINDING_HASH_INVALID")

    if "AUTHORING_BOUND" in by:
        p = by["AUTHORING_BOUND"]
        if p.get("authoring_binding_status") != "PASS":
            raise Blocked("AUTHORING_BINDING_NOT_PASS")
        if p.get("research_binding_sha256") != by["RESEARCH_BOUND"]["research_binding_sha256"]:
            raise Blocked("AUTHORING_RESEARCH_BINDING_MISMATCH")
        if not SHA_RE.fullmatch(str(p.get("authoring_binding_sha256") or "")):
            raise Blocked("AUTHORING_BINDING_HASH_INVALID")

    if "ARTICLE_PRODUCTION" in by:
        p = by["ARTICLE_PRODUCTION"]
        if p.get("article_status") != "PASS":
            raise Blocked("ARTICLE_PRODUCTION_NOT_PASS")
        if p.get("authoring_binding_sha256") != by["AUTHORING_BOUND"]["authoring_binding_sha256"]:
            raise Blocked("ARTICLE_AUTHORING_BINDING_MISMATCH")
        if p.get("article_pass_count") != state["item_count"]:
            raise Blocked("ARTICLE_PASS_COUNT_MISMATCH")
        if not SHA_RE.fullmatch(str(p.get("article_bundle_sha256") or "")):
            raise Blocked("ARTICLE_BUNDLE_HASH_INVALID")
        if p.get("lt68_all_pass") is not True or p.get("ppm679_all_pass") is not True:
            raise Blocked("ARTICLE_VALIDATORS_NOT_PASS")

    if "PSERC_PACKAGE" in by:
        p = by["PSERC_PACKAGE"]
        if p.get("pserc_status") != "PASS":
            raise Blocked("PSERC_NOT_PASS")
        if p.get("article_bundle_sha256") != by["ARTICLE_PRODUCTION"]["article_bundle_sha256"]:
            raise Blocked("PSERC_ARTICLE_BUNDLE_MISMATCH")
        if not SHA_RE.fullmatch(str(p.get("pserc_package_sha256") or "")):
            raise Blocked("PSERC_PACKAGE_HASH_INVALID")

    if "ENDSTEMPEL" in by:
        p = by["ENDSTEMPEL"]
        if p.get("endstempel_status") != "ENDSTEMPEL_PASS":
            raise Blocked("ENDSTEMPEL_NOT_PASS")
        if p.get("pserc_package_sha256") != by["PSERC_PACKAGE"]["pserc_package_sha256"]:
            raise Blocked("ENDSTEMPEL_PSERC_MISMATCH")
        if not SHA_RE.fullmatch(str(p.get("final_file_sha256") or "")):
            raise Blocked("ENDSTEMPEL_FINAL_FILE_HASH_INVALID")



def reseal(state: dict[str, Any]) -> dict[str, Any]:
    x = dict(state)
    x.pop("state_sha256", None)
    x["state_sha256"] = stable(x)
    return x


def enter(state: dict[str, Any]) -> dict[str, Any]:
    state = validate_state(state)
    proof = {
        "contract": ENTRY_PROOF_CONTRACT,
        "status": "PASS",
        "batch_sha256": state["batch_sha256"],
        "workflow_entry": "ALWAYS_FROM_STAGE_0",
        "fast_forward_mode": "VALIDATE_ONLY",
        "validated_completed_stages": [],
        "next_stage": STAGES[state["next_stage_index"]] if state["next_stage_index"] < len(STAGES) else "COMPLETE",
        "chat_may_choose_stage": False,
        "publish_allowed": False,
    }
    for pos, rec in enumerate(state["completed_stages"]):
        validate_record(rec, STAGES[pos])
        _validate_cross_stage_bindings({
            **state,
            "completed_stages": state["completed_stages"][:pos+1],
            "next_stage_index": pos+1,
            "status": "PASS" if pos+1 == len(STAGES) else "IN_PROGRESS",
        })
        proof["validated_completed_stages"].append(STAGES[pos])
    proof["proof_sha256"] = stable(proof)
    return proof


def complete_stage(state: dict[str, Any], stage: str, payload: dict[str, Any]) -> dict[str, Any]:
    validate_state(state)
    idx = state["next_stage_index"]
    if idx >= len(STAGES):
        raise Blocked("WORKFLOW_ALREADY_COMPLETE")
    expected = STAGES[idx]
    if stage != expected:
        raise Blocked(f"STAGE_OUT_OF_ORDER:{stage}:EXPECTED:{expected}")
    if payload.get("batch_sha256") != state["batch_sha256"]:
        raise Blocked("STAGE_BATCH_MISMATCH:" + stage)
    if payload.get("item_count") != state["item_count"]:
        raise Blocked("STAGE_ITEM_COUNT_MISMATCH:" + stage)
    if payload.get("publish_allowed") is not False:
        raise Blocked("STAGE_PUBLISH_INVALID:" + stage)
    new = json.loads(json.dumps(state))
    new["completed_stages"].append(seal_record(stage, payload))
    new["next_stage_index"] += 1
    if new["next_stage_index"] == len(STAGES):
        new["status"] = "PASS"
    new = reseal(new)
    validate_state(new)
    return new


def sim_hash(label: str, batch: str) -> str:
    return hashlib.sha256((label + ":" + batch).encode("utf-8")).hexdigest()


def payload_for(stage: str, state: dict[str, Any]) -> dict[str, Any]:
    batch = state["batch_sha256"]
    count = state["item_count"]
    base = {"batch_sha256": batch, "item_count": count, "publish_allowed": False}
    by = {r["stage"]: r["payload"] for r in state["completed_stages"]}
    if stage == "INTAKE":
        return {**base, "intake_status": "PASS", "intake_sha256": sim_hash("intake", batch)}
    if stage == "RESEARCH":
        return {**base, "research_status": "COMPLETE", "research_payload_sha256": sim_hash("research", batch)}
    if stage == "RESEARCH_BOUND":
        return {
            **base, "research_binding_status": "PASS",
            "research_payload_sha256": by["RESEARCH"]["research_payload_sha256"],
            "research_binding_sha256": sim_hash("research-bound", batch),
        }
    if stage == "AUTHORING_BOUND":
        return {
            **base, "authoring_binding_status": "PASS",
            "research_binding_sha256": by["RESEARCH_BOUND"]["research_binding_sha256"],
            "authoring_binding_sha256": sim_hash("authoring-bound", batch),
        }
    if stage == "ARTICLE_PRODUCTION":
        return {
            **base, "article_status": "PASS",
            "authoring_binding_sha256": by["AUTHORING_BOUND"]["authoring_binding_sha256"],
            "article_pass_count": count, "lt68_all_pass": True, "ppm679_all_pass": True,
            "article_bundle_sha256": sim_hash("articles", batch),
        }
    if stage == "PSERC_PACKAGE":
        return {
            **base, "pserc_status": "PASS",
            "article_bundle_sha256": by["ARTICLE_PRODUCTION"]["article_bundle_sha256"],
            "pserc_package_sha256": sim_hash("pserc", batch),
        }
    if stage == "ENDSTEMPEL":
        return {
            **base, "endstempel_status": "ENDSTEMPEL_PASS",
            "pserc_package_sha256": by["PSERC_PACKAGE"]["pserc_package_sha256"],
            "final_file_sha256": sim_hash("final-file", batch),
        }
    raise Blocked("UNKNOWN_STAGE:" + stage)


def build_to(batch: str, item_count: int, stage_count: int) -> dict[str, Any]:
    state = initial_state(batch, item_count)
    for stage in STAGES[:stage_count]:
        state = complete_stage(state, stage, payload_for(stage, state))
    return state


def simulate_all_entries(outdir: Path) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    batch = sim_hash("full-workflow-batch", "x" * 64)
    positives = []
    negatives = []

    for stage_count in range(len(STAGES) + 1):
        state = build_to(batch, 3, stage_count)
        proof = enter(state)
        expected = STAGES[stage_count] if stage_count < len(STAGES) else "COMPLETE"
        if proof["next_stage"] != expected:
            raise Blocked("POSITIVE_REENTRY_WRONG_NEXT_STAGE:" + expected)
        if proof["validated_completed_stages"] != STAGES[:stage_count]:
            raise Blocked("POSITIVE_REENTRY_FAST_FORWARD_INVALID:" + expected)
        positives.append({
            "entry_after_completed_count": stage_count,
            "validated_from_entrance": True,
            "fast_forwarded_stages": proof["validated_completed_stages"],
            "next_stage": expected,
            "status": "PASS",
        })

    # Negative: try to skip every next stage.
    for stage_count in range(len(STAGES) - 1):
        state = build_to(batch, 3, stage_count)
        wrong = STAGES[stage_count + 1]
        try:
            complete_stage(state, wrong, {"batch_sha256": batch, "item_count": 3, "publish_allowed": False})
        except Blocked as exc:
            negatives.append({"case": "skip-" + STAGES[stage_count] + "-to-" + wrong, "blocked": True, "reason": str(exc)})
        else:
            raise Blocked("NEGATIVE_STAGE_SKIP_NOT_BLOCKED:" + wrong)

    # Negative: tamper each completed stage hash, then re-enter through entrance.
    for stage_count in range(1, len(STAGES) + 1):
        state = build_to(batch, 3, stage_count)
        bad = json.loads(json.dumps(state))
        bad["completed_stages"][-1]["payload"]["item_count"] = 99
        bad = reseal(bad)
        try:
            enter(bad)
        except Blocked as exc:
            negatives.append({"case": "tamper-" + STAGES[stage_count-1], "blocked": True, "reason": str(exc)})
        else:
            raise Blocked("NEGATIVE_TAMPER_NOT_BLOCKED:" + STAGES[stage_count-1])

    # Negative: validly reseal a forged state that claims completed later stage but breaks cross-stage binding.
    state = build_to(batch, 3, 6)  # through PSERC
    bad = json.loads(json.dumps(state))
    bad["completed_stages"][5]["payload"]["article_bundle_sha256"] = sim_hash("forged", batch)
    rec = bad["completed_stages"][5]
    rec["payload_sha256"] = stable(rec["payload"])
    rec_copy = dict(rec); rec_copy.pop("record_sha256", None); rec["record_sha256"] = stable(rec_copy)
    bad = reseal(bad)
    try:
        enter(bad)
    except Blocked as exc:
        negatives.append({"case": "forged-pserc-cross-binding", "blocked": True, "reason": str(exc)})
    else:
        raise Blocked("NEGATIVE_CROSS_BINDING_NOT_BLOCKED")

    proof = {
        "contract": "CONCEPT_AGENT_FULL_WORKFLOW_REENTRY_ACCEPTANCE_V1",
        "status": "PASS",
        "stages": STAGES,
        "positive_entry_count": len(positives),
        "negative_case_count": len(negatives),
        "positive": positives,
        "negative": negatives,
        "rule": "EVERY_CHAT_ENTERS_AT_STAGE_0_AND_FAST_FORWARDS_ONLY_AFTER_VALIDATION",
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    (outdir / "CONCEPT_AGENT_FULL_WORKFLOW_REENTRY_ACCEPTANCE_V1.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return proof



def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Blocked("CURRENT_ENTRY_JSON_INVALID:" + str(path)) from exc
    if not isinstance(value, dict):
        raise Blocked("CURRENT_ENTRY_OBJECT_REQUIRED:" + str(path))
    return value


def _require_sha(value: Any, code: str) -> str:
    text = str(value or "")
    if not SHA_RE.fullmatch(text):
        raise Blocked(code)
    return text


def verify_current_entry(pointer_path: Path, current_state_path: Path, outdir: Path) -> dict[str, Any]:
    pointer = _load_json(pointer_path)
    current = _load_json(current_state_path)

    if pointer.get("contract") != "PFERDE_ATELIER_CONCEPT_AGENT_WORK_BINDING_POINTER_V1":
        raise Blocked("CURRENT_POINTER_CONTRACT_INVALID")
    if pointer.get("workflow") != "PFERDE_ATELIER_KONZEPT_5_CONCEPT_AGENT":
        raise Blocked("CURRENT_POINTER_WORKFLOW_INVALID")
    if pointer.get("publish_allowed") is not False or pointer.get("cross_chat_transport_required") is not True:
        raise Blocked("CURRENT_POINTER_FLAGS_INVALID")

    batch = _require_sha(pointer.get("batch_sha256"), "CURRENT_BATCH_SHA_INVALID")
    count = pointer.get("item_count")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise Blocked("CURRENT_ITEM_COUNT_INVALID")

    ca = current.get("concept_agent_current_batch")
    if not isinstance(ca, dict):
        raise Blocked("CURRENT_CONCEPT_AGENT_BATCH_MISSING")
    if ca.get("workflow") != "PFERDE_ATELIER_KONZEPT_5_CONCEPT_AGENT":
        raise Blocked("CURRENT_CONCEPT_AGENT_WORKFLOW_INVALID")
    if ca.get("batch_sha256") != batch or ca.get("item_count") != count:
        raise Blocked("CURRENT_POINTER_STATE_BINDING_MISMATCH")
    if ca.get("publish_allowed") is not False:
        raise Blocked("CURRENT_STATE_PUBLISH_INVALID")

    completed: list[str] = []

    if ca.get("intake_status") == "PASS":
        _require_sha(pointer.get("intake_sha256"), "CURRENT_INTAKE_SHA_INVALID")
        completed.append("INTAKE")
    else:
        next_stage = "INTAKE"
        proof = {
            "contract": ENTRY_PROOF_CONTRACT,
            "status": "PASS",
            "batch_sha256": batch,
            "workflow_entry": "ALWAYS_FROM_STAGE_0",
            "fast_forward_mode": "VALIDATE_ONLY",
            "validated_completed_stages": completed,
            "next_stage": next_stage,
            "chat_may_choose_stage": False,
            "source": "REAL_CURRENT_STATE",
            "publish_allowed": False,
        }
        proof["proof_sha256"] = stable(proof)
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "CONCEPT_AGENT_CURRENT_ENTRY_PROOF.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return proof

    research_pass = ca.get("research_binding_status") == "PASS"
    if research_pass:
        _require_sha(pointer.get("research_binding_sha256"), "CURRENT_RESEARCH_BINDING_SHA_INVALID")
        completed.extend(["RESEARCH", "RESEARCH_BOUND"])
    else:
        next_stage = "RESEARCH"
        proof = {
            "contract": ENTRY_PROOF_CONTRACT,
            "status": "PASS",
            "batch_sha256": batch,
            "workflow_entry": "ALWAYS_FROM_STAGE_0",
            "fast_forward_mode": "VALIDATE_ONLY",
            "validated_completed_stages": completed,
            "next_stage": next_stage,
            "chat_may_choose_stage": False,
            "source": "REAL_CURRENT_STATE",
            "publish_allowed": False,
        }
        proof["proof_sha256"] = stable(proof)
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "CONCEPT_AGENT_CURRENT_ENTRY_PROOF.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return proof

    authoring_pass = ca.get("authoring_binding_status") == "PASS"
    if authoring_pass:
        _require_sha(pointer.get("authoring_bindings_file_sha256"), "CURRENT_AUTHORING_BINDING_SHA_INVALID")
        _require_sha(pointer.get("cross_chat_transport_sha256"), "CURRENT_TRANSPORT_SHA_INVALID")
        _require_sha(pointer.get("cross_chat_transport_binding_sha256"), "CURRENT_TRANSPORT_BINDING_SHA_INVALID")
        if ca.get("cross_chat_transport_sha256") != pointer.get("cross_chat_transport_sha256"):
            raise Blocked("CURRENT_TRANSPORT_POINTER_STATE_MISMATCH")
        completed.append("AUTHORING_BOUND")
    else:
        next_stage = "AUTHORING_BOUND"
        proof = {
            "contract": ENTRY_PROOF_CONTRACT,
            "status": "PASS",
            "batch_sha256": batch,
            "workflow_entry": "ALWAYS_FROM_STAGE_0",
            "fast_forward_mode": "VALIDATE_ONLY",
            "validated_completed_stages": completed,
            "next_stage": next_stage,
            "chat_may_choose_stage": False,
            "source": "REAL_CURRENT_STATE",
            "publish_allowed": False,
        }
        proof["proof_sha256"] = stable(proof)
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "CONCEPT_AGENT_CURRENT_ENTRY_PROOF.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return proof

    body_count = ca.get("article_bodies_completed")
    lt_count = ca.get("languagetool_6_8_completed")
    ppm_count = ca.get("ppm_6_7_9_completed")
    next_article = ca.get("next_article_index")
    for name, value in (("ARTICLE", body_count), ("LT68", lt_count), ("PPM679", ppm_count), ("NEXT_ARTICLE", next_article)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > count:
            raise Blocked("CURRENT_" + name + "_COUNT_INVALID")
    if lt_count > body_count or ppm_count > body_count:
        raise Blocked("CURRENT_VALIDATOR_COUNT_AHEAD_OF_ARTICLES")
    if next_article != min(body_count, count):
        raise Blocked("CURRENT_NEXT_ARTICLE_INDEX_MISMATCH")

    article_stage_pass = body_count == count and lt_count == count and ppm_count == count
    if article_stage_pass:
        completed.append("ARTICLE_PRODUCTION")

    pserc = ca.get("pserc_batch_completed")
    endstempel = ca.get("endstempel_completed")
    final_file = ca.get("final_wordpress_import_file_present")
    if not all(isinstance(x, bool) for x in (pserc, endstempel, final_file)):
        raise Blocked("CURRENT_DOWNSTREAM_FLAGS_INVALID")
    if pserc and not article_stage_pass:
        raise Blocked("CURRENT_PSERC_BEFORE_ARTICLES_PASS")
    if endstempel and not pserc:
        raise Blocked("CURRENT_ENDSTEMPEL_BEFORE_PSERC")
    if final_file and not endstempel:
        raise Blocked("CURRENT_FINAL_FILE_BEFORE_ENDSTEMPEL")

    if not article_stage_pass:
        next_stage = "ARTICLE_PRODUCTION"
    elif not pserc:
        next_stage = "PSERC_PACKAGE"
    else:
        completed.append("PSERC_PACKAGE")
        if not endstempel:
            next_stage = "ENDSTEMPEL"
        else:
            completed.append("ENDSTEMPEL")
            if not final_file:
                raise Blocked("CURRENT_ENDSTEMPEL_FINAL_FILE_MISSING")
            next_stage = "COMPLETE"

    proof = {
        "contract": ENTRY_PROOF_CONTRACT,
        "status": "PASS",
        "batch_sha256": batch,
        "workflow_entry": "ALWAYS_FROM_STAGE_0",
        "fast_forward_mode": "VALIDATE_ONLY",
        "validated_completed_stages": completed,
        "next_stage": next_stage,
        "chat_may_choose_stage": False,
        "source": "REAL_CURRENT_STATE",
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "CONCEPT_AGENT_CURRENT_ENTRY_PROOF.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return proof



def verify_current_negative(pointer_path: Path, current_state_path: Path, outdir: Path) -> dict[str, Any]:
    pointer = _load_json(pointer_path)
    current = _load_json(current_state_path)
    cases: list[dict[str, Any]] = []

    def expect_block(name: str, mutate_pointer=None, mutate_current=None) -> None:
        p = json.loads(json.dumps(pointer))
        s = json.loads(json.dumps(current))
        if mutate_pointer is not None:
            mutate_pointer(p)
        if mutate_current is not None:
            mutate_current(s)
        tmp = outdir / ("case-" + name)
        tmp.mkdir(parents=True, exist_ok=True)
        pp = tmp / "pointer.json"
        sp = tmp / "current.json"
        pp.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        sp.write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        try:
            verify_current_entry(pp, sp, tmp)
        except Blocked as exc:
            cases.append({"case": name, "blocked": True, "reason": str(exc)})
        else:
            raise Blocked("REAL_CURRENT_NEGATIVE_NOT_BLOCKED:" + name)

    expect_block(
        "batch-mismatch",
        mutate_current=lambda s: s["concept_agent_current_batch"].__setitem__(
            "batch_sha256", "0" * 64
        ),
    )
    expect_block(
        "transport-hash-mismatch",
        mutate_current=lambda s: s["concept_agent_current_batch"].__setitem__(
            "cross_chat_transport_sha256", "0" * 64
        ),
    )
    expect_block(
        "skip-article-index",
        mutate_current=lambda s: s["concept_agent_current_batch"].__setitem__(
            "next_article_index", 5
        ),
    )
    expect_block(
        "fake-pserc-before-articles",
        mutate_current=lambda s: s["concept_agent_current_batch"].__setitem__(
            "pserc_batch_completed", True
        ),
    )
    expect_block(
        "fake-endstempel-before-pserc",
        mutate_current=lambda s: s["concept_agent_current_batch"].__setitem__(
            "endstempel_completed", True
        ),
    )
    expect_block(
        "fake-final-file-before-endstempel",
        mutate_current=lambda s: s["concept_agent_current_batch"].__setitem__(
            "final_wordpress_import_file_present", True
        ),
    )
    expect_block(
        "publish-true",
        mutate_current=lambda s: s["concept_agent_current_batch"].__setitem__(
            "publish_allowed", True
        ),
    )

    proof = {
        "contract": "CONCEPT_AGENT_REAL_CURRENT_ENTRY_NEGATIVE_V1",
        "status": "PASS",
        "case_count": len(cases),
        "cases": cases,
        "source": "REAL_CURRENT_STATE_MUTATION_TEST",
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "CONCEPT_AGENT_REAL_CURRENT_ENTRY_NEGATIVE_V1.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return proof



STAGE_ROUTE_CONTRACT = "CONCEPT_AGENT_STAGE_ROUTE_V1"
STAGE_ROUTES = {
    "INTAKE": {
        "authority": "EXISTING_CONCEPT_AGENT_INTAKE",
        "entry_ref": "concept_agent/intake_bridge.py",
        "allowed_operation": "PREPARE_INTAKE_ONLY",
    },
    "RESEARCH": {
        "authority": "EXISTING_CONCEPT_AGENT_RESEARCH",
        "entry_ref": "CONCEPT_AGENT_RESEARCH_PROCESS",
        "allowed_operation": "RESEARCH_CURRENT_BOUND_ITEM_ONLY",
    },
    "RESEARCH_BOUND": {
        "authority": "EXISTING_CONCEPT_AGENT_RESEARCH_BINDING",
        "entry_ref": "concept_agent/intake_bridge.py:bind_research",
        "allowed_operation": "BIND_EXISTING_RESEARCH_ONLY",
    },
    "AUTHORING_BOUND": {
        "authority": "CURRENT_CONCEPT_AGENT_PRODUCTION_BINDING",
        "entry_ref": "concept_agent/production_bridge.py",
        "allowed_operation": "BIND_AUTHORING_AND_LINKS_ONLY",
    },
    "ARTICLE_PRODUCTION": {
        "authority": "CURRENT_CONCEPT_AGENT_PROGRESS_GUARD",
        "entry_ref": "concept_agent/progress_guard.py",
        "allowed_operation": "EXECUTE_ONLY_HASH_BOUND_CURRENT_ACTION",
    },
    "PSERC_PACKAGE": {
        "authority": "EXISTING_PSERC_PIPELINE",
        "entry_ref": "PSERC_EXISTING_PRODUCTION_PACKAGE_ROUTE",
        "allowed_operation": "BUILD_PSERC_PACKAGE_ONLY",
    },
    "ENDSTEMPEL": {
        "authority": "EXISTING_CONCEPT_AGENT_ENDSTEMPEL",
        "entry_ref": "concept_agent/endstempel_bridge.py",
        "allowed_operation": "ENDSTEMPEL_ONLY",
    },
    "COMPLETE": {
        "authority": "NONE",
        "entry_ref": "NONE",
        "allowed_operation": "NO_WORK_ALREADY_COMPLETE",
    },
}


def stage_route_from_entry_proof(proof: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(proof, dict) or proof.get("contract") != ENTRY_PROOF_CONTRACT or proof.get("status") != "PASS":
        raise Blocked("ENTRY_PROOF_INVALID_FOR_ROUTE")
    if proof.get("workflow_entry") != "ALWAYS_FROM_STAGE_0" or proof.get("fast_forward_mode") != "VALIDATE_ONLY":
        raise Blocked("ENTRY_PROOF_ROUTE_POLICY_INVALID")
    if proof.get("chat_may_choose_stage") is not False or proof.get("publish_allowed") is not False:
        raise Blocked("ENTRY_PROOF_ROUTE_FLAGS_INVALID")
    stage = str(proof.get("next_stage") or "")
    route = STAGE_ROUTES.get(stage)
    if route is None:
        raise Blocked("NEXT_STAGE_ROUTE_UNKNOWN:" + stage)
    proof_sha = str(proof.get("proof_sha256") or "")
    if not SHA_RE.fullmatch(proof_sha):
        raise Blocked("ENTRY_PROOF_HASH_INVALID_FOR_ROUTE")
    proof_core = dict(proof)
    proof_core.pop("proof_sha256", None)
    if proof_sha != stable(proof_core):
        raise Blocked("ENTRY_PROOF_HASH_MISMATCH_FOR_ROUTE")
    terminal = stage == "COMPLETE"
    ticket = {
        "contract": STAGE_ROUTE_CONTRACT,
        "status": "PASS",
        "batch_sha256": proof["batch_sha256"],
        "entry_proof_sha256": proof_sha,
        "validated_completed_stages": proof.get("validated_completed_stages", []),
        "next_stage": stage,
        "authority": route["authority"],
        "entry_ref": route["entry_ref"],
        "allowed_operation": route["allowed_operation"],
        "chat_may_choose_stage": False,
        "alternate_route_allowed": False,
        "publish_allowed": False,
        "bound_worker": None if terminal else "BOUND_CHAT_WORKER",
        "continuation_required": not terminal,
        "worker_must_execute_allowed_operation_immediately": not terminal,
        "worker_return_must_reenter_full_workflow_gate": not terminal,
        "handoff_is_terminal": terminal,
        "same_bound_worker_must_continue_without_return": not terminal,
    }
    if terminal:
        ticket["process_trigger"] = None
    else:
        trigger_core = {
            "contract": "CONCEPT_AGENT_BOUND_STAGE_PROCESS_TRIGGER_V1",
            "batch_sha256": proof["batch_sha256"],
            "entry_proof_sha256": proof_sha,
            "stage": stage,
            "worker": "BOUND_CHAT_WORKER",
            "authority": route["authority"],
            "entry_ref": route["entry_ref"],
            "allowed_operation": route["allowed_operation"],
            "exactly_once_for_stage": True,
            "return_required": True,
            "return_to": "concept_agent/full_workflow_gate.py",
            "handoff_is_terminal": False,
            "same_bound_worker_must_continue_without_return": True,
            "publish_allowed": False,
        }
        ticket["process_trigger"] = dict(trigger_core)
        ticket["process_trigger"]["trigger_sha256"] = stable(trigger_core)
    ticket["route_sha256"] = stable(ticket)
    return ticket


def write_stage_route(entry_proof_path: Path, out_path: Path) -> dict[str, Any]:
    proof = _load_json(entry_proof_path)
    ticket = stage_route_from_entry_proof(proof)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(ticket, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return ticket


def simulate_route_matrix(outdir: Path) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    batch = sim_hash("route-matrix-batch", "x" * 64)
    positive = []
    negative = []
    for stage_count in range(len(STAGES) + 1):
        state = build_to(batch, 3, stage_count)
        entry = enter(state)
        ticket = stage_route_from_entry_proof(entry)
        expected = STAGES[stage_count] if stage_count < len(STAGES) else "COMPLETE"
        if ticket["next_stage"] != expected:
            raise Blocked("ROUTE_MATRIX_WRONG_STAGE:" + expected)
        if ticket["chat_may_choose_stage"] is not False or ticket["alternate_route_allowed"] is not False:
            raise Blocked("ROUTE_MATRIX_NOT_HARD_BOUND:" + expected)
        positive.append({
            "next_stage": expected,
            "authority": ticket["authority"],
            "allowed_operation": ticket["allowed_operation"],
            "status": "PASS",
        })

        bad = json.loads(json.dumps(entry))
        bad["next_stage"] = "COMPLETE" if expected != "COMPLETE" else "INTAKE"
        # Keep the old proof hash on purpose; route must reject the forged ticket source.
        try:
            stage_route_from_entry_proof(bad)
        except Blocked as exc:
            negative.append({"case": "forged-next-stage-" + expected, "blocked": True, "reason": str(exc)})
        else:
            # A forged proof with stale hash must never be accepted.
            if bad.get("proof_sha256") == stable({k:v for k,v in bad.items() if k!="proof_sha256"}):
                raise Blocked("ROUTE_MATRIX_TEST_SETUP_INVALID")
            raise Blocked("ROUTE_MATRIX_FORGED_STAGE_NOT_BLOCKED:" + expected)

    proof = {
        "contract": "CONCEPT_AGENT_STAGE_ROUTE_MATRIX_V1",
        "status": "PASS",
        "positive_count": len(positive),
        "negative_count": len(negative),
        "positive": positive,
        "negative": negative,
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    (outdir / "CONCEPT_AGENT_STAGE_ROUTE_MATRIX_V1.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return proof


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("simulate-all-entries")
    p.add_argument("--out", required=True)
    p = sub.add_parser("verify-current-entry")
    p.add_argument("--pointer", required=True)
    p.add_argument("--current-state", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("verify-current-negative")
    p.add_argument("--pointer", required=True)
    p.add_argument("--current-state", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("stage-route")
    p.add_argument("--entry-proof", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("simulate-route-matrix")
    p.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "verify-current-entry":
            proof = verify_current_entry(Path(args.pointer), Path(args.current_state), Path(args.out))
            print(json.dumps({
                "ok": True,
                "status": proof["status"],
                "validated_completed_stages": proof["validated_completed_stages"],
                "next_stage": proof["next_stage"],
                "proof_sha256": proof["proof_sha256"],
            }, sort_keys=True))
            return 0
        if args.cmd == "verify-current-negative":
            proof = verify_current_negative(Path(args.pointer), Path(args.current_state), Path(args.out))
            print(json.dumps({
                "ok": True,
                "status": proof["status"],
                "negative_case_count": proof["case_count"],
                "proof_sha256": proof["proof_sha256"],
            }, sort_keys=True))
            return 0
        if args.cmd == "stage-route":
            ticket = write_stage_route(Path(args.entry_proof), Path(args.out))
            print(json.dumps({
                "ok": True,
                "status": ticket["status"],
                "next_stage": ticket["next_stage"],
                "authority": ticket["authority"],
                "route_sha256": ticket["route_sha256"],
            }, sort_keys=True))
            return 0
        if args.cmd == "simulate-route-matrix":
            proof = simulate_route_matrix(Path(args.out))
            print(json.dumps({
                "ok": True,
                "status": proof["status"],
                "positive_count": proof["positive_count"],
                "negative_count": proof["negative_count"],
                "proof_sha256": proof["proof_sha256"],
            }, sort_keys=True))
            return 0
        proof = simulate_all_entries(Path(args.out))
        print(json.dumps({
            "ok": True,
            "status": proof["status"],
            "positive_entry_count": proof["positive_entry_count"],
            "negative_case_count": proof["negative_case_count"],
            "proof_sha256": proof["proof_sha256"],
        }, sort_keys=True))
        return 0
    except Blocked as exc:
        print("CONCEPT_AGENT_FULL_WORKFLOW_GATE_BLOCKED:" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
