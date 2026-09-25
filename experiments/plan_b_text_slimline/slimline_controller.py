#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any

CONTRACT = "PFERDE_ATELIER_PLAN_B_SLIMLINE_CONTRACT_V1"
STATE_CONTRACT = "PFERDE_ATELIER_PLAN_B_STATE_V1"
TICKET_CONTRACT = "PFERDE_ATELIER_PLAN_B_TICKET_V1"
ITEM_RECEIPT = "PFERDE_ATELIER_BOUND_ITEM_EXECUTION_RECEIPT_V1"
FACH_PASS = "PFERDE_ATELIER_FACHWORKFLOW_PASS_V1"
STAGE_PROOF = "PFERDE_ATELIER_FACHWORKFLOW_STAGE_EXECUTION_PROOF_V1"
FINAL_REVIEW_RECEIPT = "PFERDE_ATELIER_PLAN_B_FINAL_REVIEW_RECEIPT_V1"
EXTERNAL_FINALIZE_RECEIPT = "PFERDE_ATELIER_PLAN_B_EXTERNAL_FINALIZE_RECEIPT_V1"
ENDSTAMP_RECEIPT = "PFERDE_ATELIER_PLAN_B_ENDSTAMP_RECEIPT_V1"
REQUIRED_STAGES = [
    "research_fact_pack", "textmachine_article_type_structure", "table_contract",
    "internal_links", "languagetool", "ppm", "pserc", "pste",
    "duplicate_cannibalization", "seo", "design_format", "publish_safety",
]
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

class Blocked(RuntimeError):
    pass

def canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def stable_hash(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()

def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise Blocked("JSON_OBJECT_REQUIRED")
    return obj

def dump_atomic(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)

def safe(repo: Path, ref: str, prefix: str | None = None) -> Path:
    p = Path(str(ref or ""))
    if not str(ref or "") or p.is_absolute() or ".." in p.parts:
        raise Blocked("REF_INVALID")
    q = (repo / p).resolve(); r = repo.resolve()
    if q != r and r not in q.parents:
        raise Blocked("REF_ESCAPE")
    if prefix is not None and not p.as_posix().startswith(prefix.rstrip("/") + "/"):
        raise Blocked("REF_OUTSIDE_BOUND_ROOT")
    return q

def require_sha(v: Any, token: str) -> str:
    s = str(v or "")
    if not SHA_RE.fullmatch(s):
        raise Blocked(token)
    return s

def validate_contract(path: Path) -> dict:
    c = load(path)
    if c.get("contract") != CONTRACT or c.get("mode") != "SHADOW_ONLY_NOT_PRODUCTION_BOUND":
        raise Blocked("CONTRACT_INVALID")
    if c.get("single_door") is not True or c.get("publish_allowed") is not False:
        raise Blocked("CONTRACT_HARD_RULE_INVALID")
    g = c.get("guard") or {}; chat = c.get("chat") or {}; q = c.get("quality") or {}
    if g.get("semantics") != "DUMB_EXACT_BINDING_ONLY" or g.get("domain_logic_authority") != "NONE" or g.get("workflow_choice_authority") != "NONE":
        raise Blocked("GUARD_NOT_DUMB")
    for key in ("workflow_navigation_authority","state_write_authority","next_step_choice_authority","repair_authority","publish_authority"):
        if chat.get(key) is not False:
            raise Blocked("CHAT_NOT_STRAITJACKETED:" + key)
    if q.get("unchanged") is not True or q.get("required_stage_count") != 12 or q.get("required_stages") != REQUIRED_STAGES:
        raise Blocked("QUALITY_CONTRACT_CHANGED")
    return c

def ticket_body(state: dict) -> dict:
    if state["phase"] == "ITEM_WORK":
        item = state["items"][state["item_index"]]
        action = "EXECUTE_EXISTING_UNCHANGED_12_STAGE_FACHWORKFLOW_FOR_BOUND_ITEM"
        subject = {"canonical_article_id": item["canonical_article_id"], "plan_slot": item["plan_slot"], "allowed_output_root": item["allowed_output_root"]}
    elif state["phase"] == "FINAL_REVIEW":
        action = "EXECUTE_EXISTING_FINAL_REVIEW_ON_PREPARED_BATCH_ONLY"
        subject = {"prepared_ref": state["prepared_ref"], "prepared_sha256": state["prepared_sha256"], "batch_sha256": state["batch_sha256"]}
    elif state["phase"] == "EXTERNAL_FINALIZE":
        action = "EXECUTE_EXISTING_EXTERNAL_PSERC_FINALIZATION"
        subject = {"batch_sha256": state["batch_sha256"]}
    elif state["phase"] == "GITHUB_ENDSTAMP":
        action = "EXECUTE_EXISTING_GITHUB_ENDSTAMP"
        subject = {"batch_sha256": state["batch_sha256"], "external_package_ref": state["external_package_ref"], "external_package_sha256": state["external_package_sha256"]}
    elif state["phase"] == "COMPLETE":
        action = "STOP_COMPLETE"
        subject = {"batch_sha256": state["batch_sha256"]}
    else:
        raise Blocked("PHASE_INVALID")
    body = {"contract": TICKET_CONTRACT, "state_id": state["state_id"], "batch_sha256": state["batch_sha256"], "phase": state["phase"], "action": action, "subject": subject, "publish_allowed": False}
    body["ticket_id"] = stable_hash(body)
    return body

def validate_item_receipt(repo: Path, state: dict, receipt: dict) -> dict:
    item = state["items"][state["item_index"]]
    required = {"contract","ticket_id","batch_sha256","canonical_article_id","plan_slot","status","workflow_pass","navigation_decision","state_write_requested","workflow_change_requested","content_or_quality_rules_changed","outputs","evidence","fachworkflow_pass_ref","fachworkflow_pass_sha256","publish_allowed"}
    if set(receipt) != required or receipt.get("contract") != ITEM_RECEIPT:
        raise Blocked("ITEM_RECEIPT_FIELDS_OR_CONTRACT_INVALID")
    if receipt.get("ticket_id") != ticket_body(state)["ticket_id"] or receipt.get("batch_sha256") != state["batch_sha256"]:
        raise Blocked("ITEM_RECEIPT_TICKET_OR_BATCH_MISMATCH")
    if receipt.get("canonical_article_id") != item["canonical_article_id"] or receipt.get("plan_slot") != item["plan_slot"]:
        raise Blocked("ITEM_RECEIPT_IDENTITY_MISMATCH")
    if receipt.get("status") != "PASS" or receipt.get("workflow_pass") is not True:
        raise Blocked("ITEM_RECEIPT_NOT_PASS")
    for key in ("navigation_decision","state_write_requested","workflow_change_requested","content_or_quality_rules_changed","publish_allowed"):
        if receipt.get(key) is not False:
            raise Blocked("ITEM_RECEIPT_FORBIDDEN_AUTHORITY:" + key)
    ev = receipt.get("evidence")
    if not isinstance(ev, list) or not ev or not all(isinstance(x, str) and x.strip() for x in ev):
        raise Blocked("ITEM_RECEIPT_EVIDENCE_INVALID")
    root = item["allowed_output_root"]
    outs = receipt.get("outputs")
    if not isinstance(outs, list) or not outs:
        raise Blocked("ITEM_OUTPUTS_MISSING")
    seen=set()
    for row in outs:
        if not isinstance(row, dict) or set(row) != {"ref","sha256"}:
            raise Blocked("ITEM_OUTPUT_ROW_INVALID")
        ref = str(row["ref"]); digest = require_sha(row["sha256"], "ITEM_OUTPUT_HASH_INVALID")
        if ref in seen: raise Blocked("ITEM_OUTPUT_DUPLICATE")
        seen.add(ref)
        p = safe(repo, ref, root)
        if not p.is_file() or file_sha(p) != digest:
            raise Blocked("ITEM_OUTPUT_HASH_MISMATCH")
    pref = str(receipt.get("fachworkflow_pass_ref") or "")
    pdig = require_sha(receipt.get("fachworkflow_pass_sha256"), "FACH_PASS_HASH_INVALID")
    pp = safe(repo, pref, root)
    if not pp.is_file() or file_sha(pp) != pdig:
        raise Blocked("FACH_PASS_HASH_MISMATCH")
    fp = load(pp)
    if fp.get("contract") != FACH_PASS or fp.get("status") != "PASS" or fp.get("batch_sha256") != state["batch_sha256"] or fp.get("canonical_article_id") != item["canonical_article_id"] or fp.get("plan_slot") != item["plan_slot"] or fp.get("publish_allowed") is not False or fp.get("content_or_quality_rules_changed") is not False:
        raise Blocked("FACH_PASS_IDENTITY_OR_STATUS_INVALID")
    rows = fp.get("required_stage_proofs")
    if not isinstance(rows, list) or len(rows) != 12:
        raise Blocked("STAGE_PROOF_COUNT_INVALID")
    by_stage={}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"stage","ref","sha256"}:
            raise Blocked("STAGE_PROOF_ROW_INVALID")
        stage=str(row["stage"])
        if stage in by_stage: raise Blocked("STAGE_PROOF_DUPLICATE")
        by_stage[stage]=row
    if list(sorted(by_stage)) != list(sorted(REQUIRED_STAGES)):
        raise Blocked("STAGE_SET_INVALID")
    for stage in REQUIRED_STAGES:
        row=by_stage[stage]; sp=safe(repo,str(row["ref"]),root); sd=require_sha(row["sha256"],"STAGE_PROOF_HASH_INVALID")
        if not sp.is_file() or file_sha(sp)!=sd: raise Blocked("STAGE_PROOF_HASH_MISMATCH:"+stage)
        proof=load(sp)
        if proof.get("contract")!=STAGE_PROOF or proof.get("status")!="PASS" or proof.get("stage")!=stage or proof.get("batch_sha256")!=state["batch_sha256"] or proof.get("canonical_article_id")!=item["canonical_article_id"] or proof.get("plan_slot")!=item["plan_slot"] or proof.get("execution_performed") is not True or proof.get("publish_allowed") is not False or proof.get("content_or_quality_rules_changed") is not False:
            raise Blocked("STAGE_PROOF_INVALID:"+stage)
        require_sha(proof.get("input_sha256"),"STAGE_INPUT_HASH_INVALID:"+stage)
        arts=proof.get("artifacts")
        if not isinstance(arts,list) or not arts: raise Blocked("STAGE_ARTIFACTS_MISSING:"+stage)
        for art in arts:
            if not isinstance(art,dict) or set(art)!={"ref","sha256"}: raise Blocked("STAGE_ARTIFACT_ROW_INVALID:"+stage)
            ap=safe(repo,str(art["ref"]),root); ad=require_sha(art["sha256"],"STAGE_ARTIFACT_HASH_INVALID:"+stage)
            if not ap.is_file() or file_sha(ap)!=ad: raise Blocked("STAGE_ARTIFACT_HASH_MISMATCH:"+stage)
        if stage=="ppm":
            b=proof.get("ppm679_binding")
            keys={"ppm_version","ppm_package_sha256","article_type_templates_sha256","final_article_ref","final_article_sha256","ppm_report_ref","ppm_report_sha256"}
            if not isinstance(b,dict) or set(b)!=keys: raise Blocked("PPM_BINDING_INVALID")
            final_sha=require_sha(b.get("final_article_sha256"),"PPM_FINAL_SHA_INVALID"); report_sha=require_sha(b.get("ppm_report_sha256"),"PPM_REPORT_SHA_INVALID")
            finalp=safe(repo,str(b.get("final_article_ref")),root); reportp=safe(repo,str(b.get("ppm_report_ref")),root)
            if not finalp.is_file() or file_sha(finalp)!=final_sha or not reportp.is_file() or file_sha(reportp)!=report_sha: raise Blocked("PPM_BOUND_FILE_HASH_MISMATCH")
            report=load(reportp); checks=report.get("checks")
            if report.get("ok") is not True or report.get("technical_status")!="TECHNICAL_CHECK_OK" or report.get("content_quality_status")!="CONTENT_QUALITY_CHECK_OK" or report.get("content_hash")!=final_sha or not isinstance(checks,dict) or checks.get("content_hash")!=final_sha or checks.get("fail_closed_aggregate_status")!="PASS":
                raise Blocked("PPM_REPORT_NOT_EXACT_PASS")
    return {"outputs": outs, "fachworkflow_pass_ref": pref, "fachworkflow_pass_sha256": pdig}

