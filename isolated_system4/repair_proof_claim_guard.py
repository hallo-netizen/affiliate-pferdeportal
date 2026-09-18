from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

CASES = {
    "test_textmachine_repair_roundtrip_matrix.py": {
        "required": ("from unittest import mock", "mock.patch"),
        "classification": "MOCKED_ROUTING_RECHECK_ONLY",
    },
    "real_known_regression_acceptance_v3.py": {
        "required": ("files['final']", "'repair'"),
        "classification": "PREBUILT_FINAL_REPAIR_INPUT",
    },
    "full_local_acceptance.py": {
        "required": ("'codex_used':False", "f['final']", "'repair'"),
        "classification": "NO_CODEX_PREBUILT_FINAL_REPAIR_INPUT",
    },
}

def main() -> int:
    rows = []
    for name, spec in CASES.items():
        text = (HERE / name).read_text(encoding="utf-8")
        missing = [token for token in spec["required"] if token not in text]
        if missing:
            raise SystemExit("REPAIR_PROOF_CLASSIFICATION_SOURCE_DRIFT:" + name + ":" + ",".join(missing))
        rows.append({
            "file": name,
            "classification": spec["classification"],
            "live_codex_repair_proof_allowed": False,
        })
    out = {
        "contract": "SYSTEM4_REPAIR_PROOF_CLAIM_GUARD_V1",
        "status": "PASS",
        "historical_green_tests_live_codex_repair_proof": False,
        "reason": "Mocks or prebuilt corrected final bodies cannot prove writer-generated live repair.",
        "cases": rows,
        "publish_allowed": False,
    }
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    print("SYSTEM4_REPAIR_PROOF_CLAIM_GUARD_PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
