<?php
define('ABSPATH', __DIR__.'/');
define('APKW_VERSION','1.6.1');
define('APKW_MASTER_CONTRACT_ID','ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK');
define('APKW_CONTENT_WRITE_CAPABILITY',false);
define('APKW_RESEARCH_SCHEMA_VERSION','1.4');
define('APKW_CATEGORY_SCHEMA_VERSION','1.4');

$GLOBALS['options']=['apkw_dataforseo_login'=>'test-login','apkw_dataforseo_password'=>'test-password','apkw_default_location_name'=>'Germany','apkw_default_language_code'=>'de'];
$GLOBALS['terms']=[];$GLOBALS['posts']=[];$GLOBALS['remote_requests']=[];$GLOBALS['remote_fail_auth']=false;$GLOBALS['remote_get_override']=null;$GLOBALS['remote_post_override']=null;

function get_option($k,$d=''){return $GLOBALS['options'][$k]??$d;} function update_option($k,$v,$autoload=false){$GLOBALS['options'][$k]=$v;return true;}
function sanitize_text_field($v){return trim(strip_tags((string)$v));} function sanitize_key($v){return strtolower(preg_replace('/[^a-z0-9_\-]/','',(string)$v));}
function sanitize_title($v){$v=html_entity_decode((string)$v,ENT_QUOTES|ENT_HTML5,'UTF-8');$v=strtr($v,['ä'=>'ae','ö'=>'oe','ü'=>'ue','Ä'=>'ae','Ö'=>'oe','Ü'=>'ue','ß'=>'ss']);$v=strtolower($v);$v=preg_replace('/[^a-z0-9]+/','-',$v);return trim($v,'-');}
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);} function wp_salt($scheme='auth'){return 'test-wordpress-auth-salt-'.(string)$scheme;} function home_url($p='/'){return 'https://example.test'.($p==='/'?'/':$p);} function wp_generate_uuid4(){static $i=1;return sprintf('00000000-0000-4000-8000-%012d',$i++);} function absint($v){return abs((int)$v);} function is_wp_error($v){return false;}
function get_posts($args=[]){return [];} function get_post($id){return $GLOBALS['posts'][$id]??null;} function get_the_title($p){return is_object($p)?($p->post_title??''):'';}
function get_taxonomies($args=[],$output='names'){return ['category'=>(object)['name'=>'category'],'hp_listing_category'=>(object)['name'=>'hp_listing_category'],'journal_cat'=>(object)['name'=>'journal_cat']];}
function get_terms($args=[]){return array_values($GLOBALS['terms'][$args['taxonomy']??'']??[]);} function taxonomy_exists($t){return in_array($t,['category','hp_listing_category','journal_cat'],true);} function get_term($id,$tax){return $GLOBALS['terms'][$tax][$id]??false;} function get_term_by($field,$value,$tax){foreach($GLOBALS['terms'][$tax]??[] as $t)if(($t->$field??null)===$value)return $t;return false;}
class WP_Error { public function get_error_message(){return 'mock';} }
function make_dfs_item($keyword,$volume,$core,$intent='informational',$kd=20){return ['keyword'=>$keyword,'keyword_info'=>['search_volume'=>$volume,'cpc'=>1.0,'competition'=>0.4,'competition_level'=>'MEDIUM','monthly_searches'=>[],'last_updated_time'=>'2026-08-01 00:00:00 +00:00'],'search_intent_info'=>['main_intent'=>$intent,'foreign_intent'=>[]],'keyword_properties'=>['core_keyword'=>$core,'keyword_difficulty'=>$kd,'detected_language'=>'de']];}
function mock_cluster_items(){return [
    make_dfs_item('brot',5000,'brot','informational'),
    make_dfs_item('sauerteig',4000,'sauerteig','informational'),make_dfs_item('sauerteig selber machen',1600,'sauerteig','informational'),make_dfs_item('sauerteig ansetzen',1300,'sauerteig','informational'),make_dfs_item('sauerteig füttern',900,'sauerteig','informational'),make_dfs_item('sauerteig pflegen',700,'sauerteig','informational'),make_dfs_item('sauerteig starter',600,'sauerteig','commercial'),
    make_dfs_item('anstellgut',1800,'anstellgut','informational'),make_dfs_item('anstellgut selber machen',700,'anstellgut','informational'),make_dfs_item('anstellgut füttern',500,'anstellgut','informational'),make_dfs_item('anstellgut aufbewahren',400,'anstellgut','informational'),make_dfs_item('anstellgut auffrischen',350,'anstellgut','informational'),
    make_dfs_item('backzubehör',2500,'backzubehör','transactional'),make_dfs_item('gärkörbe',1200,'gärkörbe','transactional'),make_dfs_item('backstahl',900,'backstahl','transactional'),
    make_dfs_item('brotmagazin',700,'brotmagazin','informational'),make_dfs_item('brotkultur',650,'brotkultur','informational'),make_dfs_item('bäckerportraits',200,'bäckerportraits','informational')
];}
function mock_global_items(){return [
    make_dfs_item('brot',5000,'brot','informational'),
    make_dfs_item('sauerteig',4000,'sauerteig','informational'),
    make_dfs_item('backzubehör',2500,'backzubehör','transactional'),
    make_dfs_item('brotmagazin',700,'brotmagazin','informational')
];}
function generic_overview_item($keyword){$k=function_exists('mb_strtolower')?mb_strtolower(trim($keyword),'UTF-8'):strtolower(trim($keyword));$map=['brot'=>[5000,'brot','informational'],'sauerteig'=>[4000,'sauerteig','informational'],'sauerteig starter'=>[600,'sauerteig','commercial'],'anstellgut'=>[1800,'anstellgut','informational'],'backzubehör'=>[2500,'backzubehör','transactional'],'gärkörbe'=>[1200,'gärkörbe','transactional'],'backstahl'=>[900,'backstahl','transactional'],'brotmagazin'=>[700,'brotmagazin','informational'],'brotkultur'=>[650,'brotkultur','informational'],'bäckerportraits'=>[200,'bäckerportraits','informational']];$m=$map[$k]??[100,$k,'informational'];return make_dfs_item($keyword,$m[0],$m[1],$m[2]);}
function dfs_response($items,$cost=0.01){return ['version'=>'0.1.test','status_code'=>20000,'status_message'=>'Ok.','cost'=>$cost,'tasks'=>[['id'=>'test-task','status_code'=>20000,'status_message'=>'Ok.','cost'=>$cost,'result'=>[['total_count'=>count($items),'items'=>$items]]]]];}
function wp_remote_get($url,$args=[]){$GLOBALS['remote_requests'][]=['method'=>'GET','url'=>$url,'args'=>$args];if($GLOBALS['remote_fail_auth'])return ['response'=>['code'=>401],'body'=>'{}'];if(is_callable($GLOBALS['remote_get_override']))return ($GLOBALS['remote_get_override'])($url,$args);if(is_array($GLOBALS['remote_get_override']))return $GLOBALS['remote_get_override'];return ['response'=>['code'=>200],'body'=>json_encode(['version'=>'0.1','status_code'=>20000,'status_message'=>'Ok.','cost'=>0,'tasks'=>[]])];}
function wp_remote_post($url,$args=[]){$GLOBALS['remote_requests'][]=['method'=>'POST','url'=>$url,'args'=>$args];if($GLOBALS['remote_fail_auth'])return ['response'=>['code'=>401],'body'=>'{}'];if(is_callable($GLOBALS['remote_post_override']))return ($GLOBALS['remote_post_override'])($url,$args);if(is_array($GLOBALS['remote_post_override']))return $GLOBALS['remote_post_override'];$payload=json_decode($args['body']??'[]',true);$task=$payload[0]??[];if(str_contains($url,'keyword_overview')){$items=[];foreach($task['keywords']??[] as $kw)$items[]=generic_overview_item($kw);$data=dfs_response($items,0.02);}elseif(str_starts_with((string)($task['tag']??''),'apkw-global-')){$data=dfs_response(mock_global_items(),0.04);}else{$data=dfs_response(mock_cluster_items(),0.03);}return ['response'=>['code'=>200],'body'=>json_encode($data,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)];}
function wp_remote_retrieve_response_code($r){return (int)$r['response']['code'];} function wp_remote_retrieve_body($r){return (string)$r['body'];}

require_once dirname(__DIR__).'/includes/class-apkw-settings.php';
require_once dirname(__DIR__).'/includes/class-apkw-dataforseo.php';
require_once dirname(__DIR__).'/includes/class-apkw-inventory.php';
require_once dirname(__DIR__).'/includes/class-apkw-validator.php';
require_once dirname(__DIR__).'/includes/class-apkw-research.php';
require_once dirname(__DIR__).'/includes/class-apkw-research-evidence.php';
require_once dirname(__DIR__).'/includes/class-apkw-comparator.php';

