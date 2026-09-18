<?php
if (!defined('ABSPATH')) { return; }

final class PPM679_Content_Generator {
    const VERSION='6.7.9';
    const VALIDATION_CONTRACT_V5='SECTION_REQUIREMENTS_V1';

    public static function generate($item,$fact_pack) {
        if (!is_array($item) || !is_array($fact_pack)) {
            return array('ok'=>false,'error'=>'CANONICAL_RUNTIME_INPUT_INVALID');
        }
        $order=isset($item['runtime_order'])&&is_array($item['runtime_order'])?$item['runtime_order']:array();
        $article=isset($item['canonical_article'])&&is_array($item['canonical_article'])?$item['canonical_article']:array();
        $type=(string)($item['article_type']??'');
        $topic=trim((string)($item['topic']??''));
        $snapshot_id=(string)($item['source_snapshot_id']??'');
        $validation_contract=(string)($item['validation_contract_version']??'');
        $is_v5=$validation_contract===self::VALIDATION_CONTRACT_V5;
        if ($validation_contract!=='' && !$is_v5) {
            return array('ok'=>false,'error'=>'VALIDATION_CONTRACT_VERSION_UNKNOWN','actual'=>$validation_contract);
        }

        $required_order=array('order_id','article_type','title','slug','subject_scope','subject_label','lead','conclusion','links');
        foreach ($required_order as $field) {
            if (!array_key_exists($field,$order) || $order[$field]==='' || $order[$field]===array()) {
                return array('ok'=>false,'error'=>'CANONICAL_RUNTIME_ORDER_INCOMPLETE','field'=>$field);
            }
        }
        $required_article=array('order_id','article_type','title','slug','body_html','body_text','content_plan_hash');
        if ($is_v5) { $required_article[]='validation_contract_version'; $required_article[]='section_requirements_hash'; }
        foreach ($required_article as $field) {
            if (!array_key_exists($field,$article) || $article[$field]==='') {
                return array('ok'=>false,'error'=>'CANONICAL_ARTICLE_PAYLOAD_INCOMPLETE','field'=>$field);
            }
        }
        if ((string)$order['article_type']!==$type || (string)$article['article_type']!==$type) {
            return array('ok'=>false,'error'=>'CANONICAL_ARTICLE_TYPE_MISMATCH');
        }
        if ((string)$order['order_id']!==(string)$article['order_id']) {
            return array('ok'=>false,'error'=>'CANONICAL_ORDER_ARTICLE_ID_MISMATCH');
        }
        if ((string)$order['title']!==(string)$article['title'] || $topic!==(string)$article['title']) {
            return array('ok'=>false,'error'=>'CANONICAL_TITLE_BINDING_MISMATCH');
        }
        if ((string)$order['slug']!==(string)$article['slug']) {
            return array('ok'=>false,'error'=>'CANONICAL_SLUG_BINDING_MISMATCH');
        }
        if ((string)($fact_pack['fact_pack_id']??'')!==$snapshot_id) {
            return array('ok'=>false,'error'=>'CANONICAL_FACT_PACK_ID_BINDING_MISMATCH');
        }
        if ((string)($fact_pack['article_type']??'')!==$type || (string)($fact_pack['title_scope']??'')!==(string)$order['subject_scope']) {
            return array('ok'=>false,'error'=>'CANONICAL_FACT_PACK_SCOPE_MISMATCH');
        }
        if ((string)($fact_pack['status']??'')!=='SOURCE_VERIFIED_PRODUCTION_READY') {
            return array('ok'=>false,'error'=>'CANONICAL_FACT_PACK_NOT_READY');
        }
        $claims=isset($fact_pack['claims'])&&is_array($fact_pack['claims'])?$fact_pack['claims']:array();
        if (count($claims)<3) {
            return array('ok'=>false,'error'=>'CANONICAL_FACT_PACK_CLAIMS_INCOMPLETE');
        }

        $html=(string)$article['body_html'];
        $text=self::plain_text($html);
        if ($text!==(string)$article['body_text']) {
            return array('ok'=>false,'error'=>'CANONICAL_ARTICLE_TEXT_BINDING_MISMATCH');
        }
        $declared_hash=(string)($article['body_html_sha256']??'');
        $actual_hash=hash('sha256',$html);
        if ($declared_hash==='' || !hash_equals($actual_hash,$declared_hash)) {
            return array('ok'=>false,'error'=>'CANONICAL_ARTICLE_HASH_BINDING_MISMATCH','expected'=>$actual_hash,'actual'=>$declared_hash);
        }
        if ($is_v5) {
            $requirements=isset($item['section_requirements'])&&is_array($item['section_requirements'])?$item['section_requirements']:null;
            $requirements_hash=strtolower(trim((string)($item['section_requirements_hash']??'')));
            if (!is_array($requirements) || (string)($requirements['contract']??'')!==self::VALIDATION_CONTRACT_V5 || !isset($requirements['sections']) || !is_array($requirements['sections']) || !$requirements['sections']) {
                return array('ok'=>false,'error'=>'VALIDATION_CONTRACT_PAYLOAD_INCOMPLETE');
            }
            $actual_requirements_hash=PPM679_Diagnostic::stable_hash($requirements);
            if (!preg_match('/^[0-9a-f]{64}$/',$requirements_hash) || !hash_equals($actual_requirements_hash,$requirements_hash)) {
                return array('ok'=>false,'error'=>'SECTION_REQUIREMENTS_HASH_MISMATCH','expected'=>$actual_requirements_hash,'actual'=>$requirements_hash);
            }
            if ((string)($article['validation_contract_version']??'')!==self::VALIDATION_CONTRACT_V5 || !hash_equals($requirements_hash,strtolower(trim((string)($article['section_requirements_hash']??''))))) {
                return array('ok'=>false,'error'=>'CANONICAL_ARTICLE_VALIDATION_BINDING_MISMATCH');
            }
        } else {
            if (substr_count($html,'class="ppm-source-trace"')<3) {
                return array('ok'=>false,'error'=>'CANONICAL_ARTICLE_SOURCE_TRACE_INCOMPLETE');
            }
            foreach ($claims as $claim) {
                $source_id=(string)($claim['source_id']??'');
                $evidence_hash=strtolower(trim((string)($claim['evidence_text_sha256']??'')));
                if ($source_id==='' || !preg_match('/^[0-9a-f]{64}$/',$evidence_hash)) {
                    return array('ok'=>false,'error'=>'CANONICAL_CLAIM_SOURCE_BINDING_INVALID');
                }
                if (strpos($html,'data-source-hash="'.self::e($evidence_hash).'"')===false || strpos($html,'data-source-title="'.self::e($source_id).'"')===false) {
                    return array('ok'=>false,'error'=>'CANONICAL_ARTICLE_CLAIM_TRACE_MISSING','fact_id'=>$claim['fact_id']??null);
                }
            }
        }

        $safe_html=PPM679_WP::kses_post($html);
        if ($safe_html!==$html) {
            return array('ok'=>false,'error'=>'CANONICAL_ARTICLE_WORDPRESS_SANITIZATION_DRIFT');
        }
        return array(
            'ok'=>true,
            'article_type'=>$type,
            'title'=>(string)$article['title'],
            'slug'=>(string)$article['slug'],
            'content_html'=>$html,
            'content_hash'=>$actual_hash,
            'source_snapshot_id'=>$snapshot_id,
            'fact_pack_hash'=>PPM679_Diagnostic::stable_hash($fact_pack),
            'canonical_order_id'=>(string)$order['order_id'],
            'content_plan_hash'=>(string)$article['content_plan_hash'],
            'generator_path'=>'17_RULE_EXECUTION_CHAIN/tools/build_cross_domain_articles.py',
            'validation_contract_version'=>$is_v5?self::VALIDATION_CONTRACT_V5:'PPM679_LEGACY_V1',
            'section_requirements_hash'=>$is_v5?(string)$item['section_requirements_hash']:null
        );
    }

    private static function plain_text($html) {
        $text=html_entity_decode((string)$html,ENT_QUOTES|ENT_HTML5,'UTF-8');
        $text=(string)preg_replace('/<[^>]+>/u',' ',$text);
        return trim((string)preg_replace('/\s+/u',' ',$text));
    }

    private static function e($value) {
        return htmlspecialchars((string)$value,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');
    }
}
