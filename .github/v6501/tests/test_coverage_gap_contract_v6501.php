<?php
define('ABSPATH', __DIR__ . '/');
$GLOBALS['__opts']=array();
function sanitize_key($v){$v=strtolower((string)$v);return preg_replace('/[^a-z0-9_\-]/','',$v);}
function sanitize_text_field($v){return trim((string)$v);}
function absint($v){return abs((int)$v);}
function get_option($k,$d=false){return array_key_exists($k,$GLOBALS['__opts'])?$GLOBALS['__opts'][$k]:$d;}
function update_option($k,$v,$autoload=false){$GLOBALS['__opts'][$k]=$v;return true;}
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
$root=getenv('PPAR_TEST_PLUGIN_DIR');if(!$root){fwrite(STDERR,"PPAR_TEST_PLUGIN_DIR missing\n");exit(2);} require $root.'/includes/trait-ppar-ebay-run.php';

final class V650Harness {
    use PPAR_Ebay_Run_Trait;
    const EBAY_RUNTIME_BUILD='6.50.0-coverage-gap-contract-rootfix-20260821';
    const OPTION_EBAY_RUN_STATE='test_v650_run';
    public array $required=array();
    private function ebay_business_required_product_concept_ids(){return $this->required;}
    public function gapContract($run,$coverage){$m=new ReflectionMethod($this,'ebay_run_business_safe_supply_gap_contract');$m->setAccessible(true);return $m->invoke($this,$run,$coverage);}
    public function migrate(){return $this->maybe_migrate_ebay_safe_supply_gap_v6500();}
}

$assertions=0;$fail=0;
function ok($cond,$msg){global $assertions,$fail;$assertions++;if($cond){echo "PASS $msg\n";}else{$fail++;echo "FAIL $msg\n";}}

$fixture=getenv('PPAR_LIVE_COVERAGE_FIXTURE');if(!$fixture||!is_file($fixture)){fwrite(STDERR,"PPAR_LIVE_COVERAGE_FIXTURE missing\n");exit(2);} $data=json_decode(file_get_contents($fixture),true);
ok(is_array($data),'live raw JSON parses');
ok(($data['source_file_sha256']??'')==='466b99665bb96b12d34ba7c02a3af80c4ca2ebeb68d8b14db02c50f34507b1a1','fixture is exact projection of supplied live raw file');
ok(($data['build']??'')==='6.48.0-canonical-refresh-authority-rootfix-20260821'&&($data['run_uuid']??'')==='110e36b0-ad6b-4202-96d6-43604da654b6','fixture preserves exact live build and run UUID');
ok(absint($data['received']??0)===3137&&absint($data['accepted']??0)===350&&absint($data['review_pending']??0)===632&&absint($data['hard_blocked']??0)===985,'fixture preserves exact live aggregate intake decisions');
$stats=(array)($data['profile_stats']??array());
$required=[];$missing=[];$covered=[];$zero_received=0;$rejected_only=0;
foreach($stats as $st){
    $id=sanitize_key((string)($st['concept']??$st['expected_business_concept_id']??''));
    if($id==='')continue;$required[$id]=1;
    $a=absint($st['accepted']??0);$r=absint($st['received']??0);
    if($a>0){$covered[$id]=1;}else{$missing[$id]=1;if($r===0)$zero_received++;else $rejected_only++;}
}
$required=array_keys($required);sort($required,SORT_STRING);$missing=array_keys($missing);sort($missing,SORT_STRING);$covered=array_keys($covered);sort($covered,SORT_STRING);
ok(count($stats)===311,'live raw has 311 profile stats');
ok(count($required)===311,'live raw has 311 unique BUSINESS families');
ok(count($covered)===91,'live raw has 91 safely supplied families');
ok(count($missing)===220,'live raw has 220 families without accepted safe offer');
ok($zero_received===126,'live raw has 126 families with zero eBay results');
ok($rejected_only===94,'live raw has 94 families with results but zero accepted offers');

