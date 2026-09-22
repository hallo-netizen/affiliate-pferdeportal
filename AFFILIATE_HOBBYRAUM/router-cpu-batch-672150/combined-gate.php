<?php
/*
 * Plugin Name: PPAR 6.72.150 Combined CPU Gate
 */
if (!defined('ABSPATH')) { exit; }

final class PPAR150_Gate {
    public $phase='';
    public $sanitize=array('old'=>0,'new'=>0,'admin'=>0);
    public $rule_normalize_hits=0;
    public $settings_normalize_hits=0;
    private $rule_cache=null;
    private $settings_cache=null;
    private $control_raw=array();
    private $control_norm=array();
    public $control_status='approved';

    public function __construct(){
        add_filter('sanitize_key', function($san,$raw){
            if(isset($this->sanitize[$this->phase])) $this->sanitize[$this->phase]++;
            return $san;
        }, PHP_INT_MAX, 2);
    }

    private function old_slot_required($slot){
        $slot=sanitize_key((string)$slot);
        if($slot==='category_product'||preg_match('/^(?:hub_product|category_product|journal_product)_[123]$/',$slot)||$slot==='post_bottom_products') return 'product';
        if(in_array($slot,array('hub_after_cards','product_after_category_tiles','post_inline_banner','anzeigenmarkt_top_banner','anzeigenmarkt_category_banner','journal_banner','glossary_single_desktop_banner','glossary_single_mobile_banner','breed_single_banner','breed_single_desktop_banner','breed_single_mobile_banner','glossary_overview_banner','breed_overview_banner','start_after_topics'),true)) return 'banner';
        return '';
    }
    private function new_slot_required($slot){
        static $cache=array();
        $raw=(string)$slot;
        if(array_key_exists($raw,$cache)) return $cache[$raw];
        $slot=sanitize_key($raw);
        if($slot==='category_product'||preg_match('/^(?:hub_product|category_product|journal_product)_[123]$/',$slot)||$slot==='post_bottom_products') return $cache[$raw]='product';
        if(in_array($slot,array('hub_after_cards','product_after_category_tiles','post_inline_banner','anzeigenmarkt_top_banner','anzeigenmarkt_category_banner','journal_banner','glossary_single_desktop_banner','glossary_single_mobile_banner','breed_single_banner','breed_single_desktop_banner','breed_single_mobile_banner','glossary_overview_banner','breed_overview_banner','start_after_topics'),true)) return $cache[$raw]='banner';
        return $cache[$raw]='';
    }
    private function old_equiv($slot){
        $slot=sanitize_key($slot);
        if(preg_match('/^category_product_[123]$/',$slot)) return array($slot,'category_product');
        $groups=array(
            array('top_info','post_after_intro'),
            array('mid_content','post_mid_content','post_inline_banner'),
            array('bottom_recommendation','post_bottom_recommendation','post_bottom_products'),
            array('hub_top_cta','template_top','template_after_intro'),
            array('hub_after_cards','template_after_selected','template_mid'),
            array('hub_grid_card'),
            array('hub_mid_banner','template_mid_banner'),
            array('category_recommendation','produkt_recommendation','template_bottom','product_after_category_tiles'),
            array('glossary_single_banner','glossary_single_desktop_banner','glossary_single_mobile_banner'),
            array('breed_single_banner','breed_single_desktop_banner','breed_single_mobile_banner'),
        );
        foreach($groups as $g) if(in_array($slot,$g,true)) return $g;
        return array($slot);
    }
    private function new_equiv($slot){
        static $cache=array();
        $raw=(string)$slot;
        if(array_key_exists($raw,$cache)) return $cache[$raw];
        $slot=sanitize_key($raw);
        if(preg_match('/^category_product_[123]$/',$slot)) return $cache[$raw]=array($slot,'category_product');
        $groups=array(
            array('top_info','post_after_intro'),
            array('mid_content','post_mid_content','post_inline_banner'),
            array('bottom_recommendation','post_bottom_recommendation','post_bottom_products'),
            array('hub_top_cta','template_top','template_after_intro'),
            array('hub_after_cards','template_after_selected','template_mid'),
            array('hub_grid_card'),
            array('hub_mid_banner','template_mid_banner'),
            array('category_recommendation','produkt_recommendation','template_bottom','product_after_category_tiles'),
            array('glossary_single_banner','glossary_single_desktop_banner','glossary_single_mobile_banner'),
            array('breed_single_banner','breed_single_desktop_banner','breed_single_mobile_banner'),
        );
        foreach($groups as $g) if(in_array($slot,$g,true)) return $cache[$raw]=$g;
        return $cache[$raw]=array($slot);
    }
    private function old_slot_allowed($campaign,$slot){
        $slot=sanitize_key((string)$slot);
        $placements=isset($campaign['placements'])&&is_array($campaign['placements'])?array_map('sanitize_key',$campaign['placements']):array();
        $accepted=$this->old_equiv($slot);
        return !empty(array_intersect($accepted,$placements))||in_array('*',$placements,true);
    }
    private function new_slot_allowed($campaign,$slot){
        $slot=!empty($campaign['_ppar_runtime_normalized_slot_type'])?(string)$slot:sanitize_key((string)$slot);
        $placements=!empty($campaign['_ppar_runtime_normalized'])
            ? (isset($campaign['placements'])&&is_array($campaign['placements'])?$campaign['placements']:array())
            : (isset($campaign['placements'])&&is_array($campaign['placements'])?array_map('sanitize_key',$campaign['placements']):array());
        $accepted=$this->new_equiv($slot);
        return !empty(array_intersect($accepted,$placements))||in_array('*',$placements,true);
    }

