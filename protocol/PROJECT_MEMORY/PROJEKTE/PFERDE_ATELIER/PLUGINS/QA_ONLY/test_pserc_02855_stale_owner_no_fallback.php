<?php
/** Direct one-time QA of the ACTUAL PSERC 0.28.55 reader. No extra runtime reviewer.
 * php this.php /path/to/extracted/portal-seo-editorial-plan-compiler
 */
declare(strict_types=1);
define('ABSPATH','/qa/');
$root=rtrim((string)($argv[1]??''),'/').'/';
if(!is_file($root.'includes/class-pserc-seo-reader.php'))
    throw new RuntimeException('EXACT_PSERC_QA_SOURCE_MISSING');
require $root.'includes/class-pserc-metadata-boundary.php';
final class PSTE_Repository {public static function workflowRouteForCandidate($x):string{return 'K0';}}
final class PSTE_Normal_Metadata_Path {public static function persistedStoredTitleCandidate($x):string{return (string)($x['production_title']??'');}}
final class PSERC_Article_Type_Extension_Registry {public static function extension($x):array{return [];}}
final class PSTE_Mini_Workflow {public static array $receipt=[];public static function singleOwnerSeoFor($k,$raw):array{return self::$receipt;}}
require $root.'includes/class-pserc-seo-reader.php';
function pass(bool $ok,string $msg):void {if(!$ok)throw new RuntimeException('FAIL '.$msg);echo "PASS $msg\n";}
$key='topic-001';$raw='horseware regendecken';$title='Horseware-Regendecken im Überblick';
$receipt=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','box'=>'FREI','pool_key'=>$key,
    'raw_query'=>$raw,'source_sha256'=>hash('sha256',$key.'|'.$raw),
    'intent_slot'=>str_repeat('a',64),'approved_title'=>$title];
$base=['pool_key'=>$key,'raw_user_question'=>$raw,'production_title'=>$title,'decision'=>'PASS',
    'planning_suitability'=>'YES','automatic_pool_status'=>'PASS','topic_role'=>'ARTICLE_TOPIC',
    'context_state'=>'CURRENT','proposed_article_type'=>'Beratung','target_category_id'=>12,
    'target_category_name'=>'Pferdedecken','target_category_slug'=>'regendecken',
    'metadata_handoff_fields'=>['title','target_keyword','category','article_type','plan_slot'],
    'textmachine_handoff_status'=>'READY_FOR_COMPILER_CAPABILITY_CHECK',
    'planning_readiness_gate'=>['external_editorial_receipt'=>$receipt,
       'external_seo_owner_verdict'=>'FREI','reason_codes'=>['PSTE_SINGLE_EXTERNAL_SEO_DECISION']]];
PSTE_Mini_Workflow::$receipt=$receipt;
$valid=PSERC_SEO_Reader::normalizeCandidate($base);
pass($valid['eligibility_status']==='ELIGIBLE'&&!empty($valid['single_external_seo_owner_receipt']),
    'real PSERC reads valid ONE external owner result');
PSTE_Mini_Workflow::$receipt=[];
$stale=PSERC_SEO_Reader::normalizeCandidate($base);
pass($stale['eligibility_status']==='HELD'&&empty($stale['single_external_seo_owner_receipt'])
    &&in_array('SEO_EXTERNAL_SINGLE_OWNER_PROOF_MISSING_OR_STALE',$stale['eligibility_reasons'],true),
    'stale source proof HELD, NEVER old semantic review fallback');
PSTE_Mini_Workflow::$receipt=$receipt;
$wrong=$base;$wrong['production_title']='Changed title';
$changed=PSERC_SEO_Reader::normalizeCandidate($wrong);
pass($changed['eligibility_status']==='HELD'&&empty($changed['single_external_seo_owner_receipt']),
    'changed title HELD rather than unchecked plan release');
PSTE_Mini_Workflow::$receipt=[];
$missing=$base;$missing['planning_readiness_gate']['external_editorial_receipt']=[];
pass(PSERC_SEO_Reader::normalizeCandidate($missing)['eligibility_status']==='HELD',
    'missing source proof HELD');
$marker=$base;unset($marker['planning_readiness_gate']['external_editorial_receipt']);
pass(PSERC_SEO_Reader::normalizeCandidate($marker)['eligibility_status']==='HELD',
    'external verdict marker without genuine receipt HELD');
$legacy=$base;unset($legacy['planning_readiness_gate']);
$old=PSERC_SEO_Reader::normalizeCandidate($legacy);
pass($old['eligibility_status']==='ELIGIBLE'&&empty($old['single_external_seo_owner_receipt']),
    'genuinely unrelated legacy topic keeps original behavior');
echo "PSERC_REAL_OWNER_STALE_PROOF_NO_FALLBACK_QA_PASS; NOT_WORDPRESS_STAGING\n";
