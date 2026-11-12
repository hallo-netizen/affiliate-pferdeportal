<?php
/** One-time QA: ACTUAL PSTE 0.57.144.22 capability output vs ACTUAL PSERC 0.28.54 binding code.
 * Run: php this.php /path/to/extracted/portal-seo-editorial-plan-compiler PSTE_V22_REAL_READ_CAPABILITY_20261108.json
 * Does NOT call WordPress, modify K0, judge SEO quality or simulate a real WP end-to-end.
 */
declare(strict_types=1);
define('ABSPATH','/qa/');
$root=rtrim((string)($argv[1]??''),'/').'/';
$fixture=(string)($argv[2]??'');
if(!is_file($root.'contracts/seo-engine-capability-binding-v2.json')||!is_file($fixture))
    throw new RuntimeException('REAL_PSERC_AND_REAL_PSTE_CAPABILITY_REQUIRED');
define('PSERC_DIR',$root);
require $root.'includes/class-pserc-stable-json.php';
require $root.'includes/class-pserc-seo-source-binding.php';
$producer=json_decode(file_get_contents($fixture),true,512,JSON_THROW_ON_ERROR);
$originalBinding=json_decode(file_get_contents($root.'contracts/seo-engine-capability-binding-v2.json'),true,512,JSON_THROW_ON_ERROR);
if(!is_array($producer)||!is_array($originalBinding))
    throw new RuntimeException('REAL_INTERFACE_INPUT_INVALID');
$actual=PSERC_SEO_Source_Binding::validate(null,null,$producer);
if(empty($actual['ok'])||($actual['status']??'')!=='PSERC_SEO_CAPABILITY_BINDING_PASS')
    throw new RuntimeException('REAL_PSTE_TO_PSERC_BINDING_FAILED:'.json_encode($actual));
if(!hash_equals((string)$producer['capability_sha256'],(string)$actual['capability_sha256']))
    throw new RuntimeException('REAL_READ_CAPABILITY_SHA_CHANGED');
echo "PASS actual unchanged PSTE v22 PHP-produced capability against full PSERC 0.28.54 real source binding\n";
$mutated=$producer;$mutated['write_capability_exposed']=true;
$mutated['capability_sha256']=PSERC_Stable_Json::hash(array_diff_key($mutated,['capability_sha256'=>1]));
$bad=PSERC_SEO_Source_Binding::validate(null,$originalBinding,$mutated);
if(!empty($bad['ok']))throw new RuntimeException('PRODUCTION_WRITE_WAS_ACCEPTED');
echo "PASS exact real PSERC binding forbids write-capable producer\n";
echo "PAIRED_SOURCE_INTERFACE_QA_PASS; WORDPRESS_LIVE_AND_K0_NOT_TESTED\n";
