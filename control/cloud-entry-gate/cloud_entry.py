#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,shutil,sys
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
POINTER=REPO/'control/CURRENT_STARTMASTER.json'
CAPSULE=REPO/'.pferde-capsule'

class Blocked(RuntimeError): pass

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p:Path): return json.loads(p.read_text(encoding='utf-8'))
def rel(v:str)->Path:
    p=Path(str(v or ''))
    if not str(v or '') or p.is_absolute() or '..' in p.parts: raise Blocked('INVALID_RELATIVE_PATH')
    return p

def authority():
    if not POINTER.is_file(): raise Blocked('STARTMASTER_POINTER_MISSING')
    ptr=load(POINTER)
    rootp=REPO/rel(ptr.get('root_ref')); statep=REPO/rel(ptr.get('state_ref'))
    if not rootp.is_file() or not statep.is_file(): raise Blocked('ROOT_OR_STATE_MISSING')
    root,state=load(rootp),load(statep)
    if ptr.get('startmaster')!=root.get('startmaster') or root.get('startmaster')!=state.get('startmaster'): raise Blocked('STARTMASTER_IDENTITY_MISMATCH')
    if sha(statep)!=root.get('current_state_sha256'): raise Blocked('STATE_HASH_MISMATCH')
    if root.get('next_allowed_step')!=state.get('next_allowed_step'): raise Blocked('STEP_ROOT_STATE_MISMATCH')
    gate=state.get('execution_gate') or {}
    if gate.get('enforced') is not True: raise Blocked('GATE_NOT_ENFORCED')
    if gate.get('step_id')!=state.get('next_allowed_step'): raise Blocked('GATE_STEP_MISMATCH')
    if gate.get('state_write_authority')!='ENTRANCE_GATE_ONLY': raise Blocked('STATE_WRITE_AUTHORITY_INVALID')
    if gate.get('unknown_step_policy')!='DENY': raise Blocked('UNKNOWN_STEP_POLICY_INVALID')
    if gate.get('free_chat_direct_execution_valid') is not False: raise Blocked('FREE_CHAT_MUST_BE_INVALID')
    if gate.get('domain_logic_authority')!='NONE' or gate.get('content_quality_design_authority')!='NONE': raise Blocked('DOMAIN_AUTHORITY_MUST_BE_NONE')
    if gate.get('worker_context_policy')!='CAPSULE_ONLY': raise Blocked('WORKER_CONTEXT_NOT_CAPSULE_ONLY')
    if gate.get('hard_worker_target')!='CODEX_CLOUD': raise Blocked('HARD_WORKER_NOT_CODEX_CLOUD')
    if gate.get('api_dependency')!='NONE': raise Blocked('API_DEPENDENCY_FORBIDDEN')
    bp=REPO/rel(gate.get('bundle_ref'))
    if not bp.is_file(): raise Blocked('BUNDLE_MISSING')
    if sha(bp)!=gate.get('bundle_sha256'): raise Blocked('BUNDLE_HASH_MISMATCH')
    bundle=load(bp)
    if bundle.get('step_id')!=gate.get('step_id') or int(bundle.get('sequence',-1))!=int(gate.get('sequence',-2)): raise Blocked('BUNDLE_IDENTITY_MISMATCH')
    return ptr,root,state,gate,bundle,bp

def verify_inputs(bundle):
    rows=[]
    for i,row in enumerate(bundle.get('authorized_inputs') or []):
        p=REPO/rel(row.get('ref'))
        if not p.is_file(): raise Blocked(f'INPUT_MISSING:{i}:{row.get("ref")}')
        actual=sha(p)
        if actual!=row.get('sha256'): raise Blocked(f'INPUT_HASH_MISMATCH:{i}:{row.get("ref")}')
        rows.append((p,row))
    return rows

def materialize():
    ptr,root,state,gate,bundle,bp=authority(); inputs=verify_inputs(bundle)
    if CAPSULE.exists(): shutil.rmtree(CAPSULE)
    (CAPSULE/'inputs').mkdir(parents=True)
    copied=[]
    for n,(src,row) in enumerate(inputs,1):
        dst=CAPSULE/'inputs'/f'{n:03d}_{src.name}'
        shutil.copyfile(src,dst); dst.chmod(0o444)
        copied.append({'source_ref':row['ref'],'sha256':row['sha256'],'capsule_path':str(dst.relative_to(CAPSULE))})
    instruction=str(bundle.get('instruction') or '').strip()
    if not instruction: raise Blocked('INSTRUCTION_MISSING')
    (CAPSULE/'INSTRUCTION.txt').write_text(instruction+'\n',encoding='utf-8')
    manifest={
      'contract':'PFERDE_ATELIER_CODEX_CLOUD_CAPSULE_V1',
      'startmaster':state['startmaster'],'step_id':state['next_allowed_step'],'sequence':gate['sequence'],
      'state_sha256':root['current_state_sha256'],'bundle_sha256':gate['bundle_sha256'],'inputs':copied,
      'navigation_authority_exposed_to_worker':False,'worker_may_choose_next_step':False,
      'worker_state_write_authority':False,'workflow_change_authority':False,'api_required':False
    }
    (CAPSULE/'CAPSULE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'ok':True,'status':'CODEX_CLOUD_ENTRANCE_PASS','step_id':state['next_allowed_step'],'sequence':gate['sequence'],'capsule':'.pferde-capsule','authorized_input_count':len(copied),'next_action':'READ_ONLY_.pferde-capsule/INSTRUCTION.txt'}

def verify():
    ptr,root,state,gate,bundle,bp=authority()
    return {'ok':True,'status':'CODEX_CLOUD_GATE_VERIFY_PASS','startmaster':state['startmaster'],'step_id':state['next_allowed_step'],'sequence':gate['sequence'],'api_required':False,'domain_logic_authority':'NONE'}

def main():
    try:
        cmd=sys.argv[1] if len(sys.argv)>1 else 'verify'
        result=materialize() if cmd=='start' else verify() if cmd=='verify' else (_ for _ in ()).throw(Blocked('UNKNOWN_COMMAND'))
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except Blocked as e:
        print(json.dumps({'ok':False,'status':'CODEX_CLOUD_ENTRANCE_BLOCKED','reason':str(e)},ensure_ascii=False,indent=2)); return 2
if __name__=='__main__': raise SystemExit(main())
