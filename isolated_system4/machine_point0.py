from __future__ import annotations
import copy, hashlib, json, re, subprocess, sys
from pathlib import Path
import authoring_contract, chat_start_gate, point0_snapshot, production_checks, root_entry, source_acquisition

class MachinePoint0Error(RuntimeError): pass

SOURCE_ACQUISITION_MACHINE='SOURCE_ACQUISITION_MACHINE'
SOURCE_ACQUISITION_STAGE='SOURCE_ACQUISITION_STAGE'
RUNTIME_STATE_REL='control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
PORTAL_STRUCTURE_REL='affiliate-portal-router/assets/portal-structure-v279.json'
QUALITY_CONTRACT='content_structure_language_binding_v2'
REGISTRY_CONTRACT='portal_link_registry_snapshot_v2'
ROLE_SECTIONS={
    'parent_category':'criteria',
    'semantic_related':'decision',
    'further_information':'further_information',
}

def _head(repo:Path)->str:
    return subprocess.check_output(['git','rev-parse','--verify','HEAD'],cwd=repo,text=True).strip()

def _sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def _stable(value)->str:
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()

def _safe_repo(repo:Path,ref:str)->Path:
    p=Path(str(ref or ''))
    if not ref or p.is_absolute() or '..' in p.parts: raise MachinePoint0Error('CURRENT_RUNTIME_REF_INVALID')
    out=(repo/p).resolve(); root=repo.resolve()
    if out!=root and root not in out.parents: raise MachinePoint0Error('CURRENT_RUNTIME_REF_ESCAPE')
    return out

def bind_chat_start(snapshot:dict,event:dict)->dict:
    try: return chat_start_gate.bind(snapshot,event)
    except Exception as exc: raise MachinePoint0Error(str(exc)) from exc

def validate_chat_start(snapshot:dict)->dict:
    try: return chat_start_gate.validate(snapshot)
    except Exception as exc: raise MachinePoint0Error(str(exc)) from exc

def _source_owner_route(message:str):
    message=str(message or '').strip()
    # These failures belong to the source-loading/acquisition stage itself. They may be
    # retried/reacquired, but Point-0 must not be created from the failed acquisition.
    if message.startswith((
        'SOURCE_HTTP_FAIL:',
        'SOURCE_FETCH_RUNTIME_FAIL:',
        'SOURCE_EVIDENCE_EMPTY:',
        'SOURCE_TITLE_MISSING:',
        'SOURCE_TOO_LARGE:',
    )):
        return SOURCE_ACQUISITION_MACHINE,SOURCE_ACQUISITION_STAGE
    # Malformed/unbound requests and unknown failures are not softened into a retry.
    return None

def _walk(value):
    if isinstance(value,dict):
        yield value
        for child in value.values(): yield from _walk(child)
    elif isinstance(value,list):
        for child in value: yield from _walk(child)

def _one(nodes:list[dict],predicate,code:str)->dict:
    matches=[node for node in nodes if predicate(node)]
    if len(matches)!=1: raise MachinePoint0Error(code+':'+str(len(matches)))
    return copy.deepcopy(matches[0])

def _href(*slugs:str)->str:
    clean=[str(slug or '').strip().strip('/') for slug in slugs]
    if any(not re.fullmatch(r'[a-z0-9-]+',slug) for slug in clean): raise MachinePoint0Error('PORTAL_HIERARCHY_SLUG_INVALID')
    return '/'+('/'.join(clean))+'/'

def _marker(plan_slot:str)->str:
    if not re.fullmatch(r'[0-9a-f]{64}',str(plan_slot or '')): raise MachinePoint0Error('PLAN_SLOT_INVALID_FOR_MACHINE_BINDING')
    return 'LT'+plan_slot[:12].upper()

def _dedupe(values:list[str])->list[str]:
    out=[]; seen=set()
    for raw in values:
        value=str(raw or '').strip(); key=value.casefold()
        if value and key not in seen:
            seen.add(key); out.append(value)
    return out

def _type_authority(repo:Path,article_type:str)->tuple[object,object]:
    package=(repo/production_checks.PPM_PACKAGE_REL).resolve()
    if not package.is_file() or production_checks.file_sha256(package)!=production_checks.PPM_PACKAGE_SHA256:
        raise MachinePoint0Error('PPM679_PREWRITE_PACKAGE_HASH_MISMATCH')
    try: definition=authoring_contract._type_definition(package,article_type)
    except Exception as exc: raise MachinePoint0Error('PPM679_PREWRITE_TYPE_AUTHORITY_READ_FAILED') from exc
    if not isinstance(definition,dict) or not definition: raise MachinePoint0Error('PPM679_PREWRITE_TYPE_AUTHORITY_MISSING:'+article_type)
    cert=definition.get('certification_evidence') if isinstance(definition.get('certification_evidence'),dict) else {}
    return definition.get('search_intent'),cert.get('gold_core_binding')

