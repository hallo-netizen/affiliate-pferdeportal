#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,importlib.util,json,shutil,tempfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
MODPATH=REPO/'control/cloud-entry-gate/cloud_entry.py'
spec=importlib.util.spec_from_file_location('cloud_entry',MODPATH); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def dump(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def expect_block(fn,token):
    try: fn()
    except m.Blocked as e:
        assert token in str(e),(token,str(e)); return
    raise AssertionError('expected block '+token)

def make_repo(td:Path):
    r=td/'repo';
    for rel in ['control/CURRENT_STARTMASTER.json','control/startmaster0105/PFERDE_ATELIER_START_HERE.json','control/startmaster0105/CURRENT_STATE.json','control/startmaster0105/STEP_105000_CODEX_CLOUD_SELFTEST.json','control/startmaster0105/STEP_105001_ROOTFIX_LIVE_40_40.json']:
        src=REPO/rel; dst=r/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
    return r

def bind_state(r:Path):
    rootp=r/'control/startmaster0105/PFERDE_ATELIER_START_HERE.json'; statep=r/'control/startmaster0105/CURRENT_STATE.json'
    root=json.loads(rootp.read_text()); root['current_state_sha256']=sha(statep); dump(rootp,root)

def main():
    # Real repository positive path.
    pos=m.verify(); assert pos['status']=='CODEX_CLOUD_GATE_VERIFY_PASS'
    mat=m.materialize(); assert mat['status']=='CODEX_CLOUD_ENTRANCE_PASS'
    manifest=json.loads((REPO/'.pferde-capsule/CAPSULE_MANIFEST.json').read_text())
    assert manifest['navigation_authority_exposed_to_worker'] is False
    assert manifest['worker_may_choose_next_step'] is False
    assert manifest['worker_state_write_authority'] is False
    assert manifest['workflow_change_authority'] is False
    assert manifest['api_required'] is False
    shutil.rmtree(REPO/'.pferde-capsule')

    # Gate stays domain-blind and has no API client.
    low=MODPATH.read_text(encoding='utf-8').lower()
    for token in ['pste','pserc','ppm','languagetool','wordpress','beratung','pflege','cannibal','api.openai.com','openai_api_key','requests.post','httpx.post','urllib.request']:
        assert token not in low,token

    with tempfile.TemporaryDirectory() as t:
        r=make_repo(Path(t)); old=(m.REPO,m.POINTER,m.CAPSULE); m.REPO=r; m.POINTER=r/'control/CURRENT_STARTMASTER.json'; m.CAPSULE=r/'.pferde-capsule'
        try:
            assert m.verify()['status']=='CODEX_CLOUD_GATE_VERIFY_PASS'
            statep=r/'control/startmaster0105/CURRENT_STATE.json'; rootp=r/'control/startmaster0105/PFERDE_ATELIER_START_HERE.json'; bundlep=r/'control/startmaster0105/STEP_105000_CODEX_CLOUD_SELFTEST.json'
            original_state=json.loads(statep.read_text()); original_root=json.loads(rootp.read_text()); original_bundle=json.loads(bundlep.read_text())

            s=copy.deepcopy(original_state); s['execution_gate']['free_chat_direct_execution_valid']=True; dump(statep,s); bind_state(r); expect_block(m.verify,'FREE_CHAT_MUST_BE_INVALID')
            dump(statep,original_state); bind_state(r)
            s=copy.deepcopy(original_state); s['execution_gate']['api_dependency']='OPENAI'; dump(statep,s); bind_state(r); expect_block(m.verify,'API_DEPENDENCY_FORBIDDEN')
            dump(statep,original_state); bind_state(r)
            s=copy.deepcopy(original_state); s['execution_gate']['hard_worker_target']='LOCAL'; dump(statep,s); bind_state(r); expect_block(m.verify,'HARD_WORKER_NOT_CODEX_CLOUD')
            dump(statep,original_state); bind_state(r)
            s=copy.deepcopy(original_state); s['next_allowed_step']='SIDE_JUMP'; dump(statep,s); bind_state(r); expect_block(m.verify,'STEP_ROOT_STATE_MISMATCH')
            dump(statep,original_state); bind_state(r)
            b=copy.deepcopy(original_bundle); b['step_id']='BACKTRACK'; dump(bundlep,b); expect_block(m.verify,'BUNDLE_HASH_MISMATCH')
            dump(bundlep,original_bundle)
            p=json.loads((r/'control/CURRENT_STARTMASTER.json').read_text()); p['root_ref']='../escape.json'; dump(r/'control/CURRENT_STARTMASTER.json',p); expect_block(m.verify,'INVALID_RELATIVE_PATH')
        finally:
            m.REPO,m.POINTER,m.CAPSULE=old
    print(json.dumps({'ok':True,'status':'CODEX_CLOUD_GATE_CI_PASS','positive_negative':'PASS','api_required':False,'local_codex_required':False,'domain_logic_authority':'NONE'},indent=2))
if __name__=='__main__': main()
