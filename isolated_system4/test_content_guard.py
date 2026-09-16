import hashlib
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

import content_guard


def sha(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


E1 = 'Die konkrete Auswahl richtet sich nach dem tatsächlichen Einsatzzweck und der sicheren Handhabung.'
E2 = 'Materialzustand und passende Nutzung müssen vor dem Einsatz konkret geprüft werden.'
SOURCE_EVIDENCE = E1 + '\n' + E2 + '\nZusätzlicher Quellenkontext für den lokalen Nachweis.'


def good_research():
    return {
        'contract': content_guard.RESEARCH_CONTRACT,
        'sources': [{
            'source_id': 'src-official-1',
            'source_title': 'Fachquelle – konkrete Anleitung',
            'source_url': 'https://example.org/fachquelle',
            'retrieved_at': '2026-09-12T20:00:00Z',
            'snapshot_sha256': sha(SOURCE_EVIDENCE),
            'evidence': SOURCE_EVIDENCE,
        }],
    }


def good_facts():
    return {
        'contract': content_guard.FACTS_CONTRACT,
        'claims': [
            {'fact_id': 'fact-a', 'source_id': 'src-official-1', 'statement': 'Der Einsatzzweck ist ein konkretes Auswahlkriterium.', 'evidence_text': E1, 'evidence_text_sha256': sha(E1)},
            {'fact_id': 'fact-b', 'source_id': 'src-official-1', 'statement': 'Der Materialzustand ist vor der Nutzung zu prüfen.', 'evidence_text': E2, 'evidence_text_sha256': sha(E2)},
        ],
    }


def good_pack():
    research = good_research(); facts = good_facts(); source = research['sources'][0]
    return {
        'contract': 'canonical_fact_pack_v1',
        'status': 'SOURCE_VERIFIED_PRODUCTION_READY',
        'sources': [dict(source)],
        'claims': list(facts['claims']),
    }


class ContentGuardTests(unittest.TestCase):
    def test_positive_research_facts_pack_and_article_trace(self):
        research = good_research(); facts = good_facts(); pack = good_pack()
        content_guard.validate_research_document(research)
        content_guard.validate_facts_document(facts, research)
        content_guard.validate_fact_pack(pack, research, facts)
        article = '<article><p data-fact-ids="fact-a fact-b">Konkreter Artikelinhalt mit belegten Aussagen.</p></article>'
        self.assertEqual(content_guard.validate_single_article(article, pack)['status'], 'PASS')

    def test_historical_plain_research_text_is_blocked(self):
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'RESEARCH_JSON_INVALID'):
            content_guard.validate_research_document('R' * 100)

    def test_self_certified_source_hash_is_blocked(self):
        research = good_research(); research['sources'][0]['snapshot_sha256'] = '0' * 64
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'RESEARCH_SOURCE_HASH_MISMATCH'):
            content_guard.validate_research_document(research)

    def test_fact_without_accepted_source_is_blocked(self):
        facts = good_facts(); facts['claims'][0]['source_id'] = 'fresh-system4-source-self-made'
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'FACT_SOURCE_NOT_IN_RESEARCH'):
            content_guard.validate_facts_document(facts, good_research())

    def test_fact_text_not_present_in_captured_source_is_blocked(self):
        facts = good_facts(); invented = 'Diese erfundene Belegbehauptung steht nicht im gesicherten Quellenausschnitt.'; facts['claims'][0]['evidence_text'] = invented; facts['claims'][0]['evidence_text_sha256'] = sha(invented)
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'FACT_EVIDENCE_NOT_IN_SOURCE:0'):
            content_guard.validate_facts_document(facts, good_research())

    def test_historical_bad_fact_pack_without_sources_is_blocked(self):
        bad = {'contract': 'canonical_fact_pack_v1', 'status': 'SOURCE_VERIFIED_PRODUCTION_READY', 'claims': good_facts()['claims']}
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'FACT_PACK_SOURCES_MISSING'):
            content_guard.validate_fact_pack(bad)

    def test_fact_pack_source_without_captured_evidence_is_blocked(self):
        bad = good_pack(); bad['sources'][0].pop('evidence')
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'FACT_PACK_SOURCE_EVIDENCE_INVALID'):
            content_guard.validate_fact_pack(bad)

    def test_unknown_article_fact_id_is_blocked(self):
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'ARTICLE_UNKNOWN_FACT_ID'):
            content_guard.validate_single_article('<p data-fact-id="fact-invented">Text</p>', good_pack())

    def test_good_batch_is_distinct(self):
        bodies = [f'<article><p data-fact-id="fact-a">Thema {i} mit eigener Formulierung ' + ' '.join(f'eigen{i}_{n}' for n in range(80)) + '</p></article>' for i in range(7)]
        self.assertEqual(content_guard.validate_batch_distinctness(bodies)['status'], 'PASS')

    def test_historical_template_batch_is_blocked(self):
        common = 'Eine gute Entscheidung beginnt mit einer Bestandsaufnahme. Notiere wie häufig die Lösung gebraucht wird und welche Bedingungen bestehen. '
        bodies = [f'<article><p>{common}{common}Thema {i}.</p></article>' for i in range(7)]
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'BATCH_TEMPLATE_REUSE_BLOCKED'):
            content_guard.validate_batch_distinctness(bodies)

    def test_small_repair_passes_broad_rewrite_blocks(self):
        old = '<article><p>' + ('Konkreter fachlicher Satz. ' * 30) + '</p></article>'
        new = old.replace('Konkreter fachlicher Satz.', 'Konkreter fachlicher Satz!', 1)
        self.assertEqual(content_guard.validate_repair_continuity(old, new)['status'], 'PASS')
        replacement = '<article><p>' + ('Völlig anderer Inhalt ohne Bezug. ' * 12) + '</p></article>'
        with self.assertRaisesRegex(content_guard.ContentGuardError, 'REPAIR_SCOPE_TOO_LARGE'):
            content_guard.validate_repair_continuity(old, replacement)

    def test_hr_cont_002_sections_order_word_list_conclusion_are_individually_effective(self):
        'HR-CONT-002 required sections/order/word floor/list/conclusion must each be effect-sensitive.'
        package = Path(__file__).resolve().parent.parent / 'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
        self.assertTrue(package.is_file())
        with tempfile.TemporaryDirectory(prefix='system4-hr-cont-002-') as td:
            root = Path(td)
            with zipfile.ZipFile(package) as zf:
                zf.extractall(root)
            ppm = root / 'portal-production-machine'

            def run(rel: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ['php', str(ppm / rel)], cwd=ppm, text=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False,
                )

            positive = run('tests/test-g8-targeted-repair-faq-chain.php')
            self.assertEqual(positive.returncode, 0, positive.stderr)
            self.assertEqual(json.loads(positive.stdout).get('status'), 'PASS')

            word_probe = ppm / 'tests/__system4_hr_cont_002_word.php'
            word_probe.write_text(r'''<?php
require __DIR__.'/bootstrap-test.php';
$html='<p>Kurz und absichtlich deutlich unter dem verbindlichen Mindestumfang.</p>';
$r=PPM679_Content_Validator::check_gold_reference(array('title'=>'Kurzer Kontrolltext','article_type'=>'FAQ','content_html'=>$html,'content_hash'=>hash('sha256',$html)),'hr_cont_002_word','local',array('article_type'=>'FAQ'));
$codes=array_values(array_unique(array_map(fn($e)=>(string)($e['error_code']??''),(array)($r['errors']??array()))));
ppm_test_assert(in_array('BLOCKED_CONTENT_WORD_FLOOR',$codes,true),'word-floor mutation must expose BLOCKED_CONTENT_WORD_FLOOR');
echo json_encode(array('status'=>'PASS_HR_CONT_002_WORD','codes'=>$codes),JSON_UNESCAPED_SLASHES)."\n";
?>''', encoding='utf-8')
            baseline = run('tests/__system4_hr_cont_002_word.php')
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            cv = ppm / 'includes/content-validator.php'
            original_cv = cv.read_text(encoding='utf-8')
            word_branch = 'if ($word_count<self::MIN_WORDS) {'
            self.assertEqual(original_cv.count(word_branch), 1, word_branch)
            cv.write_text(original_cv.replace(word_branch, 'if (false) {', 1), encoding='utf-8')
            killed = run('tests/__system4_hr_cont_002_word.php')
            self.assertNotEqual(killed.returncode, 0, 'HR-CONT-002 word-floor mutation survived')
            cv.write_text(original_cv, encoding='utf-8')

            section_probe = ppm / 'tests/__system4_hr_cont_002_sections.php'
            section_probe.write_text(r'''<?php
require __DIR__.'/bootstrap-test.php';
function s4_quality($html,$sections){
  $req=array('contract'=>'SECTION_REQUIREMENTS_V1','sections'=>$sections);
  $item=array('article_type'=>'FAQ','section_requirements'=>$req,'source_snapshot_id'=>'','runtime_order'=>array('allowed_fact_ids'=>array(),'links'=>array()));
  $generated=array('article_type'=>'FAQ','title'=>'Welche Prüfung ist erforderlich?','content_html'=>$html,'content_hash'=>hash('sha256',$html));
  $rm=new ReflectionMethod(PPM679_Content_Validator::class,'quality_check_v5'); $rm->setAccessible(true);
  return $rm->invoke(null,$generated,$item,PPM679_Article_Type_Validator::type_definition('FAQ'),'hr_cont_002_sections','local',hash('sha256',$html));
}
function s4_codes($r){return array_values(array_unique(array_map(fn($e)=>(string)($e['error_code']??''),(array)($r['errors']??array()))));}
$sections=array(
 array('section_id'=>'a','order'=>1,'required_concepts'=>array(),'content_obligations'=>array('heading_required'=>false,'paragraph_required'=>false,'list_roles'=>array(),'link_roles'=>array(),'table_policy'=>'FORBIDDEN')),
 array('section_id'=>'b','order'=>2,'required_concepts'=>array(),'content_obligations'=>array('heading_required'=>false,'paragraph_required'=>false,'list_roles'=>array(),'link_roles'=>array(),'table_policy'=>'FORBIDDEN'))
);
$missing=s4_codes(s4_quality('<section data-section-id="a"></section>',$sections));
ppm_test_assert(in_array('BLOCKED_CONTENT_REQUIRED_SECTION_MISSING',$missing,true),'missing section must expose exact blocker');
$reversed=s4_codes(s4_quality('<section data-section-id="b"></section><section data-section-id="a"></section>',$sections));
ppm_test_assert(in_array('BLOCKED_CONTENT_SECTION_ORDER',$reversed,true),'reversed sections must expose exact order blocker');
echo json_encode(array('status'=>'PASS_HR_CONT_002_SECTIONS','missing'=>$missing,'reversed'=>$reversed),JSON_UNESCAPED_SLASHES)."\n";
?>''', encoding='utf-8')
            baseline = run('tests/__system4_hr_cont_002_sections.php')
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            missing_branch = "if ($id==='' || !in_array($id,$actual_ids,true)) {"
            order_branch = 'if ($expected_ids!==$actual_ids) {'
            self.assertEqual(original_cv.count(missing_branch), 1, missing_branch)
            self.assertEqual(original_cv.count(order_branch), 1, order_branch)
            cv.write_text(original_cv.replace(missing_branch, 'if (false) {', 1), encoding='utf-8')
            killed = run('tests/__system4_hr_cont_002_sections.php')
            self.assertNotEqual(killed.returncode, 0, 'HR-CONT-002 required-section mutation survived')
            cv.write_text(original_cv.replace(order_branch, 'if (false) {', 1), encoding='utf-8')
            killed = run('tests/__system4_hr_cont_002_sections.php')
            self.assertNotEqual(killed.returncode, 0, 'HR-CONT-002 section-order mutation survived')
            cv.write_text(original_cv, encoding='utf-8')

            wave2 = run('tests/test-wave2-content-mutations.php')
            self.assertEqual(wave2.returncode, 0, wave2.stderr)
            gate = ppm / 'includes/content-structure-language-gate.php'
            original_gate = gate.read_text(encoding='utf-8')
            branches = (
                ("if (count($counts)<(int)($contract['lists']['minimum_lists']??1) || $max<$required) {", 'HR-CONT-002 list mutation survived'),
                ('if ($body===null || $ratio<$min || $paragraphs<$min_p) {', 'HR-CONT-002 conclusion mutation survived'),
            )
            for old, message in branches:
                self.assertEqual(original_gate.count(old), 1, old)
                gate.write_text(original_gate.replace(old, 'if (false) {', 1), encoding='utf-8')
                killed = run('tests/test-wave2-content-mutations.php')
                self.assertNotEqual(killed.returncode, 0, message)
                gate.write_text(original_gate, encoding='utf-8')

    def test_hr_cont_003_ai_disclosure_exact_end_owner_and_recheck_are_individually_effective(self):
        'HR-CONT-003 exact AI disclosure must block, route to DRAFT_WORKER, and pass after same-checker repair.'
        import production_checks
        package = Path(__file__).resolve().parent.parent / 'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
        self.assertTrue(package.is_file())
        with tempfile.TemporaryDirectory(prefix='system4-hr-cont-003-') as td:
            root = Path(td)
            with zipfile.ZipFile(package) as zf:
                zf.extractall(root)
            ppm = root / 'portal-production-machine'
            probe = ppm / 'tests/__system4_hr_cont_003.php'
            probe.write_text(r'''<?php
require __DIR__.'/three-type-bundled-local/bootstrap-three-type.php';
function s4_eval($html,$item,$pack){
  $g=array('title'=>(string)$item['canonical_article']['title'],'article_type'=>(string)$item['article_type'],'content_html'=>$html,'content_hash'=>hash('sha256',$html));
  return PPM679_Three_Type_Local_Content_Validator::evaluate($g,$item,$pack,'hr_cont_003');
}
list($item,$pack,$generated)=ppm_three_generated('Beratung');
$original=(string)$generated['content_html'];
$good=s4_eval($original,$item,$pack);
ppm_test_assert(!empty($good['ok']),'original same article must pass exact disclosure checker');
$required='Dieser Beitrag wurde mithilfe von KI vorformuliert und anschließend redaktionell geprüft und überarbeitet.';
$bad_text=str_replace($required,'Dieser Beitrag wurde mit KI erstellt.',$original);
$r1=s4_eval($bad_text,$item,$pack); $c1=ppm_three_codes($r1['errors']??array());
ppm_test_assert(empty($r1['ok'])&&in_array('BLOCKED_CONTENT_AI_DISCLOSURE',$c1,true),'altered disclosure must expose exact blocker');
$needle='<p class="ppm-ai-disclosure">'.$required.'</p>';
ppm_test_assert(substr_count($original,$needle)===1,'exact disclosure source must occur once');
$bad_end=str_replace($needle,$needle.'<p>Nachgelagerter Inhalt.</p>',$original);
$r2=s4_eval($bad_end,$item,$pack); $c2=ppm_three_codes($r2['errors']??array());
ppm_test_assert(empty($r2['ok'])&&in_array('BLOCKED_CONTENT_AI_DISCLOSURE',$c2,true),'disclosure not at end must expose exact blocker');
$repaired=s4_eval($original,$item,$pack);
ppm_test_assert(!empty($repaired['ok']),'same article repaired disclosure must pass same checker again');
echo json_encode(array('status'=>'PASS_HR_CONT_003','altered_codes'=>$c1,'position_codes'=>$c2,'recheck_status'=>$repaired['status']),JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
?>''', encoding='utf-8')

            def run() -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ['php', str(probe)], cwd=ppm, text=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False,
                )

            baseline = run()
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            self.assertEqual(json.loads(baseline.stdout).get('status'), 'PASS_HR_CONT_003')

            findings = production_checks._ppm_repair_findings({'errors': [{
                'error_code': 'BLOCKED_CONTENT_AI_DISCLOSURE',
                'failed_rule': 'EXACT_AI_DISCLOSURE_REQUIRED_AT_ARTICLE_END',
                'field_path': 'content.ai_disclosure',
            }]})
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0]['repair_owner'], 'DRAFT_WORKER')

            source = ppm / 'includes/three-type-local-content-validator.php'
            original_source = source.read_text(encoding='utf-8')
            branch = "if(!$ok) $errors[]=self::err('BLOCKED_CONTENT_AI_DISCLOSURE'"
            self.assertEqual(original_source.count(branch), 1, branch)
            source.write_text(original_source.replace(branch, "if(false) $errors[]=self::err('BLOCKED_CONTENT_AI_DISCLOSURE'", 1), encoding='utf-8')
            killed = run()
            self.assertNotEqual(killed.returncode, 0, 'HR-CONT-003 disclosure branch mutation survived')


if __name__ == '__main__':
    unittest.main(verbosity=2)
