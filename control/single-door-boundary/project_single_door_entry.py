#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path
from typing import Any, Callable, Mapping

HERE=Path(__file__).resolve().parent
REPO_ROOT=HERE.parents[1]
PRE=HERE/'single_door_preproduction_handoff.py'
ROUTE=HERE/'single_door_route_binding.py'
GUARD=REPO_ROOT/'control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py'
CONTRACT=REPO_ROOT/'control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json'
STATE=REPO_ROOT/'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
POINTER=REPO_ROOT/'control/CURRENT_STARTMASTER.json'
PROJECT_ENTRY_CONTRACT='PFERDE_ATELIER_PROJECT_SINGLE_DOOR_ENTRY_V1'

class ProjectEntryBlocked(RuntimeError): pass

def _module(path:Path,name:str):
    if not path.is_file(): raise ProjectEntryBlocked('MODULE_MISSING:'+path.name)
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise ProjectEntryBlocked('MODULE_LOAD_FAILED:'+path.name)
    mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod
    try: spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name,None); raise
    return mod

def _pointer_authority(repo:Path)->None:
    p=repo/'control/CURRENT_STARTMASTER.json'
    obj=json.loads(p.read_text(encoding='utf-8'))
    if obj.get('startmaster')!='STARTMASTER0107': raise ProjectEntryBlocked('STARTMASTER_NOT_0107')
    if obj.get('free_chat_execution_authority') is not False: raise ProjectEntryBlocked('FREE_CHAT_AUTHORITY_MUST_BE_FALSE')
    expected='control/single-door-boundary/project_single_door_entry.py'
    gate=str(obj.get('gate_ref') or '')
    if gate not in {expected,'control/cloud-entry-gate/cloud_entry.py'}: raise ProjectEntryBlocked('PROJECT_GATE_REF_INVALID')

def current_runtime(repo:Path)->Mapping[str,Any]:
    guard=_module(repo/'control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py','runtime_guard_h7_entry')
    return guard.validate(repo,repo/'control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json',repo/'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json')

def resolve_entry(*,repo:Path,model:str='gpt-5.6-sol',runtime_provider:Callable[[Path],Mapping[str,Any]]|None=None,route_provider:Callable[[Path,int,str],Mapping[str,Any]]|None=None)->dict[str,Any]:
    repo=Path(repo).resolve(); _pointer_authority(repo)
    runtime=dict((runtime_provider or current_runtime)(repo)); status=runtime.get('status')
    if status=='READY_IDLE':
        return {'ok':True,'contract':PROJECT_ENTRY_CONTRACT,'status':'PROJECT_ARMED_NO_ACTIVE_BATCH','worker_request':None,'authoritative_execution_origin':'SINGLE_DOOR_EXECUTOR_ONLY','publish_allowed':False}
    if status=='READY_WAITING_PACKAGE':
        pre=_module(repo/'control/single-door-boundary/single_door_preproduction_handoff.py','h7_pre_entry')
        req=pre.worker_request(model)
        return {'ok':True,'contract':PROJECT_ENTRY_CONTRACT,'status':'PREPRODUCTION_SINGLE_DOOR_REQUIRED','room_token':pre.ROOM_TOKEN,'worker_request':req,'next_room_after_pass':pre.NEXT_ROOM_TOKEN,'authoritative_execution_origin':'SINGLE_DOOR_EXECUTOR_ONLY','publish_allowed':False}
    if status=='RUNTIME_INPUTS_BOUND':
        count=runtime.get('selected_item_count')
        if not isinstance(count,int) or count<1: raise ProjectEntryBlocked('BOUND_ITEM_COUNT_INVALID')
        if route_provider is not None:
            routed=dict(route_provider(repo,count,model)); room=routed.get('room_token'); req=routed.get('worker_request')
        else:
            route=_module(repo/'control/single-door-boundary/single_door_route_binding.py','h7_route_entry')
            bound=route.materialize(count); room=bound.get('first_room_token')
            req=route.worker_request_for(bound,room,model=model)
        if room!='R_001' or not isinstance(req,Mapping): raise ProjectEntryBlocked('PRODUCTIVE_ROUTE_ENTRY_INVALID')
        return {'ok':True,'contract':PROJECT_ENTRY_CONTRACT,'status':'PRODUCTIVE_SINGLE_DOOR_READY','room_token':room,'worker_request':req,'item_count':count,'authoritative_execution_origin':'SINGLE_DOOR_EXECUTOR_ONLY','publish_allowed':False}
    raise ProjectEntryBlocked('RUNTIME_STATUS_NOT_ROUTABLE:'+str(status))

def main(argv:list[str])->int:
    try:
        if argv not in ([],['status']): raise ProjectEntryBlocked('USAGE_STATUS_ONLY')
        print(json.dumps(resolve_entry(repo=REPO_ROOT),ensure_ascii=False,indent=2)); return 0
    except Exception as e:
        print(json.dumps({'ok':False,'status':'PROJECT_SINGLE_DOOR_ENTRY_BLOCKED','error':str(e),'publish_allowed':False},ensure_ascii=False,indent=2)); return 2
if __name__=='__main__': raise SystemExit(main(sys.argv[1:]))
