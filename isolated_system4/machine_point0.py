from __future__ import annotations
import copy, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
import point0_snapshot, root_entry, source_acquisition

START_EVENT_CONTRACT = 'SYSTEM4_CHAT_START_BUTTON_V1'
START_RECEIPT_CONTRACT = 'SYSTEM4_CHAT_START_RECEIPT_V1'
START_BUTTON_ID = 'PFERDE_ATELIER_4A_START'
START_ACTION = 'START_ARTICLE_BATCH'
START_ROUTE = 'SYSTEM4_POINT0_V2'

class MachinePoint0Error(RuntimeError): pass

def _head(repo:Path)->str:
    return subprocess.check_output(['git','rev-parse','--verify','HEAD'],cwd=repo,text=True).strip()

def _stable(value:Any)->str:
    raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def _has_dataforseo(value:Any)->bool:
    if isinstance(value,str): return 'dataforseo' in value.casefold()
    if isinstance(value,dict): return any(_has_dataforseo(k) or _has_dataforseo(v) for k,v in value.items())
    if isinstance(value,(list,tuple)): return any(_has_dataforseo(v) for v in value)
    return False

def _forbid_dataforseo(value:Any)->None:
    if _has_dataforseo(value): raise MachinePoint0Error('DATAFORSEO_FORBIDDEN_IN_SYSTEM4A')

def bind_chat_start(snapshot:dict,event:dict)->dict:
    if not isinstance(snapshot,dict): raise MachinePoint0Error('CHAT_START_SNAPSHOT_OBJECT_REQUIRED')
    if not isinstance(event,dict): raise MachinePoint0Error('CHAT_START_EVENT_OBJECT_REQUIRED')
    _forbid_dataforseo(event); _forbid_dataforseo(snapshot)
    batch=snapshot.get('next_textmachine_metadata_batch')
    if not isinstance(batch,dict): raise MachinePoint0Error('CHAT_START_BATCH_MISSING')
    count=batch.get('item_count'); items=batch.get('items'); batch_sha=batch.get('batch_sha256')
    if not isinstance(count,int) or count<1 or not isinstance(items,list) or len(items)!=count: raise MachinePoint0Error('CHAT_START_BATCH_COUNT_INVALID')
    if not isinstance(batch_sha,str) or len(batch_sha)!=64: raise MachinePoint0Error('CHAT_START_BATCH_SHA_INVALID')
    expected={
        'contract':START_EVENT_CONTRACT,
        'button_id':START_BUTTON_ID,
        'action':START_ACTION,
        'route':START_ROUTE,
        'article_count':count,
        'batch_sha256':batch_sha,
        'publish_allowed':False,
    }
    if event!=expected: raise MachinePoint0Error('CHAT_START_EVENT_INVALID')
    receipt_core={
        'contract':START_RECEIPT_CONTRACT,
        'button_id':START_BUTTON_ID,
        'action':START_ACTION,
        'route':START_ROUTE,
        'article_count':count,
        'batch_sha256':batch_sha,
        'publish_allowed':False,
        'event_sha256':_stable(event),
    }
    receipt=dict(receipt_core); receipt['receipt_sha256']=_stable(receipt_core)
    out=copy.deepcopy(snapshot); out['system4_chat_start']=receipt
    return out

def validate_chat_start(snapshot:dict)->dict:
    if not isinstance(snapshot,dict): raise MachinePoint0Error('CHAT_START_SNAPSHOT_OBJECT_REQUIRED')
    _forbid_dataforseo(snapshot)
    batch=snapshot.get('next_textmachine_metadata_batch'); receipt=snapshot.get('system4_chat_start')
    if not isinstance(batch,dict) or not isinstance(receipt,dict): raise MachinePoint0Error('CHAT_START_RECEIPT_REQUIRED')
    count=batch.get('item_count'); items=batch.get('items'); batch_sha=batch.get('batch_sha256')
    if not isinstance(count,int) or count<1 or not isinstance(items,list) or len(items)!=count: raise MachinePoint0Error('CHAT_START_BATCH_COUNT_INVALID')
    expected_core={
        'contract':START_RECEIPT_CONTRACT,
        'button_id':START_BUTTON_ID,
        'action':START_ACTION,
        'route':START_ROUTE,
        'article_count':count,
        'batch_sha256':batch_sha,
        'publish_allowed':False,
        'event_sha256':receipt.get('event_sha256'),
    }
    if not isinstance(expected_core['event_sha256'],str) or len(expected_core['event_sha256'])!=64: raise MachinePoint0Error('CHAT_START_EVENT_SHA_INVALID')
    if receipt.get('receipt_sha256')!=_stable(expected_core): raise MachinePoint0Error('CHAT_START_RECEIPT_INTEGRITY_FAIL')
    for key,value in expected_core.items():
        if receipt.get(key)!=value: raise MachinePoint0Error('CHAT_START_RECEIPT_BINDING_FAIL:'+key)
    if batch.get('publish_allowed') is not False: raise MachinePoint0Error('CHAT_START_PUBLISH_FLAG_INVALID')
    return receipt

