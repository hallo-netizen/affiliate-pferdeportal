<?php
$GLOBALS['p']=array();$GLOBALS['f']=array();
function ck187($ok,$name,$detail=''){echo ($ok?'PASS ':'FAIL ').$name.($detail!==''?' :: '.$detail:'')."\n";if($ok)$GLOBALS['p'][]=$name;else$GLOBALS['f'][]=$name;}
if(!class_exists('Pferdeportal_Affiliate_Router')){fwrite(STDERR,"FATAL plugin missing\n");exit(2);}
if(!class_exists('Pferde_Template_Kit')){class Pferde_Template_Kit{
 public static function affiliate_contract_version(){return '1.0';}
 public static function design_profile(){return 'pferde_atelier';}
 public static function design_profile_contract_version(){return '1.0';}
 public static function affiliate_page_type($id){return get_post_field('post_parent',(int)$id)?'category':'hub1';}
}}
if(!post_type_exists('uge_term'))register_post_type('uge_term',array('public'=>true,'supports'=>array('title','editor')));
if(!taxonomy_exists('uge_group'))register_taxonomy('uge_group',array('uge_term'),array('public'=>true,'hierarchical'=>true));
if(!post_type_exists('pa_breed'))register_post_type('pa_breed',array('public'=>true,'supports'=>array('title','editor')));
if(!taxonomy_exists('pa_breed_group'))register_taxonomy('pa_breed_group',array('pa_breed'),array('public'=>true,'hierarchical'=>true));
if(!post_type_exists('hp_listing'))register_post_type('hp_listing',array('public'=>true,'supports'=>array('title','editor')));
if(!taxonomy_exists('hp_listing_category'))register_taxonomy('hp_listing_category',array('hp_listing'),array('public'=>true,'hierarchical'=>true));
if(Pferdeportal_Affiliate_Router::VERSION!=='6.72.187'){fwrite(STDERR,"FATAL version ".Pferdeportal_Affiliate_Router::VERSION."\n");exit(2);}
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($name)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m;};
$rp=function($name)use($o){$p=new ReflectionProperty($o,$name);$p->setAccessible(true);return $p;};
$call=function($name,...$args)use($rm,$o){return $rm($name)->invokeArgs($o,$args);};
update_option('ppar_enabled','1',false);update_option('ppar_assignments_v1',array(),false);delete_option('ppar_debug');

// Test isolation: this gate may run after other disposable regression fixtures.
// Deactivate only pre-existing test campaigns in this disposable WordPress DB.
foreach((array)$call('get_campaigns') as $existingCampaign){
  $pid=absint($existingCampaign['post_id']??0);
  if($pid<=0)continue;
  $d=get_post_meta($pid,'ppar_campaign_data',true);
  if(!is_array($d))continue;
  $d['active']=0;
  update_post_meta($pid,'ppar_campaign_data',$d);
}
try{$rp('campaigns_request_cache')->setValue($o,null);}catch(Throwable $e){}
foreach(array('ranked_campaigns_request_cache','ranked_campaign_candidate_index_request_cache','ranked_campaign_raw_records_request_cache','ranked_campaign_from_post_request_cache','automation_exact_target_rank_request_cache') as $prop){
  try{$rp($prop)->setValue($o,array());}catch(Throwable $e){}
}

$http=0;
add_filter('pre_http_request',function($pre,$args,$url)use(&$http){$http++;return new WP_Error('blocked','network forbidden in strict-tier positive gate');},PHP_INT_MAX,3);

$mkpost=function($type,$title,$slug,$parent=0){
  $id=wp_insert_post(array('post_type'=>$type,'post_status'=>'publish','post_title'=>$title,'post_name'=>$slug,'post_parent'=>$parent,'post_content'=>'Fixture '.$title),true);
  if(is_wp_error($id)||!$id){fwrite(STDERR,"FATAL post ".$slug."\n");exit(2);}return (int)$id;
};
$mkterm=function($tax,$name,$slug,$parent=0){
  $r=wp_insert_term($name,$tax,array('slug'=>$slug,'parent'=>$parent));
  if(is_wp_error($r)){fwrite(STDERR,"FATAL term ".$slug." ".$r->get_error_message()."\n");exit(2);}return (int)$r['term_id'];
};

// Page levels.
$start=$mkpost('page','Start Tier 187','start-tier-187');
$hub1=$mkpost('page','Ausrüstung Tier 187','ausruestung-tier-187');
$hub2=$mkpost('page','Reiterbedarf Tier 187','reiterbedarf-tier-187',$hub1);
$leaf=$mkpost('page','Reithelme Tier 187','reithelme-tier-187',$hub2);
$journal=$mkpost('page','Journal Tier 187','journal-tier-187');
$market=$mkpost('page','Anzeigenmarkt Tier 187','anzeigenmarkt-tier-187');

