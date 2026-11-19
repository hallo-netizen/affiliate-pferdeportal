<?php
/**
 * Strict read-only technical bridge for historical PSTE topic metadata.
 * Never makes an SEO, category or article-type decision. Never changes PSTE data.
 */
if (!defined('ABSPATH')) { return; }
final class TXE_Legacy_Source_Bridge {
    public static function recover(array $proofs): array {
        $keys=[];
        foreach($proofs as $key=>$proof) {
            if(!is_array($proof) || ($proof['box']??'')!=='FREI')continue;
            $key=(string)$key;$raw=trim((string)($proof['raw_query']??''));
            if(!preg_match('/^[a-f0-9-]{32,64}$/D',$key)||$raw==='')continue;
            if(($proof['contract']??'')!=='PSTE_MINI_SEO_DECISIONS_V1')continue;
            if(!hash_equals(hash('sha256',$key.'|'.$raw),(string)($proof['source_sha256']??'')))continue;
            // A complete original receipt has its own signed/verified source of truth.
            // Do not demand another DB lookup or create a second approval path.
            $alreadyComplete=true;
            foreach(['category_slug','article_type','canonical_article_id','plan_slot'] as $f)
                if(trim((string)($proof[$f]??''))===''){$alreadyComplete=false;break;}
            if(!$alreadyComplete)$keys[]=$key;
        }
        $rows=self::readRows(array_values(array_unique($keys)));
        $out=[];$reasonCounts=[];
        foreach($proofs as $key=>$proof) {
            if(!is_array($proof)||($proof['box']??'')!=='FREI')continue;
            $key=(string)$key;$reason='ORIGINAL_SOURCE_NOT_FOUND';
            $resolved=['category_slug'=>'','article_type'=>'','canonical_article_id'=>'','plan_slot'=>''];
            $raw=trim((string)($proof['raw_query']??''));
            if(!in_array($key,$keys,true)) {
                $complete=true;
                foreach(['category_slug','article_type','canonical_article_id','plan_slot'] as $field)
                    if(trim((string)($proof[$field]??''))===''){$complete=false;break;}
                $reason=$complete?'ALREADY_COMPLETE_IN_ORIGINAL_RECEIPT':'ORIGINAL_RECEIPT_INVALID';
            } elseif(isset($rows[$key])) {
                $row=$rows[$key];$candidate=json_decode((string)($row['payload_json']??''),true);
                if(!is_array($candidate))$candidate=[];
                // The pool UUID and raw query must identify exactly the previously approved topic.
                $storedRaw=trim((string)($candidate['raw_query']??$candidate['query_record']['raw_query']??''));
                if($storedRaw!=='' && !hash_equals($storedRaw,$raw))$reason='ORIGINAL_SOURCE_QUERY_CONFLICT';
                else {
                    $meta=self::savedMetadata($row,$candidate);
                    if($meta===null)$reason='ORIGINAL_EDITORIAL_METADATA_NOT_FINAL';
                    else {
                        $cat=$meta['category_slug'];$type=$meta['article_type'];
                        $priorCat=trim((string)($proof['category_slug']??''));
                        $priorType=trim((string)($proof['article_type']??''));
                        if(($priorCat!==''&&!hash_equals($priorCat,$cat))||($priorType!==''&&!hash_equals($priorType,$type)))$reason='ORIGINAL_EDITORIAL_METADATA_CONFLICT';
                        elseif(!class_exists('PSERC_Plan_Slot_Identity')||!method_exists('PSERC_Plan_Slot_Identity','tokenFromCanonicalId'))$reason='ORIGINAL_SLOT_FUNCTION_MISSING';
                        else {
                            // pool_key is the already stored original identity, NOT a newly minted id.
                            $canonical=trim((string)($proof['canonical_article_id']??''));
                            if($canonical==='')$canonical=$key;
                            $slot=PSERC_Plan_Slot_Identity::tokenFromCanonicalId($canonical);
                            $previousSlot=trim((string)($proof['plan_slot']??''));
                            if($previousSlot!==''&&!hash_equals($previousSlot,$slot))$reason='ORIGINAL_SLOT_IDENTITY_CONFLICT';
                            else {
                                $resolved=['category_slug'=>$cat,'article_type'=>$type,
                                    'canonical_article_id'=>$canonical,'plan_slot'=>$slot];
                                $reason='RECOVERED_FROM_ORIGINAL_PSTE';
                            }
                        }
                    }
                }
            }
            $out[$key]=['data'=>$resolved,'reason'=>$reason];
            $reasonCounts[$reason]=($reasonCounts[$reason]??0)+1;
        }
        return ['items'=>$out,'counts'=>$reasonCounts];
    }

    private static function savedMetadata(array $row,array $candidate): ?array {
        $manual=(string)($row['manual_status']??'');
        $catId=0;$type='';
        if($manual==='APPROVED') {
            $catId=(int)($row['manual_category_id']??0);
            $type=trim((string)($row['manual_article_type']??''));
        } elseif($manual==='' && (string)($row['automatic_pool_status']??'')==='AUTO_RESOLVED'
            && (string)($row['planning_suitability']??'')==='YES'
            && in_array((string)($row['context_state']??''),['CURRENT','NOT_REQUIRED'],true)) {
            $path=$candidate['normal_metadata_path']??null;
            if(!is_array($path)||($path['contract']??'')!=='PSTE_NORMAL_METADATA_PATH_V2'
                ||($path['status']??'')!=='NORMAL_PASS'||empty($path['ok']))return null;
            $catId=(int)($path['target_category']['term_id']??0);
            $type=trim((string)($path['article_type']??''));
            if($catId!==(int)($row['current_category_id']??0)
                || $type!==trim((string)($candidate['proposed_article_type']??'')))return null;
        } else return null;
        if($catId<=0 || $type==='' || strlen($type)>64)return null;
        $term=function_exists('get_term')?get_term($catId,'category'):(function_exists('get_term_by')?get_term_by('id',$catId,'category'):false);
        if(!is_object($term)|| (function_exists('is_wp_error') && is_wp_error($term))
            ||(int)($term->term_id??0)!==$catId || trim((string)($term->slug??''))==='')return null;
        return ['category_slug'=>(string)$term->slug,'article_type'=>$type];
    }

    private static function readRows(array $keys): array {
        if(!$keys)return [];
        global $wpdb;
        if(!isset($wpdb)||!method_exists($wpdb,'prepare')||!method_exists($wpdb,'get_results')
            ||!class_exists('PSTE_Repository'))throw new RuntimeException('ORIGINAL_PSTE_POOL_READER_NOT_AVAILABLE');
        $table=PSTE_Repository::table('topic_pool');$out=[];
        foreach(array_chunk($keys,40) as $part) {
            $q=implode(',',array_fill(0,count($part),'%s'));
            $sql=$wpdb->prepare("SELECT * FROM {$table} WHERE pool_key IN ({$q})",...$part);
            $found=$wpdb->get_results($sql,defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
            if(!is_array($found)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('ORIGINAL_PSTE_POOL_READ_FAILED');
            foreach($found as $row) {
                if(!is_array($row))continue;
                $key=(string)($row['pool_key']??'');
                if(in_array($key,$part,true)) {
                    if(isset($out[$key]))throw new RuntimeException('ORIGINAL_PSTE_POOL_DUPLICATE_KEY');
                    $out[$key]=$row;
                }
            }
        }
        return $out;
    }
}
