<?php
if (!defined('ABSPATH')) { exit(2); }
if (!class_exists('Pferdeportal_Affiliate_Router')) { exit(3); }
$o=Pferdeportal_Affiliate_Router::instance();
$m=new ReflectionMethod($o,'ebay_deletion_compliance_snapshot');$m->setAccessible(true);
$s=$m->invoke($o);
echo 'EBAY_COMPLIANCE_SNAPSHOT='.wp_json_encode($s,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
if (!empty($s['https']) && !empty($s['token_valid']) && !empty($s['challenge_answered']) && !empty($s['signed_notification_verified']) && !empty($s['complete'])) {
  echo "EBAY_COMPLIANCE_COMPLETE\n"; exit(0);
}
$missing=array();
foreach(array('https','token_valid','challenge_answered','signed_notification_verified') as $k){if(empty($s[$k]))$missing[]=$k;}
fwrite(STDERR,'EBAY_COMPLIANCE_MISSING='.implode(',',$missing)."\n");exit(1);
