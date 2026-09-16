from __future__ import annotations
import base64, hashlib, json, re
import content_guard

CONTRACT='SYSTEM4_POINT0_SNAPSHOT_V2'
PROD_CONTRACT='SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1'
PREWRITE_CONTRACT='SYSTEM4_MACHINE_PREWRITE_ITEM_V1'
HEX64=re.compile(r'^[0-9a-f]{64}$')

class Point0Error(RuntimeError): pass

def canon(v)->bytes:
    return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')

def sha256(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def stable(v)->str: return sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))

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

def _validate_sources(sources:list[dict], *, label:str='POOL')->None:
    if not isinstance(sources,list) or not sources: raise Point0Error('RESEARCH_SOURCE_POOL_EMPTY:'+label)
    seen=set()
    for i,s in enumerate(sources):
        if not isinstance(s,dict): raise Point0Error(f'RESEARCH_SOURCE_INVALID:{label}:{i}')
        sid=s.get('source_id'); url=s.get('source_url'); title=s.get('source_title'); ev=s.get('evidence'); digest=s.get('snapshot_sha256')
        if not isinstance(sid,str) or not sid.strip() or sid in seen: raise Point0Error(f'RESEARCH_SOURCE_ID_INVALID:{label}:{i}')
        seen.add(sid)
        if not isinstance(url,str) or not re.match(r'^https?://',url): raise Point0Error(f'RESEARCH_SOURCE_URL_INVALID:{label}:{i}')
        if not isinstance(title,str) or not title.strip(): raise Point0Error(f'RESEARCH_SOURCE_TITLE_INVALID:{label}:{i}')
        if not isinstance(ev,str) or len(ev.strip())<20: raise Point0Error(f'RESEARCH_SOURCE_EVIDENCE_INVALID:{label}:{i}')
        if digest!=sha256(ev.encode('utf-8')): raise Point0Error(f'RESEARCH_SOURCE_HASH_MISMATCH:{label}:{i}')
        try: status=int(s.get('http_status',0))
        except Exception: status=0
        if status<200 or status>=300: raise Point0Error(f'RESEARCH_SOURCE_HTTP_FAIL:{label}:{i}:{s.get("http_status")}')
        if not isinstance(s.get('retrieved_at'),str) or not s['retrieved_at'].strip(): raise Point0Error(f'RESEARCH_SOURCE_RETRIEVED_AT_INVALID:{label}:{i}')
    projected={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[]}
    for s in sources:
        row={k:s[k] for k in ('source_id','source_title','source_url','retrieved_at','evidence','snapshot_sha256')}
        if isinstance(s.get('source_kind'),str) and s['source_kind'].strip(): row['source_kind']=s['source_kind'].strip()
        projected['sources'].append(row)
    try: content_guard.validate_research_document(projected)
    except content_guard.ContentGuardError as e: raise Point0Error('RESEARCH_SOURCE_CONTENT_CONTRACT_FAIL:'+label+':'+str(e)) from e

def prewrite_from_plan(article:dict, item_index:int, plan:dict)->dict:
    if not isinstance(article,dict) or not isinstance(plan,dict): raise Point0Error('PREWRITE_INPUT_INVALID')
    identity={k:article[k] for k in ('title','target_keyword','category','article_type','plan_slot')}
    for k,expected in (('article_type',article['article_type']),('target_keyword',article['target_keyword']),('topic',article['title'])):
        if plan.get(k)!=expected: raise Point0Error('PREWRITE_PLAN_IDENTITY_MISMATCH:'+k)
    quality=plan.get('quality_binding')
    if not isinstance(quality,dict) or quality.get('contract')!='content_structure_language_binding_v2': raise Point0Error('PREWRITE_QUALITY_BINDING_INVALID')
    declared=str(plan.get('quality_binding_hash') or '').strip().lower()
    if declared!=stable(quality): raise Point0Error('PREWRITE_QUALITY_BINDING_HASH_INVALID')
    category_binding=plan.get('category_binding')
    wp=quality.get('wordpress_category')
    slug=(category_binding.get('slug') if isinstance(category_binding,dict) else None) or (wp.get('slug') if isinstance(wp,dict) else None)
    if slug!=article['category']: raise Point0Error('PREWRITE_CATEGORY_MISMATCH')
    links=quality.get('link_bindings')
    registry=quality.get('portal_link_registry')
    registry_hash=str(quality.get('portal_link_registry_hash') or '').lower().strip()
    if not isinstance(links,list) or not links: raise Point0Error('PREWRITE_LINK_BINDINGS_MISSING')
    if not isinstance(registry,dict) or registry_hash!=stable(registry): raise Point0Error('PREWRITE_LINK_REGISTRY_INVALID')
    roles=[]; sections=set()
    for i,row in enumerate(links):
        if not isinstance(row,dict): raise Point0Error(f'PREWRITE_LINK_INVALID:{i}')
        role=str(row.get('role') or ''); href=str(row.get('href') or ''); section=str(row.get('section_id') or '')
        if not role or role in roles: raise Point0Error('PREWRITE_LINK_ROLE_INVALID:'+role)
        if not href.startswith('/') or href.startswith('//') or re.match(r'^[a-z]+:',href,re.I): raise Point0Error('PREWRITE_LINK_TARGET_INVALID:'+role)
        if not section or section in sections: raise Point0Error('PREWRITE_LINK_SECTION_INVALID:'+role)
        if row.get('active') is not True or str(row.get('target_status') or '')!='publish': raise Point0Error('PREWRITE_LINK_TARGET_NOT_ACTIVE:'+role)
        roles.append(role); sections.add(section)
    rails={
      'article_type':plan['article_type'],
      'target_keyword':plan['target_keyword'],
      'topic':plan['topic'],
      'search_intent':plan.get('search_intent'),
      'gold_core_binding':plan.get('gold_core_binding'),
      'category_binding':category_binding,
      'quality_binding':quality,
      'quality_binding_hash':declared,
    }
    result={'contract':PREWRITE_CONTRACT,'item_index':item_index,'plan_slot':article['plan_slot'],'article_identity':identity,'production_plan_rails':rails}
    result['binding_sha256']=stable(result)
    return result

