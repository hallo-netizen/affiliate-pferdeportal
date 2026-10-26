<?php
error_reporting(E_ALL);
class WP_Error { private $c,$m; function __construct($c='',$m=''){ $this->c=$c;$this->m=$m;} function get_error_code(){return $this->c;} function get_error_message(){return $this->m;} }
function is_wp_error($v){ return $v instanceof WP_Error; }
function sanitize_key($v){ return strtolower(preg_replace('/[^a-z0-9_\-]/','',(string)$v)); }
function sanitize_text_field($v){ return trim(strip_tags((string)$v)); }
function absint($v){ return abs((int)$v); }
function esc_url_raw($v){ return trim((string)$v); }
function get_option($k,$d=false){ return $GLOBALS['opts'][$k] ?? $d; }
function update_option($k,$v,$autoload=false){ $GLOBALS['opts'][$k]=$v; return true; }
function get_posts($args=[]){ return []; }
function wp_next_scheduled($hook){ return false; }
function wp_schedule_event(){ return true; }
function wp_clear_scheduled_hook(){ return true; }

$root=dirname(__DIR__).'/hobby-depot-affiliate-router/includes';
require_once $root.'/trait-hdar-amazon-creators.php';
require_once $root.'/trait-ppar-idealo.php';

class AmazonRoundtrip {
 use HDAR_Amazon_Creators_Trait;
 public $state=[];
 public function provider_set_access_state($p,$s,$m){ $this->state[$p]=[$s,$m]; return true; }
 public function save($raw){ return $this->amazon_creators_provider_access_save(null,'amazon',$raw,'test'); }
}
class IdealoRoundtrip {
 use PPAR_Idealo_Trait;
 const OPTION_NETWORK_IDEALO='ppar_network_idealo_v1';
 public $state=[];
 public function provider_set_access_state($p,$s,$m){ $this->state[$p]=[$s,$m]; return true; }
 public function save($raw){ return $this->idealo_provider_access_save(null,'idealo',$raw,'test'); }
}
function fail($m){ fwrite(STDERR,"FAIL: $m\n"); exit(1); }
function ok($m){ echo "PASS: $m\n"; }

$GLOBALS['opts']=[];
$secret='synthetic-amazon-secret';
$a=new AmazonRoundtrip();
$a->save(['enabled'=>1,'marketplace'=>'www.amazon.de','credential_version'=>'3.2','partner_tag'=>'tag-21','client_id'=>'cid','client_secret'=>$secret]);
$stored=get_option('hdar_amazon_creators_v1',[]);
if(($stored['client_secret']??null)!==$secret) fail('Amazon initial secret roundtrip failed');
$a->save(['enabled'=>1,'marketplace'=>'www.amazon.de','credential_version'=>'3.2','partner_tag'=>'tag-21','client_id'=>'cid','client_secret'=>'']);
$stored=get_option('hdar_amazon_creators_v1',[]);
if(($stored['client_secret']??null)!==$secret) fail('Amazon blank resave lost secret');
$a->save(['enabled'=>1,'marketplace'=>'www.amazon.de','credential_version'=>'3.2','partner_tag'=>'tag-21','client_id'=>'cid','remove_client_secret'=>1]);
$stored=get_option('hdar_amazon_creators_v1',[]);
if(($stored['client_secret']??'x')!=='') fail('Amazon explicit secret removal failed');
ok('Amazon secret save/preserve/remove roundtrip');

$GLOBALS['opts']=[];
$key='synthetic-idealo-api-key';
$i=new IdealoRoundtrip();
$i->save(['enabled'=>1,'api_key'=>$key,'adspace_id'=>'123','feed_id'=>'456','output_mode'=>'idealo_only','link_strategy'=>'hybrid']);
$stored=get_option('ppar_network_idealo_v1',[]);
if(($stored['api_key']??null)!==$key) fail('idealo initial API key roundtrip failed');
$i->save(['enabled'=>1,'api_key'=>'','adspace_id'=>'123','feed_id'=>'456','output_mode'=>'idealo_only','link_strategy'=>'hybrid']);
$stored=get_option('ppar_network_idealo_v1',[]);
if(($stored['api_key']??null)!==$key) fail('idealo blank resave lost API key');
$i->save(['enabled'=>1,'remove_api_key'=>1,'adspace_id'=>'123','feed_id'=>'456','output_mode'=>'idealo_only','link_strategy'=>'hybrid']);
$stored=get_option('ppar_network_idealo_v1',[]);
if(($stored['api_key']??'x')!=='') fail('idealo explicit API key removal failed');
ok('idealo key save/preserve/remove roundtrip');

echo "ROUNDTRIP_SECRET_VALUES_NOT_PRINTED=PASS\n";
