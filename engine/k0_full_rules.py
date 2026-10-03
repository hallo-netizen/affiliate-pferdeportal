from __future__ import annotations
import copy, json, re, sys
from pathlib import Path

from .core import ROOT, load_catalog, load_values, catalog_hash, values_hash, stable
from .checkers import run_article_content_checks, run_article_checks, article_hash
from .final_integrity import verify_article_pre_lt68, verify_article

CONTRACT='K0_FULL_RULE_BUNDLE_V1'
RULE_CONTEXT_CONTRACT='K0_AUTHORING_RULE_CONTEXT_V1'
FINAL_CONTRACT='K0_FULL_RULE_FINAL_V1'

class Blocked(RuntimeError):
    pass

def _load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,(dict,list)):
        raise Blocked('JSON_REQUIRED:'+str(path))
    return x

def _field_policy():
    return json.loads((ROOT/'FIELD_POLICY.json').read_text(encoding='utf-8'))

def _scope_reference():
    return json.loads((ROOT/'TEXTMACHINE_SCOPE_REFERENCE.json').read_text(encoding='utf-8'))

def writer_rule_bundle(article_type):
    catalog=load_catalog()
    values=load_values()
    typ=str(article_type or '')
    if typ not in values.get('types',{}):
        raise Blocked('K0_FULL_RULE_ARTICLE_TYPE_VALUES_MISSING:'+typ)
    article_rules=[r for r in catalog.get('rules',[]) if r.get('scope')=='ARTICLE']
    hard=[r for r in article_rules if r.get('classification')=='HARD']
    targets=[r for r in article_rules if r.get('classification')=='TARGET']
    field_policy=_field_policy()
    scope=_scope_reference()
    out={
      'contract':CONTRACT,
      'article_type':typ,
      'catalog_sha256':catalog_hash(),
      'rule_values_sha256':values_hash(),
      'field_policy_sha256':stable(field_policy),
      'scope_reference_sha256':stable(scope),
      'article_hard_rule_count':len(hard),
      'article_hard_rule_ids':[r['id'] for r in hard],
      'article_target_rule_ids':[r['id'] for r in targets],
      'rule_catalog':catalog,
      'rule_values':values,
      'field_policy':field_policy,
      'scope_reference':scope,
      'publish_allowed':False,
    }
    out['bundle_sha256']=stable({k:v for k,v in out.items() if k!='bundle_sha256'})
    return out

def _validate_type_meta(meta,schema):
    if not isinstance(meta,dict):
        raise Blocked('K0_RULE_CONTEXT_TYPE_META_MISSING')
    for name in schema.get('required') or []:
        if name not in meta:
            raise Blocked('K0_RULE_CONTEXT_TYPE_META_REQUIRED:'+name)
    for name,spec in (schema.get('fields') or {}).items():
        if name not in meta:
            continue
        val=meta[name]
        if spec.get('type')=='string':
            if not isinstance(val,str) or len(val.strip())<int(spec.get('min_length') or 0):
                raise Blocked('K0_RULE_CONTEXT_TYPE_META_INVALID:'+name)
        if spec.get('type')=='list':
            if not isinstance(val,list) or len(val)<int(spec.get('min_items') or 0):
                raise Blocked('K0_RULE_CONTEXT_TYPE_META_INVALID:'+name)
            if spec.get('unique_items') and len({str(x) for x in val})!=len(val):
                raise Blocked('K0_RULE_CONTEXT_TYPE_META_DUPLICATE:'+name)

