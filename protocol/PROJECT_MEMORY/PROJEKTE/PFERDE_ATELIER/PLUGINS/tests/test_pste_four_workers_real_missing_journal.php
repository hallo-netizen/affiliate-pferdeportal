<?php
declare(strict_types=1);
error_reporting(E_ERROR);ini_set('memory_limit','1024M');
define('ABSPATH','/tmp/');define('PSTE_DIR',rtrim((string)(getenv('PSTE_TEST_PLUGIN_ROOT')?:dirname(__DIR__).'/Portal SEO Topic Engine'),'/').'/');
function wp_strip_all_tags($s){return strip_tags($s);}function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}function get_option($n,$d=false){return $d;}function is_wp_error($v){return false;}
$GLOBALS['simulate_category_exists']=false;
function get_term_by($field,$slug,$taxonomy){if(!$GLOBALS['simulate_category_exists'])return false;$terms=['ausbildung-reitweisen'=>1488,'pferde-verstehen'=>1481,'alltags-pferde-haltungsformen'=>1485,'pferdeernaehrung-verstehen'=>1487,'pferdegesundheit-verstehen'=>1486,'recht-finanzen-organisation'=>1483,'pferdewissen-grundlagen'=>1500,'reiterleben-community'=>1484,'pferderassen-pferdetypen'=>1482];if(!isset($terms[$slug]))return false;return (object)['term_id'=>$terms[$slug],'slug'=>$slug,'taxonomy'=>$taxonomy,'name'=>$slug];}
foreach(glob(PSTE_DIR.'includes/*.php') as $file)require_once $file;
$d=json_decode(file_get_contents((string)(getenv('PSTE_TEST_ORIGINAL_4501_EXPORT')?:'/mnt/data/pferde-seo-audit/_SEO_EXPORT_ARBEITSKOPIE_20261016.txt')),true,512,JSON_THROW_ON_ERROR);
$baseline=$d['site_baseline'];
foreach(['Warum leckt mein Pferd viel am Salzleckstein?','Wie reitet man ohne Steigbügel?','Wie kann ich die Weidehaltung meines Pferdes organisieren?','Warum wehrt sich mein Pferd in der Herde?','Welche Pferde OP-Versicherung ist besser, Barmenia oder Uelzener?'] as $raw){
foreach([false,true] as $exists){$GLOBALS['simulate_category_exists']=$exists;
$r=PSTE_Normal_Metadata_Path::evaluateRaw($raw,$baseline);$w=$r['worker_flow']??[];
echo json_encode(['raw'=>$raw,'exists'=>$exists,'status'=>$r['status'],'title'=>$r['title'],'type'=>$r['article_type'],'target'=>$r['target_category']['slug']??'','room'=>$r['category_backlog_required']??false,'storage'=>$w['storage']??'','halt'=>$w['halted_at']??'','steps'=>$w['steps']??[],'reasons'=>array_slice($r['reason_codes']??[],0,4)],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}}