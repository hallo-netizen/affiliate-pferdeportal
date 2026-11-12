#!/usr/bin/env python3
"""Test real functions extracted from candidate HAB-only PHP, no fake public PASS."""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess,re,hashlib
base=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
p=base/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(p) as z:
 assert z.testzip() is None and len(z.namelist())==36
 a=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode()
 m=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
 css=z.read("affiliate-portal-router/assets/frontend.css").decode()
 assert "Version: 0.1.20-rc23" in m
 assert "hb_insurance_scope" in m
 assert "ppar-hb-category-products-grid" in css
 assert "multiprovider_matching_offers_for_banner" in m
 assert "image_url" in a and "idealo_materialize_campaigns()" in a
 with TemporaryDirectory() as tmp:
   files=[n for n in z.namelist() if n.endswith(".php")]
   assert len(files)==25
   for i,name in enumerate(files):
     f=Path(tmp)/f"{i}.php"; f.write_bytes(z.read(name))
     code=subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
     assert code.returncode==0,(name,code.stdout+code.stderr)
 def extract(name):
  hit=re.search(r'(?:private|public) function '+re.escape(name)+r'\s*\(',a)
  assert hit,name
  start=hit.start(); opening=a.index("{",hit.end());level=0
  for i in range(opening,len(a)):
   if a[i]=="{": level+=1
   elif a[i]=="}":
    level-=1
    if level==0:return a[start:i+1].replace("private function","public function",1)
  raise ValueError(name)
 extracted="\n".join(extract(n) for n in [
  "idealo_credentials_present","idealo_partner_api_base","idealo_validate_feed_url",
  "hb_idealo_feed_source_ready","hb_idealo_feed_download_url",
  "idealo_standalone_campaign_allowed"
 ])
 fixture=r'''<?php
class WP_Error {private $code;private $message;public function __construct($code,$msg){$this->code=$code;$this->message=$msg;} public function get_error_code(){return $this->code;} public function get_error_message(){return $this->message;}}
function is_wp_error($o){return $o instanceof WP_Error;}
function absint($v){return max(0,(int)$v);}
function wp_parse_url($v){return parse_url($v);}
function wp_http_validate_url($v){$x=parse_url($v);return is_array($x)&&($x['scheme']??'')==='https'&&!empty($x['host']);}
function sanitize_key($v){return strtolower(preg_replace('/[^a-z0-9_\-]/','',(string)$v));}
function esc_url_raw($v){return $v;}
function add_query_arg($a,$url){return $url.'?'.http_build_query($a);}
class TestIdealo {
 public $s=array();
 METHODS
 public function idealo_settings(){return $this->s;}
 public function idealo_link_strategy(){return $this->s['link_strategy']??'hybrid';}
 public function idealo_campaign_surface_kind($a){return $a['kind']??'product';}
}
function expect($ok,$name){if(!$ok){fwrite(STDERR,"FAILED ".$name.PHP_EOL);exit(1);}echo "PASS ".$name.PHP_EOL;}
$c=new TestIdealo();
$c->s=array('enabled'=>true,'adspace_id'=>'568944','feed_id'=>'2901','api_key'=>'TEST-SECRET-NOT-REAL','api_last_checked_at'=>1780000000,'feed_url'=>'','link_strategy'=>'hybrid');
expect($c->hb_idealo_feed_source_ready(),'Hab confirmed API ready without manual URL');
$url=$c->hb_idealo_feed_download_url($c->s);
expect(is_string($url)&&str_contains($url,'https://api.ingenious.cloud/creatives/productdata/export?'),'official documented export endpoint');
$q=array();parse_str(parse_url($url,PHP_URL_QUERY),$q);
expect(($q['apiKey']??'')==='TEST-SECRET-NOT-REAL'&&($q['feedId']??'')==='2901'&&($q['adspaceId']??'')==='568944','exact credential-adspace-feed binding');
expect(($q['format']??'')==='CSV'&&($q['compression']??'')==='GZIP'&&($q['csvSeparator']??'')==='COMMA','canonical importer-compatible compressed CSV');
expect(($c->s['feed_url']??'')==='','never saves API-key export URL in options');
$x=$c->s; $x['adspace_id']='568313';
expect(is_wp_error($c->hb_idealo_feed_download_url($x)),'other portal rejected');
$x=$c->s; $x['api_last_checked_at']=0;
expect(!$c->hb_idealo_feed_source_ready($x),'unverified API blocked');
$x=$c->s; $x['enabled']=false;
expect(!$c->hb_idealo_feed_source_ready($x),'disabled provider blocked');
$x=$c->s; $x['feed_url']='https://api.ingenious.cloud/creatives/productdata/export?feedId=2901';
expect($c->hb_idealo_feed_download_url($x)===$x['feed_url'],'manual original fallback preserved');
$offer=array('network'=>'idealo','kind'=>'product');
expect($c->idealo_standalone_campaign_allowed($offer,'category_product_1'),'image-backed product used at category1');
expect($c->idealo_standalone_campaign_allowed($offer,'category_product_2'),'image-backed product used at category2');
expect(!$c->idealo_standalone_campaign_allowed($offer,'post_bottom_products'),'hybrid outside categories unchanged');
expect(!$c->idealo_standalone_campaign_allowed(array('network'=>'idealo','kind'=>'comparison'),'category_product_1'),'generic comparison cannot replace concrete category product');
expect($c->idealo_standalone_campaign_allowed(array('network'=>'idealo','kind'=>'comparison'),'post_bottom_products'),'normal comparison unaffected');
echo "HAB_FULL_CARD_SOURCE_TESTS_PASS 13 tests".PHP_EOL;
'''.replace("METHODS",extracted)
 with TemporaryDirectory() as tmp:
   file=Path(tmp)/"check.php";file.write_text(fixture)
   lint=subprocess.run(["php","-l",str(file)],capture_output=True,text=True)
   assert lint.returncode==0,lint.stdout+lint.stderr
   run=subprocess.run(["php",str(file)],capture_output=True,text=True)
   assert run.returncode==0,run.stdout+run.stderr
   print(run.stdout)
 # Reuse original RC21 actual category template integration tests after adapting version.
 o=(base/"AFFILIATE/IMPLEMENTIERUNG_RC21_CATEGORY_CARDS/qa_rc21.py").read_text()
 o=o.replace("0.1.18-rc21","0.1.20-rc23")
 with TemporaryDirectory() as tmp:
   q=Path(tmp)/"old_category_test.py";q.write_text(o)
   run=subprocess.run(["python3",str(q)],capture_output=True,text=True)
   assert run.returncode==0,run.stdout+run.stderr
   print(run.stdout)
print("HAB_SOURCE_ONLY_PASS; production feed and live multi-provider NOT yet verified")
print("CANDIDATE_SHA256",hashlib.sha256(p.read_bytes()).hexdigest())
