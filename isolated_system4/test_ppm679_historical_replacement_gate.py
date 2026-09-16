from __future__ import annotations

import hashlib
import json
import unittest
import zipfile
from pathlib import Path

PACKAGE_REL = Path("control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip")
PACKAGE_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"

RETIRED_HISTORICAL_TESTS = {
    "tests/three-type-bundled-local/test-beratung-positive.php": {
        "replacements": {
            "tests/normal-draft-production/test-01-positive-1-to-4.php",
            "tests/three-type-live-test-release/test-05-category-resolution.php",
            "tests/three-type-live-test-release/test-07-bundled-simulation-success.php",
            "tests/three-type-bundled-local/test-beratung-negative.php",
        },
        "reason": "Old signed-quarantine Beratung positive fixture; current normal-draft/live positive path plus retained negative mutation cover the protection function.",
    },
    "tests/three-type-bundled-local/test-bundled-overall-and-no-live.php": {
        "replacements": {
            "tests/three-type-live-test-release/test-01-release-positive.php",
            "tests/three-type-live-test-release/test-07-bundled-simulation-success.php",
            "tests/three-type-live-test-release/test-12-static-boundaries.php",
            "tests/test-build-integrity-only.php",
        },
        "reason": "Old phase required zero WordPress writes. The successor phase intentionally permits max three controlled drafts while keeping publish/wissen/global production closed and current build integrity signed.",
    },
    "tests/three-type-bundled-local/test-pflege-positive.php": {
        "replacements": {
            "tests/normal-draft-production/test-01-positive-1-to-4.php",
            "tests/three-type-live-test-release/test-05-category-resolution.php",
            "tests/three-type-live-test-release/test-07-bundled-simulation-success.php",
            "tests/three-type-bundled-local/test-pflege-negative.php",
        },
        "reason": "Old signed-quarantine Pflege positive fixture; current normal-draft/live positive path plus retained negative mutation cover the protection function.",
    },
    "tests/three-type-bundled-local/test-release-gate-positive.php": {
        "replacements": {
            "tests/three-type-live-test-release/test-01-release-positive.php",
            "tests/three-type-live-test-release/test-02-release-negative.php",
            "tests/three-type-live-test-release/test-12-static-boundaries.php",
            "tests/test-wave2-article-type-quarantine.php",
        },
        "reason": "Old quarantine release gate is superseded by the later live-test release gate with explicit positive/negative scope checks and continued production/publish closure.",
    },
    "tests/three-type-bundled-local/test-signed-integration-traceability.php": {
        "replacements": {
            "tests/test-build-integrity-only.php",
            "tests/test-read-only-health-button.php",
            "tests/three-type-live-test-release/test-12-static-boundaries.php",
            "tests/three-type-bundled-local/test-signed-manifest-scope.php",
        },
        "reason": "Historical exact hashes are superseded by the signed current build manifest; current positive and tamper-negative integrity tests protect the same purpose.",
    },
    "tests/three-type-bundled-local/test-signed-quarantine-boundaries.php": {
        "replacements": {
            "tests/three-type-live-test-release/test-01-release-positive.php",
            "tests/three-type-live-test-release/test-11-entrypoint-authorization-negative.php",
            "tests/three-type-live-test-release/test-12-static-boundaries.php",
            "tests/normal-draft-production/test-01-positive-1-to-4.php",
        },
        "reason": "Old no-draft quarantine boundary is phase-specific; successor tests retain authorization, no-publish, no-wissen, global production closure and draft-only behavior.",
    },
    "tests/three-type-bundled-local/test-v38-baseline-byte-identity.php": {
        "replacements": {
            "tests/test-build-integrity-only.php",
            "tests/test-read-only-health-button.php",
            "tests/test-runtime-safety.php",
            "tests/three-type-live-test-release/test-12-static-boundaries.php",
        },
        "reason": "The V3.8 transition baseline is historical. Current signed-manifest integrity plus explicit tamper-negative tests now detect unintended drift against the current approved build.",
    },
    "tests/three-type-bundled-local/test-vergleich-positive.php": {
        "replacements": {
            "tests/normal-draft-production/test-01-positive-1-to-4.php",
            "tests/three-type-live-test-release/test-05-category-resolution.php",
            "tests/three-type-live-test-release/test-07-bundled-simulation-success.php",
            "tests/three-type-bundled-local/test-vergleich-negative.php",
        },
        "reason": "Old signed-quarantine Vergleich positive fixture; current normal-draft/live positive path plus retained negative mutation cover the protection function.",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Ppm679HistoricalReplacementGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(__file__).resolve().parent.parent
        self.package = self.repo / PACKAGE_REL
        self.assertTrue(self.package.is_file())
        self.assertEqual(sha256(self.package), PACKAGE_SHA256)

    def _read_json(self, zf: zipfile.ZipFile, rel: str) -> dict:
        raw = zf.read("portal-production-machine/" + rel)
        data = json.loads(raw.decode("utf-8"))
        self.assertIsInstance(data, dict)
        return data

    def test_old_tests_can_leave_current_gate_only_with_current_replacements(self) -> None:
        with zipfile.ZipFile(self.package) as zf:
            names = set(zf.namelist())
            all_test_paths = {
                n[len("portal-production-machine/") :]
                for n in names
                if n.startswith("portal-production-machine/tests/")
                and n.endswith(".php")
                and Path(n).name.startswith("test-")
            }

            self.assertEqual(set(RETIRED_HISTORICAL_TESTS), set(RETIRED_HISTORICAL_TESTS) & all_test_paths)

            registry = self._read_json(zf, "contracts/hard-rule-registry-v1.json")
            mapped = set()
            for rule in registry.get("rules", []):
                for key in ("positive_test", "negative_test"):
                    value = rule.get(key)
                    if isinstance(value, str):
                        mapped.add(value)
            self.assertTrue(set(RETIRED_HISTORICAL_TESTS).isdisjoint(mapped))

            for retired, spec in RETIRED_HISTORICAL_TESTS.items():
                replacements = set(spec["replacements"])
                self.assertTrue(replacements)
                self.assertTrue(
                    replacements.issubset(all_test_paths),
                    msg=f"{retired} replacement missing: {sorted(replacements - all_test_paths)}",
                )

            old_release = self._read_json(zf, "contracts/three-type-bundled-local-release-v1.json")
            live_release = self._read_json(zf, "contracts/three-type-bundled-live-test-release-v1.json")
            live_scope = self._read_json(zf, "traceability/THREE_TYPE_BUNDLED_LIVE_TEST_RELEASE_SCOPE.json")
            self.assertEqual(old_release.get("scope_mode"), "THREE_TYPE_BUNDLED_SIGNED_QUARANTINE_NO_LIVE")
            self.assertEqual(live_release.get("scope_mode"), "THREE_TYPE_BUNDLED_SINGLE_SESSION_MAX_THREE_DRAFTS")
            self.assertEqual(live_release.get("maximum_total_new_drafts"), 3)
            self.assertFalse(live_release.get("publish_allowed"))
            self.assertFalse(live_release.get("wissen_allowed"))
            self.assertFalse(live_release.get("global_production_release_allowed"))
            self.assertEqual(live_scope.get("maximum_future_drafts"), 3)
            self.assertIn(
                "contracts/three-type-bundled-local-release-v1.json",
                live_scope.get("authorized_existing_file_changes", []),
            )
            self.assertIn(
                "tests/three-type-bundled-local/test-v38-baseline-byte-identity.php",
                live_scope.get("authorized_existing_file_changes", []),
            )

            for retained_negative in (
                "tests/three-type-bundled-local/test-beratung-negative.php",
                "tests/three-type-bundled-local/test-pflege-negative.php",
                "tests/three-type-bundled-local/test-vergleich-negative.php",
                "tests/three-type-bundled-local/test-release-gate-negative.php",
                "tests/three-type-bundled-local/test-signed-manifest-scope.php",
                "tests/three-type-bundled-local/test-complete-category-source.php",
            ):
                self.assertIn(retained_negative, all_test_paths)
                self.assertNotIn(retained_negative, RETIRED_HISTORICAL_TESTS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