function assert_true($cond,$msg){if(!$cond)throw new RuntimeException($msg);} function codes($issues){return array_column($issues,'code');}
function cluster($id='brot',$seeds=['sauerteig','anstellgut','backzubehör','brotmagazin']){return ['cluster_id'=>$id,'name'=>'Brot','scope'=>'Brot handwerklich herstellen und vertiefen','exclusions'=>['Restaurants'],'seed_keywords'=>$seeds];}
function n($id,$block,$name,$slug,$pk,$intent,$parent=null,$level=1,$leaf=false,$cluster='brot'){$roles=['content'=>'CONTENT_EVERGREEN','marketplace'=>'MARKETPLACE_TRANSACTIONAL','magazine'=>'JOURNAL_EDITORIAL','glossary'=>'GLOSSARY_REFERENCE'];$tax=['content'=>'category','marketplace'=>'hp_listing_category','magazine'=>'journal_cat','glossary'=>'category'];return ['concept_id'=>$id,'block'=>$block,'pillar_role'=>$roles[$block],'research_cluster_id'=>$cluster,'level'=>$level,'name'=>$name,'slug'=>$slug,'parent_concept_id'=>$parent,'status'=>'APPROVED','primary_keyword'=>$pk,'search_intent'=>$intent,'intent_key'=>$id.'-intent','keyword_owner'=>true,'scope'=>'Scope '.$name,'exclusions'=>[],'longtail_potential'=>[],'is_leaf'=>$leaf,'target'=>['adapter'=>'wordpress_taxonomy','taxonomy'=>$tax[$block]]];}
function approve_initial($p){$p['initial_human_sight_review']=APKW_Validator::create_signed_review_receipt($p,'initial','Initialer Gesamtbaum sichtbar geprüft und freigegeben.',1,'2026-08-20T12:00:00Z');return $p;}
function approve_global_gap($p,$g){
    $defaults=[['core_keyword'=>'brot','decision'=>'MAIN_TOPIC','owner_concept_id'=>'c-root'],['core_keyword'=>'sauerteig','decision'=>'SUBTOPIC','owner_concept_id'=>'c-1'],['core_keyword'=>'backzubehör','decision'=>'MAIN_TOPIC','owner_concept_id'=>'m-root'],['core_keyword'=>'brotmagazin','decision'=>'MAIN_TOPIC','owner_concept_id'=>'j-root']];
    $p['global_coverage_decisions']=is_array($p['global_coverage_decisions']??null)?$p['global_coverage_decisions']:[];
    $seen=array_fill_keys(array_map(fn($d)=>$d['core_keyword']??'',$p['global_coverage_decisions']),true);
    foreach($defaults as $d){if(isset($seen[$d['core_keyword']]))continue;$owner=array_values(array_filter($p['nodes'],fn($n)=>$n['concept_id']===$d['owner_concept_id']))[0];$d['target_cluster_id']=$owner['research_cluster_id'];$d['reason']='Explizite fachliche Zuordnung.';$p['global_coverage_decisions'][]=$d;}
    $p['global_coverage_binding']=['package_id'=>$g['package_id'],'content_sha256'=>$g['content_sha256']];
    $p['global_gap_human_review']=APKW_Validator::create_signed_review_receipt($p,'global_gap','Global-Gaps und korrigierter Baum sichtbar geprüft und freigegeben.',1,'2026-08-20T12:30:00Z');return $p;
}
function draft_pkg(){ $p=['format'=>'affiliate-portal-category-package','schema_version'=>'1.4','master_contract_id'=>APKW_MASTER_CONTRACT_ID,'package_id'=>'draft-gaumen','package_version'=>1,'mode'=>'RESEARCH_DRAFT','project'=>['project_id'=>'gaumen-atelier','name'=>'Essen','scope'=>'Genussorientiertes Selbermachen; kein allgemeines Essen-Portal','target_market'=>'Germany','language_code'=>'de','exclusions'=>['Restaurants','Lieferdienste'],'discovery_seed_keywords'=>['lebensmittel selber machen','getränke selber machen','genuss handwerk']],'research_clusters'=>[cluster()],'default_targets'=>['content'=>['adapter'=>'wordpress_taxonomy','taxonomy'=>'category'],'marketplace'=>['adapter'=>'wordpress_taxonomy','taxonomy'=>'hp_listing_category'],'magazine'=>['adapter'=>'wordpress_taxonomy','taxonomy'=>'journal_cat']],'nodes'=>[
    n('c-root','content','Brot','brot','brot','informational',null,1,false),n('c-1','content','Sauerteig','sauerteig','sauerteig','informational','c-root',2,true),n('c-2','content','Anstellgut','anstellgut','anstellgut','informational','c-root',2,true),
    n('m-root','marketplace','Backzubehör','backzubehoer','backzubehör','transactional',null,1,false),n('m-1','marketplace','Gärkörbe','gaerkoerbe','gärkörbe','transactional','m-root',2,true),n('m-2','marketplace','Backstahl','backstahl','backstahl','transactional','m-root',2,true),
    n('j-root','magazine','Brotmagazin','brotmagazin','brotmagazin','informational',null,1,false),n('j-1','magazine','Brotkultur','brotkultur','brotkultur','informational','j-root',2,true),n('j-2','magazine','Bäckerportraits','baeckerportraits','bäckerportraits','informational','j-root',2,true)
]]; return approve_initial($p); }
function final_from_draft($draft,$research){$p=$draft;$reviewed=$research['source_draft']['package']??[];foreach(['global_coverage_decisions','global_coverage_binding','global_gap_human_review'] as $field)if(isset($reviewed[$field]))$p[$field]=$reviewed[$field];$p['package_id']='final-gaumen';$p['package_version']=2;$p['mode']='READ_ONLY_PREVIEW';$p['research_binding']=['package_id'=>$research['package_id'],'content_sha256'=>$research['content_sha256']];foreach($p['nodes'] as &$node){if($node['concept_id']==='c-1')$node['longtail_potential']=['sauerteig selber machen','sauerteig ansetzen','sauerteig füttern','sauerteig pflegen'];if($node['concept_id']==='c-2')$node['longtail_potential']=['anstellgut selber machen','anstellgut füttern','anstellgut aufbewahren','anstellgut auffrischen'];}unset($node);return $p;}
function research_from_draft($draft){$draft=approve_initial($draft);$GLOBALS['remote_requests']=[];$g=APKW_Research::build_global_coverage($draft,'Germany','de',1000,false);$draft=approve_global_gap($draft,$g);return APKW_Research::build_from_draft($draft,$g,'Germany','de',300,false);}

