#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import importlib.util,sys,tempfile,shutil,json

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
spec=importlib.util.spec_from_file_location('entry_h7_test',HERE/'project_single_door_entry.py')
m=importlib.util.module_from_spec(spec); sys.modules['entry_h7_test']=m; spec.loader.exec_module(m)

def expect_block(fn,token):
    try: fn()
    except Exception as e:
        assert token in str(e),(token,str(e)); return
    raise AssertionError('expected block:'+token)

with tempfile.TemporaryDirectory() as td:
    r=Path(td)
    (r/'control/single-door-boundary').mkdir(parents=True)
    (r/'control/startmaster0107/runtime_inbox').mkdir(parents=True)
    for f in ['single_door_boundary.py','single_door_preproduction_handoff.py','single_door_route_binding.py']:
        shutil.copyfile(HERE/f,r/'control/single-door-boundary'/f)
    shutil.copyfile(REPO/'control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py',r/'control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py')
    good={'contract':'PFERDE_ATELIER_CURRENT_STARTMASTER_POINTER_V1','startmaster':'STARTMASTER0107','root_ref':'control/startmaster0107/PFERDE_ATELIER_START_HERE.json','state_ref':'control/startmaster0107/CURRENT_STATE.json','gate_ref':'control/single-door-boundary/project_single_door_entry.py','free_chat_execution_authority':False}
    (r/'control/CURRENT_STARTMASTER.json').write_text(json.dumps(good))
    a=m.resolve_entry(repo=r,runtime_provider=lambda repo:{'status':'READY_IDLE'})
    assert a['status']=='PROJECT_ARMED_NO_ACTIVE_BATCH' and a['worker_request'] is None
    b=m.resolve_entry(repo=r,runtime_provider=lambda repo:{'status':'READY_WAITING_PACKAGE'})
    assert b['status']=='PREPRODUCTION_SINGLE_DOOR_REQUIRED' and b['room_token']=='R_PRE_001' and len(b['worker_request']['tools'])==1
    c=m.resolve_entry(repo=r,runtime_provider=lambda repo:{'status':'RUNTIME_INPUTS_BOUND','selected_item_count':7},route_provider=lambda repo,count,model:{'room_token':'R_001','worker_request':{'input':'R_001','tools':[{}]}})
    assert c['status']=='PRODUCTIVE_SINGLE_DOOR_READY' and c['room_token']=='R_001' and c['item_count']==7 and len(c['worker_request']['tools'])==1
    bad=dict(good); bad['free_chat_execution_authority']=True; (r/'control/CURRENT_STARTMASTER.json').write_text(json.dumps(bad))
    expect_block(lambda:m.resolve_entry(repo=r,runtime_provider=lambda repo:{'status':'READY_IDLE'}),'FREE_CHAT_AUTHORITY_MUST_BE_FALSE')
    old=dict(good); old['gate_ref']='control/cloud-entry-gate/cloud_entry.py'; (r/'control/CURRENT_STARTMASTER.json').write_text(json.dumps(old))
    expect_block(lambda:m.resolve_entry(repo=r,runtime_provider=lambda repo:{'status':'READY_IDLE'}),'PROJECT_GATE_REF_INVALID')
print('{"ok":true,"status":"H7_PROJECT_ENTRY_SELECTOR_POSITIVE_NEGATIVE_PASS","cases":5}')