def validate_rule_context(ctx,identity):
    if not isinstance(ctx,dict) or ctx.get('contract')!=RULE_CONTEXT_CONTRACT:
        raise Blocked('K0_RULE_CONTEXT_CONTRACT_INVALID')
    values=load_values()
    typ=str(identity.get('article_type') or '')
    cfg=(values.get('types') or {}).get(typ)
    if not isinstance(cfg,dict):
        raise Blocked('K0_FULL_RULE_ARTICLE_TYPE_VALUES_MISSING:'+typ)

    _validate_type_meta(ctx.get('type_meta'),cfg.get('type_meta_schema') or {})

    claims=ctx.get('research_claims')
    if not isinstance(claims,dict) or len(claims)<3:
        raise Blocked('K0_RULE_CONTEXT_RESEARCH_CLAIMS_INCOMPLETE')
    for fid,row in claims.items():
        if not isinstance(row,dict):
            raise Blocked('K0_RULE_CONTEXT_RESEARCH_CLAIM_INVALID:'+str(fid))
        required=('source_title','source_url','evidence_text_sha256','statement','evidence_text','claim_status','article_types')
        if any(k not in row for k in required):
            raise Blocked('K0_RULE_CONTEXT_RESEARCH_CLAIM_FIELDS:'+str(fid))
        if row.get('claim_status')!='FULLY_SUPPORTED' or typ not in (row.get('article_types') or []):
            raise Blocked('K0_RULE_CONTEXT_RESEARCH_CLAIM_NOT_USABLE:'+str(fid))
        if not re.fullmatch(r'[0-9a-f]{64}',str(row.get('evidence_text_sha256') or '')):
            raise Blocked('K0_RULE_CONTEXT_RESEARCH_CLAIM_HASH_INVALID:'+str(fid))

    required_ids=ctx.get('required_fact_ids')
    allowed_ids=ctx.get('allowed_fact_ids')
    if not isinstance(required_ids,list) or not required_ids or not isinstance(allowed_ids,list) or not allowed_ids:
        raise Blocked('K0_RULE_CONTEXT_FACT_ID_SETS_MISSING')
    if not set(required_ids).issubset(set(claims)) or not set(allowed_ids).issubset(set(claims)):
        raise Blocked('K0_RULE_CONTEXT_FACT_ID_UNKNOWN')
    if not set(required_ids).issubset(set(allowed_ids)):
        raise Blocked('K0_RULE_CONTEXT_REQUIRED_FACT_NOT_ALLOWED')

    links=ctx.get('bound_links')
    roles=set(values['global']['required_link_roles'])
    if not isinstance(links,list) or len(links)!=int(values['global']['visible_links_exact']):
        raise Blocked('K0_RULE_CONTEXT_LINK_COUNT_INVALID')
    actual_roles={str(x.get('role') or '') for x in links if isinstance(x,dict)}
    if actual_roles!=roles:
        raise Blocked('K0_RULE_CONTEXT_LINK_ROLES_INVALID')
    blocks=[]
    for x in links:
        href=str(x.get('href') or '')
        block=str(x.get('block') or '')
        anchor=str(x.get('anchor') or '')
        if not href.startswith('/') or href.startswith('//') or '://' in href or not block or not anchor:
            raise Blocked('K0_RULE_CONTEXT_LINK_INVALID')
        blocks.append(block)
    if len(set(blocks))!=len(blocks):
        raise Blocked('K0_RULE_CONTEXT_LINK_BLOCKS_NOT_DISTINCT')

    registry=ctx.get('link_registry')
    if not isinstance(registry,list):
        raise Blocked('K0_RULE_CONTEXT_LINK_REGISTRY_MISSING')
    reg={str(x.get('href') or ''):x for x in registry if isinstance(x,dict)}
    if any(str(x.get('href') or '') not in reg or reg[str(x.get('href') or '')].get('active') is False for x in links):
        raise Blocked('K0_RULE_CONTEXT_LINK_REGISTRY_INACTIVE')
    runtime_roles=set(ctx.get('runtime_link_roles') or [])
    if runtime_roles!=roles:
        raise Blocked('K0_RULE_CONTEXT_RUNTIME_LINK_ROLES_INVALID')

    wc=ctx.get('wordpress_category')
    if not isinstance(wc,dict) or str(wc.get('slug') or '')!=str(identity.get('category') or '') or str(wc.get('taxonomy') or '')!='category':
        raise Blocked('K0_RULE_CONTEXT_WORDPRESS_CATEGORY_INVALID')

    heading_terms=ctx.get('heading_intent_terms')
    if not isinstance(heading_terms,list) or not [x for x in heading_terms if str(x).strip()]:
        raise Blocked('K0_RULE_CONTEXT_HEADING_INTENT_TERMS_MISSING')

    comp=ctx.get('comparison_source_bindings')
    if not isinstance(comp,list):
        raise Blocked('K0_RULE_CONTEXT_COMPARISON_BINDINGS_INVALID')
    if typ=='Vergleich' and not comp:
        raise Blocked('K0_RULE_CONTEXT_COMPARISON_BINDINGS_MISSING')

    table=ctx.get('table_decision')
    if not isinstance(table,dict):
        raise Blocked('K0_RULE_CONTEXT_TABLE_DECISION_MISSING')
    tcfg=values['table']; policy=tcfg['presence_policy'][typ]
    decision=str(table.get('decision') or '')
    if policy=='REQUIRED' and decision!=tcfg['optional_decision']['include_value']:
        raise Blocked('K0_RULE_CONTEXT_TABLE_REQUIRED')
    if policy in ('REQUIRED_UNLESS_EXCEPTION','OPTIONAL'):
        if decision not in {tcfg['optional_decision']['include_value'],tcfg['optional_decision']['omit_value']}:
            raise Blocked('K0_RULE_CONTEXT_TABLE_DECISION_INVALID')
        if decision==tcfg['optional_decision']['omit_value']:
            allowed=set((tcfg.get('omission_exception') or {}).get('allowed_codes') or [])
            if str(table.get('exception_code') or '') not in allowed:
                raise Blocked('K0_RULE_CONTEXT_TABLE_EXCEPTION_INVALID')
    if len(str(table.get('rationale') or '').strip())<int(tcfg['optional_decision']['rationale_minimum_chars']):
        raise Blocked('K0_RULE_CONTEXT_TABLE_RATIONALE_TOO_SHORT')

    semantic=ctx.get('semantic_rule_results')
    if not isinstance(semantic,dict):
        raise Blocked('K0_RULE_CONTEXT_SEMANTIC_RESULTS_MISSING')
    if decision==tcfg['optional_decision']['include_value'] and semantic.get('table.value_required_if_present')!='PASS':
        raise Blocked('K0_RULE_CONTEXT_TABLE_VALUE_NOT_PREBOUND_PASS')

    out=copy.deepcopy(ctx)
    out['identity_sha256']=stable(identity)
    out['catalog_sha256']=catalog_hash()
    out['rule_values_sha256']=values_hash()
    return out

