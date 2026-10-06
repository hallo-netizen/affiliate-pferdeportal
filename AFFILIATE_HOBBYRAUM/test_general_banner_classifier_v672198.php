<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"FATAL plugin missing\n"); exit(2); }
if (Pferdeportal_Affiliate_Router::VERSION !== '6.72.198') { fwrite(STDERR,"FAIL version\n"); exit(1); }

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

$root=$term('Ausrüstung','ausruestung');
$sch=$term('Schabracken','schabracken',$root);
$decken=$term('Pferdedecken','pferdedecken',$root);
$futterRoot=$term('Fütterung','fuetterung');
$futter=$term('Pferdefutter','pferdefutter',$futterRoot);

$call('maybe_install_creative_library_schema');
$call('maybe_install_output_objects_schema');
$table=$call('creative_library_table');

global $wpdb;
$seed=function($external,$title,$description,$tags,$destination,$destinationSource,$providerTopicName='',$providerTopicSource='',$oldTarget='')use($wpdb,$table){
    $identity=hash('sha256','v672198|'.$external);
    $payload=array(
        '_declared_width'=>728,
        '_declared_height'=>90,
        '_dimension_state'=>'verified',
        '_dimension_error'=>'',
        '_image_sha256'=>hash('sha256','img|'.$external),
        '_image_mime'=>'image/png',
        '_image_bytes'=>1000,
        '_measured_at'=>time(),
        '_destination_source'=>$destinationSource,
        'provider_topic_name'=>$providerTopicName,
        'provider_topic_source'=>$providerTopicSource,
        'promotion_category_name'=>$providerTopicName,
        'information'=>$description,
    );
    $row=array(
        'provider'=>'direct',
        'partner_external_id'=>'banner-test',
        'partner_name'=>'Test Partner',
        'external_id'=>$external,
        'identity_hash'=>$identity,
        'creative_type'=>'banner',
        'title'=>$title,
        'description'=>$description,
        'tags'=>$tags,
        'image_url'=>'https://example.com/'.$external.'.png',
        'destination_url'=>$destination,
        'tracking_url'=>'https://example.com/track/'.$external,
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
        'classified_at'=>$oldTarget!==''?time():0,
        'topic_status'=>$oldTarget!==''?'auto_verified':'format_pending',
        'topic_score'=>$oldTarget!==''?100:0,
        'topic_targets'=>$oldTarget!==''?wp_json_encode(array(array(
            'portal_key'=>'pferde_atelier',
            'state'=>'mapped',
            'level'=>'exact',
            'target_key'=>$oldTarget,
            'target_label'=>'ALT',
            'confidence'=>100,
            'source'=>'old_map',
            'destination_source'=>$destinationSource,
            'destination_url'=>$destination,
            'updated_at'=>time()-1000,
        ))):'[]',
        'source_hash'=>hash('sha256','src|'.$external),
        'payload'=>wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
        'first_seen'=>time(),
        'last_seen'=>time(),
    );
    $wpdb->insert($table,$row,array_fill(0,count($row),'%s'));
    return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",$identity),ARRAY_A);
};

$rows=array();
$rows['content_schabracken']=$seed(
    'content-schabracken',
    'procavallo Banner 393923 – SCHABRACKEN DESIGNER',
    'Individueller Designer',
    'ADCELL Banner',
    'https://example.com/ausruestung/',
    'provider_explicit',
    '',
    '',
    'category:'.$root
);
$rows['provider_pferdedecken']=$seed(
    'provider-pferdedecken',
    'Winteraktion',
    '',
    'ADCELL Banner',
    'https://example.com/ausruestung/',
    'provider_explicit',
    'Pferdedecken',
    'provider_promotion_category'
);
$rows['url_fallback']=$seed(
    'url-fallback',
    'Herbstaktion',
    '',
    'ADCELL Banner',
    'https://example.com/schabracken/',
    'provider_explicit'
);
$rows['ambiguous']=$seed(
    'ambiguous',
    'Schabracken Pferdedecken Kombi-Angebot',
    '',
    'ADCELL Banner',
    'https://example.com/ausruestung/',
    'provider_explicit'
);
$rows['no_evidence']=$seed(
    'no-evidence',
    'Herbstaktion',
    '',
    'ADCELL Banner',
    'https://tracking.example/no-evidence',
    'tracking_checked'
);

