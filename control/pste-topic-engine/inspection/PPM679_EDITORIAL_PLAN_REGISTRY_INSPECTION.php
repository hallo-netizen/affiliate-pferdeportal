<?php
if (!defined('ABSPATH')) { return; }

final class PPM679_Editorial_Plan_Registry {
    const CATEGORY_SOURCE='contracts/complete-portal-category-source-v1.json';
    const JOURNAL='contracts/journal-content-block-v1.json';
    const PLAN='contracts/canonical-complete-editorial-plan-v1.json';
    const INVENTORY='contracts/wordpress-content-inventory-reconciliation-v1.json';
    const GOVERNANCE='contracts/editorial-plan-governance-v1.json';
    const REIMPORT='contracts/versioned-category-reimport-v1.json';
    const RECONCILIATION='contracts/complete-editorial-plan-reconciliation-report-v1.json';

    private static $cache=array();

    public static function load($rel){
        if(isset(self::$cache[$rel])){return self::$cache[$rel];}
        $p=PPM679_PLUGIN_DIR.$rel;
        $d=is_file($p)?json_decode((string)file_get_contents($p),true):null;
        self::$cache[$rel]=is_array($d)?$d:null;
        return self::$cache[$rel];
    }
    public static function reset_cache(){self::$cache=array();}
    private static function self_hash_error($rel,$obj){
        if(!is_array($obj)){return self::err('BLOCKED_EDITORIAL_CONTRACT_MISSING','EDITORIAL_PLAN_CONTRACT_MUST_EXIST',$rel,'valid JSON',null,'Ein Vertrag des vollständigen Redaktionsplans fehlt.');}
        $declared=(string)($obj['contract_self_sha256']??'');$copy=$obj;unset($copy['contract_self_sha256']);
        $actual=PPM679_Diagnostic::stable_hash($copy);
        return ($declared!==''&&hash_equals($declared,$actual))?null:self::err('BLOCKED_EDITORIAL_CONTRACT_SELF_HASH','EDITORIAL_PLAN_CONTRACT_SELF_HASH_MUST_MATCH',$rel.'.contract_self_sha256',$actual,$declared,'Ein Vertrag des Redaktionsplans wurde verändert.');
    }
    public static function validate(){
        $errors=array();
        $contracts=array(self::CATEGORY_SOURCE,self::JOURNAL,self::PLAN,self::INVENTORY,self::GOVERNANCE,self::REIMPORT,self::RECONCILIATION);
        foreach($contracts as $rel){$e=self::self_hash_error($rel,self::load($rel));if($e){$errors[]=$e;}}
        if($errors){return $errors;}
        $source=self::load(self::CATEGORY_SOURCE);$journal=self::load(self::JOURNAL);$plan=self::load(self::PLAN);$inventory=self::load(self::INVENTORY);$gov=self::load(self::GOVERNANCE);
        $expected_files=array(
            'category_source_sha256'=>self::CATEGORY_SOURCE,
            'journal_registry_sha256'=>self::JOURNAL,
            'editorial_plan_sha256'=>self::PLAN,
            'inventory_reconciliation_sha256'=>self::INVENTORY,
            'category_reimport_sha256'=>self::REIMPORT,
            'reconciliation_report_sha256'=>self::RECONCILIATION
        );
        foreach($expected_files as $field=>$rel){$actual=hash_file('sha256',PPM679_PLUGIN_DIR.$rel);$decl=(string)($gov['bindings'][$field]??'');if($actual===''||!hash_equals($actual,$decl)){$errors[]=self::err('BLOCKED_EDITORIAL_BINDING_HASH','EDITORIAL_GOVERNANCE_MUST_BIND_EXACT_ACTIVE_CONTRACTS','governance.bindings.'.$field,$actual,$decl,'Der Governance-Vertrag bindet nicht den aktiven Planstand.');}}
        $sc=(array)($source['counts']??array());
        foreach(array('main_hubs'=>8,'section_hubs'=>59,'product_pages'=>329,'wordpress_target_categories'=>1124,'menu_items'=>1520) as $k=>$v){if((int)($sc[$k]??-1)!==$v){$errors[]=self::err('BLOCKED_COMPLETE_PORTAL_SOURCE_COUNT','COMPLETE_PORTAL_SOURCE_COUNTS_MUST_MATCH_BOUND_STRUCTURE','category_source.counts.'.$k,$v,$sc[$k]??null,'Die vollständige Portalquelle besitzt nicht die gebundene Strukturgröße.');}}
        $categories=(array)($source['categories']??array());$slugs=array();$ids=array();
        foreach($categories as $i=>$c){$slug=(string)($c['category_slug']??'');$id=(string)($c['stable_category_id']??'');if($slug===''||isset($slugs[$slug])||$id===''||isset($ids[$id])){$errors[]=self::err('BLOCKED_COMPLETE_PORTAL_SOURCE_IDENTITY','EVERY_PORTAL_CATEGORY_REQUIRES_UNIQUE_SLUG_AND_STABLE_ID','category_source.categories['.$i.']','unique stable id and slug',array('id'=>$id,'slug'=>$slug),'Eine Portal-Zielkategorie ist nicht eindeutig.');}$slugs[$slug]=true;$ids[$id]=true;if((int)($c['portal_level']??0)!==4||($c['expected_wp_parent_chain_required']??null)!==false||(int)($c['expected_wp_taxonomy_depth']??0)!==1){$errors[]=self::err('BLOCKED_COMPLETE_PORTAL_SOURCE_TOPOLOGY','PORTAL_LEVEL_FOUR_MUST_REMAIN_SEPARATE_FROM_FLAT_WORDPRESS_DEPTH_ONE','category_source.categories['.$i.']',array('portal_level'=>4,'wp_parent_required'=>false,'wp_depth'=>1),$c,'Portalpfad und WordPress-Taxonomietiefe wurden wieder vermischt.');}}
        if(count($categories)!==1124){$errors[]=self::err('BLOCKED_COMPLETE_PORTAL_SOURCE_INCOMPLETE','COMPLETE_PORTAL_SOURCE_MUST_CONTAIN_1124_TARGET_CATEGORIES','category_source.categories',1124,count($categories),'Die Portalquelle ist unvollständig.');}
        if((int)($journal['category_count']??-1)!==9||count((array)($journal['categories']??array()))!==9){$errors[]=self::err('BLOCKED_JOURNAL_CATEGORY_COUNT','JOURNAL_MUST_CONTAIN_EXACTLY_NINE_CONFIRMED_CATEGORIES','journal.categories',9,count((array)($journal['categories']??array())),'Die bestätigten acht Journal-Kategorien sind nicht vollständig registriert.');}
        foreach((array)($journal['categories']??array()) as $i=>$c){if((array)($c['allowed_article_types']??array())!==array('journal')||($c['draft_generation_allowed']??null)!==true||($c['publish_allowed']??null)!==false||(string)($c['slug']??'')==='pferdewissen-grundlagen'&&array_key_exists('wp_term_id',$c)){$errors[]=self::err('BLOCKED_JOURNAL_GOVERNANCE','JOURNAL_CATEGORIES_REQUIRE_SIGNED_JOURNAL_DRAFT_RELEASE_WITH_RUNTIME_ONLY_TERM_ID','journal.categories['.$i.']',array('journal only','draft true','publish false','new category has no hardcoded term id'),$c,'Die Journal-Kategorie weicht vom signierten Draft-Release oder der Runtime-ID-Regel ab.');}}
        $pc=(array)($plan['counts']??array());foreach(array('portal_categories'=>1124,'portal_slots'=>5620,'journal_categories'=>9,'journal_wissen_slots'=>0,'journal_legacy_wissen_slots'=>40,'journal_slots'=>45,'total_slots'=>5665) as $k=>$v){if((int)($pc[$k]??-1)!==$v){$errors[]=self::err('BLOCKED_EDITORIAL_PLAN_COUNT','CANONICAL_EDITORIAL_PLAN_COUNTS_MUST_MATCH',$k,$v,$pc[$k]??null,'Der kanonische Gesamtredaktionsplan ist unvollständig.');}}
        $slotids=array();$percat=array();foreach((array)($plan['slots']??array()) as $i=>$s){$id=(string)($s['canonical_article_id']??'');$cat=(string)($s['stable_category_id']??'');if($id===''||isset($slotids[$id])){$errors[]=self::err('BLOCKED_EDITORIAL_PLAN_DUPLICATE_ID','EVERY_PLAN_SLOT_REQUIRES_UNIQUE_CANONICAL_ARTICLE_ID','plan.slots['.$i.'].canonical_article_id','unique id',$id,'Eine kanonische Artikelidentität ist doppelt oder leer.');}$slotids[$id]=true;$percat[$cat]=($percat[$cat]??0)+1;if(($s['publish_allowed']??null)!==false){$errors[]=self::err('BLOCKED_EDITORIAL_AUTOPUBLISH','EVERY_EDITORIAL_PLAN_SLOT_MUST_FORBID_AUTOMATIC_PUBLISH','plan.slots['.$i.'].publish_allowed',false,$s['publish_allowed']??null,'Automatische Veröffentlichung ist im Gesamtplan verboten.');}if(strtolower((string)($s['article_type']??''))==='wissen'&&($s['draft_generation_allowed']??null)!==false){$errors[]=self::err('BLOCKED_WISSEN_DRAFT_ENABLED','LEGACY_WISSEN_DRAFTS_REMAIN_BLOCKED','plan.slots['.$i.'].draft_generation_allowed',false,$s['draft_generation_allowed']??null,'Legacy-Wissen darf keinen Entwurf erzeugen.');}if(strtolower((string)($s['article_type']??''))==='journal'&&(($s['draft_generation_allowed']??null)!==true||($s['publish_allowed']??null)!==false)){$errors[]=self::err('BLOCKED_JOURNAL_SLOT_RELEASE','JOURNAL_SLOT_REQUIRES_DRAFT_TRUE_AND_PUBLISH_FALSE','plan.slots['.$i.']',array('draft'=>true,'publish'=>false),$s,'Ein Journal-Planplatz besitzt nicht die signierte Draft-only-Freigabe.');}}
        if(count($slotids)!==5665){$errors[]=self::err('BLOCKED_EDITORIAL_PLAN_SLOT_COUNT','CANONICAL_EDITORIAL_PLAN_MUST_CONTAIN_5665_UNIQUE_SLOTS','plan.slots',5665,count($slotids),'Die Zahl eindeutiger Planpositionen stimmt nicht.');}
        foreach($percat as $cat=>$count){if($count!==5){$errors[]=self::err('BLOCKED_EDITORIAL_CATEGORY_SLOT_COUNT','EVERY_REGISTERED_CATEGORY_REQUIRES_FIVE_PLAN_SLOTS','plan.categories.'.$cat,5,$count,'Eine Kategorie besitzt nicht genau fünf Planpositionen.');}}
        if((int)($inventory['counts']['total']??-1)!==39||(int)($inventory['counts']['publish']??-1)!==12||(int)($inventory['counts']['draft']??-1)!==3||(int)($inventory['counts']['trash']??-1)!==24){$errors[]=self::err('BLOCKED_CONTENT_INVENTORY_BASELINE_COUNT','USER_SUPPLIED_CONTENT_INVENTORY_COUNTS_MUST_BIND_12_PUBLISH_3_DRAFT_24_TRASH','inventory.counts',array(39,12,3,24),$inventory['counts']??null,'Der mitgeteilte WordPress-Bestand ist nicht vollständig gebunden.');}
        if(($gov['publish_path_registered']??null)!==false||($gov['automatic_publish_allowed']??null)!==false||($gov['masterfile_is_runtime_source']??null)!==false){$errors[]=self::err('BLOCKED_EDITORIAL_GOVERNANCE_POLICY','PUBLISH_MUST_BE_FALSE_AND_MASTERFILE_MUST_NOT_BE_RUNTIME_DATABASE','governance',array('publish false','master runtime false'),$gov,'Eine zentrale Governance-Grenze wurde aufgeweicht.');}
        $reconciliation=self::load(self::RECONCILIATION);$rc=(array)($reconciliation['counts']??array());
        if((int)($rc['plan_positions']??-1)!==5665||(int)($rc['inventory_items']??-1)!==39||(int)($rc['canonical_inventory_groups']??-1)!==28){$errors[]=self::err('BLOCKED_EDITORIAL_RECONCILIATION_INCOMPLETE','RECONCILIATION_MUST_COVER_ALL_PLAN_POSITIONS_AND_USER_SUPPLIED_CONTENT','reconciliation.counts',array('plan_positions'=>5665,'inventory_items'=>39,'canonical_groups'=>28),$rc,'Der Gesamtplan ist nicht vollständig mit dem mitgeteilten WordPress-Bestand abgeglichen.');}
        return $errors;
    }
    public static function plan(){return self::load(self::PLAN);}
    public static function source(){return self::load(self::CATEGORY_SOURCE);}
    public static function journal(){return self::load(self::JOURNAL);}
    public static function baseline_inventory(){return self::load(self::INVENTORY);}
    public static function find_slot($candidate){
        $candidate=is_array($candidate)?$candidate:array();$plan=self::plan();
        $cid=trim((string)($candidate['canonical_article_id']??''));$key=trim((string)($candidate['plan_item_key']??''));$title=self::normalize_title((string)($candidate['title']??$candidate['topic']??''));$slug=trim((string)($candidate['category_slug']??''));$type=strtolower(trim((string)($candidate['article_type']??'')));
        $matches=array();
        foreach((array)($plan['slots']??array()) as $slot){
            if($cid!==''&&(string)($slot['canonical_article_id']??'')===$cid){return $slot;}
            if($key!==''&&in_array($key,(array)($slot['source_plan_item_keys']??array()),true)){return $slot;}
            $same_title=$title!==''&&self::normalize_title((string)($slot['working_title']??''))===$title;
            $same_slug=$slug===''||$slug===(string)($slot['category_slug']??'');
            $same_type=$type===''||$type===strtolower((string)($slot['article_type']??''));
            if($same_title&&$same_slug&&$same_type){$matches[]=$slot;}
        }
        return count($matches)===1?$matches[0]:null;
    }
    public static function normalize_title($s){$s=preg_replace('/^\s*\[[^\]]+\]\s*/u','',(string)$s);$s=function_exists('mb_strtolower')?mb_strtolower((string)$s,'UTF-8'):strtolower((string)$s);$s=strtr($s,array('ä'=>'ae','ö'=>'oe','ü'=>'ue','ß'=>'ss'));$s=preg_replace('/[^a-z0-9]+/u',' ',$s);return trim((string)$s);}
    public static function summary(){
        $plan=self::plan();$inv=self::baseline_inventory();return array('status'=>self::validate()?'BLOCKED':'EDITORIAL_PLAN_REGISTRY_VALID','portal_categories'=>(int)($plan['counts']['portal_categories']??0),'journal_categories'=>(int)($plan['counts']['journal_categories']??0),'total_slots'=>(int)($plan['counts']['total_slots']??0),'inventory_counts'=>$inv['counts']??array(),'publish_allowed'=>false,'wissen_draft_allowed'=>false,'journal_draft_allowed'=>true);
    }
    private static function err($code,$rule,$path,$expected,$actual,$reason){return PPM679_Diagnostic::error($code,$rule,$path,$expected,$actual,$reason,'editorial_plan_registry','',__CLASS__,null,array(self::CATEGORY_SOURCE,self::JOURNAL,self::PLAN,self::INVENTORY,self::GOVERNANCE,self::REIMPORT,self::RECONCILIATION));}
}
