<?php
/*
 * Plugin Name: PPAR 6.72.151 Residue Gate
 */
if (!defined('ABSPATH')) { exit; }

final class PPAR151_Residue_Gate {
    public $phase='old';
    public $sanitize=array('old'=>0,'new'=>0,'admin'=>0);
    public $registry_filter_hits=0;
    public $term_queries=0;
    private $registry_cache=null;

    public function __construct() {
        add_filter('sanitize_key', function($san,$raw){
            if(isset($this->sanitize[$this->phase])) $this->sanitize[$this->phase]++;
            return $san;
        }, PHP_INT_MAX, 2);
        add_filter('ppar_affiliate_provider_registry', function($r){ $this->registry_filter_hits++; return $r; }, 10, 1);
        add_filter('get_term', function($term){ $this->term_queries++; return $term; }, PHP_INT_MAX, 1);
    }

    private function cache_allowed() {
        return !is_admin()
            && !(defined('DOING_CRON')&&DOING_CRON)
            && !(defined('REST_REQUEST')&&REST_REQUEST)
            && !(defined('WP_CLI')&&WP_CLI)
            && !(function_exists('wp_doing_ajax')&&wp_doing_ajax());
    }

    private function old_norm($c) {
        return array(
            'id'=>sanitize_key((string)($c['id']??'')),
            'network'=>sanitize_key((string)($c['network']??'manual')),
            'creative_type'=>sanitize_key((string)($c['creative_type']??'banner')),
            'render_mode'=>sanitize_key((string)($c['render_mode']??'image_link')),
            'programme_status'=>sanitize_key((string)($c['programme_status']??'unknown')),
            'assignment_mode'=>sanitize_key((string)($c['assignment_mode']??'page_tree')),
            'source'=>sanitize_key((string)($c['source']??'manual')),
            'placements'=>array_values(array_filter(array_map('sanitize_key',(array)($c['placements']??array())))),
        );
    }
    private function new_norm($c) {
        static $cache=array();
        $raw=array(
            'id'=>(string)($c['id']??''),
            'network'=>(string)($c['network']??'manual'),
            'creative_type'=>(string)($c['creative_type']??'banner'),
            'render_mode'=>(string)($c['render_mode']??'image_link'),
            'programme_status'=>(string)($c['programme_status']??'unknown'),
            'assignment_mode'=>(string)($c['assignment_mode']??'page_tree'),
            'source'=>(string)($c['source']??'manual'),
            'placements'=>(array)($c['placements']??array()),
        );
        $key='';
        if($this->cache_allowed()){
            $key=hash('sha256',serialize($raw));
            if(isset($cache[$key])) return $cache[$key];
        }
        $n=array(
            'id'=>sanitize_key($raw['id']),
            'network'=>sanitize_key($raw['network']),
            'creative_type'=>sanitize_key($raw['creative_type']),
            'render_mode'=>sanitize_key($raw['render_mode']),
            'programme_status'=>sanitize_key($raw['programme_status']),
            'assignment_mode'=>sanitize_key($raw['assignment_mode']),
            'source'=>sanitize_key($raw['source']),
            'placements'=>array_values(array_filter(array_map('sanitize_key',$raw['placements']))),
        );
        if($this->cache_allowed()) $cache[$key]=$n;
        return $n;
    }

    private function old_slot_allowed($c,$slot){
        $slot=sanitize_key((string)$slot);
        $placements=array_map('sanitize_key',(array)($c['placements']??array()));
        $accepted=preg_match('/^category_product_[123]$/',$slot)?array($slot,'category_product'):array($slot);
        return !empty(array_intersect($accepted,$placements))||in_array('*',$placements,true);
    }
    private function new_slot_allowed($c,$slot){
        $slot=sanitize_key((string)$slot);
        $placements=$this->new_norm($c)['placements'];
        $accepted=preg_match('/^category_product_[123]$/',$slot)?array($slot,'category_product'):array($slot);
        return !empty(array_intersect($accepted,$placements))||in_array('*',$placements,true);
    }

    private function provider_registry_defaults(){
        return array(
            'ebay'=>array('label'=>'eBay','capabilities'=>array('creatives','outputs','veto')),
            'awin'=>array('label'=>'Awin','capabilities'=>array('creatives','outputs','veto')),
            'manual'=>array('label'=>'Manuell','capabilities'=>array('creatives','outputs','veto')),
        );
    }
    private function provider_registry(){
        if($this->cache_allowed()&&is_array($this->registry_cache)) return $this->registry_cache;
        $raw=apply_filters('ppar_affiliate_provider_registry',$this->provider_registry_defaults());
        $safe=array();
        foreach($raw as $key=>$p){
            $key=sanitize_key((string)$key);
            $safe[$key]=array('key'=>$key,'label'=>(string)$p['label'],'capabilities'=>array_map('sanitize_key',(array)$p['capabilities']));
        }
        if($this->cache_allowed()) $this->registry_cache=$safe;
        return $safe;
    }
    private function old_provider_definition($provider){
        $provider=sanitize_key((string)$provider);
        $r=$this->provider_registry();
        return $r[$provider]??null;
    }
    private function new_provider_definition($provider){
        static $cache=array();
        $raw=(string)$provider;
        if($this->cache_allowed()&&array_key_exists($raw,$cache)) return $cache[$raw];
        $provider=sanitize_key($raw);
        $r=$this->provider_registry();
        $d=$r[$provider]??null;
        if($this->cache_allowed()) $cache[$raw]=$d;
        return $d;
    }

