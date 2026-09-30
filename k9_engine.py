#!/usr/bin/env python3
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "state" / "ledger.json"
CURRENT_JOB = ROOT / "runtime" / "CURRENT_JOB.json"
CHAT_ENTRY = ROOT / "runtime" / "CHAT_ENTRY.json"
AUTO_CHAIN = ROOT / "runtime" / "AUTO_CHAIN.json"
CURRENT_STATE = ROOT / "CURRENT_STATE.json"
WORKER_CONTRACTS = ROOT / "contracts" / "K9_WORKER_CONTRACTS.json"
PORTAL_BINDINGS = ROOT / "contracts" / "K9_PORTAL_BINDINGS.json"
WRITING_RULES = ROOT / "contracts" / "K9_WRITING_RULES.json"
STATUS_FILE = ROOT / "state" / "STATUS.json"
WAREHOUSE = ROOT / "warehouse"
STATIONS = ("research", "write", "check", "repair")
LT68_JAR_SHA256 = "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8"
PPM679_PACKAGE_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
INTAKE_FIELDS = {"title", "target_keyword", "category", "article_type", "plan_slot"}
AUTO_CHAIN_AFTER_SUBMISSION_RULE = "DO_NOT_STOP_WHILE_AUTO_CHAIN_ACTIVE_WAIT_FOR_NEXT_SYSTEM_GENERATED_CHAT_ENTRY_OR_AUTO_CHAIN_CLOSE"
AUTO_CHAIN_ROUTING_RULE = "SYSTEM_GENERATES_NEXT_STATION_WORKER_NEVER_SELECTS_ROUTE"

class K9Error(RuntimeError):
    pass

def stable(obj):
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def orchestration_mode():
    if not AUTO_CHAIN.exists():
        return "STATION_ONLY"
    data = load_json(AUTO_CHAIN)
    if data.get("contract") != "K9_AUTO_CHAIN_V1" or data.get("status") != "ACTIVE" or data.get("publish_allowed") is not False:
        raise K9Error("AUTO_CHAIN_STATE_INVALID")
    return "AUTO_CHAIN"

def set_orchestration_mode(mode, source_run_id="manual"):
    if mode not in ("station_only", "auto_chain", "inherit"):
        raise K9Error("ORCHESTRATION_MODE_INVALID")
    if mode == "inherit":
        return {"status": "ORCHESTRATION_INHERITED", "mode": orchestration_mode()}
    if mode == "auto_chain":
        write_json(AUTO_CHAIN, {
            "contract": "K9_AUTO_CHAIN_V1",
            "status": "ACTIVE",
            "mode": "SERIAL_ONE_ITEM_EXISTING_STATIONS",
            "source_run_id": str(source_run_id),
            "routing_authority": "K9_SYSTEM_ONLY",
            "station_worker_may_select_route": False,
            "publish_allowed": False
        })
    elif AUTO_CHAIN.exists():
        AUTO_CHAIN.unlink()
    return {
        "status": "ORCHESTRATION_MODE_SET",
        "mode": orchestration_mode()
    }

def write_current_for_job(job):
    station = job["station"]
    row = job["items"][0] if job.get("items") else {}
    is_chat = station != "check"
    current = {
        "contract": "K9_CURRENT_STATE_V3",
        "role": "SOLE_CURRENT_AUTHORITY",
        "concept": "K9",
        "branch": "konzept9/greenfield-20260929",
        "status": "OPEN_CHAT_WORKER_JOB" if is_chat else "NATIVE_CHECK_RUNNING",
        "operational_mode": "EXECUTE_RUNTIME_CHAT_ENTRY_ONLY" if is_chat else "K9_NATIVE_MACHINE_CHECK",
        "active_job": {
            "job_id": job["job_id"],
            "station": station,
            "article_title": row.get("title"),
            "item_id": row.get("item_id"),
            "runtime_entry": "runtime/CHAT_ENTRY.json" if is_chat else None,
            "job_path": "runtime/CURRENT_JOB.json"
        },
        "worker_mode": "EXECUTE_ONLY_NO_SUPERVISOR_NARRATION" if is_chat else "NATIVE_MACHINE_ONLY",
        "orchestration_mode": orchestration_mode(),
        "first_open_blocker": None,
        "next_action": "EXECUTE_RUNTIME_CHAT_ENTRY" if is_chat else "RUN_NATIVE_CHECK",
        "allowed_action": "EXECUTE_RUNTIME_CHAT_ENTRY_ONLY" if is_chat else "RUN_NATIVE_CHECK_ONLY",
        "route_lock": "EXACT_RUNTIME_CHAT_ENTRY_ONLY" if is_chat else "NATIVE_CHECK_ONLY",
        "supervisor_actions_allowed": False,
        "code_change_allowed": False,
        "all_other_actions": "DENY",
        "chat_may_route": False,
        "publish_allowed": False
    }
    write_json(CURRENT_STATE, current)
    return current

def deterministic_next_from_report(report):
    if report.get("repair_required", 0) > 0:
        return "repair"
    if report.get("ready_for_check", 0) > 0:
        return "check"
    if report.get("ready_for_write", 0) > 0:
        return "write"
    if report.get("research_open", 0) > 0:
        return "research"
    if report.get("total", 0) > 0 and report.get("fully_done") == report.get("total"):
        return "finalize"
    return None

