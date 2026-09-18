<?php
if (!defined('ABSPATH')) { return; }

/**
 * Read-only consumer of the shared signed article-type extension manifest.
 * This class owns no routing/content decision. It only verifies and exposes
 * declarative extension capabilities to generic PPM admission gates.
 */
final class PPM679_Article_Type_Extension_Registry {
    const CONTRACT='ARTICLE_TYPE_EXTENSION_MANIFEST_V1';
    const MANIFEST='contracts/article-type-extension-manifest-v1.json';
    const SIGNATURE='contracts/article-type-extension-manifest-v1.sig';

    private static $cache=null;
    private static $error=null;

    public static function load(){
        if(self::$cache!==null||self::$error!==null)return self::$cache;
        $mf=PPM679_PLUGIN_DIR.self::MANIFEST;$sf=PPM679_PLUGIN_DIR.self::SIGNATURE;
        if(!is_file($mf)||!is_file($sf)){self::$error='MISSING';return null;}
        $bytes=(string)file_get_contents($mf);$d=json_decode($bytes,true);
        if(!is_array($d)||(string)($d['contract']??'')!==self::CONTRACT){self::$error='INVALID';return null;}
        if(!function_exists('sodium_crypto_sign_verify_detached')){self::$error='SODIUM';return null;}
        $sig=base64_decode(trim((string)file_get_contents($sf)),true);$pub=base64_decode((string)PPM679_BUILD_PUBLIC_KEY_B64,true);
        if(!is_string($sig)||!is_string($pub)||!sodium_crypto_sign_verify_detached($sig,$bytes,$pub)){self::$error='SIGNATURE';return null;}
        if((string)($d['selection_policy']??'')!=='EXPLICIT_SCOPE_AND_INTENT_ONLY_NO_FALLBACK'){self::$error='SELECTION_POLICY';return null;}
        $release=(array)($d['release_policy']??array());
        foreach(array('technical_pass_required','editorial_pass_required','e2e_pass_required_for_live_release','evidence_producer_must_differ_from_release_authority','manual_override_forbidden','review_never_equals_pass','unknown_never_equals_pass') as $k){if(($release[$k]??null)!==true){self::$error='RELEASE_POLICY';return null;}}
        self::$cache=$d;return self::$cache;
    }
    public static function error(){self::load();return self::$error;}
    public static function manifest_sha256(){return is_file(PPM679_PLUGIN_DIR.self::MANIFEST)?hash_file('sha256',PPM679_PLUGIN_DIR.self::MANIFEST):'';}
    public static function extension($type){
        $m=self::load();if(!is_array($m))return null;$want=strtolower(trim((string)$type));
        foreach((array)($m['extensions']??array()) as $id=>$ext){if(!is_array($ext))continue;$aliases=array_map(static function($v){return strtolower(trim((string)$v));},(array)($ext['aliases']??array()));$aliases[]=strtolower((string)$id);$aliases[]=strtolower((string)($ext['article_type_id']??''));if(in_array($want,$aliases,true))return $ext;}
        return null;
    }
    public static function display_name($type){$e=self::extension($type);return is_array($e)?(string)($e['display_name']??''):'';}
    public static function extension_display_names(){
        $m=self::load();$out=array();if(!is_array($m))return $out;foreach((array)($m['extensions']??array()) as $e){if(!is_array($e))continue;$n=(string)($e['display_name']??'');if($n!==''&&($e['handoff_policy']['draft_supported']??false)===true&&($e['handoff_policy']['publish_allowed']??true)===false)$out[]=$n;}return array_values(array_unique($out));
    }
    public static function allowed_normal_draft_types(){return array_merge(array('FAQ','Beratung','Vergleich','Pflege'),self::extension_display_names());}
    public static function is_extension_type($type){return is_array(self::extension($type));}
    public static function capability($type,$name,$default=null){$e=self::extension($type);return is_array($e)&&array_key_exists($name,(array)($e['ppm_capabilities']??array()))?$e['ppm_capabilities'][$name]:$default;}
    public static function requires_v5($type){$e=self::extension($type);return is_array($e)&&(string)($e['handoff_policy']['schema']??'')==='EXACT_FIVE_V1';}
    public static function validate_manifest($context,$server_state_hash=''){
        if(is_array(self::load()))return array();
        return array(PPM679_Diagnostic::error('BLOCKED_ARTICLE_TYPE_EXTENSION_MANIFEST','SIGNED_ARTICLE_TYPE_EXTENSION_MANIFEST_MUST_VERIFY','article_type_extension_manifest',self::CONTRACT,self::error(),'Die gemeinsame signierte Beitragsart-Registry fehlt, ist verändert oder verletzt den fail-closed Releasevertrag.',$context,$server_state_hash,__CLASS__,null,array(self::MANIFEST,self::SIGNATURE)));
    }
    public static function reset_test_state(){self::$cache=null;self::$error=null;}
}
