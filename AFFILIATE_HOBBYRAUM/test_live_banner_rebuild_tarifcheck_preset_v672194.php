<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"FATAL plugin missing\n"); exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
$call=function($name,...$args)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);};
function t194($ok,$name,$detail=''){if(!$ok){fwrite(STDERR,"FAIL ".$name.($detail!==''?' '.$detail:'')."\n");exit(1);}echo "PASS ".$name.($detail!==''?' '.$detail:'')."\n";}
function term194($name,$slug,$parent=0){$t=get_term_by('slug',$slug,'category');if($t&&!is_wp_error($t))return(int)$t->term_id;$r=wp_insert_term($name,'category',array('slug'=>$slug,'parent'=>$parent));if(is_wp_error($r)){fwrite(STDERR,"FATAL term ".$name." ".$r->get_error_message()."\n");exit(2);}return(int)$r['term_id'];}
function target_keys194($row){$x=json_decode((string)($row['topic_targets']??''),true);$out=array();foreach((array)$x as $r){if(is_array($r)&&!empty($r['target_key']))$out[]=(string)$r['target_key'];}return$out;}
function campaigns194($o,$identity){
    $ids=(new ReflectionMethod($o,'creative_library_existing_campaign_ids'));$ids->setAccessible(true);
    $cfp=(new ReflectionMethod($o,'campaign_from_post'));$cfp->setAccessible(true);
    $out=array();
    foreach((array)$ids->invoke($o,$identity) as $id){$p=get_post($id);$c=$cfp->invoke($o,$p);if(is_array($c)){$c['_id']=$id;$out[]=$c;}}
    return $out;
}

t194(Pferdeportal_Affiliate_Router::VERSION==='6.72.194','version_672194');

// 1) Tarifcheck muss wirklich im "Aufgenommener Partner"-Dropdown verfügbar sein.
$snapshots=$call('creative_library_snapshots_for_select');
t194(isset($snapshots['direct:tarifcheck']),'tarifcheck_snapshot_exists',wp_json_encode($snapshots['direct:tarifcheck']??null));
t194(($snapshots['direct:tarifcheck']['provider']??'')==='direct','tarifcheck_snapshot_provider_direct');
t194(($snapshots['direct:tarifcheck']['external_id']??'')==='tarifcheck','tarifcheck_snapshot_external_id');
t194(($snapshots['direct:tarifcheck']['name']??'')==='Tarifcheck','tarifcheck_snapshot_name');

// Realistische Portalziele.
$aus=term194('Ausrüstung','ausruestung');
$sattel=term194('Sattel','sattel',$aus);
$sch=term194('Schabracken','schabracken',$sattel);
$fut=term194('Fütterung','fuetterung');

$call('maybe_install_creative_library_schema');
global $wpdb;
$table=$call('creative_library_table');

function seed_banner194($call,$o,$external,$dest,$title){
    global $wpdb;$table=$call('creative_library_table');
    $identity=hash('sha256','v672194|'.$external);
    $payload=array(
        '_dimension_state'=>'verified',
        '_image_sha256'=>hash('sha256','img|'.$external),
        '_image_mime'=>'image/png',
        '_image_bytes'=>1000,
        '_measured_at'=>time(),
        '_destination_source'=>'explicit',
    );
    $row=array(
        'provider'=>'direct',
        'partner_external_id'=>'194test',
        'partner_name'=>'Test Direktpartner',
        'external_id'=>$external,
        'identity_hash'=>$identity,
        'creative_type'=>'banner',
        'title'=>$title,
        'description'=>'',
        'tags'=>'',
        'image_url'=>'https://example.test/'.$external.'.png',
        'destination_url'=>$dest,
        'tracking_url'=>'https://tracking.example.test/'.$external,
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
    $cols=array_keys($row);$formats=array_fill(0,count($cols),'%s');
    $wpdb->insert($table,$row,$formats);
    $id=(int)$wpdb->insert_id;
    return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",$id),ARRAY_A);
}

// 2) Stale-Live-Fall erzeugen: URL war Fütterung -> Karte/Kampagne Fütterung,
// danach URL auf Schabracken ändern, alte Karte absichtlich stehen lassen.
$row=seed_banner194($call,$o,'stale-schabracke','https://shop.example.test/fuetterung/','Stale Schabracke');
$map1=$call('output_assign_banner_targets_from_destination_once',$row);
t194((int)($map1['mapped']??0)>=1,'seed_fuetterung_map_created',wp_json_encode($map1));
$row=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$row['id']),ARRAY_A);
t194(in_array('category:'.$fut,target_keys194($row),true),'seed_target_is_fuetterung',wp_json_encode(target_keys194($row)));

