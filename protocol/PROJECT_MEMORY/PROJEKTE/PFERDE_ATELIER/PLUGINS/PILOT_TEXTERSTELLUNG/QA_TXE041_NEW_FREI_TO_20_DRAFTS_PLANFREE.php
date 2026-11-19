<?php
// QA harness, NOT plugin code. Runs the actual candidate + unchanged PSTE/PSERC methods.
error_reporting(E_ALL);
define('ABSPATH','/qa/');define('ARRAY_A','ARRAY_A');
$GLOBALS['options']=[]; $GLOBALS['posts']=[]; $GLOBALS['next_post']=100; $GLOBALS['ppm_calls']=0; $GLOBALS['ppm_failure']=false;
class FakeDB {public string $prefix='wp_'; public string $last_error='';
 function prepare($sql,...$values){return vsprintf(str_replace('%s',"'%s'",$sql),$values);}
 function get_var($sql){return str_contains($sql,'GET_LOCK')||str_contains($sql,'RELEASE_LOCK')?'1':null;}
}
$GLOBALS['wpdb']=new FakeDB();
function home_url($path='/'){return 'https://qa.example.invalid/';} function get_current_blog_id(){return 1;}
function current_user_can($cap){return true;}function get_option($name,$default=false){return $GLOBALS['options'][$name]??$default;}
function get_site_option($name,$default=false){return $default;}
function update_option($name,$value,$autoload=false){$GLOBALS['options'][$name]=$value;return true;}
function add_action(...$args){} function add_filter($name,$fn,$priority=10,$args=1){$GLOBALS['filters'][$name][]=$fn;} function register_activation_hook(...$args){}
function qa_data_filter($value,$arr){foreach($GLOBALS['filters']['wp_insert_post_data']??[] as $cb)$value=$cb($value,$arr);return $value;}
function wp_json_encode($data,$opts=0){return json_encode($data,$opts);}function wp_strip_all_tags($s){return strip_tags($s);}
function is_admin(){return false;}
function get_term_by($field,$val,$taxonomy){return $val==='pferdepflege'?(object)['term_id'=>8,'slug'=>$val]:false;}
function sanitize_title($text){return trim(preg_replace('/[^a-z0-9]+/','-',strtolower($text)),'-');}
function wp_slash($v){return $v;}function is_wp_error($v){return false;}
function wp_insert_post($p,$err=false){$id=$GLOBALS['next_post']++;$GLOBALS['posts'][$id]=$p;return $id;}
function get_post($id,$output=null){return $GLOBALS['posts'][$id]??null;}
function get_post_meta($id,$key,$single=false){return $GLOBALS['posts'][$id]['meta_input'][$key]??'';}
function wp_get_post_categories($id){return $GLOBALS['posts'][$id]['post_category']??[];}
function get_posts($opts){return array_keys($GLOBALS['posts']);}
function wp_delete_post($id,$force=false){unset($GLOBALS['posts'][$id]);return true;}
 $GLOBALS['options']['texterstellung_testsite_confirmation_v1']=hash('sha256',home_url('/').'|'.get_current_blog_id());
require dirname(__DIR__).'/working_planfree_seo/texterstellung/texterstellung.php';
$GLOBALS['options'][TXE_Workshop::TEST_MODE_OPTION]=hash('sha256',home_url('/').'|'.get_current_blog_id());
$checks=[];$errors=[];
function ck($label,callable $f){global $checks,$errors;try{$checks[$label]=!!$f();}catch(Throwable $e){$checks[$label]=false;$errors[$label]=$e->getMessage();}}
// Generate the 20 FREI receipts with the actual (technically adapted) ORIGINAL PSTE SEO owner.
$sourceRows=[];$decisions=[];$idByIndex=[];
for($i=1;$i<=20;$i++){
 $key=hash('sha256','existing-pste-pool-key-'.$i);$raw='Pferdepflege im Test '.$i;
 $idByIndex[$i]=$key;
 $sourceRows[$key]=['id'=>$i,'pool_key'=>$key,'payload_json'=>json_encode([
   'raw_user_question'=>$raw,'proposed_article_type'=>'RATGEBER','target_category_slug'=>'pferdepflege'])];
 $decisions[]=['pool_key'=>$key,'box'=>'FREI','raw_query'=>$raw,
   'source_sha256'=>hash('sha256',$key.'|'.$raw),
   'intent_slot'=>hash('sha256','already approved unique intent '.$i),
   'approved_title'=>'','intent_summary'=>'Pferdepflege '.$i];
}
$sourceSnapshot=['complete'=>true,'sha256'=>str_repeat('d',64),'items'=>[]];
$sourceDocument=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','snapshot_sha256'=>$sourceSnapshot['sha256'],
 'owner'=>'EXTERNAL_SINGLE_SEO_EDITOR','items'=>$decisions];