def rule_binding(bundle):
    expected=writer_rule_bundle(bundle.get('article_type'))
    if bundle!=expected:
        raise Blocked('K0_WRITER_RULE_BUNDLE_DRIFT')
    return {
      'contract':'K0_WRITER_RULE_BINDING_V1',
      'catalog_sha256':bundle['catalog_sha256'],
      'rule_values_sha256':bundle['rule_values_sha256'],
      'bundle_sha256':bundle['bundle_sha256'],
      'article_hard_rule_count':bundle['article_hard_rule_count'],
      'article_hard_rule_ids':bundle['article_hard_rule_ids'],
      'publish_allowed':False,
    }

def _resolve_category(identity,category_payload):
    if not isinstance(category_payload,list):
        raise Blocked('K0_FULL_RULE_CATEGORY_RESPONSE_NOT_LIST')
    slug=str(identity.get('category') or '')
    hits=[x for x in category_payload if isinstance(x,dict) and str(x.get('slug') or '')==slug and int(x.get('id') or 0)>0]
    if len(hits)!=1:
        raise Blocked('K0_FULL_RULE_CATEGORY_NOT_UNIQUE:'+slug+':'+str(len(hits)))
    return {'id':int(hits[0]['id']),'slug':slug,'taxonomy':'category','id_source':'WORDPRESS_REST_LIVE'}

