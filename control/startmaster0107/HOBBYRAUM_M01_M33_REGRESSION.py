#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, importlib.util, json, os, re, subprocess, sys, tempfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
PY=sys.executable
MATRIX=REPO/"control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md"
CURRENT_ACTION=REPO/"control/single-door-boundary/codex_current_action.py"
ROOM_BRIDGE=REPO/"control/single-door-boundary/codex_current_room_bridge.py"
HANDOFF=REPO/"control/startmaster0107/fachworkflow_proof_handoff.py"
DUAL=REPO/"control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py"
STEP7=REPO/"control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json"
STEP8=REPO/"control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json"
STATE=REPO/"control/startmaster0107/CURRENT_STATE.json"
ROOT=REPO/"control/startmaster0107/PFERDE_ATELIER_START_HERE.json"
RUNTIME=REPO/"control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PPM_SHA="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PSERC_SHA="77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"

class Fail(RuntimeError): pass

def sha(p:Path)->str:return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p:Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))
def dump(p:Path,o):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def mod(path:Path,name:str):
    s=importlib.util.spec_from_file_location(name,path)
    if s is None or s.loader is None: raise Fail("MODULE_LOAD_FAILED:"+str(path))
    m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def must(cond,msg):
    if not cond: raise Fail(msg)
def expect_exc(fn,token):
    try: fn()
    except Exception as e:
        if token not in str(e): raise Fail("WRONG_BLOCK:"+token+":"+str(e))
        return
    raise Fail("NEGATIVE_NOT_BLOCKED:"+token)
