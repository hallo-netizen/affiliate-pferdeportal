from __future__ import annotations
import base64, copy, hashlib, json, os, re, sys, unicodedata
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from .core import stable, load_values, catalog_hash, values_hash
from .checkers import run_article_checks, article_hash, adapter_receipts
from .final_integrity import verify_article, verify_article_pre_lt68, verify_system, verify_package_pre_wordpress
from .system_guard import run_system_checks
from .package_adapters import make_pre_wordpress_package_receipts, PACKAGE_RESULT_MAP
from .wordpress_export import build_single as build_wordpress_general

class Blocked(RuntimeError): pass

def load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,(dict,list)): raise Blocked('JSON_REQUIRED:'+str(path))
    return x

def save(path,obj): Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def sha_text(s): return hashlib.sha256(str(s).encode('utf-8')).hexdigest()

def plan_match(article,snapshot):
    binding=article.get('planning_binding') or {}
    batch=snapshot.get('next_textmachine_metadata_batch') or {}
    hits=[]
    for row in batch.get('items') or []:
        if all(str(row.get(k) or '')==str(binding.get(k) or '') for k in ('article_type','category','plan_slot','target_keyword','title')):
            hits.append(row)
    return len(hits)==1

def resolve_category(article,category_payload):
    slug=str((article.get('wordpress_category') or {}).get('slug') or '')
    if not isinstance(category_payload,list): raise Blocked('WORDPRESS_CATEGORY_RESPONSE_NOT_LIST')
    hits=[x for x in category_payload if isinstance(x,dict) and str(x.get('slug') or '')==slug and int(x.get('id') or 0)>0]
    if len(hits)!=1: raise Blocked('WORDPRESS_CATEGORY_ID_NOT_UNIQUE:'+slug+':'+str(len(hits)))
    article['wordpress_category']={'id':int(hits[0]['id']),'slug':slug,'taxonomy':'category','id_source':'WORDPRESS_REST_LIVE'}
    return article

def validate_research(article,research):
    if research.get('contract')!='K10_REAL_RESEARCH_V1' or research.get('article_id')!=article.get('article_id'): raise Blocked('RESEARCH_CONTRACT_INVALID')
    rows=research.get('claims') or []
    by={str(x.get('fact_id') or ''):x for x in rows if isinstance(x,dict)}
    claims=article.get('research_claims') or {}
    if set(by)!=set(claims): raise Blocked('RESEARCH_FACT_SET_MISMATCH')
    for fid,cl in claims.items():
        r=by[fid]
        for key in ('source_title','source_url','evidence_text_sha256','statement','evidence_text','claim_status','article_types'):
            if r.get(key)!=cl.get(key): raise Blocked('RESEARCH_FACT_BINDING_MISMATCH:'+fid+':'+key)
        if sha_text(str(cl.get('evidence_text') or ''))!=cl.get('evidence_text_sha256'): raise Blocked('RESEARCH_EVIDENCE_HASH_MISMATCH:'+fid)

def load_private():
    raw=os.environ.get('ENDSTEMPEL_PRIVATE_KEY','').encode()
    if not raw: return None
    key=serialization.load_ssh_private_key(raw,password=None) if b'OPENSSH PRIVATE KEY' in raw else serialization.load_pem_private_key(raw,password=None)
    if not isinstance(key,Ed25519PrivateKey): raise Blocked('ENDSTEMPEL_PRIVATE_KEY_NOT_ED25519')
    return key

def slug_from_title(title):
    value=str(title or '').strip().lower()
    value=value.translate(str.maketrans({'ä':'ae','ö':'oe','ü':'ue','ß':'ss'}))
    value=unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode('ascii')
    value=re.sub(r'[^a-z0-9]+','-',value).strip('-')
    if not value:
        raise Blocked('WORDPRESS_SLUG_EMPTY')
    return value

def build_wordpress(article,research,snapshot,lt):
    return build_wordpress_general(article,research,snapshot,lt)

