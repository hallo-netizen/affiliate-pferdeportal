<?php
/** QA read-only root-cause test: an already-relevant typed question is blocked before category.
 * Usage: php test_pste_intent_question_type_early_stop.php <pste_package_dir> <pserc_package_dir>
 * It does NOT test actual WordPress data or modify any plugin.
 */
declare(strict_types=1);
error_reporting(E_ERROR|E_WARNING);
if($argc!==3)exit(2);
define('ABSPATH','/');
function wp_strip_all_tags($s){return strip_tags((string)$s);}
function wp_json_encode($v,$f=0){return json_encode($v,$f);}
function get_option($n,$d=false){return $d;}
function get_term_by($f,$s,$t){return false;}
$dir=rtrim($argv[1],'/').'/Portal SEO Topic Engine/';
define('PSTE_DIR',$dir);
$main=file_get_contents($dir.'portal-seo-topic-engine.php');
$a=strpos($main,'foreach ([');$b=strpos($main,'] as',$a);
if($a===false||$b===false)throw new RuntimeException('SOURCE_IMPORT_LIST_MISSING');
preg_match_all("/'(includes\/[^']+\.php)'/",substr($main,$a,$b-$a),$m);
foreach($m[1] as $f)require_once $dir.$f;
require_once rtrim($argv[2],'/').'/portal-seo-editorial-plan-compiler/includes/class-pserc-title-gate.php';
$baseline=['contract'=>'PSTE_SITE_BASELINE_V1','structure_sha256'=>str_repeat('a',64),
 'leaf_categories'=>[
  ['term_id'=>101,'name'=>'Heunetz Kosten','slug'=>'heunetz-kosten','article_type'=>'Kosten','topic_family_name'=>'Heunetz','topic_family_key'=>'heunetz','full_path'=>'Pferde/Heunetz/Kosten'],
  ['term_id'=>102,'name'=>'Heunetz FAQ','slug'=>'heunetz-faq','article_type'=>'FAQ','topic_family_name'=>'Heunetz','topic_family_key'=>'heunetz','full_path'=>'Pferde/Heunetz/FAQ'],
  ['term_id'=>103,'name'=>'Schabracke Pflege','slug'=>'schabracke-pflege','article_type'=>'Pflege','topic_family_name'=>'Schabracke','topic_family_key'=>'schabracke','full_path'=>'Pferde/Schabracke/Pflege'],
  ['term_id'=>104,'name'=>'Pferdedecke Pflege','slug'=>'pferdedecke-pflege','article_type'=>'Pflege','topic_family_name'=>'Pferdedecke','topic_family_key'=>'pferdedecke','full_path'=>'Pferde/Pferdedecke/Pflege'],
  ['term_id'=>105,'name'=>'Trense FAQ','slug'=>'trense-faq','article_type'=>'FAQ','topic_family_name'=>'Trense','topic_family_key'=>'trense','full_path'=>'Pferde/Trense/FAQ'],
 ],'portal_scope_terms'=>['Pferd','Pferde','Reiten']];
$failures=[];
foreach(['Was kostet ein Heunetz für Pferde?'=>'Kosten','Wie reinige ich eine Schabracke?'=>'Pflege','Wie pflege ich eine Pferdedecke?'=>'Pflege'] as $q=>$type){
 $p=PSTE_Normal_Metadata_Path::applyToPayload(['canonical_query'=>$q],$baseline)['normal_metadata_path'];
 $technical=(array)($p['title_pipeline']['deterministic']['reason_codes']??[]);
 $german=(array)($p['title_pipeline']['language']['reason_codes']??[]);
 $gate=PSERC_Title_Gate::verify($q,$type,['question_mark'=>'OPTIONAL']);
 if(($p['portal_relevance']??'')!=='PROVEN'||($p['editorial_area']??'')!=='FACH'
   ||($p['article_type']??'')!==$type||($p['status']??'')!=='SANDBOX_REQUIRED'
   ||($p['worker_flow']['next_step']??'')!=='title'
   ||!in_array('QUESTION_MARK_EXCLUSIVE_TO_FAQ',$technical,true)
   ||!in_array('NONFAQ_TITLE_IS_QUESTION',$german,true)
   ||!in_array('PORTAL_QUESTION_MARK_EXCLUSIVE_TO_FAQ',(array)($gate['errors']??[]),true))
  throw new RuntimeException('KNOWN_CROSS_OWNER_EARLY_STOP_NOT_REPRODUCED');
 $failures[]=['type'=>$type,'relevance'=>'PROVEN','earliest_halt'=>'title','reason'=>'NONFAQ_QUESTION_TITLES_FORBIDDEN_IN_THREE_GATES'];
}
foreach(['Was ist eine Trense?'=>'FAQ','Heunetz Kosten'=>'Kosten'] as $q=>$type){
 $p=PSTE_Normal_Metadata_Path::applyToPayload(['canonical_query'=>$q],$baseline)['normal_metadata_path'];
 if(($p['status']??'')!=='NORMAL_PASS'||($p['article_type']??'')!==$type)
  throw new RuntimeException('POSITIVE_CONTROL_NOT_PASS');
}
$gap=PSTE_Normal_Metadata_Path::applyToPayload(['canonical_query'=>'Trense reinigen'],$baseline)['normal_metadata_path'];
if(($gap['status']??'')!=='STRUCTURE_GAP'||($gap['worker_flow']['next_step']??'')!=='category')
 throw new RuntimeException('CATEGORY_GAP_NOT_SEPARATE');
$q='Wie pflege ich eine Pferdedecke?';
$p=PSTE_Normal_Metadata_Path::applyToPayload(['canonical_query'=>$q],$baseline)['normal_metadata_path'];
$n=PSTE_Editorial_Topic_Normalizer::normalize($q,'');
$generated=PSTE_Title_Pipeline::build(['raw_query'=>$q,'language_corrected_query'=>$q],
 (string)($n['subject_topic']??''),'Pflege',PSTE_Article_Type_Registry::build($baseline),
 [],(array)($p['intent_profile']??[]));
if(empty($generated['ok'])||($generated['title']??'')!=='Wie ich eine Pferdedecke pflegen')
 throw new RuntimeException('EXISTING_COMPOSER_FALSE_GREEN_NOT_REPRODUCED');
echo json_encode(['status'=>'KNOWN_SYSTEMIC_BLOCKER_REPRODUCED',
 'nonfaq_question_early_stops'=>count($failures),'unchanged_positive_controls'=>2,
 'unrelated_category_gap_kept_separate'=>true,
 'existing_composer_false_green'=>(string)$generated['title'],
 'factual_live_wp_5016_readback'=>false,'plugin_change'=>false,
 'downstream_wordpress_download_not_executed'=>true],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT),"\n";
