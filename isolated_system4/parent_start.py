from __future__ import annotations

import hashlib
import html.parser
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import point0_snapshot
import root_entry

CONTRACT='SYSTEM4_PARENT_LAUNCH_V1'
PROD_CONTRACT='SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1'
BATCH_CONTRACT='PSERC_TEXTMACHINE_METADATA_BATCH_V2'
MAX_SOURCE_BYTES=1_500_000
HERE=Path(__file__).resolve().parent
REPO=HERE.parent
BOUND_DIR=(HERE/'bound_launches').resolve()

class ParentStartError(RuntimeError): pass

def canon(value)->bytes:
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')

def sha256(data:bytes)->str: return hashlib.sha256(data).hexdigest()

def _within(child:Path,parent:Path)->bool:
    child=child.resolve(); parent=parent.resolve(); return child==parent or parent in child.parents

def _load_bound_capsule(rel_path:str,expected_sha256:str)->dict:
    if not isinstance(rel_path,str) or not rel_path.startswith('isolated_system4/bound_launches/') or '..' in Path(rel_path).parts:
        raise ParentStartError('PARENT_BOUND_CAPSULE_PATH_INVALID')
    if not re.fullmatch(r'[0-9a-f]{64}',expected_sha256 or ''):
        raise ParentStartError('PARENT_BOUND_CAPSULE_SHA_INVALID')
    path=(REPO/rel_path).resolve()
    if not _within(path,BOUND_DIR) or not path.is_file():
        raise ParentStartError('PARENT_BOUND_CAPSULE_MISSING')
    try:
        tracked=root_entry._git('ls-files','--error-unmatch','--',rel_path)
        dirty=root_entry._git('status','--porcelain=v1','--',rel_path)
    except Exception as exc:
        raise ParentStartError('PARENT_BOUND_CAPSULE_GIT_BINDING_FAILED') from exc
    if tracked.strip()!=rel_path or dirty.strip():
        raise ParentStartError('PARENT_BOUND_CAPSULE_NOT_CLEAN_TRACKED')
    raw=path.read_bytes()
    if sha256(raw)!=expected_sha256:
        raise ParentStartError('PARENT_BOUND_CAPSULE_SHA_MISMATCH')
    try: value=json.loads(raw.decode('utf-8'))
    except Exception as exc: raise ParentStartError('PARENT_BOUND_CAPSULE_JSON_INVALID') from exc
    if canon(value)!=raw:
        raise ParentStartError('PARENT_BOUND_CAPSULE_NOT_CANONICAL')
    return value

class _TextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.parts=[]; self._skip=0
    def handle_starttag(self,tag,attrs):
        if tag in {'script','style','noscript','svg'}: self._skip+=1
    def handle_endtag(self,tag):
        if tag in {'script','style','noscript','svg'} and self._skip: self._skip-=1
    def handle_data(self,data):
        if not self._skip:
            text=' '.join(str(data).split())
            if text:self.parts.append(text)
    def text(self): return ' '.join(self.parts)

def _validate_launch(value):
    if not isinstance(value,dict) or value.get('contract')!=CONTRACT: raise ParentStartError('PARENT_LAUNCH_CONTRACT_INVALID')
    if value.get('publish_allowed') is not False: raise ParentStartError('PARENT_LAUNCH_PUBLISH_MUST_BE_FALSE')
    items=value.get('items'); source_urls=value.get('source_urls')
    if not isinstance(items,list) or not items: raise ParentStartError('PARENT_LAUNCH_ITEMS_INVALID')
    if not isinstance(source_urls,list) or len(source_urls)!=len(items): raise ParentStartError('PARENT_LAUNCH_SOURCE_COUNT_MISMATCH')
    for idx,item in enumerate(items):
        if not isinstance(item,dict): raise ParentStartError(f'PARENT_LAUNCH_ITEM_INVALID:{idx}')
        for key in ('title','target_keyword','category','article_type','plan_slot'):
            if not isinstance(item.get(key),str) or not item[key].strip(): raise ParentStartError(f'PARENT_LAUNCH_ITEM_FIELD_INVALID:{idx}:{key}')
        if not re.fullmatch(r'[0-9a-f]{64}',item['plan_slot']): raise ParentStartError(f'PARENT_LAUNCH_PLAN_SLOT_INVALID:{idx}')
        urls=source_urls[idx]
        if not isinstance(urls,list) or not urls: raise ParentStartError(f'PARENT_LAUNCH_SOURCE_URLS_EMPTY:{idx}')
        for url in urls:
            if not isinstance(url,str) or not re.match(r'^https?://',url): raise ParentStartError(f'PARENT_LAUNCH_SOURCE_URL_INVALID:{idx}')
    return items,source_urls

