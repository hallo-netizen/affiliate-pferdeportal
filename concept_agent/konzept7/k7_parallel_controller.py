#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path

CONTRACT="K7_PARALLEL_BATCH_STATE_V1"
SHA_RE=re.compile(r"^[0-9a-f]{64}$")
class Blocked(RuntimeError): pass

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def seal(x):
    y=json.loads(json.dumps(x)); y.pop("state_sha256",None); y["state_sha256"]=stable(y); return y

def verify_binding(binding):
    if not isinstance(binding,dict) or binding.get("contract")!="CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1": raise Blocked("BINDING_INVALID")
    core=dict(binding); declared=core.pop("binding_sha256",None)
    if declared!=stable(core): raise Blocked("BINDING_HASH_INVALID")
    items=binding.get("items")
    if not isinstance(items,list) or len(items)!=binding.get("item_count"): raise Blocked("BINDING_ITEMS_INVALID")
    return binding

def initial(binding,lanes=4):
    verify_binding(binding)
    if lanes not in {1,2,4,8}: raise Blocked("LANES_INVALID")
    items=[]
    for i,row in enumerate(binding["items"]):
        items.append({
          "item_index":i,"plan_slot":row["identity"]["plan_slot"],"lane":i%lanes,
          "phase":"AUTHORING_REQUIRED","status":"IN_PROGRESS","revision":0,
          "draft_sha256":None,"lt68":"PENDING","ppm679":"PENDING",
          "repair_count":0,"revision_history":[]
        })
    return seal({
      "contract":CONTRACT,"status":"IN_PROGRESS","batch_sha256":binding["batch_sha256"],
      "production_binding_sha256":binding["binding_sha256"],"item_count":len(items),
      "article_lanes":lanes,"batch_phase":"ARTICLE_PRODUCTION","items":items,
      "pserc":"PENDING","endstempel":"PENDING","publish_allowed":False
    })

def verify(binding,state):
    verify_binding(binding)
    if not isinstance(state,dict) or state.get("contract")!=CONTRACT: raise Blocked("STATE_CONTRACT_INVALID")
    core=dict(state); declared=core.pop("state_sha256",None)
    if declared!=stable(core): raise Blocked("STATE_HASH_INVALID")
    if state.get("batch_sha256")!=binding.get("batch_sha256") or state.get("production_binding_sha256")!=binding.get("binding_sha256"): raise Blocked("STATE_BINDING_INVALID")
    if state.get("publish_allowed") is not False: raise Blocked("STATE_PUBLISH_INVALID")
    rows=state.get("items")
    if not isinstance(rows,list) or len(rows)!=binding.get("item_count"): raise Blocked("STATE_ITEMS_INVALID")
    for i,row in enumerate(rows):
        if row.get("item_index")!=i or row.get("plan_slot")!=binding["items"][i]["identity"]["plan_slot"]: raise Blocked("STATE_ITEM_IDENTITY_INVALID")
        if row.get("lane")!=i%state["article_lanes"]: raise Blocked("STATE_LANE_INVALID")
        if row.get("phase") not in {"AUTHORING_REQUIRED","LT68_REQUIRED","PPM679_REQUIRED","REPAIR_REQUIRED","PASS"}: raise Blocked("STATE_PHASE_INVALID")
        if row.get("status") not in {"IN_PROGRESS","PASS"}: raise Blocked("STATE_ITEM_STATUS_INVALID")
        hist=row.get("revision_history")
        if not isinstance(hist,list): raise Blocked("STATE_REVISION_HISTORY_INVALID")
        for rev in hist:
            body=rev.get("content_utf8")
            if not isinstance(body,str): raise Blocked("REVISION_BYTES_MISSING")
            if hashlib.sha256(body.encode("utf-8")).hexdigest()!=rev.get("draft_sha256"): raise Blocked("REVISION_HASH_INVALID")
    return state

def _lane_heads(state):
    heads={}
    for row in state["items"]:
        if row["phase"]=="PASS": continue
        lane=row["lane"]
        if lane not in heads: heads[lane]=row
    return [heads[k] for k in sorted(heads)]

def _gated_action(action):
    out=dict(action)
    out.update({
      "canonical_bound_worker_only":True,
      "free_chat_execution":False,
      "free_repo_search":False,
      "free_archive_search":False,
      "free_research_rerun":False,
      "alternate_route_allowed":False,
      "return_to_parallel_controller_required":True,
    })
    return out

