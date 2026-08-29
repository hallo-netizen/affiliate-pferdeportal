<?php
if (!defined('ABSPATH')) { return; }

/** Persistent, fail-closed orchestrator for fixed or target-driven broad longtail research waves. */
final class PSTE_Breadth_Research_Queue {
    public const CONTRACT='PSTE_BREADTH_RESEARCH_QUEUE_V1';
    public const VERSION='1.5.0';
    private const COMPATIBLE_VERSIONS=['1.0.0','1.1.0','1.2.0','1.3.0','1.4.0','1.5.0'];
    private const QUEUE_LOCK_TTL=120;
    private const MAX_ITEMS=40;
    private const LEGACY_MAX_ITEMS=4;
    private const DEFAULT_TARGET_USABLE=40;
    private const DEFAULT_MAX_ITEMS=40;
    private const TRANSIENT_COORDINATION_CODES=['PSTE_RESEARCH_STEP_ALREADY_RUNNING','PSTE_SANDBOX_LOCKED','PSTE_BUDGET_RESERVATION_LOCKED'];
    private const REPLAY_SAFE_LOCAL_FINALIZE_CODES=['PSTE_SANDBOX_DATAFLOW_NORMAL_PATH_RAW_MISMATCH','PSTE_SNAPSHOT_STALE_OR_CHANGED','PSTE_RESEARCH_FINALIZE_PREPARE_COUNT_MISMATCH'];

    public static function start(int $requestedCount,array $settings): array {
        // Legacy bounded breadth mode remains available for compatibility.
        return self::startQueue('FIXED_FAMILY_COUNT',0,max(1,min(self::LEGACY_MAX_ITEMS,$requestedCount)),max(1,min(self::LEGACY_MAX_ITEMS,$requestedCount)),$settings);
    }

    public static function startUntil(int $targetUsable,int $maxItems,array $settings): array {
        $targetUsable=max(1,min(200,$targetUsable>0?$targetUsable:self::DEFAULT_TARGET_USABLE));
        $maxItems=max(1,min(self::MAX_ITEMS,$maxItems>0?$maxItems:self::DEFAULT_MAX_ITEMS));
        return self::startQueue('TARGET_USABLE_CANDIDATES',$targetUsable,$maxItems,1,$settings);
    }

    private static function startQueue(string $mode,int $targetUsable,int $maxItems,int $initialItems,array $settings): array {
        PSTE_Plugin::assertReady();
        $existing=self::raw();
        if(is_array($existing)&&in_array((string)($existing['status']??''),['RUNNING','PAUSED_ERROR','OUTCOME_UNKNOWN'],true))throw new RuntimeException('PSTE_BREADTH_QUEUE_ALREADY_ACTIVE');
        if(PSTE_Research_Job::current()!==null)throw new RuntimeException('PSTE_RESEARCH_JOB_ALREADY_ACTIVE');
        $baseline=get_option(PSTE_OPTION_SITE_BASELINE,[]);
        if(!is_array($baseline)||($baseline['contract']??'')!=='PSTE_SITE_BASELINE_V1')throw new RuntimeException('PSTE_SITE_BASELINE_REQUIRED');
        $rebase=PSTE_Snapshot::rebaseResearchBaselineIfSafe($baseline);if(empty($rebase['ok']))throw new RuntimeException((string)($rebase['error_code']??'PSTE_SITE_BASELINE_STALE'));
        $baseline=(array)$rebase['baseline'];
        $candidates=self::openFamilies($baseline);
        if(!$candidates&&$mode!=='TARGET_USABLE_CANDIDATES')throw new RuntimeException('PSTE_BREADTH_NO_OPEN_FAMILIES');
        $selected=$candidates?self::spread($candidates,max(1,min($maxItems,$initialItems))):[];
        $baselineUsable=[];$contextBinding=[];
        if($mode==='TARGET_USABLE_CANDIDATES'){
            $baselineUsable=PSTE_Repository::usablePlanningTopicKeys();
            $context=PSTE_Context_Refresh::status();if((string)($context['status']??'')!=='COMPLETE')throw new RuntimeException('PSTE_PRODUCTION_WAVE_CONTEXT_COMPLETE_REQUIRED');
            $contextBinding=PSTE_Context_Index_Store::runtimeBinding($context,$baseline);
        }
        self::clearCancelRequest();$uuid=wp_generate_uuid4();$now=gmdate('c');
        $items=[];
        foreach($selected as $row)$items[]=self::queueItem($row);
        $queue=[
            'contract'=>self::CONTRACT,'version'=>self::VERSION,'queue_uuid'=>$uuid,'status'=>'RUNNING',
            'mode'=>$mode,'requested_count'=>$mode==='FIXED_FAMILY_COUNT'?count($items):$targetUsable,
            'target_usable'=>$targetUsable,'max_items'=>$maxItems,'usable_candidate_count'=>0,'raw_usable_candidate_count'=>0,'usable_topic_keys'=>[],'baseline_usable_topic_keys'=>$baselineUsable,'completion_reason'=>'',
            'local_backlog_complete'=>$mode!=='TARGET_USABLE_CANDIDATES','local_backlog_cursor'=>0,'local_backlog_processed'=>0,'local_backlog_promoted'=>0,'local_backlog_provider_calls'=>0,'context_binding'=>$contextBinding,
            'item_count'=>count($items),'current_index'=>0,'completed_count'=>0,'items'=>$items,
            'last_error'=>'','coordination_wait_code'=>'','created_at_utc'=>$now,'updated_at_utc'=>$now,
        ];
        self::save($queue);
        return self::summary($queue);
    }