$tests=[];
$tests['free_connection_test_uses_user_data_and_zero_cost']=function(){$GLOBALS['remote_requests']=[];$r=APKW_DataForSEO::test_connection();assert_true($r['ok']&&$r['cost_usd']===0.0,'Verbindungstest muss kostenfrei sein');assert_true(count($GLOBALS['remote_requests'])===1&&str_contains($GLOBALS['remote_requests'][0]['url'],'/appendix/user_data'),'Falscher Endpoint');};
$tests['connection_auth_failure_is_reported']=function(){$GLOBALS['remote_fail_auth']=true;try{APKW_DataForSEO::test_connection();throw new RuntimeException('401 hätte fehlschlagen müssen');}catch(RuntimeException $e){assert_true(str_contains($e->getMessage(),'HTTP-Fehler 401'),'401 nicht sauber gemeldet');}finally{$GLOBALS['remote_fail_auth']=false;}};
$tests['draft_requires_all_three_core_pillars']=function(){$p=draft_pkg();$p['nodes']=array_values(array_filter($p['nodes'],fn($x)=>$x['block']!=='magazine'));$v=APKW_Validator::validate($p);assert_true(in_array('THREE_PILLAR_BLOCK_MISSING',codes($v['errors']),true),'Journal-Säule muss Pflicht sein');};
$tests['draft_requires_bounded_research_clusters']=function(){$p=draft_pkg();unset($p['research_clusters']);$v=APKW_Validator::validate($p);assert_true(in_array('RESEARCH_CLUSTERS_MISSING',codes($v['errors']),true),'Research-Cluster müssen Pflicht sein');};
$tests['draft_node_must_reference_known_cluster']=function(){$p=draft_pkg();$p['nodes'][1]['research_cluster_id']='fremd';$v=APKW_Validator::validate($p);assert_true(in_array('RESEARCH_CLUSTER_UNKNOWN',codes($v['errors']),true),'Unbekannter Cluster muss blockieren');};
$tests['preflight_is_free_and_makes_no_remote_request']=function(){$GLOBALS['remote_requests']=[];$p=APKW_Research::preflight_draft(draft_pkg());assert_true($p['valid'],'Preflight sollte PASS sein');assert_true(count($GLOBALS['remote_requests'])===0,'Preflight darf keine externe API aufrufen');assert_true($p['planned_paid_calls']['total']===3,'1 globale Coverage + 1 Cluster + 1 Overview erwartet');};
$tests['broad_project_name_is_never_used_as_dataforseo_seed']=function(){$r=research_from_draft(draft_pkg());foreach($GLOBALS['remote_requests'] as $req){if($req['method']!=='POST')continue;$body=json_decode($req['args']['body'],true);$keywords=$body[0]['keywords']??[];assert_true(!in_array('Essen',$keywords,true),'Projektname Essen darf nicht automatisch als Seed verwendet werden');}assert_true($r['source_draft']['package']['project']['name']==='Essen','Projektkontext muss trotzdem erhalten bleiben');};
$tests['research_uses_exact_overview_plus_one_call_per_cluster']=function(){$p=draft_pkg();$p['research_clusters'][]=cluster('fermentation',['fermentation','kimchi']);foreach($p['nodes'] as &$node){if(in_array($node['concept_id'],['j-root','j-1','j-2'],true))$node['research_cluster_id']='fermentation';}unset($node);$p=approve_initial($p);$GLOBALS['remote_requests']=[];$g=APKW_Research::build_global_coverage($p,'Germany','de',1000,false);$p=approve_global_gap($p,$g);$r=APKW_Research::build_from_draft($p,$g,'Germany','de',300,false);$posts=array_values(array_filter($GLOBALS['remote_requests'],fn($x)=>$x['method']==='POST'));assert_true(count($posts)===4,'1 globale Coverage + 2 Cluster + 1 Overview = 4 Calls erwartet');assert_true($r['research_summary']['paid_calls_total_workflow']===4&&$r['research_summary']['paid_calls_this_stage']===3,'Callzählung im Paket falsch');};
$tests['research_package_contains_no_credentials']=function(){$r=research_from_draft(draft_pkg());$j=json_encode($r);assert_true(!str_contains($j,'test-login')&&!str_contains($j,'test-password'),'Credentials dürfen nicht exportiert werden');};
$tests['research_hash_and_source_draft_hash_verify']=function(){$r=research_from_draft(draft_pkg());$v=APKW_Research::verify_package($r);assert_true($v['valid'],'Research-Paket muss verifizierbar sein');$r['source_draft']['package']['project']['scope']='manipuliert';assert_true(!APKW_Research::verify_package($r)['valid'],'Manipulierter Source-Draft muss erkannt werden');};
$tests['exact_visible_name_duplicate_global_blocks']=function(){$p=draft_pkg();$p['nodes'][3]['name']='Sauerteig';$v=APKW_Validator::validate($p);assert_true(in_array('VISIBLE_NAME_DUPLICATE_GLOBAL',codes($v['errors']),true),'Identischer sichtbarer Name muss global blockieren');};
$tests['similar_names_across_pillars_are_allowed']=function(){$p=draft_pkg();$p['nodes'][3]['name']='Sauerteig Zubehör';$p['nodes'][3]['primary_keyword']='sauerteig zubehör';$v=APKW_Validator::validate($p);assert_true(!in_array('VISIBLE_NAME_DUPLICATE_GLOBAL',codes($v['errors']),true),'Ähnliche Namen dürfen nicht blockiert werden');};
$tests['same_primary_keyword_within_same_pillar_blocks']=function(){$p=draft_pkg();$p['nodes'][2]['primary_keyword']='sauerteig';$v=APKW_Validator::validate($p);assert_true(in_array('PRIMARY_KEYWORD_DUPLICATE_WITHIN_BLOCK',codes($v['errors']),true),'Primärkeyword-Dublette in Säule muss blockieren');};
$tests['same_primary_cross_pillar_same_intent_blocks']=function(){$p=draft_pkg();$p['nodes'][3]['primary_keyword']='sauerteig';$p['nodes'][3]['search_intent']='informational';$v=APKW_Validator::validate($p);assert_true(in_array('PRIMARY_KEYWORD_CROSS_PILLAR_SAME_INTENT',codes($v['errors']),true),'Gleiches Primärkeyword+Intent über Säulen muss blockieren');};
$tests['same_primary_cross_pillar_different_intent_is_review_not_auto_block_in_draft']=function(){$p=draft_pkg();$p['nodes'][3]['primary_keyword']='sauerteig';$p['nodes'][3]['search_intent']='transactional';$v=APKW_Validator::validate($p);assert_true($v['valid'],'Unterschiedlicher Intent über Säulen darf Draft nicht blockieren');assert_true(in_array('PRIMARY_KEYWORD_CROSS_PILLAR_REVIEW',codes($v['warnings']),true),'Overlap-Review fehlt');};
$tests['final_binding_must_match_research_and_project']=function(){$d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);assert_true(APKW_Research::verify_binding($f,$r)['valid'],'Binding sollte passen');$f['project']['project_id']='anderes';assert_true(!APKW_Research::verify_binding($f,$r)['valid'],'Projekt-Mismatch muss blockieren');};
$tests['stronger_same_core_keyword_is_flagged_and_requires_justification']=function(){$d=draft_pkg();$d['nodes'][1]['name']='Sauerteig Starter';$d['nodes'][1]['slug']='sauerteig-starter';$d['nodes'][1]['primary_keyword']='sauerteig starter';$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['nodes'][1]['longtail_potential']=['sauerteig selber machen','sauerteig ansetzen','sauerteig füttern','sauerteig pflegen'];$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);assert_true(in_array('DFS_STRONGER_CATEGORY_KEYWORD_CANDIDATE',codes($e['warnings']),true),'Stärkerer Kandidat muss gemeldet werden');assert_true(in_array('DFS_STRONGER_KEYWORD_UNRESOLVED',codes($e['errors']),true),'Ohne Begründung muss final blockieren');$f['nodes'][1]['keyword_choice_justification']='Starter ist bewusst die enger definierte Kategorie; Sauerteig bleibt Parent-/Nachbarintent.';$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);assert_true(!in_array('DFS_STRONGER_KEYWORD_UNRESOLVED',codes($e['errors']),true),'Begründete Auswahl muss diesen Gate schließen');};
$tests['real_dataforseo_longtails_are_accepted']=function(){$d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);assert_true(!in_array('DFS_LONGTAIL_NOT_EVIDENCED',codes($e['errors']),true),'Echte Research-Longtails müssen akzeptiert werden');};
$tests['invented_longtail_is_blocked']=function(){$d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['nodes'][1]['longtail_potential'][3]='erfundener sauerteig longtail xyz';$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);assert_true(in_array('DFS_LONGTAIL_NOT_EVIDENCED',codes($e['errors']),true),'Erfundener Longtail muss blockieren');};
$tests['missing_strong_keyword_core_is_reported_and_requires_decision']=function(){$d=draft_pkg();$r=research_from_draft($d);$extra=make_dfs_item('brotbackofen',6000,'brotbackofen','commercial');$r['cluster_research']['clusters'][0]['items'][]=(new ReflectionClass('APKW_DataForSEO'))?['keyword'=>'brotbackofen','search_volume'=>6000,'monthly_searches'=>[],'cpc'=>2.0,'competition'=>0.5,'competition_level'=>'MEDIUM','main_intent'=>'commercial','foreign_intent'=>[],'core_keyword'=>'brotbackofen','keyword_difficulty'=>30,'detected_language'=>'de','serp_info'=>null,'source_last_updated'=>'2026-08-01']:[];$r['content_sha256']=APKW_Research::canonical_hash($r);$f=final_from_draft($d,$r);$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);assert_true(in_array('DFS_TOP_KEYWORD_GROUP_UNRESOLVED',codes($e['errors']),true),'Starker vergessener Core muss final ungelöst blockieren');$f['keyword_coverage_decisions']=[['cluster_id'=>'brot','core_keyword'=>'brotbackofen','decision'=>'ARTICLE_ONLY','reason'=>'Wird als einzelner Ratgeber statt Kategorie behandelt.']];$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);$unresolved=array_filter($e['errors'],fn($x)=>$x['code']==='DFS_TOP_KEYWORD_GROUP_UNRESOLVED'&&str_contains($x['path'],'brotbackofen'));assert_true(count($unresolved)===0,'Dokumentierte Coverage-Entscheidung muss Core schließen');};
$tests['parent_child_same_core_is_flagged']=function(){$d=draft_pkg();$d['nodes'][0]['primary_keyword']='sauerteig starter';$r=research_from_draft($d);$f=final_from_draft($d,$r);$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);assert_true(in_array('DFS_PARENT_CHILD_SAME_CORE_UNRESOLVED',codes($e['errors']),true)||in_array('PRIMARY_KEYWORD_DUPLICATE_WITHIN_BLOCK',codes($v['errors']),true),'Gleicher Parent/Child-Core darf nicht unbemerkt passieren');};
$tests['cross_cluster_core_overlap_is_detected_globally']=function(){$d=draft_pkg();$r=research_from_draft($d);$r['cluster_research']['clusters'][]=['cluster_id'=>'fermentation','name'=>'Fermentation','scope'=>'Fermente','exclusions'=>[],'seed_keywords'=>['fermentation'],'request_sha256'=>str_repeat('b',64),'result_total_count'=>1,'returned_count'=>1,'items'=>[['keyword'=>'sauerteig fermentation','search_volume'=>500,'main_intent'=>'informational','core_keyword'=>'sauerteig','keyword_difficulty'=>20,'cpc'=>0.5]],'cost_usd'=>0.03,'task_id'=>'x'];$r['content_sha256']=APKW_Research::canonical_hash($r);$f=final_from_draft($d,$r);$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);assert_true(count($e['cross_cluster_overlaps'])>=1,'Clusterübergreifender Core-Overlap muss sichtbar sein');};
$tests['final_content_leaf_requires_at_least_three_longtails']=function(){$d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['nodes'][1]['longtail_potential']=['a','b'];$v=APKW_Validator::validate($f);assert_true(in_array('CONTENT_LEAF_LONGTAILS_INSUFFICIENT',codes($v['errors']),true),'Weniger als drei Longtails müssen blockieren');$f['nodes'][1]['longtail_potential']=['a','b','c'];$v=APKW_Validator::validate($f);assert_true(!in_array('CONTENT_LEAF_LONGTAILS_INSUFFICIENT',codes($v['errors']),true),'Drei eigenständige Longtails müssen die Mengenregel erfüllen');};
$tests['functional_article_direction_can_be_real_leaf_category_with_three_evidenced_longtails']=function(){
    $d=draft_pkg();
    $d['nodes'][1]['is_leaf']=false;$d['nodes'][1]['single_child_justification']='Funktionaler Vertiefungsast wird als eigener tragfähiger Endknoten geprüft.';
    $faq=n('c-faq','content','FAQ zu Sauerteig','faq-zu-sauerteig','sauerteig faq','informational','c-1',3,true);
    $faq['category_name_justification']='Kontextuell eindeutiger sichtbarer Name nach globaler Dublettenregel; Primärkeyword bleibt der belegte FAQ-Core.';
    $d['nodes'][]=$faq;
    $GLOBALS['remote_post_override']=function($url,$args){$payload=json_decode($args['body']??'[]',true);$task=$payload[0]??[];if(str_contains($url,'keyword_overview')){$items=[];foreach($task['keywords']??[] as $kw)$items[]=generic_overview_item($kw);return ['response'=>['code'=>200],'body'=>json_encode(dfs_response($items,0.02),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)];}if(str_starts_with((string)($task['tag']??''),'apkw-global-'))return ['response'=>['code'=>200],'body'=>json_encode(dfs_response(mock_global_items(),0.04),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)];$items=mock_cluster_items();$items[]=make_dfs_item('sauerteig faq',350,'sauerteig faq','informational');$items[]=make_dfs_item('sauerteig faq warum geht er nicht auf',120,'sauerteig faq','informational');$items[]=make_dfs_item('sauerteig faq wie oft füttern',100,'sauerteig faq','informational');$items[]=make_dfs_item('sauerteig faq wie lagern',90,'sauerteig faq','informational');return ['response'=>['code'=>200],'body'=>json_encode(dfs_response($items,0.03),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)];};
    try{$r=research_from_draft($d);}finally{$GLOBALS['remote_post_override']=null;}
    $f=final_from_draft($d,$r);
    foreach($f['nodes'] as &$node){
        if($node['concept_id']==='c-1'){$node['is_leaf']=false;$node['longtail_potential']=[];$node['single_child_justification']='Funktionaler Vertiefungsast wird als eigener tragfähiger Endknoten geprüft.';}
        if($node['concept_id']==='c-faq'){$node['longtail_potential']=['sauerteig faq warum geht er nicht auf','sauerteig faq wie oft füttern','sauerteig faq wie lagern'];$node['category_name_justification']='Kontextuell eindeutiger sichtbarer Name nach globaler Dublettenregel; Primärkeyword bleibt der belegte FAQ-Core.';}
    }unset($node);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true($v['valid'],'Fachthema -> tragfähige FAQ-Kategorie mit drei Longtails muss strukturell PASS sein: '.implode(',',codes($v['errors'])));
    assert_true(!in_array('DFS_LONGTAIL_NOT_EVIDENCED',codes($e['errors']),true)&&!in_array('DFS_LONGTAIL_NOT_BOUND_TO_NODE',codes($e['errors']),true),'Drei providerbelegte FAQ-Longtails müssen node-gebunden akzeptiert werden.');
};
$tests['content_leaf_primary_keywords_are_added_to_same_cluster_research_call_without_extra_call']=function(){
    $d=draft_pkg();$d['nodes'][1]['is_leaf']=false;$d['nodes'][1]['single_child_justification']='Kontrollierter Testast';$d['nodes'][]=n('c-faq','content','FAQ zu Sauerteig','faq-zu-sauerteig','sauerteig faq','informational','c-1',3,true);
    $d=approve_initial($d);$GLOBALS['remote_requests']=[];$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$d=approve_global_gap($d,$g);APKW_Research::build_from_draft($d,$g,'Germany','de',300,false);
    $cluster=[];foreach($GLOBALS['remote_requests'] as $req){if($req['method']!=='POST')continue;$body=json_decode($req['args']['body']??'[]',true);$task=$body[0]??[];if(str_starts_with((string)($task['tag']??''),'apkw-cluster-')){$cluster=$task;break;}}
    assert_true(in_array('sauerteig faq',$cluster['keywords']??[],true),'Primärkeyword der tiefen Content-Endkategorie muss in denselben Cluster-Research-Call aufgenommen werden.');
    $posts=array_values(array_filter($GLOBALS['remote_requests'],fn($x)=>$x['method']==='POST'));
    assert_true(count($posts)===3,'Tiefen-Seed-Erweiterung darf keinen zusätzlichen Paid Call erzeugen: 1 Global + 1 Overview + 1 Cluster.');
};
$tests['repeated_bare_faq_visible_names_remain_global_block_and_require_contextual_names']=function(){
    $p=draft_pkg();$p['nodes'][1]['is_leaf']=false;$p['nodes'][2]['is_leaf']=false;
    $p['nodes'][]=n('c-faq-1','content','FAQ','faq-sauerteig','sauerteig faq','informational','c-1',3,true);
    $p['nodes'][]=n('c-faq-2','content','FAQ','faq-anstellgut','anstellgut faq','informational','c-2',3,true);
    $v=APKW_Validator::validate($p);assert_true(in_array('VISIBLE_NAME_DUPLICATE_GLOBAL',codes($v['errors']),true),'R-046 bleibt hart: wiederholtes sichtbares „FAQ“ muss blockieren; Kontextname ist erforderlich.');
};
$tests['live_exact_visible_name_duplicate_blocks_preview']=function(){$d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$GLOBALS['terms']['category']=[7=>(object)['term_id'=>7,'parent'=>0,'name'=>'Sauerteig','slug'=>'bestehend']];$v=APKW_Validator::validate($f);$c=APKW_Comparator::compare($f,$v);assert_true($c['summary']['CONFLICT']>=1,'Live-Namensdublette muss blockieren');$GLOBALS['terms']=[];};
$tests['no_portal_write_apis_in_source']=function(){$root=dirname(__DIR__);$bad=['wp_insert_term','wp_update_term','wp_delete_term','wp_insert_post','wp_update_post','wp_delete_post','wp_set_object_terms','wp_create_category'];foreach(new RecursiveIteratorIterator(new RecursiveDirectoryIterator($root.'/includes')) as $file){if(!$file->isFile()||$file->getExtension()!=='php')continue;$src=file_get_contents($file->getPathname());foreach($bad as $fn)assert_true(!preg_match('/\b'.preg_quote($fn,'/').'\s*\(/',$src),'Verbotene Schreib-API '.$fn.' in '.$file->getFilename());}};
$tests['glossary_is_optional_auxiliary_not_fourth_required_pillar']=function(){$p=draft_pkg();$v=APKW_Validator::validate($p);assert_true($v['valid'],'Drei Kernsäulen ohne Glossar müssen gültig sein');};
$tests['cluster_seed_limit_over_200_blocks']=function(){$p=draft_pkg();$seeds=[];for($i=0;$i<201;$i++)$seeds[]='keyword '.$i;$p['research_clusters'][0]['seed_keywords']=$seeds;$v=APKW_Validator::validate($p);assert_true(in_array('RESEARCH_CLUSTER_SEEDS_TOO_MANY',codes($v['errors']),true),'Mehr als 200 Seeds müssen blockieren');};


