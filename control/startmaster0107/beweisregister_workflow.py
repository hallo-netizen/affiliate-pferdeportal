#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

REG_CONTRACT='PFERDE_ATELIER_STARTMASTER0107_BEWEISREGISTER_V1'
PTR_CONTRACT='PFERDE_ATELIER_BEWEISREGISTER_POINTER_V1'
STEP_CONTRACT='PFERDE_ATELIER_BEWEISREGISTER_STARTMASTER_V1'
BASELINE_MAIN_SHA='56937915a9ca02055ef142f03c5ec41024f9a668'
FAILED={'GESCHEITERT','GESCHEITERT_VERWORFEN','WIDERLEGT','UNZUREICHEND_FUER_AKTUELLEN_FEHLER','UEBERHOLT','TEST_ONLY_NICHT_LOESUNG'}
DONE={'ERLEDIGT','ERLEDIGTER_BEWEIS'}

def repo_root(): return Path(__file__).resolve().parents[2]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def blob_sha(p):
    b=Path(p).read_bytes(); return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def file_sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,obj):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); t=p.with_name(p.name+'.tmp')
    t.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); t.replace(p)
def paths():
    r=repo_root(); return r/'control/startmaster0107/BEWEISREGISTER.json', r/'control/startmaster0107/BEWEISREGISTER_CURRENT_STARTMASTER.json'

def verify_all():
    regp,ptrp=paths(); reg,ptr=load(regp),load(ptrp)
    if reg.get('contract')!=REG_CONTRACT: raise RuntimeError('REGISTER_CONTRACT_INVALID')
    if reg.get('source_main_sha')!=BASELINE_MAIN_SHA: raise RuntimeError('REGISTER_BASELINE_MAIN_SHA_INVALID')
    entries=reg.get('entries')
    if not isinstance(entries,list) or not entries: raise RuntimeError('REGISTER_ENTRIES_MISSING')
    ids=[str(x.get('id') or '') for x in entries if isinstance(x,dict)]
    if len(ids)!=len(entries) or len(set(ids))!=len(ids) or any(not x for x in ids): raise RuntimeError('REGISTER_IDS_INVALID_OR_DUPLICATE')
    for row in entries:
        st=row.get('status')
        if not isinstance(row.get('evidence'),list) or not row['evidence']: raise RuntimeError('REGISTER_EVIDENCE_MISSING:'+str(row.get('id')))
        if st in FAILED and row.get('repeat_forbidden') is not True: raise RuntimeError('FAILED_PATH_NOT_REPEAT_LOCKED:'+str(row.get('id')))
        if st in DONE and row.get('recheck_forbidden_while_bound_inputs_unchanged') is not True: raise RuntimeError('COMPLETED_PATH_NOT_RECHECK_LOCKED:'+str(row.get('id')))
    required=set((reg.get('history_scope') or {}).get('required_startmaster_pr_refs') or [])
    present={str(e) for row in entries for e in (row.get('evidence') or [])}
    missing=sorted(required-present)
    if missing: raise RuntimeError('HISTORY_EVIDENCE_MISSING:'+','.join(missing))
    if len([x for x in entries if x.get('id')=='O001' and x.get('status')=='OFFEN'])!=1: raise RuntimeError('CURRENT_OPEN_ROOT_PROBLEM_MISSING')
    if ptr.get('contract')!=PTR_CONTRACT: raise RuntimeError('POINTER_CONTRACT_INVALID')
    if ptr.get('register_git_blob_sha1')!=blob_sha(regp): raise RuntimeError('POINTER_REGISTER_HASH_MISMATCH')
    if ptr.get('state')!='ACTIVE': return reg,ptr,None
    ref=str(ptr.get('current_startmaster_ref') or '')
    if not ref or ref.startswith('/') or '..' in Path(ref).parts: raise RuntimeError('CURRENT_STARTMASTER_REF_INVALID')
    stepp=repo_root()/ref
    if not stepp.is_file(): raise RuntimeError('CURRENT_STARTMASTER_MISSING')
    if ptr.get('current_startmaster_git_blob_sha1')!=blob_sha(stepp): raise RuntimeError('CURRENT_STARTMASTER_HASH_MISMATCH')
    step=load(stepp)
    if step.get('contract')!=STEP_CONTRACT: raise RuntimeError('STARTMASTER_CONTRACT_INVALID')
    if step.get('register_git_blob_sha1')!=blob_sha(regp): raise RuntimeError('STARTMASTER_REGISTER_HASH_MISMATCH')
    cmds=step.get('allowed_commands')
    if not isinstance(cmds,list) or len(cmds)!=1 or not isinstance(cmds[0],str) or not cmds[0].strip(): raise RuntimeError('STARTMASTER_MUST_HAVE_EXACTLY_ONE_COMMAND')
    if step.get('step_type')=='NEW_SOLUTION':
        failed_ids={x['id'] for x in entries if x.get('repeat_forbidden') is True}
        proof=step.get('novelty_against')
        if not isinstance(proof,list): raise RuntimeError('NOVELTY_PROOF_MISSING')
        by_id={str(x.get('id') or ''):x for x in proof if isinstance(x,dict)}
        if failed_ids-set(by_id): raise RuntimeError('NOVELTY_PROOF_INCOMPLETE')
        for fid in failed_ids:
            row=by_id[fid]
            if not str(row.get('difference') or '').strip() or not str(row.get('evidence') or '').strip(): raise RuntimeError('NOVELTY_PROOF_EMPTY:'+fid)
    return reg,ptr,step