    private static function queueItem(array $row): array {
        return [
            'category_id'=>(int)$row['category_id'],'seed'=>(string)$row['seed'],'family'=>(string)$row['family'],'root'=>(string)$row['root'],
            'status'=>'PENDING','child_job_uuid'=>'','actual_cost'=>0.0,'usable_candidate_count'=>0,'candidate_count'=>0,'last_error'=>'','coordination_wait_code'=>'',
        ];
    }

    public static function advance(string $queueUuid,array $settings,bool $explicitResume=false): array {
        $token=self::acquireQueueLock();
        try{return self::advanceLocked($queueUuid,$settings,$explicitResume);}finally{self::releaseQueueLock($token);}
    }

    private static function advanceLocked(string $queueUuid,array $settings,bool $explicitResume=false): array {
        $queue=self::load();
        if(!hash_equals((string)$queue['queue_uuid'],trim($queueUuid)))throw new RuntimeException('PSTE_BREADTH_QUEUE_ID_MISMATCH');
        if(self::cancelRequested($queue))return self::settleCancellation($queue);
        if(in_array((string)$queue['status'],['COMPLETE','CANCELLED'],true))return self::summary($queue);
        if((string)$queue['status']==='OUTCOME_UNKNOWN')return self::summary($queue);
        try{$child=PSTE_Research_Job::current();}catch(Throwable $e){return self::pause($queue,self::errorCode($e));}
        $queue=self::recoverTransientCoordinationPause($queue,$child);$queue=self::recoverSafeSiteContextPause($queue,$child);
        if((string)$queue['status']==='PAUSED_ERROR'){
            if(!$explicitResume)return self::summary($queue,$child);
            $queue['status']='RUNNING';$queue['last_error']='';$queue['coordination_wait_code']='';$queue['updated_at_utc']=gmdate('c');self::save($queue);
        }
        if((string)$queue['status']!=='RUNNING')throw new RuntimeException('PSTE_BREADTH_QUEUE_STATUS_INVALID');
        if((string)($queue['mode']??'')==='TARGET_USABLE_CANDIDATES'&&empty($queue['local_backlog_complete']))return self::advanceLocalBacklog($queue);
        $idx=(int)$queue['current_index'];
        if($idx>=(int)$queue['item_count'])return self::completeOrExtend($queue);
        $item=(array)$queue['items'][$idx];
        if($child===null){
            try{
                $child=PSTE_Research_Job::start((int)$item['category_id'],(string)$item['seed'],$settings);
                $queue['items'][$idx]['status']='RUNNING';$queue['items'][$idx]['child_job_uuid']=(string)$child['job_uuid'];$queue['updated_at_utc']=gmdate('c');self::save($queue);
                if(self::cancelRequested($queue))return self::settleCancellation($queue,$child);
                return self::summary($queue,$child);
            }catch(Throwable $e){$code=self::errorCode($e);if($code==='PSTE_RESEARCH_JOB_ALREADY_ACTIVE'){try{$raced=PSTE_Research_Job::current();}catch(Throwable $ignored){$raced=null;}if(is_array($raced)&&self::childMatchesItem($raced,$item)){$queue['items'][$idx]['status']='RUNNING';$queue['items'][$idx]['child_job_uuid']=(string)$raced['job_uuid'];$queue['coordination_wait_code']='PSTE_RESEARCH_JOB_ALREADY_ACTIVE';$queue['items'][$idx]['coordination_wait_code']='PSTE_RESEARCH_JOB_ALREADY_ACTIVE';$queue['updated_at_utc']=gmdate('c');self::save($queue);return self::summary($queue,$raced);}return self::pause($queue,'PSTE_BREADTH_CHILD_JOB_MISMATCH');}if(self::isTransientCoordinationCode($code))return self::coordinationWait($queue,$code,null);return self::pause($queue,$code);}
        }
        $expected=(string)($queue['items'][$idx]['child_job_uuid']??'');
        if($expected!==''&&!hash_equals($expected,(string)$child['job_uuid']))return self::pause($queue,'PSTE_BREADTH_CHILD_JOB_MISMATCH');
        if($expected===''){$queue['items'][$idx]['child_job_uuid']=(string)$child['job_uuid'];$queue['items'][$idx]['status']='RUNNING';self::save($queue);}
        try{$child=PSTE_Research_Job::advance((string)$child['job_uuid'],$settings,$explicitResume);}catch(Throwable $e){
            $code=self::errorCode($e);
            if(self::isTransientCoordinationCode($code))return self::coordinationWait($queue,$code,$child);
            return self::pause($queue,$code);
        }
        if(self::cancelRequested($queue))return self::settleCancellation($queue,$child);
        $childStatus=(string)($child['status']??'');
        if($childStatus==='COMPLETE'){
            $rawUsable=max(0,(int)($child['usable_candidate_count']??0));$candidateCount=max(0,(int)($child['candidate_count']??0));
            $queue['items'][$idx]['status']='COMPLETE';$queue['items'][$idx]['actual_cost']=(float)($child['actual_cost']??0.0);$queue['items'][$idx]['raw_usable_candidate_count']=$rawUsable;$queue['items'][$idx]['candidate_count']=$candidateCount;$queue['items'][$idx]['last_error']='';$queue['items'][$idx]['coordination_wait_code']='';$queue['coordination_wait_code']='';
            $queue['raw_usable_candidate_count']=max(0,(int)($queue['raw_usable_candidate_count']??0))+$rawUsable;
            if((string)($queue['mode']??'FIXED_FAMILY_COUNT')==='TARGET_USABLE_CANDIDATES'){
                $counted=self::countNewUniqueUsableTopics($queue,(string)($child['job_uuid']??$queue['items'][$idx]['child_job_uuid']??''));
                $queue['usable_topic_keys']=$counted['keys'];$queue['usable_candidate_count']=count($counted['keys']);
                $queue['items'][$idx]['usable_candidate_count']=(int)$counted['added'];$queue['items'][$idx]['count_status']=(string)$counted['status'];
            }else{
                $queue['items'][$idx]['usable_candidate_count']=$rawUsable;$queue['usable_candidate_count']=max(0,(int)($queue['usable_candidate_count']??0))+$rawUsable;
            }
            $queue['current_index']=$idx+1;$queue['completed_count']=(int)$queue['completed_count']+1;$queue['updated_at_utc']=gmdate('c');
            if(self::targetReached($queue))return self::complete($queue,'TARGET_REACHED');
            if((int)$queue['current_index']>=(int)$queue['item_count'])return self::completeOrExtend($queue);
            self::save($queue);return self::summary($queue,null);
        }
        if($childStatus==='PAUSED_ERROR'){
            $queue['items'][$idx]['status']='PAUSED_ERROR';$queue['items'][$idx]['last_error']=(string)($child['last_error']??'PSTE_RESEARCH_PAUSED');
            return self::pause($queue,(string)$queue['items'][$idx]['last_error']);
        }
        if($childStatus==='OUTCOME_UNKNOWN'){
            $queue['items'][$idx]['status']='OUTCOME_UNKNOWN';$queue['items'][$idx]['last_error']=(string)($child['last_error']??'PSTE_PROVIDER_TRANSPORT_OUTCOME_UNKNOWN');
            $queue['status']='OUTCOME_UNKNOWN';$queue['last_error']=(string)$queue['items'][$idx]['last_error'];$queue['updated_at_utc']=gmdate('c');self::save($queue);return self::summary($queue,$child);
        }
        $wait=(string)($child['coordination_wait_code']??'');$queue['items'][$idx]['status']='RUNNING';$queue['items'][$idx]['coordination_wait_code']=$wait;$queue['coordination_wait_code']=$wait;$queue['last_error']='';$queue['updated_at_utc']=gmdate('c');self::save($queue);return self::summary($queue,$child);
    }


