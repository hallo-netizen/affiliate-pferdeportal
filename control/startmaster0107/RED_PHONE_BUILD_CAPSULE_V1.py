#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

CAPSULE = {
    "contract": "PFERDE_ATELIER_RED_PHONE_BUILD_CAPSULE_V1",
    "purpose": "Build exactly one sustainable direct signer call after 107008 PASS without changing article/content/quality/workflow architecture.",
    "authority": "EXECUTE_ONLY_THIS_CAPSULE_NO_FREE_NAVIGATION",
    "target": {
        "flow": "107008_PASS -> SIGN(hash) -> verify returned signature with existing production public key -> existing finalizer -> GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json",
        "signing_key_policy": "KEEP_EXISTING_PRODUCTION_KEY_ID_AND_PUBLIC_KEY",
        "publish_allowed": False,
        "plugin_change_allowed": False,
        "article_change_allowed": False,
        "quality_rule_change_allowed": False,
        "workflow_state_change_allowed": False,
        "architecture_change_allowed": False,
    },
    "hard_limits": {
        "new_runtime_files_max": 1,
        "new_test_files_max": 1,
        "existing_core_files_modified_max": 1,
        "fallback_routes_allowed": 0,
        "signer_discovery_scans_allowed": 0,
        "queues_allowed": False,
        "mailboxes_allowed": False,
        "database_allowed": False,
        "new_service_allowed": False,
        "new_key_allowed": False,
        "key_rotation_allowed": False,
        "plugin_rebuild_allowed": False,
        "repeat_passed_gate_allowed": False,
    },
    "preferred_files": {
        "runtime": "control/startmaster0107/PSERC_RED_PHONE.py",
        "test": "control/startmaster0107/PSERC_RED_PHONE_TEST.py",
        "existing_finalizer": "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py",
    },
    "build_sections": [
        {
            "id": 1,
            "name": "DIRECT_LINE",
            "instruction": "Build only the direct one-call signer path. It may transmit only the approved signing request/hash and receive only the signature/result. The private key must never enter the worker/runtime. Use the already existing production key identity. No PATH scan, no signer auto-discovery, no alternate transport.",
            "pass": [
                "107008 PASS is mandatory before any signing request",
                "exactly one signing request is sent",
                "request is bound to the exact final payload hash",
                "returned signature is checked against the existing production public key",
                "no content, article, quality, workflow-state or publish mutation occurs",
            ],
        },
        {
            "id": 2,
            "name": "SAFETY",
            "instruction": "Test the direct line locally. Fix only defects in section 1; do not redesign.",
            "positive_tests": [
                "valid 107008 receipt + exact hash + valid production-format signature response -> PASS",
            ],
            "negative_tests": [
                "missing/invalid 107008 receipt -> FAIL CLOSED",
                "changed hash -> FAIL CLOSED",
                "wrong signature -> FAIL CLOSED",
                "wrong signing key identity -> FAIL CLOSED",
                "signer unreachable/timeout -> FAIL CLOSED",
                "second/fallback signer route attempted -> FAIL",
            ],
        },
        {
            "id": 3,
            "name": "END_TO_END",
            "instruction": "Run the real finalization path from the existing 107008-approved batch through the direct line to the exact FINAL.json. Then verify repository diff and publish=false.",
            "pass": [
                "exact target filename exists",
                "package contract is PSERC_APPROVED_PRODUCTION_PACKAGE_V1",
                "signature validates with existing production public key",
                "7 existing articles are preserved byte-identically",
                "publish_allowed=false",
                "no unauthorized repository files changed",
                "no already-passed workflow stage was repeated",
            ],
        },
    ],
    "failure_rule": "Stay inside the current section and repair only its proven cause. No alternate architecture, no extra search loop, no new route. After PASS continue automatically to the next section.",
    "completion_rule": "Only SECTION_1_PASS + SECTION_2_PASS + SECTION_3_PASS equals RED_PHONE_BUILD_COMPLETE_PASS.",
}

ALLOWED_CHANGE_PREFIXES = {
    "control/startmaster0107/PSERC_RED_PHONE.py",
    "control/startmaster0107/PSERC_RED_PHONE_TEST.py",
    "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py",
    "control/startmaster0107/RED_PHONE_BUILD_CAPSULE_V1.py",
}


def git_changed_files() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise SystemExit("CAPSULE_GIT_STATUS_FAILED")
    out = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        out.append(path)
    return out


def check_scope() -> None:
    changed = git_changed_files()
    forbidden = [p for p in changed if p not in ALLOWED_CHANGE_PREFIXES]
    if forbidden:
        print(json.dumps({"status": "CAPSULE_SCOPE_FAIL", "forbidden": forbidden}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    print(json.dumps({"status": "CAPSULE_SCOPE_PASS", "changed": changed}, ensure_ascii=False, indent=2))


def show() -> None:
    print(json.dumps(CAPSULE, ensure_ascii=False, indent=2))


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    if cmd == "show":
        show()
        return 0
    if cmd == "scope":
        check_scope()
        return 0
    raise SystemExit("USE: RED_PHONE_BUILD_CAPSULE_V1.py [show|scope]")


if __name__ == "__main__":
    raise SystemExit(main())