$h=new V650Harness();$h->required=$required;$uuid='v650-test-run-uuid';
$selection=array(
    'status'=>'complete','reason'=>'canonical_gapfill','selection_scope'=>'business','owner'=>'run:'.$uuid,
    'business_target_mode'=>'gapfill','business_target_concepts'=>$missing,'business_active'=>array(),
    'stats'=>array('business'=>array('errors'=>array()))
);
$run=array('schema'=>'1.0','run_uuid'=>$uuid,'gapfill'=>array('attempts'=>1,'missing'=>$missing),'phase_state'=>array('selection'=>$selection));
$coverage=array('required'=>311,'covered'=>91,'missing'=>$missing,'counts'=>array(),'invalid'=>array());
$r=$h->gapContract($run,$coverage);
ok(($r['status']??'')==='pass','91/311 live-shape becomes proven safe supply-gap contract after one gap-fill');
ok(($r['coverage']['contract_status']??'')==='complete_with_safe_supply_gaps','coverage contract marks completion with safe supply gaps');
ok(absint($r['coverage']['open_gap_count']??0)===220,'coverage persists exactly 220 open gaps');
ok(count((array)($r['coverage']['exceptions']??array()))===220,'each open family receives explicit non-approved gap state');
ok(($r['coverage']['retry_contract']??'')==='next_scheduled_canonical_run','open gaps retry only through next scheduled canonical run');
ok(!array_filter((array)$r['coverage']['exceptions'],fn($x)=>!is_array($x)||($x['approved']??1)!==0||($x['public']??1)!==0),'safe gaps never grant approval/public output');

$bad=$run;$one=$missing[0];$bad['phase_state']['selection']['business_active']=array('item-x'=>array('concept'=>$one,'rank'=>1));
$r=$h->gapContract($bad,$coverage);
ok(($r['error_code']??'')==='business_gapfill_public_invariant_failed','selected safe winner missing from public remains hard invariant failure');

$bad=$run;$bad['phase_state']['selection']['owner']='run:other';$r=$h->gapContract($bad,$coverage);
ok(($r['error_code']??'')==='business_safe_gap_proof_missing','wrong UUID selection proof is rejected');

$bad=$run;array_pop($bad['phase_state']['selection']['business_target_concepts']);$r=$h->gapContract($bad,$coverage);
ok(($r['error_code']??'')==='business_safe_gap_scope_mismatch','targeted gap-fill scope mismatch is rejected');

$bad=$run;$bad['gapfill']['attempts']=0;$r=$h->gapContract($bad,$coverage);
ok(($r['error_code']??'')==='business_safe_gap_without_gapfill','missing families cannot bypass canonical gap-fill');

$newMissing=$missing;$newMissing[]=$covered[0];sort($newMissing,SORT_STRING);
$newCoverage=array('required'=>311,'covered'=>90,'missing'=>$newMissing,'counts'=>array());
$r=$h->gapContract($run,$newCoverage);
ok(($r['error_code']??'')==='business_safe_gap_new_missing_family','new missing family after gap-fill is not silently reclassified as supply gap');

$full=array('required'=>311,'covered'=>311,'missing'=>array(),'counts'=>array());$r=$h->gapContract($run,$full);
ok(($r['status']??'')==='pass'&&($r['coverage']['contract_status']??'')==='complete'&&($r['coverage']['open_gap_count']??-1)===0,'full 311/311 coverage remains normal complete path');

