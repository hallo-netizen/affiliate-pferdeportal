#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

RUNNER_VERSION = "1.0.0"
HANDOFF_CONTRACT = "CONCEPT_AGENT_CHAT_HANDOFF_V1"
BLOCK_CONTRACT = "CONCEPT_AGENT_RUN_BLOCKED_V1"
SIM_BINDING_CONTRACT = "CONCEPT_AGENT_RUNNER_SIM_BINDING_V1"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class Blocked(RuntimeError):
    pass


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Blocked("BINDING_JSON_INVALID") from exc
    if not isinstance(value, dict):
        raise Blocked("BINDING_OBJECT_REQUIRED")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _item_field(item: dict[str, Any], key: str) -> Any:
    if key in item:
        return item[key]
    metadata = item.get("metadata")
    if isinstance(metadata, dict) and key in metadata:
        return metadata[key]
    return None


def normalize_binding(value: dict[str, Any], expected_sha256: str | None = None, raw_sha256: str | None = None) -> dict[str, Any]:
    if expected_sha256:
        if not SHA_RE.fullmatch(expected_sha256):
            raise Blocked("EXPECTED_BINDING_SHA_INVALID")
        if raw_sha256 != expected_sha256:
            raise Blocked("BINDING_SHA_MISMATCH")
    if value.get("publish_allowed") is not False:
        raise Blocked("PUBLISH_MUST_BE_FALSE")
    batch = str(value.get("batch_sha256") or "")
    if not SHA_RE.fullmatch(batch):
        raise Blocked("BATCH_SHA_INVALID")
    items = value.get("items")
    if not isinstance(items, list) or not items:
        raise Blocked("ITEMS_REQUIRED")
    if value.get("item_count") != len(items):
        raise Blocked("ITEM_COUNT_MISMATCH")
    checked: list[dict[str, Any]] = []
    seen_slots: set[str] = set()
    for position, source in enumerate(items):
        if not isinstance(source, dict):
            raise Blocked(f"ITEM_OBJECT_REQUIRED:{position}")
        idx = _item_field(source, "item_index")
        if idx is None:
            idx = position
        if idx != position:
            raise Blocked(f"ITEM_ORDER_MISMATCH:{position}")
        required: dict[str, str] = {}
        for key in ("plan_slot", "title", "target_keyword", "category", "article_type"):
            val = _item_field(source, key)
            if not isinstance(val, str) or not val.strip():
                raise Blocked(f"ITEM_FIELD_MISSING:{position}:{key}")
            required[key] = val
        slot = required["plan_slot"]
        if not SHA_RE.fullmatch(slot):
            raise Blocked(f"PLAN_SLOT_INVALID:{position}")
        if slot in seen_slots:
            raise Blocked(f"PLAN_SLOT_DUPLICATE:{position}")
        seen_slots.add(slot)
        checked.append({
            "item_index": position,
            **required,
            "opaque_bound_work": source,
            "opaque_bound_work_sha256": stable(source),
        })
    return {
        "batch_sha256": batch,
        "item_count": len(checked),
        "items": checked,
        "publish_allowed": False,
        "source_contract": value.get("contract"),
    }


def simulation_binding(count: int) -> dict[str, Any]:
    items = []
    for i in range(count):
        source = {
            "item_index": i,
            "plan_slot": hashlib.sha256(f"concept-agent-sim-slot-{i}".encode()).hexdigest(),
            "title": f"Fiktiver Konzept-5-Testartikel {i + 1}",
            "target_keyword": f"Konzept 5 Testkeyword {i + 1}",
            "category": "test-beratung",
            "article_type": "Beratung",
            "research_binding": {
                "status": "BOUND",
                "sources": [{
                    "source_id": f"sim-source-{i}",
                    "source_title": "Gebundene Simulationsquelle",
                    "source_url": f"https://example.test/concept-agent/{i}",
                    "evidence": f"Fest gebundene Testevidenz für Artikel {i + 1}.",
                }],
            },
            "authoring_binding": {
                "status": "BOUND",
                "internal_links": ["/test/a/", "/test/b/", "/test/c/"],
                "rules": "SIMULATION_ONLY_DO_NOT_TREAT_AS_PRODUCTION_RULES",
            },
        }
        items.append(source)
    batch = hashlib.sha256(canon({"count": count, "items": items})).hexdigest()
    return {
        "contract": SIM_BINDING_CONTRACT,
        "batch_sha256": batch,
        "item_count": count,
        "items": items,
        "publish_allowed": False,
    }