    /** Current strict PASS topics minus the wave-start PASS baseline. No title words or discovery history define identity. */
    private static function countNewUniqueUsableTopics(array $queue,string $runUuid=''): array {
        $baseline=[];foreach((array)($queue['baseline_usable_topic_keys']??[]) as $key){$key=trim((string)$key);if($key!=='')$baseline[$key]=true;}
        try{$current=PSTE_Repository::usablePlanningTopicKeys();}catch(Throwable $e){return ['keys'=>(array)($queue['usable_topic_keys']??[]),'added'=>0,'status'=>'LOCAL_COUNT_READ_FAILED'];}
        $keys=[];foreach($current as $key){$key=trim((string)$key);if($key!==''&&!isset($baseline[$key]))$keys[$key]=true;}$out=array_keys($keys);sort($out,SORT_STRING);
        $before=count((array)($queue['usable_topic_keys']??[]));return ['keys'=>$out,'added'=>max(0,count($out)-$before),'status'=>'PASS_BASELINE_DELTA'];
    }

    /** Mine the already retained SEO backlog first. This phase is local and performs zero provider requests. */
    private static function advanceLocalBacklog(array $queue): array {
        $baseline=get_option(PSTE_OPTION_SITE_BASELINE,[]);if(!is_array($baseline)||($baseline['contract']??'')!=='PSTE_SITE_BASELINE_V1')return self::pause($queue,'PSTE_SITE_BASELINE_REQUIRED');
        try{$batch=PSTE_Repository::reanalyzeRetainedBacklogBatch((int)($queue['local_backlog_cursor']??0),40,$baseline,(array)($queue['context_binding']??[]));}catch(Throwable $e){return self::pause($queue,self::errorCode($e));}
        if((int)($batch['provider_calls']??-1)!==0)return self::pause($queue,'PSTE_RETAINED_BACKLOG_PROVIDER_CALL_CONTRACT_VIOLATION');
        $queue['local_backlog_cursor']=(int)($batch['cursor']??$queue['local_backlog_cursor']??0);$queue['local_backlog_processed']=(int)($queue['local_backlog_processed']??0)+(int)($batch['processed']??0);$queue['local_backlog_promoted']=(int)($queue['local_backlog_promoted']??0)+(int)($batch['promoted']??0);$queue['local_backlog_provider_calls']=0;
        $counted=self::countNewUniqueUsableTopics($queue);$queue['usable_topic_keys']=$counted['keys'];$queue['usable_candidate_count']=count($counted['keys']);$queue['updated_at_utc']=gmdate('c');
        if(self::targetReached($queue)){ $queue['local_backlog_complete']=true;return self::complete($queue,'TARGET_REACHED_FROM_RETAINED_BACKLOG'); }
        if(!empty($batch['complete'])){$queue['local_backlog_complete']=true;if((int)($queue['item_count']??0)===0){$baseline=get_option(PSTE_OPTION_SITE_BASELINE,[]);$open=self::openFamilies(is_array($baseline)?$baseline:[]);if(!$open)return self::complete($queue,'NO_OPEN_FAMILIES_AFTER_RETAINED_BACKLOG');$next=self::spread($open,1);$queue['items']=[self::queueItem((array)$next[0])];$queue['item_count']=1;}}
        self::save($queue);return self::summary($queue,null);
    }

