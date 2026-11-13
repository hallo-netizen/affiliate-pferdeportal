#!/usr/bin/env python3
"""RC28 proves actual PHP behavior against actual HAB category labels and
parent-topic facets; rejects insurance/FAQ/accessory false positives. No live
WordPress mutation. Keeps previous import/partner logic.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
from hashlib import sha256
import re
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    bridge=z.read("affiliate-portal-router/includes/class-ppar-hab-bewahr-bridge.php").decode()
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    idealo=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode()
    assert "Version: 0.1.25-rc28" in main
    assert "Über zugehörige Themenseite erkannt:" in idealo
    assert "last_catalog_signature" in idealo and "last_feed_reject_stats" in idealo
    assert "from_topic_page_categories" in bridge
    assert "count($rules)<50" in bridge
    assert "if ($is_insurance)" in bridge
    assert "($parent['name']??'')" in bridge
    assert "get_post_status((int)($parent['wp_id']??0)) === 'publish'" in bridge
    assert "output_mode" in idealo

    def extract(src,name):
        pat=re.compile(r"(?:public|private|protected)(?:\s+static)?\s+function\s+"+re.escape(name)+r"\s*\(")
        hit=pat.search(src)
        assert hit,name
        op=src.index("{",hit.end())
        depth=0
        for i in range(op,len(src)):
            if src[i]=="{":depth+=1
            if src[i]=="}":
                depth-=1
                if depth==0:
                    return src[hit.start():i+1].replace("private static function","public static function",1).replace("private function","public function",1)
        raise RuntimeError(name)
    methods="\n".join(extract(bridge,name) for name in ["ancestors","nearest_page","product_family","catalog"])
    with TemporaryDirectory() as td:
        phps=[n for n in z.namelist() if n.endswith(".php")]
        assert len(phps)==25
        for idx,name in enumerate(phps):
            p=Path(td)/f"{idx}.php"
            p.write_bytes(z.read(name))
            r=run(["php","-l",str(p)],capture_output=True,text=True)
            assert r.returncode==0,(name,r.stdout,r.stderr)
        script=r'''<?php
class WP_Error { private $x;public function __construct($s,$m=''){$this->x=$m;} }
function is_wp_error($v){return $v instanceof WP_Error;}
function absint($x){return max(0,(int)$x);}
function sanitize_text_field($x){return trim((string)$x);}
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x)));}
function sanitize_title($x){return preg_replace('/[^a-z0-9\-]/','-',strtolower(remove_accents((string)$x)));}
function remove_accents($x){return str_replace(array('ä','ö','ü','Ä','Ö','Ü','ß'),array('ae','oe','ue','Ae','Oe','Ue','ss'),(string)$x);}
function get_post_status($id){return $GLOBALS['statuses'][$id]??'publish';}
function get_option($name,$default=null){return $GLOBALS['opts'][$name]??$default;}
function wp_json_encode($x){return json_encode($x);}
function ok($p,$label){if(!$p){fwrite(STDERR,"FAIL ".$label."\n");exit(3);}echo "PASS ".$label."\n";}
class PPAR_HB_Integration {
  private static $catalog=null;
  public static $fake_nodes=array();
  public static function verified_nodes(){return self::$fake_nodes;}
  METHODS
}
$GLOBALS['opts']=array('apkw_target_tree_active_revision_v1'=>'rc28-real-parent-qa');
$GLOBALS['statuses']=array();
foreach(array(
    array('Türschloss montieren','Türschloss'),
    array('Feuerlöscher auswählen','Feuerlöscher'),
    array('Video-Türsprechanlagen montieren','Video-Türsprechanlage'),
    array('Abdichtungsmaterialien auswählen','Abdichtungsmaterial'),
    array('Akku-Ladegeräte & Defekte','Akkuladegerät'),
    array('Schließsysteme vergleichen','Schließsystem'),
    array('Rauchmelder aufstellen','Rauchmelder')
) as $v){
    ok(PPAR_HB_Integration::product_family($v[0])===$v[1],
       'Real/grammatical German physical noun recognized: '.$v[0]);
}
foreach (array('Schlüsselübergabe im Ferienhaus','Leerstehendes Wohnhaus',
 'SIM-Karten für Alarmmelder','Brandschutz beurteilen','Akku-Ladeplätze prüfen') as $v) {
    ok(PPAR_HB_Integration::product_family($v)==='','No invented sellable product for '.$v);
}
$nodes=array(
    'core:hub'=>array('id'=>'core:hub','name'=>'Hab & Bewahr','slug'=>'hab-und-bewahr','type'=>'page','pillar'=>'core','wp_id'=>1,'parent'=>''),
    'core:world:fire'=>array('id'=>'core:world:fire','name'=>'Feuer & Gase','slug'=>'feuer-und-gase','type'=>'page','pillar'=>'core','wp_id'=>2,'parent'=>'core:hub'),
    'core:world:insurance'=>array('id'=>'core:world:insurance','name'=>'Versicherungen','slug'=>'versicherungen','type'=>'page','pillar'=>'core','wp_id'=>3,'parent'=>'core:hub'),
    'core:page:rauch'=>array('id'=>'core:page:rauch','name'=>'Rauchmelder','slug'=>'rauchmelder','type'=>'page','pillar'=>'core','wp_id'=>4,'parent'=>'core:world:fire'),
    'core:page:leer'=>array('id'=>'core:page:leer','name'=>'Leerstehendes Wohnhaus','slug'=>'leerstehendes-wohnhaus','type'=>'page','pillar'=>'core','wp_id'=>5,'parent'=>'core:world:fire'),
    'core:page:material'=>array('id'=>'core:page:material','name'=>'Abdichtung von Anbauten','slug'=>'abdichtung-anbauten','type'=>'page','pillar'=>'core','wp_id'=>6,'parent'=>'core:world:fire'),
    'core:page:lock'=>array('id'=>'core:page:lock','name'=>'Türschloss','slug'=>'tuerschloss','type'=>'page','pillar'=>'core','wp_id'=>7,'parent'=>'core:world:fire'),
    'core:page:versicherung'=>array('id'=>'core:page:versicherung','name'=>'Rauchmelder Versicherung','slug'=>'rauchmelder-versicherung','type'=>'page','pillar'=>'core','wp_id'=>8,'parent'=>'core:world:insurance'),
);
foreach(range(1,17) as $n) {
    $id="core:leaf:rauch:$n";
    $nodes[$id]=array('id'=>$id,'name'=>"Montage und Wartung $n",'slug'=>"montage-und-wartung-$n",
       'type'=>'category','pillar'=>'core','wp_id'=>1000+$n,'parent'=>'core:page:rauch');
}
$nodes['core:leaf:rauch:faq']=array('id'=>'core:leaf:rauch:faq','name'=>'Rauchmelder: Häufige Fragen','slug'=>'fragen-rauchmelder','type'=>'category','pillar'=>'core','wp_id'=>1111,'parent'=>'core:page:rauch');
foreach(range(1,15) as $n){
    $id="core:leaf:leer:$n";
    $nodes[$id]=array('id'=>$id,'name'=>"Organisieren und absichern $n",'slug'=>"leerstand-$n",
       'type'=>'category','pillar'=>'core','wp_id'=>1200+$n,'parent'=>'core:page:leer');
}
$nodes['core:leaf:material']=array('id'=>'core:leaf:material','name'=>'Abdichtungsmaterialien auswählen',
 'slug'=>'abdichtungsmaterialien-auswaehlen','type'=>'category','pillar'=>'core','wp_id'=>1400,'parent'=>'core:page:material');
$nodes['core:leaf:lock']=array('id'=>'core:leaf:lock','name'=>'Auswahl und Einbau',
 'slug'=>'auswahl-und-einbau','type'=>'category','pillar'=>'core','wp_id'=>1401,'parent'=>'core:page:lock');
$nodes['core:leaf:insurance']=array('id'=>'core:leaf:insurance','name'=>'Montage und Wartung',
 'slug'=>'versicherungs-unterkategorie','type'=>'category','pillar'=>'core','wp_id'=>1402,'parent'=>'core:page:versicherung');
PPAR_HB_Integration::$fake_nodes=$nodes;
$out=PPAR_HB_Integration::catalog();
ok(is_array($out),'existing category-source catalog builds from real-style WP topic/page/category roles');
$names=array_column($out['business_concepts'],'title');
sort($names);
ok($names===array('Abdichtungsmaterial','Rauchmelder','Türschloss'),
  'Exactly 3 proven physical groups from product owner or leaf; no invented group');
ok(($out['hab_product_coverage_audit']['from_topic_page_categories']??0)===18,
  '18 editorial leaf categories inherit known product topic safely');
ok(($out['hab_product_coverage_audit']['information_excluded']??0)===1,
  'FAQ remains excluded even under a product topic');
ok(($out['hab_product_coverage_audit']['insurance_excluded']??0)===1,
  'Insurance remains excluded even under a product-named page');
ok(($out['hab_product_coverage_audit']['unclassified_review']??0)===15,
  '15 generic non-product categories remain unclassified, not forced into ads');
ok(count($out['search_rules'])===3 && count($out['article_targets'])===36,
  'Existing search-rule and article-target structures remain in place');
$GLOBALS['statuses'][7]='draft';
?>
'''
        script=script.replace("METHODS",methods)
        php=Path(td)/"test.php"
        php.write_text(script)
        r=run(["php",str(php)],capture_output=True,text=True)
        print(r.stdout)
        assert r.returncode==0,(r.stderr,r.stdout)
        print("HAB_RC28_PHP_LINT_PASS",len(phps))
print("HAB_RC28_KISS_QA_PASS")
