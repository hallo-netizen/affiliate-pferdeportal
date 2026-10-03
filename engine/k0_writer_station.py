from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

from .k0_portal_resolver import validate_intake
from .writer_contract_guard import POLICY, inspect_html, stable, sha_text, verify_package
from .k0_product_property_research import ARTICLE_TYPE as PROPERTY_WINNER_TYPE, validate_packet as validate_property_packet, Blocked as PropertyResearchBlocked
from .k0_full_rules import writer_rule_bundle, validate_rule_context, rule_binding

JOB_CONTRACT='K0_WRITER_JOB_V1'
DRAFT_CONTRACT='K0_WRITER_DRAFT_V1'
PACKAGE_CONTRACT='K0_ARTICLE_PACKAGE_V1'
SEAL_CONTRACT='K0_WRITER_SEAL_V1'
AUTHORING_CONTEXT_CONTRACT='K0_AUTHORING_CONTEXT_V1'

class Blocked(RuntimeError):
    pass

def _load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,dict):
        raise Blocked('JSON_OBJECT_REQUIRED:'+str(path))
    return x

def _job_core(intake, portal, ctx):
    rows=validate_intake(intake)
    if len(rows)!=1:
        raise Blocked('K0_WRITER_JOB_REQUIRES_ONE_ITEM')
    ident=rows[0]
    if portal.get('contract')!='K0_PORTAL_ASSIGNMENT_V1' or portal.get('status')!='PASS':
        raise Blocked('K0_WRITER_PORTAL_NOT_PASS')
    prows=portal.get('items') or []
    if len(prows)!=1 or prows[0].get('status')!='AUTO_DETECTED' or prows[0].get('job_identity')!=ident:
        raise Blocked('K0_WRITER_PORTAL_BINDING_INVALID')
    if ctx.get('contract')!=AUTHORING_CONTEXT_CONTRACT or ctx.get('publish_allowed') is not False:
        raise Blocked('K0_AUTHORING_CONTEXT_INVALID')
    run_instance_id=str(ctx.get('run_instance_id') or '')
    if not re.fullmatch(r'run:[0-9a-f]{24}',run_instance_id):
        raise Blocked('K0_AUTHORING_CONTEXT_RUN_INSTANCE_INVALID')
    if ctx.get('identity')!=ident:
        raise Blocked('K0_AUTHORING_CONTEXT_IDENTITY_MISMATCH')
    for forbidden in ('html','body','content_html','draft','article_text'):
        if forbidden in ctx:
            raise Blocked('K0_AUTHORING_CONTEXT_TEXT_PAYLOAD_FORBIDDEN:'+forbidden)
    cp=ctx.get('content_profile')
    if not isinstance(cp,dict) or not str(cp.get('search_intent') or ''):
        raise Blocked('K0_AUTHORING_CONTEXT_INTENT_MISSING')
    pc=ctx.get('production_context')
    if not isinstance(pc,dict) or not isinstance(pc.get('fact_pack'),dict) or not isinstance(pc.get('production_plan_item'),dict):
        raise Blocked('K0_AUTHORING_CONTEXT_RESEARCH_MISSING')
    try:
        rule_context=validate_rule_context(ctx.get('rule_context'),ident)
        full_rule_bundle=writer_rule_bundle(ident.get('article_type'))
        full_rule_binding=rule_binding(full_rule_bundle)
    except Exception as exc:
        raise Blocked('K0_AUTHORING_FULL_RULE_CONTEXT_INVALID:'+str(exc)) from exc
    if ident.get('article_type')==PROPERTY_WINNER_TYPE:
        try:
            property_result=validate_property_packet(ident,pc.get('property_research'))
        except PropertyResearchBlocked as exc:
            raise Blocked('K0_PROPERTY_RESEARCH_BLOCKED:'+str(exc)) from exc
        if str(cp.get('search_intent') or '')!=property_result.get('search_intent'):
            raise Blocked('K0_PROPERTY_RESEARCH_INTENT_MISMATCH')
    return {
      'contract':JOB_CONTRACT,
      'status':'OPEN',
      'identity':ident,
      'portal_id':prows[0]['portal_id'],
      'run_instance_id':run_instance_id,
      'content_profile':cp,
      'production_context':pc,
      'rule_context':rule_context,
      'writer_rule_bundle':full_rule_bundle,
      'writer_rule_binding':full_rule_binding,
      'writer_policy':POLICY,
      'writer_policy_sha256':stable(POLICY),
      'publish_allowed':False,
    }

