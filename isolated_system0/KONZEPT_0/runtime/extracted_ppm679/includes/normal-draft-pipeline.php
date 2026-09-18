<?php
if (!defined('ABSPATH')) { return; }

final class PPM679_Normal_Draft_Pipeline {
    const VERSION='6.7.9';
    const LEASE_SECONDS=900;

    public static function execute_plan($plan,$runtime_context=array()) {
        $runtime_context=is_array($runtime_context)?$runtime_context:array();
        $plan_hash=PPM679_Diagnostic::stable_hash($plan);
        $scope=PPM679_Normal_Draft_Release_Validator::expected_scope($plan,$runtime_context);
        $requirements=array(
            'server_instance_id'=>(string)($runtime_context['server_instance_id']??''),
            'article_type_release_scope'=>$scope
        );

        $editorial_candidates=array();
        foreach((array)($plan['items']??array()) as $editorial_item){
            $category_binding=is_array($editorial_item['category_binding']??null)?$editorial_item['category_binding']:array();
            if(!$category_binding){$quality=is_array($editorial_item['quality_binding']??null)?$editorial_item['quality_binding']:array();$category_binding=is_array($quality['wordpress_category']??null)?$quality['wordpress_category']:array();}
            $editorial_candidates[]=array(
                'plan_item_key'=>(string)($editorial_item['plan_item_key']??''),
                'canonical_article_id'=>(string)($editorial_item['canonical_article_id']??$editorial_item['plan_item_key']??''),
                'title'=>(string)($editorial_item['canonical_article']['title']??$editorial_item['topic']??''),
                'topic'=>(string)($editorial_item['topic']??''),
                'article_type'=>(string)($editorial_item['article_type']??''),
                'category_slug'=>(string)($category_binding['slug']??'')
            );
        }
        $editorial_gate=PPM679_Editorial_Plan_Runtime_Gate::preflight($editorial_candidates,'normal_plan_preflight','production');
        if(empty($editorial_gate['ok'])){
            $gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_plan_preflight',$plan_hash,null,null,$requirements);
            return self::result($editorial_gate['report']??array(),$gate,'ppm-normal-draft-blocked.json');
        }

        $schema=PPM679_Storage::ensure_schema();
        if(strpos((string)($schema['status']??''),'BLOCKED_')===0){
            $gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_plan_pre_accept',$plan_hash,null,null,$requirements);
            return self::result($schema,$gate,'ppm-normal-draft-blocked.json');
        }

        $initial_gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_plan_pre_accept',$plan_hash,null,null,$requirements);
        if(empty($initial_gate['ok']))return self::result($initial_gate['report'],$initial_gate,'ppm-normal-draft-blocked.json');

        $validated=PPM679_Plan_Validator::validate($plan,'normal_plan_validation',$initial_gate['state']['server_state_hash']);
        if(empty($validated['ok'])){
            $report=PPM679_Diagnostic::blocked($validated['errors'][0]['error_code'],$validated['errors'],'normal_plan_validation',$initial_gate['state']['server_state_hash'],array('plan_hash'=>$plan_hash));
            return self::result($report,$initial_gate,'ppm-normal-draft-blocked.json');
        }

        $run_id=self::id_value('run');
        $request_id=(string)($runtime_context['request_id']??'');
        if($request_id===''||!PPM679_Storage::tombstone('normal_request_id',$request_id,$run_id,'RESERVED')){
            $error=PPM679_Diagnostic::error('BLOCKED_NORMAL_REQUEST_REPLAY','NORMAL_DRAFT_REQUEST_ID_MUST_BE_UNIQUE_AND_SERVER_BOUND','runtime.request_id','unused request id',$request_id,'Die Produktionsanforderung wurde bereits verwendet oder ist nicht eindeutig gebunden.','normal_plan_accept',$initial_gate['state']['server_state_hash'],__CLASS__,null,array('includes/pipeline.php','includes/storage.php'));
            return self::result(PPM679_Diagnostic::blocked($error['error_code'],array($error),'normal_plan_accept',$initial_gate['state']['server_state_hash']),$initial_gate,'ppm-normal-draft-blocked.json');
        }
        $run=array('run_id'=>$run_id,'plan_id'=>(string)$plan['plan_id'],'plan_hash'=>$plan_hash,'stage'=>'INIT','plan'=>$plan,'workspace'=>null,'check_report'=>null,'readback'=>null,'error'=>null,'created_gmt'=>gmdate('Y-m-d H:i:s'),'updated_gmt'=>gmdate('Y-m-d H:i:s'));
        if(!PPM679_Storage::create_run($run)){
            PPM679_Storage::set_tombstone_state_for_run($run_id,'ABORTED');
            $error=PPM679_Diagnostic::error('BLOCKED_RUN_CREATE_FAILED','VALIDATED_PLAN_MUST_CREATE_ISOLATED_RUN','storage.runs','new run row',false,'Der validierte Plan konnte nicht als isolierter Lauf gespeichert werden.','normal_plan_accept',$initial_gate['state']['server_state_hash'],__CLASS__,null,array('includes/pipeline.php'));
            return self::result(PPM679_Diagnostic::blocked($error['error_code'],array($error),'normal_plan_accept',$initial_gate['state']['server_state_hash']),$initial_gate,'ppm-normal-draft-blocked.json');
        }

        $run=PPM679_Storage::get_run($run_id);
        $gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_plan_accept',$plan_hash,'INIT',$run,$requirements);
        if(empty($gate['ok']))return self::block_run($run_id,$gate['report'],$gate);
        PPM679_Storage::update_run($run_id,array('stage'=>'PLAN_ACCEPTED')); $run=PPM679_Storage::get_run($run_id);

        $gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_bootstrap',$plan_hash,'PLAN_ACCEPTED',$run,$requirements);
        if(empty($gate['ok']))return self::block_run($run_id,$gate['report'],$gate);
        $bootstrap=self::bootstrap($run_id,$plan,$gate);
        if(empty($bootstrap['ok']))return self::block_run($run_id,$bootstrap['report'],$gate);
        PPM679_Storage::update_run($run_id,array('workspace'=>$bootstrap['workspace'],'stage'=>'BOOTSTRAPPED')); $run=PPM679_Storage::get_run($run_id);

        $workspace_hash=PPM679_Diagnostic::stable_hash($bootstrap['workspace']);
        $gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_generation',$workspace_hash,'BOOTSTRAPPED',$run,$requirements);
        if(empty($gate['ok']))return self::abort_run($run_id,$gate['report'],$gate);
        $generation=self::generate_all($run_id,$plan,$gate);
        if(empty($generation['ok']))return self::abort_run($run_id,$generation['report'],$gate);
        PPM679_Storage::update_run($run_id,array('stage'=>'GENERATED')); $run=PPM679_Storage::get_run($run_id);

        $generated_hash=PPM679_Diagnostic::stable_hash($generation['generated']);
        $gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_check_only',$generated_hash,'GENERATED',$run,$requirements);
        if(empty($gate['ok']))return self::abort_run($run_id,$gate['report'],$gate);
        $check=self::check_all($run_id,$plan,$generation['generated'],$gate);
        if(empty($check['ok'])||($check['technical_status']??'')!=='TECHNICAL_CHECK_OK'||($check['content_quality_status']??'')!=='CONTENT_QUALITY_CHECK_OK')return self::abort_run($run_id,$check['report'],$gate);
        PPM679_Storage::update_run($run_id,array('check_report'=>$check['report'],'stage'=>'CHECKED')); $run=PPM679_Storage::get_run($run_id);

        $check_hash=PPM679_Diagnostic::stable_hash($check['report']);
        $gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_draft_create',$check_hash,'CHECKED',$run,$requirements);
        if(empty($gate['ok']))return self::abort_run($run_id,$gate['report'],$gate);
        $drafts=self::create_drafts($run_id,$generation['generated'],$check['report'],$gate,$plan,$runtime_context,$plan_hash);
        if(empty($drafts['ok']))return self::abort_run($run_id,$drafts['report'],$gate,$drafts['created_post_ids']??array());
        PPM679_Storage::update_run($run_id,array('stage'=>'DRAFTED')); $run=PPM679_Storage::get_run($run_id);

        $draft_hash=PPM679_Diagnostic::stable_hash($drafts['drafts']);
        $gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_draft_readback',$draft_hash,'DRAFTED',$run,$requirements);
        if(empty($gate['ok']))return self::abort_run($run_id,$gate['report'],$gate,$drafts['created_post_ids']);
        $readback=self::readback($run_id,$drafts['drafts'],$gate,count((array)$plan['items']));
        if(empty($readback['ok']))return self::abort_run($run_id,$readback['report'],$gate,$drafts['created_post_ids']);

        $editorial_state=PPM679_Editorial_Plan_Runtime_Gate::record_readback((array)($editorial_gate['bindings']??array()),(array)($readback['items']??array()),'normal_draft_readback');
        if(empty($editorial_state['ok'])){
            $error=PPM679_Diagnostic::error('BLOCKED_EDITORIAL_RUNTIME_STATE_WRITE','READBACK_MUST_UPDATE_CANONICAL_EDITORIAL_PLAN_RUNTIME_STATE','editorial_plan.runtime_state','updated state',$editorial_state,'Der Readback konnte den Laufzeitstatus des kanonischen Redaktionsplans nicht aktualisieren.','normal_draft_readback',$gate['state']['server_state_hash'],__CLASS__,null,array('includes/editorial-plan-runtime-gate.php'));
            return self::abort_run($run_id,PPM679_Diagnostic::blocked($error['error_code'],array($error),'normal_draft_readback',$gate['state']['server_state_hash']),$gate,$drafts['created_post_ids']);
        }

        PPM679_Storage::set_tombstone_state_for_run($run_id,'CONSUMED');
        PPM679_Storage::update_run($run_id,array('readback'=>$readback['report'],'stage'=>'READBACK')); $run=PPM679_Storage::get_run($run_id);
        $candidate=PPM679_Diagnostic::ok('NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH','normal_draft_complete',$gate['state']['server_state_hash'],array(
            'run_id'=>$run_id,'request_id'=>$request_id,'plan_id'=>(string)$plan['plan_id'],'plan_hash'=>$plan_hash,'article_count'=>count((array)$plan['items']),
            'workspace'=>$bootstrap['workspace'],'check_only'=>$check['report'],'draft_readback'=>$readback['report'],'drafts'=>$readback['items'],
            'user_action_required'=>'Inhalte der Entwürfe redaktionell prüfen. Keine Veröffentlichung wurde registriert.','production_allowed'=>true,'check_only_allowed'=>true,'draft_allowed'=>true,'publish_allowed'=>false,
            'editorial_plan_preflight'=>$editorial_gate['report'],'editorial_plan_runtime_state'=>$editorial_state['state']
        ));
        $candidate_hash=PPM679_Diagnostic::stable_hash($candidate);
        $final_gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_handoff_readback',$candidate_hash,'READBACK',$run,$requirements);
        if(empty($final_gate['ok']))return self::abort_run($run_id,$final_gate['report'],$final_gate,$drafts['created_post_ids']);
        $candidate['server_state_hash']=$final_gate['state']['server_state_hash']; $candidate['report_hash']=PPM679_Diagnostic::stable_hash($candidate);
        return self::result($candidate,$final_gate,'ppm-normal-draft-readback-6.7.9.json');
    }

