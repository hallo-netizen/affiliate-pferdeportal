<?php
declare(strict_types=1);
define('ABSPATH', __DIR__ . '/');
define('ARRAY_A', 'ARRAY_A');
function sanitize_key($v){ return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v)); }
function sanitize_text_field($v){ return trim((string)$v); }
function absint($v){ return abs((int)$v); }
function wp_json_encode($v,$flags=0){ return json_encode($v,$flags); }
function get_current_user_id(){ return 7; }
global $admin_mode,$ajax_mode; $admin_mode=false; $ajax_mode=false;
function is_admin(){ global $admin_mode; return (bool)$admin_mode; }
function wp_doing_ajax(){ global $ajax_mode; return (bool)$ajax_mode; }
function get_post_meta($id,$key,$single=true){ global $postmeta; return $postmeta[$id][$key] ?? ''; }
class WP_Error { public function __construct(public string $code='', public string $message=''){} }
function is_wp_error($v){ return $v instanceof WP_Error; }
function ok($c,$m){ if(!$c){fwrite(STDERR,"FAIL $m\n");exit(1);} echo "PASS $m\n"; }

class FakeWpdb {
    public string $base_prefix='slfo_'; public string $prefix='slfo_'; public int $insert_id=0;
    public array $decisions=[]; public array $ebay=[]; public array $creative=[]; public array $counts=['control'=>0,'ebay'=>0,'creative'=>0,'other'=>0];
    function prepare($q,...$args){ foreach($args as $a){$q=preg_replace('/%[sd]/',"'".str_replace("'","''",(string)$a)."'",$q,1);} return $q; }
    function get_row($q,$mode=null){
        if(str_contains($q,'ppar_control_decisions')){ $this->counts['control']++; preg_match("/decision_key='([^']+)'/",$q,$m); return $this->decisions[$m[1]??'']??null; }
        if(str_contains($q,'ppar_ebay_items')){ $this->counts['ebay']++; preg_match("/creative_identity_hash='([^']+)'/",$q,$m); $h=$m[1]??''; $row=$this->ebay[$h]??null; if(is_array($row) && str_contains($q,"seller_account_type='BUSINESS'") && ($row['seller_account_type']??'')!=='BUSINESS') return null; return $row; }
        if(str_contains($q,'ppar_creative_library')){ $this->counts['creative']++; preg_match("/identity_hash='([^']+)'/",$q,$m); return $this->creative[$m[1]??'']??null; }
        $this->counts['other']++; return null;
    }
    function delete($table,$where){
        if(str_contains($table,'ppar_control_decisions')){ foreach($this->decisions as $k=>$row){ if(($row['scope_type']??'')===($where['scope_type']??'') && ($row['scope_key']??'')===($where['scope_key']??'')){ unset($this->decisions[$k]); } } }
        return 1;
    }
    function update($table,$data,$where){
        if(str_contains($table,'ppar_control_decisions')){ foreach($this->decisions as $k=>$row){ if(($row['id']??0)==($where['id']??-1)){ $this->decisions[$k]=array_merge($row,$data); return 1; } } }
        return 1;
    }
    function insert($table,$data){
        if(str_contains($table,'ppar_control_decisions')){ $this->insert_id=count($this->decisions)+100; $data['id']=$this->insert_id; $this->decisions[$data['decision_key']]=$data; }
        return 1;
    }
}
$wpdb=new FakeWpdb();

require __DIR__.'/affiliate-portal-router/includes/trait-ppar-control-contract.php';
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay.php';
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-output-objects.php';
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay-account-deletion.php';

class Harness {
    use PPAR_Control_Contract_Trait, PPAR_Ebay_Trait, PPAR_Output_Objects_Trait, PPAR_Ebay_Account_Deletion_Trait;
    const OPTION_CONTROL_SCHEMA_VERSION='x'; const OPTION_CONTROL_SETTINGS='y'; const CONTROL_CONTRACT_VERSION='1';
    function ebay_items_table(){global $wpdb; return $wpdb->prefix.'ppar_ebay_items';}
    function creative_library_table(){global $wpdb; return $wpdb->prefix.'ppar_creative_library';}
    function control_log_event($event_type,$portal_key,$scope_type,$scope_key,$old_status,$new_status,$reason,$payload=[],$user_id=null){ return; }
    public function ebayRow($c){ $m=new ReflectionMethod($this,'ebay_business_campaign_source_row'); $m->setAccessible(true); return $m->invoke($this,$c); }
    public function creativeRow($h){ $m=new ReflectionMethod($this,'output_creative_row'); $m->setAccessible(true); return $m->invoke($this,$h); }
    public function deleteControlScope($t,$k){ $m=new ReflectionMethod($this,'ebay_deletion_delete_control_scope'); $m->setAccessible(true); return $m->invoke($this,$t,$k); }
}

