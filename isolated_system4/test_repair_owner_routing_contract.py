import json
import subprocess
import tempfile
import zipfile
import unittest
from pathlib import Path
from unittest import mock

import block_semantics
import controller
import production_checks


class RepairOwnerRoutingContractTests(unittest.TestCase):
    """Causal contract: repairability is a semantic owner decision, never a one-off symptom list."""

    def test_known_regression_pattern_is_not_allowed_to_fall_through_to_hard_block(self):
        payload = {
            'ok': False,
            'errors': [{
                'error_code': 'BLOCKED_KNOWN_REGRESSION_PATTERN',
                'failed_rule': 'known_regression_pattern',
                'field_path': 'canonical_article.body_html',
                'expected': 'no known regression pattern',
                'actual': 'known regression pattern present',
                'reason': 'article text is repairable by its producing worker',
                'validator_id': 'ppm679',
            }],
        }
        findings = production_checks._ppm_repair_findings(payload)
        self.assertTrue(findings, 'repairable PPM content finding fell through to terminal hard block')

    def test_unknown_ppm_blocker_remains_fail_closed(self):
        payload = {'ok': False, 'errors': [{'error_code': 'BLOCKED_FUTURE_UNKNOWN_FAILURE'}]}
        self.assertEqual(production_checks._ppm_repair_findings(payload), [])

    def test_integrity_and_execution_failures_are_not_reclassified_as_repair(self):
        hard_codes = [
            'PPM679_PACKAGE_HASH_MISMATCH',
            'PPM679_VALIDATOR_EXECUTION_FAILED',
            'PPM679_VALIDATOR_RESULT_INVALID',
            'PPM679_CONTENT_HASH_MISMATCH',
            'SYSTEM4_DRAFT_BINDING_INVALID',
        ]
        for code in hard_codes:
            with self.subTest(code=code):
                self.assertEqual(
                    production_checks._ppm_repair_findings({'errors': [{'error_code': code}]}),
                    [],
                    f'{code} must remain hard/fail-closed',
                )

    def test_repair_routing_contract_must_expose_owner_metadata(self):
        payload = {
            'errors': [{
                'error_code': 'BLOCKED_KNOWN_REGRESSION_PATTERN',
                'field_path': 'canonical_article.body_html',
                'failed_rule': 'known_regression_pattern',
            }]
        }
        findings = production_checks._ppm_repair_findings(payload)
        self.assertTrue(findings, 'repairable validator finding must exist')
        self.assertIn('repair_owner', findings[0], 'repair routing must name the producing owner, not only the symptom code')
        self.assertEqual(findings[0]['repair_owner'], 'DRAFT_WORKER')

    def test_repairable_family_is_classified_by_semantics_not_exact_single_code(self):
        variants = [
            ('BLOCKED_KNOWN_REGRESSION_PATTERN', 'canonical_article.body_html', 'DRAFT_WORKER'),
            ('BLOCKED_KNOWN_REGRESSION_PATTERN_REPEAT', '', 'DRAFT_WORKER'),
            ('BLOCKED_CONTENT_CONCLUSION_REQUIRED', 'canonical_article.body_html', 'DRAFT_WORKER'),
            ('BLOCKED_WAVE2_STRUCTURE_REQUIRED', 'canonical_article.body_html', 'DRAFT_WORKER'),
            ('BLOCKED_CANONICAL_RUNTIME_LINK_REQUIRED', 'canonical_article.link_binding', 'PORTAL_LINK_MACHINE'),
        ]
        for code, field_path, owner in variants:
            with self.subTest(code=code):
                findings = production_checks._ppm_repair_findings({'errors': [{'error_code': code, 'field_path': field_path}]})
                self.assertTrue(findings, f'{code} must route to repair owner instead of generic hard block')
                self.assertEqual(findings[0]['repair_owner'], owner)

    def test_owner_matrix_uses_artifact_semantics(self):
        cases = [
            ('canonical_article.body_html', 'DRAFT_WORKER'),
            ('canonical_article.title', 'PARENT_TITLE_MACHINE'),
            ('quality_binding.wordpress_category.slug', 'PARENT_CATEGORY_MACHINE'),
            ('canonical_article.article_type', 'PARENT_ARTICLE_TYPE_MACHINE'),
            ('production_plan.target_keyword', 'PARENT_KEYWORD_MACHINE'),
            ('production_plan.slot', 'PARENT_SLOT_MACHINE'),
            ('canonical_article.link_binding.href', 'PORTAL_LINK_MACHINE'),
            ('production_context.fact_pack.claims', 'CONTEXT_WORKER'),
        ]
        for field_path, owner in cases:
            with self.subTest(field_path=field_path):
                findings = production_checks._ppm_repair_findings({
                    'errors': [{
                        'error_code': 'BLOCKED_CONTENT_FIELD_INVALID',
                        'field_path': field_path,
                    }]
                })
                self.assertTrue(findings)
                self.assertEqual(findings[0]['repair_owner'], owner)

    @staticmethod
    def _minimal_state():
        return {
            'phase': 'CHECK_REQUIRED',
            'production_context': {'fact_pack': {}, 'production_plan_item': {}},
            'article': {'article_type': 'Beratung'},
            'draft_markdown': '<article><p>Test</p></article>',
            'draft_sha256': 'deadbeef',
            'checks': {},
            'last_error': None,
        }

    def _run_controller_repair_finding(self, finding):
        state = self._minimal_state()
        fake_path = Path('/tmp/system4-owner-contract-state.json')
        repair = production_checks.RepairRequired('ppm679', [finding])
        with mock.patch.object(controller, 'load', return_value=(state, fake_path)), \
             mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={}), \
             mock.patch.object(controller.content_guard, 'validate_single_article', return_value=None), \
             mock.patch.object(controller.design_guard, 'validate_design_neutrality', return_value=None), \
             mock.patch.object(controller.production_checks, 'run_all', side_effect=repair), \
             mock.patch.object(controller._engine, 'save', return_value=None):
            rc = controller.cmd_fullcheck('/tmp/irrelevant')
        return rc, state

    @staticmethod
    def _semantic_contract():
        structure = {'headings': {'reserved_headings': ['Fazit', 'Weiterführende Informationen']}}
        type_def = {'required_blocks': ['intro', 'body', 'conclusion', 'further_information']}
        return {
            'contract': 'SYSTEM4_AUTHORING_CONTRACT_V1',
            'block_semantics': block_semantics.bind(structure, type_def),
        }

    @staticmethod
    def _semantic_html(conclusion='Fazit', further='Weiterführende Informationen', order=None):
        bodies = {
            'intro': '<p>Einleitung.</p>',
            'body': '<h2>Prüfung</h2><p>Inhalt.</p>',
            'conclusion': f'<h2>{conclusion}</h2><p>Abschluss.</p>',
            'further_information': f'<h2>{further}</h2><p>Hinweise.</p>',
        }
        ids = order or ['intro', 'body', 'conclusion', 'further_information']
        return ''.join(f'<section data-block="{name}">{bodies[name]}</section>' for name in ids)

    def test_pr275_block_semantics_matrix_uses_current_same_article_repair_route(self):
        contract = self._semantic_contract()
        self.assertEqual(block_semantics.validate(self._semantic_html(), contract)['status'], 'PASS')
        cases = [
            (self._semantic_html(conclusion='Ausblick'), 'BLOCK_CONTENT_SEMANTIC_HEADING_MISMATCH'),
            (self._semantic_html(further='Lesetipps'), 'BLOCK_CONTENT_SEMANTIC_HEADING_MISMATCH'),
            (self._semantic_html(conclusion=''), 'BLOCK_CONTENT_SEMANTIC_HEADING_MISMATCH'),
            (self._semantic_html(order=['intro','body','further_information']), 'BLOCK_CONTENT_REQUIRED_BLOCK_ABSENT'),
            (self._semantic_html(order=['intro','body','further_information','conclusion']), 'BLOCK_CONTENT_BLOCK_ORDER_INVALID'),
            (self._semantic_html(order=['intro','body','conclusion','conclusion','further_information']), 'BLOCK_CONTENT_BLOCK_DUPLICATE'),
        ]
        for html, expected in cases:
            with self.subTest(expected=expected):
                with self.assertRaises(block_semantics.BlockSemanticRepairRequired) as caught:
                    block_semantics.validate(html, contract)
                codes = [row.get('error_code') for row in caught.exception.findings]
                self.assertIn(expected, codes)
                self.assertTrue(caught.exception.findings)
                self.assertTrue(all(row.get('repair_owner') == 'DRAFT_WORKER' for row in caught.exception.findings))
                rc, state = self._run_controller_repair_finding(caught.exception.findings[0])
                self.assertEqual(rc, 3)
                self.assertEqual(state['phase'], 'REPAIR_REQUIRED')

    def test_pr275_block_semantics_blocks_before_real_tool_engine(self):
        contract = self._semantic_contract()
        state = {
            'draft_markdown': self._semantic_html(conclusion='Ausblick'),
            'authoring_contract': contract,
        }
        with mock.patch.object(production_checks._engine, 'run_all') as real_engine:
            with self.assertRaises(production_checks.RepairRequired) as caught:
                production_checks.run_all(Path('/tmp'), state, {}, {})
        self.assertEqual(caught.exception.checker, 'block_semantics')
        self.assertEqual(caught.exception.findings[0]['repair_owner'], 'DRAFT_WORKER')
        real_engine.assert_not_called()

    def test_controller_draft_owner_enters_same_article_repair(self):
        rc, state = self._run_controller_repair_finding({
            'error_code': 'BLOCKED_KNOWN_REGRESSION_PATTERN',
            'repair_owner': 'DRAFT_WORKER',
        })
        self.assertEqual(rc, 3)
        self.assertEqual(state['phase'], 'REPAIR_REQUIRED')

    def test_controller_must_not_collapse_parent_owner_into_draft_repair(self):
        rc, state = self._run_controller_repair_finding({
            'error_code': 'BLOCKED_CONTENT_TITLE_INVALID',
            'field_path': 'canonical_article.title',
            'repair_owner': 'PARENT_TITLE_MACHINE',
        })
        self.assertNotEqual(
            state['phase'],
            'REPAIR_REQUIRED',
            'PARENT_TITLE_MACHINE finding was incorrectly collapsed into same-article DRAFT repair',
        )
        self.assertNotEqual(rc, 3, 'parent-owner return must be distinct from same-article repair return code')

    def test_hr_cont_001_002_repair_owner_same_article_and_same_checker_recheck(self):
        'HR-CONT-001/002 repairable content findings must return to DRAFT_WORKER and pass the same real checker after repair.'
        package = Path(__file__).resolve().parent.parent / 'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
        self.assertTrue(package.is_file())
        with tempfile.TemporaryDirectory(prefix='system4-hr-cont-repair-') as td:
            root = Path(td)
            with zipfile.ZipFile(package) as zf:
                zf.extractall(root)
            ppm = root / 'portal-production-machine'
            probe = ppm / 'tests/__system4_hr_cont_001_002_repair.php'
            probe.write_text(r'''<?php
require __DIR__.'/bootstrap-test.php';
function s4_codes($r){return array_values(array_unique(array_map(fn($e)=>(string)($e['error_code']??''),(array)($r['errors']??array()))));}
$out=array();
$base=(string)file_get_contents(__DIR__.'/fixtures/wave1/positive-control-structural-faq.html');
$title='Was muss vor einer Fahrt mit Pferdeanhänger geprüft werden?';
$bad='<h1>'.$title.'</h1>'.$base;
$r=PPM679_Known_Error_Gate::evaluate(array('title'=>$title,'article_type'=>'FAQ','content_html'=>$bad,'content_hash'=>hash('sha256',$bad)),array('article_type'=>'FAQ'),'hr_cont_001_bad','local');
$c=s4_codes($r); ppm_test_assert(in_array('BLOCKED_KNOWN_BODY_H1',$c,true),'body H1 exact blocker missing');
$fixed=PPM679_Known_Error_Gate::evaluate(array('title'=>$title,'article_type'=>'FAQ','content_html'=>$base,'content_hash'=>hash('sha256',$base)),array('article_type'=>'FAQ'),'hr_cont_001_fixed','local');
ppm_test_assert(!empty($fixed['ok']),'same article repaired body must pass same known-error checker');
$out['known_h1']=array('bad'=>$c,'recheck'=>$fixed['status']);
$posm=json_decode((string)file_get_contents(__DIR__.'/fixtures/wave2/positive-faq.json'),true);
$posh=(string)file_get_contents(__DIR__.'/fixtures/wave2/positive-faq.html');
function s4_wave($meta,$html){
 $g=array('article_type'=>$meta['article_type'],'title'=>$meta['title'],'content_html'=>$html,'content_hash'=>hash('sha256',$html));
 $i=array('article_type'=>$meta['article_type'],'quality_binding'=>$meta['quality_binding'],'quality_binding_hash'=>$meta['quality_binding_hash'],'runtime_order'=>$meta['runtime_order']);
 return PPM679_Content_Structure_Language_Gate::evaluate($g,$i,'hr_cont_wave','local');
}
$positive=s4_wave($posm,$posh); ppm_test_assert(!empty($positive['ok']),'positive Wave2 same article must PASS');
foreach(array('M01_BODY_H1'=>'BLOCKED_WAVE2_BODY_H1','M10_LIST'=>'BLOCKED_WAVE2_REQUIRED_LIST','M13_CONCLUSION'=>'BLOCKED_WAVE2_CONCLUSION_BALANCE') as $mid=>$expected){
 $dir=__DIR__.'/fixtures/wave2/mutations/'.$mid; $m=json_decode((string)file_get_contents($dir.'/metadata.json'),true); $h=(string)file_get_contents($dir.'/article.html');
 $bad=s4_wave($m,$h); $codes=s4_codes($bad); ppm_test_assert(in_array($expected,$codes,true),$mid.' exact blocker missing');
 $again=s4_wave($posm,$posh); ppm_test_assert(!empty($again['ok']),$mid.' repaired same article must pass same Wave2 checker');
 $out[$mid]=array('bad'=>$codes,'recheck'=>$again['content_structure_language_gate_status']);
}
$cand=json_decode((string)file_get_contents(dirname(__DIR__).'/contracts/g9-single-faq-approved-candidate-v1.json'),true);
$item=$cand['item']; $goodg=$cand['candidate'];
$good=PPM679_Content_Validator::check_gold_reference($goodg,'hr_cont_002_word_good','local',$item); ppm_test_assert(!empty($good['ok']),'canonical FAQ must pass word checker');
$short=$goodg; $short['content_html']='<p>Kurz.</p>'; $short['content_hash']=hash('sha256',$short['content_html']);
$badw=PPM679_Content_Validator::check_gold_reference($short,'hr_cont_002_word_bad','local',$item); $wc=s4_codes($badw); ppm_test_assert(in_array('BLOCKED_CONTENT_WORD_FLOOR',$wc,true),'word floor exact blocker missing');
$wordfixed=PPM679_Content_Validator::check_gold_reference($goodg,'hr_cont_002_word_fixed','local',$item); ppm_test_assert(!empty($wordfixed['ok']),'same canonical FAQ repaired word count must pass same checker');
$out['word_floor']=array('bad'=>$wc,'recheck'=>'PASS');
function s4_v5($html,$sections){
 $pack=array('claims'=>array(array('fact_id'=>'fact-a','claim_status'=>'FULLY_SUPPORTED','article_types'=>array('FAQ'),'statement'=>'Alpha fachlicher Inhalt','evidence_text'=>'Alpha fachlicher Inhalt')));
 PPM679_Storage::save_fact_pack('pack-x',$pack);
 $req=array('contract'=>'SECTION_REQUIREMENTS_V1','sections'=>$sections);
 $item=array('article_type'=>'FAQ','section_requirements'=>$req,'source_snapshot_id'=>'pack-x','runtime_order'=>array('allowed_fact_ids'=>array('fact-a'),'links'=>array()));
 $g=array('article_type'=>'FAQ','title'=>'Welche Prüfung ist erforderlich?','content_html'=>$html,'content_hash'=>hash('sha256',$html));
 $rm=new ReflectionMethod(PPM679_Content_Validator::class,'quality_check_v5'); $rm->setAccessible(true);
 return $rm->invoke(null,$g,$item,PPM679_Article_Type_Validator::type_definition('FAQ'),'hr_cont_002_v5','local',hash('sha256',$html));
}
$sections=array(
 array('section_id'=>'a','order'=>1,'required_concepts'=>array(),'content_obligations'=>array('heading_required'=>false,'paragraph_required'=>true,'list_roles'=>array(),'link_roles'=>array(),'table_policy'=>'FORBIDDEN')),
 array('section_id'=>'b','order'=>2,'required_concepts'=>array(),'content_obligations'=>array('heading_required'=>false,'paragraph_required'=>true,'list_roles'=>array(),'link_roles'=>array(),'table_policy'=>'FORBIDDEN'))
);
$goodhtml='<section data-section-id="a"><p data-fact-ids="fact-a">Alpha fachlicher Inhalt</p></section><section data-section-id="b"><p data-fact-ids="fact-a">Andere Formulierung zum Inhalt</p></section>';
$missing='<section data-section-id="a"><p data-fact-ids="fact-a">Alpha fachlicher Inhalt</p></section>';
$reverse='<section data-section-id="b"><p data-fact-ids="fact-a">Andere Formulierung zum Inhalt</p></section><section data-section-id="a"><p data-fact-ids="fact-a">Alpha fachlicher Inhalt</p></section>';
foreach(array('missing'=>array($missing,'BLOCKED_CONTENT_REQUIRED_SECTION_MISSING'),'order'=>array($reverse,'BLOCKED_CONTENT_SECTION_ORDER')) as $name=>$case){
 PPM679_Storage::reset_test_state(); $bad=s4_v5($case[0],$sections); $codes=s4_codes($bad); ppm_test_assert(in_array($case[1],$codes,true),$name.' exact blocker missing');
 PPM679_Storage::reset_test_state(); $fixed=s4_v5($goodhtml,$sections); ppm_test_assert(empty($fixed['errors']),$name.' repaired same article must pass same V5 quality checker');
 $out[$name]=array('bad'=>$codes,'recheck'=>'PASS');
}
echo json_encode(array('status'=>'PASS_HR_CONT_001_002_REPAIR_RECHECK','cases'=>$out),JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
?>''', encoding='utf-8')
            cp = subprocess.run(['php', str(probe)], cwd=ppm, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(json.loads(cp.stdout).get('status'), 'PASS_HR_CONT_001_002_REPAIR_RECHECK')

            repairable = (
                ('BLOCKED_KNOWN_BODY_H1', 'content.body_h1_count'),
                ('BLOCKED_WAVE2_BODY_H1', 'content.body_h1_count'),
                ('BLOCKED_CONTENT_WORD_FLOOR', 'content.word_count'),
                ('BLOCKED_CONTENT_REQUIRED_SECTION_MISSING', 'content.sections.a'),
                ('BLOCKED_CONTENT_SECTION_ORDER', 'content.section_order'),
                ('BLOCKED_WAVE2_REQUIRED_LIST', 'content.lists'),
                ('BLOCKED_WAVE2_CONCLUSION_BALANCE', 'content.body'),
            )
            for code, field in repairable:
                findings = production_checks._ppm_repair_findings({'errors': [{'error_code': code, 'field_path': field}]})
                self.assertEqual(len(findings), 1, code)
                self.assertEqual(findings[0]['repair_owner'], 'DRAFT_WORKER', code)

            self.assertEqual(production_checks._ppm_repair_findings({'errors': [{
                'error_code': 'BLOCKED_QF03_RENDERED_H1_COUNT',
                'field_path': 'rendered_dom.desktop.visible_h1_count',
            }]}), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
