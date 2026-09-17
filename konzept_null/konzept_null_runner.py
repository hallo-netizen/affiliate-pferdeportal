#!/usr/bin/env python3
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
POLICY = ROOT / "ISOLATION_POLICY.json"
STATE = ROOT / "CURRENT_STATE.json"
START = ROOT / "PFERDE_ATELIER_START_HERE.json"
EXPECTED_BRANCH = "hobbyroom/konzept-null-startmaster0102-isolated"
EXPECTED_HISTORICAL = "be89fa13c170700e9753666d1d52bfbd8b28d810"
EXPECTED_BATCH = "7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a"
EXPECTED_COUNT = 7
REQUIRED_FIELDS = ["title", "target_keyword", "category", "article_type", "plan_slot"]
STAGES = ["METADATA","RESEARCH","FACT_PACK","TEXTMASCHINE","LANGUAGETOOL_6_8","PPM_6_7_9","LOCAL_TEST_PACKAGE"]

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
    for p in (POLICY, STATE, START):
        if not p.is_file():
            die(f"MISSING_{p.name}")
    policy, state, start = load(POLICY), load(STATE), load(START)
    if policy.get("branch") != EXPECTED_BRANCH:
        die("POLICY_BRANCH_MISMATCH")
    if policy.get("historical_commit") != EXPECTED_HISTORICAL:
        die("HISTORICAL_BINDING_MISMATCH")
    forbidden = ["allow_main_write","allow_pull_request","allow_merge","allow_deploy","allow_wordpress_access","allow_wordpress_write","allow_publish","allow_external_write","allow_production_state_mutation","allow_startmaster0107_mutation","allow_current_startmaster_mutation"]
    if any(policy.get(k) is not False for k in forbidden):
        die("ISOLATION_POLICY_OPEN")
    if state.get("terminal_boundary") != "BEFORE_WORDPRESS":
        die("BAD_TERMINAL_BOUNDARY")
    if state.get("workflow") != STAGES:
        die("WORKFLOW_DRIFT")
    if state.get("article_count") != EXPECTED_COUNT:
        die("ARTICLE_COUNT_DRIFT")
    if state.get("batch_sha256") != EXPECTED_BATCH:
        die("BATCH_BINDING_DRIFT")
    if start.get("scope") != "ISOLATED_TEST_ONLY":
        die("SCOPE_DRIFT")
    if start.get("article_count") != EXPECTED_COUNT or start.get("batch_sha256") != EXPECTED_BATCH:
        die("ROOT_BATCH_DRIFT")
    return policy, state, start

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

def cmd_preflight():
    guard()
    print("KONZEPT_NULL_PREFLIGHT_PASS")

def cmd_init(src):
    guard()
    obj = json.loads(Path(src).read_text(encoding="utf-8"))
    items = normalize_items(obj)
    if len(items) != EXPECTED_COUNT:
        die("EXACTLY_SEVEN_ARTICLES_REQUIRED")
    seen_slots = set()
    for i, item in enumerate(items, 1):
        for k in REQUIRED_FIELDS:
            if not isinstance(item.get(k), str) or not item[k].strip():
                die(f"ARTICLE_{i}_MISSING_FIELD_{k}")
        if item["plan_slot"] in seen_slots:
            die("DUPLICATE_PLAN_SLOT")
        seen_slots.add(item["plan_slot"])
    supplied_batch = obj.get("batch_sha256") if isinstance(obj, dict) else None
    if supplied_batch and supplied_batch != EXPECTED_BATCH:
        die("INPUT_BATCH_SHA_MISMATCH")
    rid = hashlib.sha256(canonical(items)).hexdigest()[:20]
    wd = safe_workdir(rid)
    (wd/"metadata_7.json").write_bytes(canonical(items))
    rs = {
        "contract":"KONZEPT_NULL_BATCH_RUN_STATE_V2",
        "run_id":rid,
        "historical_startmaster":"STARTMASTER0102",
        "historical_commit":EXPECTED_HISTORICAL,
        "batch_sha256":EXPECTED_BATCH,
        "article_count":EXPECTED_COUNT,
        "current_stage":"METADATA",
        "completed":["METADATA"],
        "publish_allowed":False,
        "wordpress_access_allowed":False,
        "external_write_allowed":False,
        "items":items
    }
    (wd/"RUN_STATE.json").write_bytes(canonical(rs))
    print(str(wd/"RUN_STATE.json"))

def cmd_stage(run_state_path, stage, artifact_path):
    guard()
    rs_path = Path(run_state_path).resolve()
    if ROOT.resolve() not in rs_path.parents:
        die("STATE_OUTSIDE_KONZEPT_NULL")
    rs = load(rs_path)
    if rs.get("article_count") != EXPECTED_COUNT or rs.get("batch_sha256") != EXPECTED_BATCH:
        die("RUN_BINDING_DRIFT")
    if stage not in STAGES:
        die("UNKNOWN_STAGE")
    expected_index = len(rs.get("completed", []))
    if expected_index >= len(STAGES) or STAGES[expected_index] != stage:
        die("STAGE_ORDER_VIOLATION")
    art = Path(artifact_path)
    if not art.is_file():
        die("ARTIFACT_MISSING")
    data = art.read_bytes()
    dest = rs_path.parent / f"{stage}.artifact"
    dest.write_bytes(data)
    rs["completed"].append(stage)
    rs["current_stage"] = stage
    rs.setdefault("artifact_sha256", {})[stage] = hashlib.sha256(data).hexdigest()
    rs_path.write_bytes(canonical(rs))
    print(f"KONZEPT_NULL_STAGE_PASS:{stage}")

def cmd_finalize(run_state_path):
    guard()
    rs_path = Path(run_state_path).resolve()
    rs = load(rs_path)
    if rs.get("completed") != STAGES:
        die("INCOMPLETE_WORKFLOW")
    if rs.get("article_count") != EXPECTED_COUNT or len(rs.get("items", [])) != EXPECTED_COUNT:
        die("INCOMPLETE_BATCH")
    if rs.get("publish_allowed") or rs.get("wordpress_access_allowed") or rs.get("external_write_allowed"):
        die("BOUNDARY_BREACH")
    package = {
        "contract":"KONZEPT_NULL_7_ARTIKEL_LOCAL_TEST_PACKAGE_V1",
        "historical_startmaster":"STARTMASTER0102",
        "historical_commit":EXPECTED_HISTORICAL,
        "batch_sha256":EXPECTED_BATCH,
        "article_count":EXPECTED_COUNT,
        "production_authority":False,
        "publish_allowed":False,
        "wordpress_access_allowed":False,
        "external_write_allowed":False,
        "items":rs["items"],
        "artifact_sha256":rs.get("artifact_sha256",{})
    }
    out = rs_path.parent/"KONZEPT_NULL_7_ARTIKEL_LOCAL_TEST_PACKAGE.json"
    out.write_bytes(canonical(package))
    print(str(out))

def main(argv):
    if len(argv) < 2:
        die("USAGE")
    c = argv[1]
    if c == "preflight" and len(argv) == 2:
        cmd_preflight()
    elif c == "init" and len(argv) == 3:
        cmd_init(argv[2])
    elif c == "stage" and len(argv) == 5:
        cmd_stage(argv[2], argv[3], argv[4])
    elif c == "finalize" and len(argv) == 3:
        cmd_finalize(argv[2])
    else:
        die("USAGE")

if __name__ == "__main__":
    main(sys.argv)
