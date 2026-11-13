#!/usr/bin/env python3
"""Exercise ACTUAL RC27 PHP with the exact iPN counts seen on 13 November.
Check: preserve good existing import; never auto-switch to 548821 fashion feed;
honor deliberate verified source switch; never infer 0 from metadata means empty.
"""
from pathlib import Path
from zipfile import ZipFile
import re, subprocess, tempfile
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None and len(z.namelist())==36
    names=[n for n in z.namelist() if n.endswith(".php")]
    assert len(names)==25
    for name in names:
        path=Path(td)/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(z.read(name))
        r=subprocess.run(["php","-l",str(path)],capture_output=True,text=True)
        assert r.returncode==0,(name,r.stderr)
    trait=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode()
    assert "if (count($standards)===1) $selected=$standards[0];" not in trait
    assert "0 Produkte laut Partner-API" not in trait
    assert "Das sind keine Produktzahlen je Feed" in trait
    assert "nur für Hab & Bewahr freigegebene Quellen" in trait
    assert "Mock/Test ausgeschlossen." in trait
    assert "href=" in trait and "last_catalog_signature" in trait
    main=z.read("affiliate-portal-router/affiliate-portal-router.php")
    assert b"Version: 0.1.24-rc27" in main

    def method(name):
        match=re.search(r"    (?:public|private) function "+re.escape(name)+r"\([^)]*\)\s*\{.*?^    \}",trait,re.M|re.S)
        assert match,name
        return match.group(0)
    methods="\n".join(method(x) for x in (
        "idealo_hab_available_feeds","idealo_hab_feed_is_mock",
        "idealo_hab_feed_is_standard","idealo_hab_clear_feed_results",
        "idealo_provider_access_test","idealo_find_feed_metadata"))
    php=r'''<?php
class WP_Error {
  public $code; public $message;
  function __construct($code,$message=''){ $this->code=$code;$this->message=$message; }
  function get_error_message(){return $this->message;}
}
function is_wp_error($v){return $v instanceof WP_Error;}
function absint($x){return abs((int)$x);}
function sanitize_text_field($x){return trim((string)$x);}
function add_query_arg($q,$url){return $url.'?'.http_build_query($q);}
function wp_remote_retrieve_response_code($r){return (int)($r['code']??500);}
function wp_remote_retrieve_body($r){return $r['body']??'';}
function update_option($k,$settings,$autoload=false){$GLOBALS['s']=$settings;}
function ok($condition,$label){if(!$condition){fwrite(STDERR,"FAIL: ".$label."\n");exit(1);}echo "PASS: ".$label."\n";}
class RealSourceTest {
  const OPTION_NETWORK_IDEALO='existing-idealo-option';
  public function idealo_settings(){return $GLOBALS['s'];}
  public function inspect($s){return $this->idealo_find_feed_metadata($s);}
  private function idealo_credentials_present($s) {return !empty($s['api_key'])&&!empty($s['adspace_id'])&&!empty($s['feed_id']);}
  private function idealo_partner_api_base(){return 'https://api.ingenious.cloud';}
  private function idealo_partner_api_post($url,$key) {
    return array('code'=>200,'body'=>json_encode(array('entries'=>$GLOBALS['feeds'],'totalPages'=>1)));
  }
  public function provider_set_access_state($id,$status,$msg){$GLOBALS['access']=$status;}
''' + methods + r'''
}
$GLOBALS['feeds']=array(
 array('feedId'=>2747,'name'=>'Datafeed Fashion, Sport, Outdoor',
       'numberOfProducts'=>548821,'lastFileHash'=>'fashionhash'),
 array('feedId'=>2901,'name'=>'Standard Datafeed',
       'numberOfProducts'=>0,'lastFileHash'=>'standardhash'));
$GLOBALS['s']=array('enabled'=>true,'api_key'=>'FAKE_TEST','adspace_id'=>'568944',
 'feed_id'=>'2901','last_import_at'=>100,'last_import_count'=>1949,
 'last_remote_file_hash'=>'standardhash','last_catalog_signature'=>'abc',
 'last_feed_rows_seen'=>2194075,'refresh_state'=>'unchanged');
$p=new RealSourceTest();
$r=$p->idealo_provider_access_test(null,'idealo','v1');
ok(!is_wp_error($r),'Real API case accepted');
ok((string)$GLOBALS['s']['feed_id']==='2901'
  && $GLOBALS['s']['last_import_count']===1949
  && $GLOBALS['s']['last_import_at']===100,
  'Keep previously verified imported feed despite 0 metadata');
ok(strpos($GLOBALS['s']['api_last_message'],'1949')!==false
  && strpos($GLOBALS['s']['api_last_message'],'0 Produkte')!==false,
  'Report both API count and real staged rows without inventing an explanation');
ok(count($GLOBALS['s']['api_feed_inventory'])===2
  && $GLOBALS['s']['api_feed_inventory'][0]['mock']===false,
  'Fashion Sport Outdoor is a REAL feed, NOT an invented mock');
$meta=$p->inspect($GLOBALS['s']);
ok(!is_wp_error($meta) && $meta['feed_id']==='2901',
  'Current source matches actual selected source');
$GLOBALS['s']['feed_id']='2747';
$GLOBALS['s']['last_import_at']=0;
$GLOBALS['s']['last_import_count']=0;
$r=$p->idealo_provider_access_test(null,'idealo','v1');
ok(!is_wp_error($r) && $GLOBALS['s']['feed_id']==='2747',
  'Explicitly chosen AUTHORIZED alternative is NOT overwritten by Standard name');
$meta=$p->inspect($GLOBALS['s']);
ok(!is_wp_error($meta) && $meta['number_of_products']===548821,
  'Alternative source metadata is real and kept distinct');
$GLOBALS['s']['feed_id']='99999';
$r=$p->idealo_provider_access_test(null,'idealo','v1');
ok(is_wp_error($r) && $r->code==='hb_no_production_feed',
  'Unknown source is not guessed from an empty Standard feed');
$GLOBALS['feeds']=array(
 array('feedId'=>2747,'name'=>'Mock Data Feed Fashion, Sport, Outdoor',
       'numberOfProducts'=>548821),
 array('feedId'=>2901,'name'=>'Standard Datafeed',
       'numberOfProducts'=>0));
$GLOBALS['s']['feed_id']='2747';
$r=$p->idealo_provider_access_test(null,'idealo','v1');
ok(is_wp_error($r) && $r->code==='hb_no_production_feed',
  'Mock-only candidate rejected and zero-count Standard not auto-switched');
echo "HAB_RC27_REAL_METADATA_INTEGRATION_PASS\n";
'''
    script=Path(td)/"harness.php"
    script.write_text(php)
    res=subprocess.run(["php",str(script)],capture_output=True,text=True)
    print(res.stdout)
    assert res.returncode==0,(res.stderr,res.stdout)
    print("HAB_RC27_LINT_PASS",len(names))
print("HAB_RC27_FULL_QA_PASS")
