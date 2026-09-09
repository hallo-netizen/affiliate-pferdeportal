#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BASE_COMMIT = "679947a3c12b40a5615c4e75e32ffaf551c27f83"
BOUND_BRANCH = "endstempel-build-capsule-20260902"
CURRENT_REGRESSION_BATCH = "7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a"
FINAL_FILENAME = "GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json"

CAPSULE = {
    "contract": "PFERDE_ATELIER_ENDSTEMPEL_BUILD_CAPSULE_V1",
    "authority": "EXECUTE_ONLY_THIS_CAPSULE_NO_FREE_NAVIGATION",
    "purpose": "Build only the immutable post-107008 end-stamp and WordPress pre-import verification boundary.",
    "bound_branch": BOUND_BRANCH,
    "base_commit": BASE_COMMIT,
    "target": {
        "flow": "VALID_107008_PASS -> FREEZE_EXACT_RELEASED_ARTICLE_BYTES -> HASH_MANIFEST -> END_SIGNATURE -> FINAL_JSON -> WORDPRESS_VERIFY_BEFORE_ANY_WRITE",
        "batch_policy": "READ_FROM_VALID_107008_RECEIPT_NOT_HARDCODED",
        "current_regression_batch_only": CURRENT_REGRESSION_BATCH,
        "final_filename": FINAL_FILENAME,
        "package_contract": "PSERC_APPROVED_PRODUCTION_PACKAGE_V1",
        "article_mutation_allowed": False,
        "fachworkflow_change_allowed": False,
        "workflow_route_change_allowed": False,
        "workflow_state_change_allowed": False,
        "publish_allowed": False,
    },
    "security_model": {
        "factory_rule": "Only the exact bytes released by valid 107008 may be stamped.",
        "stamp_rule": "The signed manifest must bind batch id, 107008 receipt hash, exact file set, exact byte count and SHA-256 of every article.",
        "private_key_rule": "Private signing key must be non-exportable and must never be stored in repository, FINAL.json or WordPress.",
        "wordpress_rule": "WordPress stores only trusted public verification key material and verifies before the first content write.",
        "fail_closed": True,
        "all_or_nothing_import": True,
        "replay_rule": "A successfully imported batch id may not be imported a second time.",
    },
    "hard_limits": {
        "free_repo_search_allowed": False,
        "signer_discovery_allowed": False,
        "alternate_signing_routes_allowed": 0,
        "queues_allowed": False,
        "mailboxes_allowed": False,
        "database_architecture_allowed": False,
        "new_workflow_rooms_allowed": False,
        "new_startmaster_allowed": False,
        "article_rewrite_allowed": False,
        "article_repackaging_that_changes_bytes_allowed": False,
        "quality_rule_change_allowed": False,
        "seo_rule_change_allowed": False,
        "design_rule_change_allowed": False,
        "publish_allowed": False,
        "repeat_passed_gate_allowed": False,
        "existing_core_files_modified_max": 1,
        "new_runtime_files_max": 1,
        "new_test_files_max": 1,
        "new_wordpress_verifier_files_max": 1,
    },
    "allowed_change_files": [
        "control/startmaster0107/ENDSTEMPEL_BUILD_CAPSULE_V1.py",
        "control/startmaster0107/ENDSTEMPEL_FINALIZER.py",
        "control/startmaster0107/ENDSTEMPEL_TEST.py",
        "control/startmaster0107/ENDSTEMPEL_WORDPRESS_VERIFY.php",
        "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py",
    ],
    "protected_files": [
        "control/CURRENT_STARTMASTER.json",
        "control/startmaster0107/PFERDE_ATELIER_START_HERE.json",
        "control/startmaster0107/CURRENT_STATE.json",
        "control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json",
        "control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json",
        "control/startmaster0107/VERBINDLICHER_TEXTERSTELLUNGS_PROMPT_STARTMASTER0107.txt",
        "control/single-door-boundary/single_door_boundary.py",
        "control/single-door-boundary/single_door_route_binding.py",
        "control/output-quarantine/runtime_entry_gate.py",
    ],
    "protected_prefixes": [
        "control/startmaster0107/recovery_sources/",
        ".pferde-release-staging/",
    ],
    "build_gates": [
        {
            "id": 1,
            "name": "ORIGINAL_FREEZE",
            "instruction": "Use only a valid 107008 output-release receipt. Resolve the exact released article files from that receipt, read their bytes without rewriting them, and build one deterministic manifest containing exact file set, byte length and SHA-256 for every article plus batch id and receipt SHA-256.",
            "pass": [
                "107008 receipt contract/status/batch are valid",
                "article set comes only from released 107008 outputs",
                "article bytes before and after manifest creation are identical",
                "missing or additional article is rejected",
                "no content write operation occurs",
            ],
        },
        {
            "id": 2,
            "name": "END_STAMP",
            "instruction": "Sign only the canonical Gate-1 manifest hash. The private key must remain non-exportable/outside repository and WordPress. Verify the returned signature immediately with the bound public key before FINAL.json is accepted.",
            "pass": [
                "signature binds the complete immutable article manifest",
                "changed manifest or changed article hash invalidates signature",
                "wrong key identity or wrong signature is fail-closed",
                "private key bytes are never emitted, logged or persisted",
                "publish remains false",
            ],
        },
        {
            "id": 3,
            "name": "WORDPRESS_PREIMPORT",
            "instruction": "Build one minimal WordPress verifier. Before the first WordPress content write it must verify trusted public key id, signature, batch id, exact file set, exact article SHA-256 values and replay status. Any mismatch rejects the whole batch before content mutation.",
            "pass": [
                "verification happens before first content write",
                "one bad article blocks the complete batch",
                "already imported batch blocks replay",
                "failed import leaves no partial article import",
                "WordPress contains no private signing key",
            ],
        },
        {
            "id": 4,
            "name": "END_TO_END",
            "instruction": "Run only the fixed positive/negative tests and then scope/protected checks. Do not repeat a passed gate.",
            "positive_tests": [
                "original valid 107008 batch -> stamp valid -> WordPress verifier PASS before write",
            ],
            "negative_tests": [
                "one changed character -> BLOCK",
                "wrong batch -> BLOCK",
                "one file missing -> BLOCK",
                "one additional file -> BLOCK",
                "wrong signature -> BLOCK",
                "already imported batch -> BLOCK",
                "simulated import failure -> zero committed article writes",
            ],
            "pass": [
                "all protected workflow files unchanged",
                "all protected article source bytes unchanged",
                "only allowed change files changed",
                "no publish",
            ],
        },
    ],
    "failure_rule": "Repair only the proven defect inside the current gate. No alternate route, no free search, no redesign, no extra test loop.",
    "completion_rule": "Only GATE_1_PASS + GATE_2_PASS + GATE_3_PASS + GATE_4_PASS equals ENDSTEMPEL_COMPLETE_PASS.",
}

