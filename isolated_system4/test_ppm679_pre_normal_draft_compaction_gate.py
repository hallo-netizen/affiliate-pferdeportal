from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

PACKAGE_REL = Path("control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip")
PACKAGE_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"

OLD_PRE_NORMAL_DRAFT_TESTS = {
    "tests/g9-single-faq-entrypoint/test-g9-entrypoint-static.php",
    "tests/qf03-wordpress-draft-readback-dom/test-qf03-real-write-boundary-static.php",
    "tests/v3-stateful-e2e/test-v31-s07-abort-before-write.php",
    "tests/v3-stateful-e2e/test-v31-s08-abort-after-write-before-readback.php",
    "tests/v3-stateful-e2e/test-v31-s11-target-type-status.php",
    "tests/v3-stateful-e2e/test-v31-s12-server-build-binding.php",
    "tests/v34-category-assignment/test-v34-g9-integration.php",
    "tests/v34-category-assignment/test-v34-governance-contract.php",
    "tests/v34-category-assignment/test-v34-invariance.php",
    "tests/v34-category-assignment/test-v34-production-plan-v5-category-binding.php",
    "tests/v34-category-assignment/test-v34-sensitivity.php",
    "tests/v34-category-assignment/test-v34-structure-firewall.php",
    "tests/v34-category-assignment/test-v34-too-narrow-plan-blocked.php",
    "tests/v36-portal-wp-architecture/test-v36-readback-separated-structure.php",
    "tests/v36-portal-wp-architecture/test-v36-wp-contract-unbound-hash.php",
}

CURRENT_REPLACEMENT_TESTS = {
    "tests/test-mainblock1-link-targets.php",
    "tests/test-build-integrity-only.php",
    "tests/normal-draft-production/test-01-positive-1-to-4.php",
    "tests/normal-draft-production/test-02-cardinality-types-negative.php",
    "tests/normal-draft-production/test-03-identity-replay-negative.php",
    "tests/normal-draft-production/test-04-content-source-link-negative.php",
    "tests/normal-draft-production/test-05-readback-auth-static.php",
    "tests/normal-draft-production/test-normal-draft-journal-scope-isolation.php",
    "tests/three-type-bundled-local/test-complete-category-source.php",
}

PHP_PROBE = r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
function codes($artifact){$o=[];foreach((array)($artifact['errors']??[]) as $e){$c=(string)($e['error_code']??'');if($c!==''&&!in_array($c,$o,true))$o[]=$c;}return $o;}
function blocked($artifact){return strpos((string)($artifact['status']??''),'BLOCKED_')===0;}
$out=[];

// Current route: bad server identity must stop before any new write.
nd_reset();$p=nd_build_plan(1,'compact-server');$rt=nd_runtime($p,'compact-server');$before=count(PPM679_WP::test_posts());$rt['server_instance_id']='wrong-server';$r=PPM679_Normal_Draft_Pipeline::execute_plan($p,$rt);ppm_test_assert(blocked($r['artifact']),'server identity mutation blocks');ppm_test_assert(count(PPM679_WP::test_posts())===$before,'server identity mutation writes nothing');$out['server_identity_prewrite']=codes($r['artifact']);

// Current route: invalid cardinality must stop before any new write.
nd_reset();$p=nd_build_plan(1,'compact-zero');$p['items']=[];$rt=nd_runtime($p,'compact-zero');$before=count(PPM679_WP::test_posts());$r=PPM679_Normal_Draft_Pipeline::execute_plan($p,$rt);ppm_test_assert(blocked($r['artifact']),'zero item plan blocks');ppm_test_assert(count(PPM679_WP::test_posts())===$before,'zero item plan writes nothing');$out['cardinality_prewrite']=codes($r['artifact']);

// Current route: contract-hash tampering must stop before any new write.
nd_reset();$p=nd_build_plan(1,'compact-hash');ppm_test_assert(!empty($p['contract_hashes'])&&is_array($p['contract_hashes']),'contract hashes present');$keys=array_keys($p['contract_hashes']);$p['contract_hashes'][$keys[0]]=str_repeat('0',64);$rt=nd_runtime($p,'compact-hash');$before=count(PPM679_WP::test_posts());$r=PPM679_Normal_Draft_Pipeline::execute_plan($p,$rt);ppm_test_assert(blocked($r['artifact']),'contract hash mutation blocks');ppm_test_assert(count(PPM679_WP::test_posts())===$before,'contract hash mutation writes nothing');$out['contract_hash_prewrite']=codes($r['artifact']);

// Current route: authorization is payload-bound and one-use.
nd_reset();$p=nd_build_plan(1,'compact-auth');$item=$p['items'][0];$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);$g=PPM679_Content_Generator::generate($item,$pack);$ev=PPM679_Content_Validator::check($g,$item,'compact-auth','x');$prep=PPM679_Normal_Draft_Adapter::prepare($g,$item,['technical_status'=>$ev['technical_status'],'content_quality_status'=>$ev['content_quality_status'],'content_hash'=>$ev['content_hash']],nd_runtime($p,'compact-auth'),'run-x',PPM679_Diagnostic::stable_hash($p),'x');ppm_test_assert(!empty($prep['ok']),'prepare authorization');$a=PPM679_Normal_Draft_Adapter::issue_write_authorization($prep);$mut=$prep['payload'];$mut['post_title'].=' tampered';ppm_test_assert(!PPM679_Normal_Draft_Adapter::verify_write_authorization($a['authorization'],$mut,true),'tampered payload rejected');ppm_test_assert(PPM679_Normal_Draft_Adapter::verify_write_authorization($a['authorization'],$prep['payload'],true),'original payload authorized once');ppm_test_assert(!PPM679_Normal_Draft_Adapter::verify_write_authorization($a['authorization'],$prep['payload'],true),'authorization replay rejected');$out['authorization_one_use']=true;

