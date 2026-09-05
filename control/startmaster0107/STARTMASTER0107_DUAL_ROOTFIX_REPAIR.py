#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, importlib.util, json, os, re, shlex, subprocess, sys, tempfile, shutil
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Mapping

REPO=Path(__file__).resolve().parents[2]
SELF_REL='control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py'
BRIDGE_REL='control/single-door-boundary/codex_current_room_bridge.py'
CURRENT_ACTION_REL='control/single-door-boundary/codex_current_action.py'
HANDOFF_REL='control/startmaster0107/fachworkflow_proof_handoff.py'
ENTRY_REL='control/output-quarantine/runtime_entry_gate.py'
STEP7_REL='control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json'
STEP8_REL='control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json'
STATE_REL='control/startmaster0107/CURRENT_STATE.json'
ROOT_REL='control/startmaster0107/PFERDE_ATELIER_START_HERE.json'
PTR_REL='control/CURRENT_STARTMASTER.json'
PROMPT_REL='control/startmaster0107/VERBINDLICHER_TEXTERSTELLUNGS_PROMPT_STARTMASTER0107.txt'
RUNTIME_STATE_REL='control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
PASS_CONTRACT='PFERDE_ATELIER_FACHWORKFLOW_PASS_V1'
PACKAGE_CONTRACT='PSERC_APPROVED_PRODUCTION_PACKAGE_V1'
INTERNAL_RELEASE_CONTRACT='WORKFLOW_SUPERVISOR_RELEASE_V2_HASH_BOUND'
EXTERNAL_RELEASE_CONTRACT='WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED'
PROD_KEY_ID='workflow-ed25519-8f521756284cb375'
PROD_KEY_SHA='8f521756284cb375c907f508dac333f51b71b515419ee271ca68fa149db66f87'
PROD_PUBLIC_B64='6FCxYycU2bJysJFvtH5xZ0ia+k59ZLyK6Av8d9/ujm0='
CONTRACT_HASHES={'article_type_templates':'dc79a6d7d30fba2f7f13c80d35bf4d137669f2b3469d7bc28a5d0873858f192f','content_structure_language_gate':'756f71aa98e683b050b37fab228463569219f558729525c33c0ee0ae190e1d72','content_vault_manifest':'8dc851e01fbea1a363f3d0c52d3a348d2e608659825c9d2d1939210e7ae902de','diagnostic_contract':'13ac9764abb6c23a39a57e52fe3b217344d9ca3b6aaef96632841af3b402adf3','gold_core_binding':'68a4cd33b7b6fab7e2830f056d2e46e1952c91fecf65dfda9dd73abef09a1f92','known_error_gate':'95d499bba933a6951d72739ceac21ba669ce4a329f387df12b61722bb3742ea0','live_state_gate':'32cd3de202524a8da81ab3ecb23d97b30a945ae663800515c344bda0e94d486d','production_plan':'c6d4f816218b283eb37977ae340ffb5d345f723ab772f5cc1a355fb4b27682eb','table_contract':'1ab3e892c37e5a48517519afcccbf8ec01b9f08da141eef93d577acd456756c7'}
STAGES=['research_fact_pack','textmachine_article_type_structure','table_contract','internal_links','languagetool','ppm','pserc','pste','duplicate_cannibalization','seo','design_format','publish_safety']
PACKAGE_KEYS={'contract','fact_pack_bundle_sha256','production_plan_sha256','workflow_release_sha256','package_id','source','fact_pack_bundle','production_plan','workflow_release','package_payload_sha256'}
RELEASE_KEYS={'article_origin_policy','authoring_prompt_sha256','authoring_role','content_generation_performed_by_supervisor','contract','created_at_utc','exact_five_batch_sha256','exact_five_item_count','fact_pack_bundle_sha256','frozen_workflow_sha256','items','nullpunkt','nullpunkt_sha256','ppm_baseline_sha256','ppm_version','production_plan_sha256','release_payload_sha256','release_sha256','research_evidence_policy','sequence','signature_algorithm','signature_b64','signing_key_id','signing_public_key_sha256','status','wordpress_write_performed'}
RELEASE_META_KEYS=RELEASE_KEYS-{'fact_pack_bundle_sha256','items','production_plan_sha256','release_payload_sha256','release_sha256','signature_algorithm','signature_b64','signing_key_id','signing_public_key_sha256'}

class Blocked(RuntimeError): pass

def canonical(obj:Any)->bytes:return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def stable(obj:Any)->str:return hashlib.sha256(canonical(obj)).hexdigest()
def fsha(p:Path)->str:return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p:Path)->dict:
    x=json.loads(Path(p).read_text(encoding='utf-8'))
    if not isinstance(x,dict):raise Blocked('JSON_OBJECT_REQUIRED:'+str(p))
    return x
def dump(p:Path,x:dict):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def safe(repo:Path,ref:str)->Path:
    p=Path(str(ref or ''))
    if not str(ref or '') or p.is_absolute() or '..' in p.parts:raise Blocked('INVALID_RELATIVE_REF')
    q=(repo/p).resolve();r=repo.resolve()
    if q!=r and r not in q.parents:raise Blocked('REF_ESCAPE')
    return q
def module(p:Path,n:str):
    s=importlib.util.spec_from_file_location(n,p)
    if s is None or s.loader is None:raise Blocked('MODULE_LOAD_FAILED:'+p.name)
    m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
def repl(text:str,old:str,new:str,label:str)->str:
    n=text.count(old)
    if label=='ENTRY_FINALIZER' and 'pserc_finalization = finalizer.finalize_after_107008' in text:return text
    if label=='PREPARED_107007_PERSIST' and 'dual.persist_prepared_binding(REPO, binding)' in text:return text
    if label=='PREPARED_107008_CLEAR' and 'finalizer.clear_prepared_binding(REPO, binding["batch_sha256"])' in text:return text
    if n==0 and new in text:return text
    if n!=1:raise Blocked(label+':MATCHES='+str(n))
    return text.replace(old,new,1)

