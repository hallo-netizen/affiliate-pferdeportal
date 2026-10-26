<?php
if (!defined('ABSPATH')) { fwrite(STDERR,"WP_NOT_LOADED\n"); exit(1); }

$root=dirname(__DIR__).'/hobby-depot-affiliate-router/includes';
require_once $root.'/trait-ppar-provider-registry.php';
require_once $root.'/trait-ppar-ebay.php';

if (!function_exists('hd_category_registry_ready')) {
    function hd_category_registry_ready(){ return true; }
}
if (!function_exists('hd_category_registry_snapshot')) {
    function hd_category_registry_snapshot(){
        return [
            'contract'=>'HD004_WP_TEST','revision'=>'test-1',
            'nodes'=>[
                ['node_id'=>'core:world:gestalten','parent_id'=>'','display_name'=>'Gestalten','slug'=>'gestalten','status'=>'active','object_type'=>'page'],
                ['node_id'=>'core:hub:handarbeit','parent_id'=>'core:world:gestalten','display_name'=>'Handarbeit','slug'=>'handarbeit','status'=>'active','object_type'=>'page'],
                ['node_id'=>'core:entity:stricken','parent_id'=>'core:hub:handarbeit','display_name'=>'Stricken','slug'=>'stricken','status'=>'active','object_type'=>'page'],
                ['node_id'=>'core:leaf:stricken-anfaenger','parent_id'=>'core:entity:stricken','display_name'=>'Stricken für Anfänger','slug'=>'stricken-anfaenger','status'=>'active','object_type'=>'category'],
            ],
            'mapping'=>[
                'core:entity:stricken'=>['object_id'=>101,'object_type'=>'page'],
                'core:leaf:stricken-anfaenger'=>['object_id'=>201,'object_type'=>'category'],
            ],
        ];
    }
}

class HDAR_WP_Ebay_Roundtrip {
    use PPAR_Provider_Registry_Trait;
    use PPAR_Ebay_Trait;

    const PROVIDER_CONTRACT_VERSION='test';
    const OPTION_PROVIDER_ACCESS_STATE='hdar_test_provider_access';
    const OPTION_PROVIDER_CHANNEL_STATE='hdar_test_provider_channel';
    const OPTION_NETWORK_AWIN='hdar_test_awin';
    const OPTION_NETWORK_AWIN_PROGRAMMES='hdar_test_awin_programmes';
    const OPTION_NETWORK_ADCELL='hdar_test_adcell';
    const OPTION_NETWORK_EBAY='hdar_test_ebay';

    const EBAY_CRON_HOOK='hdar_test_ebay_cron';
    const EBAY_MAINTENANCE_CRON_HOOK='hdar_test_ebay_maintenance';
    const EBAY_MEDIA_CLEANUP_HOOK='hdar_test_ebay_media_cleanup';
    const EBAY_REFRESH_CRON_HOOK='hdar_test_ebay_refresh';
    const EBAY_REFRESH_WORKER_HOOK='hdar_test_ebay_refresh_worker';
    const EBAY_WORKER_HOOK='hdar_test_ebay_worker';
    const EBAY_BUSINESS_CLASSIFIER_VERSION='test';
    const EBAY_CONTENT_POLICY_VERSION='test';
    const EBAY_PRIVATE_CLASSIFIER_VERSION='test';
    const EBAY_MEDIA_CLEANUP_VERSION='test';
    const EBAY_RUNTIME_BUILD='test';
    const EBAY_SCHEMA_VERSION='test';
    const OPTION_EBAY_MAINTENANCE_STATE='hdar_test_ebay_maintenance_state';
    const OPTION_EBAY_MEDIA_CLEANUP_STATE='hdar_test_ebay_media_cleanup_state';
    const OPTION_EBAY_PRIVATE_STRUCTURE_VERSION='hdar_test_ebay_private_structure';
    const OPTION_EBAY_REFRESH_JOB='hdar_test_ebay_refresh_job';
    const OPTION_EBAY_SCHEMA_VERSION='hdar_test_ebay_schema';
    const OPTION_EBAY_SYNC_JOB='hdar_test_ebay_sync_job';
    const VERSION='test';
}

wp_set_current_user(1);
delete_option(HDAR_WP_Ebay_Roundtrip::OPTION_NETWORK_EBAY);
delete_option(HDAR_WP_Ebay_Roundtrip::OPTION_PROVIDER_ACCESS_STATE);

$secret='wp-runtime-ebay-secret';
$initial=[
    'enabled'=>false,
    'environment'=>'sandbox',
    'client_id'=>'cid',
    'client_secret'=>$secret,
    'epn_campaign_id'=>'1234567890',
    'affiliate_reference_prefix'=>'hobby-depot',
    'business_enabled'=>true,
    'private_enabled'=>false,
    'api_terms_confirmed'=>true,
    'privacy_policy_confirmed'=>true,
];
$h=new HDAR_WP_Ebay_Roundtrip();
$normalized=$h->ebay_normalize_settings($initial,true);
update_option(HDAR_WP_Ebay_Roundtrip::OPTION_NETWORK_EBAY,$normalized,false);

$_POST=[
    'provider'=>'ebay',
    'ppar_provider_action'=>'save',
    'ppar_provider_nonce'=>wp_create_nonce('ppar_provider_access_ebay'),
    'ppar_provider'=>[
        'ebay'=>[
            'enabled'=>'',
            'environment'=>'sandbox',
            'client_id'=>'cid',
            'client_secret'=>'',
            'epn_campaign_id'=>'1234567890',
            'affiliate_reference_prefix'=>'hobby-depot',
        ],
    ],
];
$_REQUEST=$_POST;

register_shutdown_function(function() use ($secret){
    $stored=get_option(HDAR_WP_Ebay_Roundtrip::OPTION_NETWORK_EBAY,[]);
    if (($stored['client_secret']??null)!==$secret) {
        fwrite(STDERR,"FAIL: eBay WordPress blank resave lost secret\n");
        exit(1);
    }
    if (($stored['client_id']??'')!=='cid' || ($stored['epn_campaign_id']??'')!=='1234567890') {
        fwrite(STDERR,"FAIL: eBay WordPress credential roundtrip mismatch\n");
        exit(1);
    }
    echo "PASS: eBay WordPress central save handler preserves existing secret on blank resave\n";
    echo "WORDPRESS_EBAY_SECRET_VALUE_NOT_PRINTED=PASS\n";
});

$h->handle_provider_access_save();
