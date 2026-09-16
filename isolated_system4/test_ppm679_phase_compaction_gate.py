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

OLD_THREE_TYPE_LIVE_TESTS = {
    f"tests/three-type-live-test-release/test-{i:02d}-{name}.php"
    for i, name in [
        (1, "release-positive"), (2, "release-negative"), (3, "inventory-exact"),
        (4, "inventory-mismatch-blocks"), (5, "category-resolution"), (6, "category-negative"),
        (7, "bundled-simulation-success"), (8, "authorization-one-use"),
        (9, "foreign-collision-blocks-all"), (10, "partial-session-rollback"),
        (11, "entrypoint-authorization-negative"), (12, "static-boundaries"),
        (13, "readback-negative"), (14, "live-state-scope-routing"),
        (15, "inventory-lost-ids-not-current"), (16, "plan-fingerprint-negative"),
    ]
}

CURRENT_NORMAL_DRAFT_TESTS = {
    "tests/normal-draft-production/test-01-positive-1-to-4.php",
    "tests/normal-draft-production/test-02-cardinality-types-negative.php",
    "tests/normal-draft-production/test-03-identity-replay-negative.php",
    "tests/normal-draft-production/test-04-content-source-link-negative.php",
    "tests/normal-draft-production/test-05-readback-auth-static.php",
    "tests/normal-draft-production/test-normal-draft-journal-scope-isolation.php",
}

