<?php
declare(strict_types=1);
error_reporting(E_ERROR | E_WARNING);
ini_set('memory_limit','1500M');
define('ABSPATH','/tmp/');define('PSTE_DIR',rtrim((string)getenv('PSTE_TEST_PLUGIN_ROOT'),'/').'/');
function wp_strip_all_tags($v){return strip_tags($v);}function wp_json_encode($v,$f=0){return json_encode($v,$f);}
function get_option($name,$default=false){return $default;}function is_wp_error($value){return false;}
$GLOBALS['category_exists']=false;$GLOBALS['category_error']=false;
function get_term_by($field,$slug,$tax){if($GLOBALS['category_error'])return (object)['term_id'=>0,'slug'=>'','taxonomy'=>''];if(!$GLOBALS['category_exists'])return false;$ids=['pferdegesundheit-verstehen'=>1486,'pferdewissen-grundlagen'=>1500];if(!isset($ids[$slug]))return false;return (object)['term_id'=>$ids[$slug],'name'=>$slug,'slug'=>$slug,'taxonomy'=>$tax];}
foreach(glob(PSTE_DIR.'includes/*.php') as $f)require_once $f;
$d=json_decode(file_get_contents('/mnt/data/pferde-seo-audit/_SEO_EXPORT_ARBEITSKOPIE_20261016.txt'),true,512,JSON_THROW_ON_ERROR);$b=$d['site_baseline'];
$n=0;$fail=[];
function check($condition,$label){global $n,$fail;$n++;if(!$condition)$fail[]=$label;}
foreach(['Wie alt werden Pferde?','Können Pferde schwimmen?'] as $q){
 $GLOBALS['category_exists']=false;
 $out=PSTE_Normal_Metadata_Path::evaluateRaw($q,$b);
 check(($out['status']??'')==='STRUCTURE_GAP',$q.' must hold in distinct category room');
 check(($out['worker_flow']['storage']??'')==='CATEGORY_ROOM_TOPIC_POOL',$q.' room storage');
 check(($out['worker_flow']['halted_at']??'')==='category',$q.' category-only halt');
 check(!empty($out['title_pipeline']['ok'])&&!empty($out['title']),$q.' title actually hard-validated');
 check(($out['worker_flow']['steps']['relevance']['decision']??'')==='GREEN'&&($out['worker_flow']['steps']['title']['decision']??'')==='GREEN'&&($out['worker_flow']['steps']['lane']['decision']??'')==='GREEN',$q.' workers one to three remain green');
 check(empty($out['production_handoff_attempted'])&&empty($out['write_attempted'])&&empty($out['five_field_handoff_created']),$q.' no premature production');
 check(PSTE_Category_Gap::readyForCategoryRoom($out),$q.' existing category-room acceptance');
 $GLOBALS['category_exists']=true;
 $yes=PSTE_Normal_Metadata_Path::evaluateRaw($q,$b);
 check(($yes['status']??'')==='NORMAL_PASS'&&($yes['worker_flow']['storage']??'')==='NORMAL_PATH',$q.' proven term passes');
 check(empty($yes['category_backlog_required'])&&($yes['worker_flow']['halted_at']??'')==='', $q.' existing term not backlogged');
}
$GLOBALS['category_exists']=false;
$payload=['primary_longtail_query'=>'Wie alt werden Pferde?','editorial_title'=>'Ein völlig anderer gespeicherter Titel','title_candidate_evidence'=>['contract'=>'PSTE_STORED_SOURCE_TITLE_CANDIDATE_V1','production_authority'=>false,'family_category_type_authority'=>false]];
$preserved=PSTE_Normal_Metadata_Path::applyToPayload($payload,$b);
$r=$preserved['normal_metadata_path'];
check(($r['status']??'')==='SANDBOX_REQUIRED'&&empty($r['category_backlog_required']),'different immutable stored title fails closed');
check(($r['worker_flow']['halted_at']??'')==='title','different immutable stored title halts at title');
check(($r['title']??'')==='Ein völlig anderer gespeicherter Titel','different immutable stored title kept');
$GLOBALS['category_exists']=true;
$faq=PSTE_Normal_Metadata_Path::evaluateRaw('Welche Pferde OP-Versicherung ist besser, Barmenia oder Uelzener?',$b);
check(($faq['status']??'')==='NORMAL_PASS'&&($faq['article_type']??'')==='FAQ','existing specialist path retained');
$GLOBALS['category_exists']=false;
$unrelated=PSTE_Normal_Metadata_Path::evaluateRaw('Wie alt werden Hausmäuse?',$b);
check(($unrelated['status']??'')!=='NORMAL_PASS','irrelevant question not passed');
$allok=!$fail;
echo json_encode(['ok'=>$allok,'assertions'=>$n,'failed'=>$fail],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT)."\n";
exit($allok?0:1);