def binding_sha(repo:Path)->str:return fsha(repo/SELF_REL)
def binding_descriptor(repo:Path)->dict:
    p=repo/PROMPT_REL
    if not p.is_file():raise Blocked('FACH_PROMPT_MISSING')
    return {'contract':'PFERDE_ATELIER_FACHWORKFLOW_CONTRACT_BINDING_V1','authority':'EXISTING_UNCHANGED_FACHWORKFLOW_ONLY','binding_ref':SELF_REL,'binding_sha256':binding_sha(repo),'prompt_ref':PROMPT_REL,'prompt_sha256':fsha(p),'contract_hashes':CONTRACT_HASHES,'required_pass_stages':STAGES,'rule_semantics_redefined':False,'technical_guard_semantics_authority':'NONE','content_or_quality_rules_changed':False,'publish_allowed':False}

def prepared_binding_sidecar(repo:Path,batch:str)->Path:
    if not re.fullmatch(r'[0-9a-f]{64}',str(batch or '')):raise Blocked('PREPARED_BINDING_BATCH_INVALID')
    return repo/'.pferde-release-staging'/batch/'BOUND_PREPARED_RELEASE_REF.json'

def validate_prepared_binding_payload(repo:Path,b:Mapping[str,Any])->dict:
    required={'contract','prepared_ref','prepared_sha256','batch_sha256'}
    if not isinstance(b,Mapping) or set(b)!=required:raise Blocked('PREPARED_BINDING_FIELDS_INVALID')
    if b.get('contract')!='PFERDE_ATELIER_BOUND_PREPARED_RELEASE_FOR_FINAL_REVIEW_V1':raise Blocked('PREPARED_BINDING_CONTRACT_INVALID')
    batch=str(b.get('batch_sha256') or '');ref=str(b.get('prepared_ref') or '');h=str(b.get('prepared_sha256') or '')
    if not re.fullmatch(r'[0-9a-f]{64}',batch) or not re.fullmatch(r'[0-9a-f]{64}',h):raise Blocked('PREPARED_BINDING_HASH_INVALID')
    if not ref.startswith(f'.pferde-release-staging/{batch}/'):raise Blocked('PREPARED_BINDING_REF_OUTSIDE_BATCH')
    pp=safe(repo,ref)
    if not pp.is_file() or fsha(pp)!=h:raise Blocked('PREPARED_BINDING_PREPARED_HASH_MISMATCH')
    q=load(pp)
    if q.get('contract')!='PFERDE_ATELIER_PREPARED_OUTPUT_RELEASE_V1' or q.get('status')!='PREPARED_NOT_VISIBLE' or q.get('batch_sha256')!=batch or q.get('publish_allowed') is not False:raise Blocked('PREPARED_BINDING_PREPARED_INVALID')
    return dict(b)

def persist_prepared_binding(repo:Path,b:Mapping[str,Any])->dict:
    z=validate_prepared_binding_payload(repo,b);p=prepared_binding_sidecar(repo,z['batch_sha256']);dump(p,z)
    return {'ok':True,'status':'PREPARED_BINDING_PERSISTED','ref':str(p.relative_to(repo)),'sha256':fsha(p),'publish_allowed':False}

def restore_prepared_binding(repo:Path)->dict:
    rs=repo/RUNTIME_STATE_REL
    if not rs.is_file():raise Blocked('RUNTIME_STATE_MISSING_FOR_PREPARED_BINDING')
    batch=str(load(rs).get('batch_sha256') or '');p=prepared_binding_sidecar(repo,batch)
    if not p.is_file():raise Blocked('DURABLE_PREPARED_BINDING_MISSING')
    z=validate_prepared_binding_payload(repo,load(p));cap=repo/'.pferde-capsule'
    if not cap.is_dir():raise Blocked('CAPSULE_MISSING_FOR_PREPARED_BINDING_RESTORE')
    dst=cap/'BOUND_PREPARED_RELEASE_REF.json';dump(dst,z);dst.chmod(0o444)
    return {'ok':True,'status':'PREPARED_BINDING_RESTORED','ref':str(dst.relative_to(repo)),'sha256':fsha(dst),'batch_sha256':batch,'publish_allowed':False}

def clear_prepared_binding(repo:Path,batch:str)->dict:
    p=prepared_binding_sidecar(repo,batch)
    if p.exists():p.unlink()
    return {'ok':True,'status':'PREPARED_BINDING_CLEARED','batch_sha256':batch,'publish_allowed':False}

def existing_article_source_binding(repo:Path,it:Mapping[str,Any])->dict|None:
    sp=repo/RUNTIME_STATE_REL
    if not sp.is_file():return None
    st=load(sp);batch=str(st.get('batch_sha256') or '');slot=str(it.get('plan_slot') or '')
    if not re.fullmatch(r'[0-9a-f]{64}',batch) or not re.fullmatch(r'[0-9a-f]{64}',slot):return None
    refs=[f'.pferde-release/{batch}/ARTICLE_{slot}.md',f'control/startmaster0107/recovery_sources/{batch}/ARTICLE_{slot}.md']
    for ref in refs:
        p=safe(repo,ref)
        if p.is_file():
            return {'contract':'PFERDE_ATELIER_EXISTING_ARTICLE_SOURCE_BINDING_V1','ref':ref,'sha256':fsha(p),'canonical_article_id':str(it.get('canonical_article_id') or ''),'plan_slot':slot,'usage':'PRESERVE_EXISTING_PROSE_CORRECT_ONLY_BOUND_FACHWORKFLOW_GAPS','optional_for_new_article_generation':True,'content_or_quality_rules_changed':False,'publish_allowed':False}
    return None

def validate_existing_article_source_binding(repo:Path,a:Mapping[str,Any],it:Mapping[str,Any])->None:
    src=a.get('existing_article_source_binding')
    if src is None:return
    if not isinstance(src,dict) or src.get('contract')!='PFERDE_ATELIER_EXISTING_ARTICLE_SOURCE_BINDING_V1':raise Blocked('EXISTING_ARTICLE_SOURCE_BINDING_INVALID')
    if src.get('canonical_article_id')!=it.get('canonical_article_id') or src.get('plan_slot')!=it.get('plan_slot'):raise Blocked('EXISTING_ARTICLE_SOURCE_IDENTITY_MISMATCH')
    ref=str(src.get('ref') or '');h=str(src.get('sha256') or '');p=safe(repo,ref)
    if not p.is_file() or len(h)!=64 or fsha(p)!=h:raise Blocked('EXISTING_ARTICLE_SOURCE_HASH_MISMATCH')
    if src.get('optional_for_new_article_generation') is not True or src.get('content_or_quality_rules_changed') is not False or src.get('publish_allowed') is not False:raise Blocked('EXISTING_ARTICLE_SOURCE_POLICY_INVALID')

