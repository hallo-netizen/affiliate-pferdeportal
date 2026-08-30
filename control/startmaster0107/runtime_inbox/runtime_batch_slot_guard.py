#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, hashlib, hmac, json, re, sys
from pathlib import Path

SHA_RE = re.compile(r"^[a-f0-9]{64}$")
STATE_KEYS = {
    "contract","status","generation","source_snapshot_ref","source_snapshot_sha256",
    "source_manifest_sha256","batch_sha256","production_package_ref",
    "production_package_sha256","publish_allowed"
}
EXACT_META_KEYS = {"title","target_keyword","category","article_type","plan_slot"}

class Blocked(RuntimeError):
    pass

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stable_hash(obj) -> str:
    raw=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def rel(repo: Path, value: str) -> Path:
    p=Path(str(value or ""))
    if not str(value or "") or p.is_absolute() or ".." in p.parts:
        raise Blocked("RUNTIME_REF_INVALID")
    full=(repo/p).resolve()
    root=repo.resolve()
    if root not in full.parents and full != root:
        raise Blocked("RUNTIME_REF_ESCAPE")
    return full

def valid_sha(v) -> bool:
    return isinstance(v,str) and bool(SHA_RE.fullmatch(v))

def exact_keys(obj, expected, code):
    if not isinstance(obj,dict) or set(obj) != set(expected):
        raise Blocked(code)

def validate_batch(batch: dict, contract: dict):
    if not isinstance(batch,dict):
        raise Blocked("BATCH_MISSING")
    if batch.get("contract") != contract["batch_contract"]:
        raise Blocked("BATCH_CONTRACT_INVALID")
    if batch.get("status") != contract["ready_status"]:
        raise Blocked("BATCH_NOT_READY")
    count=batch.get("item_count")
    items=batch.get("items")
    if not isinstance(count,int) or count < 1 or not isinstance(items,list) or len(items) != count:
        raise Blocked("BATCH_COUNT_INVALID")
    if batch.get("publish_allowed") is not False:
        raise Blocked("BATCH_PUBLISH_MUST_BE_FALSE")
    if batch.get("content_or_format_payload_present") is not False:
        raise Blocked("BATCH_CONTENT_PAYLOAD_FORBIDDEN")
    required=set(contract["required_metadata_fields"])
    if required != EXACT_META_KEYS:
        raise Blocked("CONTRACT_META_FIELDS_INVALID")
    slots=set()
    for i,item in enumerate(items):
        if not isinstance(item,dict) or set(item) != required:
            raise Blocked(f"BATCH_ITEM_FIELDS_INVALID:{i}")
        if not all(isinstance(item[k],str) and item[k].strip() for k in required):
            raise Blocked(f"BATCH_ITEM_SCALAR_INVALID:{i}")
        slot=item["plan_slot"]
        if not valid_sha(slot) or slot in slots:
            raise Blocked(f"BATCH_PLAN_SLOT_INVALID_OR_DUPLICATE:{i}")
        slots.add(slot)
    declared=batch.get("batch_sha256")
    if not valid_sha(declared):
        raise Blocked("BATCH_HASH_INVALID")
    payload=copy.deepcopy(batch)
    payload.pop("batch_sha256",None)
    actual=stable_hash(payload)
    if not hmac.compare_digest(actual,declared):
        raise Blocked("BATCH_HASH_MISMATCH")
    return {"batch_sha256":actual,"items":items,"slots":slots}

def validate_snapshot(repo: Path, state: dict, contract: dict):
    snap_path=rel(repo,state["source_snapshot_ref"])
    if not snap_path.is_file():
        raise Blocked("SOURCE_SNAPSHOT_MISSING")
    if not valid_sha(state["source_snapshot_sha256"]) or not hmac.compare_digest(sha_file(snap_path),state["source_snapshot_sha256"]):
        raise Blocked("SOURCE_SNAPSHOT_HASH_MISMATCH")
    snap=load(snap_path)
    manifest=snap.get("manifest_sha256")
    if not valid_sha(manifest) or not valid_sha(state["source_manifest_sha256"]) or not hmac.compare_digest(manifest,state["source_manifest_sha256"]):
        raise Blocked("SOURCE_MANIFEST_HASH_MISMATCH")
    batch=snap.get("next_textmachine_metadata_batch")
    checked=validate_batch(batch,contract)
    if not valid_sha(state["batch_sha256"]) or not hmac.compare_digest(checked["batch_sha256"],state["batch_sha256"]):
        raise Blocked("STATE_BATCH_HASH_MISMATCH")
    return snap_path,snap,batch,checked

