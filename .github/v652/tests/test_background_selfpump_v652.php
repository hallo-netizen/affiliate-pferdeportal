<?php
$root=getenv('PPAR_TEST_PLUGIN_DIR');
if(!$root){fwrite(STDERR,"missing PPAR_TEST_PLUGIN_DIR\n");exit(2);} 
$run=file_get_contents($root.'/includes/trait-ppar-ebay-run.php');
$main=file_get_contents($root.'/pferdeportal-affiliate-router.php');
$f=0;$n=0;function a($v,$m){global$f,$n;$n++;echo($v?'PASS ':'FAIL ').$m."\n";if(!$v)$f++;}
a(strpos($run,'private function ebay_run_register_background_kick')!==false,'core-cron kick registration exists');
a(strpos($run,'public function run_ebay_worker_background_kick')!==false,'public shutdown dispatcher exists');
a(strpos($run,"add_action('shutdown', array(\$this, 'run_ebay_worker_background_kick'), PHP_INT_MAX)")!==false,'dispatcher is registered only for request shutdown');
a(strpos($run,'return spawn_cron(time()) !== false;')!==false,'dispatcher uses WordPress core spawn_cron');
a(strpos($run,'wp_remote_post(')===false,'no plugin-owned HTTP loopback is reintroduced in canonical run trait');
a(strpos($run,'$when = time();')!==false,'running canonical work is due immediately instead of waiting for unrelated traffic');
a(strpos($run,"if (\$status === 'paused')")!==false && strpos($run,'$resume_at = absint')!==false,'pause keeps persisted resume boundary');
a(strpos($main,"const EBAY_WORK_BLOCK_PAUSE_SECONDS = 1;")!==false,'budget pause is short enough for autonomous core-cron chaining');
a(strpos($main,'private $ebay_worker_kick_registered = false;')!==false,'kick registration has per-request idempotence guard');
a(strpos($main,'private $ebay_worker_kick_at = 0;')!==false,'kick due timestamp is tracked');
a(strpos($run,'public function run_ebay_admin_ajax_tick()')!==false && strpos($run,"return array('status'=>sanitize_key((string)(\$run['status'] ?? 'running')),'transport'=>'wp_cron'")!==false,'admin/browser path remains scheduler-only');
a(strpos($main,"add_action(self::EBAY_WORKER_HOOK, array(\$this, 'run_ebay_canonical_worker'));")!==false,'existing canonical worker remains single fach worker authority');
if(getenv('PPAR_V652_STAGE')==='final'){
    $read=file_get_contents($root.'/readme.txt');
    a(strpos($main,' * Version: 6.52.0')!==false && strpos($main,"const VERSION = '6.52.0';")!==false,'final version is 6.52.0');
    a(strpos($main,"6.52.0-core-cron-selfpump-rootfix-20260822")!==false,'final runtime build exact');
    a(strpos($read,'CORE-CRON SELFPUMP ROOTFIX')!==false,'README documents live-rootcause background transport correction');
}
echo "ASSERTIONS=$n FAIL=$f\n";exit($f?1:0);
