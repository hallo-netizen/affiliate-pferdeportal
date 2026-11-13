#!/usr/bin/env python3
"""PHP runtime tests against literal HD009 0.1.34 preview and ORIGINAL matcher.
Only synthetic data. No real API access. No WordPress installation or DB writes.
"""
import re,sys
from pathlib import Path
from zipfile import ZipFile

plugin=Path(sys.argv[1])
output=Path(sys.argv[2])
path='affiliate-portal-router/includes/trait-ppar-idealo.php'
with ZipFile(plugin) as z:s=z.read(path).decode('utf8')
names=[
 'hd_idealo_preview_save','hd_idealo_preview_current',
 'hd_idealo_preview_allowed','hd_idealo_preview_csv',
 'hd_idealo_preview_existing_concepts','hd_idealo_standard_feed_compare_work',
 'hd_idealo_feed_source_ready','idealo_match_normalize','idealo_match_stem',
 'idealo_match_tokens','idealo_match_primary_tokens','idealo_match_distinct_tokens',
 'idealo_match_index','idealo_match_blocked','idealo_match_context_score',
 'idealo_match_feed_row_to_concept','idealo_normalize_gtins_from_values',
 'idealo_direct_image_url','idealo_open_feed_stream','idealo_stream_close'
]
def method(name):
    start=re.search(r'^    (?:private|public|protected) function '+re.escape(name)+r'\(',s,re.M)
    assert start,name
    body=s[start.start():]
    following=re.search(r'^    (?:private|public|protected) function [A-Za-z_]+\(',body[start.end()-start.start():],re.M)
    if following:
        return body[:start.end()-start.start()+following.start()].rstrip()
    return body
