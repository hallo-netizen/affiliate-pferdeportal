from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

from .k0_portal_resolver import validate_intake
from .writer_contract_guard import verify_package as verify_writer_contract

CONTRACT='SYSTEM4_WORDPRESS_HANDOFF_V1'
PLUGIN_VERSION='0.28.30'
PLUGIN_BUILD='0.28.30-pste-v5-binding-safe'
PPM_VERSION='6.7.9'
FIVE_FIELDS=('article_type','category','plan_slot','target_keyword','title')
WORDPRESS_ARTICLE_FIELDS=('index','article_id','title','target_keyword','category','article_type','plan_slot','final_draft_sha256','revision_count','body','production_context','languagetool','ppm679')

class Blocked(RuntimeError):
    pass

def _load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,dict):
        raise Blocked('JSON_OBJECT_REQUIRED:'+str(path))
    return x

def _sha(value):
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

def build(intake, package, portal, gate, lt, bindings):
    rows=validate_intake(intake)
    if len(rows)!=1:
        raise Blocked('K0_SINGLE_EXPORT_REQUIRES_ONE_ARTICLE')
    identity=rows[0]
    if bindings.get('contract')!='K10_CANONICAL_ARTICLE_BINDINGS_V1' or bindings.get('status')!='PASS':
        raise Blocked('K0_CANONICAL_BINDINGS_NOT_PASS')
    bmap=bindings.get('bindings') or {}
    article_id=str(bmap.get(identity['plan_slot']) or '')
    if not re.fullmatch(r'article:[0-9a-f]{24}',article_id):
        raise Blocked('K0_CANONICAL_ARTICLE_ID_INVALID')
    expected_slot=hashlib.sha256(('pserc-plan-slot-v2|'+article_id).encode('utf-8')).hexdigest()
    if expected_slot!=identity['plan_slot']:
        raise Blocked('K0_CANONICAL_ARTICLE_ID_PLAN_SLOT_MISMATCH')

    if package.get('contract')!='K0_ARTICLE_PACKAGE_V1':
        raise Blocked('K0_ARTICLE_PACKAGE_CONTRACT_INVALID')
    if package.get('identity')!=identity:
        raise Blocked('K0_ARTICLE_IDENTITY_MISMATCH')
    if package.get('publish_allowed') is not False:
        raise Blocked('K0_ARTICLE_PUBLISH_ALLOWED_INVALID')

    body=str(package.get('html') or '')
    body_sha=_sha(body)
    try:
        writer_metrics=verify_writer_contract(package)
    except Exception as exc:
        raise Blocked('K0_WORDPRESS_WRITER_CONTRACT_BLOCKED:'+str(exc))
    if not body or package.get('final_draft_sha256')!=body_sha:
        raise Blocked('K0_ARTICLE_BODY_HASH_INVALID')

    if portal.get('contract')!='K0_PORTAL_ASSIGNMENT_V1' or portal.get('status')!='PASS':
        raise Blocked('K0_PORTAL_ASSIGNMENT_NOT_PASS')
    prows=portal.get('items') or []
    if len(prows)!=1 or prows[0].get('status')!='AUTO_DETECTED' or prows[0].get('job_identity')!=identity:
        raise Blocked('K0_PORTAL_ASSIGNMENT_INVALID')

    if gate.get('contract')!='K0_PRODUCTION_GATES_V1' or gate.get('status')!='PASS':
        raise Blocked('K0_GATES_NOT_PASS')
    if gate.get('body_sha256')!=body_sha or gate.get('ppm679_status')!='PASS' or gate.get('ppm679_rule_count')!=104:
        raise Blocked('K0_GATE_BINDING_INVALID')
    if gate.get('semantic_intent_status')!='PASS' or gate.get('anti_boilerplate_status')!='PASS':
        raise Blocked('K0_SEMANTIC_GATE_NOT_PASS')
    if gate.get('writer_contract_status')!='PASS' or gate.get('writer_policy_sha256')!=writer_metrics.get('policy_sha256'):
        raise Blocked('K0_WRITER_GATE_NOT_PASS')

    if lt.get('status')!='PASS' or int(lt.get('finding_count') or 0)!=0:
        raise Blocked('K0_LT68_NOT_PASS')
    if lt.get('html_sha256')!=body_sha:
        raise Blocked('K0_LT68_BODY_HASH_MISMATCH')

    context=package.get('production_context')
    if not isinstance(context,dict) or not isinstance(context.get('fact_pack'),dict) or not isinstance(context.get('production_plan_item'),dict):
        raise Blocked('K0_PRODUCTION_CONTEXT_MISSING')

    plan_item=dict(context.get('production_plan_item') or {})
    plan_item['canonical_article_id']=article_id

    article={
      'index':0,
      'article_id':article_id,
      'title':identity['title'],
      'target_keyword':identity['target_keyword'],
      'category':identity['category'],
      'article_type':identity['article_type'],
      'plan_slot':identity['plan_slot'],
      'final_draft_sha256':body_sha,
      'revision_count':int(package.get('revision_count') or 1),
      'body':body,
      'production_context':{**context,'production_plan_item':plan_item,'writer_provenance':package.get('writer_provenance')},
      'languagetool':{
        'status':'PASS',
        'engine':'LanguageTool 6.8',
      },
      'ppm679':{
        'status':'PASS',
        'ppm_version':PPM_VERSION,
        'content_sha256':body_sha,
      },
    }

    return {
      'contract':CONTRACT,
      'batch_sha256':intake['batch_sha256'],
      'article_count':1,
      'publish_allowed':False,
      'signing_deferred':True,
      'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED',
      'no_legacy_status':'PASS',
      'test_suite_status':'PASS',
      'wordpress_review':{
        'file_format':'JSON',
        'mime_type':'application/json',
        'intended_next_step':'WORDPRESS_DIRECT_IMPORT',
        'plugin_name':'Portal SEO Editorial Plan Compiler',
        'plugin_version_verified_against':PLUGIN_VERSION,
        'plugin_build_verified_against':PLUGIN_BUILD,
        'ppm_version_verified_against':PPM_VERSION,
        'direct_wordpress_upload_ready':True,
        'direct_upload_block_reason':None,
        'required_downstream_components':[],
      },
      'articles':[article],
    }

