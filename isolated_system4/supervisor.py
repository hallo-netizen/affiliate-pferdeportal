from __future__ import annotations
import hashlib, json
from pathlib import Path
import point0_snapshot

CONTRACT='SYSTEM4_SUPERVISOR_STATE_V1'
class SupervisorError(RuntimeError): pass

def sha(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def canon(v)->bytes: return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()

def _item_at_snapshot(snapshot_bytes:bytes,item_index:int)->dict:
    try:value=json.loads(snapshot_bytes.decode('utf-8'))
    except Exception as exc: raise SupervisorError('PRODUCTION_SNAPSHOT_INVALID') from exc
    batch=value.get('next_textmachine_metadata_batch') if isinstance(value,dict) else None
    items=batch.get('items') if isinstance(batch,dict) else None
    if not isinstance(item_index,int) or isinstance(item_index,bool) or not isinstance(items,list) or item_index<0 or item_index>=len(items): raise SupervisorError('ARTICLE_INDEX_INVALID')
    item=items[item_index]
    if not isinstance(item,dict): raise SupervisorError('ARTICLE_BINDING_INVALID')
    return item

def arm(point0_path:Path, workspace:Path, *, actual_manifest:str, actual_head:str, item_index:int=0)->dict:
    raw=point0_path.read_bytes(); v=json.loads(raw.decode('utf-8')); prod=point0_snapshot.verify(v); _item_at_snapshot(prod,item_index)
    if v['root_manifest_sha256']!=actual_manifest: raise SupervisorError('ROOT_MANIFEST_MISMATCH')
    if v['head_sha']!=actual_head: raise SupervisorError('HEAD_SHA_MISMATCH')
    workspace.mkdir(parents=True,exist_ok=True)
    p0=workspace/'point0.json'; p0.write_bytes(raw)
    snap=workspace/'bound_snapshot.json'; snap.write_bytes(prod)
    source_pool=workspace/'bound_research_sources.json'
    source_pool.write_bytes(canon({'contract':'SYSTEM4_BOUND_RESEARCH_POOL_V1','sources':v['research_runtime']['sources']}))
    state={'contract':CONTRACT,'phase':'RESEARCH_REQUIRED','point0_sha256':sha(raw),'production_snapshot_sha256':sha(prod),'research_pool_sha256':sha(source_pool.read_bytes()),'root_manifest_sha256':actual_manifest,'head_sha':actual_head,'article_index':item_index,'worker_dispatch_allowed':True,'publish_allowed':False}
    state['supervisor_state_sha256']=sha(canon(state))
    (workspace/'supervisor_state.json').write_bytes(canon(state))
    return state

def worker_contract(workspace:Path)->dict:
    sp=workspace/'supervisor_state.json'; p0=workspace/'point0.json'; snap=workspace/'bound_snapshot.json'; pool=workspace/'bound_research_sources.json'
    if not all(p.is_file() for p in (sp,p0,snap,pool)): raise SupervisorError('SUPERVISOR_ARTIFACT_MISSING')
    s=json.loads(sp.read_text()); core=dict(s); expected=core.pop('supervisor_state_sha256',None)
    if expected!=sha(canon(core)): raise SupervisorError('SUPERVISOR_STATE_TAMPERED')
    if s.get('worker_dispatch_allowed') is not True or s.get('phase')!='RESEARCH_REQUIRED': raise SupervisorError('WORKER_DISPATCH_CLOSED')
    if sha(p0.read_bytes())!=s['point0_sha256'] or sha(snap.read_bytes())!=s['production_snapshot_sha256'] or sha(pool.read_bytes())!=s['research_pool_sha256']: raise SupervisorError('SUPERVISOR_BOUND_BYTES_CHANGED')
    _item_at_snapshot(snap.read_bytes(),s.get('article_index'))
    return {'contract':'SYSTEM4_CODEX_WORKER_DISPATCH_V1','phase':'RESEARCH_REQUIRED','production_snapshot_path':str(snap),'research_pool_path':str(pool),'point0_sha256':s['point0_sha256'],'head_sha':s['head_sha'],'article_index':s['article_index'],'publish_allowed':False,'external_web_search_allowed':False}

def _validated_state(workspace:Path)->dict:
    sp=workspace/'supervisor_state.json'; p0=workspace/'point0.json'; snap=workspace/'bound_snapshot.json'; pool=workspace/'bound_research_sources.json'; receipt=workspace/'root_receipt.json'
    if not all(p.is_file() for p in (sp,p0,snap,pool,receipt)): raise SupervisorError('SUPERVISOR_ARTIFACT_MISSING')
    s=json.loads(sp.read_text()); core=dict(s); expected=core.pop('supervisor_state_sha256',None)
    if expected!=sha(canon(core)): raise SupervisorError('SUPERVISOR_STATE_TAMPERED')
    if sha(p0.read_bytes())!=s['point0_sha256'] or sha(snap.read_bytes())!=s['production_snapshot_sha256'] or sha(pool.read_bytes())!=s['research_pool_sha256']: raise SupervisorError('SUPERVISOR_BOUND_BYTES_CHANGED')
    _item_at_snapshot(snap.read_bytes(),s.get('article_index'))
    r=json.loads(receipt.read_text()); rcore=dict(r); rexp=rcore.pop('receipt_sha256',None)
    if rexp!=sha(canon(rcore)): raise SupervisorError('ROOT_RECEIPT_TAMPERED')
    for k in ('point0_sha256','production_snapshot_sha256','research_pool_sha256','root_manifest_sha256','head_sha','article_index','publish_allowed'):
        if r.get(k)!=s.get(k): raise SupervisorError('ROOT_SUPERVISOR_BINDING_MISMATCH:'+k)
    return s

def verify_controller_binding(workspace:Path, state:dict|None=None)->dict:
    s=_validated_state(workspace)
    if state is not None:
        if state.get('source_snapshot_sha256')!=s.get('production_snapshot_sha256'): raise SupervisorError('CONTROLLER_SOURCE_SNAPSHOT_MISMATCH')
        if state.get('publish_allowed') is not False: raise SupervisorError('CONTROLLER_PUBLISH_AUTHORITY_FAIL')
        expected=_item_at_snapshot((workspace/'bound_snapshot.json').read_bytes(),s['article_index'])
        if state.get('article')!=expected: raise SupervisorError('CONTROLLER_ARTICLE_INDEX_BINDING_MISMATCH')
    return s

def expected_research_document(workspace:Path)->dict:
    _validated_state(workspace)
    pool=json.loads((workspace/'bound_research_sources.json').read_text())
    if pool.get('contract')!='SYSTEM4_BOUND_RESEARCH_POOL_V1' or not isinstance(pool.get('sources'),list) or not pool['sources']:
        raise SupervisorError('BOUND_RESEARCH_POOL_INVALID')
    rows=[]
    for src in pool['sources']:
        row={k:src[k] for k in ('source_id','source_title','source_url','retrieved_at','evidence','snapshot_sha256')}
        if isinstance(src.get('source_kind'),str) and src['source_kind'].strip(): row['source_kind']=src['source_kind'].strip()
        rows.append(row)
    return {'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':rows}

def validate_research_submission(workspace:Path, submitted:dict)->None:
    expected=expected_research_document(workspace)
    if submitted!=expected: raise SupervisorError('UNBOUND_RESEARCH_SUBMISSION_BLOCKED')
