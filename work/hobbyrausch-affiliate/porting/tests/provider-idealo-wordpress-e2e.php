<?php
if (!defined('ABSPATH')) { fwrite(STDERR,"WP_NOT_LOADED\n"); exit(1); }
function hd_e2e_fail($m){ fwrite(STDERR,"FAIL: $m\n"); exit(1); }
function hd_e2e_pass($m){ echo "PASS: $m\n"; }

$page_id=wp_insert_post([
  'post_type'=>'page','post_status'=>'publish','post_title'=>'Stricken','post_name'=>'stricken','post_content'=>'Stricken lernen'
],true);
if(is_wp_error($page_id)||!$page_id){ hd_e2e_fail('cannot create Stricken page'); }
$term=wp_insert_term('Stricken für Anfänger','category',['slug'=>'stricken-anfaenger']);
if(is_wp_error($term)){ hd_e2e_fail('cannot create Stricken category: '.$term->get_error_message()); }
$term_id=(int)$term['term_id'];

$GLOBALS['hd_e2e_registry']=[
 'contract'=>'HD004_E2E','revision'=>'e2e-1',
 'nodes'=>[
   ['node_id'=>'core:world:gestalten','parent_id'=>'','display_name'=>'Gestalten','slug'=>'gestalten','status'=>'active','object_type'=>'page'],
   ['node_id'=>'core:hub:handarbeit','parent_id'=>'core:world:gestalten','display_name'=>'Handarbeit','slug'=>'handarbeit','status'=>'active','object_type'=>'page'],
   ['node_id'=>'core:entity:stricken','parent_id'=>'core:hub:handarbeit','display_name'=>'Stricken','slug'=>'stricken','status'=>'active','object_type'=>'page'],
   ['node_id'=>'core:leaf:stricken-anfaenger','parent_id'=>'core:entity:stricken','display_name'=>'Stricken für Anfänger','slug'=>'stricken-anfaenger','status'=>'active','object_type'=>'category'],
 ],
 'mapping'=>[
   'core:entity:stricken'=>['object_id'=>(int)$page_id,'object_type'=>'page'],
   'core:leaf:stricken-anfaenger'=>['object_id'=>$term_id,'object_type'=>'category'],
 ],
];
function hd_category_registry_ready(){ return true; }
function hd_category_registry_snapshot(){ return $GLOBALS['hd_e2e_registry']; }

update_option('ppar_enabled','1',false);
update_option('ppar_disclosure','Werbelink: Test',false);
update_option('ppar_network_idealo_v1',[
 'enabled'=>true,
 'api_key'=>'synthetic-e2e-key',
 'adspace_id'=>'123',
 'feed_id'=>'456',
 'output_mode'=>'separate',
 'link_strategy'=>'products',
 'auto_refresh'=>false,
],false);

$plugin=Hobby_Depot_Affiliate_Router::instance();
$ref=new ReflectionClass($plugin);
$import=$ref->getMethod('idealo_import_feed_file'); $import->setAccessible(true);

$tmp=wp_tempnam('hd-idealo-e2e.csv');
$fh=fopen($tmp,'wb');
$headers=['id','product_title','product_deeplink','ean','gtins_product','asins_product','main_category','sub_category','brand_name','image_url','price'];
fputcsv($fh,$headers);
fputcsv($fh,[
 'prod-1','Stricken Starter Set Wolle Nadeln',
 'https://ipn.idealo.de/test?pid=prod-1&trg=https%3A%2F%2Fwww.idealo.de%2Fpreisvergleich%2FOffersOfProduct%2F123.html',
 '4006381333931','4006381333931','','Gestalten','Handarbeit','Testmarke',
 'https://cdn.idealo.com/folder/e2e-product.jpg','29.99'
]);
fputcsv($fh,[
 'prod-bad','Autoreifen Sommer 205 55 R16',
 'https://ipn.idealo.de/test?pid=prod-bad&trg=https%3A%2F%2Fwww.idealo.de%2Fpreisvergleich%2FOffersOfProduct%2F999.html',
 '5012345678900','5012345678900','','Auto','Reifen','Fremdmarke',
 'https://cdn.idealo.com/folder/e2e-bad.jpg','79.99'
]);
fclose($fh);

$result=$import->invoke($plugin,$tmp,'Hobby Depot E2E');
@unlink($tmp);
if(is_wp_error($result)){ hd_e2e_fail('idealo import: '.$result->get_error_code().' '.$result->get_error_message()); }
if(($result['status']??'')!=='success'){ hd_e2e_fail('idealo import status not success'); }
if((int)($result['details']['matching_rows']??0)!==1){ hd_e2e_fail('expected exactly one matching feed row'); }
hd_e2e_pass('idealo feed positive + negative HD-004 matching');

