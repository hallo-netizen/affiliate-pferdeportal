<?php
declare(strict_types=1);
const ABSPATH='/local-wordpress-test/';
const PSTE_OPTION_EDITORIAL_PLAN_IMPORT='pste_editorial_import';
const ARRAY_A='ARRAY_A';
$root='/mnt/data/work_pste_exportfix/Portal SEO Topic Engine/includes/';
$real=json_decode(file_get_contents('/mnt/data/pferdeatelier-mini-ergebnisse-20261108-150347.json'),true,512,JSON_THROW_ON_ERROR);
$park=$real['parkhaus_snapshot'];
$bySource=[];foreach($park['items'] as $it)$bySource[$it['source']][]=$it;
$miniCompleted=[];$byRaw=[];foreach($real['seo_subjects'] as $s)$byRaw[$s['raw_query']]=$s;
foreach($real['items'] as $it){if($it['decision']!=='JA')continue;$src=$byRaw[$it['raw_query']]??null;if(!$src)throw new Exception('MISSING_SEO_SUBJECT');$miniCompleted[$src['pool_key']]=$it;}
function assertPass($condition,$tag):void {if(!$condition)throw new RuntimeException("FAIL:$tag");echo "PASS $tag\n";}
function expectCode(callable $fn,string $tag,string $needle):void {try{$fn();}catch(Throwable $e){if(str_contains($e->getMessage(),$needle)){echo "PASS $tag - blocked: ".$e->getMessage()."\n";return;} throw new RuntimeException('FAIL '.$tag.' different error: '.$e->getMessage());}throw new RuntimeException('FAIL '.$tag.' accepted');}
function get_option($name,$default=null){global $stubOptions;return $stubOptions[$name]??$default;}
function apply_filters($name,$value){return $value;}
function wp_json_encode($x,$flags=0){return json_encode($x,$flags|JSON_THROW_ON_ERROR);}
function wp_strip_all_tags($x){return strip_tags($x);}
function get_post_types($options=[],$output='names'){return ['post'=>'post','page'=>'page','pa_breed'=>'pa_breed','uge_term'=>'uge_term','hp_listing'=>'hp_listing','hp_vendor'=>'hp_vendor'];}
function get_post($id){global $simulateMissingPostFallback,$missingPostTargets;$id=(int)$id;if(!$simulateMissingPostFallback||!in_array($id,$missingPostTargets,true))return null;return (object)['ID'=>$id,'post_title'=>'SYNTHETIC_RESOLVED_DRAFT_'.$id,'post_status'=>'trash'];}
class PSTE_Editorializer {static function sourceQuery(array $item): string{return (string)($item['raw_query']??'');}}
class PSTE_Repository {static function table($name):string{return 'pste_pool';}static function workflowRouteForCandidate($candidate):string{return 'K0';}}
class PSERC_Plan_Dependency_Fingerprint {static function isCurrent($x){return true;}}
class PSERC_Plan_Snapshot_Store {
    static function getActive(){global $stubPSERC;return ['generation'=>str_repeat('a',20),'counts'=>['compiled_items'=>count($stubPSERC)],'dependency'=>[],'snapshot_sha256'=>str_repeat('b',64)];}
    static function verifyHeader($head){return !empty($head['snapshot_sha256']);}
    static function getRecord($gen,$name,$index){global $stubPSERC;return $stubPSERC[$index]??null;}
}
class StubDb {
    public string $posts='wp_posts',$postmeta='wp_postmeta',$terms='wp_terms',$term_relationships='wp_term_relationships',$term_taxonomy='wp_term_taxonomy',$last_error='';
    public int $readCalls=0;private array $postsRows;private array $psteRows;
    function __construct(array $wp,array $pste){foreach($wp as $it)$this->postsRows[]=['ID'=>$it['id'],'post_title'=>$it['title'],'post_type'=>$it['type'],'post_status'=>$it['status'],'post_name'=>$it['slug'],'post_content'=>'','post_modified_gmt'=>$it['modified_gmt']];sort($this->postsRows);$it=$pste[0];$this->psteRows=[['id'=>1,'pool_key'=>$it['pool_key'],'candidate_id'=>$it['seo_topic_id'],'payload_json'=>json_encode(['raw_query'=>$it['raw_query'],'production_title'=>$it['title'],'target_keyword'=>$it['target_keyword'],'target_category_name'=>$it['category'],'proposed_article_type'=>$it['article_type'],'intent_profile'=>$it['intent_profile']]),'planning_suitability'=>'YES','automatic_pool_status'=>'AUTO_RESOLVED']];}
    function prepare($q,...$values){$i=0;return preg_replace_callback('/%[ds]/',function($m)use(&$i,$values){$v=$values[$i++];return $m[0]==='%d'?(string)(int)$v:"'".str_replace("'","''",(string)$v)."'";},$q);}
    function get_var($q){$this->readCalls++;if(str_contains($q,'FROM wp_posts'))return count($this->postsRows);if(str_contains($q,'FROM pste_pool'))return count($this->psteRows);throw new Exception('Unexpected COUNT '.$q);}
    function get_results($q,$as='ARRAY_A'){global $bySource;$this->readCalls++;if(str_contains($q,'FROM wp_posts')&&str_contains($q,'SELECT ID,post_title')){
        preg_match('/WHERE ID>(\d+)/',$q,$m);$cursor=(int)($m[1]??0);return array_slice(array_values(array_filter($this->postsRows,fn($x)=>$x['ID']>$cursor)),0,200);
    }if(str_contains($q,'FROM wp_postmeta')){
        preg_match('/IN \(([\d,]+)\) ORDER BY post_id/',$q,$m);$ids=array_map('intval',explode(',',$m[1]??''));$out=[];
        foreach($bySource['WORDPRESS'] as $it)if(in_array((int)$it['id'],$ids,true)){
            foreach(['_yoast_wpseo_focuskw'=>'target_keyword','_ppm679_canonical_article_id'=>'canonical_article_id','_ppm679_plan_slot_sha256'=>'plan_slot'] as $meta=>$field)if(!empty($it[$field]))$out[]=['post_id'=>$it['id'],'meta_key'=>$meta,'meta_value'=>$it[$field]];
        }return $out;
    }if(str_contains($q,'FROM wp_term_relationships')){
        preg_match('/IN \(([\d,]+)\) ORDER BY/',$q,$m);$ids=array_map('intval',explode(',',$m[1]??''));$out=[];
        foreach($bySource['WORDPRESS'] as $it)if(in_array((int)$it['id'],$ids,true))foreach($it['categories'] as $c)$out[]=['post_id'=>$it['id'],'category_id'=>$c['id'],'category_name'=>$c['name']];return $out;
    }if(str_contains($q,'FROM pste_pool')){
        preg_match('/WHERE id>(\d+)/',$q,$m);$cursor=(int)($m[1]??0);return array_values(array_filter($this->psteRows,fn($x)=>$x['id']>$cursor));
    }throw new Exception('Unexpected SQL '.substr($q,0,130));}
}
require $root.'class-pste-snapshot.php';
require $root.'class-pste-mini-workflow.php';

