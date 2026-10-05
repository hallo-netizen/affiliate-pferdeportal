<?php
$GLOBALS['sf']=array();
function sck($ok,$name,$detail=''){echo ($ok?'PASS ':'FAIL ').$name.($detail!==''?' :: '.$detail:'')."\n";if(!$ok)$GLOBALS['sf'][]=$name;}
if(!class_exists('Pferdeportal_Affiliate_Router')||Pferdeportal_Affiliate_Router::VERSION!=='6.72.186'){fwrite(STDERR,"FATAL seed requires 6.72.186\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($n)use($o){$m=new ReflectionMethod($o,$n);$m->setAccessible(true);return $m;};
$rp=function($n)use($o){$p=new ReflectionProperty($o,$n);$p->setAccessible(true);return $p;};
$call=function($n,...$a)use($rm,$o){return $rm($n)->invokeArgs($o,$a);};
update_option('ppar_enabled','1',false); update_option('ppar_assignments_v1',array(),false);

$call('maybe_install_creative_library_schema'); $call('maybe_install_output_objects_schema');
if(method_exists($o,'maybe_install_control_contract_schema'))$call('maybe_install_control_contract_schema');
$call('persist_network_settings','adcell',array('enabled'=>1,'username'=>'fixture-user','password'=>'fixture-pass','base_url'=>'https://www.adcell.de/api/v2/','test_path'=>'','csv_feed_url'=>''));

$pages=array(
 95=>array('Ausrüstung','ausruestung',0),
 106=>array('Reiterbedarf','ausruestung-reiterbedarf',95),
 108=>array('Sattel & Zubehör','ausruestung-sattel',95),
 186=>array('Reithelme','reithelme',106),
 193=>array('Schabracken','schabracken',108),
);
foreach($pages as $id=>$p){
 if(get_post($id))wp_delete_post($id,true);
 $x=wp_insert_post(array('import_id'=>$id,'post_type'=>'page','post_status'=>'publish','post_title'=>$p[0],'post_name'=>$p[1],'post_parent'=>$p[2]),true);
 if(is_wp_error($x)||absint($x)!==absint($id)){fwrite(STDERR,"FATAL page ".$id."\n");exit(2);}
}
clean_post_cache(95);

$phase='planning';$http=array('planning'=>0,'frontend'=>0);
add_filter('pre_http_request',function($pre,$args,$url)use(&$phase,&$http){
 $http[$phase]++; return array('headers'=>array(),'body'=>'','response'=>array('code'=>200,'message'=>'OK'),'cookies'=>array(),'filename'=>null);
},PHP_INT_MAX,3);

$portalKey=sanitize_key((string)$call('output_local_portal_key'));
$table=$call('creative_library_table');
$rows=array();
$real=array(
 array('7143','Guardian Horse','185797','https://shop.guardianhorse.app/?utm_source=adcell&utm_medium=banner&utm_campaign=landing&bid=185797-98720-'),
 array('14256','SanoVet','467974','https://www.sanovet.com/Anwendungsgebiete/?bid=467974-98720-'),
 array('10787','HKM','322674','https://www.hkm-sports.com/de/reiter/reithelme-sicherheitswesten/reithelme.html?utm_source=affiliate&utm_medium=banner&utm_campaign=Reithelme&bid=322674-98720-'),
);
foreach($real as $b){
 list($partnerId,$partnerName,$external,$destination)=$b;
 $raw=array(
  'creative_id'=>$external,'creative_type'=>'banner','creative_title'=>$partnerName.' '.$external,
  'creative_description'=>'','creative_tag'=>'',
  'image_source'=>'https://t.adcell.com/p/image?promoId='.$external.'&slotId=98720',
  'destination_url'=>$destination,'tracking_url'=>'https://t.adcell.com/p/click?promoId='.$external.'&slotId=98720',
  'width'=>'728','height'=>'90','status'=>'active'
 );
 $mapping=$call('creative_library_detect_mapping',array_keys($raw));
 $norm=$call('creative_library_normalize_row',$raw,$mapping,array('provider'=>'adcell','partner_external_id'=>$partnerId,'partner_name'=>$partnerName,'source_kind'=>'banner','run_uuid'=>'upgrade-realstate-186'));
 if(is_wp_error($norm)){fwrite(STDERR,"FATAL normalize ".$external."\n");exit(2);}
 $norm['width']=728;$norm['height']=90;$norm['topic_status']='auto_verified';
 $payload=json_decode((string)$norm['payload'],true);$payload=is_array($payload)?$payload:array();
 $payload['_dimension_state']='verified';$payload['_image_sha256']=hash('sha256','img-'.$external);$payload['_image_mime']='image/jpeg';$payload['_image_bytes']=65536;$payload['_measured_at']=time();$payload['_destination_source']='provider_explicit';
 $norm['payload']=wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
 $call('creative_library_upsert',$norm);
 $row=$GLOBALS['wpdb']->get_row($GLOBALS['wpdb']->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$norm['identity_hash']),ARRAY_A);
 $call('output_plan_creative',$row,true,$portalKey);
 $row=$GLOBALS['wpdb']->get_row($GLOBALS['wpdb']->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$norm['identity_hash']),ARRAY_A);
 $rows[$external]=$row;
}

