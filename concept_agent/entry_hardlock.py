#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

POINTER_CONTRACT="PFERDE_ATELIER_CONCEPT_AGENT_WORK_BINDING_POINTER_V1"
WORKFLOW="PFERDE_ATELIER_KONZEPT_5_CONCEPT_AGENT"
SHA_RE=re.compile(r"^[0-9a-f]{64}$")

class Blocked(RuntimeError): pass

def sha(raw:bytes)->str: return hashlib.sha256(raw).hexdigest()
def load(p:Path):
    x=json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(x,dict): raise Blocked("JSON_OBJECT_REQUIRED")
    return x

def probe(pointer_path:Path,current_state_path:Path,transport_path:Path|None):
    p=load(pointer_path)
    s=load(current_state_path)
    if p.get("contract")!=POINTER_CONTRACT: raise Blocked("POINTER_CONTRACT_INVALID")
    if p.get("workflow")!=WORKFLOW: raise Blocked("WORKFLOW_INVALID")
    if p.get("publish_allowed") is not False: raise Blocked("POINTER_PUBLISH_INVALID")
    batch=p.get("batch_sha256"); count=p.get("item_count")
    if not isinstance(batch,str) or not SHA_RE.fullmatch(batch): raise Blocked("BATCH_INVALID")
    if isinstance(count,bool) or not isinstance(count,int) or count<1: raise Blocked("COUNT_INVALID")
    for k in ("intake_sha256","research_binding_sha256","authoring_bindings_file_sha256","cross_chat_transport_sha256","cross_chat_transport_binding_sha256"):
        if not SHA_RE.fullmatch(str(p.get(k) or "")): raise Blocked("POINTER_HASH_INVALID:"+k)
    if p.get("cross_chat_transport_required") is not True: raise Blocked("TRANSPORT_MUST_BE_REQUIRED")

    c=s.get("concept_agent_current_batch")
    if not isinstance(c,dict): raise Blocked("CURRENT_STATE_CONCEPT_AGENT_MISSING")
    exact = {
        "workflow":p["workflow"],
        "batch_sha256":batch,
        "item_count":count,
        "intake_sha256":p["intake_sha256"],
        "research_binding_sha256":p["research_binding_sha256"],
        "authoring_bindings_file_sha256":p["authoring_bindings_file_sha256"],
        "cross_chat_transport_filename":p["cross_chat_transport_filename"],
        "cross_chat_transport_sha256":p["cross_chat_transport_sha256"],
        "publish_allowed":False,
    }
    for k,v in exact.items():
        if c.get(k)!=v: raise Blocked("CURRENT_STATE_POINTER_MISMATCH:"+k)
    if c.get("intake_status")!="PASS": raise Blocked("INTAKE_NOT_PASS")
    if c.get("research_binding_status")!="PASS": raise Blocked("RESEARCH_BINDING_NOT_PASS")
    if c.get("authoring_binding_status")!="PASS": raise Blocked("AUTHORING_BINDING_NOT_PASS")
    if c.get("article_bodies_completed")!=0 or c.get("next_article_index")!=0:
        raise Blocked("HISTORIC_HANDOFF_NOT_PRE_ARTICLE_STATE")

    decision={
        "contract":"CONCEPT_AGENT_ENTRY_HARDLOCK_DECISION_V1",
        "status":"READY" if transport_path else "BLOCKED",
        "workflow":WORKFLOW,
        "batch_sha256":batch,
        "item_count":count,
        "entry_rule":"ALWAYS_ENTER_AT_FRONT_DOOR",
        "validated_fast_forward":[
            {"stage":"INTAKE","status":"PASS","sha256":p["intake_sha256"]},
            {"stage":"RESEARCH_HASH_BINDING","status":"PASS","sha256":p["research_binding_sha256"]},
            {"stage":"AUTHORING_LINK_BINDING","status":"PASS","sha256":p["authoring_bindings_file_sha256"]},
        ],
        "next_stage":"ARTICLE_PRODUCTION",
        "next_article_index":0,
        "publish_allowed":False,
    }
    if transport_path is None:
        decision["status"]="BLOCKED"
        decision["reason"]="EXACT_CROSS_CHAT_TRANSPORT_MISSING"
        decision["expected_transport_filename"]=p["cross_chat_transport_filename"]
        decision["expected_transport_sha256"]=p["cross_chat_transport_sha256"]
        return decision

    if not transport_path.is_file(): raise Blocked("TRANSPORT_FILE_MISSING")
    raw=transport_path.read_bytes()
    actual=sha(raw)
    if actual!=p["cross_chat_transport_sha256"]:
        raise Blocked("TRANSPORT_SHA_MISMATCH")
    value=json.loads(raw.decode("utf-8"))
    if not isinstance(value,dict): raise Blocked("TRANSPORT_OBJECT_REQUIRED")
    declared=value.get("binding_sha256")
    if declared!=p["cross_chat_transport_binding_sha256"]:
        raise Blocked("TRANSPORT_BINDING_SHA_MISMATCH")
    decision["transport_sha256"]=actual
    decision["transport_binding_sha256"]=declared
    return decision