// Classic editorial post.
$catRoot=$mkterm('category','Ausrüstung Kategorie 186','ausruestung-kategorie-187');
$catLeaf=$mkterm('category','Reithelme Kategorie 186','reithelme-kategorie-187',$catRoot);
$post=$mkpost('post','Reithelme Beitrag 186','reithelme-beitrag-187');wp_set_post_categories($post,array($catLeaf),false);

// Glossary.
$ug=$mkterm('uge_group','Ausrüstung Glossar 186','ausruestung-glossar-187');
$uge=$mkpost('uge_term','Reithelm Glossar 186','reithelm-glossar-187');wp_set_object_terms($uge,array($ug),'uge_group',false);

// Breed.
$bg=$mkterm('pa_breed_group','Warmblut 186','warmblut-187');
$breed=$mkpost('pa_breed','Hannoveraner 186','hannoveraner-187');wp_set_object_terms($breed,array($bg),'pa_breed_group',false);

// HivePress.
$hpRoot=$mkterm('hp_listing_category','Reitausrüstung Markt 186','reitausruestung-markt-187');
$hpLeaf=$mkterm('hp_listing_category','Reithelme Markt 186','reithelme-markt-187',$hpRoot);
$listing=$mkpost('hp_listing','Reithelm Anbieter 186','reithelm-anbieter-187');wp_set_object_terms($listing,array($hpLeaf),'hp_listing_category',false);

$getctx=function($id)use($call){return $call('get_content_context',$id);};
$getcatctx=function($id)use($call){return $call('get_category_archive_context',get_term($id,'category'));};

$ctxHpArchive=array(
 'slugs'=>array('reithelme-markt-187','reitausruestung-markt-187'),'names'=>array('Reithelme Markt 186','Reitausrüstung Markt 186'),
 'primary_slug'=>'reithelme-markt-187','primary_name'=>'Reithelme Markt 186','post_type'=>'hp_listing_category_archive',
 'haystack'=>'reithelme markt 186 reitausruestung','post_id'=>0,'ancestor_ids'=>array(),'term_ids'=>array($hpLeaf,$hpRoot),'direct_term_slugs'=>array('reithelme-markt-187')
);
$ctxUgeGroup=array(
 'slugs'=>array('ausruestung-glossar-187'),'names'=>array('Ausrüstung Glossar 186'),
 'primary_slug'=>'ausruestung-glossar-187','primary_name'=>'Ausrüstung Glossar 186','post_type'=>'uge_group_archive',
 'haystack'=>'ausruestung glossar 186','post_id'=>0,'ancestor_ids'=>array(),'term_ids'=>array($ug),'direct_term_slugs'=>array('ausruestung-glossar-187')
);
$ctxBreedGroup=array(
 'slugs'=>array('warmblut-187'),'names'=>array('Warmblut 186'),
 'primary_slug'=>'warmblut-187','primary_name'=>'Warmblut 186','post_type'=>'pa_breed_group_archive',
 'haystack'=>'warmblut 186','post_id'=>0,'ancestor_ids'=>array(),'term_ids'=>array($bg),'direct_term_slugs'=>array('warmblut-187')
);

// Only canonical, actually active production banner slots plus every real content family.
$scenarios=array(
 array('start',$getctx($start),'start_after_topics','page:start-tier-187'),
 array('hub_after_cards',$getctx($hub1),'hub_after_cards','page:ausruestung-tier-187'),
 array('hub_grid',$getctx($hub2),'hub_grid_card','page:reiterbedarf-tier-187'),
 array('leaf_page',$getctx($leaf),'product_after_category_tiles','page:reithelme-tier-187'),
 array('category_archive',$getcatctx($catLeaf),'product_after_category_tiles','category:reithelme-kategorie-187'),
 array('classic_post',$getctx($post),'post_inline_banner','category:reithelme-kategorie-187'),
 array('journal',$getctx($journal),'journal_banner','journal:journal-tier-187'),
 array('market_page',$getctx($market),'anzeigenmarkt_top_banner','market:anzeigenmarkt'),
 array('hp_listing',$getctx($listing),'anzeigenmarkt_category_banner','market:reithelme-markt-187'),
 array('hp_listing_archive',$ctxHpArchive,'anzeigenmarkt_category_banner','market:reithelme-markt-187'),
 array('glossary_desktop',$getctx($uge),'glossary_single_desktop_banner','uge_term:reithelm-glossar-187'),
 array('glossary_mobile',$getctx($uge),'glossary_single_mobile_banner','uge_term:reithelm-glossar-187'),
 array('glossary_overview',$ctxUgeGroup,'glossary_overview_banner','uge_group:ausruestung-glossar-187'),
 array('breed_desktop',$getctx($breed),'breed_single_desktop_banner','pa_breed:hannoveraner-187'),
 array('breed_mobile',$getctx($breed),'breed_single_mobile_banner','pa_breed:hannoveraner-187'),
 array('breed_overview',$ctxBreedGroup,'breed_overview_banner','pa_breed_group:warmblut-187')
);

