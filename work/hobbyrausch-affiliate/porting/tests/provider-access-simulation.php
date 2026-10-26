<?php
error_reporting(E_ALL);

class WP_Error {
    private $code; private $message;
    public function __construct($code='', $message='') { $this->code=(string)$code; $this->message=(string)$message; }
    public function get_error_code(){ return $this->code; }
    public function get_error_message(){ return $this->message; }
}
function is_wp_error($v){ return $v instanceof WP_Error; }
function sanitize_key($v){ return strtolower(preg_replace('/[^a-z0-9_\-]/','', (string)$v)); }
function sanitize_title($v){
    $v=strtolower(trim((string)$v));
    $v=strtr($v,['ä'=>'ae','ö'=>'oe','ü'=>'ue','ß'=>'ss']);
    $v=preg_replace('/[^a-z0-9]+/','-', $v);
    return trim($v,'-');
}
function sanitize_text_field($v){ return trim(strip_tags((string)$v)); }
function absint($v){ return abs((int)$v); }
function wp_json_encode($v,$flags=0){ return json_encode($v,$flags); }
function wp_strip_all_tags($v){ return strip_tags((string)$v); }
function get_option($k,$default=false){ return $GLOBALS['wp_options'][$k] ?? $default; }
function update_option($k,$v,$autoload=false){ $GLOBALS['wp_options'][$k]=$v; return true; }

$GLOBALS['hd_registry_ready']=true;
$GLOBALS['hd_registry_snapshot']=[
 'contract'=>'HD004_TEST','revision'=>'test-1',
 'nodes'=>[
  ['node_id'=>'core:world:gestalten','parent_id'=>'','display_name'=>'Gestalten','slug'=>'gestalten','status'=>'active','object_type'=>'page'],
  ['node_id'=>'core:hub:handarbeit','parent_id'=>'core:world:gestalten','display_name'=>'Handarbeit','slug'=>'handarbeit','status'=>'active','object_type'=>'page'],
  ['node_id'=>'core:entity:stricken','parent_id'=>'core:hub:handarbeit','display_name'=>'Stricken','slug'=>'stricken','status'=>'active','object_type'=>'page'],
  ['node_id'=>'core:leaf:stricken-anfaenger','parent_id'=>'core:entity:stricken','display_name'=>'Stricken für Anfänger','slug'=>'stricken-anfaenger','status'=>'active','object_type'=>'category'],
 ],
 'mapping'=>[
  'core:entity:stricken'=>['object_id'=>101,'object_type'=>'page'],
  'core:leaf:stricken-anfaenger'=>['object_id'=>201,'object_type'=>'category'],
 ],
];
function hd_category_registry_ready(){ return (bool)$GLOBALS['hd_registry_ready']; }
function hd_category_registry_snapshot(){ return $GLOBALS['hd_registry_snapshot']; }

$root=dirname(__DIR__).'/hobby-depot-affiliate-router/includes';
require_once $root.'/trait-hdar-amazon-creators.php';
require_once $root.'/trait-ppar-ebay.php';
require_once $root.'/trait-ppar-idealo.php';

class AmazonAccessHarness {
 use HDAR_Amazon_Creators_Trait;
 public $access=['status'=>'not_configured'];
 public $paused=false;
 public function provider_access_state($provider){ return $this->access; }
 public function provider_channel_pause_gate($provider){ return $this->paused ? new WP_Error('paused','paused') : true; }
 public function active(){ return $this->amazon_creators_campaigns_should_be_active(); }
 public function credentials($s){ return $this->amazon_creators_credentials_present($s); }
}
class EbayAccessHarness {
 use PPAR_Ebay_Trait;
 const OPTION_NETWORK_EBAY='ppar_network_ebay_v1';
 public function catalog(){ return $this->ebay_portal_catalog(); }
 public function errors($s){ return $this->ebay_configuration_errors($s); }
}
class IdealoAccessHarness {
 use PPAR_Idealo_Trait;
 const OPTION_NETWORK_IDEALO='ppar_network_idealo_v1';
 public function credentials($s){ return $this->idealo_credentials_present($s); }
 public function active(){ return $this->idealo_campaigns_should_be_active(); }
}
function fail($m){ fwrite(STDERR,"FAIL: $m\n"); exit(1); }
function pass($m){ echo "PASS: $m\n"; exit(0); }

$scenario=$argv[1]??'';
$GLOBALS['wp_options']=[];

if($scenario==='amazon_disabled'){
 $GLOBALS['wp_options']['hdar_amazon_creators_v1']=['enabled'=>false,'partner_tag'=>'tag','client_id'=>'id','client_secret'=>'secret'];
 $h=new AmazonAccessHarness(); $h->access=['status'=>'connected'];
 if($h->active()) fail('disabled Amazon became active');
 pass('amazon disabled fail-closed');
}
if($scenario==='amazon_missing_credentials'){
 $GLOBALS['wp_options']['hdar_amazon_creators_v1']=['enabled'=>true,'partner_tag'=>'tag','client_id'=>'','client_secret'=>''];
 $h=new AmazonAccessHarness(); $h->access=['status'=>'connected'];
 if($h->active()) fail('Amazon with missing credentials became active');
 pass('amazon incomplete credentials fail-closed');
}
if($scenario==='amazon_unverified'){
 $GLOBALS['wp_options']['hdar_amazon_creators_v1']=['enabled'=>true,'partner_tag'=>'tag','client_id'=>'id','client_secret'=>'secret'];
 $h=new AmazonAccessHarness(); $h->access=['status'=>'credentials_saved'];
 if($h->active()) fail('unverified Amazon became active');
 pass('amazon unverified connection fail-closed');
}
if($scenario==='amazon_connected'){
 $GLOBALS['wp_options']['hdar_amazon_creators_v1']=['enabled'=>true,'partner_tag'=>'tag','client_id'=>'id','client_secret'=>'secret'];
 $h=new AmazonAccessHarness(); $h->access=['status'=>'connected'];
 if(!$h->active()) fail('connected Amazon did not become eligible');
 pass('amazon connected activation boundary');
}
if($scenario==='amazon_paused'){
 $GLOBALS['wp_options']['hdar_amazon_creators_v1']=['enabled'=>true,'partner_tag'=>'tag','client_id'=>'id','client_secret'=>'secret'];
 $h=new AmazonAccessHarness(); $h->access=['status'=>'connected']; $h->paused=true;
 if($h->active()) fail('paused Amazon became active');
 pass('amazon pause veto fail-closed');
}

