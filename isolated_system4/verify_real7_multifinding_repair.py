from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REQUIRED = {
    "BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO",
    "BLOCKED_KNOWN_SHORT_CONCLUSION",
    "BLOCKED_WAVE2_CONCLUSION_BALANCE",
    "BLOCKED_WAVE2_TABLE_VALUE",
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main(argv: list[str]) -> int:
    if len(argv) != 3:
        raise SystemExit("USAGE: verify_real7_multifinding_repair.py EVIDENCE_DIR OUTPUT_DIR")
    evidence_dir = Path(argv[1])
    output_dir = Path(argv[2])
    evidence_files = sorted(evidence_dir.glob("*-evidence.json"))
    if len(evidence_files) != 1:
        raise SystemExit("MULTIFINDING_REPAIR_EVIDENCE_COUNT_INVALID:" + str(len(evidence_files)))
    evidence = json.loads(evidence_files[0].read_text(encoding="utf-8"))
    if evidence.get("contract") != "SYSTEM4_TEST_GENERATED_REPAIR_EVIDENCE_V1":
        raise SystemExit("MULTIFINDING_REPAIR_EVIDENCE_CONTRACT_INVALID")
    if evidence.get("prebuilt_final_input_used") is not False:
        raise SystemExit("PREBUILT_FINAL_REPAIR_INPUT_FORBIDDEN")
    if evidence.get("repair_generated_from_workspace_state") is not True:
        raise SystemExit("REPAIR_NOT_GENERATED_FROM_WORKSPACE_STATE")
    if evidence.get("codex_used") is not False or evidence.get("live_codex_repair_proven") is not False:
        raise SystemExit("LIVE_CODEX_REPAIR_PROOF_FALSE_CLAIM")

    findings = evidence.get("findings")
    if not isinstance(findings, list):
        raise SystemExit("MULTIFINDING_REPAIR_FINDINGS_MISSING")
    codes = {str(row.get("error_code") or "") for row in findings if isinstance(row, dict)}
    missing = sorted(REQUIRED - codes)
    if missing:
        raise SystemExit("REAL7_REQUIRED_FINDINGS_NOT_REPRODUCED:" + ",".join(missing))
    owners = {str(row.get("repair_owner") or "") for row in findings if isinstance(row, dict)}
    if owners != {"DRAFT_WORKER"}:
        raise SystemExit("REAL7_REPAIR_OWNER_INVALID:" + ",".join(sorted(owners)))

    prefix = evidence_files[0].name[:-len("-evidence.json")]
    before = evidence_dir / (prefix + "-before.html")
    after = evidence_dir / (prefix + "-after.html")
    if not before.is_file() or not after.is_file():
        raise SystemExit("MULTIFINDING_BEFORE_AFTER_BYTES_MISSING")
    if sha(before) != evidence.get("before_sha256"):
        raise SystemExit("MULTIFINDING_BEFORE_HASH_MISMATCH")
    if sha(after) != evidence.get("after_sha256"):
        raise SystemExit("MULTIFINDING_AFTER_HASH_MISMATCH")
    if before.read_bytes() == after.read_bytes():
        raise SystemExit("MULTIFINDING_REPAIR_BYTES_UNCHANGED")

    proof_path = output_dir / "LIVE_PARITY_V2_1_PROOF.json"
    handoff_path = output_dir / "SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json"
    if not proof_path.is_file() or not handoff_path.is_file():
        raise SystemExit("MULTIFINDING_FINAL_ACCEPTANCE_OUTPUT_MISSING")
    route = json.loads(proof_path.read_text(encoding="utf-8"))
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    if route.get("article_count") != 1 or route.get("lt") != ["PASS"] or route.get("ppm") != ["PASS"]:
        raise SystemExit("MULTIFINDING_FINAL_REAL_VALIDATORS_NOT_PASS")
    articles = handoff.get("articles")
    if not isinstance(articles, list) or len(articles) != 1:
        raise SystemExit("MULTIFINDING_FINAL_HANDOFF_COUNT_INVALID")
    final_body = str(articles[0].get("body") or "")
    final_sha = hashlib.sha256(final_body.encode("utf-8")).hexdigest()
    if final_sha != evidence.get("after_sha256"):
        raise SystemExit("MULTIFINDING_AFTER_NOT_FINAL_ACCEPTED_BODY")

    proof = {
        "contract": "SYSTEM4_REAL7_MULTIFINDING_TECHNICAL_REPAIR_PROOF_V1",
        "status": "PASS",
        "required_findings": sorted(REQUIRED),
        "observed_findings": sorted(codes),
        "repair_owner": "DRAFT_WORKER",
        "before_sha256": evidence["before_sha256"],
        "after_sha256": evidence["after_sha256"],
        "real_languagetool_after_repair": "PASS",
        "real_ppm679_after_repair": "PASS",
        "prebuilt_final_input_used": False,
        "technical_repair_generation_proven": True,
        "codex_used": False,
        "live_codex_repair_proven": False,
        "live_codex_repair_status": "BLOCKED_PENDING_FRESH_EXPLICIT_USER_APPROVAL",
        "publish_allowed": False,
    }
    target = output_dir / "SYSTEM4_REAL7_MULTIFINDING_TECHNICAL_REPAIR_PROOF_V1.json"
    target.write_text(json.dumps(proof, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(proof, ensure_ascii=False, sort_keys=True))
    print("SYSTEM4_REAL7_MULTIFINDING_TECHNICAL_REPAIR_PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
