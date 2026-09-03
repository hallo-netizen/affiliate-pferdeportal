#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent.parent if HERE.parent.name=='control' else HERE
CAP=REPO/'.pferde-capsule'
CTRL=REPO/'.pferde-quarantine/_control/startmaster0107'
STATE=CTRL/'CURRENT_ROOM_STATE.json'; CP=CTRL/'BATCH_CHECKPOINT.json'
RSTATE=REPO/'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
RCON=REPO/'control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json'
ENTRY=REPO/'control/single-door-boundary/project_single_door_entry_v2.py'
ROUTE=REPO/'control/single-door-boundary/single_door_route_binding.py'
BOUNDARY=REPO/'control/single-door-boundary/single_door_boundary.py'
RGUARD=REPO/'control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py'
PREFLIGHT=REPO/'control/production-package-preflight/PRODUCTION_PACKAGE_PREFLIGHT_GUARD_STARTMASTER0103.py'
CONT=REPO/'control/production-continuity/production_continuity_guard.py'
RUNTIME_ENTRY=REPO/'control/output-quarantine/runtime_entry_gate.py'
DUAL=REPO/'control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py'
FACH='control/startmaster0107/VERBINDLICHER_TEXTERSTELLUNGS_PROMPT_STARTMASTER0107.txt'
BRIDGE='PFERDE_ATELIER_CODEX_CURRENT_ROOM_BRIDGE_V1'; BSTATE='PFERDE_ATELIER_CODEX_CURRENT_ROOM_BRIDGE_STATE_V1'
ACTION='PFERDE_ATELIER_CODEX_CURRENT_BOUND_ACTION_V1'; IREC='PFERDE_ATELIER_BOUND_ITEM_EXECUTION_RECEIPT_V1'; CPC='PFERDE_ATELIER_BATCH_CHECKPOINT_V1'

class Blocked(RuntimeError): pass

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); t=p.with_name(p.name+'.tmp'); t.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); t.replace(p)
def rel(v):
    p=Path(str(v or ''))
    if not str(v or '') or p.is_absolute() or '..' in p.parts: raise Blocked('INVALID_RELATIVE_PATH')
    return p
def mod(p,n):
    s=importlib.util.spec_from_file_location(n,p)
    if s is None or s.loader is None: raise Blocked('MODULE_LOAD_FAILED:'+Path(p).name)
    m=importlib.util.module_from_spec(s); sys.modules[n]=m; s.loader.exec_module(m); return m

