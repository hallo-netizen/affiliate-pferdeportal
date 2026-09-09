<?php
/*
 * ACM isolated candidate for the existing WORDPRESS_SIGNATURE_ENTRY_LOCK_V1.
 * It does not write content. It only verifies the existing
 * PSERC_APPROVED_PRODUCTION_PACKAGE_V1 before the existing import handoff.
 */
function acm_wp_fail($reason){ throw new RuntimeException((string)$reason); }

function acm_wp_sort_recursive($value){
    if($value instanceof stdClass){
        $vars=get_object_vars($value);
        ksort($vars,SORT_STRING);
        $obj=new stdClass();
        foreach($vars as $k=>$v)$obj->{$k}=acm_wp_sort_recursive($v);
        return $obj;
    }
    if(is_array($value)){
        $out=[];
        foreach($value as $v)$out[]=acm_wp_sort_recursive($v);
        return $out;
    }
    return $value;
}
function acm_wp_hash($value){
    $json=json_encode(acm_wp_sort_recursive($value),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
    if($json===false)acm_wp_fail('CANONICAL_JSON_FAILED');
    return hash('sha256',$json);
}
function acm_wp_exact_keys($value,$keys,$error){
    if(!is_array($value))acm_wp_fail($error);
    $a=array_keys($value);$b=array_values($keys);sort($a,SORT_STRING);sort($b,SORT_STRING);
    if($a!==$b)acm_wp_fail($error);
}
function acm_wp_verify_signed_package($path,$trustedKeys,$isBatchUsed){
    $raw=@file_get_contents($path);
    if($raw===false)acm_wp_fail('FINAL_JSON_MISSING');
    $pkgObj=json_decode($raw,false);
    $pkg=json_decode($raw,true);
    if(!($pkgObj instanceof stdClass)||!is_array($pkg))acm_wp_fail('FINAL_JSON_INVALID');
    $packageKeys=[
      'contract','fact_pack_bundle_sha256','production_plan_sha256',
      'workflow_release_sha256','package_id','source','fact_pack_bundle',
      'production_plan','workflow_release','package_payload_sha256'
    ];
    acm_wp_exact_keys($pkg,$packageKeys,'HANDOFF_PACKAGE_SCHEMA_INVALID');
    if(($pkg['contract']??'')!=='PSERC_APPROVED_PRODUCTION_PACKAGE_V1')acm_wp_fail('HANDOFF_PACKAGE_CONTRACT_INVALID');

    $bundle=$pkg['fact_pack_bundle'];$plan=$pkg['production_plan'];$release=$pkg['workflow_release'];
    if(!is_array($bundle)||!is_array($plan)||!is_array($release))acm_wp_fail('HANDOFF_PACKAGE_COMPONENT_INVALID');
    if(($bundle['contract']??'')!=='canonical_fact_pack_import_v1')acm_wp_fail('FACT_PACK_BUNDLE_CONTRACT_INVALID');
    if(($plan['contract']??'')!=='production_plan_v4')acm_wp_fail('PRODUCTION_PLAN_CONTRACT_INVALID');

    $bh=acm_wp_hash($pkgObj->fact_pack_bundle);$ph=acm_wp_hash($pkgObj->production_plan);$rh=acm_wp_hash($pkgObj->workflow_release);
    if(!hash_equals((string)($pkg['fact_pack_bundle_sha256']??''),$bh))acm_wp_fail('HANDOFF_COMPONENT_HASH_MISMATCH:fact_pack_bundle_sha256');
    if(!hash_equals((string)($pkg['production_plan_sha256']??''),$ph))acm_wp_fail('HANDOFF_COMPONENT_HASH_MISMATCH:production_plan_sha256');
    if(!hash_equals((string)($pkg['workflow_release_sha256']??''),$rh))acm_wp_fail('HANDOFF_COMPONENT_HASH_MISMATCH:workflow_release_sha256');
    $pid=acm_wp_hash(['contract'=>'PSERC_APPROVED_PRODUCTION_PACKAGE_V1','fact_pack_bundle_sha256'=>$bh,'production_plan_sha256'=>$ph,'workflow_release_sha256'=>$rh]);
    if(!hash_equals((string)($pkg['package_id']??''),$pid))acm_wp_fail('HANDOFF_PACKAGE_ID_MISMATCH');
    $copyObj=clone $pkgObj;$declared=(string)($pkg['package_payload_sha256']??'');unset($copyObj->package_payload_sha256);
    if(!hash_equals($declared,acm_wp_hash($copyObj)))acm_wp_fail('HANDOFF_PACKAGE_PAYLOAD_HASH_MISMATCH');

    if(($release['contract']??'')!=='WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED'||($release['status']??'')!=='PASS')acm_wp_fail('WORKFLOW_RELEASE_SHAPE_INVALID');
    if(($release['signature_algorithm']??'')!=='ED25519')acm_wp_fail('WORKFLOW_RELEASE_SIGNATURE_ALGORITHM_INVALID');
    if(($release['wordpress_write_performed']??null)!==false)acm_wp_fail('PREMATURE_WORDPRESS_WRITE_FORBIDDEN');

    $keyId=(string)($release['signing_key_id']??'');
    if(!isset($trustedKeys[$keyId])||!is_array($trustedKeys[$keyId]))acm_wp_fail('WORKFLOW_RELEASE_SIGNING_KEY_UNTRUSTED');
    $trusted=$trustedKeys[$keyId];
    $pub=base64_decode((string)($trusted['public_key_b64']??''),true);
    if($pub===false||strlen($pub)!==SODIUM_CRYPTO_SIGN_PUBLICKEYBYTES)acm_wp_fail('TRUSTED_PUBLIC_KEY_INVALID');
    $pubSha=hash('sha256',$pub);
    if(!hash_equals((string)($trusted['sha256']??''),$pubSha))acm_wp_fail('TRUSTED_PUBLIC_KEY_SHA_INVALID');
    if(!hash_equals((string)($release['signing_public_key_sha256']??''),$pubSha))acm_wp_fail('WORKFLOW_RELEASE_SIGNING_KEY_IDENTITY_MISMATCH');

    $payloadObj=clone $pkgObj->workflow_release;unset($payloadObj->release_payload_sha256,$payloadObj->signature_b64,$payloadObj->release_sha256);
    $payloadSha=acm_wp_hash($payloadObj);
    if(!hash_equals((string)($release['release_payload_sha256']??''),$payloadSha))acm_wp_fail('WORKFLOW_RELEASE_PAYLOAD_HASH_MISMATCH');
    $sig=base64_decode((string)($release['signature_b64']??''),true);
    if($sig===false||strlen($sig)!==SODIUM_CRYPTO_SIGN_BYTES)acm_wp_fail('WORKFLOW_RELEASE_SIGNATURE_ENCODING_INVALID');
    if(!sodium_crypto_sign_verify_detached($sig,$payloadSha,$pub))acm_wp_fail('WORKFLOW_RELEASE_SIGNATURE_INVALID');
    $releaseCopyObj=clone $pkgObj->workflow_release;unset($releaseCopyObj->release_sha256);
    if(!hash_equals((string)($release['release_sha256']??''),acm_wp_hash($releaseCopyObj)))acm_wp_fail('WORKFLOW_RELEASE_HASH_MISMATCH');

    $batch=(string)($release['exact_five_batch_sha256']??'');
    if(!preg_match('/^[0-9a-f]{64}$/',$batch))acm_wp_fail('BATCH_INVALID');
    if($isBatchUsed($batch))acm_wp_fail('BATCH_ALREADY_IMPORTED');

    $releaseItems=$release['items']??null;$planItems=$plan['items']??null;$packs=$bundle['fact_packs']??null;
    $count=(int)($release['exact_five_item_count']??-1);
    if(!is_array($releaseItems)||!is_array($planItems)||!is_array($packs)||$count<1)acm_wp_fail('FINAL_ITEM_SET_INVALID');
    if(count($releaseItems)!==$count||count($planItems)!==$count||count($packs)!==$count)acm_wp_fail('FINAL_ITEM_COUNT_MISMATCH');

    $planById=[];$sourceIds=[];
    foreach($planItems as $item){
        if(!is_array($item))acm_wp_fail('PRODUCTION_PLAN_ITEM_INVALID');
        if(array_key_exists('plan_slot',$item))acm_wp_fail('PPM_FOREIGN_PLAN_SLOT_FORBIDDEN');
        $cid=(string)($item['canonical_article_id']??'');
        if($cid===''||isset($planById[$cid]))acm_wp_fail('CANONICAL_ARTICLE_ID_INVALID_OR_DUPLICATE');
        $article=$item['canonical_article']??null;
        if(!is_array($article))acm_wp_fail('CANONICAL_ARTICLE_MISSING');
        $html=(string)($article['body_html']??'');
        if($html===''||!hash_equals((string)($article['body_html_sha256']??''),hash('sha256',$html)))acm_wp_fail('CANONICAL_ARTICLE_BODY_HASH_INVALID');
        $source=(string)($item['source_snapshot_id']??'');
        if($source==='')acm_wp_fail('SOURCE_SNAPSHOT_ID_MISSING');
        $sourceIds[$source]=true;$planById[$cid]=$item;
    }
    foreach($releaseItems as $row){
        acm_wp_exact_keys($row,['plan_slot','canonical_article_id'],'WORKFLOW_RELEASE_ITEM_SCHEMA_INVALID');
        $slot=(string)$row['plan_slot'];$cid=(string)$row['canonical_article_id'];
        if(!preg_match('/^[0-9a-f]{64}$/',$slot)||!isset($planById[$cid]))acm_wp_fail('WORKFLOW_RELEASE_ITEM_BINDING_INVALID');
    }
    foreach($packs as $pack){
        if(!is_array($pack))acm_wp_fail('FACT_PACK_INVALID');
        $sid=(string)($pack['source_snapshot_id']??'');
        if($sid===''||!isset($sourceIds[$sid]))acm_wp_fail('FACT_PACK_SOURCE_BINDING_INVALID');
    }

    return [
      'ok'=>true,
      'status'=>'SIGNED_JSON_VERIFIED_FOR_EXISTING_IMPORT_HANDOFF',
      'batch_sha256'=>$batch,
      'item_count'=>$count,
      'fact_pack_bundle'=>$bundle,
      'production_plan'=>$plan,
      'workflow_release'=>$release,
      'verified_before_first_write'=>true,
      'content_mutation_performed'=>false,
      'publish_allowed'=>false
    ];
}
?>