def prepare(intake, portal, ctx):
    core=_job_core(intake,portal,ctx)
    job_seed=stable(core)
    job_id='k0w-'+job_seed[:24]
    core['job_id']=job_id
    core['job_sha256']=stable({k:v for k,v in core.items() if k!='job_sha256'})
    return core

def _draft_sha(draft):
    return stable(draft)

def seal(job, draft):
    if job.get('contract')!=JOB_CONTRACT or job.get('status')!='OPEN' or job.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_JOB_INVALID')
    expected_job_sha=stable({k:v for k,v in job.items() if k!='job_sha256'})
    if job.get('job_sha256')!=expected_job_sha:
        raise Blocked('K0_WRITER_JOB_HASH_INVALID')
    if job.get('writer_policy_sha256')!=stable(POLICY) or job.get('writer_policy')!=POLICY:
        raise Blocked('K0_WRITER_POLICY_DRIFT')
    try:
        current_bundle=writer_rule_bundle(job.get('identity',{}).get('article_type'))
        current_binding=rule_binding(current_bundle)
    except Exception as exc:
        raise Blocked('K0_WRITER_FULL_RULE_BUNDLE_INVALID:'+str(exc)) from exc
    if job.get('writer_rule_bundle')!=current_bundle or job.get('writer_rule_binding')!=current_binding:
        raise Blocked('K0_WRITER_FULL_RULE_BUNDLE_DRIFT')
    if validate_rule_context(job.get('rule_context'),job.get('identity') or {})!=job.get('rule_context'):
        raise Blocked('K0_WRITER_RULE_CONTEXT_DRIFT')

    allowed={'contract','job_id','title','content_html','table_decision','lt_authoritative_terms','revision_count','publish_allowed'}
    if set(draft)-allowed:
        raise Blocked('K0_WRITER_DRAFT_FIELDS_INVALID:'+','.join(sorted(set(draft)-allowed)))
    if draft.get('contract')!=DRAFT_CONTRACT or draft.get('job_id')!=job.get('job_id'):
        raise Blocked('K0_WRITER_DRAFT_JOB_MISMATCH')
    if draft.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_DRAFT_PUBLISH_INVALID')
    ident=job['identity']
    if str(draft.get('title') or '')!=ident['title']:
        raise Blocked('K0_WRITER_DRAFT_TITLE_MISMATCH')
    body=str(draft.get('content_html') or '')
    metrics=inspect_html(body)

    table=draft.get('table_decision')
    if not isinstance(table,dict):
        raise Blocked('K0_WRITER_DRAFT_TABLE_DECISION_MISSING')
    if table!=job.get('rule_context',{}).get('table_decision'):
        raise Blocked('K0_WRITER_DRAFT_TABLE_DECISION_NOT_PREBOUND')
    terms=draft.get('lt_authoritative_terms')
    if not isinstance(terms,list):
        raise Blocked('K0_WRITER_DRAFT_LT_TERMS_INVALID')

    core={
      'contract':SEAL_CONTRACT,
      'status':'PASS',
      'route':'K0_WRITER_DRAFT_ONLY',
      'job_id':job['job_id'],
      'job_sha256':job['job_sha256'],
      'draft_sha256':_draft_sha(draft),
      'identity_sha256':stable(ident),
      'visible_text_sha256':sha_text(_plain_for_seal(body)),
      'section_structure_sha256':stable(metrics['normal_h2_sections']),
      'policy_sha256':metrics['policy_sha256'],
      'full_rule_bundle_sha256':job['writer_rule_binding']['bundle_sha256'],
      'full_rule_catalog_sha256':job['writer_rule_binding']['catalog_sha256'],
      'full_rule_values_sha256':job['writer_rule_binding']['rule_values_sha256'],
      'full_rule_hard_count':job['writer_rule_binding']['article_hard_rule_count'],
      'total_words':metrics['total_words'],
      'conclusion_ratio':round(metrics['conclusion_ratio'],6),
      'section_balance_status':'PASS',
      'conclusion_status':'PASS',
      'further_information_status':'PASS',
      'publish_allowed':False,
    }
    provenance={**core,'seal_sha256':stable(core)}
    out={
      'contract':PACKAGE_CONTRACT,
      'identity':ident,
      'html':body,
      'final_draft_sha256':sha_text(body),
      'content_profile':job['content_profile'],
      'rule_context':job['rule_context'],
      'writer_rule_binding':job['writer_rule_binding'],
      'table_decision':table,
      'lt_authoritative_terms':terms,
      'production_context':job['production_context'],
      'revision_count':int(draft.get('revision_count') or 1),
      'writer_provenance':provenance,
      'publish_allowed':False,
    }
    verify(job,out)
    return out

