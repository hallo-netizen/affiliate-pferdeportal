from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
from typing import Any,Mapping,Sequence
import content_guard
import design_guard
STATE_CONTRACT='SYSTEM4_CANONICAL_ARTICLE_STATE_V1'; BATCH_EVIDENCE_CONTRACT='SYSTEM4_FULL_PASS_BATCH_EVIDENCE_V1'; ALLOWED_ITEM_KEYS={'title','target_keyword','category','article_type','plan_slot'}; SHA_RE=re.compile(r'^[0-9a-f]{64}$')
class BatchGateError(RuntimeError): pass
def canonical(value:Any)->bytes: return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def stable_hash(value:Any)->str: return hashlib.sha256(canonical(value)).hexdigest()
def file_sha256(path:Path)->str: return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def text_sha256(value:str)->str: return hashlib.sha256(value.encode('utf-8')).hexdigest()
def load_json(path:Path)->dict[str,Any]:
    try: value=json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception as exc: raise BatchGateError('JSON_INVALID:'+str(path)) from exc
    if not isinstance(value,dict): raise BatchGateError('JSON_OBJECT_REQUIRED:'+str(path))
    return value
def immutable_core(state:Mapping[str,Any])->dict[str,Any]:
    try: return {key:state[key] for key in ('contract','source_snapshot_sha256','batch_sha256','article')}
    except KeyError as exc: raise BatchGateError('STATE_IMMUTABLE_CORE_MISSING') from exc
def load_snapshot(snapshot_path:Path):
    snapshot_path=Path(snapshot_path); snapshot=load_json(snapshot_path); batch=snapshot.get('next_textmachine_metadata_batch')
    if not isinstance(batch,dict) or batch.get('contract')!='PSERC_TEXTMACHINE_METADATA_BATCH_V2': raise BatchGateError('WORDPRESS_BATCH_CONTRACT_INVALID')
    if batch.get('status')!='READY_FOR_TEXTMACHINE_METADATA_INTAKE': raise BatchGateError('WORDPRESS_BATCH_NOT_READY')
    if batch.get('publish_allowed') is not False: raise BatchGateError('WORDPRESS_BATCH_PUBLISH_MUST_BE_FALSE')
    batch_sha=str(batch.get('batch_sha256') or '')
    if not SHA_RE.fullmatch(batch_sha): raise BatchGateError('WORDPRESS_BATCH_SHA_INVALID')
    items=batch.get('items')
    if not isinstance(items,list) or not items: raise BatchGateError('WORDPRESS_BATCH_ITEMS_INVALID')
    if batch.get('item_count')!=len(items): raise BatchGateError('WORDPRESS_BATCH_COUNT_MISMATCH')
    normalized=[]; seen_slots=set()
    for raw in items:
        if not isinstance(raw,dict) or set(raw)!=ALLOWED_ITEM_KEYS: raise BatchGateError('WORDPRESS_ITEM_SCHEMA_INVALID')
        item={key:str(raw[key]) for key in ALLOWED_ITEM_KEYS}
        if not all(item[key].strip() for key in ALLOWED_ITEM_KEYS): raise BatchGateError('WORDPRESS_ITEM_VALUE_INVALID')
        if not SHA_RE.fullmatch(item['plan_slot']): raise BatchGateError('WORDPRESS_PLAN_SLOT_INVALID')
        if item['plan_slot'] in seen_slots: raise BatchGateError('WORDPRESS_PLAN_SLOT_DUPLICATE')
        seen_slots.add(item['plan_slot']); normalized.append(item)
    return file_sha256(snapshot_path),batch_sha,normalized

