<?php
if (!defined('ABSPATH')) { fwrite(STDERR,"NO_WP\n"); exit(2); }
$root = getenv('GITHUB_WORKSPACE');
if (!$root) { fwrite(STDERR,"NO_GITHUB_WORKSPACE\n"); exit(3); }
$hashes = array(
 '108'=>'d8aeb69bd67a18072996da9ca8101923e6ff6765a40c5d0d6a6f74bde3be5bb3',
 '109'=>'878060d12bea49e930d22c8ea97404c4adc23e249a3c02314af78fc5c0380e8a',
 '110'=>'52e40af351c079cc6aa8d4acbcc65638d443a491a21f0682b27882a2f9d3ac95',
 '111'=>'19b20be69ed4c31ab9153428418477f6c916020b3f4ad18bb6b1c63bbbc1cf17',
 '112'=>'844d5271f41222ac9763126d75ab9ffae26a209fc6c64219f09af7e215351d90',
 '113'=>'8ad61f8ae1124b1e0474728e7466044e976141152912c51db197c7f049be2ba4',
 '114'=>'41d3a23bc95449046e28376961555b84e47fc181f1ac03ed5a666fb793c28622',
 '115'=>'77a6fade17876c0def0f2221e019eb84fb348ddf418f4813e762bea223880d52',
 '116'=>'faf8681ffe42887f35bb86e7c649deceedbfc16eee1b3d5bd90d5d2cfb9e85e1',
 '117'=>'ddfde12a96a81ce840ffbf732ab3bc7ab591a244642871f6978cc6659f099384',
);
@mkdir('/tmp/history-zips',0777,true);
foreach ($hashes as $v=>$want) {
  $src=$root.'/e2e/history-fixtures/v6.72.'.$v.'.zip.b64';
  $raw=base64_decode(file_get_contents($src),true);
  if ($raw===false) { fwrite(STDERR,"HISTORY_B64_FAIL=$v\n"); exit(4); }
  $zip='/tmp/history-zips/v6.72.'.$v.'.zip';
  file_put_contents($zip,$raw);
  $got=hash_file('sha256',$zip);
  if (!hash_equals($want,$got)) { fwrite(STDERR,"HISTORY_HASH_FAIL=$v:$got\n"); exit(5); }
  echo "HISTORY_FIXTURE_OK=6.72.$v:$got\n";
}
$plugin='/tmp/wp/wp-content/plugins/affiliate-portal-router';
$cmd='rm -rf '.escapeshellarg($plugin).' && unzip -q '.escapeshellarg('/tmp/history-zips/v6.72.108.zip').' -d '.escapeshellarg('/tmp/wp/wp-content/plugins');
passthru($cmd,$rc);
if ($rc!==0) { fwrite(STDERR,"V108_INSTALL_FAIL\n"); exit(6); }
$fixture=getenv('AFF_E2E_FIXTURE');
$child='AFF_E2E_FIXTURE='.escapeshellarg($fixture).' wp eval-file '.escapeshellarg($root.'/e2e/seed_real_state_inner.php').' --path=/tmp/wp';
passthru($child,$rc);
exit($rc);