def write_current_transition(report):
    nxt = deterministic_next_from_report(report)
    current = {
        "contract": "K9_CURRENT_STATE_V3",
        "role": "SOLE_CURRENT_AUTHORITY",
        "concept": "K9",
        "branch": "konzept9/greenfield-20260929",
        "status": "FINALIZE_PENDING" if nxt == "finalize" else "AUTO_CHAIN_TRANSITION_PENDING",
        "operational_mode": "SYSTEM_ROUTING_ONLY",
        "active_job": None,
        "orchestration_mode": orchestration_mode(),
        "first_open_blocker": None if nxt else "AUTO_CHAIN_NO_VALID_TRANSITION",
        "next_action": "RUN_FINALIZER" if nxt == "finalize" else ("PREPARE_" + str(nxt).upper() if nxt else "STOP_AND_DIAGNOSE_TRANSITION"),
        "chat_may_route": False,
        "publish_allowed": False
    }
    write_json(CURRENT_STATE, current)
    return current

def worker_contract(station):
    data = load_json(WORKER_CONTRACTS)
    if data.get("contract") != "K9_WORKER_CONTRACTS_V1":
        raise K9Error("WORKER_CONTRACT_FILE_INVALID")
    value = data.get("contracts", {}).get(station)
    if not isinstance(value, dict):
        raise K9Error("WORKER_CONTRACT_MISSING:" + station)
    return value

def portal_binding(metadata):
    data = load_json(PORTAL_BINDINGS)
    if data.get("contract") != "K9_PORTAL_BINDINGS_V1":
        raise K9Error("PORTAL_BINDING_FILE_INVALID")
    category = str(metadata.get("category") or "").strip()
    value = data.get("bindings", {}).get(category)
    if not isinstance(value, dict):
        raise K9Error("PORTAL_BINDING_MISSING:" + category)
    links = value.get("portal_links")
    if not isinstance(links, list) or len(links) != 3:
        raise K9Error("PORTAL_BINDING_LINK_COUNT_INVALID")
    roles = []
    for link in links:
        if not isinstance(link, dict):
            raise K9Error("PORTAL_BINDING_LINK_INVALID")
        for key in ("anchor", "href", "role", "section_id"):
            if not str(link.get(key) or "").strip():
                raise K9Error("PORTAL_BINDING_LINK_FIELD_MISSING:" + key)
        roles.append(link["role"])
    if set(roles) != {"parent_category", "semantic_related", "further_information"} or len(roles) != len(set(roles)):
        raise K9Error("PORTAL_BINDING_ROLES_INVALID")
    return {"portal_links": links}

def canonical_title_scope(metadata):
    raw = str(metadata.get("target_keyword") or "").strip().casefold()
    replacements = {"ä":"ae","ö":"oe","ü":"ue","ß":"ss"}
    for src,dst in replacements.items():
        raw = raw.replace(src,dst)
    scope = re.sub(r"[^a-z0-9]+", "_", raw).strip("_")
    if not scope:
        raise K9Error("RESEARCH_TITLE_SCOPE_SOURCE_MISSING")
    return scope

def ledger():
    data = load_json(LEDGER)
    if data.get("contract") != "K9_LEDGER_V1" or not isinstance(data.get("items"), list):
        raise K9Error("LEDGER_INVALID")
    return data

def current_job():
    if not CURRENT_JOB.exists():
        return None
    data = load_json(CURRENT_JOB)
    declared = data.get("job_sha256")
    core = dict(data)
    core.pop("job_sha256", None)
    if data.get("contract") != "K9_JOB_V1" or data.get("status") != "OPEN":
        raise K9Error("CURRENT_JOB_INVALID")
    if declared != stable(core):
        raise K9Error("CURRENT_JOB_HASH_INVALID")
    return data

