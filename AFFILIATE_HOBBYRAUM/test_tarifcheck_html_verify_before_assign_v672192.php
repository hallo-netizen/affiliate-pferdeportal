<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"FATAL plugin missing\n"); exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
$call=function($name,...$args)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);};
$call('maybe_install_creative_library_schema');

function tc_assert($ok,$name,$detail=''){
    if(!$ok){fwrite(STDERR,"FAIL ".$name.($detail!==''?' '.$detail:'')."\n");exit(1);}
    echo "PASS ".$name.($detail!==''?' '.$detail:'')."\n";
}
function tc_term($name,$slug,$parent=0){
    $t=get_term_by('slug',$slug,'category');
    if($t&&!is_wp_error($t))return(int)$t->term_id;
    $r=wp_insert_term($name,'category',array('slug'=>$slug,'parent'=>$parent));
    if(is_wp_error($r)){fwrite(STDERR,"FATAL term ".$name.": ".$r->get_error_message()."\n");exit(2);}
    return(int)$r['term_id'];
}
function tc_parent_slug($parts){return 'tc-parent-'.substr(hash('sha256',implode(' > ',$parts)),0,20);}
function tc_seed_path($path,$leaf_slug){
    $parts=array_values(array_filter(array_map('trim',explode(' > ',$path)),'strlen'));
    $parent=0;$seen=array();
    foreach($parts as $i=>$name){
        $seen[]=$name;
        $slug=$i===count($parts)-1?$leaf_slug:tc_parent_slug($seen);
        $parent=tc_term($name,$slug,$parent);
    }
    return $parent;
}
function tc_targets($row){
    $x=json_decode((string)($row['topic_targets']??''),true);
    return is_array($x)?array_values(array_filter($x,'is_array')):array();
}
function tc_code($destination,$label,$image='ok'){
    return '<a data-id="'.esc_attr(substr(hash('sha256',$destination.'|'.$label.'|'.$image),0,12)).'" href="https://www.awin1.com/cread.php?awinmid=11202&awinaffid=99999&ued='.rawurlencode($destination).'"><img src="https://example.com/'.rawurlencode($image).'.png" width="1" height="1" alt="'.esc_attr($label).'"></a>';
}
function tc_import_pending($call,$destination,$label,$image='ok'){
    $parsed=$call('creative_library_parse_html_codes',tc_code($destination,$label,$image),5000);
    tc_assert(!is_wp_error($parsed),'html_code_parsed_'.$image);
    $context=array('provider'=>'direct','partner_external_id'=>'tarifcheck','partner_name'=>'Tarifcheck','source_kind'=>'banner','run_uuid'=>'');
    $normalized=$call('creative_library_normalize_row',$parsed['rows'][0],$parsed['mapping'],$context);
    tc_assert(!is_wp_error($normalized),'html_code_normalized_'.$image);
    tc_assert(esc_url_raw((string)$normalized['destination_url'])===esc_url_raw($destination),'destination_resolved_before_assignment_'.$image);
    $payload=json_decode((string)$normalized['payload'],true);
    tc_assert(sanitize_key((string)($payload['_destination_source']??''))==='decoded_tracking','destination_source_decoded_'.$image);
    $result=$call('creative_library_upsert',$normalized);
    tc_assert(in_array($result,array('imported','updated','unchanged'),true),'html_code_stored_pending_'.$image,$result);
    global $wpdb;$table=$call('creative_library_table');
    $stored=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",(string)$normalized['identity_hash']),ARRAY_A);
    tc_assert(is_array($stored),'stored_row_'.$image);
    tc_assert(count(tc_targets($stored))===0,'no_target_before_technical_verification_'.$image,wp_json_encode(tc_targets($stored)));
    return $stored;
}
function tc_verify($call,$row,$name){
    $result=$call('creative_library_verify_asset_row',$row,true,false);
    global $wpdb;$table=$call('creative_library_table');
    $stored=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d",(int)$row['id']),ARRAY_A);
    return array($result,$stored);
}

$png=base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Y9Zl1sAAAAASUVORK5CYII=');
add_filter('pre_http_request',static function($pre,$args,$url)use($png){
    if(strpos((string)$url,'https://example.com/')===0){
        if(strpos((string)$url,'broken')!==false)return new WP_Error('test_image_broken','simulated broken image');
        return array(
            'headers'=>array('content-type'=>'image/png'),
            'body'=>$png,
            'response'=>array('code'=>200,'message'=>'OK'),
            'cookies'=>array(),
            'filename'=>null
        );
    }
    return $pre;
},10,3);

// Realen Kategoriebaum nachbauen.
$catalog=json_decode((string)file_get_contents(WP_PLUGIN_DIR.'/affiliate-portal-router/assets/ebay-portal-catalog-v2.json'),true);
tc_assert(is_array($catalog)&&is_array($catalog['article_targets']??null),'catalog_loaded');
$cost_records=array_values(array_filter($catalog['article_targets'],static function($x){
    return is_array($x)&&sanitize_key((string)($x['theme']??''))==='kosten';
}));
$unique_cost_paths=array();
foreach($cost_records as $x){
    $p=(string)($x['path']??'');
    if($p!==''&&!isset($unique_cost_paths[$p]))$unique_cost_paths[$p]=$x;
}
$insurance_records=array_values(array_filter($catalog['article_targets'],static function($x){
    return is_array($x)&&strpos((string)($x['path']??''),'Wissen > Versicherungen & Recht >')===0;
}));
tc_assert(count($cost_records)===67,'cost_records_67');
tc_assert(count($unique_cost_paths)===66,'cost_unique_paths_66');
tc_assert(count($insurance_records)===14,'insurance_records_14');