    private static function bootstrap($run_id,$plan,$gate) {
        $context='bootstrap';
        $state_hash=$gate['state']['server_state_hash'];
        PPM679_Storage::begin();

        $batch=PPM679_Identifier_Service::fresh('batch_id','batch',$run_id,$context,$state_hash);
        if (empty($batch['ok'])) { PPM679_Storage::set_tombstone_state_for_run($run_id,'ABORTED'); PPM679_Storage::commit(); return $batch; }
        $workspace=PPM679_Identifier_Service::fresh('workspace_id','workspace',$run_id,$context,$state_hash);
        if (empty($workspace['ok'])) { PPM679_Storage::set_tombstone_state_for_run($run_id,'ABORTED'); PPM679_Storage::commit(); return $workspace; }

        $workspace_items=array();
        foreach ($plan['items'] as $index=>$plan_item) {
            $bundle=PPM679_Identifier_Service::create_bundle($run_id,(string)$plan_item['plan_item_key'],$context,$state_hash);
            if (empty($bundle['ok'])) {
                PPM679_Storage::set_tombstone_state_for_run($run_id,'ABORTED');
                PPM679_Storage::commit();
                return $bundle;
            }
            $ids=$bundle['bundle'];
            $item=array(
                'run_id'=>$run_id,
                'plan_item_key'=>(string)$plan_item['plan_item_key'],
                'article_type'=>(string)$plan_item['article_type'],
                'topic'=>(string)$plan_item['topic'],
                'batch_article_id'=>$ids['batch_article_id'],
                'fact_pack_id'=>$ids['fact_pack_id'],
                'skeleton_id'=>$ids['skeleton_id'],
                'reservation_id'=>$ids['reservation_id'],
                'workspace_id'=>$workspace['value'],
                'skeleton_token'=>$ids['skeleton_token'],
                'lease_until_gmt'=>gmdate('Y-m-d H:i:s',time()+self::LEASE_SECONDS),
                'state'=>'RESERVED',
                'post_id'=>null,'title'=>null,'slug'=>null,'content_hash'=>null,'content_html'=>null,
            );
            if (!PPM679_Storage::add_item($item)) {
                PPM679_Storage::set_tombstone_state_for_run($run_id,'ABORTED');
                PPM679_Storage::commit();
                $error=PPM679_Diagnostic::error(
                    'BLOCKED_BOOTSTRAP_ITEM_WRITE_FAILED',
                    'EVERY_RESERVED_IDENTIFIER_BUNDLE_MUST_BIND_TO_ITEM_ATOMICALLY',
                    'workspace.items['.$index.']',
                    'stored item',
                    false,
                    'Die atomare Bindung eines serverseitigen Identifier-Bündels an den Planeintrag ist fehlgeschlagen.',
                    $context,$state_hash,__CLASS__,$index,array('includes/pipeline.php','includes/storage.php')
                );
                return array('ok'=>false,'report'=>PPM679_Diagnostic::blocked($error['error_code'],array($error),$context,$state_hash));
            }
            $workspace_items[]=array(
                'plan_item_key'=>$item['plan_item_key'],
                'article_type'=>$item['article_type'],
                'batch_article_id'=>$item['batch_article_id'],
                'fact_pack_id'=>$item['fact_pack_id'],
                'skeleton_id'=>$item['skeleton_id'],
                'reservation_id'=>$item['reservation_id'],
                'workspace_id'=>$item['workspace_id'],
                'skeleton_token'=>$item['skeleton_token'],
                'lease_until_gmt'=>$item['lease_until_gmt'],
                'state'=>'RESERVED'
            );
        }
        PPM679_Storage::commit();
        $workspace_report=array(
            'contract'=>'ppm_server_workspace_v1',
            'version'=>self::VERSION,
            'run_id'=>$run_id,
            'batch_id'=>$batch['value'],
            'workspace_id'=>$workspace['value'],
            'items'=>$workspace_items,
            'registry_hash_after'=>PPM679_Storage::registry_state()['registry_hash'],
            'created_at'=>gmdate('c')
        );
        $workspace_report['workspace_hash']=PPM679_Diagnostic::stable_hash($workspace_report);
        return array('ok'=>true,'workspace'=>$workspace_report);
    }