def write_chat_entry(job):
    station = job["station"]
    is_writer = station in ("write", "repair")
    mode = orchestration_mode()
    output_path = ("writer_drafts/" if is_writer else "submissions/") + job["job_id"] + ".json"
    entry = {
        "contract": "K9_CHAT_ENTRY_V1",
        "concept": "K9",
        "status": "OPEN_JOB_READY_FOR_CHAT",
        "repository": "hallo-netizen/affiliate-pferdeportal",
        "branch": "konzept9/greenfield-20260929",
        "job_path": "runtime/CURRENT_JOB.json",
        "submission_path": output_path,
        "job_id": job["job_id"],
        "job_sha256": job["job_sha256"],
        "station": station,
        "item_count": job["item_count"],
        "allowed_action": "EXECUTE_EXACT_STATION_ONLY",
        "execution_policy": "WORKER_EXECUTES_ONLY_NEVER_SUPERVISES",
        "input_authority_rule": "BOUND_PREDECESSOR_PRODUCTS_ARE_AUTHORITATIVE_FOR_THIS_STATION",
        "blocked_rule": "IF_EXACT_JOB_CANNOT_BE_COMPLETED_RETURN_BLOCKED_WITH_CONCRETE_INPUT_ERROR_ONLY",
        "first_action": "EXECUTE_BOUND_JOB_IMMEDIATELY",
        "first_response_rule": "NO_STATUS_REPORT_NO_DIAGNOSIS_NO_FIX_PROPOSAL_BEFORE_JOB_EXECUTION",
        "role": "WORKER_NOT_SUPERVISOR",
        "route_lock": "EXACT_RUNTIME_CHAT_ENTRY_ONLY",
        "supervisor_actions_allowed": False,
        "code_change_allowed": False,
        "all_other_actions": "DENY",
        "writer_preflight_rule": ("RUN_BOUND_WRITE_PACKAGER_PREFLIGHT_AND_FIX_ALL_FINDINGS_BEFORE_RETURN" if is_writer else None),
        "repair_scope_rule": ("REPAIR_ALL_REPORTED_FAILED_CHECK_FINDINGS_IN_ONE_PASS_ONLY" if station == "repair" else None),
        "forbidden": [
            "SEARCH_OTHER_CONCEPTS",
            "ROUTE_TO_NEXT_STATION",
            "RECONSTRUCT_JOB",
            "USE_ANY_STATE_OUTSIDE_THIS_EXACT_JOB",
            "REOPEN_OR_REEVALUATE_ACCEPTED_PREDECESSOR_STATION",
            "CHANGE_WORKFLOW_OR_ARCHITECTURE",
            "CHANGE_QUALITY_GATES",
            "RESET_OR_REPLACE_TEST_STATE",
            "CREATE_ALTERNATIVE_ROUTE_OR_FALLBACK",
            "PERFORM_SUPERVISOR_OR_SYSTEM_FIXES",
            "DISCUSS_OR_SELECT_OTHER_CONCEPT_VERSIONS"
        ],
        "completion_rule": ("WRITE_EXACT_DRAFT_TO_BOUND_WRITER_DRAFT_PATH" if is_writer
                            else "RETURN_ONE_COMPLETE_K9_SUBMISSION_FOR_THIS_EXACT_JOB"),
        "worker_type": job["worker_contract"]["worker_type"],
        "orchestration_mode": mode,
        "orchestration_state_path": "runtime/AUTO_CHAIN.json" if mode == "AUTO_CHAIN" else None,
        "after_submission_rule": AUTO_CHAIN_AFTER_SUBMISSION_RULE if mode == "AUTO_CHAIN" else "STOP_AFTER_EXACT_STATION_PRODUCT",
        "routing_rule": AUTO_CHAIN_ROUTING_RULE,
        "output_contract": job["worker_contract"]["output_contract"],
        "required_output_fields": job["worker_contract"].get("required_output_fields", []),
        "output_field_sources": job["worker_contract"].get("output_field_sources", {}),
        "packager_path": ("k9_write_packager.py" if is_writer else None),
        "writing_rules_path": ("contracts/K9_WRITING_RULES.json" if is_writer else None),
        "writing_rules_sha256": (stable(load_json(WRITING_RULES)) if is_writer else None),
        "writing_rules_coverage_contract": ((load_json(WRITING_RULES).get("coverage") or {}).get("contract") if is_writer else None),
        "complete_rule_application_required": bool(is_writer)
    }
    write_json(CHAT_ENTRY, entry)
    return entry

def eligible(item, station):
    s = item["stages"]
    if station == "research":
        return s["research"] == "PENDING"
    if station == "write":
        return s["research"] == "DONE" and s["write"] == "PENDING"
    if station == "check":
        return s["write"] == "DONE" and s["check"] == "PENDING"
    if station == "repair":
        return s["check"] == "FAIL" and s["repair"] == "PENDING"
    raise K9Error("STATION_INVALID")

def status_report(data=None):
    data = data or ledger()
    total = len(data["items"])
    fully_done = sum(1 for x in data["items"] if x["stages"]["check"] == "DONE")
    repair_required = sum(1 for x in data["items"] if x["stages"]["repair"] == "PENDING")
    ready_for_write = sum(1 for x in data["items"] if x["stages"]["research"] == "DONE" and x["stages"]["write"] == "PENDING")
    ready_for_check = sum(1 for x in data["items"] if x["stages"]["write"] == "DONE" and x["stages"]["check"] == "PENDING")
    research_open = sum(1 for x in data["items"] if x["stages"]["research"] == "PENDING")
    result = {
        "contract": "K9_STATUS_V1",
        "ledger_generation": data.get("generation"),
        "total": total,
        "fully_done": fully_done,
        "remaining": total - fully_done,
        "research_open": research_open,
        "ready_for_write": ready_for_write,
        "ready_for_check": ready_for_check,
        "repair_required": repair_required,
        "orchestration_mode": orchestration_mode(),
        "stations": {}
    }
    for station in STATIONS:
        values = [x["stages"][station] for x in data["items"]]
        result["stations"][station] = {
            key: values.count(key) for key in sorted(set(values) | {"PENDING", "DONE"})
        }
    job = current_job()
    result["active_job"] = None if job is None else {
        key: job[key] for key in ("job_id", "station", "item_count", "item_ids")
    }
    return result

def write_status(data=None):
    report = status_report(data)
    write_json(STATUS_FILE, report)
    return report

