<?php
if (!defined('ABSPATH')) { exit(2); }
if (!class_exists('Pferdeportal_Affiliate_Router')) { exit(3); }
$o=Pferdeportal_Affiliate_Router::instance();
function a43call($o,$name,...$args){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);}
function a43_count_exact($o,$slug){
  $all=a43call($o,'get_campaigns'); $out=array('total'=>0,'ebay'=>0,'idealo'=>0);
  foreach((array)$all as $c){
    if(!is_array($c)||empty($c['active'])||sanitize_key((string)($c['creative_type']??''))!=='product')continue;
    if(!in_array('page:'.$slug,(array)($c['automation_target_keys']??array()),true))continue;
    $n=sanitize_key((string)($c['network']??'')); if(!in_array($n,array('ebay','idealo'),true))continue;
    $out['total']++;$out[$n]++;
  }
  return $out;
}
$preR=a43_count_exact($o,'reithelme');
$preS=a43_count_exact($o,'halfter-und-stricke-stallhalfter');
echo 'PRE_REITHELME='.wp_json_encode($preR)."\n";
echo 'PRE_STALLHALFTER='.wp_json_encode($preS)."\n";
if($preR['total']!==0){fwrite(STDERR,"FAIL_PRE_REITHELME_NOT_DAMAGED\n");exit(10);}
if($preS['total']!==1){fwrite(STDERR,"FAIL_PRE_STALLHALFTER_NOT_ONE\n");exit(11);}

$snap=a43call($o,'aff043_snapshot');
if(is_wp_error($snap)){fwrite(STDERR,'FAIL_SNAPSHOT='.$snap->get_error_code()."\n");exit(12);}
$state=array(
 'schema'=>'1.0','status'=>'running','phase'=>'augment','cursor'=>0,
 'started_at'=>time(),'started_by'=>0,
 'snapshot_sha256'=>$snap['sha256'],'source_sha256'=>$snap['source_sha256'],
 'stats'=>array(),'errors'=>array()
);
update_option('ppar_aff043_historical_product_state_restore_v1',$state,false);
for($i=0;$i<100;$i++){
  $state=$o->run_aff043_recovery_worker();
  $status=sanitize_key((string)($state['status']??''));
  if($status!=='running')break;
}
$state=get_option('ppar_aff043_historical_product_state_restore_v1',array());
echo 'AFF043_FINAL_STATE='.wp_json_encode($state,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
if(sanitize_key((string)($state['status']??''))!=='complete'){fwrite(STDERR,"FAIL_AFF043_NOT_COMPLETE\n");exit(13);}

$postR=a43_count_exact($o,'reithelme');
$postS=a43_count_exact($o,'halfter-und-stricke-stallhalfter');
echo 'POST_REITHELME='.wp_json_encode($postR)."\n";
echo 'POST_STALLHALFTER='.wp_json_encode($postS)."\n";
if($postR['total']<3||$postR['ebay']<1||$postR['idealo']<1){fwrite(STDERR,"FAIL_REITHELME_SUPPLY\n");exit(14);}
if($postS['total']<3){fwrite(STDERR,"FAIL_STALLHALFTER_SUPPLY\n");exit(15);}

$targets=array(186=>'reithelme',174=>'halfter-und-stricke-stallhalfter');
foreach($targets as $pid=>$slug){
  $ctx=a43call($o,'get_content_context',$pid);$ids=array();$providers=array();
  foreach(array(1,2,3) as $i){
    $slot='category_product_'.$i;$cctx=$ctx;$cctx['slot_type']=$slot;
    $sel=a43call($o,'select_campaign_for_slot',$cctx,$slot,'');
    $c=is_array($sel)&&is_array($sel['campaign']??null)?$sel['campaign']:array();
    $id=absint($c['post_id']??0);$provider=sanitize_key((string)($c['network']??''));
    $html=a43call($o,'render_affiliate_slot_for_context',$pid,$cctx,$slot,'');
    $real=is_string($html)&&$html!==''&&stripos($html,'Produktvorschau')===false;
    echo 'RENDER='.$slug.':'.$slot.':'.$id.':'.$provider.':'.($real?'REAL':'NOT_REAL')."\n";
    if(!$real){fwrite(STDERR,'FAIL_RENDER_'.$slug.'_'.$slot."\n");exit(20+$i);}
    $ids[]=$id;$providers[]=$provider;
  }
  if(count(array_unique($ids))!==3){fwrite(STDERR,'FAIL_NOT_DISTINCT_'.$slug."\n");exit(30);}
  if($slug==='reithelme'&&(!in_array('ebay',$providers,true)||!in_array('idealo',$providers,true))){fwrite(STDERR,"FAIL_REITHELME_PROVIDER_MIX\n");exit(31);}
}
echo "AFF043_LIVE_DAMAGE_RESTORE_PASS\n";
