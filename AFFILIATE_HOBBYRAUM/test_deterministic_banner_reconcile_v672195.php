<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"FATAL plugin missing\n"); exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
$call=function($name,...$args)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);};
function t195($ok,$name,$detail=''){if(!$ok){fwrite(STDERR,"FAIL ".$name.($detail!==''?' '.$detail:'')."\n");exit(1);}echo "PASS ".$name.($detail!==''?' '.$detail:'')."\n";}
function term195($name,$slug,$parent=0){$t=get_term_by('slug',$slug,'category');if($t&&!is_wp_error($t))return(int)$t->term_id;$r=wp_insert_term($name,'category',array('slug'=>$slug,'parent'=>$parent));if(is_wp_error($r)){fwrite(STDERR,"FATAL term ".$name." ".$r->get_error_message()."\n");exit(2);}return(int)$r['term_id'];}
function keys195($row){$x=json_decode((string)($row['topic_targets']??''),true);$out=array();foreach((array)$x as $r){if(is_array($r)&&!empty($r['target_key']))$out[]=(string)$r['target_key'];}return$out;}
function campaign195($call,$id){$p=get_post((int)$id);return $p?$call('campaign_from_post',$p):null;}
function campaigns_by_identity195($call,$identity){$ids=$call('creative_library_existing_campaign_ids',$identity);$out=array();foreach((array)$ids as $id){$c=campaign195($call,$id);if(is_array($c)){$c['_id']=(int)$id;$out[]=$c;}}return$out;}
function seed_banner195($call,$external,$dest,$title,$partner='Test Direktpartner',$family='',$destSource='provider_explicit'){
    global $wpdb;$table=$call('creative_library_table');
    $identity=hash('sha256','v672195|'.$external);
    $payload=array(
        '_dimension_state'=>'verified',
        '_image_sha256'=>hash('sha256','img|'.$external),
        '_image_mime'=>'image/png',
        '_image_bytes'=>1000,
        '_measured_at'=>time(),
        '_destination_source'=>$destSource,
        '_manual_target_family'=>$family,
    );
    $row=array(
        'provider'=>'direct','partner_external_id'=>$partner==='Tarifcheck'?'tarifcheck':'195test','partner_name'=>$partner,
        'external_id'=>$external,'identity_hash'=>$identity,'creative_type'=>'banner','title'=>$title,'description'=>'','tags'=>'',
        'image_url'=>'https://example.com/'.$external.'.png','destination_url'=>$dest,'tracking_url'=>'https://example.com/track/'.$external,
        'width'=>728,'height'=>90,'source_status'=>'active','source_kind'=>'banner','availability_state'=>'active','missing_count'=>0,
        'last_complete_run'=>'','review_status'=>'review','selected'=>0,'content_scope'=>'unclassified','scope_source'=>'',
        'classified_at'=>0,'topic_status'=>'auto_verified','topic_score'=>0,'topic_targets'=>'[]',
        'source_hash'=>hash('sha256','src|'.$external.'|'.$family),'payload'=>wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
        'first_seen'=>time(),'last_seen'=>time(),
    );
    $wpdb->insert($table,$row,array_fill(0,count($row),'%s'));
    return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$wpdb->insert_id),ARRAY_A);
}

t195(Pferdeportal_Affiliate_Router::VERSION==='6.72.195','version_672195');
$call('maybe_install_creative_library_schema');
global $wpdb;$table=$call('creative_library_table');

// Realistische Kategorien fuer Schabracken.
$aus=term195('Ausrüstung','ausruestung');
$sattel=term195('Sattel','sattel',$aus);
$sch=term195('Schabracken','schabracken',$sattel);
$fut=term195('Fütterung','fuetterung');

