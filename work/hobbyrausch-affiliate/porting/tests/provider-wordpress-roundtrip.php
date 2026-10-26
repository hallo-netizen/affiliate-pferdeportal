<?php
if (!defined('ABSPATH')) { fwrite(STDERR,"WP_NOT_LOADED\n"); exit(1); }

$root = dirname(__DIR__) . '/hobby-depot-affiliate-router/includes';
require_once $root . '/trait-hdar-amazon-creators.php';
require_once $root . '/trait-ppar-idealo.php';

class HDAR_WP_Amazon_Roundtrip {
    use HDAR_Amazon_Creators_Trait;
    public function provider_set_access_state($provider,$status,$message){ update_option('hdar_test_state_'.$provider, compact('status','message'), false); return true; }
    public function save($raw){ return $this->amazon_creators_provider_access_save(null,'amazon',$raw,'test'); }
}
class HDAR_WP_Idealo_Roundtrip {
    use PPAR_Idealo_Trait;
    const OPTION_NETWORK_IDEALO='ppar_network_idealo_v1';
    public function provider_set_access_state($provider,$status,$message){ update_option('hdar_test_state_'.$provider, compact('status','message'), false); return true; }
    public function save($raw){ return $this->idealo_provider_access_save(null,'idealo',$raw,'test'); }
}
function hdar_fail($m){ fwrite(STDERR,"FAIL: $m\n"); exit(1); }
function hdar_ok($m){ echo "PASS: $m\n"; }

delete_option('hdar_amazon_creators_v1');
delete_option('ppar_network_idealo_v1');

$a=new HDAR_WP_Amazon_Roundtrip();
$amazon_secret='wp-runtime-amazon-secret';
$a->save(['enabled'=>1,'marketplace'=>'www.amazon.de','credential_version'=>'3.2','partner_tag'=>'tag-21','client_id'=>'cid','client_secret'=>$amazon_secret]);
$stored=get_option('hdar_amazon_creators_v1',[]);
if(($stored['client_secret']??null)!==$amazon_secret) hdar_fail('Amazon WP initial secret roundtrip');
$a->save(['enabled'=>1,'marketplace'=>'www.amazon.de','credential_version'=>'3.2','partner_tag'=>'tag-21','client_id'=>'cid','client_secret'=>'']);
$stored=get_option('hdar_amazon_creators_v1',[]);
if(($stored['client_secret']??null)!==$amazon_secret) hdar_fail('Amazon WP blank resave lost secret');
$a->save(['enabled'=>1,'marketplace'=>'www.amazon.de','credential_version'=>'3.2','partner_tag'=>'tag-21','client_id'=>'cid','remove_client_secret'=>1]);
$stored=get_option('hdar_amazon_creators_v1',[]);
if(($stored['client_secret']??'x')!=='') hdar_fail('Amazon WP explicit removal');
hdar_ok('Amazon WordPress option roundtrip');

$i=new HDAR_WP_Idealo_Roundtrip();
$idealo_key='wp-runtime-idealo-key';
$i->save(['enabled'=>1,'api_key'=>$idealo_key,'adspace_id'=>'123','feed_id'=>'456','output_mode'=>'idealo_only','link_strategy'=>'hybrid']);
$stored=get_option('ppar_network_idealo_v1',[]);
if(($stored['api_key']??null)!==$idealo_key) hdar_fail('idealo WP initial key roundtrip');
$i->save(['enabled'=>1,'api_key'=>'','adspace_id'=>'123','feed_id'=>'456','output_mode'=>'idealo_only','link_strategy'=>'hybrid']);
$stored=get_option('ppar_network_idealo_v1',[]);
if(($stored['api_key']??null)!==$idealo_key) hdar_fail('idealo WP blank resave lost key');
$i->save(['enabled'=>1,'remove_api_key'=>1,'adspace_id'=>'123','feed_id'=>'456','output_mode'=>'idealo_only','link_strategy'=>'hybrid']);
$stored=get_option('ppar_network_idealo_v1',[]);
if(($stored['api_key']??'x')!=='') hdar_fail('idealo WP explicit removal');
hdar_ok('idealo WordPress option roundtrip');

echo "WORDPRESS_RUNTIME_SECRET_VALUES_NOT_PRINTED=PASS\n";
