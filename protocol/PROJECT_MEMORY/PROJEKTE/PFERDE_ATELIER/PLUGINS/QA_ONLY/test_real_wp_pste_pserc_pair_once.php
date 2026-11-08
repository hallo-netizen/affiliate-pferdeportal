<?php
/** QA ONLY. Read-only single check in REAL isolated WordPress+MySQL with BOTH
 * COMPLETE original plugin trees already activated.
 * wp eval-file THIS_FILE boot     : verifies both real plugins; the real plan may be absent.
 * wp eval-file THIS_FILE complete : additionally requires the full saved real plan.
 * No production, no K0 write, no repeated semantic SEO check.
 */
if(!defined('ABSPATH')||!function_exists('get_option'))
    throw new RuntimeException('ACTUAL_WORDPRESS_REQUIRED');
$qaMode=(string)($args[0]??'');
if(!in_array($qaMode,['boot','complete'],true))
    throw new RuntimeException('EXPLICIT_SINGLE_PAIR_TEST_MODE_REQUIRED');
function pstePsercPairCheck(bool $ok,string $label):void {
    if(!$ok)throw new RuntimeException('PAIR_CHECK_FAILED_'.$label);
    echo 'PASS '.$label."\n";
}
pstePsercPairCheck(class_exists('PSTE_Mini_Workflow')
    &&class_exists('PSERC_Plan_Snapshot_Store')
    &&class_exists('PSERC_SEO_Source_Binding'),
    'both real plugin class trees loaded in same WordPress');
pstePsercPairCheck(defined('PSERC_VERSION')&&PSERC_VERSION==='0.28.55',
    'correct PSERC runtime version');
require_once ABSPATH.'wp-admin/includes/plugin.php';
// A loaded PHP class alone is not proof that WordPress activated a complete plugin.
// Verify PSERC's exact entrypoint plus PSTE's loaded class under an activated plugin.
$psEntry=plugin_basename(PSERC_DIR.'portal-seo-editorial-plan-compiler.php');
pstePsercPairCheck(is_plugin_active($psEntry),'complete PSERC WordPress plugin is active');
$psteFile=(new ReflectionClass('PSTE_Mini_Workflow'))->getFileName();
$psteFile=is_string($psteFile)?realpath($psteFile):false;
$psteIsActive=false;
foreach((array)get_option('active_plugins',[]) as $activeEntry){
    $pluginRoot=dirname((string)$activeEntry);
    if($pluginRoot==='.')continue;
    $realRoot=realpath(WP_PLUGIN_DIR.'/'.$pluginRoot);
    if($psteFile&&$realRoot&&str_starts_with($psteFile,$realRoot.DIRECTORY_SEPARATOR)){
        $psteIsActive=true;
        break;
    }
}
pstePsercPairCheck($psteIsActive,'complete PSTE WordPress plugin is active');
$meta=get_plugin_data(PSERC_DIR.'portal-seo-editorial-plan-compiler.php',false,false);
pstePsercPairCheck(($meta['Version']??'')===PSERC_VERSION,
    'WordPress backend plugin version equals PSERC runtime');
$integrity=PSERC_Package_Integrity::validate();
pstePsercPairCheck(!empty($integrity['ok'])
    &&(int)($integrity['required_file_count']??0)===61,
    'full original PSERC plugin integrity');
$binding=PSERC_SEO_Source_Binding::validate();
pstePsercPairCheck(!empty($binding['ok']),
    'original PSTE and PSERC read-capability binding');
$park=PSTE_Mini_Workflow::readParkhausForMini();
$s=(array)($park['sources']??[]);
echo 'ACTUAL_WP_PAIR_SINGLE_PARKHAUS '.wp_json_encode([
    'complete'=>$park['complete']??false,
    'reason'=>$park['reason']??'',
    'counts'=>[
        'WORDPRESS'=>$s['WORDPRESS']['item_count']??null,
        'PSTE_PLAN'=>$s['PSTE_PLAN']['item_count']??null,
        'PSERC_ACTIVE_PLAN'=>$s['PSERC_ACTIVE_PLAN']['item_count']??null,
        'PPM679_EXISTING_EDITORIAL_RUNTIME'=>$s['PPM679_EXISTING_EDITORIAL_RUNTIME']['item_count']??null,
    ],
    'ppm679_status'=>$s['PPM679_EXISTING_EDITORIAL_RUNTIME']['status']??null,
],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
if($qaMode==='complete'){
    pstePsercPairCheck(!empty($park['complete'])
        &&($s['PPM679_EXISTING_EDITORIAL_RUNTIME']['status']??'')==='PRESENT'
        &&(int)($s['PPM679_EXISTING_EDITORIAL_RUNTIME']['item_count']??0)>0,
        'single complete original source export; no missing/empty saved PPM679 plan');
    echo "REAL_WP_PAIR_FULL_SOURCE_QA_PASS; READ_ONLY; NO ARTICLE OR K0 WRITES\n";
}else{
    // Two complete plugins can be activated before an actual original PSERC plan exists.
    // Never misreport this technical success as an approved production source.
    echo "REAL_WP_PAIR_BOOT_QA_PASS; REAL_EDITORIAL_SOURCE_NOT_ASSERTED; READ_ONLY\n";
}