$tests['effective_cluster_seed_overflow_blocks_instead_of_silent_leaf_seed_drop']=function(){
    $p=draft_pkg();$seeds=[];for($i=0;$i<199;$i++)$seeds[]='basis keyword '.$i;$p['research_clusters'][0]['seed_keywords']=$seeds;
    $pf=APKW_Research::preflight_draft($p);
    assert_true(!$pf['valid']&&in_array('CLUSTER_RESEARCH_SEED_OVERFLOW',codes($pf['errors']),true),'199 Basisseeds plus zwei neue Content-Blatt-Primärkeywords müssen blockieren statt Tiefenseeds still zu verwerfen.');
};
$tests['three_way_primary_collision_checks_all_prior_owners']=function(){
    $p=draft_pkg();
    $p['nodes'][0]['primary_keyword']='shared keyword';$p['nodes'][0]['search_intent']='informational';
    $p['nodes'][3]['primary_keyword']='shared keyword';$p['nodes'][3]['search_intent']='transactional';
    $p['nodes'][6]['primary_keyword']='shared keyword';$p['nodes'][6]['search_intent']='transactional';
    $v=APKW_Validator::validate($p);
    assert_true(in_array('PRIMARY_KEYWORD_CROSS_PILLAR_SAME_INTENT',codes($v['errors']),true),'Dritter Owner muss auch gegen zweiten Owner geprüft werden.');
};
$tests['weaker_visible_category_name_requires_final_justification']=function(){
    $d=draft_pkg();
    $d['nodes'][1]['name']='Sauerteig Starter';$d['nodes'][1]['slug']='sauerteig-starter';$d['nodes'][1]['primary_keyword']='sauerteig';
    $r=research_from_draft($d);$f=final_from_draft($d,$r);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(in_array('DFS_CATEGORY_NAME_CHOICE_UNRESOLVED',codes($e['errors']),true),'Schwächerer sichtbarer Kategoriename muss final begründet werden.');
    foreach($f['nodes'] as &$node)if($node['concept_id']==='c-1')$node['category_name_justification']='Lesbare sichtbare Bezeichnung; Primärkeyword bleibt Sauerteig.';unset($node);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(!in_array('DFS_CATEGORY_NAME_CHOICE_UNRESOLVED',codes($e['errors']),true),'Explizite Namensbegründung muss den Namensentscheid schließen.');
};
$tests['declared_intent_mismatch_requires_final_justification']=function(){
    $d=draft_pkg();$d['nodes'][1]['search_intent']='commercial';
    $r=research_from_draft($d);$f=final_from_draft($d,$r);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(in_array('DFS_INTENT_MISMATCH_UNRESOLVED',codes($e['errors']),true),'DataForSEO-Intentabweichung darf final nicht unbemerkt bleiben.');
    foreach($f['nodes'] as &$node)if($node['concept_id']==='c-1')$node['intent_justification']='Portalrolle ist bewusst kommerziell beratend, obwohl DataForSEO informational meldet.';unset($node);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(!in_array('DFS_INTENT_MISMATCH_UNRESOLVED',codes($e['errors']),true),'Begründete Intentabweichung muss zulässig sein.');
};
$tests['longtail_must_be_evidenced_and_bound_to_its_content_node']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);
    $f['nodes'][1]['longtail_potential'][3]='anstellgut auffrischen';
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(!in_array('DFS_LONGTAIL_NOT_EVIDENCED',codes($e['errors']),true),'Testkeyword existiert im Cluster und darf nicht als unbelegt gelten.');
    assert_true(in_array('LONGTAIL_DUPLICATE_OWNERSHIP',codes($v['errors']),true)||in_array('DFS_LONGTAIL_NOT_BOUND_TO_NODE',codes($e['errors']),true),'Fremd gebundener Longtail muss durch Eigentums- oder Bindungsgate blockieren.');
};
$tests['low_relevance_zero_volume_cluster_core_does_not_consume_finite_review_gate']=function(){
    $d=draft_pkg();$r=research_from_draft($d);
    for($i=1;$i<=20;$i++)$r['cluster_research']['clusters'][0]['items'][]=['provider_rank'=>50+$i,'keyword'=>'filler cluster '.$i,'search_volume'=>10+$i,'main_intent'=>'informational','core_keyword'=>'filler cluster '.$i,'keyword_difficulty'=>1,'cpc'=>0];
    $r['cluster_research']['clusters'][0]['items'][]=['provider_rank'=>999,'keyword'=>'irrelevanter nullbegriff','search_volume'=>0,'main_intent'=>'informational','core_keyword'=>'irrelevanter nullbegriff','keyword_difficulty'=>1,'cpc'=>0];
    $r['content_sha256']=APKW_Research::canonical_hash($r);$f=final_from_draft($d,$r);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    $hits=array_filter($e['errors'],fn($x)=>$x['code']==='DFS_TOP_KEYWORD_GROUP_UNRESOLVED'&&str_contains($x['path'],'irrelevanter nullbegriff'));
    assert_true(count($hits)===0,'Ein weder volumenstarker noch provider-relevanter Nullvolumen-Core darf das finite Cluster-Review-Gate nicht verbrauchen.');
};
$tests['final_read_only_validation_path_makes_no_dataforseo_request']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$GLOBALS['remote_requests']=[];
    $v=APKW_Validator::validate($f);APKW_ResearchEvidence::analyze($f,$r,$v);APKW_Comparator::compare($f,$v);
    assert_true(count($GLOBALS['remote_requests'])===0,'Finale read-only Prüfung darf keine externe DataForSEO-Anfrage auslösen.');
};
$tests['keyword_ideas_request_uses_documented_bounded_sorting']=function(){
    $GLOBALS['remote_requests']=[];APKW_DataForSEO::keyword_ideas(['sauerteig','brot'],'Germany','de',300,false,'test');
    $req=$GLOBALS['remote_requests'][0]??null;assert_true(is_array($req),'Request fehlt');
    $body=json_decode($req['args']['body']??'[]',true);$task=$body[0]??[];
    assert_true(($task['keywords']??[])===['sauerteig','brot'],'Nur deklarierte Seeds erwartet');
    assert_true(($task['limit']??0)===300,'Limit muss gebunden bleiben');
    assert_true(($task['order_by']??[])===['relevance,desc','keyword_info.search_volume,desc'],'Dokumentiertes DataForSEO-order_by erwartet');
    assert_true(($task['closely_variants']??null)===false,'Broad-Match-Modus muss explizit bleiben');assert_true(($task['ignore_synonyms']??null)===false,'Synonyme müssen für bessere Namenskandidaten sichtbar bleiben');
};
$tests['keyword_overview_rejects_more_than_700_before_remote_call']=function(){
    $keywords=[];for($i=0;$i<701;$i++)$keywords[]='keyword '.$i;$GLOBALS['remote_requests']=[];
    try{APKW_DataForSEO::keyword_overview($keywords,'Germany','de');throw new RuntimeException('701 Keywords hätten blockieren müssen');}
    catch(RuntimeException $e){assert_true(str_contains($e->getMessage(),'maximal 700'),'Falsche 700er Fehlermeldung');}
    assert_true(count($GLOBALS['remote_requests'])===0,'Überlimit muss vor externem Request blockieren');
};
$tests['taxonomy_target_slug_collision_is_global_within_taxonomy']=function(){
    $p=draft_pkg();
    $p['nodes'][]=n('g-1','glossary','Sauerteig Begriff','sauerteig','sauerteig begriff','informational',null,1,true,'brot');
    $v=APKW_Validator::validate($p);
    assert_true(in_array('PACKAGE_TARGET_SLUG_COLLISION',codes($v['errors']),true),'Gleicher Taxonomie-Slug darf auch blockübergreifend/in anderer Hierarchie nicht kollidieren.');
};
$tests['optional_justification_fields_must_be_text']=function(){
    $p=draft_pkg();$p['nodes'][1]['category_name_justification']=['not','text'];$v=APKW_Validator::validate($p);
    assert_true(in_array('NODE_OPTIONAL_TEXT_INVALID',codes($v['errors']),true),'Begründungsfelder müssen Text sein.');
};


$tests['final_research_scope_cannot_change_without_new_research']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);
    assert_true(APKW_Research::verify_binding($f,$r)['valid'],'Unveränderter Research-Scope muss binden.');
    $f['research_clusters'][0]['seed_keywords'][]='pizzaofen';
    $bv=APKW_Research::verify_binding($f,$r);
    assert_true(!$bv['valid']&&in_array('RESEARCH_BINDING_SCOPE_MISMATCH',$bv['errors'],true),'Neue Seeds/Scope benötigen neuen Research-Lauf.');
};
$tests['corrected_primary_keyword_from_bound_cluster_is_valid_evidence']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);
    foreach($f['nodes'] as &$node){
        if($node['concept_id']==='c-1'){
            $node['name']='Sauerteig ansetzen';$node['slug']='sauerteig-ansetzen';$node['primary_keyword']='sauerteig ansetzen';
            $node['longtail_potential']=['sauerteig selber machen','sauerteig füttern','sauerteig pflegen','sauerteig starter'];
            $node['category_name_justification']='DataForSEO-Kandidat aus dem gebundenen Cluster; fachlich als eigenständige Kategorie gewählt.';
        }
    }unset($node);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(!in_array('DFS_PRIMARY_KEYWORD_UNRESOLVED',codes($e['errors']),true),'Exakter Keyword-Ideas-Treffer aus gebundenem Cluster muss als Beleg für Korrekturlauf gelten.');
    $row=array_values(array_filter($e['nodes'],fn($x)=>$x['concept_id']==='c-1'))[0]??[];
    assert_true(($row['primary_evidence_source']??'')==='KEYWORD_IDEAS_EXACT','Korrekturbeleg muss als KEYWORD_IDEAS_EXACT ausgewiesen werden.');
};
$tests['research_package_scope_hash_detects_tampering_even_if_outer_hash_recomputed']=function(){
    $r=research_from_draft(draft_pkg());
    $r['source_draft']['package']['research_clusters'][0]['seed_keywords'][]='fremdseed';
    $r['content_sha256']=APKW_Research::canonical_hash($r);
    $v=APKW_Research::verify_package($r);
    assert_true(!$v['valid']&&in_array('RESEARCH_SCOPE_HASH_MISMATCH',$v['errors'],true),'Research-Scope-Hash muss Scope-Manipulation erkennen.');
};


