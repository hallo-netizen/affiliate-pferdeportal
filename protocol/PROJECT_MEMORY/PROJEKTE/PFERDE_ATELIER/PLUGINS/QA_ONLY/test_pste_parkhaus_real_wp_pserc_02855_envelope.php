<?php
/**
 * ONE test-only WordPress integration check for ORIGINAL PSTE reader with a
 * byte-bound PSERC-0.28.55 snapshot genuinely produced by original PSERC PHP.
 * This is NOT PSERC installation or real user plan. No runtime classes shipped.
 * wp eval-file THIS_FILE FIXTURE_JSON
 */
declare(strict_types=1);
if(!defined('ABSPATH')||!class_exists('PSTE_Mini_Workflow'))
    throw new RuntimeException('REAL_WORDPRESS_WITH_PSTE_REQUIRED');
$fixture=json_decode(file_get_contents((string)($args[0]??'')),true,512,JSON_THROW_ON_ERROR);
if(($fixture['fixture_description']??'')!=='ACTUAL_PSERC_02855_STORE_OUTPUT_WITH_SYNTHETIC_QA_ARTICLE_DATA')
    throw new RuntimeException('WRONG_REAL_PSERC_02855_FIXTURE');
function qaCanonical($v) {
    if(!is_array($v)) return $v;
    if(array_is_list($v))return array_map('qaCanonical',$v);
    ksort($v,SORT_STRING);
    foreach($v as $k=>$item)$v[$k]=qaCanonical($item);
    return $v;
}
function qaHash($v):string {
    $s=wp_json_encode(qaCanonical($v),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRESERVE_ZERO_FRACTION);
    if(!is_string($s))throw new RuntimeException('QA_JSON_INVALID');
    return hash('sha256',$s);
}
function qaPass(bool $good,string $message):void {
    if(!$good)throw new RuntimeException('FAIL '.$message);
    echo "PASS ".$message."\n";
}
// Test-only adapter checks the original PSERC SHA-bound envelope from the
// original PHP producer. Actual PSERC plugin is NOT loaded by this script.
final class PSERC_Plan_Snapshot_Store {
    public static function getActive():array{return (array)get_option('pserc_plan_active_snapshot_v1',[]);}
    public static function verifyHeader(array $h):bool {
        if(($h['contract']??'')!=='PSERC_PLAN_SNAPSHOT_V1')return false;
        $digest=(string)($h['snapshot_sha256']??'');
        unset($h['snapshot_sha256']);
        return preg_match('/^[a-f0-9]{64}$/',$digest)===1&&hash_equals($digest,qaHash($h));
    }
    public static function getRecord(string $generation,string $kind,int $i):?array {
        $key='pserc_plan_'.$generation.'_'.$kind.'_'.str_pad((string)$i,6,'0',STR_PAD_LEFT);
        $env=get_option($key,null);if($env===null)return null;
        if(!is_array($env)||($env['contract']??'')!=='PSERC_PLAN_RECORD_V1'
            ||($env['generation']??'')!==$generation||($env['kind']??'')!==$kind
            ||($env['index']??-1)!==$i)throw new RuntimeException('PSERC_RECORD_ENVELOPE_INVALID');
        $payload=(array)($env['payload']??[]);
        qaPass(hash_equals((string)($env['payload_sha256']??''),qaHash($payload)),
            'authentic PSERC 0.28.55 generated record payload hash '.$i);
        $copy=$env;unset($copy['record_sha256']);
        if(!hash_equals((string)($env['record_sha256']??''),qaHash($copy)))
            throw new RuntimeException('PSERC_RECORD_ENVELOPE_HASH_INVALID');
        return $payload;
    }
}
final class PSERC_Plan_Dependency_Fingerprint {
    public static function isCurrent(array $d):bool {
        // Test-only freshness baseline, NOT production PSERC dependency data.
        return ($d['fixture_scope']??'')==='QA_ONLY_NOT_REAL_EDITORIAL_PLAN';
    }
}
$before=PSTE_Mini_Workflow::readParkhausForMini();
qaPass(empty($before['complete'])&&($before['reason']??'')==='PSERC_PLAN_NOT_PROVEN_COMPLETE',
    'missing PSERC active plan blocks real WordPress owner export');