def augment_current_action(repo:Path,a:dict,it:Mapping[str,Any])->dict:
    b=binding_descriptor(repo);root=str(a['allowed_output_root']);pref=root+'FACHWORKFLOW_PASS_'+str(it['plan_slot'])+'.json'
    runtime=load(repo/RUNTIME_STATE_REL);batch=str(runtime.get('batch_sha256') or '')
    if not re.fullmatch(r'[0-9a-f]{64}',batch):raise Blocked('FACH_HANDOFF_BATCH_INVALID')
    s=dict(a.get('item_receipt_schema') or {})
    s.update({'fachworkflow_contract_binding':b,'fachworkflow_pass_ref':pref,'fachworkflow_pass_sha256':'sha256 of exact FACHWORKFLOW_PASS.json; required with PASS','fachworkflow_pass_schema':{'contract':PASS_CONTRACT,'status':'PASS','canonical_article_id':it['canonical_article_id'],'plan_slot':it['plan_slot'],'contract_binding_ref':SELF_REL,'contract_binding_sha256':b['binding_sha256'],'required_stage_proofs':'exactly one {stage,ref,sha256} for each required_pass_stages entry; refs under allowed_output_root','fact_pack':'existing Fachworkflow fact-pack object','production_plan_item':'existing production_plan_v4 item','production_plan_header':'existing production_plan_v4 top-level fields except items','workflow_release_item':'existing current supervisor-release item','workflow_release_metadata':'exact current PSERC release metadata excluding dynamic hashes/signature/items','content_or_quality_rules_changed':False,'publish_allowed':False}})
    request_ref=root+'FACHWORKFLOW_HANDOFF_REQUEST.json'
    s['fachworkflow_pass_schema']['batch_sha256']='current bound runtime batch_sha256'
    s['fachworkflow_pass_schema']['required_stage_proofs']='exactly one real-execution proof for every required stage; identity, execution evidence and artifact hashes are verified'
    a['item_receipt_schema']=s
    a['fachworkflow_handoff']={'contract':'PFERDE_ATELIER_FACHWORKFLOW_PROOF_HANDOFF_BINDING_V1','batch_sha256':batch,'request_ref':request_ref,'request_contract':'PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1','adapter_ref':HANDOFF_REL,'adapter_sha256':fsha(repo/HANDOFF_REL),'command':'python3 '+HANDOFF_REL+' materialize '+request_ref,'executes_domain_logic':False,'accepts_only_real_stage_execution_proofs':True,'content_or_quality_rules_changed':False,'publish_allowed':False}
    src=existing_article_source_binding(repo,it)
    if src is not None:a['existing_article_source_binding']=src
    return a

def validate_fachworkflow_pass(repo:Path,a:Mapping[str,Any],it:Mapping[str,Any],d:Mapping[str,Any])->dict:
    validate_existing_article_source_binding(repo,a,it)
    b=binding_descriptor(repo);schema=a.get('item_receipt_schema') or {};expected=schema.get('fachworkflow_pass_ref')
    ref=d.get('fachworkflow_pass_ref');digest=d.get('fachworkflow_pass_sha256')
    if ref!=expected or not isinstance(digest,str) or len(digest)!=64:raise Blocked('FACH_PASS_BINDING_MISSING')
    p=safe(repo,str(ref))
    if not p.is_file() or fsha(p)!=digest:raise Blocked('FACH_PASS_HASH_MISMATCH')
    outs=d.get('outputs')
    if not isinstance(outs,list) or not any(isinstance(x,dict) and x.get('ref')==ref and x.get('sha256')==digest for x in outs):raise Blocked('FACH_PASS_NOT_BOUND_AS_OUTPUT')
    q=load(p)
    req={'contract':PASS_CONTRACT,'status':'PASS','canonical_article_id':it.get('canonical_article_id'),'plan_slot':it.get('plan_slot'),'contract_binding_ref':SELF_REL,'contract_binding_sha256':b['binding_sha256'],'content_or_quality_rules_changed':False,'publish_allowed':False}
    for k,v in req.items():
        if q.get(k)!=v:raise Blocked('FACH_PASS_FIELD_MISMATCH:'+k)
    rows=q.get('required_stage_proofs')
    if not isinstance(rows,list) or len(rows)!=len(STAGES):raise Blocked('FACH_STAGE_COUNT_INVALID')
    by={}
    for x in rows:
        if not isinstance(x,dict) or set(x)!={'stage','ref','sha256'} or x['stage'] in by:raise Blocked('FACH_STAGE_ROW_INVALID')
        by[x['stage']]=x
    if set(by)!=set(STAGES):raise Blocked('FACH_STAGE_SET_INVALID')
    runtime=load(repo/RUNTIME_STATE_REL);batch=str(runtime.get('batch_sha256') or '')
    if q.get('batch_sha256')!=batch:raise Blocked('FACH_PASS_BATCH_MISMATCH')
    root=str(a['allowed_output_root'])
    for stage in STAGES:
        x=by[stage];ref2=str(x['ref']);h=str(x['sha256'])
        if not ref2.startswith(root) or len(h)!=64:raise Blocked('FACH_STAGE_REF_INVALID:'+stage)
        sp=safe(repo,ref2)
        if not sp.is_file() or fsha(sp)!=h:raise Blocked('FACH_STAGE_HASH_MISMATCH:'+stage)
        proof=load(sp);expected={'contract':'PFERDE_ATELIER_FACHWORKFLOW_STAGE_EXECUTION_PROOF_V1','status':'PASS','batch_sha256':batch,'canonical_article_id':it.get('canonical_article_id'),'plan_slot':it.get('plan_slot'),'stage':stage,'execution_performed':True,'content_or_quality_rules_changed':False,'publish_allowed':False}
        if any(proof.get(k)!=v for k,v in expected.items()):raise Blocked('FACH_STAGE_EXECUTION_BINDING_INVALID:'+stage)
        if not re.fullmatch(r'[0-9a-f]{64}',str(proof.get('input_sha256') or '')):raise Blocked('FACH_STAGE_INPUT_HASH_INVALID:'+stage)
        evidence=proof.get('execution_evidence');artifacts=proof.get('artifacts')
        if not isinstance(evidence,list) or not evidence or not all(isinstance(v,str) and v.strip() for v in evidence):raise Blocked('FACH_STAGE_EXECUTION_EVIDENCE_MISSING:'+stage)
        if not isinstance(artifacts,list) or not artifacts:raise Blocked('FACH_STAGE_ARTIFACTS_MISSING:'+stage)
        for artifact in artifacts:
            if not isinstance(artifact,dict) or set(artifact)!={'ref','sha256'}:raise Blocked('FACH_STAGE_ARTIFACT_ROW_INVALID:'+stage)
            aref=str(artifact['ref']);ah=str(artifact['sha256'])
            if not aref.startswith(root) or not re.fullmatch(r'[0-9a-f]{64}',ah):raise Blocked('FACH_STAGE_ARTIFACT_REF_INVALID:'+stage)
            ap=safe(repo,aref)
            if not ap.is_file() or fsha(ap)!=ah:raise Blocked('FACH_STAGE_ARTIFACT_HASH_MISMATCH:'+stage)
    fp=q.get('fact_pack');pi=q.get('production_plan_item');ph=q.get('production_plan_header');ri=q.get('workflow_release_item');rm=q.get('workflow_release_metadata')
    if not all(isinstance(x,dict) for x in (fp,pi,ph,ri,rm)):raise Blocked('FACH_PRODUCTION_CONTEXT_INCOMPLETE')
    if pi.get('canonical_article_id')!=it.get('canonical_article_id') or pi.get('plan_slot')!=it.get('plan_slot'):raise Blocked('PLAN_ITEM_IDENTITY_MISMATCH')
    if ri.get('canonical_article_id')!=it.get('canonical_article_id') or ri.get('plan_slot')!=it.get('plan_slot'):raise Blocked('RELEASE_ITEM_IDENTITY_MISMATCH')
    if ph.get('contract')!='production_plan_v4' or 'items' in ph:raise Blocked('PLAN_HEADER_INVALID')
    if set(rm)!=RELEASE_META_KEYS or rm.get('contract')!=INTERNAL_RELEASE_CONTRACT or rm.get('status')!='PASS' or rm.get('wordpress_write_performed') is not False:raise Blocked('RELEASE_METADATA_INVALID')
    return q

