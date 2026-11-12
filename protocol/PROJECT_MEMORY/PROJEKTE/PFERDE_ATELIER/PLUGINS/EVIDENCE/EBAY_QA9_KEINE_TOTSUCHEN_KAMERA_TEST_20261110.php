<?php
error_reporting(E_ALL);
define('ABSPATH','/');
function wp_strip_all_tags($x){return strip_tags((string)$x);}
function remove_accents($x){return strtr((string)$x,['ä'=>'a','ö'=>'o','ü'=>'u','Ä'=>'A','Ö'=>'O','Ü'=>'U','ß'=>'ss']);}
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x)));}
function sanitize_text_field($x){return trim((string)$x);}
function sanitize_title($x){return trim(preg_replace('/[^a-z0-9-]+/','-',strtolower(remove_accents($x))),'-');}
function absint($x){return abs((int)$x);}
function is_wp_error($x){return $x instanceof WP_Error;}
class WP_Error {private $c,$m;function __construct($c,$m){$this->c=$c;$this->m=$m;}function get_error_code(){return $this->c;}function get_error_message(){return $this->m;}}
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay.php';
class FullClassifierLocal {use PPAR_Ebay_Trait;
 private function ebay_portal_catalog(){return json_decode(file_get_contents(__DIR__.'/affiliate-portal-router/assets/ebay-portal-catalog-v2.json'),true);}
 private function ebay_content_policy_reason($x){return '';}
 public function go($id,$title,$cat,$short=''){
  $m=new ReflectionMethod($this,'ebay_business_classify_portal_item_strict');
  $x=['title'=>$title,'short_description'=>$short,'category_names'=>[$cat], 'raw'=>['title'=>$title,'categories'=>[['categoryName'=>$cat]]]];
  $r=['business_concept_id'=>$id,'query'=>$title.' Pferd','expected_business_concept_id'=>$id];
  $z=$m->invoke($this,$x,$r);
  return is_wp_error($z)?['code'=>$z->get_error_code(),'message'=>$z->get_error_message()]:['ok'=>true,'concept_id'=>$z['product_concept_id']??'none','confidence'=>$z['score']??0];
 }
}
$a=new FullClassifierLocal;
foreach([
 ['concept-anhangerkameras','Rückfahrkamera Pferdeanhänger','Anhänger Kamera',''],
 ['concept-anhangerkameras','Rückfahrkamera für Pferdeanhänger','Rückfahrkamera Fahrzeug',''],
 ['concept-anhangerkameras','Anhängerkamera Rückfahrkamera Funk Pferd','Rückfahrkamera Fahrzeug',''],
 ['concept-anhangerkameras','Funk Rückfahrkamera Pferdeanhänger 12V','Auto Kamera',''],
 ['concept-anhangerkameras','Anhängerkameras Pferd','Anhänger Kamera',''],
] as $case){try{$z=$a->go(...$case);}catch(Throwable $e){$z=['exception'=>get_class($e),'message'=>$e->getMessage()];}echo json_encode(['title'=>$case[1],'result'=>$z],JSON_UNESCAPED_UNICODE)."\n";}