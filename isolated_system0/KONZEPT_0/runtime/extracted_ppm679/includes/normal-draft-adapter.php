<?php
if (!defined('ABSPATH')) { return; }
final class PPM679_Normal_Draft_Adapter {
    const VERSION='6.7.9';
    const AUTH_CONTRACT='PPM679_NORMAL_ONE_USE_PAYLOAD_AUTH_V1';
    private static $issued=array();

    private static function payload_hash($payload){
        return PPM679_Diagnostic::stable_hash(array(
            'title'=>(string)($payload['title']??''),
            'content'=>(string)($payload['content']??''),
            'slug'=>(string)($payload['slug']??''),
            'meta'=>(array)($payload['meta']??array()),
            'categories'=>array_values(array_map('intval',(array)($payload['categories']??array())))
        ));
    }
    private static function err($code,$rule,$path,$expected,$actual,$reason,$state_hash=''){
        return PPM679_Diagnostic::error($code,$rule,$path,$expected,$actual,$reason,'normal_draft_write_gate',$state_hash,__CLASS__,null,array('includes/normal-draft-adapter.php','contracts/normal-draft-release-v1.json'));
    }
    public static function prepare($candidate,$plan_item,$evidence,$runtime,$run_id,$plan_hash,$state_hash=''){
        $errors=array(); $type=(string)($candidate['article_type']??'');
        $allowed=PPM679_Article_Type_Extension_Registry::allowed_normal_draft_types();
        if(!in_array($type,$allowed,true))$errors[]=self::err('BLOCKED_NORMAL_DRAFT_TYPE','NORMAL_DRAFT_ALLOWS_ONLY_CERTIFIED_TYPES','candidate.article_type',$allowed,$type,'Der Artikeltyp ist für den normalen Draftweg nicht freigegeben.',$state_hash);
        $candidate_hash=(string)($candidate['content_hash']??''); $checked_hash=(string)($evidence['content_hash']??'');
        if(($evidence['technical_status']??'')!=='TECHNICAL_CHECK_OK'||($evidence['content_quality_status']??'')!=='CONTENT_QUALITY_CHECK_OK'||$candidate_hash===''||$checked_hash===''||!hash_equals($candidate_hash,$checked_hash)){
            $errors[]=self::err('BLOCKED_NORMAL_DRAFT_DUAL_GATE','NORMAL_DRAFT_REQUIRES_TECHNICAL_AND_CONTENT_QUALITY_PASS_ON_EXACT_HASH','candidate.content_hash',array('technical'=>'TECHNICAL_CHECK_OK','quality'=>'CONTENT_QUALITY_CHECK_OK','hash'=>$candidate_hash),array('technical'=>$evidence['technical_status']??null,'quality'=>$evidence['content_quality_status']??null,'hash'=>$checked_hash),'Die unveränderten technischen und inhaltlichen Prüfungen sind nicht beide auf demselben Inhalt PASS.',$state_hash);
        }
        foreach(array('request_id','server_instance_id','build_manifest_sha256') as $field){$value=(string)($runtime[$field]??'');if($value==='')$errors[]=self::err('BLOCKED_NORMAL_DRAFT_IDENTITY','NORMAL_DRAFT_REQUIRES_SERVER_BOUND_IDENTITY','runtime.'.$field,'non-empty',$value,'Eine serverseitige Laufbindung fehlt.',$state_hash);}
        if((int)($runtime['user_id']??0)<=0||($runtime['nonce_verified']??false)!==true||($runtime['user_triggered']??false)!==true||!PPM679_WP::current_user_can_manage()){
            $errors[]=self::err('BLOCKED_NORMAL_DRAFT_USER_AUTH','NORMAL_DRAFT_REQUIRES_VERIFIED_MANAGE_OPTIONS_REQUEST','runtime.user','verified manage_options request',$runtime,'Die serverseitige Benutzerfreigabe fehlt.',$state_hash);
        }
        $quality=is_array($plan_item['quality_binding']??null)?$plan_item['quality_binding']:array();
        $category=is_array($quality['wordpress_category']??null)?$quality['wordpress_category']:(is_array($quality['expected_category']??null)?$quality['expected_category']:array());
        $slug=(string)($category['slug']??''); $name=(string)($category['name']??'');
        $matches=$slug!==''?PPM679_WP::find_category_terms_by_slug($slug,'category'):array();
        if(count($matches)!==1){$errors[]=self::err('BLOCKED_NORMAL_DRAFT_CATEGORY_RESOLUTION','NORMAL_DRAFT_CATEGORY_MUST_RESOLVE_TO_EXACTLY_ONE_LIVE_TERM','category.matches',1,count($matches),'Die Zielkategorie ist live nicht eindeutig auflösbar.',$state_hash);$term=null;}else{$term=$matches[0];if((string)($term['name']??'')!==$name||(string)($term['slug']??'')!==$slug||(string)($term['taxonomy']??'')!=='category')$errors[]=self::err('BLOCKED_NORMAL_DRAFT_CATEGORY_IDENTITY','NORMAL_DRAFT_CATEGORY_NAME_SLUG_AND_TAXONOMY_MUST_MATCH','category.binding',array('name'=>$name,'slug'=>$slug,'taxonomy'=>'category'),array('name'=>$term['name']??null,'slug'=>$term['slug']??null,'taxonomy'=>$term['taxonomy']??null),'Die Livekategorie weicht von der geprüften Bindung ab.',$state_hash);}
        $canonical_id=trim((string)($plan_item['canonical_article_id']??$plan_item['plan_item_key']??''));
        $title=(string)($candidate['title']??''); $post_slug=(string)($candidate['slug']??'');
        if($canonical_id===''||$title===''||$post_slug==='')$errors[]=self::err('BLOCKED_NORMAL_DRAFT_ARTICLE_IDENTITY','NORMAL_DRAFT_REQUIRES_CANONICAL_ID_TITLE_AND_SLUG','candidate.identity','non-empty',array($canonical_id,$title,$post_slug),'Die kanonische Artikelidentität ist unvollständig.',$state_hash);
        if($canonical_id!==''&&PPM679_WP::find_posts_by_meta_value('_ppm679_canonical_article_id',$canonical_id))$errors[]=self::err('BLOCKED_NORMAL_DRAFT_CANONICAL_DUPLICATE','CANONICAL_ARTICLE_ID_MUST_BE_UNUSED','candidate.canonical_article_id','unused',$canonical_id,'Der kanonische Planplatz ist bereits belegt.',$state_hash);
        if($post_slug!==''&&PPM679_WP::find_posts_by_slug($post_slug))$errors[]=self::err('BLOCKED_NORMAL_DRAFT_SLUG_DUPLICATE','NORMAL_DRAFT_SLUG_MUST_BE_UNUSED','candidate.slug','unused',$post_slug,'Der vorgesehene Slug ist bereits belegt.',$state_hash);
        $normal_title=PPM679_WP::sanitize_title($title); $title_hits=array();
        foreach(PPM679_WP::get_all_post_inventory(array('publish','draft','trash','private','pending','future')) as $post){if(PPM679_WP::sanitize_title((string)($post['title']??''))===$normal_title)$title_hits[]=$post;}
        if($title_hits)$errors[]=self::err('BLOCKED_NORMAL_DRAFT_TITLE_DUPLICATE','NORMAL_DRAFT_TITLE_MUST_BE_UNUSED','candidate.title','unused',$title_hits,'Ein bestehender Beitrag verwendet denselben normalisierten Titel.',$state_hash);
        if($errors)return array('ok'=>false,'errors'=>$errors,'report'=>PPM679_Diagnostic::blocked($errors[0]['error_code'],$errors,'normal_draft_prewrite',$state_hash));
        $quality_hash=(string)($plan_item['quality_binding_hash']??PPM679_Diagnostic::stable_hash($quality));
        $meta=array(
            '_ppm679_normal_draft'=>'1','_ppm679_canonical_article_id'=>$canonical_id,'_ppm679_request_id'=>(string)$runtime['request_id'],'_ppm679_run_id'=>(string)$run_id,
            '_ppm679_server_instance_id'=>(string)$runtime['server_instance_id'],'_ppm679_user_id'=>(string)(int)$runtime['user_id'],'_ppm679_build_manifest_sha256'=>(string)$runtime['build_manifest_sha256'],
            '_ppm679_plan_hash'=>(string)$plan_hash,'_ppm679_content_hash'=>$candidate_hash,'_ppm679_article_type'=>$type,'_ppm679_publish_blocked'=>'1',
            '_ppm679_category_slug'=>$slug,'_ppm679_quality_binding_sha256'=>$quality_hash,'_ppm679_source_snapshot_id'=>(string)($plan_item['source_snapshot_id']??'')
        );
        $payload=array('title'=>$title,'content'=>(string)$candidate['content_html'],'slug'=>$post_slug,'meta'=>$meta,'categories'=>array((int)$term['term_id']));
        $fingerprint=PPM679_Diagnostic::stable_hash(array('payload'=>$payload,'request_id'=>$runtime['request_id'],'run_id'=>$run_id,'plan_hash'=>$plan_hash));
        $payload['meta']['_ppm679_planned_write_fingerprint']=$fingerprint;
        return array('ok'=>true,'payload'=>$payload,'expected'=>$payload,'canonical_article_id'=>$canonical_id,'plan_item_key'=>(string)($plan_item['plan_item_key']??$canonical_id),'article_type'=>$type,'planned_write_fingerprint'=>$fingerprint);
    }
    public static function issue_write_authorization($prepared){
        if(empty($prepared['ok'])||!is_array($prepared['payload']??null))return array('ok'=>false);
        $hash=self::payload_hash($prepared['payload']); $token='normal-auth-'.substr(hash('sha256',$hash.'|'.microtime(true).'|'.mt_rand()),0,40);
        self::$issued[$token]=array('payload_hash'=>$hash,'consumed'=>false);
        return array('ok'=>true,'authorization'=>array('contract'=>self::AUTH_CONTRACT,'token'=>$token,'payload_hash'=>$hash));
    }
    public static function verify_write_authorization($auth,$payload,$consume=false){
        if(!is_array($auth)||($auth['contract']??'')!==self::AUTH_CONTRACT)return false;
        $token=(string)($auth['token']??''); $hash=self::payload_hash($payload);
        if($token===''||!isset(self::$issued[$token])||self::$issued[$token]['consumed']||!hash_equals(self::$issued[$token]['payload_hash'],$hash)||!hash_equals((string)($auth['payload_hash']??''),$hash))return false;
        if($consume)self::$issued[$token]['consumed']=true; return true;
    }
    public static function create_draft($prepared){
        $auth=self::issue_write_authorization($prepared); if(empty($auth['ok']))return array('ok'=>false,'status'=>'BLOCKED_NORMAL_DRAFT_AUTH');
        $p=$prepared['payload']; $post_id=PPM679_WP::insert_draft($p['title'],$p['content'],$p['slug'],$p['meta'],$p['categories'],$auth['authorization']);
        if(is_object($post_id)||(int)$post_id<=0)return array('ok'=>false,'status'=>'BLOCKED_NORMAL_DRAFT_INSERT','actual'=>$post_id);
        return array('ok'=>true,'post_id'=>(int)$post_id,'expected'=>$prepared['expected'],'canonical_article_id'=>$prepared['canonical_article_id'],'plan_item_key'=>$prepared['plan_item_key'],'article_type'=>$prepared['article_type']);
    }
    public static function reset_test_state(){self::$issued=array();}
}
