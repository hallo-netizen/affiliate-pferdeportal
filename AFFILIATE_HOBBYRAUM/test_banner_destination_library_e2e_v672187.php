<?php
$GLOBALS['dest_e2e_pass']=array(); $GLOBALS['dest_e2e_fail']=array();
function dchk($cond,$name,$detail=''){ if($cond){$GLOBALS['dest_e2e_pass'][]=$name;echo "PASS $name".($detail!==''?" :: $detail":"")."\n";}else{$GLOBALS['dest_e2e_fail'][]=$name.($detail!==''?" :: $detail":"");echo "FAIL $name".($detail!==''?" :: $detail":"")."\n";}}
if(!class_exists('Pferdeportal_Affiliate_Router')){fwrite(STDERR,"FATAL plugin class missing\n");exit(2);}
if(Pferdeportal_Affiliate_Router::VERSION!=='6.72.187'){fwrite(STDERR,"FATAL wrong version ".Pferdeportal_Affiliate_Router::VERSION."\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($name)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m;};
$rp=function($name)use($o){$p=new ReflectionProperty($o,$name);$p->setAccessible(true);return $p;};
$call=function($name,...$args)use($rm,$o){return $rm($name)->invokeArgs($o,$args);};
update_option('ppar_enabled','1',false);
update_option('ppar_assignments_v1',array(),false);
delete_option('ppar_debug');
$call('maybe_install_creative_library_schema');
$call('maybe_install_output_objects_schema');

$http_calls=0;
add_filter('pre_http_request',function($pre,$args,$url)use(&$http_calls){$http_calls++; return new WP_Error('dest_e2e_network_block','network forbidden in destination-library gate');},10,3);

$mkpage=function($title,$slug,$parent=0){
  $id=wp_insert_post(array('post_type'=>'page','post_status'=>'publish','post_title'=>$title,'post_name'=>$slug,'post_parent'=>$parent,'post_content'=>'Fixture '.$title),true);
  if(is_wp_error($id)){fwrite(STDERR,"FATAL page $slug ".$id->get_error_message()."\n");exit(2);} return (int)$id;
};
$root=$mkpage('Ausrüstung URL E2E','ausruestung');
$schabracken=$mkpage('Schabracken URL E2E','schabracken',$root);
$reithelme=$mkpage('Reithelme URL E2E','reithelme',$root);
$haltung=$mkpage('Haltung URL E2E','haltung');

global $wpdb;
$table=$call('creative_library_table');
$make=function($external,$title,$destination,$tracking,$width=1200,$height=120)use($call,$wpdb,$table){
  $raw=array(
    'creative_id'=>$external,'creative_type'=>'banner','creative_title'=>$title,
    'creative_description'=>'','creative_tag'=>'Pferd',
    'image_source'=>'https://example.com/'.$external.'.jpg',
    'destination_url'=>$destination,'tracking_url'=>$tracking,
    'width'=>(string)$width,'height'=>(string)$height,'status'=>'active'
  );
  $mapping=$call('creative_library_detect_mapping',array_keys($raw));
  $norm=$call('creative_library_normalize_row',$raw,$mapping,array(
    'provider'=>'manual','partner_external_id'=>'partner-e2e','partner_name'=>'Pferde Banner E2E',
    'source_kind'=>'banner','run_uuid'=>'dest-e2e'
  ));
  if(is_wp_error($norm)){fwrite(STDERR,"FATAL normalize $external ".$norm->get_error_message()."\n");exit(2);}
  $norm['width']=$width;$norm['height']=$height;$norm['topic_status']='auto_verified';
  $payload=json_decode((string)$norm['payload'],true);$payload=is_array($payload)?$payload:array();
  $payload['_dimension_state']='verified';$payload['_dimension_error']='';$payload['_image_sha256']=str_repeat(substr(hash('sha256',$external),0,1),64);$payload['_measured_at']=time();
  $norm['payload']=wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
  $res=$call('creative_library_upsert',$norm);
  if(!in_array($res,array('imported','updated','unchanged'),true)){fwrite(STDERR,"FATAL upsert $external ".print_r($res,true)."\n");exit(2);}
  return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$norm['identity_hash']),ARRAY_A);
};
$refresh=function($row)use($wpdb,$table){return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$row['id']),ARRAY_A);};
$plan=function($row)use($call){return $call('output_plan_creative',$row,true);};
$campaign=function($row){
  $ids=get_posts(array('post_type'=>'ap_campaign','post_status'=>array('publish','draft','private'),'meta_key'=>'_ppar_creative_identity_hash','meta_value'=>(string)$row['identity_hash'],'posts_per_page'=>20,'fields'=>'ids','orderby'=>'ID','order'=>'DESC'));
  foreach((array)$ids as $id){$d=get_post_meta($id,'ppar_campaign_data',true);if(is_array($d)&&!empty($d['active']))return $d;}
  if($ids){$d=get_post_meta((int)$ids[0],'ppar_campaign_data',true);return is_array($d)?$d:array();}
  return array();
};
$records=function($row){$r=json_decode((string)($row['topic_targets']??''),true);return is_array($r)?$r:array();};
$render=function($post_id,$slot)use($rm,$o){return (string)$rm('render_affiliate_slot')->invoke($o,$post_id,$slot,'portal_context','');};
$getctx=function($id)use($rm,$o){return $rm('get_content_context')->invoke($o,$id);};

