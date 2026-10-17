<?php
declare(strict_types=1);error_reporting(E_ERROR);ini_set('memory_limit','2048M');
define('ABSPATH','/tmp/');define('PSTE_DIR','/mnt/data/seo_work/modified/Portal SEO Topic Engine/');
function wp_strip_all_tags($s){return strip_tags($s);}function wp_json_encode($v,$f=0){return json_encode($v,$f);}function get_option($n,$d=false){return $d;}function is_wp_error($v){return false;}
function get_term_by($field,$slug,$taxonomy){
$terms=['ausbildung-reitweisen'=>1488,'pferde-verstehen'=>1481,'alltags-pferde-haltungsformen'=>1485,'pferdeernaehrung-verstehen'=>1487,'pferdegesundheit-verstehen'=>1486,'recht-finanzen-organisation'=>1483,'pferdewissen-grundlagen'=>1500,'reiterleben-community'=>1484,'pferderassen-pferdetypen'=>1482];
if(!isset($terms[$slug]))return false;return (object)['term_id'=>$terms[$slug],'slug'=>$slug,'taxonomy'=>$taxonomy,'name'=>$slug];}
foreach(glob(PSTE_DIR.'includes/*.php') as $p) require_once $p;
$d=json_decode(file_get_contents('/mnt/data/pferde-seo-audit/_SEO_EXPORT_ARBEITSKOPIE_20261016.txt'),true,512,JSON_THROW_ON_ERROR);$baseline=$d['site_baseline'];$offset=(int)($argv[1]??0);$limit=(int)($argv[2]??400);
$out=['offset'=>$offset,'processed'=>0,'pass'=>0,'journal_pass'=>0,'discovery_promoted'=>0,'old_pass_now_not_pass'=>0,'statuses'=>[],'worker_stops'=>[],'errors'=>[],'invariant_failures'=>[],'research_changes'=>0];
foreach(array_slice($d['candidates'],$offset,$limit) as $original){$out['processed']++;$raw=PSTE_Normal_Metadata_Path::canonicalInputQuery(PSTE_Editorializer::sourceQuery($original));
$baselineFields=[];foreach(['primary_longtail_query','canonical_query','raw_user_question','query_record','query_aliases','candidate_id','research_origin_family_key'] as $k)$baselineFields[$k]=$original[$k]??null;
try {$row=PSTE_Normal_Metadata_Path::applyToPayload($original,$baseline,(string)($original['research_origin_family_key']??''));$path=(array)($row['normal_metadata_path']??[]);
foreach($baselineFields as $k=>$value)if(($row[$k]??null)!==$value)$out['invariant_failures'][]=[$offset+$out['processed']-1,$k];
$status=(string)($path['status']??'UNKNOWN');$out['statuses'][$status]=($out['statuses'][$status]??0)+1;$wf=(array)($path['worker_flow']??[]);if(($wf['contract']??'')!=='PSTE_NORMAL_FOUR_STEPS_V1')throw new RuntimeException('MISSING_WORKER_FLOW');
$halt=(string)($wf['halted_at']??'');$out['worker_stops'][$halt!==''?$halt:'GREEN']=($out['worker_stops'][$halt!==''?$halt:'GREEN']??0)+1;
if($status==='NORMAL_PASS'){$out['pass']++;if((string)($path['article_type']??'')==='Journal')$out['journal_pass']++;}
if((string)($original['normal_metadata_path']['status']??'')==='NORMAL_PASS'&&$status!=='NORMAL_PASS')$out['old_pass_now_not_pass']++;
if(!empty($row['discovery_only'])&&PSTE_Topic_Policy::classifyRole($row)==='ARTICLE_TOPIC')$out['discovery_promoted']++;
foreach(['write_attempted','article_or_taxonomy_write_attempted','production_handoff_attempted'] as $key)if(!empty($path[$key]))$out['invariant_failures'][]=[$offset+$out['processed']-1,$key];
} catch(Throwable $e){$out['errors'][]=[$offset+$out['processed']-1,$raw,$e->getMessage()];}
}
echo json_encode($out,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT)."\n";
exit(($out['errors']||$out['invariant_failures'])?1:0);