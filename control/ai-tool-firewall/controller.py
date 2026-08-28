#!/usr/bin/env python3
"""Pferde Atelier AI Tool Firewall Controller V1.

Only permitted production execution entry point from STARTMASTER0103 onward.
Fail-closed: state/hash/step/policy/schema mismatches do not advance state.
"""
from __future__ import annotations
import argparse, json, hashlib, os, sys, urllib.request, urllib.error
from pathlib import Path

class FirewallBlocked(RuntimeError): pass

def sha256_bytes(b: bytes)->str: return hashlib.sha256(b).hexdigest()
def load_json(p: Path): return json.loads(p.read_text(encoding='utf-8'))
def norm(x): return str(x or '').strip()

def load_authority(master: Path):
    start=load_json(master/'PFERDE_ATELIER_START_HERE.json')
    state_rel=start.get('navigation_authority')
    if not state_rel: raise FirewallBlocked('START_HERE_NAVIGATION_AUTHORITY_MISSING')
    state_path=master/state_rel
    raw=state_path.read_bytes(); state=json.loads(raw)
    if sha256_bytes(raw) != start.get('current_state_sha256'): raise FirewallBlocked('CURRENT_STATE_HASH_BINDING_MISMATCH')
    if start.get('startmaster') != state.get('startmaster'): raise FirewallBlocked('STARTMASTER_IDENTITY_MISMATCH')
    if norm(start.get('next_allowed_step')) != norm(state.get('next_allowed_step')): raise FirewallBlocked('NEXT_ALLOWED_STEP_ROOT_STATE_MISMATCH')
    return start,state,state_path

def load_policy(master: Path):
    return load_json(master/'00_CONTROL/AI_TOOL_FIREWALL_CONTROLLER_V1/STEP_TOOL_POLICY_V1.json')

def resolve_step_policy(policy, step):
    exact=(policy.get('steps') or {}).get(step)
    if exact: return exact
    for row in policy.get('prefix_rules') or []:
        if step.startswith(row.get('prefix','')): return row
    raise FirewallBlocked('NO_TOOL_POLICY_FOR_NEXT_ALLOWED_STEP')

def validate_execution_envelope(state, step_policy):
    env=state.get('execution_firewall') or {}
    if env.get('enforced') is not True: raise FirewallBlocked('EXECUTION_FIREWALL_NOT_ENFORCED')
    if norm(env.get('step')) != norm(state.get('next_allowed_step')): raise FirewallBlocked('EXECUTION_FIREWALL_STEP_MISMATCH')
    if list(env.get('allowed_tools') or []) != list(step_policy.get('allowed_tools') or []): raise FirewallBlocked('EXECUTION_FIREWALL_TOOL_POLICY_MISMATCH')
    if env.get('state_write_authority') != 'CONTROLLER_ONLY': raise FirewallBlocked('STATE_WRITE_AUTHORITY_NOT_CONTROLLER_ONLY')
    return env

def build_model_request(state, step_policy, context_text, model):
    allowed=list(step_policy.get('allowed_tools') or [])
    definitions=[]; catalog=step_policy.get('tool_definitions') or {}
    for name in allowed:
        if name not in catalog: raise FirewallBlocked('ALLOWED_TOOL_DEFINITION_MISSING:'+name)
        definitions.append(catalog[name])
    submit={'type':'function','name':'submit_step_result','description':'Submit only the result of the exact NEXT_ALLOWED_STEP.','parameters':{'type':'object','additionalProperties':False,'properties':{'step':{'type':'string','enum':[state['next_allowed_step']]},'status':{'type':'string','enum':['PASS','BLOCKED','USER_ACTION_REQUIRED']},'evidence':{'type':'array','items':{'type':'string'}},'state_transition_requested':{'type':'boolean','enum':[False]}},'required':['step','status','evidence','state_transition_requested']},'strict':True}
    definitions.append(submit)
    allowed_choice=[{'type':'function','name':n} for n in allowed+['submit_step_result']]
    return {'model':model,'input':[{'role':'developer','content':'You are an execution worker. You have ZERO workflow-navigation authority. Execute only the supplied NEXT_ALLOWED_STEP. Never invent, repeat, skip, or reorder workflow steps. Never request or perform a state transition; only the controller may do that.'},{'role':'user','content':f"NEXT_ALLOWED_STEP={state['next_allowed_step']}\n\nAUTHORIZED_CONTEXT:\n{context_text}"}],'tools':definitions,'tool_choice':{'type':'allowed_tools','mode':'required','tools':allowed_choice},'parallel_tool_calls':False}

def validate_model_tool_call(tool_name, args, state, step_policy):
    allowed=set(step_policy.get('allowed_tools') or [])|{'submit_step_result'}
    if tool_name not in allowed: raise FirewallBlocked('MODEL_ATTEMPTED_FORBIDDEN_TOOL:'+tool_name)
    if tool_name=='submit_step_result':
        if args.get('step') != state.get('next_allowed_step'): raise FirewallBlocked('MODEL_RESULT_STEP_MISMATCH')
        if args.get('state_transition_requested') is not False: raise FirewallBlocked('MODEL_STATE_WRITE_REQUEST_REJECTED')
        if args.get('status') not in {'PASS','BLOCKED','USER_ACTION_REQUIRED'}: raise FirewallBlocked('MODEL_RESULT_STATUS_INVALID')
        if not isinstance(args.get('evidence'),list): raise FirewallBlocked('MODEL_RESULT_EVIDENCE_INVALID')
    return True

def post_openai(payload):
    key=os.getenv('OPENAI_API_KEY')
    if not key: raise FirewallBlocked('OPENAI_API_KEY_MISSING')
    req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=120) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e: raise FirewallBlocked('OPENAI_API_HTTP_'+str(e.code))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--master',required=True); ap.add_argument('--context-file'); ap.add_argument('--model',default=os.getenv('PFERDE_ATELIER_MODEL','gpt-5.4')); ap.add_argument('--dry-run',action='store_true'); args=ap.parse_args()
    try:
        master=Path(args.master); _,state,_=load_authority(master); step_policy=resolve_step_policy(load_policy(master),state['next_allowed_step']); validate_execution_envelope(state,step_policy)
        context=Path(args.context_file).read_text(encoding='utf-8') if args.context_file else ''
        payload=build_model_request(state,step_policy,context,args.model)
        if args.dry_run:
            print(json.dumps({'ok':True,'status':'FIREWALL_AUTHORITY_PASS','startmaster':state['startmaster'],'next_allowed_step':state['next_allowed_step'],'allowed_tools':step_policy.get('allowed_tools',[]),'dry_run':True,'request_sha256':sha256_bytes(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())},ensure_ascii=False,indent=2)); return 0
        response=post_openai(payload); calls=[x for x in response.get('output',[]) if x.get('type')=='function_call']
        if not calls: raise FirewallBlocked('MODEL_RETURNED_NO_FUNCTION_CALL')
        for c in calls:
            try: call_args=json.loads(c.get('arguments') or '{}')
            except Exception: raise FirewallBlocked('MODEL_TOOL_ARGUMENTS_NOT_JSON')
            validate_model_tool_call(c.get('name'),call_args,state,step_policy)
        print(json.dumps({'ok':True,'status':'MODEL_CALLS_FIREWALL_VALIDATED','call_count':len(calls)},ensure_ascii=False,indent=2)); return 0
    except FirewallBlocked as e:
        print(json.dumps({'ok':False,'status':'FIREWALL_BLOCKED','reason':str(e)},ensure_ascii=False,indent=2)); return 2

if __name__=='__main__': sys.exit(main())
