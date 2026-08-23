#!/usr/bin/env python3
"""Mechanical release hardlock for production packages.

A delivery file may be emitted only when the real downstream QA artifacts prove:
PSERC envelope -> supervisor authenticity/full validation -> PSERC/PPM bridge ->
PPM normal draft -> readback PASS, plus required negative probes.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

REQUIRED_PPM_STATUS = "NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def release(candidate: Path, qa_dir: Path, output: Path) -> dict:
    ppm = load(qa_dir / "PPM679_FULL_END_TO_END.json")
    pserc = load(qa_dir / "PSERC_SUPERVISOR_PPM_FULL_END_TO_END.json")
    neg_hash = load(qa_dir / "NEGATIVE_OLD_COMPACT_FACT_HASH_BLOCKED.json")
    neg_td = load(qa_dir / "NEGATIVE_MISSING_TD_FACT_REFS_BLOCKED.json")

    checks = {
        "ppm_full": ppm.get("status") == REQUIRED_PPM_STATUS and ppm.get("draft_count") == 1,
        "pserc_envelope": pserc.get("envelope", {}).get("status") == "PSERC_PRODUCTION_PACKAGE_ENVELOPE_PASS",
        "supervisor_auth": pserc.get("authenticity", {}).get("status") == "SUPERVISOR_STORED_RELEASE_AUTHENTICITY_PASS",
        "supervisor_full": pserc.get("supervisor", {}).get("status") == "PSERC_WORKFLOW_SUPERVISOR_PASS",
        "bridge_full": pserc.get("bridge_status") == "PSERC_PPM_INTAKE_BRIDGE_EXECUTED",
        "bridge_ppm_full": pserc.get("ppm_status") == REQUIRED_PPM_STATUS,
        "negative_wrong_fact_hash": neg_hash.get("status") == "BLOCKED_FACT_PACK_HASH_MISMATCH",
        "negative_missing_td_fact_refs": neg_td.get("status") == "BLOCKED_CONTENT_FACT_REFS_MISSING",
    }
    if not all(checks.values()):
        raise SystemExit(json.dumps({"status": "FINAL_RELEASE_GATE_BLOCKED", "checks": checks}, indent=2))

    shutil.copy2(candidate, output)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return {
        "status": "FINAL_RELEASE_GATE_PASS",
        "checks": checks,
        "delivery_file": output.name,
        "sha256": digest,
        "publish_allowed": False,
        "rule": "NO_FINAL_DELIVERY_WITHOUT_REAL_PSERCPPM_DRAFT_READBACK_PREFLIGHT_PASS",
    }


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: production-package-release-gate-v2.py CANDIDATE QA_DIR OUTPUT")
    result = release(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
    print(json.dumps(result, ensure_ascii=False, indent=2))
