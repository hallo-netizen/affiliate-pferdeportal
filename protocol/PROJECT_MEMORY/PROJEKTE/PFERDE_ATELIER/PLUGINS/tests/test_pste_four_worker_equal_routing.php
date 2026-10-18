<?php
error_reporting(E_ALL);ini_set('memory_limit','1900M');
define('ABSPATH','/tmp/');define('PSTE_DIR',rtrim((string)getenv('PSTE_TEST_PLUGIN_ROOT'),'/').'/');
function wp_strip_all_tags($x){return strip_tags($x);}function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}function get_option($a,$b=false){return $b;}function is_wp_error($x){return false;}
$GLOBALS['term_exists']=true;
function get_term_by($type,$slug,$taxonomy){if(!$GLOBALS['term_exists'])return false;$cats=['ausbildung-reitweisen'=>1488,'pferde-verstehen'=>1481,'alltags-pferde-haltungsformen'=>1485,'pferdeernaehrung-verstehen'=>1487,'pferdegesundheit-verstehen'=>1486,'recht-finanzen-organisation'=>1483,'pferdewissen-grundlagen'=>1500,'reiterleben-community'=>1484,'pferderassen-pferdetypen'=>1482];return isset($cats[$slug])?(object)['term_id'=>$cats[$slug],'name'=>$slug,'slug'=>$slug,'taxonomy'=>'category']:false;}
foreach(glob(PSTE_DIR.'includes/*.php') as $p)require_once $p;
$d=json_decode(file_get_contents('/mnt/data/pferde-seo-audit/_SEO_EXPORT_ARBEITSKOPIE_20261016.txt'),true,512,JSON_THROW_ON_ERROR);$b=$d['site_baseline'];
function result(string $q,bool $categoryAvailable=true):array{global $d,$b;$GLOBALS['term_exists']=$categoryAvailable;$c=null;foreach($d['candidates'] as $x)if(($x['primary_longtail_query']??'')===$q){$c=$x;break;}if(!$c)$c=['primary_longtail_query'=>$q];return PSTE_Normal_Metadata_Path::applyToPayload($c,$b,(string)($c['research_origin_family_key']??''))['normal_metadata_path'];}
function check(bool $b,string $why):void{if(!$b)throw new RuntimeException('FAIL '.$why);echo "PASS $why\n";}
// KISS regression: the historic research-family flag must no longer be part of
// the Magazine classifier's argument contract or its admission decisions.
check((new ReflectionMethod(PSTE_Journal_Semantic_Router::class,'classifyQuestion'))->getNumberOfParameters()===1,'old family admission switch removed');
foreach([
    'Sind Haferflocken für Pferde geeignet?'=>'feeding',
    'Wie lange soll man Pferde auf die Weide lassen?'=>'housing',
    'Warum fressen Pferde auf der Weide so viel Heu?'=>'feeding',
] as $question=>$expectedDomain){
    $classified=PSTE_Journal_Semantic_Router::classifyQuestion($question);
    check(!empty($classified['ok'])&&($classified['category_key']??'')===$expectedDomain,
        'magazine category depends on the question, not DataForSEO family: '.$expectedDomain);
}
$feed=result('Sind Haferflocken für Pferde geeignet?');check($feed['status']==='NORMAL_PASS'&&($feed['target_category']['slug']??'')==='pferdeernaehrung-verstehen'&&$feed['article_type']==='Journal','familyless horse feed -> verified real journal category');
check(($feed['worker_flow']['disposition']??'')==='GREEN','all four workers GREEN with real category');
$housing=result('Wie lange soll man Pferde auf die Weide lassen?');check($housing['status']==='NORMAL_PASS'&&($housing['target_category']['slug']??'')==='alltags-pferde-haltungsformen','familyless grazing -> housing');
$oldFach=result('Sind Leinöl und Hafer für Pferde geeignet?');check($oldFach['status']==='NORMAL_PASS'&&$oldFach['article_type']==='FAQ'&&($oldFach['target_category']['slug']??'')==='hafer-faq','existing Fach family owner unchanged');
$oldJournal=result('Warum fressen Pferde auf der Weide so viel Heu?');check($oldJournal['status']==='NORMAL_PASS'&&$oldJournal['article_type']==='Journal'&&($oldJournal['target_category']['slug']??'')==='pferdeernaehrung-verstehen','specific feeding beats vague Weide, existing Journal unchanged');
$oldFach2=result('Welche Pferde OP-Versicherung ist besser, Barmenia oder Uelzener?');check($oldFach2['status']==='NORMAL_PASS'&&$oldFach2['article_type']==='FAQ'&&($oldFach2['target_category']['slug']??'')==='pferde-op-versicherung-faq','existing insurance Fach unchanged');
$notHorse=result('Warum geht mein Braun Rasierer immer wieder aus?');check($notHorse['status']==='SANDBOX_REQUIRED'&&$notHorse['portal_relevance']==='UNPROVEN','unrelated keywords never promoted');
$medical=result('Was sind die Auslöser einer Kolik bei Pferden?');check($medical['status']==='SANDBOX_REQUIRED','existing medical editorial risk hold untouched');
$missing=result('Sind Haferflocken für Pferde geeignet?',false);check($missing['status']==='STRUCTURE_GAP'&&$missing['article_type']==='Journal'&&!empty($missing['title_pipeline']['ok'])&&!empty($missing['category_backlog_required'])&&$missing['worker_flow']['storage']==='CATEGORY_ROOM_TOPIC_POOL','real missing category stores validated title outside Sandbox');
check(empty($missing['target_category']['term_id'])&&empty($missing['five_field_handoff_created'])&&empty($missing['production_handoff_attempted']),'no premature category or production authority');
$ambiguous=result('Warum fressen Pferde auf der Weide so viel Heu?',false);check($ambiguous['status']==='STRUCTURE_GAP'&&$ambiguous['worker_flow']['storage']==='CATEGORY_ROOM_TOPIC_POOL','old Journal category missing without false reroute');
echo "ALL EQUAL ROUTING TESTS PASS\n";