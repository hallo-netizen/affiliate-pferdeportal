#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
S4 = REPO / 'isolated_system4'
sys.path.insert(0, str(S4))
import handoff_transport

RUNTIME_STATE = REPO / 'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
OUTPUT_GATE = REPO / 'control/output-quarantine/output_release_gate.py'

class Blocked(RuntimeError):
    pass

def module(path: Path, name: str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise Blocked('MODULE_LOAD_FAILED')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def sha(path: Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def canon(v)->bytes: return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(path:Path)->dict:
    v=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(v,dict): raise Blocked('JSON_OBJECT_REQUIRED:'+str(path))
    return v

def prepare(handoff_path:Path)->dict:
    handoff_path=handoff_path.expanduser().resolve()
    payload, raw = handoff_transport.read_validate_handoff(handoff_path)
    if not RUNTIME_STATE.is_file(): raise Blocked('RUNTIME_STATE_MISSING')
    runtime=load(RUNTIME_STATE)
    batch=str(runtime.get('batch_sha256') or '')
    if payload.get('batch_sha256')!=batch: raise Blocked('SYSTEM4_HANDOFF_RUNTIME_BATCH_MISMATCH')
    if payload.get('publish_allowed') is not False: raise Blocked('AUTO_PUBLISH_FORBIDDEN')

    outgate=module(OUTPUT_GATE,'system4_output_release_gate')
    main_head=outgate.require_current_main()
    stage=REPO/'.pferde-release-staging'/batch/('system4-'+hashlib.sha256(raw).hexdigest())
    stage.mkdir(parents=True,exist_ok=True)
    staged=[]
    for article in payload['articles']:
        name='ARTICLE_'+article['plan_slot']+'.md'
        p=stage/name
        body=article['body'].encode('utf-8')
        if hashlib.sha256(body).hexdigest()!=article['final_draft_sha256']:
            raise Blocked('HANDOFF_ARTICLE_HASH_MISMATCH:'+article['plan_slot'])
        p.write_bytes(body)
        staged.append({'source_ref':str(handoff_path),'staged_ref':str(p.relative_to(REPO)),'sha256':sha(p)})

    prepared={
        'contract':'PFERDE_ATELIER_PREPARED_OUTPUT_RELEASE_V1',
        'status':'PREPARED_NOT_VISIBLE',
        'startmaster':'STARTMASTER0107',
        'source_step_id':'RUN_NEW_ARTICLE_BATCH_NO_STOP',
        'source_sequence':107007,
        'source_ticket_id':'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2:'+hashlib.sha256(raw).hexdigest(),
        'source_state_sha256':hashlib.sha256(raw).hexdigest(),
        'source_bundle_sha256':hashlib.sha256(raw).hexdigest(),
        'batch_sha256':batch,
        'worker_receipt_sha256':hashlib.sha256(raw).hexdigest(),
        'main_head':main_head,
        'staged_outputs':staged,
        'chat_execution_authority':'NONE',
        'chat_output_authority':'NONE',
        'domain_logic_authority':'NONE',
        'quality_authority':'NONE',
        'publish_allowed':False,
        'system4_handoff_ref':str(handoff_path),
        'system4_handoff_sha256':hashlib.sha256(raw).hexdigest(),
        'system4_handoff_contract':handoff_transport.HANDOFF_CONTRACT,
        'article_count':len(payload['articles']),
    }
    p=stage/'PREPARED_RELEASE.json'
    p.write_text(json.dumps(prepared,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return {'status':'SYSTEM4_V2_PREPARED_FOR_107008','prepared_ref':str(p.relative_to(REPO)),'prepared_sha256':sha(p),'handoff_sha256':hashlib.sha256(raw).hexdigest(),'article_count':len(payload['articles']),'batch_sha256':batch,'publish_allowed':False}

def main(argv:list[str])->int:
    try:
        if len(argv)!=3 or argv[1]!='prepare': raise Blocked('USE: system4_v2_release_bridge.py prepare HANDOFF_PATH')
        print(json.dumps(prepare(Path(argv[2])),ensure_ascii=False,sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({'status':'SYSTEM4_V2_RELEASE_BRIDGE_BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False,sort_keys=True))
        return 2
if __name__=='__main__': raise SystemExit(main(sys.argv))