// Real code: editorial normalization with supported nested formats, no casting of arrays.
$ref=new ReflectionMethod('PSTE_Snapshot','normalizeEditorialPlanItemsAgainstStructure');
$known=['title'=>['production_title'=>'Wie wähle ich Regendecken richtig aus?'],'primary_longtail_query'=>'regendecken pferd','category_id'=>0,'article_type'=>'Beratung'];
$fixed=$ref->invoke(null,[$known],['items'=>[]]);
assertPass(count($fixed)===1&&$fixed[0]['title']==='Wie wähle ich Regendecken richtig aus?','editorial_nested_title_resolved');
expectCode(fn()=>$ref->invoke(null,[['title'=>['unrecognized'=>['a','b']]]],['items'=>[]]),'editorial_ambiguous_title_blocks','PSTE_EDITORIAL_PLAN_TITLE_UNRESOLVED');
expectCode(fn()=>$ref->invoke(null,[['title'=>'Array']],['items'=>[]]),'editorial_literally_array_blocks','PSTE_EDITORIAL_PLAN_TITLE_UNRESOLVED');
$salvaged=$ref->invoke(null,[['title'=>'Array','primary_longtail_query'=>'Eindeutig gespeicherter Sachbegriff']],['items'=>[]]);
assertPass($salvaged[0]['title']==='Eindeutig gespeicherter Sachbegriff','legacy_array_title_falls_back_to_valid_original_query');


// Real code: editorialPlan status is AVAILABLE only for fully normalized records.
$prop=new ReflectionProperty('PSTE_Snapshot','structureSnapshotCache');$prop->setValue(null,['items'=>[]]);
$stubOptions=[PSTE_OPTION_EDITORIAL_PLAN_IMPORT=>['items'=>[$known]]];
$ed=PSTE_Snapshot::editorialPlan();
assertPass($ed['status']==='AVAILABLE'&&count($ed['items'])===1,'editorial_plan_status_available');
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]=['items'=>[['title'=>['foo'=>['bad']]]]];
expectCode(fn()=>PSTE_Snapshot::editorialPlan(),'editorial_plan_unusable_blocks','PSTE_EDITORIAL_PLAN_TITLE_UNRESOLVED');

