<?php
/*
 * Plugin Name: Ranking Context Normalization Gate
 */
if (!defined('ABSPATH')) { exit; }

final class PRG_Ranking_Gate {
    public $sanitize_hits = array('old'=>0,'new'=>0);
    public $phase = '';

    public function __construct() {
        add_filter('sanitize_key', function($sanitized, $raw) {
            if (isset($this->sanitize_hits[$this->phase])) { $this->sanitize_hits[$this->phase]++; }
            return $sanitized;
        }, PHP_INT_MAX, 2);
    }

    public function automation_normalize_target_key($key) {
        $key = strtolower(trim((string) $key));
        if (!preg_match('/^(page|category|journal|market|uge_group|uge_term|pa_breed|pa_breed_group):([a-z0-9_-]+)$/', $key, $match)) {
            return '';
        }
        return $match[1] . ':' . sanitize_key($match[2]);
    }

    private function auto_rank_old($campaign, $context) {
        $wanted = array_values(array_filter(array_map(array($this, 'automation_normalize_target_key'), (array) ($campaign['automation_target_keys'] ?? array()))));
        if (!$wanted) { return null; }
        $primary = isset($context['_ppar_norm_primary_slug']) ? (string)$context['_ppar_norm_primary_slug'] : sanitize_key((string) ($context['primary_slug'] ?? ''));
        $post_type = isset($context['_ppar_norm_post_type']) ? (string)$context['_ppar_norm_post_type'] : sanitize_key((string) ($context['post_type'] ?? ''));
        $available = array();
        $semantic_primary = $this->automation_normalize_target_key((string) ($context['semantic_primary_target_key'] ?? ''));
        $semantic_ancestors = array_values(array_filter(array_map(array($this, 'automation_normalize_target_key'), (array) ($context['semantic_ancestor_target_keys'] ?? array()))));
        if ($semantic_primary !== '') { $available[] = $semantic_primary; }
        foreach ($semantic_ancestors as $semantic_key) { $available[] = $semantic_key; }
        $slot_type = isset($context['slot_type']) ? (string)$context['slot_type'] : '';
        $slot_type = isset($context['_ppar_norm_post_type']) ? $slot_type : sanitize_key($slot_type);
        if ($post_type === 'page' && $slot_type === 'anzeigenmarkt_top_banner') { $available[] = 'market:anzeigenmarkt'; }
        if ($primary !== '') {
            if ($post_type === 'page') { $available[] = 'page:' . $primary; $available[] = 'journal:' . $primary; }
            elseif ($post_type === 'category_archive') { $available[] = 'category:' . $primary; $available[] = 'journal:' . $primary; }
            elseif ($post_type === 'hp_listing_category_archive') { $available[] = 'market:' . $primary; }
            elseif ($post_type === 'uge_term') { $available[] = 'uge_term:' . $primary; }
            elseif ($post_type === 'pa_breed') { $available[] = 'pa_breed:' . $primary; }
            elseif ($post_type === 'uge_group_archive') { $available[] = 'uge_group:' . $primary; }
            elseif ($post_type === 'pa_breed_group_archive') { $available[] = 'pa_breed_group:' . $primary; }
        }
        $direct_term_slugs = isset($context['_ppar_norm_direct_term_slugs']) && is_array($context['_ppar_norm_direct_term_slugs']) ? $context['_ppar_norm_direct_term_slugs'] : (array)($context['direct_term_slugs'] ?? array());
        foreach ($direct_term_slugs as $slug) {
            $slug = isset($context['_ppar_norm_direct_term_slugs']) ? (string)$slug : sanitize_key((string) $slug);
            if ($slug === '') { continue; }
            if ($post_type === 'post') { $available[] = 'category:' . $slug; $available[] = 'journal:' . $slug; }
            elseif ($post_type === 'hp_listing') { $available[] = 'market:' . $slug; }
            elseif ($post_type === 'uge_term') { $available[] = 'uge_group:' . $slug; }
            elseif ($post_type === 'pa_breed') { $available[] = 'pa_breed_group:' . $slug; }
        }
        $hierarchy_prefix='';
        if ($post_type==='page') { $hierarchy_prefix='page:'; }
        elseif ($post_type==='category_archive') { $hierarchy_prefix='category:'; }
        if ($hierarchy_prefix!=='' && $primary!=='') {
            $primary_key=$hierarchy_prefix.$primary;
            if (in_array($primary_key,$wanted,true)) return array('specificity'=>520,'matches'=>1,'reason'=>'Exakte Zielkante: '.$primary_key.'.');
            $ancestor_keys=array();
            $context_slugs = isset($context['_ppar_norm_slugs']) && is_array($context['_ppar_norm_slugs']) ? $context['_ppar_norm_slugs'] : (array)($context['slugs']??array());
            foreach ($context_slugs as $slug) {
                $slug=isset($context['_ppar_norm_slugs']) ? (string)$slug : sanitize_key((string)$slug);
                if ($slug!=='' && $slug!==$primary) { $ancestor_keys[]=$hierarchy_prefix.$slug; }
            }
            $ancestor_matches=array_values(array_intersect(array_unique($wanted),array_unique($ancestor_keys)));
            if ($ancestor_matches) return array('specificity'=>500,'matches'=>count($ancestor_matches),'reason'=>'Themenkreis über echte Vorfahren: '.implode(', ',$ancestor_matches).'.');
        }
        $matches = array_values(array_intersect(array_unique($wanted), array_unique($available)));
        if ($matches) return array('specificity'=>480,'matches'=>count($matches),'reason'=>'Automatische Zielkante: '.implode(', ',$matches).'.');
        return null;
    }