ALLOWED = set(CAPSULE["allowed_change_files"])
PROTECTED = set(CAPSULE["protected_files"])
PROTECTED_PREFIXES = tuple(CAPSULE["protected_prefixes"])


def run_git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError("GIT_FAILED:" + " ".join(args) + ":" + p.stderr.strip()[:300])
    return p.stdout


def changed_files() -> list[str]:
    names = set()
    for spec in (("diff", "--name-only", BASE_COMMIT + "...HEAD"), ("diff", "--name-only"), ("diff", "--name-only", "--cached")):
        for row in run_git(*spec).splitlines():
            row = row.strip()
            if row:
                names.add(row)
    for row in run_git("status", "--porcelain").splitlines():
        if not row.strip():
            continue
        path = row[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path:
            names.add(path)
    return sorted(names)


def is_protected(path: str) -> bool:
    return path in PROTECTED or path.startswith(PROTECTED_PREFIXES)


def scope_check() -> dict:
    changed = changed_files()
    forbidden = [p for p in changed if p not in ALLOWED]
    protected_changed = [p for p in changed if is_protected(p)]
    existing_core_changed = [p for p in changed if p == "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py"]
    new_runtime = [p for p in changed if p == "control/startmaster0107/ENDSTEMPEL_FINALIZER.py"]
    new_test = [p for p in changed if p == "control/startmaster0107/ENDSTEMPEL_TEST.py"]
    new_wp = [p for p in changed if p == "control/startmaster0107/ENDSTEMPEL_WORDPRESS_VERIFY.php"]
    errors = []
    if forbidden:
        errors.append("FORBIDDEN_CHANGED_FILES")
    if protected_changed:
        errors.append("PROTECTED_FILES_CHANGED")
    if len(existing_core_changed) > CAPSULE["hard_limits"]["existing_core_files_modified_max"]:
        errors.append("CORE_CHANGE_LIMIT")
    if len(new_runtime) > CAPSULE["hard_limits"]["new_runtime_files_max"]:
        errors.append("RUNTIME_FILE_LIMIT")
    if len(new_test) > CAPSULE["hard_limits"]["new_test_files_max"]:
        errors.append("TEST_FILE_LIMIT")
    if len(new_wp) > CAPSULE["hard_limits"]["new_wordpress_verifier_files_max"]:
        errors.append("WORDPRESS_FILE_LIMIT")
    return {
        "ok": not errors,
        "status": "ENDSTEMPEL_SCOPE_PASS" if not errors else "ENDSTEMPEL_SCOPE_BLOCKED",
        "changed": changed,
        "forbidden": forbidden,
        "protected_changed": protected_changed,
        "errors": errors,
        "publish_allowed": False,
    }


def selftest() -> dict:
    required = {
        "contract": "PFERDE_ATELIER_ENDSTEMPEL_BUILD_CAPSULE_V1",
        "authority": "EXECUTE_ONLY_THIS_CAPSULE_NO_FREE_NAVIGATION",
    }
    for key, value in required.items():
        if CAPSULE.get(key) != value:
            raise RuntimeError("CAPSULE_BINDING_INVALID:" + key)
    if CAPSULE["target"]["article_mutation_allowed"] is not False:
        raise RuntimeError("ARTICLE_MUTATION_NOT_BLOCKED")
    if CAPSULE["target"]["fachworkflow_change_allowed"] is not False:
        raise RuntimeError("FACHWORKFLOW_CHANGE_NOT_BLOCKED")
    if CAPSULE["target"]["workflow_route_change_allowed"] is not False:
        raise RuntimeError("WORKFLOW_ROUTE_CHANGE_NOT_BLOCKED")
    if CAPSULE["target"]["publish_allowed"] is not False:
        raise RuntimeError("PUBLISH_NOT_BLOCKED")
    if CAPSULE["security_model"]["fail_closed"] is not True or CAPSULE["security_model"]["all_or_nothing_import"] is not True:
        raise RuntimeError("FAIL_CLOSED_OR_ATOMIC_IMPORT_MISSING")
    gates = CAPSULE.get("build_gates")
    if not isinstance(gates, list) or [g.get("id") for g in gates] != [1, 2, 3, 4]:
        raise RuntimeError("GATE_SEQUENCE_INVALID")
    scope = scope_check()
    if not scope["ok"]:
        return scope
    return {
        "ok": True,
        "status": "ENDSTEMPEL_CAPSULE_READY_PASS",
        "base_commit": BASE_COMMIT,
        "bound_branch": BOUND_BRANCH,
        "gate_count": 4,
        "free_navigation": False,
        "article_mutation_allowed": False,
        "workflow_change_allowed": False,
        "publish_allowed": False,
        "scope": scope,
    }


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    try:
        if cmd == "show":
            out = CAPSULE
        elif cmd == "scope":
            out = scope_check()
        elif cmd == "ready":
            out = selftest()
        else:
            raise RuntimeError("USE: ENDSTEMPEL_BUILD_CAPSULE_V1.py [show|scope|ready]")
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if out.get("ok", True) else 2
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "HARD_BLOCK", "reason": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
