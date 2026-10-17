<?php
declare(strict_types=1);
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
function wp_strip_all_tags($s){return strip_tags($s);}
class PSTE_Sandbox_Record_Store {
  public static array $rows=[];
  public static function isComplete():bool{return true;}
  public static function forEachRecord(callable $cb):void{foreach(self::$rows as $id=>$r){if($cb($r,$id)===false)break;}}
}
require (getenv('PSTE_SOURCE_DIR')?:'/mnt/data/seo_work/modified/Portal SEO Topic Engine').'/includes/class-pste-sandbox-record-contract.php';
require (getenv('PSTE_SOURCE_DIR')?:'/mnt/data/seo_work/modified/Portal SEO Topic Engine').'/includes/class-pste-semantic-review-sandbox.php';
function makeRecord(string $id,string $type):array{
  $row=['sandbox_id'=>$id,'status'=>'AUTO_REENTRY_ELIGIBLE','internal_proposal'=>['reentry_proposal'=>[
    'contract'=>'PSTE_SANDBOX_REENTRY_ENVELOPE_V1','status'=>'AUTO_REENTRY_ELIGIBLE','pool_key'=>$id
  ]]];
  if($type==='tampered')$row['sandbox_dataflow']=['worker_checkpoint_sha256'=>str_repeat('c',64)];
  elseif($type==='legacy')$row['sandbox_dataflow']=[];
  return $row;
}
PSTE_Sandbox_Record_Store::$rows=['legacy'=>makeRecord('legacy','legacy'),'altered'=>makeRecord('altered','tampered')];
$r=PSTE_Semantic_Review_Sandbox::automaticReentryEnvelopes(5);
if(count($r)!==2 || ($r[0]['checkpoint_error_code']??'NOT_EMPTY')!=='' || ($r[1]['checkpoint_error_code']??'')!=='PSTE_SANDBOX_REENTRY_WORKER_CHECKPOINT_INVALID')throw new RuntimeException('CHECKPOINT_EXTRACTION_FAILED:'.json_encode($r));
echo "PASS checkpoint extractor checks legacy compatibility and rejects tampered record before DB call\n";