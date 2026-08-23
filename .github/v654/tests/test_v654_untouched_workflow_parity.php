<?php
$base=getenv('PPAR_BASE_PLUGIN_DIR')?:'';$new=getenv('PPAR_TEST_PLUGIN_DIR')?:'';
if(!$base||!$new){fwrite(STDERR,"missing plugin dirs\n");exit(2);}
$tests=0;$fails=0;function q($c,$m){global$tests,$fails;$tests++;if(!$c){$fails++;echo"FAIL $m\n";}else echo"PASS $m\n";}
function fn_src($src,$name){
 $needle='function '.$name.'(';$p=strpos($src,$needle);if($p===false)return null;
 $start=$p;while($start>0 && $src[$start-1]!="\n")$start--;
 $b=strpos($src,'{',$p);if($b===false)return null;$d=0;$n=strlen($src);
 for($i=$b;$i<$n;$i++){if($src[$i]==='{')$d++;elseif($src[$i]==='}'){$d--;if($d===0)return substr($src,$start,$i-$start+1);}}
 return null;
}
$files=['includes/trait-ppar-ebay-run.php','includes/trait-ppar-ebay.php'];
$B=[];$N=[];foreach($files as $f){$B[$f]=file_get_contents($base.'/'.$f);$N[$f]=file_get_contents($new.'/'.$f);}
$runFns=['ebay_public_checkpoint_load','ebay_public_checkpoint_is_safe','ebay_public_checkpoint_save','ebay_public_checkpoint_business_ids','ebay_public_checkpoint_private_ids','ebay_public_checkpoint_allows_business_campaign','ebay_public_checkpoint_allows_private_listing','ebay_public_checkpoint_bootstrap','ebay_run_checkpoint_business_ids_from_selection','ebay_run_checkpoint_capture_selection','ebay_run_commit_public_checkpoint','ebay_run_load','ebay_run_save','ebay_run_compare_and_swap','ebay_run_is_open','ebay_run_progress_contract_version','ebay_run_settings_snapshot','ebay_run_effective_settings','ebay_run_selection_scope','ebay_run_new_uuid','ebay_run_adopt_legacy_if_needed','ebay_run_fail','ebay_run_capture_component_state','ebay_run_progress_fingerprint','ebay_run_acquire_lease','ebay_run_release_lease','ebay_run_set_phase','ebay_run_tick_reconcile','ebay_run_tick_remote','ebay_run_tick_selection','ebay_run_public_business_coverage','ebay_run_verify_private_public','ebay_run_business_safe_supply_gap_contract','ebay_run_tick_coverage','ebay_run_tick_gapfill','ebay_run_tick_gapfill_select','ebay_run_tick_public_verify','ebay_run_checkpoint_cleanup_fail_if_needed','ebay_run_tick_checkpoint_cleanup','ebay_run_selection_prepare_tick_limit','ebay_run_selection_prepare_guard_active','ebay_run_selection_prepare_regression'];
foreach($runFns as $fn){$a=fn_src($B[$files[0]],$fn);$b=fn_src($N[$files[0]],$fn);q($a!==null&&$b!==null&&hash_equals(hash('sha256',$a),hash('sha256',$b)),'unchanged_run_'.$fn);}
$ebayFns=['ebay_classify_portal_item','ebay_business_classify_portal_item_strict','ebay_accept_item','ebay_business_curation_decision','ebay_business_relevance_report','ebay_business_quality_assess','ebay_business_creative','ebay_business_exact_product_classification','ebay_route_business','ebay_is_soft_classification_error','ebay_sync_process_item','ebay_refresh_reuse_classification','ebay_refresh_process_row'];
foreach($ebayFns as $fn){$a=fn_src($B[$files[1]],$fn);$b=fn_src($N[$files[1]],$fn);q($a!==null&&$b!==null&&hash_equals(hash('sha256',$a),hash('sha256',$b)),'unchanged_fach_'.$fn);}
echo "PARITY_ASSERTIONS=$tests FAIL=$fails\n";exit($fails?1:0);