// Full real readParkhausForMini PHP code simulated from 1,179 real export items.
$byWp=$bySource['WORDPRESS'];$byPste=$bySource['PSTE_PLAN'];$byPserc=$bySource['PSERC_ACTIVE_PLAN'];
$stubPSERC=[];foreach($byPserc as $it)$stubPSERC[]=['status'=>$it['status'],'title'=>['production_title'=>$it['title']],'target_keyword'=>['value'=>$it['target_keyword']],'seo_topic_id'=>$it['seo_topic_id'],'article_type'=>$it['article_type'],'category'=>['slug'=>$it['category_slug']],'canonical_slot'=>['canonical_article_id'=>$it['canonical_article_id'],'plan_slot_sha256'=>$it['plan_slot']],'intent_profile'=>$it['intent_profile']];
$runtimeItems=[];$missingPostTargets=[];$wpById=[];foreach($byWp as $w)$wpById[$w['id']]=$w;
foreach($bySource['PPM679_EXISTING_EDITORIAL_RUNTIME'] as $it){$runtimeItems[$it['canonical_article_id']]=['canonical_article_id'=>$it['canonical_article_id'],'plan_slot_sha256'=>$it['plan_slot'],'post_id'=>$it['post_id'],'status'=>$it['status'],'category_slug'=>$it['category'],'article_type'=>$it['article_type'],'target_keyword'=>$it['target_keyword'],'title'=>''];if(!isset($wpById[$it['post_id']]))$missingPostTargets[]=$it['post_id'];}
$stubOptions=['ppm679_editorial_plan_runtime_state_v1'=>['items'=>$runtimeItems],'pste_mini_keyword_roundtrip_v1'=>['completed'=>$miniCompleted,'active'=>null,'clarification'=>[]], PSTE_OPTION_EDITORIAL_PLAN_IMPORT=>['items'=>[$known]]];
$wpdb=new StubDb($byWp,$byPste);
$simulateMissingPostFallback=false;
$parkRes=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($parkRes['complete']===false&&str_contains($parkRes['reason'],'PPM679_RUNTIME_ARTICLE_TITLE_UNRESOLVED'),'real_1179_records_hold_three_missing_references');
assertPass(count($missingPostTargets)===3,'exactly_three_unresolved_references');

$simulateMissingPostFallback=true;
$parkRes=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($parkRes['complete']===true&&preg_match('/^[a-f0-9]{64}$/',$parkRes['sha256'])===1,'synthetic_full_parkhaus_positive');
assertPass(count($parkRes['items'])===1024+1+1+1+144,'expected_item_count_single_editorial_fixture');
$ppmRows=array_values(array_filter($parkRes['items'],fn($x)=>$x['source']==='PPM679_EXISTING_EDITORIAL_RUNTIME'));
assertPass(count($ppmRows)===144&&count(array_filter($ppmRows,fn($x)=>$x['title']!==''))===144,'all_144_ppm_titles_explicit');
assertPass(count(array_filter($ppmRows,fn($x)=>str_starts_with($x['title'],'SYNTHETIC_')))===3,'only_three_fixture_fallbacks');
assertPass(count(array_filter($ppmRows,fn($x)=>!str_starts_with($x['title'],'SYNTHETIC_')))===141,'141_real_existing_wp_titles_joined');
$before=json_encode($stubOptions);$second=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($second['sha256']===$parkRes['sha256']&&$before===json_encode($stubOptions),'readonly_deterministic_no_option_writes');
assertPass($wpdb->readCalls>0,'existing_export_read_only_sql_used');