def call_signer(payload_sha:str,cmd:str,key_id:str,key_sha:str)->str:
    req={'contract':'PSERC_SIGN_REQUEST_V1','signature_algorithm':'ED25519','signing_key_id':key_id,'signing_public_key_sha256':key_sha,'payload_sha256':payload_sha}
    p=subprocess.run(shlex.split(cmd),input=json.dumps(req,separators=(',',':'))+'\n',text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise Blocked('HOST_SIGNER_FAILED:'+(p.stderr or p.stdout).strip()[:240])
    raw=(p.stdout or '').strip()
    try:
        o=json.loads(raw);sig=str(o.get('signature_b64') or '')
        if o.get('signing_key_id',key_id)!=key_id or o.get('signing_public_key_sha256',key_sha)!=key_sha:raise Blocked('HOST_SIGNER_IDENTITY_MISMATCH')
    except json.JSONDecodeError:sig=raw
    try:b=base64.b64decode(sig,validate=True)
    except Exception as e:raise Blocked('HOST_SIGNER_ENCODING_INVALID') from e
    if len(b)!=64:raise Blocked('HOST_SIGNER_LENGTH_INVALID')
    return sig

def build_package(ctx:Mapping[str,Any],signer:Callable[[str],str],key_id:str,key_sha:str,pub_b64:str,production:bool)->dict:
    if production and (key_id!=PROD_KEY_ID or key_sha!=PROD_KEY_SHA or pub_b64!=PROD_PUBLIC_B64):raise Blocked('TEST_SIGNER_FORBIDDEN_IN_PRODUCTION')
    bundle=ctx.get('fact_pack_bundle');plan=ctx.get('production_plan');meta=ctx.get('workflow_release_metadata');items=ctx.get('workflow_release_items')
    if not isinstance(bundle,dict) or not isinstance(plan,dict) or not isinstance(meta,dict) or not isinstance(items,list) or not items:raise Blocked('FINAL_CONTEXT_INCOMPLETE')
    if bundle.get('contract')!='canonical_fact_pack_import_v1' or plan.get('contract')!='production_plan_v4' or set(meta)!=RELEASE_META_KEYS:raise Blocked('FINAL_CONTEXT_SCHEMA_INVALID')
    bh=stable(bundle);ph=stable(plan);rel=dict(meta);rel['contract']=EXTERNAL_RELEASE_CONTRACT;rel.update({'fact_pack_bundle_sha256':bh,'items':items,'production_plan_sha256':ph,'signature_algorithm':'ED25519','signing_key_id':key_id,'signing_public_key_sha256':key_sha})
    payload=stable(rel);rel['release_payload_sha256']=payload;rel['signature_b64']=signer(payload);rel['release_sha256']=stable(rel)
    if set(rel)!=RELEASE_KEYS:raise Blocked('FINAL_RELEASE_SCHEMA_INVALID')
    rh=stable(rel);pkg={'contract':PACKAGE_CONTRACT,'fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'workflow_release_sha256':rh,'package_id':stable({'contract':PACKAGE_CONTRACT,'fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'workflow_release_sha256':rh}),'source':str(ctx.get('source') or 'STARTMASTER0107_107008_RELEASE_FINALIZER'),'fact_pack_bundle':bundle,'production_plan':plan,'workflow_release':rel};pkg['package_payload_sha256']=stable(pkg)
    if set(pkg)!=PACKAGE_KEYS:raise Blocked('FINAL_PACKAGE_SCHEMA_INVALID')
    return pkg

def verify_package(repo:Path,p:Path,trusted=None):
    h=module(repo/'control/single-door-boundary/single_door_preproduction_handoff.py','dual_h7_verify')
    return h.validate_production_package(p,trusted_keys=trusted) if trusted is not None else h.validate_production_package(p)

