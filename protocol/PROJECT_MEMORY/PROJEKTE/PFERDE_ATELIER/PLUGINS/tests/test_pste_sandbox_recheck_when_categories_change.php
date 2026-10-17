<?php
declare(strict_types=1);
error_reporting(E_ALL);
define('ABSPATH','/tmp/');define('DAY_IN_SECONDS',86400);define('PSTE_VERSION','0.57.103');
define('PSTE_OPTION_SITE_BASELINE','pste_baseline');
function get_option(string $key,$default=false){return $GLOBALS['options'][$key]??$default;}
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
class PSTE_Plugin { public static function assertReady():void{} }
class PSTE_Editorializer { public const RULESET='CURRENT_TITLE_RULESET'; }
class PSTE_Article_Type_Registry { public static function build(array $b):array{return ['registry_sha256'=>'VALID'];} }
class PSTE_Snapshot { public static int $inventoryCalls=0;public static function inventory():array{self::$inventoryCalls++;return [];} }
require (getenv('PSTE_SOURCE_DIR')?:'/mnt/data/seo_work/modified/Portal SEO Topic Engine').'/includes/class-pste-semantic-review-sandbox.php';
$c='PSTE_Semantic_Review_Sandbox';
$bind=new ReflectionMethod($c,'internalStructureRecheckBinding');
$context=new ReflectionProperty($c,'admissionBatchContext');
$baseline=['contract'=>'PSTE_SITE_BASELINE_V1','structure_sha256'=>str_repeat('a',64),'protected_category_map_sha256'=>str_repeat('c',64)];
$GLOBALS['options']['pste_baseline']=$baseline;
$stored=['records'=>[],'job'=>null,'last_internal_structure_recheck_at_utc'=>gmdate('c'), 'last_internal_structure_recheck_binding_sha256'=>$bind->invoke(null,$baseline)];
$context->setValue(null,['store'=>$stored,'dirty'=>false]);
function assertCase(bool $ok,string $msg){if(!$ok)throw new RuntimeException($msg);}
$r=$c::refreshInternalStructureBacklog(false);
assertCase($r['status']==='NOT_DUE'&&PSTE_Snapshot::$inventoryCalls===0,'unchanged same-day baseline wrongly retriggered');
$baseline['structure_sha256']=str_repeat('b',64);$GLOBALS['options']['pste_baseline']=$baseline;
$r=$c::refreshInternalStructureBacklog(false);
assertCase($r['status']==='PASS'&&PSTE_Snapshot::$inventoryCalls===1,'new structure not automatically retriggered');
$state=$context->getValue();
assertCase($state['store']['last_internal_structure_recheck_binding_sha256']===$bind->invoke(null,$baseline),'new binding not durably selected');
$r=$c::refreshInternalStructureBacklog(false);
assertCase($r['status']==='NOT_DUE'&&PSTE_Snapshot::$inventoryCalls===1,'unchanged structure caused duplicate scan');
$baseline['protected_category_map_sha256']=str_repeat('d',64);$GLOBALS['options']['pste_baseline']=$baseline;
$r=$c::refreshInternalStructureBacklog(false);
assertCase($r['status']==='PASS'&&PSTE_Snapshot::$inventoryCalls===2,'new category map not automatically retriggered');
$r=$c::refreshInternalStructureBacklog(true);
assertCase($r['status']==='PASS'&&PSTE_Snapshot::$inventoryCalls===3,'force recheck blocked');
echo "PASS current structure => NOT_DUE; changed structure => PASS; same structure => NOT_DUE; changed category => PASS; force => PASS; 0 new provider calls\n";