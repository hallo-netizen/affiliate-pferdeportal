from __future__ import annotations
import hashlib, json
from pathlib import Path
import point0_snapshot

CONTRACT='SYSTEM4_SUPERVISOR_STATE_V2'
class SupervisorError(RuntimeError): pass

def sha(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def canon(v)->bytes: return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
def stable(v)->str: return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def arm(point0_path:Path, workspace:Path, *, actual_manifest:str, actual_head:str, item_index:int)->dict:
    raw=point0_path.read_bytes(); v=json.loads(raw.decode('utf-8')); prod_raw=point0_snapshot.verify(v)
    if v['root_manifest_sha256']!=actual_manifest: raise SupervisorError('ROOT_MANIFEST_MISMATCH')
    if v['head_sha']!=actual_head: raise SupervisorError('HEAD_SHA_MISMATCH')
    prod=json.loads(prod_raw.decode('utf-8')); items=prod['next_textmachine_metadata_batch']['items']
    if not isinstance(item_index,int) or isinstance(item_index,bool) or item_index<0 or item_index>=len(items): raise SupervisorError('ITEM_INDEX_INVALID')
    pool,binding=point0_snapshot.item_bindings(v,item_index)
    article=items[item_index]
    if binding.get('article_identity')!={k:article[k] for k in ('title','target_keyword','category','article_type','plan_slot')}: raise SupervisorError('PREWRITE_ARTICLE_IDENTITY_MISMATCH')
    workspace.mkdir(parents=True,exist_ok=True)
    p0=workspace/'point0.json'; p0.write_bytes(raw)
    snap=workspace/'bound_snapshot.json'; snap.write_bytes(prod_raw)
    source_pool=workspace/'bound_research_sources.json'
    source_pool.write_bytes(canon({'contract':'SYSTEM4_BOUND_RESEARCH_POOL_V2','item_index':item_index,'plan_slot':article['plan_slot'],'sources':pool['sources']}))
    prewrite=workspace/'bound_machine_prewrite.json'; prewrite.write_bytes(canon(binding))
    state={'contract':CONTRACT,'phase':'RESEARCH_REQUIRED','item_index':item_index,'plan_slot':article['plan_slot'],'point0_sha256':sha(raw),'production_snapshot_sha256':sha(prod_raw),'research_pool_sha256':sha(source_pool.read_bytes()),'machine_prewrite_sha256':sha(prewrite.read_bytes()),'root_manifest_sha256':actual_manifest,'head_sha':actual_head,'worker_dispatch_allowed':True,'publish_allowed':False}
    state['supervisor_state_sha256']=sha(canon(state))
    (workspace/'supervisor_state.json').write_bytes(canon(state))
    return state

def worker_contract(workspace:Path)->dict:
    sp=workspace/'supervisor_state.json'; p0=workspace/'point0.json'; snap=workspace/'bound_snapshot.json'; pool=workspace/'bound_research_sources.json'; pre=workspace/'bound_machine_prewrite.json'
    if not all(p.is_file() for p in (sp,p0,snap,pool,pre)): raise SupervisorError('SUPERVISOR_ARTIFACT_MISSING')
    s=json.loads(sp.read_text()); core=dict(s); expected=core.pop('supervisor_state_sha256',None)
    if expected!=sha(canon(core)): raise SupervisorError('SUPERVISOR_STATE_TAMPERED')
    if s.get('worker_dispatch_allowed') is not True or s.get('phase')!='RESEARCH_REQUIRED': raise SupervisorError('WORKER_DISPATCH_CLOSED')
    if sha(p0.read_bytes())!=s['point0_sha256'] or sha(snap.read_bytes())!=s['production_snapshot_sha256'] or sha(pool.read_bytes())!=s['research_pool_sha256'] or sha(pre.read_bytes())!=s['machine_prewrite_sha256']: raise SupervisorError('SUPERVISOR_BOUND_BYTES_CHANGED')
    return {'contract':'SYSTEM4_BOUND_WORKER_DISPATCH_V2','phase':'RESEARCH_REQUIRED','item_index':s['item_index'],'plan_slot':s['plan_slot'],'production_snapshot_path':str(snap),'research_pool_path':str(pool),'machine_prewrite_path':str(pre),'point0_sha256':s['point0_sha256'],'head_sha':s['head_sha'],'publish_allowed':False,'external_web_search_allowed':False,'machine_prewrite_mutation_allowed':False}

def _validated_state(workspace:Path)->dict:
    sp=workspace/'supervisor_state.json'; p0=workspace/'point0.json'; snap=workspace/'bound_snapshot.json'; pool=workspace/'bound_research_sources.json'; pre=workspace/'bound_machine_prewrite.json'; receipt=workspace/'root_receipt.json'
    if not all(p.is_file() for p in (sp,p0,snap,pool,pre,receipt)): raise SupervisorError('SUPERVISOR_ARTIFACT_MISSING')
    s=json.loads(sp.read_text()); core=dict(s); expected=core.pop('supervisor_state_sha256',None)
    if expected!=sha(canon(core)): raise SupervisorError('SUPERVISOR_STATE_TAMPERED')
    if sha(p0.read_bytes())!=s['point0_sha256'] or sha(snap.read_bytes())!=s['production_snapshot_sha256'] or sha(pool.read_bytes())!=s['research_pool_sha256'] or sha(pre.read_bytes())!=s['machine_prewrite_sha256']: raise SupervisorError('SUPERVISOR_BOUND_BYTES_CHANGED')
    r=json.loads(receipt.read_text()); rcore=dict(r); rexp=rcore.pop('receipt_sha256',None)
    if rexp!=sha(canon(rcore)): raise SupervisorError('ROOT_RECEIPT_TAMPERED')
    for k in ('item_index','plan_slot','point0_sha256','production_snapshot_sha256','research_pool_sha256','machine_prewrite_sha256','root_manifest_sha256','head_sha','publish_allowed'):
        if r.get(k)!=s.get(k): raise SupervisorError('ROOT_SUPERVISOR_BINDING_MISMATCH:'+k)
    return s

def verify_controller_binding(workspace:Path, state:dict|None=None)->dict:
    s=_validated_state(workspace)
    if state is not None:
        if state.get('source_snapshot_sha256')!=s.get('production_snapshot_sha256'): raise SupervisorError('CONTROLLER_SOURCE_SNAPSHOT_MISMATCH')
        if state.get('publish_allowed') is not False: raise SupervisorError('CONTROLLER_PUBLISH_AUTHORITY_FAIL')
        article=state.get('article') if isinstance(state.get('article'),dict) else {}
        if article.get('plan_slot')!=s.get('plan_slot'): raise SupervisorError('CONTROLLER_PLAN_SLOT_MISMATCH')
        pre=json.loads((workspace/'bound_machine_prewrite.json').read_text())
        if pre.get('item_index')!=s.get('item_index') or pre.get('article_identity')!={k:article.get(k) for k in ('title','target_keyword','category','article_type','plan_slot')}:
            raise SupervisorError('CONTROLLER_PREWRITE_IDENTITY_MISMATCH')
    return s

def expected_research_document(workspace:Path)->dict:
    _validated_state(workspace)
    pool=json.loads((workspace/'bound_research_sources.json').read_text())
    if pool.get('contract')!='SYSTEM4_BOUND_RESEARCH_POOL_V2' or not isinstance(pool.get('sources'),list) or not pool['sources']:
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

def validate_production_plan_submission(workspace:Path, plan:dict)->None:
    _validated_state(workspace)
    pre=json.loads((workspace/'bound_machine_prewrite.json').read_text())
    if pre.get('contract')!=point0_snapshot.PREWRITE_CONTRACT: raise SupervisorError('BOUND_PREWRITE_CONTRACT_INVALID')
    core=dict(pre); expected=core.pop('binding_sha256',None)
    if expected!=point0_snapshot.stable(core): raise SupervisorError('BOUND_PREWRITE_INTEGRITY_FAIL')
    rails=pre.get('production_plan_rails')
    if not isinstance(rails,dict): raise SupervisorError('BOUND_PREWRITE_RAILS_MISSING')
    for key,value in rails.items():
        if plan.get(key)!=value: raise SupervisorError('MACHINE_PREWRITE_RAIL_MISMATCH:'+key)
    runtime=plan.get('runtime_order') if isinstance(plan.get('runtime_order'),dict) else {}
    links=(rails.get('quality_binding') or {}).get('link_bindings') if isinstance(rails.get('quality_binding'),dict) else None
    if runtime.get('links')!=links: raise SupervisorError('MACHINE_PREWRITE_RUNTIME_LINK_MISMATCH')