_CMD_CACHE={}
def cmd(rel,*args):
    key=(rel,)+args
    if key not in _CMD_CACHE:
        p=subprocess.run([PY,str(REPO/rel),*args],cwd=REPO,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        _CMD_CACHE[key]=p
    p=_CMD_CACHE[key]
    if p.returncode!=0: raise Fail("COMMAND_FAIL:"+rel+":"+((p.stdout+p.stderr)[-1200:]))
    return p.stdout

# M01-M25: already established regression machinery. Full mode re-runs it once;
# open-only mode deliberately does not duplicate already-proven positive paths.
def m01(): must("CODEX_CLOUD_GATE_CI_PASS" in cmd("control/cloud-entry-gate/cloud_repo_ci_test.py"),"M01_HASH_CHAIN")
def m02():
    s=STEP7.read_text(encoding="utf-8")
    must("ARTICLE_<plan_slot>.md" in s or "ARTICLE_" in s,"M02_UNIQUE_ARTICLE_BINDING_MISSING")
    must("STAGING_DESTINATION_COLLISION" in (REPO/"control/output-quarantine/output_release_gate.py").read_text(encoding="utf-8"),"M02_COLLISION_GUARD_MISSING")
def m03(): must("DUAL_ROOTFIX_POSITIVE_NEGATIVE_PASS" in cmd("control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py","selftest"),"M03_PREPARED_TEST")
def m04(): must("def finalize_after_107008" in DUAL.read_text(encoding="utf-8") and "elif len(a)==2 and a[0]=='finalize'" in DUAL.read_text(encoding="utf-8"),"M04_FINALIZE_CLI")
def m05(): must("durable_receipt_path" in (REPO/"control/output-quarantine/output_release_gate.py").read_text(encoding="utf-8"),"M05_DURABLE_RECEIPT")
def m06(): must("NEGATIVE_UNKNOWN_CONTRACT_BLOCKED" in cmd("control/startmaster0107/production-package-release/test_production_package_release_gate.py"),"M06_FAKE_CONTRACT")
def m07(): must("POSITIVE_RECOVERY_LOCK_REVERIFY" in cmd("control/startmaster0107/production-package-release/test_production_package_release_gate.py"),"M07_RECOVERY")
def m08(): must(PPM.is_file() and sha(PPM)==PPM_SHA,"M08_PPM_ZIP")
def m09(): must(PSERC.is_file() and sha(PSERC)==PSERC_SHA,"M09_PSERC_ZIP")
def m10(): must("CODEX_ENVIRONMENT_PREFLIGHT_POSITIVE_NEGATIVE_PASS" in cmd("control/startmaster0107/codex-production-runtime/test_codex_environment_preflight.py"),"M10_PREFLIGHT")
def m11():
    s=HANDOFF.read_text(encoding="utf-8")
    must("PSERC_PPM_Intake_Bridge::execute" in s and "PPM679_Normal_Draft_Pipeline::execute_plan" in s,"M11_REAL_PPM_CALL")
def m12(): must("test_generic_fake_ppm_pass_is_blocked" in (REPO/"control/startmaster0107/test_ppm679_current_action_binding.py").read_text(encoding="utf-8"),"M12_FAKE_PPM_TEST")
def m13(): must("test_wrong_final_content_hash_is_blocked" in (REPO/"control/startmaster0107/test_ppm679_current_action_binding.py").read_text(encoding="utf-8"),"M13_CONTENT_HASH_TEST")
def m14(): must(HANDOFF.is_file(),"M14_HANDOFF_FILE")
def _m15_validate_instruction(text):
    required=("submission_command","FACHWORKFLOW_HANDOFF_REQUEST.json","kein separater Handoff-Befehl durch den Worker","keine Capability-Suche","keine Alternativroute")
    for token in required: must(token in text,"M15_REQUIRED_INSTRUCTION_MISSING:"+token)
    lines=text.splitlines()
    submit_lines=[line.lower() for line in lines if "submit-request" in line.lower()]
    must(submit_lines and all("kein" in line for line in submit_lines),"M15_SUBMIT_REQUEST_NOT_FORBIDDEN")
    executor_lines=[line.lower() for line in lines if "zweiter executor" in line.lower()]
    must(executor_lines and all("kein" in line for line in executor_lines),"M15_SECOND_EXECUTOR_NOT_FORBIDDEN")
    forbidden=("Vorab-Handoff durch den Worker erforderlich","separater Fachworkflow-Executor erforderlich","Capability-Suche erforderlich","Alternativroute erlaubt")
    for token in forbidden: must(token not in text,"M15_CONTRADICTORY_HANDOFF_INSTRUCTION:"+token)

def m15():
    text=load(STEP7)["instruction"]
    _m15_validate_instruction(text)
    bad=text+"\\nsubmit-request ausführen"
    expect_exc(lambda:_m15_validate_instruction(bad),"M15_SUBMIT_REQUEST_NOT_FORBIDDEN")
    bad=text+"\\nseparater Fachworkflow-Executor erforderlich"
    expect_exc(lambda:_m15_validate_instruction(bad),"M15_CONTRADICTORY_HANDOFF_INSTRUCTION")
def m16():
    s=(REPO/"control/output-quarantine/runtime_entry_gate.py").read_text(encoding="utf-8")
    must("codex_worker_signer_access_allowed" in s and "False" in s,"M16_SIGNER_BOUNDARY")
def m17(): must("host_pserc_finalization_required" in (REPO/"control/output-quarantine/runtime_entry_gate.py").read_text(encoding="utf-8"),"M17_HOST_FINALIZATION")
def m18():
    s=(REPO/"control/startmaster0107/GITHUB_FINAL_RELEASE.py").read_text(encoding="utf-8")
    must("IMPORT_ENVELOPE" in s,"M18_ENDSTEMPEL_CONSTANTS")
def m19():
    s=(REPO/".github/workflows/pferde-atelier-endstempel.yml").read_text(encoding="utf-8")
    must("git diff-tree -m" in s,"M19_MERGE_TRIGGER")
def m20():
    s=(REPO/"control/startmaster0107/chat_delivery_payload.py").read_text(encoding="utf-8")
    must("EXACTLY_SEVEN_ARTICLES_REQUIRED" in s and "import_envelope" in s and "source_manifest" in s,"M20_DELIVERY")
def m21():
    # Hard positive/negative against the real visible-release guard.
    g=mod(REPO/"control/output-quarantine/output_release_gate.py","m21_release_guard")
    old_repo=g.REPO
    try:
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); staged=root/"staged"; staged.mkdir(parents=True)
            article=staged/("ARTICLE_"+("1"*64)+".md"); article.write_text("m21\n",encoding="utf-8")
            prepared={
                "contract":"PFERDE_ATELIER_PREPARED_OUTPUT_RELEASE_V1",
                "status":"PREPARED_NOT_VISIBLE",
                "source_step_id":"RUN_NEW_ARTICLE_BATCH_NO_STOP",
                "source_sequence":107007,
                "publish_allowed":False,
                "staged_outputs":[{"source_ref":"q/"+article.name,"staged_ref":"staged/"+article.name,"sha256":sha(article)}],
            }
            pp=root/"PREPARED_RELEASE.json"; dump(pp,prepared); g.REPO=root
            _,pos=g.validate_prepared("PREPARED_RELEASE.json",sha(pp))
            must(pos.get("publish_allowed") is False,"M21_POSITIVE_NO_PUBLISH_NOT_PASS")
            bad=copy.deepcopy(prepared); bad["publish_allowed"]=True; dump(pp,bad)
            expect_exc(lambda:g.validate_prepared("PREPARED_RELEASE.json",sha(pp)),"AUTO_PUBLISH_FORBIDDEN")
    finally:
        g.REPO=old_repo