foreach((array)$fixture['options'] as $k=>$v)
    update_option((string)$k,$v,false);
$runtime=['items'=>[
    'qa-existing-article'=>['canonical_article_id'=>'qa-existing-article',
       'plan_slot_sha256'=>hash('sha256','PPM679-existing-saved-plan-slot'),
       'status'=>'PLANNED','title'=>'Bereits geplante Kaufberatung',
       'category_slug'=>'regendecken','article_type'=>'Ratgeber',
       'target_keyword'=>'regendecken kaufen']]];
update_option('ppm679_editorial_plan_runtime_state_v1',$runtime,false);
$s=PSTE_Mini_Workflow::readParkhausForMini();
echo "WP_REAL_PSTE_PSERC_ENVELOPE_RESULT ".wp_json_encode([
    'complete'=>$s['complete'],'reason'=>$s['reason'],
    'wp_count'=>$s['sources']['WORDPRESS']['item_count']??null,
    'pste_count'=>$s['sources']['PSTE_PLAN']['item_count']??null,
    'pserc_count'=>$s['sources']['PSERC_ACTIVE_PLAN']['item_count']??null,
    'runtime_count'=>$s['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']['item_count']??null,
    'runtime_status'=>$s['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']['status']??null
],JSON_UNESCAPED_UNICODE)."\n";
qaPass(!empty($s['complete'])&&($s['sources']['PSERC_ACTIVE_PLAN']['item_count']??null)===2,
    'real WordPress/PSTE reads both original PSERC-0.28.55 envelope records');
qaPass(($s['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']['status']??'')==='PRESENT'
       &&($s['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']['item_count']??null)===1,
    'real WP option reader includes already saved synthetic PPM679 plan');
$recs=array_values(array_filter((array)$s['items'],
    static fn($i)=>is_array($i)&&($i['source']??'')==='PSERC_ACTIVE_PLAN'));
qaPass(count($recs)===2&&$recs[0]['status']==='READY_FOR_METADATA_HANDOFF'
       &&$recs[1]['status']==='HELD'
       &&$recs[1]['plan_slot']==='a193b347b0c56688bf9885695fd6ce9dd1fbcafd5956236954bb6be91f3009e0',
    'PSTE keeps both PSERC READY and HELD planned article slots');
$firstKey=(string)$fixture['record_keys'][0];
$old=get_option($firstKey);
$tampered=$old;$tampered['payload']['title']['production_title']='Falscher Titel';
update_option($firstKey,$tampered,false);
$bad=PSTE_Mini_Workflow::readParkhausForMini();
qaPass(empty($bad['complete'])&&$bad['sha256']==='',
    'forged PSERC record is not exported as complete');
update_option($firstKey,$old,false);
$header=get_option('pserc_plan_active_snapshot_v1');
$stale=$header;$stale['dependency']['fixture_scope']='STALE';
update_option('pserc_plan_active_snapshot_v1',$stale,false);
$blocked=PSTE_Mini_Workflow::readParkhausForMini();
qaPass(empty($blocked['complete'])&&$blocked['sha256']==='',
    'stale PSERC header is not accepted');
update_option('pserc_plan_active_snapshot_v1',$header,false);
$restored=PSTE_Mini_Workflow::readParkhausForMini();
qaPass(!empty($restored['complete']),'restored original unchanged PSERC test envelope is complete');
delete_option('ppm679_editorial_plan_runtime_state_v1');
$missing=PSTE_Mini_Workflow::readParkhausForMini();
echo "WP_REAL_PPM679_MISSING_PLAN_SAFETY complete=".(!empty($missing['complete'])?'YES':'NO').
    " status=".($missing['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']['status']??'UNKNOWN')."\n";
echo "PSTE_PSERC_02855_ENVELOPE_WP_QA_DONE; USER_REAL_EDITORIAL_PLAN_NOT_USED\n";