def _validate_prewrite(binding:dict, article:dict, item_index:int)->None:
    if not isinstance(binding,dict) or binding.get('contract')!=PREWRITE_CONTRACT: raise Point0Error('PREWRITE_CONTRACT_INVALID:'+str(item_index))
    core=dict(binding); expected=core.pop('binding_sha256',None)
    if expected!=stable(core): raise Point0Error('PREWRITE_INTEGRITY_FAIL:'+str(item_index))
    if binding.get('item_index')!=item_index or binding.get('plan_slot')!=article.get('plan_slot'): raise Point0Error('PREWRITE_ITEM_BINDING_MISMATCH:'+str(item_index))
    identity=binding.get('article_identity')
    expected_identity={k:article[k] for k in ('title','target_keyword','category','article_type','plan_slot')}
    if identity!=expected_identity: raise Point0Error('PREWRITE_ARTICLE_IDENTITY_MISMATCH:'+str(item_index))
    rails=binding.get('production_plan_rails')
    if not isinstance(rails,dict): raise Point0Error('PREWRITE_RAILS_MISSING:'+str(item_index))
    if rails.get('article_type')!=article['article_type'] or rails.get('target_keyword')!=article['target_keyword'] or rails.get('topic')!=article['title']: raise Point0Error('PREWRITE_RAIL_IDENTITY_MISMATCH:'+str(item_index))
    quality=rails.get('quality_binding')
    if not isinstance(quality,dict) or rails.get('quality_binding_hash')!=stable(quality): raise Point0Error('PREWRITE_RAIL_QUALITY_HASH_INVALID:'+str(item_index))
    category=rails.get('category_binding'); wp=quality.get('wordpress_category')
    slug=(category.get('slug') if isinstance(category,dict) else None) or (wp.get('slug') if isinstance(wp,dict) else None)
    if slug!=article['category']: raise Point0Error('PREWRITE_RAIL_CATEGORY_MISMATCH:'+str(item_index))

def build(*, production_snapshot_bytes:bytes, root_manifest_sha256:str, head_sha:str, research_provider:str, source_pools:list[list[dict]], prewrite_bindings:list[dict])->dict:
    prod=_validate_prod(production_snapshot_bytes)
    if not HEX64.fullmatch(root_manifest_sha256 or ''): raise Point0Error('ROOT_MANIFEST_INVALID')
    if prod.get('system4_root_manifest_sha256')!=root_manifest_sha256: raise Point0Error('PRODUCTION_ROOT_MANIFEST_MISMATCH')
    if not re.fullmatch(r'^[0-9a-f]{40}$',head_sha or ''): raise Point0Error('HEAD_SHA_INVALID')
    if not isinstance(research_provider,str) or not research_provider.strip(): raise Point0Error('RESEARCH_PROVIDER_INVALID')
    items=prod['next_textmachine_metadata_batch']['items']
    if not isinstance(source_pools,list) or len(source_pools)!=len(items): raise Point0Error('RESEARCH_ITEM_POOL_COUNT_MISMATCH')
    if not isinstance(prewrite_bindings,list) or len(prewrite_bindings)!=len(items): raise Point0Error('PREWRITE_ITEM_COUNT_MISMATCH')
    pools=[]
    for i,(article,sources,binding) in enumerate(zip(items,source_pools,prewrite_bindings)):
        _validate_sources(sources,label=str(i)); _validate_prewrite(binding,article,i)
        pools.append({'item_index':i,'plan_slot':article['plan_slot'],'source_count':len(sources),'sources':sources})
    payload={
      'contract':CONTRACT,
      'head_sha':head_sha,
      'root_manifest_sha256':root_manifest_sha256,
      'publish_allowed':False,
      'production_snapshot':{'encoding':'base64','byte_length':len(production_snapshot_bytes),'sha256':sha256(production_snapshot_bytes),'payload_base64':base64.b64encode(production_snapshot_bytes).decode('ascii')},
      'research_runtime':{'status':'PASS','provider':research_provider,'item_pool_count':len(pools),'item_pools':pools},
      'machine_prewrite':{'contract':'SYSTEM4_MACHINE_PREWRITE_BATCH_V1','item_count':len(prewrite_bindings),'items':prewrite_bindings},
    }
    payload['point0_core_sha256']=sha256(canon(payload))
    return payload