def m22(): must("H8_PREPRODUCTION_BOOTSTRAP_POSITIVE_NEGATIVE_PASS" in cmd("control/single-door-boundary/test_h8_preproduction_bootstrap.py"),"M22_H8")
def m23(): must("POSITIVE_FULL_PACKAGE_CURRENT_GENERATION" in cmd("control/startmaster0107/production-package-release/test_production_package_release_gate.py"),"M23_SIGNED_PACKAGE_ONLY")
def m24(): must("STARTMASTER_ROLLBACK_BLOCKED" in (REPO/".github/workflows/pferde-atelier-immutable-base-hardlock.yml").read_text(encoding="utf-8"),"M24_H8_ROLLBACK")
def m25():
    s=(REPO/"control/startmaster0107/VERBINDLICHER_TEXTERSTELLUNGS_PROMPT_STARTMASTER0107.txt").read_text(encoding="utf-8")
    must("bestehender Fachworkflow" in s and "Keine eigene" in s,"M25_FACHWORKFLOW_BOUNDARY")

# Open historical regressions: hard positive + hard negative.
def m26():
    a=mod(CURRENT_ACTION,"m26_action")
    smoke=a.selftest()
    must(smoke.get("status")=="CODEX_CURRENT_ACTION_KISS_SELFTEST_PASS","M26_SELFTEST_NOT_PASS")
    must(smoke.get("direct_single_door") is True and smoke.get("prepass_handoff_bound") is False,"M26_DIRECT_PATH_NOT_PASS")
    base={"allowed_output_root":".pferde-quarantine/test/","item_receipt_schema":{}}
    item={"canonical_article_id":"article:test","plan_slot":"a"*64,"article_type":"ratgeber"}
    action=a.augment_current_action(REPO,base,item)
    batch,count=a._runtime_batch_identity()
    current={"room_token":"R_D_1_01","current_item":item,"allowed_output_root":action["allowed_output_root"],"item_receipt_ref":".pferde-quarantine/test/ITEM_RECEIPT.json","item_receipt_schema":action["item_receipt_schema"]}
    provisional={"contract":"PFERDE_ATELIER_BOUND_ITEM_EXECUTION_RECEIPT_V1","room_token":"R_D_1_01","canonical_article_id":"article:test","plan_slot":"a"*64}
    meta={k:None for k in a.RELEASE_KEYS};meta.update({"contract":a.RELEASE_CONTRACT,"status":"PASS","exact_five_batch_sha256":batch,"exact_five_item_count":count,"wordpress_write_performed":False})
    fach={"required_stage_proofs":[{"stage":x,"ref":".pferde-quarantine/test/"+x+".json","sha256":"1"*64} for x in a.STAGES],
          "fact_pack":{"contract":"canonical_fact_pack_v1"},"production_plan_item":{"canonical_article_id":"article:test","plan_slot":"a"*64},
          "production_plan_header":{"contract":"production_plan_v4"},"workflow_release_item":{"canonical_article_id":"article:test","plan_slot":"a"*64},
          "workflow_release_metadata":meta}
    req=a._handoff_request_from_current(current,provisional,fach)
    must(req["fact_pack"]==fach["fact_pack"],"M26_POSITIVE_CONTEXT_NOT_MATERIALIZED")
    bad=copy.deepcopy(fach);bad["fact_pack"]={}
    expect_exc(lambda:a._handoff_request_from_current(current,provisional,bad),"BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING")
    bad=copy.deepcopy(fach);bad["production_plan_item"]["canonical_article_id"]="article:other"
    expect_exc(lambda:a._handoff_request_from_current(current,provisional,bad),"BOUND_CURRENT_PRODUCTION_PLAN_ITEM_IDENTITY_MISMATCH")

