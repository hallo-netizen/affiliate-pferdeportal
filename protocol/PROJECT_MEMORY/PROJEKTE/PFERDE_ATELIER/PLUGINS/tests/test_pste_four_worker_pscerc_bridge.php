<?php
error_reporting(E_ERROR|E_WARNING);ini_set('memory_limit','1400M');
define('ABSPATH','/tmp/'); define('PSTE_DIR',rtrim((string)getenv('PSTE_TEST_PLUGIN_ROOT'),'/').'/'); define('PSERC_DIR','/mnt/data/seo_work/original/portal-seo-editorial-plan-compiler/');
function wp_strip_all_tags($s){return strip_tags($s);} function wp_json_encode($v,$f=0){return json_encode($v,$f);} function get_option($x,$d=false){return $d;} function is_wp_error($v){return false;}
$terms=['ausbildung-reitweisen'=>1488,'pferde-verstehen'=>1481,'alltags-pferde-haltungsformen'=>1485,'pferdeernaehrung-verstehen'=>1487,'pferdegesundheit-verstehen'=>1486,'recht-finanzen-organisation'=>1483,'pferdewissen-grundlagen'=>1500,'reiterleben-community'=>1484,'pferderassen-pferdetypen'=>1482];
function get_term_by($field,$slug,$tax){global $terms; if(getenv('NO_JOURNAL_TERMS')==='1')return false; if(!isset($terms[$slug]))return false;return (object)['term_id'=>$terms[$slug],'slug'=>$slug,'taxonomy'=>$tax,'name'=>$slug];}
foreach(glob(PSTE_DIR.'includes/*.php') as $p) require_once $p;
foreach(glob(PSERC_DIR.'includes/*.php') as $p) require_once $p;
$from=array_map(static fn($q)=>['q'=>$q],['Sind Haferflocken für Pferde geeignet?','Wie lange soll man Pferde auf die Weide lassen?','Warum fressen Pferde auf der Weide so viel Heu?']);
$data=json_decode(file_get_contents('/mnt/data/pferde-seo-audit/_SEO_EXPORT_ARBEITSKOPIE_20261016.txt'),true,512,JSON_THROW_ON_ERROR);
$base=$data['site_baseline'];$candidates=[];foreach($data['candidates'] as $c){$q=(string)($c['primary_longtail_query']??$c['canonical_query']??'');$candidates[$q]=$c;}
$counts=['total'=>0,'normal_pass'=>0,'verified_signed'=>0,'slot_pass'=>0,'negative_title'=>0,'negative_category'=>0,'negative_no_slot'=>0,'errors'=>[], 'examples'=>[]];
foreach($from as $e){$q=$e['q'];$counts['total']++;$c=$candidates[$q]??[];
 try{$r=PSTE_Normal_Metadata_Path::evaluateRaw($q,$base,(string)($c['research_origin_family_key']??''),[],$c);
 $status=(string)($r['status']??'');$route=$r['article_type_extension_routing']??[];$target=$r['target_category']??[];$title=(string)($r['title']??'');
 $topic=['article_type'=>(string)($r['article_type']??''),'category_id'=>(int)($target['term_id']??0),'category_name'=>(string)($target['name']??''),'category_slug'=>(string)($target['slug']??''),'title'=>$title,'production_title'=>$title,'target_keyword'=>(string)($r['target_keyword']??''),'semantic_consensus'=>(array)($r['semantic_consensus']??[]),'article_type_extension_routing'=>$route,'journal_routing'=>$route];
 $pass=$status==='NORMAL_PASS'&&($r['article_type']??'')==='Journal'; if($pass)$counts['normal_pass']++;
 $verified=PSERC_Article_Type_Extension_Registry::verifyTopicBinding($topic);if(!empty($verified['ok']))$counts['verified_signed']++;
 $slot=['plan'=>['slots'=>[['article_type'=>'Journal','category_slug'=>(string)($route['canonical_plan_category_slug']??''),'canonical_article_id'=>'simulation-only']]]];
 $g=PSERC_Article_Type_Extension_Planning_Gate::evaluate($topic,$slot);if(!empty($g['ok']))$counts['slot_pass']++;
 $bt=$topic;$bt['production_title'].=' Manipulation';$ng=PSERC_Article_Type_Extension_Registry::verifyTopicBinding($bt);if(empty($ng['ok']))$counts['negative_title']++;
 $bc=$topic;$bc['category_slug']=$topic['category_slug']==='pferde-verstehen'?'ausbildung-reitweisen':'pferde-verstehen';$ng=PSERC_Article_Type_Extension_Registry::verifyTopicBinding($bc);if(empty($ng['ok']))$counts['negative_category']++;
 $ng=PSERC_Article_Type_Extension_Planning_Gate::evaluate($topic,['plan'=>['slots'=>[]]]);if(empty($ng['ok']))$counts['negative_no_slot']++;
 $counts['examples'][]=['q'=>$q,'status'=>$status,'title'=>$title,'cat'=>$topic['category_slug'],'type'=>$topic['article_type'],'signed_ok'=>!empty($verified['ok']),'slot_ok'=>!empty($g['ok']),'route_code'=>$route['reason_codes']??[]];
 }catch(Throwable $ex){$counts['errors'][]=['q'=>$q,'error'=>$ex->getMessage()];}
}
unset($data); echo json_encode($counts,JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);echo "\n";