def _plain_for_seal(value):
    import html as htmlmod
    value=re.sub(r'(?is)<[^>]+>',' ',str(value or ''))
    value=htmlmod.unescape(value)
    return re.sub(r'\s+',' ',value).strip()

def verify(job, package):
    if job.get('contract')!=JOB_CONTRACT:
        raise Blocked('K0_WRITER_JOB_CONTRACT_INVALID')
    expected_job_sha=stable({k:v for k,v in job.items() if k!='job_sha256'})
    if job.get('job_sha256')!=expected_job_sha:
        raise Blocked('K0_WRITER_JOB_HASH_INVALID')
    if package.get('contract')!=PACKAGE_CONTRACT or package.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_PACKAGE_INVALID')
    if package.get('identity')!=job.get('identity'):
        raise Blocked('K0_WRITER_PACKAGE_IDENTITY_MISMATCH')
    if package.get('content_profile')!=job.get('content_profile'):
        raise Blocked('K0_WRITER_PACKAGE_INTENT_MISMATCH')
    if package.get('production_context')!=job.get('production_context'):
        raise Blocked('K0_WRITER_PACKAGE_CONTEXT_MISMATCH')
    if package.get('rule_context')!=job.get('rule_context'):
        raise Blocked('K0_WRITER_PACKAGE_RULE_CONTEXT_MISMATCH')
    if package.get('writer_rule_binding')!=job.get('writer_rule_binding'):
        raise Blocked('K0_WRITER_PACKAGE_FULL_RULE_BINDING_MISMATCH')
    prov=package.get('writer_provenance') or {}
    if prov.get('job_id')!=job.get('job_id') or prov.get('job_sha256')!=job.get('job_sha256'):
        raise Blocked('K0_WRITER_PACKAGE_JOB_BINDING_INVALID')
    if prov.get('identity_sha256')!=stable(job['identity']):
        raise Blocked('K0_WRITER_PACKAGE_IDENTITY_HASH_INVALID')
    if prov.get('full_rule_bundle_sha256')!=job['writer_rule_binding']['bundle_sha256'] or prov.get('full_rule_hard_count')!=job['writer_rule_binding']['article_hard_rule_count']:
        raise Blocked('K0_WRITER_PACKAGE_FULL_RULE_PROVENANCE_INVALID')
    metrics=verify_package(package)
    return {
      'contract':'K0_WRITER_SEAL_VERIFY_V1',
      'status':'PASS',
      'job_id':job['job_id'],
      'job_sha256':job['job_sha256'],
      'policy_sha256':metrics['policy_sha256'],
      'total_words':metrics['total_words'],
      'conclusion_ratio':metrics['conclusion_ratio'],
      'publish_allowed':False,
    }

def main():
    try:
        if len(sys.argv)==6 and sys.argv[1]=='prepare':
            out=prepare(_load(sys.argv[2]),_load(sys.argv[3]),_load(sys.argv[4]))
            Path(sys.argv[5]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps({'contract':JOB_CONTRACT,'status':'PASS','job_id':out['job_id'],'job_sha256':out['job_sha256'],'publish_allowed':False},ensure_ascii=False))
            return
        if len(sys.argv)==5 and sys.argv[1]=='seal':
            out=seal(_load(sys.argv[2]),_load(sys.argv[3]))
            Path(sys.argv[4]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps({'contract':SEAL_CONTRACT,'status':'PASS','job_id':out['writer_provenance']['job_id'],'seal_sha256':out['writer_provenance']['seal_sha256'],'publish_allowed':False},ensure_ascii=False))
            return
        if len(sys.argv)==4 and sys.argv[1]=='verify':
            out=verify(_load(sys.argv[2]),_load(sys.argv[3]))
            print(json.dumps(out,ensure_ascii=False))
            return
        raise Blocked('K0_WRITER_STATION_USAGE_INVALID')
    except Exception as exc:
        print(json.dumps({'contract':'K0_WRITER_STATION_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False))
        raise SystemExit(2)

if __name__=='__main__':
    main()
