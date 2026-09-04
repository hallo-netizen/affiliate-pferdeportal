#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, re, sys
from pathlib import Path
from typing import Any, Mapping

REPO=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve()
BRIDGE=REPO/'control/single-door-boundary/codex_current_room_bridge.py'
PROMPT_REL='control/startmaster0107/VERBINDLICHER_TEXTERSTELLUNGS_PROMPT_STARTMASTER0107.txt'
RUNTIME_STATE_REL='control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
HANDOFF_REL='control/startmaster0107/fachworkflow_proof_handoff.py'
CONTRACT='PFERDE_ATELIER_CODEX_CURRENT_ACTION_VIEW_V1'
PASS_CONTRACT='PFERDE_ATELIER_FACHWORKFLOW_PASS_V1'
ARTICLE_TYPE_TEMPLATES_SHA='dc79a6d7d30fba2f7f13c80d35bf4d137669f2b3469d7bc28a5d0873858f192f'
PPM679_VERSION='6.7.9'
PPM679_PACKAGE_SHA256='acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1'
STAGES=['research_fact_pack','textmachine_article_type_structure','table_contract','internal_links','languagetool','ppm','pserc','pste','duplicate_cannibalization','seo','design_format','publish_safety']
RELEASE_CONTRACT='WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED'
RELEASE_KEYS={'article_origin_policy','authoring_prompt_sha256','authoring_role','content_generation_performed_by_supervisor','contract','created_at_utc','exact_five_batch_sha256','exact_five_item_count','frozen_workflow_sha256','nullpunkt','nullpunkt_sha256','ppm_baseline_sha256','ppm_version','research_evidence_policy','sequence','status','wordpress_write_performed'}

class ViewError(RuntimeError):pass

def sha(p:Path)->str:return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p:Path)->dict:
    x=json.loads(Path(p).read_text(encoding='utf-8'))
    if not isinstance(x,dict):raise ViewError('JSON_OBJECT_REQUIRED')
    return x
def _safe_repo(repo:Path,ref:str)->Path:
    p=Path(str(ref or ''))
    if not str(ref or '') or p.is_absolute() or '..' in p.parts:raise ViewError('BOUND_REF_INVALID')
    q=(Path(repo)/p).resolve();r=Path(repo).resolve()
    if q!=r and r not in q.parents:raise ViewError('BOUND_REF_ESCAPE')
    return q
def safe(ref:str)->Path:return _safe_repo(REPO,ref)
def _bridge():
    s=importlib.util.spec_from_file_location('current_room_bridge_bound',BRIDGE)
    if s is None or s.loader is None:raise ViewError('BRIDGE_LOAD_FAILED')
    m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
    m.DUAL=SELF
    return m