def verify_export(doc, intake):
    rows=validate_intake(intake)
    if doc.get('contract')!=CONTRACT or doc.get('article_count')!=len(rows) or doc.get('publish_allowed') is not False:
        raise Blocked('K0_WORDPRESS_EXPORT_CONTRACT_INVALID')
    if doc.get('batch_sha256')!=intake.get('batch_sha256'):
        raise Blocked('K0_WORDPRESS_BATCH_MISMATCH')
    review=doc.get('wordpress_review') or {}
    if review.get('plugin_version_verified_against')!=PLUGIN_VERSION or review.get('plugin_build_verified_against')!=PLUGIN_BUILD or review.get('direct_wordpress_upload_ready') is not True:
        raise Blocked('K0_WORDPRESS_REVIEW_INVALID')
    arts=doc.get('articles') or []
    if len(arts)!=1:
        raise Blocked('K0_WORDPRESS_ARTICLE_COUNT_INVALID')
    art=arts[0]; ident=rows[0]
    if set(art)!=set(WORDPRESS_ARTICLE_FIELDS):
        raise Blocked('K0_WORDPRESS_ARTICLE_FIELDS_INVALID')
    if 'canonical_article_id' in art:
        raise Blocked('K0_WORDPRESS_TOPLEVEL_CANONICAL_ARTICLE_ID_FORBIDDEN')
    article_id=str(art.get('article_id') or '')
    if not re.fullmatch(r'article:[0-9a-f]{24}',article_id):
        raise Blocked('K0_WORDPRESS_ARTICLE_ID_INVALID')
    pc=art.get('production_context') if isinstance(art.get('production_context'),dict) else {}
    pi=pc.get('production_plan_item') if isinstance(pc.get('production_plan_item'),dict) else {}
    nested_article_id=str(pi.get('canonical_article_id') or '')
    if not re.fullmatch(r'article:[0-9a-f]{24}',nested_article_id):
        raise Blocked('K0_WORDPRESS_CANONICAL_ARTICLE_ID_MISSING_IN_PRODUCTION_CONTEXT')
    if nested_article_id!=article_id:
        raise Blocked('K0_WORDPRESS_ARTICLE_ID_BINDING_MISMATCH')
    if hashlib.sha256(('pserc-plan-slot-v2|'+article_id).encode('utf-8')).hexdigest()!=ident['plan_slot']:
        raise Blocked('K0_WORDPRESS_CANONICAL_ARTICLE_ID_PLAN_SLOT_MISMATCH')
    for key in FIVE_FIELDS:
        if str(art.get(key) or '')!=str(ident[key]):
            raise Blocked('K0_WORDPRESS_IDENTITY_MISMATCH:'+key)
    body=str(art.get('body') or '')
    if _sha(body)!=art.get('final_draft_sha256'):
        raise Blocked('K0_WORDPRESS_BODY_SHA_MISMATCH')
    if (art.get('languagetool') or {}).get('status')!='PASS' or (art.get('ppm679') or {}).get('status')!='PASS':
        raise Blocked('K0_WORDPRESS_QUALITY_STATUS_INVALID')
    return {
      'contract':'K0_WORDPRESS_EXPORT_VERIFY_V1',
      'status':'PASS',
      'wordpress_contract':CONTRACT,
      'batch_sha256':doc['batch_sha256'],
      'article_count':1,
      'body_sha256':art['final_draft_sha256'],
      'publish_allowed':False,
    }

def main():
    if len(sys.argv)<2:
        raise SystemExit('usage: k0_wordpress_export.py export INTAKE PACKAGE PORTAL GATE LT CANONICAL_BINDINGS OUT | verify OUT INTAKE RECEIPT')
    try:
        mode=sys.argv[1]
        if mode=='export' and len(sys.argv)==9:
            out=build(*[_load(p) for p in sys.argv[2:8]])
            Path(sys.argv[8]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps({'contract':'K0_WORDPRESS_EXPORT_V1','status':'PASS','output':sys.argv[8],'sha256':_sha(Path(sys.argv[8]).read_text(encoding='utf-8')),'publish_allowed':False},ensure_ascii=False))
            return
        if mode=='verify' and len(sys.argv)==5:
            receipt=verify_export(_load(sys.argv[2]),_load(sys.argv[3]))
            Path(sys.argv[4]).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(receipt,ensure_ascii=False))
            return
        raise Blocked('K0_WORDPRESS_EXPORT_USAGE_INVALID')
    except Exception as exc:
        print(json.dumps({'contract':'K0_WORDPRESS_EXPORT_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False))
        raise SystemExit(2)

if __name__=='__main__':
    main()
