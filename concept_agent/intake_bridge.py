#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

SNAPSHOT_CONTRACT = "PSERC_METADATA_ONLY_READ_ONLY_PREVIEW_V5_DUAL_STRAND"
BATCH_CONTRACT = "PSERC_TEXTMACHINE_METADATA_BATCH_V2"
READY_STATUS = "READY_FOR_TEXTMACHINE_METADATA_INTAKE"
NEXT_STEP = "APPROVED_RESEARCH_TEXT_PROCESS_INTAKE_REQUIRED"
INTAKE_CONTRACT = "CONCEPT_AGENT_AUTHORING_INTAKE_V1"
RESEARCH_SUBMISSION_CONTRACT = "CONCEPT_AGENT_RESEARCH_SUBMISSION_V1"
RESEARCH_BOUND_CONTRACT = "CONCEPT_AGENT_RESEARCH_BOUND_V1"
WORK_BINDING_CONTRACT = "CONCEPT_AGENT_WORK_BINDING_V1"
AUTHORING_SUBMISSION_CONTRACT = "CONCEPT_AGENT_AUTHORING_SUBMISSION_V1"
EXACT_FIELDS = ("title", "target_keyword", "category", "article_type", "plan_slot")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

class Blocked(RuntimeError):
    pass

def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def stable(value) -> str:
    return sha(canon(value))

