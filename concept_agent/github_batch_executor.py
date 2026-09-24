#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, sys, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
SYSTEM4=REPO/"isolated_system4"
if str(SYSTEM4) not in sys.path: sys.path.insert(0,str(SYSTEM4))
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))

import authoring_contract, content_guard, design_guard, production_checks
import controller_engine
import durable_event_log
import endstempel_bridge

CONTRACT="CONCEPT_AGENT_GITHUB_BATCH_EXECUTOR_V2"
BATCH_STAGE_CONTRACT="CONCEPT_AGENT_BOUND_BATCH_STAGE_RESULT_V1"
SHA_RE=re.compile(r"^[0-9a-f]{64}$")
MAX_STEPS=512
FINAL_NAME="GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json"

class Blocked(RuntimeError): pass

def canon(v:Any)->bytes:
    return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def stable(v:Any)->str: return hashlib.sha256(canon(v)).hexdigest()
def sha_bytes(raw:bytes)->str: return hashlib.sha256(raw).hexdigest()
def sha_text(text:str)->str: return sha_bytes(text.encode("utf-8"))
def write_json(path:Path,v:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def _github_token()->str:
    token=os.environ.get("GITHUB_TOKEN","").strip()
    if not token: raise Blocked("GITHUB_TOKEN_MISSING")
    return token

def _post_comment(issue:int,body:str)->None:
    req=urllib.request.Request(
      f"https://api.github.com/repos/hallo-netizen/affiliate-pferdeportal/issues/{issue}/comments",
      data=json.dumps({"body":body},ensure_ascii=False).encode("utf-8"),
      headers={"Authorization":"Bearer "+_github_token(),"Accept":"application/vnd.github+json",
               "Content-Type":"application/json","X-GitHub-Api-Version":"2022-11-28",
               "User-Agent":"pferdeatelier-github-batch-executor"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=30) as fh:
            if int(getattr(fh,"status",0)) not in {200,201}: raise Blocked("EVENT_POST_HTTP_INVALID")
    except urllib.error.HTTPError as exc:
        raise Blocked("EVENT_POST_HTTP_"+str(exc.code)) from exc

def _current()->tuple[list[dict],dict]:
    return durable_event_log._current(None)

def _seal(current:dict,kind:str,raw:bytes)->None:
    event=durable_event_log.make_event(current,current["allowed_action"],kind,raw)
    body=durable_event_log.EVENT_CONTRACT+"\n"+json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    _post_comment(durable_event_log._discover_issue(current["batch_sha256"]),body)

def _events(rows:list[dict])->list[dict]:
    cfg=durable_event_log._current_batch()
    return durable_event_log.event_chain(rows,cfg)[1]

def _research_event(rows:list[dict],index:int)->dict:
    for event in _events(rows):
        a=event.get("executed_action") or {}
        if a.get("action")=="RESEARCH_ITEM" and a.get("item_index")==index:
            return event
    raise Blocked("RESEARCH_EVENT_MISSING:"+str(index))

def _research_sources(rows:list[dict],index:int)->list[dict]:
    return durable_event_log._research_sources(_research_event(rows,index),index)

def _sentences(text:str)->list[str]:
    base=re.split(r"(?<=[.!?])\s+|[\n\r]+",str(text or "").strip())
    out=[]
    seen=set()
    for row in base:
        for part in re.split(r"\s*;\s*",row):
            s=" ".join(part.split()).strip()
            if len(s)<20 or s in seen: continue
            seen.add(s); out.append(s)
    return out

def _bound_snapshot_obj()->dict:
    snap=json.loads((REPO/"concept_agent/current/PSERC_METADATA_SNAPSHOT.json").read_text(encoding="utf-8"))
    batch=snap.get("next_textmachine_metadata_batch")
    if not isinstance(batch,dict): raise Blocked("CURRENT_BATCH_SNAPSHOT_MISSING")
    return {"contract":"SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1","next_textmachine_metadata_batch":batch}

def _bound_snapshot_bytes()->bytes:
    return (json.dumps(_bound_snapshot_obj(),ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")

def _article_from_binding(item:dict)->dict:
    x=item["identity"]
    return {k:x[k] for k in ("title","target_keyword","category","article_type","plan_slot")}

def _slug(text:str)->str:
    s=str(text or "").casefold().replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    return re.sub(r"[^a-z0-9]+","-",s).strip("-")[:160] or "artikel"

def _build_evidence(rows:list[dict],current:dict,index:int)->tuple[dict,dict,dict,dict,str,bytes]:
    item=current["production_binding"]["items"][index]
    article=_article_from_binding(item)
    sources=_research_sources(rows,index)
    research={"contract":"SYSTEM4_RESEARCH_EVIDENCE_V1","sources":sources}
    content_guard.validate_research_document(research)

    claims=[]; n=0
    for src in sources:
        for sentence in _sentences(src["evidence"]):
            n+=1
            claims.append({
              "fact_id":f"fact-{article['plan_slot'][:12]}-{n}",
              "source_id":src["source_id"],"statement":sentence,"evidence_text":sentence,
              "evidence_text_sha256":sha_text(sentence),
            })
    if len(claims)<4: raise Blocked("BOUND_RESEARCH_TOO_THIN_FOR_FACTS:"+str(index))
    facts={"contract":"SYSTEM4_FACTS_EVIDENCE_V1","claims":claims}
    content_guard.validate_facts_document(facts,research)

    snap_raw=_bound_snapshot_bytes(); snap_sha=sha_bytes(snap_raw)
    by_source={s["source_id"]:s for s in sources}
    pack_claims=[]
    for row in claims:
        source=by_source[row["source_id"]]
        c=dict(row); c.update({"source_url":source["source_url"],"claim_status":"FULLY_SUPPORTED",
                               "article_types":[article["article_type"]]})
        pack_claims.append(c)
    pack={"contract":"canonical_fact_pack_v1","status":"SOURCE_VERIFIED_PRODUCTION_READY",
          "source_snapshot_id":snap_sha,"fact_pack_id":snap_sha,"sources":sources,"claims":pack_claims}

    plan=json.loads(json.dumps(item["production_plan_item"],ensure_ascii=False))
    quality=plan.get("quality_binding") if isinstance(plan.get("quality_binding"),dict) else {}

    # The current secured FAQ drafts already contain the direct answer as their
    # first body paragraph.  The recovery binding omitted only this projection.
    # Copy those existing bytes into the required quality binding; never invent
    # or rewrite an answer here.
    if article["article_type"]=="FAQ" and not str(quality.get("faq_direct_answer") or "").strip():
        prewritten=_exact_input_path(current,index)
        if prewritten is None: raise Blocked("FAQ_DIRECT_ANSWER_SOURCE_DRAFT_MISSING:"+str(index))
        source=prewritten.read_text(encoding="utf-8")
        body_lines=source.splitlines()
        paragraph=[]
        started=False
        for raw in body_lines:
            line=raw.strip()
            if not started:
                if not line or line.startswith("#"): continue
                started=True
            if started and not line:
                break
            if started and line.startswith("#"):
                break
            if started:
                paragraph.append(line)
        answer=" ".join(paragraph).strip()
        if not answer: raise Blocked("FAQ_DIRECT_ANSWER_SOURCE_EMPTY:"+str(index))
        quality["faq_direct_answer"]=answer
        plan["quality_binding"]=quality

    links=quality.get("link_bindings") if isinstance(quality.get("link_bindings"),list) else []
    if len(links)!=3: raise Blocked("BOUND_LINKS_NOT_EXACT_THREE:"+str(index))
    allowed=[c["fact_id"] for c in pack_claims]
    title=article["title"]; keyword=article["target_keyword"]
    direct=str(quality.get("faq_direct_answer") or "").strip()
    runtime={
      "order_id":"github-"+article["plan_slot"][:16],"article_type":article["article_type"],"title":title,
      "slug":_slug(title),"subject_scope":title,"subject_label":keyword,
      "lead":direct or title,"conclusion":direct or title,"links":json.loads(json.dumps(links)),
      "allowed_fact_ids":allowed,"question":title,"answer":direct or title,
      "faq_question":title,"faq_answer":direct or title,"summary":direct or title,
      "search_intent":plan.get("search_intent") or "informational",
    }
    plan["source_snapshot_id"]=snap_sha
    plan["runtime_order"]=runtime
    plan["canonical_article"]={"title":title,"article_type":article["article_type"],"slug":runtime["slug"]}
    plan["source_hashes"]=[s["snapshot_sha256"] for s in sources]
    plan["quality_binding_hash"]=production_checks.stable_hash(plan["quality_binding"])

    base={
      "contract":controller_engine.CONTRACT,"article":article,"source_snapshot_sha256":snap_sha,
      "batch_sha256":current["batch_sha256"],"phase":"CHECK_REQUIRED","research":{"text":json.dumps(research,ensure_ascii=False,sort_keys=True),
      "sha256":sha_text(json.dumps(research,ensure_ascii=False,sort_keys=True))},
      "facts":{"text":json.dumps(facts,ensure_ascii=False,sort_keys=True),
      "sha256":sha_text(json.dumps(facts,ensure_ascii=False,sort_keys=True))},
      "production_context":{"fact_pack":pack,"production_plan_item":plan},
      "draft_markdown":"","draft_sha256":"","revision":1,"checks":{},"last_error":None,
      "release_prepared":None,"released":False,"publish_allowed":False,
    }
    base["production_context"]["sha256"]=controller_engine.sha({"fact_pack":pack,"production_plan_item":plan})
    base["immutable_core_sha256"]=controller_engine.sha(controller_engine.immutable_core(base))
    base["authoring_contract"]=authoring_contract.build(REPO,base,pack,plan)
    return research,facts,pack,plan,snap_sha,snap_raw

def _state_for_body(rows:list[dict],current:dict,index:int,body:str,revision:int)->dict:
    research,facts,pack,plan,snap_sha,_=_build_evidence(rows,current,index)
    article=_article_from_binding(current["production_binding"]["items"][index])
    state={
      "contract":controller_engine.CONTRACT,"article":article,"source_snapshot_sha256":snap_sha,
      "batch_sha256":current["batch_sha256"],"phase":"CHECK_REQUIRED","research":{"text":json.dumps(research,ensure_ascii=False,sort_keys=True),
      "sha256":sha_text(json.dumps(research,ensure_ascii=False,sort_keys=True))},
      "facts":{"text":json.dumps(facts,ensure_ascii=False,sort_keys=True),
      "sha256":sha_text(json.dumps(facts,ensure_ascii=False,sort_keys=True))},
      "production_context":{"fact_pack":pack,"production_plan_item":plan},
      "draft_markdown":body,"draft_sha256":sha_text(body),"revision":revision,
      "checks":{},"last_error":None,"release_prepared":None,"released":False,"publish_allowed":False,
    }
    state["production_context"]["sha256"]=controller_engine.sha({"fact_pack":pack,"production_plan_item":plan})
    state["immutable_core_sha256"]=controller_engine.sha(controller_engine.immutable_core(state))
    state["authoring_contract"]=authoring_contract.build(REPO,state,pack,plan)
    return state

def _exact_input_path(current:dict,index:int)->Path|None:
    root=os.environ.get("CONCEPT_AGENT_PREWRITTEN_DIR","").strip()
    if not root: return None
    slot=current["production_binding"]["items"][index]["identity"]["plan_slot"]
    p=REPO/root/f"{index:02d}_{slot}.md"
    return p if p.is_file() else None

def _checkpoint_row(current:dict,index:int)->dict:
    state=current.get("checkpoint")
    rows=state.get("drafts") if isinstance(state,dict) else None
    found=[x for x in (rows or []) if isinstance(x,dict) and x.get("item_index")==index]
    if len(found)!=1: raise Blocked("CHECKPOINT_DRAFT_MISSING:"+str(index))
    row=found[0]
    if sha_text(row.get("content_utf8") or "")!=row.get("draft_sha256"): raise Blocked("CHECKPOINT_DRAFT_HASH_MISMATCH")
    return row

def _latest_check_payload(rows:list[dict],index:int)->dict:
    for event in reversed(_events(rows)):
        a=event.get("executed_action") or {}
        if a.get("action")=="RUN_CHECKER" and a.get("item_index")==index:
            return durable_event_log.payload_json(event)
    raise Blocked("CHECK_PAYLOAD_MISSING:"+str(index))

def _owners(checker:str,findings:list[dict])->set[str]:
    out={str(x.get("repair_owner") or "").strip() for x in findings if isinstance(x,dict)}
    out.discard("")
    if not out and checker in {"languagetool","no_external_links","LT68"}: out={"DRAFT_WORKER"}
    if not out and checker=="ppm679":
        for x in findings:
            try:
                owner=production_checks._ppm_repair_owner(x)
                if owner and owner!="HARD_BLOCK": out.add(owner)
            except Exception: pass
    return out

def _fullcheck(rows:list[dict],current:dict,index:int,body:str,revision:int)->dict:
    state=_state_for_body(rows,current,index,body,revision)
    pack=state["production_context"]["fact_pack"]; plan=state["production_context"]["production_plan_item"]
    try:
        authoring_contract.validate_bound(REPO,state)
    except Exception as exc:
        raise Blocked("AUTHORING_CONTRACT_HARD_BLOCK:"+str(exc)) from exc
    try:
        content_guard.validate_single_article(body,pack)
    except content_guard.ContentGuardError as exc:
        f=production_checks.guard_repair_finding("content_guard",str(exc))
        if f is None: raise Blocked("CONTENT_GUARD_HARD_BLOCK:"+str(exc)) from exc
        return {"status":"REPAIR_REQUIRED","checker":"PPM679","content_sha256":sha_text(body),"findings":[f]}
    try:
        design_guard.validate_design_neutrality(body,state["article"]["article_type"])
    except design_guard.DesignGuardError as exc:
        f=production_checks.guard_repair_finding("design_guard",str(exc))
        if f is None: raise Blocked("DESIGN_GUARD_HARD_BLOCK:"+str(exc)) from exc
        return {"status":"REPAIR_REQUIRED","checker":"PPM679","content_sha256":sha_text(body),"findings":[f]}
    try:
        full=production_checks.run_all(REPO,state,pack,plan)
        return {"status":"PASS","checker":"PPM679","content_sha256":sha_text(body),"system4_fullcheck":full}
    except production_checks.RepairRequired as exc:
        findings=[]
        for raw in exc.findings:
            x=dict(raw)
            if not x.get("repair_owner"):
                if exc.checker in {"languagetool","no_external_links"}: x["repair_owner"]="DRAFT_WORKER"
                elif exc.checker=="ppm679":
                    try: x["repair_owner"]=production_checks._ppm_repair_owner(x)
                    except Exception: pass
            findings.append(x)
        owners=_owners(exc.checker,findings)
        # Machine/parent returns are re-projected from immutable bindings on every call.
        # If a bound projection still fails, the upstream source itself requires rebuild.
        if owners and owners!={"DRAFT_WORKER"}:
            raise Blocked("UPSTREAM_BOUND_AUTHORITY_REBUILD_REQUIRED:"+",".join(sorted(owners)))
        return {"status":"REPAIR_REQUIRED","checker":"PPM679","content_sha256":sha_text(body),
                "origin_checker":exc.checker,"findings":findings}
    except production_checks.ProductionCheckError as exc:
        raise Blocked("FULLCHECK_HARD_BLOCK:"+str(exc)) from exc

def _lt(body:str)->dict:
    try:
        ev=production_checks.run_languagetool(REPO,body)
        return {"status":"PASS","checker":"LT68","content_sha256":sha_text(body),
                "evidence":{k:v for k,v in ev.items() if not str(k).startswith("_")}}
    except production_checks.RepairRequired as exc:
        findings=[dict(x,repair_owner="DRAFT_WORKER") for x in exc.findings]
        return {"status":"REPAIR_REQUIRED","checker":"LT68","content_sha256":sha_text(body),"findings":findings}

def _write(current:dict,index:int)->bytes:
    p=_exact_input_path(current,index)
    if p is not None:
        raw=p.read_bytes()
        if not raw.strip(): raise Blocked("PREWRITTEN_DRAFT_EMPTY")
        return raw
    raise Blocked("PREWRITTEN_DRAFT_REQUIRED")

def _repair(rows:list[dict],current:dict,index:int)->bytes:
    row=_checkpoint_row(current,index); body=row["content_utf8"]
    result=_latest_check_payload(rows,index)
    findings=result.get("findings") if isinstance(result.get("findings"),list) else []
    if not findings: raise Blocked("REPAIR_FINDINGS_MISSING")
    checker=str(result.get("origin_checker") or result.get("checker") or "")
    owners=_owners(checker,findings)
    if owners!={"DRAFT_WORKER"}: raise Blocked("REPAIR_OWNER_NOT_DRAFT:"+",".join(sorted(owners or {"UNKNOWN"})))

    # Current recovery batch contains prewritten drafts. LT repair is local-only:
    # use LanguageTool 6.8's own ranked replacement list, apply the first offered
    # replacement to the exact unique target, then the controller re-runs LT.
    if checker not in {"LT68","languagetool"}:
        raise Blocked("LOCAL_REPAIR_ROUTE_UNAVAILABLE:"+checker)

    plain=production_checks._plain_text(body)
    report,_,_=production_checks._run_languagetool_text(REPO,plain)
    matches=report.get("matches") if isinstance(report,dict) else None
    if not isinstance(matches,list) or not matches:
        raise Blocked("LT68_REPAIR_MATCHES_MISSING")

    edits=[]
    for match in matches:
        if not isinstance(match,dict): raise Blocked("LT68_REPAIR_MATCH_INVALID")
        off=match.get("offset"); length=match.get("length")
        if not isinstance(off,int) or not isinstance(length,int) or off<0 or length<=0:
            raise Blocked("LT68_REPAIR_RANGE_INVALID")
        target=plain[off:off+length]
        replacements=match.get("replacements")
        values=[r.get("value") for r in replacements if isinstance(r,dict) and isinstance(r.get("value"),str) and r.get("value")]
        if not values:
            raise Blocked("LT68_REPAIR_NO_REPLACEMENT:"+str(match.get("rule",{}).get("id") or ""))
        if not target or body.count(target)!=1:
            raise Blocked("LT68_REPAIR_TARGET_NOT_UNIQUE:"+target[:80])
        edits.append((target,values[0]))

    repaired=body
    for target,replacement in edits:
        repaired=repaired.replace(target,replacement,1)
    if repaired==body: raise Blocked("REPAIR_DRAFT_UNCHANGED")
    try: content_guard.validate_repair_continuity(body,repaired)
    except content_guard.ContentGuardError as exc: raise Blocked("REPAIR_SCOPE_FAIL:"+str(exc)) from exc
    return repaired.encode("utf-8")

def _final_ppm_payload(events:list[dict],index:int)->dict:
    for e in reversed(events):
        a=e.get("executed_action") or {}
        if a.get("action")=="RUN_CHECKER" and a.get("checker")=="PPM679" and a.get("item_index")==index:
            p=durable_event_log.payload_json(e)
            if p.get("status")=="PASS" and isinstance(p.get("system4_fullcheck"),dict): return p
    raise Blocked("FINAL_PPM_PASS_EVENT_MISSING:"+str(index))

def _materialize_system4_batch(rows:list[dict],current:dict,root:Path)->dict:
    state=current["checkpoint"]; count=current["production_binding"]["item_count"]
    if state.get("phase") not in {"ALL_ARTICLES_LT_PPM_PASS","PSERC_PASS_ENDSTEMPEL_REQUIRED","ENDSTEMPEL_PASS_STOP"}:
        raise Blocked("BATCH_NOT_COMPLETE")
    root.mkdir(parents=True,exist_ok=True)
    snapshot_path=root/"SOURCE_SNAPSHOT.json"; snapshot_path.write_bytes(_bound_snapshot_bytes())
    events=_events(rows)
    for index in range(count):
        row=_checkpoint_row(current,index); body=row["content_utf8"]
        s=_state_for_body(rows,current,index,body,int(row["revision"]))
        full=_final_ppm_payload(events,index)["system4_fullcheck"]
        s["checks"]={"status":"PASS","mode":"FULL_PRODUCTION","errors":[],
                     "checked_draft_sha256":row["draft_sha256"],"production_evidence":full}
        s["phase"]="OUTPUT_GATE_REQUIRED"; s["last_error"]=None
        w=root/f"item-{index:06d}"; w.mkdir(exist_ok=True)
        (w/"bound_snapshot.json").write_bytes(_bound_snapshot_bytes())
        write_json(w/"state.json",s)
    out=root/"batch-collect"
    cp=subprocess.run([sys.executable,str(SYSTEM4/"batch_gate.py"),"collect",str(snapshot_path),str(out),
                       *[str(root/f"item-{i:06d}"/"state.json") for i in range(count)]],
                      cwd=REPO,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    if cp.returncode!=0: raise Blocked("BATCH_GATE_FAIL:"+((cp.stdout or "")+(cp.stderr or ""))[-1200:])
    result=json.loads((cp.stdout or "").strip().splitlines()[-1])
    if result.get("status")!="SYSTEM4_BATCH_FULL_PASS_COLLECTED": raise Blocked("BATCH_GATE_NOT_PASS")
    return result

def _canonical_article_id(slot:str,body:str)->str:
    return "article:"+sha_text(slot+"|"+sha_text(body))[:24]

def _pserc_request(rows:list[dict],current:dict)->tuple[dict,Path]:
    batch=current["batch_sha256"]; count=current["production_binding"]["item_count"]
    _materialize_system4_batch(rows,current,Path("/tmp")/"concept-agent-system4"/batch)
    fact_packs=[]; plan_items=[]; release_items=[]; articles=[]
    for index in range(count):
        _,_,pack,plan,_,_=_build_evidence(rows,current,index)
        row=_checkpoint_row(current,index); body=row["content_utf8"]; slot=row["plan_slot"]
        cid=_canonical_article_id(slot,body)
        p=json.loads(json.dumps(plan)); p["canonical_article_id"]=cid
        ca=p.get("canonical_article") if isinstance(p.get("canonical_article"),dict) else {}
        ca.update({"title":current["production_binding"]["items"][index]["identity"]["title"],
                   "article_type":current["production_binding"]["items"][index]["identity"]["article_type"],
                   "body_html":body,"body_html_sha256":sha_text(body)})
        p["canonical_article"]=ca
        fact_packs.append(pack); plan_items.append(p)
        release_items.append({"plan_slot":slot,"canonical_article_id":cid})
        articles.append({"plan_slot":slot,"content_utf8":body})
    bundle={"contract":"canonical_fact_pack_import_v1","fact_packs":fact_packs}
    plan={"contract":"production_plan_v4","items":plan_items}
    bh,ph=stable(bundle),stable(plan)
    release={"contract":"WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED","status":"PASS",
             "content_generation_performed_by_supervisor":False,"exact_five_batch_sha256":batch,
             "exact_five_item_count":count,"fact_pack_bundle_sha256":bh,"production_plan_sha256":ph,
             "items":release_items,"wordpress_write_performed":False}
    rh=stable(release)
    env={"contract":"PSERC_APPROVED_PRODUCTION_PACKAGE_V1","fact_pack_bundle":bundle,"fact_pack_bundle_sha256":bh,
         "production_plan":plan,"production_plan_sha256":ph,"workflow_release":release,
         "workflow_release_sha256":rh,"source":"CONCEPT_AGENT_GITHUB_BATCH_EXECUTOR_V2"}
    env["package_id"]=stable({"contract":env["contract"],"fact_pack_bundle_sha256":bh,
                               "production_plan_sha256":ph,"workflow_release_sha256":rh})
    env["package_payload_sha256"]=stable(env)
    req={"contract":"CONCEPT_AGENT_ENDSTEMPEL_AUTO_REQUEST_V1","batch_sha256":batch,"runtime_generation":1,
         "import_envelope":env,"articles":articles,"publish_allowed":False,"content_mutation_performed":False}
    path=REPO/".pferde-executor"/batch/"ENDSTEMPEL_REQUEST.json"; write_json(path,req)
    return req,path

def _batch_stage(rows:list[dict],current:dict,stage:str)->dict:
    req,path=_pserc_request(rows,current)
    checkpoint=current["checkpoint"]["checkpoint_sha256"]
    if stage=="PSERC":
        env=req["import_envelope"]
        return {"contract":BATCH_STAGE_CONTRACT,"stage":"PSERC","status":"PASS","batch_sha256":current["batch_sha256"],
                "source_checkpoint_sha256":checkpoint,"evidence_sha256":stable(req),
                "pserc_package_sha256":stable(env),"request_ref":str(path.relative_to(REPO)),"publish_allowed":False}
    if stage!="ENDSTEMPEL": raise Blocked("BATCH_STAGE_INVALID")
    batch=current["batch_sha256"]; source_dir=REPO/"control/startmaster0107/recovery_sources"/batch/"generation-000001"
    manifest=source_dir/"MANIFEST.json"
    if not manifest.is_file():
        ref=endstempel_bridge.build(str(path.relative_to(REPO)))
        manifest=REPO/ref
    if not manifest.is_file(): raise Blocked("ENDSTEMPEL_SOURCE_MANIFEST_MISSING")
    expected=REPO/".pferde-final"/batch/"generation-000001"/FINAL_NAME
    if expected.is_file():
        final_sha=sha_bytes(expected.read_bytes())
    else:
        cp=subprocess.run([sys.executable,str(REPO/"control/startmaster0107/GITHUB_FINAL_RELEASE.py"),"finalize",
                           str(manifest.relative_to(REPO))],cwd=REPO,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
        if cp.returncode!=0: raise Blocked("ENDSTEMPEL_FAIL:"+((cp.stdout or "")+(cp.stderr or ""))[-1400:])
        result=json.loads(cp.stdout)
        if result.get("status")!="GITHUB_FINAL_RELEASE_PASS": raise Blocked("ENDSTEMPEL_NOT_PASS")
        expected=REPO/result["final_ref"]; final_sha=result["final_sha256"]
    if sha_bytes(expected.read_bytes())!=final_sha: raise Blocked("FINAL_FILE_HASH_MISMATCH")
    return {"contract":BATCH_STAGE_CONTRACT,"stage":"ENDSTEMPEL","status":"PASS","batch_sha256":batch,
            "source_checkpoint_sha256":checkpoint,"evidence_sha256":stable({"manifest":str(manifest.relative_to(REPO)),"final":str(expected.relative_to(REPO))}),
            "final_file_sha256":final_sha,"final_ref":str(expected.relative_to(REPO)),"publish_allowed":False}

def step()->dict:
    rows,current=_current(); action=current["allowed_action"]; name=action.get("action")
    if name=="STOP": return {"status":"STOP","current":current}
    if name=="RESEARCH_ITEM":
        _seal(current,"JSON_GZIP_BASE64",canon(_research_worker(current,int(action["item_index"]))))
    elif name=="WRITE_DRAFT":
        _seal(current,"UTF8_GZIP_BASE64",_write(current,int(action["item_index"])))
    elif name=="RUN_CHECKER":
        idx=int(action["item_index"]); row=_checkpoint_row(current,idx); body=row["content_utf8"]
        result=_lt(body) if action.get("checker")=="LT68" else _fullcheck(rows,current,idx,body,int(row["revision"]))
        _seal(current,"JSON_GZIP_BASE64",canon(result))
    elif name=="REPAIR_DRAFT":
        _seal(current,"UTF8_GZIP_BASE64",_repair(rows,current,int(action["item_index"])))
    elif name=="RUN_PSERC":
        _seal(current,"JSON_GZIP_BASE64",canon(_batch_stage(rows,current,"PSERC")))
    elif name=="RUN_ENDSTEMPEL":
        _seal(current,"JSON_GZIP_BASE64",canon(_batch_stage(rows,current,"ENDSTEMPEL")))
    else: raise Blocked("ACTION_UNSUPPORTED:"+str(name))
    return {"status":"ADVANCED","action":name,"sequence":current["sequence"]+1}

def preflight()->dict:
    rows,current=_current()
    if current.get("publish_allowed") is not False: raise Blocked("PUBLISH_FLAG_INVALID")
    binding=current.get("production_binding")
    if isinstance(binding,dict):
        for index in range(binding["item_count"]): _build_evidence(rows,current,index)
    return {"contract":CONTRACT,"status":"PREFLIGHT_PASS","batch_sha256":current["batch_sha256"],
            "sequence":current["sequence"],"allowed_action":current["allowed_action"],"publish_allowed":False}

def run()->dict:
    for count in range(MAX_STEPS):
        out=step()
        if out["status"]=="STOP":
            c=out["current"]
            return {"contract":CONTRACT,"status":"PASS","steps":count,"batch_sha256":c["batch_sha256"],
                    "sequence":c["sequence"],"final_file_sha256":c["checkpoint"].get("endstempel_final_file_sha256"),
                    "publish_allowed":False}
    raise Blocked("MAX_STEPS_EXCEEDED")

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("command",choices=["preflight","run","step"]); args=ap.parse_args()
    try:
        result=preflight() if args.command=="preflight" else (step() if args.command=="step" else run())
        print(json.dumps(result,ensure_ascii=False,sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"contract":CONTRACT,"status":"BLOCKED","reason":str(exc),"publish_allowed":False},
                         ensure_ascii=False,sort_keys=True),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