    private static function targetReached(array $queue): bool {
        return (string)($queue['mode']??'FIXED_FAMILY_COUNT')==='TARGET_USABLE_CANDIDATES'
            && (int)($queue['target_usable']??0)>0
            && (int)($queue['usable_candidate_count']??0)>=(int)$queue['target_usable'];
    }

    private static function completeOrExtend(array $queue): array {
        if((string)($queue['mode']??'FIXED_FAMILY_COUNT')!=='TARGET_USABLE_CANDIDATES')return self::complete($queue,'FIXED_FAMILY_COUNT_COMPLETE');
        if(self::targetReached($queue))return self::complete($queue,'TARGET_REACHED');
        if((int)($queue['item_count']??0)>=(int)($queue['max_items']??self::DEFAULT_MAX_ITEMS))return self::complete($queue,'MAX_FAMILIES_REACHED');

        $baseline=get_option(PSTE_OPTION_SITE_BASELINE,[]);
        if(!is_array($baseline)||($baseline['contract']??'')!=='PSTE_SITE_BASELINE_V1')return self::pause($queue,'PSTE_SITE_BASELINE_REQUIRED');
        $rebase=PSTE_Snapshot::rebaseResearchBaselineIfSafe($baseline);
        if(empty($rebase['ok']))return self::pause($queue,(string)($rebase['error_code']??'PSTE_SITE_BASELINE_STALE'));
        $baseline=(array)$rebase['baseline'];
        $already=[];foreach((array)($queue['items']??[]) as $item)$already[(int)($item['category_id']??0)]=true;
        $open=array_values(array_filter(self::openFamilies($baseline),static fn(array $row): bool=>empty($already[(int)($row['category_id']??0)])));
        if(!$open)return self::complete($queue,'NO_OPEN_FAMILIES');
        $next=self::spread($open,1);
        if(!$next)return self::complete($queue,'NO_OPEN_FAMILIES');
        $queue['items'][]=self::queueItem((array)$next[0]);$queue['item_count']=count($queue['items']);$queue['updated_at_utc']=gmdate('c');self::save($queue);
        return self::summary($queue,null);
    }

    public static function requestCancel(string $queueUuid): array {
        $queue=self::load();if(!hash_equals((string)$queue['queue_uuid'],trim($queueUuid)))throw new RuntimeException('PSTE_BREADTH_QUEUE_ID_MISMATCH');
        if(in_array((string)$queue['status'],['COMPLETE','CANCELLED'],true))return self::summary($queue);
        self::storeCancelRequest((string)$queue['queue_uuid']);
        $token=self::acquireQueueLock();
        try{$queue=self::load();if(!hash_equals((string)$queue['queue_uuid'],trim($queueUuid)))throw new RuntimeException('PSTE_BREADTH_QUEUE_ID_MISMATCH');return self::settleCancellation($queue);}finally{self::releaseQueueLock($token);}
    }

    /** Read-only queue snapshot for client terminal readback. Never recovers, resumes or advances work. */
    public static function peek(): ?array {
        $q=self::raw();if($q===null)return null;self::assertQueue($q);return self::summary($q,null);
    }

    public static function current(): ?array {
        $q=self::raw();if($q===null)return null;self::assertQueue($q);$child=null;try{$child=PSTE_Research_Job::current();}catch(Throwable $ignored){}
        if(self::cancelRequested($q))return self::summary($q,$child);
        $q=self::recoverTransientCoordinationPause($q,$child);$q=self::recoverSafeSiteContextPause($q,$child);
        return self::summary($q,$child);
    }