def import_intake(path):
    if current_job() is not None:
        raise K9Error("ACTIVE_JOB_EXISTS")
    source = load_json(path)
    if source.get("contract") != "K9_INTAKE_V1" or source.get("publish_allowed") is not False:
        raise K9Error("INTAKE_CONTRACT_INVALID")
    rows = source.get("items")
    if not isinstance(rows, list) or not rows or source.get("item_count") != len(rows):
        raise K9Error("INTAKE_EMPTY_OR_INVALID")
    if not str(source.get("batch_id") or "").strip() or not str(source.get("batch_sha256") or "").strip():
        raise K9Error("INTAKE_BATCH_IDENTITY_MISSING")
    data = ledger()
    current = load_json(CURRENT_STATE) if CURRENT_STATE.is_file() else {}
    if current.get("status") == "STOP" and data["items"]:
        if not all(x.get("stages",{}).get("check") == "DONE" for x in data["items"]):
            raise K9Error("TERMINAL_LEDGER_NOT_FULLY_DONE")
        archive_dir = WAREHOUSE / "ledger-history"
        archive_path = archive_dir / ("K9-LEDGER-" + stable(data)[:20] + ".json")
        if archive_path.is_file():
            if load_json(archive_path) != data:
                raise K9Error("LEDGER_ARCHIVE_COLLISION")
        else:
            write_json(archive_path, data)
        data = {
            "contract": "K9_LEDGER_V1",
            "generation": int(data.get("generation", 0)) + 1,
            "items": []
        }
    known = {x["item_id"] for x in data["items"]}
    additions = []
    for row in rows:
        item_id = str(row.get("item_id", "")).strip()
        title = str(row.get("title", "")).strip()
        metadata = row.get("metadata", {})
        if not item_id or not title or item_id in known or not isinstance(metadata, dict):
            raise K9Error("INTAKE_ITEM_INVALID_OR_DUPLICATE")
        if set(metadata.keys()) != INTAKE_FIELDS or metadata.get("title") != title or not all(str(metadata.get(k) or "").strip() for k in INTAKE_FIELDS):
            raise K9Error("INTAKE_METADATA_NOT_EXACT_FIVE_FIELDS")
        known.add(item_id)
        additions.append({
            "item_id": item_id,
            "title": title,
            "metadata": metadata,
            "revision": 0,
            "products": {},
            "stages": {
                "research": "PENDING",
                "write": "PENDING",
                "check": "PENDING",
                "repair": "NOT_REQUIRED"
            }
        })
    data["items"].extend(additions)
    data["generation"] += 1
    write_json(LEDGER, data)
    write_status(data)
    return {"status": "INTAKE_ACCEPTED", "added": len(additions), "total": len(data["items"])}

def _product_result(item, stage):
    ref = item.get("products", {}).get(stage)
    if not isinstance(ref, dict):
        raise K9Error("INPUT_PRODUCT_REFERENCE_MISSING:" + stage)
    rel = ref.get("path")
    if not isinstance(rel, str) or not rel.startswith("warehouse/") or ".." in Path(rel).parts:
        raise K9Error("INPUT_PRODUCT_PATH_INVALID:" + stage)
    path = ROOT / rel
    if not path.is_file():
        raise K9Error("INPUT_PRODUCT_MISSING:" + stage)
    package = load_json(path)
    if ref.get("sha256") != stable(package):
        raise K9Error("INPUT_PRODUCT_HASH_MISMATCH:" + stage)
    if package.get("contract") != "K9_SUBMISSION_V1" or package.get("station") != stage:
        raise K9Error("INPUT_PRODUCT_CONTRACT_MISMATCH:" + stage)
    matches = [r for r in package.get("results", []) if r.get("item_id") == item["item_id"]]
    if len(matches) != 1:
        raise K9Error("INPUT_PRODUCT_ITEM_MISSING:" + stage)
    return matches[0], ref

def _inputs_for(item, station):
    if station == "research":
        return {
            "portal_context": portal_binding(item["metadata"]),
            "scope_context": {"title_scope": canonical_title_scope(item["metadata"])}
        }, {}
    research, research_ref = _product_result(item, "research")
    if station == "write":
        return {"research": research}, {"research": research_ref}

    article_stage = "repair" if item.get("revision", 0) > 0 and item.get("products", {}).get("repair") else "write"
    article, article_ref = _product_result(item, article_stage)
    payload = {"research": research, "article": article}
    refs = {"research": research_ref, "article": article_ref}

    if station == "repair":
        check, check_ref = _product_result(item, "check")
        payload["failed_check"] = check
        refs["failed_check"] = check_ref
    return payload, refs

def prepare(station, batch_size, source_run_id="manual"):
    if station not in STATIONS:
        raise K9Error("STATION_INVALID")
    if batch_size < 1 or batch_size > 1000:
        raise K9Error("BATCH_SIZE_INVALID")

    existing = current_job()
    if existing is not None:
        if existing["station"] != station:
            raise K9Error("ACTIVE_JOB_EXISTS_FOR_OTHER_STATION")
        latest_contract = worker_contract(station)
        if existing.get("worker_contract") != latest_contract:
            core = dict(existing)
            core["worker_contract"] = latest_contract
            core.pop("job_id", None)
            core.pop("job_sha256", None)
            core["job_id"] = "K9-" + station.upper() + "-" + stable(core)[:16]
            core["job_sha256"] = stable(core)
            write_json(CURRENT_JOB, core)
            existing = core
        write_chat_entry(existing)
        write_status()
        write_current_for_job(existing)
        return {"status": "EXISTING_JOB_REUSED", "job": existing}

    data = ledger()
    items = [x for x in data["items"] if eligible(x, station)][:batch_size]
    if not items:
        return {"status": "NO_ELIGIBLE_WORK", "station": station, "report": status_report(data)}

    job_items = []
    for item in items:
        inputs, refs = _inputs_for(item, station)
        job_items.append({
            "item_id": item["item_id"],
            "title": item["title"],
            "metadata": item["metadata"],
            "revision": item["revision"],
            "input_products": inputs,
            "input_product_refs": refs
        })

    core = {
        "contract": "K9_JOB_V1",
        "status": "OPEN",
        "station": station,
        "item_count": len(items),
        "item_ids": [x["item_id"] for x in items],
        "items": job_items,
        "source_run_id": str(source_run_id),
        "ledger_generation": data["generation"],
        "worker_contract": worker_contract(station)
    }
    core["job_id"] = "K9-" + station.upper() + "-" + stable(core)[:16]
    core["job_sha256"] = stable(core)
    write_json(CURRENT_JOB, core)
    write_chat_entry(core)
    write_status(data)
    write_current_for_job(core)
    return {"status": "NEW_JOB_PREPARED", "job": core}