source='\n'.join(method(n) for n in names)
php=r'''<?php
error_reporting(E_ALL);
ini_set('display_errors',1);
class WP_Error {
    private $code; private $message;
    function __construct($code,$message){$this->code=$code;$this->message=$message;}
    function get_error_code(){return $this->code;}
    function get_error_message(){return $this->message;}
}
function is_wp_error($x){return $x instanceof WP_Error;}
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function sanitize_text_field($x){return strip_tags((string)$x);}
function wp_strip_all_tags($x){return strip_tags((string)$x);}
function remove_accents($x){return strtr((string)$x,array('ü'=>'u','ä'=>'a','ö'=>'o','ß'=>'ss'));}
function esc_url_raw($x){return (string)$x;}
function wp_parse_url($x){return parse_url($x);}
function absint($x){return abs((int)$x);}
function get_transient($k){return $GLOBALS['transients'][$k]??false;}
function get_option($k,$default=array()){return $GLOBALS['options'][$k]??$default;}
function update_option($k,$value,$autoload=false){
    if ($k==='live_idealo') {throw new Exception('ILLEGAL LIVE SETTINGS WRITE');}
    $GLOBALS['options'][$k]=$value;return true;
}
class FakeDB {
    public $calls=array();
    function prepare($sql,...$params){$this->calls[]=array('prepare',$sql,$params);return vsprintf(str_replace(array('%s','%d'),array("'%s'",'%d'),$sql),$params);}
    function get_col($sql){$this->calls[]=array('get_col',$sql);if(strpos($sql,'SELECT DISTINCT category')!==0){throw new Exception('UNEXPECTED DB QUERY');}return array('concept-teleskop','concept-kamera');}
}
$GLOBALS['wpdb']=new FakeDB();
$GLOBALS['transients']=array();
$GLOBALS['options']=array('live_idealo'=>array('marker'=>'KEEP','feed_id'=>'2747'));
$GLOBALS['settings']=array(
    'enabled'=>true,'hobby_feed_verified'=>true,'api_key'=>'SYNTHETIC_DO_NOT_USE',
    'adspace_id'=>'568912','feed_id'=>'2747','feed_url'=>'',
    'feed_etag'=>'"2747-ETAG"','feed_last_modified'=>'prior_date',
    'api_last_checked_at'=>time()-100,'refresh_state'=>'success',
    'last_import_feed_id'=>'2747','last_import_adspace_id'=>'568912',
    'last_import_started_at'=>time()-3605,'last_import_at'=>time()-3600
);
class TestHD009 {
    const IDEALO_REFRESH_LOCK='ppar_idealo_refresh_lock_v1';
    const HD_IDEALO_PREVIEW_OPTION='ppar_hd009_feed_preview_v1';
    public $metadata_request=array();
    public $download_request=array();
    public $synthetic_path='';
    public $allow2901=true;
    private function idealo_settings(){return $GLOBALS['settings'];}
    private function idealo_credentials_present($s){
        return ($s['api_key']??'')!=='' && ($s['adspace_id']??'')==='568912' && !empty($s['hobby_feed_verified']) && ctype_digit((string)$s['feed_id']);
    }
    private function idealo_portal_supply_catalog(){
        $items=array();
        foreach(array('teleskop'=>'Teleskop','kamera'=>'Kamera','airbrush'=>'Airbrush') as $id=>$name){
            $items['concept-'.$id]=array('id'=>'concept-'.$id,'title'=>$name,
                'target_pages'=>array(array('hub'=>'Forschen','main_hub'=>'Forschen')));
        }
        return array('_idealo_required_concepts'=>$items,'hard_negative_markers'=>array());
    }
    private function idealo_find_feed_metadata($s){
        $this->metadata_request=$s;
        if (!$this->allow2901 || ($s['feed_id']??'')!=='2901' ||
            ($s['adspace_id']??'')!=='568912') {
            return new WP_Error('idealo_feed_not_found','2901 not authorized for this adspace');
        }
        return array('feed_id'=>'2901','number_of_products'=>9999);
    }
    private function idealo_download_feed_to_temp($s){
        $this->download_request=$s;
        if (($s['feed_id']??'')!=='2901'||($s['feed_url']??'')!==''||
            ($s['feed_etag']??'')!==''||($s['feed_last_modified']??'')!=='') {
            return new WP_Error('test_cross_feed_cache','Wrong feed or inherited cache!');
        }
        $f=tempnam(sys_get_temp_dir(),'hd009preview');
        copy($this->synthetic_path,$f);
        return array('status'=>'downloaded','path'=>$f);
    }
    private function network_sync_table($n){return 'hd_products';}
    // The 20 listed methods are literal PHP extracted from the newly built ZIP.
__EXTRACTED__

    public function run(){return $this->hd_idealo_standard_feed_compare_work();}
    public function parsefile($f){return $this->hd_idealo_preview_csv($f);}
    public function allowed($s){return $this->hd_idealo_preview_allowed($s);}
    public function save($v){$this->hd_idealo_preview_save($v);}
    public function current(){return $this->hd_idealo_preview_current();}
}
function ck($condition,$description){
    static $n=0;$n++;
    if(!$condition){fwrite(STDERR,"FAIL $n: $description\n");exit(1);}
    echo "PASS $n: $description\n";
}
$headers='id,product_title,product_deeplink,ean,gtins_product,asins_product,main_category,sub_category,brand_name,image_url';
$lines=array(
'1,Teleskop Refraktor,https://ipn.idealo.de/click?x=1,4006381333931,,,Astronomie,Teleskope,ACME,https://cdn.idealo.com/item1.jpg',
'2,Airbrush Pistole Profi,https://ipn.idealo.de/click?x=2,4006381333932,,,Hobby und Basteln,Airbrush,ACME,https://cdn.idealo.com/item2.jpg',
'3,Kamera Zubehör,https://ipn.idealo.de/click?x=3,,,,Foto,Objektive,ACME,https://cdn.idealo.com/item3.jpg',
'4,Schraubendreher,https://ipn.idealo.de/click?x=4,4006381333933,,,Werkzeuge,Schrauben,ACME,https://cdn.idealo.com/item4.jpg',
'5,Airbrush Flasche,https://ipn.idealo.de/click?x=5,4006381333934,,,Hobby,Hobby,ACME,https://example.org/notcdn.jpg',
'6,BAD_COLUMN_COUNT',
);
$csv=$headers."\n".implode("\n",$lines)."\n";
$f=tempnam(sys_get_temp_dir(),'hd009fixture');
file_put_contents($f,gzencode($csv,7));
$p=new TestHD009();$p->synthetic_path=$f;
ck($p->allowed($GLOBALS['settings']),'Existing authenticated 2747 baseline accepted');
$parsed=$p->parsefile($f);
ck(!is_wp_error($parsed),'Literal matcher and preview CSV parser execute on synthetic GZIP');
ck($parsed['seen']===6,'Every CSV row counted');
ck($parsed['matching_rows']===2,'Two exact product matches after original GTIN/filename/keyword safety rules');
ck($parsed['matched_concepts']===2,'Two distinct hobby concepts – not duplicated by product rows');
ck($parsed['missing_identity']===1,'No-GTIN row rejected');
ck($parsed['bad_rows']===1,'Malformed rows rejected');
ck($parsed['no_match']===1,'Unrelated product rejected');
ck($parsed['no_image']===1,'Non-authorized product image rejected');
$before=$GLOBALS['options']['live_idealo'];
$r=$p->run();
ck(!is_wp_error($r),'Complete real compare methods return result');
ck($r['current_feed']==='2747'&&$r['compared_feed']==='2901','Both exact feed IDs are preserved');
ck($r['baseline_matched']===2&&$r['standard_2901_matched']===2,'Existing vs candidate matched concepts counted separately');
ck($r['both_covered']===1&&$r['only_2901']===1&&$r['only_2747']===1&&$r['total_union']===3,'True union and both exclusive coverage computed');
ck($r['new_hobbies']===array('Airbrush') && $r['lost_hobbies']===array('Kamera'),
    'Shows exact hobbies gained or lost, not just totals');
ck($r['standard_2901_api_products']===9999&&$r['standard_2901_feed_rows']===6,
    'API count and actually scanned rows distinguished');
ck($GLOBALS['options']['live_idealo']===$before && $GLOBALS['settings']['feed_id']==='2747',
    'Production settings untouched (especially 2747 ID/output mode)');
ck($p->metadata_request['feed_id']==='2901' &&
    $p->download_request['feed_id']==='2901' &&
    $p->download_request['feed_url']==='' &&
    $p->download_request['feed_etag']==='' &&
    $p->download_request['feed_last_modified']==='',
    '2901 verified first; never reuses 2747 source URL, hash or conditional cache');
ck(!is_file($p->synthetic_path)===false,'Original synthetic source fixture intact');
ck(count($GLOBALS['wpdb']->calls)===2 &&
    strncmp($GLOBALS['wpdb']->calls[1][1],'SELECT DISTINCT category',24)===0,
    'Only read-only SELECT against existing staged 2747 data');
$p->save(array('status'=>'success','foo'=>12));
ck($p->current()['foo']===12 &&
    $GLOBALS['options']['live_idealo']===$before,
    'Comparison report writes isolated WordPress option only');
$foreign=$GLOBALS['settings'];$foreign['adspace_id']='568944';
ck(!$p->allowed($foreign),'Wrong adspace hard blocked');
$foreign=$GLOBALS['settings'];$foreign['last_import_feed_id']='2901';
ck(!$p->allowed($foreign),'Unverified current base blocked');
$foreign=$GLOBALS['settings'];$foreign['refresh_state']='running';
ck(!$p->allowed($foreign),'Concurrent real feed import blocked');
$p->allow2901=false;
$blocked=$p->run();
ck(is_wp_error($blocked) && $blocked->get_error_code()==='idealo_feed_not_found',
    'Unavailable 2901 feed causes clean failure without mutating current 2747 products');
ck($GLOBALS['options']['live_idealo']===$before,
    'Negative access test preserves production configuration');
unlink($f);
echo "ALL_SAFE_PREVIEW_RUNTIME_TESTS_PASS\n";
'''.replace('__EXTRACTED__',source)
output.parent.mkdir(exist_ok=True,parents=True)
output.write_text(php)
print('HARNESS',output,'REAL_METHODS',len(names),'BYTES',len(php))