def validate_package(repo: Path, state: dict, contract: dict, batch: dict, checked: dict):
    pkg_path=rel(repo,state["production_package_ref"])
    if not pkg_path.is_file():
        raise Blocked("PRODUCTION_PACKAGE_MISSING")
    if not valid_sha(state["production_package_sha256"]) or not hmac.compare_digest(sha_file(pkg_path),state["production_package_sha256"]):
        raise Blocked("PRODUCTION_PACKAGE_FILE_HASH_MISMATCH")
    env=load(pkg_path)
    expected={"contract","fact_pack_bundle_sha256","production_plan_sha256","workflow_release_sha256","package_id","source","fact_pack_bundle","production_plan","workflow_release","package_payload_sha256"}
    exact_keys(env,expected,"PRODUCTION_PACKAGE_SCHEMA_INVALID")
    if env.get("contract") != contract["production_package_contract"]:
        raise Blocked("PRODUCTION_PACKAGE_CONTRACT_INVALID")
    bundle=env.get("fact_pack_bundle"); plan=env.get("production_plan"); release=env.get("workflow_release")
    if not all(isinstance(x,dict) for x in (bundle,plan,release)):
        raise Blocked("PRODUCTION_PACKAGE_COMPONENT_INVALID")
    component_hashes={
        "fact_pack_bundle_sha256":stable_hash(bundle),
        "production_plan_sha256":stable_hash(plan),
        "workflow_release_sha256":stable_hash(release)
    }
    for field,actual in component_hashes.items():
        if not valid_sha(env.get(field)) or not hmac.compare_digest(env[field],actual):
            raise Blocked(f"PRODUCTION_PACKAGE_COMPONENT_HASH_MISMATCH:{field}")
    expected_id=stable_hash({
        "contract":contract["production_package_contract"],
        "fact_pack_bundle_sha256":component_hashes["fact_pack_bundle_sha256"],
        "production_plan_sha256":component_hashes["production_plan_sha256"],
        "workflow_release_sha256":component_hashes["workflow_release_sha256"]
    })
    if not valid_sha(env.get("package_id")) or not hmac.compare_digest(env["package_id"],expected_id):
        raise Blocked("PRODUCTION_PACKAGE_ID_MISMATCH")
    payload=copy.deepcopy(env); declared_payload=payload.pop("package_payload_sha256",None)
    if not valid_sha(declared_payload) or not hmac.compare_digest(stable_hash(payload),declared_payload):
        raise Blocked("PRODUCTION_PACKAGE_PAYLOAD_HASH_MISMATCH")
    if release.get("contract") != contract["workflow_release_contract"] or release.get("status") != "PASS":
        raise Blocked("WORKFLOW_RELEASE_SHAPE_INVALID")
    if release.get("signature_algorithm") != "ED25519" or not isinstance(release.get("signature_b64"),str) or not release["signature_b64"].strip():
        raise Blocked("WORKFLOW_RELEASE_SIGNATURE_METADATA_INVALID")
    release_items=release.get("items")
    if not isinstance(release_items,list) or not release_items:
        raise Blocked("WORKFLOW_RELEASE_ITEMS_EMPTY")
    current={x["plan_slot"]:x for x in checked["items"]}
    selected=[]; seen=set()
    for i,row in enumerate(release_items):
        if not isinstance(row,dict):
            raise Blocked(f"WORKFLOW_RELEASE_ITEM_INVALID:{i}")
        slot=row.get("plan_slot")
        if not valid_sha(slot) or slot in seen:
            raise Blocked(f"WORKFLOW_RELEASE_SLOT_INVALID_OR_DUPLICATE:{i}")
        if slot not in current:
            raise Blocked(f"WORKFLOW_RELEASE_SLOT_NOT_CURRENT_READY:{i}")
        seen.add(slot); selected.append(current[slot])
    signed_batch=copy.deepcopy(batch)
    signed_batch["items"]=selected
    signed_batch["item_count"]=len(selected)
    signed_batch.pop("batch_sha256",None)
    signed_batch_hash=stable_hash(signed_batch)
    if not valid_sha(release.get("exact_five_batch_sha256")) or not hmac.compare_digest(signed_batch_hash,release["exact_five_batch_sha256"]):
        raise Blocked("WORKFLOW_RELEASE_BATCH_HASH_MISMATCH")
    if int(release.get("exact_five_item_count",-1)) != len(selected):
        raise Blocked("WORKFLOW_RELEASE_BATCH_COUNT_MISMATCH")
    if not hmac.compare_digest(str(release.get("production_plan_sha256","")),component_hashes["production_plan_sha256"]):
        raise Blocked("WORKFLOW_RELEASE_PLAN_HASH_MISMATCH")
    if not hmac.compare_digest(str(release.get("fact_pack_bundle_sha256","")),component_hashes["fact_pack_bundle_sha256"]):
        raise Blocked("WORKFLOW_RELEASE_FACT_PACK_HASH_MISMATCH")
    return pkg_path,env,selected,signed_batch_hash

