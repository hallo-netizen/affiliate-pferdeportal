<?php
$root=getenv('PPAR_TEST_PLUGIN_DIR');
if(!$root){fwrite(STDERR,"missing root\n");exit(2);}
$f=0;$n=0;
function ck($v,$m){global $f,$n;$n++;echo($v?'PASS ':'FAIL ').$m."\n";if(!$v)$f++;}
$main=file_get_contents($root.'/pferdeportal-affiliate-router.php');
$run=file_get_contents($root.'/includes/trait-ppar-ebay-run.php');
$ebay=file_get_contents($root.'/includes/trait-ppar-ebay.php');
$readme=file_get_contents($root.'/readme.txt');
ck(strpos($main,'Version: 6.46.0')!==false && strpos($main,"const VERSION = '6.46.0';")!==false,'main plugin version is 6.46.0');
ck(strpos($main,'6.46.0-public-freshness-selection-contract-rootfix-20260820')!==false,'runtime build identifies public freshness rootfix');
ck(strpos($readme,'Stable tag: 6.46.0')!==false,'readme stable tag is 6.46.0');
ck(strpos($ebay,'fresh_until>%d AND (item_end_at=0 OR item_end_at>%d)')!==false,'BUSINESS concept query filters stale/ended rows before planning');
ck(strpos($ebay,'ebay_business_source_row_is_public_fresh($row, $now)')!==false,'prepare has defense-in-depth public freshness check');
ck(strpos($ebay,'business_selected_stale_during_apply')!==false,'apply phase has stale-between-prepare-and-apply soft failure');
ck(strpos($run,'maybe_migrate_ebay_public_freshness_v6460')!==false && strpos($main,'maybe_migrate_ebay_public_freshness_v6460')!==false,'narrow V6.45 stale-public migration is registered');
ck(strpos($run,"strpos(\$failure_build,'6.45.0-')!==0")!==false,'migration is provenance-gated to V6.45 failures');
ck(strpos($run,"sanitize_key((string)\$reason)!=='source_stale'")!==false,'migration refuses mixed/unknown public invalid reasons');
ck(strpos($run,"\$run['phase']='reconcile_local'")!==false,'recovery re-enters existing canonical reconcile/refresh workflow');
echo "ASSERTIONS=$n FAIL=$f\n";
exit($f?1:0);
