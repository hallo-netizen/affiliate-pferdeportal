<?php
/** One-time QA for the COMPLETE original PSERC 0.28.55 plugin package.
 * Run: php this.php EXTRACTED_PSERC_PLUGIN_ROOT frontend|admin
 * Uses test stubs for WordPress hooks. This is not a real WordPress installation.
 * No additional runtime worker, no K0, no PPM679 plan modifications.
 */
declare(strict_types=1);
define('ABSPATH','/qa/');
$GLOBALS['qa_admin']=(($argv[2]??'')==='admin');
$GLOBALS['qa_hooks']=[];
function is_admin():bool{return (bool)$GLOBALS['qa_admin'];}
function add_action($name,$callable,$priority=10,$arguments=1):bool {
    $GLOBALS['qa_hooks'][]=[
        'name'=>$name,
        'callback'=>is_array($callable)?implode('::',array_map('strval',$callable)):(is_string($callable)?$callable:'closure'),
        'priority'=>$priority
    ];
    return true;
}
function add_filter($name,$callable,$priority=10,$arguments=1):bool {
    return add_action($name,$callable,$priority,$arguments);
}
$root=rtrim((string)($argv[1]??''),'/');
if(!is_file($root.'/portal-seo-editorial-plan-compiler.php'))
    throw new RuntimeException('FULL_ORIGINAL_PSERC_QA_PACKAGE_REQUIRED');
require $root.'/portal-seo-editorial-plan-compiler.php';
if(PSERC_VERSION!=='0.28.55'||PSERC_BUILD!=='0.28.55-one-owner-no-fallback')
    throw new RuntimeException('WRONG_PSERC_RUNTIME_VERSION');
$header=(string)file_get_contents($root.'/portal-seo-editorial-plan-compiler.php');
if(preg_match('/\\* Version:\\s*([^\\s]+)/',$header,$m)!==1||$m[1]!==PSERC_VERSION)
    throw new RuntimeException('WORDPRESS_VISIBLE_VERSION_DIFFERS_FROM_RUNTIME');
$binding=PSERC_Package_Integrity::validate();
if(empty($binding['ok'])||(int)$binding['required_file_count']!==61)
    throw new RuntimeException('PSERC_ORIGINAL_PACKAGE_BINDING_FAILED');
foreach(['PSERC_Plan_Compile_Job','PSERC_Production_Trigger','PSERC_SEO_Reader'] as $class)
    if(!class_exists($class))throw new RuntimeException('MISSING_ORIGINAL_PSERC_CLASS_'.$class);
$hooks=array_column($GLOBALS['qa_hooks'],'name');
foreach(['admin_post_pserc_import_system4_drafts',
         'admin_post_pserc_run_approved_normal_draft',
         'wp_ajax_pserc_plan_compile_start',
         'wp_ajax_pserc_plan_compile_advance'] as $hook) {
    if(in_array($hook,$hooks,true)!==(bool)$GLOBALS['qa_admin'])
        throw new RuntimeException('WRONG_WP_HOOK_'.$hook);
}
foreach(['save_post_post','before_delete_post','plugins_loaded','updated_option'] as $hook)
    if(!in_array($hook,$hooks,true))
        throw new RuntimeException('MISSING_ORIGINAL_WP_HOOK_'.$hook);
echo "PASS original complete PSERC v0.28.55 WP-like plugin bootstrap in ".
    ($GLOBALS['qa_admin']?'admin':'frontend').
    " mode: 61 package files, ".count($hooks).
    " original WP hooks, WordPress header/runtime versions identical. NO REAL WP CLAIM.\n";