def run_json(cmd):
    r=subprocess.run(cmd,cwd=REPO,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode: raise Blocked('COMMAND_FAILED:'+(' '.join(map(str,cmd)))+':'+(r.stderr or r.stdout).strip()[:700])
    try: return json.loads(r.stdout)
    except json.JSONDecodeError as e: raise Blocked('COMMAND_JSON_INVALID:'+str(cmd[1])) from e

def outer_authority():
    e=run_json([sys.executable,str(ENTRY),'status'])
    if e.get('status')!='PRODUCTIVE_SINGLE_DOOR_READY' or e.get('room_token')!='R_001': raise Blocked('PRODUCTIVE_SINGLE_DOOR_NOT_READY')
    if e.get('worker_request') is not None or e.get('workflow_navigation_decision') is not False or e.get('quality_authority')!='NONE' or e.get('publish_allowed') is not False: raise Blocked('PROJECT_ENTRY_AUTHORITY_INVALID')
    ptr=load(REPO/'control/CURRENT_STARTMASTER.json'); st=load(REPO/rel(ptr['state_ref'])); g=st.get('execution_gate') or {}
    if ptr.get('free_chat_execution_authority') is not False or st.get('next_allowed_step')!='RUN_NEW_ARTICLE_BATCH_NO_STOP' or int(g.get('sequence',-1))!=107007: raise Blocked('OUTER_107007_AUTHORITY_INVALID')
    if g.get('unknown_step_policy')!='DENY' or g.get('state_write_authority')!='ENTRANCE_GATE_ONLY' or g.get('domain_logic_authority')!='NONE' or g.get('content_quality_design_authority')!='NONE': raise Blocked('OUTER_GATE_RULE_INVALID')
    bp=REPO/rel(g['bundle_ref'])
    if sha(bp)!=g.get('bundle_sha256'): raise Blocked('CURRENT_107007_BUNDLE_HASH_MISMATCH')
    b=load(bp); binds={x.get('ref'):x.get('sha256') for x in b.get('authorized_inputs',[]) if isinstance(x,dict)}
    if binds.get('control/single-door-boundary/codex_current_room_bridge.py')!=sha(Path(__file__).resolve()): raise Blocked('CURRENT_ROOM_BRIDGE_NOT_107007_HASH_BOUND')

def capsule():
    t=load(CAP/'TICKET.json'); m=load(CAP/'CAPSULE_MANIFEST.json')
    if t.get('step_id')!='RUN_NEW_ARTICLE_BATCH_NO_STOP' or int(t.get('sequence',-1))!=107007 or m.get('ticket_id')!=t.get('ticket_id'): raise Blocked('CAPSULE_NOT_CURRENT_107007')
    if m.get('navigation_authority_exposed_to_worker') is not False or m.get('worker_may_choose_next_step') is not False or m.get('worker_state_write_authority') is not False or m.get('workflow_change_authority') is not False: raise Blocked('CAPSULE_AUTHORITY_INVALID')
    if m.get('input_materialization_mode')!='HASH_VERIFIED_CANONICAL_REPO_ONLY' or m.get('capsule_input_execution_allowed') is not False or m.get('canonical_repo_execution_required') is not True: raise Blocked('CAPSULE_EXECUTION_BOUNDARY_INVALID')
    return t,m

def runtime():
    r=mod(RGUARD,'room_runtime').validate(REPO,RCON,RSTATE)
    if r.get('status')!='RUNTIME_INPUTS_BOUND' or r.get('publish_allowed') is not False: raise Blocked('RUNTIME_INPUTS_NOT_BOUND')
    return dict(r)
def items(r):
    pkg=load(REPO/rel(r['production_package'])); snap=load(REPO/rel(r['source_snapshot']))
    meta={x['plan_slot']:x for x in snap['next_textmachine_metadata_batch']['items']}
    out=[]
    for n,x in enumerate(pkg['workflow_release']['items'],1):
        m=meta.get(x.get('plan_slot'))
        if not m: raise Blocked('BOUND_ITEM_JOIN_FAILED:'+str(n))
        out.append({'ordinal':n,'canonical_article_id':x['canonical_article_id'],'plan_slot':x['plan_slot'],'title':m['title'],'target_keyword':m['target_keyword'],'category':m['category'],'article_type':m['article_type']})
    if len(out)!=r.get('selected_item_count'): raise Blocked('BOUND_ITEM_COUNT_MISMATCH')
    return out

def route(count):
    rm=mod(ROUTE,'room_route'); rt=rm.materialize(count)
    if rt.get('all_other_actions')!='DENY': raise Blocked('ROUTE_DEFAULT_DENY_MISSING')
    return rm,rt
def row(rm,rt,token): return dict(rm.resolve_room(rt,token))
def validate_cp(c):
    z=mod(CONT,'room_cont').validate(dict(c))
    if z.get('status')!='BATCH_CHECKPOINT_VALID': raise Blocked('CHECKPOINT_INVALID')
    return dict(z)
def init(ticket,r,its):
    if STATE.is_file():
        s=load(STATE)
        if s.get('contract')!=BSTATE or s.get('ticket_id')!=ticket.get('ticket_id') or s.get('state_sha256')!=ticket.get('state_sha256') or s.get('bundle_sha256')!=ticket.get('bundle_sha256') or s.get('batch_sha256')!=r.get('batch_sha256'): raise Blocked('STALE_BRIDGE_STATE_BLOCKED')
        if s.get('navigation_authority') is not False or s.get('quality_authority')!='NONE' or s.get('content_semantics_authority')!='NONE' or s.get('publish_allowed') is not False: raise Blocked('BRIDGE_STATE_AUTHORITY_INVALID')
        return s
    ids=[x['canonical_article_id'] for x in its]
    c={'contract':CPC,'batch_id':r['batch_sha256'],'bound_item_ids':ids,'completed_item_ids':[],'current_item_id':ids[0],'current_gate_id':'BOUND_ITEM_EXECUTION','next_item_id':ids[0],'input_hashes':[],'receipt_hashes':[],'status':'BATCH_ACTIVE','workflow_navigation_authority':False,'domain_logic_authority':'NONE'}
    validate_cp(c); dump(CP,c)
    s={'contract':BSTATE,'ticket_id':ticket['ticket_id'],'state_sha256':ticket['state_sha256'],'bundle_sha256':ticket['bundle_sha256'],'batch_sha256':r['batch_sha256'],'current_room_token':'R_001','accepted_output_refs':[],'status':'ACTIVE','navigation_authority':False,'content_semantics_authority':'NONE','quality_authority':'NONE','publish_allowed':False}
    dump(STATE,s); return s

def advance(s,rr,evidence):
    v=rr['worker_view']; bd=mod(BOUNDARY,'room_boundary'); b=bd.DoorBinding.from_mapping({'contract':bd.BOUNDARY_CONTRACT,'room_token':v['room_token'],'action_token':v['action_token'],'receipt_token':v['receipt_token'],'next_room_token':v['next_room_token'],'input_handles':list(v['input_handles'])})
    rec={'contract':bd.BOUNDARY_CONTRACT,'room_token':b.room_token,'action_token':b.action_token,'receipt_token':b.receipt_token,'next_room_token':b.next_room_token,'status':'PASS','evidence':evidence}
    rec=bd.validate_action_receipt(b,rec); s['current_room_token']=rec['next_room_token']; dump(STATE,s)
def item_for(its,token):
    if not token.startswith('R_D_') or not token.endswith('_01'): raise Blocked('CURRENT_ROOM_NOT_ITEM_EXECUTION')
    try: n=int(token.split('_')[2])
    except Exception as e: raise Blocked('ITEM_ROOM_TOKEN_INVALID') from e
    if n<1 or n>len(its): raise Blocked('ITEM_ROOM_OUT_OF_RANGE')
    return its[n-1]
def slug(v): return ''.join(c if c.isalnum() else '_' for c in v).strip('_')[:96] or 'item'
def action(s,it):
    root=f".pferde-quarantine/{s['ticket_id']}/{slug(it['canonical_article_id'])}"; rec=root+'/ITEM_RECEIPT.json'
    base={'contract':ACTION,'status':'CURRENT_BOUND_ACTION_READY','room_token':s['current_room_token'],'action':'EXECUTE_EXISTING_BOUND_ITEM_EXECUTOR_OPAQUE','current_item':{k:it[k] for k in ('canonical_article_id','plan_slot','title','target_keyword','category','article_type')},'fachworkflow_authority':'EXISTING_UNCHANGED_BOUND_FACHWORKFLOW_ONLY','fachworkflow_prompt_ref':FACH,'allowed_output_root':root+'/','item_receipt_ref':rec,'item_receipt_schema':{'contract':IREC,'room_token':s['current_room_token'],'canonical_article_id':it['canonical_article_id'],'plan_slot':it['plan_slot'],'status':['PASS','BLOCKED','USER_ACTION_REQUIRED'],'workflow_pass':'true only with PASS; false otherwise','navigation_decision':False,'state_write_requested':False,'workflow_change_requested':False,'content_or_quality_rules_changed':False,'outputs':'non-empty [{ref,sha256}] under allowed_output_root, excluding item_receipt_ref, only with PASS; [] otherwise','evidence':'non-empty string list'},'submission_command':f'python3 control/single-door-boundary/codex_current_room_bridge.py submit {rec}','worker_may_choose_next_room':False,'worker_may_choose_next_item':False,'workflow_navigation_authority':False,'content_or_quality_rule_change_authority':'NONE','publish_allowed':False,'all_other_actions':'DENY'}
    return mod(DUAL,'dual_rootfix_action').augment_current_action(REPO,base,it)
def check_item_receipt(d,s,it,verify=True):
    keys={'contract','room_token','canonical_article_id','plan_slot','status','workflow_pass','navigation_decision','state_write_requested','workflow_change_requested','content_or_quality_rules_changed','outputs','evidence','fachworkflow_pass_ref','fachworkflow_pass_sha256'}
    if set(d)!=keys or d.get('contract')!=IREC: raise Blocked('ITEM_RECEIPT_FIELDS_OR_CONTRACT_INVALID')
    if d.get('room_token')!=s.get('current_room_token'): raise Blocked('ITEM_RECEIPT_ROOM_MISMATCH')
    if d.get('canonical_article_id')!=it.get('canonical_article_id'): raise Blocked('ITEM_RECEIPT_ARTICLE_MISMATCH')
    if d.get('plan_slot')!=it.get('plan_slot'): raise Blocked('ITEM_RECEIPT_PLAN_SLOT_MISMATCH')
    if d.get('status') not in {'PASS','BLOCKED','USER_ACTION_REQUIRED'}: raise Blocked('ITEM_RECEIPT_STATUS_INVALID')
    if d.get('navigation_decision') is not False: raise Blocked('ITEM_NAVIGATION_AUTHORITY_FORBIDDEN')
    if d.get('state_write_requested') is not False: raise Blocked('ITEM_STATE_WRITE_AUTHORITY_FORBIDDEN')
    if d.get('workflow_change_requested') is not False: raise Blocked('ITEM_WORKFLOW_CHANGE_AUTHORITY_FORBIDDEN')
    if d.get('content_or_quality_rules_changed') is not False: raise Blocked('CONTENT_OR_QUALITY_RULE_CHANGE_FORBIDDEN')
    ev=d.get('evidence')
    if not isinstance(ev,list) or not ev or not all(isinstance(x,str) and x.strip() for x in ev): raise Blocked('ITEM_RECEIPT_EVIDENCE_INVALID')
    if d['status']!='PASS':
        if d.get('workflow_pass') is not False: raise Blocked('NONPASS_WORKFLOW_PASS_MUST_BE_FALSE')
        return {'status':d['status'],'outputs':[],'evidence':ev}
    if d.get('workflow_pass') is not True: raise Blocked('ITEM_FULL_WORKFLOW_PASS_REQUIRED')
    mod(DUAL,'dual_rootfix_pass').validate_fachworkflow_pass(REPO,action(s,it),it,d)
    outs=d.get('outputs')
    if not isinstance(outs,list) or not outs: raise Blocked('ITEM_OUTPUTS_REQUIRED')
    a=action(s,it); seen=set(); clean=[]
    for i,x in enumerate(outs):
        if not isinstance(x,dict) or set(x)!={'ref','sha256'}: raise Blocked('ITEM_OUTPUT_ROW_INVALID:'+str(i))
        ref=x['ref']
        if not ref.startswith(a['allowed_output_root']) or ref==a['item_receipt_ref'] or ref in seen: raise Blocked('ITEM_OUTPUT_REF_INVALID:'+ref)
        seen.add(ref)
        if verify:
            p=REPO/rel(ref)
            if not p.is_file() or sha(p)!=x['sha256']: raise Blocked('ITEM_OUTPUT_HASH_MISMATCH:'+ref)
        clean.append({'ref':ref,'sha256':x['sha256']})
    return {'status':'PASS','outputs':clean,'evidence':ev}
def accept(s,it,path,rr):
    if not path.is_file(): raise Blocked('ITEM_RECEIPT_MISSING')
    z=check_item_receipt(load(path),s,it,True)
    if z['status']!='PASS': return {'contract':BRIDGE,'status':z['status'],'room_token':s['current_room_token'],'evidence':z['evidence'],'advanced':False,'publish_allowed':False}
    c=load(CP); validate_cp(c); iid=it['canonical_article_id']
    if c.get('next_item_id')!=iid or iid in c.get('completed_item_ids',[]): raise Blocked('CHECKPOINT_CURRENT_ITEM_MISMATCH')
    done=list(c['completed_item_ids'])+[iid]; rem=[x for x in c['bound_item_ids'] if x not in done]
    c['completed_item_ids']=done; c['receipt_hashes']=list(c.get('receipt_hashes',[]))+[sha(path)]
    if rem: c.update(status='BATCH_ACTIVE',current_item_id=rem[0],next_item_id=rem[0],current_gate_id='BOUND_ITEM_EXECUTION')
    else: c.update(status='BATCH_COMPLETE',current_item_id=None,next_item_id=None,current_gate_id='BATCH_COMPLETE')
    validate_cp(c); dump(CP,c); s['accepted_output_refs']=list(s.get('accepted_output_refs',[]))+z['outputs']; advance(s,rr,z['evidence']); return {'status':'PASS'}
def outer_receipt(t,s):
    o=list(s.get('accepted_output_refs',[]))
    if not o: raise Blocked('OUTER_RECEIPT_OUTPUTS_MISSING')
    return {'contract':'PFERDE_ATELIER_STEP_RECEIPT_V2','ticket_id':t['ticket_id'],'step_id':t['step_id'],'sequence':t['sequence'],'state_sha256':t['state_sha256'],'bundle_sha256':t['bundle_sha256'],'status':'PASS','navigation_decision':False,'state_write_requested':False,'workflow_change_requested':False,'payload':{'execution_origin':'BOUND_WORKER','workflow_pass':True,'batch_sha256':s['batch_sha256'],'outputs':o},'evidence':['BOUND_SINGLE_DOOR_ITEM_CHAIN_COMPLETE','BATCH_CHECKPOINT_VALID_AND_COMPLETE']}
def complete(t,s):
    dump(CAP/'RECEIPT.json',outer_receipt(t,s)); z=run_json([sys.executable,str(RUNTIME_ENTRY),'complete',str(CAP/'RECEIPT.json')])
    if z.get('status')!='107007_PASS_STAGED_NOT_VISIBLE_107008_READY': raise Blocked('107007_COMPLETE_STATUS_INVALID:'+str(z.get('status')))
    s.update(status='107008_READY',current_room_token='R_009',publish_allowed=False); dump(STATE,s)
    return {'contract':BRIDGE,'status':'FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH','outer_step':107008,'visible_project_result':False,'publish_allowed':False,'worker_may_continue_without_user_review':False}
def drive(s,t,m,r,its,rm,rt):
    while True:
        tok=s['current_room_token']; rr=row(rm,rt,tok)
        if tok=='R_001':
            if m.get('canonical_repo_execution_required') is not True: raise Blocked('R001_CANONICAL_EXECUTION_NOT_BOUND')
            advance(s,rr,['CURRENT_HASH_BOUND_CAPSULE_MATERIALIZED_BY_OFFICIAL_RUNTIME_ENTRY']); continue
        if tok=='R_002':
            if runtime().get('batch_sha256')!=r.get('batch_sha256'): raise Blocked('RUNTIME_BINDING_CHANGED_DURING_BRIDGE')
            advance(s,rr,['RUNTIME_INPUTS_BOUND']); continue
        if tok=='R_003':
            p=mod(PREFLIGHT,'room_preflight'); pkg=load(REPO/rel(load(RSTATE)['production_package_ref'])); q=p.validate(pkg)
            if q.get('status')!='PASS': raise Blocked('PRODUCTION_PACKAGE_PREFLIGHT_NOT_PASS')
            advance(s,rr,['PRODUCTION_PACKAGE_PREFLIGHT_PASS']); continue
        if tok=='R_004':
            c=load(CP); validate_cp(c)
            if len(c['bound_item_ids'])!=len(its): raise Blocked('CHECKPOINT_BOUND_COUNT_MISMATCH')
            advance(s,rr,['LINEAR_BOUND_ITEM_CHAIN_MATERIALIZED']); continue
        if tok.startswith('R_D_') and tok.endswith('_01'):
            it=item_for(its,tok); proof=validate_cp(load(CP))
            if proof.get('next_item_id')!=it['canonical_article_id']: raise Blocked('CURRENT_ROOM_NOT_FIRST_REMAINING_ITEM')
            return action(s,it)
        if tok.startswith('R_D_') and tok.endswith('_02'):
            validate_cp(load(CP)); advance(s,rr,['BATCH_CHECKPOINT_VALID']); continue
        if tok=='R_006':
            q=mod(CONT,'room_finalize').finalize(load(CP))
            if q.get('status')!='BATCH_FINAL_RECEIPT_ALLOWED': raise Blocked('BATCH_FINAL_RECEIPT_NOT_ALLOWED')
            advance(s,rr,['BATCH_FINAL_RECEIPT_ALLOWED']); continue
        if tok=='R_007': dump(CAP/'RECEIPT.json',outer_receipt(t,s)); advance(s,rr,['BOUND_107007_RECEIPT_WRITTEN']); continue
        if tok=='R_008': return complete(t,s)
        raise Blocked('ROOM_NOT_EXECUTABLE_BY_107007_CODEX_BRIDGE:'+tok)
def current():
    outer_authority(); t,m=capsule(); r=runtime(); its=items(r); rm,rt=route(len(its)); s=init(t,r,its)
    if s.get('status')=='107008_READY': return {'contract':BRIDGE,'status':'FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH','outer_step':107008,'publish_allowed':False,'worker_may_continue_without_user_review':False}
    return drive(s,t,m,r,its,rm,rt)
def submit(ref):
    outer_authority(); t,m=capsule(); r=runtime(); its=items(r); rm,rt=route(len(its)); s=init(t,r,its); tok=s['current_room_token']; rr=row(rm,rt,tok); it=item_for(its,tok)
    z=accept(s,it,REPO/rel(ref),rr)
    return z if z.get('status')!='PASS' else drive(s,t,m,r,its,rm,rt)
def selftest():
    s={'ticket_id':'a'*64,'current_room_token':'R_D_1_01'}; it={'canonical_article_id':'article:test','plan_slot':'b'*64,'title':'T','target_keyword':'K','category':'C','article_type':'A'}; a=action(s,it)
    if any(k in a for k in ('rooms','route','next_room_token','server_executor','future_items','bound_item_ids')): raise AssertionError('PUBLIC_ROUTE_LEAK')
    if a['worker_may_choose_next_room'] is not False or a['worker_may_choose_next_item'] is not False or a['content_or_quality_rule_change_authority']!='NONE' or a['publish_allowed'] is not False: raise AssertionError('PUBLIC_AUTHORITY_INVALID')
    b={'contract':IREC,'room_token':'R_D_1_01','canonical_article_id':'article:test','plan_slot':'b'*64,'status':'PASS','workflow_pass':True,'navigation_decision':False,'state_write_requested':False,'workflow_change_requested':False,'content_or_quality_rules_changed':False,'outputs':[{'ref':a['allowed_output_root']+'x.json','sha256':'c'*64}],'evidence':['PASS']}; check_item_receipt(b,s,it,False)
    tests=[('room_token','R_D_2_01'),('canonical_article_id','article:other'),('plan_slot','d'*64),('navigation_decision',True),('state_write_requested',True),('workflow_change_requested',True),('content_or_quality_rules_changed',True),('workflow_pass',False)]
    n=0
    for k,v in tests:
        x=dict(b); x[k]=v
        try: check_item_receipt(x,s,it,False)
        except Blocked: n+=1
        else: raise AssertionError('NEGATIVE_NOT_BLOCKED:'+k)
    return {'ok':True,'status':'CODEX_CURRENT_ROOM_BRIDGE_SELFTEST_PASS','positive':1,'negative':n,'worker_visible_current_room_only':True,'full_route_exposed':False,'next_room_exposed':False,'worker_navigation_authority':False,'content_or_quality_rule_change_authority':'NONE','publish_allowed':False}
def main(a):
    try:
        if a==['current']: z=current()
        elif len(a)==2 and a[0]=='submit': z=submit(a[1])
        elif a==['selftest']: z=selftest()
        else: raise Blocked('USAGE: current | submit ITEM_RECEIPT.json | selftest')
        print(json.dumps(z,ensure_ascii=False,indent=2)); return 0
    except (Blocked,ValueError,KeyError,TypeError,json.JSONDecodeError) as e:
        print(json.dumps({'ok':False,'status':'CODEX_CURRENT_ROOM_BRIDGE_BLOCKED','error':str(e),'publish_allowed':False},ensure_ascii=False,indent=2)); return 2
if __name__=='__main__': raise SystemExit(main(sys.argv[1:]))
