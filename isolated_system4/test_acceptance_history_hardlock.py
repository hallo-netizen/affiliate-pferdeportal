from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
WORKFLOW = REPO / '.github/workflows/system4a-real-acceptance.yml'


def text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


class AcceptanceHistoryHardlockTests(unittest.TestCase):
    """Permanent machine assertions for failures that previously invalidated the test route.

    This is not a second workflow. It only refuses to let the existing acceptance workflow
    lose already-required stations, freshness, real checkers, repair returns, or 1..N output.
    """

    def test_no_old_article_or_candidate_can_feed_active_input_factory(self):
        src = text(HERE / 'test_route_input_factory.py')
        for forbidden in (
            'g9-single-faq-approved-candidate-v1.json',
            'full_local_acceptance',
            'recovery_sources/',
            'FIRST_FULL_RULE_TEST_ARTICLE_PROOF',
            'LIVE_BOUND_INPUT_ONE_ARTICLE',
        ):
            self.assertNotIn(forbidden, src)
        self.assertIn('SYSTEM4_FRESH_RUN_TOKEN_REQUIRED', src)
        self.assertIn("'old_article_body_used': False", src)
        self.assertIn("'g9_candidate_used': False", src)

    def test_each_acceptance_run_is_machine_bound_to_new_article_sources(self):
        factory = text(HERE / 'test_route_input_factory.py')
        route = text(HERE / 'live_parity_v2.py')
        for needle in (
            'SYSTEM4_FRESH_RUN_TOKEN',
            'fresh_run_token_sha256',
            'SYSTEM4_FRESH_ARTICLE_INPUT_V1',
            'source_freshness',
        ):
            self.assertIn(needle, factory)
        for needle in (
            'SYSTEM4_FRESH_RUN_TOKEN',
            'SYSTEM4_HISTORICAL_ARTICLE_BODY_REUSED',
            'SYSTEM4_HISTORICAL_VISIBLE_ARTICLE_REUSED',
            'SYSTEM4_CURRENT_RUN_SOURCE_TRACE_MISSING',
            'SYSTEM4_CURRENT_BATCH_DRAFT_HASH_COLLISION',
            'SYSTEM4_CURRENT_BATCH_VISIBLE_ARTICLE_COLLISION',
        ):
            self.assertIn(needle, route)

    def test_point0_root_supervisor_dispatch_cannot_be_skipped(self):
        route = text(HERE / 'live_parity_v2.py')
        controller = text(HERE / 'controller.py')
        self.assertIn("'start-point0'", route)
        self.assertIn("'worker_dispatch.json'", controller)
        self.assertIn("'root_receipt.json'", controller)
        self.assertIn("'supervisor_state.json'", controller)
        self.assertIn('MACHINE_ROUTE_BLOCK', controller)
        self.assertLess(route.index("'start-point0'"), route.index("'research'"))

    def test_full_textmachine_components_are_not_optional_in_fullcheck(self):
        controller = text(HERE / 'controller.py')
        engine = text(HERE / 'production_checks_engine.py')
        for needle in (
            'authoring_contract.validate_bound',
            'content_guard.validate_single_article',
            'design_guard.validate_design_neutrality',
            'production_checks.run_all',
        ):
            self.assertIn(needle, controller)
        for needle in (
            'LANGUAGETOOL',
            'PPM679',
        ):
            self.assertIn(needle, engine)

    def test_repairable_errors_must_return_to_owner_not_conflict_block(self):
        controller = text(HERE / 'controller.py')
        self.assertNotIn("raise Fail('REPAIR_OWNER_CONFLICT", controller)
        self.assertIn('MULTI_OWNER_RETURN', controller)
        self.assertRegex(controller, r"s\['checks'\]\['return_required'\]\s*=\s*True")
        self.assertRegex(controller, r"s\['checks'\]\['return_route'\]\s*=\s*PARENT_LAUNCH")
        self.assertIn('SYSTEM4_STAGE_OWNER_RETURN', controller)
        self.assertIn('SYSTEM4_REPAIR_OWNER_RETURN', controller)

        # Worker-owned upstream findings must stay inside the same article/workspace:
        # rollback to the earliest responsible producer, invalidate downstream proof,
        # re-enter that phase, and fail closed after a bounded number of attempts.
        for needle in (
            "ROUTE_CONTRACT = 'SYSTEM4_CANONICAL_ARTICLE_ROUTE_V1'",
            'ARTICLE_ROUTE = (',
            'MAX_UPSTREAM_REPAIR_RETURNS = 2',
            'def _rollback_upstream_worker(',
            "raise Fail('REPAIR_RETURN_LIMIT_EXHAUSTED:' + target)",
            "raise Fail('REPAIR_RETURN_SAME_ARTICLE_VIOLATION')",
            "state['route_progress'] = list(CANONICAL_COMPLETION_TRACE[:target_index])",
            "state['phase'] = target_phase",
            'SYSTEM4_CONTROLLED_REPAIR_RETURN:',
            'repaired_owner = _rollback_upstream_worker(s, p, owners, error)',
        ):
            self.assertIn(needle, controller)

    def test_same_checker_is_mandatory_after_draft_repair(self):
        route = text(HERE / 'live_parity_v2.py')
        engine = text(HERE / 'controller_engine.py')
        self.assertIn("s['phase']='CHECK_REQUIRED'", engine)
        self.assertIn("if phase=='CHECK_REQUIRED'", route)
        self.assertIn("if phase=='REPAIR_REQUIRED'", route)
        self.assertIn("'fullcheck'", route)
        self.assertIn('REPAIR_DRAFT_UNCHANGED', engine)

    def test_batch_handoff_and_output_remain_one_to_n(self):
        route = text(HERE / 'live_parity_v2.py')
        delivery = text(REPO / 'control/startmaster0107/chat_delivery_payload.py')
        final_release = text(REPO / 'control/startmaster0107/GITHUB_FINAL_RELEASE.py')
        self.assertIn("'batch_gate.py','collect'", route)
        self.assertIn("'handoff_transport.py','validate'", route)
        self.assertIn('INLINE_RECONSTRUCTION_NOT_BYTE_EQUAL', route)
        self.assertIn('count = len(articles)', delivery)
        self.assertRegex(delivery, r'count\s*<\s*1')
        self.assertIn('"item_count": count', delivery)
        self.assertIn('"article_count": count', delivery)
        for fixed in (
            r'len\(articles\)\s*!=\s*7',
            r'len\(articles\)\s*==\s*7',
            r'["\']item_count["\']\s*:\s*7',
            r'["\']article_count["\']\s*:\s*7',
        ):
            self.assertNotRegex(delivery, fixed)
        self.assertIn('IMPORT_ENVELOPE', final_release)

    def test_acceptance_workflow_has_no_codex_and_must_run_full_rule_matrix_first(self):
        workflow = text(WORKFLOW)
        # Search only executable YAML uses-lines. The workflow deliberately contains a
        # grep string proving that such a line is absent; that string is not an action.
        self.assertIsNone(re.search(r'^\s*-\s*uses:\s*openai/codex-action@', workflow, re.MULTILINE))
        self.assertIn('SYSTEM4_FRESH_RUN_TOKEN', workflow)
        matrix = 'Run immutable Textmaschine and historical negative matrix'
        one = 'Build fresh machine inputs for one article'
        self.assertIn(matrix, workflow)
        self.assertIn(one, workflow)
        self.assertLess(workflow.index(matrix), workflow.index(one))

        required_tests = (
            'test_acceptance_history_hardlock.py',
            'test_machine_route_lock_contract.py',
            'test_point0_v2.Point0V2Tests.',
            'test_root_entry.py',
            'test_source_acquisition_owner_contract.py',
            'test_indexed_ingress.py',
            'test_content_guard.py',
            'test_context_required_regression.py',
            'test_design_guard.py',
            'test_draft_bound_rebind.py',
            'test_repair_continuity.py',
            'test_repair_owner_routing_contract.py',
            'test_repair_owner_failclosed_contract.py',
            'test_stage_owner_return_contract.py',
            'test_parent_title_repair_contract.py',
            'test_parent_metadata_owner_authority_contract.py',
            'test_batch_gate.py',
            'test_universal_batch_gate.py',
            'test_handoff_transport.py',
        )
        for required in required_tests:
            self.assertIn(required, workflow, required + ' missing from permanent acceptance matrix')

        point0_methods = (
            'test_source_acquisition_200_401_403',
            'test_chat_start_required_tamper_and_dataforseo_blocked',
            'test_point0_and_prewrite_tamper_fail_closed',
        )
        for method in point0_methods:
            exact = 'test_point0_v2.Point0V2Tests.' + method
            self.assertIn(exact, workflow, exact + ' missing from permanent Point0 matrix')

    def test_m15_m38_are_bound_to_current_system4_route(self):
        matrix = text(REPO / 'control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md')
        for number in range(15, 39):
            self.assertIn('M' + str(number).zfill(2), matrix)
        step = json.loads(text(REPO / 'control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json'))['instruction']
        for token in (
            'parent_start.py start-current',
            'machine_point0.py build-current-fetch',
            'system4_107007_batch.py start',
            'root_entry.py start-point0',
            'SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY',
            'Ein automatischer Aufruf von codex_entry.py worker-start ist verboten.',
            'controller.py repair',
            'controller.py fullcheck',
            'batch_gate.py collect',
        ):
            self.assertIn(token, step)
        self.assertIn('VERBOTEN für 107007-Repair', step)
        batch = text(REPO / 'control/startmaster0107/system4_107007_batch.py')
        self.assertIn('for key in ("title", "target_keyword", "category", "article_type", "plan_slot")', batch)
        dispatch = text(HERE / 'worker_dispatch.py')
        codex = text(HERE / 'codex_entry.py')
        self.assertIn("wc.get('contract')!='SYSTEM4_CODEX_WORKER_DISPATCH_V2'", dispatch)
        self.assertIn("worker_dispatch.verify_bundle", codex)
        self.assertIn("'worker-start'", codex)
        engine = text(HERE / 'production_checks_engine.py')
        self.assertIn('PPM_VERSION = "6.7.9"', engine)
        self.assertIn('PPM679_PACKAGE_HASH_MISMATCH', engine)
        gate = text(HERE / 'batch_gate.py')
        self.assertIn("state.get('article') != dict(expected_article)", gate)
        self.assertIn('PRODUCTION_CONTEXT_HASH_INVALID', gate)
        current = json.loads(text(REPO / 'control/startmaster0107/CURRENT_STATE.json'))
        self.assertEqual(current['m38_product_fix']['plan_contract_version'], '4.0.0')
        self.assertEqual(current['m38_product_fix']['required_plugin_version'], '6.7.9')
        repair_test = subprocess.run(
            ['python3', str(REPO / 'control/startmaster0107/test_system4_107007_repair_authority.py')],
            cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False,
        )
        self.assertEqual(repair_test.returncode, 0, repair_test.stdout + '\n' + repair_test.stderr)

    def test_historical_regression_contract_remains_bound(self):
        protocol = text(HERE / 'PROTOKOLL_TESTSTRECKE_V2_20260914.md')
        permanent = (
            'fehlende Manifestbindung',
            'leerer Quellenpool',
            'falscher Source-Hash',
            'HTTP 401',
            'HTTP 403',
            'falscher Head',
            'Point-0-Tamper',
            'Workspace im Repo',
            'nichtleerer Workspace',
            'fehlender Dispatch',
            'Dispatch-Tamper',
            'freie Webfreigabe',
            'Änderung gebundener Quellenbytes',
            'ungebundene Research-Daten',
            'Fact-Quelle außerhalb Research',
            'Evidenz nicht in Quelle',
            'unbekannter PPM-Vertrag',
            'Wortminimum',
            'Inline-Designmutation',
            'externer Link',
            'unbekannte Fact-ID',
            'zu großer Same-Article-Repair',
            'Cross-Item-Research',
            'Prewrite-Byte-Tamper',
            'rehashter Linktausch',
            'Runtime-Linktausch',
            'Kategorieänderung',
            'Artikelindex/Pool/Slot-Verwechslung',
            'Source-Acquisition 200/401/403',
            'Repair ohne erneuten echten Prüferlauf',
            'Repair mit Überspringen eines späteren Prüfers',
        )
        for item in permanent:
            self.assertIn(item, protocol)

    def test_hr_proc_002_g9_write_authorization_is_individually_effective(self):
        'HR-PROC-002 explicit G9 write authorization must be effect-sensitive.'
        package = REPO / 'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
        self.assertTrue(package.is_file())
        with tempfile.TemporaryDirectory(prefix='system4-hr-proc-002-') as td:
            root = Path(td)
            with zipfile.ZipFile(package) as zf:
                zf.extractall(root)
            ppm = root / 'portal-production-machine'
            source = ppm / 'includes/g9-single-faq-entrypoint.php'
            original = source.read_text(encoding='utf-8')

            def run(rel: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ['php', str(ppm / rel)], cwd=ppm, text=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False,
                )

            positive = run('tests/g9-single-faq-entrypoint/test-g9-entrypoint-positive.php')
            self.assertEqual(positive.returncode, 0, positive.stderr)
            self.assertEqual(json.loads(positive.stdout).get('status'), 'PASS')

            probe = ppm / 'tests/__system4_hr_proc_002.php'
            probe.write_text(r'''<?php
require_once __DIR__.'/bootstrap-test.php';
function s4_run($name,$override,$expected_status){
  PPM679_WP::reset_test_state(); PPM679_Storage::reset_test_state();
  $base=array(
    'user_triggered'=>true,
    'nonce_verified'=>true,
    'current_user_can_manage'=>true,
    'declared_contract'=>PPM679_G9_Single_FAQ_Entrypoint::CONTRACT,
    'declared_plan_item_key'=>PPM679_G9_Single_FAQ_Entrypoint::PLAN_ITEM_KEY,
    'simulation_only'=>true,
    'evidence_class'=>'LOCAL_EXECUTED_TEST'
  );
  $r=PPM679_G9_Single_FAQ_Entrypoint::execute(array_merge($base,$override));
  ppm_test_assert(empty($r['ok']),$name.' must block');
  ppm_test_assert((string)$r['status']===$expected_status,$name.' must return exact '.$expected_status);
  ppm_test_assert(count(PPM679_WP::test_posts())===0,$name.' must create zero drafts');
  return (string)$r['status'];
}
$out=array();
$out['missing_user_trigger']=s4_run('missing_user_trigger',array('user_triggered'=>false),'BLOCKED_G9_NOT_USER_TRIGGERED');
$out['missing_nonce']=s4_run('missing_nonce',array('nonce_verified'=>false),'BLOCKED_G9_NONCE');
$out['missing_capability']=s4_run('missing_capability',array('current_user_can_manage'=>false),'BLOCKED_G9_CAPABILITY');
$out['wrong_entry_binding']=s4_run('wrong_entry_binding',array('declared_plan_item_key'=>'other'),'BLOCKED_G9_EXACT_ENTRY_BINDING');
echo json_encode(array('status'=>'PASS_HR_PROC_002','cases'=>$out,'drafts_created'=>0),JSON_UNESCAPED_SLASHES)."\n";
?>''', encoding='utf-8')
            baseline = run('tests/__system4_hr_proc_002.php')
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            self.assertEqual(json.loads(baseline.stdout).get('status'), 'PASS_HR_PROC_002')

            mutations = (
                ("if (($context['user_triggered']??false)!==true) {", "if (false) {"),
                ("if (($context['nonce_verified']??false)!==true) {", "if (false) {"),
                ("if (($context['current_user_can_manage']??false)!==true) {", "if (false) {"),
                ("if (($context['declared_contract']??self::CONTRACT)!==self::CONTRACT || ($context['declared_plan_item_key']??self::PLAN_ITEM_KEY)!==self::PLAN_ITEM_KEY) {", "if (false) {"),
            )
            for old, new in mutations:
                self.assertEqual(original.count(old), 1, old)
                source.write_text(original.replace(old, new, 1), encoding='utf-8')
                killed = run('tests/__system4_hr_proc_002.php')
                self.assertNotEqual(killed.returncode, 0, 'HR-PROC-002 mutation survived: ' + old)
                source.write_text(original, encoding='utf-8')

    def test_hr_cont_001_faq_title_and_body_h1_are_individually_effective(self):
        'HR-CONT-001 body-H1 and rendered single-title branches must be effect-sensitive.'
        package = REPO / 'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
        self.assertTrue(package.is_file())
        with tempfile.TemporaryDirectory(prefix='system4-hr-cont-001-') as td:
            root = Path(td)
            with zipfile.ZipFile(package) as zf:
                zf.extractall(root)
            ppm = root / 'portal-production-machine'

            def run(rel: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ['php', str(ppm / rel)], cwd=ppm, text=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False,
                )

            # Positive source and rendered controls.
            for rel in (
                'tests/test-g8-targeted-repair-faq-chain.php',
                'tests/qf03-wordpress-draft-readback-dom/test-qf03-rendered-dom-positive.php',
                'tests/test-wave1-known-error-mutations.php',
                'tests/test-wave2-content-mutations.php',
            ):
                cp = run(rel)
                self.assertEqual(cp.returncode, 0, rel + '\n' + cp.stderr)

            # Existing source/body-H1 negatives must die when their exact real branch is disabled.
            source_mutations = (
                ('includes/known-error-gate.php', 'if ($h1_count>0) {', 'tests/test-wave1-known-error-mutations.php'),
                ('includes/content-structure-language-gate.php', 'if ($h1!==0) {', 'tests/test-wave2-content-mutations.php'),
            )
            for rel_source, old, rel_test in source_mutations:
                source = ppm / rel_source
                original = source.read_text(encoding='utf-8')
                self.assertEqual(original.count(old), 1, old)
                source.write_text(original.replace(old, 'if (false) {', 1), encoding='utf-8')
                killed = run(rel_test)
                self.assertNotEqual(killed.returncode, 0, 'HR-CONT-001 source mutation survived: ' + rel_source)
                source.write_text(original, encoding='utf-8')

            # The historical rendered mutation test can stay green through redundant title checks.
            # Bind the exact H1-count rule by requiring its own error code for zero and two H1s.
            probe = ppm / 'tests/qf03-wordpress-draft-readback-dom/__system4_hr_cont_001.php'
            probe.write_text(r'''<?php
require_once dirname(__DIR__).'/bootstrap-test.php';
require_once __DIR__.'/fixture-builder.php';
$hash=hash('sha256',qf03_article_html());
$expected=array('title'=>'Was muss vor einer Fahrt geprüft werden?','post_id'=>101,'readback_content_hash'=>$hash);
$base_d=qf03_capture_fixture('desktop',101,$hash);
$base_m=qf03_capture_fixture('mobile',101,$hash);
function s4_h1_case($name,$d,$m,$expected){
  $r=PPM679_Rendered_DOM_Validator::validate_pair($d,$m,$expected);
  ppm_test_assert($r['ok']===false,$name.' must block');
  $codes=array_values(array_unique(array_map(fn($e)=>(string)($e['error_code']??''),(array)($r['report']['errors']??array()))));
  ppm_test_assert(in_array('BLOCKED_QF03_RENDERED_H1_COUNT',$codes,true),$name.' must expose exact H1-count blocker');
  return $codes;
}
$zd=$base_d; $zm=$base_m;
foreach(array(&$zd,&$zm) as &$x){$x['html']=str_replace('<h1>Was muss vor einer Fahrt geprüft werden?</h1>','',$x['html']);$x['html_sha256']=hash('sha256',$x['html']);}
unset($x);
$td=$base_d; $tm=$base_m;
foreach(array(&$td,&$tm) as &$x){$x['html']=str_replace('</h1>','</h1><h1>Was muss vor einer Fahrt geprüft werden?</h1>',$x['html']);$x['html_sha256']=hash('sha256',$x['html']);}
unset($x);
$out=array('zero_h1'=>s4_h1_case('zero_h1',$zd,$zm,$expected),'two_h1'=>s4_h1_case('two_h1',$td,$tm,$expected));
echo json_encode(array('status'=>'PASS_HR_CONT_001','cases'=>$out),JSON_UNESCAPED_SLASHES)."\n";
?>''', encoding='utf-8')
            baseline = run('tests/qf03-wordpress-draft-readback-dom/__system4_hr_cont_001.php')
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            self.assertEqual(json.loads(baseline.stdout).get('status'), 'PASS_HR_CONT_001')

            rendered = ppm / 'includes/rendered-dom-validator.php'
            original = rendered.read_text(encoding='utf-8')
            old = "if ($analysis['visible_h1_count']!==1) {"
            self.assertEqual(original.count(old), 1, old)
            rendered.write_text(original.replace(old, 'if (false) {', 1), encoding='utf-8')
            killed = run('tests/qf03-wordpress-draft-readback-dom/__system4_hr_cont_001.php')
            self.assertNotEqual(killed.returncode, 0, 'HR-CONT-001 rendered H1-count mutation survived')
            rendered.write_text(original, encoding='utf-8')


if __name__ == '__main__':
    unittest.main(verbosity=2)
