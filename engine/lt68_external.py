from __future__ import annotations
import copy, hashlib, html, json, re, subprocess, sys, tempfile
from pathlib import Path

JAR_SHA256='2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8'
ENGINE='LanguageTool 6.8 / Bestand 43'

class Blocked(RuntimeError): pass

def sha_bytes(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def sha_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def visible_text(article_html:str)->str:
    rows=[]
    for m in re.finditer(r'<(h2|p|li|th|td|small)\b[^>]*>(.*?)</\1>',article_html,re.I|re.S):
        value=html.unescape(m.group(2))
        value=re.sub(r'<[^>]+>',' ',value)
        value=re.sub(r'\s+',' ',value).strip()
        value=re.sub(r'\s+([.,;:!?])',r'\1',value)
        if value: rows.append(value)
    return '\n\n'.join(rows)

def _invoke(jar:Path,checked:str)->dict:
    with tempfile.TemporaryDirectory(prefix='k10-lt68-') as td:
        pth=Path(td)/'visible.txt'
        pth.write_text(checked,encoding='utf-8')
        p=subprocess.run(['java','-Xmx1024m','-jar',str(jar),'--json','-l','de-DE',str(pth)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120,check=False)
    if p.returncode!=0: raise Blocked('LT68_EXECUTION_FAILED:'+(p.stderr or p.stdout)[:300])
    try: raw=json.loads(p.stdout)
    except Exception as exc: raise Blocked('LT68_REPORT_INVALID') from exc
    return raw

def _filter_matches(article,checked,matches):
    terms={str(x).strip().casefold() for x in article.get('lt_authoritative_terms') or [] if str(x).strip()}
    kept=[]; ignored=[]
    for m in matches:
        rule=m.get('rule') if isinstance(m,dict) and isinstance(m.get('rule'),dict) else {}
        rid=str(rule.get('id') or '')
        off=m.get('offset'); ln=m.get('length'); token=''
        if isinstance(off,int) and isinstance(ln,int) and 0<=off<=len(checked) and 0<=ln and off+ln<=len(checked): token=checked[off:off+ln]
        exact=bool(re.fullmatch(r'[A-Za-zÄÖÜäöüß-]+',token or ''))
        if rid=='GERMAN_SPELLER_RULE' and exact and token.casefold() in terms:
            ignored.append({'rule_id':rid,'token':token,'offset':off,'length':ln})
        else:
            kept.append(m)
    return kept,ignored

def _report(article,body,checked,raw,matches,actual):
    kept,ignored=_filter_matches(article,checked,matches)
    filtered={'matches':kept,'language':raw.get('language'),'software':raw.get('software'),'warnings':raw.get('warnings',{})}
    report_json=json.dumps(filtered,ensure_ascii=False,separators=(',',':'))
    return {
        'contract':'K10_LT68_RESULT_V1','engine':ENGINE,'status':'PASS' if not kept else 'REPAIR_REQUIRED',
        'jar_sha256':actual,'article_id':article.get('article_id'),'html_sha256':sha_bytes(body.encode('utf-8')),'checked_text_sha256':sha_bytes(checked.encode('utf-8')),
        'return_code':0,'finding_count':len(kept),'ignored_spelling_count':len(ignored),'ignored_spelling':ignored,
        'findings':[{'rule_id':str((x.get('rule') or {}).get('id') or ''),'message':str(x.get('message') or ''),'offset':x.get('offset'),'length':x.get('length'),'context':str((x.get('context') or {}).get('text') or '')} for x in kept],
        'raw_report_json':report_json,'raw_report_sha256':sha_bytes(report_json.encode('utf-8')),'publish_allowed':False,
    }

def run_many(jar:Path,article_paths:list[Path])->list[dict]:
    if not jar.is_file(): raise Blocked('LT68_JAR_MISSING')
    actual=sha_file(jar)
    if actual!=JAR_SHA256: raise Blocked('LT68_JAR_HASH_MISMATCH:'+actual)
    items=[]
    cursor=0
    pieces=[]
    for idx,path in enumerate(article_paths):
        article=json.loads(Path(path).read_text(encoding='utf-8'))
        body=str(article.get('html') or '')
        if not body: raise Blocked('ARTICLE_HTML_EMPTY:'+str(path))
        checked=visible_text(body)
        if not checked: raise Blocked('LT68_VISIBLE_TEXT_EMPTY:'+str(path))
        if idx:
            pieces.append('\n\n'); cursor+=2
        start=cursor; pieces.append(checked); cursor+=len(checked); end=cursor
        items.append({'article':article,'body':body,'checked':checked,'start':start,'end':end,'path':str(path)})
    combined=''.join(pieces)
    raw=_invoke(jar,combined)
    buckets=[[] for _ in items]
    for original in raw.get('matches') or []:
        off=original.get('offset'); ln=original.get('length')
        if not isinstance(off,int) or not isinstance(ln,int): raise Blocked('LT68_MATCH_OFFSET_INVALID')
        owner=None
        for i,item in enumerate(items):
            if item['start']<=off and off+ln<=item['end']:
                owner=i; break
        if owner is None: raise Blocked('LT68_BATCH_CROSS_BOUNDARY_FINDING:'+str(off)+':'+str(ln))
        m=copy.deepcopy(original); m['offset']=off-items[owner]['start']
        buckets[owner].append(m)
    return [_report(item['article'],item['body'],item['checked'],raw,buckets[i],actual) for i,item in enumerate(items)]

def run(jar:Path,article_path:Path)->dict:
    return run_many(jar,[article_path])[0]

def _save(path,report):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def main():
    try:
        if len(sys.argv)>=2 and sys.argv[1]=='--batch':
            if len(sys.argv)!=4: raise SystemExit('usage: lt68_external.py --batch JAR MANIFEST')
            jar=Path(sys.argv[2]); manifest=json.loads(Path(sys.argv[3]).read_text(encoding='utf-8'))
            if manifest.get('contract')!='K10_LT68_BATCH_MANIFEST_V1': raise Blocked('LT68_BATCH_MANIFEST_INVALID')
            rows=manifest.get('items') or []
            if not rows: raise Blocked('LT68_BATCH_EMPTY')
            reports=run_many(jar,[Path(x['article']) for x in rows])
            for row,rep in zip(rows,reports): _save(row['output'],rep)
            summary={'contract':'K10_LT68_BATCH_RESULT_V1','status':'PASS' if all(x['status']=='PASS' for x in reports) else 'REPAIR_REQUIRED','article_count':len(reports),'java_process_count':1,'items':[{'article_id':x.get('article_id'),'status':x.get('status'),'finding_count':x.get('finding_count')} for x in reports],'publish_allowed':False}
            print(json.dumps(summary,ensure_ascii=False,indent=2))
            raise SystemExit(0 if summary['status']=='PASS' else 3)
        if len(sys.argv)!=4: raise SystemExit('usage: lt68_external.py JAR ARTICLE OUT')
        jar=Path(sys.argv[1]); article=Path(sys.argv[2]); out=Path(sys.argv[3])
        r=run(jar,article); _save(out,r); print(json.dumps(r,ensure_ascii=False,indent=2))
        raise SystemExit(0 if r['status']=='PASS' else 3)
    except Blocked as exc:
        r={'contract':'K10_LT68_RESULT_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False}
        if len(sys.argv)==4 and sys.argv[1]!='--batch':
            _save(sys.argv[3],r)
        print(json.dumps(r,ensure_ascii=False,indent=2))
        raise SystemExit(2)

if __name__=='__main__':
    main()