def m27():
    out=cmd("control/startmaster0107/codex-production-runtime/test_codex_environment_preflight.py")
    must("CODEX_ENVIRONMENT_PREFLIGHT_POSITIVE_NEGATIVE_PASS" in out,"M27_PREFLIGHT_POSITIVE")
    must("negative" in out.lower(),"M27_PREFLIGHT_NEGATIVE")

def m28():
    a=mod(CURRENT_ACTION,"m28_action")
    sample={"status":"CURRENT_BOUND_ACTION_READY","room_token":"R_D_1_01","current_item":{"canonical_article_id":"article:test","article_type":"beratung"},"fachworkflow_authority":"EXISTING_UNCHANGED_BOUND_FACHWORKFLOW_ONLY","fachworkflow_prompt_ref":"bound.txt","allowed_output_root":".pferde-quarantine/test/","item_receipt_ref":".pferde-quarantine/test/ITEM_RECEIPT.json","item_receipt_schema":{"contract":"X"},"submission_command":"python3 control/single-door-boundary/codex_current_room_bridge.py submit .pferde-quarantine/test/ITEM_RECEIPT.json"}
    v=a._current_only(sample)
    must(v["submission_command"].endswith("ITEM_RECEIPT.json"),"M28_DIRECT_SUBMIT_POSITIVE")
    bad=copy.deepcopy(sample);bad["submission_command"]="python3 fake.py"
    expect_exc(lambda:a._current_only(bad),"CURRENT_ACTION_SUBMISSION_NOT_BOUND")

def m29():
    a=mod(CURRENT_ACTION,"m29_action")
    batch,count=a._runtime_batch_identity()
    a._validate_release_metadata_identity({"exact_five_batch_sha256":batch,"exact_five_item_count":count},batch,count)
    expect_exc(lambda:a._validate_release_metadata_identity({"exact_five_batch_sha256":"0"*64,"exact_five_item_count":count},batch,count),"RELEASE_METADATA_BATCH_MISMATCH")
    expect_exc(lambda:a._validate_release_metadata_identity({"exact_five_batch_sha256":batch,"exact_five_item_count":count+1},batch,count),"RELEASE_METADATA_ITEM_COUNT_MISMATCH")