$ids=get_posts([
 'post_type'=>'ap_campaign','post_status'=>'publish','posts_per_page'=>50,'fields'=>'ids',
 'meta_query'=>[['key'=>'_ppar_idealo_external_key','compare'=>'EXISTS']]
]);
if(!$ids){ hd_e2e_fail('idealo materializer created no campaigns'); }

$product_campaign_id=0;
foreach($ids as $id){
 $data=get_post_meta($id,'ppar_campaign_data',true);
 if(is_array($data) && ($data['source']??'')==='idealo_product_feed_v1' && in_array('4006381333931',(array)($data['product_gtins']??[]),true)){
   $product_campaign_id=(int)$id; break;
 }
}
if(!$product_campaign_id){ hd_e2e_fail('no concrete idealo product campaign found'); }
hd_e2e_pass('idealo import materialized concrete campaign');

$fromPost=$ref->getMethod('campaign_from_post'); $fromPost->setAccessible(true);
$campaign=$fromPost->invoke($plugin,get_post($product_campaign_id));
if(!is_array($campaign)||($campaign['network']??'')!=='idealo'){ hd_e2e_fail('materialized campaign readback invalid'); }

$build=$ref->getMethod('build_campaign_output'); $build->setAccessible(true);
$context=[
 'post_id'=>(int)$page_id,
 'post_type'=>'page',
 'primary_slug'=>'stricken',
 'primary_name'=>'Stricken',
 'slugs'=>['stricken','stricken-anfaenger','handarbeit','gestalten'],
 'haystack'=>'stricken stricken für anfänger handarbeit gestalten',
 'term_ids'=>[$term_id],
 'ancestor_ids'=>[],
];
$out=$build->invoke($plugin,$campaign,(int)$page_id,$context,'category_product_1',false);
if(!is_array($out)||empty($out['valid'])){ hd_e2e_fail('campaign output builder rejected materialized idealo product'); }
if(strpos((string)($out['destination']??''),'ipn.idealo.de')===false){ hd_e2e_fail('idealo destination missing in campaign output'); }
hd_e2e_pass('materialized campaign builds real product output');

$renderBanner=$ref->getMethod('campaign_to_group_banner'); $renderBanner->setAccessible(true);
$gb=$renderBanner->invoke($plugin,$campaign);
if(!is_array($gb)||count($gb)<2||!is_array($gb[1])){ hd_e2e_fail('campaign to banner conversion failed'); }
$rb=$ref->getMethod('render_banner'); $rb->setAccessible(true);
$html=$rb->invoke($plugin,$gb[1],(int)$page_id,$context,$gb[0],'category_product_1');
if(strpos($html,'Bei idealo vergleichen')===false){ hd_e2e_fail('provider-specific idealo CTA missing'); }
if(strpos($html,'Stricken Starter Set')===false){ hd_e2e_fail('product title missing from rendered HTML'); }
if(preg_match('/Pferdeatelier|Pferde-Atelier|Reithelm|Satteldeck/i',$html)){ hd_e2e_fail('horse-domain marker leaked into rendered HTML'); }
hd_e2e_pass('campaign renders provider CTA + product HTML without horse markers');

$slot=$ref->getMethod('render_affiliate_slot_for_context'); $slot->setAccessible(true);
$slot_html=$slot->invoke($plugin,(int)$page_id,$context,'category_product_1','primary_product','');
if(strpos($slot_html,'ppar-slot-category_product_1')===false){ hd_e2e_fail('full slot renderer did not emit category product slot'); }
if(strpos($slot_html,'Bei idealo vergleichen')===false){ hd_e2e_fail('full slot renderer missing idealo CTA'); }
if(strpos($slot_html,'Stricken Starter Set')===false){ hd_e2e_fail('full slot renderer missing product title'); }
hd_e2e_pass('full campaign selection -> slot -> HTML readback');

$bad=get_posts([
 'post_type'=>'ap_campaign','post_status'=>'publish','posts_per_page'=>50,'fields'=>'ids',
 'meta_query'=>[['key'=>'ppar_campaign_data','value'=>'Autoreifen','compare'=>'LIKE']]
]);
if($bad){ hd_e2e_fail('negative feed row leaked into campaign materialization'); }
hd_e2e_pass('unmatched product remained fail-closed');

echo "IDEALO_PROVIDER_TO_FRONTEND_E2E=PASS\n";
