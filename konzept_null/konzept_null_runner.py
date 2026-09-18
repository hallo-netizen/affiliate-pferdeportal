#!/usr/bin/env python3
import hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
POLICY = ROOT / "ISOLATION_POLICY.json"
STATE = ROOT / "CURRENT_STATE.json"
START = ROOT / "PFERDE_ATELIER_START_HERE.json"
NAV = ROOT / "CHAT_NAVIGATION_CONTRACT.json"
EXPECTED_BRANCH = "hobbyroom/konzept-null-startmaster0102-isolated"
EXPECTED_HISTORICAL = "be89fa13c170700e9753666d1d52bfbd8b28d810"
REQUIRED_FIELDS = ["title", "target_keyword", "category", "article_type", "plan_slot"]

STAGES = [
    "METADATA",
    "SOURCE_ORDER",
    "RESEARCH",
    "SOURCE_SNAPSHOT",
    "FACT_PACK",
    "CLAIM_BINDING",
    "CANONICAL_ARTICLE",
    "PRODUCTION_PLAN_V4",
    "LANGUAGETOOL_6_8",
    "PPM_6_7_9",
    "LOCAL_TEST_PACKAGE",
]
NEXT = {
    "METADATA": "CREATE_SOURCE_ORDER",
    "SOURCE_ORDER": "PERFORM_BOUND_RESEARCH",
    "RESEARCH": "CREATE_SOURCE_SNAPSHOT",
    "SOURCE_SNAPSHOT": "CREATE_FACT_PACK",
    "FACT_PACK": "BIND_CLAIMS_TO_SOURCES",
    "CLAIM_BINDING": "CREATE_CANONICAL_ARTICLE",
    "CANONICAL_ARTICLE": "CREATE_PRODUCTION_PLAN_V4",
    "PRODUCTION_PLAN_V4": "RUN_LANGUAGETOOL_6_8",
    "LANGUAGETOOL_6_8": "RUN_PPM_6_7_9",
    "PPM_6_7_9": "BUILD_LOCAL_TEST_PACKAGE",
    "LOCAL_TEST_PACKAGE": "COMPLETE_BEFORE_WORDPRESS",
}

def die(msg):
    print(f"KONZEPT_NULL_BLOCKED:{msg}", file=sys.stderr)
    raise SystemExit(2)

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def branch_name():
    try:
        return subprocess.check_output(["git","rev-parse","--abbrev-ref","HEAD"], cwd=REPO, text=True).strip()
    except Exception:
        die("GIT_BRANCH_UNAVAILABLE")

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode("utf-8")

def guard():
    if branch_name() != EXPECTED_BRANCH:
        die("WRONG_BRANCH")
    for p in (POLICY, STATE, START, NAV):
        if not p.is_file():
            die(f"MISSING_{p.name}")
    policy, state, start, nav = load(POLICY), load(STATE), load(START), load(NAV)
    if policy.get("branch") != EXPECTED_BRANCH:
        die("POLICY_BRANCH_MISMATCH")
    if policy.get("historical_commit") != EXPECTED_HISTORICAL:
        die("HISTORICAL_BINDING_MISMATCH")
    forbidden = [
        "allow_main_write","allow_pull_request","allow_merge","allow_deploy",
        "allow_wordpress_access","allow_wordpress_write","allow_publish",
        "allow_external_write","allow_production_state_mutation",
        "allow_startmaster0107_mutation","allow_current_startmaster_mutation"
    ]
    if any(policy.get(k) is not False for k in forbidden):
        die("ISOLATION_POLICY_OPEN")
    if state.get("terminal_boundary") != "BEFORE_WORDPRESS":
        die("BAD_TERMINAL_BOUNDARY")
    if state.get("workflow") != STAGES:
        die("WORKFLOW_DRIFT")
    if nav.get("stage_order") != STAGES or nav.get("next_step_map") != NEXT:
        die("NAVIGATION_CONTRACT_DRIFT")
    if nav.get("navigation_source") != "NEXT_ALLOWED_STEP_ONLY":
        die("NAVIGATION_SOURCE_DRIFT")
    if nav.get("free_workflow_decisions") is not False:
        die("FREE_WORKFLOW_DECISION_OPEN")
    if state.get("batch_mode") != "VARIABLE_1_TO_N" or state.get("minimum_article_count") != 1:
        die("BATCH_MODE_DRIFT")
    if start.get("scope") != "ISOLATED_TEST_ONLY":
        die("SCOPE_DRIFT")
    if start.get("batch_mode") != "VARIABLE_1_TO_N":
        die("ROOT_BATCH_MODE_DRIFT")
    if start.get("next_allowed_step") != state.get("next_allowed_step"):
        die("ROOT_STATE_NEXT_STEP_MISMATCH")
    return policy, state, start, nav

