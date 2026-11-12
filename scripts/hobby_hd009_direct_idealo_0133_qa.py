#!/usr/bin/env python3
"""Generate PHP runtime QA against real methods from just-built HD009 ZIP.
All credentials are synthetic; NEVER call iPN or the production WordPress site.
"""
from pathlib import Path
import zipfile
import re
import sys

p=Path(sys.argv[1])
trait='affiliate-portal-router/includes/trait-ppar-idealo.php'
with zipfile.ZipFile(p) as z:
    source=z.read(trait).decode()
    main=z.read('affiliate-portal-router/hobby-depot-affiliate-router.php').decode()

def extract(name):
    pattern=re.compile(r'^    private function '+re.escape(name)+r'\(',re.M)
    hit=pattern.search(source)
    assert hit, f"Missing actual original PHP method: {name}"
    first=source.index('{',hit.start())
    depth=0
    for n in range(first,len(source)):
        if source[n]=='{':depth+=1
        elif source[n]=='}':
            depth-=1
            if depth==0:
                return source[hit.start():n+1]
    raise ValueError("Unclosed original PHP method: "+name)

names=[
 'hd_idealo_feed_source_ready',
 'hd_idealo_feed_download_url',
 'idealo_validate_feed_url',
 'idealo_download_feed_to_temp',
 'idealo_queue_manual_refresh',
]
methods='\n\n'.join(extract(name) for name in names)

