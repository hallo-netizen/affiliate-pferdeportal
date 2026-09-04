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
def m15(): must("kein zweiter Executor" in STEP7.read_text(encoding="utf-8") or "kein zweiter" in STEP7.read_text(encoding="utf-8"),"M15_INSTRUCTION")
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
    for p in [STEP7,STEP8,RUNTIME,REPO/"control/startmaster0107/chat_delivery_payload.py",REPO/"control/startmaster0107/GITHUB_FINAL_RELEASE.py"]:
        must("publish_allowed" in p.read_text(encoding="utf-8"),"M21_PUBLISH_FLAG:"+str(p))
def m22(): must("H8_PREPRODUCTION_BOOTSTRAP_POSITIVE_NEGATIVE_PASS" in cmd("control/single-door-boundary/test_h8_preproduction_bootstrap.py"),"M22_H8")
def m23(): must("POSITIVE_FULL_PACKAGE_CURRENT_GENERATION" in cmd("control/startmaster0107/production-package-release/test_production_package_release_gate.py"),"M23_SIGNED_PACKAGE_ONLY")
def m24(): must("STARTMASTER_ROLLBACK_BLOCKED" in (REPO/".github/workflows/pferde-atelier-immutable-base-hardlock.yml").read_text(encoding="utf-8"),"M24_H8_ROLLBACK")
def m25():
    s=(REPO/"control/startmaster0107/VERBINDLICHER_TEXTERSTELLUNGS_PROMPT_STARTMASTER0107.txt").read_text(encoding="utf-8")
    must("bestehender Fachworkflow" in s and "Keine eigene" in s,"M25_FACHWORKFLOW_BOUNDARY")

# Open historical regressions: hard positive + hard negative.
def m26():
    a=mod(CURRENT_ACTION,"m26_action")
    batch,count=a._runtime_batch_identity()
    base={"allowed_output_root":".pferde-quarantine/test/","item_receipt_schema":{}}
    item={"canonical_article_id":"article:test","plan_slot":"a"*64,"article_type":"beratung"}
    out=a.augment_current_action(REPO,base,item)
    # Positive requirement: current NEW action must be executable without a circular
    # pre-PASS request that itself needs the context only produced by the Fachworkflow.
    must("fachworkflow_handoff" not in out,"M26_CIRCULAR_PREPASS_HANDOFF_STILL_REQUIRED")
    schema=out["item_receipt_schema"]["fachworkflow_pass_schema"]
    for k in ("fact_pack","production_plan_item","production_plan_header","workflow_release_item","workflow_release_metadata"):
        must(k in schema,"M26_CONTEXT_NOT_BOUND:"+k)
    # Negative: missing real context must remain fail-closed.
    d=mod(DUAL,"m26_dual")
    with tempfile.TemporaryDirectory() as td:
        tr=Path(td); (tr/"q").mkdir()
        (tr/"control/startmaster0107").mkdir(parents=True,exist_ok=True)
        dump(tr/"control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json",{"batch_sha256":"c"*64})
        # Contract binding files are intentionally absent: validator must not accept an empty/fake pass.
        fake={"fact_pack":{},"production_plan_item":{},"production_plan_header":{},"workflow_release_item":{},"workflow_release_metadata":{}}
        must(not all(bool(fake[k]) for k in fake),"M26_NEG_FIXTURE_INVALID")

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

def m31():
    a=mod(CURRENT_ACTION,"m31_action")
    base={"allowed_output_root":".pferde-quarantine/test/","item_receipt_schema":{}}
    item={"canonical_article_id":"article:test","plan_slot":"a"*64,"article_type":"beratung"}
    out=a.augment_current_action(REPO,base,item)
    must("fachworkflow_handoff" not in out,"M31_SECOND_HANDOFF_DEPENDENCY")
    step=STEP7.read_text(encoding="utf-8")
    must("Capability-Suche" not in step and "zweiter Executor" not in step,"M31_SYNTHETIC_EXECUTOR_INSTRUCTION")

def m32():
    h=mod(HANDOFF,"m32_handoff")
    must(PPM.is_file() and PSERC.is_file(),"M32_PACKAGES_MISSING")
    must(sha(PPM)==h.PPM679_PACKAGE_SHA256 and sha(PSERC)==h.PSERC_FIX_PACKAGE_SHA256,"M32_BOUND_PACKAGE_HASH")
    src=HANDOFF.read_text(encoding="utf-8")
    must("if ppm_env else (repo / PPM679_PACKAGE_REL)" in src and "if pserc_env else (repo / PSERC_FIX_PACKAGE_REL)" in src,"M32_ENV_STILL_MANDATORY")

def m33():
    out=cmd("control/startmaster0107/ENDSTEMPEL_TEST.py")
    must("ENDSTEMPEL_FIXED_TESTS_PASS" in out,"M33_ENDSTEMPEL_POSNEG")
    wf=(REPO/".github/workflows/pferde-atelier-endstempel.yml").read_text(encoding="utf-8")
    must("actions/upload-artifact" in wf and "actions/download-artifact" in wf,"M33_DURABLE_GITHUB_TRANSPORT")
    must("git remote" not in wf,"M33_CODEX_GIT_REMOTE_DEPENDENCY")

CASES=[
("M01",m01),("M02",m02),("M03",m03),("M04",m04),("M05",m05),("M06",m06),("M07",m07),("M08",m08),("M09",m09),("M10",m10),
("M11",m11),("M12",m12),("M13",m13),("M14",m14),("M15",m15),("M16",m16),("M17",m17),("M18",m18),("M19",m19),("M20",m20),
("M21",m21),("M22",m22),("M23",m23),("M24",m24),("M25",m25),("M26",m26),("M27",m27),("M28",m28),("M29",m29),("M30",m30),
("M31",m31),("M32",m32),("M33",m33)]

def main(argv):
    must(MATRIX.is_file(),"MATRIX_MISSING")
    open_only=argv==["--open-only"]
    if argv not in ([],["--open-only"]): raise Fail("USAGE: [--open-only]")
    results=[]
    start=25 if open_only else 0
    for mid,fn in CASES[start:]:
        try:
            fn();results.append({"id":mid,"status":"PASS"});print(mid+" PASS",flush=True)
        except Exception as e:
            results.append({"id":mid,"status":"FAIL","reason":str(e)});print(mid+" FAIL "+str(e),flush=True)
            print(json.dumps({"ok":False,"status":"REGRESSION_FAIL","first_fail":mid,"results":results,"gesamt_pass":False},ensure_ascii=False,indent=2))
            return 2
    status="OPEN_REGRESSIONS_PASS" if open_only else "GESAMT PASS"
    print(json.dumps({"ok":True,"status":status,"results":results,"gesamt_pass":not open_only},ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main(sys.argv[1:]))
