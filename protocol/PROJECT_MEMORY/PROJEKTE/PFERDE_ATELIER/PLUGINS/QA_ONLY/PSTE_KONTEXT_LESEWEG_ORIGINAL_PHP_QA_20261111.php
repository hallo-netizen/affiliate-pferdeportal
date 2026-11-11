<?php
declare(strict_types=1);
/** Read-only regression on ORIGINAL PSTE class; mock WordPress options. */
define('ABSPATH','/test-not-wordpress/');
define('PSTE_OPTION_CONTEXT_INDEX_MANIFEST','pste_context_index_manifest_v2');
$GLOBALS['wpopts']=[];$GLOBALS['wpwrites']=0;$GLOBALS['checks']=0;
function get_option($key,$default=false){return $GLOBALS['wpopts'][$key]??$default;}
function update_option($key,$value,$autoload=false){$GLOBALS['wpwrites']++;$GLOBALS['wpopts'][$key]=$value;return true;}
function delete_option($key){$GLOBALS['wpwrites']++;unset($GLOBALS['wpopts'][$key]);return true;}
function check($b,$msg){$GLOBALS['checks']++;if(!$b)throw new RuntimeException($msg);}
require '/mnt/data/psqa/qa_combined/packaged_qa/Portal SEO Topic Engine/includes/class-pste-context-index-store.php';
$uuid='377882b4-3b15-4a52-b435-6cac32bda17b';
// These hashes come from user's genuine 2026-11-09 context export; artifact itself is simulated.
$baseline=['contract'=>'PSTE_SITE_BASELINE_V1','baseline_sha256'=>'41840fd1b35afee99cf7994e8b0f5ddb76532895fcdc9f99f4c90333503a8323','inventory_sha256'=>'5d26c41f8546e0611799330d1769204adece3b084b671b9b6b21160f56aa6000','structure_sha256'=>'a89b3a689c1cd1475bf3e6e558e6df77917571692595512e0551961e69509398','editorial_plan_sha256'=>'3986590a30c65c0e749ceec027e5ebdb6f04128f577d1ec32dc89351083c74a0'];
$job=['status'=>'COMPLETE','job_uuid'=>$uuid,'context_index_manifest_sha256'=>'','inventory_sha256'=>$baseline['inventory_sha256'],'structure_sha256'=>$baseline['structure_sha256'],'editorial_plan_sha256'=>$baseline['editorial_plan_sha256']];
$manifest=['contract'=>PSTE_Context_Index_Store::CONTRACT,'job_uuid'=>$uuid,'baseline_sha256'=>$baseline['baseline_sha256'],'inventory_sha256'=>$baseline['inventory_sha256'],'structure_sha256'=>$baseline['structure_sha256'],'editorial_plan_sha256'=>$baseline['editorial_plan_sha256'],'family_to_shard'=>[],'shards'=>[],'family_count'=>0,'shard_count'=>0];
$ref=new ReflectionMethod(PSTE_Context_Index_Store::class,'manifestHash');$manifest['manifest_sha256']=$ref->invoke(null,$manifest);$GLOBALS['wpopts'][PSTE_OPTION_CONTEXT_INDEX_MANIFEST]=$manifest;
$expected=0;
for($i=0;$i<120;$i++){
 $b=PSTE_Context_Index_Store::runtimeBinding($job,$baseline);
 check(($b['contract']??'')==='PSTE_CONTEXT_INDEX_RUNTIME_BINDING_V2','binding contract');
 check(($b['manifest_sha256']??'')===$manifest['manifest_sha256'],'manifest identity');
 check($GLOBALS['wpwrites']===$expected,'unexpected write on valid reader');
}
$cases=[];
function failureCase($label,array $value,array $job,array $baseline){
 $GLOBALS['wpopts'][PSTE_OPTION_CONTEXT_INDEX_MANIFEST]=$value;
 $old=$GLOBALS['wpwrites'];$blocked=false;
 try{PSTE_Context_Index_Store::runtimeBinding($job,$baseline);}catch(Throwable $e){$blocked=true;}
 check($blocked,$label.' should fail');check($GLOBALS['wpwrites']===$old,$label.' mutated WP');
 return $label;
}
$cases[]=failureCase('missing manifest',[],$job,$baseline);
$mod=$manifest;$mod['family_count']=1;$cases[]=failureCase('corrupt manifest hash',$mod,$job,$baseline);
$mod=$manifest;$mod['editorial_plan_sha256']=str_repeat('f',64);$mod['manifest_sha256']=$ref->invoke(null,$mod);$cases[]=failureCase('plan identity drift',$mod,$job,$baseline);
$mod=$manifest;$mod['inventory_sha256']=str_repeat('f',64);$mod['manifest_sha256']=$ref->invoke(null,$mod);$cases[]=failureCase('inventory identity drift',$mod,$job,$baseline);
$mod=$manifest;$mod['job_uuid']='different';$mod['manifest_sha256']=$ref->invoke(null,$mod);$cases[]=failureCase('job identity drift',$mod,$job,$baseline);
$mod=$manifest;$mod['family_count']=1;$mod['manifest_sha256']=$ref->invoke(null,$mod);$cases[]=failureCase('family count drift',$mod,$job,$baseline);
$mod=$manifest;$mod['shard_count']=1;$mod['manifest_sha256']=$ref->invoke(null,$mod);$cases[]=failureCase('shard count drift',$mod,$job,$baseline);
$mod=$manifest;$mod['contract']='forged';$mod['manifest_sha256']=$ref->invoke(null,$mod);$cases[]=failureCase('invalid contract',$mod,$job,$baseline);
$mod=$manifest;$mod['structure_sha256']=str_repeat('e',64);$mod['manifest_sha256']=$ref->invoke(null,$mod);$cases[]=failureCase('structure identity drift',$mod,$job,$baseline);
$mod=$manifest;$mod['manifest_sha256']=str_repeat('0',64);$cases[]=failureCase('invalid declared signature',$mod,$job,$baseline);
check($GLOBALS['wpwrites']===0,'all reads are read-only');
echo json_encode(['status'=>'PASS','real_plugin_class'=>'PSTE_Context_Index_Store::runtimeBinding','checks'=>$GLOBALS['checks'],'positive_repeats'=>120,'negative_cases'=>$cases,'writes'=>0,'fixture'=>'synthetic options with authentic 2026-11-09 context hash values','live_wp_test'=>false],JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE)."\n";