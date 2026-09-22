<?php
/*
 * Plugin Name: Provider Registry Gate
 */
if (!defined('ABSPATH')) { exit; }

trait PRG_Common {
    private function provider_registry_defaults() {
        return array(
            'awin'=>array('label'=>'Awin','state'=>'active','access_owner'=>'core','specialist_menu'=>true,'specialist_slug'=>'affiliate-portal-provider-awin','capabilities'=>array('credentials','connection_test','programmes','partners','offers','product_feeds','synchronization','automation','creatives','outputs','veto')),
            'adcell'=>array('label'=>'ADCELL','state'=>'active','access_owner'=>'core','specialist_menu'=>true,'specialist_slug'=>'affiliate-portal-provider-adcell','capabilities'=>array('credentials','connection_test','programmes','partners','product_feeds','synchronization','automation','creatives','outputs','veto')),
            'ebay'=>array('label'=>'eBay','state'=>'active','access_owner'=>'core','specialist_menu'=>true,'specialist_slug'=>'affiliate-portal-ebay','capabilities'=>array('credentials','connection_test','marketplace','account_deletion_notifications','partners','private_listings','business_products','synchronization','automation','creatives','outputs','veto')),
            'amazon'=>array('label'=>'Amazon','state'=>'prepared','access_owner'=>'adapter','specialist_menu'=>false,'specialist_slug'=>'affiliate-portal-provider-amazon','capabilities'=>array('creatives','outputs','veto')),
            'idealo'=>array('label'=>'idealo','state'=>'active','access_owner'=>'adapter','specialist_menu'=>true,'specialist_slug'=>'affiliate-portal-provider-idealo','capabilities'=>array('credentials','connection_test','product_feeds','synchronization','creatives','outputs','veto')),
            'direct'=>array('label'=>'Direktpartner','state'=>'active','access_owner'=>'none','specialist_menu'=>false,'specialist_slug'=>'','capabilities'=>array('partners','creatives','outputs','veto')),
            'manual'=>array('label'=>'Manuell','state'=>'active','access_owner'=>'none','specialist_menu'=>false,'specialist_slug'=>'','capabilities'=>array('creatives','outputs','veto')),
        );
    }
    private function normalize_registry($raw) {
        $raw=is_array($raw)?$raw:array(); $safe=array();
        foreach($raw as $key=>$provider){
            $key=sanitize_key((string)$key);
            if($key==='' || !is_array($provider)) continue;
            $caps=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($provider['capabilities']??array())))));
            if(!in_array('veto',$caps,true)) $caps[]='veto';
            $state=sanitize_key((string)($provider['state']??'prepared'));
            if(!in_array($state,array('active','prepared','disabled'),true)) $state='prepared';
            $access_owner=sanitize_key((string)($provider['access_owner']??'adapter'));
            if(!in_array($access_owner,array('core','adapter','none'),true)) $access_owner='adapter';
            $safe[$key]=array('key'=>$key,'label'=>sanitize_text_field((string)($provider['label']??strtoupper($key))),'state'=>$state,'access_owner'=>$access_owner,'specialist_menu'=>!empty($provider['specialist_menu']),'specialist_slug'=>sanitize_key((string)($provider['specialist_slug']??'')),'capabilities'=>$caps);
        }
        return $safe;
    }
    public function provider_definition($provider){$provider=sanitize_key((string)$provider);$registry=$this->provider_registry();return $registry[$provider]??null;}
    public function provider_exists($provider){return is_array($this->provider_definition($provider));}
    public function provider_supports($provider,$capability){$definition=$this->provider_definition($provider);return is_array($definition)&&in_array(sanitize_key((string)$capability),(array)$definition['capabilities'],true);}
    public function gate($provider){
        $provider=sanitize_key((string)$provider);
        if(!$this->provider_exists($provider)) return false;
        $definition=$this->provider_definition($provider);
        $state=is_array($definition)?sanitize_key((string)($definition['state']??'prepared')):'prepared';
        if($state!=='active') return false;
        if($this->provider_supports($provider,'credentials')) return 'credentials';
        return true;
    }
}
final class PRG_Baseline {
    use PRG_Common;
    const PROVIDER_CONTRACT_VERSION='2.0';
    public function provider_registry(){
        $raw=apply_filters('ppar_affiliate_provider_registry',$this->provider_registry_defaults(),self::PROVIDER_CONTRACT_VERSION);
        return $this->normalize_registry($raw);
    }
}
final class PRG_Candidate {
    use PRG_Common;
    const PROVIDER_CONTRACT_VERSION='2.0';
    private $provider_registry_request_cache=null;
    private function provider_registry_request_cache_allowed(){
        if((function_exists('is_admin')&&is_admin()) || (defined('DOING_CRON')&&DOING_CRON) || (defined('REST_REQUEST')&&REST_REQUEST) || (defined('WP_CLI')&&WP_CLI) || (function_exists('wp_doing_ajax')&&wp_doing_ajax())) return false;
        return true;
    }
    public function provider_registry(){
        $cache_allowed=$this->provider_registry_request_cache_allowed();
        if($cache_allowed&&is_array($this->provider_registry_request_cache)) return $this->provider_registry_request_cache;
        $raw=apply_filters('ppar_affiliate_provider_registry',$this->provider_registry_defaults(),self::PROVIDER_CONTRACT_VERSION);
        $safe=$this->normalize_registry($raw);
        if($cache_allowed) $this->provider_registry_request_cache=$safe;
        return $safe;
    }
}

