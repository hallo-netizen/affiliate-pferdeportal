#!/usr/bin/env python3
from __future__ import annotations
import html,re

class K8MechanicalPreflightError(RuntimeError): pass

TRACE_RE=re.compile(r'(?is)<span\b([^>]*\bclass=["\'][^"\']*\bppm-source-trace\b[^"\']*["\'][^>]*)></span>')

def _attr(attrs:str,name:str)->str|None:
    m=re.search(r'(?is)\b'+re.escape(name)+r'\s*=\s*(["\'])(.*?)\1',attrs)
    return html.unescape(m.group(2)).strip() if m else None

def _set_attr(attrs:str,name:str,value:str)->str:
    esc=html.escape(value,quote=True)
    pat=re.compile(r'(?is)(\b'+re.escape(name)+r'\s*=\s*)(["\'])(.*?)\2')
    if pat.search(attrs):
        return pat.sub(lambda m:m.group(1)+'"'+esc+'"',attrs,count=1)
    return attrs+' '+name+'="'+esc+'"'

def _visible(value:str)->str:
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'(?is)<[^>]+>',' ',value))).strip()

def normalize_source_traces(article_html:str,fact_pack:dict)->tuple[str,dict]:
    if not isinstance(article_html,str) or not article_html.strip():
        raise K8MechanicalPreflightError('ARTICLE_EMPTY')
    claims=fact_pack.get('claims')
    if not isinstance(claims,list) or not claims:
        raise K8MechanicalPreflightError('FACT_PACK_CLAIMS_MISSING')
    authority={}
    for row in claims:
        if not isinstance(row,dict): raise K8MechanicalPreflightError('FACT_PACK_CLAIM_INVALID')
        fid=str(row.get('fact_id') or '').strip()
        sid=str(row.get('source_id') or '').strip()
        h=str(row.get('evidence_text_sha256') or '').strip().lower()
        if not fid or not sid or not re.fullmatch(r'[0-9a-f]{64}',h):
            raise K8MechanicalPreflightError('FACT_AUTHORITY_INVALID:'+fid)
        authority[fid]=(sid,h)

    changed=0; seen=0
    def repl(m):
        nonlocal changed,seen
        attrs=m.group(1); seen+=1
        fid=_attr(attrs,'data-fact-id')
        if not fid or fid not in authority:
            raise K8MechanicalPreflightError('TRACE_FACT_UNKNOWN:'+str(fid))
        sid,h=authority[fid]
        new=_set_attr(attrs,'data-source-title',sid)
        new=_set_attr(new,'data-source-hash',h)
        if new!=attrs: changed+=1
        return '<span'+new+'></span>'

    out=TRACE_RE.sub(repl,article_html)
    if seen==0: raise K8MechanicalPreflightError('SOURCE_TRACES_MISSING')
    if _visible(out)!=_visible(article_html):
        raise K8MechanicalPreflightError('VISIBLE_TEXT_MUTATION_FORBIDDEN')
    return out,{'status':'PASS','trace_count':seen,'changed_trace_count':changed,'visible_text_unchanged':True}
