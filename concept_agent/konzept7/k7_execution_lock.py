#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path

CONTRACT="K7_EXECUTION_LOCK_V1"
SHA_RE=re.compile(r"^[0-9a-f]{64}$")
class Blocked(RuntimeError): pass

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def verify(x):
    if not isinstance(x,dict) or x.get("contract")!=CONTRACT: raise Blocked("LOCK_CONTRACT_INVALID")
    core=dict(x); declared=core.pop("lock_sha256",None)
    if declared!=stable(core): raise Blocked("LOCK_HASH_INVALID")
    if x.get("status") not in {"ACTIVE","COMPLETE"}: raise Blocked("LOCK_STATUS_INVALID")
    if not SHA_RE.fullmatch(str(x.get("batch_sha256") or "")): raise Blocked("LOCK_BATCH_INVALID")
    if not SHA_RE.fullmatch(str(x.get("production_binding_sha256") or "")): raise Blocked("LOCK_BINDING_INVALID")
    if x.get("publish_allowed") is not False: raise Blocked("LOCK_PUBLISH_INVALID")
    return x

def acquire(path:Path,batch:str,binding:str,count:int,generation:int=1):
    if not SHA_RE.fullmatch(batch) or not SHA_RE.fullmatch(binding): raise Blocked("LOCK_IDENTITY_INVALID")
    if isinstance(count,bool) or count<1 or isinstance(generation,bool) or generation<1: raise Blocked("LOCK_COUNT_OR_GENERATION_INVALID")
    if path.exists():
        x=verify(json.loads(path.read_text(encoding="utf-8")))
        same=(x["batch_sha256"]==batch and x["production_binding_sha256"]==binding and x["item_count"]==count)
        if not same: raise Blocked("CONFLICTING_START_BLOCKED")
        if x["status"]=="COMPLETE": raise Blocked("COMPLETED_RUN_REQUIRES_NEW_EXPLICIT_GENERATION")
        return {"status":"RESUME_EXISTING","lock":x}
    core={
      "contract":CONTRACT,"status":"ACTIVE","batch_sha256":batch,"production_binding_sha256":binding,
      "item_count":count,"runtime_generation":generation,
      "duplicate_start_policy":"RESUME_SAME_BATCH","conflicting_start_policy":"BLOCK",
      "chat_may_choose_stage":False,"chat_may_choose_article":False,"alternate_route_allowed":False,
      "publish_allowed":False
    }
    x=dict(core); x["lock_sha256"]=stable(core)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"status":"CREATED","lock":x}

def complete(path:Path,final_sha:str):
    if not SHA_RE.fullmatch(final_sha): raise Blocked("FINAL_SHA_INVALID")
    x=verify(json.loads(path.read_text(encoding="utf-8")))
    if x["status"]!="ACTIVE": raise Blocked("LOCK_NOT_ACTIVE")
    x.pop("lock_sha256",None); x["status"]="COMPLETE"; x["final_sha256"]=final_sha
    x["lock_sha256"]=stable(x)
    path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return x

def main(argv):
    try:
        if len(argv)>=2 and argv[1]=="acquire" and len(argv) in {6,7}:
            gen=int(argv[6]) if len(argv)==7 else 1
            out=acquire(Path(argv[2]),argv[3],argv[4],int(argv[5]),gen)
        elif len(argv)==4 and argv[1]=="complete":
            out=complete(Path(argv[2]),argv[3])
        else: raise Blocked("USAGE")
        print(json.dumps(out,ensure_ascii=False,sort_keys=True)); return 0
    except Exception as e:
        print("K7_EXECUTION_LOCK_BLOCKED:"+str(e),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main(sys.argv))
