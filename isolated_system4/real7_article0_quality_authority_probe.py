from __future__ import annotations

import json
import zipfile
from pathlib import Path

import production_checks

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SNAPSHOT = REPO / "control/startmaster0107/runtime_inbox/generations/000001/SOURCE_SNAPSHOT.json"
CURRENT = REPO / "control/startmaster0107/CURRENT_STATE.json"
PPM = REPO / production_checks.PPM_PACKAGE_REL
TYPE_MEMBER = "portal-production-machine/contracts/article-type-templates.json"
STRUCTURE_MEMBER = "portal-production-machine/contracts/content-structure-language-gate-v2.json"

REQUIRED_CODES = {
    "BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO",
    "BLOCKED_KNOWN_SHORT_CONCLUSION",
    "BLOCKED_WAVE2_CONCLUSION_BALANCE",
    "BLOCKED_WAVE2_TABLE_VALUE",
}


def main() -> int:
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    items = snapshot["next_textmachine_metadata_batch"]["items"]
    if not items:
        raise SystemExit("REAL7_ARTICLE0_METADATA_MISSING")
    item0 = items[0]
    expected_identity = {
        "article_type": "Beratung",
        "category": "hindernisstangen-beratung",
        "target_keyword": "Hindernisstangen für Pferde",
        "title": "Das Wichtigste über Hindernisstangen für Pferde",
    }
    for field, expected in expected_identity.items():
        if item0.get(field) != expected:
            raise SystemExit("REAL7_ARTICLE0_IDENTITY_DRIFT:" + field + ":" + str(item0.get(field)))

    with zipfile.ZipFile(PPM) as zf:
        types = json.loads(zf.read(TYPE_MEMBER).decode("utf-8"))
        structure = json.loads(zf.read(STRUCTURE_MEMBER).decode("utf-8"))

    beratung = (types.get("types") or {}).get("Beratung") or {}
    type_ratio = float(beratung.get("conclusion_min_ratio") or 0)
    structure_ratio = float(((structure.get("conclusion") or {}).get("minimum_ratio_by_type") or {}).get("Beratung") or 0)
    table_ratio = float((structure.get("table") or {}).get("minimum_unique_content_token_ratio") or 0)
    if type_ratio != 0.1 or structure_ratio != 0.1:
        raise SystemExit(f"REAL7_BERATUNG_CONCLUSION_THRESHOLD_DRIFT:{type_ratio}:{structure_ratio}")
    if table_ratio != 0.18:
        raise SystemExit("REAL7_TABLE_THRESHOLD_DRIFT:" + str(table_ratio))

    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    teststrecke = current.get("system4a_codex_free_teststrecke") or {}
    multi = teststrecke.get("multifinding_repair") or {}
    durable_codes = set(multi.get("required_findings") or [])
    if durable_codes != REQUIRED_CODES:
        missing = REQUIRED_CODES - durable_codes
        extra = durable_codes - REQUIRED_CODES
        raise SystemExit(
            "REAL7_DURABLE_FINDING_AUTHORITY_DRIFT:MISSING="
            + ",".join(sorted(missing))
            + ":EXTRA="
            + ",".join(sorted(extra))
        )
    quality_negative = teststrecke.get("quality_negative") or {}
    if quality_negative.get("checker") != "PPM679":
        raise SystemExit("REAL7_QUALITY_NEGATIVE_CHECKER_DRIFT")
    if float(quality_negative.get("maximum_ratio") or 0) != 0.02:
        raise SystemExit("REAL7_DUPLICATE_THRESHOLD_DRIFT")
    if quality_negative.get("repair_owner") != "DRAFT_WORKER":
        raise SystemExit("REAL7_QUALITY_NEGATIVE_OWNER_DRIFT")
    if multi.get("repairable_quality_failure_policy") not in {
        None,
        "RETURN_TO_DRAFT_WORKER_SAME_ARTICLE_UNTIL_PASS",
    }:
        raise SystemExit("REAL7_REPAIR_POLICY_DRIFT")
    for code in REQUIRED_CODES:
        owner = production_checks._ppm_repair_owner({"error_code": code})
        if owner != production_checks.DRAFT_WORKER:
            raise SystemExit("REAL7_FINDING_OWNER_DRIFT:" + code + ":" + owner)

    result = {
        "contract": "SYSTEM4_REAL7_ARTICLE0_QUALITY_AUTHORITY_PROBE_V2",
        "status": "PASS",
        "article_index": 0,
        **expected_identity,
        "conclusion_min_ratio": 0.1,
        "duplicate_sentence_max_ratio": 0.02,
        "table_unique_content_min_ratio": 0.18,
        "required_findings": sorted(REQUIRED_CODES),
        "repair_owner": "DRAFT_WORKER",
        "repairable_quality_policy": "RETURN_TO_DRAFT_WORKER_SAME_ARTICLE_UNTIL_PASS",
        "terminal_block_for_repairable_quality_findings": False,
        "publish_allowed": False,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    print("SYSTEM4_REAL7_ARTICLE0_QUALITY_AUTHORITY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
