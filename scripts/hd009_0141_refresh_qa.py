#!/usr/bin/env python3
"""Execute ORIGINAL PHP worker/schedule/activation against a deterministic mock WP.

No real Feed or WordPress credentials. Tests hash-unchanged revision upgrade,
HTTP304, one-shot scheduling, last-good refresh, and non-repetition.
"""
from zipfile import ZipFile
from pathlib import Path
import re,sys

source=Path(sys.argv[1]);dest=Path(sys.argv[2])
with ZipFile(source) as z:
    s=z.read('affiliate-portal-router/includes/trait-ppar-idealo.php').decode()
def method(n):
    m=re.search(r'^    (?:private|public|protected) function '+re.escape(n)+r'\(',s,re.M)
    assert m,n
    rest=s[m.end():]; nxt=re.search(r'^    (?:private|public|protected) function ',rest,re.M)
    return s[m.start():m.end()+nxt.start()] if nxt else s[m.start():]
methods='\n'.join(method(n) for n in [
    'idealo_match_contract_revision',
    'idealo_campaigns_should_be_active',
    'idealo_ensure_refresh_schedule',
    'idealo_refresh_remote_feed'
])
php=r'''<?php
error_reporting(E_ALL);ini_set('display_errors','1');
define('HOUR_IN_SECONDS',3600);
class WP_Error{
  private $code,$message;
  public function __construct($code,$message){$this->code=$code;$this->message=$message;}
  public function get_error_code(){return $this->code;}
  public function get_error_message(){return $this->message;}
}
function is_wp_error($x){return $x instanceof WP_Error;}
function absint($n){return abs((int)$n);}
function update_option($k,$v,$autoload=false){$GLOBALS['settings']=$v;return true;}
function wp_next_scheduled($hook){return $GLOBALS['cron'][$hook]??false;}
function wp_schedule_single_event($stamp,$hook){$GLOBALS['cron'][$hook]=$stamp;$GLOBALS['one_shots']++;return true;}
function wp_schedule_event($stamp,$freq,$hook){$GLOBALS['cron'][$hook]=$stamp;$GLOBALS['recurring']++;return true;}
function wp_clear_scheduled_hook($hook){unset($GLOBALS['cron'][$hook]);return true;}
function get_transient($key){return false;}
class RealHD009Worker {
 const OPTION_NETWORK_IDEALO='real_test_option';
 const IDEALO_REFRESH_HOOK='ppar_idealo_refresh_v1';
 const IDEALO_MANUAL_REFRESH_HOOK='ppar_idealo_manual_refresh_v1';
 private function idealo_settings(){return $GLOBALS['settings'];}
 private function idealo_credentials_present($s){return !empty($s['api_key'])&&($s['adspace_id']??'')==='568912';}
 private function idealo_sanitize_output_mode($v){return (string)$v;}
 private function hd_idealo_feed_source_ready($s){return !empty($s['hobby_feed_verified']) && $this->idealo_credentials_present($s);}
 private function idealo_find_feed_metadata($s){$GLOBALS['metadata_reads']++;return array('last_file_hash'=>$GLOBALS['remote_hash'],'last_updated_at'=>'now','number_of_products'=>540000,'advertiser_name'=>'idealo');}
 private function idealo_download_feed_to_temp($s){
   $GLOBALS['download_reads']++;$GLOBALS['download_arguments']=$s;
   if ($GLOBALS['download_mode']==='304') return array('status'=>'not_modified','etag'=>'"new"','last_modified'=>'today');
   if ($GLOBALS['download_mode']==='fail') return new WP_Error('download_failed','No feed today');
   $p=tempnam(sys_get_temp_dir(),'hd0141');
   file_put_contents($p,'synthetic');
   return array('status'=>'downloaded','path'=>$p,'etag'=>'"new"','last_modified'=>'today');
 }
 private function idealo_import_feed_file($path,$name){
   $GLOBALS['imports']++;
   if (!is_file($path)) return new WP_Error('missing','No downloaded file');
   $GLOBALS['settings']['last_match_revision']=$this->idealo_match_contract_revision();
   $GLOBALS['settings']['last_import_at']=time();
   return array('status'=>'success','message'=>'Import with full match');
 }
__METHODS__
 public function active(){return $this->idealo_campaigns_should_be_active();}
 public function schedule(){return $this->idealo_ensure_refresh_schedule();}
 public function refresh(){return $this->idealo_refresh_remote_feed(true);}
}
function ck($condition,$msg){static $n=0;$n++;if(!$condition){fwrite(STDERR,"FAIL $n $msg\n");exit(1);}echo "PASS $n $msg\n";}
$GLOBALS['cron']=array();$GLOBALS['one_shots']=0;$GLOBALS['recurring']=0;
$GLOBALS['metadata_reads']=0;$GLOBALS['download_reads']=0;$GLOBALS['imports']=0;
$GLOBALS['remote_hash']='abcdef';$GLOBALS['download_mode']='downloaded';
$GLOBALS['settings']=array(
 'enabled'=>true,'api_key'=>'DUMMY','hobby_feed_verified'=>true,
 'adspace_id'=>'568912','feed_id'=>'2747','output_mode'=>'combined',
 'last_import_feed_id'=>'2747','last_import_adspace_id'=>'568912',
 'last_remote_file_hash'=>'abcdef','last_import_at'=>time()-47*HOUR_IN_SECONDS,
 'api_last_checked_at'=>time()-200,'feed_etag'=>'"old"','feed_last_modified'=>'yesterday',
 'auto_refresh'=>true
);
$w=new RealHD009Worker();
ck(!$w->active(),'Old stale-rule campaigns must not publish during one-time recalculation');
$w->schedule();
ck($GLOBALS['one_shots']===1&&$GLOBALS['recurring']===1,'Exactly one existing one-shot worker and the existing recurring worker');
$w->schedule();
ck($GLOBALS['one_shots']===1&&$GLOBALS['recurring']===1,'A second init event must not duplicate any worker');
$r=$w->refresh();
ck(!is_wp_error($r)&&$GLOBALS['imports']===1,'New matching revision forces full import even if remote hash did not change');
ck($GLOBALS['download_reads']===1&&($GLOBALS['download_arguments']['feed_etag']??'x')===''&&($GLOBALS['download_arguments']['feed_last_modified']??'x')==='','New matching rules bypass old ETag/LastModified');
ck(($GLOBALS['settings']['last_match_revision']??'')==='hd009-match-0.1.41','Single import is now authoritative for the matching revision');
ck($w->active(),'Original activation gate admits newly matched 2747 campaigns');
$last=$GLOBALS['settings']['last_import_at'];
$r=$w->refresh();
ck(($r['status']??'')==='unchanged' && $GLOBALS['imports']===1 && $GLOBALS['download_reads']===1,'Unchanged feed never triggers a duplicate import when matching revision is current');
ck($GLOBALS['settings']['last_import_at']>=$last,'Confirmed unmodified feed renews existing 48-hour freshness window');

$GLOBALS['settings']['last_match_revision']='OLD';$GLOBALS['download_mode']='304';
$r=$w->refresh();
ck(is_wp_error($r)&&$r->get_error_code()==='idealo_rematch_requires_feed','HTTP304 cannot falsely approve new matching rules');
ck(($GLOBALS['settings']['last_match_revision']??'')==='OLD','Failed refetch never advances the semantic revision');
$GLOBALS['settings']['last_match_revision']='hd009-match-0.1.41';
$GLOBALS['remote_hash']='new-data';
$r=$w->refresh();
ck(($r['status']??'')==='unchanged','HTTP304 with verified current revision is safe');
ck($GLOBALS['settings']['last_import_at']>=time()-2,'HTTP304 keeps valid last-good product cards fresh');
$GLOBALS['settings']['enabled']=false;
ck(!$w->active(),'Disabled provider remains disabled; semantic matching does not bypass access permission');

echo "ONE_IMPORT_ONE_DECISION_AUTOMATIC_REFRESH_TESTS_PASS\n";
'''.replace('__METHODS__',methods)
dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(php)
print('ORIGINAL_REFRESH_METHODS',4,'BYTES',len(php))