    private static function generate_all($run_id,$plan,$gate) {
        $generated=array();
        $errors=array();
        foreach ($plan['items'] as $index=>$plan_item) {
            $pack=PPM679_Storage::load_fact_pack((string)$plan_item['source_snapshot_id']);
            $article=PPM679_Content_Generator::generate($plan_item,$pack);
            if (empty($article['ok'])) {
                $errors[]=PPM679_Diagnostic::error(
                    'BLOCKED_CONTENT_GENERATION_FAILED',
                    'FACT_PACK_AND_TYPE_TEMPLATE_MUST_GENERATE_ARTICLE_CANDIDATE',
                    'plan.items['.$index.']',
                    'generated article candidate',
                    $article,
                    'Die allgemeine Typvorlage konnte aus dem gebundenen Fact-Pack keinen Artikelkandidaten erzeugen.',
                    'generation',$gate['state']['server_state_hash'],__CLASS__,$index,array('includes/content-generator.php')
                );
                continue;
            }
            $generated[$plan_item['plan_item_key']]=$article;
            PPM679_Storage::update_item($run_id,$plan_item['plan_item_key'],array(
                'state'=>'GENERATED',
                'title'=>$article['title'],
                'slug'=>$article['slug'],
                'content_hash'=>$article['content_hash'],
                'content_html'=>$article['content_html']
            ));
        }
        if ($errors) {
            return array('ok'=>false,'report'=>PPM679_Diagnostic::blocked($errors[0]['error_code'],$errors,'generation',$gate['state']['server_state_hash']));
        }
        return array('ok'=>true,'generated'=>$generated);
    }

