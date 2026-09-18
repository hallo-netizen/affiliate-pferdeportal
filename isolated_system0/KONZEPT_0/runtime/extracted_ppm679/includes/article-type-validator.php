<?php
if (!defined('ABSPATH')) { return; }

final class PPM679_Article_Type_Validator {
    const VERSION = '6.7.9';
    const CONTRACT_FILE = 'contracts/article-type-templates.json';
    const JOURNAL_CONTRACT_FILE = 'contracts/journal-article-type-release-v1.json';
    const GOLD_BINDING = 'FOUR_TYPE_APPROVED_GOLD_CORE_V1';
    const REQUIRED_TYPES = array('FAQ','Beratung','Vergleich','Pflege');
    const EVIDENCE_FIELDS = array('contract','version','article_type','definition_hash','positive_status','negative_status','gold_core_binding','evidence_hash');

    public static function load_contract() {
        $file = PPM679_PLUGIN_DIR . self::CONTRACT_FILE;
        if (!is_file($file)) { return null; }
        $decoded = json_decode((string) file_get_contents($file), true);
        return is_array($decoded) ? $decoded : null;
    }

    public static function validate($context, $server_state_hash = '') {
        $contract = self::load_contract();
        if (!is_array($contract)) {
            return array(PPM679_Diagnostic::error(
                'BLOCKED_ARTICLE_TYPE_CONTRACT_MISSING',
                'ARTICLE_TYPE_CONTRACT_MUST_EXIST_AND_BE_VALID_JSON',
                self::CONTRACT_FILE,
                'valid article_type_templates_v2 JSON',
                $contract,
                'Der aktive Beitragstypvertrag fehlt oder ist nicht lesbar.',
                $context,
                $server_state_hash,
                __CLASS__,
                null,
                array(self::CONTRACT_FILE)
            ));
        }

        $errors = array();
        $types = isset($contract['types']) && is_array($contract['types']) ? $contract['types'] : array();
        foreach (self::REQUIRED_TYPES as $index => $type) {
            if (!isset($types[$type]) || !is_array($types[$type])) {
                $errors[] = PPM679_Diagnostic::error(
                    'BLOCKED_ARTICLE_TYPE_DEFINITION_MISSING',
                    'ALL_FOUR_GOLD_CORE_TYPES_MUST_HAVE_ACTIVE_DEFINITIONS',
                    'types.' . $type,
                    'active definition',
                    isset($types[$type]) ? $types[$type] : null,
                    'Der fertige Beitragstyp ist im aktiven Vertrag nicht vollständig definiert.',
                    $context,
                    $server_state_hash,
                    __CLASS__,
                    $index,
                    array(self::CONTRACT_FILE)
                );
                continue;
            }
            $spec = $types[$type];
            if (empty($spec['production_allowed'])) {
                $errors[] = PPM679_Diagnostic::error(
                    'BLOCKED_ARTICLE_TYPE_NOT_PRODUCTION_ALLOWED',
                    'GOLD_CORE_TYPE_MUST_BE_DECLARED_PRODUCTION_ALLOWED',
                    'types.' . $type . '.production_allowed',
                    true,
                    isset($spec['production_allowed']) ? $spec['production_allowed'] : null,
                    'Der freigegebene Beitragstyp ist im aktiven Vertrag nicht für die Produktion freigeschaltet.',
                    $context,
                    $server_state_hash,
                    __CLASS__,
                    $index,
                    array(self::CONTRACT_FILE)
                );
            }
            $evidence = isset($spec['certification_evidence']) && is_array($spec['certification_evidence']) ? $spec['certification_evidence'] : array();
            foreach (self::EVIDENCE_FIELDS as $field) {
                if (!array_key_exists($field, $evidence) || $evidence[$field] === '') {
                    $errors[] = PPM679_Diagnostic::error(
                        'BLOCKED_ARTICLE_TYPE_EVIDENCE_FIELD_MISSING',
                        'ARTICLE_TYPE_EVIDENCE_MUST_MATCH_SCHEMA_V2',
                        'types.' . $type . '.certification_evidence.' . $field,
                        'non-empty field',
                        array_key_exists($field, $evidence) ? $evidence[$field] : null,
                        'Der Zertifizierungsbeleg enthält nicht das vom aktiven Validator erwartete Feld.',
                        $context,
                        $server_state_hash,
                        __CLASS__,
                        $index,
                        array(self::CONTRACT_FILE)
                    );
                }
            }
            if (isset($evidence['article_type']) && (string) $evidence['article_type'] !== $type) {
                $errors[] = PPM679_Diagnostic::error(
                    'BLOCKED_ARTICLE_TYPE_EVIDENCE_TYPE_MISMATCH',
                    'EVIDENCE_ARTICLE_TYPE_MUST_EQUAL_REGISTRY_KEY',
                    'types.' . $type . '.certification_evidence.article_type',
                    $type,
                    $evidence['article_type'],
                    'Der Zertifizierungsbeleg ist an einen anderen Beitragstyp gebunden.',
                    $context,
                    $server_state_hash,
                    __CLASS__,
                    $index,
                    array(self::CONTRACT_FILE)
                );
            }
            if (isset($evidence['gold_core_binding']) && (string) $evidence['gold_core_binding'] !== self::GOLD_BINDING) {
                $errors[] = PPM679_Diagnostic::error(
                    'BLOCKED_GOLD_CORE_BINDING_MISMATCH',
                    'EVIDENCE_MUST_BIND_TO_FOUR_TYPE_GOLD_CORE',
                    'types.' . $type . '.certification_evidence.gold_core_binding',
                    self::GOLD_BINDING,
                    $evidence['gold_core_binding'],
                    'Der Beitragstypbeleg ist nicht an den unveränderten Vier-Typ-Goldkern gebunden.',
                    $context,
                    $server_state_hash,
                    __CLASS__,
                    $index,
                    array(self::CONTRACT_FILE,'contracts/gold-core-binding-v1.json')
                );
            }
            if (isset($evidence['positive_status']) && (string) $evidence['positive_status'] !== 'STRUCTURAL_CHECK_OK') {
                $errors[] = PPM679_Diagnostic::error(
                    'BLOCKED_ARTICLE_TYPE_POSITIVE_EVIDENCE_STATUS',
                    'POSITIVE_EVIDENCE_MUST_BE_STRUCTURAL_CHECK_OK',
                    'types.' . $type . '.certification_evidence.positive_status',
                    'STRUCTURAL_CHECK_OK',
                    $evidence['positive_status'],
                    'Der positive Typbeleg verwendet einen unzulässigen oder veralteten Status.',
                    $context,
                    $server_state_hash,
                    __CLASS__,
                    $index,
                    array(self::CONTRACT_FILE)
                );
            }
            if (isset($evidence['negative_status']) && (string) $evidence['negative_status'] !== 'MUTATION_BLOCK_CHECK_OK') {
                $errors[] = PPM679_Diagnostic::error(
                    'BLOCKED_ARTICLE_TYPE_NEGATIVE_EVIDENCE_STATUS',
                    'NEGATIVE_EVIDENCE_MUST_BE_MUTATION_BLOCK_CHECK_OK',
                    'types.' . $type . '.certification_evidence.negative_status',
                    'MUTATION_BLOCK_CHECK_OK',
                    $evidence['negative_status'],
                    'Der negative Typbeleg verwendet einen unzulässigen oder veralteten Status.',
                    $context,
                    $server_state_hash,
                    __CLASS__,
                    $index,
                    array(self::CONTRACT_FILE)
                );
            }
        }
        $errors = array_merge($errors, PPM679_Article_Type_Extension_Registry::validate_manifest($context,$server_state_hash));
        foreach (PPM679_Article_Type_Extension_Registry::extension_display_names() as $extension_type) {
            $definition=self::type_definition($extension_type);
            $contract_file=(string)PPM679_Article_Type_Extension_Registry::capability($extension_type,'type_definition_contract','');
            $contract=$contract_file!==''?self::load_extension_contract($extension_type):null;
            if(!is_array($contract)||!is_array($definition)){
                $errors[]=PPM679_Diagnostic::error('BLOCKED_EXTENSION_ARTICLE_TYPE_CONTRACT_MISSING','EXTENSION_TYPE_REQUIRES_DECLARED_SIGNED_CAPABILITY_CONTRACT','extension_type_contract.'.$extension_type,'valid declared extension contract',$contract,'Der deklarierte Beitragsartvertrag der Erweiterung fehlt.',$context,$server_state_hash,__CLASS__,null,array($contract_file,PPM679_Article_Type_Extension_Registry::MANIFEST));
                continue;
            }
            $claimed=(string)($contract['contract_self_sha256']??'');$copy=$contract;unset($copy['contract_self_sha256']);$actual=PPM679_Diagnostic::stable_hash($copy);
            $evidence=(array)($definition['certification_evidence']??array());$defcopy=$definition;unset($defcopy['certification_evidence']);$definition_hash=PPM679_Diagnostic::stable_hash($defcopy);$evcopy=$evidence;unset($evcopy['evidence_hash']);$evidence_hash=PPM679_Diagnostic::stable_hash($evcopy);
            $required_validation=(string)PPM679_Article_Type_Extension_Registry::capability($extension_type,'validation_contract_required','');
            if($claimed===''||!hash_equals($claimed,$actual)||($definition['article_type']??'')!==$extension_type||($definition['production_allowed']??null)!==true||($definition['publish_allowed']??null)!==false||($definition['validation_contract_required']??'')!==$required_validation||($evidence['definition_hash']??'')!==$definition_hash||($evidence['evidence_hash']??'')!==$evidence_hash){
                $errors[]=PPM679_Diagnostic::error('BLOCKED_EXTENSION_ARTICLE_TYPE_CONTRACT_INVALID','EXTENSION_TYPE_CONTRACT_MUST_MATCH_DECLARED_CAPABILITIES','extension_type_contract.'.$extension_type,'hash-bound draft-only extension definition',$contract,'Der deklarierte Beitragsartvertrag ist nicht vollständig oder nicht selbstkonsistent.',$context,$server_state_hash,__CLASS__,null,array($contract_file,PPM679_Article_Type_Extension_Registry::MANIFEST));
            }
        }
        return $errors;
    }

    public static function load_journal_contract() { return self::load_extension_contract('Journal'); }

    public static function load_extension_contract($type) {
        $relative=(string)PPM679_Article_Type_Extension_Registry::capability($type,'type_definition_contract','');
        if($relative===''){return null;}$file=PPM679_PLUGIN_DIR.ltrim($relative,'/');
        if(!is_file($file)){return null;}$decoded=json_decode((string)file_get_contents($file),true);return is_array($decoded)?$decoded:null;
    }

    public static function type_definition($type) {
        if(PPM679_Article_Type_Extension_Registry::is_extension_type($type)){$extension=self::load_extension_contract($type);return is_array($extension)&&is_array($extension['type_definition']??null)?$extension['type_definition']:null;}
        $contract = self::load_contract();
        if (!is_array($contract) || empty($contract['types'][$type]) || !is_array($contract['types'][$type])) { return null; }
        return $contract['types'][$type];
    }
}
