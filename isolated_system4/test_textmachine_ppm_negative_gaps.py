import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


PHP_PROBE = r'''<?php
require __DIR__.'/bootstrap-test.php';
$ROOT=dirname(__DIR__); $cases=array();
function cs($r){return array_values(array_unique(array_filter(array_map(fn($e)=>(string)($e['error_code']??''),(array)($r['errors']??array())))));}
function hit($id,$expected,$r){global $cases;$c=cs($r);ppm_test_assert(in_array($expected,$c,true),$id.' expected '.$expected.' got '.json_encode($c));$cases[$id]=array('expected'=>$expected,'codes'=>$c);}
function wave($meta,$html){$g=array('article_type'=>$meta['article_type'],'title'=>$meta['title'],'content_html'=>$html,'content_hash'=>hash('sha256',$html));$i=array('article_type'=>$meta['article_type'],'quality_binding'=>$meta['quality_binding'],'quality_binding_hash'=>PPM679_Diagnostic::stable_hash($meta['quality_binding']),'runtime_order'=>$meta['runtime_order']);return PPM679_Content_Structure_Language_Gate::evaluate($g,$i,'s4_gap','local');}
$meta=json_decode(file_get_contents($ROOT.'/tests/fixtures/wave2/positive-faq.json'),true);$html=file_get_contents($ROOT.'/tests/fixtures/wave2/positive-faq.html');ppm_test_assert(!empty(wave($meta,$html)['ok']),'wave base');
$f=$ROOT.'/contracts/content-structure-language-gate-v2.json';rename($f,$f.'.bak');$r=wave($meta,$html);rename($f.'.bak',$f);hit('CODE::79ded7cc3da55813','BLOCKED_WAVE2_CONTRACT_MISSING',$r);
$m=$meta;$m['quality_binding']['internal_test_marker']='';hit('CODE::6b168e832adc1a68','BLOCKED_WAVE2_INTERNAL_MARKER_MISSING',wave($m,$html));
$h=str_replace('data-block="intro"','data-block="intro-mutated"',$html);hit('CODE::0cc1b289fde9cc7c','BLOCKED_WAVE2_INTRO_NOT_FIRST',wave($meta,$h));
$h=str_replace('Welche Anhängelast vor der Fahrt wirklich zählt','Kontrolle',$html);hit('CODE::4fb61887a06711b8','BLOCKED_WAVE2_HEADING_LENGTH',wave($meta,$h));
$m=$meta;$m['quality_binding']['portal_link_registry_hash']=str_repeat('0',64);hit('CODE::59a6c4a25cf46eca','BLOCKED_WAVE2_LINK_REGISTRY_HASH',wave($m,$html));
$h=str_replace('<a href="/pferdeanhaenger-sicherheit/">Sicherheitskontrolle am Pferdeanhänger</a>','Sicherheitskontrolle am Pferdeanhänger',$html);hit('CODE::7887c9aae2a9cc0e','BLOCKED_WAVE2_INTERNAL_LINK_COUNT',wave($meta,$h));
$m=$meta;array_pop($m['quality_binding']['link_bindings']);hit('CODE::6b5cb1d05ddcea8e','BLOCKED_WAVE2_INTERNAL_LINK_ROLE_MISSING',wave($m,$html));
$h=str_replace('>Kategorie Pferdetransport und Pferdeanhänger</a>','>Anderer Anchor</a>',$html);hit('CODE::63535e13beb64c8c','BLOCKED_WAVE2_BOUND_LINK_MISSING',wave($meta,$h));
$m=$meta;$old='/transport-pferdeanhaenger/';$new='https://example.org/transport/';$h=str_replace('href="'.$old.'"','href="'.$new.'"',$html);foreach($m['quality_binding']['link_bindings'] as &$b){if($b['role']==='parent_category')$b['href']=$new;}unset($b);foreach($m['quality_binding']['portal_link_registry']['entries'] as &$e){if($e['role']==='parent_category')$e['href']=$new;}unset($e);$m['quality_binding']['portal_link_registry_hash']=PPM679_Diagnostic::stable_hash($m['quality_binding']['portal_link_registry']);hit('CODE::541bb2884cd6e949','BLOCKED_WAVE2_INTERNAL_LINK_TARGET',wave($m,$h));
$h=str_replace('data-block="further_information"','data-block="conclusion"',$html);$m=$meta;foreach($m['quality_binding']['link_bindings'] as &$b){if($b['role']==='further_information')$b['section_id']='conclusion';}unset($b);hit('CODE::bc0b298d4b3141ed','BLOCKED_WAVE2_FURTHER_INFORMATION_LINK',wave($m,$h));
$h=str_replace('data-block="further_information"','data-block="details"',$html);$m=$meta;foreach($m['quality_binding']['link_bindings'] as &$b){if($b['role']==='further_information')$b['section_id']='details';}unset($b);hit('CODE::e59d7668d197fd19','BLOCKED_WAVE2_LINKS_NOT_DISTRIBUTED',wave($m,$h));
$m=$meta;$m['quality_binding']['language_evidence']['evidence_mode']='FULL_LANGUAGETOOL43_BASELINE_PLUS_HASHED_MAINBLOCK1_DELTA_REQUIRES_INDEPENDENT_CLAUDE_REVIEW';hit('CODE::3c00ae08a16fbb04','BLOCKED_MAINBLOCK1_LANGUAGE_DELTA_EVIDENCE',wave($m,$html));

function cv($method,$args){$rm=new ReflectionMethod(PPM679_Content_Validator::class,$method);$rm->setAccessible(true);return $rm->invokeArgs(null,$args);}
$cand=json_decode(file_get_contents($ROOT.'/contracts/g9-single-faq-approved-candidate-v1.json'),true);$item=$cand['item'];$pack=$cand['fact_pack'];PPM679_Storage::reset_test_state();PPM679_Storage::save_fact_pack((string)$pack['fact_pack_id'],$pack);$body=(string)$item['canonical_article']['body_html'];$g=array('article_type'=>'FAQ','title'=>$item['canonical_article']['title'],'content_html'=>$body,'content_hash'=>hash('sha256',$body));$def=PPM679_Article_Type_Validator::type_definition('FAQ');
function tech($g,$item,$def){return cv('technical_check',array($g,$item,$def,'s4_gap','local',hash('sha256',(string)$g['content_html'])));}function qual($g,$item,$def,$req=true){return cv('quality_check',array($g,$item,$def,'s4_gap','local',hash('sha256',(string)$g['content_html']),$req));}
$m=$item;$m['validation_contract_version']='UNKNOWN_S4';hit('CODE::80b908b0c053b899','BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN',PPM679_Content_Validator::check($g,$m,'s4_gap','local'));hit('CODE::6345716fff5ece77','BLOCKED_CONTENT_TYPE_DEFINITION_MISSING',tech($g,$item,null));
$gg=$g;$gg['content_hash']=str_repeat('0',64);hit('CODE::7a360734cec5ed46','BLOCKED_CONTENT_HASH_MISMATCH',tech($gg,$item,$def));
$gg=$g;$gg['content_html']=str_replace('comparison-table','other-table',$body);$gg['content_hash']=hash('sha256',$gg['content_html']);hit('CODE::2bbe9872d3d9b521','BLOCKED_CONTENT_TABLE_COUNT',tech($gg,$item,$def));
$gg=$g;$gg['content_html']=preg_replace('/<a\b[^>]*>.*?<\/a>/su','Link entfernt',$body,1);$gg['content_hash']=hash('sha256',$gg['content_html']);hit('CODE::3d6a7e9146649e88','BLOCKED_CONTENT_VISIBLE_LINK_COUNT',tech($gg,$item,$def));
$gg=$g;$gg['title']=rtrim($g['title'],'?');hit('CODE::7df037dde178bd1c','BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK',tech($gg,$item,$def));$gg=$g;$gg['title']='Pferdeanhänger: Prüfung?';hit('CODE::d041791134eb51c2','BLOCKED_CONTENT_TITLE_COLON',tech($gg,$item,$def));$m=$item;$m['target_keyword']='UnauffindbaresZielwort';hit('CODE::10b54313009ddbda','BLOCKED_CONTENT_TARGET_KEYWORD_TITLE',tech($g,$m,$def));
$gg=$g;$gg['content_html']=str_replace('</article>','<p>PASS</p></article>',$body);$gg['content_hash']=hash('sha256',$gg['content_html']);hit('CODE::3c26d1a0184264bf','BLOCKED_CONTENT_FORBIDDEN_MACHINE_STATUS_WORD',tech($gg,$item,$def));
$gg=$g;$gg['content_html']=preg_replace('/<span class="ppm-source-trace".*?<\/span>/su','',$body);$gg['content_hash']=hash('sha256',$gg['content_html']);hit('CODE::fffed240ecd54156','BLOCKED_CONTENT_SOURCE_TRACE_COUNT',qual($gg,$item,$def,true));
$gg=$g;$gg['content_html']=preg_replace('/data-source-title="[^"]+"/u','',$body,1);$gg['content_hash']=hash('sha256',$gg['content_html']);hit('CODE::03a92f3f0c73d6e3','BLOCKED_CONTENT_SOURCE_TRACE_FIELDS',qual($gg,$item,$def,true));
$gg=$g;$gg['content_html']=preg_replace('/data-source-title="[^"]+"/u','data-source-title="Testquelle"',$body,1);$gg['content_hash']=hash('sha256',$gg['content_html']);hit('CODE::b0c5da00bb146141','BLOCKED_CONTENT_PLACEHOLDER_SOURCE_TITLE',qual($gg,$item,$def,true));
$gg=$g;$gg['content_html']=preg_replace('/data-source-hash="[0-9a-f]{64}"/u','data-source-hash="'.str_repeat('0',64).'"',$body,1);$gg['content_hash']=hash('sha256',$gg['content_html']);hit('CODE::5ad7933f8fe0b5e2','BLOCKED_CONTENT_DUMMY_SOURCE_HASH',qual($gg,$item,$def,true));
$gg=$g;$gg['content_html']=preg_replace('/<section data-block="intro">.*?<\/section>/su','<section data-block="intro"></section>',$body,1);$gg['content_hash']=hash('sha256',$gg['content_html']);hit('CODE::088d091843ab8bd0','BLOCKED_CONTENT_REQUIRED_BLOCK_EMPTY',qual($gg,$item,$def,true));
$vhtml='<article><section data-block="options"><h3>Option Alpha</h3><p data-fact-ids="fact-a">Inhalt Alpha <span class="ppm-source-trace" data-fact-id="fact-a" data-source-hash="abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd" data-source-title="Quelle Option Beta"></span></p><h3>Option Beta</h3><p data-fact-ids="fact-a">Inhalt Beta</p></section></article>';$vg=array('article_type'=>'Vergleich','title'=>'Vergleich ohne Doppelpunkt','content_html'=>$vhtml,'content_hash'=>hash('sha256',$vhtml));$vi=array('article_type'=>'Vergleich','runtime_order'=>array('links'=>array()),'source_snapshot_id'=>'');$vd=PPM679_Article_Type_Validator::type_definition('Vergleich');hit('CODE::fcfe56a35a6b7649','BLOCKED_CONTENT_SOURCE_LABEL_OPTION_MISMATCH',qual($vg,$vi,$vd,true));
$gg=$g;$gg['content_html']=preg_replace('/data-fact-id="[^"]+"/u','data-fact-id="unknown-fact"',$body,1);$gg['content_hash']=hash('sha256',$gg['content_html']);hit('CODE::1c2556fa5197bafe','BLOCKED_CONTENT_TRACE_FACT_BINDING',qual($gg,$item,$def,true));

function v5($html,$sections){$req=array('contract'=>'SECTION_REQUIREMENTS_V1','sections'=>$sections);$hash=PPM679_Diagnostic::stable_hash($req);$item=array('article_type'=>'FAQ','target_keyword'=>'','section_requirements'=>$req,'section_requirements_hash'=>$hash,'canonical_article'=>array('validation_contract_version'=>'SECTION_REQUIREMENTS_V1','section_requirements_hash'=>$hash),'runtime_order'=>array('allowed_fact_ids'=>array(),'links'=>array()),'source_snapshot_id'=>'');$g=array('article_type'=>'FAQ','title'=>'Welche Prüfung ist erforderlich?','content_html'=>$html,'content_hash'=>hash('sha256',$html));return array($g,$item,PPM679_Article_Type_Validator::type_definition('FAQ'));}
$secs=array(array('section_id'=>'a','order'=>1,'required_concepts'=>array(),'content_obligations'=>array('heading_required'=>false,'paragraph_required'=>false,'list_roles'=>array(),'link_roles'=>array(),'table_policy'=>'FORBIDDEN')),array('section_id'=>'b','order'=>2,'required_concepts'=>array(),'content_obligations'=>array('heading_required'=>false,'paragraph_required'=>false,'list_roles'=>array(),'link_roles'=>array(),'table_policy'=>'FORBIDDEN')));$vh='<section data-section-id="a"><p data-fact-ids="x">Alpha Inhalt</p></section><section data-section-id="b"><p data-fact-ids="x">Beta Inhalt</p></section>';
[$vg,$vi,$vd]=v5($vh,$secs);$vi['section_requirements']=array();hit('CODE::6c2b5fd1d7d217b3','BLOCKED_VALIDATION_CONTRACT_VERSION_MISSING',cv('technical_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
[$vg,$vi,$vd]=v5($vh,$secs);$vi['section_requirements_hash']=str_repeat('0',64);hit('CODE::33582cf3a8c1b23e','BLOCKED_SECTION_REQUIREMENTS_HASH_MISMATCH',cv('technical_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
[$vg,$vi,$vd]=v5($vh,$secs);$vi['canonical_article']['validation_contract_version']='OLD';hit('CODE::cad611712c6fd66f','BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN',cv('technical_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$dup='<section data-section-id="a"><p data-fact-ids="x">Alpha</p></section><section data-section-id="a"><p data-fact-ids="x">Alpha2</p></section><section data-section-id="b"><p data-fact-ids="x">Beta</p></section>';[$vg,$vi,$vd]=v5($dup,$secs);hit('CODE::5b2e6c92fd5d21f2','BLOCKED_CONTENT_SECTION_DUPLICATE',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$miss='<section data-section-id="a"><p data-fact-ids="x">Alpha</p></section>';[$vg,$vi,$vd]=v5($miss,$secs);hit('CODE::15fb102d6ae830a9','BLOCKED_CONTENT_REQUIRED_SECTION_MISSING',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$rev='<section data-section-id="b"><p data-fact-ids="x">Beta</p></section><section data-section-id="a"><p data-fact-ids="x">Alpha</p></section>';[$vg,$vi,$vd]=v5($rev,$secs);hit('CODE::9523b761b0c32771','BLOCKED_CONTENT_SECTION_ORDER',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$s=$secs;$s[0]['content_obligations']['heading_required']=true;[$vg,$vi,$vd]=v5($vh,$s);hit('CODE::a9683c1aaff7bc84','BLOCKED_CONTENT_REQUIRED_SECTION_MISSING',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$s=$secs;$s[0]['content_obligations']['paragraph_required']=true;$x='<section data-section-id="a"><h2>Alpha</h2></section><section data-section-id="b"><p data-fact-ids="x">Beta</p></section>';[$vg,$vi,$vd]=v5($x,$s);hit('CODE::e720ceb321185ff4','BLOCKED_CONTENT_REQUIRED_SECTION_MISSING',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$s=$secs;$s[0]['content_obligations']['list_roles']=array('checklist');[$vg,$vi,$vd]=v5($vh,$s);hit('CODE::dffa4f864d58c10e','BLOCKED_CONTENT_REQUIRED_SECTION_MISSING',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$s=$secs;$s[0]['content_obligations']['table_policy']='REQUIRED';[$vg,$vi,$vd]=v5($vh,$s);hit('CODE::57299a61510fe9f0','BLOCKED_CONTENT_REQUIRED_TABLE_MISSING',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$tab='<table><thead><tr><th>A</th><th>B</th></tr></thead><tbody><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></tbody></table>';$x='<section data-section-id="a"><p data-fact-ids="x">Alpha</p>'.$tab.'</section><section data-section-id="b"><p data-fact-ids="x">Beta</p></section>';[$vg,$vi,$vd]=v5($x,$secs);hit('CODE::5c01d193adf04de2','BLOCKED_CONTENT_FORBIDDEN_TABLE_PRESENT',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$s=$secs;$s[0]['content_obligations']['table_policy']='MAYBE';[$vg,$vi,$vd]=v5($vh,$s);hit('CODE::fe5bb9ad9627441c','BLOCKED_CONTENT_TABLE_STRUCTURE',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$s=$secs;$s[0]['content_obligations']['table_policy']='REQUIRED';$x='<section data-section-id="a"><p data-fact-ids="x">Alpha</p><table><tr><td>1</td></tr></table></section><section data-section-id="b"><p data-fact-ids="x">Beta</p></section>';[$vg,$vi,$vd]=v5($x,$s);hit('CODE::87c6e350736dda9d','BLOCKED_CONTENT_TABLE_STRUCTURE',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$x='<section data-section-id="a"><p data-fact-ids="x">Alpha <a href="/extra/">Extra</a></p></section><section data-section-id="b"><p data-fact-ids="x">Beta</p></section>';[$vg,$vi,$vd]=v5($x,$secs);hit('CODE::80149dc474a98868','BLOCKED_CONTENT_UNBOUND_INTERNAL_LINK',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$s=$secs;$s[0]['content_obligations']['link_roles']=array('parent_category');[$vg,$vi,$vd]=v5($vh,$s);$vi['runtime_order']['links']=array(array('href'=>'/bound/','anchor'=>'Bound'));hit('CODE::cfb3979ec12847df','BLOCKED_CONTENT_BOUND_LINK_MISSING',cv('quality_check_v5',array($vg,$vi,$vd,'s4_gap','local',hash('sha256',$vg['content_html']))));
$kh=file_get_contents($ROOT.'/tests/fixtures/wave1/positive-control-structural-faq.html');$kt='Was muss vor einer Fahrt mit Pferdeanhänger geprüft werden?';function ke($t,$h){return PPM679_Known_Error_Gate::evaluate(array('title'=>$t,'article_type'=>'FAQ','content_html'=>$h,'content_hash'=>hash('sha256',$h)),array('article_type'=>'FAQ'),'s4_gap','local');}$kf=$ROOT.'/contracts/known-error-gate-v1.json';rename($kf,$kf.'.bak');$rr=ke($kt,$kh);rename($kf.'.bak',$kf);hit('CODE::c64fe59d56bffb96','BLOCKED_KNOWN_ERROR_CONTRACT_MISSING',$rr);preg_match('/<h2[^>]*>(.*?)<\/h2>/su',$kh,$hm);$heading=$hm[1];$dh=preg_replace('/<h2[^>]*>.*?<\/h2>/su','<h2>'.$heading.'</h2>',$kh,2);hit('CODE::bf51d9f9d16bd30f','BLOCKED_KNOWN_DUPLICATE_HEADING',ke($kt,$dh));
echo json_encode(array('status'=>'PASS','count'=>count($cases),'cases'=>$cases),JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
?>'''


class TextmachinePPMNegativeGapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = Path(__file__).resolve().parent.parent / 'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
        if not cls.package.is_file():
            raise AssertionError('PPM 6.7.9 package missing')

    def _extract(self, root):
        with zipfile.ZipFile(self.package) as zf:
            zf.extractall(root)
        return Path(root) / 'portal-production-machine'

    def test_45_active_ppm_gap_rules_expose_exact_real_error_code(self):
        with tempfile.TemporaryDirectory(prefix='system4-ppm-gaps-') as td:
            ppm = self._extract(td)
            probe = ppm / 'tests/__system4_ppm_gap_matrix.php'
            probe.write_text(PHP_PROBE, encoding='utf-8')
            cp = subprocess.run(['php', str(probe)], cwd=ppm, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False)
            self.assertEqual(cp.returncode, 0, cp.stderr + '\n' + cp.stdout)
            report = json.loads(cp.stdout)
            self.assertEqual(report.get('status'), 'PASS')
            self.assertEqual(report.get('count'), 45)
            self.assertEqual(len(report.get('cases', {})), 45)

    def test_4_wave4_requirements_bind_to_exact_qf03_mutations(self):
        with tempfile.TemporaryDirectory(prefix='system4-ppm-w4-') as td:
            ppm = self._extract(td)
            test = ppm / 'tests/qf03-wordpress-draft-readback-dom/test-qf03-rendered-dom-mutations.php'
            cp = subprocess.run(['php', str(test)], cwd=ppm, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            report = json.loads(cp.stdout)
            self.assertEqual(report.get('status'), 'PASS')
            blocked = report.get('blocked_mutations', {})
            expected = {
                'W4::R8-0786': ('zero_h1', 'BLOCKED_QF03_RENDERED_H1_COUNT'),
                'W4::R8-0787': ('duplicate_heading', 'BLOCKED_QF03_RENDERED_DUPLICATE_HEADINGS'),
                'W4::R8-0788': ('adjacent_headings', 'BLOCKED_QF03_RENDERED_ADJACENT_HEADINGS'),
                'W4::R8-0790': ('local_evidence', 'BLOCKED_QF03_RENDERED_EVIDENCE_CLASS'),
            }
            for rule_id, (mutation, code) in expected.items():
                with self.subTest(rule_id=rule_id):
                    self.assertEqual(blocked.get(mutation), code)
            self.assertEqual(len(expected), 4)


if __name__ == '__main__':
    unittest.main(verbosity=2)