def build_check_article(package,category_payload,lt_status=None):
    ident=package.get('identity') or {}
    ctx=validate_rule_context(package.get('rule_context'),ident)
    binding=package.get('writer_rule_binding')
    if not isinstance(binding,dict):
        raise Blocked('K0_WRITER_RULE_BINDING_MISSING')
    bundle=writer_rule_bundle(ident.get('article_type'))
    if binding!=rule_binding(bundle):
        raise Blocked('K0_WRITER_RULE_BINDING_INVALID')
    article={
      'article_id':str(ident.get('plan_slot') or ''),
      'article_type':ident.get('article_type'),
      'title':ident.get('title'),
      'target_keyword':ident.get('target_keyword'),
      'type_meta':copy.deepcopy(ctx['type_meta']),
      'research_claims':copy.deepcopy(ctx['research_claims']),
      'required_fact_ids':copy.deepcopy(ctx['required_fact_ids']),
      'allowed_fact_ids':copy.deepcopy(ctx['allowed_fact_ids']),
      'bound_links':copy.deepcopy(ctx['bound_links']),
      'link_registry':copy.deepcopy(ctx['link_registry']),
      'runtime_link_roles':copy.deepcopy(ctx['runtime_link_roles']),
      'wordpress_category':_resolve_category(ident,category_payload),
      'heading_intent_terms':copy.deepcopy(ctx['heading_intent_terms']),
      'comparison_source_bindings':copy.deepcopy(ctx['comparison_source_bindings']),
      'table_decision':copy.deepcopy(ctx['table_decision']),
      'semantic_rule_results':copy.deepcopy(ctx['semantic_rule_results']),
      'table_multiword_exceptions':copy.deepcopy(ctx.get('table_multiword_exceptions') or []),
      'html':str(package.get('html') or ''),
      'external_results':{'LanguageTool 6.8':lt_status or 'PENDING'},
      'publish_allowed':False,
    }
    return article

def verify_pre_lt68(package,category_payload):
    article=build_check_article(package,category_payload)
    receipts=run_article_content_checks(article)
    report=verify_article_pre_lt68(article['article_id'],article_hash(article),receipts)
    if report.get('status')!='READY_FOR_LT68':
        failed=[r['rule_id'] for r in receipts if r.get('status')!='PASS']
        raise Blocked('K0_FULL_RULE_PRE_LT68_BLOCKED:'+','.join(failed or report.get('findings') or []))
    return {
      'contract':'K0_FULL_RULE_PRE_LT68_V1',
      'status':'READY_FOR_LT68',
      'article_id':article['article_id'],
      'article_sha256':article_hash(article),
      'hard_rule_receipts':len(receipts),
      'required_receipt_count':report.get('required_receipt_count'),
      'catalog_sha256':catalog_hash(),
      'rule_values_sha256':values_hash(),
      'body_sha256':stable(str(package.get('html') or '')),
      'publish_allowed':False,
    }

def verify_final(package,category_payload,lt):
    if not isinstance(lt,dict) or lt.get('status')!='PASS' or int(lt.get('finding_count') or 0)!=0:
        raise Blocked('K0_FULL_RULE_LT68_NOT_PASS')
    article=build_check_article(package,category_payload,'PASS')
    receipts=run_article_checks(article)
    report=verify_article(article['article_id'],article_hash(article),receipts)
    if report.get('status')!='PASS':
        failed=[r['rule_id'] for r in receipts if r.get('status')!='PASS']
        raise Blocked('K0_FULL_RULE_FINAL_BLOCKED:'+','.join(failed or report.get('findings') or []))
    return {
      'contract':FINAL_CONTRACT,
      'status':'PASS',
      'article_id':article['article_id'],
      'article_sha256':article_hash(article),
      'hard_rule_receipts':len(receipts),
      'article_hard_rule_count':len([r for r in load_catalog()['rules'] if r.get('scope')=='ARTICLE' and r.get('classification')=='HARD']),
      'catalog_sha256':catalog_hash(),
      'rule_values_sha256':values_hash(),
      'html_sha256':__import__('hashlib').sha256(str(package.get('html') or '').encode('utf-8')).hexdigest(),
      'publish_allowed':False,
    }

def main():
    try:
        if len(sys.argv)==5 and sys.argv[1]=='pre':
            out=verify_pre_lt68(_load(sys.argv[2]),_load(sys.argv[3]))
            Path(sys.argv[4]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(out,ensure_ascii=False)); return
        if len(sys.argv)==6 and sys.argv[1]=='final':
            out=verify_final(_load(sys.argv[2]),_load(sys.argv[3]),_load(sys.argv[4]))
            Path(sys.argv[5]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(out,ensure_ascii=False)); return
        raise Blocked('K0_FULL_RULE_USAGE_INVALID')
    except Exception as exc:
        print(json.dumps({'contract':'K0_FULL_RULE_GATE_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False))
        raise SystemExit(2)

if __name__=='__main__':
    main()