def _job_item(job, item_id):
    matches = [x for x in job.get("items", []) if x.get("item_id") == item_id]
    if len(matches) != 1:
        raise K9Error("JOB_ITEM_MISSING_OR_DUPLICATE")
    return matches[0]

def _validate_research_product(row, job_item):
    product = row.get("research_product")
    if not isinstance(product, dict) or product.get("contract") != "K9_RESEARCH_PRODUCT_V1":
        raise K9Error("RESEARCH_PRODUCT_CONTRACT_INVALID")
    sources = product.get("sources")
    pack = product.get("fact_pack")
    portal_links = product.get("portal_links")
    decision_support = product.get("decision_support")
    if not isinstance(sources, list) or not sources or not isinstance(pack, dict):
        raise K9Error("RESEARCH_PRODUCT_INCOMPLETE")

    bound_context = job_item.get("input_products", {}).get("portal_context")
    if not isinstance(bound_context, dict):
        raise K9Error("RESEARCH_PORTAL_CONTEXT_MISSING")
    bound_links = bound_context.get("portal_links")
    if not isinstance(portal_links, list) or len(portal_links) != 3:
        raise K9Error("RESEARCH_PORTAL_LINKS_INVALID")
    if portal_links != bound_links:
        raise K9Error("RESEARCH_PORTAL_BINDING_MISMATCH")
    roles = [x.get("role") for x in portal_links if isinstance(x, dict)]
    if set(roles) != {"parent_category", "semantic_related", "further_information"} or len(roles) != 3:
        raise K9Error("RESEARCH_PORTAL_LINK_ROLES_INVALID")
    for link in portal_links:
        if not isinstance(link, dict) or not all(str(link.get(k) or "").strip() for k in ("anchor","href","role","section_id")):
            raise K9Error("RESEARCH_PORTAL_LINK_FIELD_MISSING")

    if not isinstance(decision_support, dict):
        raise K9Error("RESEARCH_DECISION_SUPPORT_INVALID")
    goal = str(decision_support.get("decision_goal") or "").strip()
    criteria = decision_support.get("decision_criteria")
    if not goal or not isinstance(criteria, list) or len(criteria) < 2 or not all(str(x or "").strip() for x in criteria):
        raise K9Error("RESEARCH_DECISION_SUPPORT_INVALID")

    source_ids = []
    for source in sources:
        if not isinstance(source, dict):
            raise K9Error("RESEARCH_SOURCE_INVALID")
        sid = str(source.get("source_id") or "").strip()
        url = str(source.get("url") or "").strip()
        title = str(source.get("title") or "").strip()
        if not sid or not url or not title:
            raise K9Error("RESEARCH_SOURCE_REQUIRED_FIELD_MISSING")
        source_ids.append(sid)
    if len(source_ids) != len(set(source_ids)):
        raise K9Error("RESEARCH_SOURCE_ID_DUPLICATE")

    required_pack = {
        "fact_pack_id", "domain", "article_type", "title_scope", "fact_ids", "status", "claims",
        "fact_pack_hash", "source_manifest_hash", "claim_register_hash",
        "required_block_coverage", "table_evidence_coverage",
        "conclusion_evidence_coverage", "article_type_coverage",
        "temporal_validity_status", "contradiction_status",
        "production_readiness_status", "placeholder_content_status"
    }
    if not required_pack.issubset(pack):
        raise K9Error("RESEARCH_FACT_PACK_REQUIRED_FIELD_MISSING")
    if pack.get("status") != "SOURCE_VERIFIED_PRODUCTION_READY" or pack.get("production_readiness_status") != "SOURCE_VERIFIED_PRODUCTION_READY":
        raise K9Error("RESEARCH_FACT_PACK_NOT_PRODUCTION_READY")
    fact_ids = pack.get("fact_ids")
    claims = pack.get("claims")
    if not isinstance(fact_ids, list) or not fact_ids or not isinstance(claims, list) or not claims:
        raise K9Error("RESEARCH_FACT_PACK_FACTS_MISSING")
    if len(fact_ids) != len(set(fact_ids)):
        raise K9Error("RESEARCH_FACT_ID_DUPLICATE")

    expected_type = str(job_item.get("metadata", {}).get("article_type") or "").strip()
    claim_ids = []
    for claim in claims:
        if not isinstance(claim, dict):
            raise K9Error("RESEARCH_CLAIM_INVALID")
        for key in ("fact_id", "source_id", "locator", "statement", "claim_status", "subject_scope", "time_scope"):
            if not str(claim.get(key) or "").strip():
                raise K9Error("RESEARCH_CLAIM_REQUIRED_FIELD_MISSING:" + key)
        article_types = claim.get("article_types")
        if not isinstance(article_types, list) or not article_types or not all(str(x or "").strip() for x in article_types):
            raise K9Error("RESEARCH_CLAIM_ARTICLE_TYPES_INVALID:" + str(claim.get("fact_id") or ""))
        if expected_type and expected_type not in article_types:
            raise K9Error("RESEARCH_CLAIM_ARTICLE_TYPE_MISMATCH:" + str(claim.get("fact_id") or ""))
        evidence_hash = str(claim.get("evidence_text_sha256") or "").strip()
        expected_evidence_hash = hashlib.sha256(str(claim.get("statement") or "").encode("utf-8")).hexdigest()
        if evidence_hash != expected_evidence_hash:
            raise K9Error("RESEARCH_CLAIM_EVIDENCE_HASH_INVALID:" + str(claim.get("fact_id") or ""))
        if claim.get("claim_status") != "FULLY_SUPPORTED":
            raise K9Error("RESEARCH_CLAIM_NOT_FULLY_SUPPORTED")
        if claim["source_id"] not in source_ids:
            raise K9Error("RESEARCH_CLAIM_SOURCE_UNKNOWN")
        claim_ids.append(claim["fact_id"])
    if set(claim_ids) != set(fact_ids) or len(claim_ids) != len(set(claim_ids)):
        raise K9Error("RESEARCH_FACT_CLAIM_SET_MISMATCH")

    if expected_type and pack.get("article_type") != expected_type:
        raise K9Error("RESEARCH_ARTICLE_TYPE_MISMATCH")
    bound_scope = str(job_item.get("input_products", {}).get("scope_context", {}).get("title_scope") or "").strip()
    if not bound_scope:
        raise K9Error("RESEARCH_BOUND_TITLE_SCOPE_MISSING")
    if str(pack.get("title_scope") or "").strip() != bound_scope:
        raise K9Error("RESEARCH_TITLE_SCOPE_MISMATCH")
    declared = product.get("product_sha256")
    core = dict(product)
    core.pop("product_sha256", None)
    if declared != stable(core):
        raise K9Error("RESEARCH_PRODUCT_HASH_INVALID")
    return product

