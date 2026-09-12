<?php
error_reporting(E_ALL);
define('ABSPATH', __DIR__ . '/');
class WP_Error { public $code; public $message; public $data; function __construct($c,$m,$d=null){$this->code=$c;$this->message=$m;$this->data=$d;} }
function is_wp_error($v){ return $v instanceof WP_Error; }
function sanitize_text_field($v){ return trim((string)$v); }
function sanitize_textarea_field($v){ return trim((string)$v); }
function sanitize_key($v){ return preg_replace('/[^a-z0-9_\-]/','', strtolower((string)$v)); }
function esc_url_raw($v){ return preg_match('#^https?://#', (string)$v) ? (string)$v : ''; }
class FakeMaintenance { public $existing=0; public $calls=0; function find_product_id_by_identity($x){$this->calls++; return $this->existing;} }
class FakeCatalog { function resolve($label){ $map=['Material'=>'material','Gewicht'=>'weight']; return isset($map[$label]) ? $map[$label] : new WP_Error('UPC_FEATURE_LABEL_UNKNOWN','unknown'); } }
require dirname(__DIR__) . '/src/class-upc-candidate-gate.php';
function ok($cond,$msg){ if(!$cond){fwrite(STDERR,"FAIL:$msg\n"); exit(1);} echo "PASS:$msg\n"; }
$policy=['schema_version'=>'1','market_gate'=>['minimum_independent_dossiers'=>4,'exact_product_identity_required'=>true,'official_manufacturer_sources_required'=>true,'comparability_gate_required'=>true], 'groups'=>[
 ['product_group_key'=>'regendecken','required_additional_contracts'=>[]],
 ['product_group_key'=>'hufschuhe','required_additional_contracts'=>['SAFETY_FIT_ADDITIONAL_CONTRACT']]
]];
$m=new FakeMaintenance(); $g=new UPC_Candidate_Gate($m,new FakeCatalog(),$policy);
$base=['manufacturer'=>'Acme','model_name'=>'Rain 1','product_group_key'=>'regendecken','manufacturer_product_url'=>'https://manufacturer.example/rain1'];
$r=$g->evaluate($base); ok($r['status']==='RESEARCH_REQUIRED' && $r['persisted']===false,'new signal stays read-only and requests research');
$m->existing=42; $r=$g->evaluate($base); ok($r['status']==='EXISTING_PRODUCT' && $r['product_id']===42 && $r['action']==='USE_REFRESH_PATH','existing identity routes to refresh');
$m->existing=0; $unknown=$base; $unknown['product_group_key']='neue-gruppe'; $r=$g->evaluate($unknown); ok($r['status']==='GROUP_MARKET_GATE_REQUIRED' && $r['minimum_independent_dossiers']===4,'unknown group routes to market gate');
$ready=$base; $ready['facts']=[['label'=>'Material','fact_value'=>'600D','source_url'=>'https://manufacturer.example/rain1','source_type'=>'MANUFACTURER','fact_status'=>'VERIFIED','verified_at'=>'2026-09-12']];
$r=$g->evaluate($ready); ok($r['status']==='CANDIDATE_RESEARCH_READY' && $r['facts'][0]['fact_key']==='material' && $r['automatic_comparison_created']===false,'official researched candidate is ready for SEO/comparability only');
$bad=$ready; $bad['facts'][0]['source_type']='APPROVED_SECONDARY'; $r=$g->evaluate($bad); ok(is_wp_error($r) && $r->code==='UPC_CANDIDATE_SOURCE_NOT_OFFICIAL','secondary source blocked');
$bad=$ready; $bad['facts'][0]['label']='Unbekannt'; $r=$g->evaluate($bad); ok(is_wp_error($r) && $r->code==='UPC_FEATURE_LABEL_UNKNOWN','unknown feature blocked');
$hoof=$ready; $hoof['product_group_key']='hufschuhe'; $r=$g->evaluate($hoof); ok(is_wp_error($r) && $r->code==='UPC_CANDIDATE_ADDITIONAL_CONTRACT_MISSING','missing safety-fit contract blocked');
$hoof['completed_contracts']=['SAFETY_FIT_ADDITIONAL_CONTRACT']; $r=$g->evaluate($hoof); ok($r['status']==='CANDIDATE_RESEARCH_READY','safety-fit contract allows candidate');
$bad=$base; $bad['manufacturer_product_url']=''; $r=$g->evaluate($bad); ok(is_wp_error($r) && $r->code==='UPC_CANDIDATE_IDENTITY_INCOMPLETE','incomplete identity blocked');
echo "UPC_CANDIDATE_GATE_GESAMT_PASS\n";
