<?php
declare(strict_types=1);
/** Synthetic category-gap observation fixture ONLY, not proof about real WP rows. */
define('ABSPATH','/qa/');define('ARRAY_A','ARRAY_A');
$GLOBALS['db_reads']=0;$GLOBALS['writes']=0;$GLOBALS['classification_calls']=0;
class FakeDB{
 public string $last_error='';
 function prepare($sql,...$values){foreach($values as $v){$i=strpos($sql,'%s');if($i===false)throw new Exception('PLACEHOLDER_MISSING');$sql=substr_replace($sql,"'".$v."'",$i,2);}return $sql;}
 function get_results($sql,$format=ARRAY_A){++$GLOBALS['db_reads']; return $GLOBALS['source_rows'];}
}
$GLOBALS['wpdb']=new FakeDB();
class PSTE_Repository{static function table($x){return 'real_existing_pste_topic_pool';}static function saveManualDecision(...$v){++$GLOBALS['writes'];throw new Exception('UNAUTHORIZED_WRITE');}}
class PSTE_Normal_Metadata_Path{static function payloadMatchesNormalPath(...$v){++$GLOBALS['classification_calls'];return false;}}
function get_option($k,$default=false){return $default;}
function get_term(...$v){++$GLOBALS['classification_calls'];return false;}
require __DIR__.'/texterstellung/includes/class-txe-legacy-source-bridge.php';
$proofs=[];$rows=[];
foreach(range(1,3) as $i){
 $key=sprintf('a76c%04d-02ac-4c72-96cb-3a97f36de%03d',$i,$i);$raw="Pferdekategorie Fall $i";
 $proofs[$key]=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','box'=>'FREI','raw_query'=>$raw,'source_sha256'=>hash('sha256',$key.'|'.$raw)];
 $gap=$i<3?['contract'=>'PSTE_CATEGORY_GAP_ANALYSIS_V2','status'=>'CATEGORY_GAP_PROPOSED','proposal_id'=>'gap:same-proposal','proposed_name'=>'Pflege / Bau'] : [];
 $path=['contract'=>'PSTE_NORMAL_METADATA_PATH_V2','status'=>'STRUCTURE_GAP','category_backlog_required'=>true,'worker_flow'=>['storage'=>'CATEGORY_ROOM_TOPIC_POOL'],'category_gap_proposal'=>$gap];
 $rows[]=['pool_key'=>$key,'payload_json'=>json_encode(['raw_query'=>$raw,'normal_metadata_path'=>$path]),'manual_status'=>''];
}
$GLOBALS['source_rows']=$rows;
$r=TXE_Legacy_Source_Bridge::recover($proofs);
$w=$r['category_gap_watch'];
$checks=[
 'all_original_gap_topics_counted'=>$w['open_room_topics']===3,
 'stored_proposals_grouped_without_redeciding'=>$w['distinct_stored_gap_proposals']===1 && $w['proposals'][0]['count']===2,
 'non_provable_gap_held'=>$w['unresolved_stored_gap_proposal']===1,
 'one_batched_original_pool_read'=>$GLOBALS['db_reads']===1,
 'no_category_or_article_type_reclassification'=>$GLOBALS['classification_calls']===0,
 'no_original_pool_or_category_write'=>$GLOBALS['writes']===0,
 'all_three_still_held'=>($r['counts']['ORIGINAL_EDITORIAL_METADATA_NOT_FINAL']??0)===3,
];
$p=count(array_filter($checks));echo json_encode(['pass'=>$p,'total'=>count($checks),'checks'=>$checks,'limits'=>'synthetic gap rows; no WordPress execution or original 61 source payloads'],JSON_PRETTY_PRINT),"\n";exit($p===count($checks)?0:1);
