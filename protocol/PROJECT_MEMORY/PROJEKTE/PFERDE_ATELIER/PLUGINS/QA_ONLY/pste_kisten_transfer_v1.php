<?php
declare(strict_types=1);
/**
 * QA reference for the existing MINI import path; NOT a new semantic gate, worker or WP plugin.
 * No title, query equivalence, keyword or content evaluation occurs here.
 * The real MINI importer must reuse its existing source checks and atomic writer.
 */
final class PsteKistenTransferV1 {
    private const BOXES = ['FREI', 'BELEGT', 'KLAERUNG'];

    /**
     * @param array $snapshot Complete, immutable manifest from the existing WordPress source
     * @param array $responses Items already judged by THE ONE external editorial owner
     * @param callable $reserve Existing atomic slot writer: (string $slotKey, array $item): bool.
     */
    public static function distribute(array $snapshot, array $responses, callable $reserve): array {
        $out=['FREI'=>[], 'BELEGT'=>[], 'KLAERUNG'=>[], 'system_blocked'=>false];
        if(($snapshot['complete']??null)!==true ||
           !self::digest((string)($snapshot['sha256']??'')) ||
           !is_array($snapshot['originals']??null) ||
           !is_string($snapshot['current_sha256']??null) ||
           !hash_equals((string)$snapshot['sha256'], (string)$snapshot['current_sha256'])) {
            return ['FREI'=>[], 'BELEGT'=>[], 'KLAERUNG'=>[], 'system_blocked'=>true,
                'reason'=>'PORTAL_SNAPSHOT_INCOMPLETE_OR_STALE'];
        }
        $seen=[];
        foreach($responses as $item) {
            $id=is_array($item)?(string)($item['pool_key']??''):'';
            // Per-item isolation. A broken item cannot block a valid sibling.
            if($id==='' || isset($seen[$id]) || !is_array($item)) {
                $out['KLAERUNG'][]=['pool_key'=>$id,'reason'=>'INVALID_OR_DUPLICATE_ITEM_ID'];
                continue;
            }
            $seen[$id]=true;
            $original=$snapshot['originals'][$id]??null;
            if(!is_array($original) ||
               !is_string($original['raw_query']??null) ||
               !hash_equals((string)($original['raw_query']??''),(string)($item['raw_query']??'')) ||
               !hash_equals((string)($snapshot['sha256']??''),(string)($item['snapshot_sha256']??'')) ||
               !self::digest((string)($item['source_sha256']??'')) ||
               !hash_equals((string)($original['source_sha256']??''),(string)($item['source_sha256']??''))) {
                $out['KLAERUNG'][]=['pool_key'=>$id,'reason'=>'SOURCE_OR_SNAPSHOT_MISMATCH'];
                continue;
            }
            $box=(string)($item['box']??'');
            if(!in_array($box,self::BOXES,true)) {
                $out['KLAERUNG'][]=['pool_key'=>$id,'reason'=>'MISSING_EXTERNAL_DECISION'];
                continue;
            }
            if($box==='BELEGT') {
                $match=(string)($item['matched_ref']??'');
                if($match==='') {
                    $out['KLAERUNG'][]=['pool_key'=>$id,'reason'=>'DUPLICATE_WITHOUT_SOURCE'];
                    continue;
                }
                $out['BELEGT'][]=['pool_key'=>$id,'matched_ref'=>$match];
                continue;
            }
            if($box==='KLAERUNG') {
                $out['KLAERUNG'][]=['pool_key'=>$id,'reason'=>(string)($item['reason']??'EXTERNAL_REVIEW'),
                    'alternative_intent'=>(string)($item['alternative_intent']??'')];
                continue;
            }
            // FREI: never infer a free slot from a different title alone.
            $slot=(string)($item['intent_slot']??'');
            $title=trim((string)($item['approved_title']??''));
            $receipt=trim((string)($item['editorial_receipt']??''));
            if($slot===''||$title===''||$receipt==='') {
                $out['KLAERUNG'][]=['pool_key'=>$id,'reason'=>'EDITORIAL_RECEIPT_OR_SLOT_MISSING'];
                continue;
            }
            try {
                // Atomic storage/uniqueness is required here, not another SEO/semantic scan.
                $written=$reserve($slot,$item)===true;
            } catch (Throwable $e) {
                $written=false;
            }
            if(!$written){
                $out['KLAERUNG'][]=['pool_key'=>$id,'reason'=>'SLOT_WRITE_OR_CONCURRENT_RESERVATION_FAILED'];
                continue;
            }
            $out['FREI'][]=['pool_key'=>$id,'intent_slot'=>$slot,'approved_title'=>$title,
                'editorial_receipt'=>$receipt];
        }
        return $out;
    }

    private static function digest(string $value): bool {
        return preg_match('/^[a-f0-9]{64}$/D',$value)===1;
    }
}
