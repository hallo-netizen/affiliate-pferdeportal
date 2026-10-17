<?php
declare(strict_types=1);error_reporting(E_ALL);
define('ABSPATH','/tmp/');
function wp_strip_all_tags($v){return strip_tags($v);}
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
function get_option($key,$default=false){return $default;}
$dir=getenv('PSTE_SOURCE_DIR')?:'/mnt/data/seo_work/modified/Portal SEO Topic Engine';
foreach(glob($dir.'/includes/*.php') as $f) require_once $f;
function check($ok,$msg){if(!$ok)throw new RuntimeException($msg);}
$raw='Wie pflege ich mein Pferd im Winter?';
$path=['contract'=>'PSTE_NORMAL_METADATA_PATH_V2','status'=>'NORMAL_PASS','ok'=>true,'raw_query'=>$raw,'raw_query_sha256'=>hash('sha256',$raw),'title'=>'Wie pflege ich mein Pferd im Winter?','article_type'=>'FAQ',
  'title_pipeline'=>['ok'=>true],'title_candidate_only'=>false,'target_category'=>['term_id'=>345,'slug'=>'pferdepflege-faq']];
$topic=['primary_longtail_query'=>$raw,'discovery_only'=>true,'automatic_pool_status'=>'AUTO_RESOLVED','normal_metadata_path'=>$path,'derived_state_authority'=>['recomputed'=>true],
 'decision'=>'PASS','planning_readiness_gate'=>[],'pre_title_duplicate_gate'=>[],'reason_codes'=>[], 'production_title'=>$path['title']];
check(PSTE_Topic_Policy::classifyRole($topic)==='ARTICLE_TOPIC','full four step ready probe must be promoted');
foreach([
  ['case'=>'not_validated_title','mutate'=>static function(&$r){$r['normal_metadata_path']['title_pipeline']['ok']=false;}],
  ['case'=>'missing_category','mutate'=>static function(&$r){$r['normal_metadata_path']['target_category']['term_id']=0;}],
  ['case'=>'stale_unbound_raw','mutate'=>static function(&$r){$r['normal_metadata_path']['raw_query']='Anderes Thema';}],
  ['case'=>'not_current_authority','mutate'=>static function(&$r){$r['derived_state_authority']['recomputed']=false;}],
  ['case'=>'needs_sandbox','mutate'=>static function(&$r){$r['normal_metadata_path']['status']='SANDBOX_REQUIRED';}],
  ['case'=>'explicit_discovery_only','mutate'=>static function(&$r){$r['automatic_pool_status']='DISCOVERY_ONLY';}],
  ['case'=>'unresolved','mutate'=>static function(&$r){$r['automatic_pool_status']='REVIEW_REQUIRED';}],
  ['case'=>'exact_duplicate','mutate'=>static function(&$r){$r['reason_codes']=['EXACT_NORMALIZED_QUERY_DUPLICATE'];}],
  ['case'=>'covered_answer','mutate'=>static function(&$r){$r['reason_codes']=['ANSWER_EQUIVALENT_EXISTING'];}],
] as $x){$r=$topic;$x['mutate']($r);check(PSTE_Topic_Policy::classifyRole($r)!=='ARTICLE_TOPIC','incorrectly promoted '.$x['case']);}
$normal=$topic;$normal['discovery_only']=false;check(PSTE_Topic_Policy::classifyRole($normal)==='ARTICLE_TOPIC','normal article path regressed');
echo json_encode(['status'=>'PASS','positive'=>2,'negative'=>9,'logic'=>'only fully current source-bound normal passes may override old discovery label; no bypass'],JSON_PRETTY_PRINT)."\n";