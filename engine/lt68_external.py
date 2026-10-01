from __future__ import annotations
import hashlib, html, json, re, subprocess, sys
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

def run(jar:Path,article_path:Path)->dict:
    if not jar.is_file(): raise Blocked('LT68_JAR_MISSING')
    actual=sha_file(jar)
    if actual!=JAR_SHA256: raise Blocked('LT68_JAR_HASH_MISMATCH:'+actual)
    article=json.loads(article_path.read_text(encoding='utf-8'))
    body=str(article.get('html') or '')
    if not body: raise Blocked('ARTICLE_HTML_EMPTY')
    checked=visible_text(body)
    if not checked: raise Blocked('LT68_VISIBLE_TEXT_EMPTY')
    tmp=article_path.parent/'_lt_visible.txt'; tmp.write_text(checked,encoding='utf-8')
    p=subprocess.run(['java','-Xmx1024m','-jar',str(jar),'--json','-l','de-DE',str(tmp)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120,check=False)
    if p.returncode!=0: raise Blocked('LT68_EXECUTION_FAILED:'+(p.stderr or p.stdout)[:300])
    try: raw=json.loads(p.stdout)
    except Exception as exc: raise Blocked('LT68_REPORT_INVALID') from exc
    terms={str(x).strip().casefold() for x in article.get('lt_authoritative_terms') or [] if str(x).strip()}
    kept=[]; ignored=[]
    for m in raw.get('matches') or []:
        rule=m.get('rule') if isinstance(m,dict) and isinstance(m.get('rule'),dict) else {}
        rid=str(rule.get('id') or '')
        off=m.get('offset'); ln=m.get('length'); token=''
        if isinstance(off,int) and isinstance(ln,int) and 0<=off<=len(checked) and 0<=ln and off+ln<=len(checked): token=checked[off:off+ln]
        exact=bool(re.fullmatch(r'[A-Za-zÄÖÜäöüß-]+',token or ''))
        if rid=='GERMAN_SPELLER_RULE' and exact and token.casefold() in terms:
            ignored.append({'rule_id':rid,'token':token,'offset':off,'length':ln})
        else:
            kept.append(m)
    html_sha=sha_bytes(body.encode('utf-8'))
    checked_sha=sha_bytes(checked.encode('utf-8'))
    filtered={'matches':kept,'language':raw.get('language'),'software':raw.get('software'),'warnings':raw.get('warnings',{})}
    report_json=json.dumps(filtered,ensure_ascii=False,separators=(',',':'))
    return {
        'contract':'K10_LT68_RESULT_V1','engine':ENGINE,'status':'PASS' if not kept else 'REPAIR_REQUIRED',
        'jar_sha256':actual,'article_id':article.get('article_id'),'html_sha256':html_sha,'checked_text_sha256':checked_sha,
        'return_code':p.returncode,'finding_count':len(kept),'ignored_spelling_count':len(ignored),'ignored_spelling':ignored,
        'findings':[{'rule_id':str((x.get('rule') or {}).get('id') or ''),'message':str(x.get('message') or ''),'offset':x.get('offset'),'length':x.get('length'),'context':str((x.get('context') or {}).get('text') or '')} for x in kept],
        'raw_report_json':report_json,'raw_report_sha256':sha_bytes(report_json.encode('utf-8')),'publish_allowed':False,
    }

def main():
    jar=Path(sys.argv[1]); article=Path(sys.argv[2]); out=Path(sys.argv[3])
    try: r=run(jar,article)
    except Exception as exc:
        r={'contract':'K10_LT68_RESULT_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False}; out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(r,ensure_ascii=False,indent=2)); raise SystemExit(2)
    out.write_text(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(r,ensure_ascii=False,indent=2))
    raise SystemExit(0 if r['status']=='PASS' else 3)
if __name__=='__main__': main()