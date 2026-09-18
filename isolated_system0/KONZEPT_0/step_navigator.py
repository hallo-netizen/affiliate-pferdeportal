#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MACHINE=ROOT/'STEP_MACHINE.json'
STATE=ROOT/'STEP_STATE.json'

class Blocked(RuntimeError): pass

def load(p): return json.loads(p.read_text(encoding='utf-8'))

def stepmap(machine):
    return {x['id']:x for x in machine['steps']}

def validate(machine,state):
    sm=stepmap(machine)
    cur=state.get('next_allowed_step')
    if cur not in sm: raise Blocked('UNKNOWN_NEXT_ALLOWED_STEP')
    if state.get('publish_allowed') is not False: raise Blocked('PUBLISH_MUST_REMAIN_FALSE')
    if state.get('controller_only_transition') is not True: raise Blocked('CONTROLLER_ONLY_TRANSITION_REQUIRED')
    return sm,cur

def show():
    machine=load(MACHINE); state=load(STATE); sm,cur=validate(machine,state)
    print(json.dumps({'status':'PASS','next_allowed_step':cur,'step':sm[cur]},ensure_ascii=False,indent=2))

def transition(step,status,next_step=None):
    machine=load(MACHINE); state=load(STATE); sm,cur=validate(machine,state)
    if step!=cur: raise Blocked('STEP_NOT_CURRENT')
    if status not in {'PASS','BLOCKED'}: raise Blocked('INVALID_RESULT_STATUS')
    if status=='BLOCKED':
        print(json.dumps({'status':'BLOCKED','next_allowed_step':cur,'state_changed':False},indent=2)); return
    allowed=sm[cur]['next']
    if not allowed:
        if next_step is not None: raise Blocked('TERMINAL_STEP_HAS_NO_NEXT')
        state['completed_steps'].append(cur); state['status']='AWAIT_USER_REVIEW_NO_PUBLISH'
        STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'status':'PASS','completed':cur,'terminal':True,'publish_allowed':False},indent=2)); return
    if next_step not in allowed: raise Blocked('NEXT_STEP_NOT_ALLOWED')
    state['completed_steps'].append(cur)
    state['next_allowed_step']=next_step
    state['last_transition']={'from':cur,'result':'PASS','to':next_step}
    STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','completed':cur,'next_allowed_step':next_step},indent=2))

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('show')
    t=sub.add_parser('transition'); t.add_argument('--step',required=True); t.add_argument('--status',required=True); t.add_argument('--next-step')
    a=ap.parse_args()
    try:
        if a.cmd=='show': show()
        else: transition(a.step,a.status,a.next_step)
        return 0
    except Blocked as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e)},indent=2)); return 2
if __name__=='__main__': sys.exit(main())