// 1) Existing banner: real destination URL -> durable exact edge -> rendered HTML.
$sch=$make('dest-schabracken','Schabracken Banner','https://example.com/schabracken/','https://example.com/click/schabracken');
$payload=json_decode((string)$sch['payload'],true);
dchk(($payload['_destination_source']??'')==='provider_explicit','explicit_destination_source_stored');
$r=$plan($sch); dchk((int)($r['active']??0)>0,'existing_banner_materialized_active');
$sch=$refresh($sch);$rec=$records($sch);$first=$rec[0]??array();
dchk(($first['state']??'')==='mapped','existing_banner_target_mapping_persisted',wp_json_encode($first));
dchk(strpos((string)($first['target_label']??''),'Schabracken')!==false,'existing_banner_maps_to_schabracken');
$classified=$call('output_classify_for_portal',$sch,$call('output_portal_registry')[array_key_first($call('output_portal_registry'))],'portal_banner');
dchk(($classified['source']??'')==='creative_library_destination_map','stored_mapping_reused_without_reclassification');
$html=$render($schabracken,'product_after_category_tiles');
dchk(strpos($html,'dest-schabracken')!==false,'existing_banner_visible_in_final_html');
$camp=$campaign($sch);
dchk(($camp['source']??'')==='output_object_v4','materialized_campaign_uses_library_source');
dchk(in_array('page:schabracken',(array)($camp['automation_target_keys']??array()),true),'campaign_contains_stored_schabracken_edge');
dchk(in_array('product_after_category_tiles',(array)($camp['placements']??array()),true),'campaign_contains_compatible_category_slot');

// 2) Future banner imported later follows same path automatically.
$helmet=$make('dest-reithelme','Reithelme Banner','https://example.com/reithelme/','https://example.com/click/reithelme');
$r=$plan($helmet);dchk((int)($r['active']??0)>0,'future_banner_materialized_active');
$helmet=$refresh($helmet);$hrec=$records($helmet);dchk(strpos((string)($hrec[0]['target_label']??''),'Reithelme')!==false,'future_banner_maps_from_destination_url');
$html=$render($reithelme,'product_after_category_tiles');
dchk(strpos($html,'dest-reithelme')!==false,'future_banner_visible_in_final_html');

