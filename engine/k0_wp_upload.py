"""Unpack the one-click WordPress-to-K0 package without a second approval.

The original five-field batch is preserved verbatim. The separate technical
receipt contains only WordPress-owned IDs and the previously frozen intent.
No K0 writing, quality, security or publication rules are changed here.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from .wp_order_identity_receipt import inspect

class Blocked(RuntimeError): pass

def single_intake(batch: dict, row: dict) -> dict:
    original={k:v for k,v in batch.items() if k!='batch_sha256'}
    original['items']=[row]
    original['item_count']=1
    original['batch_sha256']=hashlib.sha256(json.dumps(original,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return original

def unpack(payload: dict) -> list[tuple[dict,dict]]:
    if not isinstance(payload,dict) or set(payload) != {'contract','publish_allowed','k0_intake','word_press_order_receipt'}:
        raise Blocked('WP_K0_PACKAGE_FIELDS_INVALID')
    if payload['contract']!='WP_K0_UPLOAD_PACKAGE_V1' or payload['publish_allowed'] is not False:
        raise Blocked('WP_K0_PACKAGE_CONTRACT_INVALID')
    batch=payload['k0_intake']
    receipt=payload['word_press_order_receipt']
    source, profiles, identities=inspect(receipt)
    if source!=batch:
        raise Blocked('WP_K0_PACKAGE_SOURCE_MISMATCH')
    return [(single_intake(batch,row),receipt) for row in batch['items']]

def write_runs(payload_path:Path, destination:Path):
    payload=json.loads(payload_path.read_text(encoding='utf-8'))
    jobs=unpack(payload)
    results=[]
    for i,(intake,receipt) in enumerate(jobs,1):
        target=destination/f'item-{i:02d}'
        # Existing files may only be reused byte-for-byte. No overwrite or restart.
        for name,document in (('WORDPRESS_INTAKE.json',intake),('PSERC_SOURCE_MANIFEST.json',receipt)):
            path=target/name
            content=json.dumps(document,ensure_ascii=False,indent=2)+'\n'
            if path.exists() and path.read_text(encoding='utf-8')!=content:
                raise Blocked('K0_RESUME_EXISTING_FILE_CHANGED:'+str(path))
        target.mkdir(parents=True,exist_ok=True)
        for name,document in (('WORDPRESS_INTAKE.json',intake),('PSERC_SOURCE_MANIFEST.json',receipt)):
            path=target/name
            if not path.exists(): path.write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        results.append(target)
    return results

if __name__=='__main__':
    import sys
    if len(sys.argv)!=3: raise SystemExit('usage: python -m engine.k0_wp_upload WP_K0_PACKAGE.json TEST_RUN_DIR')
    try:
        folders=write_runs(Path(sys.argv[1]),Path(sys.argv[2]))
        print(json.dumps({'status':'PASS','item_count':len(folders),'publish_allowed':False},ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False))
        raise SystemExit(2)
