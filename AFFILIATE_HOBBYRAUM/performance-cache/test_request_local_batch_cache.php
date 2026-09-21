<?php
declare(strict_types=1);
define('ABSPATH', __DIR__ . '/');
define('ARRAY_A', 'ARRAY_A');
function sanitize_key($v){ return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v)); }
function sanitize_text_field($v){ return trim((string)$v); }
function absint($v){ return abs((int)$v); }
function wp_json_encode($v,$flags=0){ return json_encode($v,$flags); }
function get_current_user_id(){ return 7; }
global $admin_mode,$ajax_mode,$postmeta; $admin_mode=false; $ajax_mode=false; $postmeta=[];
function is_admin(){ global $admin_mode; return (bool)$admin_mode; }
function wp_doing_ajax(){ global $ajax_mode; return (bool)$ajax_mode; }
function get_post_meta($id,$key,$single=true){ global $postmeta; return $postmeta[$id][$key] ?? ''; }
class WP_Error { public function __construct(public string $code='', public string $message=''){} }
function is_wp_error($v){ return $v instanceof WP_Error; }
function ok($c,$m){ if(!$c){fwrite(STDERR,"FAIL $m\n");exit(1);} echo "PASS $m\n"; }

class FakeWpdb {
  public string $base_prefix='slfo_'; public string $prefix='slfo_'; public int $insert_id=0;
  public array $decisions=[],$ebay=[],$creative=[],$counts=['control'=>0,'ebay'=>0,'creative'=>0,'other'=>0];
  function prepare($q,...$args){ if(count($args)===1&&is_array($args[0]))$args=$args[0]; foreach($args as $a){$q=preg_replace('/%[sd]/',"'".str_replace("'","''",(string)$a)."'",$q,1);} return $q; }
  private function vals($q,$field){ if(!preg_match('/'.preg_quote($field,'/').'\s+IN\s*\(([^)]*)\)/i',$q,$m))return[]; preg_match_all("/'([^']*)'/",$m[1],$mm); return $mm[1]??[]; }
  function get_results($q,$mode=null){
    if(str_contains($q,'ppar_control_decisions')){$this->counts['control']++; if(preg_match("/portal_key='([^']*)'/",$q,$m))return array_values(array_filter($this->decisions,fn($r)=>(string)($r['portal_key']??'')===$m[1])); return[];}
    if(str_contains($q,'ppar_ebay_items')){$this->counts['ebay']++; $vals=$this->vals($q,'creative_identity_hash'); $out=[]; foreach($this->ebay as $h=>$r)if(in_array($h,$vals,true)&&($r['seller_account_type']??'')==='BUSINESS')$out[]=$r; usort($out,fn($a,$b)=>(int)($b['id']??0)<=>(int)($a['id']??0)); return$out;}
    if(str_contains($q,'ppar_creative_library')){$this->counts['creative']++; $vals=$this->vals($q,'identity_hash'); $out=[]; foreach($this->creative as $h=>$r)if(in_array($h,$vals,true))$out[]=$r; return$out;}
    $this->counts['other']++; return[];
  }
  function get_row($q,$mode=null){
    if(str_contains($q,'ppar_control_decisions')){$this->counts['control']++;preg_match("/decision_key='([^']+)'/",$q,$m);return$this->decisions[$m[1]??'']??null;}
    if(str_contains($q,'ppar_ebay_items')){$this->counts['ebay']++;preg_match("/creative_identity_hash='([^']+)'/",$q,$m);$h=$m[1]??'';$r=$this->ebay[$h]??null;if(is_array($r)&&str_contains($q,"seller_account_type='BUSINESS'")&&($r['seller_account_type']??'')!=='BUSINESS')return null;return$r;}
    if(str_contains($q,'ppar_creative_library')){$this->counts['creative']++;preg_match("/identity_hash='([^']+)'/",$q,$m);return$this->creative[$m[1]??'']??null;}
    $this->counts['other']++;return null;
  }
  function delete($table,$where){if(str_contains($table,'ppar_control_decisions'))foreach($this->decisions as $k=>$r)if(($r['scope_type']??'')===($where['scope_type']??'')&&($r['scope_key']??'')===($where['scope_key']??''))unset($this->decisions[$k]);return 1;}
  function update($table,$data,$where){if(str_contains($table,'ppar_control_decisions'))foreach($this->decisions as $k=>$r)if(($r['id']??0)==($where['id']??-1)){$this->decisions[$k]=array_merge($r,$data);return 1;}return 1;}
  function insert($table,$data){if(str_contains($table,'ppar_control_decisions')){$this->insert_id=count($this->decisions)+1000;$data['id']=$this->insert_id;$this->decisions[$data['decision_key']]=$data;}return 1;}
}
$wpdb=new FakeWpdb();
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-control-contract.php';
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay.php';
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-output-objects.php';
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay-account-deletion.php';

