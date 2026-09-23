from __future__ import annotations
import hashlib, html, json, re, urllib.request, urllib.error
from urllib.parse import urlparse
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Callable

CONTRACT='SYSTEM4_MACHINE_SOURCE_REQUEST_BATCH_V1'
RESULT_CONTRACT='SYSTEM4_MACHINE_ACQUIRED_SOURCE_BATCH_V1'
FORBIDDEN_RESEARCH_HOST='pferde-atelier.de'
class SourceAcquisitionError(RuntimeError): pass

class _TextExtractor(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.skip=0; self.parts=[]; self.title=[]; self.in_title=False
    def handle_starttag(self,tag,attrs):
        t=tag.lower()
        if t in {'script','style','noscript','svg'}: self.skip+=1
        if t=='title': self.in_title=True
        if t in {'p','li','h1','h2','h3','h4','h5','h6','td','th','br','div','section','article'} and not self.skip: self.parts.append('\n')
    def handle_endtag(self,tag):
        t=tag.lower()
        if t in {'script','style','noscript','svg'} and self.skip: self.skip-=1
        if t=='title': self.in_title=False
    def handle_data(self,data):
        if self.skip: return
        if self.in_title: self.title.append(data)
        self.parts.append(data)

def _normalize_text(raw:bytes, content_type:str='')->tuple[str,str]:
    enc='utf-8'
    m=re.search(r'charset=([\w.-]+)',content_type or '',re.I)
    if m: enc=m.group(1)
    try: text=raw.decode(enc,errors='replace')
    except LookupError: text=raw.decode('utf-8',errors='replace')
    if '<html' in text[:5000].lower() or 'text/html' in (content_type or '').lower():
        parser=_TextExtractor(); parser.feed(text)
        evidence=' '.join(''.join(parser.parts).split())
        title=' '.join(''.join(parser.title).split())
    else:
        evidence=' '.join(html.unescape(text).split()); title=''
    return evidence,title

def _default_fetch(url:str, timeout:float, max_bytes:int)->dict:
    req=urllib.request.Request(url,headers={'User-Agent':'Pferde-Atelier-System4-SourceLoader/1.0','Accept':'text/html,text/plain,application/xhtml+xml;q=0.9,*/*;q=0.1'})
    try:
        with urllib.request.urlopen(req,timeout=timeout) as resp:
            status=int(getattr(resp,'status',200)); ctype=str(resp.headers.get('Content-Type','')); raw=resp.read(max_bytes+1)
    except urllib.error.HTTPError as e:
        return {'http_status':int(e.code),'body':b'','content_type':str(e.headers.get('Content-Type','')) if e.headers else ''}
    except Exception as e: raise SourceAcquisitionError('SOURCE_FETCH_RUNTIME_FAIL:'+url+':'+type(e).__name__) from e
    if len(raw)>max_bytes: raise SourceAcquisitionError('SOURCE_TOO_LARGE:'+url)
    return {'http_status':status,'body':raw,'content_type':ctype}

def acquire_batch(request_batch:dict, *, fetcher:Callable[[str,float,int],dict]|None=None, retrieved_at:str|None=None, timeout:float=20.0, max_bytes:int=1_000_000)->dict:
    if not isinstance(request_batch,dict) or request_batch.get('contract')!=CONTRACT: raise SourceAcquisitionError('SOURCE_REQUEST_CONTRACT_INVALID')
    items=request_batch.get('items')
    if not isinstance(items,list) or not items or request_batch.get('item_count')!=len(items): raise SourceAcquisitionError('SOURCE_REQUEST_ITEMS_INVALID')
    fetch=fetcher or _default_fetch
    stamp=retrieved_at or datetime.now(timezone.utc).isoformat()
    out=[]
    for i,item in enumerate(items):
        if not isinstance(item,dict) or item.get('item_index')!=i or not isinstance(item.get('plan_slot'),str) or not item['plan_slot']: raise SourceAcquisitionError('SOURCE_REQUEST_ITEM_BINDING_INVALID:'+str(i))
        requests=item.get('sources')
        if not isinstance(requests,list) or not requests: raise SourceAcquisitionError('SOURCE_REQUEST_POOL_EMPTY:'+str(i))
        seen=set(); rows=[]
        for j,row in enumerate(requests):
            if not isinstance(row,dict): raise SourceAcquisitionError(f'SOURCE_REQUEST_INVALID:{i}:{j}')
            sid=str(row.get('source_id') or '').strip(); url=str(row.get('source_url') or '').strip(); declared_title=str(row.get('source_title') or '').strip()
            if not sid or sid in seen: raise SourceAcquisitionError(f'SOURCE_REQUEST_ID_INVALID:{i}:{j}')
            seen.add(sid)
            if not re.match(r'^https?://',url): raise SourceAcquisitionError(f'SOURCE_REQUEST_URL_INVALID:{i}:{j}')
            host=(urlparse(url).hostname or '').strip().rstrip('.').casefold()
            if host==FORBIDDEN_RESEARCH_HOST or host.endswith('.'+FORBIDDEN_RESEARCH_HOST):
                raise SourceAcquisitionError(f'SOURCE_REQUEST_OWN_DOMAIN_FORBIDDEN:{i}:{j}')
            result=fetch(url,timeout,max_bytes); status=int(result.get('http_status',0))
            if status<200 or status>=300: raise SourceAcquisitionError(f'SOURCE_HTTP_FAIL:{i}:{j}:{status}')
            evidence,title_from_body=_normalize_text(result.get('body',b''),str(result.get('content_type','')))
            if len(evidence)<20: raise SourceAcquisitionError(f'SOURCE_EVIDENCE_EMPTY:{i}:{j}')
            title=declared_title or title_from_body
            if not title: raise SourceAcquisitionError(f'SOURCE_TITLE_MISSING:{i}:{j}')
            rows.append({'source_id':sid,'source_title':title,'source_url':url,'retrieved_at':stamp,'evidence':evidence,'snapshot_sha256':hashlib.sha256(evidence.encode()).hexdigest(),'http_status':status,'source_kind':str(row.get('source_kind') or 'WEB').strip() or 'WEB'})
        out.append({'item_index':i,'plan_slot':item['plan_slot'],'sources':rows})
    return {'contract':RESULT_CONTRACT,'item_count':len(out),'items':out}
