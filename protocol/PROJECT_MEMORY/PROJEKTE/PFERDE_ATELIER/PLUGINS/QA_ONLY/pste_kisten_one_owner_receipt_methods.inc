    /**
     * Same existing MINI admin import, not a new worker or review.
     * Receives the ONE external SEO decision; validates only source, time,
     * completeness, and that no two writes reserve the same slot.
     * No similarity calculation or title quality judgement.
     */
    public static function acceptSingleOwnerSeoDecisions(array $state,array $document,array $snapshot): array {
        if(($document['contract']??'')!=='PSTE_MINI_SEO_DECISIONS_V1'
            ||!is_array($document['items']??null)||!array_is_list($document['items']))
            throw new RuntimeException('PSTE_MINI_SEO_WRONG_DOCUMENT');
        if(empty($snapshot['complete'])||!preg_match('/^[a-f0-9]{64}$/D',(string)($snapshot['sha256']??''))
            ||!hash_equals((string)$snapshot['sha256'],(string)($document['snapshot_sha256']??'')))
            throw new RuntimeException('PSTE_MINI_SEO_PORTAL_PLAN_CHANGED_OR_INCOMPLETE');
        if(!isset($document['owner'])||$document['owner']!=='EXTERNAL_SINGLE_SEO_EDITOR')
            throw new RuntimeException('PSTE_MINI_SEO_OWNER_REQUIRED');
        $completed=(array)($state['completed']??[]);
        // Only check that an external BELEGT reference really identifies an
        // item in the original, read-only parkhouse. Never re-evaluate its
        // semantic similarity; that belongs to the ONE external owner.
        $existingReferences=[];
        foreach((array)($snapshot['items']??[]) as $existing){
            if(!is_array($existing))continue;
            $source=(string)($existing['source']??'');
            if($source==='')continue;
            foreach(['id','post_id','pool_key','seo_topic_id','canonical_article_id',
                'record_index','intent_slot','plan_slot'] as $field){
                if(!is_scalar($existing[$field]??null))continue;
                $identifier=trim((string)$existing[$field]);
                if($identifier!=='')$existingReferences[$source.':'.$identifier]=true;
            }
        }
        // One technical uniqueness check for the whole file, BEFORE any
        // approval is staged. Two rows for one source must never leave the
        // first FREI alive just because the second was skipped.
        $occurrences=[];
        foreach($document['items'] as $row){
            if(!is_array($row))continue;
            $id=(string)($row['pool_key']??'');
            if($id!=='')$occurrences[$id]=($occurrences[$id]??0)+1;
        }
        $updates=[];$clarification=[];$reserved=[];$seen=[];
        foreach((array)($state['seo_decisions']??[]) as $key=>$old){
            if(!is_array($old)||($old['box']??'')!=='FREI')continue;
            $oldSlot=(string)($old['intent_slot']??'');
            if($oldSlot!=='')$reserved[$oldSlot]=(string)$key;
        }
        foreach($document['items'] as $index=>$item){
            if(!is_array($item)){
                $clarification['UNKNOWN_ROW_'.$index]=[
                    'pool_key'=>'','reason_code'=>'SEO_RESULT_SHAPE_INVALID',
                    'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
                continue;
            }
            $key=(string)($item['pool_key']??'');
            if($key!==''&&($occurrences[$key]??0)>1){
                $clarification[$key]=[
                    'pool_key'=>$key,'reason_code'=>'SEO_DUPLICATE_SOURCE_ROWS',
                    'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
                // Invalidating a previous receipt is safer than reusing it
                // after a contradictory new upload. No semantic judgement.
                unset($state['seo_decisions'][$key]);
                continue;
            }
            if($key===''||!is_array($completed[$key]??null)){
                // Unknown/malformed row is not an authorized source. Other rows proceed.
                $clarification[$key!==''?$key:'UNKNOWN_ROW_'.count($seen)]=[
                    'pool_key'=>$key,'reason_code'=>'SEO_UNKNOWN_OR_DUPLICATE_SOURCE',
                    'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
                continue;
            }
            $seen[$key]=true;
            $saved=$completed[$key];$raw=(string)($saved['raw_query']??'');
            if($raw===''||($saved['decision']??'')!=='JA'
                ||!hash_equals($raw,(string)($item['raw_query']??''))
                ||!hash_equals(hash('sha256',$key.'|'.$raw),(string)($item['source_sha256']??''))){
                $clarification[$key]=['pool_key'=>$key,
                    'reason_code'=>'SEO_ORIGINAL_SOURCE_BINDING_FAILED',
                    'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
                unset($state['seo_decisions'][$key]);
                continue;
            }
            $box=(string)($item['box']??'');
            if(!in_array($box,['FREI','BELEGT','KLAERUNG'],true)){
                $box='KLAERUNG';$item['reason']='EDITORIAL_OUTCOME_MISSING';
            }
            $selected=(string)($saved['titles'][0]['title']??'');
            $intent=(string)($item['intent_summary']??'');
            $slot=(string)($item['intent_slot']??'');
            $match=(string)($item['matched_ref']??'');
            if($box==='FREI'&&($selected===''||($item['approved_title']??'')!==$selected
                ||trim($intent)===''||!preg_match('/^[a-f0-9]{64}$/D',$slot)
                ||(isset($reserved[$slot])&&$reserved[$slot]!==$key))){
                $box='KLAERUNG';$item['reason']='FREI_MISSING_OR_CONFLICTING_SOURCE_SLOT';
            }
            if($box==='BELEGT'&&($match===''||!isset($existingReferences[$match]))){
                $box='KLAERUNG';
                $item['reason']='BELEGT_REFERENCE_NOT_IN_EXISTING_PARKHAUS';
            }
            if($box==='FREI')$reserved[$slot]=$key;
            $receipt=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','pool_key'=>$key,
                'raw_query'=>$raw,'source_sha256'=>hash('sha256',$key.'|'.$raw),
                'snapshot_sha256'=>(string)$snapshot['sha256'],'box'=>$box,
                'intent_slot'=>$box==='FREI'?$slot:'',
                'matched_ref'=>$box==='BELEGT'?$match:'',
                'approved_title'=>$box==='FREI'?$selected:'',
                'intent_summary'=>$intent,
                'reason'=>$box==='KLAERUNG'?(string)($item['reason']??'EXTERNAL_UNCERTAIN'):'',
                'received_utc'=>gmdate('c')];
            $updates[$key]=$receipt;
            if($box==='KLAERUNG')$clarification[$key]=[
                'pool_key'=>$key,'reason_code'=>$receipt['reason'],
                'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
        }
        $state['seo_decisions']=array_replace((array)($state['seo_decisions']??[]),$updates);
        $state['clarification']=array_replace((array)($state['clarification']??[]),$clarification);
        foreach($updates as $key=>$receipt)if($receipt['box']!=='KLAERUNG')unset($state['clarification'][$key]);
        $count=['FREI'=>0,'BELEGT'=>0,'KLAERUNG'=>0];
        foreach($updates as $receipt)$count[$receipt['box']]++;
        foreach($clarification as $key=>$item)if(!isset($updates[$key]))$count['KLAERUNG']++;
        $state['seo_last_report']=['counts'=>$count,'snapshot_sha256'=>(string)$snapshot['sha256'],
            'received_utc'=>gmdate('c'),'semantic_evaluation_in_wordpress'=>false,
            'eligible_for_article_handoff'=>false];
        return $state;
    }

    /**
     * One existing WordPress option, atomically replaced only if it is still
     * the exact state read before the external verdict was accepted.
     * Prevents parallel receipts from claiming the same slot without adding
     * a lock table, second store, or any SEO check.
     */
    private static function storeSeoDecisionsIfUnchanged(array $before,array $after): void {
        global $wpdb;
        if(!is_object($wpdb)||empty($wpdb->options)
            ||!method_exists($wpdb,'prepare')||!method_exists($wpdb,'query')
            ||!function_exists('maybe_serialize'))
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_STORAGE_UNAVAILABLE');
        $old=maybe_serialize($before);
        $next=maybe_serialize($after);
        if(!is_string($old)||!is_string($next))
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_SERIALIZATION_FAILED');
        $sql=$wpdb->prepare(
            "UPDATE {$wpdb->options} SET option_value=%s WHERE option_name=%s AND BINARY option_value=BINARY %s",
            $next,self::STORE,$old);
        $changed=$wpdb->query($sql);
        if($changed!==1||((string)($wpdb->last_error??''))!=='')
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_CONFLICT_RELOAD_AND_RETRY');
        if(function_exists('wp_cache_delete')){
            wp_cache_delete(self::STORE,'options');
            wp_cache_delete('alloptions','options');
        }
        if(get_option(self::STORE,null)!==$after)
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_READBACK_FAILED');
    }

    public static function isMiniTopicAwaitingSeo(string $poolKey): bool {
        $state=self::loadState();
        $v=$state['completed'][$poolKey]??null;
        return is_array($v)&&($v['decision']??'')==='JA';
    }

    /**
     * The only technical proof reader for later WP/PSERC consumers.
     * No SEO evaluation, no new article decision.
     */
    public static function singleOwnerSeoFor(string $poolKey,string $rawQuery): array {
        $state=self::loadState();$data=(array)($state['seo_decisions'][$poolKey]??[]);
        $saved=(array)($state['completed'][$poolKey]??[]);
        if(($data['contract']??'')!=='PSTE_MINI_SEO_DECISIONS_V1'
            ||(string)($saved['decision']??'')!=='JA'||$poolKey===''||$rawQuery===''
            ||!hash_equals((string)($data['raw_query']??''),$rawQuery)
            ||!hash_equals((string)($saved['raw_query']??''),$rawQuery)
            ||!hash_equals(hash('sha256',$poolKey.'|'.$rawQuery),(string)($data['source_sha256']??''))
            ||(($data['box']??'')==='FREI'&&!hash_equals((string)($data['approved_title']??''),(string)($saved['titles'][0]['title']??''))))
            return [];
        return $data;
    }

