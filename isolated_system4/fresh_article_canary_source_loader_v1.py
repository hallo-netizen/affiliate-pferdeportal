#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URLS = [
    ('canary-source-1','https://www.umweltbundesamt.de/themen/gesundheit/umwelteinfluesse-auf-den-menschen/innenraumluft'),
    ('canary-source-2','https://www.umweltbundesamt.de/themen/gesundheit/umwelteinfluesse-auf-den-menschen/innenraumluft/infektioese-aerosole-in-innenraeumen'),
    ('canary-source-3','https://www.umweltbundesamt.de/umwelttipps-fuer-den-alltag/richtiges-heizen-schuetzt-das-klima-den-geldbeutel'),
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def visible_text(raw: bytes) -> str:
    text = raw.decode('utf-8','replace')
    text = re.sub(r'(?is)<script\b[^>]*>.*?</script>', ' ', text)
    text = re.sub(r'(?is)<style\b[^>]*>.*?</style>', ' ', text)
    text = re.sub(r'(?s)<[^>]+>', ' ', text)
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print('USAGE: fresh_article_canary_source_loader_v1.py WORKSPACE')
        return 2
    root = Path(argv[1]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    out = root / 'sources'
    out.mkdir(exist_ok=True)
    rows=[]
    for source_id,url in URLS:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 System4A-Canary/1.0'})
        with urllib.request.urlopen(req,timeout=30) as resp:
            raw=resp.read()
            status=int(getattr(resp,'status',200))
        if status != 200 or not raw:
            print(f'SYSTEM4_CANARY_SOURCE_LOAD_BLOCKED:{source_id}:HTTP_{status}')
            return 3
        html_path=out/f'{source_id}.html'
        text_path=out/f'{source_id}.txt'
        html_path.write_bytes(raw)
        text=visible_text(raw)
        if len(text) < 500:
            print(f'SYSTEM4_CANARY_SOURCE_LOAD_BLOCKED:{source_id}:TEXT_TOO_SHORT')
            return 3
        text_path.write_text(text,encoding='utf-8')
        rows.append({'source_id':source_id,'source_url':url,'http_status':status,'raw_sha256':sha(raw),'text_sha256':sha(text.encode('utf-8')),'text_file':str(text_path.name)})
    manifest={'contract':'SYSTEM4_CANARY_MACHINE_SOURCE_MANIFEST_V1','retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'worker_network_access_required':False,'sources':rows}
    (root/'source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('SYSTEM4_CANARY_SOURCE_LOAD_PASS:'+str(len(rows)))
    return 0

if __name__=='__main__':
    raise SystemExit(main(sys.argv))
