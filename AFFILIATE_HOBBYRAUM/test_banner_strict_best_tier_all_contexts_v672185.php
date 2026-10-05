<?php
$GLOBALS['all_fail']=array();
$GLOBALS['all_pass']=array();
function ac($ok,$name,$detail=''){
  echo ($ok?'PASS ':'FAIL ').$name.($detail!==''?' :: '.$detail:'')."\n";
  if($ok)$GLOBALS['all_pass'][]=$name; else $GLOBALS['all_fail'][]=$name;
}
if(!class_exists('Pferdeportal_Affiliate_Router')){fwrite(STDERR,"FATAL plugin missing\n");exit(2);}
if(Pferdeportal_Affiliate_Router::VERSION!=='6.72.185'){fwrite(STDERR,"FATAL version ".Pferdeportal_Affiliate_Router::VERSION."\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($name)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m;};
$rp=function($name)use($o){$p=new ReflectionProperty($o,$name);$p->setAccessible(true);return $p;};
$call=function($name,...$args)use($rm,$o){return $rm($name)->invokeArgs($o,$args);};

update_option('ppar_enabled','1',false);
update_option('ppar_assignments_v1',array(),false);
delete_option('ppar_debug');

$http=0;
add_filter('pre_http_request',function($pre,$args,$url)use(&$http){$http++;return new WP_Error('blocked','network forbidden in strict-tier gate');},PHP_INT_MAX,3);

$mkpost=function($type,$title,$slug,$parent=0){
  $id=wp_insert_post(array('post_type'=>$type,'post_status'=>'publish','post_title'=>$title,'post_name'=>$slug,'post_parent'=>$parent,'post_content'=>'Fixture '.$title),true);
  if(is_wp_error($id)||!$id){fwrite(STDERR,"FATAL post ".$slug."\n");exit(2);} return (int)$id;
};
$mkterm=function($tax,$name,$slug,$parent=0){
  $r=wp_insert_term($name,$tax,array('slug'=>$slug,'parent'=>$parent));
  if(is_wp_error($r)){fwrite(STDERR,"FATAL term ".$slug." ".$r->get_error_message()."\n");exit(2);} return (int)$r['term_id'];
};

// Real production context families: page hierarchy, category archive, post,
// journal, market/HivePress, glossary and breed.
$start=$mkpost('page','Start Tier Gate','start-tier-gate');
$hub1=$mkpost('page','Ausrüstung Tier Gate','ausruestung-tier-gate');
$hub2=$mkpost('page','Reiterbedarf Tier Gate','reiterbedarf-tier-gate',$hub1);
$leaf=$mkpost('page','Reithelme Tier Gate','reithelme-tier-gate',$hub2);
$journal=$mkpost('page','Journal Tier Gate','journal-tier-gate');
$marketPage=$mkpost('page','Anzeigenmarkt Tier Gate','anzeigenmarkt-tier-gate');

$catRoot=$mkterm('category','Ausrüstung Kategorie Tier Gate','ausruestung-kategorie-tier-gate');
$catLeaf=$mkterm('category','Reithelme Kategorie Tier Gate','reithelme-kategorie-tier-gate',$catRoot);
$post=$mkpost('post','Reithelme Beitrag Tier Gate','reithelme-beitrag-tier-gate');
wp_set_post_categories($post,array($catLeaf),false);

$ug=$mkterm('uge_group','Ausrüstung Glossar Tier Gate','ausruestung-glossar-tier-gate');
$uge=$mkpost('uge_term','Reithelm Glossar Tier Gate','reithelm-glossar-tier-gate');
wp_set_object_terms($uge,array($ug),'uge_group',false);

$bg=$mkterm('pa_breed_group','Warmblut Tier Gate','warmblut-tier-gate');
$breed=$mkpost('pa_breed','Hannoveraner Tier Gate','hannoveraner-tier-gate');
wp_set_object_terms($breed,array($bg),'pa_breed_group',false);

$hpRoot=$mkterm('hp_listing_category','Reitausrüstung Markt Tier Gate','reitausruestung-markt-tier-gate');
$hpLeaf=$mkterm('hp_listing_category','Reithelme Markt Tier Gate','reithelme-markt-tier-gate',$hpRoot);
$listing=$mkpost('hp_listing','Reithelm Anbieter Tier Gate','reithelm-anbieter-tier-gate');
wp_set_object_terms($listing,array($hpLeaf),'hp_listing_category',false);

$getctx=function($id)use($call){return $call('get_content_context',$id);};
$getcatctx=function($id)use($call){$t=get_term($id,'category');return $call('get_category_archive_context',$t);};

$ctxPageStart=$getctx($start);
$ctxHub1=$getctx($hub1);
$ctxHub2=$getctx($hub2);
$ctxLeaf=$getctx($leaf);
$ctxPost=$getctx($post);
$ctxUge=$getctx($uge);
$ctxBreed=$getctx($breed);
$ctxListing=$getctx($listing);
$ctxCat=$getcatctx($catLeaf);
$ctxJournal=$getctx($journal);
$ctxMarketPage=$getctx($marketPage);

$ctxHpArchive=array(
  'slugs'=>array('reithelme-markt-tier-gate','reitausruestung-markt-tier-gate'),
  'names'=>array('Reithelme Markt Tier Gate','Reitausrüstung Markt Tier Gate'),
  'primary_slug'=>'reithelme-markt-tier-gate','primary_name'=>'Reithelme Markt Tier Gate',
  'post_type'=>'hp_listing_category_archive','haystack'=>'reithelme markt tier gate reitausruestung',
  'post_id'=>0,'ancestor_ids'=>array(),'term_ids'=>array($hpLeaf,$hpRoot),
  'direct_term_slugs'=>array('reithelme-markt-tier-gate')
);
$ctxUgeGroup=array(
  'slugs'=>array('ausruestung-glossar-tier-gate'),'names'=>array('Ausrüstung Glossar Tier Gate'),
  'primary_slug'=>'ausruestung-glossar-tier-gate','primary_name'=>'Ausrüstung Glossar Tier Gate',
  'post_type'=>'uge_group_archive','haystack'=>'ausruestung glossar tier gate','post_id'=>0,
  'ancestor_ids'=>array(),'term_ids'=>array($ug),'direct_term_slugs'=>array('ausruestung-glossar-tier-gate')
);
$ctxBreedGroup=array(
  'slugs'=>array('warmblut-tier-gate'),'names'=>array('Warmblut Tier Gate'),
  'primary_slug'=>'warmblut-tier-gate','primary_name'=>'Warmblut Tier Gate',
  'post_type'=>'pa_breed_group_archive','haystack'=>'warmblut tier gate','post_id'=>0,
  'ancestor_ids'=>array(),'term_ids'=>array($bg),'direct_term_slugs'=>array('warmblut-tier-gate')
);

$scenarios=array(
  array('start_page',$ctxPageStart,'start_after_topics','page:start-tier-gate'),
  array('hub1_page',$ctxHub1,'hub_top_cta','page:ausruestung-tier-gate'),
  array('hub1_after_cards',$ctxHub1,'hub_after_cards','page:ausruestung-tier-gate'),
  array('hub1_grid',$ctxHub1,'hub_grid_card','page:ausruestung-tier-gate'),
  array('hub2_page',$ctxHub2,'hub_mid_banner','page:reiterbedarf-tier-gate'),
  array('leaf_product_banner',$ctxLeaf,'product_after_category_tiles','page:reithelme-tier-gate'),
  array('leaf_category_alias',$ctxLeaf,'category_recommendation','page:reithelme-tier-gate'),
  array('template_top',$ctxLeaf,'template_top','page:reithelme-tier-gate'),
  array('template_after_intro',$ctxLeaf,'template_after_intro','page:reithelme-tier-gate'),
  array('template_after_selected',$ctxLeaf,'template_after_selected','page:reithelme-tier-gate'),
  array('template_mid',$ctxLeaf,'template_mid','page:reithelme-tier-gate'),
  array('template_mid_banner',$ctxLeaf,'template_mid_banner','page:reithelme-tier-gate'),
  array('template_bottom',$ctxLeaf,'template_bottom','page:reithelme-tier-gate'),
  array('category_archive',$ctxCat,'category_recommendation','category:reithelme-kategorie-tier-gate'),
  array('post_top_info',$ctxPost,'top_info','category:reithelme-kategorie-tier-gate'),
  array('post_mid_content',$ctxPost,'mid_content','category:reithelme-kategorie-tier-gate'),
  array('post_bottom',$ctxPost,'bottom_recommendation','category:reithelme-kategorie-tier-gate'),
  array('post_after_intro',$ctxPost,'post_after_intro','category:reithelme-kategorie-tier-gate'),
  array('post_mid',$ctxPost,'post_mid_content','category:reithelme-kategorie-tier-gate'),
  array('post_bottom_rec',$ctxPost,'post_bottom_recommendation','category:reithelme-kategorie-tier-gate'),
  array('post_inline',$ctxPost,'post_inline_banner','category:reithelme-kategorie-tier-gate'),
  array('journal_page',$ctxJournal,'journal_banner','journal:journal-tier-gate'),
  array('market_page',$ctxMarketPage,'anzeigenmarkt_top_banner','market:anzeigenmarkt'),
  array('hp_listing',$ctxListing,'anzeigenmarkt_category_banner','market:reithelme-markt-tier-gate'),
  array('hp_listing_archive',$ctxHpArchive,'anzeigenmarkt_category_banner','market:reithelme-markt-tier-gate'),
  array('glossary_single',$ctxUge,'glossary_single_banner','uge_term:reithelm-glossar-tier-gate'),
  array('glossary_desktop',$ctxUge,'glossary_single_desktop_banner','uge_term:reithelm-glossar-tier-gate'),
  array('glossary_mobile',$ctxUge,'glossary_single_mobile_banner','uge_term:reithelm-glossar-tier-gate'),
  array('glossary_group_archive',$ctxUgeGroup,'glossary_overview_banner','uge_group:ausruestung-glossar-tier-gate'),
  array('breed_single',$ctxBreed,'breed_single_banner','pa_breed:hannoveraner-tier-gate'),
  array('breed_desktop',$ctxBreed,'breed_single_desktop_banner','pa_breed:hannoveraner-tier-gate'),
  array('breed_mobile',$ctxBreed,'breed_single_mobile_banner','pa_breed:hannoveraner-tier-gate'),
  array('breed_group_archive',$ctxBreedGroup,'breed_overview_banner','pa_breed_group:warmblut-tier-gate')
);

$save=$rm('save_campaign_record');
$campaignIds=array();
$flush=function()use($rp,$o){
  try{$rp('campaigns_request_cache')->setValue($o,null);}catch(Throwable $e){}
  foreach(array(
    'ranked_campaigns_request_cache','ranked_campaign_candidate_index_request_cache',
    'ranked_campaign_raw_records_request_cache','ranked_campaign_from_post_request_cache',
    'automation_exact_target_rank_request_cache'
  ) as $p){try{$rp($p)->setValue($o,array());}catch(Throwable $e){}}
};
$dimFor=function($slot)use($call){
  $rule=$call('runtime_contract_slot_rule',$slot);
  if(!is_array($rule)){return array(1200,120,'missing');}
  $rmin=(float)($rule['ratio_min']??1.0);$rmax=(float)($rule['ratio_max']??12.0);
  $ratio=max(0.1,($rmin+$rmax)/2.0);
  $minw=max(1,(int)($rule['min_width']??1));$minh=max(1,(int)($rule['min_height']??1));
  $h=max($minh,(int)ceil($minw/$ratio));
  $w=max($minw,(int)ceil($h*$ratio));
  return array($w,$h,'ok');
};
$make=function($id,$slot,$targetKey,$mode,$priority,$partner)use($save,$o,&$campaignIds,$dimFor){
  list($w,$h,$state)=$dimFor($slot);
  if($state!=='ok'){fwrite(STDERR,"FATAL no contract rule ".$slot."\n");exit(2);}
  $c=array(
    'id'=>$id,'active'=>1,'creative_type'=>'banner','network'=>'manual','programme_status'=>'active','source'=>'output_object_v4',
    'render_mode'=>'image_link','title'=>$id,'description'=>'','button_text'=>'Mehr erfahren',
    'image_url'=>'https://img.example.test/'.$id.'.jpg','url'=>'https://click.example.test/'.$id,
    'target'=>'_blank','placements'=>array($slot),'assignment_mode'=>$mode,'priority'=>$priority,
    'health_check_enabled'=>false,'dimensions'=>$w.'x'.$h,'partner'=>$partner,
    'match_descendants'=>true
  );
  if($targetKey!=='')$c['automation_target_keys']=array($targetKey);
  $pid=$save->invoke($o,$c,0);
  if(is_wp_error($pid)||!$pid){fwrite(STDERR,"FATAL campaign ".$id."\n");exit(2);}
  $campaignIds[$id]=(int)$pid; return (int)$pid;
};
$setOnly=function($keys)use(&$campaignIds,$flush){
  foreach($campaignIds as $key=>$pid){
    $d=get_post_meta($pid,'ppar_campaign_data',true);$d=is_array($d)?$d:array();
    $d['active']=in_array($key,$keys,true)?1:0;update_post_meta($pid,'ppar_campaign_data',$d);
  }
  $flush();
};
$key=function($sel){return (string)($sel['campaign']['id']??'');};

$results=array();
foreach($scenarios as $idx=>$s){
  list($name,$ctx,$slot,$targetKey)=$s;
  $safe=preg_replace('/[^a-z0-9]+/','-',strtolower($name));
  $exact='exact-'.$safe;
  $generalA='general-a-'.$safe;
  $generalB='general-b-'.$safe;
  $make($exact,$slot,$targetKey,'page_tree',1,'exact-'.$safe);
  $make($generalA,$slot,'','fallback',999,'general-a-'.$safe);
  $make($generalB,$slot,'','fallback',998,'general-b-'.$safe);
  $setOnly(array($exact,$generalA,$generalB));

  $q0=(int)$GLOBALS['wpdb']->num_queries;
  $p1=$call('select_campaign_for_slot_position',$ctx,$slot,1);
  $p2=$call('select_campaign_for_slot_position',$ctx,$slot,2);
  $q1=(int)$GLOBALS['wpdb']->num_queries;
  $k1=$key($p1);$k2=$key($p2);
  $row=array('name'=>$name,'post_type'=>(string)($ctx['post_type']??''),'slot'=>$slot,'target'=>$targetKey,'p1'=>$k1,'p2'=>$k2,'queries'=>$q1-$q0);
  $results[]=$row;
  echo 'CONTEXT_RESULT '.wp_json_encode($row,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
  ac($k1===$exact,'CTX_'.$name.'_position1_exact',$k1);
  ac($k2===$exact,'CTX_'.$name.'_position2_stays_best_tier',$k2);
}

// Pure invariant across every supported banner slot: after ranking, no lower
// relevance band may remain available to delivery/rotation.
$bannerSlots=array(
 'start_after_topics','top_info','mid_content','bottom_recommendation',
 'post_after_intro','post_mid_content','post_bottom_recommendation','post_inline_banner',
 'hub_top_cta','hub_after_cards','hub_grid_card','hub_mid_banner',
 'category_recommendation','product_after_category_tiles','produkt_recommendation',
 'template_top','template_after_intro','template_after_selected','template_mid','template_mid_banner','template_bottom',
 'journal_banner','anzeigenmarkt_top_banner','anzeigenmarkt_category_banner',
 'glossary_single_banner','glossary_single_desktop_banner','glossary_single_mobile_banner','glossary_overview_banner',
 'breed_single_banner','breed_single_desktop_banner','breed_single_mobile_banner','breed_overview_banner'
);
foreach($bannerSlots as $slot){
  ac($call('slot_required_creative_type',$slot)==='banner','SLOT_'.$slot.'_is_banner');
  ac(is_array($call('runtime_contract_slot_rule',$slot)),'SLOT_'.$slot.'_has_contract_rule');
}

ac($http===0,'ALL_CONTEXTS_zero_frontend_http','http='.$http);
echo 'ALL_CONTEXTS_SUMMARY '.wp_json_encode(array(
  'scenarios'=>count($scenarios),'passes'=>count($GLOBALS['all_pass']),'failures'=>count($GLOBALS['all_fail']),
  'http'=>$http,'results'=>$results
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
if($GLOBALS['all_fail']){echo 'ALL_CONTEXTS_FAILURES '.wp_json_encode($GLOBALS['all_fail'],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";exit(1);}
echo "STRICT_BEST_TIER_ALL_CONTEXTS_PASS\n";