def build_from_acquired(*, snapshot_bytes:bytes, acquired_batch:dict, prewrite_plan_batch:dict, provider:str, manifest:str, head:str)->dict:
    prod=point0_snapshot._validate_prod(snapshot_bytes); validate_chat_start(prod); _forbid_dataforseo(provider); _forbid_dataforseo(acquired_batch); _forbid_dataforseo(prewrite_plan_batch)
    items=prod['next_textmachine_metadata_batch']['items']
    acquired=acquired_batch.get('items') if isinstance(acquired_batch,dict) and acquired_batch.get('contract')==source_acquisition.RESULT_CONTRACT else None
    plans=prewrite_plan_batch.get('items') if isinstance(prewrite_plan_batch,dict) and prewrite_plan_batch.get('contract')=='SYSTEM4_MACHINE_PREWRITE_PLAN_BATCH_V1' else None
    if not isinstance(acquired,list) or acquired_batch.get('item_count')!=len(items) or len(acquired)!=len(items): raise MachinePoint0Error('ACQUIRED_SOURCE_BATCH_INVALID')
    if not isinstance(plans,list) or prewrite_plan_batch.get('item_count')!=len(items) or len(plans)!=len(items): raise MachinePoint0Error('PREWRITE_PLAN_BATCH_INVALID')
    pools=[]; bindings=[]
    for i,article in enumerate(items):
        ar=acquired[i]; pr=plans[i]
        if ar.get('item_index')!=i or ar.get('plan_slot')!=article['plan_slot']: raise MachinePoint0Error('ACQUIRED_SOURCE_ITEM_MISMATCH:'+str(i))
        if pr.get('item_index')!=i or pr.get('plan_slot')!=article['plan_slot'] or not isinstance(pr.get('production_plan_item'),dict): raise MachinePoint0Error('PREWRITE_PLAN_ITEM_MISMATCH:'+str(i))
        pools.append(ar['sources']); bindings.append(point0_snapshot.prewrite_from_plan(article,i,pr['production_plan_item']))
    return point0_snapshot.build(production_snapshot_bytes=snapshot_bytes,root_manifest_sha256=manifest,head_sha=head,research_provider=provider,source_pools=pools,prewrite_bindings=bindings)

def main(argv:list[str])->int:
    try:
        if len(argv)>=2 and argv[1]=='bind-start':
            if len(argv)!=5: raise MachinePoint0Error('BAD_COMMAND')
            snapshot=Path(argv[2]); event=Path(argv[3]); out=Path(argv[4])
            value=bind_chat_start(json.loads(snapshot.read_text(encoding='utf-8')),json.loads(event.read_text(encoding='utf-8')))
            out.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
            print('SYSTEM4_CHAT_START_PASS:'+value['system4_chat_start']['receipt_sha256']); return 0
        if len(argv)!=7 or argv[1] not in {'build-acquired','build-fetch'}: raise MachinePoint0Error('BAD_COMMAND')
        snapshot=Path(argv[2]); sources=Path(argv[3]); plans=Path(argv[4]); out=Path(argv[5]); provider=argv[6]
        repo=Path(__file__).resolve().parent.parent; manifest=root_entry._critical_manifest_sha256(); head=_head(repo); raw=snapshot.read_bytes()
        source_value=json.loads(sources.read_text(encoding='utf-8'))
        if argv[1]=='build-fetch':
            _forbid_dataforseo(source_value); source_value=source_acquisition.acquire_batch(source_value)
        plan_value=json.loads(plans.read_text(encoding='utf-8'))
        value=build_from_acquired(snapshot_bytes=raw,acquired_batch=source_value,prewrite_plan_batch=plan_value,provider=provider,manifest=manifest,head=head)
        out.write_bytes(point0_snapshot.canon(value)); print('SYSTEM4_MACHINE_POINT0_PASS:'+value['point0_core_sha256']); return 0
    except Exception as exc:
        print('SYSTEM4_MACHINE_POINT0_FAIL:'+str(exc)); return 2
if __name__=='__main__': raise SystemExit(main(sys.argv))