$save=$rm('save_campaign_record');$ids=array();
$flush=function()use($rp,$o){
 try{$rp('campaigns_request_cache')->setValue($o,null);}catch(Throwable $e){}
 foreach(array(
   'ranked_campaigns_request_cache','ranked_campaign_candidate_index_request_cache','ranked_campaign_raw_records_request_cache',
   'ranked_campaign_from_post_request_cache','automation_exact_target_rank_request_cache'
 ) as $p){try{$rp($p)->setValue($o,array());}catch(Throwable $e){}}
};
$dim=function($slot)use($call){
 $rule=$call('runtime_contract_slot_rule',$slot);if(!is_array($rule)){fwrite(STDERR,"FATAL no slot rule ".$slot."\n");exit(2);}
 $a=(float)($rule['ratio_min']??1);$b=(float)($rule['ratio_max']??12);$r=max(.1,($a+$b)/2);
 $mw=max(1,(int)($rule['min_width']??1));$mh=max(1,(int)($rule['min_height']??1));
 $h=max($mh,(int)ceil($mw/$r));$w=max($mw,(int)ceil($h*$r));
 return array($w,$h);
};
$make=function($id,$slot,$target,$mode,$priority,$partner)use($save,$o,&$ids,$dim){
 list($w,$h)=$dim($slot);
 $c=array(
  'id'=>$id,'active'=>1,'creative_type'=>'banner','network'=>'manual','programme_status'=>'active','source'=>'output_object_v4',
  'render_mode'=>'image_link','title'=>$id,'description'=>'','button_text'=>'Mehr erfahren',
  'image_url'=>'https://img.example.test/'.$id.'.jpg','url'=>'https://click.example.test/'.$id,
  'target'=>'_blank','placements'=>array($slot),'assignment_mode'=>$mode,'priority'=>$priority,
  'health_check_enabled'=>false,'dimensions'=>$w.'x'.$h,'partner'=>$partner,'match_descendants'=>true
 );
 if($target!=='')$c['automation_target_keys']=array($target);
 $pid=$save->invoke($o,$c,0);if(is_wp_error($pid)||!$pid){fwrite(STDERR,"FATAL campaign ".$id."\n");exit(2);}
 $ids[$id]=(int)$pid;
};
$set=function($active)use(&$ids,$flush){
 foreach($ids as $key=>$pid){$d=get_post_meta($pid,'ppar_campaign_data',true);$d=is_array($d)?$d:array();$d['active']=in_array($key,$active,true)?1:0;update_post_meta($pid,'ppar_campaign_data',$d);}
 $flush();
};
$selkey=function($s){return (string)($s['campaign']['id']??'');};
$rankkeys=function($rows){$a=array();foreach((array)$rows as $r)$a[]=array('id'=>(string)($r['campaign']['id']??''),'s'=>(int)($r['specificity']??0));return $a;};

