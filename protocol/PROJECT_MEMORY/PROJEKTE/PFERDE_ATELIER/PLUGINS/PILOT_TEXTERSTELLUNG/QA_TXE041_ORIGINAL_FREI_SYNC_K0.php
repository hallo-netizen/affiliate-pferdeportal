<?php
error_reporting(E_ALL);
define('ABSPATH','/qa/');
$GLOBALS['options']=[];
class FakeDB { public $prefix='wp_';public function prepare($q,...$v){return vsprintf(str_replace('%s',"'%s'",$q),$v);}public function get_var($q){return '1';}}
$GLOBALS['wpdb']=new FakeDB();
function home_url($p='/'){return 'https://qa.example.invalid/';}
function get_current_blog_id(){return 1;}
function current_user_can($s){return true;}
function get_option($k,$d=false){return $GLOBALS['options'][$k]??$d;}
function get_site_option($k,$d=false){return $d;}
function update_option($k,$v,$autoload=false){$GLOBALS['options'][$k]=$v;return true;}
function add_action(...$args){return true;}
function add_filter(...$args){return true;}
function register_activation_hook(...$args){}
function is_admin(){return false;}
function wp_json_encode($x,$opts=0){return json_encode($x,$opts);}
function wp_strip_all_tags($x){return strip_tags($x);}
function get_term_by($key,$value,$taxonomy){return (object)['term_id'=>4,'slug'=>$value];}
require dirname(__DIR__).'/txe041_original_k0/texterstellung/texterstellung.php';
$GLOBALS['options'][TXE_Workshop::TEST_MODE_OPTION]=hash('sha256',home_url('/').'|'.get_current_blog_id());
$checks=[];$errors=[];
function qa($label,$fn){global $checks,$errors;try{$checks[$label]=($fn()===true);}catch(Throwable $e){$checks[$label]=false;$errors[$label]=$e->getMessage();}}
$pool='pste-raw-12';$keyword='Pferdefutter im Winter lagern';$article='PSTE-original-article-123';$slot=PSERC_Plan_Slot_Identity::tokenFromCanonicalId($article);
function stateFor(string $pool,string $keyword,?string $article,?string $slot):array {
    return ['completed'=>[],'active'=>null,'clarification'=>[],
     'seo_decisions'=>[$pool=>[
      'contract'=>'PSTE_MINI_SEO_DECISIONS_V1','box'=>'FREI','raw_query'=>$keyword,'source_sha256'=>hash('sha256',$pool.'|'.$keyword),
      'approved_title'=>'Pferdefutter im Winter richtig lagern',
      'category_slug'=>$article?'pferdefutter':'','article_type'=>$article?'RATGEBER':'',
      'canonical_article_id'=>$article??'','plan_slot'=>$slot??'','intent_summary'=>'Pferdefutter lagerung',
     ]]];
}
$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']=stateFor($pool,$keyword,null,null);
qa('original_proof_is_verified_by_pste',fn()=>PSTE_Mini_Workflow::hasStoredFinalFrei($pool,$keyword));
qa('incomplete_original_is_held',function(){ $result=TXE_Workshop::loadLegacyApprovals();$o=array_values($GLOBALS['options'][TXE_Workshop::OPTION]['orders'])[0];return $result['held']===1&&$o['status']==='METADATEN_OFFEN'&&$o['article_id']===''&&$o['plan_slot']==='';});
qa('empty_original_does_not_create_article_slot',function(){$s=$GLOBALS['options'][TXE_Workshop::OPTION];return count($s['orders'])===1&&$s['orders'][array_key_first($s['orders'])]['plan_slot']==='';});
$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']=stateFor($pool,$keyword,$article,$slot);
qa('export_auto_synchronizes_completed_original',function()use($slot,$article){$out=TXE_Workshop::export(1);$o=array_values($GLOBALS['options'][TXE_Workshop::OPTION]['orders'])[0];return $out['item_count']===1&&$out['items'][0]['plan_slot']===$slot&&$o['article_id']===$article&&$o['status']==='EXPORTIERT';});
qa('no_duplicate_order_from_original_sync',fn()=>count($GLOBALS['options'][TXE_Workshop::OPTION]['orders'])===1);
qa('original_metadata_contract_valid',function(){$batch=$GLOBALS['options'][TXE_Workshop::OPTION]['last_batch'];return PSERC_Metadata_Boundary::validateBatch($batch)['ok']===true;});
qa('second_export_never_duplicates',function(){try{TXE_Workshop::export(1);return false;}catch(RuntimeException $e){return $e->getMessage()==='NO_APPROVED_READY_ARTICLES'&&count($GLOBALS['options'][TXE_Workshop::OPTION]['orders'])===1;}});
qa('unchanged_download_is_same',function(){$batch=$GLOBALS['options'][TXE_Workshop::OPTION]['last_batch'];return serialize(TXE_Workshop::redownloadBatch($batch['batch_sha256']))===serialize($batch);});
qa('no_new_original_decision_after_booking',fn()=>PSTE_Mini_Workflow::hasStoredFinalFrei('pste-raw-12','Pferdefutter im Winter lagern'));
$partial=['id'=>'manual','source_id'=>'pste-partial','origin'=>'ALT_FREIGABE','target_keyword'=>'Pferdefutter bei kalten Nächten','title'=>'Pferdefutter kühlen','category'=>'pferdefutter','article_type'=>'RATGEBER','article_id'=>'','plan_slot'=>$slot,'status'=>'FREI'];
qa('old_missing_canonical_never_becomes_exportable',function()use($partial){$m=new ReflectionMethod('TXE_Workshop','ready');return $m->invoke(null,$partial)===false;});
$pass=count(array_filter($checks));$total=count($checks);echo json_encode(['pass'=>$pass,'total'=>$total,'checks'=>$checks,'errors'=>$errors],JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),"\n";exit($pass===$total?0:1);
