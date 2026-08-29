#!/usr/bin/env python3
"""Content-blind batch continuity/no-stop guard."""
from __future__ import annotations
import argparse,json
from pathlib import Path
class Blocked(RuntimeError): pass

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def validate(s):
    if s.get('contract')!='PFERDE_ATELIER_BATCH_CHECKPOINT_V1': raise Blocked('CONTRACT')
    bound=s.get('bound_item_ids'); done=s.get('completed_item_ids')
    if not isinstance(bound,list) or not bound or len(bound)!=len(set(bound)): raise Blocked('BOUND_ITEMS')
    if not isinstance(done,list) or len(done)!=len(set(done)): raise Blocked('COMPLETED_ITEMS')
    if not set(done)<=set(bound): raise Blocked('COMPLETED_NOT_BOUND')
    status=s.get('status')
    if status not in {'BATCH_ACTIVE','BATCH_COMPLETE','BLOCKED_USER_ACTION','BLOCKED_HARD_FAIL'}: raise Blocked('STATUS')
    remaining=[x for x in bound if x not in done]
    if status=='BATCH_COMPLETE' and remaining: raise Blocked('FALSE_COMPLETE')
    if status=='BATCH_ACTIVE' and not remaining: raise Blocked('ACTIVE_WITH_NOTHING_REMAINING')
    if status=='BATCH_ACTIVE' and s.get('next_item_id')!=remaining[0]: raise Blocked('NEXT_ITEM_MISMATCH')
    if s.get('workflow_navigation_authority') is not False: raise Blocked('WORKER_NAVIGATION_FORBIDDEN')
    if s.get('domain_logic_authority')!='NONE': raise Blocked('DOMAIN_AUTHORITY_FORBIDDEN')
    return {'ok':True,'status':'BATCH_CHECKPOINT_VALID','remaining':remaining,'next_item_id':remaining[0] if remaining else None}
def finalize(s):
    validate(s)
    if s.get('status')!='BATCH_COMPLETE': raise Blocked('FINAL_RECEIPT_REQUIRES_BATCH_COMPLETE')
    return {'ok':True,'status':'BATCH_FINAL_RECEIPT_ALLOWED','completed_count':len(s['completed_item_ids'])}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('command',choices=['validate','finalize']); ap.add_argument('checkpoint'); a=ap.parse_args()
    try:
        r=validate(load(a.checkpoint)) if a.command=='validate' else finalize(load(a.checkpoint)); print(json.dumps(r,indent=2)); return 0
    except Blocked as e:
        print(json.dumps({'ok':False,'status':'BATCH_CONTINUITY_BLOCKED','reason':str(e)},indent=2)); return 2
if __name__=='__main__': raise SystemExit(main())