$getKeys=function($mapped){
    $keys=array();
    foreach((array)($mapped['targets']??array()) as $t){
        if(is_array($t) && !empty($t['target_key']))$keys[]=(string)$t['target_key'];
    }
    sort($keys);
    return $keys;
};

$m1=$call('output_assign_banner_targets_from_destination_once',$rows['content_schabracken']);
$k1=$getKeys($m1);
$ok($k1===array('category:'.$sch),'content_beats_broad_destination',wp_json_encode($k1));
$ok(!in_array('category:'.$root,$k1,true),'stale_map_not_reused');

$m2=$call('output_assign_banner_targets_from_destination_once',$rows['provider_pferdedecken']);
$k2=$getKeys($m2);
$ok($k2===array('category:'.$decken),'provider_topic_precedence',wp_json_encode($k2));

$m3=$call('output_assign_banner_targets_from_destination_once',$rows['url_fallback']);
$k3=$getKeys($m3);
$ok($k3===array('category:'.$sch),'url_fallback_when_content_has_no_target',wp_json_encode($k3));

$m4=$call('output_assign_banner_targets_from_destination_once',$rows['ambiguous']);
$k4=$getKeys($m4);
$ok($k4===array(),'ambiguous_content_fail_closed',wp_json_encode($k4));

$m5=$call('output_assign_banner_targets_from_destination_once',$rows['no_evidence']);
$k5=$getKeys($m5);
$ok($k5===array(),'tracking_only_no_evidence_fail_closed',wp_json_encode($k5));

$pre1=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$rows['content_schabracken']['id']),ARRAY_A);
$prePlan1=$call('output_plan_creative',$pre1,true);
echo "DIAG pre_plan_schabracken ".wp_json_encode($prePlan1)."\n";

// Ganze Reconcile-Runde: alte Karten werden geloescht, alle aktiven Banner neu
// bewertet und nur belastbare Treffer wieder materialisiert.
delete_option('ppar_v672198_banner_reconcile_state');
delete_option('ppar_v672198_banner_reconcile_cursor');
delete_option('ppar_v672198_banner_reconcile_result');
delete_option('ppar_v672198_banner_reconcile_reset_done');
$o->run_v672195_banner_reconcile();

$fetch=function($external)use($wpdb,$table){
    return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE external_id=%s",$external),ARRAY_A);
};
$storedKeys=function($row){
    $targets=json_decode((string)($row['topic_targets']??''),true);
    $keys=array();
    foreach((array)$targets as $t){if(is_array($t)&&!empty($t['target_key']))$keys[]=(string)$t['target_key'];}
    sort($keys);
    return $keys;
};

$r1=$fetch('content-schabracken');
$r2=$fetch('provider-pferdedecken');
$r4=$fetch('ambiguous');
$r5=$fetch('no-evidence');
$ok($storedKeys($r1)===array('category:'.$sch),'reconcile_persists_schabracken');
$ok($storedKeys($r2)===array('category:'.$decken),'reconcile_persists_pferdedecken');
$ok($storedKeys($r4)===array(),'reconcile_keeps_ambiguous_unmapped');
$ok($storedKeys($r5)===array(),'reconcile_keeps_unknown_unmapped');

$activeTargets=function($identity)use($call){
    $keys=array();
    foreach((array)$call('creative_library_existing_campaign_ids',$identity) as $id){
        $c=$call('campaign_from_post',get_post((int)$id));
        if(!is_array($c)||empty($c['active']))continue;
        foreach((array)($c['automation_target_keys']??array()) as $k)$keys[]=(string)$k;
    }
    $keys=array_values(array_unique($keys)); sort($keys); return $keys;
};
$a1=$activeTargets((string)$r1['identity_hash']);
$a2=$activeTargets((string)$r2['identity_hash']);
$a4=$activeTargets((string)$r4['identity_hash']);
$a5=$activeTargets((string)$r5['identity_hash']);
$ok($a1===array('category:schabracken'),'frontend_campaign_schabracken_active',wp_json_encode($a1));
$ok($a2===array('category:pferdedecken'),'frontend_campaign_pferdedecken_active',wp_json_encode($a2));
$ok($a4===array(),'ambiguous_creates_no_active_campaign');
$ok($a5===array(),'unknown_creates_no_active_campaign');

echo "GENERAL_BANNER_CLASSIFIER_672198_COMPLETE\n";