$approval=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions(['seo_decisions'=>[]],$sourceDocument,$sourceSnapshot,$sourceRows,[]);
$proofs=$approval['seo_decisions'];
$sourceRowsList=array_values($sourceRows);$GLOBALS['idByIndex']=$idByIndex;
$originalSelection=PSTE_Mini_Workflow::selectApprovedTitleRows($sourceRowsList,[], $proofs,100);
$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']=['seo_decisions'=>$proofs,'completed'=>[]];

ck('new_frei_20_with_original_seo_owner',function()use($proofs,$idByIndex){return count($proofs)===20 && count(array_filter($proofs,static fn($p)=>($p['box']??'')==='FREI'))===20 && count(array_filter($proofs,static fn($p)=>($p['canonical_article_id']??'')!==''))===20 && ($proofs[$idByIndex[1]]['canonical_article_id']??'')===$idByIndex[1];});
ck('original_title_worker_eligible_20',function()use($originalSelection){return count($originalSelection['items'])===20 && ($originalSelection['title_only']??null)===true;});
ck('original_frei_read_20',function(){$r=TXE_Workshop::loadLegacyApprovals();return $r['total']===20&&$r['held']===20;});
ck('title_export_20',function()use(&$titleBatch){$titleBatch=TXE_Workshop::exportTitleBatch(20);return count($titleBatch['items'])===20 && ($titleBatch['title_only']??null)===true;});
ck('title_frozen_repeated_export',function()use(&$titleBatch){return TXE_Workshop::exportTitleBatch(20)===$titleBatch;});
ck('title_import_20',function()use(&$titleBatch){$returned=$titleBatch;foreach($returned['items'] as $i=>&$row){$row['titles'][0]['title']='Pferdepflege Titel '.($i+1);}unset($row);$r=TXE_Workshop::importTitleBatch($returned);return $r['titles']===20&&$r['pending']===0;});
ck('k0_export_13',function()use(&$first){$first=TXE_Workshop::export(13);return count($first['items'])===13&&($first['item_count']??null)===13;});
ck('k0_export_7',function()use(&$second){$second=TXE_Workshop::export(13);return count($second['items'])===7&&($second['item_count']??null)===7;});
ck('k0_contract_identical_original',function()use(&$first,&$second){return PSERC_Metadata_Boundary::validateBatch($first)['ok']===true&&PSERC_Metadata_Boundary::validateBatch($second)['ok']===true;});
ck('all_20_reserved_once',function(){$s=get_option(TXE_Workshop::OPTION);return count($s['orders'])===20&&count(array_filter($s['orders'],fn($x)=>$x['status']==='EXPORTIERT'))===20;});
ck('repeated_13_download_identical',function()use(&$first){return TXE_Workshop::redownloadBatch($first['batch_sha256'])===$first;});
function handoff(array $batch):array {$articles=[];foreach($batch['items'] as $item){$i=(int)filter_var($item['target_keyword'],FILTER_SANITIZE_NUMBER_INT);$articles[]=[
 'article_id'=>$GLOBALS['idByIndex'][$i],'plan_slot'=>$item['plan_slot'],'title'=>$item['title'],
 'slug'=>'qa-pferde-pflege-'.$i,'target_keyword'=>$item['target_keyword'],'category'=>$item['category'],
 'article_type'=>$item['article_type'],'body'=>'<p>Nur QA '.$i.'</p>'
 ];}return ['contract'=>TXE_Workshop::IMPORT_CONTRACT,'articles'=>$articles];}
