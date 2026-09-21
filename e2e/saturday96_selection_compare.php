<?php
if (!defined('ABSPATH')) { exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
function sat96_call($o,$name,...$args){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);}
function sat96_pick96($o,$ctx,$slot){
    $ranked=sat96_call($o,'ranked_campaigns_for_slot',$ctx,$slot,'');
    $index=sat96_call($o,'category_product_slot_index',$slot);
    return $index>0?($ranked[$index-1]??null):($ranked[0]??null);
}
function sat96_pick132($o,$ctx,$slot){
    $ranked=sat96_call($o,'ranked_campaigns_for_slot',$ctx,$slot,'');
    $strict=sat96_call($o,'category_product_strict_relevance_tier_v672104',$ranked,$slot);
    $index=sat96_call($o,'category_product_slot_index',$slot);
    return $index>0?($strict[$index-1]??null):($strict[0]??null);
}
function sat96_pack($o,$sel){
    $c=is_array($sel)&&is_array($sel['campaign']??null)?$sel['campaign']:[];
    return [
      'post_id'=>absint($c['post_id']??0),
      'provider'=>sanitize_key((string)($c['network']??'')),
      'title'=>(string)($c['title']??''),
      'specificity'=>(int)($sel['specificity']??0),
      'matches'=>(int)($sel['matches']??0),
      'surface'=>sanitize_key((string)($c['network']??''))==='idealo' ? sat96_call($o,'idealo_campaign_surface_kind',$c) : '',
    ];
}
$base=get_option('ppar_network_idealo_v1',[]);
$base=is_array($base)?$base:[];
$base['enabled']=1;
$base['output_mode']='automatic';
$ctx0=sat96_call($o,'get_content_context',186);
foreach(['hybrid','products','comparison'] as $strategy){
    $s=$base;$s['link_strategy']=$strategy;update_option('ppar_network_idealo_v1',$s,false);
    $rows=[];
    foreach([1,2,3] as $i){
        $slot='category_product_'.$i;$ctx=$ctx0;$ctx['slot_type']=$slot;
        $old=sat96_pick96($o,$ctx,$slot);
        $cur=sat96_call($o,'select_campaign_for_slot',$ctx,$slot,'');
        $mid=sat96_pick132($o,$ctx,$slot);
        $rows[$slot]=['v67296'=>sat96_pack($o,$old),'v672132'=>sat96_pack($o,$mid),'v672133'=>sat96_pack($o,$cur)];
    }
    echo strtoupper($strategy).'='.wp_json_encode($rows,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
}
update_option('ppar_network_idealo_v1',$base,false);
