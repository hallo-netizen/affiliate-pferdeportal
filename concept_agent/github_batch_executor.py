#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, sys, tempfile, urllib.request, urllib.error
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
SYSTEM4=REPO/"isolated_system4"
if str(SYSTEM4) not in sys.path: sys.path.insert(0,str(SYSTEM4))
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))

import durable_event_log
import production_checks

CONTRACT="CONCEPT_AGENT_GITHUB_BATCH_EXECUTOR_V1"
MAX_STEPS=512

class Blocked(RuntimeError): pass

def canon(v:Any)->bytes:
    return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")

def sha_bytes(raw:bytes)->str: return hashlib.sha256(raw).hexdigest()
def sha_text(text:str)->str: return sha_bytes(text.encode("utf-8"))

def _github_token()->str:
    token=os.environ.get("GITHUB_TOKEN","").strip()
    if not token: raise Blocked("GITHUB_TOKEN_MISSING")
    return token

def _post_comment(issue:int, body:str)->None:
    req=urllib.request.Request(
        f"https://api.github.com/repos/hallo-netizen/affiliate-pferdeportal/issues/{issue}/comments",
        data=json.dumps({"body":body},ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization":"Bearer "+_github_token(),
            "Accept":"application/vnd.github+json",
            "Content-Type":"application/json",
            "X-GitHub-Api-Version":"2022-11-28",
            "User-Agent":"pferdeatelier-github-batch-executor",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req,timeout=30) as fh:
            if int(getattr(fh,"status",0)) not in {200,201}: raise Blocked("EVENT_POST_HTTP_INVALID")
    except urllib.error.HTTPError as exc:
        raise Blocked("EVENT_POST_HTTP_"+str(exc.code)) from exc

def _seal(current:dict, kind:str, raw:bytes)->None:
    event=durable_event_log.make_event(current,current["allowed_action"],kind,raw)
    body=durable_event_log.EVENT_CONTRACT+"\n"+json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    issue=durable_event_log._discover_issue(current["batch_sha256"])
    _post_comment(issue,body)

def _current()->tuple[list[dict],dict]:
    return durable_event_log._current(None)

def _exact_input_path(current:dict,index:int)->Path|None:
    root=os.environ.get("CONCEPT_AGENT_PREWRITTEN_DIR","").strip()
    if not root: return None
    binding=current.get("production_binding")
    if not isinstance(binding,dict): return None
    slot=binding["items"][index]["identity"]["plan_slot"]
    p=REPO/root/f"{index:02d}_{slot}.md"
    return p if p.is_file() else None

def _response_text(value:dict)->str:
    for row in value.get("output",[]):
        if not isinstance(row,dict) or row.get("type")!="message": continue
        for part in row.get("content",[]):
            if isinstance(part,dict) and part.get("type") in {"output_text","text"} and isinstance(part.get("text"),str):
                return part["text"]
    raise Blocked("MODEL_OUTPUT_TEXT_MISSING")

def _model_body(*, item:dict, current_body:str|None, findings:list[dict], mode:str)->str:
    key=os.environ.get("OPENAI_API_KEY","").strip()
    if not key: raise Blocked("OPENAI_API_KEY_MISSING")
    model=os.environ.get("CONCEPT_AGENT_MODEL","gpt-5.6-sol").strip()
    if mode=="write":
        task=("Schreibe exakt den gebundenen Artikel. Nutze nur die gelieferten gebundenen Quellen und Regeln. "
              "Keine Recherche, keine Workflowentscheidung, keine Metadatenänderung. Gib nur den vollständigen Artikeltext zurück.")
    else:
        task=("Repariere ausschließlich den aktuellen Artikel anhand der gelieferten exakten Findings. "
              "Ändere nur das Erforderliche, keine neue Recherche, keine Metadaten-/Workflowänderung. "
              "Gib den vollständigen korrigierten Artikeltext zurück.")
    payload={
      "model":model,
      "input":[
        {"role":"developer","content":"Du bist ausschließlich gebundener Schreib-/Reparaturarbeiter. Du hast keine Workflow-, Prüf-, Routing- oder Publish-Autorität."},
        {"role":"user","content":json.dumps({"task":task,"item":item,"current_body":current_body,"findings":findings},ensure_ascii=False)}
      ],
      "text":{"format":{"type":"json_schema","name":"bound_article","strict":True,
        "schema":{"type":"object","additionalProperties":False,"properties":{"body":{"type":"string"}},"required":["body"]}}}
    }
    req=urllib.request.Request("https://api.openai.com/v1/responses",
      data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
      headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=240) as fh: result=json.load(fh)
    except urllib.error.HTTPError as exc:
        raise Blocked("MODEL_HTTP_"+str(exc.code)) from exc
    try: parsed=json.loads(_response_text(result))
    except Exception as exc: raise Blocked("MODEL_JSON_INVALID") from exc
    body=parsed.get("body") if isinstance(parsed,dict) else None
    if not isinstance(body,str) or not body.strip(): raise Blocked("MODEL_BODY_EMPTY")
    return body

def _latest_checker_payload(rows:list[dict],current:dict)->dict:
    cfg=durable_event_log._current_batch()
    _,events=durable_event_log.event_chain(rows,cfg)
    for event in reversed(events):
        if event.get("executed_action",{}).get("action")=="RUN_CHECKER":
            return durable_event_log.payload_json(event)
    raise Blocked("REPAIR_FINDINGS_EVENT_MISSING")

def _lt_result(body:str)->dict:
    digest=sha_text(body)
    try:
        evidence=production_checks.run_languagetool(REPO,body)
        public={k:v for k,v in evidence.items() if not str(k).startswith("_")}
        return {"status":"PASS","checker":"LT68","content_sha256":digest,"evidence":public}
    except production_checks.RepairRequired as exc:
        findings=[dict(x,repair_owner="DRAFT_WORKER") for x in exc.findings]
        return {"status":"REPAIR_REQUIRED","checker":"LT68","content_sha256":digest,"findings":findings}

def _bound_fact_pack(item:dict)->tuple[dict,str]:
    research=item.get("research_bound") if isinstance(item.get("research_bound"),dict) else {}
    sources=research.get("sources") if isinstance(research.get("sources"),list) else []
    if not sources: raise Blocked("BOUND_RESEARCH_SOURCES_MISSING")
    source_id=hashlib.sha256(canon(research)).hexdigest()
    claims=[]
    for pos,src in enumerate(sources):
        ev=str(src.get("evidence") or "").strip()
        sid=str(src.get("source_id") or "").strip()
        if not ev or not sid: raise Blocked("BOUND_RESEARCH_SOURCE_INVALID")
        claims.append({
          "fact_id":hashlib.sha256((source_id+"|"+sid+"|"+str(pos)).encode()).hexdigest(),
          "source_id":sid,
          "statement":ev,
          "evidence_text":ev,
          "evidence_text_sha256":hashlib.sha256(ev.encode()).hexdigest(),
          "source_url":src.get("source_url"),
          "claim_status":"FULLY_SUPPORTED",
          "article_types":[item["identity"]["article_type"]],
        })
    pack={"contract":"canonical_fact_pack_v1","status":"SOURCE_VERIFIED_PRODUCTION_READY",
          "source_snapshot_id":source_id,"fact_pack_id":source_id,"sources":sources,"claims":claims}
    return pack,source_id

def _runtime_plan(item:dict,source_id:str)->dict:
    plan=json.loads(json.dumps(item["production_plan_item"]))
    plan["source_snapshot_id"]=source_id
    links=item.get("link_bindings") if isinstance(item.get("link_bindings"),list) else []
    role_map={}
    for row in links:
        if isinstance(row,dict) and row.get("role"):
            role_map[str(row["role"])]=dict(row)
    runtime=plan.get("runtime_order") if isinstance(plan.get("runtime_order"),dict) else {}
    runtime["links"]=role_map
    plan["runtime_order"]=runtime
    return plan

def _ppm_result(item:dict,body:str)->dict:
    digest=sha_text(body)
    pack,source_id=_bound_fact_pack(item)
    plan=_runtime_plan(item,source_id)
    try:
        ev=production_checks.run_ppm_content_validator(REPO,body,pack,plan,None)
        return {"status":"PASS","checker":"PPM679","content_sha256":digest,"evidence":ev}
    except production_checks.RepairRequired as exc:
        findings=[]
        for row in exc.findings:
            row=dict(row)
            if not row.get("repair_owner"):
                try: row["repair_owner"]=production_checks._ppm_repair_owner(row)
                except Exception: pass
            findings.append(row)
        return {"status":"REPAIR_REQUIRED","checker":"PPM679","content_sha256":digest,"findings":findings}

def _checkpoint_body(current:dict,index:int)->str:
    state=current.get("checkpoint")
    if not isinstance(state,dict): raise Blocked("CHECKPOINT_MISSING")
    matches=[x for x in state.get("drafts",[]) if isinstance(x,dict) and x.get("item_index")==index]
    if len(matches)!=1: raise Blocked("CHECKPOINT_DRAFT_MISSING")
    body=matches[0].get("content_utf8")
    if not isinstance(body,str) or not body: raise Blocked("CHECKPOINT_DRAFT_BYTES_MISSING")
    if sha_text(body)!=matches[0].get("draft_sha256"): raise Blocked("CHECKPOINT_DRAFT_HASH_MISMATCH")
    return body

def _write_or_accept(current:dict,index:int)->bytes:
    p=_exact_input_path(current,index)
    if p is not None:
        raw=p.read_bytes()
        if not raw.strip(): raise Blocked("PREWRITTEN_DRAFT_EMPTY")
        return raw
    item=current["production_binding"]["items"][index]
    return _model_body(item=item,current_body=None,findings=[],mode="write").encode("utf-8")

def _repair(current:dict,rows:list[dict],index:int)->bytes:
    body=_checkpoint_body(current,index)
    result=_latest_checker_payload(rows,current)
    findings=result.get("findings") if isinstance(result.get("findings"),list) else []
    if not findings: raise Blocked("REPAIR_FINDINGS_MISSING")
    owners={str(x.get("repair_owner") or "").strip() for x in findings if isinstance(x,dict)}
    owners.discard("")
    if not owners and str(result.get("checker") or "").upper()=="LT68": owners={"DRAFT_WORKER"}
    if owners!={"DRAFT_WORKER"}:
        raise Blocked("UPSTREAM_OWNER_RETURN_REQUIRED:"+",".join(sorted(owners or {"UNKNOWN"})))
    item=current["production_binding"]["items"][index]
    repaired=_model_body(item=item,current_body=body,findings=findings,mode="repair")
    if sha_text(repaired)==sha_text(body): raise Blocked("REPAIR_DRAFT_UNCHANGED")
    return repaired.encode("utf-8")

def _batch_stage(action:str,current:dict)->dict:
    env_name="CONCEPT_AGENT_PSERC_CMD" if action=="RUN_PSERC" else "CONCEPT_AGENT_ENDSTEMPEL_CMD"
    raise Blocked(env_name+"_NOT_BOUND")

def step()->dict:
    rows,current=_current()
    action=current["allowed_action"]
    name=action.get("action")
    if name=="STOP": return {"status":"STOP","current":current}
    if name=="RESEARCH_ITEM": raise Blocked("RESEARCH_PROVIDER_NOT_BOUND_TO_GITHUB_EXECUTOR")
    if name=="WRITE_DRAFT":
        raw=_write_or_accept(current,int(action["item_index"]))
        _seal(current,"UTF8_GZIP_BASE64",raw)
    elif name=="RUN_CHECKER":
        idx=int(action["item_index"]); body=_checkpoint_body(current,idx)
        checker=str(action.get("checker") or "")
        result=_lt_result(body) if checker=="LT68" else _ppm_result(current["production_binding"]["items"][idx],body)
        _seal(current,"JSON_GZIP_BASE64",canon(result))
    elif name=="REPAIR_DRAFT":
        raw=_repair(current,rows,int(action["item_index"]))
        _seal(current,"UTF8_GZIP_BASE64",raw)
    elif name in {"RUN_PSERC","RUN_ENDSTEMPEL"}:
        result=_batch_stage(name,current)
        _seal(current,"JSON_GZIP_BASE64",canon(result))
    else:
        raise Blocked("ACTION_UNSUPPORTED:"+str(name))
    return {"status":"ADVANCED","action":name,"sequence":current["sequence"]+1}

def run()->dict:
    history=[]
    for _ in range(MAX_STEPS):
        out=step(); history.append(out)
        if out["status"]=="STOP":
            return {"contract":CONTRACT,"status":"PASS","steps":len(history)-1,
                    "batch_sha256":out["current"]["batch_sha256"],
                    "sequence":out["current"]["sequence"],"publish_allowed":False}
    raise Blocked("MAX_STEPS_EXCEEDED")

def main()->int:
    try:
        result=run()
        print(json.dumps(result,ensure_ascii=False,sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"contract":CONTRACT,"status":"BLOCKED","reason":str(exc),"publish_allowed":False},
                         ensure_ascii=False,sort_keys=True),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
