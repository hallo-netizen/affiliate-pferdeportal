from __future__ import annotations
import base64, hashlib, json, re
import content_guard

PREPARED_CONTRACT='SYSTEM4_POINT0_PREPARED_V1'
CONTRACT='SYSTEM4_POINT0_SNAPSHOT_V1'
PROD_CONTRACT='SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1'
HEX64=re.compile(r'^[0-9a-f]{64}$')

class Point0Error(RuntimeError): pass

def canon(v)->bytes:
    return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')

def sha256(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def _validate_prod(raw:bytes)->dict:
    try: v=json.loads(raw.decode('utf-8'))
    except Exception as e: raise Point0Error('PRODUCTION_SNAPSHOT_JSON_INVALID') from e
    if not isinstance(v,dict) or v.get('contract')!=PROD_CONTRACT: raise Point0Error('PRODUCTION_SNAPSHOT_CONTRACT_INVALID')
    b=v.get('next_textmachine_metadata_batch')
    if not isinstance(b,dict) or b.get('publish_allowed') is not False: raise Point0Error('PUBLISH_AUTHORITY_FAIL')
    items=b.get('items')
    if not isinstance(items,list) or not items or b.get('item_count')!=len(items): raise Point0Error('PRODUCTION_ITEMS_INVALID')
    for item in items:
        if not isinstance(item,dict): raise Point0Error('PRODUCTION_ITEM_INVALID')
        for k in ('title','target_keyword','category','article_type','plan_slot'):
            if not isinstance(item.get(k),str) or not item[k].strip(): raise Point0Error('PRODUCTION_ITEM_FIELD_INVALID:'+k)
    return v

def _snapshot_payload(raw:bytes)->dict:
    return {'encoding':'base64','byte_length':len(raw),'sha256':sha256(raw),'payload_base64':base64.b64encode(raw).decode('ascii')}

def _decode_snapshot(ps:dict)->bytes:
    if not isinstance(ps,dict) or ps.get('encoding')!='base64': raise Point0Error('PRODUCTION_SNAPSHOT_ENCODING_INVALID')
    try: raw=base64.b64decode(ps.get('payload_base64',''),validate=True)
    except Exception as e: raise Point0Error('PRODUCTION_SNAPSHOT_BASE64_INVALID') from e
    if len(raw)!=ps.get('byte_length'): raise Point0Error('PRODUCTION_SNAPSHOT_LENGTH_MISMATCH')
    if sha256(raw)!=ps.get('sha256'): raise Point0Error('PRODUCTION_SNAPSHOT_HASH_MISMATCH')
    return raw

def _validate_sources(sources:list[dict])->None:
    if not isinstance(sources,list) or not sources: raise Point0Error('RESEARCH_SOURCE_POOL_EMPTY')
    seen=set()
    for i,s in enumerate(sources):
        if not isinstance(s,dict): raise Point0Error(f'RESEARCH_SOURCE_INVALID:{i}')
        sid=s.get('source_id'); url=s.get('source_url'); title=s.get('source_title'); ev=s.get('evidence'); digest=s.get('snapshot_sha256')
        if not isinstance(sid,str) or not sid.strip() or sid in seen: raise Point0Error(f'RESEARCH_SOURCE_ID_INVALID:{i}')
        seen.add(sid)
        if not isinstance(url,str) or not re.match(r'^https?://',url): raise Point0Error(f'RESEARCH_SOURCE_URL_INVALID:{i}')
        if not isinstance(title,str) or not title.strip(): raise Point0Error(f'RESEARCH_SOURCE_TITLE_INVALID:{i}')
        if not isinstance(ev,str) or len(ev.strip())<20: raise Point0Error(f'RESEARCH_SOURCE_EVIDENCE_INVALID:{i}')
        if digest!=sha256(ev.encode('utf-8')): raise Point0Error(f'RESEARCH_SOURCE_HASH_MISMATCH:{i}')
        if int(s.get('http_status',0))<200 or int(s.get('http_status',0))>=300: raise Point0Error(f'RESEARCH_SOURCE_HTTP_FAIL:{i}:{s.get("http_status")}')
    projected={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[]}
    for s in sources:
        row={k:s[k] for k in ('source_id','source_title','source_url','retrieved_at','evidence','snapshot_sha256')}
        if isinstance(s.get('source_kind'),str) and s['source_kind'].strip(): row['source_kind']=s['source_kind'].strip()
        projected['sources'].append(row)
    try: content_guard.validate_research_document(projected)
    except content_guard.ContentGuardError as e: raise Point0Error('RESEARCH_SOURCE_CONTENT_CONTRACT_FAIL:'+str(e)) from e

def prepare(*,production_snapshot_bytes:bytes,root_manifest_sha256:str,head_sha:str)->dict:
    prod=_validate_prod(production_snapshot_bytes)
    if not HEX64.fullmatch(root_manifest_sha256 or ''): raise Point0Error('ROOT_MANIFEST_INVALID')
    if prod.get('system4_root_manifest_sha256')!=root_manifest_sha256: raise Point0Error('PRODUCTION_ROOT_MANIFEST_MISMATCH')
    if not re.fullmatch(r'^[0-9a-f]{40}$',head_sha or ''): raise Point0Error('HEAD_SHA_INVALID')
    payload={'contract':PREPARED_CONTRACT,'head_sha':head_sha,'root_manifest_sha256':root_manifest_sha256,'publish_allowed':False,'production_snapshot':_snapshot_payload(production_snapshot_bytes),'research_runtime':{'status':'REQUIRED'}}
    payload['point0_prepared_sha256']=sha256(canon(payload))
    return payload

def verify_prepared(v:dict)->bytes:
    if not isinstance(v,dict) or v.get('contract')!=PREPARED_CONTRACT: raise Point0Error('POINT0_PREPARED_CONTRACT_INVALID')
    if v.get('publish_allowed') is not False: raise Point0Error('POINT0_PUBLISH_AUTHORITY_FAIL')
    expected=v.get('point0_prepared_sha256'); core=dict(v); core.pop('point0_prepared_sha256',None)
    if expected!=sha256(canon(core)): raise Point0Error('POINT0_PREPARED_INTEGRITY_FAIL')
    if not HEX64.fullmatch(str(v.get('root_manifest_sha256') or '')): raise Point0Error('ROOT_MANIFEST_INVALID')
    if not re.fullmatch(r'^[0-9a-f]{40}$',str(v.get('head_sha') or '')): raise Point0Error('HEAD_SHA_INVALID')
    rr=v.get('research_runtime')
    if rr!={'status':'REQUIRED'}: raise Point0Error('POINT0_PREPARED_RESEARCH_STATE_INVALID')
    raw=_decode_snapshot(v.get('production_snapshot'))
    prod=_validate_prod(raw)
    if prod.get('system4_root_manifest_sha256')!=v.get('root_manifest_sha256'): raise Point0Error('PRODUCTION_ROOT_MANIFEST_MISMATCH')
    return raw

def finalize(prepared:dict,*,research_provider:str,sources:list[dict])->dict:
    raw=verify_prepared(prepared)
    if not isinstance(research_provider,str) or not research_provider.strip(): raise Point0Error('RESEARCH_PROVIDER_INVALID')
    _validate_sources(sources)
    payload={'contract':CONTRACT,'head_sha':prepared['head_sha'],'root_manifest_sha256':prepared['root_manifest_sha256'],'publish_allowed':False,'prepared_point0_sha256':prepared['point0_prepared_sha256'],'production_snapshot':_snapshot_payload(raw),'research_runtime':{'status':'PASS','provider':research_provider,'source_count':len(sources),'sources':sources}}
    payload['point0_core_sha256']=sha256(canon(payload))
    return payload

def build(*, production_snapshot_bytes:bytes, root_manifest_sha256:str, head_sha:str, research_provider:str, sources:list[dict])->dict:
    return finalize(prepare(production_snapshot_bytes=production_snapshot_bytes,root_manifest_sha256=root_manifest_sha256,head_sha=head_sha),research_provider=research_provider,sources=sources)

def verify(v:dict)->bytes:
    if not isinstance(v,dict) or v.get('contract')!=CONTRACT: raise Point0Error('POINT0_CONTRACT_INVALID')
    if v.get('publish_allowed') is not False: raise Point0Error('POINT0_PUBLISH_AUTHORITY_FAIL')
    expected=v.get('point0_core_sha256'); core=dict(v); core.pop('point0_core_sha256',None)
    if expected!=sha256(canon(core)): raise Point0Error('POINT0_INTEGRITY_FAIL')
    if not HEX64.fullmatch(str(v.get('root_manifest_sha256') or '')): raise Point0Error('ROOT_MANIFEST_INVALID')
    if not re.fullmatch(r'^[0-9a-f]{40}$',str(v.get('head_sha') or '')): raise Point0Error('HEAD_SHA_INVALID')
    if not HEX64.fullmatch(str(v.get('prepared_point0_sha256') or '')): raise Point0Error('POINT0_PREPARED_BINDING_INVALID')
    rr=v.get('research_runtime')
    if not isinstance(rr,dict) or rr.get('status')!='PASS': raise Point0Error('RESEARCH_RUNTIME_NOT_READY')
    sources=rr.get('sources'); _validate_sources(sources)
    if rr.get('source_count')!=len(sources): raise Point0Error('RESEARCH_SOURCE_COUNT_MISMATCH')
    raw=_decode_snapshot(v.get('production_snapshot'))
    prod=_validate_prod(raw)
    if prod.get('system4_root_manifest_sha256')!=v.get('root_manifest_sha256'): raise Point0Error('PRODUCTION_ROOT_MANIFEST_MISMATCH')
    prepared={'contract':PREPARED_CONTRACT,'head_sha':v['head_sha'],'root_manifest_sha256':v['root_manifest_sha256'],'publish_allowed':False,'production_snapshot':_snapshot_payload(raw),'research_runtime':{'status':'REQUIRED'}}
    prepared['point0_prepared_sha256']=sha256(canon(prepared))
    if prepared['point0_prepared_sha256']!=v.get('prepared_point0_sha256'): raise Point0Error('POINT0_PREPARED_BINDING_MISMATCH')
    return raw
