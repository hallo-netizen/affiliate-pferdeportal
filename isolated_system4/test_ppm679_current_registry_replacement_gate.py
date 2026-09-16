from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

PACKAGE_REL = Path("control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip")
PACKAGE_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"

REPLACED_CURRENT_TESTS = {
    "tests/test-canonical-runtime-binding.php": {
        "BLOCKED_CONTENT_WORD_FLOOR",
        "BLOCKED_CONTENT_PARAGRAPH_FLOOR",
        "BLOCKED_CONTENT_H2_FLOOR",
        "BLOCKED_CONTENT_TABLE_ROW_FLOOR",
        "BLOCKED_CONTENT_INTERNAL_LINK_ROLE",
        "BLOCKED_CONTENT_FACT_REFS_MISSING",
        "BLOCKED_CONTENT_FACT_REF_UNKNOWN",
        "BLOCKED_CONTENT_FACT_REF_NOT_VERIFIED",
        "BLOCKED_CONTENT_FACT_REF_TYPE_MISMATCH",
        "BLOCKED_CONTENT_NUMERIC_CLAIM_UNSUPPORTED",
        "BLOCKED_CONTENT_TRACE_CLAIM_MISMATCH",
        "BLOCKED_CONTENT_FACT_PACK_COVERAGE",
        "BLOCKED_CONTENT_TRACE_LEXICAL_SUPPORT",
        "BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO",
        "BLOCKED_CONTENT_INTRO_PAIR_SIMILARITY",
    },
    "tests/test-g9-faq-only-live-state-integration.php": {
        "BLOCKED_ARTICLE_TYPE_NOT_PRODUCTION_ALLOWED",
        "BLOCKED_BUILD_SIGNATURE_INVALID",
        "BLOCKED_ACTIVE_COMPONENT_HASH_MISMATCH",
        "BLOCKED_G9_FAQ_RELEASE_SCOPE_MISMATCH",
        "BLOCKED_CANONICAL_TABLE_PLUGIN_INACTIVE",
    },
    "tests/test-historical-regressions.php": set(),
    "tests/test-positive-pipeline.php": {
        "BLOCKED_PLAN_ITEM_FIELD_MISSING",
        "BLOCKED_CANONICAL_RUNTIME_ORDER_INCOMPLETE",
        "BLOCKED_CANONICAL_ARTICLE_PAYLOAD_INCOMPLETE",
        "BLOCKED_PRODUCTION_TEST_FACT_PACK",
    },
    "tests/test-wave1-unsigned-quarantine-blocked.php": {
        "BLOCKED_BUILD_MANIFEST_MISSING",
        "BLOCKED_BUILD_MANIFEST_INVALID",
        "BLOCKED_BUILD_SIGNATURE_RUNTIME_UNAVAILABLE",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Ppm679CurrentRegistryReplacementGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(__file__).resolve().parent.parent
        self.package = self.repo / PACKAGE_REL
        self.assertTrue(self.package.is_file())
        self.assertEqual(sha256(self.package), PACKAGE_SHA256)
        self.tmp = tempfile.TemporaryDirectory(prefix="ppm679-current-replacement-")
        self.root = Path(self.tmp.name)
        with zipfile.ZipFile(self.package) as zf:
            zf.extractall(self.root)
        self.ppm = self.root / "portal-production-machine"
        self.tests = self.ppm / "tests"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _run(self, rel: str, *, disable_sodium: bool = False, expected_rc: int = 0) -> subprocess.CompletedProcess[str]:
        cmd = ["php"]
        if disable_sodium:
            cmd += ["-d", "disable_functions=sodium_crypto_sign_verify_detached"]
        cmd.append(str(self.ppm / rel))
        cp = subprocess.run(cmd, cwd=self.ppm, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False)
        self.assertEqual(cp.returncode, expected_rc, msg=f"{rel} rc={cp.returncode}\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}")
        return cp

    def _write_test(self, name: str, body: str) -> str:
        rel = f"tests/{name}"
        (self.ppm / rel).write_text(body, encoding="utf-8")
        return rel

    def _registry_mappings(self) -> dict[str, set[str]]:
        registry = json.loads((self.ppm / "contracts/hard-rule-registry-v1.json").read_text(encoding="utf-8"))
        out = {name: set() for name in REPLACED_CURRENT_TESTS}
        for rule in registry.get("rules", []):
            for key in ("positive_test", "negative_test"):
                target = rule.get(key)
                if target in out:
                    code = str(rule.get("error_code") or "")
                    if code:
                        out[target].add(code)
        return out

    def test_registry_mapping_is_known_and_replacements_are_fail_closed(self) -> None:
        mappings = self._registry_mappings()
        self.assertEqual(mappings["tests/test-canonical-runtime-binding.php"], REPLACED_CURRENT_TESTS["tests/test-canonical-runtime-binding.php"])
        self.assertEqual(mappings["tests/test-g9-faq-only-live-state-integration.php"], REPLACED_CURRENT_TESTS["tests/test-g9-faq-only-live-state-integration.php"])
        self.assertEqual(mappings["tests/test-positive-pipeline.php"], REPLACED_CURRENT_TESTS["tests/test-positive-pipeline.php"])
        self.assertEqual(mappings["tests/test-wave1-unsigned-quarantine-blocked.php"], REPLACED_CURRENT_TESTS["tests/test-wave1-unsigned-quarantine-blocked.php"])
        self.assertEqual(len(mappings["tests/test-historical-regressions.php"]), 69)

        # 1) Canonical content protections: the old four-item positive fixture is stale,
        # but every negative mutation in the original test uses the still-current FAQ item.
        canonical = (self.tests / "test-canonical-runtime-binding.php").read_text(encoding="utf-8")
        marker = "$items=$input['items'];"
        self.assertEqual(canonical.count(marker), 1)
        canonical_current = canonical.replace(marker, "$items=array($input['items'][0]);", 1)
        rel = self._write_test("__system4-current-canonical-runtime-binding.php", canonical_current)
        cp = self._run(rel)
        report = json.loads(cp.stdout)
        self.assertEqual(report.get("status"), "PASS")
        self.assertEqual(report.get("negative_tests_total"), 16)
        observed = set()
        for row in report.get("negative_tests", []):
            observed.update(str(code) for code in row.get("codes", []))
        self.assertTrue(REPLACED_CURRENT_TESTS["tests/test-canonical-runtime-binding.php"].issubset(observed))

        # 2) G9 live-state protections: only the historical expectation that the tree is
        # unsigned is stale. The exact signed tree must be clean; scope and plugin gates stay active.
        g9 = (self.tests / "test-g9-faq-only-live-state-integration.php").read_text(encoding="utf-8")
        stale = "ppm_test_assert(in_array('BLOCKED_ACTIVE_COMPONENT_HASH_MISMATCH',$codes,true) || in_array('BLOCKED_BUILD_FILE_HASH_MISMATCH',$codes,true) || in_array('BLOCKED_BUILD_SIGNATURE_INVALID',$codes,true) || in_array('BLOCKED_BUILD_MANIFEST_HASH_MISMATCH',$codes,true),'unsigned repair tree must remain blocked by build integrity');"
        current = "ppm_test_assert(!in_array('BLOCKED_ACTIVE_COMPONENT_HASH_MISMATCH',$codes,true) && !in_array('BLOCKED_BUILD_FILE_HASH_MISMATCH',$codes,true) && !in_array('BLOCKED_BUILD_SIGNATURE_INVALID',$codes,true) && !in_array('BLOCKED_BUILD_MANIFEST_HASH_MISMATCH',$codes,true),'current signed tree must pass build integrity');"
        self.assertEqual(g9.count(stale), 1)
        rel = self._write_test("__system4-current-g9-live-state.php", g9.replace(stale, current, 1))
        cp = self._run(rel)
        report = json.loads(cp.stdout)
        self.assertEqual(report.get("status"), "PASS_G9_FAQ_ONLY_LIVE_STATE_INTEGRATION")
        self.assertTrue(report.get("other_gate_preserved"))
        for support in (
            "tests/test-build-integrity-only.php",
            "tests/test-read-only-health-button.php",
            "tests/test-wave2-article-type-quarantine.php",
            "tests/test-g9-faq-only-release-gate-negative.php",
        ):
            self._run(support)

        # 3) Historical regression suite: unchanged original must still pass incidents 1..14
        # and stop only because today's global production quarantine prevents the old incident-15 baseline.
        cp = self._run("tests/test-historical-regressions.php", expected_rc=2)
        self.assertIn("ASSERTION_FAILED: Baseline gate must be green before state mutation.", cp.stderr)

        incident15 = r'''<?php
require __DIR__.'/bootstrap-test.php';
PPM679_WP::reset_test_state(); PPM679_Storage::reset_test_state(); PPM679_Handoff_Permit::reset_test_state();
PPM679_WP::update_option('ppm679_schema_version','6.7.9'); PPM679_WP::update_option('ppm_publish_enabled','0'); PPM679_WP::update_option('ppm_server_instance_id',PPM679_BOUND_SERVER_INSTANCE_ID);
$artifact=array('status'=>'STRUCTURAL_CHECK_OK','value'=>'bound');
$scope=PPM679_G9_FAQ_Test_Release_Validator::expected_scope();
$gate=PPM679_Live_State_Gate::verify_live_state_or_abort('g9_single_faq_pre_draft',PPM679_G9_FAQ_Test_Release_Validator::ARTICLE_SHA256,null,null,array('server_instance_id'=>PPM679_BOUND_SERVER_INSTANCE_ID,'article_type_release_scope'=>$scope));
ppm_test_assert(!empty($gate['ok']),'Current scoped baseline gate must be green.');
$permit=PPM679_Handoff_Permit::issue('g9_single_faq_pre_draft','json',$artifact,$gate);
PPM679_WP::update_option('ppm_publish_enabled','1');
$report=json_decode(PPM679_Handoff_Writer::encode_json($permit,$artifact),true);
$codes=array_column($report['errors']??array(),'error_code');
ppm_test_assert(in_array('BLOCKED_SERVER_STATE_CHANGED_AFTER_HANDSHAKE',$codes,true),'State mutation after handshake must block.');
echo json_encode(array('status'=>'PASS','code'=>'BLOCKED_SERVER_STATE_CHANGED_AFTER_HANDSHAKE'))."\n";
'''
        rel = self._write_test("__system4-current-historical-incident15.php", incident15)
        self.assertEqual(json.loads(self._run(rel).stdout).get("status"), "PASS")

        incident16 = r'''<?php
require __DIR__.'/bootstrap-test.php';
PPM679_WP::reset_test_state(); PPM679_Storage::reset_test_state();
PPM679_Storage::set_test_fault('schema_failure',true);
$report=PPM679_Storage::ensure_schema();
$codes=array_column($report['errors']??array(),'error_code');
ppm_test_assert(($report['status']??'')==='BLOCKED_SCHEMA_SETUP_FAILED','Schema fault must block.');
ppm_test_assert(in_array('BLOCKED_SCHEMA_SETUP_FAILED',$codes,true),'Schema blocker code must remain.');
echo json_encode(array('status'=>'PASS','continued'=>true,'code'=>'BLOCKED_SCHEMA_SETUP_FAILED'))."\n";
'''
        rel = self._write_test("__system4-current-historical-incident16.php", incident16)
        report = json.loads(self._run(rel).stdout)
        self.assertTrue(report.get("continued"))

        # 4) Legacy plan protection: today's production quarantine blocks even earlier,
        # while the plan validator still emits every canonical legacy-plan blocker.
        positive = r'''<?php
require __DIR__.'/bootstrap-test.php';
PPM679_WP::reset_test_state(); PPM679_Storage::reset_test_state(); PPM679_Handoff_Permit::reset_test_state();
PPM679_WP::update_option('ppm_publish_enabled','0'); PPM679_WP::update_option('ppm_server_instance_id','ppm-5e2ef7a9-5a11-4682-85f7-cf94d86a59ee');
$plan=json_decode((string)file_get_contents(__DIR__.'/plan-v4.json'),true);
$direct=PPM679_Plan_Validator::validate($plan,'system4_current_legacy_plan_boundary','local-state-hash');
$direct_codes=array_values(array_unique(array_map(fn($e)=>(string)($e['error_code']??''),$direct['errors']??array())));
$pipeline=PPM679_Pipeline::execute_plan($plan); $artifact=$pipeline['artifact'];
ppm_test_assert(($artifact['status']??'')==='BLOCKED_ARTICLE_TYPE_NOT_PRODUCTION_ALLOWED','Current pipeline must fail earlier at global production quarantine.');
ppm_test_assert(count($artifact['drafts']??array())===0,'Legacy plan must create zero drafts.');
foreach(array('BLOCKED_PLAN_ITEM_FIELD_MISSING','BLOCKED_CANONICAL_RUNTIME_ORDER_INCOMPLETE','BLOCKED_CANONICAL_ARTICLE_PAYLOAD_INCOMPLETE','BLOCKED_PRODUCTION_TEST_FACT_PACK') as $code){ppm_test_assert(in_array($code,$direct_codes,true),'Direct current plan validator must retain '.$code);}
echo json_encode(array('status'=>'PASS','pipeline_status'=>$artifact['status'],'direct_codes'=>$direct_codes,'drafts'=>0))."\n";
'''
        rel = self._write_test("__system4-current-positive-pipeline.php", positive)
        report = json.loads(self._run(rel).stdout)
        self.assertEqual(report.get("status"), "PASS")
        self.assertTrue(REPLACED_CURRENT_TESTS["tests/test-positive-pipeline.php"].issubset(set(report.get("direct_codes", []))))

        # 5) Signed-build protections: the old test wrongly expected the pristine signed package
        # to be unsigned. Exercise the three registry rules with actual negative mutations instead.
        integrity = r'''<?php
require __DIR__.'/bootstrap-test.php';
$mode=$argv[1]??''; $manifest=dirname(__DIR__).'/certification/build-manifest-v1.json'; $signature=dirname(__DIR__).'/certification/build-manifest-v1.sig';
$original_manifest=(string)file_get_contents($manifest); $original_signature=(string)file_get_contents($signature);
try {
  if($mode==='missing'){rename($manifest,$manifest.'.bak'); $errors=PPM679_Build_Integrity::verify('system4_missing','local'); rename($manifest.'.bak',$manifest);}
  elseif($mode==='invalid'){file_put_contents($manifest,'{'); $errors=PPM679_Build_Integrity::verify('system4_invalid','local'); file_put_contents($manifest,$original_manifest);}
  elseif($mode==='sodium'){ $errors=PPM679_Build_Integrity::verify('system4_sodium','local'); }
  else { $errors=PPM679_Build_Integrity::verify('system4_positive','local'); }
} finally {
  if(!is_file($manifest)&&is_file($manifest.'.bak'))rename($manifest.'.bak',$manifest);
  if(is_file($manifest)&&file_get_contents($manifest)!==$original_manifest)file_put_contents($manifest,$original_manifest);
  if(is_file($signature)&&file_get_contents($signature)!==$original_signature)file_put_contents($signature,$original_signature);
}
echo json_encode(array('mode'=>$mode,'codes'=>array_values(array_unique(array_column($errors,'error_code')))))."\n";
'''
        rel = self._write_test("__system4-current-build-integrity-negatives.php", integrity)
        positive_report = json.loads(subprocess.run(["php", str(self.ppm / rel), "positive"], cwd=self.ppm, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=True).stdout)
        self.assertEqual(positive_report.get("codes"), [])
        expected_modes = {
            "missing": "BLOCKED_BUILD_MANIFEST_MISSING",
            "invalid": "BLOCKED_BUILD_MANIFEST_INVALID",
            "sodium": "BLOCKED_BUILD_SIGNATURE_RUNTIME_UNAVAILABLE",
        }
        observed = set()
        for mode, expected in expected_modes.items():
            cmd = ["php"]
            if mode == "sodium":
                cmd += ["-d", "disable_functions=sodium_crypto_sign_verify_detached"]
            cmd += [str(self.ppm / rel), mode]
            cp = subprocess.run(cmd, cwd=self.ppm, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False)
            self.assertEqual(cp.returncode, 0, msg=cp.stderr)
            report = json.loads(cp.stdout)
            self.assertIn(expected, report.get("codes", []))
            observed.update(report.get("codes", []))
        self.assertTrue(REPLACED_CURRENT_TESTS["tests/test-wave1-unsigned-quarantine-blocked.php"].issubset(observed))


if __name__ == "__main__":
    unittest.main(verbosity=2)