$tests['similar_cross_pillar_core_with_same_coarse_intent_can_pass_when_function_is_justified']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);
    foreach($f['nodes'] as &$node){
        if($node['concept_id']==='c-1'){$node['overlap_justification']='Evergreen-Grundlagen und systematische Anleitung im Content.';$node['longtail_potential']=['sauerteig ansetzen','sauerteig füttern','sauerteig pflegen','sauerteig starter'];}
        if($node['concept_id']==='j-1'){
            $node['name']='Sauerteig selber machen';$node['slug']='sauerteig-selber-machen';$node['primary_keyword']='sauerteig selber machen';$node['search_intent']='informational';
            $node['overlap_justification']='Journal behandelt Geschichten, Experimente und aktuelle Praxis statt Evergreen-Grundlagen.';
        }
    }unset($node);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(!in_array('DFS_CORE_CROSS_PILLAR_SAME_INTENT',codes($e['errors']),true),'Grober gleicher DataForSEO-Intent darf eine begründete säulengetrennte Nutzung nicht pauschal blockieren.');
    assert_true(!in_array('DFS_CORE_CROSS_PILLAR_JUSTIFICATION_MISSING',codes($e['errors']),true),'Begründete funktionale Trennung muss Cross-Pillar-Core schließen.');
    assert_true(in_array('DFS_CORE_CROSS_PILLAR_SAME_COARSE_INTENT_REVIEW',codes($e['warnings']),true),'Gleicher grober Intent muss trotzdem als Review sichtbar bleiben.');
};



$tests['free_connection_test_blocks_unexpected_nonzero_cost']=function(){
    $GLOBALS['remote_get_override']=['response'=>['code'=>200],'body'=>json_encode(['version'=>'0.1','status_code'=>20000,'status_message'=>'Ok.','cost'=>0.01,'tasks'=>[]])];
    try{APKW_DataForSEO::test_connection();throw new RuntimeException('Nicht-null Kosten hätten blockieren müssen.');}
    catch(RuntimeException $e){assert_true(str_contains($e->getMessage(),'unerwartete Kosten'),'Falsche Kosten-Anomalie-Meldung.');}
    $GLOBALS['remote_get_override']=null;
};
$tests['malformed_dataforseo_json_blocks']=function(){
    $GLOBALS['remote_post_override']=['response'=>['code'=>200],'body'=>'not-json'];
    try{APKW_DataForSEO::keyword_ideas(['brot'],'Germany','de');throw new RuntimeException('Ungültiges JSON hätte blockieren müssen.');}
    catch(RuntimeException $e){assert_true(str_contains($e->getMessage(),'kein gültiges JSON'),'Ungültiges Provider-JSON muss konkret blockieren.');}
    $GLOBALS['remote_post_override']=null;
};
$tests['dataforseo_top_level_status_failure_blocks']=function(){
    $GLOBALS['remote_post_override']=['response'=>['code'=>200],'body'=>json_encode(['status_code'=>50000,'status_message'=>'Provider failed','cost'=>0])];
    try{APKW_DataForSEO::keyword_ideas(['brot'],'Germany','de');throw new RuntimeException('Provider-Statusfehler hätte blockieren müssen.');}
    catch(RuntimeException $e){assert_true(str_contains($e->getMessage(),'Provider failed'),'Top-Level-Providerfehler muss weitergereicht werden.');}
    $GLOBALS['remote_post_override']=null;
};
$tests['dataforseo_task_status_failure_blocks']=function(){
    $GLOBALS['remote_post_override']=['response'=>['code'=>200],'body'=>json_encode(['status_code'=>20000,'status_message'=>'Ok.','cost'=>0,'tasks'=>[['id'=>'x','status_code'=>40000,'status_message'=>'Task failed','cost'=>0,'result'=>[]]]])];
    try{APKW_DataForSEO::keyword_ideas(['brot'],'Germany','de');throw new RuntimeException('Task-Statusfehler hätte blockieren müssen.');}
    catch(RuntimeException $e){assert_true(str_contains($e->getMessage(),'Task failed'),'Taskfehler muss konkret blockieren.');}
    $GLOBALS['remote_post_override']=null;
};
$tests['admin_source_has_capability_nonces_and_safe_json_embedding']=function(){
    $src=file_get_contents(dirname(__DIR__).'/includes/class-apkw-admin.php');
    assert_true(str_contains($src,"current_user_can('manage_options')"),'Admin muss Capability prüfen.');
    assert_true(str_contains($src,'check_admin_referer'),'Admin-Aktionen müssen Nonces prüfen.');
    assert_true(str_contains($src,'JSON_HEX_TAG|JSON_HEX_AMP|JSON_HEX_APOS|JSON_HEX_QUOT'),'Report-Einbettung muss Script-Breakout härten.');
};

$tests['end_to_end_valid_final_passes_all_local_gates']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);
    $rv=APKW_Research::verify_package($r);$bv=APKW_Research::verify_binding($f,$r);$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);$c=APKW_Comparator::compare($f,$v);
    assert_true($rv['valid'],'Research-Verifikation muss PASS sein');
    assert_true($bv['valid'],'Research-Bindung muss PASS sein');
    assert_true($v['valid'],'Finales Schema/Workflow muss PASS sein: '.implode(',',codes($v['errors'])));
    assert_true($e['valid'],'DataForSEO-Evidenz muss PASS sein: '.implode(',',codes($e['errors'])));
    assert_true($c['status']==='PASS_READ_ONLY_PREVIEW','Live-Vorschau muss lokal PASS sein');
};



$tests['project_discovery_seeds_are_required']=function(){
    $p=draft_pkg();unset($p['project']['discovery_seed_keywords']);$v=APKW_Validator::validate($p);
    assert_true(in_array('PROJECT_DISCOVERY_SEEDS_MISSING',codes($v['errors']),true),'Projektweite Discovery-Seeds müssen Pflicht sein.');
};
$tests['single_project_discovery_seed_is_allowed_with_review_warning']=function(){
    $p=draft_pkg();$p['project']['discovery_seed_keywords']=['genuss handwerk'];$v=APKW_Validator::validate($p);
    assert_true($v['valid'],'Ein fachlich sinnvoller Discovery-Seed darf nicht durch eine willkürliche Mindestanzahl blockiert werden.');
    assert_true(in_array('PROJECT_DISCOVERY_SEEDS_NARROW_REVIEW',codes($v['warnings']),true),'Ein einzelner Seed soll als Coverage-Review-Hinweis sichtbar bleiben.');
};
$tests['empty_project_discovery_seed_list_blocks']=function(){
    $p=draft_pkg();$p['project']['discovery_seed_keywords']=[];$v=APKW_Validator::validate($p);
    assert_true(in_array('PROJECT_DISCOVERY_SEEDS_MISSING',codes($v['errors']),true),'Ohne Discovery-Seed kann die projektweite Coverage nicht geprüft werden.');
};
$tests['global_discovery_request_uses_only_declared_project_seeds']=function(){
    $d=draft_pkg();$GLOBALS['remote_requests']=[];$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$d=approve_global_gap($d,$g);APKW_Research::build_from_draft($d,$g,'Germany','de',300,false);
    $global=null;foreach($GLOBALS['remote_requests'] as $req){if($req['method']!=='POST')continue;$body=json_decode($req['args']['body']??'[]',true);$task=$body[0]??[];if(str_starts_with((string)($task['tag']??''),'apkw-global-')){$global=$task;break;}}
    assert_true(is_array($global),'Global-Discovery-Request fehlt.');
    assert_true(($global['keywords']??[])===$d['project']['discovery_seed_keywords'],'Global Discovery darf nur deklarierte Projekt-Seeds verwenden.');
    assert_true(!in_array($d['project']['name'],$global['keywords']??[],true),'Projektname darf nicht heimlich als Seed ergänzt werden.');
};
$tests['global_discovery_is_exactly_one_call_per_research_run']=function(){
    $d=draft_pkg();$d['research_clusters'][]=cluster('fermentation',['fermentation','kimchi']);foreach($d['nodes'] as &$n){if(in_array($n['concept_id'],['j-root','j-1','j-2'],true))$n['research_cluster_id']='fermentation';}unset($n);$d=approve_initial($d);
    $GLOBALS['remote_requests']=[];$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$d=approve_global_gap($d,$g);APKW_Research::build_from_draft($d,$g,'Germany','de',300,false);$count=0;
    foreach($GLOBALS['remote_requests'] as $req){if($req['method']!=='POST')continue;$body=json_decode($req['args']['body']??'[]',true);if(str_starts_with((string)($body[0]['tag']??''),'apkw-global-'))$count++;}
    assert_true($count===1,'Pro Research-Lauf ist exakt ein projektweiter Global-Coverage-Call vorgesehen.');
};
$tests['global_core_similarity_without_explicit_decision_blocks']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);unset($f['global_coverage_decisions']);$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(in_array('DFS_GLOBAL_TOPIC_GAP_UNRESOLVED',codes($e['errors']),true),'Keyword-Ähnlichkeit allein darf einen globalen Fund nicht fachlich freigeben.');
};
$tests['missing_high_volume_global_main_topic_blocks_final']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$r['global_discovery']['items'][]=['keyword'=>'pizza selber machen','search_volume'=>9000,'main_intent'=>'informational','core_keyword'=>'pizza','keyword_difficulty'=>30,'cpc'=>1.2];$r['content_sha256']=APKW_Research::canonical_hash($r);
    $f=final_from_draft($d,$r);$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(in_array('DFS_GLOBAL_TOPIC_GAP_UNRESOLVED',codes($e['errors']),true),'Starkes globales Themenfeld ohne Cluster muss final blockieren.');
};
$tests['explicit_out_of_scope_decision_resolves_global_gap']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$r['global_discovery']['items'][]=['keyword'=>'pizza selber machen','search_volume'=>9000,'main_intent'=>'informational','core_keyword'=>'pizza','keyword_difficulty'=>30,'cpc'=>1.2];$r['content_sha256']=APKW_Research::canonical_hash($r);
    $f=final_from_draft($d,$r);$f['global_coverage_decisions'][]=['core_keyword'=>'pizza','decision'=>'OUT_OF_SCOPE','reason'=>'Bewusst außerhalb des fachlich festgelegten Portalumfangs.'];$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(!in_array('DFS_GLOBAL_TOPIC_GAP_UNRESOLVED',codes($e['errors']),true),'Explizite zulässige Global-Coverage-Entscheidung muss den Gap schließen.');
};
$tests['invalid_global_coverage_decision_blocks_schema']=function(){
    $p=draft_pkg();$p['global_coverage_decisions']=[['core_keyword'=>'pizza','decision'=>'IGNORE','reason'=>'nein']];$v=APKW_Validator::validate($p);
    assert_true(in_array('GLOBAL_COVERAGE_DECISION_VALUE_INVALID',codes($v['errors']),true),'Ungültige Global-Coverage-Entscheidung muss blockieren.');
};
$tests['changing_project_discovery_seeds_after_research_breaks_binding']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['project']['discovery_seed_keywords'][]='pizza selber machen';$bv=APKW_Research::verify_binding($f,$r);
    assert_true(!$bv['valid']&&in_array('RESEARCH_BINDING_SCOPE_MISMATCH',$bv['errors'],true),'Projektweite Discovery-Seeds dürfen nach Research nicht still verändert werden.');
};
$tests['v13_node_contract_remains_compatible_without_new_required_function_field']=function(){
    $p=draft_pkg();$v=APKW_Validator::validate($p);
    assert_true($v['valid'],'DataForSEO-Gate darf den bestehenden V1.3-Knotenvertrag nicht unnötig um ein neues Pflichtfeld erweitern.');
};
$tests['same_core_cross_pillar_is_not_auto_blocked_when_names_and_pillar_roles_differ']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);
    foreach($f['nodes'] as &$node){
        if($node['concept_id']==='c-1'){$node['longtail_potential']=['sauerteig ansetzen','sauerteig füttern','sauerteig pflegen','sauerteig starter'];$node['overlap_justification']='Content liefert Evergreen-Grundlagen.';}
        if($node['concept_id']==='j-1'){$node['name']='Sauerteig selber machen';$node['slug']='sauerteig-selber-machen';$node['primary_keyword']='sauerteig selber machen';$node['overlap_justification']='Journal liefert redaktionelle Experimente und Praxisbeobachtungen.';}
    }unset($node);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(!in_array('DFS_CORE_CROSS_PILLAR_JUSTIFICATION_MISSING',codes($e['errors']),true),'Begründete, unterschiedlich benannte Säulenrollen dürfen bei gleichem Core bestehen bleiben.');
};
$tests['duplicate_longtail_ownership_between_content_nodes_blocks']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['nodes'][2]['longtail_potential'][0]='sauerteig ansetzen';$v=APKW_Validator::validate($f);
    assert_true(in_array('LONGTAIL_DUPLICATE_OWNERSHIP',codes($v['errors']),true),'Ein Longtail darf nicht zwei Content-Knoten gehören.');
};
$tests['longtail_cannot_equal_another_nodes_primary_keyword']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['nodes'][1]['longtail_potential'][0]='anstellgut';$v=APKW_Validator::validate($f);
    assert_true(in_array('LONGTAIL_COLLIDES_WITH_PRIMARY_KEYWORD',codes($v['errors']),true),'Longtail darf nicht Primärkeyword eines anderen Knotens sein.');
};
$tests['low_relevance_zero_volume_global_core_does_not_consume_finite_review_gate']=function(){
    $d=draft_pkg();$r=research_from_draft($d);
    for($i=1;$i<=25;$i++)$r['global_discovery']['items'][]=['provider_rank'=>50+$i,'keyword'=>'filler global '.$i,'search_volume'=>20+$i,'main_intent'=>'informational','core_keyword'=>'filler global '.$i,'keyword_difficulty'=>1,'cpc'=>0];
    $r['global_discovery']['items'][]=['provider_rank'=>999,'keyword'=>'nullthema','search_volume'=>0,'main_intent'=>'informational','core_keyword'=>'nullthema','keyword_difficulty'=>1,'cpc'=>0];$r['content_sha256']=APKW_Research::canonical_hash($r);
    $f=final_from_draft($d,$r);$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);$hits=array_filter($e['errors'],fn($x)=>$x['code']==='DFS_GLOBAL_TOPIC_GAP_UNRESOLVED'&&str_contains($x['path'],'nullthema'));
    assert_true(count($hits)===0,'Ein weder volumenstarker noch provider-relevanter Nullvolumen-Core darf das finite Global-Review-Gate nicht verbrauchen.');
};
$tests['research_package_requires_global_discovery_section']=function(){
    $r=research_from_draft(draft_pkg());unset($r['global_discovery']);$r['content_sha256']=APKW_Research::canonical_hash($r);$v=APKW_Research::verify_package($r);
    assert_true(!$v['valid']&&in_array('RESEARCH_GLOBAL_DISCOVERY_MISSING',$v['errors'],true),'Research-Paket ohne Global Discovery muss blockieren.');
};
$tests['tampering_global_discovery_without_rehash_is_detected']=function(){
    $r=research_from_draft(draft_pkg());$r['global_discovery']['items'][0]['search_volume']=999999;$v=APKW_Research::verify_package($r);
    assert_true(!$v['valid']&&in_array('RESEARCH_CONTENT_HASH_MISMATCH',$v['errors'],true),'Manipulation globaler Evidenz muss am Paket-Hash scheitern.');
};
$tests['global_limit_is_bounded_to_dataforseo_maximum']=function(){
    $d=draft_pkg();$GLOBALS['remote_requests']=[];APKW_Research::build_global_coverage($d,'Germany','de',5000,false);$limit=null;
    foreach($GLOBALS['remote_requests'] as $req){if($req['method']!=='POST')continue;$body=json_decode($req['args']['body']??'[]',true);$task=$body[0]??[];if(str_starts_with((string)($task['tag']??''),'apkw-global-')){$limit=$task['limit']??null;break;}}
    assert_true($limit===1000,'Global Discovery muss selbst bei zu großem Eingabewert auf 1000 begrenzt werden.');
};



