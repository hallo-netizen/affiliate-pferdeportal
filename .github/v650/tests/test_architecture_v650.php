<?php
$root=getenv('PPAR_TEST_PLUGIN_DIR');$base=getenv('PPAR_V649_BASELINE_DIR');$stage=getenv('PPAR_V650_STAGE')?:'final';
if(!$root||!$base){fwrite(STDERR,"missing roots\n");exit(2);} $main=file_get_contents($root.'/pferdeportal-affiliate-router.php');$run=file_get_contents($root.'/includes/trait-ppar-ebay-run.php');$read=file_get_contents($root.'/readme.txt');$f=0;$n=0;function ck650($v,$m){global$f,$n;$n++;echo($v?'PASS ':'FAIL ').$m."\n";if(!$v)$f++;}
ck650(strpos($run,'ebay_run_business_safe_supply_gap_contract')!==false,'V6.50 safe-supply-gap contract exists');
ck650(strpos($run,"'code'=>'safe_supply_gap_open','approved'=>0,'public'=>0")!==false,'open gap is explicitly non-approved and non-public');
ck650(strpos($run,'business_gapfill_public_invariant_failed')!==false,'selected-but-not-public remains hard invariant error');
ck650(strpos($run,"'retry'=>'next_scheduled_canonical_run'")!==false,'gap retry uses existing canonical schedule only');
ck650(strpos($run,"business_safe_gap_proof_missing")!==false&&strpos($run,"business_safe_gap_scope_mismatch")!==false&&strpos($run,"business_safe_gap_new_missing_family")!==false,'missing proof/scope/new-family states fail closed');
ck650(strpos($run,"method_exists(\$this,'ebay_business_required_product_concept_ids')")!==false,'run-trait compatibility guard preserves authoritative manifest when available');
$changed=[];$it=new RecursiveIteratorIterator(new RecursiveDirectoryIterator($root,FilesystemIterator::SKIP_DOTS));foreach($it as $file){if(!$file->isFile())continue;$rel=substr($file->getPathname(),strlen($root)+1);$bp=$base.'/'.$rel;if(!is_file($bp)||hash_file('sha256',$file->getPathname())!==hash_file('sha256',$bp))$changed[]=$rel;}sort($changed);
$expected=$stage==='step1'?array('includes/trait-ppar-ebay-run.php'):($stage==='step2'?array('includes/trait-ppar-ebay-run.php','pferdeportal-affiliate-router.php'):array('includes/trait-ppar-ebay-run.php','pferdeportal-affiliate-router.php','readme.txt'));
ck650($changed===$expected,'production scope matches exact V6.50 stage');
ck650(hash_file('sha256',$root.'/includes/trait-ppar-ebay.php')===hash_file('sha256',$base.'/includes/trait-ppar-ebay.php'),'classifier/materializer trait byte-identical to V6.49');
ck650(hash_file('sha256',$root.'/assets/ebay-portal-catalog-v2.json')===hash_file('sha256',$base.'/assets/ebay-portal-catalog-v2.json'),'authoritative BUSINESS catalog byte-identical to V6.49');
ck650(hash_file('sha256',$root.'/assets/portal-structure-v279.json')===hash_file('sha256',$base.'/assets/portal-structure-v279.json'),'portal structure byte-identical to V6.49');
if($stage==='step1'){
 ck650(strpos($run,'maybe_migrate_ebay_safe_supply_gap_v6500')===false,'step1 contains no migration yet');
 ck650(strpos($main,"maybe_migrate_ebay_safe_supply_gap_v6500")===false,'step1 init path unchanged');
}elseif($stage==='step2'){
 ck650(strpos($run,'maybe_migrate_ebay_safe_supply_gap_v6500')!==false,'step2 adds guarded same-UUID migration');
 ck650(strpos($main,"maybe_migrate_ebay_safe_supply_gap_v6500'), 10")!==false,'step2 migration is wired before transport');
 ck650(strpos($main,'Version: 6.49.0')!==false,'step2 remains non-release intermediate version');
}else{
 ck650(strpos($main,'Version: 6.50.0')!==false&&strpos($main,"const VERSION = '6.50.0'")!==false,'final V6.50 header and constant');
 ck650(strpos($main,"6.50.0-coverage-gap-contract-rootfix-20260821")!==false,'final V6.50 runtime build');
 $p650=strpos($main,"maybe_migrate_ebay_safe_supply_gap_v6500'), 10");$pt=strpos($main,"maybe_migrate_ebay_worker_transport_v6412'), 10");ck650($p650!==false&&$pt!==false&&$p650<$pt,'V6.50 state migration runs before worker-transport migration');
 ck650(strpos($read,'COVERAGE GAP CONTRACT ROOTFIX')!==false,'README documents V6.50 contract rootfix');
}
echo "ASSERTIONS=$n FAIL=$f\n";exit($f?1:0);
