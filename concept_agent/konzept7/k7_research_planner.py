#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path

CONTRACT="K7_RESEARCH_PLAN_V1"
SHA_RE=re.compile(r"^[0-9a-f]{64}$")
class Blocked(RuntimeError): pass

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def _valid_bound_for_intake(intake,bound):
    if not isinstance(bound,dict) or bound.get("contract")!="CONCEPT_AGENT_RESEARCH_BOUND_V1": return False
    core=dict(bound); declared=core.pop("research_binding_sha256",None)
    if declared!=stable(core): return False
    if bound.get("batch_sha256")!=intake.get("batch_sha256") or bound.get("item_count")!=intake.get("item_count"): return False
    rows=bound.get("items"); items=intake.get("items")
    if not isinstance(rows,list) or not isinstance(items,list) or len(rows)!=len(items): return False
    for i,(a,r) in enumerate(zip(items,rows)):
        if r.get("item_index")!=i or r.get("plan_slot")!=a.get("plan_slot") or r.get("article_identity_sha256")!=a.get("identity_sha256"): return False
        src=r.get("sources")
        if not isinstance(src,list) or not src or r.get("source_pool_sha256")!=stable(src): return False
        for s in src:
            ev=s.get("evidence"); h=s.get("snapshot_sha256")
            if not isinstance(ev,str) or hashlib.sha256(ev.encode()).hexdigest()!=h: return False
    return bound.get("draft_allowed") is True and bound.get("publish_allowed") is False

def plan(intake,bound=None,lanes=4):
    if not isinstance(intake,dict) or intake.get("contract")!="CONCEPT_AGENT_AUTHORING_INTAKE_V1": raise Blocked("INTAKE_INVALID")
    items=intake.get("items")
    if not isinstance(items,list) or len(items)!=intake.get("item_count"): raise Blocked("INTAKE_COUNT_INVALID")
    if lanes not in {1,2,4,8}: raise Blocked("RESEARCH_LANES_INVALID")
    exact_reuse=_valid_bound_for_intake(intake,bound)
    rows=[]
    for i,a in enumerate(items):
        rows.append({
          "item_index":i,"plan_slot":a["plan_slot"],"article_identity_sha256":a["identity_sha256"],
          "mode":"REUSE_EXACT_BOUND_RESEARCH" if exact_reuse else "RESEARCH_REQUIRED",
          "lane":None if exact_reuse else i%lanes,
          "new_external_lookup_required":not exact_reuse
        })
    out={
      "contract":CONTRACT,"status":"PASS","batch_sha256":intake["batch_sha256"],"item_count":len(items),
      "parallel_research_lanes":lanes,"exact_bound_reuse":exact_reuse,
      "policy":{
        "exact_hash_bound_reuse_first":True,
        "cross_batch_unverified_reuse":False,
        "cache_candidate_without_revalidation":"FORBIDDEN",
        "own_domain_research":"FORBIDDEN",
        "research_only_for_cache_miss":True
      },
      "items":rows,"publish_allowed":False
    }
    out["plan_sha256"]=stable(out); return out

def main(argv):
    try:
        if len(argv) not in {4,5}: raise Blocked("USE: k7_research_planner.py INTAKE BOUND_OR_DASH OUT [LANES]")
        intake=json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        bound=None if argv[2]=="-" else json.loads(Path(argv[2]).read_text(encoding="utf-8"))
        out=plan(intake,bound,int(argv[4]) if len(argv)==5 else 4)
        Path(argv[3]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"status":"PASS","reuse":out["exact_bound_reuse"],"research_required":sum(x["new_external_lookup_required"] for x in out["items"]),"lanes":out["parallel_research_lanes"]},sort_keys=True)); return 0
    except Exception as e:
        print("K7_RESEARCH_PLANNER_BLOCKED:"+str(e),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main(sys.argv))
