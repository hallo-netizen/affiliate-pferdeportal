<?php
define('ABSPATH', __DIR__ . '/');
define('ARRAY_A', 'ARRAY_A');
class WP_Error { private $code; function __construct($c,$m=''){ $this->code=$c; } function get_error_code(){ return $this->code; } }
function is_wp_error($v){ return $v instanceof WP_Error; }
function absint($v){ return abs((int)$v); }
function sanitize_key($v){ return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v)); }
function sanitize_text_field($v){ return trim((string)$v); }
function esc_url_raw($v){ return preg_match('#^https?://#',(string)$v) ? (string)$v : ''; }
class UPK_Repository { const SUBJECT_PRODUCT='product'; }
class DB {
 public $prefix='wp_'; public $last=null; public $rows=[];
 function prepare($q,...$args){ $this->last=['query'=>$q,'args'=>$args]; return $this->last; }
 function get_results($prepared,$format=null){ return $this->rows; }
}
function ok($c,$m){ if(!$c){fwrite(STDERR,"FAIL:$m\n");exit(1);} echo "PASS:$m\n"; }
require dirname( __DIR__ ) . '/src/class-upc-affiliate-bridge.php';

$db=new DB();
$GLOBALS['wpdb']=$db;
$db->rows=[
 ['id'=>2,'manufacturer'=>'Maker B','model_name'=>'Model B','product_group_key'=>'regendecken','manufacturer_product_url'=>'https://maker.example/b','last_verified_at'=>'2026-09-01'],
 ['id'=>5,'manufacturer'=>'Maker C','model_name'=>'Model C','product_group_key'=>'winterdecken','manufacturer_product_url'=>'https://maker.example/c','last_verified_at'=>'2026-08-01'],
];
$r=UPC_Affiliate_Bridge::missing_identifier_products(999);
ok($r['status']==='AFFILIATE_IDENTIFIER_RESEARCH_REQUIRED' && $r['count']===2,'coverage positive');
ok($r['products'][0]['requested_identifier_types']===['GTIN','EAN','MPN'],'requests exact identifier types only');
ok($db->last['args'][6]===500,'coverage limit hard capped');
$q=$db->last['query'];
ok(false!==strpos($q,"identifier_type IN (%s,%s,%s)"),'query requires GTIN EAN MPN');
ok(false!==strpos($q,"source_type IN (%s,%s)"),'query requires official source type');
ok(false!==strpos($q,"i.source_url <> ''") && false!==strpos($q,'i.verified_at IS NOT NULL'),'query requires source url and verified date');
ok(false!==strpos($q,"lifecycle_status IN ('ACTIVE','TEMPORARILY_UNAVAILABLE','UNKNOWN')"),'discontinued products excluded');

$db->rows=[];
$r=UPC_Affiliate_Bridge::missing_identifier_products(100,'Regendecken');
ok($r['count']===0,'covered group may return empty');
ok(false!==strpos($db->last['query'],'p.product_group_key = %s') && $db->last['args'][0]==='regendecken','optional group filter bound');
ok($db->last['args'][7]===100,'group query limit bound');

$db->rows=[['id'=>9,'manufacturer'=>'','model_name'=>'Broken','product_group_key'=>'regendecken','manufacturer_product_url'=>'https://maker.example/broken']];
$r=UPC_Affiliate_Bridge::missing_identifier_products();
ok(is_wp_error($r) && $r->get_error_code()==='UPC_IDENTIFIER_COVERAGE_PRODUCT_INVALID','incomplete row blocks fail closed');

$src=file_get_contents(dirname( __DIR__ ) . '/src/class-upc-affiliate-identifier-coverage.php');
ok(false===stripos($src,'INSERT INTO') && false===stripos($src,'UPDATE ') && false===stripos($src,'DELETE FROM'),'coverage is read only');
ok(false===stripos($src,'CREATE TABLE') && false===stripos($src,'wp_schedule'),'coverage adds no storage or scheduler');
echo "UPC_AFFILIATE_IDENTIFIER_COVERAGE_GESAMT_PASS\n";