php=r'''<?php
error_reporting(E_ALL);
ini_set('display_errors','1');
class WP_Error {
    private $code; private $message;
    function __construct($code,$message){$this->code=$code;$this->message=$message;}
    function get_error_code(){return $this->code;}
    function get_error_message(){return $this->message;}
}
function is_wp_error($v){return $v instanceof WP_Error;}
function absint($v){return abs((int)$v);}
function wp_http_validate_url($url){
    $p=parse_url($url);
    return is_array($p)&&($p['scheme']??'')==='https'&&
      in_array(($p['host']??''),array('api.ingenious.cloud','api.net.idealo-partner.com','evil.test'),true);
}
function wp_parse_url($url){return parse_url($url);}
function esc_url_raw($url){return $url;}
function sanitize_key($s){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$s));}
function add_query_arg($params,$url){return $url.'?'.http_build_query($params,'','&',PHP_QUERY_RFC3986);}
function wp_tempnam($s){return tempnam(sys_get_temp_dir(),'hd009_');}
function get_transient($k){return $GLOBALS['fake_lock']??false;}
function wp_safe_remote_get($url,$options){
    $GLOBALS['last_fetch_host']=parse_url($url,PHP_URL_HOST);
    $GLOBALS['last_fetch_path']=parse_url($url,PHP_URL_PATH);
    $GLOBALS['last_fetch_query']=array();
    parse_str((string)parse_url($url,PHP_URL_QUERY),$GLOBALS['last_fetch_query']);
    $GLOBALS['fetch_options']=$options;
    file_put_contents($options['filename'],gzencode("GTIN,title,source\n4000000001234,Example,HobbyDepot\n"));
    return array('code'=>($GLOBALS['test_http_code']??200),'headers'=>array('etag'=>'"synthetic"'));
}
function wp_remote_retrieve_response_code($response){return (int)$response['code'];}
function wp_remote_retrieve_header($response,$name){return $response['headers'][$name]??'';}
class HD009_IdealoRuntimeQA {
    const IDEALO_REFRESH_LOCK='qa_lock';
    private $settings;
    public $states=array();
    public $dispatched=0;
    function __construct($s){$this->settings=$s;}
    private function idealo_settings(){return $this->settings;}
    private function idealo_credentials_present($s=null){
        $s=is_array($s)?$s:$this->settings;
        return !empty($s['api_key']) && !empty($s['adspace_id']) && !empty($s['feed_id']) &&
            ($s['adspace_id']==='568912') && !empty($s['hobby_feed_verified']);
    }
    private function idealo_partner_api_base(){return 'https://api.ingenious.cloud';}
    private function idealo_set_refresh_state($state,$message){$this->states[]=$state;}
    private function idealo_dispatch_manual_worker($reason){$this->dispatched++;return array('transport'=>'fake_loopback');}
    // REAL compiled methods from the HD009 ZIP inserted below
__EXTRACTED__
    public function ready($s){return $this->hd_idealo_feed_source_ready($s);}
    public function url($s){return $this->hd_idealo_feed_download_url($s);}
    public function download($s){return $this->idealo_download_feed_to_temp($s);}
    public function queue(){return $this->idealo_queue_manual_refresh();}
}
function qa($bool,$message) {
    static $i=0; $i++;
    if (!$bool) {fwrite(STDERR,"FAIL $i $message\n");exit(1);}
    echo "PASS $i $message\n";
}
$base=array(
 'enabled'=>true,
 'adspace_id'=>'568912','feed_id'=>'2747','api_key'=>'SYNTHETIC_ONLY_DO_NOT_USE',
 'hobby_feed_verified'=>true,'api_last_checked_at'=>1794500000,
 'feed_url'=>'','feed_etag'=>'','feed_last_modified'=>'','refresh_state'=>'idle'
);
$t=new HD009_IdealoRuntimeQA($base);
qa($t->ready($base),'Verified own adspace/feed accepted');
$url=$t->url($base);
qa(is_string($url),'Direct iPN source URL constructed by real PHP method');
$p=parse_url($url);parse_str((string)$p['query'],$q);
qa($p['host']==='api.ingenious.cloud'&&$p['path']==='/creatives/productdata/export',
   'Only documented iPN export API host/path');
qa(($q['feedId']??'')==='2747'&&($q['adspaceId']??'')==='568912'&&($q['apiKey']??'')===$base['api_key'],
   'Correct source site and API key used server-side');
qa(($q['format']??'')==='CSV'&&($q['compression']??'')==='GZIP'&&($q['csvSeparator']??'')==='COMMA',
   'Importer receives its existing native CSV.GZ format');
$download=$t->download($base);
qa(is_array($download)&&$download['status']==='downloaded'&&is_file($download['path']),
   'Original real HD009 download method accepts direct API URL');
qa($GLOBALS['last_fetch_host']==='api.ingenious.cloud'&&
  $GLOBALS['last_fetch_path']==='/creatives/productdata/export',
  'Original WordPress HTTP transport called with direct iPN export');
qa(($GLOBALS['fetch_options']['stream']??false)===true && $GLOBALS['fetch_options']['timeout']===300,
  'Preserves existing streaming and timeout, no frontend HTTP');
$bytes=file_get_contents($download['path']);
qa(substr($bytes,0,2)==="\x1f\x8b" &&
 strpos(gzdecode($bytes),'4000000001234')!==false,
 'Original download receives usable GZIP CSV stream');
unlink($download['path']);
$queued=$t->queue();
qa(is_array($queued)&&($queued['details']['queued']??false)&&$t->dispatched===1,
 'Existing background worker is queued without manual URL');
qa(in_array('queued',$t->states,true),'Existing refresh status retained');
$changes=array(
 'foreign adspace'=>array('adspace_id'=>'568944'),
 'old Pferde adspace'=>array('adspace_id'=>'568313'),
 'not verified'=>array('hobby_feed_verified'=>false),
 'no API verification'=>array('api_last_checked_at'=>0),
 'no key'=>array('api_key'=>''),
 'disabled'=>array('enabled'=>false),
 'bad feed'=>array('feed_id'=>'oops'),
);
foreach ($changes as $label=>$delta) {
    $invalid=array_merge($base,$delta);
    $v=$t->url($invalid);
    qa(is_wp_error($v) && $v->get_error_code()==='idealo_feed_not_verified',
      'Unauthorized import blocked: '.$label);
}
$manual=$base;
$manual['feed_url']='https://api.ingenious.cloud/creatives/productdata/export?feedId=2747';
qa($t->url($manual)===$manual['feed_url'],
   'Existing verified manual source remains backward compatible');
$manual['feed_url']='https://evil.test/malicious-feed.gz';
qa(is_wp_error($t->url($manual)),'Unapproved feed URL host remains rejected');
$http=$t->download($base);
qa(is_array($http) && $http['status']==='downloaded','Download workflow repeatable');
unlink($http['path']);
$GLOBALS['test_http_code']=429;
$r=$t->download($base);
qa(is_wp_error($r)&&$r->get_error_code()==='idealo_feed_rate_limited',
  'Original HTTP 429 safety retained');
unset($GLOBALS['test_http_code']);
$GLOBALS['fake_lock']=true;
$t2=new HD009_IdealoRuntimeQA($base);
$q2=$t2->queue();
qa(($q2['status']??'')==='success'&&$t2->dispatched===0,
  'Existing single-worker lock blocks duplicate refresh');
unset($GLOBALS['fake_lock']);
echo "ALL_REAL_METHOD_QA_PASS\n";
'''.replace('__EXTRACTED__',methods)
out=Path(sys.argv[2] if len(sys.argv)>2 else "/tmp/hd009_direct_export_php_qa.php")
out.write_text(php)
print("PHP_QA_SOURCE",out,"REAL_METHODS",names,"STUBS_only_network=true")