def build_prepared(repo: Path, state: dict) -> tuple[str,str]:
    root = safe(repo, state["shadow_root"])
    root.mkdir(parents=True, exist_ok=True)
    prepared = {"contract":"PFERDE_ATELIER_PLAN_B_PREPARED_BATCH_V1","status":"PREPARED_NOT_VISIBLE","batch_sha256":state["batch_sha256"],"item_count":len(state["items"]),"item_results":state["item_results"],"publish_allowed":False}
    p = root / "PREPARED_BATCH.json"
    dump_atomic(p, prepared)
    return p.relative_to(repo.resolve()).as_posix(), file_sha(p)

def validate_phase_receipt(repo: Path, state: dict, receipt: dict) -> None:
    ticket=ticket_body(state)
    if receipt.get("ticket_id") != ticket["ticket_id"] or receipt.get("batch_sha256") != state["batch_sha256"] or receipt.get("status") != "PASS" or receipt.get("publish_allowed") is not False:
        raise Blocked("PHASE_RECEIPT_BINDING_OR_STATUS_INVALID")
    if state["phase"] == "FINAL_REVIEW":
        if receipt.get("contract") != FINAL_REVIEW_RECEIPT or receipt.get("prepared_ref") != state["prepared_ref"] or receipt.get("prepared_sha256") != state["prepared_sha256"] or receipt.get("reviewed_prepared_release_only") is not True:
            raise Blocked("FINAL_REVIEW_RECEIPT_INVALID")
    elif state["phase"] == "EXTERNAL_FINALIZE":
        if receipt.get("contract") != EXTERNAL_FINALIZE_RECEIPT:
            raise Blocked("EXTERNAL_FINALIZE_RECEIPT_INVALID")
        ref=str(receipt.get("package_ref") or ""); digest=require_sha(receipt.get("package_sha256"),"EXTERNAL_PACKAGE_SHA_INVALID")
        p=safe(repo,ref)
        if not p.is_file() or file_sha(p)!=digest: raise Blocked("EXTERNAL_PACKAGE_HASH_MISMATCH")
        pkg=load(p)
        if pkg.get("contract")!="PSERC_APPROVED_PRODUCTION_PACKAGE_V1" or pkg.get("publish_allowed") is not False:
            raise Blocked("EXTERNAL_PACKAGE_CONTRACT_INVALID")
        state["external_package_ref"]=ref; state["external_package_sha256"]=digest
    elif state["phase"] == "GITHUB_ENDSTAMP":
        if receipt.get("contract") != ENDSTAMP_RECEIPT:
            raise Blocked("ENDSTAMP_RECEIPT_INVALID")
        ref=str(receipt.get("final_ref") or ""); digest=require_sha(receipt.get("final_sha256"),"ENDSTAMP_FINAL_SHA_INVALID")
        p=safe(repo,ref)
        if not p.is_file() or file_sha(p)!=digest: raise Blocked("ENDSTAMP_FINAL_HASH_MISMATCH")
        pkg=load(p)
        if pkg.get("status")!="ENDSTEMPEL_PASS" or pkg.get("publish_allowed") is not False or pkg.get("content_mutation_performed") is not False:
            raise Blocked("ENDSTAMP_FINAL_CONTRACT_INVALID")
    else:
        raise Blocked("PHASE_RECEIPT_NOT_ALLOWED")

