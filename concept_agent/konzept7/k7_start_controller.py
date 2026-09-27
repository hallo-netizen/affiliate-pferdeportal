#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
if str(Path(__file__).resolve().parent) not in sys.path: sys.path.insert(0,str(Path(__file__).resolve().parent))

import intake_bridge,production_bridge
import k7_execution_lock,k7_research_planner,k7_parallel_controller,k7_closeout_plan

CONTRACT="K7_RUN_ROOT_V1"
class Blocked(RuntimeError): pass

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def load(path):
    x=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(x,dict): raise Blocked("JSON_OBJECT_REQUIRED")
    return x

def _verify_root(x):
    if x.get("contract")!=CONTRACT: raise Blocked("RUN_ROOT_CONTRACT_INVALID")
    core=dict(x); declared=core.pop("run_root_sha256",None)
    if declared!=stable(core): raise Blocked("RUN_ROOT_HASH_INVALID")
    if x.get("publish_allowed") is not False: raise Blocked("RUN_ROOT_PUBLISH_INVALID")
    return x

def _write(path,x):
    x=dict(x); x.pop("run_root_sha256",None); x["run_root_sha256"]=stable(x)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return x

def start(snapshot_path:Path,research_path:Path|None,state_dir:Path,lanes=4,generation=1):
    snap=load(snapshot_path)
    intake=intake_bridge.prepare(snap)
    state_dir.mkdir(parents=True,exist_ok=True)
    root_path=state_dir/"K7_RUN_ROOT.json"
    closeout_path=state_dir/"K7_CLOSEOUT_PLAN.json"
    if root_path.exists():
        rr=_verify_root(load(root_path))
        if rr["batch_sha256"]!=intake["batch_sha256"] or rr["intake_sha256"]!=intake["intake_sha256"]:
            raise Blocked("CONFLICTING_START_BLOCKED")
        start_status="RESUME_EXISTING_RUN"
    else:
        rr=_write(root_path,{
          "contract":CONTRACT,"status":"ACTIVE","batch_sha256":intake["batch_sha256"],
          "intake_sha256":intake["intake_sha256"],"item_count":intake["item_count"],
          "runtime_generation":generation,"article_lanes":lanes,
          "duplicate_start_policy":"RESUME_SAME_RUN","conflicting_start_policy":"BLOCK",
          "chat_may_choose_stage":False,"chat_may_choose_article":False,
          "alternate_route_allowed":False,"publish_allowed":False
        })
        start_status="NEW_RUN_CREATED"
    if not closeout_path.exists():
        closeout=_write(closeout_path,k7_closeout_plan.build(intake["batch_sha256"],intake["item_count"],generation))
    else:
        closeout=load(closeout_path)
    bound=load(research_path) if research_path and research_path.is_file() else None
    rp=k7_research_planner.plan(intake,bound,lanes)
    (state_dir/"K7_RESEARCH_PLAN.json").write_text(json.dumps(rp,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (state_dir/"K7_INTAKE.json").write_text(json.dumps(intake,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if not rp["exact_bound_reuse"]:
        return {"status":start_status,"stage":"RESEARCH_REQUIRED","research_plan":rp,"closeout_plan":closeout,"publish_allowed":False}
    binding=production_bridge.build(snap,intake,bound)
    (state_dir/"K7_PRODUCTION_BINDING.json").write_text(json.dumps(binding,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lock=k7_execution_lock.acquire(state_dir/"K7_EXECUTION_LOCK.json",binding["batch_sha256"],binding["binding_sha256"],binding["item_count"],generation)
    state_path=state_dir/"K7_PARALLEL_STATE.json"
    if state_path.exists():
        pstate=load(state_path); k7_parallel_controller.verify(binding,pstate)
    else:
        pstate=k7_parallel_controller.initial(binding,lanes)
        state_path.write_text(json.dumps(pstate,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rr=load(root_path); rr.pop("run_root_sha256",None)
    rr["production_binding_sha256"]=binding["binding_sha256"]; rr["status"]="PRODUCTION_ACTIVE"
    _write(root_path,rr)
    return {
      "status":start_status,"stage":pstate["batch_phase"],"execution_lock_status":lock["status"],
      "ready_actions":k7_parallel_controller.ready_actions(binding,pstate),
      "closeout_plan":closeout,"publish_allowed":False
    }

def main(argv):
    try:
        if len(argv) not in {5,6,7}: raise Blocked("USE: k7_start_controller.py SNAPSHOT RESEARCH_OR_DASH STATE_DIR LANES [GENERATION]")
        research=None if argv[2]=="-" else Path(argv[2])
        out=start(Path(argv[1]),research,Path(argv[3]),int(argv[4]),int(argv[5]) if len(argv)>5 else 1)
        print(json.dumps(out,ensure_ascii=False,sort_keys=True)); return 0
    except Exception as e:
        print("K7_START_CONTROLLER_BLOCKED:"+str(e),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main(sys.argv))
