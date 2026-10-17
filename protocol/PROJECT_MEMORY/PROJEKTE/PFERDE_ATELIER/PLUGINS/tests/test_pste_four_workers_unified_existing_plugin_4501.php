<?php
// Read-only integration regression: actual PSTE PHP classes and stored WP export.
// Does not stand in for a live MariaDB/WordPress/PPM production acceptance test.
error_reporting(E_ERROR | E_WARNING);
ini_set('memory_limit','1600M');
define('ABSPATH','/tmp/');
define('PSTE_DIR',rtrim((string)getenv('PSTE_TEST_PLUGIN_ROOT'),'/').'/');
function wp_strip_all_tags($s){return strip_tags($s);}
function wp_json_encode($v,$f=0){return json_encode($v,$f);}
function get_option($n,$d=false){return $d;}
function is_wp_error($v){return false;}
function get_term_by($field,$slug,$taxonomy){
    $j=['ausbildung-reitweisen'=>1488,'pferde-verstehen'=>1481,'alltags-pferde-haltungsformen'=>1485,
        'pferdeernaehrung-verstehen'=>1487,'pferdegesundheit-verstehen'=>1486,
        'recht-finanzen-organisation'=>1483,'pferdewissen-grundlagen'=>1500,
        'reiterleben-community'=>1484,'pferderassen-pferdetypen'=>1482];
    return isset($j[$slug])?(object)['term_id'=>$j[$slug],'slug'=>$slug,'name'=>$slug,'taxonomy'=>$taxonomy]:false;
}
foreach(glob(PSTE_DIR.'includes/*.php') as $p)require_once $p;
$d=json_decode(file_get_contents((string)getenv('PSTE_TEST_EXPORT')),true,512,JSON_THROW_ON_ERROR);
$b=$d['site_baseline'];
$counts=['bad_details'=>[],'processed'=>0,'question_title_pass'=>0,'phrase_title_pass'=>0,'category_only'=>0,'lane_yellow'=>0,'relevance_yellow'=>0,'category_yellow'=>0,'pass'=>0,'changes'=>0,'bad_statuses'=>0];
foreach((array)$d['candidates'] as $row){
    $raw=PSTE_Editorializer::sourceQuery($row);
    $out=PSTE_Normal_Metadata_Path::applyToPayload($row,$b,(string)($row['research_origin_family_key']??''));
    if($raw!==PSTE_Editorializer::sourceQuery($out))$counts['changes']++;
    $path=(array)($out['normal_metadata_path']??[]);$steps=(array)($path['worker_flow']['steps']??[]);
    if(count($steps)!==4){$counts['bad_statuses']++;$counts['bad_details'][]=['bad_steps',$raw,count($steps)];}
    if(!empty($path['title_precheck_validated'])){
        if(PSTE_Normalizer::isQuestion($raw))$counts['question_title_pass']++;
        else $counts['phrase_title_pass']++;
        if(empty($path['title_pipeline']['ok'])){$counts['bad_statuses']++;$counts['bad_details'][]=['bad_title_pipeline',$raw,$path['status']??null,$path['title_candidate_source']??null];}
    }
    $stop=(string)($path['worker_flow']['halted_at']??'');
    if($stop==='lane')$counts['lane_yellow']++;
    if($stop==='relevance')$counts['relevance_yellow']++;
    if($stop==='category')$counts['category_yellow']++;
    if(($path['worker_flow']['storage']??'')==='CATEGORY_ROOM_TOPIC_POOL')$counts['category_only']++;
    if(($path['status']??'')==='NORMAL_PASS')$counts['pass']++;
    foreach(['production_handoff_attempted','write_attempted','article_or_taxonomy_write_attempted'] as $key)
        if(!empty($path[$key])){$counts['bad_statuses']++;$counts['bad_details'][]=['bad_write',$raw,$key];}
    $counts['processed']++;
}
$ok=$counts['processed']===4501 && $counts['phrase_title_pass']>100
    && $counts['question_title_pass']>20 && !$counts['changes'] && !$counts['bad_statuses'];
echo json_encode(['ok'=>$ok,'counts'=>$counts],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT)."\n";
exit($ok?0:1);