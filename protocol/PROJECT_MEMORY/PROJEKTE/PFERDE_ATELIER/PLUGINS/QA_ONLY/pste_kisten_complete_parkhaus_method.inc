    /**
     * SINGLE read-only parkhouse export for the existing MINI batch.
     * Collects data, never performs or re-performs an SEO/intent decision.
     * Fail closed: missing WP, PSTE, editorial-plan or PSERC data never becomes FREI.
     */
    public static function readParkhausForMini(): array {
        $result=['contract'=>'PSTE_MINI_PARKHAUS_SNAPSHOT_V1','complete'=>false,
            'created_at_utc'=>gmdate('c'),'items'=>[],'sources'=>[],
            'sha256'=>'','reason'=>'PORTAL_INVENTORY_INCOMPLETE'];
        try {
            global $wpdb;
            if(!isset($wpdb)||!is_object($wpdb)||!method_exists($wpdb,'prepare')
                ||!method_exists($wpdb,'get_results')||!method_exists($wpdb,'get_var')
                ||!function_exists('get_post_types'))
                throw new RuntimeException('WP_READ_API_MISSING');
            $types=array_values(array_unique(array_filter(array_merge(['post','page'],
                array_values((array)get_post_types(['public'=>true],'names')),
                array_values((array)get_post_types(['publicly_queryable'=>true],'names'))),
                static fn($x)=>is_string($x)&&$x!==''&&$x!=='attachment')));
            sort($types,SORT_STRING);
            if(!$types)throw new RuntimeException('WP_PUBLIC_TYPES_MISSING');
            $states=['publish','draft','future','pending','private'];
            $placeholderTypes=implode(',',array_fill(0,count($types),'%s'));
            $placeholderStates=implode(',',array_fill(0,count($states),'%s'));
            $criteria="post_type IN ($placeholderTypes) AND post_status IN ($placeholderStates)";
            $params=array_merge($types,$states);
            $countSql=$wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->posts} WHERE ".$criteria,...$params);
            $before=(int)$wpdb->get_var($countSql);
            if((string)($wpdb->last_error??'')!=='')throw new RuntimeException('WP_COUNT_FAILED');
            $items=[];$cursor=0;
            while(true){
                $pageSql=$wpdb->prepare(
                    "SELECT ID,post_title,post_type,post_status,post_name,post_content,post_modified_gmt ".
                    "FROM {$wpdb->posts} WHERE ID>%d AND ".$criteria." ORDER BY ID ASC LIMIT 200",
                    $cursor,...$params);
                $rows=$wpdb->get_results($pageSql,defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
                if(!is_array($rows)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('WP_PAGE_READ_FAILED');
                if(!$rows)break;
                $ids=[];$index=[];
                foreach($rows as $row){
                    if(!is_array($row))$row=(array)$row;
                    $id=(int)($row['ID']??0);
                    if($id<=$cursor)throw new RuntimeException('WP_CURSOR_INVALID');
                    $cursor=$id;$ids[]=$id;
                    $content=(string)($row['post_content']??'');
                    preg_match_all('/<h[1-6][^>]*>(.*?)<\/h[1-6]>/isu',$content,$match);
                    $headings=array_values(array_map(static fn($h)=>trim(wp_strip_all_tags($h)),
                        (array)($match[1]??[])));
                    $items[]=['source'=>'WORDPRESS','id'=>$id,'title'=>(string)($row['post_title']??''),
                        'type'=>(string)($row['post_type']??''),'status'=>(string)($row['post_status']??''),
                        'slug'=>(string)($row['post_name']??''),'modified_gmt'=>(string)($row['post_modified_gmt']??''),
                        'headings'=>$headings,'content_sha256'=>hash('sha256',$content),
                        'target_keyword'=>'','canonical_article_id'=>'','plan_slot'=>'','categories'=>[]];
                    $index[$id]=count($items)-1;
                }
                $idList=implode(',',array_map('intval',$ids));
                $meta=$wpdb->get_results("SELECT post_id,meta_key,meta_value FROM {$wpdb->postmeta} ".
                    "WHERE meta_key IN ('_yoast_wpseo_focuskw','_ppm679_canonical_article_id','_ppm679_plan_slot_sha256') ".
                    "AND post_id IN ($idList) ORDER BY post_id ASC",
                    defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
                if(!is_array($meta)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('WP_SEO_META_READ_FAILED');
                foreach($meta as $row){if(!is_array($row))$row=(array)$row;$id=(int)($row['post_id']??0);
                    if(!isset($index[$id]))continue;
                    $metaKey=(string)($row['meta_key']??'');
                    if($metaKey==='_yoast_wpseo_focuskw')$items[$index[$id]]['target_keyword']=(string)($row['meta_value']??'');
                    elseif($metaKey==='_ppm679_canonical_article_id')$items[$index[$id]]['canonical_article_id']=(string)($row['meta_value']??'');
                    elseif($metaKey==='_ppm679_plan_slot_sha256')$items[$index[$id]]['plan_slot']=(string)($row['meta_value']??'');}
                $categories=$wpdb->get_results(
                    "SELECT tr.object_id AS post_id,tt.term_id AS category_id,t.name AS category_name ".
                    "FROM {$wpdb->term_relationships} tr ".
                    "INNER JOIN {$wpdb->term_taxonomy} tt ON tt.term_taxonomy_id=tr.term_taxonomy_id ".
                    "INNER JOIN {$wpdb->terms} t ON t.term_id=tt.term_id ".
                    "WHERE tt.taxonomy='category' AND tr.object_id IN ($idList) ORDER BY tr.object_id,tt.term_id",
                    defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
                if(!is_array($categories)||(string)($wpdb->last_error??'')!=='')
                    throw new RuntimeException('WP_CATEGORY_READ_FAILED');
                foreach($categories as $row){if(!is_array($row))$row=(array)$row;$id=(int)($row['post_id']??0);
                    if(isset($index[$id]))$items[$index[$id]]['categories'][]=[
                        'id'=>(int)($row['category_id']??0),'name'=>(string)($row['category_name']??'')];}
            }
            $after=(int)$wpdb->get_var($countSql);
            if((string)($wpdb->last_error??'')!==''||$before!==$after||count($items)!==$before)
                throw new RuntimeException('WP_INVENTORY_CHANGED_DURING_SCAN');
            $result['sources']['WORDPRESS']=['complete'=>true,'item_count'=>count($items),
                'post_types'=>$types,'statuses'=>$states];
            $result['items']=$items;

            $pool=PSTE_Repository::table('topic_pool');
            $planCountSql="SELECT COUNT(*) FROM $pool WHERE planning_suitability IN ('YES','PROVISIONAL')";
            $planBefore=(int)$wpdb->get_var($planCountSql);
            if((string)($wpdb->last_error??'')!=='')throw new RuntimeException('PSTE_PLAN_COUNT_FAILED');
            $psteCount=0;$last=0;
            while(true){
                $q=$wpdb->prepare("SELECT id,pool_key,candidate_id,payload_json,planning_suitability,automatic_pool_status ".
                    "FROM $pool WHERE id>%d AND planning_suitability IN ('YES','PROVISIONAL') ".
                    "ORDER BY id ASC LIMIT 200",$last);
                $rows=$wpdb->get_results($q,defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
                if(!is_array($rows)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('PSTE_PLAN_READ_FAILED');
                if(!$rows)break;
                foreach($rows as $row){if(!is_array($row))$row=(array)$row;
                    $id=(int)($row['id']??0);if($id<=$last)throw new RuntimeException('PSTE_PLAN_CURSOR_INVALID');$last=$id;
                    $data=json_decode((string)($row['payload_json']??''),true);
                    if(!is_array($data))throw new RuntimeException('PSTE_PLAN_INVALID_JSON');
                    $result['items'][]=['source'=>'PSTE_PLAN','pool_key'=>(string)($row['pool_key']??''),
                        'seo_topic_id'=>(string)($row['candidate_id']??$data['candidate_id']??''),
                        'raw_query'=>PSTE_Editorializer::sourceQuery($data),
                        'title'=>(string)($data['production_title']??$data['editorial_title']??''),
                        'target_keyword'=>(string)($data['target_keyword']??''),
                        'category'=>(string)($data['target_category_name']??''),
                        'article_type'=>(string)($data['proposed_article_type']??''),
                        'planning_suitability'=>(string)($row['planning_suitability']??''),
                        'status'=>(string)($row['automatic_pool_status']??''),
                        'plan_slot'=>(string)($data['plan_slot']??''),
                        'intent_profile'=>(array)($data['intent_profile']??[])];
                    $psteCount++;
                }
            }
            $planAfter=(int)$wpdb->get_var($planCountSql);
            if((string)($wpdb->last_error??'')!==''||$planBefore!==$planAfter||$psteCount!==$planBefore)
                throw new RuntimeException('PSTE_PLAN_CHANGED_DURING_SCAN');
            $result['sources']['PSTE_PLAN']=['complete'=>true,'item_count'=>$psteCount];

            // The optional imported editorial plan is already a read-only PSTE source.
            $editorial=PSTE_Snapshot::editorialPlan();
            $result['sources']['EDITORIAL_PLAN']=['status'=>(string)($editorial['status']??'NOT_AVAILABLE'),
                'sha256'=>(string)($editorial['sha256']??'NOT_AVAILABLE'),
                'item_count'=>count((array)($editorial['items']??[]))];
            foreach((array)($editorial['items']??[]) as $row){if(!is_array($row))continue;
                $result['items'][]=['source'=>'EDITORIAL_PLAN','status'=>(string)($row['status']??'PLANNED'),
                    'title'=>(string)($row['title']??''),'target_keyword'=>(string)($row['target_keyword']??''),
                    'plan_slot'=>(string)($row['plan_slot']??''),'article_type'=>(string)($row['article_type']??''),
                    'category'=>(string)($row['category_name']??'')];}

            $pserc=self::readExistingPsercPlanForParkhaus();
            $result['sources']['PSERC_ACTIVE_PLAN']=[
                'complete'=>!empty($pserc['complete']),'reason'=>(string)($pserc['reason']??''),
                'snapshot_sha256'=>(string)($pserc['snapshot_sha256']??''),
                'item_count'=>(int)($pserc['item_count']??0)];
            foreach((array)($pserc['items']??[]) as $item)if(is_array($item))$result['items'][]=$item;
            // Every actual source must be present and trustworthy. Editorial plan may
            // explicitly be NOT_AVAILABLE, as PSERC's own bound dependency contract allows.
            if(empty($pserc['complete']))throw new RuntimeException('PSERC_PLAN_NOT_PROVEN_COMPLETE');

            // Earlier externally approved slots live in the existing MINI option.
            // Show them to the same owner on later batches; no shadow database.
            $mini=self::loadState();$reservations=0;
            foreach((array)($mini['seo_decisions']??[]) as $key=>$receipt){
                if(!is_array($receipt)||($receipt['box']??'')!=='FREI')continue;
                $result['items'][]=['source'=>'MINI_RESERVED',
                    'pool_key'=>(string)$key,'title'=>(string)($receipt['approved_title']??''),
                    'raw_query'=>(string)($receipt['raw_query']??''),
                    'intent_slot'=>(string)($receipt['intent_slot']??''),
                    'status'=>'PLANNED','intent_summary'=>(string)($receipt['intent_summary']??'')];
                $reservations++;
            }
            $result['sources']['MINI_RESERVED']=['complete'=>true,'item_count'=>$reservations];
            $revisions=(array)($result['sources']??[]);
            $encoded=wp_json_encode(['sources'=>$revisions,'items'=>$result['items']],
                JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
            if(!is_string($encoded))throw new RuntimeException('PARKHAUS_ENCODING_FAILED');
            $result['sha256']=hash('sha256',$encoded);
            $result['complete']=true;$result['reason']='';
            return $result;
        } catch(Throwable $e) {
            // Incomplete source is NEVER semantic clearance. Keep the partial data
            // available for a technical diagnostic but no automatic FREI.
            $result['reason']=substr((string)$e->getMessage(),0,180);
            $result['sha256']='';
            $result['complete']=false;
            return $result;
        }
    }

