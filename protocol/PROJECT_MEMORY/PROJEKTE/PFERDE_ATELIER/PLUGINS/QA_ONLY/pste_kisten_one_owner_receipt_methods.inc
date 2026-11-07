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
        $updates=[];$clarification=[];$reserved=[];$seen=[];
        foreach($document['items'] as $item){
            if(!is_array($item))throw new RuntimeException('PSTE_MINI_SEO_RESULT_SHAPE_INVALID');
            $key=(string)($item['pool_key']??'');
            if($key===''||isset($seen[$key])||!is_array($completed[$key]??null))
                throw new RuntimeException('PSTE_MINI_SEO_UNKNOWN_OR_DUPLICATE_TOPIC');
            $seen[$key]=true;
            $saved=$completed[$key];$raw=(string)($saved['raw_query']??'');
            if($raw===''||($saved['decision']??'')!=='JA'
                ||!hash_equals($raw,(string)($item['raw_query']??''))
                ||!hash_equals(hash('sha256',$key.'|'.$raw),(string)($item['source_sha256']??'')))
                throw new RuntimeException('PSTE_MINI_SEO_ORIGINAL_SOURCE_BINDING_FAILED');
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
                ||isset($reserved[$slot]))){
                $box='KLAERUNG';$item['reason']='FREI_MISSING_OR_CONFLICTING_SOURCE_SLOT';
            }
            if($box==='BELEGT'&&$match===''){
                $box='KLAERUNG';$item['reason']='BELEGT_WITHOUT_SOURCE_REFERENCE';
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
        $state['seo_last_report']=['counts'=>$count,'snapshot_sha256'=>(string)$snapshot['sha256'],
            'received_utc'=>gmdate('c'),'semantic_evaluation_in_wordpress'=>false,
            'eligible_for_article_handoff'=>false];
        return $state;
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