    private function old_family($raw){
        static $map=null;
        $slug=sanitize_key((string)$raw);
        if($slug==='') return '';
        if($map===null) $map=array('reithelme-faq'=>'reithelme','decken-zubehoer'=>'pferdedecken','trensen-gebisse'=>'trensen');
        return sanitize_key((string)($map[$slug]??''));
    }
    private function new_family($raw){
        static $map=null,$cache=array();
        $raw=(string)$raw;
        if(array_key_exists($raw,$cache)) return $cache[$raw];
        $slug=sanitize_key($raw);
        if($slug==='') return $cache[$raw]='';
        if($map===null) $map=array('reithelme-faq'=>'reithelme','decken-zubehoer'=>'pferdedecken','trensen-gebisse'=>'trensen');
        return $cache[$raw]=(string)($map[$slug]??'');
    }

    private function normalize_rules($rules){
        $this->rule_normalize_hits++;
        $safe=array();
        foreach((array)$rules as $rule){
            if(!is_array($rule)) continue;
            $id=sanitize_key((string)($rule['id']??''));
            $query=sanitize_text_field((string)($rule['query']??''));
            $target=sanitize_title((string)($rule['target_term_slug']??''));
            if($id===''||$query===''||$target==='') continue;
            $safe[$id]=array(
                'id'=>substr($id,0,80),
                'label'=>substr(sanitize_text_field((string)($rule['label']??$id)),0,120),
                'query'=>substr($query,0,100),
                'target_term_slug'=>substr($target,0,120),
                'category_ids'=>array(),
                'active'=>!empty($rule['active']),
                'private'=>!empty($rule['private']),
                'business'=>!empty($rule['business']),
            );
        }
        return array_values($safe);
    }
    private function source_rules(){
        return array(
            array('id'=>'Decken Regel','query'=>'Regendecken Pferd','target_term_slug'=>'pferdedecken','label'=>'Decken','active'=>1,'business'=>1),
            array('id'=>'Trensen Regel','query'=>'Englische Trense','target_term_slug'=>'trensen','label'=>'Trensen','active'=>1,'business'=>1),
        );
    }
    private function old_rules(){ return $this->normalize_rules($this->source_rules()); }
    private function new_rules(){
        $cache_allowed=!is_admin() && !(defined('DOING_CRON')&&DOING_CRON) && !(defined('REST_REQUEST')&&REST_REQUEST) && !(defined('WP_CLI')&&WP_CLI) && !(function_exists('wp_doing_ajax')&&wp_doing_ajax());
        if($cache_allowed&&is_array($this->rule_cache)) return $this->rule_cache;
        $r=$this->normalize_rules($this->source_rules());
        if($cache_allowed) $this->rule_cache=$r;
        return $r;
    }
    private function normalize_settings(){
        $this->settings_normalize_hits++;
        return array('enabled'=>true,'environment'=>'production','rules'=>$this->new_rules(),'affiliate_reference_prefix'=>sanitize_key('pferde-atelier'));
    }
    private function new_settings(){
        $cache_allowed=!is_admin() && !(defined('DOING_CRON')&&DOING_CRON) && !(defined('REST_REQUEST')&&REST_REQUEST) && !(defined('WP_CLI')&&WP_CLI) && !(function_exists('wp_doing_ajax')&&wp_doing_ajax());
        if($cache_allowed&&is_array($this->settings_cache)) return $this->settings_cache;
        $s=$this->normalize_settings();
        if($cache_allowed) $this->settings_cache=$s;
        return $s;
    }

    private function old_control($portal,$scope,$key){
        $portal=sanitize_key((string)$portal); $scope=sanitize_key((string)$scope); $key=sanitize_text_field((string)$key);
        $norm=hash('sha256',$portal.'|'.$scope.'|'.$key);
        if(isset($this->control_norm[$norm])) return $this->control_norm[$norm];
        return $this->control_norm[$norm]=array('exists'=>1,'status'=>$this->control_status,'reason'=>'fixture');
    }
    private function new_control($portal,$scope,$key){
        $raw=(string)$portal."\x1f".(string)$scope."\x1f".(string)$key;
        if(array_key_exists($raw,$this->control_raw)) return $this->control_raw[$raw];
        $portal=sanitize_key((string)$portal); $scope=sanitize_key((string)$scope); $key=sanitize_text_field((string)$key);
        $norm=hash('sha256',$portal.'|'.$scope.'|'.$key);
        if(isset($this->control_norm[$norm])) return $this->control_raw[$raw]=$this->control_norm[$norm];
        $r=array('exists'=>1,'status'=>$this->control_status,'reason'=>'fixture');
        $this->control_norm[$norm]=$r; $this->control_raw[$raw]=$r; return $r;
    }
    public function mutate_control($status){
        $this->control_status=$status;
        $this->control_norm=array();
        $this->control_raw=array();
    }

