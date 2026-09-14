from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import point0_snapshot
import root_entry

CONTRACT='SYSTEM4_PARENT_LAUNCH_V1'
PROD_CONTRACT='SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1'
BATCH_CONTRACT='PSERC_TEXTMACHINE_METADATA_BATCH_V2'
HERE=Path(__file__).resolve().parent
REPO=HERE.parent
BOUND_DIR=(HERE/'bound_launches').resolve()

class ParentStartError(RuntimeError): pass

def canon(value)->bytes:
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')

def sha256(data:bytes)->str: return hashlib.sha256(data).hexdigest()

def _within(child:Path,parent:Path)->bool:
    child=child.resolve(); parent=parent.resolve(); return child==parent or parent in child.parents

def _load_bound_capsule(rel_path:str,expected_sha256:str)->dict:
    if not isinstance(rel_path,str) or not rel_path.startswith('isolated_system4/bound_launches/') or '..' in Path(rel_path).parts:
        raise ParentStartError('PARENT_BOUND_CAPSULE_PATH_INVALID')
    if not re.fullmatch(r'[0-9a-f]{64}',expected_sha256 or ''):
        raise ParentStartError('PARENT_BOUND_CAPSULE_SHA_INVALID')
    path=(REPO/rel_path).resolve()
    if not _within(path,BOUND_DIR) or not path.is_file():
        raise ParentStartError('PARENT_BOUND_CAPSULE_MISSING')
    try:
        tracked=root_entry._git('ls-files','--error-unmatch','--',rel_path)
        dirty=root_entry._git('status','--porcelain=v1','--',rel_path)
    except Exception as exc:
        raise ParentStartError('PARENT_BOUND_CAPSULE_GIT_BINDING_FAILED') from exc
    if tracked.strip()!=rel_path or dirty.strip():
        raise ParentStartError('PARENT_BOUND_CAPSULE_NOT_CLEAN_TRACKED')
    raw=path.read_bytes()
    if sha256(raw)!=expected_sha256:
        raise ParentStartError('PARENT_BOUND_CAPSULE_SHA_MISMATCH')
    try: value=json.loads(raw.decode('utf-8'))
    except Exception as exc: raise ParentStartError('PARENT_BOUND_CAPSULE_JSON_INVALID') from exc
    if canon(value)!=raw:
        raise ParentStartError('PARENT_BOUND_CAPSULE_NOT_CANONICAL')
    return value

def _validate_source(source,idx,src_idx):
    if not isinstance(source,dict): raise ParentStartError(f'PARENT_BOUND_SOURCE_INVALID:{idx}:{src_idx}')
    required=('source_id','source_title','source_url','retrieved_at','evidence','snapshot_sha256','http_status','source_kind')
    for key in required:
        if key not in source: raise ParentStartError(f'PARENT_BOUND_SOURCE_FIELD_MISSING:{idx}:{src_idx}:{key}')
    if not isinstance(source['source_id'],str) or not source['source_id'].strip(): raise ParentStartError(f'PARENT_BOUND_SOURCE_ID_INVALID:{idx}:{src_idx}')
    if not isinstance(source['source_title'],str) or not source['source_title'].strip(): raise ParentStartError(f'PARENT_BOUND_SOURCE_TITLE_INVALID:{idx}:{src_idx}')
    if not isinstance(source['source_url'],str) or not re.match(r'^https?://',source['source_url']): raise ParentStartError(f'PARENT_BOUND_SOURCE_URL_INVALID:{idx}:{src_idx}')
    if not isinstance(source['retrieved_at'],str) or 'T' not in source['retrieved_at']: raise ParentStartError(f'PARENT_BOUND_SOURCE_TIME_INVALID:{idx}:{src_idx}')
    if not isinstance(source['evidence'],str) or len(source['evidence'].strip())<20: raise ParentStartError(f'PARENT_BOUND_SOURCE_EVIDENCE_INVALID:{idx}:{src_idx}')
    if source['snapshot_sha256']!=sha256(source['evidence'].encode('utf-8')): raise ParentStartError(f'PARENT_BOUND_SOURCE_SHA_MISMATCH:{idx}:{src_idx}')
    if source['http_status']!=200: raise ParentStartError(f'PARENT_BOUND_SOURCE_HTTP_NOT_VERIFIED:{idx}:{src_idx}')
    if source['source_kind']!='parent_machine_bound_snapshot': raise ParentStartError(f'PARENT_BOUND_SOURCE_KIND_INVALID:{idx}:{src_idx}')
    return dict(source)

