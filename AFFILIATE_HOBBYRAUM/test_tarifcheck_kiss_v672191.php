<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR, "FATAL plugin missing\n"); exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
$call=function($name,...$args)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);};

$call('maybe_install_creative_library_schema');

function tc_assert($ok,$name,$detail=''){
    if(!$ok){fwrite(STDERR,"FAIL ".$name.($detail!==''?' '.$detail:'')."\n");exit(1);}
    echo "PASS ".$name.($detail!==''?' '.$detail:'')."\n";
}
function tc_term($name,$slug,$parent=0){
    $by_slug=get_term_by('slug',$slug,'category');
    if($by_slug && !is_wp_error($by_slug)) return (int)$by_slug->term_id;
    $r=wp_insert_term($name,'category',array('slug'=>$slug,'parent'=>$parent));
    if(is_wp_error($r)){fwrite(STDERR,"FATAL term ".$name." [".$slug."]: ".$r->get_error_message()."\n");exit(2);}
    return (int)$r['term_id'];
}
function tc_parent_slug($parts){
    return 'tc-parent-'.substr(hash('sha256',implode(' > ',$parts)),0,20);
}
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
function tc_code($destination,$alt){
    return '<a data-id="'.esc_attr(substr(hash('sha256',$destination.'|'.$alt),0,12)).'" href="https://www.awin1.com/cread.php?awinmid=11202&awinaffid=99999&ued='.rawurlencode($destination).'"><img src="https://example.com/'.rawurlencode(strtolower(str_replace(' ','-',$alt))).'.jpg" width="728" height="90" alt="'.esc_attr($alt).'"></a>';
}
function tc_import_and_map($call,$destination,$label){
    $parsed=$call('creative_library_parse_html_codes',tc_code($destination,$label),5000);
    if(is_wp_error($parsed)){fwrite(STDERR,"FAIL parse ".$label." ".$parsed->get_error_message()."\n");exit(1);}
    $context=array('provider'=>'direct','partner_external_id'=>'tarifcheck','partner_name'=>'Tarifcheck','source_kind'=>'banner','run_uuid'=>'');
    $row=$parsed['rows'][0]??array();
    $normalized=$call('creative_library_normalize_row',$row,$parsed['mapping'],$context);
    if(is_wp_error($normalized)){fwrite(STDERR,"FAIL normalize ".$label." ".$normalized->get_error_message()."\n");exit(1);}
    if(esc_url_raw((string)($normalized['destination_url']??''))!==esc_url_raw($destination)){
        fwrite(STDERR,"FAIL destination decode ".$label." got ".($normalized['destination_url']??'')."\n");exit(1);
    }
    $payload=json_decode((string)($normalized['payload']??''),true);
    if(!is_array($payload)||sanitize_key((string)($payload['_destination_source']??''))!=='decoded_tracking'){
        fwrite(STDERR,"FAIL destination provenance ".$label."\n");exit(1);
    }
    $result=$call('creative_library_upsert',$normalized);
    if(!in_array($result,array('imported','updated','unchanged'),true)){
        fwrite(STDERR,"FAIL upsert ".$label." result=".$result."\n");exit(1);
    }
    global $wpdb;
    $table=$call('creative_library_table');
    $stored=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",(string)$normalized['identity_hash']),ARRAY_A);
    if(!is_array($stored)){fwrite(STDERR,"FAIL stored row ".$label."\n");exit(1);}
    $map=$call('output_assign_banner_targets_from_destination_once',$stored);
    $stored=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s",(string)$normalized['identity_hash']),ARRAY_A);
    return array($map,$stored);
}
function tc_targets($row){
    $x=json_decode((string)($row['topic_targets']??''),true);
    return is_array($x)?array_values(array_filter($x,'is_array')):array();
}

