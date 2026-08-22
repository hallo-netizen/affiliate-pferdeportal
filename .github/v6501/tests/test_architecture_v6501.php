<?php
$root=getenv('PPAR_TEST_PLUGIN_DIR');$base=getenv('PPAR_V650_BASELINE_DIR');$stage=getenv('PPAR_V6501_STAGE')?:'step1';
if(!$root||!$base){fwrite(STDERR,"missing roots\n");exit(2);} $main=file_get_contents($root.'/pferdeportal-affiliate-router.php');$run=file_get_contents($root.'/includes/trait-ppar-ebay-run.php');$read=file_get_contents($root.'/readme.txt');$f=0;$n=0;function ck6501($v,$m){global$f,$n;$n++;echo($v?'PASS ':'FAIL ').$m."\n";if(!$v)$f++;}
ck6501(strpos($run,'safe_supply_gap_stale_proof_recovery')!==false,'stale-proof recovery contract exists');
ck6501(strpos($run,"'phase']='coverage_verify'")!==false,'recovery re-enters existing coverage_verify');
ck6501(strpos($run,"['discovery']=array()")!==false&&strpos($run,"['selection']=array()")!==false,'stale discovery and selection are discarded');
ck6501(strpos($run,"['coverage']=array()")!==false&&strpos($run,"['gapfill']=array('attempts'=>0,'missing'=>array())")!==false,'stale coverage and gapfill proof are discarded');
ck6501(strpos($run,"business_safe_gap_new_missing_family")!==false&&strpos($run,"strpos(\$failure_build,'6.50.0-')===0")!==false,'exact failed V6.50 live-upgrade signature is recoverable');
ck6501(strpos($run,"insufficient_safe_sources")!==false&&strpos($run,"strpos(\$failure_build,'6.49.0-')===0")!==false,'exact V6.49 predecessor signature remains recoverable');
ck6501(strpos($run,'ebay_run_business_safe_supply_gap_contract')!==false&&strpos($run,'business_gapfill_public_invariant_failed')!==false,'safe-gap proof and selected-winner fail-closed guard remain');
$changed=[];$it=new RecursiveIteratorIterator(new RecursiveDirectoryIterator($root,FilesystemIterator::SKIP_DOTS));foreach($it as $file){if(!$file->isFile())continue;$rel=substr($file->getPathname(),strlen($root)+1);$bp=$base.'/'.$rel;if(!is_file($bp)||hash_file('sha256',$file->getPathname())!==hash_file('sha256',$bp))$changed[]=$rel;}sort($changed);
$expected=$stage==='step1'?array('includes/trait-ppar-ebay-run.php'):array('includes/trait-ppar-ebay-run.php','pferdeportal-affiliate-router.php','readme.txt');
ck6501($changed===$expected,'production scope is exact for current V6.50.1 step');
foreach(array('includes/trait-ppar-ebay.php','includes/trait-ppar-creative-library.php','includes/trait-ppar-awin-programme-gate.php','assets/ebay-portal-catalog-v2.json','assets/portal-structure-v279.json','assets/frontend.css','assets/frontend.js') as $rel){ck6501(hash_file('sha256',$root.'/'.$rel)===hash_file('sha256',$base.'/'.$rel),$rel.' byte-identical to binding V6.50 MASTER');}
ck6501(substr_count($main,"maybe_migrate_ebay_safe_supply_gap_v6500'), 10")===1,'existing recovery hook unchanged and unique');
$baseMain=file_get_contents($base.'/pferdeportal-affiliate-router.php');ck6501(substr_count($main,"ppar_ebay_discovery_tick")===substr_count($baseMain,"ppar_ebay_discovery_tick"),'no second discovery cron introduced');
if($stage==='step1'){
 ck6501(strpos($main,'Version: 6.50.0')!==false&&strpos($main,"const VERSION = '6.50.0'")!==false,'step1 keeps binding release metadata unchanged');
}else{
 ck6501(strpos($main,'Version: 6.50.1')!==false&&strpos($main,"const VERSION = '6.50.1'")!==false,'final version metadata is 6.50.1');
 ck6501(strpos($main,"6.50.1-safe-gap-stale-proof-rootfix-20260822")!==false,'final runtime build is exact');
 ck6501(strpos($read,'SAFE GAP STALE PROOF ROOTFIX')!==false&&strpos($read,'Stable tag: 6.50.1')!==false,'README documents final rootfix');
}
echo "ASSERTIONS=$n FAIL=$f\n";exit($f?1:0);