def _rules(it:Mapping[str,Any])->dict:
    t=str(it.get('article_type') or '').strip()
    if not t:raise ViewError('ARTICLE_TYPE_BINDING_MISSING')
    return {'contract':'PFERDE_ATELIER_TEXTMACHINE_ARTICLE_TYPE_RULESET_BINDING_V1','article_type':t,'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'selection_authority':'BOUND_CURRENT_ITEM_ONLY','rule_semantics_redefined':False,'content_or_quality_rules_changed':False,'publish_allowed':False}

def _ppm_requirement()->dict:
    return {'ppm_version':PPM679_VERSION,'ppm_package_sha256':PPM679_PACKAGE_SHA256,'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'stage':'ppm','real_ppm_execution_required':True,'final_article_hash_must_equal_ppm_content_hash':True,'ppm679_binding_required_fields':['ppm_version','ppm_package_sha256','article_type_templates_sha256','final_article_ref','final_article_sha256','ppm_report_ref','ppm_report_sha256'],'technical_guard_semantics_authority':'NONE','content_or_quality_rules_changed':False,'publish_allowed':False}

def _contract_binding()->dict:
    p=REPO/PROMPT_REL
    if not p.is_file():raise ViewError('FACH_PROMPT_MISSING')
    return {'contract':'PFERDE_ATELIER_FACHWORKFLOW_CONTRACT_BINDING_V1','authority':'EXISTING_UNCHANGED_FACHWORKFLOW_ONLY','binding_ref':'control/single-door-boundary/codex_current_action.py','binding_sha256':sha(SELF),'prompt_ref':PROMPT_REL,'prompt_sha256':sha(p),'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'required_pass_stages':STAGES,'technical_guard_semantics_authority':'NONE','content_or_quality_rules_changed':False,'publish_allowed':False}

def _runtime_batch_identity()->tuple[str,int]:
    runtime=load(REPO/RUNTIME_STATE_REL);batch=str(runtime.get('batch_sha256') or '');pref=str(runtime.get('production_package_ref') or '');digest=str(runtime.get('production_package_sha256') or '')
    if not re.fullmatch(r'[0-9a-f]{64}',batch):raise ViewError('RUNTIME_BATCH_BINDING_INVALID')
    pp=safe(pref)
    if not pp.is_file() or not re.fullmatch(r'[0-9a-f]{64}',digest) or sha(pp)!=digest:raise ViewError('RUNTIME_PRODUCTION_PACKAGE_BINDING_INVALID')
    pkg=load(pp);wr=pkg.get('workflow_release');items=wr.get('items') if isinstance(wr,dict) else None
    if not isinstance(wr,dict) or not isinstance(items,list) or not items:raise ViewError('RUNTIME_PRODUCTION_PACKAGE_CONTEXT_INVALID')
    if wr.get('exact_five_batch_sha256')!=batch or int(wr.get('exact_five_item_count') or -1)!=len(items):raise ViewError('RUNTIME_PRODUCTION_PACKAGE_IDENTITY_INVALID')
    return batch,len(items)

def _validate_release_metadata_identity(rm:Mapping[str,Any],batch:str,batch_count:int)->None:
    if rm.get('exact_five_batch_sha256')!=batch:raise ViewError('RELEASE_METADATA_BATCH_MISMATCH')
    if int(rm.get('exact_five_item_count') or -1)!=batch_count:raise ViewError('RELEASE_METADATA_ITEM_COUNT_MISMATCH')

def _validate_ppm_stage(repo:Path,root:str,proof:Mapping[str,Any],receipt_outputs:Any)->None:
    binding=proof.get('ppm679_binding')
    keys={'ppm_version','ppm_package_sha256','article_type_templates_sha256','final_article_ref','final_article_sha256','ppm_report_ref','ppm_report_sha256'}
    if not isinstance(binding,dict) or set(binding)!=keys:raise ViewError('PPM679_REAL_BINDING_MISSING')
    if binding.get('ppm_version')!=PPM679_VERSION:raise ViewError('PPM679_VERSION_MISMATCH')
    if binding.get('ppm_package_sha256')!=PPM679_PACKAGE_SHA256:raise ViewError('PPM679_PACKAGE_HASH_MISMATCH')
    if binding.get('article_type_templates_sha256')!=ARTICLE_TYPE_TEMPLATES_SHA:raise ViewError('PPM679_RULESET_HASH_MISMATCH')
    final_ref=str(binding.get('final_article_ref') or '');final_sha=str(binding.get('final_article_sha256') or '')
    report_ref=str(binding.get('ppm_report_ref') or '');report_sha=str(binding.get('ppm_report_sha256') or '')
    if not final_ref.startswith(root) or not report_ref.startswith(root):raise ViewError('PPM679_REF_OUTSIDE_BOUND_ROOT')
    if not re.fullmatch(r'[0-9a-f]{64}',final_sha) or not re.fullmatch(r'[0-9a-f]{64}',report_sha):raise ViewError('PPM679_HASH_INVALID')
    final_path=_safe_repo(repo,final_ref);report_path=_safe_repo(repo,report_ref)
    if not final_path.is_file() or sha(final_path)!=final_sha:raise ViewError('PPM679_FINAL_ARTICLE_HASH_MISMATCH')
    if not report_path.is_file() or sha(report_path)!=report_sha:raise ViewError('PPM679_REPORT_HASH_MISMATCH')
    if proof.get('input_sha256')!=final_sha:raise ViewError('PPM679_STAGE_INPUT_NOT_FINAL_ARTICLE')
    arts=proof.get('artifacts')
    if not isinstance(arts,list):raise ViewError('PPM679_ARTIFACTS_MISSING')
    if not any(isinstance(x,dict) and x.get('ref')==final_ref and x.get('sha256')==final_sha for x in arts):raise ViewError('PPM679_FINAL_ARTICLE_NOT_BOUND_AS_ARTIFACT')
    if not any(isinstance(x,dict) and x.get('ref')==report_ref and x.get('sha256')==report_sha for x in arts):raise ViewError('PPM679_REPORT_NOT_BOUND_AS_ARTIFACT')
    if not isinstance(receipt_outputs,list) or not any(isinstance(x,dict) and x.get('ref')==final_ref and x.get('sha256')==final_sha for x in receipt_outputs):raise ViewError('PPM679_FINAL_ARTICLE_NOT_BOUND_AS_OUTPUT')
    report=load(report_path);checks=report.get('checks')
    if report.get('ok') is not True:raise ViewError('PPM679_NOT_PASS')
    if report.get('technical_status')!='TECHNICAL_CHECK_OK':raise ViewError('PPM679_TECHNICAL_NOT_PASS')
    if report.get('content_quality_status')!='CONTENT_QUALITY_CHECK_OK':raise ViewError('PPM679_CONTENT_QUALITY_NOT_PASS')
    if report.get('content_hash')!=final_sha:raise ViewError('PPM679_CONTENT_HASH_NOT_FINAL_ARTICLE')
    if not isinstance(checks,dict) or checks.get('content_hash')!=final_sha or checks.get('fail_closed_aggregate_status')!='PASS':raise ViewError('PPM679_FAIL_CLOSED_NOT_PASS')

# These two functions are the only callbacks the existing room bridge uses after DUAL is bound to this file.
def augment_current_action(repo:Path,a:dict,it:Mapping[str,Any])->dict:
    r=_rules(it);b=_contract_binding();batch,batch_count=_runtime_batch_identity();root=str(a['allowed_output_root']);pref=root+'FACHWORKFLOW_PASS_'+str(it['plan_slot'])+'.json'
    metadata_binding={'required_fields':sorted(RELEASE_KEYS),'contract':RELEASE_CONTRACT,'status':'PASS','exact_five_batch_sha256':batch,'exact_five_item_count':batch_count,'wordpress_write_performed':False,'remaining_fields_authority':'EXISTING_UNCHANGED_FACHWORKFLOW_ONLY','technical_identity_binding_only':True,'content_or_quality_rules_changed':False,'publish_allowed':False}
    s=dict(a.get('item_receipt_schema') or {})
    s.update({'fachworkflow_contract_binding':b,'textmachine_ruleset_binding':r,'ppm679_requirement':_ppm_requirement(),'fachworkflow_pass_ref':pref,'fachworkflow_pass_sha256':'sha256 of exact bound FACHWORKFLOW_PASS; required with PASS','fachworkflow_pass_schema':{'contract':PASS_CONTRACT,'status':'PASS','batch_sha256':batch,'canonical_article_id':it['canonical_article_id'],'plan_slot':it['plan_slot'],'article_type':r['article_type'],'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'required_stage_proofs':'exact required stage set with real artifacts and hashes','workflow_release_metadata_binding':metadata_binding,'content_or_quality_rules_changed':False,'publish_allowed':False}})
    a['item_receipt_schema']=s
    request_ref=root+'FACHWORKFLOW_HANDOFF_REQUEST.json'
    a['fachworkflow_handoff']={'contract':'PFERDE_ATELIER_FACHWORKFLOW_PROOF_HANDOFF_BINDING_V1','batch_sha256':batch,'request_ref':request_ref,'request_contract':'PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1','request_required_fields':['contract','room_token','batch_sha256','canonical_article_id','plan_slot','allowed_output_root','item_receipt_ref','fachworkflow_pass_ref','contract_binding_ref','contract_binding_sha256','stage_proofs','fact_pack','production_plan_item','production_plan_header','workflow_release_item','workflow_release_metadata'],'adapter_ref':HANDOFF_REL,'adapter_sha256':sha(REPO/HANDOFF_REL),'command':'python3 '+HANDOFF_REL+' materialize '+request_ref,'technical_guard_executes_domain_logic':False,'adapter_executes_bound_ppm_stage':True,'content_or_quality_rules_changed':False,'publish_allowed':False}
    # NEW intentionally has no existing article source. The existing fachworkflow handoff remains bound.
    a.pop('existing_article_source_binding',None)
    return a

def validate_fachworkflow_pass(repo:Path,a:Mapping[str,Any],it:Mapping[str,Any],d:Mapping[str,Any])->dict:
    r=_rules(it);schema=a.get('item_receipt_schema') or {};ref=str(d.get('fachworkflow_pass_ref') or '');digest=str(d.get('fachworkflow_pass_sha256') or '')
    if ref!=schema.get('fachworkflow_pass_ref') or not re.fullmatch(r'[0-9a-f]{64}',digest):raise ViewError('FACH_PASS_BINDING_MISSING')
    p=safe(ref)
    if not p.is_file() or sha(p)!=digest:raise ViewError('FACH_PASS_HASH_MISMATCH')
    outs=d.get('outputs')
    if not isinstance(outs,list) or not any(isinstance(x,dict) and x.get('ref')==ref and x.get('sha256')==digest for x in outs):raise ViewError('FACH_PASS_NOT_BOUND_AS_OUTPUT')
    q=load(p);batch,batch_count=_runtime_batch_identity()
    req={'contract':PASS_CONTRACT,'status':'PASS','batch_sha256':batch,'canonical_article_id':it.get('canonical_article_id'),'plan_slot':it.get('plan_slot'),'article_type':r['article_type'],'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'content_or_quality_rules_changed':False,'publish_allowed':False}
    for k,v in req.items():
        if q.get(k)!=v:raise ViewError('FACH_PASS_FIELD_MISMATCH:'+k)
    rows=q.get('required_stage_proofs')
    if not isinstance(rows,list) or len(rows)!=len(STAGES):raise ViewError('FACH_STAGE_COUNT_INVALID')
    by={}
    for x in rows:
        if not isinstance(x,dict) or set(x)!={'stage','ref','sha256'} or x['stage'] in by:raise ViewError('FACH_STAGE_ROW_INVALID')
        by[x['stage']]=x
    if set(by)!=set(STAGES):raise ViewError('FACH_STAGE_SET_INVALID')
    root=str(a['allowed_output_root'])
    for stage in STAGES:
        x=by[stage];sr=str(x['ref']);h=str(x['sha256'])
        if not sr.startswith(root) or not re.fullmatch(r'[0-9a-f]{64}',h):raise ViewError('FACH_STAGE_REF_INVALID:'+stage)
        sp=safe(sr)
        if not sp.is_file() or sha(sp)!=h:raise ViewError('FACH_STAGE_HASH_MISMATCH:'+stage)
        proof=load(sp);expected={'contract':'PFERDE_ATELIER_FACHWORKFLOW_STAGE_EXECUTION_PROOF_V1','status':'PASS','batch_sha256':batch,'canonical_article_id':it.get('canonical_article_id'),'plan_slot':it.get('plan_slot'),'article_type':r['article_type'],'article_type_templates_sha256':ARTICLE_TYPE_TEMPLATES_SHA,'stage':stage,'execution_performed':True,'content_or_quality_rules_changed':False,'publish_allowed':False}
        if any(proof.get(k)!=v for k,v in expected.items()):raise ViewError('FACH_STAGE_EXECUTION_BINDING_INVALID:'+stage)
        if not re.fullmatch(r'[0-9a-f]{64}',str(proof.get('input_sha256') or '')):raise ViewError('FACH_STAGE_INPUT_HASH_INVALID:'+stage)
        ev=proof.get('execution_evidence');arts=proof.get('artifacts')
        if not isinstance(ev,list) or not ev or not all(isinstance(v,str) and v.strip() for v in ev):raise ViewError('FACH_STAGE_EXECUTION_EVIDENCE_MISSING:'+stage)
        if not isinstance(arts,list) or not arts:raise ViewError('FACH_STAGE_ARTIFACTS_MISSING:'+stage)
        for art in arts:
            if not isinstance(art,dict) or set(art)!={'ref','sha256'}:raise ViewError('FACH_STAGE_ARTIFACT_ROW_INVALID:'+stage)
            ar=str(art['ref']);ah=str(art['sha256'])
            if not ar.startswith(root) or not re.fullmatch(r'[0-9a-f]{64}',ah):raise ViewError('FACH_STAGE_ARTIFACT_REF_INVALID:'+stage)
            ap=safe(ar)
            if not ap.is_file() or sha(ap)!=ah:raise ViewError('FACH_STAGE_ARTIFACT_HASH_MISMATCH:'+stage)
        if stage=='ppm':_validate_ppm_stage(REPO,root,proof,d.get('outputs'))
    fp=q.get('fact_pack');pi=q.get('production_plan_item');ph=q.get('production_plan_header');ri=q.get('workflow_release_item');rm=q.get('workflow_release_metadata')
    if not all(isinstance(x,dict) for x in (fp,pi,ph,ri,rm)):raise ViewError('FACH_PRODUCTION_CONTEXT_INCOMPLETE')
    if pi.get('canonical_article_id')!=it.get('canonical_article_id') or pi.get('plan_slot')!=it.get('plan_slot'):raise ViewError('PLAN_ITEM_IDENTITY_MISMATCH')
    if ri.get('canonical_article_id')!=it.get('canonical_article_id') or ri.get('plan_slot')!=it.get('plan_slot'):raise ViewError('RELEASE_ITEM_IDENTITY_MISMATCH')
    if ph.get('contract')!='production_plan_v4' or 'items' in ph:raise ViewError('PLAN_HEADER_INVALID')
    if set(rm)!=RELEASE_KEYS:
        missing=','.join(sorted(RELEASE_KEYS-set(rm)));extra=','.join(sorted(set(rm)-RELEASE_KEYS));raise ViewError('RELEASE_METADATA_FIELDS_INVALID:missing='+missing+':extra='+extra)
    if rm.get('contract')!=RELEASE_CONTRACT or rm.get('status')!='PASS' or rm.get('wordpress_write_performed') is not False:raise ViewError('RELEASE_METADATA_IDENTITY_INVALID')
    _validate_release_metadata_identity(rm,batch,batch_count)
    return q

def _current_only(data:dict)->dict:
    status=data.get('status')
    if status=='CURRENT_BOUND_ACTION_READY':
        need=('room_token','current_item','fachworkflow_authority','fachworkflow_prompt_ref','allowed_output_root','item_receipt_ref','item_receipt_schema','fachworkflow_handoff','submission_command')
        if any(k not in data for k in need):raise ViewError('CURRENT_ACTION_FIELDS_MISSING')
        pref='python3 control/single-door-boundary/codex_current_room_bridge.py submit ';sub=str(data['submission_command'])
        if not sub.startswith(pref) or sub[len(pref):]!=str(data['item_receipt_ref']):raise ViewError('CURRENT_ACTION_SUBMISSION_NOT_BOUND')
        return {'contract':CONTRACT,'status':status,'room_token':data['room_token'],'instruction':'EXECUTE_CURRENT_BOUND_ITEM_NOW','current_item':data['current_item'],'fachworkflow_authority':data['fachworkflow_authority'],'fachworkflow_prompt_ref':data['fachworkflow_prompt_ref'],'allowed_output_root':data['allowed_output_root'],'item_receipt_ref':data['item_receipt_ref'],'item_receipt_schema':data['item_receipt_schema'],'fachworkflow_handoff':data['fachworkflow_handoff'],'submission_command':'python3 control/single-door-boundary/codex_current_action.py submit '+data['item_receipt_ref'],'publish_allowed':False}
    if status in {'BLOCKED','USER_ACTION_REQUIRED','FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH'}:return {'contract':CONTRACT,'status':status,'room_token':data.get('room_token'),'error':data.get('error'),'evidence':data.get('evidence'),'outer_step':data.get('outer_step'),'publish_allowed':False}
    if data.get('ok') is False:return {'contract':CONTRACT,'status':'BLOCKED','error':data.get('error') or status or 'BOUND_BRIDGE_BLOCKED','publish_allowed':False}
    raise ViewError('BOUND_BRIDGE_STATUS_NOT_WORKER_VISIBLE')

def _run(args:list[str])->dict:
    b=_bridge()
    try:return b.current() if args==['current'] else b.submit(args[1])
    except Exception as e:
        if e.__class__.__name__ in {'Blocked','ViewError'}:return {'ok':False,'status':'BLOCKED','error':str(e),'publish_allowed':False}
        raise

def selftest()->dict:
    # View test: old article source cannot leak; the existing bound fachworkflow handoff must remain visible.
    handoff={'contract':'PFERDE_ATELIER_FACHWORKFLOW_PROOF_HANDOFF_BINDING_V1','batch_sha256':'b'*64,'request_ref':'.pferde-quarantine/test/FACHWORKFLOW_HANDOFF_REQUEST.json','request_contract':'PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1','adapter_ref':HANDOFF_REL,'adapter_sha256':'a'*64,'command':'python3 '+HANDOFF_REL+' materialize .pferde-quarantine/test/FACHWORKFLOW_HANDOFF_REQUEST.json','technical_guard_executes_domain_logic':False,'adapter_executes_bound_ppm_stage':True,'content_or_quality_rules_changed':False,'publish_allowed':False}
    sample={'status':'CURRENT_BOUND_ACTION_READY','room_token':'R_D_1_01','current_item':{'canonical_article_id':'article:test','article_type':'ratgeber'},'fachworkflow_authority':'EXISTING_UNCHANGED_BOUND_FACHWORKFLOW_ONLY','fachworkflow_prompt_ref':'bound.txt','allowed_output_root':'.pferde-quarantine/test/','item_receipt_ref':'.pferde-quarantine/test/ITEM_RECEIPT.json','item_receipt_schema':{'contract':'X'},'existing_article_source_binding':{'ref':'old.md'},'fachworkflow_handoff':handoff,'submission_command':'python3 control/single-door-boundary/codex_current_room_bridge.py submit .pferde-quarantine/test/ITEM_RECEIPT.json'}
    v=_current_only(sample)
    if 'existing_article_source_binding' in v or 'submit-request' in v['submission_command']:raise AssertionError('OLD_SOURCE_OR_SUBMIT_REQUEST_LEAK')
    if v.get('fachworkflow_handoff')!=handoff:raise AssertionError('FACHWORKFLOW_HANDOFF_NOT_EXPOSED')
    # Binding test itself is deterministic and article-type specific.
    a=augment_current_action(REPO,{'allowed_output_root':'.pferde-quarantine/test/','item_receipt_schema':{}},{'canonical_article_id':'article:test','plan_slot':'a'*64,'article_type':'ratgeber'})
    rb=a['item_receipt_schema']['textmachine_ruleset_binding'];mb=a['item_receipt_schema']['fachworkflow_pass_schema']['workflow_release_metadata_binding']
    if rb['article_type']!='ratgeber' or rb['article_type_templates_sha256']!=ARTICLE_TYPE_TEMPLATES_SHA:raise AssertionError('ARTICLE_TYPE_RULESET_BINDING_FAIL')
    if set(mb['required_fields'])!=RELEASE_KEYS or mb['exact_five_batch_sha256']!=_runtime_batch_identity()[0] or mb['exact_five_item_count']!=_runtime_batch_identity()[1]:raise AssertionError('RELEASE_METADATA_SCHEMA_BINDING_FAIL')
    live_batch,live_count=_runtime_batch_identity()
    if not re.fullmatch(r'[0-9a-f]{64}',live_batch) or live_count<1:raise AssertionError('RUNTIME_BATCH_IDENTITY_FAIL')
    good={'exact_five_batch_sha256':live_batch,'exact_five_item_count':live_count};_validate_release_metadata_identity(good,live_batch,live_count)
    for bad,label in [({'exact_five_batch_sha256':'0'*64,'exact_five_item_count':live_count},'BATCH'),({'exact_five_batch_sha256':live_batch,'exact_five_item_count':live_count+1},'COUNT')]:
        try:_validate_release_metadata_identity(bad,live_batch,live_count);raise AssertionError('RELEASE_METADATA_NEGATIVE_NOT_BLOCKED:'+label)
        except ViewError:pass
    return {'ok':True,'status':'CODEX_CURRENT_ACTION_KISS_SELFTEST_PASS','direct_single_door':True,'old_article_source_bound':False,'handoff_request_bound':True,'article_type_ruleset_bound':True,'strict_real_stage_validator':True,'release_metadata_batch_bound':True,'release_metadata_item_count_bound':True,'content_or_quality_authority':'NONE','publish_allowed':False}

def main(argv:list[str])->int:
    try:
        if argv==['selftest']:z=selftest()
        elif argv==['current']:z=_current_only(_run(argv))
        elif len(argv)==2 and argv[0]=='submit':z=_current_only(_run(argv))
        else:raise ViewError('USAGE: current | submit ITEM_RECEIPT.json | selftest')
        print(json.dumps(z,ensure_ascii=False,indent=2));return 0 if z.get('status')!='BLOCKED' else 2
    except Exception as e:
        print(json.dumps({'contract':CONTRACT,'status':'BLOCKED','error':str(e),'publish_allowed':False},ensure_ascii=False,indent=2));return 2
if __name__=='__main__':raise SystemExit(main(sys.argv[1:]))
