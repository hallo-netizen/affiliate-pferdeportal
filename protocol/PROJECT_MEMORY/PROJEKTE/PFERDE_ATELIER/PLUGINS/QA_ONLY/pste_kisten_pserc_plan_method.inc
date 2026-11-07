    /**
     * READ-ONLY parkhouse source from the already-existing PSERC plan snapshot.
     * No new semantic gate and no compiler invocation. Include READY and HELD
     * records, so a held intended article cannot silently disappear from inventory.
     */
    public static function readExistingPsercPlanForParkhaus(): array {
        $empty=['complete'=>false,'source'=>'PSERC_EXISTING_ACTIVE_PLAN','items'=>[],
            'generation'=>'','snapshot_sha256'=>'','reason'=>'PSERC_ACTIVE_PLAN_NOT_AVAILABLE'];
        if(!class_exists('PSERC_Plan_Snapshot_Store')
            ||!class_exists('PSERC_Plan_Dependency_Fingerprint'))return $empty;
        $head=PSERC_Plan_Snapshot_Store::getActive();
        if(!is_array($head)||!PSERC_Plan_Snapshot_Store::verifyHeader($head)
            ||!PSERC_Plan_Dependency_Fingerprint::isCurrent((array)($head['dependency']??[]))){
            $empty['reason']='PSERC_ACTIVE_PLAN_INCOMPLETE_OR_STALE';
            return $empty;
        }
        $generation=(string)($head['generation']??'');
        $count=$head['counts']['compiled_items']??null;
        if(!preg_match('/^[a-f0-9]{20}$/D',$generation)
            ||!is_int($count)||$count<0||$count>100000){
            $empty['reason']='PSERC_ACTIVE_PLAN_INVALID_GENERATION_OR_COUNT';
            return $empty;
        }
        $items=[];
        for($i=0;$i<$count;$i++){
            $row=PSERC_Plan_Snapshot_Store::getRecord($generation,'final_item',$i);
            if(!is_array($row)||($row['status']??'')===''){
                $empty['reason']='PSERC_ACTIVE_PLAN_RECORD_MISSING';
                return $empty;
            }
            $title=trim((string)($row['title']['production_title']??''));
            $keyword=trim((string)($row['target_keyword']['value']??''));
            $identity=trim((string)($row['seo_topic_id']??''));
            // An unfinished article title remains a valid *occupied or uncertain*
            // planning record; never hide it merely because the title is blank.
            $items[]=[
                'source'=>'PSERC_ACTIVE_PLAN','record_index'=>$i,'seo_topic_id'=>$identity,
                'title'=>$title,'target_keyword'=>$keyword,
                'article_type'=>(string)($row['article_type']??''),
                'category_slug'=>(string)($row['category']['slug']??''),
                'status'=>(string)$row['status'],
                'canonical_article_id'=>(string)($row['canonical_slot']['canonical_article_id']??''),
                'plan_slot'=>(string)($row['canonical_slot']['plan_slot_sha256']??''),
                'intent_profile'=>(array)($row['intent_profile']??[]),
            ];
        }
        $again=PSERC_Plan_Snapshot_Store::getActive();
        if(!PSERC_Plan_Snapshot_Store::verifyHeader((array)$again)
           ||!hash_equals((string)($head['snapshot_sha256']??''),
               (string)($again['snapshot_sha256']??''))
           ||!PSERC_Plan_Dependency_Fingerprint::isCurrent((array)($again['dependency']??[]))){
            $empty['reason']='PSERC_ACTIVE_PLAN_CHANGED_WHILE_READING';
            return $empty;
        }
        return ['complete'=>true,'source'=>'PSERC_EXISTING_ACTIVE_PLAN',
            'generation'=>$generation,
            'snapshot_sha256'=>(string)$head['snapshot_sha256'],
            'item_count'=>count($items),'items'=>$items,'reason'=>''];
    }