$tests['global_stage_is_one_paid_call_only']=function(){
    $d=draft_pkg();$GLOBALS['remote_requests']=[];$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);
    $posts=array_values(array_filter($GLOBALS['remote_requests'],fn($x)=>$x['method']==='POST'));
    assert_true(count($posts)===1,'Global-Stufe darf genau einen Paid-Request ausführen.');
    assert_true(($g['research_summary']['paid_calls_this_stage']??0)===1,'Global-Paket muss genau 1 Call ausweisen.');
    $body=json_decode($posts[0]['args']['body']??'[]',true);assert_true(str_starts_with((string)($body[0]['tag']??''),'apkw-global-'),'Global-Stufe darf nur Global Keyword Ideas ausführen.');
};
$tests['detail_stage_reuses_global_and_makes_zero_global_calls']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$d=approve_global_gap($d,$g);$GLOBALS['remote_requests']=[];$r=APKW_Research::build_from_draft($d,$g,'Germany','de',300,false);
    $global_calls=0;foreach($GLOBALS['remote_requests'] as $req){if($req['method']!=='POST')continue;$body=json_decode($req['args']['body']??'[]',true);if(str_starts_with((string)($body[0]['tag']??''),'apkw-global-'))$global_calls++;}
    assert_true($global_calls===0,'Detail-Stufe darf Global-Coverage nicht erneut bezahlen.');
    assert_true(($r['research_summary']['global_discovery_calls_this_stage']??-1)===0,'Research-Paket muss 0 Global-Calls in der Detailstufe ausweisen.');
};
$tests['main_topic_cluster_correction_after_global_is_allowed_without_new_global_call']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);
    $d['research_clusters'][]=cluster('fermentation',['fermentation','kimchi']);foreach($d['nodes'] as &$n){if(in_array($n['concept_id'],['j-root','j-1','j-2'],true))$n['research_cluster_id']='fermentation';}unset($n);$d=approve_global_gap($d,$g);
    $gb=APKW_Research::verify_global_binding($d,$g);assert_true($gb['valid'],'Korrigierte Hauptthemen/Cluster müssen bei unverändertem Projektscope dieselbe Global-Coverage wiederverwenden dürfen.');
    $GLOBALS['remote_requests']=[];$r=APKW_Research::build_from_draft($d,$g,'Germany','de',300,false);$global_calls=0;foreach($GLOBALS['remote_requests'] as $req){if($req['method']!=='POST')continue;$body=json_decode($req['args']['body']??'[]',true);if(str_starts_with((string)($body[0]['tag']??''),'apkw-global-'))$global_calls++;}
    assert_true($global_calls===0&&($r['cluster_research']['cluster_count']??0)===2,'Neue/angepasste Cluster müssen ohne erneuten Global-Call tief recherchiert werden.');
};
$tests['changing_project_scope_after_global_requires_new_global_coverage']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$d['project']['scope'].=' plus Restaurants';$gb=APKW_Research::verify_global_binding($d,$g);
    assert_true(!$gb['valid']&&in_array('GLOBAL_COVERAGE_PROJECT_SCOPE_MISMATCH',$gb['errors'],true),'Echte Projektscope-Änderung muss neue Global-Coverage verlangen.');
};
$tests['changing_global_discovery_seeds_after_global_requires_new_global_coverage']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$d['project']['discovery_seed_keywords'][]='restaurants';$gb=APKW_Research::verify_global_binding($d,$g);
    assert_true(!$gb['valid']&&in_array('GLOBAL_COVERAGE_PROJECT_SCOPE_MISMATCH',$gb['errors'],true),'Discovery-Seed-Änderung muss neue Global-Coverage verlangen.');
};
$tests['detail_research_embeds_and_verifies_bound_global_package']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$d=approve_global_gap($d,$g);$r=APKW_Research::build_from_draft($d,$g,'Germany','de',300,false);$v=APKW_Research::verify_package($r);
    assert_true($v['valid'],'Detail-Research muss eingebettete Global-Coverage vollständig verifizieren.');
    $r['global_coverage_package']['global_discovery']['items'][0]['search_volume']=123456;$r['content_sha256']=APKW_Research::canonical_hash($r);$v2=APKW_Research::verify_package($r);
    assert_true(!$v2['valid']&&in_array('RESEARCH_EMBEDDED_GLOBAL_COVERAGE_CONTENT_HASH_MISMATCH',$v2['errors'],true),'Manipuliertes eingebettetes Global-Paket muss trotz neuem äußeren Hash blockieren.');
};
$tests['detail_preflight_blocks_when_global_provider_returns_no_reviewable_evidence']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$g['global_discovery']['items']=[];$g['content_sha256']=APKW_Research::canonical_hash($g);
    $GLOBALS['remote_requests']=[];$pf=APKW_Research::preflight_detail($d,$g);
    assert_true(!$pf['valid']&&in_array('GLOBAL_COVERAGE_NO_REVIEW_GROUPS',codes($pf['errors']),true),'Leere Global-Coverage muss fail-closed blockieren.');
    assert_true(count($GLOBALS['remote_requests'])===0,'Fail-closed Vorprüfung darf keinen Paid-Detailrequest auslösen.');
};
$tests['detail_preflight_blocks_unresolved_global_gap_before_any_paid_detail_request']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);
    array_unshift($g['global_discovery']['items'],['provider_rank'=>1,'keyword'=>'pizzaofen','search_volume'=>3000,'main_intent'=>'commercial','core_keyword'=>'pizzaofen','keyword_difficulty'=>20,'cpc'=>1.2]);
    $g['content_sha256']=APKW_Research::canonical_hash($g);
    $GLOBALS['remote_requests']=[];$pf=APKW_Research::preflight_detail($d,$g);
    assert_true(!$pf['valid']&&in_array('GLOBAL_COVERAGE_CORE_UNRESOLVED',codes($pf['errors']),true),'Ungeklärtes globales Themenfeld muss die kostenfreie Detail-Vorprüfung blockieren.');
    assert_true(count($GLOBALS['remote_requests'])===0,'Blockierte Detail-Vorprüfung darf keinen Paid-Request auslösen.');
};
$tests['global_gap_can_be_resolved_as_main_topic_with_valid_root_owner']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);
    array_unshift($g['global_discovery']['items'],['provider_rank'=>1,'keyword'=>'pizzaofen','search_volume'=>3000,'main_intent'=>'commercial','core_keyword'=>'pizzaofen','keyword_difficulty'=>20,'cpc'=>1.2]);$g['content_sha256']=APKW_Research::canonical_hash($g);
    $d['global_coverage_decisions'][]=['core_keyword'=>'pizzaofen','decision'=>'MAIN_TOPIC','target_cluster_id'=>'brot','owner_concept_id'=>'c-root','reason'=>'Fachlich dem bestehenden Root-Cluster als Hauptthemenentscheidung zugeordnet.'];$d=approve_global_gap($d,$g);
    $pf=APKW_Research::preflight_detail($d,$g);assert_true($pf['valid'],'Gültige MAIN_TOPIC-Entscheidung mit Root-Owner muss das Gate schließen.');
};
$tests['global_gap_main_topic_owner_must_be_root_and_cluster_consistent']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);
    array_unshift($g['global_discovery']['items'],['provider_rank'=>1,'keyword'=>'pizzaofen','search_volume'=>3000,'main_intent'=>'commercial','core_keyword'=>'pizzaofen','keyword_difficulty'=>20,'cpc'=>1.2]);$g['content_sha256']=APKW_Research::canonical_hash($g);
    $d['global_coverage_decisions'][]=['core_keyword'=>'pizzaofen','decision'=>'MAIN_TOPIC','target_cluster_id'=>'brot','owner_concept_id'=>'c-1','reason'=>'Absichtlicher Negativtest.'];
    $pf=APKW_Research::preflight_detail($d,$g);assert_true(!$pf['valid']&&in_array('GLOBAL_COVERAGE_MAIN_TOPIC_OWNER_NOT_ROOT',codes($pf['errors']),true),'MAIN_TOPIC darf nicht auf Unterknoten zeigen.');
};
$tests['global_gap_subtopic_and_article_only_decisions_are_supported']=function(){
    foreach([
        ['decision'=>'SUBTOPIC','target_cluster_id'=>'brot','owner_concept_id'=>'c-1'],
        ['decision'=>'ARTICLE_ONLY','target_cluster_id'=>'brot']
    ] as $choice){
        $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);array_unshift($g['global_discovery']['items'],['provider_rank'=>1,'keyword'=>'pizzaofen','search_volume'=>3000,'main_intent'=>'commercial','core_keyword'=>'pizzaofen','keyword_difficulty'=>20,'cpc'=>1.2]);$g['content_sha256']=APKW_Research::canonical_hash($g);
        $d['global_coverage_decisions'][]=['core_keyword'=>'pizzaofen','reason'=>'Fachliche Coverage-Entscheidung.']+$choice;$d=approve_global_gap($d,$g);
        $pf=APKW_Research::preflight_detail($d,$g);assert_true($pf['valid'],$choice['decision'].' muss als dokumentierte Coverage-Entscheidung unterstützt werden.');
    }
};
$tests['provider_relevance_can_surface_zero_volume_global_gap']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);
    array_unshift($g['global_discovery']['items'],['provider_rank'=>1,'keyword'=>'relevantes randthema','search_volume'=>0,'main_intent'=>'informational','core_keyword'=>'relevantes randthema','keyword_difficulty'=>5,'cpc'=>0]);$g['content_sha256']=APKW_Research::canonical_hash($g);
    $pf=APKW_Research::preflight_detail($d,$g);
    assert_true(!$pf['valid']&&in_array('GLOBAL_COVERAGE_CORE_UNRESOLVED',codes($pf['errors']),true),'Top-Provider-Relevanz muss als Vollständigkeitssignal sichtbar bleiben, auch ohne starres Mindestvolumen.');
};
$tests['cluster_coverage_uses_provider_relevance_in_addition_to_volume']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);
    array_unshift($r['cluster_research']['clusters'][0]['items'],['provider_rank'=>1,'keyword'=>'fermentiertes brot spezial','search_volume'=>0,'main_intent'=>'informational','core_keyword'=>'fermentiertes brot spezial','keyword_difficulty'=>5,'cpc'=>0]);$r['content_sha256']=APKW_Research::canonical_hash($r);
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    $hits=array_filter($e['errors'],fn($x)=>$x['code']==='DFS_TOP_KEYWORD_GROUP_UNRESOLVED'&&str_contains($x['path'],'fermentiertes brot spezial'));
    assert_true(count($hits)===1,'Cluster-Coverage muss auch provider-relevante Keywordgruppen prüfen und darf nicht nur nach Suchvolumen sortieren.');
};
$tests['admin_detail_preflight_uses_global_coverage_gate_before_paid_button']=function(){
    $src=file_get_contents(dirname(__DIR__).'/includes/class-apkw-admin.php');
    assert_true(str_contains($src,'APKW_Research::preflight_detail($draft,$global)'),'Admin muss das vollständige Global-Coverage-Gate in der kostenfreien Detail-Vorprüfung ausführen.');
};
$tests['schema_files_match_runtime_schema_version_1_4']=function(){
    foreach(['schema-category-v1.4.json','schema-research-v1.4.json'] as $file){$d=json_decode(file_get_contents(dirname(__DIR__).'/'.$file),true);assert_true(is_array($d),'Schema JSON ungültig: '.$file);assert_true(($d['properties']['schema_version']['const']??null)==='1.4','Schema-Datei und Runtime-Version müssen 1.4 entsprechen: '.$file);}
};
$tests['admin_source_exposes_two_stage_paid_flow_not_combined_run']=function(){
    $src=file_get_contents(dirname(__DIR__).'/includes/class-apkw-admin.php');
    assert_true(str_contains($src,'apkw_run_global_coverage')&&str_contains($src,'apkw_run_detail_research'),'Admin muss getrennte Global- und Detailstufe anbieten.');
    assert_true(!str_contains($src,'apkw_run_bounded_research'),'Alte kombinierte Paid-Route darf nicht mehr aktiv sein.');
    assert_true(str_contains($src,'0 erneute Global-Coverage'),'UI muss kostenrelevante Wiederverwendung der Global-Coverage klar zeigen.');
};