// 1) Autoritativen Portal-Katalog prüfen.
$catalog_path=WP_PLUGIN_DIR.'/affiliate-portal-router/assets/ebay-portal-catalog-v2.json';
$catalog=json_decode((string)file_get_contents($catalog_path),true);
tc_assert(is_array($catalog)&&is_array($catalog['article_targets']??null),'catalog_loaded');
$cost_records=array_values(array_filter($catalog['article_targets'],static function($x){
    return is_array($x)&&sanitize_key((string)($x['theme']??''))==='kosten';
}));
tc_assert(count($cost_records)===67,'catalog_cost_records_67','count='.count($cost_records));
foreach($cost_records as $x){
    tc_assert(preg_match('/^Kosten(?:\\s|$)/u',(string)($x['category_name']??''))===1,'catalog_cost_name_prefix',(string)($x['category_slug']??''));
    tc_assert(preg_match('/-kosten$/',(string)($x['category_slug']??''))===1,'catalog_cost_slug_suffix',(string)($x['category_slug']??''));
}
$unique_paths=array();
foreach($cost_records as $x){
    $path=(string)($x['path']??'');
    if($path!==''&&!isset($unique_paths[$path])){$unique_paths[$path]=$x;}
}
tc_assert(count($unique_paths)===66,'catalog_cost_unique_paths_66','unique='.count($unique_paths));

$insurance_records=array_values(array_filter($catalog['article_targets'],static function($x){
    return is_array($x)&&strpos((string)($x['path']??''),'Wissen > Versicherungen & Recht >')===0;
}));
tc_assert(count($insurance_records)===14,'catalog_insurance_records_14','count='.count($insurance_records));

// 2) Den kompletten eindeutigen Kostenbaum in echter Hierarchie in WordPress nachbauen.
$cost_ids=array();
foreach($unique_paths as $x){
    $slug=sanitize_key((string)$x['category_slug']);
    $id=tc_seed_path((string)$x['path'],$slug);
    $cost_ids[$slug]=$id;
}
tc_assert(count($cost_ids)===66,'seeded_all_unique_cost_categories','count='.count($cost_ids));

// Nicht-Kosten-Fallen in mehreren Ästen.
$aus=tc_term('Ausrüstung','tc-ausruestung-trap');
$reit=tc_term('Reiterbedarf','tc-reiterbedarf-trap',$aus);
$not_cost=tc_term('Kredit Kosten','kredit-kosten-falsch',$reit);
$not_cost2=tc_term('Kostenfalle','kostenfalle',$reit);

// Kompletter konfigurierter Versicherungsast.
$insurance_ids=array();
foreach($insurance_records as $x){
    $slug=sanitize_key((string)$x['category_slug']);
    $id=tc_seed_path((string)$x['path'],$slug);
    $insurance_ids[$slug]=$id;
}
tc_assert(count($insurance_ids)===14,'seeded_all_insurance_leaf_categories','count='.count($insurance_ids));
$outside=tc_term('Pferdehaftpflicht','pferdehaftpflicht-ausserhalb',$reit);

$portalKey=sanitize_key((string)$call('output_local_portal_key'));
$portal=null;
foreach((array)$call('output_portal_registry') as $p){
    if(is_array($p)&&!empty($p['enabled'])&&sanitize_key((string)($p['key']??''))===$portalKey){$portal=$p;break;}
}
tc_assert(is_array($portal),'local_portal_present');

// 3) Kredit-URL muss auf ALLE realen Kosten-Kategorien gehen.
list($creditMap,$creditRow)=tc_import_and_map($call,'https://www.tarifcheck.de/kredit/','Tarifcheck Kredit');
$creditTargets=tc_targets($creditRow);
$creditKeys=array_values(array_map(static function($x){return (string)($x['target_key']??'');},$creditTargets));
tc_assert((int)($creditMap['mapped']??0)===66,'credit_mapped_all_unique_cost_categories','mapped='.(int)($creditMap['mapped']??0));
tc_assert(count($creditTargets)===66,'credit_has_66_fixed_cost_targets','count='.count($creditTargets));
foreach($cost_ids as $slug=>$id){
    tc_assert(in_array('category:'.$id,$creditKeys,true),'credit_contains_cost_'.$slug);
}
tc_assert(!in_array('category:'.$not_cost,$creditKeys,true),'credit_rejects_kosten_word_wrong_leaf');
tc_assert(!in_array('category:'.$not_cost2,$creditKeys,true),'credit_rejects_non_cost_suffix');
foreach($insurance_ids as $slug=>$id){
    tc_assert(!in_array('category:'.$id,$creditKeys,true),'credit_rejects_insurance_'.$slug);
}

// URL schlägt Titel: Kredit bleibt Kosten trotz Versicherungs-Titel.
list($creditTitleMap,$creditTitleRow)=tc_import_and_map($call,'https://www.tarifcheck.de/kredit/?proof=insurance-title','Tarifcheck Pferdehaftpflicht');
tc_assert((int)($creditTitleMap['mapped']??0)===66,'credit_url_beats_insurance_title');

