<?php
/** PSTE 0.57.104+ conservative four-worker reorder on actual original class code. */
error_reporting(E_ERROR|E_WARNING);ini_set('memory_limit','1900M');
define('ABSPATH','/tmp/');define('PSTE_DIR',rtrim((string)getenv('PSTE_TEST_PLUGIN_ROOT'),'/').'/');
function wp_strip_all_tags($v){return strip_tags($v);}function wp_json_encode($v,$f=0){return json_encode($v,$f);}function get_option($name,$default=false){return $default;}function is_wp_error($v){return false;}
$GLOBALS['journal_terms_available']=true;
function get_term_by($field,$slug,$taxonomy){
 if(!$GLOBALS['journal_terms_available'])return false;
 $terms=['ausbildung-reitweisen'=>1488,'pferde-verstehen'=>1481,'alltags-pferde-haltungsformen'=>1485,'pferdeernaehrung-verstehen'=>1487,'pferdegesundheit-verstehen'=>1486,'recht-finanzen-organisation'=>1483,'pferdewissen-grundlagen'=>1500,'reiterleben-community'=>1484,'pferderassen-pferdetypen'=>1482];
 return isset($terms[$slug])?(object)['term_id'=>$terms[$slug],'slug'=>$slug,'name'=>$slug,'taxonomy'=>$taxonomy]:false;
}
foreach(glob(PSTE_DIR.'includes/*.php') as $p)require_once $p;
$data=json_decode(file_get_contents(getenv('PSTE_REPLAY_SNAPSHOT')?:'/mnt/data/pferde-seo-audit/_SEO_EXPORT_ARBEITSKOPIE_20261016.txt'),true,512,JSON_THROW_ON_ERROR);
$baseline=$data['site_baseline'];$index=[];foreach($data['candidates'] as $item)$index[(string)($item['primary_longtail_query']??'')]=$item;
function runCase(string $raw,bool $term=true):array{global $index,$baseline;$GLOBALS['journal_terms_available']=$term;$row=$index[$raw]??['primary_longtail_query'=>$raw];return PSTE_Normal_Metadata_Path::applyToPayload($row,$baseline,(string)($row['research_origin_family_key']??''));}
function ensure(bool $ok,string $test):void{if(!$ok)throw new RuntimeException('FAILED: '.$test);echo "PASS: $test\n";}
$unassigned='Was sind Dickmacher für Pferde?';$path=runCase($unassigned)['normal_metadata_path'];$wf=(array)$path['worker_flow'];
ensure($path['portal_relevance']==='PROVEN','worker1 portal relevance PROVEN');
ensure($path['status']==='SANDBOX_REQUIRED'&&!empty($path['title_precheck_validated']),'old family miss no longer interrupts title check');
ensure($path['title']===$unassigned&&!empty($path['title_pipeline']['ok']),'original readable title passed existing title gates');
ensure(($wf['steps']['title']['decision']??'')==='GREEN'&&($wf['steps']['lane']['decision']??'')==='YELLOW'&&($wf['steps']['category']['decision']??'')==='NOT_STARTED','workers executed in prescribed order');
ensure($wf['halted_at']==='lane'&&$wf['resume_from']==='lane'&&$wf['storage']==='EXISTING_SANDBOX','precise lane hold in existing Sandbox');
ensure(empty($path['category_backlog_required'])&&empty($path['article_type'])&&empty($path['target_category']),'unknown lane never becomes fictitious missing category');
ensure(empty($path['production_handoff_attempted'])&&empty($path['five_field_handoff_created']),'no premature production handoff');
$stored=runCase($unassigned);ensure(($stored['production_title']??'')===''&&($stored['editorial_title']??'')===$unassigned,'independent title visible, never an approved production title');
$wrong=runCase('pferd minecraft');ensure(empty($wrong['normal_metadata_path']['title_precheck_validated'])&&($wrong['normal_metadata_path']['status']??'')!=='NORMAL_PASS','nonquestion horse mention cannot be promoted');
$nonHorse=runCase('Warum geht mein Braun Rasierer immer wieder aus?');ensure(($nonHorse['normal_metadata_path']['portal_relevance']??'')==='UNPROVEN'&&!empty($nonHorse['normal_metadata_path']['sandbox_required']),'unrelated topic retained for relevance review');
$valid=runCase('Sind Haferflocken für Pferde geeignet?');ensure(($valid['normal_metadata_path']['status']??'')==='NORMAL_PASS'&&($valid['normal_metadata_path']['target_category']['slug']??'')==='pferdeernaehrung-verstehen','already verified Journal topic unchanged');
$fach=runCase('Welche Pferde OP-Versicherung ist besser, Barmenia oder Uelzener?');ensure(($fach['normal_metadata_path']['status']??'')==='NORMAL_PASS'&&($fach['normal_metadata_path']['article_type']??'')==='FAQ','existing Fach path unchanged');
$missing=runCase('Sind Haferflocken für Pferde geeignet?',false);ensure(($missing['normal_metadata_path']['worker_flow']['storage']??'')==='CATEGORY_ROOM_TOPIC_POOL'&&empty($missing['normal_metadata_path']['sandbox_required']),'confirmed lane and finished title without category uses distinct category room');
ensure(empty($missing['production_handoff_attempted'])&&empty($missing['textmachine_handoff_status']==='READY_FOR_COMPILER_CAPABILITY_CHECK'),'missing category cannot create production handoff');
echo "EXISTING FOUR-WORKER ORDER TEST PASSED\n";