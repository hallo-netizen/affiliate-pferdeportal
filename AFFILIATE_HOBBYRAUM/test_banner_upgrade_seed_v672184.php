<?php
$GLOBALS['seed_fail']=array(); $GLOBALS['seed_pass']=array();
function schk($cond,$name,$detail=''){ if($cond){$GLOBALS['seed_pass'][]=$name;echo "PASS $name".($detail!==''?" :: $detail":"")."\n";}else{$GLOBALS['seed_fail'][]=$name.($detail!==''?" :: $detail":"");echo "FAIL $name".($detail!==''?" :: $detail":"")."\n";}}
if(!class_exists('Pferdeportal_Affiliate_Router')){fwrite(STDERR,"FATAL plugin missing\n");exit(2);}
if(Pferdeportal_Affiliate_Router::VERSION!=='6.72.184'){fwrite(STDERR,"FATAL seed requires 6.72.184, got ".Pferdeportal_Affiliate_Router::VERSION."\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($name)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m;};
$call=function($name,...$args)use($rm,$o){return $rm($name)->invokeArgs($o,$args);};
update_option('ppar_enabled','1',false);
update_option('ppar_assignments_v1',array(),false);
$call('maybe_install_creative_library_schema');
$call('maybe_install_output_objects_schema');
$mkpage=function($title,$slug,$parent=0){
  $id=wp_insert_post(array('post_type'=>'page','post_status'=>'publish','post_title'=>$title,'post_name'=>$slug,'post_parent'=>$parent,'post_content'=>'Fixture '.$title),true);
  if(is_wp_error($id)){fwrite(STDERR,"FATAL page $slug\n");exit(2);} return (int)$id;
};
$root=$mkpage('Ausrüstung Upgrade E2E','ausruestung-upgrade-e2e');
$sch=$mkpage('Schabracken Upgrade E2E','schabracken-upgrade-e2e',$root);
$other=$mkpage('Ohne Treffer Upgrade E2E','ohne-treffer-upgrade-e2e');
$feed=$mkpage('Fütterung Upgrade E2E','fuetterung-upgrade-e2e');
$fixedPage=$mkpage('Feste Ausnahme Upgrade E2E','feste-ausnahme-upgrade-e2e',$root);

$save=$rm('save_campaign_record');
$mkcamp=function($id,$args=array())use($save,$o){
  $base=array(
    'id'=>$id,'active'=>1,'creative_type'=>'banner','network'=>'manual','programme_status'=>'active',
    'render_mode'=>'image_link','title'=>$id,'description'=>'','button_text'=>'Mehr erfahren',
    'image_url'=>'https://example.com/'.$id.'.jpg','url'=>'https://example.com/'.$id.'-click',
    'target'=>'_blank','placements'=>array('product_after_category_tiles'),'assignment_mode'=>'fallback',
    'priority'=>10,'health_check_enabled'=>false,'dimensions'=>'1200x120','partner'=>'legacy-'.$id,'source'=>'legacy-migration'
  );
  $pid=$save->invoke($o,array_replace($base,$args),0);
  if(is_wp_error($pid)||!$pid){fwrite(STDERR,"FATAL campaign $id\n");exit(2);} return (int)$pid;
};

$legacy=$mkcamp('legacy-sanovet',array('title'=>'Gesunde Pferde beginnen bei der Fütterung','priority'=>999));
$render=function($id,$slot)use($rm,$o){return (string)$rm('render_affiliate_slot')->invoke($o,$id,$slot,'portal_context','');};
$before=$render($sch,'product_after_category_tiles');
schk(strpos($before,'legacy-sanovet')===false,'PRE_UPGRADE_184_legacy_automatic_already_blocked',substr(strip_tags($before),0,160));

global $wpdb;
$table=$call('creative_library_table');
$raw=array(
  'creative_id'=>'library-schabracken','creative_type'=>'banner','creative_title'=>'Schabracken Designer',
  'creative_description'=>'','creative_tag'=>'Schabracken Pferd',
  'image_source'=>'https://example.com/library-schabracken.jpg',
  'destination_url'=>'https://example.com/schabracken-upgrade-e2e/',
  'tracking_url'=>'https://example.com/library-schabracken-click',
  'width'=>'1200','height'=>'120','status'=>'active'
);
$mapping=$call('creative_library_detect_mapping',array_keys($raw));
$norm=$call('creative_library_normalize_row',$raw,$mapping,array(
  'provider'=>'manual','partner_external_id'=>'partner-upgrade','partner_name'=>'Schabracken Partner',
  'source_kind'=>'banner','run_uuid'=>'upgrade-seed'
));
if(is_wp_error($norm)){fwrite(STDERR,"FATAL normalize ".$norm->get_error_message()."\n");exit(2);}
$norm['width']=1200;$norm['height']=120;$norm['topic_status']='auto_verified';
$payload=json_decode((string)$norm['payload'],true);$payload=is_array($payload)?$payload:array();
$payload['_dimension_state']='verified';$payload['_dimension_error']='';$payload['_image_sha256']=hash('sha256','library-schabracken');$payload['_measured_at']=time();
$norm['payload']=wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
$up=$call('creative_library_upsert',$norm);
schk(in_array($up,array('imported','updated','unchanged'),true),'seed_relevant_banner_in_library_unplanned');

// Realer Gegenfall, den der bisherige Test nicht abgedeckt hat:
// echte Ziel-URL = Fütterung, aber eine bereits gespeicherte Library-Kante zeigt fälschlich auf Schabracken.
$staleRaw=array(
  'creative_id'=>'stale-sanovet-library','creative_type'=>'banner','creative_title'=>'Gesunde Pferde beginnen bei der Fütterung',
  'creative_description'=>'Gezielte Ergänzung für jeden Bereich','creative_tag'=>'Fütterung Pferd',
  'image_source'=>'https://example.com/stale-sanovet-library.jpg',
  'destination_url'=>'https://example.com/fuetterung-upgrade-e2e/',
  'tracking_url'=>'https://example.com/stale-sanovet-library-click',
  'width'=>'1200','height'=>'100','status'=>'active'
);
$staleMapping=$call('creative_library_detect_mapping',array_keys($staleRaw));
$staleNorm=$call('creative_library_normalize_row',$staleRaw,$staleMapping,array(
  'provider'=>'manual','partner_external_id'=>'partner-sanovet','partner_name'=>'SanoVet',
  'source_kind'=>'banner','run_uuid'=>'upgrade-stale-edge'
));
if(is_wp_error($staleNorm)){fwrite(STDERR,"FATAL stale normalize ".$staleNorm->get_error_message()."\n");exit(2);}
$staleNorm['width']=1200;$staleNorm['height']=100;$staleNorm['topic_status']='auto_verified';
$stalePayload=json_decode((string)$staleNorm['payload'],true);$stalePayload=is_array($stalePayload)?$stalePayload:array();
$stalePayload['_dimension_state']='verified';$stalePayload['_dimension_error']='';$stalePayload['_image_sha256']=hash('sha256','stale-sanovet-library');$stalePayload['_measured_at']=time();
$staleNorm['payload']=wp_json_encode($stalePayload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
$staleUp=$call('creative_library_upsert',$staleNorm);
schk(in_array($staleUp,array('imported','updated','unchanged'),true),'seed_stale_sanovet_banner_in_library');

$portals=$call('output_portal_registry');
$portal=null;
foreach((array)$portals as $candidatePortal){if(is_array($candidatePortal)&&!empty($candidatePortal['enabled'])){$portal=$candidatePortal;break;}}
if(!is_array($portal)){fwrite(STDERR,"FATAL no enabled portal\n");exit(2);}
$targets=$call('output_portal_targets',$portal);
if(is_wp_error($targets)){fwrite(STDERR,"FATAL targets ".$targets->get_error_message()."\n");exit(2);}
$schTarget=null;$feedTarget=null;
foreach((array)$targets as $target){
  if(!is_array($target)){continue;}
  if((string)($target['slug']??'')==='schabracken-upgrade-e2e'){$schTarget=$target;}
  if((string)($target['slug']??'')==='fuetterung-upgrade-e2e'){$feedTarget=$target;}
}
if(!is_array($schTarget)||!is_array($feedTarget)){fwrite(STDERR,"FATAL fixture targets missing\n");exit(2);}
$staleRow=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$staleNorm['identity_hash']),ARRAY_A);
if(!is_array($staleRow)){fwrite(STDERR,"FATAL stale row missing\n");exit(2);}
$staleRecords=array(array(
  'portal_key'=>sanitize_key((string)($portal['key']??'')),
  'state'=>'mapped','level'=>'exact',
  'target_key'=>(string)$schTarget['key'],'target_label'=>(string)$schTarget['label'],
  'confidence'=>100,'source'=>'creative_library_destination_map',
  'destination_source'=>'provider_explicit',
  'destination_url'=>'https://example.com/fuetterung-upgrade-e2e/',
  'compatible_slots'=>array('product_after_category_tiles'),
  'updated_at'=>time()
));
$wpdb->update($table,array(
  'topic_status'=>'auto_verified','topic_score'=>100,
  'topic_targets'=>wp_json_encode($staleRecords,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
  'classified_at'=>time()
),array('id'=>absint($staleRow['id'])));
$staleRow=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$staleNorm['identity_hash']),ARRAY_A);
$stalePlanned=$call('output_plan_creative',$staleRow,true);
schk(absint($stalePlanned['active']??0)>0,'PRE_UPGRADE_stale_library_edge_materialized_wrongly');
$staleBefore=$render($sch,'product_after_category_tiles');
schk(strpos($staleBefore,'stale-sanovet-library')!==false,'PRE_UPGRADE_184_stale_library_banner_visible_on_schabracken',substr(strip_tags($staleBefore),0,160));
update_option('ppar_banner_library_migration_state_v672184','done',false);
schk((string)get_option('ppar_banner_library_migration_state_v672184','')==='done','PRE_UPGRADE_184_migration_already_done');