// Realistische Tarifcheck-Ziele.
$kostenRoot=term195('Ausrüstung & Alltag','ausruestung-alltag');
$kosten1=term195('Kosten Sattel','sattel-kosten',$kostenRoot);
$kosten2=term195('Kosten Stall','stall-kosten',$kostenRoot);
$wissen=term195('Wissen','wissen');
$versicherungRoot=term195('Versicherungen & Recht','versicherungen-recht',$wissen);
$versicherung1=term195('Pferdehaftpflicht','pferdehaftpflicht',$versicherungRoot);
$versicherung2=term195('Rechtsschutz Pferd','rechtsschutz-pferd',$versicherungRoot);

// A) Reale 6.72.194-Luecke: stale Auto-Kampagne wird erzeugt und danach
// absichtlich von BEIDEN bekannten Creative-Metakeys getrennt.
$row=seed_banner195($call,'stale-schabracke','https://shop.example.com/fuetterung/','Stale Schabracke');
$m1=$call('output_assign_banner_targets_from_destination_once',$row);
t195((int)($m1['mapped']??0)>=1,'seed_fuetterung_map_created',wp_json_encode($m1));
$row=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$row['id']),ARRAY_A);
t195(in_array('category:'.$fut,keys195($row),true),'seed_target_fuetterung');
$p1=$call('output_plan_creative',$row,true);
t195(is_array($p1),'seed_fuetterung_plan_runs',wp_json_encode($p1));
$before=campaigns_by_identity195($call,$row['identity_hash']);
$auto=array_values(array_filter($before,static fn($c)=>(($c['source']??'')==='output_object_v4'&&!empty($c['active']))));
t195(count($auto)>=1,'stale_auto_active_before');
$staleId=(int)$auto[0]['_id'];
delete_post_meta($staleId,'_ppar_creative_identity_hash');
delete_post_meta($staleId,'ppar_library_identity_hash');
t195(count((array)$call('creative_library_existing_campaign_ids',$row['identity_hash']))===0,'stale_identity_links_removed');

$wpdb->update($table,array('destination_url'=>'https://shop.example.com/schabracken/'),array('id'=>(int)$row['id']));

// B) Manuelle Kampagne und Produktkampagne duerfen vom GLOBALEN Reset nicht beruehrt werden.
$manual=$call('central_blank_campaign');
$manual['id']='manual-fixed-195';$manual['name']='Manual Fixed 195';$manual['active']=true;$manual['creative_type']='banner';
$manual['source']='manual_editor';$manual['quality_manual_status']='approved';$manual['assignment_mode']='page_tree';
$manual['automation_target_keys']=array('category:fuetterung');$manual['placements']=array('product_after_category_tiles');
$manual['image_url']='https://example.com/manual.png';$manual['url']='https://example.com/track/manual';
$manualId=$call('save_campaign_record',$manual,0);
t195((int)$manualId>0,'manual_fixture_created');

$product=$call('central_blank_campaign');
$product['id']='product-auto-195';$product['name']='Product 195';$product['active']=true;$product['creative_type']='product';
$product['source']='output_object_v4';$product['quality_manual_status']='auto_verified';$product['automation_target_keys']=array('category:schabracken');
$product['placements']=array('category_product_1');$product['image_url']='https://example.com/product.png';$product['url']='https://example.com/product';
$productId=$call('save_campaign_record',$product,0);
t195((int)$productId>0,'product_fixture_created');

// C) Tarifcheck explizit: reine Tracking-Fallback-URL darf durch die bewusst
// gespeicherte Gruppe fachlich zugeordnet werden.
$tcKosten=seed_banner195($call,'tc-kosten','https://tracking.example.com/click/kredit','Tarifcheck Kredit','Tarifcheck','kosten','tracking_fallback');
$mk=$call('output_assign_banner_targets_from_destination_once',$tcKosten);
t195((int)($mk['mapped']??0)>=2,'tarifcheck_kosten_mapped',wp_json_encode($mk));
$tcKosten=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$tcKosten['id']),ARRAY_A);
$kk=keys195($tcKosten);
t195(in_array('category:'.$kosten1,$kk,true)&&in_array('category:'.$kosten2,$kk,true),'tarifcheck_kosten_all_cost_leaves',wp_json_encode($kk));
t195(!in_array('category:'.$versicherung1,$kk,true),'tarifcheck_kosten_not_insurance');

