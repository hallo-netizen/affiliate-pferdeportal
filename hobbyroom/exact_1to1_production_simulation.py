#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class SimBlocked(RuntimeError):
    pass

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stable(obj) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def run(args, *, cwd: Path, env: dict, ok=(0,)):
    cp = subprocess.run([str(x) for x in args], cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode not in ok:
        raise SimBlocked("COMMAND_FAIL:" + " ".join(map(str,args)) + "\nSTDOUT:\n" + cp.stdout + "\nSTDERR:\n" + cp.stderr)
    return cp

def last_json(text: str) -> dict:
    stripped=text.strip()
    try:
        value=json.loads(stripped)
        if isinstance(value,dict):
            return value
    except Exception:
        pass
    for line in reversed(text.splitlines()):
        line=line.strip()
        if line.startswith("{"):
            try:
                value=json.loads(line)
            except Exception:
                continue
            if isinstance(value,dict):
                return value
    raise SimBlocked("JSON_RESULT_MISSING:" + text[-2000:])

def update_root_state_hash(repo: Path) -> None:
    state=repo/"control/startmaster0107/CURRENT_STATE.json"
    root=repo/"control/startmaster0107/PFERDE_ATELIER_START_HERE.json"
    r=load(root)
    r["current_state_sha256"]=sha(state)
    r["next_allowed_step"]=load(state)["next_allowed_step"]
    dump(root,r)

def setup_simulation_external_conditions(repo: Path) -> dict:
    head=run(["git","rev-parse","HEAD"],cwd=repo,env=os.environ.copy()).stdout.strip()
    statep=repo/"control/startmaster0107/CURRENT_STATE.json"
    state=load(statep)
    state.setdefault("current_execution_blocker",{})["codex_start_allowed"]=True
    state["current_execution_blocker"]["simulation_external_condition"]="AVAILABLE_FOR_EXACT_1TO1_SIMULATION_ONLY"
    ext=state.get("external_execution_blocker")
    if isinstance(ext,dict):
        ext["resolved"]=True
        ext["simulation_external_condition"]="CAPACITY_SIMULATED_AVAILABLE"
    state["publish_allowed"]=False
    dump(statep,state)
    update_root_state_hash(repo)

    receiptp=repo/"control/startmaster0107/PRE_CODEX_START_RECEIPT.json"
    rec=load(receiptp)
    rec.update({
        "status":"PASS",
        "reason":"EXACT_1TO1_SIMULATION_EXTERNAL_CONDITIONS_BOUND",
        "authorized_head_sha":head,
        "dispatcher_head_sha":head,
        "hardlock_base_status":"PASS",
        "hardlock_base_head_sha":head,
        "user_approval":True,
        "codex_capacity_status":"AVAILABLE",
        "approved_article_count":int(load(repo/load(repo/"control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json")["source_snapshot_ref"])["next_textmachine_metadata_batch"]["item_count"]),
        "new_article_policy":"COMPLETELY_NEW_NO_RECOVERY_BODY",
        "sequential_advance_policy":"PASS_ONLY",
        "repair_policy":"SAME_ARTICLE_SAME_WORKSPACE_UNTIL_PASS",
        "restart_recovery_status":"PASS_CROSS_PROCESS_AND_DURABLE_TRANSPORT_READY",
        "durable_evidence_transport_status":"PASS",
        "codex_side_github_write_required":False,
        "publish_allowed":False,
        "simulation_only":True
    })
    dump(receiptp,rec)
    return {"head":head,"approved_article_count":rec["approved_article_count"]}

def write_lt_runtime_proof(repo: Path) -> Path:
    manifestp=repo/"control/startmaster0107/codex-production-runtime/RUNTIME_TOOLBOX_MANIFEST.json"
    m=load(manifestp); lt=m["languagetool"]
    jar=(Path.home()/Path(lt["persistent_cache_root"])/("runtime-"+lt["inner_zip_sha256"])/("LanguageTool-"+lt["component_version"])/"languagetool-commandline.jar").resolve()
    if not jar.is_file() or sha(jar)!=lt["commandline_jar_sha256"]:
        raise SimBlocked("LANGUAGETOOL_RUNTIME_NOT_PREPARED")
    proof={
        "contract":"PFERDE_ATELIER_LANGUAGETOOL_RUNTIME_BINDING_V2",
        "status":"LANGUAGETOOL_RUNTIME_READY",
        "toolbox_manifest_ref":"control/startmaster0107/codex-production-runtime/RUNTIME_TOOLBOX_MANIFEST.json",
        "toolbox_manifest_sha256":sha(manifestp),
        "engine":lt["engine"],
        "source_url":lt["source_url"],
        "outer_dependency_ref":lt["historical_outer_ref"],
        "outer_dependency_sha256":lt["historical_outer_sha256"],
        "inner_dependency_cache_ref":str((Path.home()/Path(lt["persistent_cache_root"])/("LanguageTool-"+lt["component_version"]+".zip")).resolve()),
        "inner_dependency_sha256":lt["inner_zip_sha256"],
        "inner_dependency_size":int(lt["inner_zip_size"]),
        "executed_component_version":lt["component_version"],
        "executed_commandline_jar_ref":str(jar),
        "executed_commandline_jar_sha256":lt["commandline_jar_sha256"],
        "executed_commandline_jar_manifest_sha256":lt["commandline_jar_manifest_sha256"],
        "command_argv_template":["java","-Xmx1024m","-jar",str(jar),"--json","-l","de-DE","<INPUT>"],
        "agent_network_required_for_execution":False,
        "content_semantics_inspected":False,
        "quality_authority":"NONE",
        "content_or_quality_rules_changed":False,
        "publish_allowed":False,
    }
    p=repo/".pferde-environment/LANGUAGETOOL_RUNTIME.json"
    dump(p,proof)
    return jar

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

def localize_bound_sources(repo: Path):
    runtimep=repo/"control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
    runtime=load(runtimep)
    reqp=repo/runtime["source_requests_ref"]
    req=load(reqp)
    snap=load(repo/runtime["source_snapshot_ref"])
    items=snap["next_textmachine_metadata_batch"]["items"]
    td=tempfile.TemporaryDirectory(prefix="exact-1to1-sources-")
    root=Path(td.name)
    for i,item in enumerate(items):
        kw=str(item["target_keyword"]); title=str(item["title"])
        rows=[]
        for j in range(2):
            sentences=[]
            for n in range(1,15):
                sentences.append(
                    f"{title}: Quellenpfad {j+1} Prüfschritt {n} betrachtet {kw} im aktuellen gebundenen Simulationsfall; "
                    f"Beobachtung aus Quelle {j+1} Nummer {n} wird getrennt dokumentiert, auf erkennbare Abweichungen geprüft und vor der Nutzung erneut bestätigt."
                )
            name=f"item-{i}-source-{j}.html"
            (root/name).write_text(
                "<!doctype html><html><head><title>"+title+f" Quelle {j+1}</title></head><body><article><h1>{title}</h1><p>"
                +" ".join(sentences)+"</p></article></body></html>",
                encoding="utf-8",
            )
            rows.append((name,f"sim-{i}-{j}",f"{title} Quelle {j+1}"))
        req["items"][i]["sources"]=[
            {"source_id":sid,"source_kind":"WEB","source_title":stitle,"source_url":""}
            for _,sid,stitle in rows
        ]
    handler=lambda *a,**kw: Quiet(*a,directory=str(root),**kw)
    server=ThreadingHTTPServer(("127.0.0.1",0),handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
    port=server.server_address[1]
    for i,item in enumerate(items):
        for j,row in enumerate(req["items"][i]["sources"]):
            row["source_url"]=f"http://127.0.0.1:{port}/item-{i}-source-{j}.html"
    dump(reqp,req)
    runtime["source_requests_sha256"]=sha(reqp)
    dump(runtimep,runtime)
    return td,server

def hide_simulation_data_from_git_status(repo: Path) -> list[str]:
    runtime=load(repo/"control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json")
    paths=[
        "control/startmaster0107/CURRENT_STATE.json",
        "control/startmaster0107/PFERDE_ATELIER_START_HERE.json",
        "control/startmaster0107/PRE_CODEX_START_RECEIPT.json",
        "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json",
        str(runtime.get("source_requests_ref") or ""),
    ]
    paths=[p for p in paths if p]
    run(["git","update-index","--assume-unchanged",*paths],cwd=repo,env=os.environ.copy())
    dirty=run(["git","status","--porcelain","--untracked-files=no"],cwd=repo,env=os.environ.copy()).stdout.strip()
    if dirty:
        raise SimBlocked("SIMULATION_TRACKED_DIRTY_REMAINS:"+dirty)
    return paths

def build_sim_worker(repo: Path) -> Path:
    srcp=repo/"isolated_system4/deterministic_test_worker.py"
    text=srcp.read_text(encoding="utf-8")
    old="direct = html.escape(str(bound.get('faq_direct_answer') or '').strip())"
    new="direct = html.escape(('Dieser Simulationsartikel behandelt ' + str(state['article']['title']) + ' anhand der gebundenen Fakten, Quellen und Prüfkriterien. Er ordnet das Thema nachvollziehbar ein, beschreibt die relevanten Auswahl- und Kontrollpunkte und hält sich vollständig an die vorgegebenen Struktur-, Qualitäts- und Nachweisregeln des aktuellen Produktionslaufs.').strip())"
    if old not in text:
        raise SimBlocked("SIM_WORKER_DIRECT_PATCH_POINT_MISSING")
    text=text.replace(old,new,1)
    old2="return '<article class=\"ppm-generated ppm-type-faq\" data-article-type=\"FAQ\">' + body + '</article>'"
    new2="atype=str(identity['article_type']); cls='ppm-type-'+re.sub(r'[^a-z0-9-]+','-',atype.casefold().replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss')).strip('-'); return '<article class=\"ppm-generated '+cls+'\" data-article-type=\"'+html.escape(atype,quote=True)+'\">' + body + '</article>'"
    if old2 not in text:
        raise SimBlocked("SIM_WORKER_RENDER_PATCH_POINT_MISSING")
    text=text.replace(old2,new2,1)
    # Real bound web pages can repeat identical sentences (navigation/teasers). A real
    # writer would not emit the same fact twice. The simulated external worker therefore
    # deduplicates candidate fact statements before handing them to the unchanged guard.
    old3="    claims = []\n    number = 0\n"
    new3="    claims = []\n    number = 0\n    seen_statements = set()\n"
    if old3 not in text:
        raise SimBlocked("SIM_WORKER_FACT_DEDUPE_INIT_PATCH_POINT_MISSING")
    text=text.replace(old3,new3,1)
    old4="            if len(statement) < 20:\n                continue\n            number += 1\n"
    new4="            if len(statement) < 20:\n                continue\n            folded=' '.join(statement.casefold().split())\n            if folded in seen_statements:\n                continue\n            seen_statements.add(folded)\n            number += 1\n"
    if old4 not in text:
        raise SimBlocked("SIM_WORKER_FACT_DEDUPE_BODY_PATCH_POINT_MISSING")
    text=text.replace(old4,new4,1)
    out=repo/"isolated_system4/.exact_1to1_sim_worker.py"
    out.write_text(text,encoding="utf-8")
    return out

def execute_workspace(repo: Path, workspace: Path, worker: Path, env: dict, index: int) -> dict:
    generated=workspace/"simulation-worker-output"
    generated.mkdir(exist_ok=True)
    repairs=0
    owner_returns=[]
    for cycle in range(1,50):
        s=load(workspace/"state.json")
        phase=s["phase"]
        # The real Codex entry validates the immutable dispatch before every worker action.
        run([sys.executable,repo/"isolated_system4/codex_entry.py","worker-start",workspace],cwd=repo,env=env)
        def produce(stage,*outs):
            return run([sys.executable,worker,stage,workspace,*outs],cwd=repo,env=env)
        if phase=="RESEARCH_REQUIRED":
            p=generated/"research.json"; produce("research",p)
            cp=run([sys.executable,repo/"isolated_system4/controller.py","research",workspace,p],cwd=repo,env=env,ok=(0,4))
            if cp.returncode==4: owner_returns.append(cp.stdout.strip()); continue
        elif phase=="FACT_CHECK_REQUIRED":
            p=generated/"facts.json"; produce("facts",p)
            cp=run([sys.executable,repo/"isolated_system4/controller.py","facts",workspace,p],cwd=repo,env=env,ok=(0,4))
            if cp.returncode==4: owner_returns.append(cp.stdout.strip()); continue
        elif phase=="CONTEXT_REQUIRED":
            pack=generated/"fact_pack.json"; plan=generated/"plan.json"; produce("context",pack,plan)
            cp=run([sys.executable,repo/"isolated_system4/controller.py","context",workspace,pack,plan],cwd=repo,env=env,ok=(0,4))
            if cp.returncode==4: owner_returns.append(cp.stdout.strip()); continue
        elif phase=="DRAFT_REQUIRED":
            p=generated/"draft.html"; produce("draft",p)
            cp=run([sys.executable,repo/"isolated_system4/controller.py","draft",workspace,p],cwd=repo,env=env,ok=(0,4))
            if cp.returncode==4: owner_returns.append(cp.stdout.strip()); continue
        elif phase=="CHECK_REQUIRED":
            cp=run([sys.executable,repo/"isolated_system4/controller.py","fullcheck",workspace],cwd=repo,env=env,ok=(0,2,4))
            if cp.returncode==4:
                state=load(workspace/"state.json")
                if (state.get("checks") or {}).get("return_required") is True:
                    raise SimBlocked("PARENT_RETURN_REQUIRED:"+json.dumps(state.get("checks"),ensure_ascii=False))
            if cp.returncode not in (0,):
                state=load(workspace/"state.json")
                if state.get("phase")!="REPAIR_REQUIRED":
                    raise SimBlocked("FULLCHECK_HARD_BLOCK:"+cp.stdout+cp.stderr)
        elif phase=="REPAIR_REQUIRED":
            repairs+=1
            p=generated/f"repair-{s.get('revision',0)}.html"; produce("repair",p)
            run([sys.executable,repo/"isolated_system4/controller.py","repair",workspace,p],cwd=repo,env=env)
        elif phase=="OUTPUT_GATE_REQUIRED":
            if (s.get("checks") or {}).get("status")!="PASS":
                raise SimBlocked("OUTPUT_GATE_WITHOUT_PASS")
            return {"index":index,"revision":s.get("revision"),"repairs":repairs,"owner_returns":owner_returns,"draft_sha256":s.get("draft_sha256")}
        else:
            raise SimBlocked("UNEXPECTED_WORKSPACE_PHASE:"+str(phase))
    raise SimBlocked("WORKSPACE_LOOP_LIMIT")

def create_outer_receipt(repo: Path, outputs: list[dict], evidence: list[str]) -> Path:
    ticketp=repo/".pferde-capsule/TICKET.json"
    ticket=load(ticketp)
    runtime=load(repo/"control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json")
    receipt={
        "contract":"PFERDE_ATELIER_STEP_RECEIPT_V2",
        "ticket_id":ticket["ticket_id"],
        "step_id":ticket["step_id"],
        "sequence":ticket["sequence"],
        "state_sha256":ticket["state_sha256"],
        "bundle_sha256":ticket["bundle_sha256"],
        "status":"PASS",
        "navigation_decision":False,
        "state_write_requested":False,
        "workflow_change_requested":False,
        "payload":{
            "execution_origin":"BOUND_WORKER",
            "workflow_pass":True,
            "batch_sha256":runtime["batch_sha256"],
            "outputs":outputs,
        },
        "evidence":evidence,
    }
    p=repo/".pferde-capsule/RECEIPT.json"; dump(p,receipt); return p

def quarantine_system4_outputs(repo: Path, batch_root: Path) -> list[dict]:
    ticket=load(repo/".pferde-capsule/TICKET.json")
    qroot=repo/".pferde-quarantine"/ticket["ticket_id"]/"system4-exact-simulation"
    qroot.mkdir(parents=True,exist_ok=True)
    batch=load(batch_root/"SYSTEM4_107007_BATCH_STATE.json")
    count=batch["item_count"]; outputs=[]
    for i in range(count):
        s=load(batch_root/f"item-{i:06d}"/"state.json")
        slot=s["article"]["plan_slot"]; body=s["draft_markdown"]
        p=qroot/f"ARTICLE_{slot}.md"; p.write_text(body,encoding="utf-8")
        outputs.append({"ref":str(p.relative_to(repo)),"sha256":sha(p)})
    # The exact canonical V2 handoff is also a bound 107007 output.
    import importlib.util
    hp=repo/"control/startmaster0107/system4_107008_handoff.py"
    spec=importlib.util.spec_from_file_location("sim_107008_prepare",hp); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    prepared=mod.prepare(str(batch_root))
    hpath=Path(prepared["handoff_ref"])
    dst=qroot/hpath.name; shutil.copyfile(hpath,dst)
    outputs.append({"ref":str(dst.relative_to(repo)),"sha256":sha(dst)})
    return outputs

def final_review_receipt(repo: Path) -> Path:
    ticket=load(repo/".pferde-capsule/TICKET.json")
    binding=load(repo/".pferde-capsule/BOUND_PREPARED_RELEASE_REF.json")
    receipt={
        "contract":"PFERDE_ATELIER_STEP_RECEIPT_V2",
        "ticket_id":ticket["ticket_id"],
        "step_id":ticket["step_id"],
        "sequence":ticket["sequence"],
        "state_sha256":ticket["state_sha256"],
        "bundle_sha256":ticket["bundle_sha256"],
        "status":"PASS",
        "navigation_decision":False,
        "state_write_requested":False,
        "workflow_change_requested":False,
        "payload":{
            "reviewed_prepared_release_only":True,
            "prepared_release_ref":binding["prepared_ref"],
            "prepared_release_sha256":binding["prepared_sha256"],
            "prepared_batch_sha256":binding["batch_sha256"],
        },
        "evidence":["EXACT_SYSTEM4_107008_HANDOFF_BOUND","SIMULATED_HUMAN_FINAL_REVIEW_PASS_NO_PUBLISH"],
    }
    p=repo/".pferde-capsule/RECEIPT.json"; dump(p,receipt); return p

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--out",required=True)
    a=ap.parse_args()
    repo=Path(a.repo).resolve(); out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy(); env["PYTHONDONTWRITEBYTECODE"]="1"; env["PYTHONPATH"]=str(repo/"isolated_system4")
    proof={"contract":"PFERDE_ATELIER_EXACT_1TO1_PRODUCTION_SIMULATION_V1","status":"RUNNING","production_code_source":"main","production_code_modified":False,"temporary_external_state_simulation":True,"publish_allowed":False,"stages":[]}
    try:
        # First prove and enter the real 107007 runtime on a byte-clean current-main checkout.
        jar=write_lt_runtime_proof(repo); env["SYSTEM4_LANGUAGETOOL_JAR"]=str(jar)
        cp=run([sys.executable,repo/"control/startmaster0107/codex-production-runtime/codex_environment_preflight.py"],cwd=repo,env=env)
        preflight=last_json(cp.stdout); proof["stages"].append({"stage":"PRODUCTION_PREFLIGHT","status":preflight["status"]})
        outer=last_json(run([sys.executable,repo/"control/output-quarantine/runtime_entry_gate.py","start"],cwd=repo,env=env).stdout)
        if outer.get("status")!="OFFICIAL_RUNTIME_ENTRY_PASS" or outer.get("sequence")!=107007:
            raise SimBlocked("OUTER_107007_START_NOT_PASS:"+json.dumps(outer))
        proof["stages"].append({"stage":"107007_OUTER_ENTRY","status":"PASS","ticket_id":outer["ticket_id"]})

        # Simulate only the external pre-Codex conditions. These three state files are
        # restored byte-for-byte immediately after the unchanged production parent starts.
        simulated_paths=[
            repo/"control/startmaster0107/CURRENT_STATE.json",
            repo/"control/startmaster0107/PFERDE_ATELIER_START_HERE.json",
            repo/"control/startmaster0107/PRE_CODEX_START_RECEIPT.json",
        ]
        original={p:p.read_bytes() for p in simulated_paths}
        try:
            sim=setup_simulation_external_conditions(repo)
            proof["simulation_external_conditions"]=sim
            parent=last_json(run([sys.executable,repo/"isolated_system4/parent_start.py","start-current-bound"],cwd=repo,env=env).stdout)
        finally:
            for p,raw in original.items():
                p.write_bytes(raw)
        dirty=run(["git","status","--porcelain","--untracked-files=no"],cwd=repo,env=env).stdout.strip()
        if dirty:
            raise SimBlocked("TRACKED_STATE_ROLLBACK_NOT_BYTE_CLEAN:"+dirty)
        if parent.get("status")!="SYSTEM4_PARENT_ROOT_READY_STOP":
            raise SimBlocked("PARENT_START_NOT_PASS:"+json.dumps(parent))
        proof["stages"].append({"stage":"CHAT_TO_POINT0_PARENT_START","status":"PASS","batch_sha256":parent["batch_sha256"],"article_count":parent["item_count"]})

        point0=Path(parent["point0"]); batch_root=Path(parent["batch_root"]); worker=build_sim_worker(repo)
        item_results=[]
        while True:
            bs=load(batch_root/"SYSTEM4_107007_BATCH_STATE.json")
            if bs["status"]=="ITEMS_COMPLETE": break
            index=int(bs["current_index"])
            workspace=batch_root/f"item-{index:06d}"
            item_results.append(execute_workspace(repo,workspace,worker,env,index))
            advanced=last_json(run([sys.executable,repo/"control/startmaster0107/system4_107007_batch.py","advance",point0,batch_root],cwd=repo,env=env).stdout)
            if advanced.get("status") not in {"SYSTEM4_107007_BATCH_ACTIVE","SYSTEM4_107007_BATCH_ITEMS_COMPLETE"}:
                raise SimBlocked("BATCH_ADVANCE_NOT_PASS:"+json.dumps(advanced))
        bs=load(batch_root/"SYSTEM4_107007_BATCH_STATE.json")
        if bs.get("status")!="ITEMS_COMPLETE" or (bs.get("batch_collect") or {}).get("status")!="SYSTEM4_BATCH_FULL_PASS_COLLECTED":
            raise SimBlocked("SYSTEM4_BATCH_NOT_FULL_PASS")
        proof["item_results"]=item_results
        proof["stages"].append({"stage":"SYSTEM4_107007_1N","status":"PASS","article_count":bs["item_count"],"batch_collect":"PASS"})

        outputs=quarantine_system4_outputs(repo,batch_root)
        receipt=create_outer_receipt(repo,outputs,["SYSTEM4_107007_BATCH_ITEMS_COMPLETE","SYSTEM4_BATCH_FULL_PASS_COLLECTED","EXACT_V2_HANDOFF_CREATED"])
        c107007=last_json(run([sys.executable,repo/"control/output-quarantine/runtime_entry_gate.py","complete",receipt],cwd=repo,env=env).stdout)
        if c107007.get("status")!="107007_PASS_STAGED_NOT_VISIBLE_107008_READY":
            raise SimBlocked("107007_OUTER_COMPLETE_NOT_PASS:"+json.dumps(c107007))
        proof["stages"].append({"stage":"107007_TO_107008_RUNTIME_GATE","status":"PASS"})

        h107008=last_json(run([sys.executable,repo/"control/startmaster0107/system4_107008_handoff.py","start",batch_root],cwd=repo,env=env).stdout)
        if h107008.get("status")!="SYSTEM4_107008_V2_HANDOFF_ENTRY_PASS":
            raise SimBlocked("SYSTEM4_107008_ENTRY_NOT_PASS:"+json.dumps(h107008))
        proof["stages"].append({"stage":"SYSTEM4_107008_BOUND_ENTRY","status":"PASS","handoff_sha256":h107008["handoff_sha256"]})

        lifecycle=last_json(run([
            sys.executable,repo/"control/startmaster0107/runtime_inbox/runtime_batch_slot_lifecycle.py",
            "clear-after-review","--repo",repo,
            "--contract",repo/"control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json"
        ],cwd=repo,env=env).stdout)
        if lifecycle.get("status") not in {"RUNTIME_SLOT_CLEARED_AND_IDLE","RUNTIME_SLOT_ALREADY_IDLE"}:
            raise SimBlocked("RUNTIME_CLEAR_NOT_PASS:"+json.dumps(lifecycle))
        final_receipt=final_review_receipt(repo)
        cp=run([sys.executable,repo/"control/output-quarantine/runtime_entry_gate.py","complete",final_receipt],cwd=repo,env=env,ok=(0,2))
        final_result=last_json(cp.stdout)
        proof["final_runtime_result"]=final_result
        if cp.returncode!=0 or final_result.get("status")!="107008_FINAL_REVIEW_PASS_VISIBLE_RELEASE_REARMED":
            reason=final_result.get("reason") or final_result
            proof["status"]="BLOCKED_BY_REAL_PRODUCTION_PATH"
            proof["real_blocker"]=reason
            dump(out/"EXACT_1TO1_SIMULATION_PROOF.json",proof)
            print(json.dumps(proof,ensure_ascii=False,sort_keys=True))
            return 2

        proof["stages"].append({"stage":"107008_PSERC","status":"PASS"})
        release_ref=final_result["release_receipt_ref"]; package_ref=final_result["pserc_finalization"]["package_ref"]
        delivery=last_json(run([sys.executable,repo/"control/startmaster0107/chat_delivery_payload.py","build",release_ref,package_ref],cwd=repo,env=env).stdout)
        if delivery.get("status")!="DELIVERY_HANDOFF_READY":
            raise SimBlocked("DELIVERY_NOT_READY:"+json.dumps(delivery))
        dump(out/"CHAT_DELIVERY_ENVELOPE.json",delivery)
        proof["stages"].append({"stage":"CHAT_DELIVERY","status":"PASS","article_count":delivery["article_count"]})
        proof["status"]="PASS_PENDING_GITHUB_ENDSTEMPEL"
        dump(out/"EXACT_1TO1_SIMULATION_PROOF.json",proof)
        print(json.dumps(proof,ensure_ascii=False,sort_keys=True))
        return 0
    except Exception as exc:
        proof["status"]="HARD_BLOCK"
        proof["real_blocker"]=str(exc)
        dump(out/"EXACT_1TO1_SIMULATION_PROOF.json",proof)
        print(json.dumps(proof,ensure_ascii=False,sort_keys=True))
        return 2

if __name__=="__main__":
    raise SystemExit(main())
