from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import content_guard
import production_checks

ROOT = Path(__file__).resolve().parent
REF = ROOT / "reference_quality"
ORIGINAL = REF / "putzplatzmatten_original_reference.md"
OPTIMIZED = REF / "putzplatzmatten_optimized_reference.md"
ORIGINAL_SHA256 = "b920d086ed9707d4be770cde87f25d5cc8e34717637264d5cc179dae15245b4f"
OPTIMIZED_SHA256 = "61eae6307be3e9bb4d3bcb7ccbc1453853c02251a0569c782b50ce020791f74a"
PROOF = ROOT / "FIRST_FULL_RULE_TEST_ARTICLE_PROOF.json"


class ReferenceQualityError(RuntimeError):
    pass


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(value: str) -> list[str]:
    return re.findall(r"\b[\wÄÖÜäöüß-]+\b", value, re.UNICODE)


def section(md: str, heading: str) -> str:
    marker = "## " + heading
    if marker not in md:
        return ""
    tail = md.split(marker, 1)[1]
    return tail.split("\n## ", 1)[0].strip()


def table_body_rows(md: str) -> int:
    lines = [line.strip() for line in md.splitlines()]
    count = 0
    inside = False
    separator_seen = False
    for line in lines:
        if line.startswith("|") and line.endswith("|"):
            if not inside:
                inside = True
                continue
            if re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", line):
                separator_seen = True
                continue
            if separator_seen:
                count += 1
        elif inside:
            break
    return count


def normalized_sentences(md: str) -> list[str]:
    value = re.sub(r"(?m)^#{1,6}\s+.*$", " ", md)
    value = re.sub(r"(?m)^\|.*\|$", " ", value)
    value = re.sub(r"(?m)^[-*]\s+", "", value)
    raw = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", value).strip())
    out = []
    for row in raw:
        token = re.sub(r"\s+", " ", row.casefold()).strip()
        if len(words(token)) >= 6:
            out.append(token)
    return out


def duplicate_sentence_ratio(md: str) -> float:
    rows = normalized_sentences(md)
    if not rows:
        return 0.0
    duplicate_instances = len(rows) - len(set(rows))
    return duplicate_instances / len(rows)


def main() -> int:
    if sha(ORIGINAL) != ORIGINAL_SHA256:
        raise ReferenceQualityError("ORIGINAL_REFERENCE_HASH_CHANGED")
    if sha(OPTIMIZED) != OPTIMIZED_SHA256:
        raise ReferenceQualityError("OPTIMIZED_REFERENCE_HASH_CHANGED")

    original = ORIGINAL.read_text(encoding="utf-8")
    optimized = OPTIMIZED.read_text(encoding="utf-8")

    continuity = content_guard.validate_repair_continuity(original, optimized)

    if "## Fazit" in original:
        raise ReferenceQualityError("ORIGINAL_REFERENCE_UNEXPECTEDLY_CHANGED")
    conclusion = section(optimized, "Fazit")
    if not conclusion:
        raise ReferenceQualityError("OPTIMIZED_REFERENCE_CONCLUSION_MISSING")

    original_rows = table_body_rows(original)
    optimized_rows = table_body_rows(optimized)
    if optimized_rows <= original_rows:
        raise ReferenceQualityError("OPTIMIZED_REFERENCE_TABLE_NOT_STRONGER")

    original_dup = duplicate_sentence_ratio(original)
    optimized_dup = duplicate_sentence_ratio(optimized)
    if optimized_dup > original_dup:
        raise ReferenceQualityError("OPTIMIZED_REFERENCE_DUPLICATION_REGRESSED")

    for phrase in (
        "Putzplatzmatten für Pferde",
        "tragfähige, ebene",
        "Puzzleverbindungen",
        "Stehende Nässe",
        "Herstellerangaben",
        "Probefläche",
    ):
        if phrase.casefold() not in optimized.casefold():
            raise ReferenceQualityError("OPTIMIZED_REFERENCE_SUBJECT_DRIFT:" + phrase)

    # Real LanguageTool 6.8; the hash-bound JAR is supplied by the existing
    # System-4A acceptance workflow. This is the only executable language check here.
    lt = production_checks.run_languagetool(ROOT.parent, optimized)

    # Do not invent a second PPM quality authority. Instead, bind this reference
    # test to the existing proof that the current PPM 6.7.9 quality validator
    # accepted a real horse-domain full-rule article, while the normal System-4A
    # workflow continues to execute the current PPM positive/negative matrix.
    proof = json.loads(PROOF.read_text(encoding="utf-8"))
    ppm = proof.get("authoritative_tool_bindings", {}).get("ppm", {})
    positive = proof.get("positive_test", {})
    if proof.get("status") != "PASS":
        raise ReferenceQualityError("KNOWN_GOOD_PPM_PROOF_NOT_PASS")
    if ppm.get("package_sha256") != production_checks.PPM_PACKAGE_SHA256:
        raise ReferenceQualityError("KNOWN_GOOD_PPM_PROOF_PACKAGE_DRIFT")
    if positive.get("content_quality_status") != "CONTENT_QUALITY_CHECK_OK":
        raise ReferenceQualityError("KNOWN_GOOD_PPM_CONTENT_QUALITY_NOT_PASS")
    if positive.get("fail_closed_aggregate_status") != "PASS":
        raise ReferenceQualityError("KNOWN_GOOD_PPM_AGGREGATE_NOT_PASS")

    result = {
        "contract": "SYSTEM4A_REFERENCE_QUALITY_REGRESSION_V1",
        "status": "PASS",
        "scope": "TEST_ONLY_REFERENCE_NOT_PRODUCTION_PASS_AUTHORITY",
        "original_sha256": ORIGINAL_SHA256,
        "optimized_sha256": OPTIMIZED_SHA256,
        "original_word_count": len(words(original)),
        "optimized_word_count": len(words(optimized)),
        "repair_continuity": continuity,
        "original_duplicate_sentence_ratio_diagnostic": round(original_dup, 6),
        "optimized_duplicate_sentence_ratio_diagnostic": round(optimized_dup, 6),
        "original_table_body_rows": original_rows,
        "optimized_table_body_rows": optimized_rows,
        "optimized_conclusion_words": len(words(conclusion)),
        "languagetool": {
            "status": lt["status"],
            "engine": lt["engine"],
            "finding_count": lt["finding_count"],
        },
        "ppm_authority": {
            "package_sha256": production_checks.PPM_PACKAGE_SHA256,
            "known_good_real_article_proof": "FIRST_FULL_RULE_TEST_ARTICLE_PROOF.json",
            "reference_article_direct_ppm_pass_claimed": False,
        },
        "production_rules_changed": False,
        "publish_allowed": False,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    print("SYSTEM4A_REFERENCE_QUALITY_REGRESSION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