def _fetch_source(url,source_id):
    req=urllib.request.Request(url,headers={'User-Agent':'pferde-atelier-system4-parent-start/1.0'})
    try:
        with urllib.request.urlopen(req,timeout=30) as response:
            status=int(getattr(response,'status',0) or 0); raw=response.read(MAX_SOURCE_BYTES+1); final_url=response.geturl(); content_type=str(response.headers.get('Content-Type',''))
    except Exception as exc: raise ParentStartError('PARENT_SOURCE_FETCH_FAILED:'+url+':'+exc.__class__.__name__) from exc
    if status<200 or status>=300: raise ParentStartError('PARENT_SOURCE_HTTP_FAIL:'+url+':'+str(status))
    if len(raw)>MAX_SOURCE_BYTES: raise ParentStartError('PARENT_SOURCE_TOO_LARGE:'+url)
    charset='utf-8'; match=re.search(r'charset=([^;\s]+)',content_type,flags=re.I)
    if match: charset=match.group(1).strip('"\'')
    try: decoded=raw.decode(charset,errors='replace')
    except LookupError: decoded=raw.decode('utf-8',errors='replace')
    if 'html' in content_type.lower() or '<html' in decoded[:500].lower():
        parser=_TextExtractor(); parser.feed(decoded); evidence=parser.text()
    else: evidence=' '.join(decoded.split())
    if len(evidence.strip())<20: raise ParentStartError('PARENT_SOURCE_EVIDENCE_EMPTY:'+url)
    title=final_url; title_match=re.search(r'<title[^>]*>(.*?)</title>',decoded,flags=re.I|re.S)
    if title_match:
        clean=' '.join(re.sub(r'<[^>]+>',' ',title_match.group(1)).split())
        if clean:title=clean
    return {'source_id':source_id,'source_title':title,'source_url':final_url,'retrieved_at':datetime.now(timezone.utc).isoformat(),'evidence':evidence,'snapshot_sha256':sha256(evidence.encode('utf-8')),'http_status':status,'source_kind':'parent_machine_http'}

def _build_production_snapshot(items,manifest):
    material={'contract':BATCH_CONTRACT,'content_or_format_payload_present':False,'item_count':len(items),'items':items,'maximum_articles':0,'maximum_articles_per_type':0,'publish_allowed':False,'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE'}
    material['batch_sha256']=sha256(canon(material))
    return canon({'contract':PROD_CONTRACT,'next_textmachine_metadata_batch':material,'source_snapshot_original_sha256':sha256(canon(items)),'system4_root_manifest_sha256':manifest})

def run_launch(launch,runtime_root:Path):
    if _within(runtime_root,REPO): raise ParentStartError('PARENT_RUNTIME_MUST_BE_OUTSIDE_REPO')
    items,source_urls=_validate_launch(launch); manifest=root_entry._critical_manifest_sha256(); head=root_entry._git('rev-parse','--verify','HEAD'); production_bytes=_build_production_snapshot(items,manifest)
    runtime_root.mkdir(parents=True,exist_ok=False); workspaces=[]
    for index,urls in enumerate(source_urls):
        prepared=point0_snapshot.prepare(production_snapshot_bytes=production_bytes,root_manifest_sha256=manifest,head_sha=head)
        sources=[_fetch_source(url,f'parent-{index}-{src_index}') for src_index,url in enumerate(urls)]
        final=point0_snapshot.finalize(prepared,research_provider='SYSTEM4_PARENT_MACHINE_HTTP_V1',sources=sources)
        point0_path=runtime_root/f'point0-{index}.json'; point0_path.write_bytes(point0_snapshot.canon(final)); workspace=runtime_root/f'item-{index}'
        rc=root_entry.main(['root_entry.py','start-point0',str(point0_path),str(workspace),str(index)])
        if rc!=0: raise ParentStartError(f'PARENT_ROOT_START_FAILED:{index}:{rc}')
        workspaces.append(workspace)
    receipt={'contract':'SYSTEM4_PARENT_START_RECEIPT_V1','head_sha':head,'root_manifest_sha256':manifest,'article_count':len(items),'workspaces':[str(p) for p in workspaces],'publish_allowed':False}
    (runtime_root/'parent_start_receipt.json').write_bytes(canon(receipt)); return workspaces

def main(argv):
    try:
        if len(argv)!=5 or argv[1]!='start-bound': raise ParentStartError('PARENT_START_BAD_COMMAND')
        launch=_load_bound_capsule(argv[2],argv[3]); workspaces=run_launch(launch,Path(argv[4]))
        print('SYSTEM4_PARENT_START_PASS:POINT0_ROOT_DISPATCH_READY:ARTICLE_COUNT='+str(len(workspaces)))
        for index,workspace in enumerate(workspaces): print('SYSTEM4_PARENT_WORKSPACE:'+str(index)+':'+str(workspace))
        return 0
    except Exception as exc:
        print('SYSTEM4_PARENT_START_FAIL:'+str(exc)); return 2

if __name__=='__main__': raise SystemExit(main(sys.argv))
