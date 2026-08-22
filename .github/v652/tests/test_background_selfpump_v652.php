<?php
$root=getenv('PPAR_TEST_PLUGIN_DIR');
if(!$root){fwrite(STDERR,"missing PPAR_TEST_PLUGIN_DIR\n");exit(2);} 
$run=file_get_contents($root.'/includes/trait-ppar-ebay-run.php');
$main=file_get_contents($root.'/pferdeportal-affiliate-router.php');
$f=0;$n=0;function a($v,$m){global$f,$n;$n++;echo($v?'PASS ':'FAIL ').$m."\n";if(!$v)$f++;}
a(strpos($run,'private function ebay_run_register_background_dispatch')!==false,'background dispatch registration exists');
a(strpos($run,'public function run_ebay_worker_background_dispatch')!==false,'shutdown dispatcher exists');
a(strpos($run,"add_action('shutdown', array(\$this, 'run_ebay_worker_background_dispatch'), PHP_INT_MAX)")!==false,'dispatcher is registered only at request shutdown');
a(strpos($run,'private function ebay_run_spawn_core_cron_handoff')!==false,'cron-request handoff helper exists');
a(substr_count($run,'wp_remote_post(')===1,'exactly one controlled HTTP call exists in canonical run trait');
a(strpos($run,"site_url('wp-cron.php')")!==false,'controlled HTTP handoff targets WordPress core wp-cron only');
a(strpos($run,"defined('DOING_CRON') && DOING_CRON")!==false,'cron context is explicitly separated from normal core spawn');
a(strpos($run,'spawn_cron(microtime(true))')!==false,'normal request path uses WordPress core spawn_cron');
a(strpos($run,'$when = time();')!==false,'running canonical work is due immediately');
a(strpos($run,'$pause_seconds = max(1, $pause_seconds);')!==false,'budget pause has a bounded one-second minimum');
a(strpos($main,"const EBAY_WORK_BLOCK_PAUSE_SECONDS = 1;")!==false,'configured background block yield is one second');
a(strpos($main,'private $ebay_worker_dispatch_registered = false;')!==false,'dispatch registration is request-idempotent');
a(strpos($main,'private $ebay_worker_dispatch_at = 0;')!==false,'dispatch due timestamp is tracked');
a(strpos($run,'public function run_ebay_admin_ajax_tick()')!==false && strpos($run,"'transport'=>'wp_cron'")!==false,'admin/browser path remains scheduler/status compatibility only');
a(strpos($main,"add_action(self::EBAY_WORKER_HOOK, array(\$this, 'run_ebay_canonical_worker'));")!==false,'canonical worker remains sole fach worker hook');
a(strpos($run,'register_rest_route')===false && strpos($run,'wp_ajax_')===false,'no new direct HTTP fach-worker endpoint exists');
if(getenv('PPAR_V652_STAGE')==='final'){
    $read=file_get_contents($root.'/readme.txt');
    a(strpos($main,' * Version: 6.52.0')!==false && strpos($main,"const VERSION = '6.52.0';")!==false,'final version is 6.52.0');
    a(strpos($main,"6.52.0-core-cron-handoff-rootfix-20260822")!==false,'final runtime build exact');
    a(strpos($read,'CORE-CRON HANDOFF ROOTFIX')!==false,'README documents live-rootcause transport correction');
}
echo "ASSERTIONS=$n FAIL=$f\n";exit($f?1:0);
