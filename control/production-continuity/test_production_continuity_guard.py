#!/usr/bin/env python3
import copy,json,subprocess,sys,tempfile
from pathlib import Path
G=Path(__file__).with_name('production_continuity_guard.py')
def run(cmd,obj):
    with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False) as f:
        json.dump(obj,f); p=f.name
    return subprocess.run([sys.executable,str(G),cmd,p],capture_output=True,text=True)
base={'contract':'PFERDE_ATELIER_BATCH_CHECKPOINT_V1','batch_id':'B1','bound_item_ids':['A','B','C'],'completed_item_ids':['A'],'next_item_id':'B','current_gate_id':'G','status':'BATCH_ACTIVE','workflow_navigation_authority':False,'domain_logic_authority':'NONE'}
assert run('validate',base).returncode==0
assert run('finalize',base).returncode!=0
for mutate in [lambda x:x.update(completed_item_ids=['A','X']),lambda x:x.update(next_item_id='C'),lambda x:x.update(workflow_navigation_authority=True),lambda x:x.update(domain_logic_authority='SOME'),lambda x:x.update(status='BATCH_COMPLETE'),lambda x:x.update(bound_item_ids=['A','A'])]:
    x=copy.deepcopy(base); mutate(x); assert run('validate',x).returncode!=0
complete=copy.deepcopy(base); complete.update(completed_item_ids=['A','B','C'],next_item_id=None,status='BATCH_COMPLETE')
assert run('validate',complete).returncode==0
assert run('finalize',complete).returncode==0
resume=copy.deepcopy(base); resume.update(completed_item_ids=['A','B'],next_item_id='C')
r=run('validate',resume); assert r.returncode==0 and '"C"' in r.stdout
print(json.dumps({'ok':True,'status':'PRODUCTION_CONTINUITY_POSITIVE_NEGATIVE_PASS','cases':10},indent=2))