def safe_workdir(run_id):
    p = (ROOT / "work" / run_id).resolve()
    allowed = (ROOT / "work").resolve()
    if allowed not in p.parents:
        die("OUTPUT_ESCAPE")
    p.mkdir(parents=True, exist_ok=True)
    return p

def normalize_items(obj):
    if isinstance(obj, dict) and isinstance(obj.get("items"), list):
        return obj["items"]
    if isinstance(obj, dict) and isinstance(obj.get("metadata_handoff", {}).get("items"), list):
        return obj["metadata_handoff"]["items"]
    if isinstance(obj, list):
        return obj
    die("INPUT_SHAPE_UNSUPPORTED")

def validate_metadata_items(items):
    if len(items) < 1:
        die("AT_LEAST_ONE_ARTICLE_REQUIRED")
    seen_slots=set()
    for i,item in enumerate(items,1):
        for k in REQUIRED_FIELDS:
            if not isinstance(item.get(k),str) or not item[k].strip():
                die(f"ARTICLE_{i}_MISSING_FIELD_{k}")
        if item["plan_slot"] in seen_slots:
            die("DUPLICATE_PLAN_SLOT")
        seen_slots.add(item["plan_slot"])

def expected_next_from_completed(completed):
    if not completed:
        return "LOAD_METADATA_BATCH_READ_ONLY"
    if completed[-1] not in NEXT:
        die("UNKNOWN_COMPLETED_STAGE")
    return NEXT[completed[-1]]

def validate_run_state(rs):
    if rs.get("contract") != "KONZEPT_NULL_BATCH_RUN_STATE_V4":
        die("RUN_STATE_CONTRACT_MISMATCH")
    if rs.get("historical_startmaster") != "STARTMASTER0102" or rs.get("historical_commit") != EXPECTED_HISTORICAL:
        die("RUN_HISTORICAL_BINDING_MISMATCH")
    if not isinstance(rs.get("article_count"), int) or rs["article_count"] < 1:
        die("RUN_BATCH_INVALID")
    if len(rs.get("items",[])) != rs["article_count"]:
        die("RUN_BATCH_COUNT_DRIFT")
    validate_metadata_items(rs["items"])
    completed=rs.get("completed")
    if not isinstance(completed,list) or not completed:
        die("RUN_COMPLETED_INVALID")
    if completed != STAGES[:len(completed)]:
        die("STAGE_ORDER_VIOLATION")
    expected=expected_next_from_completed(completed)
    if rs.get("next_allowed_step") != expected:
        die("RUN_NEXT_ALLOWED_STEP_DRIFT")
    if rs.get("publish_allowed") or rs.get("wordpress_access_allowed") or rs.get("external_write_allowed"):
        die("BOUNDARY_BREACH")
    return completed, expected

def cmd_preflight():
    guard()
    print("KONZEPT_NULL_PREFLIGHT_PASS")

def cmd_root():
    _,state,start,_=guard()
    print(json.dumps({
        "contract":"KONZEPT_NULL_ROOT_NAVIGATION_V1",
        "root":"konzept_null/PFERDE_ATELIER_START_HERE.json",
        "state":"konzept_null/CURRENT_STATE.json",
        "next_allowed_step":state["next_allowed_step"],
        "free_workflow_decisions":False,
        "publish_allowed":False,
        "wordpress_access_allowed":False
    },ensure_ascii=False,indent=2))

def cmd_init(src):
    guard()
    obj=json.loads(Path(src).read_text(encoding="utf-8"))
    items=normalize_items(obj)
    validate_metadata_items(items)
    calculated_input_sha=hashlib.sha256(canonical(items)).hexdigest()
    supplied_batch=obj.get("batch_sha256") if isinstance(obj,dict) else None
    if supplied_batch is not None and (not isinstance(supplied_batch,str) or not re.fullmatch(r"[0-9a-fA-F]{64}",supplied_batch)):
        die("INVALID_SUPPLIED_BATCH_SHA256")
    run_binding_sha=supplied_batch.lower() if supplied_batch else calculated_input_sha
    rid=calculated_input_sha[:20]
    wd=safe_workdir(rid)
    (wd/"metadata_batch.json").write_bytes(canonical(items))
    rs={
        "contract":"KONZEPT_NULL_BATCH_RUN_STATE_V4",
        "run_id":rid,
        "historical_startmaster":"STARTMASTER0102",
        "historical_commit":EXPECTED_HISTORICAL,
        "input_binding_sha256":run_binding_sha,
        "calculated_metadata_sha256":calculated_input_sha,
        "article_count":len(items),
        "current_stage":"METADATA",
        "completed":["METADATA"],
        "next_allowed_step":NEXT["METADATA"],
        "publish_allowed":False,
        "wordpress_access_allowed":False,
        "external_write_allowed":False,
        "items":items
    }
    (wd/"RUN_STATE.json").write_bytes(canonical(rs))
    print(str(wd/"RUN_STATE.json"))