def ready_actions(binding,state):
    verify(binding,state)
    if state["batch_phase"]=="ARTICLE_PRODUCTION":
        out=[]
        for row in _lane_heads(state):
            phase=row["phase"]
            if phase=="AUTHORING_REQUIRED": action={"action":"WRITE_DRAFT"}
            elif phase=="LT68_REQUIRED": action={"action":"RUN_CHECKER","checker":"LT68","draft_sha256":row["draft_sha256"]}
            elif phase=="PPM679_REQUIRED": action={"action":"RUN_CHECKER","checker":"PPM679","draft_sha256":row["draft_sha256"]}
            elif phase=="REPAIR_REQUIRED": action={"action":"REPAIR_DRAFT","finding_sha256":row.get("finding_sha256")}
            else: continue
            action.update({"item_index":row["item_index"],"plan_slot":row["plan_slot"],"lane":row["lane"]})
            out.append(_gated_action(action))
        return out
    if state["batch_phase"]=="PSERC_REQUIRED": return [_gated_action({"action":"RUN_PSERC","item_count":state["item_count"]})]
    if state["batch_phase"]=="ENDSTEMPEL_REQUIRED": return [_gated_action({"action":"RUN_ENDSTEMPEL","item_count":state["item_count"]})]
    if state["batch_phase"]=="COMPLETE": return [{"action":"STOP","reason":"BATCH_COMPLETE_ENDSTEMPEL_PASS"}]
    raise Blocked("BATCH_PHASE_INVALID")

def _row(state,index):
    if not isinstance(index,int) or index<0 or index>=len(state["items"]): raise Blocked("ITEM_INDEX_INVALID")
    return state["items"][index]

def _record_draft(binding,state,index,content):
    verify(binding,state); out=json.loads(json.dumps(state)); row=_row(out,index)
    if row["phase"]!="AUTHORING_REQUIRED": raise Blocked("WRITE_NOT_ALLOWED")
    if not isinstance(content,str) or not content.strip(): raise Blocked("DRAFT_EMPTY")
    sha=hashlib.sha256(content.encode()).hexdigest()
    row["revision"]=1; row["draft_sha256"]=sha; row["phase"]="LT68_REQUIRED"
    row["revision_history"]=[{"revision":1,"reason":"FIRST_DRAFT","content_utf8":content,"draft_sha256":sha}]
    return seal(out)

def _record_check(binding,state,index,checker,status,findings=None):
    verify(binding,state); out=json.loads(json.dumps(state)); row=_row(out,index); checker=checker.upper()
    if status not in {"PASS","REPAIR_REQUIRED"}: raise Blocked("CHECK_STATUS_INVALID")
    if checker=="LT68" and row["phase"]!="LT68_REQUIRED": raise Blocked("LT_ORDER_INVALID")
    if checker=="PPM679" and row["phase"]!="PPM679_REQUIRED": raise Blocked("PPM_ORDER_INVALID")
    if checker not in {"LT68","PPM679"}: raise Blocked("CHECKER_INVALID")
    if status=="REPAIR_REQUIRED":
        if not isinstance(findings,list) or not findings: raise Blocked("FINDINGS_REQUIRED")
        row["phase"]="REPAIR_REQUIRED"; row["repair_checker"]=checker
        row["finding_sha256"]=stable(findings); row["finding_count"]=len(findings)
        return seal(out)
    if checker=="LT68":
        row["lt68"]="PASS"; row["phase"]="PPM679_REQUIRED"; return seal(out)
    row["ppm679"]="PASS"; row["phase"]="PASS"; row["status"]="PASS"
    if all(x["phase"]=="PASS" for x in out["items"]):
        out["batch_phase"]="PSERC_REQUIRED"; out["status"]="PASS"
    return seal(out)

