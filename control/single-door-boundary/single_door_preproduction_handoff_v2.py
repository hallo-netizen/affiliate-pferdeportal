#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,sys
from pathlib import Path
from typing import Any,Callable,Mapping
HERE=Path(__file__).resolve().parent
BOUNDARY_PATH=HERE/"single_door_boundary.py"
ROOM_TOKEN="R_PRE_001";ACTION_TOKEN="A_PRE_001";INPUT_HANDLE="I_PRE_PACKAGE_001";RECEIPT_TOKEN="P_PRE_001";NEXT_ROOM_TOKEN="R_001"
class HandoffV2Blocked(RuntimeError): pass

def _module(path:Path,name:str):
    if not path.is_file(): raise HandoffV2Blocked("MODULE_MISSING:"+path.name)
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise HandoffV2Blocked("MODULE_LOAD_FAILED:"+path.name)
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod

def boundary_module(): return _module(BOUNDARY_PATH,"single_door_boundary_h81_pre")
def binding(boundary=None):
    boundary=boundary or boundary_module()
    return boundary.DoorBinding.from_mapping({"contract":boundary.BOUNDARY_CONTRACT,"room_token":ROOM_TOKEN,"action_token":ACTION_TOKEN,"receipt_token":RECEIPT_TOKEN,"next_room_token":NEXT_ROOM_TOKEN,"input_handles":[INPUT_HANDLE]})
def worker_request(model:str,boundary=None)->dict[str,Any]:
    boundary=boundary or boundary_module();return boundary.build_worker_request(binding=binding(boundary),model=model)
def resolve_handle(handle_map:Mapping[str,str],repo:Path)->Path:
    if set(handle_map)!={INPUT_HANDLE}: raise HandoffV2Blocked("HANDLE_MAP_INVALID")
    rel=Path(str(handle_map.get(INPUT_HANDLE) or ""))
    if not str(rel) or rel.is_absolute() or ".." in rel.parts: raise HandoffV2Blocked("HANDLE_PATH_INVALID")
    full=(repo.resolve()/rel).resolve()
    if repo.resolve() not in full.parents: raise HandoffV2Blocked("HANDLE_PATH_ESCAPE")
    return full

def execute_bound_preproduction_action(*,handle_map:Mapping[str,str],repo:Path,attach_callable:Callable[[Path],Mapping[str,Any]],boundary=None)->dict[str,Any]:
    repo=Path(repo).resolve();boundary=boundary or boundary_module();b=binding(boundary);package=resolve_handle(handle_map,repo)
    prov=_module(repo/"control/single-door-boundary/preproduction_provenance_guard_v2.py","h81_pre_prov");proof=prov.validate_signed_existing_process(repo,package)
    if proof.get("status")!="H81_PREPRODUCTION_PROVENANCE_PASS": raise HandoffV2Blocked("PREPRODUCTION_PROVENANCE_NOT_PASS")
    result=attach_callable(package)
    if not isinstance(result,Mapping) or result.get("status")!="RUNTIME_BATCH_EXECUTION_READY": raise HandoffV2Blocked("ATTACH_DID_NOT_REACH_EXECUTION_READY")
    receipt={"contract":boundary.BOUNDARY_CONTRACT,"room_token":ROOM_TOKEN,"action_token":ACTION_TOKEN,"receipt_token":RECEIPT_TOKEN,"next_room_token":NEXT_ROOM_TOKEN,"status":"PASS","evidence":["H81_ENTRY_RECEIPT:"+str(proof.get("entry_receipt_sha256")),"SIGNED_CURRENT_GENERATION_PACKAGE:"+str(proof.get("artifact_sha256")),"RUNTIME_BATCH_EXECUTION_READY"]}
    return boundary.validate_action_receipt(b,receipt)

def attach_via_current_lifecycle(*,repo:Path,handle_map:Mapping[str,str],boundary=None)->dict[str,Any]:
    repo=Path(repo).resolve();life=_module(repo/"control/startmaster0107/runtime_inbox/runtime_batch_slot_lifecycle.py","h81_lifecycle");contract=repo/"control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json"
    return execute_bound_preproduction_action(handle_map=handle_map,repo=repo,attach_callable=lambda p:life.attach_package(repo,contract,str(p)),boundary=boundary)
def main()->int:
    try:
        req=worker_request("gpt-5.6-sol");print(json.dumps({"ok":True,"status":"H81_PREPRODUCTION_PACKAGE_SINGLE_DOOR_READY","room_token":req["input"],"tool_count":len(req["tools"]),"next_room_token":NEXT_ROOM_TOKEN,"quality_authority":"NONE","content_semantics_inspected":False},indent=2));return 0
    except Exception as exc: print(json.dumps({"ok":False,"status":"H81_PREPRODUCTION_HANDOFF_BLOCKED","error":str(exc),"publish_allowed":False},indent=2));return 2
if __name__=="__main__": raise SystemExit(main())