def context_from_release(repo:Path,receipt_ref:str)->dict:
    r=load(safe(repo,receipt_ref))
    if r.get('contract')!='PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2' or r.get('status')!='OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED' or r.get('publish_allowed') is not False:raise Blocked('FINAL_RELEASE_RECEIPT_INVALID')
    passes=[]
    for x in r.get('outputs') or []:
        if not isinstance(x,dict):raise Blocked('RELEASE_OUTPUT_ROW_INVALID')
        ref=str(x.get('released_ref') or '');p=safe(repo,ref)
        if not p.is_file() or fsha(p)!=x.get('sha256'):raise Blocked('RELEASE_OUTPUT_HASH_MISMATCH')
        if p.name=='FACHWORKFLOW_PASS.json' or p.name.startswith('FACHWORKFLOW_PASS_') or p.name.endswith('_FACHWORKFLOW_PASS.json'):passes.append(load(p))
    if not passes:raise Blocked('FINAL_FACHWORKFLOW_CONTEXT_NOT_RELEASED')
    headers=[x['production_plan_header'] for x in passes];metas=[x['workflow_release_metadata'] for x in passes]
    if any(x!=headers[0] for x in headers[1:]) or any(x!=metas[0] for x in metas[1:]):raise Blocked('FINAL_CONTEXT_HEADER_DRIFT')
    meta=metas[0]
    if meta.get('exact_five_batch_sha256')!=r.get('batch_sha256') or int(meta.get('exact_five_item_count') or -1)!=len(passes):raise Blocked('FINAL_CONTEXT_BATCH_MISMATCH')
    plan=dict(headers[0]);plan['items']=[x['production_plan_item'] for x in passes]
    bundle={'contract':'canonical_fact_pack_import_v1','created_at':meta['created_at_utc'],'fact_packs':[x['fact_pack'] for x in passes]}
    return {'source':'STARTMASTER0107_107008_RELEASE_FINALIZER','fact_pack_bundle':bundle,'production_plan':plan,'workflow_release_metadata':meta,'workflow_release_items':[x['workflow_release_item'] for x in passes]}

def resolve_signer_cmd()->str:
    direct=os.environ.get('PSERC_SIGNER_CMD','').strip()
    if direct:return direct
    found=[]
    for k,v in os.environ.items():
        value=str(v or '').strip()
        if k!='PSERC_SIGNER_CMD' and k.endswith('_SIGNER_CMD') and value:
            found.append(value)
    unique=[]
    for value in found:
        if value not in unique:unique.append(value)
    if len(unique)==1:
        os.environ['PSERC_SIGNER_CMD']=unique[0]
        return unique[0]
    if len(unique)>1:raise Blocked('HOST_SIDE_WORKFLOW_SUPERVISOR_SIGNER_ACCESS_AMBIGUOUS')
    raise Blocked('HOST_SIDE_WORKFLOW_SUPERVISOR_SIGNER_ACCESS_MISSING')

def finalize_after_107008(repo:Path,receipt_ref:str)->dict:
    repo=Path(repo).resolve();r=load(safe(repo,receipt_ref));batch=str(r.get('batch_sha256') or '');outdir=repo/'.pferde-release'/batch;outdir.mkdir(parents=True,exist_ok=True);status=outdir/'PSERC_FINALIZATION_STATUS.json'
    try:
        ctx=context_from_release(repo,receipt_ref);cmd=resolve_signer_cmd()
        pkg=build_package(ctx,lambda h:call_signer(h,cmd,PROD_KEY_ID,PROD_KEY_SHA),PROD_KEY_ID,PROD_KEY_SHA,PROD_PUBLIC_B64,True)
        out=outdir/'GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json';dump(out,pkg);verify_package(repo,out)
        gate=module(repo/'control/startmaster0107/production-package-release/production_package_release_gate.py','dual_release_gate');gate.validate_package(out,repo,True)
        z={'ok':True,'status':'PSERC_FINAL_PACKAGE_PASS','package_ref':str(out.relative_to(repo)),'package_sha256':fsha(out),'package_id':pkg['package_id'],'publish_allowed':False}
    except Exception as e:z={'ok':False,'status':'PSERC_FINAL_PACKAGE_BLOCKED','reason':str(e),'publish_allowed':False}
    dump(status,z);return z

def patch_current_action(repo:Path):
    p=repo/CURRENT_ACTION_REL;t=p.read_text(encoding='utf-8')
    t=repl(t,'            "item_receipt_schema": data["item_receipt_schema"],\n            "submission_command":','            "item_receipt_schema": data["item_receipt_schema"],\n            "existing_article_source_binding": data.get("existing_article_source_binding"),\n            "submission_command":','CURRENT_ACTION_SOURCE_PROPAGATION')
    t=repl(t,'        "item_receipt_schema": {"contract": "X"},\n        "submission_command":','        "item_receipt_schema": {"contract": "X"},\n        "existing_article_source_binding": {"contract": "PFERDE_ATELIER_EXISTING_ARTICLE_SOURCE_BINDING_V1", "ref": "control/startmaster0107/recovery_sources/test/ARTICLE_test.md", "sha256": "a" * 64},\n        "submission_command":','CURRENT_ACTION_SELFTEST_SAMPLE')
    t=repl(t,'    if view.get("publish_allowed") is not False:\n        raise AssertionError("PUBLISH_NOT_BLOCKED")\n    return {','    if view.get("publish_allowed") is not False:\n        raise AssertionError("PUBLISH_NOT_BLOCKED")\n    if view.get("existing_article_source_binding") != sample["existing_article_source_binding"]:\n        raise AssertionError("EXISTING_ARTICLE_SOURCE_NOT_PROPAGATED")\n    sample_without = dict(sample); sample_without.pop("existing_article_source_binding")\n    view_without = _current_only(sample_without)\n    if view_without.get("existing_article_source_binding") is not None:\n        raise AssertionError("EXISTING_ARTICLE_SOURCE_NOT_OPTIONAL")\n    return {','CURRENT_ACTION_SELFTEST_ASSERT')
    p.write_text(t,encoding='utf-8')