// Current route: readback must reject category and content/status mutations.
$write=PPM679_Normal_Draft_Adapter::create_draft($prep);ppm_test_assert(!empty($write['ok']),'write for readback probe');$snap=PPM679_WP::get_post_snapshot($write['post_id']);$bad=$snap;$bad['category_ids']=[999999];$v=PPM679_Normal_Draft_Readback_Validator::validate_batch([$bad],[$prep['expected']],1);ppm_test_assert(empty($v['ok']),'category readback mutation rejected');$bad=$snap;$bad['post_content'].=' MUTATION';$v=PPM679_Normal_Draft_Readback_Validator::validate_batch([$bad],[$prep['expected']],1);ppm_test_assert(empty($v['ok']),'content readback mutation rejected');$bad=$snap;$bad['post_status']='publish';$v=PPM679_Normal_Draft_Readback_Validator::validate_batch([$bad],[$prep['expected']],1);ppm_test_assert(empty($v['ok']),'status readback mutation rejected');$out['readback_category_content_status']=true;

// Current adapter must still verify authorization before the actual draft insert.
$adapter=(string)file_get_contents(PPM679_PLUGIN_DIR.'includes/normal-draft-adapter.php');$create=strpos($adapter,'function create_draft');ppm_test_assert($create!==false,'current create_draft exists');$tail=substr($adapter,$create);$verify=strpos($tail,'verify_write_authorization');$insert=strpos($tail,'insert_draft');ppm_test_assert($verify!==false&&$insert!==false&&$verify<$insert,'authorization verification precedes draft insert');foreach(['nonce_verified','user_triggered','current_user_can_manage'] as $needle)ppm_test_assert(strpos($adapter,$needle)!==false,$needle.' current boundary remains');$out['write_boundary_order']=true;

echo json_encode(['status'=>'PASS_PRE_NORMAL_DRAFT_REPLACED_BY_CURRENT_PROTECTIONS','checks'=>$out],JSON_UNESCAPED_SLASHES)."\n";
'''


class PreNormalDraftCompactionGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(__file__).resolve().parent.parent
        self.package = self.repo / PACKAGE_REL
        self.assertTrue(self.package.is_file())
        self.assertEqual(hashlib.sha256(self.package.read_bytes()).hexdigest(), PACKAGE_SHA256)
        self.tmp = tempfile.TemporaryDirectory(prefix="ppm679-pre-normal-compaction-")
        self.root = Path(self.tmp.name)
        with zipfile.ZipFile(self.package) as zf:
            zf.extractall(self.root)
        self.ppm = self.root / "portal-production-machine"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_old_shells_are_unbound_and_current_replacements_exist(self) -> None:
        tests = {p.relative_to(self.ppm).as_posix() for p in (self.ppm / "tests").rglob("test-*.php")}
        self.assertTrue(OLD_PRE_NORMAL_DRAFT_TESTS.issubset(tests))
        self.assertTrue(CURRENT_REPLACEMENT_TESTS.issubset(tests))
        registry = (self.ppm / "contracts/hard-rule-registry-v1.json").read_text(encoding="utf-8")
        for rel in OLD_PRE_NORMAL_DRAFT_TESTS:
            self.assertNotIn(rel, registry, msg=f"legacy shell is still registry-bound: {rel}")

        link_test = (self.ppm / "tests/test-mainblock1-link-targets.php").read_text(encoding="utf-8")
        self.assertIn("post_type", link_test)
        self.assertIn("post_status", link_test)
        category_test = (self.ppm / "tests/three-type-bundled-local/test-complete-category-source.php").read_text(encoding="utf-8")
        self.assertIn("1124", category_test)
        self.assertIn("779", category_test)
        integrity_test = (self.ppm / "tests/test-build-integrity-only.php").read_text(encoding="utf-8")
        self.assertTrue("sha256" in integrity_test.lower() or "hash" in integrity_test.lower())

    def test_current_normal_draft_runtime_replaces_the_old_safety_intent(self) -> None:
        probe = self.ppm / "__system4-pre-normal-compaction.php"
        probe.write_text(PHP_PROBE, encoding="utf-8")
        cp = subprocess.run(["php", str(probe)], cwd=self.ppm, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False)
        self.assertEqual(cp.returncode, 0, msg=f"STDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}")
        report = json.loads(cp.stdout)
        self.assertEqual(report.get("status"), "PASS_PRE_NORMAL_DRAFT_REPLACED_BY_CURRENT_PROTECTIONS")
        self.assertEqual(set(report.get("checks", {})), {
            "server_identity_prewrite", "cardinality_prewrite", "contract_hash_prewrite",
            "authorization_one_use", "readback_category_content_status", "write_boundary_order",
        })


if __name__ == "__main__":
    unittest.main(verbosity=2)
