<?php
declare(strict_types=1);
const ABSPATH='/local-wordpress-test/';
const PSTE_OPTION_EDITORIAL_PLAN_IMPORT='pste_editorial_import';
const ARRAY_A='ARRAY_A';
$root='/mnt/data/work_pste_05714425/Portal SEO Topic Engine/includes/';
$real=json_decode(file_get_contents('/mnt/data/pferdeatelier-mini-ergebnisse-20261108-162920.json'),true,512,JSON_THROW_ON_ERROR);
$park=$real['parkhaus_snapshot'];
$bySource=[];foreach($park['items'] as $it)$bySource[$it['source']][]=$it;
$miniCompleted=[];$byRaw=[];foreach($real['seo_subjects'] as $s)$byRaw[$s['raw_query']]=$s;
foreach($real['items'] as $it){if($it['decision']!=='JA')continue;$src=$byRaw[$it['raw_query']]??null;if(!$src)throw new Exception('MISSING_SEO_SUBJECT');$miniCompleted[$src['pool_key']]=$it;}
function assertPass($condition,$tag):void {if(!$condition)throw new RuntimeException("FAIL:$tag");echo "PASS $tag\n";}
function expectCode(callable $fn,string $tag,string $needle):void {try{$fn();}catch(Throwable $e){if(str_contains($e->getMessage(),$needle)){echo "PASS $tag - blocked: ".$e->getMessage()."\n";return;} throw new RuntimeException('FAIL '.$tag.' different error: '.$e->getMessage());}throw new RuntimeException('FAIL '.$tag.' accepted');}
function get_option($name,$default=null){global $stubOptions;return $stubOptions[$name]??$default;}
function apply_filters($name,$value){global $stubFilter;return $name==='pste_read_only_editorial_plan_snapshot'&&isset($stubFilter)?$stubFilter:$value;}
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
expectCode(fn()=>PSTE_Snapshot::editorialPlan(),'editorial_plan_unusable_blocks','PSTE_EDITORIAL_PLAN_ITEM_UNRESOLVED');
$readQuarantine=PSTE_Snapshot::editorialPlanForParkhaus();
assertPass($readQuarantine['status']==='QUARANTINED'&&$readQuarantine['unresolved_count']===1&&count($readQuarantine['items'])===1,'old_bad_editorial_source_readable_as_quarantine');
assertPass(($readQuarantine['items'][0]['raw_title_fields']['title']['foo'][0]??'')==='bad'&&$readQuarantine['items'][0]['title']===''&&strlen($readQuarantine['items'][0]['raw_record_sha256'])===64,'original_nested_invalid_title_preserved_for_repair_no_fake');

