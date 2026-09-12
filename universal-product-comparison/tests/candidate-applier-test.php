<?php
define('ABSPATH', __DIR__.'/');
class WP_Error { public $code; function __construct($c,$m=''){ $this->code=$c; } }
function is_wp_error($v){return $v instanceof WP_Error;}
function sanitize_text_field($v){return trim((string)$v);} function sanitize_textarea_field($v){return trim((string)$v);} function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));} function esc_url_raw($v){return preg_match('#^https?://#',(string)$v)?(string)$v:'';}
class UPK_Repository { const SUBJECT_PRODUCT='product'; }
class FakeDB { public $queries=[]; function query($q){$this->queries[]=$q; return true;} }
class FakeMaintenance { public $existing=0; function find_product_id_by_identity($i){return $this->existing;} }
class FakeKnowledge { public $created=[]; public $facts=[]; public $create_error=null; public $fact_error_at=0; function create_product($d){$this->created[]=$d; return $this->create_error ?: 77;} function add_fact($t,$id,$d){$this->facts[]=$d; if($this->fact_error_at && count($this->facts)===$this->fact_error_at)return new WP_Error('FACT_FAIL'); return count($this->facts);} }
require dirname(__DIR__).'/src/class-upc-candidate-applier.php';
function ok($c,$m){if(!$c){fwrite(STDERR,"FAIL:$m\n");exit(1);}echo"PASS:$m\n";}
$c=['status'=>'CANDIDATE_RESEARCH_READY','persisted'=>false,'identity'=>['manufacturer'=>'Acme','model_name'=>'Rain 1','product_group_key'=>'regendecken','generation'=>''],'manufacturer_product_url'=>'https://manufacturer.example/rain1','verified_at'=>'2026-09-12 00:00:00','facts'=>[['fact_key'=>'material','fact_value'=>'600D','fact_note'=>'','unit'=>'','source_url'=>'https://manufacturer.example/rain1','source_type'=>'MANUFACTURER','verified_at'=>'2026-09-12 00:00:00','fact_status'=>'VERIFIED']]];
$r=['seo_status'=>'PASS','comparability_status'=>'PASS','product_group_key'=>'regendecken'];
$db=new FakeDB();$k=new FakeKnowledge();$m=new FakeMaintenance();$a=new UPC_Candidate_Applier($db,$k,$m);
$x=$a->apply($c,$r);ok($x['status']==='NEW_PRODUCT_ACCEPTED'&&$x['reevaluate_product_group']===true&&$x['automatic_comparison_created']===false&&$x['article_write']===false,'new candidate accepted without comparison/article');ok($db->queries===['START TRANSACTION','COMMIT'],'successful apply commits atomically');ok($k->created[0]['lifecycle_status']==='UNKNOWN','lifecycle is not guessed');
$bad=$r;$bad['seo_status']='FAIL';$x=$a->apply($c,$bad);ok(is_wp_error($x)&&$x->code==='UPC_CANDIDATE_SEO_NOT_PASS','seo fail blocks');
$bad=$r;$bad['comparability_status']='FAIL';$x=$a->apply($c,$bad);ok(is_wp_error($x)&&$x->code==='UPC_CANDIDATE_COMPARABILITY_NOT_PASS','comparability fail blocks');
$bad=$r;$bad['product_group_key']='winterdecken';$x=$a->apply($c,$bad);ok(is_wp_error($x)&&$x->code==='UPC_CANDIDATE_RELEASE_GROUP_MISMATCH','release group mismatch blocks');
$m->existing=55;$x=$a->apply($c,$r);ok($x['status']==='EXISTING_PRODUCT_USE_REFRESH'&&$x['product_id']===55,'race-safe existing identity uses refresh');$m->existing=0;
$db=new FakeDB();$k=new FakeKnowledge();$k->create_error=new WP_Error('CREATE_FAIL');$a=new UPC_Candidate_Applier($db,$k,$m);$x=$a->apply($c,$r);ok(is_wp_error($x)&&$x->code==='CREATE_FAIL'&&end($db->queries)==='ROLLBACK','create failure rolls back');
$db=new FakeDB();$k=new FakeKnowledge();$k->fact_error_at=1;$a=new UPC_Candidate_Applier($db,$k,$m);$x=$a->apply($c,$r);ok(is_wp_error($x)&&$x->code==='FACT_FAIL'&&end($db->queries)==='ROLLBACK','fact failure rolls back');
$badc=$c;$badc['status']='RESEARCH_REQUIRED';$x=$a->apply($badc,$r);ok(is_wp_error($x)&&$x->code==='UPC_CANDIDATE_NOT_READY','unresearched candidate blocks');
$src=file_get_contents(dirname(__DIR__).'/src/class-upc-candidate-applier.php');ok(false===stripos($src,'create_comparison')&&false===stripos($src,'wp_insert_post')&&false===stripos($src,'wp_update_post'),'applier has no comparison or article write');
echo "UPC_CANDIDATE_APPLIER_GESAMT_PASS\n";