    /** @return list<array{category_id:int,seed:string,family:string,root:string}> */
    public static function openFamilies(array $baseline): array {
        $families=PSTE_Category_Context::familyAnchors($baseline);
        $input=array_map(static fn(array $f)=>['term_id'=>(int)$f['term_id'],'name'=>(string)$f['topic_family_name'],'slug'=>(string)$f['topic_family_key']],$families);
        $progress=PSTE_Repository::categoryProgress($input);$states=[];
        foreach((array)($progress['items']??[]) as $p)$states[(int)($p['term_id']??0)]=(string)($p['state']??'');
        $rootStats=[];
        foreach($families as $f){
            $id=(int)$f['term_id'];$root=self::rootKey($id,$baseline);
            if(!isset($rootStats[$root]))$rootStats[$root]=['total'=>0,'processed'=>0];
            $rootStats[$root]['total']++;
            if(($states[$id]??'')!=='NOT_ANALYZED')$rootStats[$root]['processed']++;
        }
        $out=[];
        foreach($families as $f){$id=(int)$f['term_id'];if(($states[$id]??'')!=='NOT_ANALYZED')continue;$root=self::rootKey($id,$baseline);$out[]=['category_id'=>$id,'seed'=>(string)$f['topic_family_name'],'family'=>(string)$f['topic_family_name'],'root'=>$root,'root_processed_count'=>(int)($rootStats[$root]['processed']??0),'root_total_count'=>(int)($rootStats[$root]['total']??0)];}
        usort($out,static fn($a,$b)=>[(int)($a['root_processed_count']??0),(string)$a['root'],(string)$a['family'],(int)$a['category_id']]<=>[(int)($b['root_processed_count']??0),(string)$b['root'],(string)$b['family'],(int)$b['category_id']]);return $out;
    }

    /** @param list<array{category_id:int,seed:string,family:string,root:string}> $rows */
    public static function spread(array $rows,int $count): array {
        $count=max(1,min(self::MAX_ITEMS,$count));$groups=[];$processed=[];
        foreach($rows as $r){$root=(string)$r['root'];$groups[$root][]=$r;$processed[$root]=(int)($r['root_processed_count']??($processed[$root]??0));}
        foreach($groups as &$g)usort($g,static fn($a,$b)=>[(string)$a['family'],(int)$a['category_id']]<=>[(string)$b['family'],(int)$b['category_id']]);unset($g);
        $selected=[];
        while(count($selected)<$count){
            $roots=array_keys(array_filter($groups,static fn($g)=>$g!==[]));
            if(!$roots)break;
            usort($roots,static fn($a,$b)=>[(int)($processed[$a]??0),(string)$a]<=>[(int)($processed[$b]??0),(string)$b]);
            $moved=false;
            foreach($roots as $root){if(!$groups[$root])continue;$row=array_shift($groups[$root]);$selected[]=$row;$processed[$root]=(int)($processed[$root]??0)+1;$moved=true;if(count($selected)>=$count)break;}
            if(!$moved)break;
        }
        return $selected;
    }

    private static function rootKey(int $termId,array $baseline): string {
        foreach((array)($baseline['leaf_categories']??[]) as $leaf){if(!is_array($leaf)||(int)($leaf['term_id']??0)!==$termId)continue;$nodes=(array)($leaf['portal_path_nodes']??[]);if(isset($nodes[0])&&is_array($nodes[0])){$slug=trim((string)($nodes[0]['slug']??''));$name=trim((string)($nodes[0]['name']??''));if($slug!==''||$name!=='')return $slug!==''?$slug:$name;}$names=(array)($leaf['portal_ancestor_page_names']??[]);if(isset($names[0])&&trim((string)$names[0])!=='')return trim((string)$names[0]);}
        return 'ROOT_UNRESOLVED';
    }
    private static function recoverTransientCoordinationPause(array $queue,?array $child): array {
        $code=(string)($queue['last_error']??'');
        if((string)($queue['status']??'')!=='PAUSED_ERROR'||(!self::isTransientCoordinationCode($code)&&!self::isReplaySafeLocalFinalizeCode($code)))return $queue;
        if(!is_array($child)||(string)($child['status']??'')!=='RUNNING')return $queue;
        $idx=(int)($queue['current_index']??0);if(!isset($queue['items'][$idx])||!is_array($queue['items'][$idx]))return $queue;
        if(!self::childMatchesItem($child,(array)$queue['items'][$idx]))return $queue;
        $actual=(string)($child['job_uuid']??'');if($actual==='')return $queue;$expected=(string)($queue['items'][$idx]['child_job_uuid']??'');
        if($expected==='')$queue['items'][$idx]['child_job_uuid']=$actual;
        $queue['status']='RUNNING';$queue['last_error']='';$queue['coordination_wait_code']=$code;$queue['items'][$idx]['status']='RUNNING';$queue['items'][$idx]['last_error']='';$queue['items'][$idx]['coordination_wait_code']=$code;$queue['updated_at_utc']=gmdate('c');self::save($queue);
        return $queue;
    }
    private static function recoverSafeSiteContextPause(array $queue,?array $child): array {
        if((string)($queue['status']??'')!=='PAUSED_ERROR'||(string)($queue['last_error']??'')!=='PSTE_SITE_BASELINE_STALE')return $queue;
        if(!is_array($child)||(string)($child['status']??'')!=='RUNNING'||(string)($child['coordination_wait_code']??'')!=='PSTE_SITE_CONTEXT_REBASED_SAFE')return $queue;
        $idx=(int)($queue['current_index']??0);if(!isset($queue['items'][$idx])||!is_array($queue['items'][$idx])||!self::childMatchesItem($child,(array)$queue['items'][$idx]))return $queue;
        $queue['status']='RUNNING';$queue['last_error']='';$queue['coordination_wait_code']='PSTE_SITE_CONTEXT_REBASED_SAFE';$queue['items'][$idx]['status']='RUNNING';$queue['items'][$idx]['last_error']='';$queue['items'][$idx]['coordination_wait_code']='PSTE_SITE_CONTEXT_REBASED_SAFE';$queue['updated_at_utc']=gmdate('c');self::save($queue);return $queue;
    }