// Full real readParkhausForMini PHP code simulated from 1,179 real export items.
$byWp=$bySource['WORDPRESS'];$byPste=$bySource['PSTE_PLAN'];$byPserc=$bySource['PSERC_ACTIVE_PLAN'];
$stubPSERC=[];foreach($byPserc as $it)$stubPSERC[]=['status'=>$it['status'],'title'=>['production_title'=>$it['title']],'target_keyword'=>['value'=>$it['target_keyword']],'seo_topic_id'=>$it['seo_topic_id'],'article_type'=>$it['article_type'],'category'=>['slug'=>$it['category_slug']],'canonical_slot'=>['canonical_article_id'=>$it['canonical_article_id'],'plan_slot_sha256'=>$it['plan_slot']],'intent_profile'=>$it['intent_profile']];
$runtimeItems=[];$missingPostTargets=[];$wpById=[];foreach($byWp as $w)$wpById[$w['id']]=$w;
foreach($bySource['PPM679_EXISTING_EDITORIAL_RUNTIME'] as $it){$runtimeItems[$it['canonical_article_id']]=['canonical_article_id'=>$it['canonical_article_id'],'plan_slot_sha256'=>$it['plan_slot'],'post_id'=>$it['post_id'],'status'=>$it['status'],'category_slug'=>$it['category'],'article_type'=>$it['article_type'],'target_keyword'=>$it['target_keyword'],'title'=>''];if(!isset($wpById[$it['post_id']]))$missingPostTargets[]=$it['post_id'];}
// Emulate exactly the 9 formerly exported invalid rows from the actual user file:
// they contain only the literal title 'Array' and no further semantic hints.
$realEditorialNine=[];
foreach($bySource['EDITORIAL_PLAN'] as $r){
    $sourceRow=['title'=>'Array','primary_longtail_query'=>'Array','category_name'=>'','intent_cluster_id'=>'','headings'=>[],'source_reference'=>''];
    $raw=wp_json_encode($sourceRow,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
    assertPass(hash('sha256',$raw)===$r['raw_record_sha256'],'live_original_editorial_legacy_row_identical_'.$r['source_index']);
    $realEditorialNine[]=['title'=>'Array','primary_longtail_query'=>'Array','target_keyword'=>'','plan_slot'=>'','status'=>'PLANNED'];
}

$stubOptions=['ppm679_editorial_plan_runtime_state_v1'=>['items'=>$runtimeItems],
 'pste_mini_keyword_roundtrip_v1'=>['completed'=>$miniCompleted,'active'=>null,'clarification'=>[]],
 PSTE_OPTION_EDITORIAL_PLAN_IMPORT=>['items'=>array_map(fn($x)=>['title'=>$x['title'],'status'=>$x['status'],
 'target_keyword'=>$x['target_keyword'],'plan_slot'=>$x['plan_slot']],$realEditorialNine)]];
$wpdb=new StubDb($byWp,$byPste);
$simulateMissingPostFallback=false;
$before=json_encode($stubOptions);
$realReady=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($realReady['complete']===true&&preg_match('/^[a-f0-9]{64}$/D',$realReady['sha256'])===1,'real_1179_parkhouse_complete_with_protected_historic_artifacts');
assertPass(count($realReady['items'])===1179,'all_real_1179_records_including_nine_legacy_and_three_opaque_reservations');
$realSources=$realReady['sources'];
assertPass(count($realSources)===6&&$realSources['WORDPRESS']['item_count']===1024&&$realSources['PSTE_PLAN']['item_count']===1&&$realSources['EDITORIAL_PLAN']['item_count']===9&&$realSources['PSERC_ACTIVE_PLAN']['item_count']===1&&$realSources['PPM679_EXISTING_EDITORIAL_RUNTIME']['item_count']===144&&$realSources['MINI_RESERVED']['item_count']===0,'all_six_real_sources_and_counts_unchanged');
assertPass($realSources['WORDPRESS']['canonical_collision_count']===1
    &&count($realSources['WORDPRESS']['canonical_collisions'])===1,
    'real_wp_identity_inventory_detects_canonical_alias_reuse_in_two_different_articles');
$duplicateId=$realSources['WORDPRESS']['canonical_collisions'][0];
assertPass($duplicateId['post_ids']===[16029,972638],
    'actual_duplicate_canonical_is_specific_real_16029_and_972638_pair');
assertPass($realSources['EDITORIAL_PLAN']['source_origin']==='OPTION'&&$realSources['EDITORIAL_PLAN']['source_conflict']===false,'original_import_proven_from_option_in_local_exact_fixture');
assertPass($realSources['EDITORIAL_PLAN']['legacy_empty_count']===9&&$realSources['EDITORIAL_PLAN']['unresolved_count']===0,'nine_old_ghosts_classified_by_identity_not_count');
assertPass($realSources['PPM679_EXISTING_EDITORIAL_RUNTIME']['historical_orphan_count']===3&&$realSources['PPM679_EXISTING_EDITORIAL_RUNTIME']['unresolved_count']===0,'three_nonexistent_historic_posts_kept_as_technical_reservations');
$editorialRows=array_values(array_filter($realReady['items'],fn($x)=>$x['source']==='EDITORIAL_PLAN'));
assertPass(count($editorialRows)===9&&count(array_filter($editorialRows,fn($x)=>$x['status']==='LEGACY_EMPTY_PLACEHOLDER'&&$x['semantic_occupancy']==='NONE'))===9,'all_nine_ghosts_kept_but_not_active_article_entities');
assertPass($editorialRows[0]['raw_title_fields']['title']==='Array'&&strlen($editorialRows[0]['raw_record_sha256'])===64,'original_corrupt_fields_preserved_exactly');
$ppmRows=array_values(array_filter($realReady['items'],fn($x)=>$x['source']==='PPM679_EXISTING_EDITORIAL_RUNTIME'));
assertPass(count($ppmRows)===144&&count(array_filter($ppmRows,fn($x)=>$x['title_status']==='RESOLVED'))===141&&count(array_filter($ppmRows,fn($x)=>$x['title_status']==='HISTORICAL_ORPHAN_RESERVATION'))===3,'real_141_named_articles_and_three_historic_tombstones');
assertPass(count(array_filter($ppmRows,fn($x)=>$x['technical_reservation']===true&&preg_match('/^[a-f0-9]{64}$/D',$x['plan_slot'])===1))===144,'all_144_slots_technically_reserved_including_orphans');
assertPass(count(array_filter($ppmRows,fn($x)=>$x['semantic_occupancy']==='NONE'))===3,'historic_missing_posts_not_claimed_as_existing_article_content');
$slotOwner=array_values(array_filter($ppmRows,
    fn($x)=>(int)$x['post_id']===972638));
assertPass(count($slotOwner)===1&&$slotOwner[0]['title']==='Warum sagt man eigentlich „alte Schabracke“?'
    &&$slotOwner[0]['post_link_status']==='EXACT_SLOT_OWNER_WITH_DUPLICATE_CANONICAL_ALIAS',
    'one_matching_immutable_slot_wins_over_unrelated_canonical_only_alias_without_dropping_article');
$edSafe=PSTE_Snapshot::editorialPlan();
assertPass($edSafe['status']==='NOT_AVAILABLE'&&$edSafe['sha256']==='NOT_AVAILABLE'&&count($edSafe['items'])===0,'legacy_broken_import_no_longer_blocks_other_baseline_consumers');
$again=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($realReady['sha256']===$again['sha256']&&$before===json_encode($stubOptions),'real_ready_snapshot_stable_and_readonly');
assertPass(count($missingPostTargets)===3,'exactly_three_original_missing_post_ids');
$simDoc=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','owner'=>'EXTERNAL_SINGLE_SEO_EDITOR',
 'snapshot_sha256'=>str_repeat('a',64),'items'=>[]];