def cmd_next(run_state_path):
    guard()
    rs_path=Path(run_state_path).resolve()
    if ROOT.resolve() not in rs_path.parents:
        die("STATE_OUTSIDE_KONZEPT_NULL")
    rs=load(rs_path)
    _,expected=validate_run_state(rs)
    print(json.dumps({
        "contract":"KONZEPT_NULL_NEXT_ALLOWED_STEP_V1",
        "run_id":rs["run_id"],
        "current_stage":rs["completed"][-1],
        "next_allowed_step":expected,
        "no_other_step_allowed":True
    },ensure_ascii=False,indent=2))

def cmd_stage(run_state_path, stage, artifact_path):
    guard()
    rs_path=Path(run_state_path).resolve()
    if ROOT.resolve() not in rs_path.parents:
        die("STATE_OUTSIDE_KONZEPT_NULL")
    rs=load(rs_path)
    completed,expected_action=validate_run_state(rs)
    expected_index=len(completed)
    if expected_index >= len(STAGES):
        die("WORKFLOW_ALREADY_COMPLETE")
    expected_stage=STAGES[expected_index]
    if stage != expected_stage:
        die(f"STAGE_ORDER_VIOLATION_EXPECTED_{expected_stage}")
    if expected_action != NEXT[completed[-1]]:
        die("NEXT_ALLOWED_STEP_MISMATCH")
    art=Path(artifact_path)
    if not art.is_file():
        die("ARTIFACT_MISSING")
    data=art.read_bytes()
    if not data:
        die("ARTIFACT_EMPTY")
    dest=rs_path.parent/f"{stage}.artifact"
    dest.write_bytes(data)
    rs["completed"].append(stage)
    rs["current_stage"]=stage
    rs.setdefault("artifact_sha256",{})[stage]=hashlib.sha256(data).hexdigest()
    rs["next_allowed_step"]=NEXT[stage]
    rs_path.write_bytes(canonical(rs))
    print(f"KONZEPT_NULL_STAGE_PASS:{stage}:NEXT={rs['next_allowed_step']}")

def cmd_finalize(run_state_path):
    guard()
    rs_path=Path(run_state_path).resolve()
    if ROOT.resolve() not in rs_path.parents:
        die("STATE_OUTSIDE_KONZEPT_NULL")
    rs=load(rs_path)
    completed,expected=validate_run_state(rs)
    if completed != STAGES:
        die("INCOMPLETE_WORKFLOW")
    if expected != "COMPLETE_BEFORE_WORDPRESS":
        die("TERMINAL_NEXT_STEP_MISMATCH")
    package={
        "contract":"KONZEPT_NULL_LOCAL_TEST_PACKAGE_V3",
        "historical_startmaster":"STARTMASTER0102",
        "historical_commit":EXPECTED_HISTORICAL,
        "input_binding_sha256":rs["input_binding_sha256"],
        "calculated_metadata_sha256":rs["calculated_metadata_sha256"],
        "article_count":rs["article_count"],
        "production_authority":False,
        "publish_allowed":False,
        "wordpress_access_allowed":False,
        "external_write_allowed":False,
        "terminal_boundary":"BEFORE_WORDPRESS",
        "completed":STAGES,
        "next_allowed_step":"COMPLETE_BEFORE_WORDPRESS",
        "items":rs["items"],
        "artifact_sha256":rs.get("artifact_sha256",{})
    }
    out=rs_path.parent/"KONZEPT_NULL_LOCAL_TEST_PACKAGE.json"
    out.write_bytes(canonical(package))
    print(str(out))

def main(argv):
    if len(argv)<2:
        die("USAGE")
    c=argv[1]
    if c=="preflight" and len(argv)==2:
        cmd_preflight()
    elif c=="root" and len(argv)==2:
        cmd_root()
    elif c=="init" and len(argv)==3:
        cmd_init(argv[2])
    elif c=="next" and len(argv)==3:
        cmd_next(argv[2])
    elif c=="stage" and len(argv)==5:
        cmd_stage(argv[2],argv[3],argv[4])
    elif c=="finalize" and len(argv)==3:
        cmd_finalize(argv[2])
    else:
        die("USAGE")

if __name__=="__main__":
    main(sys.argv)