def _prewrite_plan(repo:Path,article:dict)->dict:
    structure_path=(repo/PORTAL_STRUCTURE_REL).resolve()
    if not structure_path.is_file(): raise MachinePoint0Error('PORTAL_STRUCTURE_MISSING')
    structure_raw=structure_path.read_bytes()
    try: structure=json.loads(structure_raw.decode('utf-8'))
    except Exception as exc: raise MachinePoint0Error('PORTAL_STRUCTURE_INVALID') from exc
    nodes=[dict(node) for node in _walk(structure) if isinstance(node,dict)]
    category_slug=str(article.get('category') or '').strip()
    article_type=str(article.get('article_type') or '').strip()
    category=_one(
        nodes,
        lambda n:n.get('node_type')=='themenkategorie' and n.get('category_slug')==category_slug and int(n.get('level') or 0)==4,
        'PORTAL_CATEGORY_NOT_UNIQUE',
    )
    if str(category.get('theme') or '').casefold()!=article_type.casefold():
        raise MachinePoint0Error('PORTAL_CATEGORY_ARTICLE_TYPE_MISMATCH')
    main_slug=str(category.get('main_slug') or '').strip()
    hub_slug=str(category.get('hub_slug') or '').strip()
    product_slug=str(category.get('product_slug') or '').strip()
    main_title=str(category.get('main_hub') or '').strip()
    hub_title=str(category.get('hub') or '').strip()
    product_title=str(category.get('product') or '').strip()
    category_name=str(category.get('category_name') or '').strip()
    hierarchy_path=str(category.get('path') or '').strip()
    if not all((main_slug,hub_slug,product_slug,main_title,hub_title,product_title,category_name,hierarchy_path)):
        raise MachinePoint0Error('PORTAL_CATEGORY_HIERARCHY_INCOMPLETE')
    main=_one(nodes,lambda n:n.get('node_type')=='main_hub' and n.get('slug')==main_slug and int(n.get('level') or 0)==1,'PORTAL_MAIN_HUB_NOT_UNIQUE')
    hub=_one(nodes,lambda n:n.get('node_type')=='bereichs_hub' and n.get('slug')==hub_slug and int(n.get('level') or 0)==2,'PORTAL_AREA_HUB_NOT_UNIQUE')
    product=_one(nodes,lambda n:n.get('node_type')=='produktseite' and n.get('slug')==product_slug and int(n.get('level') or 0)==3,'PORTAL_PRODUCT_PAGE_NOT_UNIQUE')
    if str(hub.get('parent_slug') or '')!=main_slug: raise MachinePoint0Error('PORTAL_AREA_PARENT_MISMATCH')
    if str(product.get('parent_slug') or '')!=hub_slug: raise MachinePoint0Error('PORTAL_PRODUCT_PARENT_MISMATCH')
    if str(main.get('title') or '')!=main_title or str(hub.get('title') or '')!=hub_title or str(product.get('title') or '')!=product_title:
        raise MachinePoint0Error('PORTAL_HIERARCHY_TITLE_MISMATCH')
    structure_sha=_sha(structure_raw)
    base_links=[
        {'role':'parent_category','href':_href(main_slug),'anchor':main_title,'reason':'Maschinell gebundener Portal-Hauptbereich','section_id':ROLE_SECTIONS['parent_category']},
        {'role':'semantic_related','href':_href(main_slug,hub_slug),'anchor':hub_title,'reason':'Maschinell gebundener Portal-Bereich','section_id':ROLE_SECTIONS['semantic_related']},
        {'role':'further_information','href':_href(main_slug,hub_slug,product_slug),'anchor':product_title,'reason':'Maschinell gebundene Portal-Produktseite','section_id':ROLE_SECTIONS['further_information']},
    ]
    links=[dict(row,active=True,target_type='portal_route',target_status='publish') for row in base_links]
    registry={'contract':REGISTRY_CONTRACT,'snapshot_source_sha256':structure_sha,'entries':copy.deepcopy(links)}
    target_keyword=str(article.get('target_keyword') or '').strip()
    intent_terms=_dedupe([target_keyword,product_title,hub_title,main_title])
    if not intent_terms: raise MachinePoint0Error('MACHINE_INTENT_TERMS_EMPTY')
    table_statement='Die Tabelle bündelt die wichtigsten Auswahlkriterien für '+target_keyword+' und macht die entscheidenden Prüfpunkte direkt vergleichbar.'
    category_binding={
        'slug':category_slug,
        'name':category_name,
        'hierarchy_path':hierarchy_path,
        'taxonomy':'category',
        'category_source_snapshot_hash':structure_sha,
        'semantic_binding_not_numeric_identity':True,
    }
    quality={
        'contract':QUALITY_CONTRACT,
        'internal_test_marker':_marker(str(article.get('plan_slot') or '')),
        'intent_terms':intent_terms,
        'table_value_statement':table_statement,
        'language_evidence':{},
        'wordpress_category':copy.deepcopy(category_binding),
        'link_bindings':links,
        'portal_link_registry':registry,
        'portal_link_registry_hash':_stable(registry),
    }
    search_intent,gold_core_binding=_type_authority(repo,article_type)
    return {
        'article_type':article_type,
        'target_keyword':target_keyword,
        'topic':str(article.get('title') or '').strip(),
        'search_intent':search_intent,
        'gold_core_binding':gold_core_binding,
        'category_binding':category_binding,
        'quality_binding':quality,
        'quality_binding_hash':_stable(quality),
    }

