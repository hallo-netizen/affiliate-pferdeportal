<?php
if (!class_exists('Pferde_Template_Kit')) {
    class Pferde_Template_Kit {
        public static function affiliate_contract_version(){ return '1.0'; }
        public static function design_profile(){ return 'pferde_atelier'; }
        public static function design_profile_contract_version(){ return '1.0'; }
        public static function affiliate_page_type($page_id){
            $p=get_post((int)$page_id);
            if(!$p) return '';
            $parent=(int)$p->post_parent;
            if($parent<=0) return 'hub1';
            $pp=get_post($parent);
            if($pp && (int)$pp->post_parent===0) return 'hub2';
            return 'category';
        }
    }
}
