<?php
define('ABSPATH', __DIR__ . '/');
define('ARRAY_A', 'ARRAY_A');

class WP_Error {
    private $code;
    public function __construct($code,$message=''){ $this->code=$code; }
    public function get_error_code(){ return $this->code; }
}
function is_wp_error($v){ return $v instanceof WP_Error; }
function absint($v){ return abs((int)$v); }
function sanitize_key($v){ return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v)); }
function sanitize_text_field($v){ return trim((string)$v); }
function sanitize_textarea_field($v){ return trim((string)$v); }
function esc_url_raw($v){ return preg_match('#^https?://#',(string)$v) ? (string)$v : ''; }
function current_time($type,$gmt=false){ return '2026-09-12 10:00:00'; }

class FakeDB {
    public $prefix='wp_';
    public $last_error='';
    public $insert_id=10;
    public $existing_identifier=null;
    public $last_insert=null;
    public $last_update=null;
    public $last_results_query='';
    public function prepare($q,...$args){ return ['query'=>$q,'args'=>$args]; }
    public function get_var($p){
        if(false!==strpos($p['query'],'wp_upk_products')) return 1;
        if(false!==strpos($p['query'],'wp_upk_variants')) return 2;
        if(false!==strpos($p['query'],'wp_upk_facts')) return 0;
        return null;
    }
    public function get_row($p,$format=null){
        if(false!==strpos($p['query'],'wp_upk_identifiers')) return $this->existing_identifier;
        if(false!==strpos($p['query'],'wp_upk_products')) return ['id'=>1,'manufacturer'=>'Maker','model_name'=>'Model','product_group_key'=>'group'];
        return null;
    }
    public function insert($table,$data,$formats){
        $this->last_insert=['table'=>$table,'data'=>$data,'formats'=>$formats];
        return 1;
    }
    public function update($table,$data,$where,$formats,$where_formats){
        $this->last_update=['table'=>$table,'data'=>$data,'where'=>$where];
        return 1;
    }
    public function get_results($p,$format=null){
        $this->last_results_query=$p['query'];
        return [];
    }
}
function ok($cond,$label){
    if(!$cond){ fwrite(STDERR,"FAIL:$label\n"); exit(1); }
    echo "PASS:$label\n";
}

require dirname( __DIR__, 2 ) . '/universal-product-knowledge/src/class-upk-repository.php';
$db=new FakeDB();
$repo=new UPK_Repository($db);

$id=$repo->add_identifier(UPK_Repository::SUBJECT_PRODUCT,1,'EAN','4000000000001');
ok($id===10,'legacy identifier remains insertable');
ok($db->last_insert['data']['source_url']==='' && $db->last_insert['data']['source_type']==='' && $db->last_insert['data']['verified_at']===null,'legacy identifier remains unbound');

$id=$repo->add_identifier(UPK_Repository::SUBJECT_PRODUCT,1,'EAN','4000000000002',[
    'source_url'=>'https://maker.example/model',
    'source_type'=>'MANUFACTURER',
    'verified_at'=>'2026-09-12'
]);
ok($id===10,'source-bound identifier inserts');
ok($db->last_insert['data']['source_url']==='https://maker.example/model','identifier source url stored');
ok($db->last_insert['data']['source_type']==='MANUFACTURER','identifier source type stored');
ok($db->last_insert['data']['verified_at']==='2026-09-12 00:00:00','identifier verified date normalized');

$bad=$repo->add_identifier(UPK_Repository::SUBJECT_PRODUCT,1,'EAN','4000000000003',[
    'source_url'=>'',
    'source_type'=>'MANUFACTURER',
    'verified_at'=>'2026-09-12'
]);
ok(is_wp_error($bad) && $bad->get_error_code()==='UPK_IDENTIFIER_EVIDENCE_INCOMPLETE','partial evidence blocked');

$bad=$repo->add_identifier(UPK_Repository::SUBJECT_PRODUCT,1,'EAN','4000000000003',[
    'source_url'=>'https://maker.example/model',
    'source_type'=>'MANUFACTURER',
    'verified_at'=>'not-a-date'
]);
ok(is_wp_error($bad) && $bad->get_error_code()==='UPK_INVALID_DATETIME','invalid identifier date blocked');

$db->existing_identifier=['id'=>7,'subject_type'=>'product','subject_id'=>1];
$id=$repo->add_identifier(UPK_Repository::SUBJECT_PRODUCT,1,'EAN','4000000000002',[
    'source_url'=>'https://maker.example/model-v2',
    'source_type'=>'OFFICIAL_DOCUMENTATION',
    'verified_at'=>'2026-09-13'
]);
ok($id===7,'existing same identifier reused');
ok($db->last_update['data']['source_url']==='https://maker.example/model-v2' && $db->last_update['data']['source_type']==='OFFICIAL_DOCUMENTATION','existing identifier evidence updates');