    private static function settleCancellation(array $queue,?array $child=null): array {
        if(!self::cancelRequested($queue))return self::summary($queue,$child);
        if(in_array((string)($queue['status']??''),['COMPLETE','CANCELLED'],true)){self::clearCancelRequest((string)$queue['queue_uuid']);return self::summary($queue,$child);}
        if($child===null){try{$child=PSTE_Research_Job::current();}catch(Throwable $e){throw $e;}}
        $idx=(int)($queue['current_index']??0);
        if(is_array($child)){
            if(!isset($queue['items'][$idx])||!is_array($queue['items'][$idx])||!self::childMatchesItem($child,(array)$queue['items'][$idx]))throw new RuntimeException('PSTE_BREADTH_CANCEL_CHILD_JOB_MISMATCH');
            try{$cancelled=PSTE_Research_Job::cancelForBreadthStop((string)$child['job_uuid']);}
            catch(Throwable $e){
                $code=self::errorCode($e);
                if(in_array($code,['PSTE_RESEARCH_STEP_ALREADY_RUNNING','PSTE_BREADTH_CANCEL_WAIT_IN_FLIGHT'],true)){
                    $queue['status']='RUNNING';$queue['last_error']='';$queue['coordination_wait_code']=$code;$queue['items'][$idx]['status']='RUNNING';$queue['items'][$idx]['last_error']='';$queue['items'][$idx]['coordination_wait_code']=$code;$queue['updated_at_utc']=gmdate('c');self::save($queue);return self::summary($queue,$child);
                }
                if($code==='PSTE_BREADTH_CANCEL_PROVIDER_OUTCOME_UNKNOWN'){
                    $queue['status']='OUTCOME_UNKNOWN';$queue['last_error']=$code;$queue['coordination_wait_code']='';$queue['items'][$idx]['status']='OUTCOME_UNKNOWN';$queue['items'][$idx]['last_error']=$code;$queue['items'][$idx]['coordination_wait_code']='';$queue['updated_at_utc']=gmdate('c');self::save($queue);return self::summary($queue,$child);
                }
                throw $e;
            }
            $queue['items'][$idx]['status']='CANCELLED';$queue['items'][$idx]['actual_cost']=(float)($cancelled['actual_cost']??$queue['items'][$idx]['actual_cost']??0.0);$queue['items'][$idx]['last_error']='';$queue['items'][$idx]['coordination_wait_code']='';
        }elseif(isset($queue['items'][$idx])&&is_array($queue['items'][$idx])&&(string)($queue['items'][$idx]['status']??'')!=='COMPLETE'){
            $queue['items'][$idx]['status']='CANCELLED_NO_ACTIVE_CHILD';$queue['items'][$idx]['last_error']='';$queue['items'][$idx]['coordination_wait_code']='';
        }
        for($i=$idx+1;$i<(int)($queue['item_count']??0);$i++)if(isset($queue['items'][$i])&&is_array($queue['items'][$i])&&(string)($queue['items'][$i]['status']??'')!=='COMPLETE'){$queue['items'][$i]['status']='CANCELLED_NOT_STARTED';$queue['items'][$i]['last_error']='';$queue['items'][$i]['coordination_wait_code']='';}
        $queue['status']='CANCELLED';$queue['last_error']='';$queue['coordination_wait_code']='';$queue['cancelled_at_utc']=gmdate('c');$queue['updated_at_utc']=$queue['cancelled_at_utc'];self::save($queue);self::clearCancelRequest((string)$queue['queue_uuid']);return self::summary($queue,null);
    }

    private static function cancelMarker(): ?array {
        $m=get_option(PSTE_OPTION_BREADTH_RESEARCH_CANCEL,null);if($m===null||$m===false||$m==='')return null;if(!is_array($m))throw new RuntimeException('PSTE_BREADTH_CANCEL_STORAGE_INVALID');
        $decl=(string)($m['sha256']??'');$copy=$m;unset($copy['sha256']);if(($m['contract']??'')!=='PSTE_BREADTH_CANCEL_REQUEST_V1'||!preg_match('/^[a-f0-9]{64}$/',$decl)||!hash_equals(hash('sha256',self::canonicalJson($copy)),$decl))throw new RuntimeException('PSTE_BREADTH_CANCEL_REQUEST_INVALID');return $m;
    }
    private static function cancelRequested(array $queue): bool {$m=self::cancelMarker();return is_array($m)&&hash_equals((string)($queue['queue_uuid']??''),(string)($m['queue_uuid']??''));}
    private static function storeCancelRequest(string $queueUuid): void {$m=['contract'=>'PSTE_BREADTH_CANCEL_REQUEST_V1','queue_uuid'=>$queueUuid,'requested_at_utc'=>gmdate('c')];$m['sha256']=hash('sha256',self::canonicalJson($m));update_option(PSTE_OPTION_BREADTH_RESEARCH_CANCEL,$m,false);$stored=self::cancelMarker();if(!is_array($stored)||!hash_equals($queueUuid,(string)($stored['queue_uuid']??'')))throw new RuntimeException('PSTE_BREADTH_CANCEL_REQUEST_READBACK_MISMATCH');}
    private static function clearCancelRequest(string $queueUuid=''): void {$m=get_option(PSTE_OPTION_BREADTH_RESEARCH_CANCEL,null);if(!is_array($m)){if($queueUuid==='')delete_option(PSTE_OPTION_BREADTH_RESEARCH_CANCEL);return;}if($queueUuid===''||hash_equals($queueUuid,(string)($m['queue_uuid']??'')))delete_option(PSTE_OPTION_BREADTH_RESEARCH_CANCEL);}