foreach($scenarios as $s){
 list($name,$ctx,$slot,$target)=$s;$safe=preg_replace('/[^a-z0-9]+/','-',strtolower($name));
 $e1='exact1-'.$safe;$e2='exact2-'.$safe;$g1='general1-'.$safe;$g2='general2-'.$safe;
 $make($e1,$slot,$target,'page_tree',1,'exact-a-'.$safe);
 $make($g1,$slot,'','fallback',999,'general-a-'.$safe);
 $make($g2,$slot,'','fallback',998,'general-b-'.$safe);

 // One exact: exact must be fixed. No lower tier may remain in ranked pool.
 $set(array($e1,$g1,$g2));
 $q0=(int)$GLOBALS['wpdb']->num_queries;
 $p1=$call('select_campaign_for_slot_position',$ctx,$slot,1);
 $p2=$call('select_campaign_for_slot_position',$ctx,$slot,2);
 $rank=$call('ranked_campaigns_for_slot',$ctx,$slot,'');
 $q1=(int)$GLOBALS['wpdb']->num_queries;
 $k1=$selkey($p1);$k2=$selkey($p2);$rk=$rankkeys($rank);
 echo 'ONE_EXACT '.wp_json_encode(array('name'=>$name,'post_type'=>$ctx['post_type']??'','slot'=>$slot,'p1'=>$k1,'p2'=>$k2,'rank'=>$rk,'queries'=>$q1-$q0),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
 ck187($k1===$e1,'ONE_'.$name.'_p1_exact',$k1);
 ck187($k2===$e1,'ONE_'.$name.'_p2_same_exact',$k2);
 ck187(count($rank)>=1 && count(array_filter($rank,function($x)use($call,$rank){
   $top=(int)($rank[0]['specificity']??0);return $call('banner_distribution_relevance_band',(int)($x['specificity']??0))!==$call('banner_distribution_relevance_band',$top);
 }))===0,'ONE_'.$name.'_rank_contains_only_best_band',wp_json_encode($rk));

 // Multiple exact: rotate only among exact group, never general.
 $make($e2,$slot,$target,'page_tree',2,'exact-b-'.$safe);
 $set(array($e1,$e2,$g1,$g2));
 $p1b=$call('select_campaign_for_slot_position',$ctx,$slot,1);
 $p2b=$call('select_campaign_for_slot_position',$ctx,$slot,2);
 $rankb=$call('ranked_campaigns_for_slot',$ctx,$slot,'');
 $a=$selkey($p1b);$b=$selkey($p2b);$exactSet=array($e1,$e2);
 echo 'MULTI_EXACT '.wp_json_encode(array('name'=>$name,'slot'=>$slot,'p1'=>$a,'p2'=>$b,'rank'=>$rankkeys($rankb)),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
 ck187(in_array($a,$exactSet,true),'MULTI_'.$name.'_p1_exact',$a);
 ck187(in_array($b,$exactSet,true),'MULTI_'.$name.'_p2_exact',$b);
 ck187($a!==$b,'MULTI_'.$name.'_rotates_inside_exact',$a.'|'.$b);

 // General-only: no unrelated automatic banner may be delivered on a topic-bound slot.
 $set(array($g1,$g2));
 $pg=$call('select_campaign_for_slot_position',$ctx,$slot,1);
 $rg=$call('ranked_campaigns_for_slot',$ctx,$slot,'');
 echo 'GENERAL_ONLY '.wp_json_encode(array('name'=>$name,'slot'=>$slot,'p1'=>$selkey($pg),'rank'=>$rankkeys($rg)),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
 ck187($pg===null,'GENERAL_'.$name.'_automatic_slot_empty');
 ck187(count($rg)===0,'GENERAL_'.$name.'_rank_empty');
}

// Pure hierarchy proof on every active production banner slot.
$activeSlots=array(
 'start_after_topics','hub_grid_card','hub_after_cards','product_after_category_tiles','journal_banner',
 'anzeigenmarkt_top_banner','anzeigenmarkt_category_banner','glossary_single_desktop_banner','glossary_single_mobile_banner',
 'breed_single_desktop_banner','breed_single_mobile_banner','post_inline_banner','glossary_overview_banner','breed_overview_banner'
);
foreach($activeSlots as $slot){
 $synthetic=array(
   array('specificity'=>520,'campaign'=>array('id'=>'exact')),
   array('specificity'=>430,'campaign'=>array('id'=>'broad')),
   array('specificity'=>100,'campaign'=>array('id'=>'general')),
   array('specificity'=>5,'campaign'=>array('id'=>'technical'))
 );
 $only=$call('banner_strict_best_relevance_tier_v672187',$synthetic,$slot);
 ck187(count($only)===1 && (string)($only[0]['campaign']['id']??'')==='exact','HIER_'.$slot.'_exact_excludes_all_lower');

 $only=$call('banner_strict_best_relevance_tier_v672187',array_slice($synthetic,1),$slot);
 ck187(count($only)===1 && (string)($only[0]['campaign']['id']??'')==='broad','HIER_'.$slot.'_broad_excludes_general_technical');

 $only=$call('banner_strict_best_relevance_tier_v672187',array_slice($synthetic,2),$slot);
 ck187(count($only)===0,'HIER_'.$slot.'_general_blocked_without_topic');

 $only=$call('banner_strict_best_relevance_tier_v672187',array_slice($synthetic,3),$slot);
 ck187(count($only)===0,'HIER_'.$slot.'_technical_blocked_without_topic');
}

ck187($http===0,'PERFORMANCE_zero_frontend_http','http='.$http);
echo 'SUMMARY187 '.wp_json_encode(array('scenarios'=>count($scenarios),'passes'=>count($GLOBALS['p']),'failures'=>count($GLOBALS['f']),'http'=>$http),JSON_UNESCAPED_SLASHES)."\n";
if($GLOBALS['f']){echo 'FAILURES187 '.wp_json_encode($GLOBALS['f'],JSON_UNESCAPED_SLASHES)."\n";exit(1);}
echo "STRICT_BEST_TIER_ALL_ACTIVE_CONTEXTS_672187_PASS\n";