def _validate_article_product(row, job_item):
    product = row.get("article_product")
    if not isinstance(product, dict) or product.get("contract") != "K9_ARTICLE_PRODUCT_V1":
        raise K9Error("ARTICLE_PRODUCT_CONTRACT_INVALID")
    title = str(product.get("title") or "").strip()
    html = str(product.get("content_html") or "")
    if not title or not html.strip():
        raise K9Error("ARTICLE_PRODUCT_CONTENT_MISSING")
    content_sha = hashlib.sha256(html.encode("utf-8")).hexdigest()
    if product.get("content_sha256") != content_sha:
        raise K9Error("ARTICLE_PRODUCT_CONTENT_HASH_INVALID")

    research_row = job_item.get("input_products", {}).get("research")
    if not isinstance(research_row, dict):
        raise K9Error("ARTICLE_RESEARCH_INPUT_MISSING")
    research = research_row.get("research_product")
    if not isinstance(research, dict):
        raise K9Error("ARTICLE_RESEARCH_PRODUCT_MISSING")
    if product.get("research_product_sha256") != research.get("product_sha256"):
        raise K9Error("ARTICLE_RESEARCH_BINDING_MISMATCH")

    ppm_item = product.get("ppm_item")
    if not isinstance(ppm_item, dict):
        raise K9Error("ARTICLE_PPM_ITEM_MISSING")
    fact_pack = research.get("fact_pack", {})
    if ppm_item.get("source_snapshot_id") != fact_pack.get("fact_pack_id"):
        raise K9Error("ARTICLE_PPM_SOURCE_BINDING_MISMATCH")
    if ppm_item.get("article_type") != fact_pack.get("article_type"):
        raise K9Error("ARTICLE_PPM_TYPE_BINDING_MISMATCH")
    canonical = ppm_item.get("canonical_article")
    if not isinstance(canonical, dict) or canonical.get("body_html") != html or canonical.get("title") != title:
        raise K9Error("ARTICLE_PPM_CANONICAL_BINDING_MISMATCH")

    declared = product.get("product_sha256")
    core = dict(product)
    core.pop("product_sha256", None)
    if declared != stable(core):
        raise K9Error("ARTICLE_PRODUCT_HASH_INVALID")
    return product

def _validate_check_product(row, job_item):
    lt = row.get("lt68_result")
    ppm = row.get("ppm679_result")
    writing = row.get("writing_rules_result")
    if not isinstance(lt, dict) or lt.get("contract") != "K9_LT68_RESULT_V1":
        raise K9Error("CHECK_LT68_RESULT_INVALID")
    if not isinstance(ppm, dict) or ppm.get("contract") != "K9_PPM679_RESULT_V1":
        raise K9Error("CHECK_PPM679_RESULT_INVALID")
    if not isinstance(writing, dict) or writing.get("contract") != "K9_WRITING_RULES_RESULT_V1":
        raise K9Error("CHECK_WRITING_RULES_RESULT_INVALID")

    article_row = job_item.get("input_products", {}).get("article")
    if not isinstance(article_row, dict):
        raise K9Error("CHECK_ARTICLE_INPUT_MISSING")
    article = article_row.get("article_product")
    if not isinstance(article, dict):
        raise K9Error("CHECK_ARTICLE_PRODUCT_MISSING")
    content_sha = article.get("content_sha256")

    if lt.get("jar_sha256") != LT68_JAR_SHA256 or lt.get("article_sha256") != content_sha:
        raise K9Error("CHECK_LT68_BINDING_INVALID")
    if ppm.get("ppm_package_sha256") != PPM679_PACKAGE_SHA256 or ppm.get("content_sha256") != content_sha:
        raise K9Error("CHECK_PPM679_BINDING_INVALID")
    if writing.get("content_sha256") != content_sha or writing.get("writing_rules_sha256") != article.get("writing_rules_sha256"):
        raise K9Error("CHECK_WRITING_RULES_BINDING_INVALID")
    if lt.get("status") not in ("PASS", "REPAIR_REQUIRED") or ppm.get("status") not in ("PASS", "REPAIR_REQUIRED") or writing.get("status") not in ("PASS", "REPAIR_REQUIRED"):
        raise K9Error("CHECK_RESULT_STATUS_INVALID")
    return lt, ppm, writing

