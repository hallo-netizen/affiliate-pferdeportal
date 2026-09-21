<?php
if (!defined('ABSPATH')) { exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
function zc($o,$m,...$a){$r=new ReflectionMethod($o,$m);$r->setAccessible(true);return $r->invokeArgs($o,$a);}
function zsel($o,$slot){$ctx=zc($o,'get_content_context',186);$ctx['slot_type']=$slot;$s=zc($o,'select_campaign_for_slot',$ctx,$slot,'');return is_array($s)&&is_array($s['campaign']??null)?$s['campaign']:array();}
$phase=getenv('AFF_PHASE')?:'';
if($phase==='broken'){
  $e=get_option('ppar_network_ebay_v1',array());$e=is_array($e)?$e:array();$e['enabled']=1;$e['environment']='production';update_option('ppar_network_ebay_v1',$e,false);
  update_option('ppar_ebay_deletion_state_v1',array('challenge_answered_at'=>0,'last_notification_status'=>'','last_notification_at'=>0,'last_error'=>''),false);
  do_action('init');
  $e=get_option('ppar_network_ebay_v1',array());
  if(!empty($e['enabled'])){fwrite(STDERR,"FAIL_EBAY_NOT_DISABLED\n");exit(10);}
  $gate=zc($o,'control_provider_gate','ebay','pferde-atelier-de');
  if(!is_wp_error($gate)||$gate->get_error_code()!=='control_provider_access_disabled'){fwrite(STDERR,"FAIL_CONTROL_GATE\n");exit(11);}
  $i=get_option('ppar_network_idealo_v1',array());$i=is_array($i)?$i:array();$i['enabled']=1;$i['output_mode']='idealo_only';$i['link_strategy']='products';update_option('ppar_network_idealo_v1',$i,false);
  foreach(array('category_product_1','category_product_2','category_product_3') as $slot){$c=zsel($o,$slot);if(sanitize_key((string)($c['network']??''))==='ebay'){fwrite(STDERR,"FAIL_IDEALO_ONLY_LEAK_".$slot."\n");exit(12);}}
  echo "BROKEN_STATE_PASS control_provider_access_disabled + idealo_only_no_ebay\n";exit(0);
}
if($phase==='restored'){
  $e=get_option('ppar_network_ebay_v1',array());$e=is_array($e)?$e:array();$e['enabled']=1;$e['environment']='production';update_option('ppar_network_ebay_v1',$e,false);
  $i=get_option('ppar_network_idealo_v1',array());$i=is_array($i)?$i:array();$i['enabled']=1;$i['output_mode']='automatic';$i['link_strategy']='products';update_option('ppar_network_idealo_v1',$i,false);
  $now=time();update_option('ppar_ebay_deletion_state_v1',array('challenge_answered_at'=>$now,'last_notification_at'=>$now,'last_notification_status'=>'verified','last_notification_hash'=>str_repeat('a',64),'last_deleted_items'=>0,'last_deleted_creatives'=>0,'last_deleted_outputs'=>0,'last_error'=>''),false);
  update_option('ppar_provider_access_state_v1',array('ebay'=>array('status'=>'connected','last_checked'=>$now,'message'=>'E2E verified'),'idealo'=>array('status'=>'connected','last_checked'=>$now,'message'=>'E2E verified')),false);
  do_action('init');
  $e=get_option('ppar_network_ebay_v1',array());if(empty($e['enabled'])){fwrite(STDERR,"FAIL_EBAY_REDISABLED\n");exit(20);}
  $want=array('category_product_1'=>array(15921,'ebay'),'category_product_2'=>array(16299,'idealo'),'category_product_3'=>array(15986,'ebay'));
  foreach($want as $slot=>$w){$ctx=zc($o,'get_content_context',186);$ctx['slot_type']=$slot;$c=zsel($o,$slot);$id=absint($c['post_id']??0);$n=sanitize_key((string)($c['network']??''));$html=zc($o,'render_affiliate_slot_for_context',186,$ctx,$slot,'');$real=is_string($html)&&$html!==''&&stripos($html,'Produktvorschau')===false;echo "$slot=$id:$n:".($real?'real':'notreal')."\n";if($id!==$w[0]||$n!==$w[1]||!$real){fwrite(STDERR,"FAIL_RESTORED_".$slot."\n");exit(21);}}
  echo "RESTORED_STATE_PASS 15921/16299/15986 real cards\n";exit(0);
}
fwrite(STDERR,"UNKNOWN_PHASE\n");exit(3);
