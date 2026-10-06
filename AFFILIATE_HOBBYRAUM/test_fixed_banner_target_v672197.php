<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"FATAL plugin missing\n"); exit(2); }
if (Pferdeportal_Affiliate_Router::VERSION !== '6.72.197') { fwrite(STDERR,"FAIL version_672197\n"); exit(1); }

$o=Pferdeportal_Affiliate_Router::instance();
$call=function($name,...$args)use($o){
    $m=new ReflectionMethod($o,$name);
    $m->setAccessible(true);
    return $m->invokeArgs($o,$args);
};
$ok=function($cond,$name,$detail=''){
    if(!$cond){fwrite(STDERR,"FAIL ".$name.($detail!==''?' '.$detail:'')."\n");exit(1);}
    echo "PASS ".$name.($detail!==''?' '.$detail:'')."\n";
};
$term=function($name,$slug,$parent=0){
    $t=get_term_by('slug',$slug,'category');
    if($t&&!is_wp_error($t))return(int)$t->term_id;
    $r=wp_insert_term($name,'category',array('slug'=>$slug,'parent'=>$parent));
    if(is_wp_error($r)){fwrite(STDERR,"FATAL term ".$name." ".$r->get_error_message()."\n");exit(2);}
    return(int)$r['term_id'];
};

$aus=$term('Ausrüstung','ausruestung');
$sattel=$term('Sattel','sattel',$aus);
$sch=$term('Schabracken','schabracken',$sattel);

$call('maybe_install_creative_library_schema');
$call('maybe_install_output_objects_schema');
$portalKey=$call('output_local_portal_key');
$portal=$call('output_portal_by_key',$portalKey,true);
$ok(is_array($portal),'portal_available');

$targets=$call('output_portal_targets',$portal);
$fixed=null;
foreach((array)$targets as $t){
    if(is_array($t) && sanitize_key((string)($t['type']??''))==='category' && sanitize_key((string)($t['slug']??''))==='schabracken'){
        $fixed=$t; break;
    }
}
$ok(is_array($fixed),'schabracken_target_found');

global $wpdb;
$table=$call('creative_library_table');
$external='kiss-fixed-393923';
$identity=hash('sha256','v672197|'.$external);
$payload=array(
    '_dimension_state'=>'verified',
    '_image_sha256'=>hash('sha256','img|'.$external),
    '_image_mime'=>'image/png',
    '_image_bytes'=>1000,
    '_measured_at'=>time(),
    '_destination_source'=>'provider_explicit',
);
$row=array(
    'provider'=>'direct',
    'partner_external_id'=>'procavallo',
    'partner_name'=>'procavallo',
    'external_id'=>$external,
    'identity_hash'=>$identity,
    'creative_type'=>'banner',
    'title'=>'procavallo Banner 393923',
    'description'=>'',
    'tags'=>'',
    'image_url'=>'https://example.com/393923.png',
    'destination_url'=>'https://example.com/ausruestung/',
    'tracking_url'=>'https://example.com/track/393923',
    'width'=>728,
    'height'=>90,
    'source_status'=>'active',
    'source_kind'=>'banner',
    'availability_state'=>'active',
    'missing_count'=>0,
    'last_complete_run'=>'',
    'review_status'=>'review',
    'selected'=>0,
    'content_scope'=>'unclassified',
    'scope_source'=>'',
    'classified_at'=>0,
    'topic_status'=>'auto_verified',
    'topic_score'=>0,
    'topic_targets'=>'[]',
    'source_hash'=>hash('sha256','src|'.$external),
    'payload'=>wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
    'first_seen'=>time(),
    'last_seen'=>time(),
);
$wpdb->insert($table,$row,array_fill(0,count($row),'%s'));
$row=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$identity),ARRAY_A);
$ok(is_array($row),'creative_seeded');

$decisionPayload=array(
    'target_type'=>(string)($fixed['type']??''),
    'target_key'=>(string)($fixed['key']??''),
    'target_label'=>(string)($fixed['label']??''),
    'target_context'=>(string)($fixed['context']??''),
    'slot_id'=>'',
);
$saved=$call('output_set_portal_decision',$portalKey,$identity,'approved','KISS: Banner 393923 fest auf Schabracken.',$decisionPayload);
$ok(!is_wp_error($saved),'fixed_decision_saved');

$classification=$call('output_classify_for_portal',$row,$portal,'portal_banner');
$ok(is_array($classification) && ($classification['source']??'')==='manual_fixed_target','manual_fixed_classification');
$ok(sanitize_key((string)($classification['target']['slug']??''))==='schabracken','manual_fixed_target_schabracken');

$plan=$call('output_plan_creative',$row,true,$portalKey);
$ok(is_array($plan),'plan_runs',wp_json_encode($plan));
$ok((int)($plan['blocked']??0)===0,'fixed_banner_zero_blockers',wp_json_encode($plan));
$ok((int)($plan['active']??0)>=1,'fixed_banner_published',wp_json_encode($plan));

$ids=$call('creative_library_existing_campaign_ids',$identity);
$ok(!empty($ids),'fixed_campaign_exists');
$campaign=null;
$campaignId=0;
foreach((array)$ids as $id){
    $c=$call('campaign_from_post',get_post((int)$id));
    if(is_array($c) && !empty($c['active'])){
        $campaign=$c; $campaignId=(int)$id; break;
    }
}
$ok(is_array($campaign),'fixed_campaign_active');
$ok(sanitize_key((string)($campaign['quality_manual_status']??''))==='fixed','fixed_quality_status');
$ok(empty($campaign['match_descendants']),'fixed_no_descendant_guessing');
$keys=array_values(array_filter(array_map('sanitize_text_field',(array)($campaign['automation_target_keys']??array()))));
$ok($keys===array('category:schabracken'),'fixed_exact_runtime_target',wp_json_encode($keys));

$reset=$call('creative_library_deactivate_all_automatic_banner_campaigns');
$after=$call('campaign_from_post',get_post($campaignId));
$ok(is_array($after)&&!empty($after['active']),'fixed_survives_auto_reset','reset_count='.(int)$reset);
$ok(sanitize_key((string)($after['quality_manual_status']??''))==='fixed','fixed_status_survives_reset');

echo "FIXED_BANNER_TARGET_672197_COMPLETE\n";
