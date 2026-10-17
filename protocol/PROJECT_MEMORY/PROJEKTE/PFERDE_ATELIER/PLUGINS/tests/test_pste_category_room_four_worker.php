<?php
declare(strict_types=1);
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
function wp_strip_all_tags($s){return strip_tags($s);}
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
$root=rtrim((string)(getenv('PSTE_TEST_PLUGIN_ROOT')?:dirname(__DIR__).'/Portal SEO Topic Engine'),'/').'/';
foreach(glob($root.'includes/*.php') as $file)require_once $file;
function ensure($ok,$case){if(!$ok)throw new RuntimeException('FAILED: '.$case);echo "PASS $case\n";}
$raw='Wie lange dauert die Eingewöhnung im Offenstall?';
$good=['contract'=>'PSTE_NORMAL_METADATA_PATH_V2','status'=>'STRUCTURE_GAP','raw_query'=>$raw,'raw_query_sha256'=>hash('sha256',$raw),'portal_relevance'=>'PROVEN','structure_gap_backlog_required'=>true,'sandbox_required'=>false,'title'=>'Wie lange dauert die Eingewöhnung im Offenstall?','title_pipeline'=>['ok'=>true],'title_candidate_only'=>false,'article_type'=>'Journal','target_keyword'=>'Eingewöhnung im Offenstall','target_category'=>[],'reason_codes'=>['PSTE_RELEVANT_TOPIC_CATEGORY_GAP_RETAINED']];
ensure(PSTE_Category_Gap::readyForCategoryRoom($good),'green 3 workers missing category enters separate room');
$r=PSTE_Semantic_Review_Sandbox::admitFromNormalPath('topic:test',$good);ensure(($r['status']??'')==='CATEGORY_ROOM_TOPIC_POOL' && empty($r['admitted']),'category room bypasses sandbox admission without DB');
$bad=$good;$bad['portal_relevance']='UNPROVEN';ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'unproven relevance stays out of category room');
$bad=$good;$bad['title_pipeline']['ok']=false;ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'unverified title stays out');
$bad=$good;$bad['title_candidate_only']=true;ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'candidate title is not approved title');
$bad=$good;$bad['article_type']='';ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'unknown Fach/Magazin stays out');
$bad=$good;$bad['target_category']=['term_id'=>1485,'slug'=>'alltags-pferde-haltungsformen'];ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'existing category stays out');
$bad=$good;$bad['status']='SANDBOX_REQUIRED';ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'sandbox case remains sandbox');
$bad=$good;$bad['sandbox_required']=true;ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'sandbox flag cannot enter room');
$bad=$good;$bad['raw_query_sha256']=str_repeat('a',64);ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'tampered keyword blocked');
$bad=$good;$bad['structure_gap_backlog_required']=false;ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'unproved category gap blocked');
$bad=$good;$bad['title']='';ensure(!PSTE_Category_Gap::readyForCategoryRoom($bad),'empty title blocked');
echo "ALL CATEGORY ROOM NEGATIVE TESTS PASS\n";