<?php
$GLOBALS['af']=array();
function ack($ok,$name,$detail=''){echo ($ok?'PASS ':'FAIL ').$name.($detail!==''?' :: '.$detail:'')."\n";if(!$ok)$GLOBALS['af'][]=$name;}
if(!class_exists('Pferdeportal_Affiliate_Router')||Pferdeportal_Affiliate_Router::VERSION!=='6.72.187'){fwrite(STDERR,"FATAL assert requires 6.72.187\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($n)use($o){$m=new ReflectionMethod($o,$n);$m->setAccessible(true);return $m;};
$rp=function($n)use($o){$p=new ReflectionProperty($o,$n);$p->setAccessible(true);return $p;};
$call=function($n,...$a)use($rm,$o){return $rm($n)->invokeArgs($o,$a);};
$f=get_option('ppar_v187_realstate_fixture',array());if(!is_array($f)||empty($f['helmet_identity'])){fwrite(STDERR,"FATAL fixture missing\n");exit(2);}

ack((string)get_option('ppar_banner_library_migration_state_v672185','')==='done','OLD_185_done_state_present');
ack(Pferdeportal_Affiliate_Router::OPTION_BANNER_LIBRARY_MIGRATION_STATE==='ppar_banner_library_migration_state_v672187','NEW_187_distinct_migration_state');
ack((string)get_option(Pferdeportal_Affiliate_Router::OPTION_BANNER_LIBRARY_MIGRATION_STATE,'')!=='done','NEW_187_not_suppressed_by_old_state');

update_option(Pferdeportal_Affiliate_Router::OPTION_BANNER_LIBRARY_MIGRATION_STATE,'running',false);
$call('run_banner_library_migration_v672187');
ack((string)get_option(Pferdeportal_Affiliate_Router::OPTION_BANNER_LIBRARY_MIGRATION_STATE,'')==='done','MIGRATION_187_completed');

$table=$call('creative_library_table');
$row=$GLOBALS['wpdb']->get_row($GLOBALS['wpdb']->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",(string)$f['helmet_identity']),ARRAY_A);
$records=is_array($row)?json_decode((string)($row['topic_targets']??''),true):array();$records=is_array($records)?$records:array();
$portalKey=sanitize_key((string)$call('output_local_portal_key'));
$helmetRecord=array();
foreach($records as $rec){if(is_array($rec)&&sanitize_key((string)($rec['portal_key']??''))===$portalKey){$helmetRecord=$rec;break;}}
echo 'HELMET_RECORD '.wp_json_encode($helmetRecord,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
ack(sanitize_key((string)($helmetRecord['state']??''))==='mapped','MIGRATION_helmet_mapped');
ack(sanitize_key((string)($helmetRecord['level']??''))==='exact','MIGRATION_helmet_exact');
ack((string)($helmetRecord['target_key']??'')==='page:186','MIGRATION_helmet_page_186');

$helmetCampaign=absint($f['helmet_campaign']??0);
$campaignData=get_post_meta($helmetCampaign,'ppar_campaign_data',true);$campaignData=is_array($campaignData)?$campaignData:array();
echo 'HELMET_CAMPAIGN '.wp_json_encode(array('id'=>$helmetCampaign,'mode'=>$campaignData['assignment_mode']??'','targets'=>$campaignData['automation_target_keys']??array(),'active'=>$campaignData['active']??null),JSON_UNESCAPED_SLASHES)."\n";
ack(sanitize_key((string)($campaignData['assignment_mode']??''))==='page_tree','MIGRATION_existing_campaign_page_tree');
ack(in_array('page:reithelme',(array)($campaignData['automation_target_keys']??array()),true),'MIGRATION_existing_campaign_runtime_target_reithelme');

// Generic full-pool work must be cancelled for this banner-only release.
update_option(Pferdeportal_Affiliate_Router::OPTION_FULL_POOL_AUTOMATION_CURSOR,123,false);
wp_schedule_single_event(time()+300,Pferdeportal_Affiliate_Router::FULL_POOL_WORKER_HOOK);
$call('ensure_full_pool_automation');
ack((string)get_option(Pferdeportal_Affiliate_Router::OPTION_FULL_POOL_AUTOMATION_VERSION,'')==='6.72.187','PERF_full_pool_marked_done_187');
ack(get_option(Pferdeportal_Affiliate_Router::OPTION_FULL_POOL_AUTOMATION_CURSOR,null)===null,'PERF_full_pool_cursor_removed');
ack(!wp_next_scheduled(Pferdeportal_Affiliate_Router::FULL_POOL_WORKER_HOOK),'PERF_full_pool_worker_cancelled');

// Product sentinels are byte-identical after banner-only migration.
ack(get_post_meta(absint($f['ebay']??0),'ppar_campaign_data',true)===$f['ebay_data'],'EBAY_product_unchanged');
ack(get_post_meta(absint($f['idealo']??0),'ppar_campaign_data',true)===$f['idealo_data'],'IDEALO_product_unchanged');

// Fresh frontend request-local caches.
try{$rp('campaigns_request_cache')->setValue($o,null);}catch(Throwable $e){}
foreach(array('ranked_campaigns_request_cache','ranked_campaign_candidate_index_request_cache','ranked_campaign_raw_records_request_cache','ranked_campaign_from_post_request_cache','automation_exact_target_rank_request_cache') as $p){try{$rp($p)->setValue($o,array());}catch(Throwable $e){}}

$http=0;add_filter('pre_http_request',function($pre,$args,$url)use(&$http){$http++;return new WP_Error('blocked','frontend network forbidden');},PHP_INT_MAX,3);
$ctx186=$call('get_content_context',186);$ctx193=$call('get_content_context',193);
$sel186=$call('select_campaign_for_slot_position',$ctx186,'product_after_category_tiles',1);
$sel193=$call('select_campaign_for_slot_position',$ctx193,'product_after_category_tiles',1);
$d186=(string)($sel186['campaign']['destination_url']??'');$s186=(int)($sel186['specificity']??0);
echo 'POST187 '.wp_json_encode(array('reithelme'=>array('specificity'=>$s186,'destination'=>$d186),'schabracken'=>$sel193===null?'EMPTY':(string)($sel193['campaign']['destination_url']??''),'http'=>$http),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
ack($s186>=500 && strpos($d186,'/reithelme-sicherheitswesten/reithelme.html')!==false,'GREEN_187_reithelme_exact');
ack($sel193===null,'GREEN_187_schabracken_no_cross_topic_banner');
ack($http===0,'GREEN_187_frontend_zero_http','http='.$http);

// Manual FIXED remains a deliberate exception and still works.
$guardianIds=get_posts(array('post_type'=>Pferdeportal_Affiliate_Router::CAMPAIGN_POST_TYPE,'post_status'=>array('publish','draft','private'),'meta_key'=>'_ppar_creative_identity_hash','meta_value'=>(string)($f['guardian_identity']??''),'fields'=>'ids','posts_per_page'=>1));
$guardianId=$guardianIds?absint($guardianIds[0]):0;
update_option('ppar_assignments_v1',array(193=>array('banner_mode'=>'fixed','banner_id'=>$guardianId,'products_mode'=>'automatic','product_ids'=>array(),'apply_descendants'=>false,'repair_reason'=>'v187 fixed regression')),false);
$fixed=$call('assignment_selection_for_slot',$ctx193,'product_after_category_tiles');
$fixedDest=(string)($fixed['selection']['campaign']['destination_url']??'');
ack(!empty($fixed['handled']) && strpos($fixedDest,'guardianhorse.app')!==false,'MANUAL_FIXED_general_banner_still_allowed');
update_option('ppar_assignments_v1',array(),false);

$result=get_option('ppar_banner_library_migration_result_v672187',array());
echo 'MIGRATION_RESULT '.wp_json_encode($result,JSON_UNESCAPED_SLASHES)."\n";
ack(absint($result['target_repaired']??0)>=1,'MIGRATION_target_repaired_count','count='.absint($result['target_repaired']??0));

if($GLOBALS['af']){echo 'FAILURES '.wp_json_encode($GLOBALS['af'])."\n";exit(1);}
echo "REALSTATE_672186_TO_672187_RED_GREEN_PASS\n";