// Actual real import decision validator with true source hashes from existing 87.
$subjects=$real['seo_subjects'];$a=$subjects[0];$b=$subjects[1];$c=$subjects[2];$titleByRaw=[];foreach($real['items'] as $row)$titleByRaw[$row['raw_query']]=$row['titles'][0]['title']??'';
$create=function($row,$box,$slot,$match='')use($titleByRaw){return ['pool_key'=>$row['pool_key'],'raw_query'=>$row['raw_query'],'source_sha256'=>$row['source_sha256'],'box'=>$box,'intent_summary'=>'Eindeutige Suchabsicht im simulierten Beleg','approved_title'=>$titleByRaw[$row['raw_query']],'intent_slot'=>$slot,'matched_ref'=>$match];};
$slot=hash('sha256','LOCAL_UNIQUE_ARTICLE_SLOT_UNOCCUPIED');$wpExisting=$byWp[0];$doc=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','owner'=>'EXTERNAL_SINGLE_SEO_EDITOR','snapshot_sha256'=>$parkRes['sha256'],'items'=>[$create($a,'FREI',$slot),$create($b,'BELEGT','', 'WORDPRESS:'.$wpExisting['id']),$create($c,'KLAERUNG','')]];
$input=['completed'=>$miniCompleted,'seo_decisions'=>[],'clarification'=>[]];
$new=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$doc,$parkRes);
assertPass($new['seo_last_report']['counts']===['FREI'=>1,'BELEGT'=>1,'KLAERUNG'=>1],'one_seo_owner_three_boxes_positive');
assertPass($new['seo_last_report']['semantic_evaluation_in_wordpress']===false&&$new['seo_last_report']['eligible_for_article_handoff']===false,'no_second_semantic_reviewer_or_article');
$stubOptions['pste_mini_keyword_roundtrip_v1']=$new;
assertPass(PSTE_Mini_Workflow::singleOwnerSeoFor($a['pool_key'],$a['raw_query'])['box']==='FREI','source_bound_free_receipt_readable');
assertPass(PSTE_Mini_Workflow::singleOwnerSeoFor($a['pool_key'],$a['raw_query'],true)===[],'handoff_requires_existing_plan_checkpoint');
$wrong=$doc;$wrong['snapshot_sha256']=str_repeat('0',64);
expectCode(fn()=>PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$wrong,$parkRes),'stale_snapshot_fails_closed','PSTE_MINI_SEO_PORTAL_PLAN_CHANGED_OR_INCOMPLETE');
$wrong=$doc;$wrong['owner']='OTHER_OWNER';
expectCode(fn()=>PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$wrong,$parkRes),'second_owner_rejected','PSTE_MINI_SEO_OWNER_REQUIRED');
$wrong=$doc;$wrong['items'][1]=$create($b,'FREI',$slot);
$conflict=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$wrong,$parkRes);
assertPass($conflict['seo_last_report']['counts']['KLAERUNG']===2&&$conflict['seo_last_report']['counts']['FREI']===1,'duplicate_slot_demoted_to_clarification');
$wrong=$doc;$wrong['items'][0]['raw_query']='changed query';
$conflict=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$wrong,$parkRes);
assertPass(($conflict['clarification'][$a['pool_key']]['reason_code']??'')==='SEO_ORIGINAL_SOURCE_BINDING_FAILED','altered_source_demoted_to_clarification');
$wrong=$doc;$wrong['items'][1]['matched_ref']='WORDPRESS:999999999';
$conflict=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$wrong,$parkRes);
assertPass(($conflict['clarification'][$b['pool_key']]['reason_code']??'')==='BELEGT_REFERENCE_NOT_IN_EXISTING_PARKHAUS','fabricated_existing_reference_rejected');
$wrong=$doc;$wrong['items'][0]['intent_slot']=$bySource['PPM679_EXISTING_EDITORIAL_RUNTIME'][0]['plan_slot'];
$conflict=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$wrong,$parkRes);
assertPass(($conflict['clarification'][$a['pool_key']]['reason_code']??'')==='FREI_MISSING_OR_CONFLICTING_SOURCE_SLOT','occupied_plan_slot_cannot_be_free');
$wrong=$doc;$wrong['items'][]=$wrong['items'][0];
$conflict=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$wrong,$parkRes);
assertPass(($conflict['clarification'][$a['pool_key']]['reason_code']??'')==='SEO_DUPLICATE_SOURCE_ROWS','duplicate_source_cannot_be_free');

// All original 87 real candidates can be safely held without creating any articles.
$allRows=[];foreach($subjects as $row)$allRows[]=$create($row,'KLAERUNG','');
$bulk=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','owner'=>'EXTERNAL_SINGLE_SEO_EDITOR','snapshot_sha256'=>$parkRes['sha256'],'items'=>$allRows],$parkRes);
assertPass($bulk['seo_last_report']['counts']['KLAERUNG']===87&&$bulk['seo_last_report']['counts']['FREI']===0,'all_87_original_topics_safe_clarification_no_article');