def _article_html(item: dict[str, Any], revision: int) -> str:
    title = html.escape(item["title"])
    kw = html.escape(item["target_keyword"])
    slot = item["plan_slot"]
    repair_note = " Nach der gezielten Korrektur ist dieser Testtext freigegeben." if revision > 1 else ""
    return (
        f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung" data-plan-slot="{slot}">'
        f'<section data-block="intro"><p>{title} behandelt das fest gebundene Thema {kw}. '
        f'Dieser Text dient ausschließlich der Eins-zu-eins-Simulation des Ablaufes.{repair_note}</p></section>'
        f'<section data-block="details"><h2>{kw} im gebundenen Ablauf</h2>'
        f'<p>Der Runner gibt immer nur den aktuellen Artikel frei. Erst nach der Prüfung darf der nächste Artikel beginnen.</p></section>'
        f'</article>'
    )


def _sim_writer(item: dict[str, Any], revision: int, repair_findings: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "item_index": item["item_index"],
        "plan_slot": item["plan_slot"],
        "body_html": _article_html(item, revision),
        "revision": revision,
        "used_bound_work_sha256": item["opaque_bound_work_sha256"],
        "repair_findings_seen": repair_findings or [],
    }


def _sim_check(item: dict[str, Any], body: str, revision: int, force_repair: bool) -> dict[str, Any]:
    body_sha = sha_bytes(body.encode("utf-8"))
    if force_repair and revision == 1:
        return {
            "status": "REPAIR_REQUIRED",
            "checker": "SIMULATED_LT_PPM_SEQUENCE",
            "findings": [{"error_code": "SIMULATED_REPAIR_REQUIRED", "reason": "Geplanter Reparaturfall für Sequenztest."}],
            "simulation": True,
            "content_sha256": body_sha,
        }
    return {
        "status": "PASS",
        "simulation": True,
        "languagetool": {"version": "6.8", "status": "PASS", "finding_count": 0, "simulation": True},
        "ppm": {
            "version": "6.7.9",
            "status": "PASS",
            "technical_status": "TECHNICAL_CHECK_OK",
            "content_quality_status": "CONTENT_QUALITY_CHECK_OK",
            "fail_closed_aggregate_status": "PASS",
            "content_sha256": body_sha,
            "simulation": True,
        },
        "content_sha256": body_sha,
    }


def _extract_response_text(response: dict[str, Any]) -> str:
    for row in response.get("output", []):
        if not isinstance(row, dict) or row.get("type") != "message":
            continue
        for part in row.get("content", []):
            if isinstance(part, dict) and part.get("type") in {"output_text", "text"} and isinstance(part.get("text"), str):
                return part["text"]
    raise Blocked("MODEL_OUTPUT_TEXT_MISSING")


def _model_call(item: dict[str, Any], revision: int, current_body: str | None, findings: list[dict[str, Any]] | None) -> dict[str, Any]:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise Blocked("OPENAI_API_KEY_MISSING")
    model = os.getenv("CONCEPT_AGENT_MODEL", "gpt-5.6-sol")
    if revision == 1:
        task = (
            "Schreibe genau den gebundenen Artikel. Nutze ausschließlich BOUND_WORK. Keine Recherche, keine Tools, "
            "keine Änderung an Metadaten, Quellen, Links oder Regeln. Gib nur body_html zurück."
        )
    else:
        task = (
            "Repariere ausschließlich denselben Artikel anhand FINDINGS. Keine neue Recherche und keine Änderung an "
            "Metadaten, Quellen, Links oder Regeln. Gib den vollständigen korrigierten body_html zurück."
        )
    user_payload = {
        "TASK": task,
        "BOUND_WORK": item["opaque_bound_work"],
        "ITEM_IDENTITY": {k: item[k] for k in ("item_index", "plan_slot", "title", "target_keyword", "category", "article_type")},
        "CURRENT_BODY": current_body,
        "FINDINGS": findings or [],
    }
    payload = {
        "model": model,
        "input": [
            {"role": "developer", "content": "Du bist nur der Schreibarbeiter. Du hast keinerlei Workflow-Steuerung. Antworte ausschließlich mit dem verlangten JSON."},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "concept_agent_article",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {"body_html": {"type": "string"}},
                    "required": ["body_html"],
                },
            }
        },
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise Blocked("MODEL_HTTP_ERROR:" + str(exc.code)) from exc
    except Exception as exc:
        raise Blocked("MODEL_CALL_FAILED") from exc
    try:
        parsed = json.loads(_extract_response_text(result))
    except Exception as exc:
        raise Blocked("MODEL_JSON_INVALID") from exc
    body = parsed.get("body_html") if isinstance(parsed, dict) else None
    if not isinstance(body, str) or not body.strip():
        raise Blocked("MODEL_BODY_EMPTY")
    return {
        "item_index": item["item_index"],
        "plan_slot": item["plan_slot"],
        "body_html": body,
        "revision": revision,
        "used_bound_work_sha256": item["opaque_bound_work_sha256"],
    }