class Harness {
 use PPAR_Control_Contract_Trait, PPAR_Ebay_Trait, PPAR_Output_Objects_Trait, PPAR_Ebay_Account_Deletion_Trait;
 const OPTION_CONTROL_SCHEMA_VERSION='x'; const OPTION_CONTROL_SETTINGS='y'; const CONTROL_CONTRACT_VERSION='1';
 public array $campaigns=[];
 function get_campaigns(){return $this->campaigns;}
 function ebay_items_table(){global $wpdb;return $wpdb->prefix.'ppar_ebay_items';}
 function creative_library_table(){global $wpdb;return $wpdb->prefix.'ppar_creative_library';}
 function control_log_event($event_type,$portal_key,$scope_type,$scope_key,$old_status,$new_status,$reason,$payload=[],$user_id=null){}
 public function ebayRow($c){$m=new ReflectionMethod($this,'ebay_business_campaign_source_row');$m->setAccessible(true);return $m->invoke($this,$c);}
 public function creativeRow($h){$m=new ReflectionMethod($this,'output_creative_row');$m->setAccessible(true);return $m->invoke($this,$h);}
 public function deleteControlScope($t,$k){$m=new ReflectionMethod($this,'ebay_deletion_delete_control_scope');$m->setAccessible(true);return $m->invoke($this,$t,$k);}
}
function dk($p,$t,$k){return hash('sha256',sanitize_key($p).'|'.sanitize_key($t).'|'.$k);}
function hh($i){return hash('sha256','campaign-'.$i);}
$portal='pferde-atelier'; $h=new Harness();

for($i=0;$i<315;$i++){ $k=dk($portal,'creative','control-'.$i); $wpdb->decisions[$k]=['id'=>$i+1,'decision_key'=>$k,'portal_key'=>$portal,'scope_type'=>'creative','scope_key'=>'control-'.$i,'status'=>($i===7?'veto':'approved'),'reason'=>'fixture','payload'=>'{}','user_id'=>7,'created_at'=>1,'updated_at'=>2];}
$b=$wpdb->counts['control']; for($i=0;$i<315;$i++){ $r=$h->control_get_decision($portal,'creative','control-'.$i); if($i===7)ok(($r['status']??'')==='veto','portal batch preserves veto');}
ok($wpdb->counts['control']===$b+1,'315 distinct control keys -> 1 batch query');
$b=$wpdb->counts['control']; for($i=0;$i<100;$i++)$h->control_get_decision($portal,'creative','missing-'.$i); ok($wpdb->counts['control']===$b,'missing control keys -> 0 extra queries after batch');
$id=$h->control_set_decision($portal,'creative','control-0','veto','changed');ok($id===1,'control write succeeds');$b=$wpdb->counts['control'];$r=$h->control_get_decision($portal,'creative','control-0');ok($wpdb->counts['control']===$b+1&&($r['status']??'')==='veto','write invalidates portal batch');
$h->control_reset_decision($portal,'creative','control-0');$r=$h->control_get_decision($portal,'creative','control-0');ok(($r['status']??'')==='automatic','reset remains fresh');

for($i=0;$i<792;$i++){ $post=10000+$i;$hash=hh($i);$postmeta[$post]=['_ppar_ebay_business_auto'=>1,'_ppar_creative_identity_hash'=>$hash];$h->campaigns[]=['network'=>'ebay','post_id'=>$post,'creative_type'=>'product','active'=>true];$wpdb->ebay[$hash]=['id'=>$i+1,'creative_identity_hash'=>$hash,'seller_account_type'=>'BUSINESS','item_id'=>'B'.$i];if($i<87)$wpdb->creative[$hash]=['id'=>$i+1,'identity_hash'=>$hash,'title'=>'Creative '.$i];}
$b=$wpdb->counts['ebay'];for($i=0;$i<792;$i++)$r=$h->ebayRow($h->campaigns[$i]);ok($wpdb->counts['ebay']===$b+1,'792 distinct eBay BUSINESS hashes -> 1 batch query');ok(($r['item_id']??'')==='B791','eBay batch preserves exact row');
$b=$wpdb->counts['creative'];for($i=0;$i<87;$i++)$r=$h->creativeRow(hh($i));ok($wpdb->counts['creative']===$b+1,'87 distinct creative hashes -> 1 batch query');ok(($r['title']??'')==='Creative 86','creative batch preserves exact row');

$ph=hash('sha256','private');$pp=20000;$postmeta[$pp]=['_ppar_ebay_business_auto'=>1,'_ppar_creative_identity_hash'=>$ph];$h2=new Harness();$h2->campaigns=[['network'=>'ebay','post_id'=>$pp,'creative_type'=>'product','active'=>true]];$wpdb->ebay[$ph]=['id'=>9999,'creative_identity_hash'=>$ph,'seller_account_type'=>'INDIVIDUAL','item_id'=>'PRIVATE'];$b=$wpdb->counts['ebay'];$r=$h2->ebayRow($h2->campaigns[0]);ok($wpdb->counts['ebay']===$b+1&&$r===[],'PRIVATE cannot satisfy BUSINESS batch');

$admin_mode=true;$ha=new Harness();$ha->campaigns=$h->campaigns;$b=$wpdb->counts['ebay'];for($i=0;$i<3;$i++)$ha->ebayRow($ha->campaigns[0]);ok($wpdb->counts['ebay']===$b+3,'admin eBay stays uncached');$b=$wpdb->counts['creative'];for($i=0;$i<3;$i++)$ha->creativeRow(hh(0));ok($wpdb->counts['creative']===$b+3,'admin creative stays uncached');
echo "ALL REQUEST-LOCAL BATCH QUERY TESTS PASS\n";