    private static function acquireQueueLock(): string {$token=hash('sha256',microtime(true).'|'.wp_generate_uuid4());$payload=['token'=>$token,'expires_at'=>time()+self::QUEUE_LOCK_TTL];if(add_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK,$payload,'',false))return $token;$existing=get_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK,[]);if(is_array($existing)&&(int)($existing['expires_at']??0)<time()){if(get_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK,[])===$existing)delete_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK);if(add_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK,$payload,'',false))return $token;}throw new RuntimeException('PSTE_BREADTH_QUEUE_STEP_ALREADY_RUNNING');}
    private static function releaseQueueLock(string $token): void {$existing=get_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK,[]);if(is_array($existing)&&hash_equals($token,(string)($existing['token']??'')))delete_option(PSTE_OPTION_BREADTH_RESEARCH_LOCK);}

    private static function isTransientCoordinationCode(string $code): bool {return in_array($code,self::TRANSIENT_COORDINATION_CODES,true);}
    private static function isReplaySafeLocalFinalizeCode(string $code): bool {return in_array($code,self::REPLAY_SAFE_LOCAL_FINALIZE_CODES,true);}
    private static function childMatchesItem(array $child,array $item): bool {$expected=(string)($item['child_job_uuid']??'');$actual=(string)($child['job_uuid']??'');if($actual===''||($expected!==''&&!hash_equals($expected,$actual)))return false;if(isset($child['category_id'])&&(int)$child['category_id']!==(int)($item['category_id']??0))return false;if(isset($child['seed'])&&trim((string)$child['seed'])!==trim((string)($item['seed']??$child['seed'])))return false;return true;}
    private static function coordinationWait(array $queue,string $code,?array $child): array {$idx=(int)($queue['current_index']??0);if(isset($queue['items'][$idx])&&is_array($queue['items'][$idx])){$queue['items'][$idx]['status']='RUNNING';$queue['items'][$idx]['last_error']='';$queue['items'][$idx]['coordination_wait_code']=$code;}if(is_array($child)&&isset($queue['items'][$idx])&&(string)($queue['items'][$idx]['child_job_uuid']??'')==='')$queue['items'][$idx]['child_job_uuid']=(string)($child['job_uuid']??'');$queue['status']='RUNNING';$queue['last_error']='';$queue['coordination_wait_code']=$code;$queue['updated_at_utc']=gmdate('c');self::save($queue);return self::summary($queue,$child);}

    private static function complete(array $queue,string $reason='COMPLETE'): array {$queue['status']='COMPLETE';$queue['completion_reason']=$reason;$queue['last_error']='';$queue['coordination_wait_code']='';$queue['updated_at_utc']=gmdate('c');self::save($queue);return self::summary($queue);}
    private static function pause(array $queue,string $error): array {$idx=(int)$queue['current_index'];if(isset($queue['items'][$idx])){$queue['items'][$idx]['status']='PAUSED_ERROR';$queue['items'][$idx]['last_error']=$error;$queue['items'][$idx]['coordination_wait_code']='';}$queue['status']='PAUSED_ERROR';$queue['last_error']=$error;$queue['coordination_wait_code']='';$queue['updated_at_utc']=gmdate('c');self::save($queue);return self::summary($queue);}
    private static function summary(array $q,?array $child=null): array {
        $m=self::cancelMarker();$cancel=is_array($m)&&hash_equals((string)($q['queue_uuid']??''),(string)($m['queue_uuid']??''));
        $mode=(string)($q['mode']??'FIXED_FAMILY_COUNT');$target=(int)($q['target_usable']??0);$usable=(int)($q['usable_candidate_count']??0);
        return ['contract'=>self::CONTRACT,'queue_uuid'=>(string)$q['queue_uuid'],'status'=>(string)$q['status'],'mode'=>$mode,'requested_count'=>(int)$q['requested_count'],'target_usable'=>$target,'usable_candidate_count'=>$usable,'raw_usable_candidate_count'=>(int)($q['raw_usable_candidate_count']??$usable),'target_achieved'=>$mode==='TARGET_USABLE_CANDIDATES'&&$target>0&&$usable>=$target,'max_items'=>(int)($q['max_items']??($q['item_count']??self::LEGACY_MAX_ITEMS)),'completion_reason'=>(string)($q['completion_reason']??''),'local_backlog_complete'=>!empty($q['local_backlog_complete']),'local_backlog_cursor'=>(int)($q['local_backlog_cursor']??0),'local_backlog_processed'=>(int)($q['local_backlog_processed']??0),'local_backlog_promoted'=>(int)($q['local_backlog_promoted']??0),'local_backlog_provider_calls'=>(int)($q['local_backlog_provider_calls']??0),'item_count'=>(int)$q['item_count'],'current_index'=>(int)$q['current_index'],'completed_count'=>(int)$q['completed_count'],'last_error'=>(string)$q['last_error'],'coordination_wait_code'=>(string)($q['coordination_wait_code']??''),'cancel_requested'=>$cancel,'cancel_requested_at_utc'=>$cancel?(string)($m['requested_at_utc']??''):'','cancelled_at_utc'=>(string)($q['cancelled_at_utc']??''),
            'items'=>array_map(static fn($i)=>['category_id'=>(int)$i['category_id'],'family'=>(string)$i['family'],'root'=>(string)$i['root'],'status'=>(string)$i['status'],'actual_cost'=>(float)$i['actual_cost'],'usable_candidate_count'=>(int)($i['usable_candidate_count']??0),'raw_usable_candidate_count'=>(int)($i['raw_usable_candidate_count']??($i['usable_candidate_count']??0)),'candidate_count'=>(int)($i['candidate_count']??0),'count_status'=>(string)($i['count_status']??''),'last_error'=>(string)$i['last_error'],'coordination_wait_code'=>(string)($i['coordination_wait_code']??'')],(array)$q['items']),'child'=>$child,'updated_at_utc'=>(string)$q['updated_at_utc']];
    }
    private static function raw(): ?array {$v=get_option(PSTE_OPTION_BREADTH_RESEARCH_QUEUE,null);if($v===null||$v===false||$v==='')return null;if(!is_array($v))throw new RuntimeException('PSTE_BREADTH_QUEUE_STORAGE_INVALID');return $v;}
    private static function load(): array {$q=self::raw();if($q===null)throw new RuntimeException('PSTE_BREADTH_QUEUE_MISSING');self::assertQueue($q);return $q;}
    private static function save(array $q): void {$q=self::withHash($q);update_option(PSTE_OPTION_BREADTH_RESEARCH_QUEUE,$q,false);$stored=get_option(PSTE_OPTION_BREADTH_RESEARCH_QUEUE,null);if(!is_array($stored)||!hash_equals((string)$q['sha256'],(string)($stored['sha256']??'')))throw new RuntimeException('PSTE_BREADTH_QUEUE_READBACK_MISMATCH');self::assertQueue($stored);}
    private static function withHash(array $q): array {$q['contract']=self::CONTRACT;$q['version']=self::VERSION;unset($q['sha256']);$q['sha256']=hash('sha256',self::canonicalJson($q));return $q;}
    private static function assertQueue(array $q): void {
        if(($q['contract']??'')!==self::CONTRACT||!in_array((string)($q['version']??''),self::COMPATIBLE_VERSIONS,true))throw new RuntimeException('PSTE_BREADTH_QUEUE_CONTRACT_INVALID');
        $decl=(string)($q['sha256']??'');$copy=$q;unset($copy['sha256']);if(!preg_match('/^[a-f0-9]{64}$/',$decl)||!hash_equals(hash('sha256',self::canonicalJson($copy)),$decl))throw new RuntimeException('PSTE_BREADTH_QUEUE_HASH_MISMATCH');
        $itemCount=(int)($q['item_count']??0);$allowZero=in_array((string)($q['version']??''),['1.4.0','1.5.0'],true)&&(string)($q['mode']??'')==='TARGET_USABLE_CANDIDATES';if($itemCount<($allowZero?0:1)||$itemCount>self::MAX_ITEMS)throw new RuntimeException('PSTE_BREADTH_QUEUE_SIZE_INVALID');
        if(!in_array((string)($q['status']??''),['RUNNING','PAUSED_ERROR','OUTCOME_UNKNOWN','COMPLETE','CANCELLED'],true))throw new RuntimeException('PSTE_BREADTH_QUEUE_STATUS_INVALID');
        if(in_array((string)($q['version']??''),['1.3.0','1.4.0','1.5.0'],true)&&(string)($q['mode']??'')==='TARGET_USABLE_CANDIDATES'){
            if((int)($q['target_usable']??0)<1||(int)($q['max_items']??0)<1||(int)$q['max_items']>self::MAX_ITEMS)throw new RuntimeException('PSTE_BREADTH_TARGET_CONFIG_INVALID');
        }
    }
    private static function canonicalJson($value): string {$json=wp_json_encode(self::canonicalize($value),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRESERVE_ZERO_FRACTION);if(!is_string($json))throw new RuntimeException('PSTE_BREADTH_QUEUE_JSON_ENCODE_FAILED');return $json;}
    private static function canonicalize($v){if(!is_array($v))return $v;if($v===[])return [];$list=array_keys($v)===range(0,count($v)-1);if($list)return array_map([self::class,'canonicalize'],$v);ksort($v,SORT_STRING);foreach($v as $k=>$x)$v[$k]=self::canonicalize($x);return $v;}
    private static function errorCode(Throwable $e): string {$code=strtoupper(trim((string)$e->getMessage()));$code=(string)preg_replace('/[^A-Z0-9_:\-]/','_',$code);return substr($code!==''?$code:'PSTE_BREADTH_QUEUE_FAILED',0,180);}
}
