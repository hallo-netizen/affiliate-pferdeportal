#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, re, sys
from pathlib import Path
from typing import Any, Mapping

REPO=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve()
SELF_REL='control/single-door-boundary/codex_current_action.py'
BRIDGE=REPO/'control/single-door-boundary/codex_current_room_bridge.py'
PROMPT_REL='control/startmaster0107/VERBINDLICHER_TEXTERSTELLUNGS_PROMPT_STARTMASTER0107.txt'
RUNTIME_STATE_REL='control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
STATE_REL='control/startmaster0107/CURRENT_STATE.json'
HANDOFF_REL='control/startmaster0107/fachworkflow_proof_handoff.py'
CONTRACT='PFERDE_ATELIER_CODEX_CURRENT_ACTION_VIEW_V1'
PASS_CONTRACT='PFERDE_ATELIER_FACHWORKFLOW_PASS_V1'
AGGREGATE_CONTRACT='PFERDE_ATELIER_EXISTING_VALIDATORS_AGGREGATE_V1'
ARTICLE_TYPE_TEMPLATES_SHA='dc79a6d7d30fba2f7f13c80d35bf4d137669f2b3469d7bc28a5d0873858f192f'
PPM679_VERSION='6.7.9'
PPM679_PACKAGE_SHA256='acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1'
PSERC_PACKAGE_SHA256='77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314'
HANDOFF_REQUEST_REQUIRED_FIELDS=['contract','room_token','batch_sha256','canonical_article_id','plan_slot','allowed_output_root','item_receipt_ref','fachworkflow_pass_ref','contract_binding_ref','contract_binding_sha256','stage_proofs','fact_pack','production_plan_item','production_plan_header','workflow_release_item','workflow_release_metadata']

class ViewError(RuntimeError): pass

def sha(p:Path)->str: return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p:Path)->dict:
    x=json.loads(Path(p).read_text(encoding='utf-8'))
    if not isinstance(x,dict): raise ViewError('JSON_OBJECT_REQUIRED')
    return x

def _safe_repo(repo:Path,ref:str)->Path:
    p=Path(str(ref or ''))
    if not str(ref or '') or p.is_absolute() or '..' in p.parts: raise ViewError('BOUND_REF_INVALID')
    q=(Path(repo)/p).resolve(); r=Path(repo).resolve()
    if q!=r and r not in q.parents: raise ViewError('BOUND_REF_ESCAPE')
    return q

def safe(ref:str)->Path: return _safe_repo(REPO,ref)

def _bridge():
    s=importlib.util.spec_from_file_location('current_room_bridge_bound',BRIDGE)
    if s is None or s.loader is None: raise ViewError('BRIDGE_LOAD_FAILED')
    m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m); m.DUAL=SELF
    return m

def _assert_bound_adapters()->None:
    st=load(REPO/STATE_REL); gate=st.get('execution_gate') or {}; step_ref=str(gate.get('bundle_ref') or ''); step_path=safe(step_ref)
    if not step_path.is_file() or sha(step_path)!=gate.get('bundle_sha256'): raise ViewError('CURRENT_107007_BUNDLE_HASH_MISMATCH')
    step=load(step_path); binds={str(x.get('ref') or ''):str(x.get('sha256') or '') for x in (step.get('authorized_inputs') or []) if isinstance(x,dict)}
    for ref in (SELF_REL,HANDOFF_REL):
        p=REPO/ref
        if not p.is_file() or binds.get(ref)!=sha(p): raise ViewError('AUTHORIZED_INPUT_HASH_MISMATCH:'+ref)