expectCode(fn()=>PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions(['completed'=>$miniCompleted],$simDoc,$realReady),
 'old_or_fake_snapshot_hash_never_reused','PSTE_MINI_SEO_PORTAL_PLAN_CHANGED_OR_INCOMPLETE');
// The external WP filter must never hide a DIFFERENT persisted editorial source.
$stubFilter=['items'=>[['title'=>'Filter plant einen echten Artikel','canonical_article_id'=>'article:filter']]];
$sourceClash=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($sourceClash['complete']===false&&str_contains($sourceClash['reason'],'EDITORIAL_PLAN_SOURCE_CONFLICT')&&$sourceClash['sources']['EDITORIAL_PLAN']['source_conflict']===true,'filter_cannot_silently_override_stored_option');
expectCode(fn()=>PSTE_Snapshot::editorialPlan(),'baseline_filter_option_conflict_rejected','PSTE_EDITORIAL_PLAN_SOURCE_CONFLICT');
$stubFilter=$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT];
$matched=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($matched['complete']===true&&$matched['sources']['EDITORIAL_PLAN']['source_origin']==='FILTER_AND_OPTION_IDENTICAL','matching_filter_and_option_safe_and_proven');
$stubFilter=null;
// A damaged row with ANY real identity, keyword or extra field must still stop clearance.
$originalEditorial=$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT];
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]['items'][0]['canonical_article_id']='article:real-reserved';
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'EDITORIAL_PLAN_UNRESOLVED:1'),'unknown_old_row_with_canonical_identity_never_silently_ignored');
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]=$originalEditorial;
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]['items'][0]['target_keyword']='regendecke pferd';
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'EDITORIAL_PLAN_UNRESOLVED:1'),'unknown_old_row_with_keyword_not_a_legacy_empty_ghost');
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]=$originalEditorial;
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]['items'][0]['unexpected_payload']='real_details';
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'EDITORIAL_PLAN_UNRESOLVED:1'),'unknown_old_row_with_extra_fields_blocks');
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]=$originalEditorial;
// Invalid source format or malformed row cannot masquerade as no plan.
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]=['new_unknown_format'=>['not_a_plan'=>'but_content']];
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'EDITORIAL_PLAN_UNRESOLVED:1')
    &&$unsafe['sources']['EDITORIAL_PLAN']['status']==='UNRECOGNIZED_FORMAT',
    'unexpected_nonempty_editorial_contract_never_silently_treated_as_no_plan');
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]=['items'=>array_merge($originalEditorial['items'],['MALFORMED_ROW'])];
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'EDITORIAL_PLAN_UNRESOLVED:1')
    &&$unsafe['sources']['EDITORIAL_PLAN']['item_count']===10,
    'scalar_import_rows_not_dropped_from_source_count');
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]=$originalEditorial;
// An uncreated planned slot and an identity collision cannot become a tombstone.
$originalRuntime=$stubOptions['ppm679_editorial_plan_runtime_state_v1'];
$firstOrphan=array_key_first(array_filter($originalRuntime['items'],fn($x)=>in_array((int)$x['post_id'],$missingPostTargets,true)));
$stubOptions['ppm679_editorial_plan_runtime_state_v1']['items'][$firstOrphan]['status']='PLANNED';
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'PPM679_RUNTIME_TITLE_UNRESOLVED:1'),'uncreated_new_plan_does_not_masquerade_as_historical_orphan');
$stubOptions['ppm679_editorial_plan_runtime_state_v1']=$originalRuntime;
$stubOptions['ppm679_editorial_plan_runtime_state_v1']['items'][$firstOrphan]['target_keyword']='ungeprüftes neues Thema';
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'PPM679_RUNTIME_TITLE_UNRESOLVED:1'),'titleless_plan_with_keyword_still_blocks_semantic_clearance');
$stubOptions['ppm679_editorial_plan_runtime_state_v1']=$originalRuntime;
$otherRuntime=array_keys($originalRuntime['items'])[1];
$stubOptions['ppm679_editorial_plan_runtime_state_v1']['items'][$firstOrphan]['plan_slot_sha256']=$originalRuntime['items'][$otherRuntime]['plan_slot_sha256'];
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'EXISTING_RUNTIME_DUPLICATE_PLAN_SLOT'),'duplicate_original_slots_block_complete_export');
$stubOptions['ppm679_editorial_plan_runtime_state_v1']=$originalRuntime;
// Changing original records changes the version fingerprint, never reuses approval.
$changed=$stubOptions['ppm679_editorial_plan_runtime_state_v1'];
$changed['items'][$firstOrphan]['post_id']=99999999;
$stubOptions['ppm679_editorial_plan_runtime_state_v1']=$changed;
$changedSnap=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($changedSnap['complete']&&$changedSnap['sha256']!==$realReady['sha256'],'source_change_rebinds_complete_snapshot_hash');
$stubOptions['ppm679_editorial_plan_runtime_state_v1']=$originalRuntime;
// A unique migrated WordPress ID may be re-associated only by SAME canonical AND slot.
$orphanRow=$originalRuntime['items'][$firstOrphan];
$relocated=['source'=>'WORDPRESS','id'=>974000,'title'=>'SYNTHETIC_MIGRATED_SAME_CANONICAL_AND_SLOT',
 'type'=>'post','status'=>'publish','slug'=>'migrated-test','modified_gmt'=>'2026-11-08 00:00:00',
 'categories'=>[],'target_keyword'=>'','canonical_article_id'=>$orphanRow['canonical_article_id'],
 'plan_slot'=>$orphanRow['plan_slot_sha256']];