if($scenario==='idealo_missing_credentials'){
 $h=new IdealoAccessHarness();
 if($h->credentials(['api_key'=>'','adspace_id'=>'','feed_id'=>''])) fail('idealo empty credentials accepted');
 pass('idealo incomplete credentials fail-closed');
}
if($scenario==='idealo_valid_credentials'){
 $h=new IdealoAccessHarness();
 if(!$h->credentials(['api_key'=>'key','adspace_id'=>'123','feed_id'=>'456'])) fail('idealo valid credential shape rejected');
 pass('idealo credential shape accepted');
}
if($scenario==='idealo_disabled'){
 $GLOBALS['wp_options']['ppar_network_idealo_v1']=['enabled'=>false,'output_mode'=>'idealo_only'];
 $h=new IdealoAccessHarness();
 if($h->active()) fail('disabled idealo became active');
 pass('idealo disabled fail-closed');
}
if($scenario==='idealo_enabled'){
 $GLOBALS['wp_options']['ppar_network_idealo_v1']=['enabled'=>true,'output_mode'=>'idealo_only'];
 $h=new IdealoAccessHarness();
 if(!$h->active()) fail('enabled idealo output mode not eligible');
 pass('idealo enabled output boundary');
}

if($scenario==='ebay_missing_credentials'){
 $h=new EbayAccessHarness(); $cat=$h->catalog();
 if(is_wp_error($cat)) fail('ebay catalog unavailable in credential test');
 $s=[
  'client_id'=>'','client_secret'=>'','epn_campaign_id'=>'',
  'marketplace_id'=>'EBAY_DE',
  'rules'=>[['id'=>'r1','query'=>'Stricken','target_term_slug'=>'stricken','active'=>true,'business'=>true]],
  'catalog_verified_sha256'=>$cat['source_sha256'],'catalog_verified_at'=>time(),
  'business_enabled'=>true,'private_enabled'=>false,
  'api_terms_confirmed'=>true,'privacy_policy_confirmed'=>true,'environment'=>'sandbox'
 ];
 $e=$h->errors($s);
 if(count(array_filter($e,fn($x)=>str_contains($x,'Client-ID fehlt')))!==1) fail('ebay missing client id not rejected');
 if(count(array_filter($e,fn($x)=>str_contains($x,'Client-Secret fehlt')))!==1) fail('ebay missing client secret not rejected');
 pass('ebay incomplete credentials fail-closed');
}
if($scenario==='ebay_unconfirmed'){
 $h=new EbayAccessHarness(); $cat=$h->catalog();
 $s=[
  'client_id'=>'id','client_secret'=>'secret','epn_campaign_id'=>'1234567890',
  'marketplace_id'=>'EBAY_DE',
  'rules'=>[['id'=>'r1','query'=>'Stricken','target_term_slug'=>'stricken','active'=>true,'business'=>true]],
  'catalog_verified_sha256'=>$cat['source_sha256'],'catalog_verified_at'=>time(),
  'business_enabled'=>true,'private_enabled'=>false,
  'api_terms_confirmed'=>false,'privacy_policy_confirmed'=>false,'environment'=>'sandbox'
 ];
 $e=$h->errors($s);
 if(!array_filter($e,fn($x)=>str_contains($x,'API-/EPN-Verträge'))) fail('ebay missing terms not rejected');
 if(!array_filter($e,fn($x)=>str_contains($x,'Datenschutz'))) fail('ebay missing privacy not rejected');
 pass('ebay legal confirmations fail-closed');
}
if($scenario==='ebay_valid'){
 $h=new EbayAccessHarness(); $cat=$h->catalog();
 if(is_wp_error($cat)) fail('ebay catalog unavailable');
 $s=[
  'client_id'=>'id','client_secret'=>'secret','epn_campaign_id'=>'1234567890',
  'marketplace_id'=>'EBAY_DE',
  'rules'=>[['id'=>'r1','query'=>'Stricken','target_term_slug'=>'stricken','active'=>true,'business'=>true]],
  'catalog_verified_sha256'=>$cat['source_sha256'],'catalog_verified_at'=>time(),
  'business_enabled'=>true,'private_enabled'=>false,
  'api_terms_confirmed'=>true,'privacy_policy_confirmed'=>true,'environment'=>'sandbox'
 ];
 $e=$h->errors($s);
 if($e) fail('ebay valid sandbox gate errors: '.implode(' | ',$e));
 pass('ebay complete configuration boundary');
}

fail('unknown scenario '.$scenario);
