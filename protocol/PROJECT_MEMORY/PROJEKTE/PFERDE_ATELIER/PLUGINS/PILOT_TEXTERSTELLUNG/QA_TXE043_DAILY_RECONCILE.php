<?php
declare(strict_types=1);
define('ABSPATH','/qa/');define('ARRAY_A','ARRAY_A');define('DOING_CRON',true);
$GLOBALS['options']=[];$GLOBALS['hooks']=[];$GLOBALS['schedules']=[];
function home_url($p='/'){return 'https://qa.test.invalid/';} function get_current_blog_id(){return 1;}
function get_option($k,$d=false){return $GLOBALS['options'][$k]??$d;}
function get_site_option($k,$d=false){return $d;}
function update_option($k,$v,$a=false){$GLOBALS['options'][$k]=$v;return true;}
function current_user_can($k){return false;}
function add_action($name,$callback,$priority=10,$count=1){$GLOBALS['hooks'][$name][]=$callback;}
function add_filter(...$v){}function remove_action(...$v){}function register_activation_hook(...$v){}function register_deactivation_hook(...$v){}
function wp_next_scheduled($name){return isset($GLOBALS['schedules'][$name])?$GLOBALS['schedules'][$name]:false;}
function wp_schedule_event($time,$interval,$name){$GLOBALS['schedules'][$name]=$time;return true;}
function wp_clear_scheduled_hook($name){unset($GLOBALS['schedules'][$name]);return true;}
function is_admin(){return false;}function wp_json_encode($x,$f=0){return json_encode($x,$f);}
function wp_strip_all_tags($s){return strip_tags($s);}function is_wp_error($x){return false;}
// No mutable topic DB is made available: the empty pool/receipt must not be invented.
class Db {public string $prefix='wp_';public string $last_error='';}
$GLOBALS['wpdb']=new Db();
require __DIR__.'/../texterstellung/texterstellung.php';
$checks=[];function check_cat($n,$x){$GLOBALS['checks'][$n]=(bool)$x;}
TXE_Workshop::init();check_cat('no_daily_schedule_without_explicit_site_confirmation',empty($GLOBALS['schedules']));
$GLOBALS['options']['texterstellung_testsite_confirmation_v1']=hash('sha256',home_url('/').'|'.get_current_blog_id());
TXE_Workshop::init();check_cat('daily_hook_scheduled_after_confirmation',isset($GLOBALS['schedules']['txe_existing_category_reconcile_daily']));
$once=count($GLOBALS['schedules']);TXE_Workshop::init();check_cat('same_hook_not_scheduled_twice',count($GLOBALS['schedules'])===$once);
TXE_Workshop::reconcileExistingCategoryBindings();check_cat('no_fabricated_source_after_daily_run',empty($GLOBALS['options']['texterstellung_orders_v1']));
TXE_Workshop::deactivate();check_cat('schedule_removed_on_deactivation',empty($GLOBALS['schedules']));
$tests=$GLOBALS['checks'];$p=count(array_filter($tests));echo json_encode(['tests'=>$tests,'pass'=>$p,'total'=>count($tests)],JSON_PRETTY_PRINT),"\n";
exit($p===count($tests)?0:1);