$newWp=array_merge($byWp,[$relocated]);$bySource['WORDPRESS']=$newWp;$wpdb=new StubDb($newWp,$byPste);
$rebuilt=PSTE_Mini_Workflow::readParkhausForMini();
$relinked=array_values(array_filter($rebuilt['items'],fn($x)=>$x['source']==='PPM679_EXISTING_EDITORIAL_RUNTIME'&&$x['canonical_article_id']===$orphanRow['canonical_article_id']));
assertPass($rebuilt['complete']&&count($relinked)===1&&$relinked[0]['resolved_post_id']===974000&&$relinked[0]['title']==='SYNTHETIC_MIGRATED_SAME_CANONICAL_AND_SLOT','migrated_post_relinked_only_with_immutable_two_field_match');
assertPass($rebuilt['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']['historical_orphan_count']===2,'migration_reduces_orphans_without_losing_reservations');
$newWp[count($newWp)-1]['plan_slot']=str_repeat('b',64);$bySource['WORDPRESS']=$newWp;$wpdb=new StubDb($newWp,$byPste);
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'PPM679_RUNTIME_TITLE_UNRESOLVED:1'),'wrong_migrated_slot_never_guessed_by_canonical_alone');
// Identity collision coverage must work for reused WordPress post IDs and
// double-claimed exact canonical+slot, not just the real alias with empty slot.
$reusedWp=$byWp;foreach($reusedWp as &$r){if((int)$r['id']===972638){
    $r['canonical_article_id']='article:REUSED_OTHER_ID';break;
}}unset($r);
$bySource['WORDPRESS']=$reusedWp;$wpdb=new StubDb($reusedWp,$byPste);
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'PPM679_RUNTIME_TITLE_UNRESOLVED:1'),
    'recycled_wordpress_post_id_with_different_canonical_must_not_supply_foreign_title');
