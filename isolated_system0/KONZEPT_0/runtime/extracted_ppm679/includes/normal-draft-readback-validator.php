<?php
if (!defined('ABSPATH')) { return; }
final class PPM679_Normal_Draft_Readback_Validator {
    const VERSION='6.7.9';
    private static function meta($meta,$key){return (string)PPM679_WP::scalar_meta((array)$meta,$key);}
    private static function err($code,$path,$expected,$actual,$reason){return PPM679_Diagnostic::error($code,'NORMAL_DRAFT_READBACK_MUST_MATCH_EXACTLY',$path,$expected,$actual,$reason,'normal_draft_readback','',__CLASS__,null,array('includes/normal-draft-readback-validator.php'));}
    public static function validate($snapshot,$expected){
        $errors=array(); if(!is_array($snapshot))return array('ok'=>false,'status'=>'BLOCKED_NORMAL_READBACK_SNAPSHOT');
        if((string)($snapshot['post_status']??'')!=='draft')$errors[]=self::err('BLOCKED_NORMAL_READBACK_STATUS','post_status','draft',$snapshot['post_status']??null,'Der gespeicherte Beitrag ist kein Entwurf.');
        if((string)($snapshot['post_type']??'')!=='post')$errors[]=self::err('BLOCKED_NORMAL_READBACK_TYPE','post_type','post',$snapshot['post_type']??null,'Der gespeicherte Inhalt ist kein normaler Beitrag.');
        foreach(array('post_title'=>'title','post_name'=>'slug') as $field=>$expected_field){if((string)($snapshot[$field]??'')!==(string)($expected[$expected_field]??''))$errors[]=self::err('BLOCKED_NORMAL_READBACK_FIELD',$field,$expected[$expected_field]??null,$snapshot[$field]??null,'Ein gespeichertes Kernfeld weicht ab.');}
        $actual_hash=hash('sha256',(string)($snapshot['post_content']??'')); $wanted_hash=hash('sha256',(string)($expected['content']??''));
        if(!hash_equals($wanted_hash,$actual_hash))$errors[]=self::err('BLOCKED_NORMAL_READBACK_CONTENT_HASH','post_content_hash',$wanted_hash,$actual_hash,'Der gespeicherte Artikeltext ist nicht byteidentisch.');
        $actual_categories=array_values(array_map('intval',(array)($snapshot['category_ids']??array()))); $wanted_categories=array_values(array_map('intval',(array)($expected['categories']??array()))); sort($actual_categories);sort($wanted_categories);
        if($actual_categories!==$wanted_categories)$errors[]=self::err('BLOCKED_NORMAL_READBACK_CATEGORY','category_ids',$wanted_categories,$actual_categories,'Die gespeicherte Kategorie weicht ab.');
        $meta=(array)($snapshot['meta']??array());
        foreach(array('_ppm679_normal_draft','_ppm679_canonical_article_id','_ppm679_request_id','_ppm679_run_id','_ppm679_server_instance_id','_ppm679_user_id','_ppm679_build_manifest_sha256','_ppm679_plan_hash','_ppm679_content_hash','_ppm679_article_type','_ppm679_publish_blocked','_ppm679_category_slug','_ppm679_quality_binding_sha256','_ppm679_source_snapshot_id','_ppm679_planned_write_fingerprint') as $key){$wanted=(string)($expected['meta'][$key]??'');$actual=self::meta($meta,$key);if($wanted===''||$actual!==$wanted)$errors[]=self::err('BLOCKED_NORMAL_READBACK_META','meta.'.$key,$wanted,$actual,'Ein gespeichertes Herkunfts- oder Sperrmetafeld weicht ab.');}
        if(self::meta($meta,'_ppm679_publish_blocked')!=='1')$errors[]=self::err('BLOCKED_NORMAL_READBACK_PUBLISH','meta._ppm679_publish_blocked','1',self::meta($meta,'_ppm679_publish_blocked'),'Die Publish-Sperre fehlt.');
        $item=array('post_id'=>(int)($snapshot['ID']??0),'post_status'=>(string)($snapshot['post_status']??''),'article_type'=>self::meta($meta,'_ppm679_article_type'),'canonical_article_id'=>self::meta($meta,'_ppm679_canonical_article_id'),'title'=>(string)($snapshot['post_title']??''),'slug'=>(string)($snapshot['post_name']??''),'content_hash'=>$actual_hash,'category_ids'=>$actual_categories,'publish_allowed'=>false);
        if($errors)return array('ok'=>false,'status'=>'BLOCKED_NORMAL_DRAFT_READBACK','item'=>$item,'report'=>PPM679_Diagnostic::blocked($errors[0]['error_code'],$errors,'normal_draft_readback','',array('item'=>$item,'publish_allowed'=>false)));
        return array('ok'=>true,'status'=>'NORMAL_DRAFT_READBACK_PASS','item'=>$item,'report'=>PPM679_Diagnostic::ok('NORMAL_DRAFT_READBACK_PASS','normal_draft_readback','',array('item'=>$item,'publish_allowed'=>false)));
    }
    public static function validate_batch($snapshots,$expectations,$expected_count){
        $snapshots=array_values((array)$snapshots);$expectations=array_values((array)$expectations);$errors=array();$items=array();
        if($expected_count<1||$expected_count>4||count($snapshots)!==$expected_count||count($expectations)!==$expected_count)$errors[]=self::err('BLOCKED_NORMAL_READBACK_BATCH_COUNT','batch.count',$expected_count,array('snapshots'=>count($snapshots),'expectations'=>count($expectations)),'Die Readback-Menge stimmt nicht mit dem Produktionsplan überein.');
        for($i=0;$i<min(count($snapshots),count($expectations));$i++){$one=self::validate($snapshots[$i],$expectations[$i]);$items[]=$one['item']??array();if(empty($one['ok']))foreach((array)($one['report']['errors']??array()) as $error)$errors[]=$error;}
        if($errors)return array('ok'=>false,'status'=>'BLOCKED_NORMAL_DRAFT_READBACK_BATCH','items'=>$items,'report'=>PPM679_Diagnostic::blocked($errors[0]['error_code'],$errors,'normal_draft_readback_batch','',array('expected_count'=>$expected_count,'actual_count'=>count($snapshots),'publish_allowed'=>false)));
        return array('ok'=>true,'status'=>'NORMAL_DRAFT_READBACK_BATCH_PASS','items'=>$items,'report'=>PPM679_Diagnostic::ok('NORMAL_DRAFT_READBACK_BATCH_PASS','normal_draft_readback_batch','',array('expected_count'=>$expected_count,'actual_count'=>count($snapshots),'items'=>$items,'publish_allowed'=>false)));
    }
}
