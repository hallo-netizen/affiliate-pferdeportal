<?php
declare(strict_types=1);
define('ABSPATH','/wp/');
$GLOBALS['read_terms']=[100=>(object)['term_id'=>100,'slug'=>'beratung-foo','taxonomy'=>'category'],101=>(object)['term_id'=>101,'slug'=>'journal-bar','taxonomy'=>'category']];
$GLOBALS['opts']=['pste_site_baseline_v1'=>['contract'=>'PSTE_SITE_BASELINE_V1','structure_sha256'=>str_repeat('a',64)]];
function get_term($id,$tax){return $GLOBALS['read_terms'][$id]??false;}
function get_option($name,$default=[]){return $GLOBALS['opts'][$name]??$default;}
function is_wp_error($o){return false;}
// This is the ORIGINAL metadata-path class from the unchanged PSTE tree.
// Its payload binding helper only needs the original editorial query reader.
final class PSTE_Editorializer {public static function sourceQuery(array $a): string {return (string)($a['raw_query']??'');}}
require __DIR__.'/../texterstellung/original/pste/includes/class-pste-normal-metadata-path.php';
require __DIR__.'/../texterstellung/includes/class-txe-legacy-source-bridge.php';
$r=new ReflectionMethod(TXE_Legacy_Source_Bridge::class,'savedMetadata');$r->setAccessible(true);
$tests=[];
$run=function(string $name,array $row,array $candidate,?array $expected) use(&$tests,$r){$actual=$r->invoke(null,$row,$candidate);$tests[$name]=$actual===$expected;if(!$tests[$name])fwrite(STDERR,"FAIL $name ".json_encode($actual)."\n");};
$base=['manual_status'=>'REASSIGNED','manual_category_id'=>100,'manual_article_type'=>'Beratung','current_category_id'=>100,'reviewed_by'=>2,'context_state'=>'PENDING'];
$expected=['category_slug'=>'beratung-foo','article_type'=>'Beratung'];
$run('original_REASSIGNED_single_confirmed_owner',$base,[],$expected);
$run('original_REASSIGNED_without_reviewer_held',array_replace($base,['reviewed_by'=>0]),[],null);
$run('original_REASSIGNED_wrong_current_category_held',array_replace($base,['current_category_id'=>101]),[],null);
$run('APPROVED_is_not_a_category_vote',array_replace($base,['manual_status'=>'APPROVED']),[],null);
$run('no_existing_category_held',array_replace($base,['manual_category_id'=>999,'current_category_id'=>999]),[],null);
$path=['contract'=>'PSTE_NORMAL_METADATA_PATH_V2','status'=>'NORMAL_PASS','ok'=>true,'editorial_area'=>'FACH',
    'raw_query'=>'horseware regendecken','raw_query_sha256'=>hash('sha256','horseware regendecken'),
    'target_category'=>['term_id'=>100,'slug'=>'beratung-foo'],'article_type'=>'Beratung'];
$payload=['raw_query'=>'horseware regendecken','normal_metadata_path'=>$path,'proposed_article_type'=>'Beratung'];
$auto=['manual_status'=>'','context_state'=>'CURRENT','current_category_id'=>100,'structure_sha256'=>str_repeat('a',64)];
// The actual PSTE baseline option constant must be used (its value differs by versions).
define('PSTE_OPTION_SITE_BASELINE','pste_site_baseline_v1');
$run('original_normal_path_without_old_PPM_planning_gate',$auto,$payload,$expected);
$run('normal_path_invalid_source_query_held',$auto,array_replace($payload,['raw_query'=>'unrelated']),null);
$run('normal_path_stale_structure_held',array_replace($auto,['structure_sha256'=>str_repeat('b',64)]),$payload,null);
$run('normal_path_missing_term_held',array_replace($auto,['current_category_id'=>999]),$payload,null);
$run('normal_path_article_type_disagreement_held',$auto,array_replace($payload,['proposed_article_type'=>'Kosten']),null);
$run('normal_path_open_category_review_held',$auto,array_replace($payload,['normal_metadata_path'=>array_replace($path,['status'=>'STRUCTURE_GAP','ok'=>false])]),null);
$run('normal_path_undecided_area_held',$auto,array_replace($payload,['normal_metadata_path'=>array_replace($path,['editorial_area'=>'UNDECIDED'])]),null);
$passed=count(array_filter($tests));echo json_encode(['status'=>$passed===count($tests)?'PASS':'FAIL','tests'=>$passed,'total'=>count($tests),'checks'=>$tests],JSON_PRETTY_PRINT),"\n";
exit($passed===count($tests)?0:1);