def init_state(repo: Path, contract_path: Path, batch_path: Path, state_path: Path, shadow_root: str) -> dict:
    validate_contract(contract_path)
    batch=load(batch_path)
    batch_sha=require_sha(batch.get("batch_sha256"),"BATCH_SHA_INVALID")
    items=batch.get("items")
    if not isinstance(items,list) or not items: raise Blocked("BATCH_ITEMS_INVALID")
    clean=[]; seen=set()
    for row in items:
        if not isinstance(row,dict): raise Blocked("BATCH_ITEM_INVALID")
        cid=str(row.get("canonical_article_id") or ""); slot=require_sha(row.get("plan_slot"),"PLAN_SLOT_INVALID")
        if not cid or cid in seen: raise Blocked("BATCH_ITEM_ID_INVALID")
        seen.add(cid)
        clean.append({"canonical_article_id":cid,"plan_slot":slot,"allowed_output_root":f"{shadow_root.rstrip('/')}/items/{slot}/"})
    state={"contract":STATE_CONTRACT,"state_id":"","batch_sha256":batch_sha,"items":clean,"item_index":0,"item_results":[],"phase":"ITEM_WORK","status":"ACTIVE","shadow_root":shadow_root.rstrip("/"),"prepared_ref":"","prepared_sha256":"","external_package_ref":"","external_package_sha256":"","publish_allowed":False}
    state["state_id"]=stable_hash({k:v for k,v in state.items() if k!="state_id"})
    dump_atomic(state_path,state)
    return state

