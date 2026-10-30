<?php
/* Strict WordPress+real MySQL acceptance for isolated disposable HD009 installation. */
if (!defined('WP_CLI') || !WP_CLI || !defined('HD009_DISPOSABLE_WORDPRESS_TEST')
    || HD009_DISPOSABLE_WORDPRESS_TEST !== true || !defined('DB_NAME') || DB_NAME !== 'hd009_test') {
    throw new RuntimeException('Refuse any non-disposable WordPress/database');
}
function hd009_gate($ok,$message){if(!$ok){throw new RuntimeException('FAIL '.$message);}echo "PASS ".$message."\n";}
wp_set_current_user(1);
hd009_gate(class_exists('Hobby_Depot_Affiliate_Router') && class_exists('HD009_CI_Design_Fixture'),'real HD009 plugin and synthetic design present');
$app=Hobby_Depot_Affiliate_Router::instance();
$cat=HDAR_Hobby_Depot_Source::catalog();
hd009_gate(!is_wp_error($cat) && count((array)($cat['business_concepts']??[]))===320
    && (int)($cat['business_supply_contract']['required_count']??0)===320,'320 obligatory Hobby Depot targets');
$norm=$app->ebay_normalize_settings(['private_enabled'=>true,'business_enabled'=>true],true);
hd009_gate(empty($norm['private_enabled'])&&!empty($norm['business_enabled']),'stored PRIVATE=true cannot be activated');
$portals=$app->output_portal_registry();$local=reset($portals);
hd009_gate(is_array($local)&&!empty($local['key']),'local Hobby Depot output portal found');
$concepts=(array)$cat['business_concepts'];
$first=(array)reset($concepts);
$sample=[
 'provider'=>'ebay','partner_external_id'=>'seller-ci-test','creative_type'=>'product','source_kind'=>'ebay_business_item',
 'identity_hash'=>hash('sha256','hd009-preflight'),'tracking_url'=>'https://www.ebay.de/itm/200001?campid=1234567890',
 'title'=>(string)$first['title'],'source_status'=>'active'
];
$no_credentials=$app->control_partner_gate($sample,$local);
hd009_gate(is_wp_error($no_credentials) && $no_credentials->get_error_code()==='control_provider_credentials_missing','missing eBay credentials block publication for the correct reason');
update_option('ppar_network_ebay_v1',[
 'enabled'=>true,'business_enabled'=>true,'private_enabled'=>true,
 'client_id'=>'HD009_CI_NONPRODUCTION','client_secret'=>'HD009_CI_NO_REAL_SECRET',
 'epn_campaign_id'=>'1234567890','environment'=>'production'],false);
