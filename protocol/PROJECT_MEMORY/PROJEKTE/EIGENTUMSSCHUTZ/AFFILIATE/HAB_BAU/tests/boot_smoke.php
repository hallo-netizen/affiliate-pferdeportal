<?php
/**
 * Real plugin entrypoint boot smoke, not just PHP syntax.
 * Stub WordPress Hook API; no credentials, database or HTTP.
 */
error_reporting(E_ALL);
define('ABSPATH','/mock/');
$GLOBALS['hooks']=array();
function add_filter($tag,$cb,$pri=10,$args=1){$GLOBALS['hooks'][$tag][]=$cb;return true;}
function add_action($tag,$cb,$pri=10,$args=1){$GLOBALS['hooks'][$tag][]=$cb;return true;}
function register_activation_hook($file,$cb){$GLOBALS['hooks']['activation'][]=$cb;}
function register_deactivation_hook($file,$cb){$GLOBALS['hooks']['deactivation'][]=$cb;}
function wp_doing_ajax(){return false;}
function is_admin(){return false;}
function get_option($key,$default=false){return $default;}
function get_bloginfo($type=''){return 'Hab & Bewahr';}
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function sanitize_title($x){return trim(preg_replace('/[^a-z0-9]+/','-',strtolower((string)$x)),'-');}
function absint($x){return abs((int)$x);}
function home_url($path=''){return 'https://hab-und-bewahr.de/'.ltrim($path,'/');}
class WP_Error { public function __construct($code,$message=''){} }
function is_wp_error($x){return $x instanceof WP_Error;}
require __DIR__.'/../_build/affiliate-portal-router/affiliate-portal-router.php';
if(!class_exists('Portal_Affiliate_Router'))throw new Exception('core_router_missing');
foreach(array(
 'PPAR_Affiliate_Source_Plan',
 'PPAR_Affiliate_Admin_KISS',
 'PPAR_Deal_Radar',
 'PPAR_Partner_Analytics_Admin',
 'PPAR_DS24_Manual_Downstream',
 'PPAR_HB_Integration',
) as $class) {
 if(!class_exists($class))throw new Exception('Feature class not loaded: '.$class);
}
foreach(array(
 'ppar_affiliate_provider_registry',
 'ppar_partner_analytics_providers',
 'ppar_affiliate_slot_matrix',
 'ppar_portal_source_catalog',
 'hbdp_article_product_cards_html',
 'ppar_deal_radar_hourly_v1',
 'ppar_partner_analytics_ingest',
 'update_option_ppar_digistore24_affiliations_v1',
 'admin_post_ppar_universal_manual_import',
 'rest_api_init',
) as $tag) {
 if(empty($GLOBALS['hooks'][$tag]))throw new Exception('Expected functional feature hook missing: '.$tag);
}
foreach(array('pftk_hub_grid_affiliate_data','pftk_leaf_category_affiliate_slot_html','pftk_market_affiliate_slot_html') as $tag) {
 if(!empty($GLOBALS['hooks'][$tag]))throw new Exception('Foreign theme hook still registered: '.$tag);
}
echo 'HB_AFFILIATE_REAL_BOOTSTRAP_PASS '.count($GLOBALS['hooks'])." hook types\n";
