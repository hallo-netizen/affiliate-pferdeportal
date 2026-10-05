<?php
$GLOBALS['fails']=array();
function tcheck($ok,$name,$detail=''){
  echo ($ok?'PASS ':'FAIL ').$name.($detail!==''?' :: '.$detail:'')."\n";
  if(!$ok)$GLOBALS['fails'][]=$name;
}
if(!class_exists('Pferdeportal_Affiliate_Router')){fwrite(STDERR,"FATAL plugin missing\n");exit(2);}
if(Pferdeportal_Affiliate_Router::VERSION!=='6.72.185'){fwrite(STDERR,"FATAL version ".Pferdeportal_Affiliate_Router::VERSION."\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($name)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m;};
$rp=function($name)use($o){$p=new ReflectionProperty($o,$name);$p->setAccessible(true);return $p;};
$call=function($name,...$args)use($rm,$o){return $rm($name)->invokeArgs($o,$args);};

update_option('ppar_enabled','1',false);
update_option('ppar_assignments_v1',array(),false);
delete_option('ppar_debug');

$http=0;
add_filter('pre_http_request',function($pre,$args,$url)use(&$http){$http++;return new WP_Error('blocked','network forbidden');},PHP_INT_MAX,3);

$root=wp_insert_post(array('post_type'=>'page','post_status'=>'publish','post_title'=>'Ausrüstung Tier Gate','post_name'=>'ausruestung-tier-gate'));
$reit=wp_insert_post(array('post_type'=>'page','post_status'=>'publish','post_title'=>'Reithelme Tier Gate','post_name'=>'reithelme-tier-gate','post_parent'=>$root));
if(!$root||!$reit){fwrite(STDERR,"FATAL page create\n");exit(2);}

$save=$rm('save_campaign_record');
$ids=array();
$make=function($id,$args=array())use($save,$o,&$ids){
  $base=array(
    'id'=>$id,'active'=>1,'creative_type'=>'banner','network'=>'manual','programme_status'=>'active','source'=>'output_object_v4',
    'render_mode'=>'image_link','title'=>$id,'description'=>'','button_text'=>'Mehr erfahren',
    'image_url'=>'https://img.example.test/'.$id.'.jpg','url'=>'https://click.example.test/'.$id,
    'target'=>'_blank','placements'=>array('product_after_category_tiles'),'assignment_mode'=>'fallback','priority'=>10,
    'health_check_enabled'=>false,'dimensions'=>'1200x120','partner'=>'partner-'.$id,
  );
  $c=array_replace($base,$args);
  $pid=$save->invoke($o,$c,0);
  if(is_wp_error($pid)||!$pid){fwrite(STDERR,"FATAL campaign ".$id."\n");exit(2);}
  $ids[$id]=(int)$pid;
};
$flush=function()use($rp,$o){
  try{$rp('campaigns_request_cache')->setValue($o,null);}catch(Throwable $e){}
  foreach(array('ranked_campaigns_request_cache','ranked_campaign_candidate_index_request_cache','ranked_campaign_raw_records_request_cache','ranked_campaign_from_post_request_cache') as $p){
    try{$rp($p)->setValue($o,array());}catch(Throwable $e){}
  }
};
$set=function($active)use(&$ids,$flush){
  foreach($ids as $key=>$pid){
    $d=get_post_meta($pid,'ppar_campaign_data',true);$d=is_array($d)?$d:array();
    $d['active']=in_array($key,$active,true)?1:0;update_post_meta($pid,'ppar_campaign_data',$d);
  }
  $flush();
};
$cid=function($sel){return (string)($sel['campaign']['id']??'');};

$make('exact-one',array(
  'assignment_mode'=>'page_tree',
  'automation_target_keys'=>array('page:reithelme-tier-gate'),
  'priority'=>1,'partner'=>'helmet-exact'
));
$make('general-a',array('assignment_mode'=>'fallback','priority'=>999,'partner'=>'general-a'));
$make('general-b',array('assignment_mode'=>'fallback','priority'=>998,'partner'=>'general-b'));
$make('general-c',array('assignment_mode'=>'fallback','priority'=>997,'partner'=>'general-c'));

$ctx=$call('get_content_context',$reit);

// A: exactly one exact banner must monopolize every banner position.
$set(array('exact-one','general-a','general-b','general-c'));
$q0=(int)$GLOBALS['wpdb']->num_queries;
$p1=$call('select_campaign_for_slot_position',$ctx,'product_after_category_tiles',1);
$p2=$call('select_campaign_for_slot_position',$ctx,'product_after_category_tiles',2);
$q1=(int)$GLOBALS['wpdb']->num_queries;
echo 'CASE_A '.wp_json_encode(array('p1'=>$cid($p1),'p2'=>$cid($p2),'queries'=>$q1-$q0,'http'=>$http),JSON_UNESCAPED_SLASHES)."\n";
tcheck($cid($p1)==='exact-one','ONE_EXACT_position1_exact',$cid($p1));
tcheck($cid($p2)==='exact-one','ONE_EXACT_position2_must_stay_exact',$cid($p2));
tcheck(!in_array($cid($p1),array('general-a','general-b','general-c'),true) && !in_array($cid($p2),array('general-a','general-b','general-c'),true),'ONE_EXACT_general_never_enters_delivery');

// B: multiple exact banners may rotate, but only inside exact group.
$make('exact-two',array(
  'assignment_mode'=>'page_tree',
  'automation_target_keys'=>array('page:reithelme-tier-gate'),
  'priority'=>2,'partner'=>'helmet-exact-2'
));
$set(array('exact-one','exact-two','general-a','general-b','general-c'));
$p1b=$call('select_campaign_for_slot_position',$ctx,'product_after_category_tiles',1);
$p2b=$call('select_campaign_for_slot_position',$ctx,'product_after_category_tiles',2);
echo 'CASE_B '.wp_json_encode(array('p1'=>$cid($p1b),'p2'=>$cid($p2b),'http'=>$http),JSON_UNESCAPED_SLASHES)."\n";
$exactSet=array('exact-one','exact-two');
tcheck(in_array($cid($p1b),$exactSet,true),'MULTI_EXACT_position1_exact',$cid($p1b));
tcheck(in_array($cid($p2b),$exactSet,true),'MULTI_EXACT_position2_exact',$cid($p2b));
tcheck($cid($p1b)!==$cid($p2b),'MULTI_EXACT_rotation_within_exact_group',$cid($p1b).'|'.$cid($p2b));
tcheck($http===0,'FRONTEND_zero_http_calls','http='.$http);

echo 'SUMMARY passes='.(7-count($GLOBALS['fails'])).' failures='.count($GLOBALS['fails'])."\n";
if($GLOBALS['fails']){echo 'FAILURES '.wp_json_encode($GLOBALS['fails'])."\n";exit(1);}
echo "STRICT_BEST_BANNER_TIER_PASS\n";
