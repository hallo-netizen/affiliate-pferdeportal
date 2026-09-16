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
function blocked($artifact){return strpos((string)($artifact['status']??''),'BLOCKED_')===0;}
function run_block_no_write($plan,$runtime,$label){$r=PPM679_Normal_Draft_Pipeline::execute_plan($plan,$runtime);ppm_test_assert(blocked($r['artifact']),$label.' must block');ppm_test_assert(count(PPM679_WP::test_posts())===0,$label.' must create no post');return (string)$r['artifact']['status'];}
$out=[];

nd_reset();$p=nd_build_plan(1,'compact-server');$rt=nd_runtime($p,'compact-server');$rt['server_instance_id']='wrong-server';$out['server_identity_prewrite']=run_block_no_write($p,$rt,'server identity mutation');
nd_reset();$p=nd_build_plan(1,'compact-build');$rt=nd_runtime($p,'compact-build');$rt['build_manifest_sha256']=str_repeat('0',64);$out['build_identity_prewrite']=run_block_no_write($p,$rt,'build identity mutation');
nd_reset();$p=nd_build_plan(1,'compact-zero');$p['items']=[];$out['cardinality_prewrite']=run_block_no_write($p,nd_runtime($p,'compact-zero'),'zero item plan');
nd_reset();$p=nd_build_plan(1,'compact-hash');$keys=array_keys($p['contract_hashes']);ppm_test_assert(count($keys)>0,'contract hashes present');$p['contract_hashes'][$keys[0]]=str_repeat('0',64);$out['contract_hash_prewrite']=run_block_no_write($p,nd_runtime($p,'compact-hash'),'contract hash mutation');

nd_reset();$c=json_decode((string)file_get_contents(PPM679_PLUGIN_DIR.'contracts/g9-single-faq-approved-candidate-v1.json'),true);$b=$c['item']['quality_binding'];$map=array('parent_category'=>array('id'=>101,'type'=>'page','status'=>'publish','parent_url'=>''),'semantic_related'=>array('id'=>102,'type'=>'page','status'=>'publish','parent_url'=>'https://pferde-atelier.de/transport/'),'further_information'=>array('id'=>103,'type'=>'page','status'=>'publish','parent_url'=>'https://pferde-atelier.de/transport/'));ppm_test_assert(!empty(PPM679_WordPress_Link_Target_Validator::revalidate_live_before_write($b,'compact-links',$map)['ok']),'valid link targets pass');$bad=$map;$bad['semantic_related']['type']='post';ppm_test_assert(empty(PPM679_WordPress_Link_Target_Validator::revalidate_live_before_write($b,'compact-links',$bad)['ok']),'post link target blocks');$bad=$map;$bad['semantic_related']['status']='draft';ppm_test_assert(empty(PPM679_WordPress_Link_Target_Validator::revalidate_live_before_write($b,'compact-links',$bad)['ok']),'non-published link target blocks');$bad=$map;$bad['further_information']['id']=0;ppm_test_assert(empty(PPM679_WordPress_Link_Target_Validator::revalidate_live_before_write($b,'compact-links',$bad)['ok']),'missing link target blocks');$out['link_target_type_status']=true;

nd_reset();$p=nd_build_plan(1,'compact-category');$cat=$p['items'][0]['quality_binding']['wordpress_category'];$good=PPM679_WP::resolve_category_binding($cat);ppm_test_assert(!empty($good['ok']),'current bound category resolves');$bad=$cat;$bad['slug']='definitely-missing-category';ppm_test_assert(empty(PPM679_WP::resolve_category_binding($bad)['ok']),'missing category blocks');$out['category_resolution']=true;

nd_reset();$p=nd_build_plan(1,'compact-auth');$item=$p['items'][0];$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);$g=PPM679_Content_Generator::generate($item,$pack);$ev=PPM679_Content_Validator::check($g,$item,'compact-auth','x');$prep=PPM679_Normal_Draft_Adapter::prepare($g,$item,['technical_status'=>$ev['technical_status'],'content_quality_status'=>$ev['content_quality_status'],'content_hash'=>$ev['content_hash']],nd_runtime($p,'compact-auth'),'run-x',PPM679_Diagnostic::stable_hash($p),'x');ppm_test_assert(!empty($prep['ok']),'prepare authorization');$a=PPM679_Normal_Draft_Adapter::issue_write_authorization($prep);$mut=$prep['payload'];$mut['title']=(string)$mut['title'].' tampered';ppm_test_assert(!PPM679_Normal_Draft_Adapter::verify_write_authorization($a['authorization'],$mut,true),'tampered payload rejected');ppm_test_assert(PPM679_Normal_Draft_Adapter::verify_write_authorization($a['authorization'],$prep['payload'],true),'original payload authorized once');ppm_test_assert(!PPM679_Normal_Draft_Adapter::verify_write_authorization($a['authorization'],$prep['payload'],true),'authorization replay rejected');ppm_test_assert(PPM679_WP::insert_draft('unauthorized','x','unauthorized',[],[],null)===0,'direct unauthorized write blocked');ppm_test_assert(count(PPM679_WP::test_posts())===0,'unauthorized write creates no post');$out['authorization_and_write_chokepoint']=true;

$write=PPM679_Normal_Draft_Adapter::create_draft($prep);ppm_test_assert(!empty($write['ok']),'authorized current draft write passes');ppm_test_assert(count(PPM679_WP::test_posts())===1,'exactly one authorized draft exists');$snap=PPM679_WP::get_post_snapshot($write['post_id']);ppm_test_assert(($snap['post_status']??'')==='draft'&&($snap['post_type']??'')==='post','authorized object is a draft post');$bad=$snap;$bad['category_ids']=[999999];ppm_test_assert(empty(PPM679_Normal_Draft_Readback_Validator::validate_batch([$bad],[$prep['expected']],1)['ok']),'category readback mutation rejected');$bad=$snap;$bad['post_content'].=' MUTATION';ppm_test_assert(empty(PPM679_Normal_Draft_Readback_Validator::validate_batch([$bad],[$prep['expected']],1)['ok']),'content readback mutation rejected');$bad=$snap;$bad['post_status']='publish';ppm_test_assert(empty(PPM679_Normal_Draft_Readback_Validator::validate_batch([$bad],[$prep['expected']],1)['ok']),'status readback mutation rejected');$out['readback_category_content_status']=true;

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

    def test_current_normal_draft_runtime_replaces_the_old_safety_intent(self) -> None:
        probe = self.ppm / "__system4-pre-normal-compaction.php"
        probe.write_text(PHP_PROBE, encoding="utf-8")
        cp = subprocess.run(["php", str(probe)], cwd=self.ppm, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False)
        self.assertEqual(cp.returncode, 0, msg=f"STDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}")
        report = json.loads(cp.stdout)
        self.assertEqual(report.get("status"), "PASS_PRE_NORMAL_DRAFT_REPLACED_BY_CURRENT_PROTECTIONS")
        self.assertEqual(set(report.get("checks", {})), {
            "server_identity_prewrite", "build_identity_prewrite", "cardinality_prewrite", "contract_hash_prewrite",
            "link_target_type_status", "category_resolution", "authorization_and_write_chokepoint",
            "readback_category_content_status",
        })


if __name__ == "__main__":
    unittest.main(verbosity=2)