$fixed=$mkcamp('legacy-fixed-banner',array('priority'=>1));
update_option('ppar_assignments_v1',array(
  $fixedPage=>array('banner_mode'=>'fixed','banner_id'=>$fixed,'products_mode'=>'automatic','product_ids'=>array(),'apply_descendants'=>false,'repair_reason'=>'upgrade fixture fixed')
),false);
$fixedBefore=$render($fixedPage,'product_after_category_tiles');
schk(strpos($fixedBefore,'legacy-fixed-banner')!==false,'PRE_UPGRADE_fixed_legacy_banner_visible');

$product1=$mkcamp('product-ebay-sentinel',array(
  'creative_type'=>'product','network'=>'ebay','source'=>'output_object_v4','assignment_mode'=>'page_tree',
  'automation_target_keys'=>array('page:schabracken-upgrade-e2e'),'placements'=>array('category_product_1'),
  'title'=>'eBay Sentinel','image_url'=>'https://example.com/product-ebay.jpg','url'=>'https://example.com/product-ebay-click',
  'product_gtins'=>array('4006381333931'),'seller_name'=>'Seller A'
));
$product2=$mkcamp('product-idealo-sentinel',array(
  'creative_type'=>'product','network'=>'idealo','source'=>'output_object_v4','assignment_mode'=>'page_tree',
  'automation_target_keys'=>array('page:schabracken-upgrade-e2e'),'placements'=>array('category_product_2'),
  'title'=>'Idealo Sentinel','image_url'=>'https://example.com/product-idealo.jpg','url'=>'https://example.com/product-idealo-click',
  'product_gtins'=>array('5901234123457'),'seller_name'=>'Seller B'
));
$p1=get_post_meta($product1,'ppar_campaign_data',true); $p2=get_post_meta($product2,'ppar_campaign_data',true);
update_option('ppar_full_pool_automation_version_v1','6.72.184',false);
update_option('ppar_full_pool_automation_cursor_v1',123,false);
if(!wp_next_scheduled(Pferdeportal_Affiliate_Router::FULL_POOL_WORKER_HOOK)){wp_schedule_single_event(time()+3600,Pferdeportal_Affiliate_Router::FULL_POOL_WORKER_HOOK);}
update_option('ppar_v672185_upgrade_fixture',array(
  'root'=>$root,'sch'=>$sch,'other'=>$other,'feed'=>$feed,'fixed_page'=>$fixedPage,
  'legacy'=>$legacy,'fixed'=>$fixed,'library_identity'=>$norm['identity_hash'],'stale_identity'=>$staleNorm['identity_hash'],
  'product1'=>$product1,'product2'=>$product2,
  'product1_hash'=>hash('sha256',serialize($p1)),'product2_hash'=>hash('sha256',serialize($p2))
),false);
schk(wp_next_scheduled(Pferdeportal_Affiliate_Router::FULL_POOL_WORKER_HOOK)!==false,'PRE_UPGRADE_full_pool_event_exists_for_negative_control');
echo "SUMMARY passes=".count($GLOBALS['seed_pass'])." failures=".count($GLOBALS['seed_fail'])."\n";
if($GLOBALS['seed_fail']){echo "FAILURES ".wp_json_encode($GLOBALS['seed_fail'])."\n";exit(1);}
echo "UPGRADE_SEED_672184_PASS\n";
