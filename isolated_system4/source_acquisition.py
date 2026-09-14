from __future__ import annotations

import base64
import hashlib
import html
import ipaddress
import json
import os
import re
import socket
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Callable

CONTRACT='SYSTEM4_MACHINE_SOURCE_ACQUISITION_V1'
PROVIDER='DATAFORSEO_GOOGLE_ORGANIC_LIVE_ADVANCED'
ENDPOINT='https://api.dataforseo.com/v3/serp/google/organic/live/advanced'
LOCATION_CODE=2276
LANGUAGE_CODE='de'
MIN_SOURCES=3
MAX_SOURCES=12
MAX_FETCH_BYTES=1_500_000
MIN_EVIDENCE_CHARS=400
OWN_HOSTS={'pferde-atelier.de','www.pferde-atelier.de'}

class SourceAcquisitionError(RuntimeError):pass

def canon(v)->bytes:return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def sha256_bytes(v:bytes)->str:return hashlib.sha256(v).hexdigest()
def sha256_text(v:str)->str:return sha256_bytes(v.encode('utf-8'))

def _public_url(url:str,resolver:Callable=socket.getaddrinfo)->str:
    try:p=urllib.parse.urlsplit(url)
    except Exception as exc:raise SourceAcquisitionError('SOURCE_URL_INVALID') from exc
    if p.scheme not in {'http','https'} or not p.hostname or p.username or p.password:raise SourceAcquisitionError('SOURCE_URL_INVALID')
    host=p.hostname.lower().rstrip('.')
    if host in OWN_HOSTS or host.endswith('.pferde-atelier.de'):raise SourceAcquisitionError('SOURCE_URL_OWN_DOMAIN_BLOCKED')
    if host in {'localhost','localhost.localdomain'} or host.endswith('.localhost'):raise SourceAcquisitionError('SOURCE_URL_PRIVATE_HOST_BLOCKED')
    try:rows=resolver(host,p.port or (443 if p.scheme=='https' else 80),type=socket.SOCK_STREAM)
    except Exception as exc:raise SourceAcquisitionError('SOURCE_HOST_RESOLUTION_FAILED') from exc
    addresses={row[4][0] for row in rows if row and len(row)>4 and row[4]}
    if not addresses:raise SourceAcquisitionError('SOURCE_HOST_RESOLUTION_EMPTY')
    for raw in addresses:
        try:addr=ipaddress.ip_address(raw)
        except ValueError as exc:raise SourceAcquisitionError('SOURCE_HOST_ADDRESS_INVALID') from exc
        if not addr.is_global:raise SourceAcquisitionError('SOURCE_URL_PRIVATE_ADDRESS_BLOCKED')
    return urllib.parse.urlunsplit((p.scheme,p.netloc,p.path or '/',p.query,''))

class _TextExtractor(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag.lower() in {'script','style','noscript','svg','template'}:self.skip+=1
    def handle_endtag(self,tag):
        if tag.lower() in {'script','style','noscript','svg','template'} and self.skip:self.skip-=1
    def handle_data(self,data):
        if not self.skip and data.strip():self.parts.append(data)

def normalize_content(raw:bytes,content_type:str)->str:
    if len(raw)>MAX_FETCH_BYTES:raise SourceAcquisitionError('SOURCE_BODY_TOO_LARGE')
    lower=(content_type or '').lower()
    if not any(token in lower for token in ('text/html','application/xhtml+xml','text/plain')):raise SourceAcquisitionError('SOURCE_CONTENT_TYPE_BLOCKED')
    text=raw.decode('utf-8','replace')
    if 'html' in lower or 'xhtml' in lower:
        parser=_TextExtractor();parser.feed(text);text=' '.join(parser.parts)
    text=html.unescape(text);text=re.sub(r'\s+',' ',text).strip()
    if len(text)<MIN_EVIDENCE_CHARS:raise SourceAcquisitionError('SOURCE_EVIDENCE_TOO_SHORT')
    return text

def _default_page_fetch(url:str)->tuple[int,str,bytes,str]:
    safe=_public_url(url)
    req=urllib.request.Request(safe,headers={'User-Agent':'PferdeAtelier-System4-SourceTransport/1.0','Accept':'text/html,application/xhtml+xml,text/plain;q=0.9'})
    with urllib.request.urlopen(req,timeout=20) as r:
        final=_public_url(r.geturl())
        status=int(getattr(r,'status',0) or r.getcode() or 0)
        ctype=str(r.headers.get('Content-Type','')).split(';',1)[0].strip().lower()
        raw=r.read(MAX_FETCH_BYTES+1)
    if status<200 or status>=300:raise SourceAcquisitionError('SOURCE_HTTP_STATUS:'+str(status))
    return status,ctype,raw,final

def _default_serp_fetch(keyword:str,login:str,password:str)->dict:
    if not login or not password:raise SourceAcquisitionError('DATAFORSEO_CREDENTIALS_MISSING')
    payload=[{'keyword':keyword,'location_code':LOCATION_CODE,'language_code':LANGUAGE_CODE,'depth':100}]
    auth=base64.b64encode((login+':'+password).encode('utf-8')).decode('ascii')
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload,ensure_ascii=False).encode('utf-8'),headers={'Authorization':'Basic '+auth,'Content-Type':'application/json','Accept':'application/json','User-Agent':'PferdeAtelier-System4-SourceTransport/1.0'},method='POST')
    with urllib.request.urlopen(req,timeout=30) as r:
        raw=r.read(5_000_001)
        if len(raw)>5_000_000:raise SourceAcquisitionError('DATAFORSEO_RESPONSE_TOO_LARGE')
        if int(getattr(r,'status',0) or r.getcode() or 0)!=200:raise SourceAcquisitionError('DATAFORSEO_HTTP_FAIL')
    try:return json.loads(raw.decode('utf-8'))
    except Exception as exc:raise SourceAcquisitionError('DATAFORSEO_JSON_INVALID') from exc