$tcVers=seed_banner195($call,'tc-vers','https://tracking.example.com/click/versicherung','Tarifcheck Versicherung','Tarifcheck','versicherung','tracking_fallback');
$mv=$call('output_assign_banner_targets_from_destination_once',$tcVers);
t195((int)($mv['mapped']??0)>=2,'tarifcheck_versicherung_mapped',wp_json_encode($mv));
$tcVers=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$tcVers['id']),ARRAY_A);
$vk=keys195($tcVers);
t195(in_array('category:'.$versicherung1,$vk,true)&&in_array('category:'.$versicherung2,$vk,true),'tarifcheck_versicherung_all_real_leaves',wp_json_encode($vk));
t195(!in_array('category:'.$kosten1,$vk,true),'tarifcheck_versicherung_not_cost');

// D) Gegenfall: Tracking-only Tarifcheck OHNE explizite Gruppe bleibt blockiert.
$tcUnknown=seed_banner195($call,'tc-unknown','https://tracking.example.com/click/xyz','Tarifcheck unbekannt','Tarifcheck','','tracking_fallback');
$mu=$call('output_assign_banner_targets_from_destination_once',$tcUnknown);
t195((int)($mu['mapped']??0)===0,'tarifcheck_tracking_without_explicit_family_blocked',wp_json_encode($mu));

// Reconcile exakt wie im Backend. Globaler Auto-Bannerreset muss den
// absichtlich unverknuepften stale Fütterungsbanner treffen.
delete_option('ppar_v672195_banner_reconcile_state');
delete_option('ppar_v672195_banner_reconcile_cursor');
delete_option('ppar_v672195_banner_reconcile_result');
delete_option('ppar_v672195_banner_reconcile_reset_done');
$call('run_v672195_banner_reconcile');

$staleAfter=campaign195($call,$staleId);
t195(is_array($staleAfter)&&empty($staleAfter['active']),'unlinked_stale_auto_campaign_globally_disabled',wp_json_encode($staleAfter));

$rebuilt=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$row['id']),ARRAY_A);
$rk=keys195($rebuilt);
t195(in_array('category:'.$sch,$rk,true),'rebuilt_target_schabracken',wp_json_encode($rk));
t195(!in_array('category:'.$fut,$rk,true),'rebuilt_target_no_fuetterung',wp_json_encode($rk));

$newCampaigns=campaigns_by_identity195($call,$row['identity_hash']);
$newAuto=array_values(array_filter($newCampaigns,static fn($c)=>(($c['source']??'')==='output_object_v4'&&!empty($c['active']))));
$hasSch=false;$hasFut=false;
foreach($newAuto as $c){$ak=(array)($c['automation_target_keys']??array());if(in_array('category:schabracken',$ak,true))$hasSch=true;if(in_array('category:fuetterung',$ak,true))$hasFut=true;}
t195($hasSch,'current_auto_campaign_schabracken');
t195(!$hasFut,'no_current_auto_campaign_fuetterung');

$manualAfter=campaign195($call,$manualId);
$productAfter=campaign195($call,$productId);
t195(is_array($manualAfter)&&!empty($manualAfter['active']),'manual_campaign_preserved');
t195(is_array($productAfter)&&!empty($productAfter['active']),'product_campaign_preserved');

$res=get_option('ppar_v672195_banner_reconcile_result',array());
t195(!empty($res['done']),'reconcile_done',wp_json_encode($res));
t195((int)($res['global_deactivated_auto_banners']??0)>=1,'global_reset_counted',wp_json_encode($res));

echo "DETERMINISTIC_BANNER_RECONCILE_672195_COMPLETE\n";