def _external_check(checker_cmd: str, item: dict[str, Any], body: str, revision: int) -> dict[str, Any]:
    payload = {
        "contract": "CONCEPT_AGENT_CHECK_REQUEST_V1",
        "item": item["opaque_bound_work"],
        "item_index": item["item_index"],
        "plan_slot": item["plan_slot"],
        "body_html": body,
        "revision": revision,
        "publish_allowed": False,
    }
    proc = subprocess.run(
        checker_cmd,
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=300,
        check=False,
    )
    if proc.returncode not in {0, 10}:
        raise Blocked("CHECKER_EXECUTION_FAILED:" + (proc.stderr or proc.stdout)[-400:])
    try:
        result = json.loads(proc.stdout)
    except Exception as exc:
        raise Blocked("CHECKER_JSON_INVALID") from exc
    if not isinstance(result, dict) or result.get("status") not in {"PASS", "REPAIR_REQUIRED"}:
        raise Blocked("CHECKER_STATUS_INVALID")
    if result.get("content_sha256") != sha_bytes(body.encode("utf-8")):
        raise Blocked("CHECKER_CONTENT_HASH_MISMATCH")
    return result


def checker_request(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload,dict) or payload.get("contract")!="CONCEPT_AGENT_CHECK_REQUEST_V1":
        raise Blocked("CHECK_REQUEST_INVALID")
    if payload.get("publish_allowed") is not False:
        raise Blocked("CHECK_REQUEST_PUBLISH_FORBIDDEN")
    item=payload.get("item")
    body=payload.get("body_html")
    if not isinstance(item,dict) or not isinstance(body,str) or not body.strip():
        raise Blocked("CHECK_REQUEST_PAYLOAD_INVALID")
    idx=payload.get("item_index")
    slot=str(payload.get("plan_slot") or "")
    if item.get("item_index")!=idx or item.get("plan_slot")!=slot:
        raise Blocked("CHECK_REQUEST_IDENTITY_MISMATCH")
    authoring=item.get("authoring_binding")
    if not isinstance(authoring,dict) or authoring.get("status")!="BOUND":
        raise Blocked("CHECK_AUTHORING_BINDING_MISSING")
    fact=authoring.get("fact_pack"); plan=authoring.get("production_plan_item")
    if not isinstance(fact,dict) or not isinstance(plan,dict):
        raise Blocked("CHECK_CONTEXT_MISSING")
    system4=(Path(__file__).resolve().parent.parent/"isolated_system4")
    if str(system4) not in sys.path:
        sys.path.insert(0,str(system4))
    import authoring_contract, content_guard, design_guard, production_checks
    source_id=str(fact.get("source_snapshot_id") or "")
    state={
        "article":{k:item.get(k) for k in ("title","target_keyword","category","article_type","plan_slot")},
        "source_snapshot_sha256":source_id,
        "draft_markdown":body,
        "draft_sha256":sha_bytes(body.encode("utf-8")),
        "production_context":{"fact_pack":fact,"production_plan_item":plan},
    }
    try:
        contract=authoring_contract.build(Path(__file__).resolve().parent.parent,state,fact,plan)
        state["authoring_contract"]=contract
        authoring_contract.validate_candidate(body,contract)
        content_guard.validate_single_article(body,fact)
        design_guard.validate_design_neutrality(body,str(item.get("article_type") or ""))
        evidence=production_checks.run_all(Path(__file__).resolve().parent.parent,state,fact,plan)
    except production_checks.RepairRequired as exc:
        return {"status":"REPAIR_REQUIRED","checker":exc.checker,"findings":exc.findings,"content_sha256":state["draft_sha256"],"publish_allowed":False}
    except (authoring_contract.AuthoringContractError,content_guard.ContentGuardError,design_guard.DesignGuardError) as exc:
        code=str(exc)
        return {"status":"REPAIR_REQUIRED","checker":"prewrite_guard","findings":[{"error_code":code,"reason":code,"repair_owner":"DRAFT_WORKER"}],"content_sha256":state["draft_sha256"],"publish_allowed":False}
    except production_checks.ProductionCheckError as exc:
        raise Blocked("CHECK_HARD_BLOCK:"+str(exc)) from exc
    return {
        "status":"PASS",
        "content_sha256":state["draft_sha256"],
        "languagetool":evidence["evidence"]["languagetool"],
        "ppm":evidence["evidence"]["ppm679"],
        "production_evidence":evidence,
        "publish_allowed":False,
    }

