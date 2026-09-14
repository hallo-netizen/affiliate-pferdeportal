from __future__ import annotations
import hashlib, json
from pathlib import Path
import point0_snapshot, supervisor, root_supervisor_bridge

CONTRACT='SYSTEM4_SUPERVISOR_DISPATCH_BUNDLE_V1'
class WorkerDispatchError(RuntimeError): pass

def sha(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def canon(v)->bytes: return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()

def build_bundle(point0:dict, root_receipt:dict, worker_contract:dict)->dict:
    b={'contract':CONTRACT,'point0':point0,'root_receipt':root_receipt,'worker_contract':worker_contract,'publish_allowed':False}
    b['bundle_sha256']=sha(canon(b))
    return b

def verify_bundle(bundle:dict, *, actual_manifest:str, actual_head:str)->tuple[dict,bytes]:
    if not isinstance(bundle,dict) or bundle.get('contract')!=CONTRACT: raise WorkerDispatchError('DISPATCH_CONTRACT_INVALID')
    if bundle.get('publish_allowed') is not False: raise WorkerDispatchError('DISPATCH_PUBLISH_AUTHORITY_FAIL')
    core=dict(bundle); expected=core.pop('bundle_sha256',None)
    if expected!=sha(canon(core)): raise WorkerDispatchError('DISPATCH_BUNDLE_TAMPERED')
    p0=bundle.get('point0'); raw=point0_snapshot.verify(p0)
    if p0['root_manifest_sha256']!=actual_manifest: raise WorkerDispatchError('DISPATCH_ROOT_MANIFEST_MISMATCH')
    if p0['head_sha']!=actual_head: raise WorkerDispatchError('DISPATCH_HEAD_MISMATCH')
    rr=bundle.get('root_receipt'); wc=bundle.get('worker_contract')
    if not isinstance(rr,dict) or not isinstance(wc,dict): raise WorkerDispatchError('DISPATCH_BINDING_MISSING')
    rcore=dict(rr); rexp=rcore.pop('receipt_sha256',None)
    if rexp!=sha(canon(rcore)): raise WorkerDispatchError('DISPATCH_ROOT_RECEIPT_TAMPERED')
    if rr.get('root_manifest_sha256')!=actual_manifest or rr.get('head_sha')!=actual_head: raise WorkerDispatchError('DISPATCH_ROOT_RECEIPT_IDENTITY_MISMATCH')
    if rr.get('point0_sha256')!=sha(point0_snapshot.canon(p0)): raise WorkerDispatchError('DISPATCH_POINT0_RECEIPT_MISMATCH')
    if wc.get('contract')!='SYSTEM4_CODEX_WORKER_DISPATCH_V1' or wc.get('external_web_search_allowed') is not False or wc.get('publish_allowed') is not False: raise WorkerDispatchError('DISPATCH_WORKER_CONTRACT_INVALID')
    if wc.get('point0_sha256')!=rr.get('point0_sha256') or wc.get('head_sha')!=actual_head or wc.get('root_receipt_sha256')!=rexp: raise WorkerDispatchError('DISPATCH_WORKER_BINDING_MISMATCH')
    return wc,raw