$collisionWp=$byWp;
$originalWP=null;foreach($byWp as $r){if((int)$r['id']===972638){$originalWP=$r;break;}}
assertPass(is_array($originalWP),'original_verified_article_present_in_wp_inventory');
$double=$originalWP;$double['id']=974001;$double['title']='SYNTHETIC_OWNERSHIP_COLLISION';
$collisionWp[]=$double;$bySource['WORDPRESS']=$collisionWp;$wpdb=new StubDb($collisionWp,$byPste);
$unsafe=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($unsafe['complete']===false&&str_contains($unsafe['reason'],'PPM679_RUNTIME_TITLE_UNRESOLVED:1'),
    'two_posts_with_same_canonical_and_same_plan_slot_do_not_get_silent_owner_assignment');
$bySource['WORDPRESS']=$byWp;$wpdb=new StubDb($byWp,$byPste);
$bySource['WORDPRESS']=$byWp;$wpdb=new StubDb($byWp,$byPste);
assertPass($wpdb->readCalls===0,'test_fixture_reset_before_owner_decisions');

$subjects=$real['seo_subjects'];$a=$subjects[0];$b=$subjects[1];$c=$subjects[2];
$titleByRaw=[];foreach($real['items'] as $row)$titleByRaw[$row['raw_query']]=$row['titles'][0]['title']??'';
$create=function($row,$box,$slot,$match='')use($titleByRaw){return ['pool_key'=>$row['pool_key'],
 'raw_query'=>$row['raw_query'],'source_sha256'=>$row['source_sha256'],'box'=>$box,
 'intent_summary'=>'Ausschließlich technischer Testbeleg','approved_title'=>$titleByRaw[$row['raw_query']],
 'intent_slot'=>$slot,'matched_ref'=>$match];};