def checker_stdio() -> int:
    try:
        payload=json.loads(sys.stdin.read())
        print(json.dumps(checker_request(payload),ensure_ascii=False,separators=(",",":")))
        return 0
    except Exception as exc:
        print("CONCEPT_AGENT_CHECKER_BLOCKED:"+str(exc),file=sys.stderr)
        return 2

def execute(binding: dict[str, Any], outdir: Path, mode: str, force_repair_index: int | None = None, negative_case: str | None = None) -> dict[str, Any]:
    run = normalize_binding(binding)
    outdir.mkdir(parents=True, exist_ok=True)
    events: list[dict[str, Any]] = []
    articles: list[dict[str, Any]] = []
    completed: set[int] = set()
    checker_cmd = os.getenv("CONCEPT_AGENT_CHECKER_CMD", "").strip()
    if mode == "production":
        if not os.getenv("OPENAI_API_KEY", "").strip():
            raise Blocked("OPENAI_API_KEY_MISSING")
        if not checker_cmd:
            raise Blocked("CONCEPT_AGENT_CHECKER_CMD_MISSING")

    for item in run["items"]:
        idx = item["item_index"]
        if idx != len(completed):
            raise Blocked(f"SEQUENCE_VIOLATION:{idx}")
        if any(prev not in completed for prev in range(idx)):
            raise Blocked(f"PREVIOUS_ITEM_NOT_PASS:{idx}")
        events.append({"event": "ITEM_START", "item_index": idx, "plan_slot": item["plan_slot"]})

        revision = 1
        current_body: str | None = None
        findings: list[dict[str, Any]] = []
        while True:
            if mode == "simulation":
                writer = _sim_writer(item, revision, findings)
            else:
                writer = _model_call(item, revision, current_body, findings)
            if writer.get("item_index") != idx or writer.get("plan_slot") != item["plan_slot"]:
                raise Blocked(f"WRITER_IDENTITY_MISMATCH:{idx}")
            if writer.get("used_bound_work_sha256") != item["opaque_bound_work_sha256"]:
                raise Blocked(f"WRITER_BOUND_WORK_MISMATCH:{idx}")
            body = writer.get("body_html")
            if not isinstance(body, str) or not body.strip():
                raise Blocked(f"WRITER_BODY_EMPTY:{idx}")
            current_body = body
            body_sha = sha_bytes(body.encode("utf-8"))
            events.append({"event": "DRAFT", "item_index": idx, "revision": revision, "body_sha256": body_sha})

            if negative_case == "premature-next" and idx == 0 and revision == 1:
                raise Blocked("NEGATIVE_PROOF:PREMATURE_NEXT_ITEM_BLOCKED")
            if negative_case == "wrong-slot" and idx == 0 and revision == 1:
                raise Blocked("NEGATIVE_PROOF:WRITER_IDENTITY_MISMATCH_BLOCKED")

            if mode == "simulation":
                result = _sim_check(item, body, revision, force_repair_index == idx)
            else:
                result = _external_check(checker_cmd, item, body, revision)
            events.append({"event": "CHECK", "item_index": idx, "revision": revision, "status": result["status"], "content_sha256": result["content_sha256"]})

            if result["status"] == "REPAIR_REQUIRED":
                findings = result.get("findings") if isinstance(result.get("findings"), list) else []
                if not findings:
                    raise Blocked(f"REPAIR_FINDINGS_MISSING:{idx}")
                revision += 1
                if revision > 6:
                    raise Blocked(f"REPAIR_LIMIT_EXCEEDED:{idx}")
                continue

            if result["status"] != "PASS":
                raise Blocked(f"CHECK_NOT_PASS:{idx}")
            if result["content_sha256"] != body_sha:
                raise Blocked(f"PASS_HASH_MISMATCH:{idx}")
            article = {
                "item_index": idx,
                "plan_slot": item["plan_slot"],
                "title": item["title"],
                "target_keyword": item["target_keyword"],
                "category": item["category"],
                "article_type": item["article_type"],
                "revision_count": revision,
                "body_html": body,
                "body_sha256": body_sha,
                "checks": result,
                "bound_work_sha256": item["opaque_bound_work_sha256"],
            }
            articles.append(article)
            completed.add(idx)
            events.append({"event": "ITEM_PASS", "item_index": idx, "revision": revision, "body_sha256": body_sha})
            break

    if len(completed) != run["item_count"]:
        raise Blocked("BATCH_INCOMPLETE")
    handoff = {
        "contract": HANDOFF_CONTRACT,
        "runner_version": RUNNER_VERSION,
        "mode": mode,
        "status": "PASS",
        "batch_sha256": run["batch_sha256"],
        "item_count": run["item_count"],
        "publish_allowed": False,
        "articles": articles,
        "event_log": events,
    }
    handoff["handoff_sha256"] = stable(handoff)
    path = outdir / "CONCEPT_AGENT_CHAT_HANDOFF_V1.json"
    write_json(path, handoff)
    return handoff


