from __future__ import annotations
import copy, hashlib, json
from typing import Any

START_EVENT_CONTRACT = 'SYSTEM4_CHAT_START_BUTTON_V1'
START_RECEIPT_CONTRACT = 'SYSTEM4_CHAT_START_RECEIPT_V1'
START_BUTTON_ID = 'PFERDE_ATELIER_4A_START'
START_ACTION = 'START_ARTICLE_BATCH'
START_ROUTE = 'SYSTEM4_POINT0_V2'

class ChatStartError(RuntimeError): pass

def stable(value:Any)->str:
    raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def has_dataforseo(value:Any)->bool:
    if isinstance(value,str): return 'dataforseo' in value.casefold()
    if isinstance(value,dict): return any(has_dataforseo(k) or has_dataforseo(v) for k,v in value.items())
    if isinstance(value,(list,tuple)): return any(has_dataforseo(v) for v in value)
    return False

def forbid_dataforseo(value:Any)->None:
    if has_dataforseo(value): raise ChatStartError('DATAFORSEO_FORBIDDEN_IN_SYSTEM4A')

def _batch(snapshot:dict)->dict:
    if not isinstance(snapshot,dict): raise ChatStartError('CHAT_START_SNAPSHOT_OBJECT_REQUIRED')
    batch=snapshot.get('next_textmachine_metadata_batch')
    if not isinstance(batch,dict): raise ChatStartError('CHAT_START_BATCH_MISSING')
    count=batch.get('item_count'); items=batch.get('items'); batch_sha=batch.get('batch_sha256')
    if not isinstance(count,int) or isinstance(count,bool) or count<1 or not isinstance(items,list) or len(items)!=count: raise ChatStartError('CHAT_START_BATCH_COUNT_INVALID')
    if not isinstance(batch_sha,str) or len(batch_sha)!=64: raise ChatStartError('CHAT_START_BATCH_SHA_INVALID')
    if batch.get('publish_allowed') is not False: raise ChatStartError('CHAT_START_PUBLISH_FLAG_INVALID')
    return batch

def bind(snapshot:dict,event:dict)->dict:
    if not isinstance(event,dict): raise ChatStartError('CHAT_START_EVENT_OBJECT_REQUIRED')
    forbid_dataforseo(snapshot); forbid_dataforseo(event)
    batch=_batch(snapshot); count=batch['item_count']; batch_sha=batch['batch_sha256']
    expected={
        'contract':START_EVENT_CONTRACT,
        'button_id':START_BUTTON_ID,
        'action':START_ACTION,
        'route':START_ROUTE,
        'article_count':count,
        'batch_sha256':batch_sha,
        'publish_allowed':False,
    }
    if event!=expected: raise ChatStartError('CHAT_START_EVENT_INVALID')
    core={
        'contract':START_RECEIPT_CONTRACT,
        'button_id':START_BUTTON_ID,
        'action':START_ACTION,
        'route':START_ROUTE,
        'article_count':count,
        'batch_sha256':batch_sha,
        'publish_allowed':False,
        'event_sha256':stable(event),
    }
    receipt=dict(core); receipt['receipt_sha256']=stable(core)
    out=copy.deepcopy(snapshot); out['system4_chat_start']=receipt
    return out

def validate(snapshot:dict)->dict:
    forbid_dataforseo(snapshot)
    batch=_batch(snapshot); receipt=snapshot.get('system4_chat_start')
    if not isinstance(receipt,dict): raise ChatStartError('CHAT_START_RECEIPT_REQUIRED')
    event_sha=receipt.get('event_sha256')
    if not isinstance(event_sha,str) or len(event_sha)!=64: raise ChatStartError('CHAT_START_EVENT_SHA_INVALID')
    core={
        'contract':START_RECEIPT_CONTRACT,
        'button_id':START_BUTTON_ID,
        'action':START_ACTION,
        'route':START_ROUTE,
        'article_count':batch['item_count'],
        'batch_sha256':batch['batch_sha256'],
        'publish_allowed':False,
        'event_sha256':event_sha,
    }
    if receipt.get('receipt_sha256')!=stable(core): raise ChatStartError('CHAT_START_RECEIPT_INTEGRITY_FAIL')
    for key,value in core.items():
        if receipt.get(key)!=value: raise ChatStartError('CHAT_START_RECEIPT_BINDING_FAIL:'+key)
    if set(receipt)!=set(core)|{'receipt_sha256'}: raise ChatStartError('CHAT_START_RECEIPT_FIELDS_INVALID')
    return receipt