def assert_execution_only_entry(job):
    if job.get("station") == "check":
        return
    if not CHAT_ENTRY.exists():
        raise K9Error("CHAT_ENTRY_REQUIRED_FOR_CHAT_WORKER")
    entry = load_json(CHAT_ENTRY)
    if entry.get("job_id") != job.get("job_id") or entry.get("job_sha256") != job.get("job_sha256"):
        raise K9Error("CHAT_ENTRY_JOB_MISMATCH")
    if entry.get("execution_policy") != "WORKER_EXECUTES_ONLY_NEVER_SUPERVISES":
        raise K9Error("CHAT_ENTRY_EXECUTION_POLICY_INVALID")
    if entry.get("route_lock") != "EXACT_RUNTIME_CHAT_ENTRY_ONLY" or entry.get("all_other_actions") != "DENY":
        raise K9Error("CHAT_ENTRY_ROUTE_LOCK_INVALID")
    if entry.get("supervisor_actions_allowed") is not False or entry.get("code_change_allowed") is not False:
        raise K9Error("CHAT_ENTRY_WORKER_PRIVILEGE_INVALID")
    if entry.get("input_authority_rule") != "BOUND_PREDECESSOR_PRODUCTS_ARE_AUTHORITATIVE_FOR_THIS_STATION":
        raise K9Error("CHAT_ENTRY_INPUT_AUTHORITY_RULE_INVALID")
    if entry.get("blocked_rule") != "IF_EXACT_JOB_CANNOT_BE_COMPLETED_RETURN_BLOCKED_WITH_CONCRETE_INPUT_ERROR_ONLY":
        raise K9Error("CHAT_ENTRY_BLOCKED_RULE_INVALID")
    mode = entry.get("orchestration_mode")
    if mode not in ("STATION_ONLY", "AUTO_CHAIN"):
        raise K9Error("CHAT_ENTRY_ORCHESTRATION_MODE_INVALID")
    if entry.get("routing_rule") != AUTO_CHAIN_ROUTING_RULE:
        raise K9Error("CHAT_ENTRY_ROUTING_RULE_INVALID")
    if mode == "AUTO_CHAIN":
        if entry.get("after_submission_rule") != AUTO_CHAIN_AFTER_SUBMISSION_RULE or entry.get("orchestration_state_path") != "runtime/AUTO_CHAIN.json":
            raise K9Error("CHAT_ENTRY_AUTO_CHAIN_GUARD_INVALID")
    elif entry.get("after_submission_rule") != "STOP_AFTER_EXACT_STATION_PRODUCT":
        raise K9Error("CHAT_ENTRY_STATION_ONLY_GUARD_INVALID")
    required_forbidden = {
        "REOPEN_OR_REEVALUATE_ACCEPTED_PREDECESSOR_STATION",
        "CHANGE_WORKFLOW_OR_ARCHITECTURE",
        "CHANGE_QUALITY_GATES",
        "RESET_OR_REPLACE_TEST_STATE",
        "CREATE_ALTERNATIVE_ROUTE_OR_FALLBACK",
        "PERFORM_SUPERVISOR_OR_SYSTEM_FIXES",
        "DISCUSS_OR_SELECT_OTHER_CONCEPT_VERSIONS"
    }
    if not required_forbidden.issubset(set(entry.get("forbidden") or [])):
        raise K9Error("CHAT_ENTRY_EXECUTION_GUARD_INCOMPLETE")
    if job.get("station") in ("write","repair"):
        rules=load_json(WRITING_RULES)
        if entry.get("writing_rules_path")!="contracts/K9_WRITING_RULES.json" or entry.get("writing_rules_sha256")!=stable(rules):
            raise K9Error("CHAT_ENTRY_COMPLETE_WRITING_RULE_BINDING_INVALID")
        if entry.get("writing_rules_coverage_contract")!="K9_COMPLETE_RULE_COVERAGE_V1" or entry.get("complete_rule_application_required") is not True:
            raise K9Error("CHAT_ENTRY_RULE_COVERAGE_GUARD_INVALID")
        if entry.get("writer_preflight_rule")!="RUN_BOUND_WRITE_PACKAGER_PREFLIGHT_AND_FIX_ALL_FINDINGS_BEFORE_RETURN":
            raise K9Error("CHAT_ENTRY_WRITER_PREFLIGHT_GUARD_INVALID")
        if job.get("station")=="repair" and entry.get("repair_scope_rule")!="REPAIR_ALL_REPORTED_FAILED_CHECK_FINDINGS_IN_ONE_PASS_ONLY":
            raise K9Error("CHAT_ENTRY_REPAIR_SCOPE_GUARD_INVALID")