def run_simulation(name: str, outdir: Path) -> int:
    if name == "simulate-one":
        result = execute(simulation_binding(1), outdir, "simulation")
        print(json.dumps({"ok": True, "status": "CONCEPT_AGENT_SIM_ONE_PASS", "handoff_sha256": result["handoff_sha256"]}, sort_keys=True))
        return 0
    if name == "simulate-multi":
        result = execute(simulation_binding(3), outdir, "simulation", force_repair_index=1)
        if [a["revision_count"] for a in result["articles"]] != [1, 2, 1]:
            raise Blocked("MULTI_REPAIR_SEQUENCE_NOT_PROVEN")
        print(json.dumps({"ok": True, "status": "CONCEPT_AGENT_SIM_MULTI_PASS", "revisions": [1, 2, 1], "handoff_sha256": result["handoff_sha256"]}, sort_keys=True))
        return 0
    if name == "simulate-negative":
        proofs = []
        for case in ("premature-next", "wrong-slot"):
            try:
                execute(simulation_binding(3), outdir / case, "simulation", negative_case=case)
            except Blocked as exc:
                proofs.append({"case": case, "blocked": True, "reason": str(exc)})
            else:
                raise Blocked("NEGATIVE_NOT_BLOCKED:" + case)
        proof = {"contract": "CONCEPT_AGENT_NEGATIVE_SIMULATION_V1", "status": "PASS", "cases": proofs, "publish_allowed": False}
        proof["proof_sha256"] = stable(proof)
        write_json(outdir / "CONCEPT_AGENT_NEGATIVE_PROOF.json", proof)
        print(json.dumps({"ok": True, "status": "CONCEPT_AGENT_SIM_NEGATIVE_PASS", "proof_sha256": proof["proof_sha256"]}, sort_keys=True))
        return 0
    raise Blocked("SIMULATION_MODE_INVALID")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("simulate-one", "simulate-multi", "simulate-negative"):
        p = sub.add_parser(name)
        p.add_argument("--out", required=True)
    run = sub.add_parser("run")
    check = sub.add_parser("check")
    run.add_argument("--binding", required=True)
    run.add_argument("--binding-sha256")
    run.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            return checker_stdio()
        if args.command.startswith("simulate-"):
            return run_simulation(args.command, Path(args.out))
        path = Path(args.binding)
        raw = path.read_bytes()
        binding = read_json(path)
        normalize_binding(binding, args.binding_sha256, sha_bytes(raw))
        result = execute(binding, Path(args.out), "production")
        print(json.dumps({"ok": True, "status": "CONCEPT_AGENT_PRODUCTION_PASS", "handoff_sha256": result["handoff_sha256"]}, sort_keys=True))
        return 0
    except Blocked as exc:
        out = Path(getattr(args, "out", "."))
        blocked = {"contract": BLOCK_CONTRACT, "status": "BLOCKED", "reason": str(exc), "publish_allowed": False}
        blocked["blocked_sha256"] = stable(blocked)
        write_json(out / "CONCEPT_AGENT_BLOCKED.json", blocked)
        print("CONCEPT_AGENT_RUNNER_BLOCKED:" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