    private static function check_all($run_id,$plan,$generated,$gate) {
        $errors=array(); $items=array();
        $technical_ok=true; $quality_ok=true;
        foreach ($plan['items'] as $index=>$plan_item) {
            $key=$plan_item['plan_item_key'];
            $candidate=$generated[$key]??array();
            $check=PPM679_Content_Validator::check($candidate,$plan_item,'check_only',$gate['state']['server_state_hash']);
            $item_technical=($check['technical_status']??'')==='TECHNICAL_CHECK_OK';
            $item_quality=($check['content_quality_status']??'')==='CONTENT_QUALITY_CHECK_OK';
            $technical_ok=$technical_ok&&$item_technical;
            $quality_ok=$quality_ok&&$item_quality;
            $items[]=array(
                'plan_item_key'=>$key,
                'article_type'=>$plan_item['article_type'],
                'status'=>($item_technical&&$item_quality)?'TECHNICAL_AND_CONTENT_QUALITY_CHECK_OK':'BLOCKED_CONTENT_VALIDATION',
                'technical_status'=>$check['technical_status']??'BLOCKED_TECHNICAL_CHECK',
                'content_quality_status'=>$check['content_quality_status']??'BLOCKED_CONTENT_QUALITY_CHECK',
                'content_hash'=>$check['content_hash']??'',
                'checks'=>$check['checks']??array(),
                'errors'=>$check['errors']
            );
            if (!$check['ok']) { $errors=array_merge($errors,$check['errors']); }
            else { PPM679_Storage::update_item($run_id,$key,array('state'=>'CHECKED')); }
        }
        $aggregate=PPM679_Fail_Closed_Aggregator::aggregate_item_results($items);
        $technical_ok=$technical_ok&&!empty($aggregate['ok']);
        $quality_ok=$quality_ok&&!empty($aggregate['ok']);
        $extra=array(
            'items'=>$items,
            'technical_status'=>$technical_ok?'TECHNICAL_CHECK_OK':'BLOCKED_TECHNICAL_CHECK',
            'content_quality_status'=>$quality_ok?'CONTENT_QUALITY_CHECK_OK':'BLOCKED_CONTENT_QUALITY_CHECK',
            'known_error_batch_gate_status'=>($aggregate['status']??'BLOCKED'),
            'draft_create_allowed'=>false,
            'publish_allowed'=>false
        );
        if (empty($aggregate['ok']) && !$errors) {
            $errors[]=PPM679_Diagnostic::error(
                'BLOCKED_FAIL_CLOSED_AGGREGATE',
                'EVERY_ITEM_AND_INTEGRITY_STATUS_MUST_EXPLICITLY_PASS',
                'check_only.fail_closed_aggregate',
                'PASS',
                $aggregate,
                'Die zusammengefasste Freigabe wurde fail-closed blockiert.',
                'check_only',$gate['state']['server_state_hash'],__CLASS__,null,array('includes/pipeline.php','includes/fail-closed-aggregator.php')
            );
        }
        if ($errors || !$technical_ok || !$quality_ok) {
            if (!$errors) {
                $errors[]=PPM679_Diagnostic::error(
                    'BLOCKED_DUAL_CONTENT_GATE_INCOMPLETE',
                    'DRAFT_REQUIRES_TECHNICAL_AND_CONTENT_QUALITY_CHECK_ON_SAME_HASH',
                    'check_only',
                    array('technical_status'=>'TECHNICAL_CHECK_OK','content_quality_status'=>'CONTENT_QUALITY_CHECK_OK'),
                    array('technical_status'=>$extra['technical_status'],'content_quality_status'=>$extra['content_quality_status']),
                    'Mindestens eines der beiden unabhängig ausgewiesenen Prüfergebnisse fehlt.',
                    'check_only',$gate['state']['server_state_hash'],__CLASS__,null,array('includes/pipeline.php','includes/content-validator.php')
                );
            }
            return array('ok'=>false,'technical_status'=>$extra['technical_status'],'content_quality_status'=>$extra['content_quality_status'],'report'=>PPM679_Diagnostic::blocked($errors[0]['error_code'],$errors,'check_only',$gate['state']['server_state_hash'],$extra));
        }
        $report=PPM679_Diagnostic::ok('CLOSED_CHAIN_CHECK_OK','check_only',$gate['state']['server_state_hash'],$extra);
        return array('ok'=>true,'technical_status'=>'TECHNICAL_CHECK_OK','content_quality_status'=>'CONTENT_QUALITY_CHECK_OK','report'=>$report);
    }