def validate_submission(job, submission):
    if submission.get("contract") != "K9_SUBMISSION_V1":
        raise K9Error("SUBMISSION_CONTRACT_INVALID")
    if submission.get("job_id") != job["job_id"] or submission.get("station") != job["station"]:
        raise K9Error("SUBMISSION_JOB_MISMATCH")
    rows = submission.get("results")
    if not isinstance(rows, list) or len(rows) != job["item_count"]:
        raise K9Error("SUBMISSION_PARTIAL_OR_COUNT_MISMATCH")
    ids = [r.get("item_id") for r in rows]
    if len(ids) != len(set(ids)) or set(ids) != set(job["item_ids"]):
        raise K9Error("SUBMISSION_ITEM_SET_MISMATCH")
    by_id = {r["item_id"]: r for r in rows}
    station = job["station"]
    for item_id in job["item_ids"]:
        row = by_id[item_id]
        job_item = _job_item(job, item_id)
        if station == "research":
            _validate_research_product(row, job_item)
        elif station == "write":
            _validate_article_product(row, job_item)
        elif station == "check":
            _validate_check_product(row, job_item)
        elif station == "repair":
            _validate_article_product(row, job_item)
    return by_id

def accept(path):
    submission = load_json(path)
    archived = WAREHOUSE / "jobs" / f"{submission.get('job_id', 'UNKNOWN')}.json"
    if archived.exists():
        return {"status": "ALREADY_ACCEPTED", "job_id": submission.get("job_id")}

    job = current_job()
    if job is None:
        raise K9Error("NO_ACTIVE_JOB")
    assert_execution_only_entry(job)
    by_id = validate_submission(job, submission)
    data = ledger()
    if data["generation"] != job["ledger_generation"]:
        raise K9Error("LEDGER_CHANGED_DURING_OPEN_JOB")

    items = {x["item_id"]: x for x in data["items"]}
    stage = job["station"]
    product_rel = f"warehouse/{stage}/{job['job_id']}.json"
    product_ref = {"job_id": job["job_id"], "path": product_rel, "sha256": stable(submission)}

    for item_id in job["item_ids"]:
        item = items[item_id]
        result = by_id[item_id]
        if not eligible(item, stage):
            raise K9Error("LEDGER_DRIFT_OR_DUPLICATE_PROCESSING")
        item.setdefault("products", {})[stage] = dict(product_ref)

        if stage == "research":
            item["stages"]["research"] = "DONE"
        elif stage == "write":
            item["stages"]["write"] = "DONE"
        elif stage == "check":
            lt_status = result["lt68_result"]["status"]
            ppm_status = result["ppm679_result"]["status"]
            writing_status = result["writing_rules_result"]["status"]
            if lt_status == "PASS" and ppm_status == "PASS" and writing_status == "PASS":
                item["stages"]["check"] = "DONE"
                item["stages"]["repair"] = "NOT_REQUIRED"
            else:
                item["stages"]["check"] = "FAIL"
                item["stages"]["repair"] = "PENDING"
        elif stage == "repair":
            item["revision"] += 1
            item["stages"]["repair"] = "DONE"
            item["stages"]["check"] = "PENDING"

    data["generation"] += 1
    write_json(ROOT / product_rel, submission)
    write_json(WAREHOUSE / "jobs" / f"{job['job_id']}.json", job)
    write_json(LEDGER, data)
    CURRENT_JOB.unlink()
    if CHAT_ENTRY.exists():
        CHAT_ENTRY.unlink()
    final_report = write_status(data)
    if orchestration_mode() == "AUTO_CHAIN":
        write_current_transition(final_report)
    return {
        "status": "ACCEPTED",
        "job_id": job["job_id"],
        "station": stage,
        "item_count": job["item_count"],
        "report": final_report
    }

def auto_next_station():
    if orchestration_mode() != "AUTO_CHAIN":
        raise K9Error("AUTO_NEXT_REQUIRES_ACTIVE_AUTO_CHAIN")
    if current_job() is not None:
        raise K9Error("AUTO_NEXT_ACTIVE_JOB_EXISTS")
    report = status_report()
    nxt = deterministic_next_from_report(report)
    if nxt is None:
        raise K9Error("AUTO_NEXT_NO_VALID_TRANSITION")
    return {"status": "AUTO_NEXT_READY", "next": nxt, "report": report}

def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="cmd", required=True)
    p = subs.add_parser("import-intake")
    p.add_argument("path")
    p = subs.add_parser("prepare")
    p.add_argument("station", choices=STATIONS)
    p.add_argument("batch_size", type=int)
    p.add_argument("--source-run-id", default="manual")
    p = subs.add_parser("accept")
    p.add_argument("path")
    p = subs.add_parser("orchestration")
    p.add_argument("mode", choices=("station_only", "auto_chain", "inherit"))
    p.add_argument("--source-run-id", default="manual")
    subs.add_parser("auto-next")
    subs.add_parser("status")
    args = parser.parse_args()

    try:
        if args.cmd == "import-intake":
            result = import_intake(args.path)
        elif args.cmd == "prepare":
            result = prepare(args.station, args.batch_size, args.source_run_id)
        elif args.cmd == "accept":
            result = accept(args.path)
        elif args.cmd == "orchestration":
            result = set_orchestration_mode(args.mode, args.source_run_id)
        elif args.cmd == "auto-next":
            result = auto_next_station()
        else:
            result = status_report()
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    except K9Error as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(2)

if __name__ == "__main__":
    main()