$plan1=$call('output_plan_creative',$row,true);
t194(is_array($plan1),'seed_fuetterung_plan_runs',wp_json_encode($plan1));
$before=campaigns194($o,$row['identity_hash']);
$beforeAuto=array_values(array_filter($before,static function($c){return ($c['source']??'')==='output_object_v4'&&!empty($c['active']);}));
t194(count($beforeAuto)>=1,'stale_auto_campaign_active_before_rebuild',wp_json_encode($beforeAuto));

$wpdb->update($table,array('destination_url'=>'https://shop.example.test/schabracken/'),array('id'=>(int)$row['id']));
$stale=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$row['id']),ARRAY_A);
t194(in_array('category:'.$fut,target_keys194($stale),true),'stale_map_still_fuetterung_before_rebuild');

// 3) No-map-Fall mit alter aktiver Auto-Kampagne.
$unknown=seed_banner194($call,$o,'stale-unknown','https://shop.example.test/fuetterung/','Stale Unknown');
$call('output_assign_banner_targets_from_destination_once',$unknown);
$unknown=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$unknown['id']),ARRAY_A);
$call('output_plan_creative',$unknown,true);
$wpdb->update($table,array('destination_url'=>'https://shop.example.test/zzzz-kein-portalziel-194/'),array('id'=>(int)$unknown['id']));

// 4) Manuelle Kampagne mit derselben Creative-Identity muss erhalten bleiben.
$manual=$call('central_blank_campaign');
$manual['id']='manual-fixed-194';
$manual['name']='Manual Fixed 194';
$manual['active']=true;
$manual['creative_type']='banner';
$manual['source']='manual_editor';
$manual['quality_manual_status']='approved';
$manual['assignment_mode']='page_tree';
$manual['automation_target_keys']=array('category:fuetterung');
$manual['placements']=array('product_after_category_tiles');
$manual['image_url']='https://example.test/manual.png';
$manual['url']='https://tracking.example.test/manual';
$manualId=$call('save_campaign_record',$manual,0);
update_post_meta((int)$manualId,'_ppar_creative_identity_hash',(string)$unknown['identity_hash']);
t194((int)$manualId>0,'manual_fixed_fixture_created');

// Rebuild erzwingen.
delete_option('ppar_v672194_banner_target_rebuild_state');
delete_option('ppar_v672194_banner_target_rebuild_cursor');
delete_option('ppar_v672194_banner_target_rebuild_result');
$call('run_v672194_banner_target_rebuild');

// Schabracken-Row muss neu gebunden sein.
$rebuilt=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$row['id']),ARRAY_A);
$keys=target_keys194($rebuilt);
t194(in_array('category:'.$sch,$keys,true),'rebuilt_target_contains_schabracken',wp_json_encode($keys));
t194(!in_array('category:'.$fut,$keys,true),'rebuilt_target_removed_fuetterung',wp_json_encode($keys));

$after=campaigns194($o,$row['identity_hash']);
$activeAfter=array_values(array_filter($after,static function($c){return ($c['source']??'')==='output_object_v4'&&!empty($c['active']);}));
t194(count($activeAfter)>=1,'rebuilt_auto_campaign_active');
$hasSch=false;$hasFut=false;
foreach($activeAfter as $c){$ak=(array)($c['automation_target_keys']??array());if(in_array('category:schabracken',$ak,true))$hasSch=true;if(in_array('category:fuetterung',$ak,true))$hasFut=true;}
t194($hasSch,'active_campaign_now_schabracken',wp_json_encode($activeAfter));
t194(!$hasFut,'no_active_auto_campaign_still_fuetterung',wp_json_encode($activeAfter));

// Unbekannte URL: keine Karte und keine automatische aktive Kampagne.
$unknownAfter=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$unknown['id']),ARRAY_A);
t194(count(target_keys194($unknownAfter))===0,'unknown_destination_has_no_target_map',wp_json_encode(target_keys194($unknownAfter)));
$unknownCampaigns=campaigns194($o,$unknown['identity_hash']);
$unknownAutoActive=array_values(array_filter($unknownCampaigns,static function($c){return ($c['source']??'')==='output_object_v4'&&!empty($c['active']);}));
t194(count($unknownAutoActive)===0,'unknown_destination_stale_auto_campaign_deactivated',wp_json_encode($unknownAutoActive));
$manualAfter=$call('campaign_from_post',get_post((int)$manualId));
t194(is_array($manualAfter)&&!empty($manualAfter['active']),'manual_fixed_campaign_preserved');

$res=get_option('ppar_v672194_banner_target_rebuild_result',array());
t194(!empty($res['done']),'rebuild_result_done',wp_json_encode($res));
t194((int)($res['processed']??0)>=2,'rebuild_processed_active_banners',wp_json_encode($res));

// Kein neuer Tabellenentwurf: nur bestehender Bestand.
echo "LIVE_BANNER_REBUILD_TARIFCHECK_PRESET_672194_COMPLETE\n";