def _rules(it:Mapping[str,Any])->dict:
    t=str(it.get('article_type') or '').strip()
    if not t: raise ViewError('ARTICLE_TYPE_BINDING_MISSING')
    return {'contract':'PFERDE_ATELIER_TEXTMACHINE_ARTICLE_TYPE_RULESET_BINDING_V1','article_type':t,'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'selection_authority':'BOUND_CURRENT_ITEM_ONLY','rule_semantics_redefined':False,'content_or_quality_rules_changed':False,'publish_allowed':False}

def _ppm_requirement()->dict:
    return {'ppm_version':PPM679_VERSION,'ppm_package_sha256':PPM679_PACKAGE_SHA256,'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'real_ppm_execution_required':True,'final_article_hash_must_equal_ppm_content_hash':True,'technical_guard_semantics_authority':'NONE','content_or_quality_rules_changed':False,'publish_allowed':False}

def _runtime_context()->dict:
    runtime=load(REPO/RUNTIME_STATE_REL); batch=str(runtime.get('batch_sha256') or ''); pref=str(runtime.get('production_package_ref') or ''); digest=str(runtime.get('production_package_sha256') or '')
    if runtime.get('status')!='EXECUTION_READY' or runtime.get('publish_allowed') is not False or not re.fullmatch(r'[0-9a-f]{64}',batch): raise ViewError('RUNTIME_BATCH_BINDING_INVALID')
    pp=safe(pref)
    if not pp.is_file() or not re.fullmatch(r'[0-9a-f]{64}',digest) or sha(pp)!=digest: raise ViewError('RUNTIME_PRODUCTION_PACKAGE_BINDING_INVALID')
    pkg=load(pp); wr=pkg.get('workflow_release'); items=wr.get('items') if isinstance(wr,dict) else None
    if not isinstance(wr,dict) or not isinstance(items,list) or not items: raise ViewError('RUNTIME_PRODUCTION_PACKAGE_CONTEXT_INVALID')
    if wr.get('exact_five_batch_sha256')!=batch or int(wr.get('exact_five_item_count') or -1)!=len(items): raise ViewError('RUNTIME_PRODUCTION_PACKAGE_IDENTITY_INVALID')
    sref=str(runtime.get('source_snapshot_ref') or ''); sdigest=str(runtime.get('source_snapshot_sha256') or ''); sp=safe(sref)
    if not sp.is_file() or sha(sp)!=sdigest: raise ViewError('RUNTIME_SOURCE_SNAPSHOT_BINDING_INVALID')
    snap=load(sp); mb=snap.get('next_textmachine_metadata_batch'); metas=mb.get('items') if isinstance(mb,dict) else None
    if not isinstance(mb,dict) or mb.get('batch_sha256')!=batch or not isinstance(metas,list) or len(metas)!=len(items): raise ViewError('RUNTIME_METADATA_BATCH_INVALID')
    plan=pkg.get('production_plan')
    if not isinstance(plan,dict) or plan.get('contract')!='production_plan_v4': raise ViewError('RUNTIME_PRODUCTION_PLAN_INVALID')
    header=dict(plan); header.pop('items',None); metadata=dict(wr); metadata.pop('items',None)
    return {'runtime':runtime,'batch':batch,'count':len(items),'package':pkg,'release_items':items,'meta_items':metas,'plan_header':header,'release_metadata':metadata,'source_sha256':sdigest,'package_sha256':digest}

def _runtime_batch_identity()->tuple[str,int]:
    c=_runtime_context(); return c['batch'],c['count']

def _validate_release_metadata_identity(rm:Mapping[str,Any],batch:str,batch_count:int)->None:
    if rm.get('exact_five_batch_sha256')!=batch: raise ViewError('RELEASE_METADATA_BATCH_MISMATCH')
    if int(rm.get('exact_five_item_count') or -1)!=batch_count: raise ViewError('RELEASE_METADATA_ITEM_COUNT_MISMATCH')

def _bound_expected(it:Mapping[str,Any])->dict:
    c=_runtime_context(); slot=str(it.get('plan_slot') or ''); cid=str(it.get('canonical_article_id') or '')
    metas=[x for x in c['meta_items'] if isinstance(x,dict) and str(x.get('plan_slot') or '')==slot]
    rels=[x for x in c['release_items'] if isinstance(x,dict) and str(x.get('plan_slot') or '')==slot]
    if len(metas)!=1 or len(rels)!=1: raise ViewError('BOUND_RUNTIME_ITEM_NOT_UNIQUE')
    meta=dict(metas[0]); rel=dict(rels[0])
    if rel.get('canonical_article_id')!=cid: raise ViewError('BOUND_RUNTIME_CANONICAL_ID_MISMATCH')
    for k in ('title','target_keyword','category','article_type'):
        if str(it.get(k) or '')!=str(meta.get(k) or ''): raise ViewError('CURRENT_ITEM_RUNTIME_METADATA_MISMATCH:'+k)
    return {'ctx':c,'meta':meta,'release_item':rel}

def _contract_binding()->dict:
    _assert_bound_adapters(); p=REPO/PROMPT_REL
    if not p.is_file(): raise ViewError('FACH_PROMPT_MISSING')
    return {'contract':'PFERDE_ATELIER_FACHWORKFLOW_CONTRACT_BINDING_V1','authority':'EXISTING_UNCHANGED_FACHWORKFLOW_ONLY','binding_ref':SELF_REL,'binding_sha256':sha(SELF),'prompt_ref':PROMPT_REL,'prompt_sha256':sha(p),'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'aggregate_proof_contract':AGGREGATE_CONTRACT,'worker_stage_pass_proofs_allowed':False,'technical_guard_semantics_authority':'NONE','content_or_quality_rules_changed':False,'publish_allowed':False}

def augment_current_action(repo:Path,a:dict,it:Mapping[str,Any])->dict:
    _assert_bound_adapters(); r=_rules(it); b=_contract_binding(); bound=_bound_expected(it); batch=bound['ctx']['batch']; root=str(a['allowed_output_root']); pref=root+'FACHWORKFLOW_PASS_'+str(it['plan_slot'])+'.json'
    metadata_binding={'source':'BOUND_RUNTIME_PRODUCTION_PACKAGE_ONLY','exact_five_batch_sha256':batch,'exact_five_item_count':bound['ctx']['count'],'wordpress_write_performed':False,'content_or_quality_rules_changed':False,'publish_allowed':False}
    s=dict(a.get('item_receipt_schema') or {})
    s.update({'fachworkflow_contract_binding':b,'textmachine_ruleset_binding':r,'ppm679_requirement':_ppm_requirement(),'worker_stage_proofs_required_value':[],'fachworkflow_pass_ref':pref,'fachworkflow_pass_sha256':'sha256 of exact adapter-generated FACHWORKFLOW_PASS; required with PASS','fachworkflow_pass_schema':{'contract':PASS_CONTRACT,'status':'PASS','batch_sha256':batch,'canonical_article_id':it['canonical_article_id'],'plan_slot':it['plan_slot'],'article_type':r['article_type'],'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'aggregate_check_contract':AGGREGATE_CONTRACT,'worker_stage_proofs_accepted':False,'workflow_release_metadata_binding':metadata_binding,'content_or_quality_rules_changed':False,'publish_allowed':False}})
    a['item_receipt_schema']=s; request_ref=root+'FACHWORKFLOW_HANDOFF_REQUEST.json'
    a['fachworkflow_handoff']={'contract':'PFERDE_ATELIER_FACHWORKFLOW_PROOF_HANDOFF_BINDING_V1','batch_sha256':batch,'request_ref':request_ref,'request_contract':'PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1','request_required_fields':HANDOFF_REQUEST_REQUIRED_FIELDS,'stage_proofs_required_value':[],'adapter_ref':HANDOFF_REL,'adapter_sha256':sha(REPO/HANDOFF_REL),'command':'python3 '+HANDOFF_REL+' materialize '+request_ref,'technical_guard_executes_domain_logic':False,'adapter_executes_bound_ppm_stage':True,'adapter_executes_real_languagetool':True,'worker_pass_authority':'NONE','content_or_quality_rules_changed':False,'publish_allowed':False}
    a.pop('existing_article_source_binding',None); return a

def validate_fachworkflow_pass(repo:Path,a:Mapping[str,Any],it:Mapping[str,Any],d:Mapping[str,Any])->dict:
    _assert_bound_adapters(); r=_rules(it); schema=a.get('item_receipt_schema') or {}; ref=str(d.get('fachworkflow_pass_ref') or ''); digest=str(d.get('fachworkflow_pass_sha256') or '')
    if ref!=schema.get('fachworkflow_pass_ref') or not re.fullmatch(r'[0-9a-f]{64}',digest): raise ViewError('FACH_PASS_BINDING_MISSING')
    p=safe(ref)
    if not p.is_file() or sha(p)!=digest: raise ViewError('FACH_PASS_HASH_MISMATCH')
    outs=d.get('outputs')
    if not isinstance(outs,list) or not any(isinstance(x,dict) and x.get('ref')==ref and x.get('sha256')==digest for x in outs): raise ViewError('FACH_PASS_NOT_BOUND_AS_OUTPUT')
    q=load(p); bound=_bound_expected(it); c=bound['ctx']; batch=c['batch']
    req={'contract':PASS_CONTRACT,'status':'PASS','batch_sha256':batch,'canonical_article_id':it.get('canonical_article_id'),'plan_slot':it.get('plan_slot'),'article_type':r['article_type'],'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'content_or_quality_rules_changed':False,'publish_allowed':False}
    for k,v in req.items():
        if q.get(k)!=v: raise ViewError('FACH_PASS_FIELD_MISMATCH:'+k)
    if 'required_stage_proofs' in q or 'stage_proofs' in q: raise ViewError('FOREIGN_STAGE_PASS_PROOFS_FORBIDDEN')
    if q.get('contract_binding_ref')!=SELF_REL or q.get('contract_binding_sha256')!=sha(SELF): raise ViewError('FACH_PASS_CONTRACT_BINDING_MISMATCH')
    agg=q.get('aggregate_check')
    if not isinstance(agg,dict): raise ViewError('FACH_AGGREGATE_MISSING')
    expected={'contract':AGGREGATE_CONTRACT,'status':'PASS','batch_sha256':batch,'canonical_article_id':it.get('canonical_article_id'),'plan_slot':it.get('plan_slot'),'article_type':r['article_type'],'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'runtime_source_snapshot_sha256':c['source_sha256'],'runtime_production_package_sha256':c['package_sha256'],'handoff_adapter_ref':HANDOFF_REL,'handoff_adapter_sha256':sha(REPO/HANDOFF_REL),'current_action_ref':SELF_REL,'current_action_sha256':sha(SELF),'ppm_version':PPM679_VERSION,'ppm_package_sha256':PPM679_PACKAGE_SHA256,'pserc_package_sha256':PSERC_PACKAGE_SHA256,'execution_path':'PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','worker_pass_authority':'NONE','worker_stage_proofs_accepted':False,'content_or_quality_rules_changed':False,'publish_allowed':False}
    for k,v in expected.items():
        if agg.get(k)!=v: raise ViewError('FACH_AGGREGATE_FIELD_MISMATCH:'+k)
    root=str(a['allowed_output_root']); final_ref=root+'ARTICLE_'+str(it.get('plan_slot'))+'.md'; final_sha=str(agg.get('final_article_sha256') or '')
    if agg.get('final_article_ref')!=final_ref or not re.fullmatch(r'[0-9a-f]{64}',final_sha): raise ViewError('FACH_FINAL_ARTICLE_BINDING_INVALID')
    final=safe(final_ref)
    if not final.is_file() or sha(final)!=final_sha: raise ViewError('FACH_FINAL_ARTICLE_HASH_MISMATCH')
    if not any(isinstance(x,dict) and x.get('ref')==final_ref and x.get('sha256')==final_sha for x in outs): raise ViewError('FACH_FINAL_ARTICLE_NOT_OUTPUT')
    report_ref=str(agg.get('ppm_report_ref') or ''); report_sha=str(agg.get('ppm_report_sha256') or '')
    if report_ref!=root+'PPM679_REPORT.json' or not re.fullmatch(r'[0-9a-f]{64}',report_sha): raise ViewError('FACH_PPM_REPORT_BINDING_INVALID')
    rp=safe(report_ref)
    if not rp.is_file() or sha(rp)!=report_sha: raise ViewError('FACH_PPM_REPORT_HASH_MISMATCH')
    report=load(rp); checks=report.get('checks')
    if report.get('ok') is not True or report.get('technical_status')!='TECHNICAL_CHECK_OK' or report.get('content_quality_status')!='CONTENT_QUALITY_CHECK_OK' or report.get('content_hash')!=final_sha or not isinstance(checks,dict) or checks.get('content_hash')!=final_sha or checks.get('fail_closed_aggregate_status')!='PASS': raise ViewError('FACH_PPM_REPORT_NOT_PASS')
    lt=agg.get('languagetool')
    if not isinstance(lt,dict) or lt.get('engine')!='LanguageTool 6.8 / Bestand 43' or lt.get('return_code')!=0 or lt.get('raw_finding_count')!=0 or lt.get('unresolved_finding_count')!=0: raise ViewError('FACH_LANGUAGETOOL_NOT_PASS')
    lref=str(lt.get('raw_report_ref') or ''); lsha=str(lt.get('raw_report_sha256') or '')
    if lref!=root+'LANGUAGETOOL_REPORT.json' or not re.fullmatch(r'[0-9a-f]{64}',lsha): raise ViewError('FACH_LANGUAGETOOL_REPORT_BINDING_INVALID')
    lp=safe(lref)
    if not lp.is_file() or sha(lp)!=lsha: raise ViewError('FACH_LANGUAGETOOL_REPORT_HASH_MISMATCH')
    if not any(isinstance(x,dict) and x.get('ref')==lref and x.get('sha256')==lsha for x in outs): raise ViewError('FACH_LANGUAGETOOL_REPORT_NOT_OUTPUT')
    fp=q.get('fact_pack'); pi=q.get('production_plan_item'); ph=q.get('production_plan_header'); ri=q.get('workflow_release_item'); rm=q.get('workflow_release_metadata')
    if not isinstance(fp,dict) or not fp or not isinstance(pi,dict): raise ViewError('FACH_PRODUCTION_CONTEXT_INCOMPLETE')
    meta=bound['meta']; expected_pi={'canonical_article_id':it.get('canonical_article_id'),'plan_slot':it.get('plan_slot'),'article_type':meta.get('article_type'),'target_keyword':meta.get('target_keyword'),'topic':meta.get('title')}
    for k,v in expected_pi.items():
        if pi.get(k)!=v: raise ViewError('PLAN_ITEM_IDENTITY_MISMATCH:'+k)
    if ph!=c['plan_header'] or ri!=bound['release_item'] or rm!=c['release_metadata']: raise ViewError('BOUND_RUNTIME_CONTEXT_MISMATCH')
    _validate_release_metadata_identity(rm,batch,c['count']); return q

def _current_only(data:dict)->dict:
    status=data.get('status')
    if status=='CURRENT_BOUND_ACTION_READY':
        need=('room_token','current_item','fachworkflow_authority','fachworkflow_prompt_ref','allowed_output_root','item_receipt_ref','item_receipt_schema','fachworkflow_handoff','submission_command')
        if any(k not in data for k in need): raise ViewError('CURRENT_ACTION_FIELDS_MISSING')
        pref='python3 control/single-door-boundary/codex_current_room_bridge.py submit '; sub=str(data['submission_command'])
        if not sub.startswith(pref) or sub[len(pref):]!=str(data['item_receipt_ref']): raise ViewError('CURRENT_ACTION_SUBMISSION_NOT_BOUND')
        return {'contract':CONTRACT,'status':status,'room_token':data['room_token'],'instruction':'EXECUTE_BOUND_FACHWORKFLOW_PROMPT_AS_CURRENT_WORKER_NOW','worker_role':'CURRENT_CODEX_IS_BOUND_FACHWORKFLOW_WORKER','separate_fachworkflow_executor_required':False,'separate_fachworkflow_capability_required':False,'fachworkflow_work_generation_authority':'CURRENT_CODEX_WORKER_MUST_GENERATE_REAL_CURRENT_OUTPUTS','fachworkflow_pass_authority':'HASH_BOUND_ADAPTER_PLUS_EXISTING_VALIDATORS_ONLY','current_item':data['current_item'],'fachworkflow_authority':data['fachworkflow_authority'],'fachworkflow_prompt_ref':data['fachworkflow_prompt_ref'],'allowed_output_root':data['allowed_output_root'],'item_receipt_ref':data['item_receipt_ref'],'item_receipt_schema':data['item_receipt_schema'],'fachworkflow_handoff':data['fachworkflow_handoff'],'submission_command':'python3 control/single-door-boundary/codex_current_action.py submit '+data['item_receipt_ref'],'publish_allowed':False}
    if status in {'BLOCKED','USER_ACTION_REQUIRED','FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH'}: return {'contract':CONTRACT,'status':status,'room_token':data.get('room_token'),'error':data.get('error'),'evidence':data.get('evidence'),'outer_step':data.get('outer_step'),'publish_allowed':False}
    if data.get('ok') is False: return {'contract':CONTRACT,'status':'BLOCKED','error':data.get('error') or status or 'BOUND_BRIDGE_BLOCKED','publish_allowed':False}
    raise ViewError('BOUND_BRIDGE_STATUS_NOT_WORKER_VISIBLE')

def _run(args:list[str])->dict:
    b=_bridge()
    try: return b.current() if args==['current'] else b.submit(args[1])
    except Exception as e:
        if e.__class__.__name__ in {'Blocked','ViewError'}: return {'ok':False,'status':'BLOCKED','error':str(e),'publish_allowed':False}
        raise

def selftest()->dict:
    _assert_bound_adapters(); batch,count=_runtime_batch_identity(); good={'exact_five_batch_sha256':batch,'exact_five_item_count':count}; _validate_release_metadata_identity(good,batch,count)
    negatives=0
    for bad in ({'exact_five_batch_sha256':'0'*64,'exact_five_item_count':count},{'exact_five_batch_sha256':batch,'exact_five_item_count':count+1}):
        try: _validate_release_metadata_identity(bad,batch,count)
        except ViewError: negatives+=1
        else: raise AssertionError('RELEASE_METADATA_NEGATIVE_NOT_BLOCKED')
    if negatives!=2: raise AssertionError('NEGATIVE_COUNT_INVALID')
    return {'ok':True,'status':'CODEX_CURRENT_ACTION_KISS_SELFTEST_PASS','positive':1,'negative':negatives,'direct_single_door':True,'current_codex_is_bound_fachworkflow_worker':True,'separate_fachworkflow_executor_required':False,'separate_fachworkflow_capability_required':False,'worker_generates_real_current_fachworkflow_outputs':True,'worker_does_not_self_attest_pass':True,'worker_stage_pass_proofs_allowed':False,'aggregate_pass_authority':'HASH_BOUND_ADAPTER_PLUS_EXISTING_VALIDATORS_ONLY','article_type_ruleset_bound':True,'release_metadata_batch_bound':True,'release_metadata_item_count_bound':True,'content_or_quality_authority':'NONE','publish_allowed':False}

def main(argv:list[str])->int:
    try:
        if argv==['selftest']: z=selftest()
        elif argv==['current']: z=_current_only(_run(argv))
        elif len(argv)==2 and argv[0]=='submit': z=_current_only(_run(argv))
        else: raise ViewError('USAGE: current | submit ITEM_RECEIPT.json | selftest')
        print(json.dumps(z,ensure_ascii=False,indent=2)); return 0 if z.get('status')!='BLOCKED' else 2
    except Exception as e:
        print(json.dumps({'contract':CONTRACT,'status':'BLOCKED','error':str(e),'publish_allowed':False},ensure_ascii=False,indent=2)); return 2
if __name__=='__main__': raise SystemExit(main(sys.argv[1:]))