def _validate_launch(value):
    if not isinstance(value,dict) or value.get('contract')!=CONTRACT: raise ParentStartError('PARENT_LAUNCH_CONTRACT_INVALID')
    if value.get('publish_allowed') is not False: raise ParentStartError('PARENT_LAUNCH_PUBLISH_MUST_BE_FALSE')
    if 'source_urls' in value: raise ParentStartError('PARENT_LAUNCH_FREE_NETWORK_SOURCE_URLS_FORBIDDEN')
    items=value.get('items'); bound_sources=value.get('bound_sources')
    if not isinstance(items,list) or not items: raise ParentStartError('PARENT_LAUNCH_ITEMS_INVALID')
    if not isinstance(bound_sources,list) or len(bound_sources)!=len(items): raise ParentStartError('PARENT_LAUNCH_SOURCE_COUNT_MISMATCH')
    checked=[]
    for idx,item in enumerate(items):
        if not isinstance(item,dict): raise ParentStartError(f'PARENT_LAUNCH_ITEM_INVALID:{idx}')
        for key in ('title','target_keyword','category','article_type','plan_slot'):
            if not isinstance(item.get(key),str) or not item[key].strip(): raise ParentStartError(f'PARENT_LAUNCH_ITEM_FIELD_INVALID:{idx}:{key}')
        if not re.fullmatch(r'[0-9a-f]{64}',item['plan_slot']): raise ParentStartError(f'PARENT_LAUNCH_PLAN_SLOT_INVALID:{idx}')
        sources=bound_sources[idx]
        if not isinstance(sources,list) or not sources: raise ParentStartError(f'PARENT_BOUND_SOURCES_EMPTY:{idx}')
        checked.append([_validate_source(source,idx,src_idx) for src_idx,source in enumerate(sources)])
    return items,checked

def _build_production_snapshot(items,manifest):
    material={'contract':BATCH_CONTRACT,'content_or_format_payload_present':False,'item_count':len(items),'items':items,'maximum_articles':0,'maximum_articles_per_type':0,'publish_allowed':False,'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE'}
    material['batch_sha256']=sha256(canon(material))
    return canon({'contract':PROD_CONTRACT,'next_textmachine_metadata_batch':material,'source_snapshot_original_sha256':sha256(canon(items)),'system4_root_manifest_sha256':manifest})

def run_launch(launch,runtime_root:Path):
    if _within(runtime_root,REPO): raise ParentStartError('PARENT_RUNTIME_MUST_BE_OUTSIDE_REPO')
    items,bound_sources=_validate_launch(launch); manifest=root_entry._critical_manifest_sha256(); head=root_entry._git('rev-parse','--verify','HEAD'); production_bytes=_build_production_snapshot(items,manifest)
    runtime_root.mkdir(parents=True,exist_ok=False); workspaces=[]
    for index,sources in enumerate(bound_sources):
        prepared=point0_snapshot.prepare(production_snapshot_bytes=production_bytes,root_manifest_sha256=manifest,head_sha=head)
        final=point0_snapshot.finalize(prepared,research_provider='SYSTEM4_PARENT_MACHINE_BOUND_SNAPSHOT_V1',sources=sources)
        point0_path=runtime_root/f'point0-{index}.json'; point0_path.write_bytes(point0_snapshot.canon(final)); workspace=runtime_root/f'item-{index}'
        rc=root_entry.main(['root_entry.py','start-point0',str(point0_path),str(workspace),str(index)])
        if rc!=0: raise ParentStartError(f'PARENT_ROOT_START_FAILED:{index}:{rc}')
        workspaces.append(workspace)
    receipt={'contract':'SYSTEM4_PARENT_START_RECEIPT_V1','head_sha':head,'root_manifest_sha256':manifest,'article_count':len(items),'workspaces':[str(p) for p in workspaces],'source_transport':'PREBOUND_PARENT_SNAPSHOTS_NO_CODEX_NETWORK','publish_allowed':False}
    (runtime_root/'parent_start_receipt.json').write_bytes(canon(receipt)); return workspaces

def main(argv):
    try:
        if len(argv)!=5 or argv[1]!='start-bound': raise ParentStartError('PARENT_START_BAD_COMMAND')
        launch=_load_bound_capsule(argv[2],argv[3]); workspaces=run_launch(launch,Path(argv[4]))
        print('SYSTEM4_PARENT_START_PASS:POINT0_ROOT_DISPATCH_READY:ARTICLE_COUNT='+str(len(workspaces)))
        for index,workspace in enumerate(workspaces): print('SYSTEM4_PARENT_WORKSPACE:'+str(index)+':'+str(workspace))
        return 0
    except Exception as exc:
        print('SYSTEM4_PARENT_START_FAIL:'+str(exc)); return 2

if __name__=='__main__': raise SystemExit(main(sys.argv))