PHP_PROBE = r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
function acodes($artifact){$o=[];foreach((array)($artifact['errors']??[]) as $e){$c=(string)($e['error_code']??'');if($c!==''&&!in_array($c,$o,true))$o[]=$c;}return $o;}
$out=[];
nd_reset();$p=nd_build_plan(4,'scope');$rt=nd_runtime($p,'scope');$scope=PPM679_Normal_Draft_Release_Validator::expected_scope($p,$rt);$e=PPM679_Normal_Draft_Release_Validator::validate('normal_plan_preflight','',$scope);ppm_test_assert($e===[],'normal scope positive');$bad=$scope;$bad['maximum_articles']=3;$e=PPM679_Normal_Draft_Release_Validator::validate('normal_plan_preflight','',$bad);ppm_test_assert(in_array('BLOCKED_NORMAL_RELEASE_SCOPE_MISMATCH',array_column($e,'error_code'),true),'normal scope mutation blocks');$out['scope']=true;
nd_reset();$p=nd_build_plan(1,'unrelated');PPM679_WP::seed_test_post(['ID'=>21001,'post_title'=>'Unrelated old','post_name'=>'unrelated-old','post_status'=>'publish','post_type'=>'post','post_content'=>'old','meta'=>[],'category_ids'=>[]]);$r=PPM679_Normal_Draft_Pipeline::execute_plan($p,nd_runtime($p,'unrelated'));ppm_test_assert(strpos((string)($r['artifact']['status']??''),'NORMAL_DRAFT_END_TO_END')===0,'unrelated inventory allowed');$out['unrelated_inventory']=true;
nd_reset();$p=nd_build_plan(1,'dup-canon');$it=$p['items'][0];PPM679_WP::seed_test_post(['ID'=>21002,'post_title'=>'X','post_name'=>'x','post_status'=>'publish','post_type'=>'post','post_content'=>'old','meta'=>['_ppm679_canonical_article_id'=>$it['canonical_article_id']],'category_ids'=>[]]);$r=PPM679_Normal_Draft_Pipeline::execute_plan($p,nd_runtime($p,'dup-canon'));ppm_test_assert(strpos((string)($r['artifact']['status']??''),'BLOCKED_')===0&&count(PPM679_WP::test_posts())===1,'canonical collision blocks before new write');$out['canonical_collision']=acodes($r['artifact']);
nd_reset();$p=nd_build_plan(1,'dup-slug');$it=$p['items'][0];PPM679_WP::seed_test_post(['ID'=>21003,'post_title'=>'X','post_name'=>$it['canonical_article']['slug'],'post_status'=>'publish','post_type'=>'post','post_content'=>'old','meta'=>[],'category_ids'=>[]]);$r=PPM679_Normal_Draft_Pipeline::execute_plan($p,nd_runtime($p,'dup-slug'));ppm_test_assert(in_array('BLOCKED_NORMAL_DRAFT_SLUG_DUPLICATE',acodes($r['artifact']),true)&&count(PPM679_WP::test_posts())===1,'slug collision blocks before new write');$out['slug_collision']=true;
nd_reset();$p=nd_build_plan(1,'dup-title');$it=$p['items'][0];PPM679_WP::seed_test_post(['ID'=>21004,'post_title'=>$it['canonical_article']['title'],'post_name'=>'other-slug','post_status'=>'publish','post_type'=>'post','post_content'=>'old','meta'=>[],'category_ids'=>[]]);$r=PPM679_Normal_Draft_Pipeline::execute_plan($p,nd_runtime($p,'dup-title'));ppm_test_assert(strpos((string)($r['artifact']['status']??''),'BLOCKED_')===0&&count(PPM679_WP::test_posts())===1,'title collision blocks before new write');$out['title_collision']=acodes($r['artifact']);
nd_reset();$p=nd_build_plan(1,'cat');$item=$p['items'][0];$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);$g=PPM679_Content_Generator::generate($item,$pack);$ev=PPM679_Content_Validator::check($g,$item,'cat-prep','x');PPM679_WP::reset_test_state();$prep=PPM679_Normal_Draft_Adapter::prepare($g,$item,['technical_status'=>$ev['technical_status'],'content_quality_status'=>$ev['content_quality_status'],'content_hash'=>$ev['content_hash']],nd_runtime($p,'cat'),'run-x',PPM679_Diagnostic::stable_hash($p),'x');ppm_test_assert(empty($prep['ok'])&&in_array('BLOCKED_NORMAL_DRAFT_CATEGORY_RESOLUTION',array_column($prep['errors'],'error_code'),true),'missing category blocked');$out['category_missing']=true;
nd_reset();$p=nd_build_plan(1,'auth');$item=$p['items'][0];$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);$g=PPM679_Content_Generator::generate($item,$pack);$ev=PPM679_Content_Validator::check($g,$item,'auth-prep','x');$prep=PPM679_Normal_Draft_Adapter::prepare($g,$item,['technical_status'=>$ev['technical_status'],'content_quality_status'=>$ev['content_quality_status'],'content_hash'=>$ev['content_hash']],nd_runtime($p,'auth'),'run-x',PPM679_Diagnostic::stable_hash($p),'x');ppm_test_assert(!empty($prep['ok']),'prepare auth');$a=PPM679_Normal_Draft_Adapter::issue_write_authorization($prep);$mut=$prep['payload'];$mut['meta']['_ppm679_planned_write_fingerprint']='tampered';ppm_test_assert(!PPM679_Normal_Draft_Adapter::verify_write_authorization($a['authorization'],$mut,true),'payload/fingerprint tamper rejected');ppm_test_assert(PPM679_Normal_Draft_Adapter::verify_write_authorization($a['authorization'],$prep['payload'],true),'original auth first use');ppm_test_assert(!PPM679_Normal_Draft_Adapter::verify_write_authorization($a['authorization'],$prep['payload'],true),'auth replay rejected');$out['authorization_fingerprint']=true;
$write=PPM679_Normal_Draft_Adapter::create_draft($prep);ppm_test_assert(!empty($write['ok']),'write for readback');$snap=PPM679_WP::get_post_snapshot($write['post_id']);$bad=$snap;$bad['post_content'].=' MUTATION';$v=PPM679_Normal_Draft_Readback_Validator::validate_batch([$bad],[$prep['expected']],1);ppm_test_assert(empty($v['ok']),'content mutation rejected');$bad=$snap;$bad['post_status']='publish';$v=PPM679_Normal_Draft_Readback_Validator::validate_batch([$bad],[$prep['expected']],1);ppm_test_assert(empty($v['ok']),'publish mutation rejected');$out['readback']=true;
nd_reset();PPM679_WP::seed_test_post(['ID'=>22001,'post_title'=>'A','post_status'=>'draft','post_type'=>'post','post_name'=>'a','meta'=>[],'category_ids'=>[]]);PPM679_WP::seed_test_post(['ID'=>22002,'post_title'=>'B','post_status'=>'draft','post_type'=>'post','post_name'=>'b','meta'=>[],'category_ids'=>[]]);$rm=new ReflectionMethod('PPM679_Normal_Draft_Pipeline','abort_run');$rm->setAccessible(true);$report=PPM679_Diagnostic::blocked('X',[],'probe','');$gate=['state'=>['server_state_hash'=>'']];$rm->invoke(null,'missing-run',$report,$gate,[22001,22002]);ppm_test_assert(PPM679_WP::get_post_snapshot(22001)===null&&PPM679_WP::get_post_snapshot(22002)===null,'rollback deletes owned posts');$out['rollback']=true;
$adapter=file_get_contents(PPM679_PLUGIN_DIR.'includes/normal-draft-adapter.php');foreach(['nonce_verified','user_triggered','current_user_can_manage'] as $needle)ppm_test_assert(strpos($adapter,$needle)!==false,$needle.' remains enforced');
echo json_encode(['status'=>'PASS_CURRENT_NORMAL_DRAFT_REPLACES_THREE_TYPE_LIVE_PHASE','checks'=>$out],JSON_UNESCAPED_SLASHES)."\n";
'''


class Ppm679PhaseCompactionGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(__file__).resolve().parent.parent
        self.package = self.repo / PACKAGE_REL
        self.assertTrue(self.package.is_file())
        self.assertEqual(hashlib.sha256(self.package.read_bytes()).hexdigest(), PACKAGE_SHA256)
        self.tmp = tempfile.TemporaryDirectory(prefix="ppm679-phase-compaction-")
        self.root = Path(self.tmp.name)
        with zipfile.ZipFile(self.package) as zf:
            zf.extractall(self.root)
        self.ppm = self.root / "portal-production-machine"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_three_type_live_phase_is_replaced_by_current_normal_draft_protections(self) -> None:
        old = json.loads((self.ppm / "contracts/three-type-bundled-live-test-release-v1.json").read_text(encoding="utf-8"))
        current = json.loads((self.ppm / "contracts/normal-draft-release-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(old["created_at"][:10], "2026-07-29")
        self.assertEqual(old["scope_mode"], "THREE_TYPE_BUNDLED_SINGLE_SESSION_MAX_THREE_DRAFTS")
        self.assertFalse(old["global_production_release_allowed"])
        self.assertEqual(current["created_at"][:10], "2026-07-31")
        self.assertEqual(current["scope_mode"], "REUSABLE_NORMAL_DRAFT_1_TO_4")
        self.assertTrue({"FAQ", "Beratung", "Vergleich", "Pflege"}.issubset(set(current["allowed_article_types"])))
        self.assertFalse(current["publish_allowed"])

        test_files = {p.relative_to(self.ppm).as_posix() for p in (self.ppm / "tests").rglob("test-*.php")}
        self.assertTrue(OLD_THREE_TYPE_LIVE_TESTS.issubset(test_files))
        self.assertTrue(CURRENT_NORMAL_DRAFT_TESTS.issubset(test_files))

        probe = self.ppm / "__system4-current-normal-draft-compaction.php"
        probe.write_text(PHP_PROBE, encoding="utf-8")
        cp = subprocess.run(["php", str(probe)], cwd=self.ppm, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False)
        self.assertEqual(cp.returncode, 0, msg=f"STDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}")
        report = json.loads(cp.stdout)
        self.assertEqual(report.get("status"), "PASS_CURRENT_NORMAL_DRAFT_REPLACES_THREE_TYPE_LIVE_PHASE")
        self.assertEqual(set(report.get("checks", {})), {"scope", "unrelated_inventory", "canonical_collision", "slug_collision", "title_collision", "category_missing", "authorization_fingerprint", "readback", "rollback"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
