<?php
/** Real PSTE class regression for the four existing sequential decisions; no WordPress writes. */
declare(strict_types=1);error_reporting(E_ERROR);ini_set('memory_limit','2G');
define('ABSPATH','/tmp/');define('PSTE_DIR',rtrim((string)getenv('PSTE_TEST_PLUGIN_ROOT'),'/').'/');
function wp_strip_all_tags($s){return strip_tags($s);}function wp_json_encode($v,$f=0){return json_encode($v,$f);}function get_option($k,$v=false){return $v;}function is_wp_error($e){return false;}
function get_term_by($field,$slug,$taxonomy){$known=['ausbildung-reitweisen'=>1488,'pferde-verstehen'=>1481,'alltags-pferde-haltungsformen'=>1485,'pferdeernaehrung-verstehen'=>1487,'pferdegesundheit-verstehen'=>1486,'recht-finanzen-organisation'=>1483,'pferdewissen-grundlagen'=>1500,'reiterleben-community'=>1484,'pferderassen-pferdetypen'=>1482];return isset($known[$slug])?(object)['term_id'=>$known[$slug],'slug'=>$slug,'taxonomy'=>$taxonomy,'name'=>$slug]:false;}
foreach(glob(PSTE_DIR.'includes/*.php') as $f)require_once $f;
$archive=getenv('PSTE_REPLAY_SNAPSHOT')?:'/mnt/data/pferde-seo-audit/_SEO_EXPORT_ARBEITSKOPIE_20261016.txt';$d=json_decode(file_get_contents($archive),true,512,JSON_THROW_ON_ERROR);
$b=$d['site_baseline'];$r=PSTE_Article_Type_Registry::build($b);$index=[];foreach($d['candidates'] as $a)$index[(string)($a['primary_longtail_query']??'')]=$a;
function check(bool $ok,string $why):void{if(!$ok)throw new RuntimeException($why);echo "PASS: ".$why."\n";}
$question='Was sind Dickmacher für Pferde?';$e=$index[$question];
$rel=PSTE_Portal_Relevance_Gate::evaluateBeforeAssignment($question,$b,$r,(string)($e['research_origin_family_key']??''));
check(!empty($rel['ok'])&&empty($rel['family_hint']['family_key']), 'Worker 1 independent of DataForSEO family');
$p=PSTE_Normal_Metadata_Path::applyToPayload($e,$b,(string)($e['research_origin_family_key']??''));$n=$p['normal_metadata_path'];
check(!empty($n['title_precheck_validated'])&&($n['worker_flow']['steps']['title']['decision']??'')==='GREEN','Worker 2 does not require family assignment');
check(($n['worker_flow']['halted_at']??'')==='lane'&&($n['worker_flow']['storage']??'')==='EXISTING_SANDBOX','Unclear lane yellow, category not invented');
check(($p['production_title']??'')===''&&($p['textmachine_handoff_status']??'')!=='READY_FOR_COMPILER_CAPABILITY_CHECK','No blocked item reaches compiler');
$nonHorse=PSTE_Portal_Relevance_Gate::evaluateBeforeAssignment('Kaffeemaschine günstig kaufen',$b,$r);
check(empty($nonHorse['ok'])&&($nonHorse['status']??'')==='EXTERNAL_REVIEW_REQUIRED','Unrelated keyword remains yellow');
$bad=['contract'=>'PSTE_PORTAL_RELEVANCE_PROOF_V1','status'=>'RELEVANT_FOR_PORTAL','raw_query_sha256'=>str_repeat('0',64),'family_name'=>''];
$forged=PSTE_Portal_Relevance_Gate::evaluateBeforeAssignment($question,$b,$r,'',$bad);
check(empty($forged['ok'])&&($forged['status']??'')==='BLOCKED','Invalid bound proof rejected before auto-context');
$fach=$index['Welche Pferde OP-Versicherung ist besser, Barmenia oder Uelzener?'];
$f=PSTE_Normal_Metadata_Path::applyToPayload($fach,$b,(string)($fach['research_origin_family_key']??''))['normal_metadata_path'];
check(($f['status']??'')==='NORMAL_PASS'&&($f['article_type']??'')==='FAQ','Original Fach success preserved');
$journal=$index['Sind Haferflocken für Pferde geeignet?'];
$j=PSTE_Normal_Metadata_Path::applyToPayload($journal,$b,(string)($journal['research_origin_family_key']??''))['normal_metadata_path'];
check(($j['status']??'')==='NORMAL_PASS'&&($j['article_type']??'')==='Journal','Original Journal success preserved');
check(empty($j['production_handoff_attempted'])&&empty($j['article_or_taxonomy_write_attempted']),'No provider, taxonomy or publish write attempted');
echo "WORKER CORE ROOT ORDER REGRESSION PASS\n";