if(getenv('PPAR_EXPECT_V650_MIGRATION')==='1'){
$failed=array(
 'schema'=>'1.0','build'=>'6.49.0-public-coverage-target-bridge-rootfix-20260821','run_uuid'=>$uuid,
 'status'=>'failed','phase'=>'failed','finished_at'=>12345,'error_code'=>'insufficient_safe_sources','error_message'=>'old terminal',
 'config_snapshot'=>array('seller_routes'=>array('business'=>1,'private'=>1)),
 'coverage'=>$coverage,'gapfill'=>array('attempts'=>1,'missing'=>$missing),
 'phase_state'=>array('refresh'=>array('sentinel'=>'KEEP_REFRESH'),'discovery'=>array('sentinel'=>'OLD_DISCOVERY'),'selection'=>$selection),
 'errors'=>array(array('code'=>'insufficient_safe_sources','at'=>12345,'details'=>array('phase'=>'coverage_verify','build'=>'6.49.0-public-coverage-target-bridge-rootfix-20260821'))),
 'source_sentinel'=>array('do_not_touch'=>1),'end_manifest'=>array('old'=>1)
);
$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE]=$failed;$h->migrate();$after=$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE];
ok(($after['run_uuid']??'')===$uuid,'V6.49 stale-gap migration preserves exact UUID');
ok(($after['status']??'')==='running'&&($after['phase']??'')==='coverage_verify','V6.49 stale-gap migration re-enters current coverage verification');
ok(($after['phase_state']['refresh']['sentinel']??'')==='KEEP_REFRESH','migration preserves upstream refresh/source evidence');
ok(($after['phase_state']['discovery']??null)===array()&&($after['phase_state']['selection']??null)===array(),'migration discards stale discovery and selection proof');
ok(($after['coverage']??null)===array(),'migration discards stale coverage truth');
ok(absint($after['gapfill']['attempts']??99)===0&&($after['gapfill']['missing']??null)===array(),'migration resets stale gapfill so exactly one current canonical gapfill may run');
ok(($after['source_sentinel']['do_not_touch']??0)===1,'migration preserves unrelated durable state');
ok(($after['error_code']??'')===''&&($after['error_message']??'')==='','migration clears only top-level terminal error for continuation');
ok(count((array)($after['recovery_history']??array()))===1&&($after['recovery_history'][0]['reason']??'')==='safe_supply_gap_stale_proof_recovery','migration records versioned stale-proof recovery history');
$once=serialize($after);$h->migrate();$twice=serialize($GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE]);
ok($once===$twice,'recovery is idempotent after state is reopened');
$v650stale=$failed;
$v650stale['build']='6.50.0-coverage-gap-contract-rootfix-20260821';
$v650stale['status']='failed';$v650stale['phase']='failed';$v650stale['finished_at']=12399;
$v650stale['error_code']='business_safe_gap_new_missing_family';$v650stale['error_message']='live drift';
$v650stale['resume_reason']='safe_supply_gap_contract_recovery';
$v650stale['errors']=array(array('code'=>'business_safe_gap_new_missing_family','at'=>12399,'details'=>array('phase'=>'public_verify','build'=>'6.50.0-coverage-gap-contract-rootfix-20260821')));
$v650stale['recovery_history']=array(array('at'=>12346,'reason'=>'safe_supply_gap_contract_recovery','error_code'=>'insufficient_safe_sources','migration_key'=>'old-v650-marker'));
$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE]=$v650stale;$h->migrate();$after=$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE];
ok(($after['run_uuid']??'')===$uuid&&($after['status']??'')==='running'&&($after['phase']??'')==='coverage_verify','actual V6.50 stale-proof live signature re-enters current coverage on same UUID');
ok(($after['coverage']??null)===array()&&absint($after['gapfill']['attempts']??99)===0,'actual V6.50 stale-proof recovery discards old coverage and gapfill proof');
ok(($after['phase_state']['refresh']['sentinel']??'')==='KEEP_REFRESH'&&($after['phase_state']['discovery']??null)===array()&&($after['phase_state']['selection']??null)===array(),'actual V6.50 stale-proof recovery keeps upstream evidence but resets derived components');
$neg=$v650stale;$neg['recovery_history']=array();
$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE]=$neg;$h->migrate();$after=$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE];
ok(($after['status']??'')==='failed'&&($after['error_code']??'')==='business_safe_gap_new_missing_family','unproven V6.50 public failure remains hard failed');
$neg=$failed;$neg['phase_state']['selection']['business_active']=array('item-x'=>array('concept'=>$missing[0],'rank'=>1));
$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE]=$neg;$h->migrate();$after=$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE];
ok(($after['status']??'')==='failed'&&($after['error_code']??'')==='insufficient_safe_sources','migration refuses inconsistent old safe-winner proof');
$neg=$failed;$neg['errors'][0]['details']['phase']='public_verify';
$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE]=$neg;$h->migrate();$after=$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE];
ok(($after['status']??'')==='failed','migration refuses wrong V6.49 failure phase');
$neg=$failed;$neg['build']='6.48.0-canonical-refresh-authority-rootfix-20260821';$neg['errors'][0]['details']['build']=$neg['build'];
$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE]=$neg;$h->migrate();$after=$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE];
ok(($after['status']??'')==='failed'&&($after['build']??'')===$neg['build'],'migration refuses non-V6.49/non-V6.50 stale-proof build');
$neg=$failed;$neg['error_code']='transport_failed';$neg['errors']=array(array('code'=>'transport_failed','at'=>12345,'details'=>array('phase'=>'coverage_verify','build'=>'6.49.0-public-coverage-target-bridge-rootfix-20260821')));
$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE]=$neg;$h->migrate();$after=$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE];
ok(($after['status']??'')==='failed'&&($after['error_code']??'')==='transport_failed','unrelated technical error remains hard failed');
$neg=$failed;$neg['config_snapshot']['seller_routes']['business']=0;
$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE]=$neg;$h->migrate();$after=$GLOBALS['__opts'][V650Harness::OPTION_EBAY_RUN_STATE];
ok(($after['status']??'')==='failed','recovery never crosses seller-route scope');
}
echo "ASSERTIONS=$assertions FAIL=$fail\n";exit($fail?1:0);