$GLOBALS['prg_phase']='';
$GLOBALS['prg_filter_hits']=array('baseline'=>0,'candidate'=>0,'admin'=>0);
$GLOBALS['prg_sanitize_key']=array('baseline'=>0,'candidate'=>0,'admin'=>0);
$GLOBALS['prg_sanitize_text']=array('baseline'=>0,'candidate'=>0,'admin'=>0);

add_filter('ppar_affiliate_provider_registry',function($registry,$contract){
    $p=(string)($GLOBALS['prg_phase']??'');
    if(isset($GLOBALS['prg_filter_hits'][$p])) $GLOBALS['prg_filter_hits'][$p]++;
    $registry['My Provider!']=array('label'=>'<b>My Provider</b>','state'=>'ACTIVE','access_owner'=>'adapter','specialist_menu'=>true,'specialist_slug'=>'My Provider Page','capabilities'=>array(' outputs ','outputs','veto',''));
    return $registry;
},50,2);
add_filter('sanitize_key',function($v,$raw){$p=(string)($GLOBALS['prg_phase']??'');if(isset($GLOBALS['prg_sanitize_key'][$p]))$GLOBALS['prg_sanitize_key'][$p]++;return $v;},PHP_INT_MAX,2);
add_filter('sanitize_text_field',function($v,$raw){$p=(string)($GLOBALS['prg_phase']??'');if(isset($GLOBALS['prg_sanitize_text'][$p]))$GLOBALS['prg_sanitize_text'][$p]++;return $v;},PHP_INT_MAX,2);

function prg_run_public(){
    $n=5000; $b=new PRG_Baseline(); $c=new PRG_Candidate();
    $GLOBALS['prg_phase']='baseline'; $b_registry=$b->provider_registry(); $b_results=array();
    for($i=0;$i<$n;$i++) $b_results[]=$b->gate('manual');
    $GLOBALS['prg_phase']='candidate'; $c_registry=$c->provider_registry(); $c_results=array();
    for($i=0;$i<$n;$i++) $c_results[]=$c->gate('manual');
    header('Content-Type: application/json');
    echo wp_json_encode(array(
        'baseline_registry_hash'=>hash('sha256',wp_json_encode($b_registry)),
        'candidate_registry_hash'=>hash('sha256',wp_json_encode($c_registry)),
        'result_hash_baseline'=>hash('sha256',serialize($b_results)),
        'result_hash_candidate'=>hash('sha256',serialize($c_results)),
        'filter_hits'=>$GLOBALS['prg_filter_hits'],
        'sanitize_key'=>$GLOBALS['prg_sanitize_key'],
        'sanitize_text_field'=>$GLOBALS['prg_sanitize_text'],
        'candidate_extension'=>$c_registry['myprovider']??null,
    )); exit;
}
function prg_run_admin(){
    $GLOBALS['prg_phase']='admin'; $c=new PRG_Candidate(); $r=array();
    for($i=0;$i<50;$i++) $r[]=$c->gate('manual');
    header('Content-Type: application/json');
    echo wp_json_encode(array('result_hash'=>hash('sha256',serialize($r)),'filter_hits'=>$GLOBALS['prg_filter_hits']['admin'],'sanitize_key'=>$GLOBALS['prg_sanitize_key']['admin'])); exit;
}
add_action('template_redirect',function(){if(isset($_GET['prg_public'])) prg_run_public();},-1000);
add_action('admin_post_nopriv_prg_admin','prg_run_admin');
