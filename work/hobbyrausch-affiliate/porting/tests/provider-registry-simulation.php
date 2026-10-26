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
    $v = strtolower(trim((string)$v));
    $v = strtr($v, ['ä'=>'ae','ö'=>'oe','ü'=>'ue','ß'=>'ss']);
    $v = preg_replace('/[^a-z0-9]+/','-', $v);
    return trim($v,'-');
}
function sanitize_text_field($v){ return trim(strip_tags((string)$v)); }
function absint($v){ return abs((int)$v); }
function wp_json_encode($v,$flags=0){ return json_encode($v,$flags); }

$scenario = $argv[1] ?? '';
$GLOBALS['hd_registry_ready'] = !str_ends_with($scenario, '_missing');
$GLOBALS['hd_registry_snapshot'] = [
    'contract'=>'HD004_TEST',
    'revision'=>'test-1',
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

$root = dirname(__DIR__) . '/hobby-depot-affiliate-router/includes';
require_once $root . '/trait-hdar-amazon-creators.php';
require_once $root . '/trait-ppar-ebay.php';
require_once $root . '/trait-ppar-idealo.php';

class AmazonHarness {
    use HDAR_Amazon_Creators_Trait;
    public function runConcepts(){ return $this->amazon_creators_hobby_depot_concepts(); }
}
class EbayHarness {
    use PPAR_Ebay_Trait;
    public function runCatalog(){ return $this->ebay_portal_catalog(); }
}
class IdealoHarness {
    use PPAR_Idealo_Trait;
    public function runCatalog(){ return $this->idealo_portal_supply_catalog(); }
}

function fail($msg){ fwrite(STDERR, "FAIL: $msg\n"); exit(1); }
function pass($msg){ echo "PASS: $msg\n"; }

if ($scenario === 'amazon_missing') {
    $r=(new AmazonHarness())->runConcepts();
    if (!is_wp_error($r) || $r->get_error_code() !== 'amazon_hobby_depot_registry_missing') fail('amazon missing registry did not fail closed');
    pass('amazon missing registry fail-closed'); exit(0);
}
if ($scenario === 'amazon_valid') {
    $r=(new AmazonHarness())->runConcepts();
    if (is_wp_error($r) || count($r)!==1) fail('amazon valid registry concept count');
    if (($r[0]['title']??'')!=='Stricken' || !in_array('category:stricken-anfaenger',$r[0]['target_keys']??[],true)) fail('amazon valid registry target binding');
    pass('amazon valid HD-004 concept binding'); exit(0);
}
if ($scenario === 'ebay_missing') {
    $r=(new EbayHarness())->runCatalog();
    if (!is_wp_error($r) || $r->get_error_code() !== 'ebay_hobby_depot_registry_missing') fail('ebay missing registry did not fail closed');
    pass('ebay missing registry fail-closed'); exit(0);
}
if ($scenario === 'ebay_valid') {
    $r=(new EbayHarness())->runCatalog();
    if (is_wp_error($r) || ($r['schema']??'')!=='HOBBY_DEPOT_DYNAMIC_EBAY_V1') fail('ebay valid registry schema');
    if (($r['counts']['business_concepts']??0)!==1 || ($r['counts']['article_categories']??0)!==1) fail('ebay valid registry counts');
    pass('ebay valid HD-004 catalog binding'); exit(0);
}
if ($scenario === 'idealo_missing') {
    $r=(new IdealoHarness())->runCatalog();
    if (!is_wp_error($r) || $r->get_error_code() !== 'idealo_hobby_depot_registry_missing') fail('idealo missing registry did not fail closed');
    pass('idealo missing registry fail-closed'); exit(0);
}
if ($scenario === 'idealo_valid') {
    $r=(new IdealoHarness())->runCatalog();
    if (is_wp_error($r) || ($r['schema']??'')!=='HOBBY_DEPOT_DYNAMIC_REGISTRY_V1') fail('idealo valid registry schema');
    if (($r['counts']['product_concepts']??0)!==1 || ($r['counts']['article_targets']??0)!==1) fail('idealo valid registry counts');
    pass('idealo valid HD-004 catalog binding'); exit(0);
}
fail('unknown scenario ' . $scenario);
