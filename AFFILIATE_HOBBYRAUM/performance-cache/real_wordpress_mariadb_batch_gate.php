<?php
if (!defined('ABSPATH')) { exit; }

add_action('template_redirect', static function () {
    if ((string)($_GET['ppar_perf_batch_gate'] ?? '') !== '1') { return; }
    header('Content-Type: text/plain; charset=utf-8');
    @set_time_limit(300);
    global $wpdb;

    $fail=static function(string $m):void{status_header(500);echo "FAIL {$m}\n";exit;};
    $pass=static function(string $m):void{echo "PASS {$m}\n";};
    $assert=static function($c,string $m)use($fail,$pass):void{if(!$c)$fail($m);$pass($m);};

    if(!class_exists('Pferdeportal_Affiliate_Router')) $fail('affiliate plugin class missing');
    $o=Pferdeportal_Affiliate_Router::instance();
    $o->maybe_install_control_contract_schema();
    $o->maybe_install_ebay_schema();
    $o->maybe_install_creative_library_schema();

    $portal='pferde-atelier'; $now=time();
    $control=$wpdb->base_prefix.'ppar_control_decisions';
    $ebay=$wpdb->prefix.'ppar_ebay_items';
    $creative=$wpdb->base_prefix.'ppar_creative_library';

    // 315 distinct control keys, matching the live residual Heuwaagen count.
    for($i=0;$i<315;$i++){
        $scope_key='ci-control-'.$i;
        $key=hash('sha256',sanitize_key($portal).'|creative|'.$scope_key);
        $wpdb->insert($control,array(
            'decision_key'=>$key,'portal_key'=>$portal,'scope_type'=>'creative','scope_key'=>$scope_key,
            'status'=>($i===7?'veto':'approved'),'reason'=>'CI fixture','payload'=>'{}','user_id'=>0,
            'created_at'=>$now,'updated_at'=>$now,
        ));
    }
    $before=(int)$wpdb->num_queries; $r=null;
    for($i=0;$i<315;$i++){ $r=$o->control_get_decision($portal,'creative','ci-control-'.$i); if($i===7)$assert(($r['status']??'')==='veto','control batch preserves veto'); }
    $delta=(int)$wpdb->num_queries-$before;
    $assert($delta===1,'315 distinct control reads collapse to exactly 1 portal query');

    $before=(int)$wpdb->num_queries;
    for($i=0;$i<100;$i++) $o->control_get_decision($portal,'creative','ci-missing-'.$i);
    $delta=(int)$wpdb->num_queries-$before;
    $assert($delta===0,'100 missing control keys add zero queries after portal preload');

    $write=$o->control_set_decision($portal,'creative','ci-control-0','veto','CI changed');
    $assert(!is_wp_error($write),'control write succeeds');
    $before=(int)$wpdb->num_queries;
    $fresh=$o->control_get_decision($portal,'creative','ci-control-0');
    $delta=(int)$wpdb->num_queries-$before;
    $assert($delta===1 && ($fresh['status']??'')==='veto','control write invalidates batch and reloads fresh veto');

    // Synthetic immutable campaign snapshot; no need to render 792 posts.
    $campaigns=array(); $post_ids=array();
    for($i=0;$i<792;$i++){
        $post_id=100000+$i; $hash=hash('sha256','ci-campaign-'.$i); $post_ids[]=$post_id;
        $campaigns[]=array('network'=>'ebay','post_id'=>$post_id,'creative_type'=>'product','active'=>true);
        $wpdb->insert($wpdb->postmeta,array('post_id'=>$post_id,'meta_key'=>'_ppar_ebay_business_auto','meta_value'=>'1'));
        $wpdb->insert($wpdb->postmeta,array('post_id'=>$post_id,'meta_key'=>'_ppar_creative_identity_hash','meta_value'=>$hash));
        $wpdb->insert($ebay,array(
            'portal_key'=>$portal,'item_id'=>'ci-'.$i,'seller_account_type'=>'BUSINESS','route_mode'=>'product','rule_id'=>'ci',
            'creative_identity_hash'=>$hash,'title'=>'CI '.$i,'condition_text'=>'New','location_text'=>'DE',
            'affiliate_url'=>'https://example.test/a','item_web_url'=>'https://example.test/a','image_url'=>'https://example.test/a.jpg',
            'source_hash'=>hash('sha256','source-'.$i),'rejection_reason'=>'','source_state'=>'available','policy_state'=>'allowed',
            'route_state'=>'ready','output_state'=>'candidate','last_seen'=>$now,'fresh_until'=>$now+3600,'created_at'=>$now,'updated_at'=>$now
        ));
        if($i<87){
            $wpdb->insert($creative,array(
                'provider'=>'awin','partner_external_id'=>'ci','partner_name'=>'CI','external_id'=>'creative-'.$i,
                'identity_hash'=>$hash,'creative_type'=>'banner','title'=>'Creative '.$i,'tags'=>'horse',
                'image_url'=>'https://example.test/c.jpg','destination_url'=>'https://example.test/horse',
                'tracking_url'=>'https://example.test/track','source_hash'=>hash('sha256','creative-'.$i),
                'first_seen'=>$now,'last_seen'=>$now
            ));
        }
    }
    update_meta_cache('post',$post_ids);

    $rp=new ReflectionProperty($o,'campaigns_request_cache'); $rp->setAccessible(true); $rp->setValue($o,$campaigns);
    $rmE=new ReflectionMethod($o,'ebay_business_campaign_source_row'); $rmE->setAccessible(true);
    $before=(int)$wpdb->num_queries; $last=array();
    for($i=0;$i<792;$i++) $last=$rmE->invoke($o,$campaigns[$i]);
    $delta=(int)$wpdb->num_queries-$before;
    $assert($delta===1,'792 distinct eBay BUSINESS hashes collapse to exactly 1 IN query');
    $assert(is_array($last)&&($last['item_id']??'')==='ci-791'&&($last['seller_account_type']??'')==='BUSINESS','eBay batch preserves exact latest BUSINESS row');

    $rmC=new ReflectionMethod($o,'output_creative_row'); $rmC->setAccessible(true);
    $before=(int)$wpdb->num_queries; $lastCreative=null;
    for($i=0;$i<87;$i++) $lastCreative=$rmC->invoke($o,hash('sha256','ci-campaign-'.$i));
    $delta=(int)$wpdb->num_queries-$before;
    $assert($delta===1,'87 distinct creative hashes collapse to exactly 1 IN query');
    $assert(is_array($lastCreative)&&($lastCreative['title']??'')==='Creative 86','creative batch preserves exact identity row');

    // PRIVATE must never satisfy the BUSINESS batch.
    $privateId=200000; $privateHash=hash('sha256','ci-private');
    $wpdb->insert($wpdb->postmeta,array('post_id'=>$privateId,'meta_key'=>'_ppar_ebay_business_auto','meta_value'=>'1'));
    $wpdb->insert($wpdb->postmeta,array('post_id'=>$privateId,'meta_key'=>'_ppar_creative_identity_hash','meta_value'=>$privateHash));
    update_meta_cache('post',array($privateId));
    $wpdb->insert($ebay,array(
        'portal_key'=>$portal,'item_id'=>'ci-private','seller_account_type'=>'INDIVIDUAL','route_mode'=>'listing','rule_id'=>'ci',
        'creative_identity_hash'=>$privateHash,'title'=>'CI PRIVATE','condition_text'=>'Used','location_text'=>'DE',
        'affiliate_url'=>'https://example.test/p','item_web_url'=>'https://example.test/p','image_url'=>'https://example.test/p.jpg',
        'source_hash'=>hash('sha256','private-source'),'rejection_reason'=>'','source_state'=>'available','policy_state'=>'allowed',
        'route_state'=>'ready','output_state'=>'listing_pending','last_seen'=>$now,'fresh_until'=>$now+3600,'created_at'=>$now,'updated_at'=>$now
    ));
    $rp->setValue($o,array(array('network'=>'ebay','post_id'=>$privateId,'creative_type'=>'product','active'=>true)));
    // fresh plugin instance is unavailable by singleton; clear only request-local eBay cache via reflection.
    $ec=new ReflectionProperty($o,'ebay_business_campaign_source_row_cache');$ec->setAccessible(true);$ec->setValue($o,array());
    $ep=new ReflectionProperty($o,'ebay_business_campaign_source_row_cache_primed');$ep->setAccessible(true);$ep->setValue($o,false);
    $before=(int)$wpdb->num_queries; $private=$rmE->invoke($o,array('network'=>'ebay','post_id'=>$privateId));
    $delta=(int)$wpdb->num_queries-$before;
    $assert($delta===1 && $private===array(),'PRIVATE seller remains blocked by BUSINESS batch');

    echo "REAL_WORDPRESS_MARIADB_PERFORMANCE_BATCH_PASS\n";
    exit;
},0);
