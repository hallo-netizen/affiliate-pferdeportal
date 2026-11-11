<?php
declare(strict_types=1);
/** Read-only, offline, end-to-end contract simulation. Not a production K0 run. */
error_reporting(E_ALL);
define('ABSPATH', '/qa-no-real-wordpress/');
define('ARRAY_A','ARRAY_A');
define('PSERC_VERSION','0.28.65');
define('PSERC_BUILD','QA_LOCAL_ONLY');
$qa=__DIR__; $pste=dirname($qa).'/qa_combined/packaged_qa/Portal SEO Topic Engine/includes/';
$pserc=$qa.'/pserc-qa-next/portal-seo-editorial-plan-compiler/includes/';
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
function wp_strip_all_tags($v){return strip_tags($v);}
function is_wp_error($v){return false;}
function wp_remote_retrieve_response_code($r){return $r['response']['code'];}
function wp_remote_retrieve_body($r){return $r['body'];}
function wp_slash($v){return $v;}
function sanitize_title($s){$s=function_exists('mb_strtolower')?mb_strtolower($s,'UTF-8'):strtolower($s);$s=preg_replace('/[^a-z0-9äöüß]+/u','-',$s);return trim($s,'-');}
class PSTE_Credentials {public static function resolve(){return ['login'=>'fake-qa-only','password'=>'fake-qa-only'];}}
$GLOBALS['provider_calls']=[];$GLOBALS['scenario']='good';$GLOBALS['transients']=[];$GLOBALS['posts']=[];$GLOBALS['next_post_id']=2000;
function get_transient($k){return $GLOBALS['transients'][$k]??false;}
function set_transient($k,$v,$ttl){$GLOBALS['transients'][$k]=$v;return true;}
function delete_transient($k){unset($GLOBALS['transients'][$k]);return true;}
function wp_remote_request($url,$args){
  $GLOBALS['provider_calls'][]=['url'=>$url,'method'=>$args['method'],'payload'=>json_decode($args['body']??'null',true)];
  $items=[];
  foreach(['horseware regendecken','fliegen regendecke pferd','regendecke pferd 0g'] as $i=>$query){
    $items[]=['keyword'=>$query,'keyword_info'=>['search_volume'=>[110,70,50][$i],'cpc'=>0.2,'competition'=>0.23]];
  }
  $status=$GLOBALS['scenario']==='provider_error'?40102:20000;
  $b=['status_code'=>20000,'status_message'=>'Ok.','cost'=>0.0,'tasks_count'=>1,'tasks_error'=>0,
    'tasks'=>[['status_code'=>$status,'status_message'=>$status===20000?'OK':'QA error','result'=>[['items'=>$items]]]]];
  if($GLOBALS['scenario']==='invalid_json')return ['response'=>['code'=>200],'body'=>'{bad'];
  return ['response'=>['code'=>200],'body'=>json_encode($b,JSON_UNESCAPED_UNICODE)];
}
// Fake WordPress draft database. No disk/database writes.
function get_term_by($kind,$slug,$taxonomy){return $slug==='pferdedecken-regendecken-beratung'?(object)['term_id'=>10,'slug'=>$slug]:false;}
function get_posts($filter){return array_keys($GLOBALS['posts']);}
function get_post($id,$output=null){return $GLOBALS['posts'][$id]??null;}
function get_post_meta($id,$key,$single){return $GLOBALS['posts'][$id]['meta_input'][$key]??'';}
function wp_get_post_categories($id){return $GLOBALS['posts'][$id]['post_category']??[];}
function wp_insert_post($post,$wp_error=true){$id=++$GLOBALS['next_post_id'];$GLOBALS['posts'][$id]=$post;return $id;}
function wp_delete_post($id,$force=true){unset($GLOBALS['posts'][$id]);return true;}
class PPM679_Editorial_Plan_Runtime_Gate {
 public static function record_readback($bindings,$readbacks,$source){
  if($source!=='wordpress_article_import'||count($bindings)!==count($readbacks))return ['ok'=>false];
  foreach($readbacks as $r){if(!isset($GLOBALS['posts'][$r['post_id']]))return ['ok'=>false];}
  return ['ok'=>true,'status'=>'QA_MOCK_RUNTIME_SYNC_PASS','publish_allowed'=>false];
 }
}
require_once $pste.'class-pste-normalizer.php';
require_once $pste.'class-pste-dataforseo-client.php';
require_once $pste.'class-pste-article-type-registry.php';
require_once $pste.'class-pste-intent-profile.php';
require_once $pserc.'class-pserc-stable-json.php';
require_once $pserc.'class-pserc-plan-slot-identity.php';
require_once $pserc.'class-pserc-metadata-boundary.php';
require_once $pserc.'class-pserc-system4-import.php';
$pass=0;$fail=[];$checks=[];
function check($condition,$name){global $pass,$fail,$checks;$checks[]=['name'=>$name,'pass'=>(bool)$condition];if($condition)$pass++;else $fail[]=$name;}
$oldFile=dirname($qa,2).'/seo-redaktionsplan-ohne-suchintent-nachweis-42619ca7b6e36a625e0c8ae4e562534a9ff1b115ac7772f598435a064d06f546 (2).json';
$old=json_decode(file_get_contents($oldFile),true,512,JSON_THROW_ON_ERROR);
$assertive=fn($text)=>$text;
$client=new PSTE_DataForSEO_Client('sandbox');
$keywordRows=[];
foreach(['keywordSuggestions','relatedKeywords','keywordIdeas'] as $method){
 $response= $method==='keywordIdeas'?$client->$method(['regendecken'],'Germany','German',100):$client->$method('regendecken','Germany','German',100);
 $rows=PSTE_DataForSEO_Client::extractKeywords($response);
 check(count($rows)===3,'DataForSEO '.$method.' accepted + extracted 3 rows');
 check(PSTE_DataForSEO_Client::responseCostUsd($response)===0.0,'DataForSEO '.$method.' fixture zero billed cost');
 $keywordRows=array_merge($keywordRows,$rows);
}
check(count($GLOBALS['provider_calls'])===3,'DataForSEO exactly 3 mocked HTTP requests');
$cached=$client->keywordSuggestions('regendecken','Germany','German',100);
check(PSTE_DataForSEO_Client::cacheHit($cached)===true,'DataForSEO same-request cache readback');
check(count($GLOBALS['provider_calls'])===3,'DataForSEO duplicate cached request incurs no further HTTP call');
check(count(array_unique(array_column($keywordRows,'keyword')))==3,'provider rows dedupe 3 distinct keywords');
check(PSTE_DataForSEO_Client::endpointAllowed('POST','/v3/dataforseo_labs/google/related_keywords/live'),'provider allowlist accepts documented endpoint');
check(!PSTE_DataForSEO_Client::endpointAllowed('DELETE','/v3/dataforseo_labs/google/related_keywords/live'),'provider allowlist rejects forbidden endpoint');
try {$client->request('DELETE','/v3/dataforseo_labs/google/related_keywords/live');check(false,'forbidden network endpoint blocked');}
catch(RuntimeException $e){check($e->getMessage()==='PSTE_ENDPOINT_NOT_ALLOWLISTED','forbidden network endpoint blocked');}
$GLOBALS['scenario']='provider_error';
try{$client->request('POST','/v3/dataforseo_labs/google/related_keywords/live',[['keyword'=>'regendecken']]);check(false,'provider error blocked');}
catch(Throwable $e){check(str_contains($e->getMessage(),'PROVIDER'),'provider error blocked');}
$GLOBALS['scenario']='invalid_json';
try{$client->request('POST','/v3/dataforseo_labs/google/related_keywords/live',[['keyword'=>'regendecken']]);check(false,'malformed provider JSON blocked');}
catch(Throwable $e){check(str_contains($e->getMessage(),'RESPONSE_INVALID_JSON'),'malformed provider JSON blocked');}
$GLOBALS['scenario']='good';
$realRows=$old['items'];$batch=$old['next_textmachine_metadata_batch'];
check(PSERC_Metadata_Boundary::validateBatch($batch)['ok']===true,'original WordPress export five-field boundary PASS');
$registry=['families'=>['regendecken'=>['by_type'=>['beratung'=>['article_type'=>'Beratung']]]]];
$semantic=['ok'=>true,'resolved_article_type'=>'Beratung','intent_consensus'=>true,'strand_a'=>['search_intent'=>'EDITORIAL_INFORMATION'],'strand_b'=>['search_intent'=>'EDITORIAL_INFORMATION']];
$newManifest=$old;
$research=[];
foreach($realRows as $i=>$item){
 $raw=$item['intent_profile']['raw_query'];
 check(in_array($raw,array_column($keywordRows,'keyword'),true),'DataForSEO result matches stored real topic '.$i);
 $profile=$item['intent_profile'];
 check(PSTE_Intent_Profile::verifiedPreTypeForRaw($profile,$raw),'saved real SEO-first source proof signed '.$i);
 $bound=PSTE_Intent_Profile::bindArticleType($profile,$semantic,$registry,'regendecken');
 check($bound['status']==='PASS'&&$bound['phase']==='BOUND_TYPE','PSTE real original profile binding '.$i);
 check($bound['search_intent']===$profile['primary_user_goal'],'original SEO intent preserved into bind '.$i);
 check(!empty($bound['profile_sha256']),'signed final profile '.$i);
 $newManifest['items'][$i]['intent_profile']=$bound;
 $research[]=['keyword'=>$raw,'volume_fixture'=>[110,70,50][$i],'real_wp_topic_id'=>$item['seo_topic_id'],'analysis_source'=>'REAL_EXISTING_PRE_TYPE','provider_fixture'=>'SIMULATED'];
}
unset($newManifest['manifest_sha256']);$newManifest['manifest_sha256']=PSERC_Stable_Json::hash($newManifest);
check(PSERC_Stable_Json::hash(array_diff_key($newManifest,['manifest_sha256'=>true]))===$newManifest['manifest_sha256'],'new manifest correctly signed');
check($newManifest['next_textmachine_metadata_batch']===$batch,'five-field SEO to PSERC export unchanged');
foreach($newManifest['items'] as $i=>$row){
 $p=$row['intent_profile'];$pHash=$p['profile_sha256'];unset($p['profile_sha256'],$p['analysis_sha256']);
 check(PSERC_Stable_Json::hash($p)===$pHash,'PSERC upstream source proof '.$i);
 check(PSERC_Stable_Json::hash($row['metadata_binding'])===PSERC_Stable_Json::hash($batch['items'][$i]),'export source row exact identity '.$i);
}
// K0 import mirrored from original GitHub engine/k0_seo_owner_binding.py + k0_portal_resolver.py.
$k0Imported=0;
foreach($batch['items'] as $i=>$row){
 $one=['contract'=>$batch['contract'],'status'=>$batch['status'],'item_count'=>1,'publish_allowed'=>false,'content_or_format_payload_present'=>false,'items'=>[$row]];
 $one['batch_sha256']=PSERC_Stable_Json::hash($one);
 check(PSERC_Metadata_Boundary::validateBatch($one)['ok']===true,'K0 single metadata intake valid '.$i);
 $source=$newManifest['items'][$i]['intent_profile'];
 $k0Safe=$row==$newManifest['items'][$i]['metadata_binding']&&($source['status']??'')==='PASS'&&($source['article_type']??'')===$row['article_type']&&($source['search_intent']??'')==='INFORMATIONAL_FOCUS';
 check($k0Safe,'K0 owner-only source gate verified '.$i);
 if($k0Safe)$k0Imported++;
}
check($k0Imported===3,'K0 three source-verified imports simulated');
// Negative cases: intentional tampering or unauthorized extra field.
$bad=$batch;$bad['items'][0]['body_html']='<h1>untrusted</h1>';check(PSERC_Metadata_Boundary::validateBatch($bad)['ok']===false,'content injected into five-field intake blocked');
$bad=$batch;$bad['items'][1]['plan_slot']=$batch['items'][0]['plan_slot'];check(PSERC_Metadata_Boundary::validateBatch($bad)['ok']===false,'duplicated canonical slot blocked');
$bad=$batch;$bad['items'][0]['title']='changed without new signature';check(PSERC_Metadata_Boundary::validateBatch($bad)['ok']===false,'changed article title without signature blocked');
$bad=$newManifest;$bad['items'][0]['intent_profile']['search_intent']='BUY';check(PSERC_Stable_Json::hash(array_diff_key($bad,['manifest_sha256'=>true]))!==$bad['manifest_sha256'],'changed goal without source signature blocked');
// Full post import uses the existing PSERC System4 code in fake WP, fixture article content NOT K0 production.
$wordpress=[];
foreach($realRows as $i=>$row){
 $b=$batch['items'][$i];$articleId=$row['canonical_slot']['canonical_article_id'];
 check(PSERC_Plan_Slot_Identity::tokenFromCanonicalId($articleId)===$b['plan_slot'],'canonical ID owns plan slot '.$i);
 $slug=['qa-horseware-regendecken','qa-fliegen-regendecke','qa-regendecke-0g'][$i];
 $body='<p><strong>SIMULATION. Kein echter redaktionell geprüfter Artikel.</strong></p><p>Testtext für Import und Export zu: '.htmlspecialchars($b['title'],ENT_QUOTES,'UTF-8').'.</p>';
 $wordpress[]=['article_id'=>$articleId,'slug'=>$slug,'plan_slot'=>$b['plan_slot'],'title'=>$b['title'],'target_keyword'=>$b['target_keyword'],'category'=>$b['category'],'article_type'=>$b['article_type'],'body'=>$body];
}
$wpPayload=['contract'=>'PFERDE_ATELIER_WORDPRESS_IMPORT_V1','articles'=>$wordpress];
$validate=PSERC_System4_Import::normalizePayload($wpPayload);
check(($validate['ok']??false)===true,'WordPress post import normalized via real PSERC code');
$wpResult=PSERC_System4_Import::importPayload($wpPayload);
check(($wpResult['ok']??false)===true,'WordPress post import actually executed in mock WP via real PSERC code');
check(count($GLOBALS['posts'])===3,'WordPress draft importer produced 3 simulated posts');
check(count($wpResult['created_post_ids']??[])===3,'WordPress importer verified 3 readbacks');
check(($wpResult['publish_allowed']??null)===false,'WordPress importer cannot publish');
$bad=$wpPayload;$bad['articles'][0]['plan_slot']=str_repeat('0',64);
check(($x=PSERC_System4_Import::normalizePayload($bad))['ok']===false,'WordPress importer rejects wrong plan-slot');
$bad=$wpPayload;$bad['articles'][1]['slug']=$bad['articles'][0]['slug'];
check(PSERC_System4_Import::normalizePayload($bad)['ok']===false,'WordPress importer rejects duplicate slug');
$bad=$wpPayload;$bad['articles'][1]['body']='';
check(PSERC_System4_Import::normalizePayload($bad)['ok']===false,'WordPress importer rejects empty article');
// Pure file export. It tests a TXT file boundary, NOT LLM text generation, fact-checking, or LanguageTool.
$txt="SIMULATIONSERGEBNIS – KEIN PRODUKTIONSARTIKEL\n\n";
foreach($wordpress as $i=>$a){
 $txt.="=== Testartikel ".($i+1)." ===\n".$a['title']."\n";
 $txt.="Suchintention aus gespeichertem SEO-Nachweis: ".$newManifest['items'][$i]['intent_profile']['search_intent']."\n";
 $txt.="Keyword: ".$a['target_keyword']."\nKategorie: ".$a['category']."\n\n";
 $bodyPlain=preg_replace('/<\/p>/i',"\n\n",$a['body']);
 $txt.=trim(html_entity_decode(strip_tags($bodyPlain),ENT_QUOTES,'UTF-8'))."\n\n";
}
file_put_contents($qa.'/simulierter-text-export.txt',$txt);
check(file_get_contents($qa.'/simulierter-text-export.txt')===$txt,'TXT export real filesystem readback');
check(!str_contains($txt,'<p>'),'TXT export stripped HTML');
check(substr_count($txt,'=== Testartikel')===3,'TXT export exactly 3 article test records');
// The fake completed SEO proof must NOT be a production-shaped top-level JSON.
file_put_contents($qa.'/QA-NICHT-IMPORTIEREN-seo-export.json',json_encode(['contract'=>'OFFLINE_SIMULATION_NOT_IMPORTABLE_V1','publish_allowed'=>false,'simulated'=>true,'non_production_fixture'=>$newManifest],JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
file_put_contents($qa.'/QA-NICHT-IMPORTIEREN-wordpress.json',json_encode(['contract'=>'OFFLINE_SIMULATION_NOT_IMPORTABLE_V1','publish_allowed'=>false,'simulated'=>true,'non_production_fixture'=>$wpPayload],JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
$report=[
 'status'=>$fail?'FAIL':'PASS','passed'=>$pass,'failed'=>count($fail),'failures'=>$fail,
 'scope'=>['DataForSEO HTTP'=>'MOCKED_NO_NETWORK','SEO 3 keyword rows'=>'PROVIDER_FIXTURE','PRE_TYPE saved provenance'=>'REAL_USER_EXPORT','PSTE intent binder'=>'ACTUAL_PATCHED_PHP','PSERC metadata validator'=>'ACTUAL_PHP','PSERC manifest hash'=>'ACTUAL_PHP','K0 intake'=>'MIRRORED_VALIDATOR_ONLY_NOT_REAL_PYTHON_RUN','WordPress final article import'=>'ACTUAL_PSERC_PHP_WITH_FAKE_WP_DATABASE','TXT export'=>'FILE_IO_TEST_FIXTURE_NOT_REAL_K0_PRODUCTION'],
 'real_articles'=>count($realRows),'mock_provider_calls'=>count($GLOBALS['provider_calls']),'k0_verified_import_items'=>$k0Imported,'simulated_wp_drafts'=>count($GLOBALS['posts']),
 'simulation_exports_are_non_importable_wrappers'=>true,'real_production_text_generated'=>false,'wordpress_test_installation_touched'=>false,'dataforseo_paid_request_sent'=>false,'publish_allowed'=>false,
 'seo_manifest_sha256'=>$newManifest['manifest_sha256'],'original_batch_sha256'=>$batch['batch_sha256'],'text_sha256'=>hash('sha256',$txt),'checks'=>$checks,
];
file_put_contents($qa.'/ergebnis-vollworkflow-simulation.json',json_encode($report,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
echo json_encode(['status'=>$report['status'],'passed'=>$pass,'failed'=>count($fail),'failures'=>$fail,'real_articles'=>count($realRows),'provider_calls'=>count($GLOBALS['provider_calls']),'drafts'=>count($GLOBALS['posts']),'txt_bytes'=>strlen($txt)],JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE)."\n";
if($fail)exit(2);