def patch_bridge(repo:Path):
    p=repo/BRIDGE_REL;t=p.read_text(encoding='utf-8')
    t=repl(t,"RUNTIME_ENTRY=REPO/'control/output-quarantine/runtime_entry_gate.py'\nFACH=","RUNTIME_ENTRY=REPO/'control/output-quarantine/runtime_entry_gate.py'\nDUAL=REPO/'control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py'\nFACH=",'BRIDGE_DUAL_CONST')
    if 'dual_rootfix_action' not in t:
        pat=re.compile(r"def action\(s,it\):\n(.*?)\ndef check_item_receipt\(d,s,it,verify=True\):",re.S);m=pat.search(t)
        if not m:raise Blocked('BRIDGE_ACTION_NOT_FOUND')
        old=m.group(0);body=m.group(1);ret='return {'
        i=body.find(ret)
        if i<0:raise Blocked('BRIDGE_ACTION_RETURN_NOT_FOUND')
        prefix=body[:i];expr=body[i+len('return '):]
        new="def action(s,it):\n"+prefix+"base="+expr+"\n    return mod(DUAL,'dual_rootfix_action').augment_current_action(REPO,base,it)\ndef check_item_receipt(d,s,it,verify=True):"
        t=t.replace(old,new,1)
    old="keys={'contract','room_token','canonical_article_id','plan_slot','status','workflow_pass','navigation_decision','state_write_requested','workflow_change_requested','content_or_quality_rules_changed','outputs','evidence'}"
    new="keys={'contract','room_token','canonical_article_id','plan_slot','status','workflow_pass','navigation_decision','state_write_requested','workflow_change_requested','content_or_quality_rules_changed','outputs','evidence','fachworkflow_pass_ref','fachworkflow_pass_sha256'}"
    t=repl(t,old,new,'BRIDGE_RECEIPT_KEYS')
    t=repl(t,"if d.get('workflow_pass') is not True: raise Blocked('ITEM_FULL_WORKFLOW_PASS_REQUIRED')\n    outs=d.get('outputs')","if d.get('workflow_pass') is not True: raise Blocked('ITEM_FULL_WORKFLOW_PASS_REQUIRED')\n    mod(DUAL,'dual_rootfix_pass').validate_fachworkflow_pass(REPO,action(s,it),it,d)\n    outs=d.get('outputs')",'BRIDGE_PASS_VALIDATE')
    p.write_text(t,encoding='utf-8')

def patch_prepared_binding(repo:Path):
    p=repo/ENTRY_REL;t=p.read_text(encoding='utf-8')
    t=repl(t,'def start() -> dict:\n    authority()\n    proof = freshness()\n    result = cloud().materialize()','def start() -> dict:\n    _, state, gate, _ = authority()\n    proof = freshness()\n    result = cloud().materialize()','PREPARED_START_AUTHORITY')
    t=repl(t,'    boundary = enforce_capsule_execution_boundary()\n    write_capsule_json("FRESHNESS_PROOF.json", proof)','    boundary = enforce_capsule_execution_boundary()\n    restored_prepared_binding = None\n    if int(gate.get("sequence", -1)) == 107008 and state.get("next_allowed_step") == "FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH":\n        dual = module(REPO / "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py", "dual_rootfix_prepared_restore")\n        restored_prepared_binding = dual.restore_prepared_binding(REPO)\n    write_capsule_json("FRESHNESS_PROOF.json", proof)','PREPARED_START_RESTORE')
    t=repl(t,'        write_capsule_json("FRESHNESS_PROOF.json", post_proof)\n        write_capsule_json("BOUND_PREPARED_RELEASE_REF.json", binding)','        dual = module(REPO / "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py", "dual_rootfix_prepared_persist")\n        dual.persist_prepared_binding(REPO, binding)\n        write_capsule_json("FRESHNESS_PROOF.json", post_proof)\n        write_capsule_json("BOUND_PREPARED_RELEASE_REF.json", binding)','PREPARED_107007_PERSIST')
    t=repl(t,'        pserc_finalization = finalizer.finalize_after_107008(REPO, committed["release_receipt_ref"])\n        return {','        pserc_finalization = finalizer.finalize_after_107008(REPO, committed["release_receipt_ref"])\n        finalizer.clear_prepared_binding(REPO, binding["batch_sha256"])\n        return {','PREPARED_107008_CLEAR')
    p.write_text(t,encoding='utf-8')

def patch_entry(repo:Path):
    p=repo/ENTRY_REL;t=p.read_text(encoding='utf-8')
    t=repl(t,'        if committed.get("status") != "OUTPUT_RELEASE_PASS_FINAL":\n            raise Blocked("FINAL_VISIBLE_RELEASE_NOT_PASS")\n        return {','        if committed.get("status") != "OUTPUT_RELEASE_PASS_FINAL":\n            raise Blocked("FINAL_VISIBLE_RELEASE_NOT_PASS")\n        finalizer = module(REPO / "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py", "dual_rootfix_107008_finalizer")\n        pserc_finalization = finalizer.finalize_after_107008(REPO, committed["release_receipt_ref"])\n        return {','ENTRY_FINALIZER')
    t=repl(t,'            "released_count": committed["released_count"],\n            "rearmed_step_id": finished.get("rearmed_step_id"),','            "released_count": committed["released_count"],\n            "pserc_finalization": pserc_finalization,\n            "rearmed_step_id": finished.get("rearmed_step_id"),','ENTRY_RESULT')
    p.write_text(t,encoding='utf-8')

def upsert(bundle:dict,ref:str,h:str):
    for x in bundle.setdefault('authorized_inputs',[]):
        if isinstance(x,dict) and x.get('ref')==ref:x['sha256']=h;return
    bundle['authorized_inputs'].append({'ref':ref,'sha256':h})
