<?php
require __DIR__.'/lib.php';
rg_settings_business_only();
$p=rg_plugin();
function v646_call($obj,$name,...$args){$m=new ReflectionMethod($obj,$name);$m->setAccessible(true);return $m->invokeArgs($obj,$args);}
$required=v646_call($p,'ebay_business_required_product_concept_ids');
rg_assert(count((array)$required)===311,'real manifest has 311 BUSINESS concepts');
$concept=sanitize_key((string)$required[0]);
$table=v646_call($p,'ebay_items_table');
global $wpdb;$now=time();
$payload=wp_json_encode(array('portal_classification'=>array('product_concept_id'=>$concept,'business_match_contract'=>'concept_v3')));
$ok=$wpdb->insert($table,array('portal_key'=>'local','item_id'=>'v646-stale-gate','seller_account_type'=>'BUSINESS','route_mode'=>'business_affiliate','rule_id'=>$concept,'title'=>'gate','condition_text'=>'Neu','location_text'=>'DE','affiliate_url'=>'https://example.invalid/a','item_web_url'=>'https://example.invalid/a','image_url'=>'https://example.invalid/a.jpg','source_hash'=>hash('sha256','v646-stale-gate'),'source_payload'=>$payload,'source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready','output_state'=>'candidate','policy_version'=>Pferdeportal_Affiliate_Router::EBAY_CONTENT_POLICY_VERSION,'classifier_version'=>Pferdeportal_Affiliate_Router::EBAY_BUSINESS_CLASSIFIER_VERSION,'source_checked_at'=>$now-21610,'last_seen'=>$now-21610,'fresh_until'=>$now-10,'created_at'=>$now-21610,'updated_at'=>$now-21610));
rg_assert($ok!==false,'stale source persisted in real MariaDB');
$rows=v646_call($p,'ebay_business_selection_concept_rows',$concept,rg_settings_business_only());
rg_assert(count((array)$rows)===0,'real selector SQL excludes stale source');
$wpdb->update($table,array('source_checked_at'=>$now,'last_seen'=>$now,'fresh_until'=>$now+21600,'updated_at'=>$now),array('item_id'=>'v646-stale-gate'));
$rows=v646_call($p,'ebay_business_selection_concept_rows',$concept,rg_settings_business_only());
rg_assert(count((array)$rows)===1,'revalidated source becomes selector eligible');
$wpdb->update($table,array('fresh_until'=>$now-10),array('item_id'=>'v646-stale-gate'));
$state=array('business_cursor'=>0,'business_active'=>array('v646-stale-gate'=>array('concept'=>$concept,'rank'=>1)),'business_soft_failed'=>array(),'stats'=>array('business'=>array('scanned'=>0,'materialized'=>0,'active'=>0,'errors'=>array())),'plan_stats'=>array());
$apply=Closure::bind(function(&$s){return $this->ebay_selection_apply_business_batch($this->ebay_settings(),$s,1);},$p,get_class($p));$apply($state);
rg_assert(!isset($state['business_active']['v646-stale-gate']),'apply rejects winner that aged out');
rg_assert(($state['business_soft_failed']['v646-stale-gate']['code']??'')==='business_selected_stale_during_apply','apply records stale soft failure');
$uuid='v646-real-stale-recovery';$invalid=array();for($i=1;$i<=231;$i++){$invalid[$i]='source_stale';}
$run=rg_base_run($uuid,888,10);$run['build']='6.45.0-canonical-run-persistence-race-rootfix-20260820';$run['status']='failed';$run['phase']='failed';$run['finished_at']=$now;$run['error_code']='insufficient_safe_sources';$run['phase_state']['selection']=array('stats'=>array('business'=>array('materialized'=>231)));$run['phase_state']['refresh']=array('status'=>'completed');$run['coverage']=array('required'=>311,'covered'=>0,'missing'=>$required,'invalid'=>$invalid);$run['gapfill']=array('attempts'=>1,'missing'=>$required);$run['errors']=array(array('code'=>'insufficient_safe_sources','at'=>$now,'details'=>array('phase'=>'coverage_verify','build'=>'6.45.0-canonical-run-persistence-race-rootfix-20260820')));
rg_reset_run($run);update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_REFRESH_JOB,array('status'=>'completed'),false);$p->maybe_migrate_ebay_public_freshness_v6460();$after=rg_run();
rg_assert(($after['run_uuid']??'')===$uuid,'recovery preserves exact run UUID');
rg_assert(($after['status']??'')==='running'&&($after['phase']??'')==='reconcile_local','all-stale proof reopens canonical reconcile path');
rg_assert(get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_REFRESH_JOB,array('x'=>1))===array(),'recovery clears completed refresh only after CAS');
$once=$after;$p->maybe_migrate_ebay_public_freshness_v6460();rg_assert(rg_run()===$once,'recovery is idempotent');
$bad=$run;$bad['run_uuid']=$uuid.'-mixed';$bad['coverage']['invalid'][1]='campaign_not_public';rg_reset_run($bad);update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_REFRESH_JOB,array('status'=>'completed'),false);$p->maybe_migrate_ebay_public_freshness_v6460();$bad_after=rg_run();
rg_assert(($bad_after['status']??'')==='failed','mixed invalid reason stays terminal');
rg_assert(get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_REFRESH_JOB,array())!==array(),'mixed case does not reset refresh');
echo "PUBLIC_FRESHNESS_V646_OK\n";
