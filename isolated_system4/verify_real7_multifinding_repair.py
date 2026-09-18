from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import repair_proof_contract

REQUIRED = {
    "BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO",
    "BLOCKED_KNOWN_SHORT_CONCLUSION",
    "BLOCKED_WAVE2_CONCLUSION_BALANCE",
    "BLOCKED_WAVE2_TABLE_VALUE",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _plain(html: str) -> str:
    value = re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>", " ", html)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    return " ".join(value.split())


def _word_count(value: str) -> int:
    return len(re.findall(r"\b[\wÄÖÜäöüß-]+\b", value, re.UNICODE))


def _conclusion_metrics(html: str) -> tuple[float, int, int]:
    match = re.search(
        r'(?is)<section\b[^>]*data-block=(["\'])conclusion\1[^>]*>(.*?)</section>',
        html,
    )
    if not match:
        raise SystemExit("FINAL_CONCLUSION_BLOCK_MISSING")
    body = match.group(2)
    total_words = _word_count(_plain(html))
    conclusion_words = _word_count(_plain(body))
    paragraphs = len(re.findall(r"(?is)<p\b[^>]*>.*?</p>", body))
    ratio = conclusion_words / total_words if total_words else 0.0
    return ratio, conclusion_words, paragraphs


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        raise SystemExit("USAGE: verify_real7_multifinding_repair.py EVIDENCE_DIR OUTPUT_DIR")
    evidence_dir = Path(argv[1])
    output_dir = Path(argv[2])
    evidence_files = sorted(evidence_dir.glob("*-evidence.json"))
    if len(evidence_files) < 2:
        raise SystemExit("WORKSHOP_LOOP_REPAIR_COUNT_TOO_LOW:" + str(len(evidence_files)))
    evidences = [json.loads(path.read_text(encoding="utf-8")) for path in evidence_files]

    for evidence in evidences:
        if evidence.get("contract") != "SYSTEM4_TEST_GENERATED_REPAIR_EVIDENCE_V1":
            raise SystemExit("MULTIFINDING_REPAIR_EVIDENCE_CONTRACT_INVALID")
        if evidence.get("prebuilt_final_input_used") is not False:
            raise SystemExit("PREBUILT_FINAL_REPAIR_INPUT_FORBIDDEN")
        if evidence.get("repair_generated_from_workspace_state") is not True:
            raise SystemExit("REAL7_REPAIRABLE_FINDINGS_NOT_RETURNED_TO_WORKSHOP")
        if evidence.get("worker") != "DETERMINISTIC_TEST_WORKER" or evidence.get("codex_used") is not False:
            raise SystemExit("TECHNICAL_TEST_WORKER_IDENTITY_INVALID")
        if evidence.get("mocks_used") is not False or evidence.get("prepared_final_fixture_used") is not False:
            raise SystemExit("MOCK_OR_PREBUILT_FINAL_FORBIDDEN")
        if evidence.get("live_codex_repair_proven") is not False:
            raise SystemExit("LIVE_CODEX_REPAIR_FALSE_CLAIM")
        findings = evidence.get("findings")
        if not isinstance(findings, list) or not findings:
            raise SystemExit("MULTIFINDING_REPAIR_FINDINGS_MISSING")
        owners = {str(row.get("repair_owner") or "") for row in findings if isinstance(row, dict)}
        if owners != {"DRAFT_WORKER"}:
            raise SystemExit("REAL7_REPAIR_OWNER_INVALID:" + ",".join(sorted(owners)))

    first_findings = evidences[0]["findings"]
    codes = {str(row.get("error_code") or "") for row in first_findings if isinstance(row, dict)}
    missing = sorted(REQUIRED - codes)
    if missing:
        raise SystemExit("REAL7_REQUIRED_FINDINGS_NOT_REPRODUCED:" + ",".join(missing))

    before_paths: list[Path] = []
    after_paths: list[Path] = []
    for evidence_file, evidence in zip(evidence_files, evidences):
        prefix = evidence_file.name[:-len("-evidence.json")]
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
        before_paths.append(before)
        after_paths.append(after)

    for left, right in zip(after_paths, before_paths[1:]):
        if left.read_bytes() != right.read_bytes():
            raise SystemExit("WORKSHOP_LOOP_ARTICLE_CONTINUITY_BROKEN")

    proof_path = output_dir / "LIVE_PARITY_V2_1_PROOF.json"
    handoff_path = output_dir / "SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json"
    if not proof_path.is_file() or not handoff_path.is_file():
        raise SystemExit("MULTIFINDING_FINAL_ACCEPTANCE_OUTPUT_MISSING")
    route = json.loads(proof_path.read_text(encoding="utf-8"))
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    if route.get("article_count") != 1 or route.get("lt") != ["PASS"] or route.get("ppm") != ["PASS"]:
        raise SystemExit("MULTIFINDING_FINAL_REAL_VALIDATORS_NOT_PASS")
    if route.get("real_codex_repair_proven") is not False:
        raise SystemExit("DETERMINISTIC_ROUTE_MUST_NOT_CLAIM_REAL_CODEX")
    articles = handoff.get("articles")
    if not isinstance(articles, list) or len(articles) != 1:
        raise SystemExit("MULTIFINDING_FINAL_HANDOFF_COUNT_INVALID")
    final_body = str(articles[0].get("body") or "")
    final_sha = hashlib.sha256(final_body.encode("utf-8")).hexdigest()
    if final_sha != evidences[-1].get("after_sha256"):
        raise SystemExit("MULTIFINDING_AFTER_NOT_FINAL_ACCEPTED_BODY")

    conclusion_ratio, conclusion_words, conclusion_paragraphs = _conclusion_metrics(final_body)
    if conclusion_ratio < 0.10 or conclusion_paragraphs < 2:
        raise SystemExit(
            f"FINAL_BERATUNG_CONCLUSION_TARGET_NOT_MET:{conclusion_ratio}:{conclusion_paragraphs}"
        )

    synthetic_classification = repair_proof_contract.classify_repair_proof({
        "repair_routing_proven": True,
        "same_article_repair": True,
        "recheck_executed": True,
        "worker": "DETERMINISTIC_TEST_WORKER",
        "codex_used": False,
        "mocks_used": False,
        "prepared_final_fixture_used": False,
    })
    if synthetic_classification.get("repair_proof_level") != repair_proof_contract.ROUTING_PROVEN:
        raise SystemExit("SYNTHETIC_REPAIR_PROOF_LEVEL_INVALID")
    if synthetic_classification.get("real_codex_repair_proven") is not False:
        raise SystemExit("SYNTHETIC_REPAIR_MUST_NOT_PROVE_CODEX")

    proof = {
        "contract": "SYSTEM4_REAL7_MULTIFINDING_TECHNICAL_REPAIR_PROOF_V2",
        "status": "PASS",
        "required_findings": sorted(REQUIRED),
        "observed_findings": sorted(codes),
        "repair_owner": "DRAFT_WORKER",
        "workshop_return_count": len(evidences),
        "same_article_continuity_across_repairs": True,
        "before_sha256": evidences[0]["before_sha256"],
        "after_sha256": evidences[-1]["after_sha256"],
        "final_conclusion_ratio": conclusion_ratio,
        "final_conclusion_words": conclusion_words,
        "final_conclusion_paragraphs": conclusion_paragraphs,
        "real_beratung_conclusion_minimum_applied": 0.10,
        "real_languagetool_after_repair": "PASS",
        "real_ppm679_after_repair": "PASS",
        "prebuilt_final_input_used": False,
        "technical_repair_generation_proven": True,
        "repair_proof_level": repair_proof_contract.ROUTING_PROVEN,
        "repairable_quality_failure_policy": "RETURN_TO_DRAFT_WORKER_SAME_ARTICLE_UNTIL_PASS",
        "terminal_block_for_repairable_quality_findings": False,
        "codex_used": False,
        "live_codex_repair_proven": False,
        "publish_allowed": False,
    }
    target = output_dir / "SYSTEM4_REAL7_MULTIFINDING_TECHNICAL_REPAIR_PROOF_V2.json"
    target.write_text(json.dumps(proof, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(proof, ensure_ascii=False, sort_keys=True))
    print("SYSTEM4_REAL7_MULTIFINDING_TECHNICAL_REPAIR_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