$cost_ids=array();
foreach($unique_cost_paths as $x){
    $slug=sanitize_key((string)$x['category_slug']);
    $cost_ids[$slug]=tc_seed_path((string)$x['path'],$slug);
}
$insurance_ids=array();
foreach($insurance_records as $x){
    $slug=sanitize_key((string)$x['category_slug']);
    $insurance_ids[$slug]=tc_seed_path((string)$x['path'],$slug);
}
tc_assert(count($cost_ids)===66,'seeded_cost_66');
tc_assert(count($insurance_ids)===14,'seeded_insurance_14');

// Kredit: vor Prüfung keine Zuordnung, nach Prüfung alle Kosten.
$creditPending=tc_import_pending($call,'https://www.tarifcheck.de/kredit/','Tarifcheck Kredit','credit-ok');
list($creditVerify,$creditRow)=tc_verify($call,$creditPending,'credit');
tc_assert(!is_wp_error($creditVerify),'credit_image_verification_pass');
$creditTargets=tc_targets($creditRow);
tc_assert(count($creditTargets)===66,'credit_targets_after_verification_66','count='.count($creditTargets));
$creditKeys=array_column($creditTargets,'target_key');
foreach($cost_ids as $slug=>$id)tc_assert(in_array('category:'.$id,$creditKeys,true),'credit_contains_'.$slug);
foreach($insurance_ids as $slug=>$id)tc_assert(!in_array('category:'.$id,$creditKeys,true),'credit_excludes_insurance_'.$slug);

// Versicherung: vor Prüfung keine Zuordnung, nach Prüfung alle Versicherungsblätter.
$insPending=tc_import_pending($call,'https://www.tarifcheck.de/pferdehaftpflicht/','Tarifcheck Pferdehaftpflicht','insurance-ok');
list($insVerify,$insRow)=tc_verify($call,$insPending,'insurance');
tc_assert(!is_wp_error($insVerify),'insurance_image_verification_pass');
$insTargets=tc_targets($insRow);
tc_assert(count($insTargets)===14,'insurance_targets_after_verification_14','count='.count($insTargets));
$insKeys=array_column($insTargets,'target_key');
foreach($insurance_ids as $slug=>$id)tc_assert(in_array('category:'.$id,$insKeys,true),'insurance_contains_'.$slug);
foreach($cost_ids as $slug=>$id)tc_assert(!in_array('category:'.$id,$insKeys,true),'insurance_excludes_cost_'.$slug);

// URL schlägt Titel.
$trapPending=tc_import_pending($call,'https://www.tarifcheck.de/kredit/?proof=insurance-title','Tarifcheck Pferdehaftpflicht','credit-title-trap');
list($trapVerify,$trapRow)=tc_verify($call,$trapPending,'credit_title_trap');
tc_assert(!is_wp_error($trapVerify),'credit_title_trap_image_pass');
tc_assert(count(tc_targets($trapRow))===66,'credit_url_beats_insurance_title');

// Unbekannt / gemischt bleiben auch nach erfolgreicher Bildprüfung ohne Ziel.
$unknownPending=tc_import_pending($call,'https://www.tarifcheck.de/strom/','Tarifcheck Strom','unknown-ok');
list($unknownVerify,$unknownRow)=tc_verify($call,$unknownPending,'unknown');
tc_assert(!is_wp_error($unknownVerify),'unknown_image_verification_pass');
tc_assert(count(tc_targets($unknownRow))===0,'unknown_stays_unassigned_after_verification');

$mixedPending=tc_import_pending($call,'https://www.tarifcheck.de/kredit/versicherung/','Tarifcheck gemischt','mixed-ok');
list($mixedVerify,$mixedRow)=tc_verify($call,$mixedPending,'mixed');
tc_assert(!is_wp_error($mixedVerify),'mixed_image_verification_pass');
tc_assert(count(tc_targets($mixedRow))===0,'mixed_stays_unassigned_after_verification');

// Kaputtes Bild: niemals Zielkarte.
$brokenPending=tc_import_pending($call,'https://www.tarifcheck.de/kredit/','Tarifcheck Kredit','broken');
list($brokenVerify,$brokenRow)=tc_verify($call,$brokenPending,'broken');
tc_assert(is_wp_error($brokenVerify),'broken_image_verification_fails');
tc_assert(count(tc_targets($brokenRow))===0,'broken_image_never_gets_target');
tc_assert(sanitize_key((string)($brokenRow['topic_status']??''))==='format_blocked','broken_image_format_blocked');

// Runtime liest nur gespeicherte Karte.
$portalKey=sanitize_key((string)$call('output_local_portal_key'));
$portal=null;
foreach((array)$call('output_portal_registry') as $p){
    if(is_array($p)&&!empty($p['enabled'])&&sanitize_key((string)($p['key']??''))===$portalKey){$portal=$p;break;}
}
tc_assert(is_array($portal),'local_portal_present');
$runtime=$call('output_banner_destination_classification',$creditRow,$portal);
tc_assert(is_array($runtime)&&sanitize_key((string)($runtime['source']??''))==='tarifcheck_credit_all_cost_categories','runtime_reads_stored_credit_map');
$runtimeKeys=array_values(array_unique(array_filter((array)($runtime['_ppar_banner_target_keys']??array()))));
tc_assert(count($runtimeKeys)===66,'runtime_credit_keys_66');

echo "TARIFCHECK_HTML_VERIFY_BEFORE_ASSIGN_672192_COMPLETE\n";