    private static function create_drafts($run_id,$generated,$check_report,$gate,$plan,$runtime_context,$plan_hash) {
        $checked=array(); foreach((array)($check_report['items']??array()) as $item){if(is_array($item)&&isset($item['plan_item_key']))$checked[(string)$item['plan_item_key']]=$item;}
        $plan_items=array(); foreach((array)($plan['items']??array()) as $item){if(is_array($item)&&isset($item['plan_item_key']))$plan_items[(string)$item['plan_item_key']]=$item;}
        $prepared=array(); $errors=array(); $seen_ids=array();$seen_titles=array();$seen_slugs=array();
        foreach((array)$plan['items'] as $index=>$plan_item){
            $key=(string)$plan_item['plan_item_key']; $candidate=$generated[$key]??array(); $evidence=$checked[$key]??array();
            $one=PPM679_Normal_Draft_Adapter::prepare($candidate,$plan_item,$evidence,$runtime_context,$run_id,$plan_hash,$gate['state']['server_state_hash']);
            if(empty($one['ok'])){foreach((array)($one['errors']??array()) as $error)$errors[]=$error;continue;}
            $identity=(string)$one['canonical_article_id'];$title=PPM679_WP::sanitize_title((string)$one['payload']['title']);$slug=(string)$one['payload']['slug'];
            if(isset($seen_ids[$identity])||isset($seen_titles[$title])||isset($seen_slugs[$slug]))$errors[]=PPM679_Diagnostic::error('BLOCKED_NORMAL_DRAFT_BATCH_DUPLICATE','NORMAL_DRAFT_BATCH_IDENTITIES_MUST_BE_UNIQUE','drafts['.$index.'].identity','unique',array($identity,$title,$slug),'Innerhalb der Produktionswelle kollidieren Artikelidentität, Titel oder Slug.','normal_draft_create',$gate['state']['server_state_hash'],__CLASS__,$index,array('includes/pipeline.php'));
            $seen_ids[$identity]=true;$seen_titles[$title]=true;$seen_slugs[$slug]=true;$prepared[]=$one;
        }
        if($errors)return array('ok'=>false,'report'=>PPM679_Diagnostic::blocked($errors[0]['error_code'],$errors,'normal_draft_create',$gate['state']['server_state_hash']),'created_post_ids'=>array());
        if(count($prepared)!==count((array)$plan['items'])){
            $error=PPM679_Diagnostic::error('BLOCKED_NORMAL_DRAFT_PREWRITE_COUNT','ALL_PLAN_ITEMS_MUST_PASS_BEFORE_FIRST_WRITE','drafts.prepared_count',count((array)$plan['items']),count($prepared),'Nicht alle Artikel haben die vollständige Vorprüfung bestanden.','normal_draft_create',$gate['state']['server_state_hash'],__CLASS__,null,array('includes/pipeline.php'));
            return array('ok'=>false,'report'=>PPM679_Diagnostic::blocked($error['error_code'],array($error),'normal_draft_create',$gate['state']['server_state_hash']),'created_post_ids'=>array());
        }
        $drafts=array();$created=array();
        foreach($prepared as $index=>$one){
            $write=PPM679_Normal_Draft_Adapter::create_draft($one);
            if(empty($write['ok'])){
                foreach($created as $post_id)PPM679_WP::delete_post($post_id);
                $error=PPM679_Diagnostic::error('BLOCKED_NORMAL_DRAFT_CREATE_FAILED','PREPARED_ARTICLE_MUST_CREATE_NEW_WORDPRESS_DRAFT_ONLY','drafts['.$index.']','positive draft post id',$write,'Der vollständig geprüfte Artikel konnte nicht als neuer WordPress-Entwurf angelegt werden.','normal_draft_create',$gate['state']['server_state_hash'],__CLASS__,$index,array('includes/pipeline.php','includes/normal-draft-adapter.php'));
                return array('ok'=>false,'report'=>PPM679_Diagnostic::blocked($error['error_code'],array($error),'normal_draft_create',$gate['state']['server_state_hash']),'created_post_ids'=>$created);
            }
            $post_id=(int)$write['post_id'];$created[]=$post_id;
            $drafts[]=array('plan_item_key'=>$write['plan_item_key'],'article_type'=>$write['article_type'],'post_id'=>$post_id,'expected'=>$write['expected'],'status'=>'draft');
            PPM679_Storage::update_item($run_id,(string)$write['plan_item_key'],array('state'=>'DRAFTED','post_id'=>$post_id));
        }
        return array('ok'=>true,'drafts'=>$drafts,'created_post_ids'=>$created);
    }

