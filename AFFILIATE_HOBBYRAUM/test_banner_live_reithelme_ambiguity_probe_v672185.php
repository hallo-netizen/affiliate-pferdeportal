<?php
if(!class_exists('Pferdeportal_Affiliate_Router')){fwrite(STDERR,"FATAL plugin missing\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$call=function($name,...$args)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);};
$portalKey=sanitize_key((string)$call('output_local_portal_key'));
$portal=null;
foreach((array)$call('output_portal_registry') as $p){
    if(is_array($p)&&!empty($p['enabled'])&&sanitize_key((string)($p['key']??''))===$portalKey){$portal=$p;break;}
}
if(!is_array($portal)){fwrite(STDERR,"FATAL portal missing\n");exit(2);}
global $wpdb;
$table=$call('creative_library_table');
$row=$wpdb->get_row("SELECT * FROM {$table} WHERE provider='adcell' AND partner_external_id='10787' AND external_id='322674' LIMIT 1",ARRAY_A);
if(!is_array($row)){fwrite(STDERR,"FATAL 322674 missing\n");exit(2);}

// Ignore the derived persisted fallback only in-memory; source DB is not changed.
$raw=$row;
$raw['topic_targets']='[]';
$raw['topic_score']=0;
$raw['classified_at']=0;
$classification=$call('output_banner_destination_classification',$raw,$portal);
$semantic=$call('output_destination_semantic_text',$raw);
$destTokens=$call('output_tokens',$semantic);
$exact=array();
foreach((array)$call('output_portal_targets',$portal) as $target){
    if(!is_array($target)||sanitize_key((string)($target['type']??''))!=='page')continue;
    $slugTokens=$call('output_tokens',str_replace(array('-','_'),' ',(string)($target['slug']??'')));
    if($slugTokens && !array_diff($slugTokens,$destTokens)){
        $exact[]=array('key'=>(string)($target['key']??''),'slug'=>(string)($target['slug']??''),'label'=>(string)($target['label']??''),'depth'=>(int)($target['depth']??0));
    }
}
echo 'REITHELME_RAW_CLASSIFICATION '.wp_json_encode($classification,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'REITHELME_EXACT_SLUG_CANDIDATES '.wp_json_encode($exact,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
$keys=array_column($exact,'key');
$ok=sanitize_key((string)($classification['source']??''))==='banner_destination_ambiguous'
    && in_array('page:186',$keys,true)
    && in_array('page:187',$keys,true);
if(!$ok){fwrite(STDERR,"FAIL expected exact real ambiguity not proven\n");exit(1);}
echo "NEGATIVE_REAL_REITHELME_AMBIGUITY_PROVEN\n";