def refresh(repo:Path):
    b7=load(repo/STEP7_REL);b8=load(repo/STEP8_REL)
    for b in (b7,b8):upsert(b,SELF_REL,fsha(repo/SELF_REL));upsert(b,ENTRY_REL,fsha(repo/ENTRY_REL))
    upsert(b7,BRIDGE_REL,fsha(repo/BRIDGE_REL));upsert(b7,CURRENT_ACTION_REL,fsha(repo/CURRENT_ACTION_REL));dump(repo/STEP8_REL,b8)
    if not isinstance(b7.get('next_binding'),dict) or b7['next_binding'].get('bundle_ref')!=STEP8_REL:raise Blocked('NEXT_BINDING_INVALID')
    b7['next_binding']['bundle_sha256']=fsha(repo/STEP8_REL);dump(repo/STEP7_REL,b7);h7=fsha(repo/STEP7_REL)
    st=load(repo/STATE_REL);st['execution_gate']['bundle_sha256']=h7;st['execution_gate_rearm_target']['bundle_sha256']=h7;st['visible_output_security']['official_runtime_entry_sha256']=fsha(repo/ENTRY_REL);dump(repo/STATE_REL,st)
    root=load(repo/ROOT_REL);root['current_state_sha256']=fsha(repo/STATE_REL);dump(repo/ROOT_REL,root)
    ptr=load(repo/PTR_REL);ptr['execution_entrance_gate_sha256']=fsha(repo/ENTRY_REL);dump(repo/PTR_REL,ptr)
def apply(repo:Path)->dict:
    patch_current_action(repo);patch_bridge(repo);patch_entry(repo);patch_prepared_binding(repo);refresh(repo);return {'ok':True,'status':'DUAL_ROOTFIX_APPLIED','publish_allowed':False}