def _current_snapshot_and_plans(repo:Path,manifest:str)->tuple[bytes,dict]:
    state_path=repo/RUNTIME_STATE_REL
    if not state_path.is_file(): raise MachinePoint0Error('CURRENT_RUNTIME_STATE_MISSING')
    state=json.loads(state_path.read_text(encoding='utf-8'))
    if state.get('status')!='EXECUTION_READY' or state.get('publish_allowed') is not False:
        raise MachinePoint0Error('CURRENT_RUNTIME_NOT_EXECUTION_READY')
    generation=state.get('generation')
    if not isinstance(generation,int) or isinstance(generation,bool) or generation<1:
        raise MachinePoint0Error('CURRENT_RUNTIME_GENERATION_INVALID')
    expected_ref=f'control/startmaster0107/runtime_inbox/generations/{generation:06d}/SOURCE_SNAPSHOT.json'
    source_ref=str(state.get('source_snapshot_ref') or '')
    if source_ref!=expected_ref: raise MachinePoint0Error('CURRENT_RUNTIME_SOURCE_REF_MISMATCH')
    source_path=_safe_repo(repo,source_ref)
    raw=source_path.read_bytes()
    expected_sha=str(state.get('source_snapshot_sha256') or '')
    if not re.fullmatch(r'[0-9a-f]{64}',expected_sha) or _sha(raw)!=expected_sha:
        raise MachinePoint0Error('CURRENT_RUNTIME_SOURCE_HASH_MISMATCH')
    projection=json.loads(raw.decode('utf-8'))
    if projection.get('contract')!='PFERDE_ATELIER_RUNTIME_SNAPSHOT_PROJECTION_V1':
        raise MachinePoint0Error('CURRENT_RUNTIME_SOURCE_CONTRACT_INVALID')
    batch=projection.get('next_textmachine_metadata_batch')
    if not isinstance(batch,dict) or batch.get('batch_sha256')!=state.get('batch_sha256') or batch.get('publish_allowed') is not False:
        raise MachinePoint0Error('CURRENT_RUNTIME_BATCH_BINDING_MISMATCH')
    items=batch.get('items')
    if not isinstance(items,list) or not items or batch.get('item_count')!=len(items):
        raise MachinePoint0Error('CURRENT_RUNTIME_ITEMS_INVALID')
    prod={
        'contract':point0_snapshot.PROD_CONTRACT,
        'next_textmachine_metadata_batch':copy.deepcopy(batch),
        'source_snapshot_original_sha256':str(projection.get('source_snapshot_sha256') or expected_sha),
        'system4_root_manifest_sha256':manifest,
    }
    event={
        'contract':chat_start_gate.START_EVENT_CONTRACT,
        'button_id':chat_start_gate.START_BUTTON_ID,
        'action':chat_start_gate.START_ACTION,
        'route':chat_start_gate.START_ROUTE,
        'article_count':len(items),
        'batch_sha256':batch['batch_sha256'],
        'publish_allowed':False,
    }
    prod=bind_chat_start(prod,event)
    plans=[]
    for index,article in enumerate(items):
        if not isinstance(article,dict): raise MachinePoint0Error('CURRENT_RUNTIME_ITEM_INVALID:'+str(index))
        plans.append({'item_index':index,'plan_slot':article.get('plan_slot'),'production_plan_item':_prewrite_plan(repo,article)})
    plan_batch={
        'contract':'SYSTEM4_MACHINE_PREWRITE_PLAN_BATCH_V1',
        'item_count':len(plans),
        'authority':'CURRENT_RUNTIME_PLUS_PORTAL_STRUCTURE_PLUS_PPM679',
        'items':plans,
    }
    return point0_snapshot.canon(prod),plan_batch

