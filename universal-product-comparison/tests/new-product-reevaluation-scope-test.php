<?php

define( 'ABSPATH', __DIR__ . '/' );
class WP_Error { private $code; public function __construct($c,$m=''){ $this->code=$c; } public function get_error_code(){ return $this->code; } }
function is_wp_error($v){ return $v instanceof WP_Error; }
function absint($v){ return abs((int)$v); }
function sanitize_key($v){ return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v)); }
class UPK_Repository { const SUBJECT_PRODUCT='product'; const SUBJECT_VARIANT='variant'; }

class Scope_Fake_WPDB {
    public $prefix='wp_';
    public $queries=[];
    public $write_count=0;
    public function prepare($query,...$args){ return ['query'=>$query,'args'=>$args]; }
    public function get_var($prepared){
        $this->queries[]=$prepared;
        $q=$prepared['query']; $id=(int)($prepared['args'][0]??0);
        if(false!==strpos($q,'SELECT product_group_key')){
            if(77===$id)return 'regendecken';
            if(88===$id)return '';
            return null;
        }
        if(false!==strpos($q,'SELECT id FROM wp_upk_products')){
            return in_array($id,[77,88],true)?$id:null;
        }
        return null;
    }
    public function get_col($prepared){
        $this->queries[]=$prepared;
        $q=$prepared['query'];
        if(false!==strpos($q,'FROM wp_upk_products') && false!==strpos($q,'id <> %d')){
            return ['12','5','12'];
        }
        if(false!==strpos($q,'FROM wp_upc_comparisons')){
            return ['9','3','9'];
        }
        return [];
    }
    public function insert(){ $this->write_count++; return 1; }
    public function update(){ $this->write_count++; return 1; }
    public function delete(){ $this->write_count++; return 1; }
    public function query($q){ $this->write_count++; return true; }
}
function ok($c,$m){ if(!$c){fwrite(STDERR,"FAIL:$m\n");exit(1);} echo "PASS:$m\n"; }
require dirname(__DIR__).'/src/class-upc-maintenance.php';
$db=new Scope_Fake_WPDB(); $m=new UPC_Maintenance($db);
$r=$m->reevaluation_scope_for_new_product(77);
ok(!is_wp_error($r),'new product scope positive');
ok($r['product_group_key']==='regendecken','product group resolved from stored product');
ok($r['peer_product_ids']===[5,12],'peer products normalized and deduplicated');
ok($r['existing_comparison_ids']===[3,9],'existing comparisons normalized and deduplicated');
ok($r['automatic_comparison_created']===false,'scope creates no automatic comparison');
$peer_query=''; $comparison_query=''; foreach($db->queries as $p){if(false!==strpos($p['query'],'id <> %d'))$peer_query=$p['query']; if(false!==strpos($p['query'],'FROM wp_upc_comparisons'))$comparison_query=$p['query'];}
ok(false!==strpos($peer_query,"lifecycle_status IN ('ACTIVE','TEMPORARILY_UNAVAILABLE','UNKNOWN')"),'discontinued peers excluded');
ok(false!==strpos($peer_query,'product_group_key = %s') && false!==strpos($peer_query,'id <> %d'),'peer scope stays same group and excludes new product');
ok(false!==strpos($comparison_query,'product_group_key = %s'),'comparison scope stays same group');
ok($db->write_count===0,'scope is read only');
$r=$m->reevaluation_scope_for_new_product(999); ok(is_wp_error($r)&&$r->get_error_code()==='UPC_PRODUCT_NOT_FOUND','unknown product blocked');
$r=$m->reevaluation_scope_for_new_product(88); ok(is_wp_error($r)&&$r->get_error_code()==='UPC_PRODUCT_GROUP_MISSING','missing group blocked');
$src=file_get_contents(dirname(__DIR__).'/src/class-upc-maintenance.php');
ok(false===stripos($src,'create_comparison')&&false===stripos($src,'wp_insert_post')&&false===stripos($src,'wp_update_post'),'scope contains no comparison/article write');
echo "UPC_NEW_PRODUCT_REEVALUATION_SCOPE_GESAMT_PASS\n";