ck('import_first_13',function()use(&$first){$r=TXE_Workshop::importDraftsIndividually(handoff($first));return $r['imported']===13&&$r['created']===13&&count($GLOBALS['posts'])===13;});
ck('import_remaining_7',function()use(&$second){$r=TXE_Workshop::importDraftsIndividually(handoff($second));return $r['imported']===7&&$r['created']===7&&count($GLOBALS['posts'])===20;});
ck('no_separate_planning_write',function(){return get_option('ppm679_editorial_plan_runtime_state_v1','NOT_SET')==='NOT_SET';});
ck('all_20_drafts_and_original_blocks',function(){return count($GLOBALS['posts'])===20&&count(array_filter($GLOBALS['posts'],fn($p)=>$p['post_status']==='draft'&&($p['meta_input']['_ppm679_publish_blocked']??'')==='1'))===20;});
ck('return_again_no_new_posts',function()use(&$first){(new ReflectionClass(PSERC_System4_Import::class))->getProperty('collisionIndex')->setValue(null,null);$r=TXE_Workshop::importDraftsIndividually(handoff($first));return $r['created']===0&&count($GLOBALS['posts'])===20;});
ck('works_without_ppm_runtime',function(){return !class_exists('PPM679_Editorial_Plan_Runtime_Gate',false) && $GLOBALS['ppm_calls']===0;});
ck('modified_content_duplicate_refused',function()use(&$first){
    (new ReflectionClass(PSERC_System4_Import::class))->getProperty('collisionIndex')->setValue(null,null);
    $v=handoff($first);$v['articles'][0]['body']='<p>Abweichender Inhalt</p>';
    $r=TXE_Workshop::importDraftsIndividually($v);return $r['imported']===12&&count($r['held'])===1&&count($GLOBALS['posts'])===20;
});
ck('wrong_article_id_refused',function()use(&$first){$v=handoff($first);$v['articles'][0]['article_id']='falsch-id';$r=TXE_Workshop::importDraftsIndividually($v);return $r['created']===0&&count($r['held'])===1&&count($GLOBALS['posts'])===20;});
ck('wrong_category_refused',function()use(&$first){$v=handoff($first);$v['articles'][0]['category']='falsche-kategorie';$r=TXE_Workshop::importDraftsIndividually($v);return $r['created']===0&&count($r['held'])===1&&count($GLOBALS['posts'])===20;});
ck('missing_plan_slot_refused',function()use(&$first){$v=handoff($first);$v['articles'][0]['plan_slot']='';$r=TXE_Workshop::importDraftsIndividually($v);return $r['created']===0&&count($r['held'])===1&&count($GLOBALS['posts'])===20;});
ck('publish_and_legacy_block_meta_preserved',function(){return count(array_filter($GLOBALS['posts'],fn($p)=>$p['post_status']==='draft' && ($p['meta_input']['_pserc_publish_blocked']??'')==='1' &&($p['meta_input']['_ppm679_publish_blocked']??'')==='1'))===20;});
ck('published_transition_blocked',function(){ $r=qa_data_filter(['post_status'=>'publish'],['ID'=>100]);return $r['post_status']==='draft'; });
ck('scheduled_publication_blocked',function(){ $r=qa_data_filter(['post_status'=>'future'],['ID'=>100]);return $r['post_status']==='draft'; });
ck('unrelated_post_not_blocked',function(){ $r=qa_data_filter(['post_status'=>'publish'],['ID'=>99999]);return $r['post_status']==='publish'; });
ck('already_public_post_preserved',function(){ $old=$GLOBALS['posts'][100]['post_status'];$GLOBALS['posts'][100]['post_status']='publish';$r=qa_data_filter(['post_status'=>'publish'],['ID'=>100]);$GLOBALS['posts'][100]['post_status']=$old;return $r['post_status']==='publish'; });
ck('old_frei_unchanged',function()use($proofs){return get_option('pste_mini_keyword_roundtrip_v1')['seo_decisions']===$proofs;});
$pass=count(array_filter($checks));echo json_encode(['pass'=>$pass,'total'=>count($checks),'checks'=>$checks,'errors'=>$errors],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE),"\n";exit($pass===count($checks)?0:1);