$db->existing_identifier=['id'=>8,'subject_type'=>'product','subject_id'=>99];
$bad=$repo->add_identifier(UPK_Repository::SUBJECT_PRODUCT,1,'EAN','4000000000002',[
    'source_url'=>'https://maker.example/model',
    'source_type'=>'MANUFACTURER',
    'verified_at'=>'2026-09-12'
]);
ok(is_wp_error($bad) && $bad->get_error_code()==='UPK_IDENTIFIER_CONFLICT','identifier conflict remains fail closed');

$db->existing_identifier=null;
$repo->get_product_bundle(1);
ok(false!==strpos($db->last_results_query,'source_url') && false!==strpos($db->last_results_query,'source_type') && false!==strpos($db->last_results_query,'verified_at'),'identifier readback includes evidence');

$plugin=file_get_contents(dirname( __DIR__, 2 ) . '/universal-product-knowledge/universal-product-knowledge.php');
ok(false!==strpos($plugin,"UPK_SCHEMA_VERSION', '3'"),'schema bumped to 3');
ok(false!==strpos($plugin,'source_url text NULL') && false!==strpos($plugin,"source_type varchar(32) NOT NULL DEFAULT ''") && false!==strpos($plugin,'verified_at datetime NULL'),'identifier table receives evidence columns');
ok(false===stripos($plugin,'CREATE TABLE wp_'),'no second identifier table introduced');

require dirname( __DIR__ ) . '/src/class-upc-affiliate-bridge.php';
$method=new ReflectionMethod('UPC_Affiliate_Bridge','exact_identifiers');
$method->setAccessible(true);
$knowledge=['identifiers'=>[
    ['identifier_type'=>'EAN','identifier_value'=>'4000000000001','source_url'=>'https://maker.example/a','source_type'=>'MANUFACTURER','verified_at'=>'2026-09-12'],
    ['identifier_type'=>'GTIN','identifier_value'=>'04000000000018','source_url'=>'https://maker.example/b','source_type'=>'OFFICIAL_DOCUMENTATION','verified_at'=>'2026-09-12'],
    ['identifier_type'=>'MPN','identifier_value'=>'MPN-SECONDARY','source_url'=>'https://shop.example/x','source_type'=>'APPROVED_SECONDARY','verified_at'=>'2026-09-12'],
    ['identifier_type'=>'EAN','identifier_value'=>'4000000000009','source_url'=>'','source_type'=>'','verified_at'=>''],
    ['identifier_type'=>'MANUFACTURER_ARTICLE_NUMBER','identifier_value'=>'ART-1','source_url'=>'https://maker.example/a','source_type'=>'MANUFACTURER','verified_at'=>'2026-09-12'],
    ['identifier_type'=>'MPN','identifier_value'=>'MPN-BADDATE','source_url'=>'https://maker.example/a','source_type'=>'MANUFACTURER','verified_at'=>'not-a-date'],
]];
$out=$method->invoke(null,$knowledge);
ok(count($out)===2,'affiliate only receives official source-bound exact identifiers');
ok($out[0]['type']==='EAN' && $out[1]['type']==='GTIN','affiliate preserves only allowed exact types');

require dirname( __DIR__, 2 ) . '/universal-product-knowledge/src/class-upk-change-fingerprint.php';
class FPRepo {
    public $bundle;
    public function get_product_bundle($id){ return $this->bundle; }
    public function get_variant_bundle($id){ return new WP_Error('NA'); }
}
$fpRepo=new FPRepo();
$base=[
 'manufacturer'=>'Maker','model_name'=>'Model','model_family'=>'','product_group_key'=>'group',
 'manufacturer_product_url'=>'https://maker.example/model','generation'=>'','lifecycle_status'=>'ACTIVE','successor_product_id'=>null,
 'identifiers'=>[['identifier_type'=>'EAN','identifier_value'=>'4000000000001','source_url'=>'https://maker.example/id','source_type'=>'MANUFACTURER','verified_at'=>'2026-09-12']],
 'facts'=>[]
];
$fpRepo->bundle=$base; $fp=new UPK_Change_Fingerprint($fpRepo); $h1=$fp->product(1);
$base['identifiers'][0]['verified_at']='2026-10-12'; $fpRepo->bundle=$base; $h2=$fp->product(1);
ok($h1===$h2,'identifier re-verification date alone does not trigger semantic change');
$base['identifiers'][0]['source_url']='https://maker.example/id-v2'; $fpRepo->bundle=$base; $h3=$fp->product(1);
ok($h2!==$h3,'identifier evidence source change triggers semantic change');

echo "UPK_IDENTIFIER_EVIDENCE_AFFILIATE_GESAMT_PASS\n";
