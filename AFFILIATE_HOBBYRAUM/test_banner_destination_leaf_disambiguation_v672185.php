<?php
// Candidate-only contract: generic final destination path leaf may disambiguate
// otherwise equal portal targets. No provider/partner special case.
if(!class_exists('Pferdeportal_Affiliate_Router')){fwrite(STDERR,"FATAL plugin missing\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$call=function($name,...$args)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);};
$portalKey=sanitize_key((string)$call('output_local_portal_key'));
$portal=null;
foreach((array)$call('output_portal_registry') as $p){
    if(is_array($p)&&!empty($p['enabled'])&&sanitize_key((string)($p['key']??''))===$portalKey){$portal=$p;break;}
}
if(!is_array($portal)){fwrite(STDERR,"FATAL portal missing\n");exit(2);}

function mkrow($url){
  return array(
    'id'=>0,'provider'=>'manual','partner_external_id'=>'leaf-contract',
    'creative_type'=>'banner','destination_url'=>$url,
    'payload'=>wp_json_encode(array('_destination_source'=>'provider_explicit')),
    'topic_targets'=>'[]','topic_score'=>0,'classified_at'=>0
  );
}
$real='https://www.hkm-sports.com/de/reiter/reithelme-sicherheitswesten/reithelme.html?utm_source=affiliate&utm_medium=banner&utm_campaign=Reithelme&bid=322674-98720-';
$amb='https://example.com/reiter/reithelme-sicherheitswesten/';
$r1=$call('output_banner_destination_classification',mkrow($real),$portal);
$r2=$call('output_banner_destination_classification',mkrow($amb),$portal);
echo 'REAL_RESULT '.wp_json_encode($r1,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
echo 'AMBIGUOUS_RESULT '.wp_json_encode($r2,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
$real_ok=is_array($r1)&&sanitize_key((string)($r1['source']??''))==='banner_destination_url'
  && (string)($r1['target']['key']??'')==='page:186';
$amb_ok=is_array($r2)&&sanitize_key((string)($r2['source']??''))==='banner_destination_ambiguous'
  && empty($r2['target']);
if(!$real_ok){fwrite(STDERR,"FAIL real leaf URL did not resolve to page:186\n");exit(1);}
if(!$amb_ok){fwrite(STDERR,"FAIL true ambiguity did not remain ambiguous\n");exit(1);}
echo "PASS_REAL_LEAF_DISAMBIGUATION\n";
echo "PASS_TRUE_AMBIGUITY_REMAINS_BLOCKED\n";

// trigger live51 leaf candidate workflow