def validate_full_production_evidence(checks:Mapping[str,Any],draft_sha:str)->dict[str,Any]:
    prod=checks.get('production_evidence')
    if not isinstance(prod,dict): raise BatchGateError('FULL_PRODUCTION_EVIDENCE_MISSING')
    if prod.get('contract')!='SYSTEM4_FULL_PRODUCTION_CHECK_V1' or prod.get('status')!='PASS': raise BatchGateError('FULL_PRODUCTION_EVIDENCE_INVALID')
    if prod.get('checked_draft_sha256')!=draft_sha: raise BatchGateError('FULL_PRODUCTION_EVIDENCE_DRAFT_MISMATCH')
    if prod.get('publish_allowed') is not False: raise BatchGateError('FULL_PRODUCTION_EVIDENCE_PUBLISH_MUST_BE_FALSE')
    evidence=prod.get('evidence')
    if not isinstance(evidence,dict): raise BatchGateError('FULL_PRODUCTION_NESTED_EVIDENCE_MISSING')
    no_legacy=evidence.get('no_legacy'); no_links=evidence.get('no_external_links'); lt=evidence.get('languagetool'); ppm=evidence.get('ppm679')
    if not isinstance(no_legacy,dict) or no_legacy.get('status')!='PASS' or no_legacy.get('legacy_import_count')!=0: raise BatchGateError('NO_LEGACY_EVIDENCE_NOT_PASS')
    if not isinstance(no_links,dict) or no_links.get('status')!='PASS' or no_links.get('external_link_count')!=0: raise BatchGateError('EXTERNAL_LINK_EVIDENCE_NOT_PASS')
    if not isinstance(lt,dict) or lt.get('status')!='PASS' or lt.get('engine')!='LanguageTool 6.8 / Bestand 43' or lt.get('finding_count')!=0: raise BatchGateError('LANGUAGETOOL_EVIDENCE_NOT_PASS')
    if not isinstance(ppm,dict) or ppm.get('status')!='PASS' or ppm.get('ppm_version')!='6.7.9': raise BatchGateError('PPM679_EVIDENCE_NOT_PASS')
    if ppm.get('technical_status')!='TECHNICAL_CHECK_OK' or ppm.get('content_quality_status')!='CONTENT_QUALITY_CHECK_OK' or ppm.get('fail_closed_aggregate_status')!='PASS': raise BatchGateError('PPM679_EVIDENCE_NOT_PASS')
    if ppm.get('content_sha256')!=draft_sha: raise BatchGateError('PPM679_CONTENT_HASH_MISMATCH')
    source=ppm.get('language_evidence_source')
    if source not in ('BOUND_CURRENT_REUSED','REAL_LT68_FULLCHECK_REUSED','REAL_LT68_CURRENT_DRAFT_REFRESHED'): raise BatchGateError('PPM679_LANGUAGE_EVIDENCE_SOURCE_INVALID')
    return {'languagetool':{'engine':lt['engine'],'status':'PASS','finding_count':0},'ppm679':{'version':'6.7.9','status':'PASS','technical_status':ppm['technical_status'],'content_quality_status':ppm['content_quality_status'],'fail_closed_aggregate_status':ppm['fail_closed_aggregate_status'],'language_evidence_source':source},'no_legacy':'PASS','external_links':'PASS'}

def _validated_stage_text(state:Mapping[str,Any],field:str)->str:
    value=state.get(field)
    if not isinstance(value,dict) or not isinstance(value.get('text'),str) or text_sha256(value['text'])!=value.get('sha256'):
        raise BatchGateError('STATE_'+field.upper()+'_INTEGRITY_FAIL')
    return value['text']

def validate_state(state,expected_article,source_snapshot_sha256,batch_sha256):
    if state.get('contract')!=STATE_CONTRACT: raise BatchGateError('STATE_CONTRACT_INVALID')
    if stable_hash(immutable_core(state))!=state.get('immutable_core_sha256'): raise BatchGateError('STATE_IMMUTABLE_CORE_TAMPERED')
    if state.get('source_snapshot_sha256')!=source_snapshot_sha256: raise BatchGateError('STATE_SOURCE_SNAPSHOT_MISMATCH')
    if state.get('batch_sha256')!=batch_sha256: raise BatchGateError('STATE_BATCH_MISMATCH')
    if state.get('article')!=dict(expected_article): raise BatchGateError('STATE_ARTICLE_BINDING_MISMATCH')
    if state.get('publish_allowed') is not False: raise BatchGateError('STATE_PUBLISH_MUST_BE_FALSE')
    if state.get('phase')!='OUTPUT_GATE_REQUIRED': raise BatchGateError('STATE_NOT_AT_OUTPUT_GATE')
    if state.get('released') is not False: raise BatchGateError('STATE_ALREADY_RELEASED')
    if state.get('release_prepared') is not None: raise BatchGateError('PER_ARTICLE_RELEASE_PREPARED_FORBIDDEN')
    checks=state.get('checks')
    if not isinstance(checks,dict) or checks.get('status')!='PASS' or checks.get('mode')!='FULL_PRODUCTION': raise BatchGateError('FULL_PRODUCTION_PASS_REQUIRED')
    draft=state.get('draft_markdown'); draft_sha=str(state.get('draft_sha256') or '')
    if not isinstance(draft,str) or not draft or text_sha256(draft)!=draft_sha: raise BatchGateError('STATE_DRAFT_HASH_INVALID')
    if checks.get('checked_draft_sha256')!=draft_sha: raise BatchGateError('FULL_PRODUCTION_CHECK_HASH_MISMATCH')
    quality_summary=validate_full_production_evidence(checks,draft_sha)
    context=state.get('production_context')
    if not isinstance(context,dict) or set(context)!={'fact_pack','production_plan_item','sha256'}: raise BatchGateError('PRODUCTION_CONTEXT_INVALID')
    if stable_hash({'fact_pack':context['fact_pack'],'production_plan_item':context['production_plan_item']})!=context.get('sha256'): raise BatchGateError('PRODUCTION_CONTEXT_HASH_INVALID')
    research_text=_validated_stage_text(state,'research'); facts_text=_validated_stage_text(state,'facts')
    try:
        content_guard.validate_fact_pack(context['fact_pack'],research_text,facts_text)
        content_guard.validate_article_fact_ids(draft,context['fact_pack'])
    except content_guard.ContentGuardError as exc: raise BatchGateError('CONTENT_CONTEXT_NOT_PASS:'+str(exc)) from exc
    try: design_summary=design_guard.validate_design_neutrality(draft,expected_article['article_type'])
    except design_guard.DesignGuardError as exc: raise BatchGateError('DESIGN_GUARD_NOT_PASS:'+str(exc)) from exc
    return {'plan_slot':expected_article['plan_slot'],'draft':draft,'draft_sha256':draft_sha,'state_sha256':stable_hash(dict(state)),'production_context_sha256':context['sha256'],'check_evidence_sha256':stable_hash(checks),'revision':int(state.get('revision') or 0),'quality_summary':quality_summary,'design_summary':design_summary}