    private function auto_rank_new($campaign, $context) {
        $wanted = isset($campaign['automation_target_keys']) && is_array($campaign['automation_target_keys']) ? array_values(array_filter($campaign['automation_target_keys'])) : array();
        if (!$wanted) { return null; }
        $primary = sanitize_key((string) ($context['primary_slug'] ?? ''));
        $post_type = sanitize_key((string) ($context['post_type'] ?? ''));
        $available = array();
        $semantic_primary = isset($context['_ppar_norm_semantic_primary_target_key']) ? (string)$context['_ppar_norm_semantic_primary_target_key'] : $this->automation_normalize_target_key((string)($context['semantic_primary_target_key'] ?? ''));
        $semantic_ancestors = isset($context['_ppar_norm_semantic_ancestor_target_keys']) && is_array($context['_ppar_norm_semantic_ancestor_target_keys']) ? $context['_ppar_norm_semantic_ancestor_target_keys'] : array_values(array_filter(array_map(array($this,'automation_normalize_target_key'), (array)($context['semantic_ancestor_target_keys'] ?? array()))));
        if ($semantic_primary !== '') { $available[] = $semantic_primary; }
        foreach ($semantic_ancestors as $semantic_key) { $available[] = $semantic_key; }
        $slot_type = sanitize_key((string) ($context['slot_type'] ?? ''));
        if ($post_type === 'page' && $slot_type === 'anzeigenmarkt_top_banner') { $available[] = 'market:anzeigenmarkt'; }
        if ($primary !== '') {
            if ($post_type === 'page') { $available[] = 'page:' . $primary; $available[] = 'journal:' . $primary; }
            elseif ($post_type === 'category_archive') { $available[] = 'category:' . $primary; $available[] = 'journal:' . $primary; }
            elseif ($post_type === 'hp_listing_category_archive') { $available[] = 'market:' . $primary; }
            elseif ($post_type === 'uge_term') { $available[] = 'uge_term:' . $primary; }
            elseif ($post_type === 'pa_breed') { $available[] = 'pa_breed:' . $primary; }
            elseif ($post_type === 'uge_group_archive') { $available[] = 'uge_group:' . $primary; }
            elseif ($post_type === 'pa_breed_group_archive') { $available[] = 'pa_breed_group:' . $primary; }
        }
        foreach ((array) ($context['direct_term_slugs'] ?? array()) as $slug) {
            $slug = sanitize_key((string) $slug);
            if ($slug === '') { continue; }
            if ($post_type === 'post') { $available[] = 'category:' . $slug; $available[] = 'journal:' . $slug; }
            elseif ($post_type === 'hp_listing') { $available[] = 'market:' . $slug; }
            elseif ($post_type === 'uge_term') { $available[] = 'uge_group:' . $slug; }
            elseif ($post_type === 'pa_breed') { $available[] = 'pa_breed_group:' . $slug; }
        }
        $hierarchy_prefix='';
        if ($post_type==='page') { $hierarchy_prefix='page:'; }
        elseif ($post_type==='category_archive') { $hierarchy_prefix='category:'; }
        if ($hierarchy_prefix!=='' && $primary!=='') {
            $primary_key=$hierarchy_prefix.$primary;
            if (in_array($primary_key,$wanted,true)) return array('specificity'=>520,'matches'=>1,'reason'=>'Exakte Zielkante: '.$primary_key.'.');
            $ancestor_keys=array();
            foreach ((array)($context['slugs']??array()) as $slug) {
                $slug=sanitize_key((string)$slug);
                if ($slug!=='' && $slug!==$primary) { $ancestor_keys[]=$hierarchy_prefix.$slug; }
            }
            $ancestor_matches=array_values(array_intersect(array_unique($wanted),array_unique($ancestor_keys)));
            if ($ancestor_matches) return array('specificity'=>500,'matches'=>count($ancestor_matches),'reason'=>'Themenkreis über echte Vorfahren: '.implode(', ',$ancestor_matches).'.');
        }
        $matches = array_values(array_intersect(array_unique($wanted), array_unique($available)));
        if ($matches) return array('specificity'=>480,'matches'=>count($matches),'reason'=>'Automatische Zielkante: '.implode(', ',$matches).'.');
        return null;
    }