    private static function readback($run_id,$drafts,$gate,$expected_count) {
        $snapshots=array();$expectations=array();
        foreach($drafts as $draft){$snapshots[]=PPM679_WP::get_post_snapshot((int)$draft['post_id']);$expectations[]=(array)$draft['expected'];}
        $batch=PPM679_Normal_Draft_Readback_Validator::validate_batch($snapshots,$expectations,(int)$expected_count);
        if(empty($batch['ok']))return array('ok'=>false,'report'=>$batch['report'],'items'=>$batch['items']??array());
        foreach($drafts as $draft)PPM679_Storage::update_item($run_id,(string)$draft['plan_item_key'],array('state'=>'READBACK'));
        return array('ok'=>true,'report'=>$batch['report'],'items'=>$batch['items']);
    }

    private static function block_run($run_id,$report,$gate) {
        PPM679_Storage::update_run($run_id,array('stage'=>'BLOCKED','error'=>$report));
        return self::result($report,$gate,'ppm-normal-draft-blocked.json');
    }

    private static function abort_run($run_id,$report,$gate,$post_ids=array()) {
        foreach ((array)$post_ids as $post_id) { PPM679_WP::delete_post($post_id); }
        PPM679_Storage::set_tombstone_state_for_run($run_id,'ABORTED');
        PPM679_Storage::update_run($run_id,array('stage'=>'BLOCKED','error'=>$report));
        return self::result($report,$gate,'ppm-normal-draft-blocked.json');
    }

    private static function result($artifact,$gate,$filename) {
        return array('artifact'=>$artifact,'gate'=>$gate,'filename'=>$filename);
    }

    private static function id_value($prefix) {
        try { $random=bin2hex(random_bytes(18)); }
        catch (Throwable $e) { $random=hash('sha256',microtime(true).'|'.mt_rand()); }
        return $prefix.'-'.substr($random,0,32);
    }
}