def organic_candidates(response:dict)->list[dict]:
    if not isinstance(response,dict) or response.get('status_code')!=20000:raise SourceAcquisitionError('DATAFORSEO_RESPONSE_NOT_OK')
    tasks=response.get('tasks')
    if not isinstance(tasks,list) or len(tasks)!=1 or not isinstance(tasks[0],dict):raise SourceAcquisitionError('DATAFORSEO_TASK_INVALID')
    if tasks[0].get('status_code')!=20000:raise SourceAcquisitionError('DATAFORSEO_TASK_NOT_OK')
    results=tasks[0].get('result')
    if not isinstance(results,list) or not results or not isinstance(results[0],dict):raise SourceAcquisitionError('DATAFORSEO_RESULT_INVALID')
    items=results[0].get('items')
    if not isinstance(items,list):raise SourceAcquisitionError('DATAFORSEO_ITEMS_INVALID')
    rows=[]
    for item in items:
        if not isinstance(item,dict) or item.get('type')!='organic':continue
        url=str(item.get('url') or '').strip();title=str(item.get('title') or '').strip();domain=str(item.get('domain') or '').strip().lower()
        try:rank=int(item.get('rank_absolute') or item.get('rank_group') or 999999)
        except Exception:rank=999999
        if url and title:rows.append({'url':url,'title':title,'domain':domain,'rank_absolute':rank,'rank_group':int(item.get('rank_group') or rank)})
    rows.sort(key=lambda row:(row['rank_absolute'],row['rank_group'],row['url']))
    return rows

def acquire(keyword:str,*,login:str|None=None,password:str|None=None,serp_fetch:Callable|None=None,page_fetch:Callable|None=None,resolver:Callable=socket.getaddrinfo)->dict:
    keyword=' '.join(str(keyword or '').split())
    if not keyword:raise SourceAcquisitionError('SOURCE_KEYWORD_EMPTY')
    login=login if login is not None else os.environ.get('DATAFORSEO_LOGIN','')
    password=password if password is not None else os.environ.get('DATAFORSEO_PASSWORD','')
    provider=(serp_fetch or _default_serp_fetch)(keyword,login,password)
    candidates=organic_candidates(provider)
    fetch=page_fetch or _default_page_fetch
    sources=[];failures=[];seen_urls=set();seen_hosts=set()
    for row in candidates:
        if len(sources)>=MAX_SOURCES:break
        try:
            safe=_public_url(row['url'],resolver=resolver)
            host=(urllib.parse.urlsplit(safe).hostname or '').lower()
            key=safe.rstrip('/')
            if key in seen_urls or host in seen_hosts:continue
            status,ctype,raw,final=fetch(safe)
            final=_public_url(final,resolver=resolver)
            final_host=(urllib.parse.urlsplit(final).hostname or '').lower()
            if final_host in seen_hosts:continue
            if status<200 or status>=300:raise SourceAcquisitionError('SOURCE_HTTP_STATUS:'+str(status))
            evidence=normalize_content(raw,ctype)
            source_id='src-'+sha256_text(final)[:16]
            sources.append({'source_id':source_id,'source_title':row['title'],'source_url':final,'retrieved_at':'RUNTIME','evidence':evidence,'snapshot_sha256':sha256_text(evidence),'http_status':status,'source_kind':'DATAFORSEO_ORGANIC_FETCHED','serp_rank_absolute':row['rank_absolute'],'serp_rank_group':row['rank_group']})
            seen_urls.add(key);seen_hosts.add(final_host)
        except SourceAcquisitionError as exc:
            failures.append({'url':row.get('url'),'reason':str(exc)})
    if len(sources)<MIN_SOURCES:raise SourceAcquisitionError('RESEARCH_SOURCE_POOL_INSUFFICIENT:'+str(len(sources)))
    core={'contract':CONTRACT,'provider':PROVIDER,'endpoint':ENDPOINT,'keyword':keyword,'location_code':LOCATION_CODE,'language_code':LANGUAGE_CODE,'selection_policy':'ORGANIC_RANK_ASC_ONE_SOURCE_PER_HOST_NO_SEMANTIC_MACHINE_SELECTION','provider_response_sha256':sha256_bytes(canon(provider)),'source_count':len(sources),'sources':sources,'fetch_failures':failures}
    core['source_pool_sha256']=sha256_bytes(canon(core))
    return core

def point0_sources(acquisition:dict)->list[dict]:
    if not isinstance(acquisition,dict) or acquisition.get('contract')!=CONTRACT:raise SourceAcquisitionError('SOURCE_ACQUISITION_CONTRACT_INVALID')
    expected=acquisition.get('source_pool_sha256');core=dict(acquisition);core.pop('source_pool_sha256',None)
    if expected!=sha256_bytes(canon(core)):raise SourceAcquisitionError('SOURCE_ACQUISITION_HASH_INVALID')
    return [{k:row[k] for k in ('source_id','source_title','source_url','retrieved_at','evidence','snapshot_sha256','http_status','source_kind')} for row in acquisition['sources']]
