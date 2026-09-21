<?php
if(!defined('ABSPATH')){fwrite(STDERR,"ABSPATH missing\n");exit(1);}
if(!class_exists('PSTE_Plugin')){fwrite(STDERR,"PSTE not loaded\n");exit(1);}

PSTE_Repository::createSchema();
update_option(PSTE_OPTION_SCHEMA,'12',false);
update_option(PSTE_OPTION_EDITORIAL_REBUILD_MARKER,PSTE_Editorializer::RULESET,false);
update_option(PSTE_OPTION_EDITORIAL_REBUILD_REPORT,[
    'contract'=>'PSTE_EDITORIAL_METADATA_REBUILD_AUDIT_V1',
    'ruleset'=>PSTE_Editorializer::RULESET,
    'report'=>['contract'=>PSTE_Editorializer::RULESET]
],false);
$marker=['contract'=>'PSTE_SAFE_MIGRATION_PROTOCOL_MARKER_V1','protocol'=>PSTE_SAFE_MIGRATION_PROTOCOL,'updated_at_utc'=>gmdate('c')];
$marker['sha256']=hash('sha256',wp_json_encode($marker,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRESERVE_ZERO_FRACTION));
update_option(PSTE_OPTION_SAFE_MIGRATION_PROTOCOL,$marker,false);
update_option(PSTE_OPTION_BOOT_STATUS,[
    'contract'=>'PSTE_SAFE_BOOT_STATUS_V1','status'=>'READY','stage'=>'READY','error_code'=>'','message'=>'E2E READY',
    'version'=>PSTE_VERSION,'schema'=>'12','updated_at_utc'=>gmdate('c'),'details'=>[]
],false);

$settings=PSTE_Plugin::defaults();
$settings['feature_enabled']=true;
$settings['environment']='sandbox';
$settings['run_budget_usd']=50.0;
$settings['absolute_ceiling_usd']=100.0;
$settings['daily_budget_usd']=100.0;
$settings['monthly_budget_usd']=1000.0;
update_option(PSTE_OPTION_SETTINGS,$settings,false);
PSTE_Credentials::saveFromAdmin('e2e-login','e2e-password');

$fixture=json_decode(file_get_contents(WP_PLUGIN_DIR.'/portal-seo-topic-engine/fixtures/portal-category-map-v1.json'),true);
if(!is_array($fixture)||empty($fixture['entries']))throw new RuntimeException('FIXTURE_INVALID');

$byProduct=[];
foreach($fixture['entries'] as $e){
    if(!is_array($e))continue;
    $p=(string)($e['product_page_slug']??'');
    if($p==='')continue;
    $byProduct[$p][]=$e;
}
$wanted=['heutaschen'];
foreach(array_keys($byProduct) as $p){
    if(count($wanted)>=80)break;
    if(!in_array($p,$wanted,true))$wanted[]=$p;
}

$pageIds=[];
$ensurePage=function(string $slug,string $name,int $parent=0) use (&$pageIds){
    $key=$slug.'|'.$parent;
    if(isset($pageIds[$key]))return $pageIds[$key];
    $existing=get_page_by_path($slug,OBJECT,'page');
    if($existing){$pageIds[$key]=(int)$existing->ID;return (int)$existing->ID;}
    $id=wp_insert_post(['post_type'=>'page','post_status'=>'publish','post_title'=>$name,'post_name'=>$slug,'post_parent'=>$parent],true);
    if(is_wp_error($id))throw new RuntimeException('PAGE_CREATE_'.$id->get_error_code());
    $pageIds[$key]=(int)$id;
    return (int)$id;
};

foreach($wanted as $product){
    foreach($byProduct[$product] as $e){
        $main=$ensurePage((string)$e['main_hub_slug'],(string)$e['main_hub_name'],0);
        $section=$ensurePage((string)$e['section_hub_slug'],(string)$e['section_hub_name'],$main);
        $ensurePage((string)$e['product_page_slug'],(string)$e['product_page_name'],$section);
        $exists=term_exists((string)$e['category_slug'],'category');
        if(!$exists){
            $r=wp_insert_term((string)$e['category_name'],'category',['slug'=>(string)$e['category_slug']]);
            if(is_wp_error($r))throw new RuntimeException('TERM_CREATE_'.$r->get_error_code());
        }
    }
}

update_option(PSTE_OPTION_EDITORIAL_PLAN_IMPORT,['items'=>[]],false);
$baseline=PSTE_Runner::captureSiteBaseline();
if(($baseline['status']??'')!=='CURRENT')throw new RuntimeException('BASELINE_NOT_CURRENT_'.($baseline['status']??''));

$contextStart=PSTE_Context_Refresh::start($baseline,'E2E_REAL_WORDPRESS');
if(!in_array((string)($contextStart['status']??''),['PENDING','RUNNING','COMPLETE'],true)){
    throw new RuntimeException('CONTEXT_START_FAILED_'.(string)($contextStart['error_code']??$contextStart['status']??''));
}

for($i=0;$i<500;$i++){
    $s=PSTE_Context_Refresh::status();
    if(($s['status']??'')==='COMPLETE')break;
    if(($s['status']??'')==='BLOCKED'){
        throw new RuntimeException('CONTEXT_BLOCKED_'.(string)($s['error_code']??'').'__'.(string)($s['error_message']??''));
    }
    PSTE_Context_Refresh::processBatch();
}

$ctx=PSTE_Context_Refresh::status();
if(($ctx['status']??'')!=='COMPLETE')throw new RuntimeException('CONTEXT_NOT_COMPLETE_'.($ctx['status']??''));

$term=get_term_by('slug','heutaschen-beratung','category');
if(!$term)throw new RuntimeException('HEUTASCHEN_TERM_MISSING');

update_option('pste_e2e_heutaschen_term_id',(int)$term->term_id,false);
delete_option(PSTE_OPTION_ACTIVE_RESEARCH_JOB);
delete_option(PSTE_OPTION_BREADTH_RESEARCH_QUEUE);
delete_option(PSTE_OPTION_RESEARCH_DRIVER_STATE);
delete_option(PSTE_OPTION_RESEARCH_DRIVER_LOCK);
delete_option(PSTE_OPTION_RESEARCH_STEP_LOCK);
delete_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK);
delete_option('pste_e2e_provider_counts');
delete_option('pste_e2e_paa_ready_count');
update_option('pste_e2e_provider_mode','normal',false);

echo wp_json_encode([
    'ready'=>PSTE_Plugin::isReady(),
    'baseline_status'=>$baseline['status'],
    'context_status'=>$ctx['status'],
    'term_id'=>(int)$term->term_id,
    'family_count'=>count($wanted)
],JSON_UNESCAPED_SLASHES)."\n";
