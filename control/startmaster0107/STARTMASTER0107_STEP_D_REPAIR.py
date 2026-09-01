#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, json, shutil, subprocess, sys, zlib
from pathlib import Path

EXPECTED_BASELINE_COMMIT="56937915a9ca02055ef142f03c5ec41024f9a668"
EXPECTED_REPAIR_BRANCH="startmaster0107-step-d-rootfix-20260901"
APPLY_SHA256="ff89f961e99b0e923b348221f7be21706f20d3760d2254cc98ed62beb0bdc841"
FROZEN_TEST_SHA256="899ec5b3af606547d7291e44eb82a9596d1f07aa2b70f7f41dd3a4abb71f3eb2"
FROZEN_CONTRACT_SHA256="822401d582a751a99e519341e9c1560d198f37778ed67ba42dd5b9a111b4b59f"
TEST_PATH="control/startmaster0107/test_rootfix_terminal_completion_proof.py"
_FALSE_MARKERS=("executor","not executable","no executable","ausführbar","materialisier","materializ")
_EMBEDDED_APPLY_ZLIB_B64="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"

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def sha256_file(p): return sha256_bytes(Path(p).read_bytes())
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def git(repo,*args,check=True):
    cp=subprocess.run(["git",*args],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and cp.returncode: raise RuntimeError("GIT_FAILED:"+" ".join(args)+":"+(cp.stderr or cp.stdout).strip()[:500])
    return (cp.stdout or "").strip(),cp.returncode

def identity(repo):
    head,_=git(repo,"rev-parse","HEAD")
    _,rc=git(repo,"merge-base","--is-ancestor",EXPECTED_BASELINE_COMMIT,"HEAD",check=False)
    if rc: raise RuntimeError("REPAIR_BASELINE_NOT_ANCESTOR:"+head)
    branch,_=git(repo,"branch","--show-current",check=False)
    return {"head":head,"branch":branch or "DETACHED_OR_SYNTHETIC"}

def false_terminal(term):
    if not isinstance(term,dict): return False
    if term.get("step_id")!="RUN_NEW_ARTICLE_BATCH_NO_STOP" or int(term.get("sequence",-1))!=107007: return False
    if term.get("status") not in {"BLOCKED","USER_ACTION_REQUIRED"}: return False
    ev=" ".join(str(x) for x in (term.get("evidence") or [])).lower()
    return ("fachworkflow" in ev or "workflow" in ev) and any(x in ev for x in _FALSE_MARKERS)

def recover_false_terminal(repo):
    statep=repo/"control/startmaster0107/CURRENT_STATE.json"; rootp=repo/"control/startmaster0107/PFERDE_ATELIER_START_HERE.json"
    state=load(statep); term=state.get("execution_gate_terminal")
    if term is None: return {"status":"NO_TERMINAL_RECOVERY_NEEDED","recovered":False}
    if term.get("status")=="PASS": raise RuntimeError("REFUSE_TO_RECOVER_PASS_TERMINAL")
    if not false_terminal(term): raise RuntimeError("REFUSE_TO_RECOVER_UNRECOGNIZED_TERMINAL_NONPASS")
    ctrl=repo/".pferde-quarantine/_control/startmaster0107"
    cp=load(ctrl/"BATCH_CHECKPOINT.json") if (ctrl/"BATCH_CHECKPOINT.json").is_file() else None
    rs=load(ctrl/"CURRENT_ROOM_STATE.json") if (ctrl/"CURRENT_ROOM_STATE.json").is_file() else None
    if cp and list(cp.get("completed_item_ids") or []): raise RuntimeError("REFUSE_TO_RECOVER_WITH_COMPLETED_ITEMS")
    if rs and list(rs.get("accepted_output_refs") or []): raise RuntimeError("REFUSE_TO_RECOVER_WITH_ACCEPTED_OUTPUTS")
    for pat in ("*OUTPUT_RELEASE_RECEIPT*","*FINAL_OUTPUT_RELEASE*"):
        if list(repo.glob(".pferde*/**/"+pat)): raise RuntimeError("REFUSE_TO_RECOVER_AFTER_OUTPUT_RELEASE")
    for rel in ("control/startmaster0107/CURRENT_STATE.json","control/startmaster0107/PFERDE_ATELIER_START_HERE.json"):
        clean,_=git(repo,"show","HEAD:"+rel); (repo/rel).write_text(clean+("" if clean.endswith("\n") else "\n"),encoding="utf-8")
    if ctrl.exists(): shutil.rmtree(ctrl)
    cap=repo/".pferde-capsule"
    if cap.exists(): shutil.rmtree(cap)
    ticket=str(term.get("ticket_id") or "")
    failed=repo/".pferde-quarantine"/ticket
    if len(ticket)==64 and failed.exists(): shutil.rmtree(failed)
    return {"status":"KNOWN_FALSE_107007_TERMINAL_RECOVERED","recovered":True,"progress_erased":False,"publish_allowed":False}

def load_embedded_apply():
    raw=zlib.decompress(base64.b64decode(_EMBEDDED_APPLY_ZLIB_B64))
    if sha256_bytes(raw)!=APPLY_SHA256: raise RuntimeError("EMBEDDED_APPLY_IDENTITY_INVALID")
    ns={"__name__":"startmaster0107_embedded_apply"}
    exec(compile(raw.decode("utf-8"),"<embedded-step-c-rootfix>","exec"),ns)
    return ns

def rootfix_applied(repo):
    testp=repo/TEST_PATH; bridge=repo/"control/single-door-boundary/codex_current_room_bridge.py"; runtime=repo/"control/output-quarantine/runtime_entry_gate.py"
    if not (testp.is_file() and bridge.is_file() and runtime.is_file()): return False
    if sha256_file(testp)!=FROZEN_TEST_SHA256: return False
    if "validate_item_terminal_completion" not in bridge.read_text(encoding="utf-8"): return False
    if "validate_final_terminal_completion" not in runtime.read_text(encoding="utf-8"): return False
    ptr=load(repo/"control/CURRENT_STARTMASTER.json"); statep=repo/"control/startmaster0107/CURRENT_STATE.json"; root=load(repo/"control/startmaster0107/PFERDE_ATELIER_START_HERE.json")
    return ptr.get("execution_entrance_gate_sha256")==sha256_file(runtime) and root.get("current_state_sha256")==sha256_file(statep) and load(statep).get("publish_allowed") is False

def apply_rootfix(repo):
    if rootfix_applied(repo): return "ROOTFIX_ALREADY_APPLIED_IDENTICAL"
    ns=load_embedded_apply(); ns["patch"](repo)
    if not rootfix_applied(repo): raise RuntimeError("ROOTFIX_POST_APPLY_IDENTITY_INVALID")
    return "ROOTFIX_APPLIED"

def frozen_tests(repo):
    p=repo/TEST_PATH
    if not p.is_file() or sha256_file(p)!=FROZEN_TEST_SHA256: raise RuntimeError("FROZEN_TEST_SCRIPT_IDENTITY_INVALID")
    cp=subprocess.run([sys.executable,str(p)],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if cp.returncode: raise RuntimeError("FROZEN_TESTS_FAILED:"+(cp.stderr or cp.stdout).strip()[:1000])
    out=json.loads(cp.stdout)
    if out.get("status")!="STARTMASTER0107_FROZEN_TERMINAL_PROOF_TESTS_PASS" or out.get("publish_allowed") is not False: raise RuntimeError("FROZEN_TEST_STATUS_INVALID")
    return out["status"]

def ready(repo):
    a=subprocess.run([sys.executable,"control/output-quarantine/runtime_entry_gate.py","start"],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if a.returncode: raise RuntimeError("OFFICIAL_ENTRY_START_FAILED:"+(a.stderr or a.stdout).strip()[:1000])
    start=json.loads(a.stdout)
    if start.get("publish_allowed") is not False: raise RuntimeError("OFFICIAL_ENTRY_PUBLISH_INVALID")
    b=subprocess.run([sys.executable,"control/single-door-boundary/codex_current_action.py","current"],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if b.returncode: raise RuntimeError("CURRENT_ACTION_FAILED:"+(b.stderr or b.stdout).strip()[:1000])
    cur=json.loads(b.stdout)
    if cur.get("status")!="CURRENT_BOUND_ACTION_READY": raise RuntimeError("CURRENT_ACTION_NOT_READY:"+str(cur.get("status")))
    for k in ("current_item","fachworkflow_prompt_ref","allowed_output_root","item_receipt_schema","submission_command"):
        if k not in cur: raise RuntimeError("CURRENT_ACTION_FIELD_MISSING:"+k)
    if cur.get("publish_allowed") is not False: raise RuntimeError("CURRENT_ACTION_PUBLISH_INVALID")
    return {"status":"STEP_D_REPAIR_READY_FOR_BOUND_FACHWORKFLOW","room_token":cur.get("room_token"),"current_article_id":(cur.get("current_item") or {}).get("canonical_article_id"),"fachworkflow_prompt_ref":cur.get("fachworkflow_prompt_ref"),"submission_command":cur.get("submission_command"),"publish_allowed":False}

def main(argv):
    if len(argv)!=1:
        print("usage: STARTMASTER0107_STEP_D_REPAIR.py <repo-root>",file=sys.stderr); return 64
    repo=Path(argv[0]).resolve()
    try:
        ident=identity(repo); recovery=recover_false_terminal(repo); rootfix=apply_rootfix(repo); frozen=frozen_tests(repo); rdy=ready(repo)
        print(json.dumps({"ok":True,"status":"STARTMASTER0107_STEP_D_REPAIR_PASS_READY","repository_head":ident["head"],"repository_branch":ident["branch"],"expected_repair_branch":EXPECTED_REPAIR_BRANCH,"recovery":recovery,"rootfix":rootfix,"frozen_tests":frozen,"frozen_test_contract_sha256":FROZEN_CONTRACT_SHA256,"ready":rdy,"new_controller_created":False,"new_executor_created":False,"domain_or_quality_logic_changed":False,"publish_allowed":False,"next_action":"EXECUTE_CURRENT_BOUND_ITEM_NOW_USING_FACHWORKFLOW_PROMPT_REF_THEN_SUBMISSION_COMMAND"},ensure_ascii=False,indent=2)); return 0
    except Exception as e:
        print(json.dumps({"ok":False,"status":"STARTMASTER0107_STEP_D_REPAIR_BLOCKED","error":str(e),"publish_allowed":False},ensure_ascii=False,indent=2)); return 2

if __name__=="__main__": raise SystemExit(main(sys.argv[1:]))
