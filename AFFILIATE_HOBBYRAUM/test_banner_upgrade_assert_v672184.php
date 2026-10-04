<?php
$GLOBALS['up_fail']=array(); $GLOBALS['up_pass']=array();
function uchk($cond,$name,$detail=''){ if($cond){$GLOBALS['up_pass'][]=$name;echo "PASS $name".($detail!==''?" :: $detail":"")."\n";}else{$GLOBALS['up_fail'][]=$name.($detail!==''?" :: $detail":"");echo "FAIL $name".($detail!==''?" :: $detail":"")."\n";}}
if(!class_exists('Pferdeportal_Affiliate_Router')){fwrite(STDERR,"FATAL plugin missing\n");exit(2);}
if(Pferdeportal_Affiliate_Router::VERSION!=='6.72.184'){fwrite(STDERR,"FATAL assert requires 6.72.184, got ".Pferdeportal_Affiliate_Router::VERSION."\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($name)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m;};
$call=function($name,...$args)use($rm,$o){return $rm($name)->invokeArgs($o,$args);};
$f=get_option('ppar_v672184_upgrade_fixture',array());
if(!is_array($f)||empty($f['sch'])){fwrite(STDERR,"FATAL fixture missing\n");exit(2);}
$http=0;
add_filter('pre_http_request',function($pre,$args,$url)use(&$http){$http++;return new WP_Error('upgrade_e2e_network_forbidden','network forbidden');},10,3);
$render=function($id,$slot)use($rm,$o){return (string)$rm('render_affiliate_slot')->invoke($o,$id,$slot,'portal_context','');};

// 1) New automatic contract is immediate: legacy automatic source can no longer win.
$preMigration=$render((int)$f['sch'],'product_after_category_tiles');
uchk(strpos($preMigration,'legacy-sanovet')===false,'automatic_pool_rejects_legacy_banner_before_migration');

// 2) This release must NOT restart the full 4000-row product/banner pool.
$call('ensure_full_pool_automation');
uchk((string)get_option('ppar_full_pool_automation_version_v1','')==='6.72.184','full_pool_version_marked_without_rescan');
uchk(wp_next_scheduled(Pferdeportal_Affiliate_Router::FULL_POOL_WORKER_HOOK)===false,'old_full_pool_event_cleared');
uchk(get_option('ppar_full_pool_automation_cursor_v1',null)===null,'old_full_pool_cursor_removed');

// 3) Banner-only migration to completion.
update_option(Pferdeportal_Affiliate_Router::OPTION_BANNER_LIBRARY_MIGRATION_STATE,'running',false);
delete_option(Pferdeportal_Affiliate_Router::OPTION_BANNER_LIBRARY_MIGRATION_CURSOR);
for($i=0;$i<20;$i++){
  $call('run_banner_library_migration_v672184');
  if((string)get_option(Pferdeportal_Affiliate_Router::OPTION_BANNER_LIBRARY_MIGRATION_STATE,'')==='done')break;
}
uchk((string)get_option(Pferdeportal_Affiliate_Router::OPTION_BANNER_LIBRARY_MIGRATION_STATE,'')==='done','banner_only_migration_completes');
$result=get_option('ppar_banner_library_migration_result_v672184',array());
uchk(absint($result['processed']??0)>=1,'banner_only_migration_processed_rows',wp_json_encode($result));

// 4) Real page output: relevant stored destination wins, old SanoVet disappears.
$after=$render((int)$f['sch'],'product_after_category_tiles');
uchk(strpos($after,'library-schabracken')!==false,'POST_UPGRADE_relevant_library_banner_visible',substr(strip_tags($after),0,160));
uchk(strpos($after,'legacy-sanovet')===false,'POST_UPGRADE_wrong_sanovet_absent');

global $wpdb;
$creativeTable=$call('creative_library_table');
$row=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$creativeTable} WHERE identity_hash=%s",(string)$f['library_identity']),ARRAY_A);
$targets=is_array($row)?json_decode((string)($row['topic_targets']??''),true):array();
$targets=is_array($targets)?$targets:array();
uchk(!empty($targets),'existing_banner_mapping_persisted');
uchk(strpos((string)($targets[0]['target_label']??''),'Schabracken')!==false,'existing_banner_mapped_to_schabracken',wp_json_encode($targets[0]??array()));

// 5) Manual fixed legacy exception must remain valid, but only on its fixed page.
$fixedHtml=$render((int)$f['fixed_page'],'product_after_category_tiles');
uchk(strpos($fixedHtml,'legacy-fixed-banner')!==false,'manual_fixed_legacy_exception_preserved');
$autoOther=$render((int)$f['other'],'product_after_category_tiles');
uchk(strpos($autoOther,'legacy-fixed-banner')===false,'manual_fixed_legacy_not_in_automatic_pool');

// 6) Product sentinels are byte-for-byte unchanged.
$p1=get_post_meta((int)$f['product1'],'ppar_campaign_data',true); $p2=get_post_meta((int)$f['product2'],'ppar_campaign_data',true);
uchk(hash('sha256',serialize($p1))===(string)$f['product1_hash'],'ebay_product_campaign_unchanged');
uchk(hash('sha256',serialize($p2))===(string)$f['product2_hash'],'idealo_product_campaign_unchanged');

// 7) Future banner follows same library path.
$raw=array(
  'creative_id'=>'future-reithelme-184','creative_type'=>'banner','creative_title'=>'Reithelme Future',
  'creative_description'=>'','creative_tag'=>'Reithelme Pferd',
  'image_source'=>'https://example.com/future-reithelme-184.jpg',
  'destination_url'=>'https://example.com/ohne-treffer-upgrade-e2e/',
  'tracking_url'=>'https://example.com/future-reithelme-184-click',
  'width'=>'1200','height'=>'120','status'=>'active'
);
$mapping=$call('creative_library_detect_mapping',array_keys($raw));
$norm=$call('creative_library_normalize_row',$raw,$mapping,array(
  'provider'=>'manual','partner_external_id'=>'partner-future','partner_name'=>'Future Partner','source_kind'=>'banner','run_uuid'=>'future-184'
));
if(is_wp_error($norm)){fwrite(STDERR,"FATAL future normalize\n");exit(2);}
$norm['width']=1200;$norm['height']=120;$norm['topic_status']='auto_verified';
$payload=json_decode((string)$norm['payload'],true);$payload=is_array($payload)?$payload:array();
$payload['_dimension_state']='verified';$payload['_image_sha256']=hash('sha256','future-reithelme-184');$payload['_measured_at']=time();
$norm['payload']=wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
$up=$call('creative_library_upsert',$norm);
uchk(in_array($up,array('imported','updated','unchanged'),true),'future_banner_enters_same_library');
$futureRow=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$creativeTable} WHERE identity_hash=%s",$norm['identity_hash']),ARRAY_A);
$planned=$call('output_plan_creative',$futureRow,true);
uchk(absint($planned['active']??0)>0,'future_banner_materialized_active');
$futureHtml=$render((int)$f['other'],'product_after_category_tiles');
uchk(strpos($futureHtml,'future-reithelme-184')!==false,'future_banner_visible_from_stored_mapping');

// 8) Runtime performance guard: no network activity anywhere in migration/render path.
uchk($http===0,'complete_upgrade_gate_zero_remote_http','http_calls='.$http);

// 9) Hook scope: migration is admin/background only, never init/frontend.
uchk(has_action('admin_init',array($o,'ensure_banner_library_migration_v672184'))!==false,'migration_bound_to_admin_init');
uchk(has_action(Pferdeportal_Affiliate_Router::BANNER_LIBRARY_MIGRATION_HOOK,array($o,'run_banner_library_migration_v672184'))!==false,'migration_bound_to_background_hook');

echo "SUMMARY passes=".count($GLOBALS['up_pass'])." failures=".count($GLOBALS['up_fail'])."\n";
if($GLOBALS['up_fail']){echo "FAILURES ".wp_json_encode($GLOBALS['up_fail'])."\n";exit(1);}
echo "FULL_672183_TO_672184_BANNER_MIGRATION_E2E_PASS\n";