def submit(repo: Path, contract_path: Path, state_path: Path, receipt_path: Path) -> dict:
    validate_contract(contract_path)
    state=load(state_path)
    if state.get("contract")!=STATE_CONTRACT or state.get("status")!="ACTIVE" or state.get("publish_allowed") is not False:
        raise Blocked("STATE_INVALID_OR_INACTIVE")
    receipt=load(receipt_path)
    if state["phase"]=="ITEM_WORK":
        result=validate_item_receipt(repo,state,receipt)
        state["item_results"].append({"canonical_article_id":state["items"][state["item_index"]]["canonical_article_id"],"plan_slot":state["items"][state["item_index"]]["plan_slot"],**result})
        state["item_index"]+=1
        if state["item_index"]>=len(state["items"]):
            pref,pdig=build_prepared(repo,state); state["prepared_ref"]=pref; state["prepared_sha256"]=pdig; state["phase"]="FINAL_REVIEW"
    elif state["phase"]=="FINAL_REVIEW":
        validate_phase_receipt(repo,state,receipt); state["phase"]="EXTERNAL_FINALIZE"
    elif state["phase"]=="EXTERNAL_FINALIZE":
        validate_phase_receipt(repo,state,receipt); state["phase"]="GITHUB_ENDSTAMP"
    elif state["phase"]=="GITHUB_ENDSTAMP":
        validate_phase_receipt(repo,state,receipt); state["phase"]="COMPLETE"; state["status"]="COMPLETE"
    else:
        raise Blocked("SUBMIT_NOT_ALLOWED")
    dump_atomic(state_path,state)
    return {"ok":True,"status":"AUTO_ADVANCED" if state["status"]=="ACTIVE" else "COMPLETE","next":ticket_body(state),"publish_allowed":False}

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("command",choices=["init","current","submit","status"])
    ap.add_argument("--repo",default=".")
    ap.add_argument("--contract",required=True)
    ap.add_argument("--state",required=True)
    ap.add_argument("--batch")
    ap.add_argument("--receipt")
    ap.add_argument("--shadow-root",default=".plan-b-shadow")
    a=ap.parse_args(); repo=Path(a.repo).resolve(); cp=Path(a.contract).resolve(); sp=Path(a.state).resolve()
    try:
        if a.command=="init":
            if not a.batch: raise Blocked("BATCH_REQUIRED")
            out=init_state(repo,cp,Path(a.batch).resolve(),sp,a.shadow_root)
            result={"ok":True,"status":"INITIALIZED","next":ticket_body(out),"publish_allowed":False}
        elif a.command=="current":
            validate_contract(cp); s=load(sp); result={"ok":True,"status":s["status"],"next":ticket_body(s),"publish_allowed":False}
        elif a.command=="submit":
            if not a.receipt: raise Blocked("RECEIPT_REQUIRED")
            result=submit(repo,cp,sp,Path(a.receipt).resolve())
        else:
            validate_contract(cp); s=load(sp); result={"ok":True,"status":s["status"],"phase":s["phase"],"item_index":s["item_index"],"item_count":len(s["items"]),"publish_allowed":False}
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except Exception as exc:
        print(json.dumps({"ok":False,"status":"HARD_BLOCK","reason":str(exc),"publish_allowed":False},ensure_ascii=False,indent=2)); return 2

if __name__=="__main__":
    raise SystemExit(main())