def validate(repo: Path, contract_path: Path, state_path: Path):
    contract=load(contract_path)
    if contract.get("contract") != "PFERDE_ATELIER_RUNTIME_BATCH_SLOT_CONTRACT_V1":
        raise Blocked("SLOT_CONTRACT_INVALID")
    state=load(state_path)
    exact_keys(state,STATE_KEYS,"RUNTIME_STATE_SCHEMA_INVALID")
    if state.get("contract") != "PFERDE_ATELIER_RUNTIME_BATCH_SLOT_STATE_V1":
        raise Blocked("RUNTIME_STATE_CONTRACT_INVALID")
    if state.get("publish_allowed") is not False:
        raise Blocked("RUNTIME_PUBLISH_MUST_BE_FALSE")
    if not isinstance(state.get("generation"),int) or state["generation"] < 0:
        raise Blocked("RUNTIME_GENERATION_INVALID")
    status=state.get("status")
    if status not in contract.get("allowed_states",[]):
        raise Blocked("RUNTIME_STATUS_INVALID")
    dynamic_fields=["source_snapshot_ref","source_snapshot_sha256","source_manifest_sha256","batch_sha256","production_package_ref","production_package_sha256"]
    if status=="NO_ACTIVE_BATCH":
        if any(state.get(k) not in ("",None) for k in dynamic_fields):
            raise Blocked("IDLE_STATE_MUST_BE_EMPTY")
        return {"ok":True,"status":"READY_IDLE","generation":state["generation"],"terminal":False,"write_receipt":False,"publish_allowed":False}
    if state["generation"] < 1:
        raise Blocked("ACTIVE_GENERATION_INVALID")
    snap_path,snap,batch,checked=validate_snapshot(repo,state,contract)
    if status=="BATCH_READY_PACKAGE_PENDING":
        if state.get("production_package_ref") not in ("",None) or state.get("production_package_sha256") not in ("",None):
            raise Blocked("PENDING_PACKAGE_FIELDS_MUST_BE_EMPTY")
        return {"ok":True,"status":"READY_WAITING_PACKAGE","generation":state["generation"],"terminal":False,"write_receipt":False,"batch_sha256":checked["batch_sha256"],"item_count":len(checked["items"]),"source_snapshot":str(snap_path.relative_to(repo)),"publish_allowed":False}
    pkg_path,env,selected,signed_hash=validate_package(repo,state,contract,batch,checked)
    return {
        "ok":True,"status":"RUNTIME_INPUTS_BOUND","generation":state["generation"],"terminal":False,"write_receipt":False,
        "batch_sha256":checked["batch_sha256"],"ready_item_count":len(checked["items"]),
        "selected_item_count":len(selected),"signed_batch_sha256":signed_hash,
        "source_snapshot":str(snap_path.relative_to(repo)),"production_package":str(pkg_path.relative_to(repo)),
        "package_id":env["package_id"],"publish_allowed":False,
        "signature_note":"ED25519 authenticity remains enforced by the existing PSERC Workflow Supervisor at runtime"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("state")
    ap.add_argument("--contract",required=True)
    ap.add_argument("--repo",default=".")
    a=ap.parse_args()
    repo=Path(a.repo).resolve()
    try:
        out=validate(repo,Path(a.contract).resolve(),Path(a.state).resolve())
        print(json.dumps(out,ensure_ascii=False,indent=2))
        return 0
    except (Blocked,ValueError,KeyError,TypeError,json.JSONDecodeError) as e:
        print(json.dumps({"ok":False,"status":"RUNTIME_BATCH_SLOT_BLOCKED","error":str(e),"publish_allowed":False},ensure_ascii=False,indent=2))
        return 2

if __name__=="__main__":
    raise SystemExit(main())