$slot=hash('sha256','LOCAL_UNIQUE_ARTICLE_SLOT_UNOCCUPIED');
$doc=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','owner'=>'EXTERNAL_SINGLE_SEO_EDITOR',
 'snapshot_sha256'=>$realReady['sha256'],'items'=>[
 $create($a,'FREI',$slot),$create($b,'BELEGT','', 'WORDPRESS:'.$byWp[0]['id']),$create($c,'KLAERUNG','')]];
$input=['completed'=>$miniCompleted,'seo_decisions'=>[],'clarification'=>[]];
$realAccepted=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$doc,$realReady);
assertPass($realAccepted['seo_last_report']['counts']===['FREI'=>1,'BELEGT'=>1,'KLAERUNG'=>1],
 'technical_owner_acceptance_works_on_real_full_1179_snapshot_no_synthetic_source_rows');
$testOrphan=array_values(array_filter($ppmRows,fn($r)=>$r['title_status']==='HISTORICAL_ORPHAN_RESERVATION'))[0];
$forged=$doc;$forged['items'][1]=$create($b,'BELEGT','', 'PPM679_EXISTING_EDITORIAL_RUNTIME:'.$testOrphan['canonical_article_id']);
$fail=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$forged,$realReady);
assertPass($fail['seo_last_report']['counts']['KLAERUNG']===2&&($fail['clarification'][$b['pool_key']]['reason_code']??'')==='BELEGT_REFERENCE_NOT_IN_EXISTING_PARKHAUS',
 'historical_orphan_cannot_be_forged_as_existing_semantic_article');
$forged=$doc;$forged['items'][1]=$create($b,'BELEGT','', 'EDITORIAL_PLAN:EDITORIAL_PLAN:0');
$fail=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$forged,$realReady);
assertPass($fail['seo_last_report']['counts']['KLAERUNG']===2,'empty_legacy_placeholder_cannot_prove_an_existing_article');
$forged=$doc;$forged['items'][0]=$create($a,'FREI',$testOrphan['plan_slot']);
$fail=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($input,$forged,$realReady);
assertPass(($fail['clarification'][$a['pool_key']]['reason_code']??'')==='FREI_MISSING_OR_CONFLICTING_SOURCE_SLOT',
 'historic_missing_post_reserves_technical_slot_for_all_future_writes');

// Explicitly SYNTHETIC positive fixtures for the 9 old title-less records and
// the 3 WordPress posts not present in the user's exported inventory.
$stubOptions[PSTE_OPTION_EDITORIAL_PLAN_IMPORT]=['items'=>array_map(fn($i)=>[
 'title'=>['production_title'=>'SYNTHETIC_EDITORIAL_TITLE_'.($i+1)],
 'status'=>'PLANNED'],range(0,8))];
$simulateMissingPostFallback=true;
$parkRes=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($parkRes['complete']===true&&preg_match('/^[a-f0-9]{64}$/',$parkRes['sha256'])===1,'synthetic_complete_parkhaus_positive');
assertPass(count($parkRes['items'])===1179,'positive_fixture_same_1179_item_count');
$ppmRows=array_values(array_filter($parkRes['items'],fn($x)=>$x['source']==='PPM679_EXISTING_EDITORIAL_RUNTIME'));
assertPass(count($ppmRows)===144&&count(array_filter($ppmRows,fn($x)=>$x['title']!==''))===144,'positive_all_144_ppm_titles_explicit');
assertPass(count(array_filter($ppmRows,fn($x)=>str_starts_with($x['title'],'SYNTHETIC_')))===3,'positive_only_three_synthetic_post_titles');
assertPass(count(array_filter($ppmRows,fn($x)=>!str_starts_with($x['title'],'SYNTHETIC_')))===141,'positive_141_real_linked_wp_titles');
$before=json_encode($stubOptions);$second=PSTE_Mini_Workflow::readParkhausForMini();
assertPass($second['sha256']===$parkRes['sha256']&&$before===json_encode($stubOptions),'positive_fixture_readonly_deterministic');
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
echo "PASS TOTAL LOCAL REALDATA-BASED PHP WORKFLOW SIMULATION (3 synthetic missing posts only; live v24 source)\n";