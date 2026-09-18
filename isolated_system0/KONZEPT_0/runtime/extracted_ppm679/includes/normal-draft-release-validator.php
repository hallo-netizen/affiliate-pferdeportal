<?php
if (!defined('ABSPATH')) { return; }
final class PPM679_Normal_Draft_Release_Validator {
    const VERSION='6.7.9';
    const CONTRACT='NORMAL_DRAFT_RELEASE_SCOPE_V1';
    const CONTRACT_FILE='contracts/normal-draft-release-v1.json';
    const SCOPE_MODE='REUSABLE_NORMAL_DRAFT_1_TO_4';
    const MIN_ARTICLES=1;
    const MAX_ARTICLES=4;

    public static function load(){
        $file=PPM679_PLUGIN_DIR.self::CONTRACT_FILE;
        $decoded=is_file($file)?json_decode((string)file_get_contents($file),true):null;
        return is_array($decoded)?$decoded:null;
    }
    public static function expected_scope($plan,$runtime){
        $items=array_values((array)($plan['items']??array()));
        $types=array(); foreach($items as $item){$types[]=(string)($item['article_type']??'');}
        return array(
            'contract'=>self::CONTRACT,
            'scope_mode'=>self::SCOPE_MODE,
            'release_contract_sha256'=>self::file_hash(self::CONTRACT_FILE),
            'plan_hash'=>PPM679_Diagnostic::stable_hash($plan),
            'request_id'=>(string)($runtime['request_id']??''),
            'server_instance_id'=>(string)($runtime['server_instance_id']??''),
            'user_id'=>(int)($runtime['user_id']??0),
            'nonce_verified'=>($runtime['nonce_verified']??false)===true,
            'user_triggered'=>($runtime['user_triggered']??false)===true,
            'article_count'=>count($items),
            'requested_article_types'=>$types,
            'minimum_articles'=>self::MIN_ARTICLES,
            'maximum_articles'=>self::MAX_ARTICLES,
            'maximum_articles_per_type'=>1,
            'publish_allowed'=>false,
            'wissen_allowed'=>true,
        );
    }
    public static function validate($action_context,$server_state_hash,$scope,$contract_override=null){
        $errors=array(); $contract=$contract_override!==null&&PPM679_WP::is_test_mode()?$contract_override:self::load();
        if(!is_array($scope)) return array(self::err('BLOCKED_NORMAL_RELEASE_SCOPE_MISSING','NORMAL_DRAFT_REQUIRES_EXPLICIT_RELEASE_SCOPE','scope','object',$scope,'Der normale Draft-Release-Scope fehlt.',$action_context,$server_state_hash));
        if(!is_array($contract)) return array(self::err('BLOCKED_NORMAL_RELEASE_CONTRACT_MISSING','NORMAL_DRAFT_RELEASE_CONTRACT_MUST_LOAD','contract',self::CONTRACT,$contract,'Der normale Draft-Freigabevertrag fehlt.',$action_context,$server_state_hash));
        $contexts=array_values((array)($contract['action_contexts']??array()));
        if(!in_array((string)$action_context,$contexts,true)) $errors[]=self::err('BLOCKED_NORMAL_RELEASE_ACTION_CONTEXT','NORMAL_DRAFT_ACTION_CONTEXT_MUST_BE_CONTRACT_BOUND','action_context',$contexts,$action_context,'Der normale Draftweg wurde in einem nicht freigegebenen Kontext aufgerufen.',$action_context,$server_state_hash);
        $claimed=(string)($contract['contract_self_sha256']??''); $copy=$contract; unset($copy['contract_self_sha256']); $actual=PPM679_Diagnostic::stable_hash($copy);
        if($claimed===''||!hash_equals($claimed,$actual)) $errors[]=self::err('BLOCKED_NORMAL_RELEASE_CONTRACT_HASH','NORMAL_DRAFT_RELEASE_CONTRACT_SELF_HASH_MUST_MATCH','contract.contract_self_sha256',$actual,$claimed,'Der normale Draft-Freigabevertrag wurde verändert.',$action_context,$server_state_hash);
        $exact=array('contract'=>self::CONTRACT,'scope_mode'=>self::SCOPE_MODE,'release_contract_sha256'=>self::file_hash(self::CONTRACT_FILE),'minimum_articles'=>1,'maximum_articles'=>4,'maximum_articles_per_type'=>1,'publish_allowed'=>false,'wissen_allowed'=>true);
        foreach($exact as $key=>$wanted){$got=$scope[$key]??null;if(PPM679_Diagnostic::stable_hash($wanted)!==PPM679_Diagnostic::stable_hash($got))$errors[]=self::err('BLOCKED_NORMAL_RELEASE_SCOPE_MISMATCH','NORMAL_DRAFT_RELEASE_SCOPE_MUST_MATCH_EXACTLY','scope.'.$key,$wanted,$got,'Der normale Draft-Scope weicht von der Freigabe ab.',$action_context,$server_state_hash);}
        $count=(int)($scope['article_count']??0); $types=array_values((array)($scope['requested_article_types']??array()));
        if($count<1||$count>4||count($types)!==$count) $errors[]=self::err('BLOCKED_NORMAL_RELEASE_CARDINALITY','NORMAL_DRAFT_REQUIRES_1_TO_4_ARTICLES','scope.article_count','1..4',$count,'Die Artikelanzahl liegt außerhalb der Freigabe.',$action_context,$server_state_hash);
        if(count(array_unique($types))!==count($types)) $errors[]=self::err('BLOCKED_NORMAL_RELEASE_DUPLICATE_TYPE','NORMAL_DRAFT_ALLOWS_EACH_TYPE_AT_MOST_ONCE','scope.requested_article_types','unique types',$types,'Ein Artikeltyp kommt mehrfach vor.',$action_context,$server_state_hash);
        $allowed=PPM679_Article_Type_Extension_Registry::allowed_normal_draft_types(); foreach($types as $type){if(!in_array($type,$allowed,true))$errors[]=self::err('BLOCKED_NORMAL_RELEASE_TYPE','NORMAL_DRAFT_ALLOWS_ONLY_SIGNED_RELEASE_TYPES','scope.requested_article_types',$allowed,$type,'Ein nicht freigegebener Artikeltyp wurde angefordert.',$action_context,$server_state_hash);}
        $errors=array_merge($errors,PPM679_Article_Type_Extension_Registry::validate_manifest($action_context,$server_state_hash));
        foreach($types as $type){
            if(!PPM679_Article_Type_Extension_Registry::is_extension_type($type))continue;
            $spec=PPM679_Article_Type_Validator::type_definition($type);$contract_file=(string)PPM679_Article_Type_Extension_Registry::capability($type,'type_definition_contract','');
            $required_validation=(string)PPM679_Article_Type_Extension_Registry::capability($type,'validation_contract_required','');
            if(!is_array($spec)||($spec['article_type']??'')!==$type||($spec['production_allowed']??null)!==true||($spec['publish_allowed']??null)!==false||($spec['validation_contract_required']??'')!==$required_validation){
                $errors[]=self::err('BLOCKED_NORMAL_RELEASE_EXTENSION_TYPE_DEFINITION','NORMAL_DRAFT_EXTENSION_TYPE_REQUIRES_SIGNED_DECLARATIVE_CAPABILITY','scope.requested_article_types','valid signed draft-only extension definition',$spec,'Eine registrierte Beitragsart besitzt keinen gültigen deklarativen Draft-Vertrag.',$action_context,$server_state_hash);
            }
            if($contract_file===''||!is_file(PPM679_PLUGIN_DIR.ltrim($contract_file,'/\\')))$errors[]=self::err('BLOCKED_NORMAL_RELEASE_EXTENSION_CONTRACT_FILE','NORMAL_DRAFT_EXTENSION_TYPE_CONTRACT_MUST_EXIST','scope.requested_article_types','declared type definition contract',$contract_file,'Der deklarierte Beitragstypvertrag der Erweiterung fehlt.',$action_context,$server_state_hash);
        }
        foreach(array('plan_hash','request_id','server_instance_id') as $f){$v=(string)($scope[$f]??'');if($v===''||($f==='plan_hash'&&!preg_match('/^[a-f0-9]{64}$/',$v)))$errors[]=self::err('BLOCKED_NORMAL_RELEASE_IDENTITY','NORMAL_DRAFT_SCOPE_REQUIRES_SERVER_BOUND_IDENTITY','scope.'.$f,'non-empty bound value',$v,'Eine serverseitige Laufbindung fehlt.',$action_context,$server_state_hash);}
        if((int)($scope['user_id']??0)<=0||($scope['nonce_verified']??false)!==true||($scope['user_triggered']??false)!==true)$errors[]=self::err('BLOCKED_NORMAL_RELEASE_USER_IDENTITY','NORMAL_DRAFT_REQUIRES_VERIFIED_SERVER_USER_REQUEST','scope.user_identity','verified user request',$scope,'Die serverseitig verifizierte Nutzeranforderung fehlt.',$action_context,$server_state_hash);
        $type_contract=PPM679_Article_Type_Validator::load_contract();
        foreach((array)($contract['type_bindings']??array()) as $type=>$binding){$spec=PPM679_Article_Type_Validator::type_definition($type);if(!is_array($spec)){$errors[]=self::err('BLOCKED_NORMAL_RELEASE_TYPE_BINDING','NORMAL_DRAFT_REQUIRES_UNCHANGED_TYPE_DEFINITION','types.'.$type,'defined',$spec,'Ein Artikeltyp fehlt.',$action_context,$server_state_hash);continue;}$actual_binding=array('production_allowed'=>$spec['production_allowed']??null,'certification_status'=>$spec['certification_status']??null,'definition_hash'=>$spec['certification_evidence']['definition_hash']??null,'evidence_hash'=>$spec['certification_evidence']['evidence_hash']??null);if(PPM679_Diagnostic::stable_hash($binding)!==PPM679_Diagnostic::stable_hash($actual_binding))$errors[]=self::err('BLOCKED_NORMAL_RELEASE_TYPE_BINDING','NORMAL_DRAFT_REQUIRES_UNCHANGED_TYPE_DEFINITION','types.'.$type,$binding,$actual_binding,'Die eingefrorene Artikeltypdefinition oder Evidenz wurde verändert.',$action_context,$server_state_hash);}
        $journal_policy=(array)($contract['journal_scope_policy']??array());
        $expected_journal_policy=array(
            'normal_affiliate_draft_requires_live_journal_snapshot'=>false,
            'journal_or_wissen_candidate_requires_live_journal_snapshot'=>true,
            'journal_registry_structural_validation_required_for_all_runs'=>true,
            'cross_block_duplicate_control_including_wissen_required_for_all_runs'=>true,
            'journal_mismatch_must_remain_visible_and_fail_closed_for_journal_or_wissen'=>true,
        );
        if(PPM679_Diagnostic::stable_hash($journal_policy)!==PPM679_Diagnostic::stable_hash($expected_journal_policy))$errors[]=self::err('BLOCKED_NORMAL_RELEASE_JOURNAL_SCOPE_POLICY','NORMAL_DRAFT_JOURNAL_SCOPE_POLICY_MUST_MATCH_EXACTLY','contract.journal_scope_policy',$expected_journal_policy,$journal_policy,'Die Trennung zwischen normaler Affiliate-Produktion und Journal/Wissen-Liveprüfung wurde verändert.',$action_context,$server_state_hash);
        foreach((array)($contract['protected_quality_hashes']??array()) as $relative=>$wanted){$got=self::file_hash($relative);if($got===''||!hash_equals((string)$wanted,$got))$errors[]=self::err('BLOCKED_NORMAL_RELEASE_QUALITY_HASH','PROTECTED_QUALITY_FILE_MUST_REMAIN_BYTE_IDENTICAL','protected_quality_hashes.'.$relative,$wanted,$got,'Eine geschützte Qualitäts- oder Inhaltsdatei wurde verändert.',$action_context,$server_state_hash);}
        return $errors;
    }
    private static function file_hash($relative){$file=PPM679_PLUGIN_DIR.ltrim((string)$relative,'/');return is_file($file)?hash_file('sha256',$file):'';}
    private static function err($code,$rule,$path,$expected,$actual,$reason,$context,$hash){return PPM679_Diagnostic::error($code,$rule,$path,$expected,$actual,$reason,$context,$hash,__CLASS__,null,array(self::CONTRACT_FILE,'contracts/article-type-templates.json'));}
}
