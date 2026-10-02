from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

class Blocked(RuntimeError):
    pass

FIVE_FIELDS=('article_type','category','plan_slot','target_keyword','title')
JOB_METADATA_CONTRACT='K10_JOB_METADATA_BINDING_V1'
JOB_METADATA_SOURCE='CURRENT_UPLOADED_WORDPRESS_INTAKE'

def _load(path):
    obj=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(obj,dict):
        raise Blocked('JSON_OBJECT_REQUIRED:'+str(path))
    return obj

def _save(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def _sha_text(value):
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

def validate_intake(intake):
    if intake.get('contract')!='PSERC_TEXTMACHINE_METADATA_BATCH_V2':
        raise Blocked('INTAKE_CONTRACT_INVALID')
    if intake.get('status')!='READY_FOR_TEXTMACHINE_METADATA_INTAKE':
        raise Blocked('INTAKE_STATUS_INVALID')
    if intake.get('content_or_format_payload_present') is not False:
        raise Blocked('INTAKE_CONTENT_PAYLOAD_FORBIDDEN')
    if intake.get('publish_allowed') is not False:
        raise Blocked('PUBLISH_ALLOWED_MUST_BE_FALSE')

    rows=intake.get('items') or []
    if not isinstance(rows,list) or not rows:
        raise Blocked('INTAKE_ITEMS_REQUIRED')
    if intake.get('item_count')!=len(rows):
        raise Blocked('INTAKE_ITEM_COUNT_MISMATCH')

    seen=set()
    for idx,item in enumerate(rows):
        if not isinstance(item,dict) or set(item)!=set(FIVE_FIELDS):
            keys=','.join(sorted(item)) if isinstance(item,dict) else 'NOT_OBJECT'
            raise Blocked('INTAKE_NOT_EXACT_FIVE_FIELDS:'+str(idx)+':'+keys)
        for key in FIVE_FIELDS:
            if not isinstance(item.get(key),str) or not item[key].strip():
                raise Blocked('INTAKE_FIELD_INVALID:'+str(idx)+':'+key)
        ident=tuple(item[k] for k in FIVE_FIELDS)
        if ident in seen:
            raise Blocked('INTAKE_DUPLICATE_ARTICLE_IDENTITY:'+str(idx))
        seen.add(ident)

    declared=str(intake.get('batch_sha256') or '')
    core=dict(intake); core.pop('batch_sha256',None)
    actual=hashlib.sha256(json.dumps(core,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
    if declared!=actual:
        raise Blocked('INTAKE_BATCH_SHA256_MISMATCH')
    return rows

def build_job_metadata_snapshot(intake):
    rows=validate_intake(intake)
    return {
      'contract':JOB_METADATA_CONTRACT,
      'source':JOB_METADATA_SOURCE,
      'source_batch_sha256':intake['batch_sha256'],
      'system_boundary':{'publish_allowed':False},
      'next_textmachine_metadata_batch':{'items':rows},
    }

def _select_current_item(rows, article):
    binding=article.get('planning_binding') or {}
    hits=[row for row in rows if all(str(binding.get(k) or '')==row[k] for k in FIVE_FIELDS)]
    if len(hits)!=1:
        raise Blocked('ARTICLE_NOT_UNIQUELY_BOUND_TO_CURRENT_UPLOADED_INTAKE:'+str(len(hits)))
    return hits[0]

def validate(run_dir, pserc_path):
    root=Path(run_dir)
    intake=_load(root/'WORDPRESS_INTAKE.json')
    research=_load(root/'RESEARCH.json')
    article=_load(root/'ARTICLE_INPUT.json')
    pserc=_load(pserc_path)

    rows=validate_intake(intake)
    expected_snapshot=build_job_metadata_snapshot(intake)
    if pserc!=expected_snapshot:
        raise Blocked('JOB_METADATA_BINDING_MISMATCH_CURRENT_UPLOAD_REQUIRED')

    item=_select_current_item(rows,article)
    binding=article.get('planning_binding') or {}
    if any(str(binding.get(k) or '')!=item[k] for k in FIVE_FIELDS):
        raise Blocked('ARTICLE_PLANNING_BINDING_MISMATCH')
    if str(article.get('article_id') or '')!=item['plan_slot']:
        raise Blocked('ARTICLE_ID_MUST_EQUAL_PLAN_SLOT')
    if article.get('publish_allowed') is not False:
        raise Blocked('ARTICLE_PUBLISH_ALLOWED_MUST_BE_FALSE')
    if pserc.get('system_boundary',{}).get('publish_allowed') is not False:
        raise Blocked('PSERC_PUBLISH_BOUNDARY_INVALID')

    if research.get('contract')!='K10_REAL_RESEARCH_V1':
        raise Blocked('RESEARCH_CONTRACT_INVALID')
    if str(research.get('article_id') or '')!=item['plan_slot']:
        raise Blocked('RESEARCH_ARTICLE_ID_MISMATCH')
    if research.get('publish_allowed') is not False:
        raise Blocked('RESEARCH_PUBLISH_ALLOWED_MUST_BE_FALSE')
    sources=research.get('sources') or []
    claims=research.get('claims') or []
    if len(sources)<2:
        raise Blocked('RESEARCH_MINIMUM_TWO_REAL_SOURCES_REQUIRED')
    if len(claims)<3:
        raise Blocked('RESEARCH_MINIMUM_THREE_BOUND_CLAIMS_REQUIRED')
    urls=set()
    for src in sources:
        if not isinstance(src,dict) or not str(src.get('title') or '').strip():
            raise Blocked('RESEARCH_SOURCE_TITLE_INVALID')
        url=str(src.get('url') or '').strip()
        if not url.startswith(('https://','http://')):
            raise Blocked('RESEARCH_SOURCE_URL_INVALID')
        urls.add(url)
    if len(urls)<2:
        raise Blocked('RESEARCH_MINIMUM_TWO_DISTINCT_URLS_REQUIRED')

    by={}
    for claim in claims:
        if not isinstance(claim,dict):
            raise Blocked('RESEARCH_CLAIM_INVALID')
        fid=str(claim.get('fact_id') or '')
        if not fid or fid in by:
            raise Blocked('RESEARCH_FACT_ID_INVALID:'+fid)
        if claim.get('claim_status')!='FULLY_SUPPORTED':
            raise Blocked('RESEARCH_CLAIM_NOT_FULLY_SUPPORTED:'+fid)
        ev=str(claim.get('evidence_text') or '')
        if not ev.strip() or _sha_text(ev)!=claim.get('evidence_text_sha256'):
            raise Blocked('RESEARCH_EVIDENCE_HASH_INVALID:'+fid)
        url=str(claim.get('source_url') or '')
        if url not in urls:
            raise Blocked('RESEARCH_CLAIM_SOURCE_NOT_REGISTERED:'+fid)
        by[fid]=claim

    article_claims=article.get('research_claims') or {}
    if set(article_claims)!=set(by):
        raise Blocked('ARTICLE_RESEARCH_FACT_SET_MISMATCH')
    for fid,claim in article_claims.items():
        src=by[fid]
        for key in ('source_title','source_url','evidence_text_sha256','statement','evidence_text','claim_status','article_types'):
            if claim.get(key)!=src.get(key):
                raise Blocked('ARTICLE_RESEARCH_BINDING_MISMATCH:'+fid+':'+key)

    html=str(article.get('html') or '')
    if not html.strip():
        raise Blocked('ARTICLE_HTML_EMPTY')
    report={
      'contract':'K10_GENERIC_PRODUCTION_ENTRY_V2',
      'status':'READY_FOR_K10_PREFLIGHT',
      'article_id':item['plan_slot'],
      'title':item['title'],
      'source_batch_item_count':len(rows),
      'source_batch_sha256':intake['batch_sha256'],
      'source_count':len(sources),
      'claim_count':len(claims),
      'metadata_authority':'CURRENT_UPLOADED_WORDPRESS_INTAKE',
      'publish_allowed':False,
    }
    return report

def main():
    if len(sys.argv)==4 and sys.argv[1]=='bind':
        try:
            intake=_load(sys.argv[2])
            snapshot=build_job_metadata_snapshot(intake)
            _save(sys.argv[3],snapshot)
            print(json.dumps({
              'contract':JOB_METADATA_CONTRACT,
              'status':'BOUND_FROM_CURRENT_UPLOADED_WORDPRESS_INTAKE',
              'item_count':len(snapshot['next_textmachine_metadata_batch']['items']),
              'source_batch_sha256':snapshot['source_batch_sha256'],
              'publish_allowed':False,
            },ensure_ascii=False,indent=2))
            raise SystemExit(0)
        except Blocked as exc:
            print(json.dumps({'contract':JOB_METADATA_CONTRACT,'status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False,indent=2))
            raise SystemExit(2)

    if len(sys.argv)!=3:
        raise SystemExit('usage: production_entry.py RUN_DIR JOB_METADATA | production_entry.py bind WORDPRESS_INTAKE OUT')
    try:
        report=validate(sys.argv[1],sys.argv[2])
        print(json.dumps(report,ensure_ascii=False,indent=2))
        raise SystemExit(0)
    except Blocked as exc:
        print(json.dumps({'contract':'K10_GENERIC_PRODUCTION_ENTRY_V2','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False,indent=2))
        raise SystemExit(2)

if __name__=='__main__':
    main()