def build_from_acquired(*, snapshot_bytes:bytes, acquired_batch:dict, prewrite_plan_batch:dict, provider:str, manifest:str, head:str)->dict:
    prod=point0_snapshot._validate_prod(snapshot_bytes); validate_chat_start(prod)
    try:
        chat_start_gate.forbid_dataforseo(provider); chat_start_gate.forbid_dataforseo(acquired_batch); chat_start_gate.forbid_dataforseo(prewrite_plan_batch)
    except Exception as exc: raise MachinePoint0Error(str(exc)) from exc
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

def _acquire(source_value:dict,out:Path):
    try:
        chat_start_gate.forbid_dataforseo(source_value)
        return source_acquisition.acquire_batch(source_value)
    except source_acquisition.SourceAcquisitionError as exc:
        routed=_source_owner_route(str(exc))
        if routed is None: raise
        owner,route=routed
        if out.exists(): raise MachinePoint0Error('SOURCE_OWNER_RETURN_POINT0_ALREADY_EXISTS') from exc
        print('SYSTEM4_SOURCE_OWNER_RETURN:'+owner+':'+route+':'+str(exc))
        return None

def main(argv:list[str])->int:
    try:
        if len(argv)>=2 and argv[1]=='bind-start':
            if len(argv)!=5: raise MachinePoint0Error('BAD_COMMAND')
            snapshot=Path(argv[2]); event=Path(argv[3]); out=Path(argv[4])
            value=bind_chat_start(json.loads(snapshot.read_text(encoding='utf-8')),json.loads(event.read_text(encoding='utf-8')))
            out.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
            print('SYSTEM4_CHAT_START_PASS:'+value['system4_chat_start']['receipt_sha256']); return 0
        repo=Path(__file__).resolve().parent.parent; manifest=root_entry._critical_manifest_sha256(); head=_head(repo)
        if len(argv)==5 and argv[1]=='build-current-fetch':
            sources=Path(argv[2]); out=Path(argv[3]); provider=argv[4]
            if out.exists(): raise MachinePoint0Error('POINT0_OUTPUT_ALREADY_EXISTS')
            raw,plan_value=_current_snapshot_and_plans(repo,manifest)
            source_value=json.loads(sources.read_text(encoding='utf-8'))
            acquired=_acquire(source_value,out)
            if acquired is None: return 4
            value=build_from_acquired(snapshot_bytes=raw,acquired_batch=acquired,prewrite_plan_batch=plan_value,provider=provider,manifest=manifest,head=head)
            out.write_bytes(point0_snapshot.canon(value))
            print('SYSTEM4_MACHINE_POINT0_CURRENT_PASS:'+value['point0_core_sha256']); return 0
        if len(argv)!=7 or argv[1] not in {'build-acquired','build-fetch'}: raise MachinePoint0Error('BAD_COMMAND')
        snapshot=Path(argv[2]); sources=Path(argv[3]); plans=Path(argv[4]); out=Path(argv[5]); provider=argv[6]
        raw=snapshot.read_bytes()
        source_value=json.loads(sources.read_text(encoding='utf-8'))
        if argv[1]=='build-fetch':
            source_value=_acquire(source_value,out)
            if source_value is None: return 4
        plan_value=json.loads(plans.read_text(encoding='utf-8'))
        value=build_from_acquired(snapshot_bytes=raw,acquired_batch=source_value,prewrite_plan_batch=plan_value,provider=provider,manifest=manifest,head=head)
        out.write_bytes(point0_snapshot.canon(value)); print('SYSTEM4_MACHINE_POINT0_PASS:'+value['point0_core_sha256']); return 0
    except Exception as exc:
        print('SYSTEM4_MACHINE_POINT0_FAIL:'+str(exc)); return 2
if __name__=='__main__': raise SystemExit(main(sys.argv))
