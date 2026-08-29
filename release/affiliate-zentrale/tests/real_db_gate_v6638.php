<?php
$mode = getenv('GATE_MODE') ?: 'positive_upgrade';
$uuid = '7ff7434e-f12a-493b-8485-1e98188ef02c';
function gfail($m){fwrite(STDERR,"FAIL $m\n");exit(1);} function gpass($m){echo "PASS $m\n";}
function admin_user(){ $u=get_user_by('login','admin'); if(!$u)gfail('admin_missing'); wp_set_current_user($u->ID); }
function calls(){ $v=get_option('v6638_gate_http_calls',array()); return is_array($v)?$v:array(); }
function clear_calls(){ update_option('v6638_gate_http_calls',array(),false); }
function zero_fixture($uuid){ return array(
 'schema'=>'1.0','build'=>'6.63.4-live-observed-gap-proof-recovery-rootfix-20260828','run_uuid'=>$uuid,
 'status'=>'running','phase'=>'reconcile_local','started_at'=>time()-60,'finished_at'=>0,
 'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'external_tick','orchestrator_contract'=>'external_tick_v2',
 'progress_seq'=>0,'transport_tick_count'=>0,'phase_tick_count'=>0,'no_progress_count'=>0,'last_progress_at'=>time()-60,
 'progress_contract_version'=>'3.1','phase_state'=>array(),'error_code'=>'','error_message'=>'',
 'config_snapshot'=>array('seller_routes'=>array('private'=>1,'business'=>1),'settings'=>array()),
 'coverage'=>array('required'=>311,'covered'=>0,'missing'=>array()),
 'checkpoint_id'=>'ZERO-TICK-SAFE','checkpoint_base_id'=>'ZERO-TICK-SAFE',
 'checkpoint_candidate'=>array('business_campaign_ids'=>array(501,502),'private_listing_ids'=>array(101,102))
 ); }
function raw_has_uuid($uuid){ global $wpdb; $raw=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE)); return is_string($raw)&&strpos($raw,$uuid)!==false; }
admin_user();

if($mode==='negative_seed'){
 if(Pferdeportal_Affiliate_Router::VERSION!=='6.63.4') gfail('negative_version_6634'); gpass('negative_version_6634');
 if(Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD!=='6.63.4-live-observed-gap-proof-recovery-rootfix-20260828') gfail('negative_build_6634'); gpass('negative_build_6634');
 clear_calls(); update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,zero_fixture($uuid),false);
 if(!raw_has_uuid($uuid)) gfail('negative_seed_mariadb_persisted'); gpass('negative_seed_mariadb_persisted');
 echo "NEGATIVE_SEED_V6634_PASS\n"; exit(0);
}
if($mode==='negative_probe'){
 if(Pferdeportal_Affiliate_Router::VERSION!=='6.63.4') gfail('negative_probe_version');
 $r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array());
 if(($r['status']??'')!=='running'||($r['phase']??'')!=='reconcile_local') gfail('old_run_not_stalled_running'); gpass('old_run_stays_running_reconcile');
 if(($r['run_uuid']??'')!==$uuid) gfail('old_run_uuid_changed'); gpass('old_run_same_uuid');
 if((int)($r['progress_seq']??-1)!==0||(int)($r['transport_tick_count']??-1)!==0||(int)($r['phase_tick_count']??-1)!==0) gfail('old_run_unexpected_progress'); gpass('old_run_zero_ticks_terminal_reproduction');
 if(calls()) gfail('old_run_unexpected_selfdrive'); gpass('old_run_no_selfdrive_dispatch');
 if(!raw_has_uuid($uuid)) gfail('negative_probe_mariadb_persisted'); gpass('negative_probe_mariadb_persisted');
 echo "NEGATIVE_V6634_ZERO_TICK_STALL_REPRODUCED\n"; exit(0);
}

if(Pferdeportal_Affiliate_Router::VERSION!=='6.63.8') gfail('version_6638'); gpass('version_6638');
if(Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD!=='6.63.8-self-driven-canonical-orchestrator-rootfix-20260829') gfail('build_6638'); gpass('build_6638');
$o=Pferdeportal_Affiliate_Router::instance();