$tests['final_approved_requires_visible_sight_review_receipt']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['mode']='FINAL_APPROVED';
    $v=APKW_Validator::validate($f);
    assert_true(!$v['valid']&&in_array('HUMAN_SIGHT_REVIEW_MISSING',codes($v['errors']),true),'FINAL_APPROVED darf ohne dokumentierte Sichtprüfung niemals PASS werden.');
};
$tests['matching_visible_sight_review_receipt_allows_final_approved']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['mode']='FINAL_APPROVED';
    $f['human_sight_review']=APKW_Validator::create_signed_review_receipt($f,'final','Gesamtbaum im Chat sichtbar geprüft und fachlich freigegeben.',1,'2026-08-20T13:30:00Z');
    $v=APKW_Validator::validate($f);
    assert_true($v['valid'],'Passende Sichtfreigabe muss FINAL_APPROVED ermöglichen: '.implode(',',codes($v['errors'])));
};
$tests['structure_change_after_visible_review_invalidates_receipt']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['mode']='FINAL_APPROVED';
    $f['human_sight_review']=APKW_Validator::create_signed_review_receipt($f,'final','Sichtprüfung PASS.',1,'2026-08-20T13:30:00Z');
    $f['nodes'][1]['name']='Nachträglich geändert';
    $v=APKW_Validator::validate($f);
    assert_true(!$v['valid']&&in_array('HUMAN_SIGHT_REVIEW_SCOPE_CHANGED',codes($v['errors']),true),'Jede Strukturänderung nach Sichtprüfung muss erneute Sichtprüfung erzwingen.');
};
$tests['review_scope_hash_is_order_insensitive_but_content_sensitive']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$a=APKW_Validator::review_scope_hash($f);
    $f2=$f;$f2['nodes']=array_reverse($f2['nodes']);$f2['project']['exclusions']=array_reverse($f2['project']['exclusions']);$b=APKW_Validator::review_scope_hash($f2);
    assert_true($a===$b,'Reine Array-Reihenfolge darf keine erneute Sichtprüfung erzwingen.');
    $f2['nodes'][0]['scope'].=' geändert';$c=APKW_Validator::review_scope_hash($f2);assert_true($a!==$c,'Inhaltliche Strukturänderung muss Review-Scope ändern.');
};
$tests['admin_exposes_visible_sight_review_as_mandatory_gate']=function(){
    $src=file_get_contents(dirname(__DIR__).'/includes/class-apkw-admin.php');
    assert_true(str_contains($src,'sichtbare Erstprüfung')&&str_contains($src,'sichtbare Global-Gap-Prüfung')&&str_contains($src,'sichtbare Finalprüfung'),'Admin-Workflow muss alle drei sichtbaren Pflichtfreigaben nennen.');
    assert_true(str_contains($src,'READY_FOR_VISIBLE_SIGHT_REVIEW')&&str_contains($src,'PASS_FINAL_APPROVED'),'Admin muss Vor-Sichtprüfung und finale Freigabe technisch unterscheiden.');
};

$tests['end_to_end_final_approved_passes_same_dataforseo_gates_as_preview']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['mode']='FINAL_APPROVED';
    $f['human_sight_review']=APKW_Validator::create_signed_review_receipt($f,'final','Gesamtbaum sichtbar geprüft und freigegeben.',1,'2026-08-20T13:30:00Z');
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);$c=APKW_Comparator::compare($f,$v);
    assert_true($v['valid'],'FINAL_APPROVED Validator muss PASS sein.');
    assert_true($e['valid'],'FINAL_APPROVED muss dieselben DataForSEO-Evidenzgates wie Preview bestehen: '.implode(',',codes($e['errors'])));
    assert_true($c['status']==='PASS_READ_ONLY_PREVIEW','Comparator bleibt rein lesend und muss PASS sein.');
};
$tests['final_approved_cannot_bypass_missing_dataforseo_evidence_even_with_fresh_review_hash']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['mode']='FINAL_APPROVED';
    $f['nodes'][1]['primary_keyword']='nicht belegtes phantom keyword';$f['nodes'][1]['name']='Phantom Kategorie';$f['nodes'][1]['slug']='phantom-kategorie';
    $f['human_sight_review']=APKW_Validator::create_signed_review_receipt($f,'final','Absichtlicher Negativtest.',1,'2026-08-20T13:30:00Z');
    $v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(!$e['valid']&&in_array('DFS_PRIMARY_KEYWORD_UNRESOLVED',codes($e['errors']),true),'Sichtfreigabe darf fehlende DataForSEO-Evidenz niemals überstimmen.');
};
$tests['final_approved_validation_performs_zero_external_requests']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['mode']='FINAL_APPROVED';
    $f['human_sight_review']=APKW_Validator::create_signed_review_receipt($f,'final','Sichtprüfung PASS.',1,'2026-08-20T13:30:00Z');
    $GLOBALS['remote_requests']=[];$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);$c=APKW_Comparator::compare($f,$v);
    assert_true($v['valid']&&$e['valid']&&$c['status']==='PASS_READ_ONLY_PREVIEW','Finalprüfung muss lokal PASS sein.');
    assert_true(count($GLOBALS['remote_requests'])===0,'Finale Freigabeprüfung darf keine externe DataForSEO-Abfrage auslösen.');
};

