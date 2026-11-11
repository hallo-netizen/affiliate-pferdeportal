<?php
error_reporting(E_ALL);
define('ABSPATH', __DIR__);
class WP_Error { private $code; private $message; public function __construct($code,$message){$this->code=$code;$this->message=$message;} public function get_error_code(){return $this->code;} public function get_error_message(){return $this->message;} }
function is_wp_error($x){return $x instanceof WP_Error;}
function absint($x){return abs((int)$x);}
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function sanitize_title($x){$x=strtolower((string)$x);$x=str_replace(['ä','ö','ü','ß'],['ae','oe','ue','ss'],$x);return trim(preg_replace('/[^a-z0-9]+/','-',$x),'-');}
function sanitize_text_field($x){return trim((string)$x);}
require $argv[1];
class QA10Facade {use PPAR_Ebay_Trait; public function testReport($run,$plan,$summary){return $this->ebay_missing_family_diagnostic_rows($run,$plan,$summary);} }
$thing=new QA10Facade();
$base=['required'=>298,'covered'=>296,'missing'=>['concept-anhangerbeleuchtung','concept-pferdesattel']];
$profileA=['expected_business_concept_id'=>'concept-anhangerbeleuchtung','query'=>'LED Rückleuchte Pferdeanhänger','requests'=>1,'received'=>20,'accepted'=>0,'hard_blocked'=>6,'technical_blocked'=>2,'duplicates_skipped'=>5,'review_pending'=>3,'capacity_skipped'=>2,'complete'=>true,'hard_reasons'=>['ebay_marketplace_mismatch'=>4,'ebay_portal_topic_negative'=>2],'review_reasons'=>['ebay_business_concept_missing'=>3],'technical_reasons'=>['http_request_failed'=>2]];
$profileB=['expected_business_concept_id'=>'concept-anhangerbeleuchtung','query'=>'Anhängerbeleuchtung','requests'=>1,'received'=>15,'accepted'=>0,'hard_blocked'=>4,'technical_blocked'=>0,'duplicates_skipped'=>8,'review_pending'=>1,'capacity_skipped'=>0,'complete'=>false,'hard_reasons'=>['ebay_marketplace_mismatch'=>4]];
$profileC=['expected_business_concept_id'=>'concept-pferdesattel','query'=>'Dressursattel Pferd','requests'=>1,'received'=>6,'accepted'=>0,'hard_blocked'=>1,'technical_blocked'=>0,'duplicates_skipped'=>0,'review_pending'=>3,'capacity_skipped'=>0,'complete'=>true,'review_reasons'=>['ebay_business_concept_missing'=>3]];
$summary=['profile_stats'=>['a'=>$profileA,'b'=>$profileB,'c'=>$profileC]];
$r=$thing->testReport(['schema'=>'1.0','run_uuid'=>'qa10-fixture','coverage'=>$base],[],$summary);
if(!$r['valid']||$r['required']!==298||count($r['rows'])!==2){fwrite(STDERR,'FAIL report body '.json_encode($r)."\n");exit(2);}
$rows=array_column($r['rows'],null,'id');
$x=$rows['concept-anhangerbeleuchtung'];
$assert=['requests'=>2,'found'=>35,'accepted'=>0,'blocked'=>12];
foreach($assert as $k=>$val){if($x[$k]!==$val)throw new RuntimeException("FAIL $k ".$x[$k]);}
if(strpos($x['assessment'],'Technisch offen')!==0)throw new RuntimeException('Wrong assessment');
if($x['rejection_reasons']['ebay_marketplace_mismatch']!==8)throw new RuntimeException('old reason changed');
$y=$rows['concept-pferdesattel'];if($y['found']!==6||count($y['rejection_reasons'])!==1)throw new RuntimeException('second family mismatch');
if(isset($x['duplicates_skipped'])){
 $add=['duplicates_skipped'=>13,'review_pending'=>4,'capacity_skipped'=>2,'search_incomplete'=>true];
 foreach($add as $k=>$value){if(($x[$k]??null)!==$value)throw new RuntimeException("new metric $k mismatch");}
 echo "PASS QA10: real existing report method, source=298, 2 missing, duplicate=13, review=4, capacity=2, unfinished=true, all previous fields identical\n";
}else{echo "PASS QA9 baseline: real existing report method, source=298, 2 missing; skips/review/capacity ABSENT in report\n";}
$bad=$thing->testReport(['coverage'=>['required'=>298,'missing'=>['concept-random-invalid']]],[],$summary);
if($bad['valid'])throw new RuntimeException('invalid concept accepted');
echo "PASS invalid family fail-closed\n";