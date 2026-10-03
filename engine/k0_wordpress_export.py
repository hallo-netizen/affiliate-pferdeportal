from __future__ import annotations
import hashlib, json, re, sys, unicodedata
from pathlib import Path

from .k0_portal_resolver import validate_intake
from .writer_contract_guard import verify_package as verify_writer_contract

CONTRACT='PFERDE_ATELIER_WORDPRESS_IMPORT_V1'
SOURCE='K0_CANONICAL_WORKFLOW'
PLUGIN_VERSION='0.28.30'
PLUGIN_BUILD='0.28.30-pste-v5-binding-safe'
WORDPRESS_ARTICLE_FIELDS=('article_id','plan_slot','title','slug','target_keyword','category','article_type','body')
FIVE_FIELDS=('article_type','category','plan_slot','target_keyword','title')

class Blocked(RuntimeError):
    pass

def _load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,dict):
        raise Blocked('JSON_OBJECT_REQUIRED:'+str(path))
    return x

def _sha(value):
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

def slug_from_title(title):
    value=str(title or '').strip().lower()
    value=value.translate(str.maketrans({'ä':'ae','ö':'oe','ü':'ue','ß':'ss'}))
    value=unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode('ascii')
    value=re.sub(r'[^a-z0-9]+','-',value).strip('-')
    if not value:
        raise Blocked('WORDPRESS_SLUG_EMPTY')
    return value

def build(intake, package, portal, gate, lt, bindings):
    rows=validate_intake(intake)
    if len(rows)!=1:
        raise Blocked('K0_SINGLE_EXPORT_REQUIRES_ONE_ARTICLE')
    identity=rows[0]

    # Internal canonical binding remains mandatory, but it is not the WordPress article_id.
    if bindings.get('contract')!='K10_CANONICAL_ARTICLE_BINDINGS_V1' or bindings.get('status')!='PASS':
        raise Blocked('K0_CANONICAL_BINDINGS_NOT_PASS')
    bmap=bindings.get('bindings') or {}
    canonical_id=str(bmap.get(identity['plan_slot']) or '')
    if not re.fullmatch(r'article:[0-9a-f]{24}',canonical_id):
        raise Blocked('K0_CANONICAL_ARTICLE_ID_INVALID')
    expected_slot=hashlib.sha256(('pserc-plan-slot-v2|'+canonical_id).encode('utf-8')).hexdigest()
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

    # Exact proven K10 WordPress article schema.
    article={
      'article_id':identity['plan_slot'],
      'plan_slot':identity['plan_slot'],
      'title':identity['title'],
      'slug':slug_from_title(identity['title']),
      'target_keyword':identity['target_keyword'],
      'category':identity['category'],
      'article_type':identity['article_type'],
      'body':body,
    }
    if any(not str(article[k]).strip() for k in WORDPRESS_ARTICLE_FIELDS):
        raise Blocked('K0_WORDPRESS_FIELD_EMPTY')

    return {
      'contract':CONTRACT,
      'source':SOURCE,
      'article_count':1,
      'publish_allowed':False,
      'articles':[article],
    }

def verify_export(doc, intake):
    rows=validate_intake(intake)
    if doc.get('contract')!=CONTRACT or doc.get('source')!=SOURCE or doc.get('article_count')!=len(rows) or doc.get('publish_allowed') is not False:
        raise Blocked('K0_WORDPRESS_EXPORT_CONTRACT_INVALID')
    arts=doc.get('articles') or []
    if len(arts)!=1:
        raise Blocked('K0_WORDPRESS_ARTICLE_COUNT_INVALID')
    art=arts[0]; ident=rows[0]
    if set(art)!=set(WORDPRESS_ARTICLE_FIELDS):
        raise Blocked('K0_WORDPRESS_ARTICLE_FIELDS_INVALID')
    if str(art.get('article_id') or '')!=ident['plan_slot']:
        raise Blocked('K0_WORDPRESS_ARTICLE_ID_MUST_EQUAL_PLAN_SLOT')
    if str(art.get('plan_slot') or '')!=ident['plan_slot']:
        raise Blocked('K0_WORDPRESS_PLAN_SLOT_MISMATCH')
    if str(art.get('slug') or '')!=slug_from_title(ident['title']):
        raise Blocked('K0_WORDPRESS_SLUG_MISMATCH')
    for key in ('title','target_keyword','category','article_type'):
        if str(art.get(key) or '')!=str(ident[key]):
            raise Blocked('K0_WORDPRESS_IDENTITY_MISMATCH:'+key)
    body=str(art.get('body') or '')
    if not body:
        raise Blocked('K0_WORDPRESS_BODY_EMPTY')
    return {
      'contract':'K0_WORDPRESS_EXPORT_VERIFY_V2',
      'status':'PASS',
      'wordpress_contract':CONTRACT,
      'article_count':1,
      'body_sha256':_sha(body),
      'article_id_equals_plan_slot':True,
      'slug_status':'PASS',
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
            print(json.dumps({'contract':'K0_WORDPRESS_EXPORT_V2','status':'PASS','output':sys.argv[8],'sha256':_sha(Path(sys.argv[8]).read_text(encoding='utf-8')),'publish_allowed':False},ensure_ascii=False))
            return
        if mode=='verify' and len(sys.argv)==5:
            receipt=verify_export(_load(sys.argv[2]),_load(sys.argv[3]))
            Path(sys.argv[4]).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(receipt,ensure_ascii=False))
            return
        raise Blocked('K0_WORDPRESS_EXPORT_USAGE_INVALID')
    except Exception as exc:
        print(json.dumps({'contract':'K0_WORDPRESS_EXPORT_V2','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False))
        raise SystemExit(2)

if __name__=='__main__':
    main()
