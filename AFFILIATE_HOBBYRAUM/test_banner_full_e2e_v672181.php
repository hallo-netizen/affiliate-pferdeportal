<?php
$GLOBALS['e2e_failures']=array(); $GLOBALS['e2e_passes']=array();
function chk($cond,$name,$detail=''){ if($cond){$GLOBALS['e2e_passes'][]=$name; echo "PASS $name".($detail!==''?" :: $detail":"")."\n";}else{$GLOBALS['e2e_failures'][]=$name.($detail!==''?" :: $detail":""); echo "FAIL $name".($detail!==''?" :: $detail":"")."\n";}}
function contains_text($hay,$needle){ return strpos((string)$hay,(string)$needle)!==false; }
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"FATAL plugin class missing\n"); exit(2); }
if (Pferdeportal_Affiliate_Router::VERSION !== '6.72.181') { fwrite(STDERR,"FATAL wrong version ".Pferdeportal_Affiliate_Router::VERSION."\n"); exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
$rm=function($name)use($o){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m;};
$rp=function($name)use($o){$p=new ReflectionProperty($o,$name);$p->setAccessible(true);return $p;};
$call=function($name,...$args)use($rm,$o){return $rm($name)->invokeArgs($o,$args);};
update_option('ppar_enabled','1',false);
update_option('ppar_assignments_v1',array(),false);
delete_option('ppar_debug');

$http_calls=0;
add_filter('pre_http_request',function($pre,$args,$url)use(&$http_calls){$http_calls++; return new WP_Error('e2e_http_block','network blocked in local gate');},10,3);

$mkpost=function($type,$title,$slug,$parent=0){
  $id=wp_insert_post(array('post_type'=>$type,'post_status'=>'publish','post_title'=>$title,'post_name'=>$slug,'post_parent'=>$parent,'post_content'=>'Fixture '.$title),true);
  if(is_wp_error($id)){fwrite(STDERR,"FATAL post $slug ".$id->get_error_message()."\n");exit(2);} return (int)$id;
};
$mkterm=function($tax,$name,$slug,$parent=0){
  $e=get_term_by('slug',$slug,$tax); if($e&&!is_wp_error($e)) return (int)$e->term_id;
  $r=wp_insert_term($name,$tax,array('slug'=>$slug,'parent'=>$parent)); if(is_wp_error($r)){fwrite(STDERR,"FATAL term $slug ".$r->get_error_message()."\n");exit(2);} return (int)$r['term_id'];
};
$parent=$mkpost('page','Ausrüstung E2E','ausruestung-e2e');
$child=$mkpost('page','Schabracken E2E','schabracken-e2e',$parent);
$other=$mkpost('page','Fremd E2E','fremd-e2e');
$nomatch=$mkpost('page','Ohne Treffer E2E','ohne-treffer-e2e');
$catParent=$mkterm('category','Ausrüstung E2E','ausruestung-kat-e2e');
$catChild=$mkterm('category','Schabracken E2E','schabracken-kat-e2e',$catParent);
$catNone=$mkterm('category','Ohne Treffer E2E','ohne-treffer-kat-e2e');
$post=$mkpost('post','Schabracken Beitrag E2E','schabracken-beitrag-e2e');
wp_set_post_categories($post,array($catChild),false);
$ug=$mkterm('uge_group','Ausrüstung Glossar E2E','ausruestung-glossar-e2e');
$uge=$mkpost('uge_term','Trense E2E','trense-e2e'); wp_set_object_terms($uge,array($ug),'uge_group',false);
$bg=$mkterm('pa_breed_group','Warmblut E2E','warmblut-e2e');
$breed1=$mkpost('pa_breed','Rasse Eins E2E','rasse-eins-e2e'); wp_set_object_terms($breed1,array($bg),'pa_breed_group',false);
$breed2=$mkpost('pa_breed','Rasse Zwei E2E','rasse-zwei-e2e'); wp_set_object_terms($breed2,array($bg),'pa_breed_group',false);
$breed3=$mkpost('pa_breed','Rasse Drei E2E','rasse-drei-e2e'); wp_set_object_terms($breed3,array($bg),'pa_breed_group',false);

$save=$rm('save_campaign_record');
$campaign_ids=[];
$make_campaign=function($id,$args=array())use($save,$o,&$campaign_ids){
  $base=array(
    'id'=>$id,'active'=>1,'creative_type'=>'banner','network'=>'manual','programme_status'=>'active',
    'render_mode'=>'image_link','title'=>$id,'description'=>'','button_text'=>'Mehr erfahren',
    'image_url'=>'https://img.example.test/'.$id.'.jpg','url'=>'https://click.example.test/'.$id,
    'target'=>'_blank','placements'=>array('*'),'assignment_mode'=>'fallback','priority'=>10,
    'health_check_enabled'=>false,'dimensions'=>'1200x120','partner'=>'partner-'.$id,
  );
  $c=array_replace($base,$args);
  $pid=$save->invoke($o,$c,0);
  if(is_wp_error($pid)||!$pid){fwrite(STDERR,"FATAL campaign $id\n");exit(2);}
  $campaign_ids[$id]=(int)$pid; return (int)$pid;
};
$set_active_only=function($ids)use(&$campaign_ids,$rp,$o){
  foreach($campaign_ids as $key=>$pid){$d=get_post_meta($pid,'ppar_campaign_data',true);$d=is_array($d)?$d:array();$d['active']=in_array($key,$ids,true)?1:0;update_post_meta($pid,'ppar_campaign_data',$d);}
  $rp('campaigns_request_cache')->setValue($o,null);
  foreach(array('ranked_campaigns_request_cache','ranked_campaign_candidate_index_request_cache','ranked_campaign_raw_records_request_cache','ranked_campaign_from_post_request_cache') as $prop){
    try{$p=$rp($prop);$p->setValue($o,array());}catch(Throwable $e){}
  }
};
$render_post=function($post_id,$slot)use($rm,$o){return (string)$rm('render_affiliate_slot')->invoke($o,$post_id,$slot,'portal_context','');};
$render_context=function($content_id,$context,$slot)use($rm,$o){return (string)$rm('render_affiliate_slot_for_context')->invoke($o,$content_id,$context,$slot,'portal_context','');};
$getctx=function($id)use($rm,$o){return $rm('get_content_context')->invoke($o,$id);};
$getcatctx=function($term_id)use($rm,$o){$t=get_term($term_id,'category');return $rm('get_category_archive_context')->invoke($o,$t);};
$ranked=function($ctx,$slot)use($rm,$o){return $rm('ranked_campaigns_for_slot')->invoke($o,$ctx,$slot,'');};
$ids=function($rows){$o=[];foreach((array)$rows as $r){$o[]=(string)($r['campaign']['id']??'').':'.(int)($r['specificity']??-1);}return $o;};

// --- Core inventory ---
$tech=$make_campaign('tech-wide',array(
  'assignment_mode'=>'page_tree','automation_target_keys'=>array('page:fremd-e2e'),
  'placements'=>array('hub_after_cards'),'dimensions'=>'1200x120','priority'=>5,'partner'=>'p-tech'
));
$invalid=$make_campaign('invalid-wide',array(
  'assignment_mode'=>'page_tree','automation_target_keys'=>array('category:ohne-treffer-kat-e2e'),
  'placements'=>array('hub_after_cards'),'dimensions'=>'400x400','priority'=>999,'partner'=>'p-invalid'
));

// 1. First proven divergence target: canonical slot vs real category alias.
$set_active_only(array('tech-wide','invalid-wide'));
$catNoneCtx=$getcatctx($catNone);
$htmlCanonical=$render_context('term_'.$catNone,$catNoneCtx,'product_after_category_tiles');
$htmlRealAlias=$render_context('term_'.$catNone,$catNoneCtx,'category_recommendation');
chk(trim($htmlCanonical)!=='' && contains_text($htmlCanonical,'tech-wide'),'canonical_category_slot_technical_fallback_visible',substr(strip_tags($htmlCanonical),0,120));
chk(!contains_text($htmlCanonical,'invalid-wide'),'canonical_category_slot_invalid_geometry_blocked');
chk(trim($htmlRealAlias)!=='','REAL_category_recommendation_technical_fallback_visible',substr(strip_tags($htmlRealAlias),0,120));
chk(!contains_text($htmlRealAlias,'invalid-wide'),'REAL_category_recommendation_invalid_geometry_blocked');

// 2. Exact > broad > general > technical on page.
$exactPage=$make_campaign('exact-page',array('assignment_mode'=>'page_tree','automation_target_keys'=>array('page:schabracken-e2e'),'placements'=>array('product_after_category_tiles'),'dimensions'=>'1200x120','priority'=>1,'partner'=>'p1'));
$broadPage=$make_campaign('broad-page',array('assignment_mode'=>'page_tree','automation_target_keys'=>array('page:ausruestung-e2e'),'placements'=>array('product_after_category_tiles'),'dimensions'=>'1200x120','priority'=>900,'partner'=>'p2'));
$general=$make_campaign('general-wide',array('assignment_mode'=>'fallback','placements'=>array('product_after_category_tiles'),'dimensions'=>'1200x120','priority'=>999,'partner'=>'p3'));
$set_active_only(array('tech-wide','invalid-wide','exact-page','broad-page','general-wide'));
$childHtml=$render_post($child,'product_after_category_tiles');
chk(contains_text($childHtml,'exact-page'),'page_exact_beats_broad_general_technical');
chk(!contains_text($childHtml,'broad-page')&&!contains_text($childHtml,'general-wide')&&!contains_text($childHtml,'invalid-wide'),'page_exact_excludes_lower_or_invalid');
$nomatchHtml=$render_post($nomatch,'product_after_category_tiles');
chk(contains_text($nomatchHtml,'general-wide'),'page_general_beats_technical_when_no_topic');
$set_active_only(array('tech-wide','invalid-wide'));
$nomatchTech=$render_post($nomatch,'product_after_category_tiles');
chk(trim($nomatchTech)!=='' && !contains_text($nomatchTech,'invalid-wide'),'page_technical_fallback_visible_without_topic');

// 3. Category exact through the real archive slot.
$exactCat=$make_campaign('exact-category',array('assignment_mode'=>'page_tree','automation_target_keys'=>array('category:schabracken-kat-e2e'),'placements'=>array('product_after_category_tiles'),'dimensions'=>'1200x120','priority'=>1,'partner'=>'pcat'));
$set_active_only(array('exact-category','tech-wide','invalid-wide'));
$catCtx=$getcatctx($catChild);
$catHtml=$render_context('term_'.$catChild,$catCtx,'category_recommendation');
chk(contains_text($catHtml,'exact-category'),'category_real_slot_exact_visible');
chk(!contains_text($catHtml,'invalid-wide'),'category_real_slot_invalid_geometry_blocked');

// 4. Classic post.
$exactPost=$make_campaign('exact-post',array('assignment_mode'=>'page_tree','automation_target_keys'=>array('category:schabracken-kat-e2e'),'placements'=>array('post_inline_banner'),'dimensions'=>'1000x100','priority'=>1,'partner'=>'ppost'));
$badPost=$make_campaign('bad-post-square',array('assignment_mode'=>'page_tree','automation_target_keys'=>array('category:schabracken-kat-e2e'),'placements'=>array('post_inline_banner'),'dimensions'=>'400x400','priority'=>999,'partner'=>'pbadpost'));
$generalPost=$make_campaign('general-post',array('assignment_mode'=>'fallback','placements'=>array('post_inline_banner'),'dimensions'=>'1000x100','priority'=>999,'partner'=>'pgpost'));
$set_active_only(array('exact-post','bad-post-square','general-post'));
$postHtml=$render_post($post,'post_inline_banner');
$postRank=$ranked($getctx($post),'post_inline_banner');
echo "TRACE post_candidates=".json_encode($ids($postRank) ?? array())."\n";
echo "TRACE post_html=".substr(preg_replace('/\s+/',' ',strip_tags($postHtml)),0,220)."\n";
chk(contains_text($postHtml,'exact-post'),'post_exact_visible');
chk(!contains_text($postHtml,'bad-post-square'),'post_invalid_geometry_blocked');

// 5. Glossary single.
$exactGloss=$make_campaign('exact-glossary',array('assignment_mode'=>'page_tree','automation_target_keys'=>array('uge_term:trense-e2e'),'placements'=>array('glossary_single_desktop_banner'),'dimensions'=>'400x400','priority'=>1,'partner'=>'pgloss'));
$generalGloss=$make_campaign('general-glossary',array('assignment_mode'=>'fallback','placements'=>array('glossary_single_desktop_banner'),'dimensions'=>'400x400','priority'=>999,'partner'=>'pggloss'));
$set_active_only(array('exact-glossary','general-glossary'));
$glossHtml=$render_post($uge,'glossary_single_desktop_banner');
chk(contains_text($glossHtml,'exact-glossary'),'glossary_exact_visible');

// 6. Breeds: topic neutral, stable distribution, visible.
$breedA=$make_campaign('breed-a',array('assignment_mode'=>'page_tree','automation_target_keys'=>array('pa_breed:other-breed'),'placements'=>array('breed_single_desktop_banner'),'dimensions'=>'400x400','priority'=>999,'partner'=>'breed-partner-a'));
$breedB=$make_campaign('breed-b',array('assignment_mode'=>'fallback','placements'=>array('breed_single_desktop_banner'),'dimensions'=>'400x400','priority'=>1,'partner'=>'breed-partner-b'));
$set_active_only(array('breed-a','breed-b'));
$breedCtx1=$getctx($breed1); $breedCtx2=$getctx($breed2); $breedCtx3=$getctx($breed3);
$selBreed1=$rm('select_campaign_for_slot')->invoke($o,$breedCtx1,'breed_single_desktop_banner','');
$selBreed2=$rm('select_campaign_for_slot')->invoke($o,$breedCtx2,'breed_single_desktop_banner','');
$selBreed3=$rm('select_campaign_for_slot')->invoke($o,$breedCtx3,'breed_single_desktop_banner','');
echo "TRACE breed_selected=".json_encode(array(
  (string)($selBreed1['campaign']['id']??''),
  (string)($selBreed2['campaign']['id']??''),
  (string)($selBreed3['campaign']['id']??'')
))."\n";
foreach(array(1=>$selBreed1,2=>$selBreed2,3=>$selBreed3) as $n=>$sel){
  $camp=is_array($sel['campaign']??null)?$sel['campaign']:array();
  $gb=$rm('campaign_to_group_banner')->invoke($o,$camp);
  echo "TRACE breed_group_banner_".$n."=".json_encode(array(
    'campaign'=>(string)($camp['id']??''),
    'group'=>(string)($gb[0]['id']??''),
    'banner'=>(string)($gb[1]['id']??''),
    'url'=>(string)($gb[1]['url']??'')
  ))."\n";
}
$breedHtml1=$render_post($breed1,'breed_single_desktop_banner');
$breedHtml2=$render_post($breed2,'breed_single_desktop_banner');
$breedHtml3=$render_post($breed3,'breed_single_desktop_banner');
foreach(array(1=>$breedHtml1,2=>$breedHtml2,3=>$breedHtml3) as $n=>$h){
  preg_match('/href="([^"]+)"/',$h,$m);
  echo "TRACE breed_html_href_".$n."=".($m[1]??'')."\n";
}
echo "TRACE breed1_candidates=".json_encode($ids($ranked($getctx($breed1),'breed_single_desktop_banner')) ?? array())."\n";
echo "TRACE breed2_candidates=".json_encode($ids($ranked($getctx($breed2),'breed_single_desktop_banner')) ?? array())."\n";
echo "TRACE breed3_candidates=".json_encode($ids($ranked($getctx($breed3),'breed_single_desktop_banner')) ?? array())."\n";
chk(trim($breedHtml1)!==''&&trim($breedHtml2)!==''&&trim($breedHtml3)!=='','breed_all_visible');
$breedUrls=array();
foreach(array($breedHtml1,$breedHtml2,$breedHtml3) as $h){
  if(contains_text($h,'https://click.example.test/breed-a'))$breedUrls[]='a';
  elseif(contains_text($h,'https://click.example.test/breed-b'))$breedUrls[]='b';
  else $breedUrls[]='?';
}
chk(count(array_unique($breedUrls))>=2,'breed_stable_distribution_uses_multiple_banners',implode(',',$breedUrls));

// 7. Manual override precedence and NONE.
$set_active_only(array('exact-page','general-wide'));
update_option('ppar_assignments_v1',array($child=>array('banner_mode'=>'fixed','banner_id'=>$campaign_ids['general-wide'],'products_mode'=>'automatic','product_ids'=>array(),'apply_descendants'=>false,'repair_reason'=>'E2E fixed')),false);
$fixedHtml=$render_post($child,'product_after_category_tiles');
chk(contains_text($fixedHtml,'general-wide'),'manual_fixed_assignment_overrides_automatic_exact');
update_option('ppar_assignments_v1',array($child=>array('banner_mode'=>'none','banner_id'=>0,'products_mode'=>'automatic','product_ids'=>array(),'apply_descendants'=>false,'repair_reason'=>'E2E none')),false);
$noneHtml=$render_post($child,'product_after_category_tiles');
chk(trim(strip_tags($noneHtml))==='' || contains_text($noneHtml,'affiliate_assignment_disabled'),'manual_none_suppresses_banner');
update_option('ppar_assignments_v1',array(),false);

// 8. Banner never fills product slot.
$set_active_only(array('exact-page','general-wide','tech-wide'));
$productHtml=$render_post($child,'category_product_1');
chk(trim($productHtml)==='' || !contains_text($productHtml,'ppar-affiliate-slot'),'banner_does_not_fill_product_slot');

// 9. Full ranked candidate proof for real category slot.
$set_active_only(array('tech-wide','invalid-wide'));
$rankReal=$ranked($catNoneCtx,'category_recommendation');
$rankCanonical=$ranked($catNoneCtx,'product_after_category_tiles');
echo "TRACE canonical_candidates=".json_encode($ids($rankCanonical))."\n";
echo "TRACE real_alias_candidates=".json_encode($ids($rankReal))."\n";
chk(count($rankCanonical)>0,'canonical_candidate_pool_nonempty');
chk(count($rankReal)>0,'REAL_alias_candidate_pool_nonempty');

// 10. No outbound provider/network calls in the complete render gate.
chk($http_calls===0,'no_remote_http_calls_during_render','http_calls='.$http_calls);

echo "SUMMARY passes=".count($GLOBALS['e2e_passes'])." failures=".count($GLOBALS['e2e_failures'])."\n";
if($GLOBALS['e2e_failures']){echo "FAILURES ".json_encode($GLOBALS['e2e_failures'],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";exit(1);}
echo "FULL_WORDPRESS_MARIADB_BANNER_E2E_PASS\n";