def current():
    _,ptr,step=verify_all()
    if ptr.get('state')!='ACTIVE' or step is None:
        print('STEP_ID=NEXT_STARTMASTER_REQUIRED'); print('COMMAND=NO_PROJECT_ACTION_AUTHORIZED'); return 0
    print('STEP_ID='+str(step['step_id'])); print('COMMAND='+step['allowed_commands'][0]); return 0

def verify_register(receipt=None):
    _,ptr,step=verify_all()
    out={'contract':'PFERDE_ATELIER_BEWEISREGISTER_STEP_RECEIPT_V1','step_id':step['step_id'],'status':'PASS','register_git_blob_sha1':ptr['register_git_blob_sha1'],'startmaster_git_blob_sha1':ptr['current_startmaster_git_blob_sha1'],'checks':{'declared_history_refs_present':True,'failed_paths_repeat_locked':True,'completed_paths_recheck_locked_while_unchanged':True,'one_active_task_one_command':True,'current_open_problem_registered':True}}
    if receipt: dump(receipt,out)
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0

def complete(receipt):
    _,ptr,step=verify_all(); rp=Path(receipt); rec=load(rp)
    if rec.get('contract')!='PFERDE_ATELIER_BEWEISREGISTER_STEP_RECEIPT_V1': raise RuntimeError('RECEIPT_CONTRACT_INVALID')
    if rec.get('step_id')!=step.get('step_id'): raise RuntimeError('RECEIPT_STEP_MISMATCH')
    if rec.get('register_git_blob_sha1')!=ptr.get('register_git_blob_sha1'): raise RuntimeError('RECEIPT_REGISTER_HASH_MISMATCH')
    if rec.get('startmaster_git_blob_sha1')!=ptr.get('current_startmaster_git_blob_sha1'): raise RuntimeError('RECEIPT_STARTMASTER_HASH_MISMATCH')
    if rec.get('status')!='PASS': raise RuntimeError('NONPASS_DOES_NOT_ADVANCE')
    nxt=step.get('next_startmaster_ref')
    if not nxt:
        dump(paths()[1],{'contract':PTR_CONTRACT,'state':'NEXT_STARTMASTER_REQUIRED','register_git_blob_sha1':ptr['register_git_blob_sha1'],'completed_step_id':step['step_id'],'completed_receipt_sha256':file_sha256(rp),'current_startmaster_ref':None,'current_startmaster_git_blob_sha1':None})
        print('PASS_NEXT_STARTMASTER_REQUIRED'); return 0
    np=repo_root()/nxt
    if not np.is_file(): raise RuntimeError('NEXT_STARTMASTER_MISSING')
    ns=load(np)
    if ns.get('register_git_blob_sha1')!=ptr['register_git_blob_sha1']: raise RuntimeError('NEXT_STARTMASTER_REGISTER_HASH_MISMATCH')
    dump(paths()[1],{'contract':PTR_CONTRACT,'state':'ACTIVE','register_git_blob_sha1':ptr['register_git_blob_sha1'],'current_startmaster_ref':nxt,'current_startmaster_git_blob_sha1':blob_sha(np),'previous_step_id':step['step_id'],'previous_receipt_sha256':file_sha256(rp)})
    print('PASS_NEXT_STARTMASTER_ACTIVATED'); return 0

def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('current'); vr=sub.add_parser('verify-register'); vr.add_argument('--receipt'); co=sub.add_parser('complete'); co.add_argument('receipt')
    a=ap.parse_args(argv)
    try:
        if a.cmd=='current': return current()
        if a.cmd=='verify-register': return verify_register(a.receipt)
        return complete(a.receipt)
    except Exception as exc:
        print('BLOCKED:'+str(exc)); return 2
if __name__=='__main__': raise SystemExit(main())
