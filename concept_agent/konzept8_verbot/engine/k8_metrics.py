#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys,time
from pathlib import Path

CONTRACT="K8_RUN_METRICS_V1"
class Blocked(RuntimeError): pass

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def load(path):
    if not path.exists():
        return {"contract":CONTRACT,"events":[],"publish_allowed":False}
    x=json.loads(path.read_text(encoding="utf-8"))
    if x.get("contract")!=CONTRACT or x.get("publish_allowed") is not False: raise Blocked("METRICS_INVALID")
    core=dict(x); declared=core.pop("metrics_sha256",None)
    if declared!=stable(core): raise Blocked("METRICS_HASH_INVALID")
    return x

def save(path,x):
    x=dict(x); x.pop("metrics_sha256",None); x["metrics_sha256"]=stable(x)
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return x

def event(path,phase,item_index=None,kind="POINT",timestamp_ns=None,meta=None):
    x=load(path); ts=int(timestamp_ns if timestamp_ns is not None else time.time_ns())
    if kind not in {"START","END","POINT"}: raise Blocked("EVENT_KIND_INVALID")
    row={"seq":len(x["events"])+1,"phase":str(phase),"kind":kind,"timestamp_ns":ts,"item_index":item_index,"meta":meta or {}}
    x["events"].append(row); return save(path,x)

def summary(x):
    starts={}; durations={}
    for e in x["events"]:
        key=(e.get("item_index"),e["phase"])
        if e["kind"]=="START": starts[key]=e["timestamp_ns"]
        elif e["kind"]=="END" and key in starts:
            durations.setdefault(e["phase"],[]).append((e["timestamp_ns"]-starts.pop(key))/1e9)
    return {k:{"count":len(v),"total_seconds":round(sum(v),3),"average_seconds":round(sum(v)/len(v),3)} for k,v in durations.items() if v}

def main(argv):
    try:
        if len(argv)<4: raise Blocked("USAGE")
        p=Path(argv[1]); cmd=argv[2]
        if cmd=="event":
            phase=argv[3]; kind=argv[4] if len(argv)>4 else "POINT"; idx=None if len(argv)<6 or argv[5]=="-" else int(argv[5])
            x=event(p,phase,idx,kind)
            print(json.dumps({"status":"PASS","event_count":len(x["events"])},sort_keys=True))
        elif cmd=="summary":
            x=load(p); print(json.dumps(summary(x),sort_keys=True))
        else: raise Blocked("COMMAND_INVALID")
        return 0
    except Exception as e:
        print("K8_METRICS_BLOCKED:"+str(e),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main(sys.argv))
