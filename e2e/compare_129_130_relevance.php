<?php
if (!defined('ABSPATH')) exit(2);
$o=Pferdeportal_Affiliate_Router::instance();
function ccall($o,$n,...$a){$m=new ReflectionMethod($o,$n);$m->setAccessible(true);return $m->invokeArgs($o,$a);}
$ctx=ccall($o,'get_content_context',186);$ctx['slot_type']='category_product_1';
$c=ccall($o,'ranked_campaigns_for_slot',$ctx,'category_product_1','');
function brief($rows){$out=[];foreach(array_slice(array_values($rows),0,12) as $r){$x=$r['campaign']??[];$out[]=['id'=>(int)($x['post_id']??0),'provider'=>sanitize_key((string)($x['network']??'')),'spec'=>(int)($r['specificity']??0),'matches'=>(int)($r['matches']??0),'priority'=>(int)($r['priority']??0),'title'=>(string)($x['title']??'')];}return $out;}
$best=(int)($c[0]['specificity']??0);
$v129=array_values(array_filter($c,fn($r)=>(int)($r['specificity']??0)===$best));
$v130=($best>=500&&$best<1000)?array_values(array_filter($c,fn($r)=>($s=(int)($r['specificity']??0))>=500&&$s<1000)):$v129;
echo 'BEST_SPEC='.$best."\n";
echo 'RAW_TOP='.wp_json_encode(brief($c),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'V129_TOP='.wp_json_encode(brief($v129),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'V130_TOP='.wp_json_encode(brief($v130),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