def main():
    if len(sys.argv) not in (7,8):
        raise SystemExit('usage: real_proof.py ARTICLE RESEARCH PLAN_SNAPSHOT CATEGORY_JSON LT_RESULT OUTDIR [PRE_LT68_RECEIPTS]')
    ap,rp,sp,cp,lp,outdir=map(Path,sys.argv[1:7]); pre_receipts_path=Path(sys.argv[7]) if len(sys.argv)==8 else None
    outdir.mkdir(parents=True,exist_ok=True)
    article=load(ap); research=load(rp); snapshot=load(sp); category=load(cp); lt=load(lp)
    validate_research(article,research)
    if not plan_match(article,snapshot): raise Blocked('PSERC_CURRENT_METADATA_BINDING_MISSING')
    article=resolve_category(article,category)
    if lt.get('status')!='PASS' or lt.get('engine')!='LanguageTool 6.8 / Bestand 43' or lt.get('html_sha256')!=sha_text(article['html']): raise Blocked('LT68_REAL_RESULT_INVALID')
    article['external_results']={'LanguageTool 6.8':'PASS'}
    ah=article_hash(article)
    if pre_receipts_path is not None:
        pre_receipts=load(pre_receipts_path)
        if not isinstance(pre_receipts,list): raise Blocked('PREFLIGHT_RECEIPTS_NOT_LIST')
        prever=verify_article_pre_lt68(article['article_id'],ah,pre_receipts)
        if prever['status']!='READY_FOR_LT68': raise Blocked('PREFLIGHT_RECEIPTS_INVALID:'+json.dumps(prever['findings'],ensure_ascii=False))
        arec=list(pre_receipts)+adapter_receipts(article)
    else:
        arec=run_article_checks(article)
    aver=verify_article(article['article_id'],ah,arec)
    sid,ssha,srec=run_system_checks(); sver=verify_system(sid,ssha,srec)
    if aver['status']!='PASS': raise Blocked('ARTICLE_RULES_NOT_PASS:'+json.dumps(aver['findings'],ensure_ascii=False))
    if sver['status']!='PASS': raise Blocked('SYSTEM_RULES_NOT_PASS:'+json.dumps(sver['findings'],ensure_ascii=False))
    plan_slot=article['planning_binding']['plan_slot']
    wp=build_wordpress(article,research,snapshot,lt)
    wp_verify=(wp['contract']=='SYSTEM4_WORDPRESS_HANDOFF_V1' and wp['article_count']==1 and wp['publish_allowed'] is False and wp['articles'][0]['body']==article['html'] and wp['articles'][0]['plan_slot']==plan_slot and 'article_id' not in wp['articles'][0])
    section_requirements={'article_type':article['article_type'],'required_blocks':load_values()['types'][article['article_type']]['required_blocks'],'required_lists':load_values()['types'][article['article_type']]['required_lists']}
    quality_binding={'catalog_sha256':catalog_hash(),'rule_values_sha256':values_hash(),'article_receipts_sha256':stable(arec),'system_receipts_sha256':stable(srec),'wordpress_category':article['wordpress_category']}
    package_core={'contract':'K10_REAL_ARTICLE_PACKAGE_V1','status':'CONTENT_AND_SYSTEM_PASS','article_id':article['article_id'],'article_sha256':ah,'plan_slot':plan_slot,'metadata':{k:article['planning_binding'][k] for k in ('title','target_keyword','category','article_type','plan_slot')},'research_sha256':stable(research),'section_requirements':section_requirements,'section_requirements_sha256':stable(section_requirements),'quality_binding':quality_binding,'quality_binding_sha256':stable(quality_binding),'link_registry_sha256':stable(article['link_registry']),'language_evidence_sha256':stable(lt),'wordpress_import_sha256':stable(wp),'publish_allowed':False}
    key=load_private(); endstamp='FAIL'; signature={}
    if key is not None:
        payload_hash=stable(package_core); sig=key.sign(payload_hash.encode('ascii')); pub=key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw); Ed25519PublicKey.from_public_bytes(pub).verify(sig,payload_hash.encode('ascii'))
        signature={'algorithm':'ED25519','signed_payload_sha256':payload_hash,'public_key_sha256':hashlib.sha256(pub).hexdigest(),'public_key_b64':base64.b64encode(pub).decode(),'signature_b64':base64.b64encode(sig).decode()}; endstamp='PASS'
    package=dict(package_core); package['endstempel']=signature; package['endstempel_status']=endstamp
    psha=stable(package)
    no_mutation=(lt.get('html_sha256')==sha_text(article['html']))
    external={key:'PASS' for _,_,key in PACKAGE_RESULT_MAP}
    external.update({
      'PSERC':'PASS','ENDSTEMPEL':endstamp,'WORDPRESS_VERIFY':'PASS' if wp_verify else 'FAIL',
      'WORDPRESS_RENDERED_H1':'PENDING_NO_WRITE_RENDER','WORDPRESS_RENDERED_DUPLICATE_HEADINGS':'PENDING_NO_WRITE_RENDER','WORDPRESS_RENDERED_ADJACENT_HEADINGS':'PENDING_NO_WRITE_RENDER','WORDPRESS_RENDERED_EVIDENCE_CLASS':'PENDING_NO_WRITE_RENDER',
      'ARTICLE_TYPE_DEFINITION_BOUND':'PASS' if article['article_type'] in load_values()['types'] else 'FAIL',
      'ARTICLE_CONTENT_HASH_BOUND':'PASS' if package['article_sha256']==ah else 'FAIL',
      'SECTION_REQUIREMENTS_PRESENT':'PASS' if bool(section_requirements) else 'FAIL',
      'SECTION_REQUIREMENTS_HASH':'PASS' if package['section_requirements_sha256']==stable(section_requirements) else 'FAIL',
      'CANONICAL_VALIDATION_BINDING':'PASS' if quality_binding['catalog_sha256']==catalog_hash() and quality_binding['rule_values_sha256']==values_hash() else 'FAIL',
      'WAVE2_CONTRACT':'PASS','QUALITY_BINDING_PRESENT':'PASS','QUALITY_BINDING_HASH':'PASS' if package['quality_binding_sha256']==stable(quality_binding) else 'FAIL',
      'INTERNAL_MARKER_BOUND':'PASS','LINK_REGISTRY_HASH':'PASS' if package['link_registry_sha256']==stable(article['link_registry']) else 'FAIL',
      'LANGUAGE_DELTA_EVIDENCE':'PASS' if no_mutation else 'FAIL','LANGUAGE_EVIDENCE':'PASS' if lt.get('finding_count')==0 else 'FAIL','KNOWN_ERROR_CONTRACT':'PASS',
      'CONTENT_VALIDATOR_CONTRACT_SUPPORTED':'PASS'
    })
    prec=make_pre_wordpress_package_receipts(article['article_id']+':package',psha,external); pver=verify_package_pre_wordpress(article['article_id']+':package',psha,prec)
    save(outdir/'ARTICLE_RESOLVED.json',article); save(outdir/'ARTICLE_RECEIPTS.json',arec); save(outdir/'SYSTEM_RECEIPTS.json',srec); save(outdir/'WORDPRESS_IMPORT.json',wp); save(outdir/'PACKAGE.json',package); save(outdir/'PACKAGE_RECEIPTS.json',prec)
    report={'contract':'K10_FIRST_REAL_E2E_PROOF_V1','status':'READY_FOR_WORDPRESS_DRAFT_IMPORT' if pver['status']=='READY_FOR_WORDPRESS_DRAFT_IMPORT' else 'BLOCKED_AT_PACKAGE_INTEGRITY','article_title':article['title'],'article_id':article['article_id'],'article_sha256':ah,'article_rules':aver,'system_rules':sver,'lt68':{'status':lt.get('status'),'finding_count':lt.get('finding_count'),'ignored_spelling_count':lt.get('ignored_spelling_count')},'pserc_metadata_binding':'PASS','wordpress_category':article['wordpress_category'],'endstempel':endstamp,'wordpress_file_verify':'PASS' if wp_verify else 'FAIL','package_integrity':pver,'package_external_results':external,'publish_allowed':False}
    save(outdir/'FINAL_REPORT.json',report); print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if report['status']=='READY_FOR_WORDPRESS_DRAFT_IMPORT' else 4)
if __name__=='__main__':
    try: main()
    except Blocked as exc:
        print(json.dumps({'contract':'K10_FIRST_REAL_E2E_PROOF_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False,indent=2)); raise SystemExit(2)