    public function public_gate(){
        $slots=array('category_product_1','category_product_2','hub_after_cards','post_inline_banner','unknown slot');
        $campaigns=array();
        for($i=0;$i<4000;$i++){
            $placements=array($i%2?'category_product':'hub_after_cards');
            $campaigns[]=array('placements'=>array_map('sanitize_key',$placements));
        }

        $this->phase='old';
        $old=array();
        for($r=0;$r<5;$r++){
            foreach($slots as $slot){
                $old[]=$this->old_slot_required($slot);
                $old[]=$this->old_equiv($slot);
            }
            foreach($campaigns as $c){
                $old[]=$this->old_slot_allowed($c,'category_product_1');
            }
            foreach(array('reithelme-faq','Decken-Zubehoer','trensen-gebisse','unbekannt') as $slug){
                for($i=0;$i<500;$i++) $old[]=$this->old_family($slug);
            }
        }
        for($i=0;$i<1000;$i++) $old[]=$this->old_control('horse portal','provider','ebay');
        $old_rules=array();
        for($i=0;$i<200;$i++) $old_rules[]=$this->old_rules();
        $old_hits=$this->sanitize['old'];

        // reset semantic control cache so both variants begin from same state.
        $this->control_norm=array();
        $this->control_raw=array();
        $rules_before=$this->rule_normalize_hits;

        $this->phase='new';
        $new=array();
        for($r=0;$r<5;$r++){
            foreach($slots as $slot){
                $new[]=$this->new_slot_required($slot);
                $new[]=$this->new_equiv($slot);
            }
            foreach($campaigns as $c){
                $c['_ppar_runtime_normalized']=1;
                $c['_ppar_runtime_normalized_slot_type']=1;
                $new[]=$this->new_slot_allowed($c,'category_product_1');
            }
            foreach(array('reithelme-faq','Decken-Zubehoer','trensen-gebisse','unbekannt') as $slug){
                for($i=0;$i<500;$i++) $new[]=$this->new_family($slug);
            }
        }
        for($i=0;$i<1000;$i++) $new[]=$this->new_control('horse portal','provider','ebay');
        $new_rules=array();
        for($i=0;$i<200;$i++) $new_rules[]=$this->new_rules();
        $settings=array();
        for($i=0;$i<200;$i++) $settings[]=$this->new_settings();
        $new_hits=$this->sanitize['new'];

        // Negative fallback: unmarked campaign must still sanitize exactly like old semantics.
        $weird=array('placements'=>array('Category Product','HUB_AFTER_CARDS'));
        $fallback_old=$this->old_slot_allowed($weird,'category_product_1');
        $fallback_new=$this->new_slot_allowed($weird,'category_product_1');

        $before_mut=$this->new_control('horse portal','provider','ebay');
        $this->mutate_control('veto');
        $after_mut=$this->new_control('horse portal','provider','ebay');

        return array(
            'old_hash'=>hash('sha256',serialize($old)),
            'new_hash'=>hash('sha256',serialize($new)),
            'old_rules_hash'=>hash('sha256',serialize($old_rules[0])),
            'new_rules_hash'=>hash('sha256',serialize($new_rules[0])),
            'settings_hash'=>hash('sha256',serialize($settings[0])),
            'sanitize_old'=>$old_hits,
            'sanitize_new'=>$new_hits,
            'new_rule_normalize_calls'=>$this->rule_normalize_hits-$rules_before,
            'new_settings_normalize_calls'=>$this->settings_normalize_hits,
            'fallback_old'=>$fallback_old,
            'fallback_new'=>$fallback_new,
            'control_before'=>$before_mut['status'],
            'control_after'=>$after_mut['status'],
        );
    }

    public function admin_gate(){
        $this->phase='admin';
        $before=$this->rule_normalize_hits;
        $hash='';
        for($i=0;$i<50;$i++) $hash=hash('sha256',serialize($this->new_rules()));
        return array('rule_calls'=>$this->rule_normalize_hits-$before,'hash'=>$hash,'sanitize'=>$this->sanitize['admin']);
    }
}

$GLOBALS['ppar150_gate']=new PPAR150_Gate();
add_action('template_redirect',function(){
    if(!isset($_GET['ppar150_public'])) return;
    header('Content-Type: application/json');
    echo wp_json_encode($GLOBALS['ppar150_gate']->public_gate());
    exit;
},-1000);
add_action('admin_post_nopriv_ppar150_admin',function(){
    header('Content-Type: application/json');
    echo wp_json_encode($GLOBALS['ppar150_gate']->admin_gate());
    exit;
});