// 4) Versicherung geht ausschließlich auf alle echten Blattkategorien im Versicherungsast.
list($insMap,$insRow)=tc_import_and_map($call,'https://www.tarifcheck.de/pferdehaftpflicht/','Tarifcheck Pferdehaftpflicht');
$insTargets=tc_targets($insRow);
$insKeys=array_values(array_map(static function($x){return (string)($x['target_key']??'');},$insTargets));
tc_assert((int)($insMap['mapped']??0)===14,'insurance_mapped_all_insurance_categories','mapped='.(int)($insMap['mapped']??0));
tc_assert(count($insTargets)===14,'insurance_has_14_fixed_targets','count='.count($insTargets));
foreach($insurance_ids as $slug=>$id){
    tc_assert(in_array('category:'.$id,$insKeys,true),'insurance_contains_'.$slug);
}
foreach($insTargets as $x){
    $label=(string)($x['target_label']??'');
    tc_assert(strpos($label,'Versicherungen & Recht')!==false,'insurance_only_real_insurance_branch',$label);
}
tc_assert(!in_array('category:'.$outside,$insKeys,true),'insurance_rejects_same_topic_outside_branch');
foreach($cost_ids as $slug=>$id){
    tc_assert(!in_array('category:'.$id,$insKeys,true),'insurance_rejects_cost_'.$slug);
}
list($insuranceTitleMap,$insuranceTitleRow)=tc_import_and_map($call,'https://www.tarifcheck.de/pferdehaftpflicht/?proof=credit-title','Tarifcheck Kredit');
tc_assert((int)($insuranceTitleMap['mapped']??0)===14,'insurance_url_beats_credit_title');

// 5) Unbekannt / gemischt fail-closed.
list($unknownMap,$unknownRow)=tc_import_and_map($call,'https://www.tarifcheck.de/strom/','Tarifcheck Strom');
tc_assert((int)($unknownMap['mapped']??0)===0,'unknown_tarifcheck_fail_closed',wp_json_encode(tc_targets($unknownRow)));
tc_assert(count(tc_targets($unknownRow))===0,'unknown_has_no_target');
list($mixedMap,$mixedRow)=tc_import_and_map($call,'https://www.tarifcheck.de/kredit/versicherung/','Tarifcheck gemischt');
tc_assert((int)($mixedMap['mapped']??0)===0,'mixed_family_fail_closed',wp_json_encode(tc_targets($mixedRow)));
tc_assert(count(tc_targets($mixedRow))===0,'mixed_has_no_target');

// 6) Runtime liest nur gespeicherte Karte und trägt ALLE Kosten-Slugs in eine Kampagne.
$runtime=$call('output_banner_destination_classification',$creditRow,$portal);
tc_assert(is_array($runtime)&&sanitize_key((string)($runtime['source']??''))==='tarifcheck_credit_all_cost_categories','runtime_reads_tarifcheck_cost_map',wp_json_encode($runtime));
$runtimeKeys=array_values(array_unique(array_filter(array_map('sanitize_text_field',(array)($runtime['_ppar_banner_target_keys']??array())))));
tc_assert(count($runtimeKeys)===66,'runtime_exposes_all_cost_campaign_targets','count='.count($runtimeKeys));
foreach($unique_paths as $x){
    tc_assert(in_array('category:'.sanitize_key((string)$x['category_slug']),$runtimeKeys,true),'runtime_has_slug_'.sanitize_key((string)$x['category_slug']));
}
$insRuntime=$call('output_banner_destination_classification',$insRow,$portal);
tc_assert(is_array($insRuntime)&&sanitize_key((string)($insRuntime['source']??''))==='tarifcheck_insurance_all_insurance_categories','runtime_reads_tarifcheck_insurance_map',wp_json_encode($insRuntime));
$insRuntimeKeys=array_values(array_unique(array_filter(array_map('sanitize_text_field',(array)($insRuntime['_ppar_banner_target_keys']??array())))));
tc_assert(count($insRuntimeKeys)===14,'runtime_exposes_all_insurance_campaign_targets','count='.count($insRuntimeKeys));
foreach($insurance_records as $x){
    tc_assert(in_array('category:'.sanitize_key((string)$x['category_slug']),$insRuntimeKeys,true),'runtime_has_insurance_slug_'.sanitize_key((string)$x['category_slug']));
}

echo "TARIFCHECK_KISS_672191_ALL_COST_AND_INSURANCE_CATEGORIES_COMPLETE\n";
