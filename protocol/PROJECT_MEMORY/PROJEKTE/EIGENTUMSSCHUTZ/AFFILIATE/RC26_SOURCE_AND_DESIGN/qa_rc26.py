#!/usr/bin/env python3
"""Acceptance of actual RC26 plugin ZIP: production feed auto-pick, strict mock
exclusion, source-change invalidation, preserved RC25 mapping and styling.
No live credentials are used. API fixtures are intentionally tests, not data.
"""
import re
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZipFile

P=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip")
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    a=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode("utf-8")
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode("utf-8")
    css=z.read("affiliate-portal-router/assets/frontend.css").decode("utf-8")
    assert "Version: 0.1.23-rc26" in main
    assert "border:0!important;overflow:visible!important" in main
    assert "border:1px solid #d2dbd5!important;overflow:hidden!important" not in main
    assert "last_catalog_signature" in a and "last_feed_reject_stats" in a
    assert "['feed_id'] = '2901'" not in a
    assert "hb_mock_feed_forbidden" in a
    assert "idealo_hab_available_feeds" in a
    assert "api_feed_inventory" in a
    assert "background:#FAF8F4!important" in css and "color:#B35C40!important" in css
    assert "border-radius:1px!important" in css and "margin-bottom:32px!important" in css
    assert "border:0!important" in css[css.index("/* HAB RC26 only:"):]
    assert "Alle" not in a[a.index("iPN-Feedvergleich"):a.index("iPN-Feedvergleich")+250]
    # Extract actual PHP functions from built ZIP, not copies of reimplemented rules.
    def method(name):
        pat=r"    (?:private|public) function "+re.escape(name)+r"\([^)]*\)\s*\{.*?^    \}"
        m=re.search(pat,a,re.M|re.S)
        assert m,name
        return m.group(0)
    fnames=[
      "idealo_hab_available_feeds",
      "idealo_hab_feed_is_mock",
      "idealo_hab_feed_is_standard",
      "idealo_hab_clear_feed_results",
      "idealo_find_feed_metadata",
      "idealo_provider_access_test",
    ]
    extracted="\n".join(method(name) for name in fnames)
    assert "idealo_hab_feed_is_standard" in extracted
    with tempfile.TemporaryDirectory() as td:
        files=[p for p in z.namelist() if p.endswith(".php")]
        assert len(files)==25,len(files)
        for name in files:
            target=Path(td)/name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(z.read(name))
            r=subprocess.run(["php","-l",str(target)],capture_output=True,text=True)
            assert r.returncode==0,(name,r.stdout,r.stderr)
        php=r'''<?php
class WP_Error {
    public $code; public $message;
    function __construct($code,$message=""){ $this->code=$code; $this->message=$message; }
    public function get_error_message(){return $this->message;}
}
function is_wp_error($v){return $v instanceof WP_Error;}
function absint($v){return abs((int)$v);}
function sanitize_text_field($v){return trim((string)$v);}
function add_query_arg($parts,$url){return $url.'?'.http_build_query($parts);}
function wp_remote_retrieve_response_code($v){return $v['code']??500;}
function wp_remote_retrieve_body($v){return $v['body']??'';}
function update_option($k,$s,$a=false){$GLOBALS['settings']=$s;}
function probe($v,$message){if(!$v){fwrite(STDERR,"FAILED ".$message."\n");exit(1);}echo "PASS ".$message."\n";}
class OriginalIdealoTest {
    const OPTION_NETWORK_IDEALO='existing_option';
    public function idealo_settings(){return $GLOBALS['settings'];}
    private function idealo_credentials_present($s){return !empty($s['api_key'])&&!empty($s['adspace_id'])&&!empty($s['feed_id']);}
    private function idealo_partner_api_base(){return 'https://api.ingenious.cloud';}
    private function idealo_partner_api_post($url,$key){
        $GLOBALS['api_calls']++;
        if(!empty($GLOBALS['bad_api']))return new WP_Error('offline','offline');
        return array('code'=>200,'body'=>json_encode(array(
           'entries'=>$GLOBALS['feeds'],'totalPages'=>1)));
    }
    public function provider_set_access_state($provider,$status,$message){
        $GLOBALS['access_status']=$status;
    }
''' + extracted + r'''
}
$GLOBALS['settings']=array(
  'enabled'=>true,'api_key'=>'FAKE_FIXTURE_KEY','adspace_id'=>'568944',
  'feed_id'=>'2901','last_import_at'=>100,'last_import_count'=>1799,
  'last_catalog_signature'=>'old','last_remote_file_hash'=>'old',
  'feed_etag'=>'old-etag','feed_url'=>'old_url',
  'refresh_state'=>'success');
$GLOBALS['feeds']=array(
 array('feedId'=>2901,'name'=>'Mock Data Feed Fashion Sport Auto',
     'numberOfProducts'=>800,'lastFileHash'=>'testhash'),
 array('feedId'=>3007,'name'=>'Standard Datafeed',
     'numberOfProducts'=>2901,'lastFileHash'=>'prodhash'));
$GLOBALS['api_calls']=0;
$p=new OriginalIdealoTest();
$test=$p->idealo_provider_access_test(null,'idealo','v1');
probe(!is_wp_error($test) && $test['metadata']['feed_id']==='3007',
    'Select ONLY verified production Standard Datafeed from same adspace');
probe($GLOBALS['settings']['feed_id']==='3007'
  && $GLOBALS['settings']['last_import_at']===0
  && $GLOBALS['settings']['last_catalog_signature']===''
  && $GLOBALS['settings']['feed_url']==='',
    'Changing feed invalidates stale public import, cache and saved URL');
probe(count($GLOBALS['settings']['api_feed_inventory'])===2
  && $GLOBALS['settings']['api_feed_inventory'][0]['mock']===true
  && $GLOBALS['settings']['api_feed_inventory'][1]['mock']===false,
    'Show both real provider feeds, mark mock as EXCLUDED');
$meta=$p->idealo_find_feed_metadata($GLOBALS['settings']);
probe($meta['name']==='Standard Datafeed' && $meta['number_of_products']===2901,
    'Refresh reads only the authorized active production feed');
$bad=$GLOBALS['settings'];$bad['feed_id']='2901';
$meta=$p->idealo_find_feed_metadata($bad);
probe(is_wp_error($meta)&&$meta->code==='hb_mock_feed_forbidden',
    'Production refresh REJECTS a selected mock feed');
$state=$GLOBALS['settings'];
$test=$p->idealo_provider_access_test(null,'idealo','v1');
probe(!is_wp_error($test)&&$GLOBALS['settings']['feed_id']===$state['feed_id'],
    'Repeated check does not switch source or reset a good import');
$GLOBALS['feeds']=array(
 array('feedId'=>5000,'name'=>'Mock Data Feed Fashion Sport Auto'),
 array('feedId'=>5001,'name'=>'Sample Feed Fashion'));
$GLOBALS['settings']['feed_id']='5000';
$test=$p->idealo_provider_access_test(null,'idealo','v1');
probe(is_wp_error($test) && $test->code==='hb_no_production_feed'
  && $GLOBALS['access_status']==='failed',
    'Mock-only account fails closed; no guessed Standard feed');
$GLOBALS['feeds']=array(
 array('feedId'=>6101,'name'=>'Standarddatenfeed','numberOfProducts'=>1900),
 array('feedId'=>6102,'name'=>'Mock Data Feed Fashion Sport Auto'));
$GLOBALS['settings']['feed_id']='6102';
$test=$p->idealo_provider_access_test(null,'idealo','v1');
probe(!is_wp_error($test) && $GLOBALS['settings']['feed_id']==='6101',
    'Recognize German Standarddatenfeed variant');
$GLOBALS['bad_api']=true;
$prior=$GLOBALS['settings']['feed_id'];
$test=$p->idealo_provider_access_test(null,'idealo','v1');
probe(is_wp_error($test) && $GLOBALS['settings']['feed_id']===$prior,
    'Provider API error does not switch source');
echo "HAB_RC26_SOURCE_INTEGRATION_PASS\n";
'''
        script=Path(td)/"test.php"
        script.write_text(php)
        r=subprocess.run(["php",str(script)],capture_output=True,text=True)
        print(r.stdout)
        assert r.returncode==0,(r.stderr,r.stdout)
        print("HAB_RC26_PHP_LINT_PASS",len(files))
print("HAB_RC26_COMPLETE_QA_PASS")