// 3) No trustworthy destination => general fallback, not invented topic and not empty.
$general=$make('dest-general','Allgemeiner Banner','','https://example.com/general-click');
$payload=json_decode((string)$general['payload'],true);
dchk(($payload['_destination_source']??'')==='tracking_fallback','tracking_only_marked_as_nonsemantic');
$r=$plan($general);dchk((int)($r['active']??0)>0,'tracking_only_banner_materialized_as_general_fallback');
$general=$refresh($general);$grec=$records($general);dchk(($grec[0]['state']??'')==='general','general_fallback_persisted_in_library',wp_json_encode($grec[0]??array()));
$gcamp=$campaign($general);
dchk(($gcamp['assignment_mode']??'')==='fallback' && empty($gcamp['automation_target_keys']),'general_campaign_has_no_fake_topic_edge');
$html=$render($haltung,'product_after_category_tiles');
dchk(strpos($html,'dest-general')===false,'general_fallback_stored_but_not_auto_delivered_without_topic');

// 4) Technical negative: square banner may exist, but never fills wide category slot.
$square=$make('dest-square','Quadrat Banner','https://example.com/schabracken/','https://example.com/click/square',400,400);
$r=$plan($square);$squareCamp=$campaign($square);
$html=$render($schabracken,'product_after_category_tiles');
dchk(strpos($html,'dest-square')===false,'invalid_geometry_never_fills_wide_slot');
dchk(!in_array('product_after_category_tiles',(array)($squareCamp['placements']??array()),true),'invalid_geometry_not_stored_for_wide_slot');

// 5) Changed target URL invalidates old mapping and produces a new edge.
$mutable=$make('dest-mutable','Wechsel Banner','https://example.com/schabracken/','https://example.com/click/mutable');
$plan($mutable);$mutable=$refresh($mutable);
$before=$records($mutable);dchk(strpos((string)($before[0]['target_label']??''),'Schabracken')!==false,'mutable_initial_edge_schabracken');
$mutable2=$make('dest-mutable','Wechsel Banner','https://example.com/reithelme/','https://example.com/click/mutable');
$cleared=$records($mutable2);
dchk(empty($cleared),'changed_destination_clears_old_mapping_before_replan');
$plan($mutable2);$mutable2=$refresh($mutable2);$after=$records($mutable2);
dchk(strpos((string)($after[0]['target_label']??''),'Reithelme')!==false,'changed_destination_recomputed_to_reithelme');

// 6) Frontend hot path: stored output_object banner performs no DB/HTTP work inside match ranking.
$rankMethod=$rm('campaign_match_rank');
$camp=$campaign($sch);
$ctx=$getctx($haltung);$ctx['slot_type']='product_after_category_tiles';
$camp['destination_url']='https://example.com/haltung/';
$q0=(int)$wpdb->num_queries;$h0=$http_calls;
$rank=null;for($i=0;$i<1000;$i++){$rank=$rankMethod->invoke($o,$camp,$ctx);}
$q1=(int)$wpdb->num_queries;$h1=$http_calls;
dchk(($q1-$q0)===0,'frontend_stored_mapping_rank_adds_zero_db_queries','delta='.($q1-$q0));
dchk(($h1-$h0)===0,'frontend_stored_mapping_rank_adds_zero_http_calls','delta='.($h1-$h0));
dchk((int)($rank['specificity']??0)===5,'frontend_ignores_misleading_destination_after_materialization',wp_json_encode($rank));

// 7) Entire test itself must not have triggered remote transport.
dchk($http_calls===0,'complete_destination_library_gate_uses_zero_remote_http','http_calls='.$http_calls);

echo "SUMMARY passes=".count($GLOBALS['dest_e2e_pass'])." failures=".count($GLOBALS['dest_e2e_fail'])."\n";
if($GLOBALS['dest_e2e_fail']){echo "FAILURES ".wp_json_encode($GLOBALS['dest_e2e_fail'])."\n";exit(1);}
echo "FULL_DESTINATION_LIBRARY_WORDPRESS_MARIADB_E2E_PASS\n";