    private function old_private_parent_term(){
        return get_term_by('slug','private-anzeigen','hp_listing_category');
    }
    private function new_private_parent_term(){
        static $resolved=false,$cached=null;
        if($this->cache_allowed()&&$resolved) return $cached;
        $term=get_term_by('slug','private-anzeigen','hp_listing_category');
        if($this->cache_allowed()){ $cached=is_object($term)?$term:null; $resolved=true; return $cached; }
        return is_object($term)?$term:null;
    }

    private function campaigns(){
        $out=array();
        $nets=array('ebay','awin','manual');
        $types=array('product','banner');
        $modes=array('page_tree','auto_topic','fallback');
        $slots=array('category_product','category_product_1','hub_after_cards','post_inline_banner');
        for($i=0;$i<1200;$i++){
            $out[]=array(
                'id'=>'Campaign '.$i,
                'network'=>$nets[$i%3],
                'creative_type'=>$types[$i%2],
                'render_mode'=>$i%5===0?'html':'image_link',
                'programme_status'=>$i%7===0?'paused':'active',
                'assignment_mode'=>$modes[$i%3],
                'source'=>$i%2?'output_object_v4':'manual',
                'placements'=>array($slots[$i%4],$i%11===0?'*':''),
            );
        }
        return $out;
    }

    public function public_gate(){
        $campaigns=$this->campaigns();
        $slots=array('category_product_1','category_product_2','hub_after_cards','post_inline_banner');

        $this->phase='old';
        $old=array();
        for($round=0;$round<6;$round++){
            foreach($campaigns as $c){
                $n=$this->old_norm($c);
                $old[]=array($n['network'],$n['creative_type'],$n['assignment_mode'],$this->old_slot_allowed($c,$slots[$round%4]));
            }
        }
        for($i=0;$i<4000;$i++) $old[]=$this->old_provider_definition($i%2?'ebay':'awin');
        for($i=0;$i<200;$i++){ $t=$this->old_private_parent_term(); $old[]=is_object($t)?(int)$t->term_id:0; }
        $old_hits=$this->sanitize['old'];

        $this->registry_cache=null;
        $this->phase='new';
        $new=array();
        for($round=0;$round<6;$round++){
            foreach($campaigns as $c){
                $n=$this->new_norm($c);
                $new[]=array($n['network'],$n['creative_type'],$n['assignment_mode'],$this->new_slot_allowed($c,$slots[$round%4]));
            }
        }
        for($i=0;$i<4000;$i++) $new[]=$this->new_provider_definition($i%2?'ebay':'awin');
        for($i=0;$i<200;$i++){ $t=$this->new_private_parent_term(); $new[]=is_object($t)?(int)$t->term_id:0; }
        $new_hits=$this->sanitize['new'];

        // Mutation safety: changed raw campaign must produce changed normalized value.
        $mut=$campaigns[0];
        $before=$this->new_norm($mut);
        $mut['network']='AWIN';
        $after=$this->new_norm($mut);

        return array(
            'old_hash'=>hash('sha256',serialize($old)),
            'new_hash'=>hash('sha256',serialize($new)),
            'sanitize_old'=>$old_hits,
            'sanitize_new'=>$new_hits,
            'mutation_before'=>$before['network'],
            'mutation_after'=>$after['network'],
            'registry_filter_hits'=>$this->registry_filter_hits,
            'term_filter_hits'=>$this->term_queries,
        );
    }

    public function admin_gate(){
        $this->phase='admin';
        $campaign=$this->campaigns()[0];
        for($i=0;$i<100;$i++){
            $this->new_norm($campaign);
            $this->new_provider_definition('ebay');
            $this->new_private_parent_term();
        }
        return array('sanitize'=>$this->sanitize['admin'],'registry_filter_hits'=>$this->registry_filter_hits,'term_filter_hits'=>$this->term_queries);
    }
}

$GLOBALS['ppar151_gate']=new PPAR151_Residue_Gate();
add_action('init',function(){
    if(!term_exists('private-anzeigen','hp_listing_category')){
        wp_insert_term('Private Anzeigen','hp_listing_category',array('slug'=>'private-anzeigen'));
    }
},1);
add_action('template_redirect',function(){
    if(!isset($_GET['ppar151'])) return;
    header('Content-Type: application/json');
    echo wp_json_encode($GLOBALS['ppar151_gate']->public_gate());
    exit;
},-1000);
add_action('admin_post_nopriv_ppar151_admin',function(){
    header('Content-Type: application/json');
    echo wp_json_encode($GLOBALS['ppar151_gate']->admin_gate());
    exit;
});
