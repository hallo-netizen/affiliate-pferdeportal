#!/usr/bin/env python3
"""Execute the actual HAB iPN GZIP/CSV import method as a black-box with a
synthetic private test feed. Does not assert a REAL authorized feed was fetched."""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess,re
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
p=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(p) as z:
 src=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode()
 def extract(n):
  match=re.search(r"(?:private|public) function "+n+r"\s*\(",src)
  assert match,n
  st=match.start()
  op=src.index("{",match.end())
  depth=0
  for i in range(op,len(src)):
   if src[i]=="{":depth+=1
   elif src[i]=="}":
    depth-=1
    if depth==0:return src[st:i+1].replace("private function","public function",1)
  raise ValueError(n)
 names=["idealo_open_feed_stream","idealo_stream_close","idealo_normalize_gtins_from_values",
        "idealo_normalize_asins_from_values","idealo_import_feed_file"]
 methods="\n".join(extract(x) for x in names)
 harness=r'''<?php
class WP_Error {private $c;private $m;public function __construct($c,$m){$this->c=$c;$this->m=$m;}public function get_error_message(){return $this->m;}public function get_error_code(){return $this->c;}}
function is_wp_error($x){return $x instanceof WP_Error;}
function absint($v){return max(0,(int)$v);}
function sanitize_key($s){return strtolower(preg_replace('/[^a-z0-9_\-]/','',(string)$s));}
function sanitize_text_field($s){return trim((string)$s);}
function get_option($k,$default=array()){return $GLOBALS['options'][$k]??$default;}
function update_option($k,$v,$autoload=false){$GLOBALS['options'][$k]=$v;return true;}
function expect($ok,$message){if(!$ok){fwrite(STDERR,'FAIL '.$message.PHP_EOL);exit(4);}echo 'PASS '.$message.PHP_EOL;}
class ExistingHabProductPipeline {
  const OPTION_NETWORK_IDEALO='hab_idealo_test';
  public $synced=array();
  public $activationCalls=0;
  public $lastMaterialized=array();
  METHODS
  public function idealo_match_index(){return array('concepts'=>array('haustuerschloesser'=>array('id'=>'haustuerschloesser')));}
  public function idealo_match_feed_row_to_concept($row) {
    if(strpos((string)($row['product_title']??''),'Schließzylinder')===false){return array('status'=>'none');}
    return array('status'=>'matched','concept'=>array('id'=>'haustuerschloesser','main_hub'=>'Sicherheit','hub'=>'Haustürschlösser'),'score'=>280,'context'=>3);
  }
  public function idealo_direct_image_url($url) {
    $p=parse_url((string)$url);
    if(!is_array($p)||($p['scheme']??'')!=='https'||($p['host']??'')!=='cdn.idealo.com') return '';
    return $url;
  }
  public function network_sync_upsert_products($network,$parsed) {
    $this->synced[]=$parsed;
    return array('products'=>count($parsed['rows']),'pass'=>count($parsed['rows']),'warn'=>0);
  }
  public function idealo_settings(){return get_option(self::OPTION_NETWORK_IDEALO,array());}
  public function idealo_campaigns_should_be_active(){return !empty($this->idealo_settings()['enabled']) && in_array(($this->idealo_settings()['output_mode']??''),array('automatic','combined','separate','idealo_only'),true);}
  public function idealo_materialize_campaigns() {
    $this->lastMaterialized=$this->synced[count($this->synced)-1]['rows']??array();
    return array('campaigns'=>count($this->lastMaterialized),'targets'=>1);
  }
  public function idealo_sync_campaign_activation() {
    $this->activationCalls++;
    $s=$this->idealo_settings();
    expect(($s['output_mode']??'')==='automatic','activated only after real matching products are materialized');
  }
  public function provider_set_access_state($provider,$status,$message){return true;}
  public function idealo_credentials_present($settings){return !empty($settings['api_key'])&&!empty($settings['feed_id'])&&!empty($settings['adspace_id']);}
}
function makefile($rows) {
 $path=tempnam(sys_get_temp_dir(),'habgz');
 $head=array('id','product_title','product_deeplink','ean','gtins_product','asins_product','main_category','sub_category','brand_name','image_url','price');
 $fd=fopen('php://temp','w+');fputcsv($fd,$head);
 foreach($rows as $r) fputcsv($fd,$r);
 rewind($fd);$csv=stream_get_contents($fd);fclose($fd);
 file_put_contents($path,gzencode($csv,6));
 return $path;
}
$GLOBALS['options']=array('hab_idealo_test'=>array('enabled'=>true,'adspace_id'=>'568944','feed_id'=>'2901','api_key'=>'FAKE_TEST_KEY','output_mode'=>'ebay_only','link_strategy'=>'hybrid','last_import_at'=>0));
$a=new ExistingHabProductPipeline();
$f=makefile(array(
 array('1','ABUS Schließzylinder K25 30/30','https://ipn.idealo.de/ts/i001/tsc','4001234567890','4001234567890','B012345678','Schutz','Türschlösser','ABUS','https://cdn.idealo.com/test/image1.jpg','49.90'),
 array('2','GERCAR Schließzylinder 35/35','https://ipn.idealo.de/ts/i001/tsc','4001234567891','4001234567891','','Schutz','Türschlösser','GERCAR','https://cdn.idealo.com/test/image2.jpg','24.50'),
 array('3','Schließzylinder mit nicht freigegebenem Foto','https://ipn.idealo.de/ts/i001/tsc','4001234567892','4001234567892','','Schutz','Türschlösser','UNKNOWN','http://example.com/image.jpg','10.00'),
 array('4','Austernmesser Küchenzubehör','https://ipn.idealo.de/ts/i001/tsc','4001234567893','4001234567893','','Küche','Besteck','UNKNOWN','https://cdn.idealo.com/test/irrelevant.jpg','11.00')
));
$result=$a->idealo_import_feed_file($f,'synthetic test CSV.GZ');
unlink($f);
expect(!is_wp_error($result), 'actual GZIP parser + CSV mapping');
expect(count($a->synced)===1, 'single network import, no additional subsystem');
expect(count($a->synced[0]['rows'])===2, 'only two relevant licensed-image products accepted');
expect(($a->lastMaterialized[0]['__image_url']??'')==='https://cdn.idealo.com/test/image1.jpg','original product image passed to existing materializer');
expect(($a->lastMaterialized[0]['asins_product']??'')==='B012345678','source-backed Amazon ASIN retained for button matching');
expect($a->activationCalls===1, 'single centralized activation');
expect(($a->idealo_settings()['last_materialized_count']??-1)===2,'materialized status persisted');
expect(($a->idealo_settings()['output_mode']??'')==='automatic','temporary pre-import gate lifted only after matched feed rows');
expect(($a->idealo_settings()['link_strategy']??'')==='hybrid','existing other slot strategy remains unchanged');
echo 'HAB_FULL_FEED_SIMULATION_PASS - synthetic records only, real provider not yet contacted'.PHP_EOL;
'''.replace("METHODS",methods)
 with TemporaryDirectory() as t:
  f=Path(t)/"verify.php";f.write_text(harness)
  lint=subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
  assert lint.returncode==0,lint.stdout+lint.stderr
  test=subprocess.run(["php",str(f)],capture_output=True,text=True)
  assert test.returncode==0,test.stdout+test.stderr
  print(test.stdout)