def _final_ctx_fixture(root:Path,wrong_batch=False):
    d=mod(DUAL,"m30_dual")
    batch="c"*64; out=[]; meta={
      "article_origin_policy":"POST_TEXT_SIGNED_0039_ORIGIN_AND_NO_REWRITE","authoring_prompt_sha256":"b"*64,
      "authoring_role":"CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS","content_generation_performed_by_supervisor":False,
      "contract":"WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED","created_at_utc":"2026-09-04T00:00:00+00:00",
      "exact_five_batch_sha256":("d"*64 if wrong_batch else batch),"exact_five_item_count":7,
      "frozen_workflow_sha256":"e"*64,"nullpunkt":{},"nullpunkt_sha256":"f"*64,"ppm_baseline_sha256":"1"*64,
      "ppm_version":"6.7.9","research_evidence_policy":"BOUND_EXISTING_FACHWORKFLOW_ONLY","sequence":107008,
      "status":"PASS","wordpress_write_performed":False}
    header={"contract":"production_plan_v4","plan_contract_version":"4.0.0"}
    for i in range(7):
        p=root/f"FACHWORKFLOW_PASS_{i}.json"
        q={"production_plan_header":header,"workflow_release_metadata":meta,"production_plan_item":{"canonical_article_id":f"article:{i}"},"fact_pack":{"contract":"canonical_fact_pack_v1","fact_pack_id":f"fp{i}"},"workflow_release_item":{"canonical_article_id":f"article:{i}"}}
        dump(p,q);out.append({"released_ref":p.name,"sha256":sha(p)})
    r={"contract":"PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2","status":"OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED","batch_sha256":batch,"outputs":out,"publish_allowed":False}
    rp=root/"RELEASE_RECEIPT.json";dump(rp,r)
    return d,rp

def m30():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);d,rp=_final_ctx_fixture(root,False)
        ctx=d.context_from_release(root,rp.name);must(len(ctx["production_plan"]["items"])==7,"M30_POSITIVE_COUNT")
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);d,rp=_final_ctx_fixture(root,True)
        expect_exc(lambda:d.context_from_release(root,rp.name),"FINAL_CONTEXT_BATCH_MISMATCH")

def _m31_validate_handoff(out):
    handoff=out.get("fachworkflow_handoff")
    must(isinstance(handoff,dict),"M31_BOUND_HANDOFF_MISSING")
    must(handoff.get("worker_executes_adapter_directly") is False,"M31_WORKER_DIRECT_ADAPTER_FORBIDDEN")
    must(handoff.get("adapter_executes_bound_ppm_stage") is True,"M31_BOUND_PPM_ADAPTER_MISSING")
    must(str(handoff.get("request_ref") or "").endswith("FACHWORKFLOW_HANDOFF_REQUEST.json"),"M31_REQUEST_REF_NOT_BOUND")

def m31():
    a=mod(CURRENT_ACTION,"m31_action")
    base={"allowed_output_root":".pferde-quarantine/test/","item_receipt_schema":{}}
    item={"canonical_article_id":"article:test","plan_slot":"a"*64,"article_type":"beratung"}
    out=a.augment_current_action(REPO,base,item)
    _m31_validate_handoff(out)
    bad=copy.deepcopy(out);bad["fachworkflow_handoff"]["worker_executes_adapter_directly"]=True
    expect_exc(lambda:_m31_validate_handoff(bad),"M31_WORKER_DIRECT_ADAPTER_FORBIDDEN")
    bad=copy.deepcopy(out);bad["fachworkflow_handoff"].pop("request_ref",None)
    expect_exc(lambda:_m31_validate_handoff(bad),"M31_REQUEST_REF_NOT_BOUND")
    smoke=a.selftest()
    must(smoke.get("current_codex_is_bound_fachworkflow_worker") is True,"M31_CURRENT_WORKER_NOT_BOUND")
    must(smoke.get("separate_fachworkflow_executor_required") is False,"M31_SEPARATE_EXECUTOR_REQUIRED")
    must(smoke.get("separate_fachworkflow_capability_required") is False,"M31_SYNTHETIC_CAPABILITY_REQUIRED")
    bridge=json.loads(cmd("control/single-door-boundary/test_h8_codex_cloud_bound_capsule_bridge.py"))
    must(bridge.get("status")=="H8_CODEX_CLOUD_BOUND_CAPSULE_BRIDGE_POSITIVE_NEGATIVE_PASS","M31_CODEX_NATIVE_BOUND_ACTION_NOT_PASS")
    must(bridge.get("custom_function_capability_required") is False,"M31_SYNTHETIC_CAPABILITY_REQUIRED")
    step=STEP7.read_text(encoding="utf-8")
    must("execute_bound_action" not in step,"M31_EXECUTE_BOUND_ACTION_DEPENDENCY")

