<?php
error_reporting(E_ALL);
define('ABSPATH','/qa/');
$GLOBALS['options']=[];
$GLOBALS['hooks']=[];
class FakeDB { public $prefix='wp_';public function prepare($q,...$v){return vsprintf(str_replace('%s',"'%s'",$q),$v);}public function get_var($q){return '1';}}
$GLOBALS['wpdb']=new FakeDB();
function home_url($p='/'){return 'https://qa.example.invalid/';}
function get_current_blog_id(){return 1;}
function current_user_can($s){return true;}
function get_option($k,$d=false){return $GLOBALS['options'][$k]??$d;}
function get_site_option($k,$d=false){return $d;}
function update_option($k,$v,$autoload=false){$GLOBALS['options'][$k]=$v;return true;}
function add_action(...$args){$GLOBALS['hooks'][$args[0]][]=$args[1];return true;}
function add_filter(...$args){return add_action(...$args);}
function register_activation_hook(...$args){}
function is_admin(){return false;}
function wp_json_encode($x,$opts=0){return json_encode($x,$opts);}
function wp_strip_all_tags($x){return strip_tags($x);}
require dirname(__DIR__).'/txe041_original_k0/texterstellung/texterstellung.php';
$GLOBALS['options'][TXE_Workshop::TEST_MODE_OPTION]=hash('sha256',home_url('/').'|'.get_current_blog_id());
$checks=[];
function qa($label,$callback){try {$result=$callback();$GLOBALS['checks'][$label]=$result===true;}catch(Throwable $e){$GLOBALS['checks'][$label]=false;$GLOBALS['errors'][$label]=$e->getMessage();}}
$sample=function($n){$id='original-article-'.$n;return ['id'=>'TXE-'.$n,'title'=>'Pferdefutter richtig lagern '.$n,'target_keyword'=>'pferdefutter lagerung '.$n,'category'=>'futter','article_type'=>'RATGEBER','plan_slot'=>PSERC_Plan_Slot_Identity::tokenFromCanonicalId($id),'article_id'=>$id,'status'=>'FREI','batch'=>'','post_id'=>0];};
$orders=array_map($sample,range(1,20));
$reflection=new ReflectionMethod('TXE_Workshop','assemble');
$batch=$reflection->invoke(null,$orders);
$expected=PSERC_Plan_Snapshot_Store::batchFromItems(array_map(fn($o)=>array_intersect_key($o,array_fill_keys(['title','target_keyword','category','article_type','plan_slot'],1)),$orders));
qa('original_psेrc_batch_bytes_identical',fn()=>serialize($batch)===serialize($expected));
qa('exactly_five_k0_fields',fn()=>count($batch['items'])===20&&count($batch['items'][0])===5&&array_keys($batch['items'][0])===['title','target_keyword','category','article_type','plan_slot']);
qa('original_metadata_boundary_pass',fn()=>PSERC_Metadata_Boundary::validateBatch($batch)['ok']===true);
qa('no_publish_flag',fn()=>($batch['publish_allowed']??null)===false);
qa('all_twenty_preserve_original_slots',fn()=>array_column($batch['items'],'plan_slot')===array_column($orders,'plan_slot'));
qa('original_hash_matches',fn()=>hash_equals(PSERC_Stable_Json::hash(array_diff_key($batch,['batch_sha256'=>true])),$batch['batch_sha256']));
qa('tamper_is_rejected',function()use($batch){$a=$batch;$a['items'][0]['target_keyword']='tampered';return PSERC_Metadata_Boundary::validateBatch($a)['ok']===false;});
qa('duplicate_slot_is_rejected',function()use($batch){$a=$batch;$a['items'][1]['plan_slot']=$a['items'][0]['plan_slot'];$tmp=$a;unset($tmp['batch_sha256']);$a['batch_sha256']=PSERC_Stable_Json::hash($tmp);return PSERC_Metadata_Boundary::validateBatch($a)['ok']===false;});
qa('duplicate_title_is_rejected',function()use($batch){$a=$batch;$a['items'][1]['title']=$a['items'][0]['title'];$tmp=$a;unset($tmp['batch_sha256']);$a['batch_sha256']=PSERC_Stable_Json::hash($tmp);return PSERC_Metadata_Boundary::validateBatch($a)['ok']===false;});
qa('extra_payload_is_rejected',function()use($batch){$a=$batch;$a['items'][0]['content_html']='unsafe';$tmp=$a;unset($tmp['batch_sha256']);$a['batch_sha256']=PSERC_Stable_Json::hash($tmp);return PSERC_Metadata_Boundary::validateBatch($a)['ok']===false;});
qa('empty_batch_is_not_exported',function()use($reflection){try{$reflection->invoke(null,[]);return false;}catch(RuntimeException $e){return str_contains($e->getMessage(),'PSERC_METADATA_NO_READY_ITEMS');}});
$GLOBALS['options'][TXE_Workshop::OPTION]=['version'=>1,'orders'=>array_combine(array_column($orders,'id'),$orders),'last_batch'=>null,'research'=>[],'title_batches'=>[],'active_title_batch'=>''];
$exp=TXE_Workshop::export(13);
qa('export_reserves_exactly_13',fn()=>count(array_filter($GLOBALS['options'][TXE_Workshop::OPTION]['orders'],fn($o)=>$o['status']==='EXPORTIERT'))===13 && $exp['item_count']===13);
qa('redownload_identical_no_second_booking',fn()=>serialize(TXE_Workshop::redownloadBatch($exp['batch_sha256']))===serialize($exp));
$second=TXE_Workshop::export(20);
qa('second_export_seven_remaining',fn()=>$second['item_count']===7&&count(array_filter($GLOBALS['options'][TXE_Workshop::OPTION]['orders'],fn($o)=>$o['status']==='EXPORTIERT'))===20);
qa('unchanged_original_source_paths',fn()=>class_exists('PSERC_Metadata_Boundary',false)&&class_exists('PSERC_Plan_Snapshot_Store',false));
$count=count($checks);$passed=count(array_filter($checks));$result=['passed'=>$passed,'total'=>$count,'checks'=>$checks,'errors'=>$GLOBALS['errors']??[]];echo json_encode($result,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),'\n';exit($passed===$count?0:1);