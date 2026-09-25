#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, re, sys
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SYSTEM4 = REPO / "isolated_system4"
if str(SYSTEM4) not in sys.path:
    sys.path.insert(0, str(SYSTEM4))

import authoring_contract  # type: ignore
import machine_point0  # type: ignore
import production_checks  # type: ignore
import intake_bridge
import progress_guard

CONTRACT = "CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1"
CHECKPOINT_CONTRACT = progress_guard.CHECKPOINT_CONTRACT
FORBIDDEN_RESEARCH_HOST = "pferde-atelier.de"

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

def _host(url: str) -> str:
    return (urlparse(url).hostname or "").strip().rstrip(".").casefold()

def _forbidden_own_domain(url: str) -> bool:
    host = _host(url)
    return host == FORBIDDEN_RESEARCH_HOST or host.endswith("." + FORBIDDEN_RESEARCH_HOST)

def _validate_research_bound(intake: dict, bound: dict) -> list[dict]:
    if bound.get("contract") != intake_bridge.RESEARCH_BOUND_CONTRACT:
        raise Blocked("RESEARCH_BOUND_CONTRACT_INVALID")
    core = dict(bound)
    declared = core.pop("research_binding_sha256", None)
    if not isinstance(declared, str) or declared != stable(core):
        raise Blocked("RESEARCH_BOUND_HASH_MISMATCH")
    if bound.get("batch_sha256") != intake.get("batch_sha256") or bound.get("item_count") != intake.get("item_count"):
        raise Blocked("RESEARCH_BOUND_BATCH_OR_COUNT_MISMATCH")
    if bound.get("draft_allowed") is not True or bound.get("publish_allowed") is not False:
        raise Blocked("RESEARCH_BOUND_FLAGS_INVALID")
    rows = bound.get("items")
    if not isinstance(rows, list) or len(rows) != intake["item_count"]:
        raise Blocked("RESEARCH_BOUND_ITEMS_INVALID")
    checked = []
    for index, (article, row) in enumerate(zip(intake["items"], rows)):
        if not isinstance(row, dict) or row.get("item_index") != index or row.get("plan_slot") != article["plan_slot"]:
            raise Blocked(f"RESEARCH_BOUND_ITEM_IDENTITY_MISMATCH:{index}")
        if row.get("article_identity_sha256") != article["identity_sha256"]:
            raise Blocked(f"RESEARCH_BOUND_ARTICLE_HASH_MISMATCH:{index}")
        sources = row.get("sources")
        if not isinstance(sources, list) or not sources or row.get("source_pool_sha256") != stable(sources):
            raise Blocked(f"RESEARCH_BOUND_SOURCE_POOL_INVALID:{index}")
        for sidx, source in enumerate(sources):
            if not isinstance(source, dict):
                raise Blocked(f"RESEARCH_SOURCE_INVALID:{index}:{sidx}")
            url = str(source.get("source_url") or "")
            if _forbidden_own_domain(url):
                raise Blocked(f"RESEARCH_SOURCE_OWN_DOMAIN_FORBIDDEN:{index}:{sidx}")
            evidence = source.get("evidence")
            digest = source.get("snapshot_sha256")
            if not isinstance(evidence, str) or hashlib.sha256(evidence.encode("utf-8")).hexdigest() != digest:
                raise Blocked(f"RESEARCH_SOURCE_EVIDENCE_HASH_MISMATCH:{index}:{sidx}")
        checked.append(row)
    return checked