// PSERC 0.28.55 actual adapter, no second SEO verdict.
class PSERC_Metadata_Boundary {public static function forbiddenContentPath($candidate,$path){return '';}}
class PSTE_Normal_Metadata_Path {public static function persistedStoredTitleCandidate($candidate){return (string)($candidate['production_title']??'');}}
class PSERC_Article_Type_Extension_Registry {public static function extension($type){return null;}}
require '/mnt/data/inspect_pserc/portal-seo-editorial-plan-compiler/includes/class-pserc-seo-reader.php';
$passCandidate=[
 'pool_key'=>$a['pool_key'],'production_title'=>$titleByRaw[$a['raw_query']],
 'raw_keyword_preserved'=>$a['raw_query'],'decision'=>'PASS','planning_suitability'=>'YES',
 'pool_status'=>'AUTO_RESOLVED','topic_role'=>'ARTICLE_TOPIC','context_state'=>'CURRENT',
 'proposed_article_type'=>'Beratung','target_category_slug'=>'testkategorie',
 'target_keyword'=>$a['raw_query'],
 'metadata_handoff_fields'=>['title','target_keyword','category','article_type','plan_slot'],
 'textmachine_handoff_status'=>'READY_FOR_COMPILER_CAPABILITY_CHECK',
 'planning_readiness_gate'=>['external_editorial_receipt'=>$new['seo_decisions'][$a['pool_key']]]
];
$adapter=PSERC_SEO_Reader::normalizeCandidate($passCandidate);
assertPass($adapter['eligibility_status']==='ELIGIBLE'&&($adapter['single_external_seo_owner_receipt']['box']??'')==='FREI','real_pserc_reader_accepts_exact_single_owner_receipt');
$stale=$passCandidate;$stale['planning_readiness_gate']['external_editorial_receipt']['intent_slot']=str_repeat('d',64);
$adapter=PSERC_SEO_Reader::normalizeCandidate($stale);
assertPass($adapter['eligibility_status']==='HELD'&&in_array('SEO_EXTERNAL_SINGLE_OWNER_PROOF_MISSING_OR_STALE',$adapter['eligibility_reasons'],true),'real_pserc_reader_stale_receipt_held');
$other=$passCandidate;unset($other['planning_readiness_gate']);
$other['pool_key']='other_unrelated_legacy_source';
$adapter=PSERC_SEO_Reader::normalizeCandidate($other);
assertPass($adapter['eligibility_status']==='ELIGIBLE','unrelated_legacy_candidate_not_blocked_by_single_owner');
$blocked=$passCandidate;$blocked['planning_readiness_gate']['external_editorial_receipt']['approved_title']='FALSCH';
$adapter=PSERC_SEO_Reader::normalizeCandidate($blocked);
// Only the source/slot/title binding comes from the stored receipt; the adapter never re-evaluates topic meaning.
assertPass($adapter['eligibility_status']==='ELIGIBLE','pserc_ignores_untrusted_receipt_extra_title_but_uses_stored_exact_source_title');
// Exact normal WordPress admin UI output (without a browser): primary actions + hidden expert controls.
function esc_html($x){return htmlspecialchars((string)$x,ENT_QUOTES,'UTF-8');}
function esc_url($x){return htmlspecialchars((string)$x,ENT_QUOTES,'UTF-8');}
function admin_url($path){return 'https://wp-test.local/wp-admin/'.$path;}
function wp_nonce_field($action){echo '<input type="hidden" name="_wpnonce" value="simulation-'.$action.'">';}
ob_start();PSTE_Mini_Workflow::renderKeywords();$markup=ob_get_clean();
assertPass(str_contains($markup,'Externe SEO-Prüfung')&&str_contains($markup,'Redaktionsstand für externe SEO-Prüfung exportieren')&&str_contains($markup,'Extern geprüfte SEO-Ergebnisdatei')&&substr_count($markup,'name="include_parkhaus"')===1,'simple_normal_ui_export_import_status_once');
assertPass(str_contains($markup,'<details class="pste-box"><summary>Weitere Werkzeuge (nur für Sonderfälle)'),'advanced_legacy_tools_collapsed');
$stubOptions['pste_mini_keyword_roundtrip_v1']=['completed'=>[],'active'=>null,'clarification'=>[]];
ob_start();PSTE_Mini_Workflow::renderKeywords();$freshMarkup=ob_get_clean();
assertPass(str_contains($freshMarkup,'100 noch offene Stichwörter exportieren')&&!str_contains($freshMarkup,'name="include_parkhaus"'),'fresh_start_ui_shows_only_first_action');
$stubOptions['pste_mini_keyword_roundtrip_v1']=['completed'=>[],'active'=>['items'=>[$real['items'][0]]],'clarification'=>[]];
ob_start();PSTE_Mini_Workflow::renderKeywords();$openMarkup=ob_get_clean();
assertPass(str_contains($openMarkup,'Stichwortstapel noch offen')&&str_contains($openMarkup,'Stichwörter übernehmen')&&!str_contains($openMarkup,'name="include_parkhaus"'),'open_batch_ui_no_premature_seo_export');
echo "PASS TOTAL LOCAL REALDATA-BASED PHP WORKFLOW SIMULATION (3 synthetic missing posts only)\n";