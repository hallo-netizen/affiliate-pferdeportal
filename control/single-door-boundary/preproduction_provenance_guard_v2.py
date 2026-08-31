#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,sys
from datetime import datetime,timezone
from pathlib import Path
from typing import Any,Callable,Mapping
HERE=Path(__file__).resolve().parent
EXPECTED_SEQUENCE=["START_GATE_PASS","ASSIGNMENT_AND_PLAN_SLOT_BOUND","FINAL_TITLE_LOCKED","EXACT_FIVE_PASS","RESEARCH_EVIDENCE_GATE_PASS","AUTHORIZED_0039_RESEARCH_TEXT_PROCESS","ARTICLE_ORIGIN_AND_IMMUTABILITY_GATE_PASS","LANGUAGE_AND_QUALITY_PASS","FACT_PACK_AND_PLAN_BOUND","PPM_6_7_9_READY"]
EXPECTED_AUTHORING_ROLE="CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS"
EXPECTED_AUTHORING_PROCESS="STARTMASTER_0039_CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS"
class ProvenanceV2Blocked(RuntimeError): pass

def _module(path:Path,name:str):
    if not path.is_file(): raise ProvenanceV2Blocked("MODULE_MISSING:"+path.name)
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise ProvenanceV2Blocked("MODULE_LOAD_FAILED:"+path.name)
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod

def _time(value:Any,code:str)->datetime:
    try: dt=datetime.fromisoformat(str(value).replace("Z","+00:00"))
    except Exception as exc: raise ProvenanceV2Blocked(code) from exc
    if dt.tzinfo is None: raise ProvenanceV2Blocked(code)
    return dt.astimezone(timezone.utc)

def _entry_receipt(repo:Path)->dict[str,Any]:
    author=_module(repo/"control/single-door-boundary/single_door_authoring_entry.py","h81_prov_author")
    cur=author.current_binding(repo);p=author.entry_receipt_path(repo,cur["generation"])
    if not p.is_file(): raise ProvenanceV2Blocked("H81_PREPRODUCTION_ENTRY_RECEIPT_MISSING")
    try: receipt=json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc: raise ProvenanceV2Blocked("H81_PREPRODUCTION_ENTRY_RECEIPT_JSON_INVALID") from exc
    return author.validate_entry_receipt(repo,receipt)

def validate_signed_existing_process(repo:Path,package_path:Path,*,release_validator:Callable[[Path,Path],Mapping[str,Any]]|None=None,entry_receipt_provider:Callable[[Path],Mapping[str,Any]]|None=None)->dict[str,Any]:
    repo=Path(repo).resolve();package_path=Path(package_path).resolve();receipt=dict((entry_receipt_provider or _entry_receipt)(repo))
    if release_validator is None:
        gate=_module(repo/"control/startmaster0107/production-package-release/production_package_release_gate.py","h81_release_gate")
        proof=gate.validate_package(package_path,repo,True)
    else: proof=dict(release_validator(package_path,repo))
    if not proof.get("ok"): raise ProvenanceV2Blocked("H81_EXISTING_SIGNED_PACKAGE_VALIDATION_FAILED")
    env=json.loads(package_path.read_text(encoding="utf-8"));release=env.get("workflow_release")
    if not isinstance(release,dict) or release.get("contract")!="WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED" or release.get("status")!="PASS": raise ProvenanceV2Blocked("H81_WORKFLOW_RELEASE_SHAPE_INVALID")
    if release.get("authoring_role")!=EXPECTED_AUTHORING_ROLE: raise ProvenanceV2Blocked("H81_AUTHORING_ROLE_INVALID")
    if list(release.get("sequence") or [])!=EXPECTED_SEQUENCE: raise ProvenanceV2Blocked("H81_SUPERVISOR_SEQUENCE_INVALID")
    if release.get("content_generation_performed_by_supervisor") is not False or release.get("wordpress_write_performed") is not False: raise ProvenanceV2Blocked("H81_SUPERVISOR_ROLE_BOUNDARY_INVALID")
    items=release.get("items")
    if not isinstance(items,list) or not items: raise ProvenanceV2Blocked("H81_WORKFLOW_RELEASE_ITEMS_MISSING")
    for i,item in enumerate(items):
        if not isinstance(item,dict): raise ProvenanceV2Blocked(f"H81_WORKFLOW_RELEASE_ITEM_INVALID:{i}")
        if item.get("authoring_process")!=EXPECTED_AUTHORING_PROCESS: raise ProvenanceV2Blocked(f"H81_UNAUTHORIZED_AUTHORING_PROCESS:{i}")
        if item.get("research_evidence_gate_status")!="PASS" or item.get("article_origin_gate_status")!="PASS" or item.get("language_quality_gate_status")!="PASS": raise ProvenanceV2Blocked(f"H81_REQUIRED_GATE_NOT_PASS:{i}")
        if item.get("external_rewrite_detected") is not False or item.get("trusted_self_approval") is not False or item.get("content_hash_locked") is not True: raise ProvenanceV2Blocked(f"H81_ORIGIN_IMMUTABILITY_INVALID:{i}")
    if _time(release.get("created_at_utc"),"H81_RELEASE_TIME_INVALID")<_time(receipt.get("created_at_utc"),"H81_ENTRY_TIME_INVALID"): raise ProvenanceV2Blocked("H81_RELEASE_PREDATES_FIRST_DOOR")
    return {"ok":True,"status":"H81_PREPRODUCTION_PROVENANCE_PASS","package_id":proof.get("package_id"),"artifact_sha256":proof.get("artifact_sha256"),"entry_receipt_sha256":receipt.get("receipt_sha256"),"authoring_role":EXPECTED_AUTHORING_ROLE,"authoring_process":EXPECTED_AUTHORING_PROCESS,"quality_authority":"NONE","content_semantics_inspected":False,"publish_allowed":False}

def validate_attached_package(repo:Path,*,release_validator=None,entry_receipt_provider=None)->dict[str,Any]:
    repo=Path(repo).resolve();state=json.loads((repo/"control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json").read_text(encoding="utf-8"))
    if state.get("status")!="EXECUTION_READY": raise ProvenanceV2Blocked("H81_ATTACHED_PROVENANCE_REQUIRES_EXECUTION_READY")
    ref=Path(str(state.get("production_package_ref") or ""))
    if not str(ref) or ref.is_absolute() or ".." in ref.parts: raise ProvenanceV2Blocked("H81_ATTACHED_PACKAGE_REF_INVALID")
    package=(repo/ref).resolve()
    if repo not in package.parents: raise ProvenanceV2Blocked("H81_ATTACHED_PACKAGE_REF_ESCAPE")
    return validate_signed_existing_process(repo,package,release_validator=release_validator,entry_receipt_provider=entry_receipt_provider)

def main()->int:
    try: print(json.dumps(validate_attached_package(HERE.parents[1]),ensure_ascii=False,indent=2));return 0
    except Exception as exc: print(json.dumps({"ok":False,"status":"H81_PREPRODUCTION_PROVENANCE_BLOCKED","error":str(exc),"publish_allowed":False},ensure_ascii=False,indent=2));return 2
if __name__=="__main__": raise SystemExit(main())
