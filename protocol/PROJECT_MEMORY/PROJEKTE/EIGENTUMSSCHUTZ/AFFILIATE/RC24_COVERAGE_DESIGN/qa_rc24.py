#!/usr/bin/env python3
"""HAB RC24: genuine catalog, source property, coverage and regression checks.
Only synthetic test category entries; never claims user WP live update.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import re,hashlib
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
p=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(p) as z:
 assert z.testzip() is None and len(z.namelist())==36
 main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
 bridge=z.read("affiliate-portal-router/includes/class-ppar-hab-bewahr-bridge.php").decode()
 idealo=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode()
 css=z.read("affiliate-portal-router/assets/frontend.css").decode()
 assert 'Version: 0.1.21-rc24' in main
 assert "count($rules) < 50" not in bridge
 assert "'insurance_excluded'" in bridge
 assert "'unclassified_review'" in bridge
 assert "'last_feed_reject_stats'" in idealo
 assert "'last_matched_concept_ids'" in idealo
 assert 'Produktabdeckung – prüfbarer Bericht' in idealo
 assert '/311 Produktkonzepte' not in idealo
 assert "contract_concepts'=>count($concept_map)" in idealo
 assert 'Verfügbar' in main
 assert "margin-top:auto!important" in css
 assert "border:1px solid #d2dbd5!important" in css
 assert "idealo_hab_card_properties($payload,$title)" in idealo
 assert "idealo_hab_coverage_report()" in idealo
 phps=[n for n in z.namelist() if n.endswith(".php")]
 assert len(phps)==25
 with TemporaryDirectory() as td:
  for i,fn in enumerate(phps):
   f=Path(td)/f"{i}.php";f.write_bytes(z.read(fn))
   r=run(["php","-l",str(f)],capture_output=True,text=True)
   assert r.returncode==0,(fn,r.stdout,r.stderr)
 def extract(src,name):
  pat=re.compile(r"(?:public|private|protected)(?:\s+static)?\s+function\s+"+re.escape(name)+r"\s*\(")
  hit=pat.search(src)
  assert hit,name
  op=src.index("{",hit.end()); depth=0
  for i in range(op,len(src)):
   if src[i]=="{":depth+=1
   elif src[i]=="}":
    depth-=1
    if depth==0:
     return src[hit.start():i+1].replace("private static function","public static function",1).replace("private function","public function",1)
  raise Exception(name)
 funcs="\n".join(extract(bridge,x) for x in ["ancestors","nearest_page","product_family","catalog"])
 method="\n".join(extract(idealo,x) for x in ["idealo_hab_card_properties","idealo_hab_coverage_report"])
 source=r'''<?php
class WP_Error {private $x;public function __construct($x,$s=''){$this->x=$x;}}
function is_wp_error($x){return $x instanceof WP_Error;}
function absint($x){return max(0,(int)$x);}
function sanitize_text_field($x){return trim((string)$x);}
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x)));}
function sanitize_title($x){return preg_replace('/[^a-z0-9-]/','-',strtolower((string)$x));}
function remove_accents($x){return str_replace(array('ä','ö','ü','Ä','Ö','Ü','ß'),array('ae','oe','ue','Ae','Oe','Ue','ss'),(string)$x);}
function get_post_status($id){return 'publish';}
function get_option($x,$default=null){return $GLOBALS['mock_options'][$x]??$default;}
function wp_json_encode($x){return json_encode($x);}
function expect($v,$msg){if(!$v){fwrite(STDERR,"FAIL ".$msg.PHP_EOL);exit(3);}echo "PASS ".$msg.PHP_EOL;}
class PPAR_HB_Integration {
 private static $catalog=null;
 public static $fake_nodes=array();
 public static function verified_nodes(){return self::$fake_nodes;}
 METHODS
}
class HabIdealoCoverage {
 public $s=array();
 private $idx=array();
 OTHER_METHODS
 public function idealo_settings(){return $this->s;}
 public function idealo_match_index(){return $this->idx;}
 public function feedIndex($x){$this->idx=$x;}
}
$GLOBALS['mock_options']=array('apkw_target_tree_active_revision_v1'=>'qa-rc24');
$tree=array(
 'core:hub'=>array('id'=>'core:hub','name'=>'Hab','slug'=>'hab','pillar'=>'core','type'=>'page','wp_id'=>1,'parent'=>''),
 'core:world:schutz'=>array('id'=>'core:world:schutz','name'=>'Einbruch und Diebstahl','slug'=>'einbruch','pillar'=>'core','type'=>'page','wp_id'=>2,'parent'=>'core:hub'),
 'core:world:versicherung'=>array('id'=>'core:world:versicherung','name'=>'Versicherungen','slug'=>'versicherungen','pillar'=>'core','type'=>'page','wp_id'=>3,'parent'=>'core:hub')
);
for($i=1;$i<=80;$i++){
 $parent='core:area:'.$i;$key='core:leaf:'.$i;
 $tree[$parent]=array('id'=>$parent,'name'=>'Türschutz '.$i,'slug'=>'tuerschutz'.$i,'pillar'=>'core','type'=>'page','wp_id'=>1000+$i,'parent'=>'core:world:schutz');
 $tree[$key]=array('id'=>$key,'name'=>'Schließzylinder '.$i,'slug'=>'schliesszylinder'.$i,'pillar'=>'core','type'=>'category','wp_id'=>2000+$i,'parent'=>$parent);
}
$tree['core:area:vers']=array('id'=>'core:area:vers','name'=>'Tarifbereiche','slug'=>'tarife','pillar'=>'core','type'=>'page','wp_id'=>4050,'parent'=>'core:world:versicherung');
for($i=1;$i<=20;$i++){
 $key='core:leaf:vers'.$i;
 $tree[$key]=array('id'=>$key,'name'=>'Rauchmelder Versicherung '.$i,'slug'=>'versicherung-'. $i,'pillar'=>'core','type'=>'category','wp_id'=>4100+$i,'parent'=>'core:area:vers');
}
for($i=1;$i<=5;$i++){
 $key='core:leaf:faq'.$i;
 $tree[$key]=array('id'=>$key,'name'=>'Schließzylinder: Häufige Fragen '.$i,'slug'=>'fragen-'.$i,'pillar'=>'core','type'=>'category','wp_id'=>4200+$i,'parent'=>'core:area:1');
}
for($i=1;$i<=4;$i++){
 $key='core:leaf:review'.$i;
 $tree[$key]=array('id'=>$key,'name'=>'Außenverkaufsstand Ausstattung '.$i,'slug'=>'review-'.$i,'pillar'=>'core','type'=>'category','wp_id'=>4300+$i,'parent'=>'core:area:1');
}
PPAR_HB_Integration::$fake_nodes=$tree;
$out=PPAR_HB_Integration::catalog();
expect(is_array($out),'original category catalog builds from active WP-style tree');
expect(count($out['business_concepts'])===80,'50-rule cap removed: all 80 unique material product concepts available');
expect(($out['hab_product_coverage_audit']['insurance_excluded']??0)===20,'20 insurance categories explicitly excluded');
expect(($out['hab_product_coverage_audit']['information_excluded']??0)===5,'five FAQ categories excluded');
expect(($out['hab_product_coverage_audit']['unclassified_review']??0)===4,'unknown product family kept for review, not falsely marked unavailable');
expect(($out['business_supply_contract']['required_count']??0)===80,'coverage denominator follows real eligible concepts, never 311');
$e=new HabIdealoCoverage();
$x=$e->idealo_hab_card_properties(array('brand_name'=>'ABUS','sub_category'=>'Schließzylinder'),'ABUS Türschloss Schließzylinder A93 NG 30/45 (86176)');
expect(strpos($x,'Marke: ABUS')!==false && strpos($x,'Maße: 30/45')!==false && strpos($x,'Art.-Nr.: 86176')!==false,'real brand, dimensions and model are displayed from feed/title');
$y=$e->idealo_hab_card_properties(array('brand_name'=>'VisorTech'),'VisorTech Elektronischer Tür-Schließzylinder (NX4349)');
expect(strpos($y,'NX4349')!==false && strpos($y,'VisorTech')!==false,'other authentic product attributes shown');
$z=$e->idealo_hab_card_properties(array(),'Frei erfundenes Objekt');
expect(strpos($z,'Maße:')===false && strpos($z,'Marke:')===false,'unknown attributes never invented');
$index=array();
foreach($out['business_concepts'] as $row){
 $id=$row['id'];$index[$id]=array('id'=>$id,'title'=>$row['title'],'main_hub'=>'Einbruch und Diebstahl');
}
$e->feedIndex(array('concepts'=>$index,'catalog'=>$out));
$e->s=array('last_matched_concept_ids'=>array_keys(array_slice($index,0,12,true)),'last_feed_rows_seen'=>250,'last_import_count'=>15,
 'last_feed_reject_stats'=>array('missing_gtin'=>100,'accepted'=>15));
$report=$e->idealo_hab_coverage_report();
expect($report['concept_count']===80&&$report['matched_count']===12&&$report['missing_count']===68,'honest current target denominator and uncovered concepts');
expect(($report['tree']['insurance_excluded']??0)===20,'insurance never enters denominator');
expect(($report['reasons']['missing_gtin']??0)===100,'feed rejection counts preserved in report');
expect(!isset($report['api_key']),'report contains no API secrets');
echo 'HAB_RC24_CATALOG_AUDIT_FEATURES_13_CASES_PASS'.PHP_EOL;
'''.replace("OTHER_METHODS",method).replace("METHODS",funcs)
 with TemporaryDirectory() as td:
  f=Path(td)/"qa.php";f.write_text(source)
  lint=run(["php","-l",str(f)],capture_output=True,text=True)
  assert lint.returncode==0,lint.stdout+lint.stderr
  result=run(["php",str(f)],capture_output=True,text=True)
  assert result.returncode==0,result.stdout+result.stderr
  print(result.stdout)
print('HAB_RC24_PLUGIN_LINT_25_PASS; 36 CRC PASS; SHA256',hashlib.sha256(p.read_bytes()).hexdigest())