def selftest(repo:Path)->dict:
    b=binding_descriptor(repo);assert set(b['contract_hashes'])==set(CONTRACT_HASHES)
    assert 'dual_rootfix_prepared_restore' in (repo/ENTRY_REL).read_text() and 'dual_rootfix_prepared_persist' in (repo/ENTRY_REL).read_text()
    with tempfile.TemporaryDirectory() as td:
        tr=Path(td);batch='c'*64;prep=tr/'.pferde-release-staging'/batch/'ticket'/'PREPARED_RELEASE.json';prep.parent.mkdir(parents=True,exist_ok=True);dump(prep,{'contract':'PFERDE_ATELIER_PREPARED_OUTPUT_RELEASE_V1','status':'PREPARED_NOT_VISIBLE','batch_sha256':batch,'publish_allowed':False})
        binding={'contract':'PFERDE_ATELIER_BOUND_PREPARED_RELEASE_FOR_FINAL_REVIEW_V1','prepared_ref':str(prep.relative_to(tr)),'prepared_sha256':fsha(prep),'batch_sha256':batch};persist_prepared_binding(tr,binding)
        (tr/Path(RUNTIME_STATE_REL).parent).mkdir(parents=True,exist_ok=True);dump(tr/RUNTIME_STATE_REL,{'batch_sha256':batch});(tr/'.pferde-capsule').mkdir();z=restore_prepared_binding(tr);assert z['status']=='PREPARED_BINDING_RESTORED';assert load(tr/'.pferde-capsule/BOUND_PREPARED_RELEASE_REF.json')==binding
        prep.write_text('{}',encoding='utf-8')
        try:restore_prepared_binding(tr);raise AssertionError('NEG_PREPARED_BINDING_TAMPER')
        except Blocked:pass
        clear_prepared_binding(tr,batch);assert not prepared_binding_sidecar(tr,batch).exists()
    assert 'dual_rootfix_pass' in (repo/BRIDGE_REL).read_text() and 'pserc_finalization' in (repo/ENTRY_REL).read_text()
    with tempfile.TemporaryDirectory() as td:
        tr=Path(td);(tr/'q').mkdir();(tr/Path(PROMPT_REL).parent).mkdir(parents=True);shutil.copy(repo/PROMPT_REL,tr/PROMPT_REL);(tr/Path(SELF_REL).parent).mkdir(parents=True,exist_ok=True);shutil.copy(repo/SELF_REL,tr/SELF_REL);shutil.copy(repo/HANDOFF_REL,tr/HANDOFF_REL)
        a={'allowed_output_root':'q/','item_receipt_schema':{}};it={'canonical_article_id':'article:test','plan_slot':'a'*64}
        (tr/Path(RUNTIME_STATE_REL).parent).mkdir(parents=True,exist_ok=True);dump(tr/RUNTIME_STATE_REL,{'batch_sha256':'c'*64})
        srcp=tr/f".pferde-release/{'c'*64}/ARTICLE_{it['plan_slot']}.md";srcp.parent.mkdir(parents=True,exist_ok=True);srcp.write_text('existing',encoding='utf-8')
        a=augment_current_action(tr,a,it);assert a['existing_article_source_binding']['sha256']==fsha(srcp);rows=[]
        for s in STAGES:
            artifact='q/'+s+'.artifact';(tr/artifact).write_text('real-stage-output',encoding='utf-8')
            proof={'contract':'PFERDE_ATELIER_FACHWORKFLOW_STAGE_EXECUTION_PROOF_V1','status':'PASS','batch_sha256':'c'*64,'canonical_article_id':it['canonical_article_id'],'plan_slot':it['plan_slot'],'stage':s,'execution_performed':True,'input_sha256':'1'*64,'execution_evidence':['selftest stage runner completed'],'artifacts':[{'ref':artifact,'sha256':fsha(tr/artifact)}],'content_or_quality_rules_changed':False,'publish_allowed':False}
            ref='q/'+s+'.json';dump(tr/ref,proof);rows.append({'stage':s,'ref':ref,'sha256':fsha(tr/ref)})
        meta={'article_origin_policy':'POST_TEXT_SIGNED_0039_ORIGIN_AND_NO_REWRITE','authoring_prompt_sha256':'b'*64,'authoring_role':'CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS','content_generation_performed_by_supervisor':False,'contract':INTERNAL_RELEASE_CONTRACT,'created_at_utc':'2026-09-02T00:00:00+00:00','exact_five_batch_sha256':'c'*64,'exact_five_item_count':1,'frozen_workflow_sha256':'d'*64,'nullpunkt':{},'nullpunkt_sha256':'e'*64,'ppm_baseline_sha256':'f'*64,'ppm_version':'6.7.9','research_evidence_policy':'BOUND_EXISTING_FACHWORKFLOW_ONLY','sequence':107008,'status':'PASS','wordpress_write_performed':False}
        q={'contract':PASS_CONTRACT,'status':'PASS','batch_sha256':'c'*64,'canonical_article_id':it['canonical_article_id'],'plan_slot':it['plan_slot'],'contract_binding_ref':SELF_REL,'contract_binding_sha256':binding_sha(tr),'required_stage_proofs':rows,'fact_pack':{'contract':'canonical_fact_pack_v1','fact_pack_id':'fp'},'production_plan_item':{'canonical_article_id':it['canonical_article_id'],'plan_slot':it['plan_slot']},'production_plan_header':{'contract':'production_plan_v4','plan_contract_version':'4.0.0','required_plugin_version':'6.7.9','contract_hashes':CONTRACT_HASHES},'workflow_release_item':{'canonical_article_id':it['canonical_article_id'],'plan_slot':it['plan_slot']},'workflow_release_metadata':meta,'content_or_quality_rules_changed':False,'publish_allowed':False};pref=a['item_receipt_schema']['fachworkflow_pass_ref'];dump(tr/pref,q);h=fsha(tr/pref);d={'outputs':[{'ref':pref,'sha256':h}],'fachworkflow_pass_ref':pref,'fachworkflow_pass_sha256':h};validate_fachworkflow_pass(tr,a,it,d)
        srcp.write_text('tampered-existing',encoding='utf-8')
        try:validate_fachworkflow_pass(tr,a,it,d);raise AssertionError('NEG_EXISTING_SOURCE_HASH')
        except Blocked:pass
        srcp.write_text('existing',encoding='utf-8')
        bad=deepcopy(d);bad['fachworkflow_pass_sha256']='0'*64
        try:validate_fachworkflow_pass(tr,a,it,bad);raise AssertionError('NEG_FACH_HASH')
        except Blocked:pass
        (tr/rows[0]['ref']).write_text('tampered')
        try:validate_fachworkflow_pass(tr,a,it,d);raise AssertionError('NEG_STAGE_HASH')
        except Blocked:pass
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    priv=Ed25519PrivateKey.generate();pub=priv.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw);ks=hashlib.sha256(pub).hexdigest();ki='test-'+ks[:16];pb=base64.b64encode(pub).decode();sign=lambda h:base64.b64encode(priv.sign(h.encode('ascii'))).decode()
    meta={'article_origin_policy':'POST_TEXT_SIGNED_0039_ORIGIN_AND_NO_REWRITE','authoring_prompt_sha256':'b'*64,'authoring_role':'CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS','content_generation_performed_by_supervisor':False,'contract':INTERNAL_RELEASE_CONTRACT,'created_at_utc':'2026-09-02T00:00:00+00:00','exact_five_batch_sha256':'c'*64,'exact_five_item_count':1,'frozen_workflow_sha256':'d'*64,'nullpunkt':{},'nullpunkt_sha256':'e'*64,'ppm_baseline_sha256':'f'*64,'ppm_version':'6.7.9','research_evidence_policy':'BOUND_EXISTING_FACHWORKFLOW_ONLY','sequence':107008,'status':'PASS','wordpress_write_performed':False}
    ctx={'source':'SELFTEST','fact_pack_bundle':{'contract':'canonical_fact_pack_import_v1','fact_packs':[{'contract':'canonical_fact_pack_v1','fact_pack_id':'fp'}]},'production_plan':{'contract':'production_plan_v4','items':[{'canonical_article_id':'article:test','plan_slot':'a'*64}]},'workflow_release_metadata':meta,'workflow_release_items':[{'canonical_article_id':'article:test','plan_slot':'a'*64}]};pkg=build_package(ctx,sign,ki,ks,pb,False)
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'p.json';dump(p,pkg);trusted={ki:{'sha256':ks,'public_key_b64':pb}};assert verify_package(repo,p,trusted)['ok']
        w=deepcopy(pkg);w['extra']=1;dump(p,w)
        try:verify_package(repo,p,trusted);raise AssertionError('NEG_KEYS')
        except Exception:pass
        w=deepcopy(pkg);w['production_plan_sha256']='0'*64;dump(p,w)
        try:verify_package(repo,p,trusted);raise AssertionError('NEG_COMPONENT_HASH')
        except Exception:pass
        w=deepcopy(pkg);w['workflow_release']['signature_b64']='';w['workflow_release_sha256']=stable(w['workflow_release']);w['package_id']=stable({'contract':PACKAGE_CONTRACT,'fact_pack_bundle_sha256':w['fact_pack_bundle_sha256'],'production_plan_sha256':w['production_plan_sha256'],'workflow_release_sha256':w['workflow_release_sha256']});z=dict(w);z.pop('package_payload_sha256',None);w['package_payload_sha256']=stable(z);dump(p,w)
        try:verify_package(repo,p,trusted);raise AssertionError('NEG_SIGNATURE')
        except Exception:pass
    try:build_package(ctx,sign,ki,ks,pb,True);raise AssertionError('NEG_TEST_SIGNER')
    except Blocked:pass
    cp=subprocess.run([sys.executable,str(repo/'control/single-door-boundary/codex_current_action.py'),'selftest'],cwd=repo,text=True,capture_output=True)
    if cp.returncode:raise Blocked('CURRENT_ACTION_SELFTEST_FAIL:'+cp.stdout+cp.stderr)
    return {'ok':True,'status':'DUAL_ROOTFIX_POSITIVE_NEGATIVE_PASS','positive':True,'negative':True,'publish_allowed':False}
def main(a:list[str])->int:
    try:
        if a==['apply']:o=apply(REPO)
        elif a==['selftest']:o=selftest(REPO)
        elif a==['apply-and-test']:apply(REPO);o=selftest(REPO)
        elif len(a)==2 and a[0]=='finalize':o=finalize_after_107008(REPO,a[1])
        else:raise Blocked('USAGE: apply | selftest | apply-and-test | finalize RECEIPT_REF')
        print(json.dumps(o,ensure_ascii=False,indent=2));return 0 if o.get('ok',True) else 2
    except Exception as e:print(json.dumps({'ok':False,'status':'DUAL_ROOTFIX_BLOCKED','reason':str(e),'publish_allowed':False},ensure_ascii=False,indent=2));return 2
if __name__=='__main__':raise SystemExit(main(sys.argv[1:]))