function decisionKey($p,$t,$k){ return hash('sha256',sanitize_key($p).'|'.sanitize_key($t).'|'.$k); }
$portal='pferde-atelier'; $scope='creative'; $sk='abc'; $dk=decisionKey($portal,$scope,$sk);
$wpdb->decisions[$dk]=['id'=>1,'decision_key'=>$dk,'portal_key'=>$portal,'scope_type'=>$scope,'scope_key'=>$sk,'status'=>'approved','reason'=>'ok','payload'=>'{}','user_id'=>7,'created_at'=>1,'updated_at'=>2];
$h=new Harness();
for($i=0;$i<11297;$i++) $r=$h->control_get_decision($portal,$scope,$sk);
ok($wpdb->counts['control']===1,'11297 identical control reads collapse to 1 DB query');
ok(($r['status']??'')==='approved','control result unchanged');
$before=$wpdb->counts['control']; for($i=0;$i<1000;$i++) $m=$h->control_get_decision($portal,'creative','missing');
ok($wpdb->counts['control']===$before+1,'1000 missing control reads collapse to 1 DB query');
ok(($m['exists']??true)===false && ($m['status']??'')==='automatic','missing control semantics unchanged');
$before=$wpdb->counts['control']; foreach(['A','B','C'] as $x){for($i=0;$i<20;$i++)$h->control_get_decision($portal,'slot',$x);} ok($wpdb->counts['control']===$before+3,'different decision keys never collide');
$id=$h->control_set_decision($portal,$scope,$sk,'veto','stop'); ok($id===1,'control write succeeds'); $before=$wpdb->counts['control']; $after=$h->control_get_decision($portal,$scope,$sk); ok($wpdb->counts['control']===$before+1,'write invalidates cached decision'); ok(($after['status']??'')==='veto','write then read sees fresh veto');
$h->control_reset_decision($portal,$scope,$sk); $after=$h->control_get_decision($portal,$scope,$sk); ok(($after['status']??'')==='automatic','reset then read sees fresh automatic');
$h->control_set_decision($portal,$scope,'delete-me','approved','temp');
$warm=$h->control_get_decision($portal,$scope,'delete-me'); ok(($warm['exists']??false)===true,'control delete fixture cached');
$h->deleteControlScope($scope,'delete-me'); $before=$wpdb->counts['control']; $gone=$h->control_get_decision($portal,$scope,'delete-me'); ok($wpdb->counts['control']===$before+1 && ($gone['exists']??true)===false,'direct control deletion clears request cache');

$hashA=str_repeat('a',64); $hashB=str_repeat('b',64); global $postmeta; $postmeta=[10=>['_ppar_ebay_business_auto'=>1,'_ppar_creative_identity_hash'=>$hashA],11=>['_ppar_ebay_business_auto'=>1,'_ppar_creative_identity_hash'=>$hashB]];
$wpdb->ebay[$hashA]=['id'=>10,'creative_identity_hash'=>$hashA,'seller_account_type'=>'BUSINESS','item_id'=>'A']; $wpdb->ebay[$hashB]=['id'=>11,'creative_identity_hash'=>$hashB,'seller_account_type'=>'BUSINESS','item_id'=>'B'];
$cA=['network'=>'ebay','post_id'=>10]; $cB=['network'=>'ebay','post_id'=>11]; $before=$wpdb->counts['ebay']; for($i=0;$i<1484;$i++)$er=$h->ebayRow($cA); ok($wpdb->counts['ebay']===$before+1,'1484 identical eBay BUSINESS reads collapse to 1 DB query'); ok(($er['item_id']??'')==='A','eBay result unchanged'); $h->ebayRow($cB); ok($wpdb->counts['ebay']===$before+2,'eBay hash A/B never collide');
$postmeta[12]=['_ppar_ebay_business_auto'=>1,'_ppar_creative_identity_hash'=>str_repeat('c',64)]; $before=$wpdb->counts['ebay']; for($i=0;$i<100;$i++)$empty=$h->ebayRow(['network'=>'ebay','post_id'=>12]); ok($wpdb->counts['ebay']===$before+1 && $empty===[],'missing eBay BUSINESS row cached safely');

$wpdb->creative[$hashA]=['id'=>20,'identity_hash'=>$hashA,'title'=>'A']; $wpdb->creative[$hashB]=['id'=>21,'identity_hash'=>$hashB,'title'=>'B']; $before=$wpdb->counts['creative']; for($i=0;$i<305;$i++)$cr=$h->creativeRow($hashA); ok($wpdb->counts['creative']===$before+1,'305 identical creative reads collapse to 1 DB query'); ok(($cr['title']??'')==='A','creative result unchanged'); $h->creativeRow($hashB); ok($wpdb->counts['creative']===$before+2,'creative hash A/B never collide'); $missingHash=str_repeat('d',64); $before=$wpdb->counts['creative']; for($i=0;$i<100;$i++)$empty=$h->creativeRow($missingHash); ok($wpdb->counts['creative']===$before+1 && $empty===null,'missing creative row cached safely');

global $admin_mode; $admin_mode=true; $hAdmin=new Harness(); $before=$wpdb->counts['ebay']; for($i=0;$i<3;$i++)$hAdmin->ebayRow($cA); ok($wpdb->counts['ebay']===$before+3,'admin eBay reads stay uncached to avoid stale write/read state'); $before=$wpdb->counts['creative']; for($i=0;$i<3;$i++)$hAdmin->creativeRow($hashA); ok($wpdb->counts['creative']===$before+3,'admin creative reads stay uncached to avoid stale write/read state'); $admin_mode=false;
$hashP=str_repeat('e',64); $postmeta[13]=['_ppar_ebay_business_auto'=>1,'_ppar_creative_identity_hash'=>$hashP]; $wpdb->ebay[$hashP]=['id'=>13,'creative_identity_hash'=>$hashP,'seller_account_type'=>'INDIVIDUAL','item_id'=>'P']; $private=$h->ebayRow(['network'=>'ebay','post_id'=>13]); ok($private===[],'PRIVATE seller cannot satisfy BUSINESS cache/query');
echo "ALL REQUEST-LOCAL QUERY CACHE TESTS PASS\n";
