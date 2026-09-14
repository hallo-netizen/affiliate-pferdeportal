from __future__ import annotations
import hashlib, json
from pathlib import Path
import point0_snapshot, supervisor

class RootBridgeError(RuntimeError): pass

def sha(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def canon(v)->bytes: return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()

def bind_point0(point0_path:Path, workspace:Path, *, actual_manifest:str, actual_head:str)->dict:
    if workspace.exists() and any(workspace.iterdir()): raise RootBridgeError('WORKSPACE_NOT_EMPTY')
    state=supervisor.arm(point0_path,workspace,actual_manifest=actual_manifest,actual_head=actual_head)
    receipt={'contract':'SYSTEM4_ROOT_POINT0_RECEIPT_V1','point0_sha256':state['point0_sha256'],'production_snapshot_sha256':state['production_snapshot_sha256'],'research_pool_sha256':state['research_pool_sha256'],'root_manifest_sha256':actual_manifest,'head_sha':actual_head,'phase':'RESEARCH_REQUIRED','publish_allowed':False}
    receipt['receipt_sha256']=sha(canon(receipt))
    (workspace/'root_receipt.json').write_bytes(canon(receipt))
    return receipt

def dispatch(workspace:Path)->dict:
    rp=workspace/'root_receipt.json'
    if not rp.is_file(): raise RootBridgeError('ROOT_RECEIPT_MISSING')
    r=json.loads(rp.read_text()); core=dict(r); expected=core.pop('receipt_sha256',None)
    if expected!=sha(canon(core)): raise RootBridgeError('ROOT_RECEIPT_TAMPERED')
    c=supervisor.worker_contract(workspace)
    for k in ('point0_sha256','head_sha','publish_allowed'):
        if c[k]!=r[k]: raise RootBridgeError('ROOT_SUPERVISOR_BINDING_MISMATCH:'+k)
    c['root_receipt_sha256']=expected
    return c
