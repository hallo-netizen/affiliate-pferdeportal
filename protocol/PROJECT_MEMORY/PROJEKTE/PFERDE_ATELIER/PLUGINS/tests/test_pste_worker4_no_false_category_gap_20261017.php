<?php
/** Existing-plugin, read-only four-worker regression. No DB or publication authority. */
declare(strict_types=1);
error_reporting(E_ERROR|E_WARNING);ini_set('memory_limit','1300M');
define('ABSPATH','/tmp/');define('PSTE_DIR',rtrim((string)getenv('PSTE_TEST_PLUGIN_ROOT'),'/').'/');
function wp_strip_all_tags($x){return strip_tags($x);}function wp_json_encode($x,$f=0){return json_encode($x,$f);}function get_option($n,$d=false){return $d;}function is_wp_error($v){return false;}
function get_term_by($field,$slug,$tax){if(empty($GLOBALS['journal_terms_available']))return false;$ids=['ausbildung-reitweisen'=>1488,'pferde-verstehen'=>1481,'alltags-pferde-haltungsformen'=>1485,'pferdeernaehrung-verstehen'=>1487,'pferdegesundheit-verstehen'=>1486,'recht-finanzen-organisation'=>1483,'pferdewissen-grundlagen'=>1500,'reiterleben-community'=>1484,'pferderassen-pferdetypen'=>1482];return isset($ids[$slug])?(object)['term_id'=>$ids[$slug],'slug'=>$slug,'name'=>$slug,'taxonomy'=>$tax]:false;}
foreach(glob(PSTE_DIR.'includes/*.php') as $f)require_once $f;
$d=json_decode(file_get_contents((string)getenv('PSTE_TEST_EXPORT')),true,512,JSON_THROW_ON_ERROR);$b=$d['site_baseline'];$n=0;$errors=[];
function check($yes,$why){global $n,$errors;$n++;if(!$yes)$errors[]=$why;}
$GLOBALS['journal_terms_available']=true;
$existing=PSTE_Normal_Metadata_Path::evaluateRaw('Wie alt werden Pferde?',$b);
check(($existing['status']??'')==='NORMAL_PASS'&&($existing['article_type']??'')==='Journal','known existing magazine category remains normal PASS');
check(($existing['worker_flow']['storage']??'')==='NORMAL_PATH','existing category not wrongly treated as new-category demand');
$GLOBALS['journal_terms_available']=false;
foreach(['Wie alt werden Pferde?'] as $raw){
    $x=PSTE_Normal_Metadata_Path::evaluateRaw($raw,$b);
    check($x['status']==='STRUCTURE_GAP',$raw.' -> structural gap');
    check(($x['worker_flow']['storage']??'')==='CATEGORY_ROOM_TOPIC_POOL',$raw.' -> separate category room');
    check(($x['worker_flow']['halted_at']??'')==='category',$raw.' -> worker 4');
    check(PSTE_Category_Gap::readyForCategoryRoom($x),$raw.' -> existing room integrity');
    check(is_array($x['category_gap_proposal']??null) && !empty($x['category_gap_proposal']), $raw.' -> existing category gap proposal');
    check(empty($x['target_category']) && empty($x['production_handoff_attempted']) && empty($x['write_attempted']),$raw.' -> no fabricated WP term / writes');
}
foreach(['minecraft pferd sattel','mein pferde-abenteuer','pferde einfach malen'] as $raw){
    $x=PSTE_Normal_Metadata_Path::evaluateRaw($raw,$b);
    check(($x['status']??'')==='SANDBOX_REQUIRED',$raw.' -> no false completed title');
    check(($x['worker_flow']['halted_at']??'')==='title',$raw.' -> paused at actual title worker');
    check(($x['worker_flow']['storage']??'')==='EXISTING_SANDBOX',$raw.' -> no false category room');
}
$GLOBALS['journal_terms_available']=true;
$unresolved=PSTE_Normal_Metadata_Path::evaluateRaw('Was ist die teuerste OP beim Pferd?',$b);
check(($unresolved['status']??'')==='SANDBOX_REQUIRED','known magazine taxonomy and Fach no-match must not invent missing category');
check(($unresolved['worker_flow']['storage']??'')==='EXISTING_SANDBOX','unclear taxonomy stays in existing Sandbox');
check(empty($unresolved['category_backlog_required'])&&empty($unresolved['structure_gap_backlog_required']),'no manufactured category creation task');
check(($unresolved['family_structure_routing']['contract']??'')===PSTE_Family_Structure_Router::CONTRACT,'existing structure evidence reused without category authority');
$GLOBALS['journal_terms_available']=false;
$absent=PSTE_Normal_Metadata_Path::evaluateRaw('Was ist die teuerste OP beim Pferd?',$b);
check(($absent['status']??'')==='SANDBOX_REQUIRED','no false missing category from unmatched Fach family even when journal taxonomies missing');
check(($absent['worker_flow']['storage']??'')==='EXISTING_SANDBOX','uncertain classification must remain gray');
$GLOBALS['journal_terms_available']=true;
$special=PSTE_Normal_Metadata_Path::evaluateRaw('Welche Pferde OP-Versicherung ist besser, Barmenia oder Uelzener?',$b);
check(($special['status']??'')==='NORMAL_PASS'&&($special['article_type']??'')==='FAQ',$special['status']??' -> existing insurance Fach ownership');
check(($special['worker_flow']['storage']??'')==='NORMAL_PATH','valid Fach route never forced into new category');
$journal=PSTE_Normal_Metadata_Path::evaluateRaw('Sind Haferflocken für Pferde geeignet?',$b);
check(($journal['status']??'')==='NORMAL_PASS'&&($journal['article_type']??'')==='Journal','existing magazine route intact');
$wrong=PSTE_Normal_Metadata_Path::evaluateRaw('Wie alt werden Hausmäuse?',$b);
check(($wrong['status']??'')!=='NORMAL_PASS'&&($wrong['status']??'')!=='STRUCTURE_GAP','non-portal question cannot enter category room');
$stored=['primary_longtail_query'=>'Wie alt werden Pferde?','editorial_title'=>'Ein anderes gespeichertes Thema','title_candidate_evidence'=>['contract'=>'PSTE_STORED_SOURCE_TITLE_CANDIDATE_V1','production_authority'=>false,'family_category_type_authority'=>false]];
$reentry=PSTE_Normal_Metadata_Path::applyToPayload($stored,$b);
check(($reentry['normal_metadata_path']['status']??'')!=='NORMAL_PASS'&&($reentry['normal_metadata_path']['status']??'')!=='STRUCTURE_GAP','immutable divergent title cannot be silently replaced');
check(($reentry['editorial_title']??'')==='Ein anderes gespeichertes Thema','source title retained');
print json_encode(['pass'=>!$errors,'checks'=>$n,'errors'=>$errors],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT)."\n";
exit($errors?1:0);