// Reproduce the real persisted defect: the Reithelm creative exists, but its
// central edge/campaign is stale-general while old v672185 migration is already done.
$guardianRecords=json_decode((string)($rows['185797']['topic_targets']??''),true);
$guardianRecords=is_array($guardianRecords)?$guardianRecords:array();
$helmet=$rows['322674'];
$GLOBALS['wpdb']->update($table,array('topic_score'=>1,'topic_targets'=>wp_json_encode($guardianRecords,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),'classified_at'=>time()),array('id'=>absint($helmet['id'])));
$campaignIds=get_posts(array('post_type'=>Pferdeportal_Affiliate_Router::CAMPAIGN_POST_TYPE,'post_status'=>array('publish','draft','private'),'meta_key'=>'_ppar_creative_identity_hash','meta_value'=>(string)$helmet['identity_hash'],'fields'=>'ids','posts_per_page'=>-1));
$helmetCampaign=0;
foreach((array)$campaignIds as $pid){
 $d=get_post_meta($pid,'ppar_campaign_data',true);
 if(!is_array($d)||sanitize_key((string)($d['creative_type']??''))!=='banner')continue;
 $d['active']=1;$d['assignment_mode']='fallback';$d['automation_target_keys']=array();$d['match_descendants']=false;$d['auto_topic_score']=1;$d['auto_topic_label']='Ausrüstung';
 update_post_meta($pid,'ppar_campaign_data',$d);$helmetCampaign=absint($pid);
}
update_option('ppar_banner_library_migration_state_v672185','done',false);
update_option('ppar_full_pool_automation_version_v1','6.72.186',false);
update_option(Pferdeportal_Affiliate_Router::OPTION_FULL_POOL_AUTOMATION_CURSOR,123,false);
wp_schedule_single_event(time()+300,Pferdeportal_Affiliate_Router::FULL_POOL_WORKER_HOOK);

// Product sentinels must remain byte-identical through the banner-only repair.
$save=$rm('save_campaign_record');
$mkprod=function($id,$network)use($save,$o){
 $c=array('id'=>$id,'active'=>1,'creative_type'=>'product','network'=>$network,'programme_status'=>'active','source'=>'output_object_v4','render_mode'=>'image_link','title'=>$id,'image_url'=>'https://img.example.test/'.$id.'.jpg','url'=>'https://click.example.test/'.$id,'target'=>'_blank','placements'=>array('category_product_1'),'assignment_mode'=>'fallback','priority'=>10,'health_check_enabled'=>false,'dimensions'=>'400x400','partner'=>$network.'-sentinel');
 return absint($save->invoke($o,$c,0));
};
$ebay=$mkprod('ebay-v187-sentinel','ebay');$idealo=$mkprod('idealo-v187-sentinel','idealo');
$ebayData=get_post_meta($ebay,'ppar_campaign_data',true);$idealoData=get_post_meta($idealo,'ppar_campaign_data',true);

try{$rp('campaigns_request_cache')->setValue($o,null);}catch(Throwable $e){}
foreach(array('ranked_campaigns_request_cache','ranked_campaign_candidate_index_request_cache','ranked_campaign_raw_records_request_cache','ranked_campaign_from_post_request_cache','automation_exact_target_rank_request_cache') as $p){try{$rp($p)->setValue($o,array());}catch(Throwable $e){}}

$phase='frontend';$http['frontend']=0;
$ctx186=$call('get_content_context',186);$ctx193=$call('get_content_context',193);
$sel186=$call('select_campaign_for_slot_position',$ctx186,'product_after_category_tiles',1);
$sel193=$call('select_campaign_for_slot_position',$ctx193,'product_after_category_tiles',1);
$sp186=(int)($sel186['specificity']??0);$sp193=(int)($sel193['specificity']??0);
echo 'PRE186 '.wp_json_encode(array(
 'reithelme'=>array('specificity'=>$sp186,'partner'=>(string)($sel186['campaign']['partner']??''),'destination'=>(string)($sel186['campaign']['destination_url']??'')),
 'schabracken'=>array('specificity'=>$sp193,'partner'=>(string)($sel193['campaign']['partner']??''),'destination'=>(string)($sel193['campaign']['destination_url']??'')),
 'frontend_http'=>$http['frontend']
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";

sck($helmetCampaign>0,'SEED_helmet_campaign_exists');
sck((string)get_option('ppar_banner_library_migration_state_v672185','')==='done','SEED_old_185_migration_done');
sck($sp186===100,'RED_186_reithelme_only_general');
sck($sp193===100,'RED_186_schabracken_only_general');
sck($http['frontend']===0,'RED_186_frontend_zero_http','http='.$http['frontend']);

update_option('ppar_v187_realstate_fixture',array(
 'helmet_identity'=>(string)$helmet['identity_hash'],'helmet_campaign'=>$helmetCampaign,
 'guardian_identity'=>(string)$rows['185797']['identity_hash'],'ebay'=>$ebay,'idealo'=>$idealo,
 'ebay_data'=>$ebayData,'idealo_data'=>$idealoData
),false);

if($GLOBALS['sf']){echo 'FAILURES '.wp_json_encode($GLOBALS['sf'])."\n";exit(1);}
echo "REALSTATE_672186_RED_SEED_PASS\n";