def verify(v:dict)->bytes:
    if not isinstance(v,dict) or v.get('contract')!=CONTRACT: raise Point0Error('POINT0_CONTRACT_INVALID')
    if v.get('publish_allowed') is not False: raise Point0Error('POINT0_PUBLISH_AUTHORITY_FAIL')
    expected=v.get('point0_core_sha256'); core=dict(v); core.pop('point0_core_sha256',None)
    if expected!=sha256(canon(core)): raise Point0Error('POINT0_INTEGRITY_FAIL')
    if not HEX64.fullmatch(str(v.get('root_manifest_sha256') or '')): raise Point0Error('ROOT_MANIFEST_INVALID')
    if not re.fullmatch(r'^[0-9a-f]{40}$',str(v.get('head_sha') or '')): raise Point0Error('HEAD_SHA_INVALID')
    ps=v.get('production_snapshot')
    if not isinstance(ps,dict) or ps.get('encoding')!='base64': raise Point0Error('PRODUCTION_SNAPSHOT_ENCODING_INVALID')
    try: raw=base64.b64decode(ps.get('payload_base64',''),validate=True)
    except Exception as e: raise Point0Error('PRODUCTION_SNAPSHOT_BASE64_INVALID') from e
    if len(raw)!=ps.get('byte_length'): raise Point0Error('PRODUCTION_SNAPSHOT_LENGTH_MISMATCH')
    if sha256(raw)!=ps.get('sha256'): raise Point0Error('PRODUCTION_SNAPSHOT_HASH_MISMATCH')
    prod=_validate_prod(raw)
    if prod.get('system4_root_manifest_sha256')!=v.get('root_manifest_sha256'): raise Point0Error('PRODUCTION_ROOT_MANIFEST_MISMATCH')
    items=prod['next_textmachine_metadata_batch']['items']
    rr=v.get('research_runtime')
    if not isinstance(rr,dict) or rr.get('status')!='PASS': raise Point0Error('RESEARCH_RUNTIME_NOT_READY')
    pools=rr.get('item_pools')
    if not isinstance(pools,list) or rr.get('item_pool_count')!=len(items) or len(pools)!=len(items): raise Point0Error('RESEARCH_ITEM_POOL_COUNT_MISMATCH')
    pre=v.get('machine_prewrite'); bindings=pre.get('items') if isinstance(pre,dict) else None
    if not isinstance(pre,dict) or pre.get('contract')!='SYSTEM4_MACHINE_PREWRITE_BATCH_V1' or pre.get('item_count')!=len(items) or not isinstance(bindings,list) or len(bindings)!=len(items): raise Point0Error('PREWRITE_BATCH_INVALID')
    for i,(article,pool,binding) in enumerate(zip(items,pools,bindings)):
        if not isinstance(pool,dict) or pool.get('item_index')!=i or pool.get('plan_slot')!=article['plan_slot']: raise Point0Error('RESEARCH_ITEM_POOL_BINDING_MISMATCH:'+str(i))
        sources=pool.get('sources'); _validate_sources(sources,label=str(i))
        if pool.get('source_count')!=len(sources): raise Point0Error('RESEARCH_SOURCE_COUNT_MISMATCH:'+str(i))
        _validate_prewrite(binding,article,i)
    return raw

def item_bindings(v:dict, item_index:int)->tuple[dict,dict]:
    raw=verify(v); prod=json.loads(raw.decode('utf-8')); items=prod['next_textmachine_metadata_batch']['items']
    if not isinstance(item_index,int) or isinstance(item_index,bool) or item_index<0 or item_index>=len(items): raise Point0Error('POINT0_ITEM_INDEX_INVALID')
    return v['research_runtime']['item_pools'][item_index], v['machine_prewrite']['items'][item_index]