def _record_repair(binding,state,index,content):
    verify(binding,state); out=json.loads(json.dumps(state)); row=_row(out,index)
    if row["phase"]!="REPAIR_REQUIRED": raise Blocked("REPAIR_NOT_ALLOWED")
    if not isinstance(content,str) or not content.strip(): raise Blocked("REPAIR_EMPTY")
    sha=hashlib.sha256(content.encode()).hexdigest()
    if sha==row["draft_sha256"]: raise Blocked("REPAIR_UNCHANGED")
    row["revision"]+=1; row["repair_count"]+=1
    row["revision_history"].append({
      "revision":row["revision"],"reason":"BUNDLED_REPAIR_"+str(row.get("repair_checker") or ""),
      "source_finding_sha256":row.get("finding_sha256"),"source_finding_count":row.get("finding_count"),
      "content_utf8":content,"draft_sha256":sha
    })
    row["draft_sha256"]=sha; row["lt68"]="PENDING"; row["ppm679"]="PENDING"; row["phase"]="LT68_REQUIRED"
    row.pop("repair_checker",None); row.pop("finding_sha256",None); row.pop("finding_count",None)
    return seal(out)

def _record_stage(binding,state,stage):
    verify(binding,state); out=json.loads(json.dumps(state))
    if stage=="PSERC":
        if out["batch_phase"]!="PSERC_REQUIRED": raise Blocked("PSERC_NOT_ALLOWED")
        out["pserc"]="PASS"; out["batch_phase"]="ENDSTEMPEL_REQUIRED"
    elif stage=="ENDSTEMPEL":
        if out["batch_phase"]!="ENDSTEMPEL_REQUIRED" or out["pserc"]!="PASS": raise Blocked("ENDSTEMPEL_NOT_ALLOWED")
        out["endstempel"]="PASS"; out["batch_phase"]="COMPLETE"; out["status"]="PASS"
    else: raise Blocked("STAGE_INVALID")
    return seal(out)

def _load_persisted_state(binding,state_path):
    path=Path(state_path)
    if not path.is_file(): raise Blocked("DURABLE_STATE_MISSING")
    state=json.loads(path.read_text(encoding="utf-8"))
    verify(binding,state)
    return state

def _persist_state(binding,state_path,state):
    verify(binding,state)
    path=Path(state_path)
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+".tmp")
    tmp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    tmp.replace(path)
    readback=_load_persisted_state(binding,path)
    if readback.get("state_sha256")!=state.get("state_sha256"):
        raise Blocked("DURABLE_STATE_READBACK_MISMATCH")
    return readback

def record_draft(binding,state_path,index,content):
    state=_load_persisted_state(binding,state_path)
    return _persist_state(binding,state_path,_record_draft(binding,state,index,content))

def record_check(binding,state_path,index,checker,status,findings=None):
    state=_load_persisted_state(binding,state_path)
    return _persist_state(binding,state_path,_record_check(binding,state,index,checker,status,findings))

def record_repair(binding,state_path,index,content):
    state=_load_persisted_state(binding,state_path)
    return _persist_state(binding,state_path,_record_repair(binding,state,index,content))

def record_stage(binding,state_path,stage):
    state=_load_persisted_state(binding,state_path)
    return _persist_state(binding,state_path,_record_stage(binding,state,stage))

def simulate(binding,lanes):
    state=initial(binding,lanes)
    while state["batch_phase"]=="ARTICLE_PRODUCTION":
        acts=ready_actions(binding,state)
        for a in acts:
            i=a["item_index"]; action=a["action"]
            if action=="WRITE_DRAFT": state=_record_draft(binding,state,i,f"<article><h2>Artikel {i}</h2><p>synthetic-{i}</p></article>")
            elif action=="RUN_CHECKER": state=_record_check(binding,state,i,a["checker"],"PASS")
            else: raise Blocked("UNEXPECTED_SIM_ACTION")
    state=_record_stage(binding,state,"PSERC"); state=_record_stage(binding,state,"ENDSTEMPEL")
    if ready_actions(binding,state)[0]["action"]!="STOP": raise Blocked("SIM_NOT_TERMINAL")
    return state

def main(argv):
    try:
        if len(argv)!=5 or argv[1]!="simulate": raise Blocked("USE: k7_parallel_controller.py simulate BINDING LANES OUT")
        b=json.loads(Path(argv[2]).read_text(encoding="utf-8")); s=simulate(b,int(argv[3]))
        Path(argv[4]).write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"status":"PASS","lanes":s["article_lanes"],"items":s["item_count"],"batch_phase":s["batch_phase"]},sort_keys=True)); return 0
    except Exception as e:
        print("K7_PARALLEL_CONTROLLER_BLOCKED:"+str(e),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main(sys.argv))