    private function prep_context($context, $slot_type) {
        $r=$context;
        $r['slot_type']=sanitize_key((string)$slot_type);
        $r['_ppar_norm_primary_slug']=sanitize_key((string)($context['primary_slug']??''));
        $r['_ppar_norm_post_type']=sanitize_key((string)($context['post_type']??''));
        $r['_ppar_norm_ancestor_ids']=isset($context['ancestor_ids'])&&is_array($context['ancestor_ids'])?array_map('intval',$context['ancestor_ids']):array();
        $r['_ppar_norm_slugs']=isset($context['slugs'])&&is_array($context['slugs'])?array_map('sanitize_key',$context['slugs']):array();
        $r['_ppar_norm_term_ids']=isset($context['term_ids'])&&is_array($context['term_ids'])?array_map('intval',$context['term_ids']):array();
        $r['_ppar_norm_direct_term_slugs']=isset($context['direct_term_slugs'])&&is_array($context['direct_term_slugs'])?array_values(array_filter(array_map('sanitize_key',$context['direct_term_slugs']))):array();
        $r['_ppar_norm_semantic_primary_target_key']=$this->automation_normalize_target_key((string)($context['semantic_primary_target_key']??''));
        $r['_ppar_norm_semantic_ancestor_target_keys']=array_values(array_filter(array_map(array($this,'automation_normalize_target_key'),(array)($context['semantic_ancestor_target_keys']??array()))));
        return $r;
    }

    public function run_gate() {
        $contexts=array(
            array('primary_slug'=>'mueslis-fuer-pferde','post_type'=>'page','slugs'=>array('mueslis-fuer-pferde','fuetterung-kraftfutter','fuetterung'),'ancestor_ids'=>array(11,12),'term_ids'=>array(),'direct_term_slugs'=>array(),'semantic_primary_target_key'=>'page:mueslis-fuer-pferde','semantic_ancestor_target_keys'=>array('page:fuetterung-kraftfutter','page:fuetterung'),'slot_type'=>'category_product_1'),
            array('primary_slug'=>'wasserkanister','post_type'=>'page','slugs'=>array('wasserkanister','fuetterung-wasser','fuetterung'),'ancestor_ids'=>array(21,22),'term_ids'=>array(),'direct_term_slugs'=>array(),'semantic_primary_target_key'=>'page:wasserkanister','semantic_ancestor_target_keys'=>array('page:fuetterung-wasser','page:fuetterung'),'slot_type'=>'category_product_2'),
            array('primary_slug'=>'haltungsberatung','post_type'=>'page','slugs'=>array('haltungsberatung','wissen-beratung-und-partner','wissen'),'ancestor_ids'=>array(31,32),'term_ids'=>array(),'direct_term_slugs'=>array(),'semantic_primary_target_key'=>'page:haltungsberatung','semantic_ancestor_target_keys'=>array('page:wissen-beratung-und-partner','page:wissen'),'slot_type'=>'category_product_3')
        );
        $campaigns=array();
        for($i=0;$i<5000;$i++){
            $ctx=$contexts[$i%count($contexts)];
            $target = ($i%4===0) ? $ctx['semantic_primary_target_key'] : (($i%4===1) ? $ctx['semantic_ancestor_target_keys'][0] : 'page:anderes-thema-'.$i);
            $campaigns[]=array(
                'automation_target_keys'=>array_values(array_unique(array_filter(array_map(array($this,'automation_normalize_target_key'),array($target,'journal:'.$ctx['primary_slug']))))),
                'match_slugs'=>array_map('sanitize_key',array($ctx['primary_slug'],'sonstiges')),
            );
        }

        $this->phase='old';
        $old=array();
        foreach($contexts as $context){
            foreach($campaigns as $campaign){ $old[]=$this->auto_rank_old($campaign,$context); }
        }
        $old_hits=$this->sanitize_hits['old'];

        $this->phase='new';
        $new=array();
        foreach($contexts as $context){
            $prepared=$this->prep_context($context,$context['slot_type']);
            foreach($campaigns as $campaign){ $new[]=$this->auto_rank_new($campaign,$prepared); }
        }
        $new_hits=$this->sanitize_hits['new'];

        return array(
            'old_hash'=>hash('sha256',serialize($old)),
            'new_hash'=>hash('sha256',serialize($new)),
            'old_sanitize_key'=>$old_hits,
            'new_sanitize_key'=>$new_hits,
            'rows'=>count($old),
        );
    }
}

add_action('template_redirect', function(){
    if (!isset($_GET['ranking_gate'])) { return; }
    $g=new PRG_Ranking_Gate();
    header('Content-Type: application/json');
    echo wp_json_encode($g->run_gate());
    exit;
}, -1000);