def _load(path: Path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED")
    return value

def _validate_item(item: dict, index: int) -> dict:
    if not isinstance(item, dict) or set(item) != set(EXACT_FIELDS):
        raise Blocked(f"EXACT_FIVE_FIELDS_REQUIRED:{index}")
    out = {}
    for key in EXACT_FIELDS:
        value = item.get(key)
        if not isinstance(value, str) or not value.strip():
            raise Blocked(f"ITEM_FIELD_INVALID:{index}:{key}")
        out[key] = value
    if not SHA_RE.fullmatch(out["plan_slot"]):
        raise Blocked(f"PLAN_SLOT_INVALID:{index}")
    return out

def prepare(snapshot: dict) -> dict:
    if snapshot.get("contract") != SNAPSHOT_CONTRACT:
        raise Blocked("SNAPSHOT_CONTRACT_INVALID")
    if snapshot.get("next_step") != NEXT_STEP:
        raise Blocked("NEXT_STEP_INVALID")
    rules = snapshot.get("hard_rules") or {}
    if rules.get("approved_research_text_process_required") is not True:
        raise Blocked("APPROVED_RESEARCH_PROCESS_NOT_REQUIRED")
    if rules.get("text_machine_is_only_content_and_format_authority") is not True:
        raise Blocked("TEXTMACHINE_AUTHORITY_MISSING")
    if rules.get("metadata_handoff_exact_scalar_fields") != list(EXACT_FIELDS):
        raise Blocked("METADATA_FIELD_CONTRACT_INVALID")
    batch = snapshot.get("next_textmachine_metadata_batch")
    if not isinstance(batch, dict) or batch.get("contract") != BATCH_CONTRACT:
        raise Blocked("BATCH_CONTRACT_INVALID")
    if batch.get("status") != READY_STATUS:
        raise Blocked("BATCH_NOT_READY")
    if batch.get("publish_allowed") is not False:
        raise Blocked("PUBLISH_MUST_BE_FALSE")
    if batch.get("content_or_format_payload_present") is not False:
        raise Blocked("CONTENT_MUST_NOT_PREEXIST")
    items = batch.get("items")
    if not isinstance(items, list) or not items or batch.get("item_count") != len(items):
        raise Blocked("BATCH_COUNT_INVALID")
    declared = str(batch.get("batch_sha256") or "")
    if not SHA_RE.fullmatch(declared):
        raise Blocked("BATCH_SHA_INVALID")
    core = dict(batch)
    core.pop("batch_sha256", None)
    if stable(core) != declared:
        raise Blocked("BATCH_SHA_MISMATCH")
    checked = []
    seen = set()
    for index, item in enumerate(items):
        row = _validate_item(item, index)
        if row["plan_slot"] in seen:
            raise Blocked(f"PLAN_SLOT_DUPLICATE:{index}")
        seen.add(row["plan_slot"])
        checked.append({"item_index": index, **row, "identity_sha256": stable(row)})
    request = {
        "contract": INTAKE_CONTRACT,
        "source_contract": SNAPSHOT_CONTRACT,
        "batch_sha256": declared,
        "item_count": len(checked),
        "items": checked,
        "authoring_role": "CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS",
        "research": {
            "status": "RESEARCH_REQUIRED",
            "owner": "CONCEPT_AGENT",
            "source_selection": "AGENT_SELECTED_THEN_HASH_BOUND_PER_ITEM",
            "research_must_be_bound_before_draft": True,
            "unbound_claims_forbidden": True,
            "legacy_system4_source_requests_required": False,
            "legacy_runtime_slot_consulted": False,
        },
        "downstream": {
            "language_tool_version": "6.8",
            "ppm_version": "6.7.9",
            "pserc_required": True,
            "endstempel_request_contract": "CONCEPT_AGENT_ENDSTEMPEL_AUTO_REQUEST_V1",
            "publish_allowed": False,
        },
        "publish_allowed": False,
    }
    request["intake_sha256"] = stable(request)
    return request

def bind_research(intake: dict, submission: dict) -> dict:
    if not isinstance(intake, dict) or intake.get("contract") != INTAKE_CONTRACT:
        raise Blocked("INTAKE_INVALID")
    expected_hash = intake.get("intake_sha256")
    core = dict(intake)
    core.pop("intake_sha256", None)
    if expected_hash != stable(core):
        raise Blocked("INTAKE_INTEGRITY_FAIL")
    if not isinstance(submission, dict) or submission.get("contract") != RESEARCH_SUBMISSION_CONTRACT:
        raise Blocked("RESEARCH_SUBMISSION_INVALID")
    if submission.get("batch_sha256") != intake.get("batch_sha256"):
        raise Blocked("RESEARCH_BATCH_MISMATCH")
    rows = submission.get("items")
    if not isinstance(rows, list) or submission.get("item_count") != intake.get("item_count") or len(rows) != intake.get("item_count"):
        raise Blocked("RESEARCH_COUNT_MISMATCH")
    out_rows = []
    for index, (article, row) in enumerate(zip(intake["items"], rows)):
        if not isinstance(row, dict) or row.get("item_index") != index or row.get("plan_slot") != article.get("plan_slot"):
            raise Blocked(f"RESEARCH_ITEM_BINDING_MISMATCH:{index}")
        sources = row.get("sources")
        if not isinstance(sources, list) or not sources:
            raise Blocked(f"RESEARCH_SOURCE_POOL_EMPTY:{index}")
        seen = set(); checked_sources = []
        for sidx, source in enumerate(sources):
            if not isinstance(source, dict):
                raise Blocked(f"RESEARCH_SOURCE_INVALID:{index}:{sidx}")
            required = ("source_id", "source_title", "source_url", "evidence", "snapshot_sha256")
            if any(not isinstance(source.get(k), str) or not source[k].strip() for k in required):
                raise Blocked(f"RESEARCH_SOURCE_FIELD_INVALID:{index}:{sidx}")
            sid = source["source_id"]
            if sid in seen:
                raise Blocked(f"RESEARCH_SOURCE_DUPLICATE:{index}:{sid}")
            seen.add(sid)
            if not source["source_url"].startswith(("https://", "http://")):
                raise Blocked(f"RESEARCH_SOURCE_URL_INVALID:{index}:{sidx}")
            if sha(source["evidence"].encode("utf-8")) != source["snapshot_sha256"]:
                raise Blocked(f"RESEARCH_EVIDENCE_HASH_MISMATCH:{index}:{sidx}")
            checked_sources.append({k: source[k] for k in required})
        out_rows.append({
            "item_index": index,
            "plan_slot": article["plan_slot"],
            "article_identity_sha256": article["identity_sha256"],
            "sources": checked_sources,
            "source_pool_sha256": stable(checked_sources),
        })
    bound = {
        "contract": RESEARCH_BOUND_CONTRACT,
        "batch_sha256": intake["batch_sha256"],
        "item_count": intake["item_count"],
        "items": out_rows,
        "draft_allowed": True,
        "publish_allowed": False,
    }
    bound["research_binding_sha256"] = stable(bound)
    return bound

def build_work_binding(intake: dict, research_bound: dict, authoring: dict) -> dict:
    """Bind already-produced research + prewrite authoring data. No research/generation occurs here."""
    if not isinstance(intake, dict) or intake.get("contract") != INTAKE_CONTRACT:
        raise Blocked("INTAKE_INVALID")
    icore=dict(intake); ideclared=icore.pop("intake_sha256",None)
    if ideclared != stable(icore):
        raise Blocked("INTAKE_INTEGRITY_FAIL")
    if not isinstance(research_bound, dict) or research_bound.get("contract") != RESEARCH_BOUND_CONTRACT:
        raise Blocked("RESEARCH_BOUND_INVALID")
    rcore=dict(research_bound); rdeclared=rcore.pop("research_binding_sha256",None)
    if rdeclared != stable(rcore):
        raise Blocked("RESEARCH_BOUND_INTEGRITY_FAIL")
    if research_bound.get("batch_sha256") != intake.get("batch_sha256") or research_bound.get("item_count") != intake.get("item_count"):
        raise Blocked("RESEARCH_BOUND_BATCH_MISMATCH")
    if not isinstance(authoring,dict) or authoring.get("contract") != AUTHORING_SUBMISSION_CONTRACT:
        raise Blocked("AUTHORING_SUBMISSION_INVALID")
    if authoring.get("batch_sha256") != intake.get("batch_sha256") or authoring.get("item_count") != intake.get("item_count"):
        raise Blocked("AUTHORING_BATCH_MISMATCH")
    arows=authoring.get("items")
    if not isinstance(arows,list) or len(arows)!=intake.get("item_count"):
        raise Blocked("AUTHORING_COUNT_MISMATCH")
    work=[]
    for idx,(meta,rrow,arow) in enumerate(zip(intake["items"],research_bound["items"],arows)):
        if not isinstance(arow,dict) or arow.get("item_index")!=idx or arow.get("plan_slot")!=meta["plan_slot"]:
            raise Blocked(f"AUTHORING_ITEM_BINDING_MISMATCH:{idx}")
        for key in EXACT_FIELDS:
            if arow.get(key)!=meta.get(key):
                raise Blocked(f"AUTHORING_METADATA_DRIFT:{idx}:{key}")
        fact=arow.get("fact_pack"); plan=arow.get("production_plan_item")
        if not isinstance(fact,dict) or fact.get("contract")!="canonical_fact_pack_v1" or fact.get("status")!="SOURCE_VERIFIED_PRODUCTION_READY":
            raise Blocked(f"AUTHORING_FACT_PACK_INVALID:{idx}")
        claims=fact.get("claims")
        if not isinstance(claims,list) or len(claims)<3 or any(not isinstance(c,dict) or c.get("claim_status")!="FULLY_SUPPORTED" for c in claims):
            raise Blocked(f"AUTHORING_FACT_CLAIMS_INVALID:{idx}")
        if not isinstance(plan,dict):
            raise Blocked(f"AUTHORING_PLAN_INVALID:{idx}")
        if plan.get("article_type")!=meta["article_type"] or plan.get("target_keyword")!=meta["target_keyword"] or plan.get("topic")!=meta["title"]:
            raise Blocked(f"AUTHORING_PLAN_IDENTITY_MISMATCH:{idx}")
        quality=plan.get("quality_binding")
        if not isinstance(quality,dict) or quality.get("contract")!="content_structure_language_binding_v2":
            raise Blocked(f"AUTHORING_QUALITY_BINDING_INVALID:{idx}")
        links=quality.get("link_bindings")
        if not isinstance(links,list) or len(links)!=3:
            raise Blocked(f"AUTHORING_INTERNAL_LINK_COUNT_INVALID:{idx}")
        roles=[str(x.get("role") or "") for x in links if isinstance(x,dict)]
        if roles!=["parent_category","semantic_related","further_information"]:
            raise Blocked(f"AUTHORING_INTERNAL_LINK_ROLES_INVALID:{idx}")
        for lidx,link in enumerate(links):
            href=str(link.get("href") or "")
            if not href.startswith("/") or href.startswith("//") or "://" in href:
                raise Blocked(f"AUTHORING_INTERNAL_LINK_INVALID:{idx}:{lidx}")
        qcopy=dict(quality); qhash=str(plan.get("quality_binding_hash") or "")
        if qhash!=stable(qcopy):
            raise Blocked(f"AUTHORING_QUALITY_BINDING_HASH_INVALID:{idx}")
        rsources=rrow.get("sources") if isinstance(rrow,dict) else None
        fsources=fact.get("sources")
        if not isinstance(rsources,list) or not isinstance(fsources,list):
            raise Blocked(f"AUTHORING_SOURCE_BINDING_INVALID:{idx}")
        rids={str(s.get("source_id")) for s in rsources if isinstance(s,dict)}
        fids={str(s.get("source_id")) for s in fsources if isinstance(s,dict)}
        if not fids or not fids.issubset(rids):
            raise Blocked(f"AUTHORING_SOURCE_NOT_RESEARCH_BOUND:{idx}")
        system4=Path(__file__).resolve().parent.parent/"isolated_system4"
        if str(system4) not in sys.path:
            sys.path.insert(0,str(system4))
        import authoring_contract
        source_snapshot_id=str(fact.get("source_snapshot_id") or "")
        state={
            "article":{k:meta[k] for k in EXACT_FIELDS},
            "source_snapshot_sha256":source_snapshot_id,
        }
        try:
            contract=authoring_contract.build(Path(__file__).resolve().parent.parent,state,fact,plan)
        except Exception as exc:
            raise Blocked(f"AUTHORING_CONTRACT_INVALID:{idx}:"+str(exc)) from exc
        work.append({
            "item_index":idx,
            "plan_slot":meta["plan_slot"],
            "title":meta["title"],
            "target_keyword":meta["target_keyword"],
            "category":meta["category"],
            "article_type":meta["article_type"],
            "research_binding":{
                "status":"BOUND",
                "sources":rsources,
                "source_pool_sha256":rrow["source_pool_sha256"],
            },
            "authoring_binding":{
                "status":"BOUND",
                "internal_links":links,
                "fact_pack":fact,
                "production_plan_item":plan,
                "authoring_contract":contract,
            },
        })
    out={
        "contract":WORK_BINDING_CONTRACT,
        "batch_sha256":intake["batch_sha256"],
        "item_count":intake["item_count"],
        "items":work,
        "publish_allowed":False,
    }
    out["binding_sha256"]=stable(out)
    return out

def bind_files(intake_path: str, research_path: str, authoring_path: str, out_path: str) -> dict:
    result=build_work_binding(_load(Path(intake_path)),_load(Path(research_path)),_load(Path(authoring_path)))
    Path(out_path).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return result

def prepare_file(snapshot_path: str, out_path: str) -> dict:
    request = prepare(_load(Path(snapshot_path)))
    Path(out_path).write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return request

def main(argv: list[str]) -> int:
    try:
        if len(argv) == 4 and argv[1] == "prepare":
            result = prepare_file(argv[2], argv[3])
            print(json.dumps({"status":"CONCEPT_AGENT_INTAKE_READY","batch_sha256":result["batch_sha256"],"item_count":result["item_count"],"intake_sha256":result["intake_sha256"],"publish_allowed":False}, ensure_ascii=False, sort_keys=True))
            return 0
        if len(argv) == 6 and argv[1] == "bind-work":
            result=bind_files(argv[2],argv[3],argv[4],argv[5])
            print(json.dumps({"status":"CONCEPT_AGENT_WORK_BINDING_READY","batch_sha256":result["batch_sha256"],"item_count":result["item_count"],"binding_sha256":result["binding_sha256"],"publish_allowed":False},ensure_ascii=False,sort_keys=True))
            return 0
        raise Blocked("USE: intake_bridge.py prepare SNAPSHOT_JSON OUT_JSON | bind-work INTAKE_JSON RESEARCH_BOUND_JSON AUTHORING_JSON OUT_JSON")
    except Exception as exc:
        print("CONCEPT_AGENT_INTAKE_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