def sim_transport(pointer:dict)->bytes:
    # Positive control only: uses a self-contained fixture pointer whose expected hashes are derived from these exact bytes.
    return json.dumps({
        "contract":"CONCEPT_AGENT_WORK_BINDING_TEST_V1",
        "binding_sha256":"PLACEHOLDER",
        "batch_sha256":pointer["batch_sha256"],
        "item_count":pointer["item_count"],
        "items":[{"item_index":i,"plan_slot":hashlib.sha256(f"slot-{i}".encode()).hexdigest()} for i in range(pointer["item_count"])],
        "publish_allowed":False
    },ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()

def simulation(out:Path):
    out.mkdir(parents=True,exist_ok=True)
    batch=hashlib.sha256(b"real16-positive-control").hexdigest()
    base={
      "contract":POINTER_CONTRACT,"workflow":WORKFLOW,"batch_sha256":batch,"item_count":16,
      "intake_sha256":hashlib.sha256(b"intake").hexdigest(),
      "research_binding_sha256":hashlib.sha256(b"research").hexdigest(),
      "authoring_bindings_file_sha256":hashlib.sha256(b"authoring").hexdigest(),
      "cross_chat_transport_filename":"CONCEPT_AGENT_16_WORK_BINDING.json",
      "cross_chat_transport_sha256":"0"*64,"cross_chat_transport_binding_sha256":"0"*64,
      "cross_chat_transport_required":True,"article_bodies_present":False,"next_article_index":0,"publish_allowed":False
    }
    tval={"contract":"CONCEPT_AGENT_WORK_BINDING_TEST_V1","batch_sha256":batch,"item_count":16,"items":[],"publish_allowed":False}
    core=dict(tval); core["binding_sha256"]=hashlib.sha256(json.dumps(tval,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    raw=(json.dumps(core,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
    base["cross_chat_transport_sha256"]=sha(raw)
    base["cross_chat_transport_binding_sha256"]=core["binding_sha256"]
    cur={"concept_agent_current_batch":{
      "workflow":WORKFLOW,"batch_sha256":batch,"item_count":16,
      "intake_status":"PASS","research_binding_status":"PASS","authoring_binding_status":"PASS",
      "article_bodies_completed":0,"next_article_index":0,
      "intake_sha256":base["intake_sha256"],"research_binding_sha256":base["research_binding_sha256"],
      "authoring_bindings_file_sha256":base["authoring_bindings_file_sha256"],
      "cross_chat_transport_filename":base["cross_chat_transport_filename"],
      "cross_chat_transport_sha256":base["cross_chat_transport_sha256"],"publish_allowed":False
    }}
    pp=out/"pointer.json"; sp=out/"current.json"; tp=out/base["cross_chat_transport_filename"]
    pp.write_text(json.dumps(base,indent=2)+"\n"); sp.write_text(json.dumps(cur,indent=2)+"\n"); tp.write_bytes(raw)
    pos=probe(pp,sp,tp)
    if pos.get("status")!="READY" or pos.get("next_stage")!="ARTICLE_PRODUCTION" or pos.get("next_article_index")!=0:
        raise Blocked("POSITIVE_NOT_READY")
    neg=[]
    # Missing transport must block.
    x=probe(pp,sp,None)
    if x.get("status")!="BLOCKED" or x.get("reason")!="EXACT_CROSS_CHAT_TRANSPORT_MISSING":
        raise Blocked("NEGATIVE_MISSING_TRANSPORT_NOT_BLOCKED")
    neg.append(x)
    # Tamper must block.
    tp.write_bytes(raw+b"X")
    try: probe(pp,sp,tp)
    except Blocked as e: neg.append({"status":"BLOCKED","reason":str(e)})
    else: raise Blocked("NEGATIVE_TAMPER_NOT_BLOCKED")
    proof={"contract":"CONCEPT_AGENT_ENTRY_HARDLOCK_SIMULATION_V1","status":"PASS","positive":pos,"negative":neg}
    (out/"ENTRY_HARDLOCK_SIMULATION_PROOF.json").write_text(json.dumps(proof,indent=2)+"\n")
    return proof

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("probe"); p.add_argument("--pointer",required=True); p.add_argument("--current-state",required=True); p.add_argument("--transport"); p.add_argument("--out",required=True)
    s=sub.add_parser("simulate"); s.add_argument("--out",required=True)
    a=ap.parse_args()
    try:
        if a.cmd=="simulate":
            r=simulation(Path(a.out)); print(json.dumps({"ok":True,"status":r["status"]},sort_keys=True)); return 0
        d=probe(Path(a.pointer),Path(a.current_state),Path(a.transport) if a.transport else None)
        Path(a.out).parent.mkdir(parents=True,exist_ok=True); Path(a.out).write_text(json.dumps(d,indent=2)+"\n")
        print(json.dumps(d,sort_keys=True))
        return 0 if d["status"]=="READY" else 20
    except Exception as e:
        print("CONCEPT_AGENT_ENTRY_HARDLOCK_BLOCKED:"+str(e),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
