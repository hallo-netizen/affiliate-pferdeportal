<?php
$GLOBALS['fails']=array();
function ck($ok,$name,$detail=''){echo ($ok?'PASS ':'FAIL ').$name.($detail!==''?' :: '.$detail:'')."\n";if(!$ok)$GLOBALS['fails'][]=$name;}
if(!class_exists('Pferdeportal_Affiliate_Router')){fwrite(STDERR,"FATAL plugin missing\n");exit(2);}
if(Pferdeportal_Affiliate_Router::VERSION!=='6.72.186'){fwrite(STDERR,"FATAL version ".Pferdeportal_Affiliate_Router::VERSION."\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($name)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m;};
$rp=function($name)use($o){$p=new ReflectionProperty($o,$name);$p->setAccessible(true);return $p;};
$call=function($name,...$args)use($rm,$o){return $rm($name)->invokeArgs($o,$args);};

update_option('ppar_enabled','1',false);
update_option('ppar_assignments_v1',array(),false);
delete_option('ppar_debug');

$call('maybe_install_creative_library_schema');
$call('maybe_install_output_objects_schema');
if(method_exists($o,'maybe_install_control_contract_schema'))$call('maybe_install_control_contract_schema');
$call('persist_network_settings','adcell',array(
  'enabled'=>1,'username'=>'diag-user','password'=>'diag-pass',
  'base_url'=>'https://www.adcell.de/api/v2/','test_path'=>'','csv_feed_url'=>''
));
$portalKey=sanitize_key((string)$call('output_local_portal_key'));
if($portalKey===''){fwrite(STDERR,"FATAL portal key\n");exit(2);}

// Exact real hierarchy needed for the two live pages.
$pages=array(
  95=>array('Ausrüstung','ausruestung',0),
  106=>array('Reiterbedarf','ausruestung-reiterbedarf',95),
  108=>array('Sattel & Zubehör','ausruestung-sattel',95),
  186=>array('Reithelme','reithelme',106),
  193=>array('Schabracken','schabracken',108),
);
foreach($pages as $id=>$p){
  if(get_post($id))wp_delete_post($id,true);
  $made=wp_insert_post(array('import_id'=>$id,'post_type'=>'page','post_status'=>'publish','post_title'=>$p[0],'post_name'=>$p[1],'post_parent'=>$p[2],'post_content'=>''),true);
  if(is_wp_error($made)||absint($made)!==absint($id)){fwrite(STDERR,"FATAL page ".$id."\n");exit(2);}
}
clean_post_cache(95);

// Real creatives observed on the live site in the current investigation.
// Destination URLs are the real no-follow redirects captured earlier.
$banners=array(
  array('7143','Guardian Horse','185797','https://shop.guardianhorse.app/?utm_source=adcell&utm_medium=banner&utm_campaign=landing&bid=185797-98720-'),
  array('14256','SanoVet','467974','https://www.sanovet.com/Anwendungsgebiete/?bid=467974-98720-'),
  array('10787','HKM','322674','https://www.hkm-sports.com/de/reiter/reithelme-sicherheitswesten/reithelme.html?utm_source=affiliate&utm_medium=banner&utm_campaign=Reithelme&bid=322674-98720-'),
  array('10787','HKM','322270','https://www.hkm-sports.com/de/kollektionen/lyon.html?bid=322270-98720-'),
  array('10787','HKM','321102','https://www.hkm-sports.com/de/sale.html?utm_source=affiliate&utm_medium=banner&utm_campaign=sale&bid=321102-98720-'),
  array('12248','Lax Tierfutter','374472','https://www.lax-tierfutter.de/?bid=374472-98720-'),
  array('13043','Procavallo','393901','https://www.procavallo.de/online-designer?bid=393901-98720-'),
  array('13043','Procavallo','391771','https://www.procavallo.de/online-designer?bid=391771-98720-'),
  array('17148','Hotti24','607373','https://www.hotti24.de/?utm_source=adcell&utm_medium=affiliate&utm_campaign=banner&bid=607373-98720-'),
  array('7276','Vetevo','375241','https://vetevo.de/collections/alle-produkte?f_tierart=F_Hund&utm_source=adcell&utm_medium=affiliate&utm_campaign=hund&utm_content=728x90&klar_source=adcell&bid=375241-98720-'),
);

$table=$call('creative_library_table');
$created=array();
foreach($banners as $b){
  list($partnerId,$partnerName,$external,$destination)=$b;
  $raw=array(
    'creative_id'=>$external,'creative_type'=>'banner','creative_title'=>$partnerName.' '.$external,
    'creative_description'=>'','creative_tag'=>'',
    'image_source'=>'https://t.adcell.com/p/image?promoId='.$external.'&slotId=98720',
    'destination_url'=>$destination,
    'tracking_url'=>'https://t.adcell.com/p/click?promoId='.$external.'&slotId=98720',
    'width'=>'728','height'=>'90','status'=>'active'
  );
  $mapping=$call('creative_library_detect_mapping',array_keys($raw));
  $norm=$call('creative_library_normalize_row',$raw,$mapping,array(
    'provider'=>'adcell','partner_external_id'=>$partnerId,'partner_name'=>$partnerName,
    'source_kind'=>'banner','run_uuid'=>'real-schabracken-672186'
  ));
  if(is_wp_error($norm)){fwrite(STDERR,"FATAL normalize ".$external." ".$norm->get_error_message()."\n");exit(2);}
  $norm['width']=728;$norm['height']=90;$norm['topic_status']='auto_verified';
  $payload=json_decode((string)$norm['payload'],true);$payload=is_array($payload)?$payload:array();
  $payload['_dimension_state']='verified';$payload['_dimension_error']='';
  $payload['_image_sha256']=hash('sha256','img-'.$external);$payload['_image_mime']='image/jpeg';$payload['_image_bytes']=65536;$payload['_measured_at']=time();
  $payload['_destination_source']='provider_explicit';
  $norm['payload']=wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
  $up=$call('creative_library_upsert',$norm);
  if(!in_array($up,array('imported','updated','unchanged'),true)){fwrite(STDERR,"FATAL upsert ".$external."\n");exit(2);}
  $row=$GLOBALS['wpdb']->get_row($GLOBALS['wpdb']->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$norm['identity_hash']),ARRAY_A);
  $planned=$call('output_plan_creative',$row,true,$portalKey);
  $row=$GLOBALS['wpdb']->get_row($GLOBALS['wpdb']->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$norm['identity_hash']),ARRAY_A);
  $records=json_decode((string)($row['topic_targets']??''),true);$records=is_array($records)?$records:array();
  $created[$external]=array('planned'=>$planned,'records'=>$records,'row'=>$row);
  echo 'CLASSIFY '.wp_json_encode(array('creative'=>$external,'partner'=>$partnerName,'destination'=>$destination,'records'=>$records,'planned'=>$planned),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}

// Refill frontend caches from materialized local state.
try{$rp('campaigns_request_cache')->setValue($o,null);}catch(Throwable $e){}
foreach(array('ranked_campaigns_request_cache','ranked_campaign_candidate_index_request_cache','ranked_campaign_raw_records_request_cache','ranked_campaign_from_post_request_cache') as $prop){
  try{$rp($prop)->setValue($o,array());}catch(Throwable $e){}
}

$phase='frontend';$http=0;
add_filter('pre_http_request',function($pre,$args,$url)use(&$http){$http++;return new WP_Error('blocked','frontend network forbidden');},PHP_INT_MAX,3);

$rows=function($arr){
  $out=array();
  foreach((array)$arr as $r){
    $c=is_array($r['campaign']??null)?$r['campaign']:array();
    $out[]=array(
      'id'=>(string)($c['id']??''),
      'partner'=>(string)($c['partner']??''),
      'specificity'=>(int)($r['specificity']??-1),
      'matches'=>(int)($r['matches']??0),
      'reason'=>(string)($r['reason']??''),
      'targets'=>(array)($c['automation_target_keys']??array()),
      'destination'=>(string)($c['destination_url']??''),
    );
  }
  return $out;
};
$ctx193=$call('get_content_context',193);
$ctx186=$call('get_content_context',186);
$unc193=$call('ranked_campaigns_for_slot_uncached',$ctx193,'product_after_category_tiles','');
$strict193=$call('ranked_campaigns_for_slot',$ctx193,'product_after_category_tiles','');
$sel193=$call('select_campaign_for_slot_position',$ctx193,'product_after_category_tiles',1);
$unc186=$call('ranked_campaigns_for_slot_uncached',$ctx186,'product_after_category_tiles','');
$strict186=$call('ranked_campaigns_for_slot',$ctx186,'product_after_category_tiles','');
$sel186=$call('select_campaign_for_slot_position',$ctx186,'product_after_category_tiles',1);

echo 'CTX193 '.wp_json_encode($ctx193,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'RAW193 '.wp_json_encode($rows($unc193),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'STRICT193 '.wp_json_encode($rows($strict193),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'SELECT193 '.wp_json_encode($rows(array($sel193)),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'RAW186 '.wp_json_encode($rows($unc186),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'STRICT186 '.wp_json_encode($rows($strict186),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'SELECT186 '.wp_json_encode($rows(array($sel186)),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";

$recordFor=function($external)use(&$created,$portalKey){
  foreach((array)($created[$external]['records']??array()) as $r){
    if(sanitize_key((string)($r['portal_key']??''))===$portalKey)return $r;
  }
  return array();
};
$g=$recordFor('185797');
$h=$recordFor('322674');
ck(sanitize_key((string)($g['state']??''))==='general','GUARDIAN_is_general',wp_json_encode($g));
ck(sanitize_key((string)($g['level']??''))==='general','GUARDIAN_level_general',wp_json_encode($g));
ck(sanitize_key((string)($h['state']??''))==='mapped','REITHELM_is_mapped',wp_json_encode($h));
ck(sanitize_key((string)($h['level']??''))==='exact','REITHELM_level_exact',wp_json_encode($h));
ck((string)($h['target_key']??'')==='page:186','REITHELM_target_page_186',wp_json_encode($h));

$max193=-1;foreach((array)$unc193 as $r)$max193=max($max193,(int)($r['specificity']??-1));
$max186=-1;foreach((array)$unc186 as $r)$max186=max($max186,(int)($r['specificity']??-1));
ck($max193<200,'SCHABRACKEN_has_no_exact_or_extended_candidate_in_observed_real_pool','max='.$max193);
ck($max193===100,'SCHABRACKEN_best_available_band_is_general','max='.$max193);
ck($max186>=500,'REITHELME_has_exact_candidate','max='.$max186);
$sel186id=(string)($sel186['campaign']['id']??'');
$sel186dest=(string)($sel186['campaign']['destination_url']??'');
ck(strpos($sel186dest,'/reithelme-sicherheitswesten/reithelme.html')!==false,'REITHELME_selects_exact_322674',$sel186id.' '.$sel186dest);
ck($http===0,'FRONTEND_zero_http_calls','http='.$http);

echo 'SUMMARY passes='.(10-count($GLOBALS['fails'])).' failures='.count($GLOBALS['fails'])."\n";
if($GLOBALS['fails']){echo 'FAILURES '.wp_json_encode($GLOBALS['fails'])."\n";exit(1);}
echo "REAL_SCHABRACKEN_POOL_ROOTCAUSE_672186_PASS\n";
