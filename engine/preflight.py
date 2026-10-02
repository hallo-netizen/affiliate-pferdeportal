from __future__ import annotations
import copy, html, json, re, sys
from pathlib import Path
from .core import load_values
from .checkers import run_article_content_checks, article_hash
from .final_integrity import verify_article_pre_lt68

class Blocked(RuntimeError): pass

def _load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,(dict,list)): raise Blocked('JSON_REQUIRED:'+str(path))
    return x

def _save(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def resolve_category(article,category_payload):
    slug=str((article.get('wordpress_category') or {}).get('slug') or '')
    if not isinstance(category_payload,list): raise Blocked('WORDPRESS_CATEGORY_RESPONSE_NOT_LIST')
    hits=[x for x in category_payload if isinstance(x,dict) and str(x.get('slug') or '')==slug and int(x.get('id') or 0)>0]
    if len(hits)!=1: raise Blocked('WORDPRESS_CATEGORY_ID_NOT_UNIQUE:'+slug+':'+str(len(hits)))
    out=copy.deepcopy(article)
    out['wordpress_category']={'id':int(hits[0]['id']),'slug':slug,'taxonomy':'category','id_source':'WORDPRESS_REST_LIVE'}
    return out

def _trace(fid,claim):
    return '<span class="ppm-source-trace" data-fact-id="'+html.escape(str(fid),quote=True)+'" data-source-title="'+html.escape(str(claim.get('source_title') or ''),quote=True)+'" data-source-hash="'+html.escape(str(claim.get('evidence_text_sha256') or ''),quote=True)+'"></span>'

def _fact_ids(value):
    out=[]
    for raw in re.findall(r'data-fact-ids\s*=\s*["\']([^"\']+)["\']',str(value or ''),re.I):
        for fid in raw.split():
            if fid not in out: out.append(fid)
    return out

def _trace_ids(value):
    out=[]
    for tag in re.findall(r'(?is)<span\b[^>]*class\s*=\s*["\'][^"\']*\bppm-source-trace\b[^"\']*["\'][^>]*>',str(value or '')):
        m=re.search(r'data-fact-id\s*=\s*["\']([^"\']+)["\']',tag,re.I)
        if m and m.group(1) not in out: out.append(m.group(1))
    return out

def _insert_into_first_factual_unit(body, trace_markup):
    pat=re.compile(r'(?is)<(p|li|td)\b([^>]*data-fact-ids\s*=\s*["\'][^"\']+["\'][^>]*)>')
    m=pat.search(body)
    if not m: return body,False
    return body[:m.end()]+trace_markup+body[m.end():],True

def materialize_trace_bindings(article):
    out=copy.deepcopy(article)
    claims=out.get('research_claims') or {}
    cfg=load_values()
    required=set((cfg['types'].get(out.get('article_type')) or {}).get('fact_trace_required_blocks') or [])
    minimum=int(cfg['global']['source_trace']['minimum_count'])
    inserted=[]

    secpat=re.compile(r'(?is)(<section\b([^>]*)>)(.*?)(</section>)')
    def first_pass(m):
        open_tag,attrs,body,close=m.group(1),m.group(2),m.group(3),m.group(4)
        bm=re.search(r'data-block\s*=\s*["\']([^"\']+)["\']',attrs,re.I)
        block=bm.group(1) if bm else ''
        used=_fact_ids(body); existing=_trace_ids(body)
        desired=[]
        if block=='conclusion':
            desired=[fid for fid in used if fid not in existing]
        elif block in required and used and not existing:
            desired=[used[0]]
        marks=[]
        for fid in desired:
            cl=claims.get(fid)
            if isinstance(cl,dict):
                marks.append(_trace(fid,cl)); inserted.append({'block':block,'fact_id':fid,'reason':'conclusion_all' if block=='conclusion' else 'required_block'})
        if marks:
            body,ok=_insert_into_first_factual_unit(body,''.join(marks))
            if not ok:
                for row in desired:
                    inserted[:] = [x for x in inserted if not (x['block']==block and x['fact_id']==row)]
        return open_tag+body+close

    out['html']=secpat.sub(first_pass,str(out.get('html') or ''))

    # Fill the existing global minimum with real already-bound claims only.
    while len(_trace_ids(out['html']))<minimum:
        changed=False
        def fill_one(m):
            nonlocal changed
            if changed: return m.group(0)
            open_tag,attrs,body,close=m.group(1),m.group(2),m.group(3),m.group(4)
            bm=re.search(r'data-block\s*=\s*["\']([^"\']+)["\']',attrs,re.I)
            block=bm.group(1) if bm else ''
            used=_fact_ids(body); existing=_trace_ids(body)
            for fid in used:
                if fid in existing or not isinstance(claims.get(fid),dict): continue
                body2,ok=_insert_into_first_factual_unit(body,_trace(fid,claims[fid]))
                if ok:
                    inserted.append({'block':block,'fact_id':fid,'reason':'global_minimum'})
                    changed=True
                    return open_tag+body2+close
            return m.group(0)
        out['html']=secpat.sub(fill_one,out['html'])
        if not changed: break

    return out,{'inserted':inserted,'inserted_count':len(inserted),'visible_text_changed':False}

def preflight_article(article):
    prepared,binding=materialize_trace_bindings(article)
    receipts=run_article_content_checks(prepared)
    verification=verify_article_pre_lt68(prepared['article_id'],article_hash(prepared),receipts)
    report={
      'contract':'K10_ARTICLE_PREFLIGHT_V1',
      'status':verification['status'],
      'article_id':prepared['article_id'],
      'article_sha256':article_hash(prepared),
      'receipt_count':len(receipts),
      'trace_materialization':binding,
      'verification':verification,
      'publish_allowed':False,
    }
    return prepared,receipts,report

def main():
    if len(sys.argv)!=4:
        raise SystemExit('usage: preflight.py ARTICLE CATEGORY_JSON OUTDIR')
    article_path,category_path,outdir=map(Path,sys.argv[1:])
    outdir.mkdir(parents=True,exist_ok=True)
    try:
        article=_load(article_path); category=_load(category_path)
        resolved=resolve_category(article,category)
        prepared,receipts,report=preflight_article(resolved)
        _save(outdir/'ARTICLE_PREPARED.json',prepared)
        _save(outdir/'ARTICLE_RECEIPTS_PRE_LT68.json',receipts)
        _save(outdir/'PREFLIGHT_REPORT.json',report)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        raise SystemExit(0 if report['status']=='READY_FOR_LT68' else 4)
    except Blocked as exc:
        report={'contract':'K10_ARTICLE_PREFLIGHT_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False}
        _save(outdir/'PREFLIGHT_REPORT.json',report)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        raise SystemExit(2)

if __name__=='__main__':
    main()