$tests['global_paid_stage_blocks_without_initial_visible_review']=function(){
    $d=draft_pkg();unset($d['initial_human_sight_review']);$GLOBALS['remote_requests']=[];
    try{APKW_Research::build_global_coverage($d,'Germany','de',1000,false);throw new RuntimeException('Global-Coverage hätte ohne Erst-Sichtprüfung blockieren müssen.');}
    catch(RuntimeException $e){assert_true(str_contains($e->getMessage(),'INITIAL_HUMAN_SIGHT_REVIEW'),'Fehlende Erst-Sichtprüfung muss konkret blockieren.');}
    assert_true(count($GLOBALS['remote_requests'])===0,'Ohne Erst-Sichtprüfung darf kein kostenpflichtiger Request entstehen.');
};
$tests['initial_visible_review_is_hash_bound_and_invalidated_by_tree_change']=function(){
    $d=draft_pkg();$d['nodes'][1]['name']='Sauerteig verändert';$pf=APKW_Research::preflight_draft($d);
    assert_true(!$pf['valid']&&in_array('INITIAL_HUMAN_SIGHT_REVIEW_SCOPE_CHANGED',codes($pf['errors']),true),'Änderung nach Erst-Sichtfreigabe muss neuen Review erzwingen.');
};
$tests['detail_stage_blocks_without_global_gap_visible_review']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$GLOBALS['remote_requests']=[];$pf=APKW_Research::preflight_detail($d,$g);
    assert_true(!$pf['valid']&&in_array('GLOBAL_GAP_HUMAN_REVIEW_MISSING',codes($pf['errors']),true),'Detailresearch muss ohne sichtbare Global-Gap-Freigabe blockieren.');
    assert_true(count($GLOBALS['remote_requests'])===0,'Fehlende Global-Gap-Sichtprüfung darf keinen Paid-Request auslösen.');
};
$tests['global_gap_visible_review_is_hash_bound_and_invalidated_by_change']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$d=approve_global_gap($d,$g);$d['nodes'][1]['name']='Nach Freigabe verändert';$pf=APKW_Research::preflight_detail($d,$g);
    assert_true(!$pf['valid']&&in_array('GLOBAL_GAP_HUMAN_REVIEW_SCOPE_CHANGED',codes($pf['errors']),true),'Änderung nach Global-Gap-Freigabe muss Detailresearch blockieren.');
};
$tests['deferred_global_gap_blocks_detail_research']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);array_unshift($g['global_discovery']['items'],['provider_rank'=>1,'keyword'=>'pizzaofen','search_volume'=>3000,'main_intent'=>'commercial','core_keyword'=>'pizzaofen','keyword_difficulty'=>20,'cpc'=>1.2]);$g['content_sha256']=APKW_Research::canonical_hash($g);
    $d['global_coverage_decisions'][]=['core_keyword'=>'pizzaofen','decision'=>'DEFERRED','reason'=>'Absichtlicher Negativtest.'];$d=approve_global_gap($d,$g);$pf=APKW_Research::preflight_detail($d,$g);
    assert_true(!$pf['valid']&&in_array('GLOBAL_COVERAGE_CORE_DEFERRED_BLOCKS_DETAIL',codes($pf['errors']),true),'DEFERRED darf Detailresearch nicht als erledigten Coverage-Befund passieren lassen.');
};
$tests['deferred_cluster_gap_blocks_ready_and_final']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$r['cluster_research']['clusters'][0]['items'][]=['provider_rank'=>1,'keyword'=>'brotbackofen','search_volume'=>9999,'main_intent'=>'commercial','core_keyword'=>'brotbackofen','keyword_difficulty'=>20,'cpc'=>1.0];$r['content_sha256']=APKW_Research::canonical_hash($r);
    $f=final_from_draft($d,$r);$f['keyword_coverage_decisions']=[['cluster_id'=>'brot','core_keyword'=>'brotbackofen','decision'=>'DEFERRED','reason'=>'Absichtlicher Negativtest.']];$v=APKW_Validator::validate($f);$e=APKW_ResearchEvidence::analyze($f,$r,$v);
    assert_true(in_array('DFS_TOP_KEYWORD_GROUP_DEFERRED_BLOCKS_FINAL',codes($e['errors']),true),'DEFERRED darf READY/FINAL nicht schließen.');
};
$tests['old_paid_global_package_without_initial_review_is_not_valid_new_workflow_input']=function(){
    $d=draft_pkg();unset($d['initial_human_sight_review']);$v=APKW_Validator::validate_initial_review_gate($d);
    assert_true(!$v['valid'],'Historischer Paid-Lauf ohne vorgelagerte Sichtfreigabe darf nicht als neuer Workflow-PASS gelten.');
};

$tests['target_market_change_after_initial_review_blocks_paid_global']=function(){
    $d=draft_pkg();$d['project']['target_market']='Austria';$GLOBALS['remote_requests']=[];try{APKW_Research::build_global_coverage($d,'Austria','de',1000,false);throw new RuntimeException('Marktänderung hätte blockieren müssen.');}catch(RuntimeException $e){assert_true(str_contains($e->getMessage(),'INITIAL_HUMAN_SIGHT_REVIEW_SCOPE_CHANGED'),'Geänderter Zielmarkt muss die initiale Sichtfreigabe invalidieren.');}assert_true(count($GLOBALS['remote_requests'])===0,'Marktänderung darf keinen Paid-Call auslösen.');
};
$tests['runtime_language_cannot_bypass_project_contract']=function(){
    $d=draft_pkg();$GLOBALS['remote_requests']=[];try{APKW_Research::build_global_coverage($d,'Germany','en',1000,false);throw new RuntimeException('Abweichende Laufzeitsprache hätte blockieren müssen.');}catch(RuntimeException $e){assert_true(str_contains($e->getMessage(),'PROJECT CONTRACT'),'Laufzeitparameter müssen dem gebundenen Projektvertrag entsprechen.');}assert_true(count($GLOBALS['remote_requests'])===0,'Abweichende Sprache darf keinen Paid-Call auslösen.');
};


$tests['all_export_schemas_bind_master_contract_and_market_language']=function(){
    $root=dirname(__DIR__);
    foreach(['schema-category-v1.4.json','schema-global-coverage-v1.0.json','schema-research-v1.4.json'] as $file){
        $schema=json_decode(file_get_contents($root.'/'.$file),true,512,JSON_THROW_ON_ERROR);
        assert_true(in_array('master_contract_id',$schema['required']??[],true),$file.' muss master_contract_id verlangen.');
        assert_true(($schema['properties']['master_contract_id']['const']??'')===APKW_MASTER_CONTRACT_ID,$file.' muss exakt den aktiven Mastervertrag binden.');
    }
    foreach(['schema-global-coverage-v1.0.json','schema-research-v1.4.json'] as $file){
        $schema=json_decode(file_get_contents($root.'/'.$file),true,512,JSON_THROW_ON_ERROR);
        foreach(['location_name','language_code'] as $field)assert_true(in_array($field,$schema['properties']['market']['required']??[],true),$file.' muss market.'.$field.' verlangen.');
    }
};

$tests['admin_review_signing_actions_are_capability_nonce_and_explicit_confirmation_gated']=function(){
    $src=file_get_contents(dirname(__DIR__).'/includes/class-apkw-admin.php');
    foreach(['apkw_sign_initial_review','apkw_sign_global_gap_review','apkw_sign_final_review'] as $action)assert_true(str_contains($src,"admin_post_{$action}"),"Fehlende Review-Signieraktion: {$action}");
    assert_true(substr_count($src,"current_user_can('manage_options')")>=4,'Review-Signierung muss manage_options erzwingen.');
    assert_true(str_contains($src,'check_admin_referer($action,$nonce_field)')&&str_contains($src,'apkw_visible_review_confirmation'),'Review-Signierung benötigt Nonce und explizite Bestätigung.');
    assert_true(str_contains($src,'create_signed_review_receipt'),'Admin muss serverseitig signierte Review-Quittungen erzeugen.');
    assert_true(str_contains($src,'apkw_expected_review_scope_sha256')&&str_contains($src,'require_visible_scope_match'),'Signierung muss zusätzlich an den im sichtbaren Review bestätigten Scope-Hash gebunden sein.');
};

$tests['manual_initial_review_hash_injection_without_server_signature_blocks']=function(){
    $d=draft_pkg();
    $d['initial_human_sight_review']=['status'=>'APPROVED_INITIAL_TREE','review_scope_sha256'=>APKW_Validator::initial_review_scope_hash($d),'approved_at_utc'=>'2026-08-20T12:00:00Z','review_summary'=>'Manuell injiziert','approved_by_user_id'=>1];
    $GLOBALS['remote_requests']=[];$pf=APKW_Research::preflight_draft($d);
    assert_true(!$pf['valid']&&in_array('INITIAL_HUMAN_SIGHT_REVIEW_SIGNATURE_MISSING',codes($pf['errors']),true),'Manuell gesetzter Status+Hash darf ohne Serversignatur nicht freigeben.');
    assert_true(count($GLOBALS['remote_requests'])===0,'Injizierte Initialfreigabe darf keinen Paid-Call ermöglichen.');
};
$tests['forged_initial_review_signature_blocks']=function(){
    $d=draft_pkg();$d['initial_human_sight_review']['receipt_signature_sha256']=str_repeat('a',64);$pf=APKW_Research::preflight_draft($d);
    assert_true(!$pf['valid']&&in_array('INITIAL_HUMAN_SIGHT_REVIEW_SIGNATURE_INVALID',codes($pf['errors']),true),'Gefälschte Signatur muss blockieren.');
};
$tests['manual_global_gap_review_hash_injection_without_server_signature_blocks']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$d=approve_global_gap($d,$g);
    unset($d['global_gap_human_review']['receipt_signature_sha256']);$pf=APKW_Research::preflight_detail($d,$g);
    assert_true(!$pf['valid']&&in_array('GLOBAL_GAP_HUMAN_REVIEW_SIGNATURE_MISSING',codes($pf['errors']),true),'Manuelle Global-Gap-Freigabe ohne Signatur muss blockieren.');
};
$tests['manual_final_review_hash_injection_without_server_signature_blocks']=function(){
    $d=draft_pkg();$r=research_from_draft($d);$f=final_from_draft($d,$r);$f['mode']='FINAL_APPROVED';
    $f['human_sight_review']=['status'=>'APPROVED_AFTER_VISIBLE_REVIEW','review_scope_sha256'=>APKW_Validator::review_scope_hash($f),'approved_at_utc'=>'2026-08-20T13:30:00Z','review_summary'=>'Manuell injiziert','approved_by_user_id'=>1];
    $v=APKW_Validator::validate($f);assert_true(!$v['valid']&&in_array('HUMAN_SIGHT_REVIEW_SIGNATURE_MISSING',codes($v['errors']),true),'Manuelle Finalfreigabe ohne Serversignatur muss blockieren.');
};
$tests['global_package_market_tamper_with_recomputed_outer_hash_blocks']=function(){
    $d=draft_pkg();$g=APKW_Research::build_global_coverage($d,'Germany','de',1000,false);$g['market']['location_name']='Austria';$g['content_sha256']=APKW_Research::canonical_hash($g);$v=APKW_Research::verify_global_coverage($g);
    assert_true(!$v['valid']&&in_array('GLOBAL_COVERAGE_MARKET_MISMATCH',$v['errors'],true),'Neuberechneter Hash darf falschen Markt nicht legitimieren.');
};
$tests['research_package_language_tamper_with_recomputed_outer_hash_blocks']=function(){
    $r=research_from_draft(draft_pkg());$r['market']['language_code']='en';$r['content_sha256']=APKW_Research::canonical_hash($r);$v=APKW_Research::verify_package($r);
    assert_true(!$v['valid']&&in_array('RESEARCH_LANGUAGE_MISMATCH',$v['errors'],true),'Neuberechneter Research-Hash darf falsche Sprache nicht legitimieren.');
};
$tests['wrong_master_contract_blocks_category_and_research_scopes']=function(){
    $d=draft_pkg();$d['master_contract_id']='ALTER_MASTER';$v=APKW_Validator::validate($d);assert_true(in_array('MASTER_CONTRACT_ID_MISMATCH',codes($v['errors']),true),'Falscher Mastervertrag muss Category-Paket blockieren.');
};
$tests['master_contract_is_part_of_review_scope_hash']=function(){
    $d=draft_pkg();$a=APKW_Validator::initial_review_scope_hash($d);$d['master_contract_id']='ALTER_MASTER';$b=APKW_Validator::initial_review_scope_hash($d);assert_true($a!==$b,'Mastervertrag muss Review-Scope verändern.');
};

$passed=0;$failed=[];foreach($tests as $name=>$test){try{$test();$passed++;echo "PASS $name\n";}catch(Throwable $e){$failed[$name]=$e->getMessage();echo "FAIL $name: {$e->getMessage()}\n";}}echo 'TOTAL '.count($tests).' PASS '.$passed.' FAIL '.count($failed)."\n";if($failed)exit(1);
