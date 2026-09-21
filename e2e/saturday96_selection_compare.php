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

function sat96_apply_candidate_fix($o,$ranked,$slot,$strategy){
    $strict=sat96_call($o,'category_product_strict_relevance_tier_v672104',$ranked,$slot);
    if (!preg_match('/^category_product_[123]$/',sanitize_key((string)$slot)) || !in_array($strategy,['hybrid','comparison'],true)) {
        return $strict;
    }
    $seen=[];
    foreach($strict as $candidate){
        $c=is_array($candidate['campaign']??null)?$candidate['campaign']:[];
        $k=absint($c['post_id']??0);
        if($k>0)$seen[$k]=1;
    }
    foreach($ranked as $candidate){
        $c=is_array($candidate['campaign']??null)?$candidate['campaign']:[];
        if(sanitize_key((string)($c['network']??''))!=='idealo')continue;
        if(sat96_call($o,'idealo_campaign_surface_kind',$c)!=='comparison')continue;
        $k=absint($c['post_id']??0);
        if($k>0 && isset($seen[$k]))continue;
        $strict[]=$candidate;
        if($k>0)$seen[$k]=1;
    }
    return array_values($strict);
}
function sat96_pickfix($o,$ctx,$slot,$strategy){
    $ranked=sat96_call($o,'ranked_campaigns_for_slot',$ctx,$slot,'');
    $fixed=sat96_apply_candidate_fix($o,$ranked,$slot,$strategy);
    $fixed=sat96_call($o,'category_product_provider_mix_v672133',$fixed,$slot);
    $index=sat96_call($o,'category_product_slot_index',$slot);
    return $index>0?($fixed[$index-1]??null):($fixed[0]??null);
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
        $fix=sat96_pickfix($o,$ctx,$slot,$strategy);
        $rows[$slot]=['v67296'=>sat96_pack($o,$old),'v672132'=>sat96_pack($o,$mid),'v672133'=>sat96_pack($o,$cur),'candidate_fix'=>sat96_pack($o,$fix)];
    }
    echo strtoupper($strategy).'='.wp_json_encode($rows,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
}
update_option('ppar_network_idealo_v1',$base,false);

$synthetic=[
 ['specificity'=>520,'matches'=>1,'campaign'=>['post_id'=>9001,'network'=>'idealo','idealo_surface_kind'=>'comparison']],
 ['specificity'=>430,'matches'=>2,'campaign'=>['post_id'=>9002,'network'=>'ebay']],
 ['specificity'=>430,'matches'=>2,'campaign'=>['post_id'=>9003,'network'=>'idealo','idealo_surface_kind'=>'comparison']],
];
$neg=sat96_apply_candidate_fix($o,$synthetic,'category_product_2','hybrid');
$ids=array_map(static function($x){return absint($x['campaign']['post_id']??0);},$neg);
echo 'NEGATIVE_FIX_IDS='.wp_json_encode($ids)."\n";
if(in_array(9002,$ids,true)) { fwrite(STDERR,"NEGATIVE_FAIL_WEAKER_NON_IDEALO_REINTRODUCED\n"); exit(9); }
if(!in_array(9003,$ids,true)) { fwrite(STDERR,"POSITIVE_FAIL_IDEALO_COMPARISON_NOT_RESTORED\n"); exit(10); }
echo "CANDIDATE_FIX_NEGATIVE_PASS\n";