def collect_batch(snapshot_path:Path,state_paths:Sequence[Path],out_dir:Path):
    source_snapshot_sha,batch_sha,items=load_snapshot(Path(snapshot_path))
    if len(state_paths)!=len(items): raise BatchGateError('STATE_COUNT_MISMATCH')
    states_by_slot={}
    for path in state_paths:
        state=load_json(Path(path)); article=state.get('article'); slot=str(article.get('plan_slot') or '') if isinstance(article,dict) else ''
        if not SHA_RE.fullmatch(slot): raise BatchGateError('STATE_PLAN_SLOT_INVALID')
        if slot in states_by_slot: raise BatchGateError('STATE_PLAN_SLOT_DUPLICATE')
        states_by_slot[slot]=state
    expected_slots={item['plan_slot'] for item in items}
    if set(states_by_slot)!=expected_slots: raise BatchGateError('STATE_SET_MISMATCH')
    out_dir=Path(out_dir); out_dir.mkdir(parents=True,exist_ok=True); article_rows=[]; state_rows=[]
    for item in items:
        validated=validate_state(states_by_slot[item['plan_slot']],item,source_snapshot_sha,batch_sha); name='ARTICLE_'+item['plan_slot']+'.md'; article_path=out_dir/name; article_path.write_bytes(validated['draft'].encode('utf-8'))
        if file_sha256(article_path)!=validated['draft_sha256']: raise BatchGateError('ARTICLE_OUTPUT_BYTES_CHANGED')
        article_rows.append({'name':name,'plan_slot':item['plan_slot'],'sha256':validated['draft_sha256'],'byte_length':article_path.stat().st_size,'content_utf8':validated['draft'],'revision':validated['revision'],'quality':validated['quality_summary'],'design':validated['design_summary']})
        state_rows.append({'plan_slot':item['plan_slot'],'state_sha256':validated['state_sha256'],'production_context_sha256':validated['production_context_sha256'],'check_evidence_sha256':validated['check_evidence_sha256']})
    try: diversity=content_guard.validate_batch_distinctness([row['content_utf8'] for row in article_rows])
    except content_guard.ContentGuardError as exc: raise BatchGateError(str(exc)) from exc
    actual_article_names=sorted(path.name for path in out_dir.glob('ARTICLE_*.md') if path.is_file()); expected_article_names=sorted(row['name'] for row in article_rows)
    if actual_article_names!=expected_article_names: raise BatchGateError('ARTICLE_OUTPUT_SET_MISMATCH')
    evidence={'contract':BATCH_EVIDENCE_CONTRACT,'status':'FULL_PASS_BATCH_COLLECTED','source_snapshot_sha256':source_snapshot_sha,'batch_sha256':batch_sha,'article_count':len(article_rows),'articles':article_rows,'state_evidence':state_rows,'batch_distinctness':diversity,'publish_allowed':False,'content_mutation_performed':False,'design_mutation_performed':False,'next_required':'SIGNED_WORKFLOW_RELEASE'}
    evidence['batch_evidence_sha256']=stable_hash(evidence); evidence_path=out_dir/'system4_batch_evidence.json'; evidence_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return {'status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','batch_sha256':batch_sha,'article_count':len(article_rows),'batch_evidence_path':str(evidence_path),'batch_evidence_sha256':file_sha256(evidence_path),'next_required':'SIGNED_WORKFLOW_RELEASE','publish_allowed':False}


def main(argv):
    try:
        if len(argv) < 5 or argv[1] != 'collect':
            raise BatchGateError('USE: batch_gate.py collect SNAPSHOT OUT_DIR STATE_JSON...')
        result = collect_batch(Path(argv[2]), [Path(value) for value in argv[4:]], Path(argv[3]))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (BatchGateError, json.JSONDecodeError) as exc:
        print('SYSTEM4_BATCH_FAIL:' + str(exc))
        return 2

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