if($mode==='positive_upgrade'){
 $r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array());
 if(($r['status']??'')!=='running'||($r['phase']??'')!=='reconcile_local') gfail('upgrade_run_not_running'); gpass('upgrade_run_running_reconcile');
 if(($r['run_uuid']??'')!==$uuid) gfail('upgrade_uuid_changed'); gpass('upgrade_same_uuid');
 if(($r['build']??'')!==Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD) gfail('upgrade_build_not_adopted'); gpass('upgrade_build_adopted');
 if(($r['worker_transport']??'')!=='self_drive'||($r['orchestrator_contract']??'')!=='self_drive_v1'||($r['resume_reason']??'')!=='zero_tick_self_drive_adoption') gfail('upgrade_selfdrive_contract'); gpass('upgrade_selfdrive_contract');
 $c=calls(); if(count($c)!==1) gfail('upgrade_exactly_one_dispatch_'.count($c)); gpass('upgrade_exactly_one_dispatch');
 $body=$c[0]['body']??array(); if(($body['run_uuid']??'')!==$uuid||($body['action']??'')!=='ppar_ebay_canonical_self_drive') gfail('upgrade_dispatch_binding'); gpass('upgrade_dispatch_uuid_action_bound');
 if(!raw_has_uuid($uuid)) gfail('upgrade_mariadb_same_uuid'); gpass('upgrade_mariadb_same_uuid');
 $o->maybe_adopt_stalled_zero_tick_ebay_run_v6638(); if(count(calls())!==1) gfail('upgrade_adoption_not_idempotent'); gpass('upgrade_adoption_idempotent');
 $mutations=array(
  'progress_seq'=>function(&$x){$x['progress_seq']=1;}, 'transport_tick'=>function(&$x){$x['transport_tick_count']=1;},
  'phase_tick'=>function(&$x){$x['phase_tick_count']=1;}, 'phase_state'=>function(&$x){$x['phase_state']=array('selection'=>array('status'=>'running'));},
  'owner'=>function(&$x){$x['owner']='worker:x';}, 'lease'=>function(&$x){$x['lease_expires_at']=time()+30;},
  'no_progress'=>function(&$x){$x['no_progress_count']=1;}, 'error'=>function(&$x){$x['error_code']='some_error';},
  'wrong_phase'=>function(&$x){$x['phase']='selection_prepare';}, 'wrong_build'=>function(&$x){$x['build']='other-build';}
 );
 foreach($mutations as $name=>$fn){$x=zero_fixture($uuid);$fn($x);update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$x,false);clear_calls();$o->maybe_adopt_stalled_zero_tick_ebay_run_v6638();$a=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array());if(($a['build']??'')!==($x['build']??'')||calls())gfail('negative_'.$name);gpass('negative_'.$name.'_failclosed');}
 $uuid2='d4fd17b4-f44a-4b89-8e12-live-observed';$cp='safe-live-checkpoint';
 $checkpoint=array('schema'=>'1.0','status'=>'safe','checkpoint_id'=>$cp,'business_campaign_ids'=>array(501,502),'private_listing_ids'=>array(101,102));
 $buildrun=array('schema'=>'1.0','build'=>'6.47.0-dynamic-business-rule-context-rootfix-20260821','run_uuid'=>$uuid2,'status'=>'failed','phase'=>'failed','finished_at'=>2000,'progress_contract_version'=>'3.1','worker_transport'=>'admin_ajax','config_snapshot'=>array('seller_routes'=>array('private'=>1,'business'=>1),'settings'=>array()),'checkpoint_base_id'=>$cp,'checkpoint_id'=>$cp,'checkpoint_safe'=>1,'checkpoint_candidate'=>array('business_campaign_ids'=>array(999),'private_listing_ids'=>array(888)),'phase_state'=>array('selection'=>array('status'=>'complete'),'discovery'=>array('cursor'=>123)),'coverage'=>array('required'=>311,'covered'=>0),'gapfill'=>array('attempts'=>2,'missing'=>array('stale')),'private_public_revalidation'=>array('status'=>'complete'),'errors'=>array(array('code'=>'run_build_changed_restart_required','at'=>2000,'details'=>array('phase'=>'reconcile_local','build'=>'6.63.4-live-observed-gap-proof-recovery-rootfix-20260828','previous_build'=>'6.47.0-dynamic-business-rule-context-rootfix-20260821','checkpoint_id'=>$cp,'progress_contract_version'=>'3.1'))),'error_code'=>'run_build_changed_restart_required','error_message'=>'closed');
 update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_PUBLIC_CHECKPOINT,$checkpoint,false);update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$buildrun,false);clear_calls();$o->maybe_recover_ebay_build_change_checkpoint_same_uuid_v6636();$rr=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array());
 if(($rr['status']??'')!=='running'||($rr['phase']??'')!=='reconcile_local'||($rr['run_uuid']??'')!==$uuid2)gfail('v6636_same_uuid_recovery');gpass('v6636_same_uuid_recovery');
 if(($rr['checkpoint_candidate']['business_campaign_ids']??array())!==array(501,502)||($rr['checkpoint_candidate']['private_listing_ids']??array())!==array(101,102))gfail('v6636_safe_checkpoint_reset');gpass('v6636_safe_checkpoint_reset');
 $hs=$o->run_housekeeping();if(($hs['status']??'')!=='deferred_busy')gfail('housekeeping_busy_failclosed');gpass('housekeeping_busy_failclosed');
 $rr['status']='completed';$rr['phase']='completed';$rr['finished_at']=time();update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$rr,false);
 global $wpdb;$runs=$wpdb->prefix.'ppar_sync_runs';$products=$wpdb->prefix.'ppar_sync_products';$now=time();
 $wpdb->insert($runs,array('network'=>'idealo','operation'=>'gate_old','status'=>'success','started_at'=>$now-101*DAY_IN_SECONDS,'finished_at'=>$now-100*DAY_IN_SECONDS,'items_seen'=>1,'items_imported'=>1,'items_updated'=>0,'items_skipped'=>0,'items_failed'=>0,'message'=>'old','details'=>'{}'));
 $old_run_id=(int)$wpdb->insert_id;$wpdb->insert($runs,array('network'=>'idealo','operation'=>'gate_recent','status'=>'success','started_at'=>$now-2*DAY_IN_SECONDS,'finished_at'=>$now-DAY_IN_SECONDS,'items_seen'=>1,'items_imported'=>1,'items_updated'=>0,'items_skipped'=>0,'items_failed'=>0,'message'=>'recent','details'=>'{}'));$recent_run_id=(int)$wpdb->insert_id;
 $wpdb->insert($products,array('network'=>'idealo','external_key'=>'hk-preserve-product','programme_external_id'=>'p1','programme_name'=>'P','title'=>'Preserve result','image_url'=>'https://example.test/i.jpg','tracking_url'=>'https://example.test/t','destination_url'=>'https://example.test/d','price'=>'10','currency'=>'EUR','brand'=>'B','category'=>'C','quality_status'=>'pass','source_hash'=>hash('sha256','x'),'source_headers'=>'{}','payload'=>'{"x":1}','first_seen'=>$now-201*DAY_IN_SECONDS,'last_seen'=>$now-200*DAY_IN_SECONDS));
 $product_id=(int)$wpdb->insert_id;
 $up=wp_upload_dir(null,false);$dir=rtrim($up['basedir'],'/\\').'/ppar-affiliate-product-images';wp_mkdir_p($dir);$orphan=$dir.'/ebay-realdb-orphan.jpg';$ref=$dir.'/idealo-realdb-referenced.jpg';file_put_contents($orphan,'orphan');file_put_contents($ref,'referenced');touch($orphan,$now-40*DAY_IN_SECONDS);touch($ref,$now-40*DAY_IN_SECONDS);update_option('v6638_hk_reference',basename($ref),false);
 $hs=$o->run_housekeeping();if(($hs['status']??'')!=='complete')gfail('housekeeping_complete');gpass('housekeeping_complete');
 if((int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$runs} WHERE id=%d",$old_run_id))!==0)gfail('housekeeping_old_terminal_history_deleted');gpass('housekeeping_old_terminal_history_deleted');
 if((int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$runs} WHERE id=%d",$recent_run_id))!==1)gfail('housekeeping_recent_history_preserved');gpass('housekeeping_recent_history_preserved');
 if((int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$products} WHERE id=%d",$product_id))!==1)gfail('housekeeping_product_source_preserved');gpass('housekeeping_product_source_preserved_no_result_shrink');
 if(file_exists($orphan))gfail('housekeeping_orphan_file_deleted');gpass('housekeeping_orphan_file_deleted');if(!file_exists($ref))gfail('housekeeping_referenced_file_preserved');gpass('housekeeping_referenced_file_preserved');@unlink($ref);delete_option('v6638_hk_reference');
 echo "REAL_WORDPRESS_MARIADB_UPGRADE_V6638_PASS\n";exit(0);
}

if($mode==='fresh'){
 global $wpdb;$expected=array('ppar_sync_runs','ppar_sync_products','ppar_ebay_items','ppar_automation_runs','ppar_automation_jobs','ppar_creative_library','ppar_output_objects');
 foreach($expected as $suffix){$t=$wpdb->prefix.$suffix;$v=$wpdb->get_var($wpdb->prepare('SHOW TABLES LIKE %s',$t));if($v!==$t)gfail('fresh_table_'.$suffix);gpass('fresh_table_'.$suffix);}
 delete_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE);$h=$o->run_housekeeping();if(($h['status']??'')!=='complete')gfail('fresh_housekeeping');gpass('fresh_housekeeping');
 clear_calls();update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,zero_fixture($uuid),false);$o->maybe_adopt_stalled_zero_tick_ebay_run_v6638();$r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array());
 if(($r['run_uuid']??'')!==$uuid||($r['worker_transport']??'')!=='self_drive'||($r['orchestrator_contract']??'')!=='self_drive_v1')gfail('fresh_selfdrive_adoption');gpass('fresh_selfdrive_adoption');if(count(calls())!==1)gfail('fresh_one_dispatch');gpass('fresh_one_dispatch');if(!raw_has_uuid($uuid))gfail('fresh_mariadb_persistence');gpass('fresh_mariadb_persistence');
 echo "REAL_WORDPRESS_MARIADB_FRESH_INSTALL_V6638_PASS\n";exit(0);
}
gfail('unknown_mode');