def build(snapshot: dict, intake: dict, research_bound: dict) -> dict:
    expected_intake = intake_bridge.prepare(snapshot)
    if intake != expected_intake:
        raise Blocked("CURRENT_INTAKE_NOT_EXACT_SNAPSHOT_DERIVATION")
    rows = _validate_research_bound(intake, research_bound)

    package = (REPO / production_checks.PPM_PACKAGE_REL).resolve()
    if not package.is_file():
        raise Blocked("PPM679_PACKAGE_MISSING")
    if production_checks.file_sha256(package) != production_checks.PPM_PACKAGE_SHA256:
        raise Blocked("PPM679_PACKAGE_HASH_MISMATCH")

    static_rules = authoring_contract._static_ppm_rules(package)
    article_types = sorted({str(item["article_type"]) for item in intake["items"]})
    type_authority = {
        article_type: authoring_contract._type_definition(package, article_type)
        for article_type in article_types
    }

    items = []
    for index, (article, research) in enumerate(zip(intake["items"], rows)):
        plan = machine_point0._prewrite_plan(REPO, article)
        prewrite = machine_point0.point0_snapshot.prewrite_from_plan(article, index, plan)
        links = plan["quality_binding"].get("link_bindings")
        if not isinstance(links, list) or len(links) != 3 or len({x.get("role") for x in links}) != 3:
            raise Blocked(f"CURRENT_LINK_BINDING_INVALID:{index}")
        item = {
            "item_index": index,
            "identity": {
                k: article[k]
                for k in ("item_index", "title", "target_keyword", "category", "article_type", "plan_slot", "identity_sha256")
            },
            "research_bound": research,
            "prewrite_binding": prewrite,
            "production_plan_item": plan,
            "link_bindings": links,
            "authoring_authority": {
                "ppm_version": production_checks.PPM_VERSION,
                "ppm_package_sha256": production_checks.PPM_PACKAGE_SHA256,
                "structure_contract": static_rules["structure"],
                "static_validator_constants": static_rules["constants"],
                "article_type_definition": type_authority[article["article_type"]],
            },
            "forbidden_inputs": {
                "historical_article_content": True,
                "recovery_article_content": True,
                "historical_production_routes": True,
                "free_rule_lookup": True,
                "free_link_selection": True,
                "own_domain_research": FORBIDDEN_RESEARCH_HOST,
            },
        }
        item["bound_work_sha256"] = stable(item)
        items.append(item)

    result = {
        "contract": CONTRACT,
        "status": "AUTHORING_READY",
        "batch_sha256": intake["batch_sha256"],
        "item_count": len(items),
        "source_intake_sha256": intake["intake_sha256"],
        "source_research_binding_sha256": research_bound["research_binding_sha256"],
        "quality_authority": {
            "source": "EXISTING_PPM_6_7_9_AND_EXISTING_PORTAL_STRUCTURE",
            "ppm_version": production_checks.PPM_VERSION,
            "ppm_package_ref": production_checks.PPM_PACKAGE_REL,
            "ppm_package_sha256": production_checks.PPM_PACKAGE_SHA256,
            "static_authority_sha256": stable({"static_rules": static_rules, "type_authority": type_authority}),
            "rule_search_during_production": False,
            "links_are_prebound": True,
        },
        "route_policy": {
            "text_start_modified": False,
            "current_snapshot_only": True,
            "legacy_runtime_inbox_forbidden": True,
            "legacy_parent_start_forbidden": True,
            "historical_concept_agent_runner_forbidden": True,
            "historical_article_reference_forbidden": True,
            "recovery_article_reference_forbidden": True,
            "own_domain_research_forbidden": FORBIDDEN_RESEARCH_HOST,
            "quality_core_changed": False,
            "publish_allowed": False,
        },
        "progress_policy": {
            "checkpoint_required_before_every_action": True,
            "checkpoint_contract": CHECKPOINT_CONTRACT,
            "universal_reentry_decision_required_before_every_action": True,
            "universal_reentry_gate_ref": "concept_agent/universal_reentry_guard.py",
            "outer_stage_gate_ref": "concept_agent/full_workflow_gate.py",
            "allowed_action_is_hash_bound": True,
            "durable_draft_bytes_required_in_checkpoint": True,
            "batch_draft_attach_forbidden": True,
            "single_checkpoint_selected_article_only": True,
            "same_article_on_repair": True,
            "resume_from_last_checkpoint_only": True,
            "missing_or_mismatched_checkpoint": "STOP",
        },
        "items": items,
        "publish_allowed": False,
    }
    result["binding_sha256"] = stable(result)
    return result

def initial_checkpoint(binding: dict) -> dict:
    core = dict(binding)
    declared = core.pop("binding_sha256", None)
    if binding.get("contract") != CONTRACT or declared != stable(core):
        raise Blocked("PRODUCTION_BINDING_INVALID")
    state = {
        "contract": CHECKPOINT_CONTRACT,
        "batch_sha256": binding["batch_sha256"],
        "production_binding_sha256": binding["binding_sha256"],
        "item_count": binding["item_count"],
        "status": "IN_PROGRESS",
        "phase": "AUTHORING_REQUIRED",
        "next_item_index": 0,
        "completed_items": [],
        "current_item": None,
        "previous_checkpoint_sha256": None,
        "drafts": [],
        "publish_allowed": False,
    }
    state["allowed_action"] = progress_guard.expected_action(binding, state)
    state["checkpoint_sha256"] = stable(state)
    return state

def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main(argv: list[str]) -> int:
    try:
        if len(argv) != 7 or argv[1] != "bind":
            raise Blocked("USE: production_bridge.py bind SNAPSHOT INTAKE RESEARCH_BOUND OUT_BINDING OUT_CHECKPOINT")
        result = build(load(Path(argv[2])), load(Path(argv[3])), load(Path(argv[4])))
        checkpoint = initial_checkpoint(result)
        write_json(Path(argv[5]), result)
        write_json(Path(argv[6]), checkpoint)
        print(json.dumps({
            "status": "CONCEPT_AGENT_CURRENT_PRODUCTION_READY",
            "batch_sha256": result["batch_sha256"],
            "item_count": result["item_count"],
            "binding_sha256": result["binding_sha256"],
            "checkpoint_sha256": checkpoint["checkpoint_sha256"],
            "publish_allowed": False,
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print("CONCEPT_AGENT_PRODUCTION_BIND_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
