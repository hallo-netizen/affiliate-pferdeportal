#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
from typing import Any,Callable,Mapping
HERE=Path(__file__).resolve().parent
REPO_ROOT=HERE.parents[1]
PROJECT_ENTRY_CONTRACT="PFERDE_ATELIER_PROJECT_SINGLE_DOOR_ENTRY_V3"
H81_BOUNDARY_CONTRACT="PFERDE_ATELIER_H81_PREPRODUCTION_AUTHORING_BOUNDARY_V1"
class ProjectEntryBlocked(RuntimeError): pass

def _module(path:Path,name:str):
    if not path.is_file(): raise ProjectEntryBlocked("MODULE_MISSING:"+path.name)
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise ProjectEntryBlocked("MODULE_LOAD_FAILED:"+path.name)
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod

def _git_blob_sha1(path:Path)->str:
    raw=path.read_bytes();return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()

def _pointer_authority(repo:Path)->None:
    repo=repo.resolve();obj=json.loads((repo/"control/CURRENT_STARTMASTER.json").read_text(encoding="utf-8"))
    if obj.get("startmaster")!="STARTMASTER0107": raise ProjectEntryBlocked("STARTMASTER_NOT_0107")
    if obj.get("free_chat_execution_authority") is not False: raise ProjectEntryBlocked("FREE_CHAT_AUTHORITY_MUST_BE_FALSE")
    expected="control/single-door-boundary/project_single_door_entry_v3.py"
    if obj.get("gate_ref")!=expected: raise ProjectEntryBlocked("PROJECT_GATE_REF_INVALID")
    ref=obj.get("h81_boundary_ref");blob=obj.get("h81_boundary_git_blob_sha1")
    if ref!="control/single-door-boundary/H81_PREPRODUCTION_AUTHORING_BOUNDARY.json": raise ProjectEntryBlocked("H81_BOUNDARY_REF_INVALID")
    mp=repo/ref
    if not mp.is_file() or _git_blob_sha1(mp)!=blob: raise ProjectEntryBlocked("H81_BOUNDARY_HASH_MISMATCH")
    manifest=json.loads(mp.read_text(encoding="utf-8"))
    if manifest.get("contract")!=H81_BOUNDARY_CONTRACT or manifest.get("domain_blind") is not True or manifest.get("quality_authority")!="NONE" or manifest.get("content_semantics_authority")!="NONE": raise ProjectEntryBlocked("H81_BOUNDARY_INVALID")
    seen=set()
    for row in manifest.get("file_bindings") or []:
        if not isinstance(row,dict) or set(row)!={"ref","git_blob_sha1"}: raise ProjectEntryBlocked("H81_FILE_BINDING_INVALID")
        r=str(row["ref"]);seen.add(r);p=repo/r
        if not p.is_file() or _git_blob_sha1(p)!=row["git_blob_sha1"]: raise ProjectEntryBlocked("H81_FILE_BINDING_HASH_MISMATCH:"+r)
    if expected not in seen: raise ProjectEntryBlocked("H81_PROJECT_ENTRY_NOT_HASH_BOUND")

def current_runtime(repo:Path)->Mapping[str,Any]:
    guard=_module(repo/"control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py","h81_runtime_guard")
    return guard.validate(repo,repo/"control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json",repo/"control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json")

def resolve_entry(*,repo:Path,model:str="gpt-5.6-sol",runtime_provider:Callable[[Path],Mapping[str,Any]]|None=None,attached_provenance_provider:Callable[[Path],Mapping[str,Any]]|None=None,route_provider:Callable[[Path,int,str],Mapping[str,Any]]|None=None)->dict[str,Any]:
    repo=Path(repo).resolve();_pointer_authority(repo);runtime=dict((runtime_provider or current_runtime)(repo));status=runtime.get("status")
    if status=="READY_IDLE": return {"ok":True,"contract":PROJECT_ENTRY_CONTRACT,"status":"PROJECT_ARMED_NO_ACTIVE_BATCH","worker_request":None,"authoritative_execution_origin":"SINGLE_DOOR_ONLY","publish_allowed":False}
    if status=="READY_WAITING_PACKAGE":
        author=_module(repo/"control/single-door-boundary/single_door_authoring_entry.py","h81_author_entry")
        req=author.worker_request(model)
        return {"ok":True,"contract":PROJECT_ENTRY_CONTRACT,"status":"PREPRODUCTION_AUTHORING_SINGLE_DOOR_REQUIRED","room_token":author.ROOM_TOKEN,"worker_request":req,"bound_executor":author.BOUND_EXECUTOR,"next_room_after_pass":author.NEXT_ROOM_TOKEN,"authoritative_execution_origin":"SINGLE_DOOR_ONLY","publish_allowed":False}
    if status=="RUNTIME_INPUTS_BOUND":
        prov=_module(repo/"control/single-door-boundary/preproduction_provenance_guard_v2.py","h81_prov_entry")
        proof=dict((attached_provenance_provider or prov.validate_attached_package)(repo))
        if proof.get("status")!="H81_PREPRODUCTION_PROVENANCE_PASS": raise ProjectEntryBlocked("ATTACHED_PACKAGE_PROVENANCE_NOT_PASS")
        count=runtime.get("selected_item_count")
        if not isinstance(count,int) or count<1: raise ProjectEntryBlocked("BOUND_ITEM_COUNT_INVALID")
        if route_provider is None:
            route=_module(repo/"control/single-door-boundary/single_door_route_binding.py","h81_route_entry");bound=route.materialize(count);room=bound.get("first_room_token");req=route.worker_request_for(bound,room,model=model)
        else:
            routed=dict(route_provider(repo,count,model));room=routed.get("room_token");req=routed.get("worker_request")
        if room!="R_001" or not isinstance(req,Mapping): raise ProjectEntryBlocked("PRODUCTIVE_ROUTE_ENTRY_INVALID")
        return {"ok":True,"contract":PROJECT_ENTRY_CONTRACT,"status":"PRODUCTIVE_SINGLE_DOOR_READY","room_token":room,"worker_request":req,"item_count":count,"entry_receipt_sha256":proof.get("entry_receipt_sha256"),"authoritative_execution_origin":"SINGLE_DOOR_ONLY","publish_allowed":False}
    raise ProjectEntryBlocked("RUNTIME_STATUS_NOT_ROUTABLE:"+str(status))

def main(argv:list[str])->int:
    ap=argparse.ArgumentParser();ap.add_argument("command",nargs="?",default="status",choices=["status"]);ap.add_argument("--repo",default=str(REPO_ROOT));a=ap.parse_args(argv)
    try: print(json.dumps(resolve_entry(repo=Path(a.repo)),ensure_ascii=False,indent=2));return 0
    except Exception as exc: print(json.dumps({"ok":False,"status":"PROJECT_SINGLE_DOOR_ENTRY_BLOCKED","error":str(exc),"publish_allowed":False},ensure_ascii=False,indent=2));return 2
if __name__=="__main__": raise SystemExit(main(sys.argv[1:]))