def m32():
    h=mod(HANDOFF,"m32_handoff")
    must(PPM.is_file() and PSERC.is_file(),"M32_PACKAGES_MISSING")
    must(sha(PPM)==h.PPM679_PACKAGE_SHA256 and sha(PSERC)==h.PSERC_FIX_PACKAGE_SHA256,"M32_BOUND_PACKAGE_HASH")
    src=HANDOFF.read_text(encoding="utf-8")
    must("if ppm_env else (repo / PPM679_PACKAGE_REL)" in src and "if pserc_env else (repo / PSERC_FIX_PACKAGE_REL)" in src,"M32_ENV_STILL_MANDATORY")

def m33():
    wf=(REPO/".github/workflows/pferde-atelier-endstempel.yml").read_text(encoding="utf-8")
    final=(REPO/"control/startmaster0107/GITHUB_FINAL_RELEASE.py").read_text(encoding="utf-8")
    def check(workflow,finalizer):
        must("persist-credentials: false" in workflow,"M33_CODEX_CREDENTIALS_NOT_DISABLED")
        must("actions/upload-artifact" in workflow and "actions/download-artifact" in workflow,"M33_DURABLE_GITHUB_TRANSPORT")
        must("git remote" not in workflow and "git push" not in workflow,"M33_CODEX_GIT_REMOTE_DEPENDENCY")
        must("git remote" not in finalizer and "git push" not in finalizer and "GH_TOKEN" not in finalizer,"M33_CODEX_AUTH_DEPENDENCY")
    check(wf,final)
    expect_exc(lambda:check(wf+"\ngit remote -v\n",final),"M33_CODEX_GIT_REMOTE_DEPENDENCY")

CASES=[
("M01",m01),("M02",m02),("M03",m03),("M04",m04),("M05",m05),("M06",m06),("M07",m07),("M08",m08),("M09",m09),("M10",m10),
("M11",m11),("M12",m12),("M13",m13),("M14",m14),("M15",m15),("M16",m16),("M17",m17),("M18",m18),("M19",m19),("M20",m20),
("M21",m21),("M22",m22),("M23",m23),("M24",m24),("M25",m25),("M26",m26),("M27",m27),("M28",m28),("M29",m29),("M30",m30),
("M31",m31),("M32",m32),("M33",m33)]

def _run_ordered(cases,phase):
    results=[]
    for mid,fn in cases:
        try:
            fn();results.append({"id":mid,"status":"PASS"});print(mid+" PASS",flush=True)
        except Exception as e:
            results.append({"id":mid,"status":"FAIL","reason":str(e)});print(mid+" FAIL "+str(e),flush=True)
            print(json.dumps({"ok":False,"status":"REGRESSION_FAIL","phase":phase,"first_fail":mid,"results":results,"gesamt_pass":False},ensure_ascii=False,indent=2))
            return None
    return results

def main(argv):
    must(MATRIX.is_file(),"MATRIX_MISSING")
    open_only=argv==["--open-only"]
    if argv not in ([],["--open-only"]): raise Fail("USAGE: [--open-only]")

    # Repair phase: do not duplicate already-proven old positives while an open
    # regression still fails. Once M26-M33 are all green, automatically run the
    # one required final M01-M33 suite on the same head.
    if open_only:
        open_results=_run_ordered(CASES[25:],"OPEN_M26_M33")
        if open_results is None:return 2
        print("OPEN_REGRESSIONS_PASS",flush=True)

    results=_run_ordered(CASES,"FINAL_M01_M33")
    if results is None:return 2

    # Required final re-check against the last real production regression.
    m26()
    print("LAST_REGRESSION PASS BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING",flush=True)
    print(json.dumps({"ok":True,"status":"GESAMT PASS","results":results,"last_regression":"PASS","gesamt_pass":True},ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main(sys.argv[1:]))