update_option('ppar_enabled','1',false);
$yes_credentials=$app->control_partner_gate($sample,$local);
hd009_gate(!is_wp_error($yes_credentials),'synthetic configured credentials permit isolated output');
$raw=[
 'itemId'=>'v1|200001|0','title'=>'Hobby 1-1 Original Werkzeug Komplettset',
 'listingMarketplaceId'=>'EBAY_DE',
 'itemAffiliateWebUrl'=>'https://www.ebay.de/itm/200001?mkevt=1&mkcid=1&campid=1234567890&toolid=10001',
 'itemWebUrl'=>'https://www.ebay.de/itm/200001',
 'image'=>['imageUrl'=>'https://i.ebayimg.com/images/g/test.jpg'],
 'price'=>['value'=>'39.99','currency'=>'EUR'],
 'seller'=>['sellerAccountType'=>'BUSINESS','username'=>'hd009-ci-seller','feedbackPercentage'=>99.9,'feedbackScore'=>10000],
 'buyingOptions'=>['FIXED_PRICE'],'itemLocation'=>['country'=>'DE'],
 'returnTerms'=>['returnsAccepted'=>true]
];
$settings=$app->ebay_normalize_settings(['enabled'=>true,'business_enabled'=>true,'epn_campaign_id'=>'1234567890'],true);
hd009_gate(!is_wp_error($app->ebay_accept_item($raw,'BUSINESS',$settings)),'original code accepts own EPN link');
$plain=$raw;$plain['itemAffiliateWebUrl']=$raw['itemWebUrl'];
hd009_gate(is_wp_error($app->ebay_accept_item($plain,'BUSINESS',$settings)),'original code rejects untracked eBay link');
$foreign=$raw;$foreign['itemAffiliateWebUrl']='https://www.ebay.de/itm/200001?campid=9876543210';
hd009_gate(is_wp_error($app->ebay_accept_item($foreign,'BUSINESS',$settings)),'original code rejects foreign EPN campaign');
$creatives=[];$first_page_id=0;$seen=[];
foreach($concepts as $n=>$concept){
 $target=(array)($concept['target_pages'][0]??[]);
 $slug=sanitize_title((string)($target['slug']??''));
 hd009_gate($slug!==''&&!isset($seen[$slug]),'unique hobby '.$slug);
 $seen[$slug]=true;
 $page_id=wp_insert_post(['post_type'=>'page','post_title'=>(string)$concept['title'],
  'post_name'=>$slug,'post_status'=>'publish',
  'post_content'=>'HD009 local test [pp_affiliate_slot type="category_product_1" intent="portal_context"]'],true);
 if(is_wp_error($page_id) || !$page_id){throw new RuntimeException('Real WP page insert failure '.$slug);}
 if(!$first_page_id){$first_page_id=(int)$page_id;}
 $idx=count($seen);$id=200000+$idx;
 $url='https://www.ebay.de/itm/'.$id.'?mkevt=1&mkcid=1&campid=1234567890&toolid=10001';
 $title=(string)$concept['title'].' Original Werkzeug Komplettset';
 $payload=[
  'ebay_seller_account_type'=>'BUSINESS','ebay_seller_username'=>'seller-'.$idx,
  'ebay_item_id'=>'v1|'.$id.'|0','ebay_item_end_at'=>0,'ebay_buying_options'=>['FIXED_PRICE'],
  'ebay_rule_id'=>(string)$concept['id'],'ebay_verified_product_slug'=>$slug,
  'ebay_verified_product_concept'=>(string)$concept['id'],'ebay_verified_concept_kind'=>'product',
  'ebay_verified_product_targets'=>[$slug],
  'ebay_verified_path'=>(string)($target['main_hub']??'Welt').' > '.(string)$concept['title'],
  'ebay_verified_score'=>100,'ebay_evidence_hash'=>hash('sha256',$title),
  'ebay_business_match_contract'=>'concept_v3',
  'ebay_quality_score'=>97,'ebay_quality_relevance'=>100,'ebay_quality_seller'=>100,
  'ebay_quality_offer'=>80,'ebay_quality_price'=>100,
  'ebay_seller_feedback_percentage'=>99.9,'ebay_seller_feedback_score'=>10000,
  'product_gtins'=>[],'price'=>'39.99','currency'=>'EUR','availability'=>'available',
  '_dimension_state'=>'pending','_declared_width'=>0,'_declared_height'=>0
 ];
 $creatives[]=[
  'provider'=>'ebay','partner_external_id'=>'seller-'.$idx,'partner_name'=>'eBay: seller-'.$idx,
  'external_id'=>'v1-'.$id.'-0','identity_hash'=>hash('sha256','hd009-ci-'.$slug),
  'creative_type'=>'product','title'=>$title,'description'=>'39.99 EUR',
  'tags'=>'eBay, '.$concept['title'],'image_url'=>'https://i.ebayimg.com/images/g/test.jpg',
  'destination_url'=>$url,'tracking_url'=>$url,'width'=>0,'height'=>0,
  'source_status'=>'active','source_kind'=>'ebay_business_item','availability_state'=>'active',
  'missing_count'=>0,'last_complete_run'=>'hd009-ci',
  'review_status'=>'review','selected'=>0,'content_scope'=>'unclassified',
  'scope_source'=>'','classified_at'=>0,'topic_status'=>'format_pending',
  'topic_score'=>0,'topic_targets'=>'[]','source_hash'=>hash('sha256',$slug.'-source'),
  'payload'=>wp_json_encode($payload)
 ];
}
hd009_gate(count($creatives)===320 && count($seen)===320,'320 actual WP pages inserted');
$app->maybe_install_output_objects_schema();
global $wpdb;
$table=$wpdb->base_prefix.'ppar_output_objects';
hd009_gate($wpdb->get_var($wpdb->prepare('SHOW TABLES LIKE %s',$table))===$table,'real MySQL output table exists');
$count=0;
foreach($creatives as $creative){
 $r=$app->output_plan_creative($creative,true);
 if(empty($r['active']) || !empty($r['blocked'])) {
  throw new RuntimeException('Output failure '.($count+1).' '.json_encode($r,JSON_UNESCAPED_UNICODE));
 }
 $count++;
}
hd009_gate($count===320,'320 original output_plan_creative calls active');
$objects=$wpdb->get_results("SELECT provider, status, output_type, campaign_post_id FROM ".$table,ARRAY_A);
hd009_gate(count($objects)===320,'320 actual MySQL output objects');
$campaigns=[];
foreach($objects as $o){
 hd009_gate($o['status']==='published' && $o['provider']==='ebay' && $o['output_type']==='product_campaign','persisted published eBay campaign');
 $id=(int)$o['campaign_post_id'];
 $campaign=get_post_meta($id,'ppar_campaign_data',true);
 hd009_gate($id>0 && get_post_status($id)==='publish'
  && is_array($campaign)&&!empty($campaign['active'])&&($campaign['network']??'')==='ebay'
  && !empty($campaign['automation_target_keys']),'campaign WP post/meta readback');
 hd009_gate(str_contains((string)($campaign['url']??''),'campid=1234567890'),'commissionable link stored');
 $campaigns[$id]=1;
}
hd009_gate(count($campaigns)===320,'320 distinct campaign posts');
global $post;
$post=get_post($first_page_id);setup_postdata($post);
$html=apply_filters('the_content',(string)$post->post_content);
wp_reset_postdata();
hd009_gate(str_contains($html,'campid=1234567890'),'WordPress shortcode renders tracked product URL');
$bad=$creatives[0];$bad['identity_hash']=hash('sha256','hd009-negative-new-target');
$payload=json_decode($bad['payload'],true);
$payload['ebay_verified_product_slug']='unknown-hobby-999';
$bad['payload']=wp_json_encode($payload);
$neg=$app->output_plan_creative($bad,true);
hd009_gate(empty($neg['active']),'unknown hobby cannot publish');
$still=(int)$wpdb->get_var("SELECT COUNT(*) FROM ".$table." WHERE provider='ebay' AND status='published' AND output_type='product_campaign'");
hd009_gate($still===320,'negative case has not changed published count');
$private=(int)$wpdb->get_var("SELECT COUNT(*) FROM ".$table." WHERE output_type='hivepress_listing' AND status='published'");
hd009_gate($private===0,'no PRIVATE/HivePress output');
echo "HD009_REAL_WP_MYSQL_ACCEPTANCE_PASS\n";
