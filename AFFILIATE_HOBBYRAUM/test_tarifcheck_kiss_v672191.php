<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR, "FATAL plugin missing\n"); exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
$call=function($name,...$args)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);};

$call('maybe_install_creative_library_schema');

function tc_term($name,$slug,$parent=0){
    $existing=term_exists($slug,'category');
    if(is_array($existing)) return (int)$existing['term_id'];
    if(is_int($existing)) return $existing;
    $r=wp_insert_term($name,'category',array('slug'=>$slug,'parent'=>$parent));
    if(is_wp_error($r)){fwrite(STDERR,"FATAL term ".$name.": ".$r->get_error_message()."\n");exit(2);}
    return (int)$r['term_id'];
}
$kosten=tc_term('Kosten','kosten');
$versicherung=tc_term('Versicherungen & Recht','versicherungen-recht');
$kreditKosten=tc_term('Kredit','kredit-kosten',$kosten);
$kreditVers=tc_term('Kredit','kredit-versicherung',$versicherung);
$haftVers=tc_term('Pferdehaftpflicht','pferdehaftpflicht-versicherung',$versicherung);
$haftKosten=tc_term('Pferdehaftpflicht','pferdehaftpflicht-kosten',$kosten);
$stromKosten=tc_term('Strom','strom-kosten',$kosten);

$portalKey=sanitize_key((string)$call('output_local_portal_key'));
$portal=null;
foreach((array)$call('output_portal_registry') as $p){
    if(is_array($p)&&!empty($p['enabled'])&&sanitize_key((string)($p['key']??''))===$portalKey){$portal=$p;break;}
}
if(!is_array($portal)){fwrite(STDERR,"FATAL local portal missing\n");exit(2);}

function tc_code($destination,$alt){
    return '<a data-id="'.esc_attr(substr(hash('sha256',$destination),0,12)).'" href="https://www.awin1.com/cread.php?awinmid=11202&awinaffid=99999&ued='.rawurlencode($destination).'"><img src="https://example.com/'.rawurlencode(strtolower(str_replace(' ','-',$alt))).'.jpg" width="728" height="90" alt="'.esc_attr($alt).'"></a>';
}
function tc_import_and_map($call,$o,$destination,$label){
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
function tc_assert($ok,$name,$detail=''){
    if(!$ok){fwrite(STDERR,"FAIL ".$name.($detail!==''?' '.$detail:'')."\n");exit(1);}
    echo "PASS ".$name.($detail!==''?' '.$detail:'')."\n";
}

list($creditMap,$creditRow)=tc_import_and_map($call,$o,'https://www.tarifcheck.de/kredit/','Tarifcheck Kredit');
$creditTargets=tc_targets($creditRow);
tc_assert((int)($creditMap['mapped']??0)>=1,'credit_mapped');
tc_assert(count($creditTargets)===1,'credit_one_target',wp_json_encode($creditTargets));
tc_assert((string)($creditTargets[0]['target_key']??'')==='category:'.$kreditKosten,'credit_only_kosten',wp_json_encode($creditTargets));
tc_assert(strpos((string)($creditTargets[0]['target_label']??''),'Kosten')!==false,'credit_label_under_kosten');
tc_assert((string)($creditTargets[0]['target_key']??'')!=='category:'.$kreditVers,'credit_not_versicherung');

list($insMap,$insRow)=tc_import_and_map($call,$o,'https://www.tarifcheck.de/pferdehaftpflicht/','Tarifcheck Pferdehaftpflicht');
$insTargets=tc_targets($insRow);
tc_assert((int)($insMap['mapped']??0)>=1,'insurance_mapped');
tc_assert(count($insTargets)===1,'insurance_one_target',wp_json_encode($insTargets));
tc_assert((string)($insTargets[0]['target_key']??'')==='category:'.$haftVers,'insurance_only_versicherung',wp_json_encode($insTargets));
tc_assert(strpos((string)($insTargets[0]['target_label']??''),'Versicher')!==false,'insurance_label_under_versicherung');
tc_assert((string)($insTargets[0]['target_key']??'')!=='category:'.$haftKosten,'insurance_not_kosten');

list($unknownMap,$unknownRow)=tc_import_and_map($call,$o,'https://www.tarifcheck.de/strom/','Tarifcheck Strom');
tc_assert((int)($unknownMap['mapped']??0)===0,'unknown_tarifcheck_fail_closed',wp_json_encode(tc_targets($unknownRow)));
tc_assert(count(tc_targets($unknownRow))===0,'unknown_has_no_target');

list($mixedMap,$mixedRow)=tc_import_and_map($call,$o,'https://www.tarifcheck.de/kredit/versicherung/','Tarifcheck gemischt');
tc_assert((int)($mixedMap['mapped']??0)===0,'mixed_family_fail_closed',wp_json_encode(tc_targets($mixedRow)));
tc_assert(count(tc_targets($mixedRow))===0,'mixed_has_no_target');

$runtime=$call('output_banner_destination_classification',$creditRow,$portal);
tc_assert(is_array($runtime)&&sanitize_key((string)($runtime['source']??''))==='creative_library_destination_map','runtime_reads_stored_map',wp_json_encode($runtime));
tc_assert((string)($runtime['target']['key']??'')==='category:'.$kreditKosten,'runtime_credit_target_is_kosten');

echo "TARIFCHECK_KISS_672191_COMPLETE\n";
