<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Canonical durable eBay run coordinator.
 *
 * This trait deliberately does not replace the proven acceptance, classification,
 * source upsert, HivePress materialisation or BUSINESS campaign materialisation
 * code. It only owns orchestration, persistence, leases and terminal verification.
 */
trait PPAR_Ebay_Run_Trait {
    private function ebay_run_option_key() {
        $constant = static::class . '::OPTION_EBAY_RUN_STATE';
        return defined($constant) ? (string)constant($constant) : 'ppar_ebay_run_state_v1';
    }

    private function ebay_public_checkpoint_option_key() {
        $constant = static::class . '::OPTION_EBAY_PUBLIC_CHECKPOINT';
        return defined($constant) ? (string)constant($constant) : 'ppar_ebay_public_checkpoint_v1';
    }

    private function ebay_run_history_option_key() {
        $constant = static::class . '::OPTION_EBAY_RUN_HISTORY';
        return defined($constant) ? (string)constant($constant) : 'ppar_ebay_run_history_v1';
    }

    private function ebay_public_checkpoint_load() {
        $checkpoint = get_option($this->ebay_public_checkpoint_option_key(), array());
        return is_array($checkpoint) ? $checkpoint : array();
    }

    private function ebay_public_checkpoint_is_safe($checkpoint = null) {
        if (!is_array($checkpoint)) { $checkpoint = $this->ebay_public_checkpoint_load(); }
        return (string)($checkpoint['schema'] ?? '') === '1.0'
            && sanitize_key((string)($checkpoint['status'] ?? '')) === 'safe'
            && sanitize_text_field((string)($checkpoint['checkpoint_id'] ?? '')) !== '';
    }

    private function ebay_public_checkpoint_save($checkpoint) {
        $checkpoint = is_array($checkpoint) ? $checkpoint : array();
        $checkpoint['schema'] = '1.0';
        $checkpoint['status'] = 'safe';
        $checkpoint['updated_at'] = time();
        $checkpoint['business_campaign_ids'] = array_values(array_unique(array_filter(array_map('absint', (array)($checkpoint['business_campaign_ids'] ?? array())))));
        $checkpoint['private_listing_ids'] = array_values(array_unique(array_filter(array_map('absint', (array)($checkpoint['private_listing_ids'] ?? array())))));
        sort($checkpoint['business_campaign_ids'], SORT_NUMERIC);
        sort($checkpoint['private_listing_ids'], SORT_NUMERIC);
        if (sanitize_text_field((string)($checkpoint['checkpoint_id'] ?? '')) === '') {
            $checkpoint['checkpoint_id'] = substr(hash('sha256', wp_json_encode(array(
                'business'=>$checkpoint['business_campaign_ids'],
                'private'=>$checkpoint['private_listing_ids'],
                'at'=>microtime(true),
            ), JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)), 0, 24);
        }
        update_option($this->ebay_public_checkpoint_option_key(), $checkpoint, false);
        $verify = $this->ebay_public_checkpoint_load();
        return serialize($verify) === serialize($checkpoint) ? $checkpoint : false;
    }

    private function ebay_public_checkpoint_business_ids($checkpoint = null) {
        if (!is_array($checkpoint)) { $checkpoint = $this->ebay_public_checkpoint_load(); }
        if (!$this->ebay_public_checkpoint_is_safe($checkpoint)) { return array(); }
        $ids = array_values(array_unique(array_filter(array_map('absint', (array)($checkpoint['business_campaign_ids'] ?? array())))));
        sort($ids, SORT_NUMERIC);
        return $ids;
    }

    private function ebay_public_checkpoint_private_ids($checkpoint = null) {
        if (!is_array($checkpoint)) { $checkpoint = $this->ebay_public_checkpoint_load(); }
        if (!$this->ebay_public_checkpoint_is_safe($checkpoint)) { return array(); }
        $ids = array_values(array_unique(array_filter(array_map('absint', (array)($checkpoint['private_listing_ids'] ?? array())))));
        sort($ids, SORT_NUMERIC);
        return $ids;
    }

    private function ebay_public_checkpoint_allows_business_campaign($campaign_id) {
        $checkpoint = $this->ebay_public_checkpoint_load();
        if (!$this->ebay_public_checkpoint_is_safe($checkpoint)) { return true; }
        return in_array(absint($campaign_id), $this->ebay_public_checkpoint_business_ids($checkpoint), true);
    }

    private function ebay_public_checkpoint_allows_private_listing($listing_id) {
        $checkpoint = $this->ebay_public_checkpoint_load();
        if (!$this->ebay_public_checkpoint_is_safe($checkpoint)) { return true; }
        return in_array(absint($listing_id), $this->ebay_public_checkpoint_private_ids($checkpoint), true);
    }

    private function ebay_run_is_active($run = null) {
        if (!is_array($run)) { $run = $this->ebay_run_load(); }
        return (string)($run['schema'] ?? '') === '1.0'
            && in_array(sanitize_key((string)($run['status'] ?? '')), array('running','paused'), true)
            && !in_array(sanitize_key((string)($run['phase'] ?? '')), array('completed','failed'), true);
    }

    private function ebay_run_archive_terminal($run) {
        $run = is_array($run) ? $run : array();
        if ((string)($run['schema'] ?? '') !== '1.0') { return; }
        $status = sanitize_key((string)($run['status'] ?? ''));
        if (!in_array($status, array('failed','completed'), true)) { return; }
        $history = get_option($this->ebay_run_history_option_key(), array());
        $history = is_array($history) ? $history : array();
        $history[] = array(
            'run_uuid'=>sanitize_text_field((string)($run['run_uuid'] ?? '')),
            'status'=>$status,
            'phase'=>sanitize_key((string)($run['phase'] ?? '')),
            'error_code'=>sanitize_key((string)($run['error_code'] ?? '')),
            'started_at'=>absint($run['started_at'] ?? 0),
            'finished_at'=>absint($run['finished_at'] ?? 0),
            'build'=>sanitize_text_field((string)($run['build'] ?? '')),
            'checkpoint_id'=>sanitize_text_field((string)($run['checkpoint_id'] ?? $run['checkpoint_base_id'] ?? '')),
        );
        if (count($history) > 10) { $history = array_slice($history, -10); }
        update_option($this->ebay_run_history_option_key(), $history, false);
    }

    /**
     * V6.63.6 exact state-only recovery for the live build-change closure that was
     * produced after the V6.47 -> V6.63.4 transition. The old generic restart
     * button would create a new UUID. For this one proven state we instead re-enter
     * reconcile_local on the SAME UUID from the durable safe public checkpoint.
     * No provider/discovery/materialized tail from the incompatible build is trusted.
     */
    public function maybe_recover_ebay_build_change_checkpoint_same_uuid_v6636() {
        if (function_exists('current_user_can') && !current_user_can('manage_options')) { return; }
        $run=$this->ebay_run_load();
        if ((string)($run['schema']??'')!=='1.0' || sanitize_key((string)($run['status']??''))!=='failed'
            || sanitize_key((string)($run['error_code']??''))!=='run_build_changed_restart_required') { return; }
        $loaded=$run;
        $uuid=sanitize_text_field((string)($run['run_uuid']??'')); if($uuid===''){return;}
        $failure=$this->ebay_run_last_failure_entry($run,'run_build_changed_restart_required');
        $details=is_array($failure['details']??null)?$failure['details']:array();
        if(sanitize_key((string)($details['phase']??''))!=='reconcile_local'){return;}
        if(!hash_equals('6.63.4-live-observed-gap-proof-recovery-rootfix-20260828',sanitize_text_field((string)($details['build']??'')))){return;}
        if(!hash_equals('6.47.0-dynamic-business-rule-context-rootfix-20260821',sanitize_text_field((string)($details['previous_build']??'')))){return;}
        if((string)($run['progress_contract_version']??'')!=='3.1'){return;}
        $routes=is_array($run['config_snapshot']['seller_routes']??null)?$run['config_snapshot']['seller_routes']:array();
        if(empty($routes['private']) || empty($routes['business'])){return;}
        $checkpoint=$this->ebay_public_checkpoint_load();
        if(!$this->ebay_public_checkpoint_is_safe($checkpoint)){return;}
        $checkpoint_id=sanitize_text_field((string)($checkpoint['checkpoint_id']??''));
        $failed_checkpoint=sanitize_text_field((string)($run['checkpoint_id']??$details['checkpoint_id']??$run['checkpoint_base_id']??''));
        if($checkpoint_id==='' || $failed_checkpoint==='' || !hash_equals($checkpoint_id,$failed_checkpoint)){return;}
        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$uuid.'|'.$failure_at.'|same_uuid_safe_checkpoint_reentry|6.63.6');
        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $history[]=array('at'=>time(),'reason'=>'same_uuid_safe_checkpoint_reentry','error_code'=>'run_build_changed_restart_required','migration_key'=>$marker,
            'from_build'=>sanitize_text_field((string)($details['previous_build']??'')),'failure_build'=>sanitize_text_field((string)($details['build']??'')),
            'checkpoint_id'=>$checkpoint_id,'full_run_restarted'=>0,'new_uuid_created'=>0);
        if(count($history)>8){$history=array_slice($history,-8);}
        $run['recovery_history']=$history;
        $run['build']=self::EBAY_RUNTIME_BUILD;$run['status']='running';$run['phase']='reconcile_local';$run['finished_at']=0;
        $run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='external_tick';$run['resume_reason']='same_uuid_safe_checkpoint_reentry';
        $run['resume_at']=0;$run['no_progress_count']=0;$run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();
        $run['progress_contract_version']=$this->ebay_run_progress_contract_version();
        // Incompatible-build derived tails are intentionally discarded. The durable
        // safe public checkpoint is the sole starting truth, while the UUID persists.
        $run['phase_state']=array();$run['coverage']=array();$run['gapfill']=array('attempts'=>0,'missing'=>array());$run['end_manifest']=array();
        $run['checkpoint_base_id']=$checkpoint_id;$run['checkpoint_id']=$checkpoint_id;
        $run['checkpoint_candidate']=array('business_campaign_ids'=>$this->ebay_public_checkpoint_business_ids($checkpoint),'private_listing_ids'=>$this->ebay_public_checkpoint_private_ids($checkpoint));
        $run['checkpoint_cleanup_selection']=array();$run['checkpoint_verified_manifest']=array();
        $run['private_public_revalidation']=array();
        if($this->ebay_run_compare_and_swap($loaded,$run)===false){return;}
        update_option(self::OPTION_EBAY_SELECTION_STATE,array(),false);
        $this->ebay_run_bootstrap_recovered_external_tick_v6632($uuid);
    }

    /**
     * V6.63.8 exact live-state adoption.
     *
     * The observed production run can be left at reconcile_local with zero
     * transport ticks because V6.63.4 persists the run but delegates every
     * package to an external GitHub heartbeat. If that scheduler is delayed,
     * nothing in WordPress advances the already-authorized run.
     *
     * Only the exact zero-work state is safe to adopt across the build change:
     * no package, cursor or phase work has run yet. Preserve the UUID, checkpoint
     * and complete immutable run snapshot, change only the build/driver contract
     * and immediately start the private self-drive chain. Any state with actual
     * work remains subject to the generic fail-closed build-change rule below.
     */
    public function maybe_adopt_stalled_zero_tick_ebay_run_v6638() {
        $run = $this->ebay_run_load();
        if ((string)($run['schema'] ?? '') !== '1.0' || !$this->ebay_run_is_active($run)) { return; }
        if (!hash_equals('6.63.4-live-observed-gap-proof-recovery-rootfix-20260828', sanitize_text_field((string)($run['build'] ?? '')))) { return; }
        if (sanitize_key((string)($run['status'] ?? '')) !== 'running'
            || sanitize_key((string)($run['phase'] ?? '')) !== 'reconcile_local'
            || absint($run['progress_seq'] ?? 0) !== 0
            || absint($run['transport_tick_count'] ?? 0) !== 0
            || absint($run['phase_tick_count'] ?? 0) !== 0
            || sanitize_text_field((string)($run['owner'] ?? '')) !== ''
            || absint($run['lease_expires_at'] ?? 0) !== 0
            || absint($run['no_progress_count'] ?? 0) !== 0
            || sanitize_key((string)($run['error_code'] ?? '')) !== '') { return; }
        $phase_state = is_array($run['phase_state'] ?? null) ? $run['phase_state'] : array();
        if ($phase_state) { return; }

        $before = $run;
        $run['build'] = self::EBAY_RUNTIME_BUILD;
        $run['worker_transport'] = 'self_drive';
        $run['orchestrator_contract'] = 'self_drive_v1';
        $run['resume_reason'] = 'zero_tick_self_drive_adoption';
        $run['last_progress_at'] = time();
        $run['self_drive_adopted_at'] = time();
        $saved = $this->ebay_run_compare_and_swap($before, $run);
        if ($saved === false) { return; }
        $this->ebay_run_dispatch_self_drive((string)($run['run_uuid'] ?? ''), 'zero_tick_upgrade');
    }

    /** Generic future-proof upgrade rule: never revive a run from another build. */
    public function maybe_close_incompatible_ebay_run_for_checkpoint_restart() {
        $run = $this->ebay_run_load();
        if (!$this->ebay_run_is_active($run)) { return; }
        $old_build = sanitize_text_field((string)($run['build'] ?? ''));
        if ($old_build === '' || hash_equals($old_build, (string)self::EBAY_RUNTIME_BUILD)) { return; }
        $this->ebay_run_fail('run_build_changed_restart_required', 'Der alte Lauf wurde sauber beendet. Ein neuer Lauf startet vom letzten sicheren Checkpoint.', array(
            'previous_build'=>$old_build,
            'checkpoint_id'=>sanitize_text_field((string)($run['checkpoint_id'] ?? $run['checkpoint_base_id'] ?? '')),
        ));
    }

    private function ebay_run_checkpoint_staging_active() {
        if (empty($this->ebay_canonical_worker_active)) { return false; }
        $run = $this->ebay_run_load();
        return $this->ebay_run_is_open($run) && is_array($run['checkpoint_candidate'] ?? null);
    }

    private function ebay_public_checkpoint_bootstrap($settings) {
        $current = $this->ebay_public_checkpoint_load();
        if ($this->ebay_public_checkpoint_is_safe($current)) { return $current; }
        $settings = is_array($settings) ? $settings : array();
        $business_ids = array();
        $private_ids = array();
        global $wpdb;

        // Bootstrap is a snapshot of the already-safe PUBLIC house, not of the
        // routes selected for the next run. A BUSINESS-only run must therefore
        // preserve the current PRIVATE floor and vice versa.
        if (is_object($wpdb) && method_exists($wpdb, 'get_results') && method_exists($this, 'output_objects_table')) {
            $wpdb->last_error = '';
            $rows = (array)$wpdb->get_results("SELECT * FROM {$this->output_objects_table()} WHERE provider='ebay' AND output_type='product_campaign' AND status='published' AND campaign_post_id>0 ORDER BY id ASC LIMIT 1201", ARRAY_A);
            if (trim((string)($wpdb->last_error ?? '')) !== '') {
                return new WP_Error('public_checkpoint_bootstrap_storage_failed', 'Der sichere BUSINESS-Ausgangsbestand konnte nicht vollständig gelesen werden.');
            }
            if (count($rows) >= 1201) {
                return new WP_Error('public_checkpoint_bootstrap_bound_exceeded', 'Der sichere BUSINESS-Ausgangsbestand überschreitet die harte Bootstrap-Grenze.');
            }
            $per_concept = array();
            foreach ($rows as $object) {
                $campaign_id = absint($object['campaign_post_id'] ?? 0);
                if ($campaign_id <= 0 || !method_exists($this, 'output_campaign_by_post_id')) { continue; }
                $campaign = $this->output_campaign_by_post_id($campaign_id);
                if (!is_array($campaign) || empty($campaign['active'])) { continue; }
                if (method_exists($this, 'ebay_business_campaign_source_allows_delivery_base') && !$this->ebay_business_campaign_source_allows_delivery_base($campaign)) { continue; }
                $source = method_exists($this, 'ebay_business_campaign_source_row') ? $this->ebay_business_campaign_source_row($campaign) : array();
                $concept = sanitize_key((string)($source['rule_id'] ?? ''));
                if ($concept === '') { continue; }
                if (absint($per_concept[$concept] ?? 0) >= 3) { continue; }
                $per_concept[$concept] = absint($per_concept[$concept] ?? 0) + 1;
                $business_ids[] = $campaign_id;
            }
        }

        if (is_object($wpdb) && isset($wpdb->posts) && method_exists($wpdb, 'get_col') && method_exists($wpdb, 'prepare')) {
            $postmeta = isset($wpdb->postmeta) ? $wpdb->postmeta : $wpdb->prefix . 'postmeta';
            $wpdb->last_error = '';
            $ids = (array)$wpdb->get_col("SELECT DISTINCT p.ID FROM {$wpdb->posts} p INNER JOIN {$postmeta} pm ON pm.post_id=p.ID WHERE p.post_type='hp_listing' AND p.post_status='publish' AND pm.meta_key='_ppar_ebay_item_id' ORDER BY p.ID ASC LIMIT 1001");
            if (trim((string)($wpdb->last_error ?? '')) !== '') {
                return new WP_Error('public_checkpoint_bootstrap_storage_failed', 'Der sichere PRIVATE-Ausgangsbestand konnte nicht vollständig gelesen werden.');
            }
            if (count($ids) >= 1001) {
                return new WP_Error('public_checkpoint_bootstrap_bound_exceeded', 'Der sichere PRIVATE-Ausgangsbestand überschreitet die harte Bootstrap-Grenze.');
            }
            // Preserve the currently safe public set independently of the next
            // run's route snapshot. Existing public safety decides membership;
            // the next run's cap is not allowed to truncate the safe base.
            foreach ($ids as $id) {
                $id = absint($id); if ($id <= 0) { continue; }
                $item_id = function_exists('get_post_meta') ? sanitize_text_field((string)get_post_meta($id, '_ppar_ebay_item_id', true)) : '';
                if ($item_id === '') { continue; }
                $wpdb->last_error = '';
                $source = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->ebay_items_table()} WHERE item_id=%s AND seller_account_type='INDIVIDUAL' ORDER BY id DESC LIMIT 1", $item_id), ARRAY_A);
                if (trim((string)($wpdb->last_error ?? '')) !== '') {
                    return new WP_Error('public_checkpoint_bootstrap_storage_failed', 'Der sichere PRIVATE-Ausgangsbestand konnte nicht vollständig aufgelöst werden.');
                }
                $post = function_exists('get_post') ? get_post($id) : null;
                if (!is_object($post)) { continue; }
                if (method_exists($this, 'ebay_private_public_post_allowed_base') && !$this->ebay_private_public_post_allowed_base($post, is_array($source)?$source:array(), true, time())) { continue; }
                $private_ids[] = $id;
            }
        }

        $checkpoint = array(
            'checkpoint_id'=>substr(hash('sha256', 'bootstrap|'.microtime(true).'|'.wp_json_encode(array($business_ids,$private_ids))), 0, 24),
            'created_at'=>time(),
            'source'=>'bootstrap_current_safe_public_subset',
            'run_uuid'=>'',
            'business_campaign_ids'=>$business_ids,
            'private_listing_ids'=>$private_ids,
            'verification'=>array('business_visible'=>count($business_ids),'private_visible'=>count($private_ids)),
        );
        $saved = $this->ebay_public_checkpoint_save($checkpoint);
        return $saved !== false ? $saved : new WP_Error('public_checkpoint_bootstrap_failed', 'Der sichere öffentliche Ausgangscheckpoint konnte nicht gespeichert werden.');
    }

    private function ebay_run_checkpoint_business_ids_from_selection($selection, $existing = array(), $mode = 'full') {
        $selection = is_array($selection) ? $selection : array();
        $mode = sanitize_key((string)$mode);
        $ids = array_values(array_unique(array_filter(array_map('absint', (array)$existing))));
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb, 'get_row') || !method_exists($wpdb, 'get_results')) { return $ids; }
        $targets = array_values(array_unique(array_filter(array_map('sanitize_key', (array)($selection['business_target_concepts'] ?? array())))));
        if ($mode !== 'gapfill') {
            $ids = array();
        } elseif ($targets) {
            $target_map = array_fill_keys($targets, true);
            $kept = array();
            foreach ($ids as $campaign_id) {
                $campaign = method_exists($this, 'output_campaign_by_post_id') ? $this->output_campaign_by_post_id($campaign_id) : null;
                $source = is_array($campaign) && method_exists($this, 'ebay_business_campaign_source_row') ? $this->ebay_business_campaign_source_row($campaign) : array();
                $concept = sanitize_key((string)($source['rule_id'] ?? ''));
                if ($concept === '' || !isset($target_map[$concept])) { $kept[] = $campaign_id; }
            }
            $ids = $kept;
        }

        $rows = array();
        foreach ((array)($selection['business_active'] ?? array()) as $item_id=>$entry) {
            $item_id = sanitize_text_field((string)$item_id); if ($item_id === '') { continue; }
            $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->ebay_items_table()} WHERE item_id=%s AND seller_account_type='BUSINESS' ORDER BY id DESC LIMIT 1", $item_id), ARRAY_A);
            if (is_array($row)) { $rows[] = $row; }
        }
        foreach ((array)($selection['business_soft_failed'] ?? array()) as $item_id=>$entry) {
            $entry = is_array($entry) ? $entry : array();
            $row_id = absint($entry['row_id'] ?? 0);
            if ($row_id > 0) {
                $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->ebay_items_table()} WHERE id=%d AND seller_account_type='BUSINESS'", $row_id), ARRAY_A);
            } else {
                $item_id = sanitize_text_field((string)$item_id);
                $row = $item_id !== '' ? $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->ebay_items_table()} WHERE item_id=%s AND seller_account_type='BUSINESS' ORDER BY id DESC LIMIT 1", $item_id), ARRAY_A) : null;
            }
            if (is_array($row)) { $rows[] = $row; }
        }
        foreach ($rows as $row) {
            $hash = strtolower(sanitize_text_field((string)($row['creative_identity_hash'] ?? '')));
            if (!preg_match('/^[a-f0-9]{64}$/', $hash) || !method_exists($this, 'output_objects_table')) { continue; }
            $objects = (array)$wpdb->get_results($wpdb->prepare("SELECT * FROM {$this->output_objects_table()} WHERE provider='ebay' AND output_type='product_campaign' AND creative_identity_hash=%s AND campaign_post_id>0 ORDER BY id ASC", $hash), ARRAY_A);
            foreach ($objects as $object) {
                $campaign_id = absint($object['campaign_post_id'] ?? 0); if ($campaign_id <= 0) { continue; }
                $campaign = method_exists($this, 'output_campaign_by_post_id') ? $this->output_campaign_by_post_id($campaign_id) : null;
                if (!is_array($campaign) || empty($campaign['active'])) { continue; }
                if (method_exists($this, 'ebay_business_campaign_source_allows_delivery_base') && !$this->ebay_business_campaign_source_allows_delivery_base($campaign)) { continue; }
                $ids[] = $campaign_id;
            }
        }
        $ids = array_values(array_unique(array_filter(array_map('absint', $ids))));
        sort($ids, SORT_NUMERIC);
        return $ids;
    }

    /**
     * V6.63.3 durable BUSINESS gap-fill proof.
     *
     * `phase_state.selection` is the current selector cursor and is legitimately
     * replaced by the required PRIVATE tail. The BUSINESS safe-gap contract must
     * therefore not use that mutable cursor as its only proof source. Persist the
     * minimal terminal canonical-gapfill evidence inside the gapfill state itself.
     * No source rows, campaign payloads or PRIVATE data are duplicated here.
     */
    private function ebay_run_business_gapfill_proof_from_selection($selection, $run_uuid) {
        $selection=is_array($selection)?$selection:array();
        $uuid=sanitize_text_field((string)$run_uuid);
        if($uuid==='' || sanitize_key((string)($selection['status']??''))!=='complete'
            || sanitize_key((string)($selection['reason']??''))!=='canonical_gapfill'
            || sanitize_key((string)($selection['selection_scope']??''))!=='business'
            || sanitize_text_field((string)($selection['owner']??''))!=='run:'.$uuid
            || sanitize_key((string)($selection['business_target_mode']??''))!=='gapfill'){
            return array();
        }
        $targets=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($selection['business_target_concepts']??array())))));
        sort($targets,SORT_STRING);
        if(!$targets){return array();}
        $selected=array();
        foreach((array)($selection['business_active']??array()) as $entry){
            if(!is_array($entry)){continue;}
            $concept=sanitize_key((string)($entry['concept']??''));
            if($concept!==''){$selected[$concept]=1;}
        }
        $selected=array_keys($selected);sort($selected,SORT_STRING);
        return array(
            'version'=>'1.0','status'=>'complete','reason'=>'canonical_gapfill',
            'selection_scope'=>'business','owner'=>'run:'.$uuid,
            'business_target_mode'=>'gapfill','business_target_concepts'=>$targets,
            'selected_concepts'=>$selected,'captured_at'=>time(),
        );
    }

    private function ebay_run_checkpoint_capture_selection($selection, $mode = 'full') {
        $selection = is_array($selection) ? $selection : array();
        $run = $this->ebay_run_load();
        if (!$this->ebay_run_is_open($run)) { return false; }
        $mode = sanitize_key((string)$mode);
        $candidate = is_array($run['checkpoint_candidate'] ?? null) ? $run['checkpoint_candidate'] : array('business_campaign_ids'=>array(),'private_listing_ids'=>array());
        $scope = sanitize_key((string)($selection['selection_scope'] ?? $this->ebay_run_selection_scope($run)));
        if ($scope !== 'private') {
            $candidate['business_campaign_ids'] = $this->ebay_run_checkpoint_business_ids_from_selection($selection, (array)($candidate['business_campaign_ids'] ?? array()), $mode);
        }
        if ($mode !== 'gapfill' && $scope !== 'business') {
            $candidate['private_listing_ids'] = array_values(array_unique(array_filter(array_map('absint', array_values((array)($selection['private_keep_posts'] ?? array()))))));
            sort($candidate['private_listing_ids'], SORT_NUMERIC);
        }
        $run['checkpoint_candidate'] = $candidate;

        if ($mode !== 'gapfill') {
            if ($scope === 'private') {
                // PRIVATE tail revalidation runs after an already-completed BUSINESS
                // selection/gap-fill. Replacing the cleanup plan here would erase the
                // BUSINESS active/reserve proof and could make final checkpoint cleanup
                // treat every BUSINESS row as unselected. Merge only PRIVATE-owned state.
                $base = is_array($run['checkpoint_cleanup_selection'] ?? null) ? $run['checkpoint_cleanup_selection'] : array();
                foreach ($selection as $key=>$value) {
                    $key = (string)$key;
                    if (strpos($key, 'private') === 0 || strpos($key, 'prepare_private') === 0) {
                        $base[$key] = $value;
                    }
                }
                $base_stats = is_array($base['stats'] ?? null) ? $base['stats'] : array();
                $sel_stats = is_array($selection['stats'] ?? null) ? $selection['stats'] : array();
                if (isset($sel_stats['private'])) { $base_stats['private'] = $sel_stats['private']; }
                $base['stats'] = $base_stats;
                unset($base['checkpoint_private_cleanup_initialized'], $base['checkpoint_private_cleanup_done']);
                $run['checkpoint_cleanup_selection'] = $base;
            } else {
                $run['checkpoint_cleanup_selection'] = $selection;
            }
        } else {
            $proof=$this->ebay_run_business_gapfill_proof_from_selection($selection,(string)($run['run_uuid']??''));
            if(!isset($run['gapfill'])||!is_array($run['gapfill'])){$run['gapfill']=array();}
            if($proof){$run['gapfill']['selection_proof']=$proof;}else{unset($run['gapfill']['selection_proof']);}
            $base = is_array($run['checkpoint_cleanup_selection'] ?? null) ? $run['checkpoint_cleanup_selection'] : array();
            $targets = array_values(array_unique(array_filter(array_map('sanitize_key', (array)($selection['business_target_concepts'] ?? array())))));
            $target_map = array_fill_keys($targets, true);
            foreach (array('business_active','business_reserve','business_soft_failed') as $key) {
                $old = is_array($base[$key] ?? null) ? $base[$key] : array();
                foreach ($old as $item_id=>$entry) {
                    $entry_arr = is_array($entry) ? $entry : array();
                    $concept = sanitize_key((string)($entry_arr['concept'] ?? ''));
                    if ($concept !== '' && isset($target_map[$concept])) { unset($old[$item_id]); }
                }
                foreach ((array)($selection[$key] ?? array()) as $item_id=>$entry) { $old[$item_id] = $entry; }
                $base[$key] = $old;
            }
            $run['checkpoint_cleanup_selection'] = $base;
        }
        return $this->ebay_run_save($run);
    }

    private function ebay_run_commit_public_checkpoint($run, $business, $private) {
        $run = is_array($run) ? $run : $this->ebay_run_load();
        $candidate = is_array($run['checkpoint_candidate'] ?? null) ? $run['checkpoint_candidate'] : array();
        $checkpoint = array(
            'checkpoint_id'=>substr(hash('sha256', sanitize_text_field((string)($run['run_uuid'] ?? '')).'|'.microtime(true).'|'.wp_json_encode($candidate)), 0, 24),
            'created_at'=>time(),
            'source'=>'canonical_public_verify',
            'run_uuid'=>sanitize_text_field((string)($run['run_uuid'] ?? '')),
            'business_campaign_ids'=>(array)($candidate['business_campaign_ids'] ?? array()),
            'private_listing_ids'=>(array)($candidate['private_listing_ids'] ?? array()),
            'verification'=>array('business'=>$business,'private'=>$private),
        );
        return $this->ebay_public_checkpoint_save($checkpoint);
    }

    private function ebay_run_load() {
        $run = get_option($this->ebay_run_option_key(), array());
        return is_array($run) ? $run : array();
    }

    private function ebay_run_save($run) {
        $run = is_array($run) ? $run : array();
        $run['schema'] = '1.0';
        $run['build'] = self::EBAY_RUNTIME_BUILD;
        $run['updated_at'] = time();
        update_option($this->ebay_run_option_key(), $run, false);
        return $run;
    }

    /**
     * Persist one state-only transition only if the exact snapshot that was
     * inspected is still current. This is deliberately separate from ordinary
     * worker saves: init migrations execute outside the worker lease and must
     * never be able to replay a stale whole-run snapshot over a newer cursor.
     *
     * Returns the persisted run on success, false when another request changed
     * the durable run first. A CAS miss is not an error: the next request must
     * re-evaluate the now-current state instead of forcing the old transition.
     */
    private function ebay_run_compare_and_swap($before, $after) {
        $before = is_array($before) ? $before : array();
        $after = is_array($after) ? $after : array();
        $after['schema'] = '1.0';
        $after['build'] = self::EBAY_RUNTIME_BUILD;
        $after['updated_at'] = time();
        $key = $this->ebay_run_option_key();

        global $wpdb;
        if (is_object($wpdb) && isset($wpdb->options) && method_exists($wpdb, 'query')
            && method_exists($wpdb, 'prepare') && function_exists('maybe_serialize')) {
            $before_serialized = maybe_serialize($before);
            $after_serialized = maybe_serialize($after);
            $changed = $wpdb->query($wpdb->prepare(
                "UPDATE {$wpdb->options} SET option_value=%s WHERE option_name=%s AND option_value=%s",
                $after_serialized, $key, $before_serialized
            ));
            if ((int)$changed !== 1) { return false; }
            if (function_exists('wp_cache_delete')) {
                wp_cache_delete($key, 'options');
                wp_cache_delete('alloptions', 'options');
            }
            return $after;
        }

        // Deterministic test/stub fallback. Compare the complete durable value
        // immediately before writing; if it moved, fail closed and do not write.
        $current = $this->ebay_run_load();
        if (serialize($current) !== serialize($before)) { return false; }
        update_option($key, $after, false);
        $verify = $this->ebay_run_load();
        return serialize($verify) === serialize($after) ? $after : false;
    }

    private function ebay_run_is_open($run = null) {
        if (!is_array($run)) { $run = $this->ebay_run_load(); }
        return (string)($run['schema'] ?? '') === '1.0'
            && in_array(sanitize_key((string)($run['status'] ?? '')), array('running'), true)
            && !in_array(sanitize_key((string)($run['phase'] ?? '')), array('completed','failed'), true);
    }

    private function ebay_run_phase_state_load($key) {
        $key = sanitize_key((string)$key);
        if ($key === '') { return array(); }
        $run = $this->ebay_run_load();
        if ($this->ebay_run_is_open($run) || (string)($run['schema'] ?? '') === '1.0') {
            $phase_state = is_array($run['phase_state'] ?? null) ? $run['phase_state'] : array();
            $state = $phase_state[$key] ?? array();
            return is_array($state) ? $state : array();
        }
        return array();
    }

    private function ebay_run_phase_state_save($key, $state) {
        $key = sanitize_key((string)$key);
        if ($key === '') { return false; }
        $run = $this->ebay_run_load();
        if ((string)($run['schema'] ?? '') !== '1.0') { return false; }
        if (!isset($run['phase_state']) || !is_array($run['phase_state'])) { $run['phase_state'] = array(); }
        $run['phase_state'][$key] = is_array($state) ? $state : array();
        $this->ebay_run_save($run);
        return true;
    }

    private function ebay_run_context_active() {
        return !empty($this->ebay_canonical_worker_active) && $this->ebay_run_is_open();
    }

    private function ebay_run_worker_transport_migration_key() {
        $constant = static::class . '::OPTION_EBAY_WORKER_TRANSPORT_MIGRATION';
        return defined($constant) ? (string)constant($constant) : 'ppar_ebay_worker_transport_migration_v6412';
    }

    /** V6.63.8 canonical driver.
     *
     * The fach worker remains single-owner and bounded. Continuation no longer
     * depends on a delayed external scheduler: exactly one signed same-origin
     * loopback request is queued for the already-authorized run. The public
     * external heartbeat remains a watchdog/kick path only.
     */
    private function ebay_run_schedule_worker($delay = 10) {
        $run = $this->ebay_run_load();
        if (!$this->ebay_run_is_active($run)) { return false; }
        return $this->ebay_run_dispatch_self_drive((string)($run['run_uuid'] ?? ''), 'schedule');
    }

    /** Compatibility no-ops retained so older state/tests cannot accidentally
     * revive the retired WP-Cron/background-dispatch transports. */
    private function ebay_run_register_background_dispatch($when) { return false; }
    private function ebay_run_spawn_core_cron_handoff() { return false; }
    private function ebay_run_wait_for_cron_lock_resolution($initial_lock, $max_wait_seconds = 5) { return false; }
    private function ebay_run_fail_background_dispatch($code, $details = array()) { return false; }
    public function run_ebay_worker_background_dispatch() { return false; }

    /** Stateless signed continuation contract.
     *
     * No per-package transient/option is written. The signature is bound to the
     * exact run UUID plus the current progress/tick counters. A replay therefore
     * becomes stale as soon as one canonical package starts, while the existing
     * lease remains the final concurrency guard for a simultaneous duplicate.
     */
    private function ebay_run_self_drive_secret() {
        if (!function_exists('wp_salt')) { return ''; }
        $secret = (string)wp_salt('auth');
        return strlen($secret) >= 32 ? $secret : '';
    }

    private function ebay_run_self_drive_signature($run_uuid, $progress_seq, $transport_tick_count, $expires_at, $nonce) {
        $secret = $this->ebay_run_self_drive_secret();
        $uuid = sanitize_text_field((string)$run_uuid);
        $nonce = sanitize_text_field((string)$nonce);
        if ($secret === '' || $uuid === '' || $nonce === '') { return ''; }
        $message = implode('|', array(
            $uuid,
            (string)absint($progress_seq),
            (string)absint($transport_tick_count),
            (string)absint($expires_at),
            $nonce,
            'self_drive_v1',
        ));
        return hash_hmac('sha256', $message, $secret);
    }

    private function ebay_run_validate_self_drive_request($signature, $run_uuid, $expected_progress, $expected_tick, $expires_at, $nonce) {
        $signature = strtolower(trim((string)$signature));
        $uuid = sanitize_text_field((string)$run_uuid);
        $nonce = sanitize_text_field((string)$nonce);
        $expires_at = absint($expires_at);
        $now = time();
        $ttl = max(60, absint(self::EBAY_SELF_DRIVE_TOKEN_TTL));
        if ($uuid === '' || !preg_match('/^[a-f0-9]{64}$/', $signature) || !preg_match('/^[a-f0-9]{32,96}$/', $nonce)) { return false; }
        if ($expires_at < $now || $expires_at > ($now + $ttl + 5)) { return false; }
        $expected = $this->ebay_run_self_drive_signature($uuid, $expected_progress, $expected_tick, $expires_at, $nonce);
        if ($expected === '' || !hash_equals($expected, $signature)) { return false; }

        $run = $this->ebay_run_load();
        if (!$this->ebay_run_is_active($run)
            || !hash_equals($uuid, sanitize_text_field((string)($run['run_uuid'] ?? '')))
            || absint($run['progress_seq'] ?? 0) !== absint($expected_progress)
            || absint($run['transport_tick_count'] ?? 0) !== absint($expected_tick)) { return false; }
        return true;
    }

    private function ebay_run_dispatch_self_drive($run_uuid, $reason = 'continuation') {
        $uuid = sanitize_text_field((string)$run_uuid);
        if ($uuid === '' || !function_exists('wp_safe_remote_post') || !function_exists('admin_url')
            || !function_exists('home_url') || !function_exists('wp_parse_url')) { return false; }

        $run = $this->ebay_run_load();
        if (!$this->ebay_run_is_active($run) || !hash_equals($uuid, sanitize_text_field((string)($run['run_uuid'] ?? '')))) { return false; }
        $secret = $this->ebay_run_self_drive_secret();
        if ($secret === '') { return false; }
        try { $nonce = bin2hex(random_bytes(24)); } catch (Throwable $e) { return false; }
        $expires_at = time() + max(60, absint(self::EBAY_SELF_DRIVE_TOKEN_TTL));
        $expected_progress = absint($run['progress_seq'] ?? 0);
        $expected_tick = absint($run['transport_tick_count'] ?? 0);
        $signature = $this->ebay_run_self_drive_signature($uuid, $expected_progress, $expected_tick, $expires_at, $nonce);
        if ($signature === '') { return false; }

        $endpoint = admin_url('admin-post.php');
        $home = home_url('/');
        if ($endpoint === '' || $home === '') { return false; }
        $u = wp_parse_url($endpoint); $h = wp_parse_url($home);
        if (!is_array($u) || !is_array($h)) { return false; }
        $scheme = strtolower((string)($u['scheme'] ?? ''));
        $host = strtolower((string)($u['host'] ?? ''));
        $home_scheme = strtolower((string)($h['scheme'] ?? ''));
        $home_host = strtolower((string)($h['host'] ?? ''));
        $port = absint($u['port'] ?? ($scheme === 'https' ? 443 : 80));
        $home_port = absint($h['port'] ?? ($home_scheme === 'https' ? 443 : 80));
        if ($scheme !== 'https' || $home_scheme !== 'https' || $host === '' || !hash_equals($home_host, $host) || $port !== $home_port) { return false; }

        $response = wp_safe_remote_post($endpoint, array(
            'timeout'=>1,
            'blocking'=>false,
            'redirection'=>0,
            'sslverify'=>apply_filters('https_local_ssl_verify', false),
            'headers'=>array('Cache-Control'=>'no-store'),
            'body'=>array(
                'action'=>self::EBAY_SELF_DRIVE_ACTION,
                'signature'=>$signature,
                'run_uuid'=>$uuid,
                'expected_progress'=>$expected_progress,
                'expected_tick'=>$expected_tick,
                'expires_at'=>$expires_at,
                'nonce'=>$nonce,
                'reason'=>sanitize_key((string)$reason),
            ),
            'user-agent'=>'Affiliate-Zentrale/'.self::VERSION.'; '.home_url('/'),
        ));
        return !is_wp_error($response);
    }

    /** Runtime core for the signed private driver; kept return-based so the
     * complete signature/UUID/state/lease behaviour is locally testable without
     * coupling the test harness to admin-post exit semantics. */
    private function ebay_run_handle_self_drive_request($signature, $run_uuid, $expected_progress, $expected_tick, $expires_at, $nonce) {
        $uuid = sanitize_text_field((string)$run_uuid);
        if (!$this->ebay_run_validate_self_drive_request($signature, $uuid, $expected_progress, $expected_tick, $expires_at, $nonce)) {
            return array('status'=>'forbidden','run_uuid'=>$uuid,'next_dispatched'=>0);
        }

        $result = $this->run_ebay_canonical_worker();
        $fresh = $this->ebay_run_load();
        $tick = sanitize_key((string)($result['tick_result'] ?? 'retryable_error'));
        $next = false;
        if ($this->ebay_run_is_active($fresh) && in_array($tick, array('advanced','retryable_error'), true)) {
            $next = $this->ebay_run_dispatch_self_drive($uuid, 'continuation');
        }
        return array(
            'status'=>$tick,
            'reason'=>sanitize_key((string)($result['reason'] ?? '')),
            'run_uuid'=>$uuid,
            'next_dispatched'=>$next ? 1 : 0,
            'progress_before'=>absint($result['progress_before'] ?? 0),
            'progress_after'=>absint($result['progress_after'] ?? ($fresh['progress_seq'] ?? 0)),
        );
    }

    public function handle_ebay_self_drive_worker() {
        $signature = isset($_POST['signature']) ? (string)wp_unslash($_POST['signature']) : '';
        $uuid = isset($_POST['run_uuid']) ? sanitize_text_field((string)wp_unslash($_POST['run_uuid'])) : '';
        $expected_progress = isset($_POST['expected_progress']) ? absint(wp_unslash($_POST['expected_progress'])) : 0;
        $expected_tick = isset($_POST['expected_tick']) ? absint(wp_unslash($_POST['expected_tick'])) : 0;
        $expires_at = isset($_POST['expires_at']) ? absint(wp_unslash($_POST['expires_at'])) : 0;
        $nonce = isset($_POST['nonce']) ? sanitize_text_field((string)wp_unslash($_POST['nonce'])) : '';
        $result = $this->ebay_run_handle_self_drive_request($signature, $uuid, $expected_progress, $expected_tick, $expires_at, $nonce);
        if (sanitize_key((string)($result['status'] ?? '')) === 'forbidden') {
            if (function_exists('status_header')) { status_header(403); }
            exit;
        }
        if (function_exists('status_header')) { status_header(204); }
        exit;
    }

    private function ebay_external_tick_url() {
        if (!function_exists('rest_url')) { return ''; }
        return rest_url(self::EBAY_EXTERNAL_TICK_REST_NAMESPACE . self::EBAY_EXTERNAL_TICK_REST_ROUTE);
    }

    public function register_ebay_external_tick_route() {
        if (!function_exists('register_rest_route')) { return; }
        register_rest_route(self::EBAY_EXTERNAL_TICK_REST_NAMESPACE, self::EBAY_EXTERNAL_TICK_REST_ROUTE, array(
            'methods'=>'POST',
            'callback'=>array($this,'handle_ebay_external_tick'),
            'permission_callback'=>'__return_true',
        ));
    }

    /** Public heartbeat admission gate. The endpoint cannot change settings or
     * choose an operation; it can only advance already-authorized canonical work.
     * A durable 45s rate gate bounds abusive/repeated calls before any fach work. */
    private function ebay_external_tick_admit() {
        $now = time();
        $key = self::OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK;
        $last = absint(get_option($key, 0));
        if ($last > 0 && ($now - $last) < 45) { return false; }
        if ($last > 0) { delete_option($key); }
        if (add_option($key, $now, '', false)) { return true; }
        $last = absint(get_option($key, 0));
        if ($last > 0 && ($now - $last) < 45) { return false; }
        update_option($key, $now, false);
        return true;
    }

    /** Determine the next automatic canonical operation without any server cron.
     * Discovery owns the complete 3h cycle; otherwise refresh is due hourly. */
    private function ebay_external_tick_due_operation($settings) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        if (empty($settings['enabled'])) { return ''; }
        $now = time();
        $sync = is_array($settings['last_sync'] ?? null) ? $settings['last_sync'] : array();
        $refresh = is_array($settings['last_refresh'] ?? null) ? $settings['last_refresh'] : array();
        $last_sync = absint($sync['finished_at'] ?? 0);
        $last_refresh = absint($refresh['finished_at'] ?? 0);
        if ($last_sync <= 0 || ($now - $last_sync) >= 3 * HOUR_IN_SECONDS) { return 'sync'; }
        if (!empty($settings['inventory_refresh_enabled']) && ($last_refresh <= 0 || ($now - $last_refresh) >= HOUR_IN_SECONDS)) { return 'refresh'; }
        return '';
    }

    /** KISS public heartbeat. One POST performs at most one bounded canonical
     * package. The caller gets no control over provider, operation or settings.
     * Candidate-local failures remain skippable inside the worker; terminal
     * system failures remain terminal until an explicit admin restart. */
    public function handle_ebay_external_tick($request) {
        if (function_exists('nocache_headers')) { nocache_headers(); }
        if (!$this->ebay_external_tick_admit()) {
            $out = array('status'=>'throttled','transport'=>'external_tick','server_time'=>time(),'contract'=>'external_tick_v2');
            return function_exists('rest_ensure_response') ? rest_ensure_response($out) : $out;
        }

        $settings = $this->ebay_settings();
        if (empty($settings['enabled'])) {
            $out=array('status'=>'disabled','transport'=>'external_tick','server_time'=>time(),'contract'=>'external_tick_v2');
            return function_exists('rest_ensure_response') ? rest_ensure_response($out) : $out;
        }

        $run = $this->ebay_run_load();
        $recovery_run = '';
        if (is_object($request) && method_exists($request, 'get_param')) {
            $recovery_run = sanitize_text_field((string)$request->get_param('recovery_run'));
        } elseif (is_array($request)) {
            $recovery_run = sanitize_text_field((string)($request['recovery_run'] ?? ''));
        }
        // A one-shot recovery bootstrap is bound to the exact reopened run UUID.
        // If it arrives late, it must never turn into the generic due-operation
        // path and accidentally start a successor run. Ordinary heartbeat calls
        // carry no recovery_run and retain the existing KISS behaviour.
        if ($recovery_run !== '') {
            $current_uuid = sanitize_text_field((string)($run['run_uuid'] ?? ''));
            $current_status = sanitize_key((string)($run['status'] ?? ''));
            $resume_reason = sanitize_key((string)($run['resume_reason'] ?? ''));
            $recovery_reason_ok=in_array($resume_reason,array('private_public_gate_recovery','business_gap_proof_recovery','private_public_freshness_revalidation'),true);
            if ($current_uuid === '' || !hash_equals($current_uuid, $recovery_run) || !$this->ebay_run_is_active($run) || !$recovery_reason_ok) {
                $status = $current_status === 'completed' ? 'completed' : ($current_status === 'failed' ? 'failed' : 'idle');
                $out=array('status'=>$status,'transport'=>'external_tick','server_time'=>time(),'contract'=>'external_tick_v2','run_uuid'=>$current_uuid,'reason'=>'stale_recovery_bootstrap');
                return function_exists('rest_ensure_response') ? rest_ensure_response($out) : $out;
            }
        }
        $stored_status = sanitize_key((string)($run['status'] ?? ''));
        if ((string)($run['schema'] ?? '') === '1.0' && $stored_status === 'failed') {
            $out=array(
                'status'=>'failed','transport'=>'external_tick','restart_required'=>1,'server_time'=>time(),'contract'=>'external_tick_v2',
                'run_uuid'=>sanitize_text_field((string)($run['run_uuid']??'')),
                'phase'=>sanitize_key((string)($run['phase']??'failed')),
                'error_code'=>sanitize_key((string)($run['error_code']??'')),
            );
            return function_exists('rest_ensure_response') ? rest_ensure_response($out) : $out;
        }

        if (!$this->ebay_run_is_active($run)) {
            $operation = $this->ebay_external_tick_due_operation($settings);
            if ($operation === '') {
                $out=array('status'=>'idle','transport'=>'external_tick','server_time'=>time(),'contract'=>'external_tick_v2');
                return function_exists('rest_ensure_response') ? rest_ensure_response($out) : $out;
            }
            $started = $this->ebay_run_start(false, $operation);
            if (is_wp_error($started)) { return $started; }
        }

        $result = $this->run_ebay_canonical_worker();
        if (!is_array($result)) {
            $result=array('tick_result'=>'retryable_error','reason'=>'worker_result_missing');
        }
        $fresh = $this->ebay_run_load();
        $tick_result=sanitize_key((string)($result['tick_result']??'retryable_error'));
        if(!in_array($tick_result,array('advanced','busy','retryable_error','completed','failed'),true)){$tick_result='retryable_error';}
        $self_drive_handoff=false;
        if($this->ebay_run_is_active($fresh) && in_array($tick_result,array('advanced','retryable_error'),true)){
            $self_drive_handoff=$this->ebay_run_dispatch_self_drive((string)($fresh['run_uuid']??''),'external_watchdog');
        }
        $out=array(
            'status'=>$tick_result,
            'run_status'=>sanitize_key((string)($fresh['status']??'idle')),
            'phase'=>sanitize_key((string)($fresh['phase']??'idle')),
            'transport'=>'external_tick',
            'server_time'=>time(),
            'contract'=>'external_tick_v2',
            'run_uuid'=>sanitize_text_field((string)($fresh['run_uuid']??'')),
            'progress_seq'=>absint($fresh['progress_seq']??0),
            'progress_before'=>absint($result['progress_before']??0),
            'progress_after'=>absint($result['progress_after']??($fresh['progress_seq']??0)),
            'reason'=>sanitize_key((string)($result['reason']??'')),
            'tick_count'=>absint($fresh['transport_tick_count']??0),
            'no_progress_count'=>absint($fresh['no_progress_count']??0),
            'skipped_item_errors'=>absint($fresh['skipped_item_errors_count']??0),
            'completed_with_skips'=>!empty($fresh['completed_with_skips'])?1:0,
            'error_code'=>sanitize_key((string)($fresh['error_code']??'')),
            'self_drive_handoff'=>$self_drive_handoff?1:0,
        );
        return function_exists('rest_ensure_response') ? rest_ensure_response($out) : $out;
    }

    private function ebay_run_pause_for_budget($run, $reason = 'work_block_budget') {
        $run = is_array($run) ? $run : $this->ebay_run_load();
        if (!$this->ebay_run_is_open($run)) { return $run; }
        $pause_seconds = defined(static::class . '::EBAY_WORK_BLOCK_PAUSE_SECONDS') ? absint(constant(static::class . '::EBAY_WORK_BLOCK_PAUSE_SECONDS')) : 1;
        $pause_seconds = max(1, $pause_seconds);
        $run['status'] = 'paused';
        $run['resume_reason'] = sanitize_key((string)$reason);
        $run['resume_at'] = time() + $pause_seconds;
        $run['owner'] = '';
        $run['lease_expires_at'] = 0;
        $run['work_block_started_at'] = 0;
        $run['work_block_tick_count'] = 0;
        return $this->ebay_run_save($run);
    }

    private function ebay_run_resume_paused_if_due($run) {
        $run = is_array($run) ? $run : $this->ebay_run_load();
        if (sanitize_key((string)($run['status'] ?? '')) !== 'paused') { return $run; }
        $resume_at = absint($run['resume_at'] ?? 0);
        if ($resume_at > time()) { return $run; }
        $before = $run;
        $run['status'] = 'running';
        $run['resume_reason'] = '';
        $run['resume_at'] = 0;
        $run['work_block_started_at'] = time();
        $run['work_block_tick_count'] = 0;
        $run['owner'] = '';
        $run['lease_expires_at'] = 0;
        $saved = $this->ebay_run_compare_and_swap($before, $run);
        return is_array($saved) ? $saved : $this->ebay_run_load();
    }

    /** State-only migration for an already-open V6.41.0/V6.41.1 run. No cursor,
     * source, listing, campaign, taxonomy or selection plan is reset/mutated. */
    public function maybe_migrate_ebay_worker_transport_v6412() {
        if ((string)get_option($this->ebay_run_worker_transport_migration_key(), '') === 'done') { return; }
        if (function_exists('wp_clear_scheduled_hook')) {
            wp_clear_scheduled_hook(self::EBAY_WORKER_HOOK);
            if (defined(static::class . '::EBAY_REFRESH_WORKER_HOOK')) {
                wp_clear_scheduled_hook(self::EBAY_REFRESH_WORKER_HOOK);
            }
        }
        $run = $this->ebay_run_load();
        if ((string)($run['schema'] ?? '') === '1.0') {
            $before = $run;
            $run['worker_transport'] = 'admin_ajax';
            if (sanitize_key((string)($run['resume_reason'] ?? '')) === 'awaiting_server_cron') {
                $run['resume_reason'] = 'awaiting_admin_ajax';
            }
            if ($this->ebay_run_compare_and_swap($before, $run) === false) {
                // Another request changed the run. Do not stamp the one-time
                // migration done until a later request re-evaluates that state.
                return;
            }
        }
        update_option($this->ebay_run_worker_transport_migration_key(), 'done', false);
    }

    /** Current durable progress-contract version. Kept separate from the plugin
     * build so state migration is based on the persisted contract, not on a
     * brittle one-off version prefix. */
    private function ebay_run_progress_contract_version() {
        $constant = static::class . '::EBAY_PROGRESS_CONTRACT_VERSION';
        return defined($constant) ? (string)constant($constant) : '2.0';
    }

    /** Return the last matching persistent failure entry without mutating state. */
    private function ebay_run_last_failure_entry($run, $code = '') {
        $errors = is_array($run['errors'] ?? null) ? $run['errors'] : array();
        $code = sanitize_key((string)$code);
        for ($i = count($errors) - 1; $i >= 0; $i--) {
            $entry = is_array($errors[$i] ?? null) ? $errors[$i] : array();
            if ($code !== '' && sanitize_key((string)($entry['code'] ?? '')) !== $code) { continue; }
            return $entry;
        }
        return array();
    }

    /**
     * V6.42.1 state-only migration for the proven old progress-contract defect.
     *
     * Root cause: V6.41.2/V6.41.3 could advance fair PRIVATE per-leaf prepare
     * cursors while the canonical no-progress fingerprint stayed unchanged.
     * V6.42 fixed the fingerprint itself, but its recovery was incorrectly tied
     * to one build prefix plus one global option. A real V6.41.2 failed run could
     * therefore remain terminal forever even though it had the exact proven
     * false-stall shape.
     *
     * This migration is per run + per failure event, fail-closed and state-only.
     * It never reopens a current-contract failure. It never mutates source rows,
     * listings, campaigns or taxonomies. If policy/catalog changed since the
     * failed run, only derived selection/coverage state is invalidated and the
     * same immutable run UUID re-enters reconcile_local.
     */
    public function maybe_migrate_ebay_progress_contract_v6421() {
        $run = $this->ebay_run_load();
        if ((string)($run['schema'] ?? '') !== '1.0') { return; }
        $loaded_run = $run;

        $current_contract = $this->ebay_run_progress_contract_version();
        $current_catalog = hash_file('sha256', __DIR__ . '/../assets/ebay-portal-catalog-v2.json') ?: '';
        $status = sanitize_key((string)($run['status'] ?? ''));
        $run_contract = sanitize_text_field((string)($run['progress_contract_version'] ?? ''));
        $build = sanitize_text_field((string)($run['build'] ?? ''));
        $affected_build = strpos($build, '6.41.2-') === 0 || strpos($build, '6.41.3-') === 0;
        $contract_changed = (string)($run['policy_version'] ?? '') !== (string)self::EBAY_CONTENT_POLICY_VERSION
            || ($current_catalog !== '' && (string)($run['catalog_version'] ?? '') !== $current_catalog);

        // Open affected old-contract run: upgrade the contract in-place. If the
        // policy/catalog also changed, a derived selection plan is unsafe to
        // resume; preserve remote/source cursors and re-enter reconciliation.
        if ($this->ebay_run_is_open($run) && ($run_contract !== $current_contract || $affected_build)) {
            $history = is_array($run['recovery_history'] ?? null) ? $run['recovery_history'] : array();
            $marker = hash('sha256', (string)($run['run_uuid'] ?? '').'|open|'.$current_contract.'|'.$build.'|'.($contract_changed?'1':'0'));
            foreach ($history as $entry) {
                if (is_array($entry) && hash_equals($marker, (string)($entry['migration_key'] ?? ''))) { return; }
            }
            $history[] = array('at'=>time(),'from_build'=>$build,'reason'=>'progress_contract_upgrade_open_run','migration_key'=>$marker,'contract_reconcile'=>$contract_changed?1:0);
            if (count($history) > 8) { $history = array_slice($history, -8); }
            $run['recovery_history'] = $history;
            $run['progress_contract_version'] = $current_contract;
            $run['owner'] = '';
            $run['lease_expires_at'] = 0;
            $run['worker_transport'] = 'admin_ajax';
            $run['no_progress_count'] = 0;
            if ($contract_changed) {
                $run['phase'] = 'reconcile_local';
                $run['resume_reason'] = 'progress_contract_policy_reconcile';
                if (!isset($run['phase_state']) || !is_array($run['phase_state'])) { $run['phase_state'] = array(); }
                $run['phase_state']['selection'] = array();
                $run['coverage'] = array();
                $run['gapfill'] = array('attempts'=>0,'missing'=>array());
                $run['end_manifest'] = array();
                $run['policy_version'] = (string)self::EBAY_CONTENT_POLICY_VERSION;
                if ($current_catalog !== '') { $run['catalog_version'] = $current_catalog; }
            } else {
                $run['resume_reason'] = 'progress_contract_upgraded_in_place';
            }
            if ($this->ebay_run_compare_and_swap($loaded_run, $run) !== false && $contract_changed) {
                update_option(self::OPTION_EBAY_SELECTION_STATE, array(), false);
            }
            return;
        }

        if ($status !== 'failed' || sanitize_key((string)($run['error_code'] ?? '')) !== 'canonical_worker_no_progress') { return; }

        $failure = $this->ebay_run_last_failure_entry($run, 'canonical_worker_no_progress');
        $details = is_array($failure['details'] ?? null) ? $failure['details'] : array();
        $failed_phase = sanitize_key((string)($details['phase'] ?? ''));
        $failure_build = sanitize_text_field((string)($details['build'] ?? $build));
        $failure_contract = sanitize_text_field((string)($details['progress_contract_version'] ?? $run_contract));
        $affected_failure_build = strpos($failure_build, '6.41.2-') === 0 || strpos($failure_build, '6.41.3-') === 0;

        // A failure explicitly produced under the current progress contract is a
        // real failure until separately diagnosed. Never auto-recover it.
        if ($failure_contract !== '' && hash_equals($current_contract, $failure_contract)) { return; }
        if (!$affected_failure_build) { return; }

        $selection = is_array($run['phase_state']['selection'] ?? null) ? $run['phase_state']['selection'] : array();
        $selection_status = sanitize_key((string)($selection['status'] ?? ''));
        $leaf_offsets = is_array($selection['prepare_private_leaf_offsets'] ?? null) ? $selection['prepare_private_leaf_offsets'] : array();
        $leaf_offset_progress = 0;
        foreach ($leaf_offsets as $offset) { $leaf_offset_progress += absint($offset); }
        $proven_private_prepare_progress = !empty($selection['prepare_private_initialized'])
            && empty($selection['prepare_private_complete'])
            && (absint($selection['prepare_private_scanned'] ?? 0) > 0
                || absint($selection['prepare_private_leaf_index'] ?? 0) > 0
                || $leaf_offset_progress > 0);
        $exact_false_failure = $failed_phase === 'selection_prepare'
            && in_array($selection_status, array('pending','preparing'), true)
            && $proven_private_prepare_progress;
        if (!$exact_false_failure) { return; }

        $failure_at = absint($failure['at'] ?? $run['finished_at'] ?? 0);
        $migration_key = hash('sha256', (string)($run['run_uuid'] ?? '').'|'.$failure_at.'|canonical_worker_no_progress|selection_prepare|'.$current_contract);
        $history = is_array($run['recovery_history'] ?? null) ? $run['recovery_history'] : array();
        foreach ($history as $entry) {
            if (is_array($entry) && hash_equals($migration_key, (string)($entry['migration_key'] ?? ''))) { return; }
        }

        $history[] = array(
            'at'=>time(),'from_build'=>$failure_build,'from_progress_contract'=>$failure_contract,
            'error_code'=>'canonical_worker_no_progress','reason'=>'legacy_private_prepare_progress_fingerprint_omission',
            'migration_key'=>$migration_key,'contract_reconcile'=>$contract_changed?1:0,
        );
        if (count($history) > 8) { $history = array_slice($history, -8); }
        $run['recovery_history'] = $history;
        $run['status'] = 'running';
        $run['phase'] = $contract_changed ? 'reconcile_local' : 'selection_prepare';
        $run['finished_at'] = 0;
        $run['owner'] = '';
        $run['lease_expires_at'] = 0;
        $run['worker_transport'] = 'admin_ajax';
        $run['resume_reason'] = $contract_changed ? 'legacy_false_stall_policy_reconcile' : 'legacy_false_stall_recovered';
        $run['no_progress_count'] = 0;
        $run['error_code'] = '';
        $run['error_message'] = '';
        $run['last_progress_at'] = time();
        $run['progress_contract_version'] = $current_contract;
        if ($contract_changed) {
            if (!isset($run['phase_state']) || !is_array($run['phase_state'])) { $run['phase_state'] = array(); }
            $run['phase_state']['selection'] = array();
            $run['coverage'] = array();
            $run['gapfill'] = array('attempts'=>0,'missing'=>array());
            $run['end_manifest'] = array();
            $run['policy_version'] = (string)self::EBAY_CONTENT_POLICY_VERSION;
            if ($current_catalog !== '') { $run['catalog_version'] = $current_catalog; }
        }
        if ($this->ebay_run_compare_and_swap($loaded_run, $run) !== false && $contract_changed) {
            update_option(self::OPTION_EBAY_SELECTION_STATE, array(), false);
        }
    }


    /**
     * V6.43.0 state-only migration for one proven canonical PARTIAL-checkpoint
     * false stall. It reopens a failed run only when the persisted nested
     * discovery state itself proves that the same run stopped on a resumable
     * segment_time_budget checkpoint in the exact matching scope. Unknown or
     * current failures remain terminal.
     */
    public function maybe_migrate_ebay_partial_checkpoint_v6430() {
        $run=$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0') { return; }
        $loaded_run=$run;
        if(sanitize_key((string)($run['status']??''))!=='failed' || sanitize_key((string)($run['error_code']??''))!=='canonical_worker_no_progress') { return; }
        $failure=$this->ebay_run_last_failure_entry($run,'canonical_worker_no_progress');
        $details=is_array($failure['details']??null)?$failure['details']:array();
        $failed_phase=sanitize_key((string)($details['phase']??''));
        if(!in_array($failed_phase,array('refresh_remote','gapfill_discovery'),true)) { return; }
        $job=is_array($run['phase_state']['discovery']??null)?$run['phase_state']['discovery']:array();
        if(!$this->ebay_sync_job_is_resumable_partial($job)) { return; }
        $scope=sanitize_key((string)($job['scope']??''));
        $expected_scope=$failed_phase==='gapfill_discovery'?'business_recovery':'all';
        if($scope!==$expected_scope) { return; }
        $run_uuid=sanitize_text_field((string)($run['run_uuid']??''));
        $job_uuid=sanitize_text_field((string)($job['run_uuid']??''));
        if($run_uuid==='' || $job_uuid==='' || !hash_equals($run_uuid,$job_uuid)) { return; }
        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();
        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$run_uuid.'|'.$failure_at.'|partial_checkpoint|'.$failed_phase.'|'.$scope);
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $history[]=array('at'=>time(),'reason'=>'canonical_partial_checkpoint_resume','phase'=>$failed_phase,'scope'=>$scope,'migration_key'=>$marker);
        if(count($history)>8){$history=array_slice($history,-8);}
        $run['recovery_history']=$history;$run['status']='running';$run['phase']=$failed_phase;$run['finished_at']=0;$run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='admin_ajax';$run['resume_reason']='partial_checkpoint_resume';$run['no_progress_count']=0;$run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();
        $this->ebay_run_compare_and_swap($loaded_run,$run);
    }

    /**
     * V6.44.0 state-only recovery for the proven BUSINESS materialisation
     * dead-end. The old selector treated one candidate-local soft output-plan
     * failure as a terminal failure of the whole 311-family run, so the
     * canonical coverage/gap-fill phases could never do the job they own.
     *
     * Recovery is deliberately fail-closed: the same run UUID is reopened only
     * when every persisted materialisation error is independently proven soft.
     * Storage/source/commit/unknown errors remain terminal.
     */
    private function ebay_run_business_materialization_error_is_proven_soft_v6440($entry) {
        $entry=is_array($entry)?$entry:array();
        $code=sanitize_key((string)($entry['code']??''));
        if($code==='ebay_business_materialization_not_active'){return true;}
        if($code!=='business_selection_commit_failed'){return false;}
        // One historical edge case: route_business already preserved a verified
        // Last-Known-Good output, then the generic active-selected commit rejected
        // that intentional review_last_good state. Prove that exact row state
        // before treating the old commit failure as candidate-local.
        $item_id=sanitize_text_field((string)($entry['item_id']??''));
        if($item_id==='' || !method_exists($this,'ebay_items_table')){return false;}
        global $wpdb;
        if(!is_object($wpdb)||!method_exists($wpdb,'get_row')||!method_exists($wpdb,'prepare')){return false;}
        $row=$wpdb->get_row($wpdb->prepare(
            "SELECT * FROM {$this->ebay_items_table()} WHERE item_id=%s AND seller_account_type='BUSINESS' ORDER BY id DESC LIMIT 1",
            $item_id
        ),ARRAY_A);
        if(!is_array($row)){return false;}
        $route=sanitize_key((string)($row['route_state']??''));
        $reason=sanitize_text_field((string)($row['rejection_reason']??''));
        return $route==='review_last_good' && strpos($reason,'[ebay_business_materialization_not_active]')!==false;
    }

    public function maybe_migrate_ebay_business_materialization_v6440() {
        $run=$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0') { return; }
        $loaded_run=$run;
        if(sanitize_key((string)($run['status']??''))!=='failed'
            || sanitize_key((string)($run['error_code']??''))!=='business_recovery_incomplete'){return;}
        $failure=$this->ebay_run_last_failure_entry($run,'business_recovery_incomplete');
        $details=is_array($failure['details']??null)?$failure['details']:array();
        $failed_phase=sanitize_key((string)($details['phase']??''));
        if($failed_phase!=='' && $failed_phase!=='business_materialize'){return;}
        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        if(sanitize_key((string)($selection['failure_reason']??''))!=='business_recovery_incomplete'){return;}
        $errors=is_array($selection['stats']['business']['errors']??null)?$selection['stats']['business']['errors']:array();
        if(!$errors){return;}
        foreach($errors as $entry){if(!$this->ebay_run_business_materialization_error_is_proven_soft_v6440($entry)){return;}}

        $uuid=sanitize_text_field((string)($run['run_uuid']??''));
        if($uuid===''){return;}
        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$uuid.'|'.$failure_at.'|business_materialization_soft_candidates|6.44.0');
        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $history[]=array('at'=>time(),'reason'=>'business_materialization_soft_candidate_recovery','error_code'=>'business_recovery_incomplete','migration_key'=>$marker,'soft_errors'=>count($errors));
        if(count($history)>8){$history=array_slice($history,-8);}

        // Preserve source/refresh state and immutable run identity. Only the
        // derived selection/coverage tail is rebuilt under the corrected rule.
        $run['recovery_history']=$history;$run['status']='running';$run['phase']='selection_prepare';$run['finished_at']=0;
        $run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='admin_ajax';
        $run['resume_reason']='business_materialization_soft_candidate_recovery';$run['no_progress_count']=0;
        $run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();
        if(!isset($run['phase_state'])||!is_array($run['phase_state'])){$run['phase_state']=array();}
        $run['phase_state']['selection']=array();$run['coverage']=array();$run['gapfill']=array('attempts'=>0,'missing'=>array());$run['end_manifest']=array();
        // The legacy selection option is only cleared after the canonical CAS
        // won. A losing concurrent migration must not mutate any durable state.
        if($this->ebay_run_compare_and_swap($loaded_run,$run)!==false){
            update_option(self::OPTION_EBAY_SELECTION_STATE,array(),false);
        }
    }


    /**
     * V6.46 state-only recovery for the V6.45 public-freshness contract gap.
     *
     * The recovery is intentionally narrow. It reopens only a V6.45
     * insufficient_safe_sources failure whose persisted coverage proves that
     * every examined published BUSINESS object was rejected solely because its
     * source freshness expired while the same run had successfully materialised
     * BUSINESS winners. That state is impossible under the corrected selector:
     * stale rows are no longer eligible for prepare/apply.
     *
     * The same UUID is preserved. Only derived selection/coverage state and the
     * already-completed refresh sub-job are invalidated so the canonical workflow
     * re-enters its existing bounded local-reconcile -> remote-refresh path.
     */
    public function maybe_migrate_ebay_public_freshness_v6460() {
        $run=$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0'){return;}
        $loaded_run=$run;
        if(sanitize_key((string)($run['status']??''))!=='failed'
            || sanitize_key((string)($run['error_code']??''))!=='insufficient_safe_sources'){return;}
        $failure=$this->ebay_run_last_failure_entry($run,'insufficient_safe_sources');
        $details=is_array($failure['details']??null)?$failure['details']:array();
        $failed_phase=sanitize_key((string)($details['phase']??''));
        $failure_build=sanitize_text_field((string)($details['build']??$run['build']??''));
        if($failed_phase!=='' && $failed_phase!=='coverage_verify'){return;}
        if(strpos($failure_build,'6.45.0-')!==0){return;}

        $coverage=is_array($run['coverage']??null)?$run['coverage']:array();
        $required=absint($coverage['required']??0);
        $covered=absint($coverage['covered']??0);
        $missing=array_values(array_filter(array_map('sanitize_key',(array)($coverage['missing']??array()))));
        $invalid=is_array($coverage['invalid']??null)?$coverage['invalid']:array();
        if($required!==311 || $covered!==0 || count($missing)!==311 || !$invalid){return;}
        foreach($invalid as $reason){
            if(sanitize_key((string)$reason)!=='source_stale'){return;}
        }
        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        if(absint($selection['stats']['business']['materialized']??0)<1){return;}

        $uuid=sanitize_text_field((string)($run['run_uuid']??''));
        if($uuid===''){return;}
        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$uuid.'|'.$failure_at.'|public_freshness_contract|6.46.0');
        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $history[]=array(
            'at'=>time(),'reason'=>'public_freshness_contract_recovery',
            'error_code'=>'insufficient_safe_sources','migration_key'=>$marker,
            'stale_public_objects'=>count($invalid),
        );
        if(count($history)>8){$history=array_slice($history,-8);}

        $run['recovery_history']=$history;
        $run['status']='running';$run['phase']='reconcile_local';$run['finished_at']=0;
        $run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='admin_ajax';
        $run['resume_reason']='public_freshness_contract_recovery';$run['no_progress_count']=0;
        $run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();
        if(!isset($run['phase_state'])||!is_array($run['phase_state'])){$run['phase_state']=array();}
        $run['phase_state']['selection']=array();
        $run['phase_state']['refresh']=array();
        $run['coverage']=array();
        $run['gapfill']=array('attempts'=>0,'missing'=>array());
        $run['end_manifest']=array();

        // All nested-option mutation happens only after the canonical CAS won.
        // A concurrent request can therefore never lose its newer run state.
        if($this->ebay_run_compare_and_swap($loaded_run,$run)!==false){
            update_option(self::OPTION_EBAY_SELECTION_STATE,array(),false);
            update_option(self::OPTION_EBAY_REFRESH_JOB,array(),false);
        }
    }

    /**
     * V6.48 canonical-state recovery for the proven V6.46 dynamic BUSINESS rule-context loss.
     *
     * Root cause of the V6.47 live miss: schema-1.0 component state is owned by the
     * canonical run's phase_state. ebay_refresh_job_save() therefore writes the
     * completed refresh into phase_state.refresh and intentionally does NOT mirror
     * it into the legacy OPTION_EBAY_REFRESH_JOB. V6.47 nevertheless required both
     * stores to contain the same completed refresh, so a valid canonical production
     * state could never pass that extra legacy gate. The V6.47 real gate hid this by
     * manually seeding the non-authoritative legacy option.
     *
     * This recovery now uses exactly one authority for schema-1.0: the canonical
     * phase_state.refresh with the same run UUID. Legacy standalone component options
     * are neither proof nor veto. All other provenance/coverage/selection/gap-fill
     * guards remain unchanged and fail-closed. The method name is retained for
     * compatibility with the existing init hook and historical test harnesses.
     */
    public function maybe_migrate_ebay_dynamic_business_rule_context_v6470() {
        $run=$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0'){return;}
        $loaded_run=$run;
        if(sanitize_key((string)($run['status']??''))!=='failed'
            || sanitize_key((string)($run['error_code']??''))!=='insufficient_safe_sources'){return;}
        $failure=$this->ebay_run_last_failure_entry($run,'insufficient_safe_sources');
        $details=is_array($failure['details']??null)?$failure['details']:array();
        if(sanitize_key((string)($details['phase']??''))!=='coverage_verify'){return;}
        $failure_build=sanitize_text_field((string)($details['build']??$run['build']??''));
        if(strpos($failure_build,'6.46.0-')!==0){return;}

        $routes=is_array($run['config_snapshot']['seller_routes']??null)?$run['config_snapshot']['seller_routes']:array();
        if(empty($routes['business'])){return;}
        $required_now=array_values(array_unique(array_filter(array_map('sanitize_key',(array)$this->ebay_business_required_product_concept_ids()))));
        sort($required_now,SORT_STRING);
        if(count($required_now)!==311){return;}
        $coverage=is_array($run['coverage']??null)?$run['coverage']:array();
        $missing=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($coverage['missing']??array())))));
        $missing_sorted=$missing;sort($missing_sorted,SORT_STRING);
        if(absint($coverage['required']??0)!==311 || absint($coverage['covered']??0)!==0
            || count($missing_sorted)!==311 || $missing_sorted!==$required_now){return;}

        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        if(absint($selection['stats']['business']['materialized']??0)!==0
            || absint($selection['stats']['business']['active']??0)!==0){return;}
        if(absint($run['gapfill']['attempts']??0)<1){return;}

        $uuid=sanitize_text_field((string)($run['run_uuid']??''));
        if($uuid===''){return;}
        // Schema-1.0 has one authoritative component-state store: canonical
        // phase_state. The legacy standalone refresh option is deliberately ignored
        // here because production saves no longer mirror canonical refresh state to it.
        $refresh=is_array($run['phase_state']['refresh']??null)?$run['phase_state']['refresh']:array();
        if(sanitize_key((string)($refresh['status']??''))!=='completed'
            || !hash_equals($uuid,sanitize_text_field((string)($refresh['run_uuid']??'')))){return;}

        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$uuid.'|'.$failure_at.'|dynamic_business_rule_context|canonical-state-v648');
        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $history[]=array(
            'at'=>time(),'reason'=>'dynamic_business_rule_context_recovery',
            'error_code'=>'insufficient_safe_sources','migration_key'=>$marker,
            'missing_business_concepts'=>count($missing),'preserved_refresh'=>1,
        );
        if(count($history)>8){$history=array_slice($history,-8);}

        $run['recovery_history']=$history;
        $run['status']='running';$run['phase']='gapfill_discovery';$run['finished_at']=0;
        $run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='admin_ajax';
        $run['resume_reason']='dynamic_business_rule_context_recovery';$run['no_progress_count']=0;
        $run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();
        if(!isset($run['phase_state'])||!is_array($run['phase_state'])){$run['phase_state']=array();}
        // Preserve phase_state.refresh byte-for-byte; it proves the completed
        // V6.46 remote pass and prevents an unnecessary second full refresh.
        $run['phase_state']['discovery']=array();
        $run['phase_state']['selection']=array();
        $run['gapfill']=array('attempts'=>1,'missing'=>$missing);
        $run['end_manifest']=array();

        // Legacy discovery/selection residue is cleared only after the canonical CAS.
        // The legacy refresh option is intentionally neither read nor changed: under
        // schema-1.0 it is non-authoritative historical residue.
        if($this->ebay_run_compare_and_swap($loaded_run,$run)!==false){
            update_option(self::OPTION_EBAY_SYNC_JOB,array(),false);
            update_option(self::OPTION_EBAY_SELECTION_STATE,array(),false);
        }
    }

    /**
     * V6.49 state-only recovery for the V6.48 public-coverage target bridge bug.
     *
     * V6.48 correctly linked a published output object back to its eBay source
     * row, but then passed that source-table row into
     * ebay_business_campaign_target_keys(). That helper consumes a Creative
     * Library row and therefore returned an empty expected target set for every
     * otherwise-valid BUSINESS campaign. The public gate consequently recorded
     * target_mismatch and could force a false 0/311 insufficient_safe_sources
     * terminal state after a successful materialization path.
     *
     * Recovery is deliberately narrow and state-only. It reopens only the exact
     * V6.48 terminal signature with the current 311 manifest and at least one
     * persisted target_mismatch proof. Existing refresh/discovery/selection and
     * public output are preserved byte-for-byte. Only derived coverage/gap-fill
     * accounting is invalidated so the corrected public gate runs first; if real
     * families are still missing it may use the normal one bounded targeted
     * gap-fill for that corrected subset under the same UUID.
     */
    public function maybe_migrate_ebay_public_coverage_target_v6490() {
        $run=$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0'){return;}
        $loaded_run=$run;
        if(sanitize_key((string)($run['status']??''))!=='failed'
            || sanitize_key((string)($run['error_code']??''))!=='insufficient_safe_sources'){return;}
        $failure=$this->ebay_run_last_failure_entry($run,'insufficient_safe_sources');
        $details=is_array($failure['details']??null)?$failure['details']:array();
        if(sanitize_key((string)($details['phase']??''))!=='coverage_verify'){return;}
        $failure_build=sanitize_text_field((string)($details['build']??$run['build']??''));
        if(strpos($failure_build,'6.48.0-')!==0){return;}

        $routes=is_array($run['config_snapshot']['seller_routes']??null)?$run['config_snapshot']['seller_routes']:array();
        if(empty($routes['business'])){return;}
        $required_now=array_values(array_unique(array_filter(array_map('sanitize_key',(array)$this->ebay_business_required_product_concept_ids()))));
        sort($required_now,SORT_STRING);
        if(count($required_now)!==311){return;}
        $coverage=is_array($run['coverage']??null)?$run['coverage']:array();
        $missing=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($coverage['missing']??array())))));
        $missing_sorted=$missing;sort($missing_sorted,SORT_STRING);
        if(absint($coverage['required']??0)!==311 || absint($coverage['covered']??0)!==0
            || count($missing_sorted)!==311 || $missing_sorted!==$required_now){return;}
        if(absint($run['gapfill']['attempts']??0)<1){return;}
        $invalid=is_array($coverage['invalid']??null)?$coverage['invalid']:array();
        if(!$invalid){return;}
        $target_mismatch=0;
        foreach($invalid as $reason){if(sanitize_key((string)$reason)==='target_mismatch'){$target_mismatch++;}}
        if($target_mismatch<1){return;}

        $uuid=sanitize_text_field((string)($run['run_uuid']??''));
        if($uuid===''){return;}
        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$uuid.'|'.$failure_at.'|public_coverage_target_bridge|6.49.0');
        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $history[]=array(
            'at'=>time(),'reason'=>'public_coverage_target_contract_recovery',
            'error_code'=>'insufficient_safe_sources','migration_key'=>$marker,
            'target_mismatch_objects'=>$target_mismatch,'preserved_components'=>1,
        );
        if(count($history)>8){$history=array_slice($history,-8);}

        $run['recovery_history']=$history;
        $run['status']='running';$run['phase']='coverage_verify';$run['finished_at']=0;
        $run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='admin_ajax';
        $run['resume_reason']='public_coverage_target_contract_recovery';$run['no_progress_count']=0;
        $run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();
        // Refresh/discovery/selection are already completed evidence and remain
        // untouched. Only data derived from the broken public gate is discarded.
        $run['coverage']=array();
        $run['gapfill']=array('attempts'=>0,'missing'=>array());
        $run['end_manifest']=array();
        $this->ebay_run_compare_and_swap($loaded_run,$run);
    }

    /**
     * V6.50.1 state-only recovery for the stale-proof upgrade path.
     *
     * V6.50 incorrectly reused a terminal V6.49 gap-fill proof and jumped
     * directly to public_verify. Public coverage can change between the old
     * failure and the upgrade, so the old missing/selection proof is derived
     * stale state. Reopen only the exact affected upgrade signatures, preserve
     * the same run UUID and upstream refresh/source evidence, discard only the
     * stale derived discovery/selection/coverage/gap-fill state, and re-enter
     * the existing coverage_verify -> one canonical targeted gap-fill path.
     */
    public function maybe_migrate_ebay_safe_supply_gap_v6500() {
        $run=$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0'){return;}
        $loaded_run=$run;
        if(sanitize_key((string)($run['status']??''))!=='failed'){return;}

        $error_code=sanitize_key((string)($run['error_code']??''));
        $failure=$this->ebay_run_last_failure_entry($run,$error_code);
        $details=is_array($failure['details']??null)?$failure['details']:array();
        $failure_phase=sanitize_key((string)($details['phase']??''));
        $failure_build=sanitize_text_field((string)($details['build']??$run['build']??''));

        $from_v649=$error_code==='insufficient_safe_sources'
            && $failure_phase==='coverage_verify'
            && strpos($failure_build,'6.49.0-')===0;

        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();
        $has_v650_stale_recovery=false;
        foreach($history as $entry){
            if(is_array($entry)
                && sanitize_key((string)($entry['reason']??''))==='safe_supply_gap_contract_recovery'
                && sanitize_key((string)($entry['error_code']??''))==='insufficient_safe_sources'){
                $has_v650_stale_recovery=true;break;
            }
        }
        $from_v650_stale_failure=$error_code==='business_safe_gap_new_missing_family'
            && $failure_phase==='public_verify'
            && strpos($failure_build,'6.50.0-')===0
            && sanitize_key((string)($run['resume_reason']??''))==='safe_supply_gap_contract_recovery'
            && $has_v650_stale_recovery;

        if(!$from_v649 && !$from_v650_stale_failure){return;}

        $routes=is_array($run['config_snapshot']['seller_routes']??null)?$run['config_snapshot']['seller_routes']:array();
        if(empty($routes['business'])){return;}
        $coverage=is_array($run['coverage']??null)?$run['coverage']:array();
        if(!empty($coverage['error_code']) || empty($coverage['missing']) || absint($run['gapfill']['attempts']??0)<1){return;}

        // The old terminal proof is used only to prove that this is the exact
        // safe-supply-gap upgrade path. It is never reused as current truth.
        $result=$this->ebay_run_business_safe_supply_gap_contract($run,$coverage);
        if(($result['status']??'')!=='pass'){return;}

        $uuid=sanitize_text_field((string)($run['run_uuid']??''));
        if($uuid===''){return;}
        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$uuid.'|'.$failure_at.'|safe_supply_gap_stale_proof_recovery|6.50.1');
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $history[]=array(
            'at'=>time(),'reason'=>'safe_supply_gap_stale_proof_recovery',
            'error_code'=>$error_code,'migration_key'=>$marker,
            'preserved_components'=>1,'discarded_derived_gap_proof'=>1,
        );
        if(count($history)>8){$history=array_slice($history,-8);}

        $run['recovery_history']=$history;
        $run['status']='running';$run['phase']='coverage_verify';$run['finished_at']=0;
        $run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='admin_ajax';
        $run['resume_reason']='safe_supply_gap_stale_proof_recovery';$run['no_progress_count']=0;
        $run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();
        if(!isset($run['phase_state'])||!is_array($run['phase_state'])){$run['phase_state']=array();}
        // Preserve upstream refresh/source evidence. Discovery and selection are
        // derived from the old missing set and must be recomputed for current gaps.
        $run['phase_state']['discovery']=array();
        $run['phase_state']['selection']=array();
        $run['coverage']=array();
        $run['gapfill']=array('attempts'=>0,'missing'=>array());
        $run['end_manifest']=array();
        $this->ebay_run_compare_and_swap($loaded_run,$run);
    }

    /** Backward-compatible entry point retained for older test harnesses. */
    public function maybe_recover_ebay_false_no_progress_v6420() {
        return $this->maybe_migrate_ebay_progress_contract_v6421();
    }

    /** Backward-compatible admin endpoint. It never executes fach logic; it can
     * only ensure that the background worker is scheduled. */
    public function run_ebay_admin_ajax_tick() {
        $run = $this->ebay_run_load();
        return array(
            'status'=>$this->ebay_run_is_active($run)?sanitize_key((string)($run['status']??'running')):'idle',
            'transport'=>'external_tick','run_uuid'=>(string)($run['run_uuid']??''),
            'tick_count'=>absint($run['transport_tick_count']??0),
        );
    }

    /** Snapshot only operational values. Provider credentials are intentionally
     * not duplicated into the durable run option; current credentials are merged
     * at worker time while all behavioural/routing settings stay frozen. */
    private function ebay_run_settings_snapshot($settings) {
        $settings = is_array($settings) ? $this->ebay_normalize_settings($settings, true) : array();
        $drop = array('client_id','client_secret','last_test','last_sync','last_refresh','rules');
        foreach ($drop as $key) { unset($settings[$key]); }
        return $settings;
    }

    private function ebay_run_effective_settings($run) {
        $override = $this->ebay_run_settings_override;
        $this->ebay_run_settings_override = null;
        $live = $this->ebay_settings();
        $this->ebay_run_settings_override = $override;
        $snapshot = is_array($run['config_snapshot']['settings'] ?? null) ? $run['config_snapshot']['settings'] : array();
        foreach ($snapshot as $key => $value) {
            if (in_array($key, array('client_id','client_secret','last_test','last_sync','last_refresh','rules'), true)) { continue; }
            $live[$key] = $value;
        }
        // Rules are immutable plugin catalog data for this build. Credentials are
        // live operational secrets and may be rotated without mutating run scope.
        $live['rules'] = $this->ebay_catalog_rules();
        return $this->ebay_normalize_settings($live, true);
    }

    private function ebay_run_selection_scope($run) {
        $routes = is_array($run['config_snapshot']['seller_routes'] ?? null) ? $run['config_snapshot']['seller_routes'] : array();
        $private = !empty($routes['private']);
        $business = !empty($routes['business']);
        return $private && $business ? 'all' : ($private ? 'private' : ($business ? 'business' : ''));
    }

    private function ebay_run_new_uuid() {
        return function_exists('wp_generate_uuid4') ? wp_generate_uuid4() : substr(hash('sha256', microtime(true) . '|canonical|' . mt_rand()), 0, 36);
    }

    private function ebay_run_legacy_raw_states() {
        return array(
            'discovery'=>is_array(get_option(self::OPTION_EBAY_SYNC_JOB, array())) ? get_option(self::OPTION_EBAY_SYNC_JOB, array()) : array(),
            'refresh'=>is_array(get_option(self::OPTION_EBAY_REFRESH_JOB, array())) ? get_option(self::OPTION_EBAY_REFRESH_JOB, array()) : array(),
            'selection'=>is_array(get_option(self::OPTION_EBAY_SELECTION_STATE, array())) ? get_option(self::OPTION_EBAY_SELECTION_STATE, array()) : array(),
            'maintenance'=>is_array(get_option(self::OPTION_EBAY_MAINTENANCE_STATE, array())) ? get_option(self::OPTION_EBAY_MAINTENANCE_STATE, array()) : array(),
        );
    }

    /** State-only adoption of one compatible V6.40 open chain. No source/post/
     * campaign mutation occurs here. Ambiguous competing owners fail closed. */
    private function ebay_run_adopt_legacy_if_needed() {
        $current = $this->ebay_run_load();
        if ((string)($current['schema'] ?? '') === '1.0') { return $current; }
        $legacy = $this->ebay_run_legacy_raw_states();
        $sync = $legacy['discovery']; $refresh = $legacy['refresh']; $selection = $legacy['selection'];
        $sync_open = in_array(sanitize_key((string)($sync['status'] ?? '')), array('queued','running','partial'), true);
        $refresh_open = in_array(sanitize_key((string)($refresh['status'] ?? '')), array('queued','running','partial'), true);
        $selection_open = in_array(sanitize_key((string)($selection['status'] ?? '')), array('pending','preparing','running'), true);
        if (!$sync_open && !$refresh_open && !$selection_open) { return array(); }

        $uuid = '';
        $operation = 'refresh';
        $phase = 'reconcile_local';
        $remote_subphase = 'inventory';
        $compatible = true;
        if ($sync_open) {
            $uuid = sanitize_text_field((string)($sync['run_uuid'] ?? ''));
            $operation = 'sync'; $phase = 'refresh_remote'; $remote_subphase = 'discovery';
        }
        if ($refresh_open) {
            $r_uuid = sanitize_text_field((string)($refresh['run_uuid'] ?? ''));
            if ($uuid !== '' && $r_uuid !== '' && !hash_equals($uuid, $r_uuid)) { $compatible = false; }
            if ($uuid === '') { $uuid = $r_uuid; }
            $operation = 'refresh';
            $rphase = sanitize_key((string)($refresh['summary']['phase'] ?? ''));
            $phase = in_array($rphase, array('local_reconciliation','asset_verification'), true) ? 'reconcile_local' : 'refresh_remote';
            $remote_subphase = 'inventory';
        }
        if ($selection_open) {
            $owner = sanitize_text_field((string)($selection['owner'] ?? ''));
            if (strpos($owner, 'sync:') === 0) { $s_uuid = substr($owner, 5); }
            elseif (strpos($owner, 'refresh:') === 0) { $s_uuid = substr($owner, 8); }
            elseif (strpos($owner, 'run:') === 0) { $s_uuid = substr($owner, 4); }
            else { $s_uuid = ''; }
            if ($uuid !== '' && $s_uuid !== '' && !hash_equals($uuid, $s_uuid)) { $compatible = false; }
            if ($uuid === '' && $s_uuid !== '') { $uuid = $s_uuid; }
            if (!$sync_open && !$refresh_open) { $operation = 'selection'; }
            $phase = 'selection_prepare';
        }
        if (!$compatible || $uuid === '') {
            $blocked = array(
                'schema'=>'1.0','build'=>self::EBAY_RUNTIME_BUILD,'run_uuid'=>$uuid !== '' ? $uuid : $this->ebay_run_new_uuid(),
                'status'=>'failed','phase'=>'failed','started_at'=>time(),'updated_at'=>time(),'finished_at'=>time(),
                'error_code'=>'blocked_migration_required','error_message'=>'Mehrere alte eBay-Workerzustände besitzen keine eindeutig gemeinsame Run-Identität.',
                'phase_state'=>$legacy,
            );
            return $this->ebay_run_save($blocked);
        }
        $settings = $this->ebay_settings();
        $run = array(
            'schema'=>'1.0','build'=>self::EBAY_RUNTIME_BUILD,'run_uuid'=>$uuid,'status'=>'running','phase'=>$phase,
            'operation'=>$operation,'remote_subphase'=>$remote_subphase,'started_at'=>min(array_filter(array_map('absint', array($sync['created_at']??0,$refresh['created_at']??0,$selection['started_at']??0))) ?: array(time())),
            'updated_at'=>time(),'finished_at'=>0,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'admin_ajax','resume_reason'=>'adopted_legacy_state',
            'no_progress_count'=>0,'last_progress_at'=>time(),'progress_seq'=>0,
            'config_snapshot'=>array('seller_routes'=>array('private'=>!empty($settings['private_enabled']),'business'=>!empty($settings['business_enabled'])),'settings'=>$this->ebay_run_settings_snapshot($settings)),
            'catalog_version'=>hash_file('sha256', __DIR__ . '/../assets/ebay-portal-catalog-v2.json') ?: '',
            'policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,'private_classifier_version'=>self::EBAY_PRIVATE_CLASSIFIER_VERSION,'business_classifier_version'=>self::EBAY_BUSINESS_CLASSIFIER_VERSION,'progress_contract_version'=>$this->ebay_run_progress_contract_version(),
            'phase_state'=>$legacy,'coverage'=>array(),'errors'=>array(),'start_manifest'=>array('adopted_legacy'=>1),'end_manifest'=>array(),
        );
        return $this->ebay_run_save($run);
    }

    private function ebay_run_start($manual = false, $operation = 'sync') {
        $operation = sanitize_key((string)$operation);
        if (!in_array($operation, array('sync','refresh'), true)) { return new WP_Error('ebay_run_operation_invalid', 'Ungültiger eBay-Gesamtlauf.'); }
        $run = $this->ebay_run_load();
        if ($this->ebay_run_is_active($run)) {
            $this->ebay_run_schedule_worker(1);
            return array('status'=>'already_running','run_uuid'=>(string)$run['run_uuid'],'phase'=>(string)$run['phase'],'transport'=>'self_drive');
        }
        $settings = $this->ebay_settings();
        if (empty($settings['enabled']) && !$manual) { return array('status'=>'disabled'); }
        $errors = $this->ebay_configuration_errors($settings);
        if ($errors) { return new WP_Error('ebay_configuration_invalid', implode(' ', $errors)); }
        $scope = $this->ebay_selection_scope_for_enabled_routes('all', $settings);
        if ($scope === '') { return new WP_Error('ebay_routes_disabled', 'PRIVATE und BUSINESS sind beide deaktiviert.'); }

        if ((string)($run['schema'] ?? '') === '1.0') { $this->ebay_run_archive_terminal($run); }
        $checkpoint = $this->ebay_public_checkpoint_bootstrap($settings);
        if (is_wp_error($checkpoint)) { return $checkpoint; }
        $checkpoint = is_array($checkpoint) ? $checkpoint : array();

        $uuid = $this->ebay_run_new_uuid();
        $run = array(
            'schema'=>'1.0','build'=>self::EBAY_RUNTIME_BUILD,'run_uuid'=>$uuid,'status'=>'running','phase'=>'reconcile_local','operation'=>$operation,
            'remote_subphase'=>$operation === 'sync' ? 'discovery' : 'inventory','started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,
            'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'self_drive','orchestrator_contract'=>'self_drive_v1','resume_reason'=>'','resume_at'=>0,'no_progress_count'=>0,'last_progress_at'=>time(),'progress_seq'=>0,'last_transport_tick_at'=>0,'transport_tick_count'=>0,
            'work_block_started_at'=>time(),'work_block_tick_count'=>0,
            'config_snapshot'=>array('seller_routes'=>array('private'=>!empty($settings['private_enabled']),'business'=>!empty($settings['business_enabled'])),'settings'=>$this->ebay_run_settings_snapshot($settings)),
            'catalog_version'=>hash_file('sha256', __DIR__ . '/../assets/ebay-portal-catalog-v2.json') ?: '',
            'policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,'private_classifier_version'=>self::EBAY_PRIVATE_CLASSIFIER_VERSION,'business_classifier_version'=>self::EBAY_BUSINESS_CLASSIFIER_VERSION,'progress_contract_version'=>$this->ebay_run_progress_contract_version(),
            'phase_state'=>array(),'coverage'=>array(),'gapfill'=>array('attempts'=>0,'missing'=>array()),'errors'=>array(),'skipped_item_errors_count'=>0,'skipped_item_errors'=>array(),'completed_with_skips'=>0,
            'checkpoint_base_id'=>sanitize_text_field((string)($checkpoint['checkpoint_id'] ?? '')),
            'checkpoint_candidate'=>array(
                'business_campaign_ids'=>$this->ebay_public_checkpoint_business_ids($checkpoint),
                'private_listing_ids'=>$this->ebay_public_checkpoint_private_ids($checkpoint),
            ),
            'checkpoint_cleanup_selection'=>array(),
            'checkpoint_verified_manifest'=>array(),
            'start_manifest'=>array('operation'=>$operation,'selection_scope'=>$scope,'seller_routes'=>array('private'=>!empty($settings['private_enabled']),'business'=>!empty($settings['business_enabled'])),'checkpoint_id'=>sanitize_text_field((string)($checkpoint['checkpoint_id'] ?? ''))),
            'end_manifest'=>array(),
        );
        $this->ebay_run_save($run);
        $self_drive=$this->ebay_run_dispatch_self_drive($uuid,'run_start');
        return array('status'=>'queued','run_uuid'=>$uuid,'phase'=>'reconcile_local','transport'=>'self_drive','self_drive_dispatched'=>$self_drive?1:0);
    }

    private function ebay_run_fail($code, $message, $details = array()) {
        $run = $this->ebay_run_load();
        if ((string)($run['schema'] ?? '') !== '1.0') { $run = array('schema'=>'1.0','run_uuid'=>$this->ebay_run_new_uuid(),'started_at'=>time()); }
        $failed_phase=sanitize_key((string)($run['phase']??''));
        $details=is_array($details)?$details:array();
        if(empty($details['phase'])){$details['phase']=$failed_phase;}
        if(empty($details['build'])){$details['build']=self::EBAY_RUNTIME_BUILD;}
        if(empty($details['progress_contract_version'])){$details['progress_contract_version']=$this->ebay_run_progress_contract_version();}
        $run['status']='failed';$run['phase']='failed';$run['finished_at']=time();
        $run['error_code']=sanitize_key((string)$code);$run['error_message']=sanitize_text_field((string)$message);
        $run['progress_contract_version']=$this->ebay_run_progress_contract_version();
        if (!isset($run['errors']) || !is_array($run['errors'])) { $run['errors']=array(); }
        $run['errors'][]=array('code'=>$run['error_code'],'message'=>$run['error_message'],'at'=>time(),'details'=>$details);
        $checkpoint=$this->ebay_public_checkpoint_load();
        $run['checkpoint_safe']= $this->ebay_public_checkpoint_is_safe($checkpoint) ? 1 : 0;
        $run['checkpoint_id']=sanitize_text_field((string)($checkpoint['checkpoint_id']??$run['checkpoint_base_id']??''));
        $run['restart_available']=1;
        $run['owner']='';$run['lease_expires_at']=0;$run['resume_at']=0;
        return $this->ebay_run_save($run);
    }

    private function ebay_run_complete($manifest = array()) {
        $run=$this->ebay_run_load();
        $run['status']='completed';$run['phase']='completed';$run['finished_at']=time();$run['resume_reason']='';$run['resume_at']=0;
        $run['completed_with_skips']=absint($run['skipped_item_errors_count']??0)>0?1:0;
        $checkpoint=$this->ebay_public_checkpoint_load();
        if($this->ebay_public_checkpoint_is_safe($checkpoint)){
            $run['checkpoint_id']=sanitize_text_field((string)($checkpoint['checkpoint_id']??''));
            if(!is_array($manifest)){$manifest=array();}
            $manifest['checkpoint_id']=$run['checkpoint_id'];
        }
        $run['end_manifest']=is_array($manifest)?$manifest:array();$run['owner']='';$run['lease_expires_at']=0;$run['restart_available']=0;
        return $this->ebay_run_save($run);
    }

    /** Mirror the real component cursor/state into the one durable canonical run.
     * Legacy workers still persist their own bounded job state; the canonical run
     * must snapshot that real state after every tick so progress/no-progress,
     * reloads and upgrades observe the same cursors instead of stale phase_state. */
    private function ebay_run_capture_component_state($run = null, $keys = array()) {
        $run=is_array($run)?$run:$this->ebay_run_load();
        if(!$this->ebay_run_is_open($run)){return $run;}
        $keys=$keys?array_values(array_unique(array_map('sanitize_key',(array)$keys))):array('maintenance','discovery','refresh','selection');
        if(!isset($run['phase_state'])||!is_array($run['phase_state'])){$run['phase_state']=array();}
        foreach($keys as $key){
            $state=array();
            if($key==='maintenance' && method_exists($this,'ebay_maintenance_state_load')){$state=$this->ebay_maintenance_state_load();}
            elseif($key==='discovery' && method_exists($this,'ebay_sync_job_load')){$state=$this->ebay_sync_job_load();}
            elseif($key==='refresh' && method_exists($this,'ebay_refresh_job_load')){$state=$this->ebay_refresh_job_load();}
            elseif($key==='selection' && method_exists($this,'ebay_selection_state_load')){$state=$this->ebay_selection_state_load();}
            if(is_array($state)&&$state){$run['phase_state'][$key]=$state;}
        }
        return $this->ebay_run_save($run);
    }

    private function ebay_run_progress_fingerprint($run) {
        $run=is_array($run)?$run:array();$phase_state=is_array($run['phase_state']??null)?$run['phase_state']:array();
        $sync=is_array($phase_state['discovery']??null)?$phase_state['discovery']:array();
        $refresh=is_array($phase_state['refresh']??null)?$phase_state['refresh']:array();
        $selection=is_array($phase_state['selection']??null)?$phase_state['selection']:array();
        $maintenance=is_array($phase_state['maintenance']??null)?$phase_state['maintenance']:array();
        return hash('sha256', wp_json_encode(array(
            'phase'=>sanitize_key((string)($run['phase']??'')),'remote_subphase'=>sanitize_key((string)($run['remote_subphase']??'')),'progress_contract_version'=>sanitize_text_field((string)($run['progress_contract_version']??'')),
            'sync'=>array('status'=>$sync['status']??'','profile_cursor'=>absint($sync['profile_cursor']??0),'progress_seq'=>absint($sync['progress_seq']??0),'current_page_index'=>absint($sync['current_page']['index']??0)),
            'refresh'=>array('status'=>$refresh['status']??'','last_id'=>absint($refresh['last_id']??0),'progress_seq'=>absint($refresh['progress_seq']??0),'checked'=>absint($refresh['summary']['checked']??0),'phase'=>$refresh['summary']['phase']??''),
            // One authoritative selection progress contract. Do not duplicate
            // a partial cursor list here: that omission caused the V6.41.3
            // production false-stall during fair PRIVATE per-leaf preparation.
            'selection_fingerprint'=>method_exists($this,'ebay_selection_progress_fingerprint') ? $this->ebay_selection_progress_fingerprint($selection) : '',
            'maintenance'=>array('cursor'=>absint($maintenance['cursor']??0),'completed_at'=>absint($maintenance['completed_at']??0)),
            'coverage'=>array('covered'=>absint($run['coverage']['covered']??0),'missing'=>count((array)($run['coverage']['missing']??array()))),
            'gapfill_attempts'=>absint($run['gapfill']['attempts']??0),
            'checkpoint_cleanup'=>array(
                'business_cursor'=>absint($run['checkpoint_cleanup_selection']['business_prune_cursor']??0),
                'business_done'=>!empty($run['checkpoint_cleanup_selection']['checkpoint_business_cleanup_done'])?1:0,
                'private_cursor'=>absint($run['checkpoint_cleanup_selection']['private_post_cursor']??0),
                'private_done'=>!empty($run['checkpoint_cleanup_selection']['checkpoint_private_cleanup_done'])?1:0,
            ),
        ), JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
    }

    private function ebay_run_acquire_lease(&$run) {
        $run=$this->ebay_run_load();
        if(!$this->ebay_run_is_open($run)){return false;}
        $now=time();$owner=sanitize_text_field((string)($run['owner']??''));$expires=absint($run['lease_expires_at']??0);
        if($owner!=='' && $expires>$now){return false;}
        $token='worker:'.substr(hash('sha256', self::EBAY_RUNTIME_BUILD.'|'.microtime(true).'|'.mt_rand()),0,24);
        $candidate=$run;$candidate['owner']=$token;$candidate['lease_expires_at']=$now+45;$candidate['last_worker_at']=$now;$candidate['schema']='1.0';$candidate['build']=self::EBAY_RUNTIME_BUILD;$candidate['updated_at']=$now;

        // Acquire the persistent lease atomically. Two simultaneous cron requests
        // must not both become owner after reading the same expired state.
        global $wpdb;
        if(is_object($wpdb) && isset($wpdb->options) && method_exists($wpdb,'query') && method_exists($wpdb,'prepare') && function_exists('maybe_serialize')){
            $key=$this->ebay_run_option_key();$before=maybe_serialize($run);$after=maybe_serialize($candidate);
            $changed=$wpdb->query($wpdb->prepare("UPDATE {$wpdb->options} SET option_value=%s WHERE option_name=%s AND option_value=%s",$after,$key,$before));
            if((int)$changed!==1){$run=$this->ebay_run_load();return false;}
            if(function_exists('wp_cache_delete')){wp_cache_delete($key,'options');wp_cache_delete('alloptions','options');}
            $run=$candidate;return $token;
        }

        // Test/stub fallback: WordPress without a query-capable options table.
        $this->ebay_run_save($candidate);$verify=$this->ebay_run_load();
        if(!hash_equals($token,sanitize_text_field((string)($verify['owner']??'')))){return false;}
        $run=$verify;return $token;
    }

    private function ebay_run_release_lease($token) {
        $run=$this->ebay_run_load();$owner=sanitize_text_field((string)($run['owner']??''));
        if ($token!=='' && $owner!=='' && hash_equals($owner,$token)) {$run['owner']='';$run['lease_expires_at']=0;$this->ebay_run_save($run);}
    }

    private function ebay_run_set_phase($phase, $resume_reason = '') {
        $run=$this->ebay_run_load();if(!$this->ebay_run_is_open($run)){return $run;}
        $run['phase']=sanitize_key((string)$phase);$run['resume_reason']=sanitize_key((string)$resume_reason);$run['progress_seq']=absint($run['progress_seq']??0)+1;$run['last_progress_at']=time();$run['no_progress_count']=0;
        return $this->ebay_run_save($run);
    }

    private function ebay_run_tick_reconcile($run, $settings) {
        $stats=$this->run_ebay_maintenance_v2(250,false,8,true);
        if (is_wp_error($stats)) { $this->ebay_run_fail($stats->get_error_code(),$stats->get_error_message()); return; }
        $this->ebay_run_capture_component_state(null,array('maintenance'));
        $state=$this->ebay_maintenance_state_load();
        if ($this->ebay_maintenance_state_is_current($state)) {
            $this->ebay_run_set_phase('refresh_remote','');
        }
    }

    private function ebay_run_tick_remote($run, $settings) {
        $sub=sanitize_key((string)($run['remote_subphase']??'inventory'));
        if ($sub==='discovery') {
            $job=$this->ebay_sync_job_load();
            $status=sanitize_key((string)($job['status']??''));
            if ($status==='partial') {
                if ($this->ebay_sync_job_is_resumable_partial($job) && sanitize_key((string)($job['scope']??''))==='all') {
                    $author_id=absint($job['listing_author_id']??0);
                    $job=$this->ebay_sync_resume_partial_job($job,$author_id);
                    if(!$job){$this->ebay_run_fail('discovery_partial_resume_failed','Persistierter Discovery-Checkpoint konnte nicht fortgesetzt werden.',array('stopped_reason'=>sanitize_key((string)($job['summary']['budget']['stopped_reason']??''))));return;}
                } else {
                    $reason=sanitize_key((string)($job['summary']['budget']['stopped_reason']??'discovery_partial_unresumable'));
                    $this->ebay_run_fail('discovery_partial_unresumable','Discovery endete in einem nicht fortsetzbaren PARTIAL-Zustand.',array('stopped_reason'=>$reason,'scope'=>sanitize_key((string)($job['scope']??''))));return;
                }
            } elseif (!$this->ebay_sync_job_is_open($job) && $status!=='completed') {
                $start=$this->ebay_start_sync_job(false,'all','background');
                if (is_wp_error($start)) {$this->ebay_run_fail($start->get_error_code(),$start->get_error_message());return;}
            }
            $this->run_ebay_sync_worker(true);
            $this->ebay_run_capture_component_state(null,array('discovery'));
            $job=$this->ebay_sync_job_load();$status=sanitize_key((string)($job['status']??''));
            if ($status==='failed') {
                $error_list=is_array($job['summary']['errors']??null)?$job['summary']['errors']:array();
                $last=$error_list ? (array)$error_list[count($error_list)-1] : array();
                $code=sanitize_key((string)($last['code']??$job['failure_reason']??'discovery_failed'));
                $msg=sanitize_text_field((string)($last['error']??$job['failure_reason']??'eBay-Discovery ist fehlgeschlagen.'));
                $this->ebay_run_fail($code!==''?$code:'discovery_failed',$msg);return;
            }
            if ($status==='completed') {
                $run=$this->ebay_run_load();$run['remote_subphase']='inventory';$run['resume_reason']='';$run['progress_seq']=absint($run['progress_seq']??0)+1;$run['last_progress_at']=time();$this->ebay_run_save($run);
            }
            return;
        }

        $job=$this->ebay_refresh_job_load();
        if (!$this->ebay_refresh_job_is_open($job)) {
            if ($this->ebay_refresh_job_is_resumable_partial($job)) {
                $job=$this->ebay_refresh_resume_partial_job($job);
            } elseif ($this->ebay_refresh_job_is_bounded_manual_partial($job)) {
                $job=$this->ebay_refresh_resume_bounded_remote_job($job);
            } elseif (sanitize_key((string)($job['status']??''))!=='completed') {
                $start=$this->ebay_start_inventory_refresh_job(true,true);
                if (is_wp_error($start)) {$this->ebay_run_fail($start->get_error_code(),$start->get_error_message());return;}
                $job=$this->ebay_refresh_job_load();
            }
        }
        if ($this->ebay_refresh_job_is_open($job)) {$this->run_ebay_inventory_refresh_worker(true);$job=$this->ebay_refresh_job_load();}
        $this->ebay_run_capture_component_state(null,array('refresh'));
        $status=sanitize_key((string)($job['status']??''));
        if ($status==='failed') {
            $code=sanitize_key((string)($job['summary']['failure_reason']??$job['failure_reason']??'inventory_refresh_failed'));
            $this->ebay_run_fail($code!==''?$code:'inventory_refresh_failed',sanitize_text_field((string)($job['summary']['stopped_reason']??$job['summary']['failure_reason']??'eBay-Bestandsabgleich ist fehlgeschlagen.')));return;
        }
        if ($status==='partial') {
            $run=$this->ebay_run_load();$run['resume_reason']=sanitize_key((string)($job['summary']['stopped_reason']??'bounded_checkpoint'));$this->ebay_run_save($run);return;
        }
        if ($status==='completed') {$this->ebay_run_set_phase('selection_prepare','');}
    }

    private function ebay_run_tick_selection($run, $settings) {
        $scope=$this->ebay_run_selection_scope($run);
        if($scope===''){$this->ebay_run_fail('selection_scope_empty','Der beim Runstart gespeicherte Seller-Routen-Snapshot enthält keine aktive Route.');return;}
        $canonical_phase=sanitize_key((string)($run['phase']??''));
        $selection=$this->ebay_selection_state_load();
        if(!$this->ebay_selection_state_is_open($selection) && sanitize_key((string)($selection['status']??''))!=='complete'){
            $selection=$this->ebay_selection_request('canonical_run','run:'.sanitize_text_field((string)$run['run_uuid']),true,$scope);
            $this->ebay_run_capture_component_state(null,array('selection'));
        }
        if(sanitize_key((string)($selection['status']??''))==='failed'){
            $this->ebay_run_fail(sanitize_key((string)($selection['failure_reason']??'selection_failed')),sanitize_text_field((string)($selection['error']??$selection['failure_reason']??'Bestandsauswahl ist fehlgeschlagen.')));return;
        }
        if(sanitize_key((string)($selection['status']??''))==='complete'){
            $this->ebay_run_checkpoint_capture_selection($selection,'full');
            $revalidated=$this->ebay_run_mark_private_public_revalidation_complete($selection);
            $this->ebay_run_set_phase('coverage_verify',$revalidated?'private_public_revalidated':'');return;
        }
        // The target contract names BUSINESS selection as its own durable phase.
        // Winner ranking is produced during bounded selection_prepare. Expose one
        // state-only checkpoint before materialisation so the canonical run never
        // jumps directly from prepare to mutation. No winner/source/output data is
        // changed here; an inconsistent nested selection fails closed.
        if($canonical_phase==='business_select'){
            $nested_phase=sanitize_key((string)($selection['phase']??''));
            if(!in_array($nested_phase,array('business_materialize','business_prune'),true)){
                $this->ebay_run_fail('business_select_checkpoint_invalid','BUSINESS-Select-Checkpoint passt nicht zum persistenten Selection-Zustand.',array('selection_phase'=>$nested_phase));return;
            }
            $this->ebay_run_set_phase('business_materialize','');
            return;
        }
        $selection=$this->ebay_selection_process_tick($settings,$selection);
        $this->ebay_run_capture_component_state(null,array('selection'));
        if(sanitize_key((string)($selection['status']??''))==='failed'){
            $this->ebay_run_fail(sanitize_key((string)($selection['failure_reason']??'selection_failed')),sanitize_text_field((string)($selection['error']??$selection['failure_reason']??'Bestandsauswahl ist fehlgeschlagen.')));return;
        }
        $phase=sanitize_key((string)($selection['phase']??''));
        $mapped='selection_prepare';
        if(in_array($phase,array('business_materialize','business_prune'),true)){
            $mapped=($canonical_phase==='selection_prepare' && $phase==='business_materialize')?'business_select':'business_materialize';
        }
        elseif(in_array($phase,array('private_prune','private','private_verify'),true)){$mapped=in_array($phase,array('private','private_verify'),true)?'private_materialize':'private_select';}
        $run=$this->ebay_run_load();if($this->ebay_run_is_open($run)){$run['phase']=$mapped;$this->ebay_run_save($run);}
        if(sanitize_key((string)($selection['status']??''))==='complete'){
            $this->ebay_run_checkpoint_capture_selection($selection,'full');
            $revalidated=$this->ebay_run_mark_private_public_revalidation_complete($selection);
            $this->ebay_run_set_phase('coverage_verify',$revalidated?'private_public_revalidated':'');
        }
    }

    /** Public BUSINESS coverage from actual published output objects plus the
     * current source/policy/product-identity contract. The query is hard bounded;
     * a bound overflow fails closed instead of turning into an unbounded scan. */
    private function ebay_run_public_business_coverage($allowed_campaign_ids = null) {
        $required=array_values(array_filter(array_map('sanitize_key',$this->ebay_business_required_product_concept_ids())));
        $allowed_map=is_array($allowed_campaign_ids)?array_fill_keys(array_values(array_filter(array_map('absint',$allowed_campaign_ids))),true):null;
        if(!$required){return array('required'=>0,'covered'=>0,'missing'=>array(),'counts'=>array(),'invalid'=>array(),'error_code'=>'business_supply_contract_invalid');}
        $required_map=array_fill_keys($required,true);$covered=array();$counts=array();$invalid=array();
        global $wpdb;
        if(!is_object($wpdb)||!method_exists($wpdb,'get_results')||!method_exists($this,'output_objects_table')){
            return array('required'=>count($required),'covered'=>0,'missing'=>$required,'counts'=>array(),'invalid'=>array(),'error_code'=>'business_public_storage_unavailable');
        }
        $output_table=$this->output_objects_table();$limit=1201;
        $objects=(array)$wpdb->get_results("SELECT * FROM {$output_table} WHERE provider='ebay' AND output_type='product_campaign' AND status='published' AND campaign_post_id>0 ORDER BY id ASC LIMIT {$limit}",ARRAY_A);
        if(count($objects)>1200){
            return array('required'=>count($required),'covered'=>0,'missing'=>$required,'counts'=>array(),'invalid'=>array(),'error_code'=>'business_public_object_bound_exceeded');
        }
        $now=time();
        foreach($objects as $object){
            $oid=absint($object['id']??0);$campaign_id=absint($object['campaign_post_id']??0);
            if(is_array($allowed_map) && !isset($allowed_map[$campaign_id])){continue;}
            $hash=strtolower(sanitize_text_field((string)($object['creative_identity_hash']??'')));
            if(!preg_match('/^[a-f0-9]{64}$/',$hash)){$invalid[$oid?:count($invalid)+1]='creative_identity_missing';continue;}
            $row=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->ebay_items_table()} WHERE creative_identity_hash=%s AND seller_account_type='BUSINESS' ORDER BY id DESC LIMIT 1",$hash),ARRAY_A);
            if(!is_array($row)){$invalid[$oid]='source_missing';continue;}
            if(sanitize_key((string)($row['status']??''))==='blocked_manual'){$invalid[$oid]='manual_block';continue;}
            if(sanitize_key((string)($row['source_state']??''))!=='available'){$invalid[$oid]='source_not_available';continue;}
            if(sanitize_key((string)($row['policy_state']??''))!=='allowed'){$invalid[$oid]='policy_not_allowed';continue;}
            if(!in_array(sanitize_key((string)($row['route_state']??'')),array('ready','review_last_good'),true)){$invalid[$oid]='route_not_public';continue;}
            if(absint($row['fresh_until']??0)<=$now){$invalid[$oid]='source_stale';continue;}
            $end=absint($row['item_end_at']??0);if($end>0&&$end<=$now){$invalid[$oid]='source_ended';continue;}
            if($this->ebay_public_content_policy_reason_from_source_row($row,(string)($row['title']??''))!==''){$invalid[$oid]='content_policy';continue;}
            $image=$this->ebay_remote_image_url_validate((string)($object['image_url']??$row['image_url']??''));
            if($image===''){$invalid[$oid]='image_invalid';continue;}

            $payload=json_decode((string)($row['source_payload']??''),true);$payload=is_array($payload)?$payload:array();
            $class=is_array($payload['portal_classification']??null)?$payload['portal_classification']:array();
            $concept=sanitize_key((string)($class['product_concept_id']??''));
            if($concept===''||!isset($required_map[$concept])||sanitize_key((string)($row['rule_id']??''))!==$concept){$invalid[$oid]='concept_identity_mismatch';continue;}
            if(sanitize_key((string)($class['business_match_contract']??''))!=='concept_v3'){$invalid[$oid]='concept_contract_missing';continue;}

            // Public coverage must reconstruct the expected campaign target set
            // from the same verified Creative Library contract that originally
            // materialized the campaign. ebay_business_campaign_target_keys()
            // consumes a Creative Library row (provider/source_kind/creative_type/
            // payload), not an eBay source-table row (source_payload/rule_id).
            // Passing the source row here made the expected set empty for every
            // otherwise-valid BUSINESS campaign and therefore forced a false
            // target_mismatch / 0-of-N result. Keep source freshness/concept
            // identity authoritative above, then bridge to the exact linked
            // creative by the immutable identity hash for target verification.
            if(!method_exists($this,'creative_library_table')){$invalid[$oid]='creative_storage_unavailable';continue;}
            $creative=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->creative_library_table()} WHERE identity_hash=%s ORDER BY id DESC LIMIT 1",$hash),ARRAY_A);
            if(!is_array($creative)){$invalid[$oid]='creative_missing';continue;}
            $creative_payload=json_decode((string)($creative['payload']??''),true);$creative_payload=is_array($creative_payload)?$creative_payload:array();
            if(sanitize_key((string)($creative['provider']??''))!=='ebay'
                || sanitize_key((string)($creative['source_kind']??''))!=='ebay_business_item'
                || sanitize_key((string)($creative['creative_type']??''))!=='product'
                || sanitize_key((string)($creative_payload['ebay_verified_product_concept']??''))!==$concept
                || sanitize_text_field((string)($creative_payload['ebay_item_id']??''))!==sanitize_text_field((string)($row['item_id']??''))){$invalid[$oid]='creative_source_mismatch';continue;}

            $campaign_id=absint($object['campaign_post_id']??0);
            $campaign=method_exists($this,'output_campaign_by_post_id')?$this->output_campaign_by_post_id($campaign_id):null;
            if(!is_array($campaign) && function_exists('get_post')){$post=get_post($campaign_id);$campaign=$post?$this->campaign_from_post($post):null;}
            if(!is_array($campaign)||empty($campaign['active'])||sanitize_key((string)($campaign['network']??''))!=='ebay'||sanitize_key((string)($campaign['creative_type']??''))!=='product'){$invalid[$oid]='campaign_not_public';continue;}
            $actual=array_values(array_unique(array_filter(array_map(array($this,'automation_normalize_target_key'),(array)($campaign['automation_target_keys']??array())))));
            $expected=array_values(array_unique(array_filter(array_map(array($this,'automation_normalize_target_key'),$this->ebay_business_campaign_target_keys($creative)))));
            if(!$actual||!$expected||!array_intersect($actual,$expected)){$invalid[$oid]='target_mismatch';continue;}

            $covered[$concept]=1;$counts[$concept]=absint($counts[$concept]??0)+1;
        }
        $over=array();foreach($counts as $concept=>$count){if($count>3){$over[$concept]=$count;}}
        $missing=array_values(array_diff($required,array_keys($covered)));sort($missing,SORT_STRING);
        $out=array('required'=>count($required),'covered'=>count($covered),'missing'=>$missing,'counts'=>$counts,'invalid'=>$invalid,'over_capacity'=>$over);
        if($over){$out['error_code']='business_family_cap_exceeded';}
        return $out;
    }

    private function ebay_run_verify_private_public($settings, $allowed_listing_ids = null) {
        if(empty($settings['private_enabled'])){return array('status'=>'disabled','public'=>0,'invalid'=>array());}
        global $wpdb;$invalid=array();$public=0;$cap=min(250,max(1,absint($settings['private_active_cap']??250)));
        $allowed_map=is_array($allowed_listing_ids)?array_fill_keys(array_values(array_filter(array_map('absint',$allowed_listing_ids))),true):null;
        $seen=array();
        if(!is_object($wpdb)||!method_exists($wpdb,'get_results')||!method_exists($wpdb,'get_row')){return array('status'=>'failed','error_code'=>'private_public_storage_unavailable','public'=>0,'invalid'=>array());}
        $postmeta=isset($wpdb->postmeta)?$wpdb->postmeta:$wpdb->prefix.'postmeta';
        $markers=array('_ppar_ebay_item_id','_ppar_ebay_seller_type','_ppar_ebay_affiliate_url','_ppar_ebay_source_hash','_ppar_ebay_portal_path','_ppar_ebay_target_term_id');
        $quoted=array_map(static function($v){return "'".esc_sql($v)."'";},$markers);
        $sql="SELECT DISTINCT p.ID FROM {$wpdb->posts} p INNER JOIN {$postmeta} pm ON pm.post_id=p.ID WHERE p.post_type='hp_listing' AND p.post_status='publish' AND pm.meta_key IN (".implode(',',$quoted).") ORDER BY p.ID ASC LIMIT 1001";
        $posts=(array)$wpdb->get_results($sql,ARRAY_A);
        if(count($posts)>1000){return array('status'=>'failed','error_code'=>'private_public_bound_exceeded','public'=>count($posts),'invalid'=>array());}
        $now=time();
        foreach($posts as $post){
            $id=absint($post['ID']??0);if($id<=0){continue;}
            if(is_array($allowed_map) && !isset($allowed_map[$id])){continue;}
            $own=$this->ebay_private_post_ownership($id);if(empty($own['owned'])){continue;}$public++;$seen[$id]=1;
            $hard=$this->ebay_private_post_hard_negative_reason($id);if($hard!==''){$invalid[$id]='hard_negative:'.$hard;continue;}
            $item_id=function_exists('get_post_meta')?sanitize_text_field((string)get_post_meta($id,'_ppar_ebay_item_id',true)):'';
            if($item_id===''){$invalid[$id]='item_identity_missing';continue;}
            $row=$wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->ebay_items_table()} WHERE item_id=%s AND seller_account_type='INDIVIDUAL' ORDER BY id DESC LIMIT 1",$item_id),ARRAY_A);
            if(!is_array($row)){$invalid[$id]='source_missing';continue;}
            $listing_hash=function_exists('get_post_meta')?strtolower(sanitize_text_field((string)get_post_meta($id,'_ppar_ebay_source_hash',true))):'';
            $row_hash=strtolower(sanitize_text_field((string)($row['source_hash']??'')));
            if($listing_hash===''||$row_hash===''||!hash_equals($listing_hash,$row_hash)){$invalid[$id]='source_hash_mismatch';continue;}
            if(sanitize_key((string)($row['status']??''))==='blocked_manual'){$invalid[$id]='manual_block';continue;}
            if(sanitize_key((string)($row['source_state']??''))!=='available'){$invalid[$id]='source_not_available';continue;}
            if(sanitize_key((string)($row['policy_state']??''))!=='allowed'){$invalid[$id]='policy_not_allowed';continue;}
            if(sanitize_key((string)($row['route_state']??''))!=='ready'){$invalid[$id]='route_not_ready';continue;}
            $target=absint($row['target_term_id']??0);if($target<=0){$invalid[$id]='target_missing';continue;}
            if(absint($row['fresh_until']??0)<=$now){$invalid[$id]='source_stale';continue;}
            $end=absint($row['item_end_at']??0);if($end>0&&$end<=$now){$invalid[$id]='ended';continue;}
            $reason=$this->ebay_public_content_policy_reason_from_source_row($row,(string)($row['title']??''));if($reason!==''){$invalid[$id]='policy:'.$reason;continue;}
            if($this->ebay_remote_image_url_validate((string)($row['image_url']??''))===''){$invalid[$id]='image_invalid';continue;}
            if(function_exists('wp_get_post_terms')){
                $terms=wp_get_post_terms($id,'hp_listing_category',array('fields'=>'ids'));
                if(is_wp_error($terms)||!in_array($target,array_map('absint',(array)$terms),true)){$invalid[$id]='target_taxonomy_mismatch';continue;}
            }
        }
        if(is_array($allowed_map)){
            foreach(array_keys($allowed_map) as $id){if(!isset($seen[$id])){$invalid[absint($id)]='checkpoint_candidate_not_published';}}
        }
        if($public>$cap){return array('status'=>'failed','error_code'=>'private_public_cap_exceeded','public'=>$public,'invalid'=>$invalid);}
        if($invalid){return array('status'=>'failed','error_code'=>'private_public_gate_failed','public'=>$public,'invalid'=>$invalid);}
        return array('status'=>'pass','public'=>$public,'invalid'=>array());
    }

    /**
     * V6.63 PRIVATE tail revalidation contract.
     *
     * Root cause proven on the V6.62 live run: after a full ALL selection, a
     * long BUSINESS gap-fill replaces phase_state.selection with a BUSINESS-only
     * selector while checkpoint_candidate.private_listing_ids intentionally keep
     * the earlier PRIVATE candidate set. Hours later public_verify validates those
     * earlier PRIVATE rows against current source freshness/end/policy state and can
     * terminal-fail even though all BUSINESS work is complete. The correct fix is
     * not a whole-run restart: rerun exactly the existing bounded PRIVATE selector,
     * preserve BUSINESS candidates/gap proof and then re-enter coverage/public gates.
     */
    private function ebay_run_private_public_revalidation_required($run, $settings) {
        $run=is_array($run)?$run:array();$settings=is_array($settings)?$settings:array();
        if(empty($settings['private_enabled'])){return false;}
        if(absint($run['gapfill']['attempts']??0)<1){return false;}
        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        if(sanitize_key((string)($selection['selection_scope']??''))!=='business'){return false;}
        if(sanitize_key((string)($selection['status']??''))!=='complete'){return false;}
        $state=is_array($run['private_public_revalidation']??null)?$run['private_public_revalidation']:array();
        return sanitize_key((string)($state['status']??''))!=='complete';
    }

    private function ebay_run_begin_private_public_revalidation($run, $reason='post_business_gapfill', $failure=array()) {
        $run=is_array($run)?$run:$this->ebay_run_load();
        if(!$this->ebay_run_is_open($run)){return false;}
        $routes=is_array($run['config_snapshot']['seller_routes']??null)?$run['config_snapshot']['seller_routes']:array();
        if(empty($routes['private'])){return false;}
        $state=is_array($run['private_public_revalidation']??null)?$run['private_public_revalidation']:array();
        $status=sanitize_key((string)($state['status']??''));
        if(in_array($status,array('pending','running'),true)){
            $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
            return sanitize_key((string)($selection['selection_scope']??''))==='private' && $this->ebay_selection_state_is_open($selection);
        }
        if($status==='complete' || absint($state['attempts']??0)>=1){return false;}

        $uuid=sanitize_text_field((string)($run['run_uuid']??''));if($uuid===''){return false;}
        $failure=is_array($failure)?$failure:array();
        $invalid=is_array($failure['invalid']??null)?$failure['invalid']:array();
        $reason_counts=array();foreach($invalid as $value){$k=sanitize_key((string)$value);if($k===''){$k='unknown';}$reason_counts[$k]=absint($reason_counts[$k]??0)+1;}
        $run['private_public_revalidation']=array(
            'status'=>'pending','attempts'=>1,'started_at'=>time(),
            'reason'=>sanitize_key((string)$reason),'failure_reason_counts'=>$reason_counts,
            'business_campaign_count'=>count((array)($run['checkpoint_candidate']['business_campaign_ids']??array())),
            'private_candidate_count_before'=>count((array)($run['checkpoint_candidate']['private_listing_ids']??array())),
        );
        $run['phase']='selection_prepare';$run['resume_reason']='private_public_revalidation';
        $run['progress_seq']=absint($run['progress_seq']??0)+1;$run['last_progress_at']=time();$run['no_progress_count']=0;
        $this->ebay_run_save($run);
        $selection=$this->ebay_selection_request('private_public_revalidation','run:'.$uuid,true,'private');
        if(sanitize_key((string)($selection['status']??''))==='failed'){
            $this->ebay_run_fail('private_public_revalidation_start_failed','PRIVATE-Endrevalidierung konnte nicht sicher gestartet werden.',array('selection'=>$selection));
            return false;
        }
        $current=$this->ebay_run_load();
        if($this->ebay_run_is_open($current)){
            $marker=is_array($current['private_public_revalidation']??null)?$current['private_public_revalidation']:array();
            $marker['status']='running';$marker['selection_owner']=sanitize_text_field((string)($selection['owner']??''));
            $current['private_public_revalidation']=$marker;$this->ebay_run_save($current);
        }
        return true;
    }

    private function ebay_run_mark_private_public_revalidation_complete($selection) {
        $selection=is_array($selection)?$selection:array();
        if(sanitize_key((string)($selection['selection_scope']??''))!=='private' || sanitize_key((string)($selection['status']??''))!=='complete'){return false;}
        $run=$this->ebay_run_load();if(!$this->ebay_run_is_open($run)){return false;}
        $state=is_array($run['private_public_revalidation']??null)?$run['private_public_revalidation']:array();
        if(!in_array(sanitize_key((string)($state['status']??'')),array('pending','running'),true)){return false;}
        $state['status']='complete';$state['completed_at']=time();
        $state['private_candidate_count_after']=count((array)($run['checkpoint_candidate']['private_listing_ids']??array()));
        $run['private_public_revalidation']=$state;$this->ebay_run_save($run);return true;
    }

    /** Only transient source-freshness churn is eligible for a bounded PRIVATE tail. */
    private function ebay_run_private_public_freshness_only_failure($private) {
        $private=is_array($private)?$private:array();
        if(sanitize_key((string)($private['error_code']??''))!=='private_public_gate_failed'){return false;}
        $invalid=is_array($private['invalid']??null)?$private['invalid']:array();
        if(!$invalid){return false;}
        foreach($invalid as $reason){
            if(sanitize_key((string)$reason)!=='source_stale'){return false;}
        }
        return true;
    }

    /**
     * V6.63.5 bounded runtime repair when a PRIVATE winner expires between the
     * final PRIVATE selector and public_verify. It keeps BUSINESS evidence and the
     * same run UUID, replaces only the PRIVATE tail, and is capped fail-closed.
     */
    private function ebay_run_reopen_private_after_public_freshness_churn($run,$private,$reason='public_gate_source_stale') {
        $run=is_array($run)?$run:$this->ebay_run_load();
        if(!$this->ebay_run_is_open($run) || !$this->ebay_run_private_public_freshness_only_failure($private)){return false;}
        $routes=is_array($run['config_snapshot']['seller_routes']??null)?$run['config_snapshot']['seller_routes']:array();
        if(empty($routes['private'])){return false;}
        $uuid=sanitize_text_field((string)($run['run_uuid']??''));if($uuid===''){return false;}
        $state=is_array($run['private_public_revalidation']??null)?$run['private_public_revalidation']:array();
        $churn=absint($state['public_freshness_churn_attempts']??0);
        if($churn>=2){return false;}
        $invalid=(array)($private['invalid']??array());$reason_counts=array();
        foreach($invalid as $value){$k=sanitize_key((string)$value);if($k===''){$k='unknown';}$reason_counts[$k]=absint($reason_counts[$k]??0)+1;}
        $run['private_public_revalidation']=array(
            'status'=>'pending','attempts'=>absint($state['attempts']??0)+1,
            'public_freshness_churn_attempts'=>$churn+1,'started_at'=>time(),
            'reason'=>sanitize_key((string)$reason),'failure_reason_counts'=>$reason_counts,
            'business_campaign_count'=>count((array)($run['checkpoint_candidate']['business_campaign_ids']??array())),
            'private_candidate_count_before'=>count((array)($run['checkpoint_candidate']['private_listing_ids']??array())),
        );
        $run['phase']='selection_prepare';$run['resume_reason']='private_public_freshness_revalidation';
        $run['progress_seq']=absint($run['progress_seq']??0)+1;$run['last_progress_at']=time();$run['no_progress_count']=0;
        $this->ebay_run_save($run);
        $selection=$this->ebay_selection_request('private_public_freshness_revalidation','run:'.$uuid,true,'private');
        if(sanitize_key((string)($selection['status']??''))==='failed'){
            $this->ebay_run_fail('private_public_freshness_revalidation_start_failed','PRIVATE-Frische-Endrevalidierung konnte nicht sicher gestartet werden.',array('selection'=>$selection));
            return false;
        }
        $current=$this->ebay_run_load();
        if($this->ebay_run_is_open($current)){
            $marker=is_array($current['private_public_revalidation']??null)?$current['private_public_revalidation']:array();
            $marker['status']='running';$marker['selection_owner']=sanitize_text_field((string)($selection['owner']??''));
            $current['private_public_revalidation']=$marker;$this->ebay_run_save($current);
        }
        return true;
    }

    /**
     * V6.63.5 state-only recovery for the exact live V6.63.4 terminal state:
     * BUSINESS proof recovery completed, the fresh PRIVATE tail completed, but
     * final public_verify rejected one or more winners solely as source_stale.
     */
    public function maybe_recover_ebay_private_public_freshness_v6635() {
        if(function_exists('current_user_can') && !current_user_can('manage_options')){return;}
        $run=$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0' || sanitize_key((string)($run['status']??''))!=='failed'){return;}
        $loaded=$run;$code=sanitize_key((string)($run['error_code']??''));
        if($code!=='private_public_gate_failed'){return;}
        $failure=$this->ebay_run_last_failure_entry($run,$code);$details=is_array($failure['details']??null)?$failure['details']:array();
        if(sanitize_key((string)($details['phase']??''))!=='public_verify'){return;}
        $failure_build=sanitize_text_field((string)($details['build']??$run['build']??''));
        if($failure_build!=='6.63.4-live-observed-gap-proof-recovery-rootfix-20260828'){return;}
        $private=array('error_code'=>$code,'invalid'=>is_array($details['invalid']??null)?$details['invalid']:array(),'public'=>absint($details['public']??0));
        if(!$this->ebay_run_private_public_freshness_only_failure($private)){return;}
        $routes=is_array($run['config_snapshot']['seller_routes']??null)?$run['config_snapshot']['seller_routes']:array();
        if(empty($routes['private']) || empty($routes['business'])){return;}
        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        if(sanitize_key((string)($selection['status']??''))!=='complete'
            || sanitize_key((string)($selection['phase']??''))!=='complete'
            || absint($selection['prepare_private_scanned']??0)<1){return;}
        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();$has_business_proof_recovery=false;
        foreach($history as $entry){if(is_array($entry)&&sanitize_key((string)($entry['reason']??''))==='business_gap_proof_regeneration'){$has_business_proof_recovery=true;break;}}
        if(!$has_business_proof_recovery){return;}
        $uuid=sanitize_text_field((string)($run['run_uuid']??''));if($uuid===''){return;}
        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$uuid.'|'.$failure_at.'|private_public_freshness_revalidation|6.63.5');
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $reason_counts=array();foreach((array)$private['invalid'] as $value){$k=sanitize_key((string)$value);$reason_counts[$k]=absint($reason_counts[$k]??0)+1;}
        $history[]=array('at'=>time(),'reason'=>'private_public_freshness_revalidation','error_code'=>$code,'migration_key'=>$marker,
            'preserved_run_uuid'=>1,'preserved_business_candidates'=>count((array)($run['checkpoint_candidate']['business_campaign_ids']??array())),
            'preserved_business_gap_proof'=>!empty($run['gapfill']['selection_proof'])?1:0,'failure_reason_counts'=>$reason_counts,
            'discovery_restarted'=>0,'full_run_restarted'=>0,'external_tick_bootstrap_requested'=>1);
        if(count($history)>8){$history=array_slice($history,-8);}
        $prior=is_array($run['private_public_revalidation']??null)?$run['private_public_revalidation']:array();
        $run['recovery_history']=$history;$run['status']='running';$run['phase']='selection_prepare';$run['finished_at']=0;
        $run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='external_tick';$run['resume_reason']='private_public_freshness_revalidation';$run['no_progress_count']=0;
        $run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();$run['progress_seq']=absint($run['progress_seq']??0)+1;
        $run['progress_contract_version']=$this->ebay_run_progress_contract_version();
        $run['private_public_revalidation']=array('status'=>'pending','attempts'=>absint($prior['attempts']??0)+1,'public_freshness_churn_attempts'=>1,
            'started_at'=>time(),'reason'=>'live_v6634_source_stale','failure_reason_counts'=>$reason_counts,
            'private_candidate_count_before'=>count((array)($run['checkpoint_candidate']['private_listing_ids']??array())),
            'business_campaign_count'=>count((array)($run['checkpoint_candidate']['business_campaign_ids']??array())));
        $saved=$this->ebay_run_compare_and_swap($loaded,$run);if($saved===false){return;}
        $selection=$this->ebay_selection_request('private_public_freshness_revalidation','run:'.$uuid,true,'private');
        if(sanitize_key((string)($selection['status']??''))==='failed'){
            $this->ebay_run_fail('private_public_freshness_revalidation_start_failed','PRIVATE-Frische-Endrevalidierung konnte aus dem V6.63.4-Livezustand nicht sicher gestartet werden.',array('selection'=>$selection));return;
        }
        $current=$this->ebay_run_load();if($this->ebay_run_is_open($current)){$state=is_array($current['private_public_revalidation']??null)?$current['private_public_revalidation']:array();$state['status']='running';$state['selection_owner']=sanitize_text_field((string)($selection['owner']??''));$current['private_public_revalidation']=$state;$this->ebay_run_save($current);}
        $this->ebay_run_bootstrap_recovered_external_tick_v6632($uuid);
    }

    /**
     * V6.63 one-time state-only recovery for the exact V6.62 production failure.
     * It preserves run UUID, source/refresh evidence, BUSINESS candidates, gap-fill
     * proof and the current public checkpoint. No listing/campaign/source mutation
     * happens on admin_init. The next external heartbeat performs the ordinary
     * bounded PRIVATE selector. New-build failures are never auto-reopened.
     */
    /**
     * V6.63.2 one-shot bootstrap for a recovered terminal run. The canonical
     * worker remains external_tick-only: this performs exactly one non-blocking
     * same-origin POST after the state-only recovery has been persisted and the
     * PRIVATE selector has been queued. It schedules no cron, creates no second
     * run and writes no state after dispatch, so a fast worker cannot be
     * overwritten by the originating admin request. The 15-minute GitHub safety
     * schedule remains the fallback if the loopback transport is unavailable.
     */
    private function ebay_run_bootstrap_recovered_external_tick_v6632($run_uuid) {
        return $this->ebay_run_dispatch_self_drive((string)$run_uuid, 'recovery_bootstrap');
    }

    public function maybe_recover_ebay_private_public_gate_v6630() {
        if(function_exists('current_user_can') && !current_user_can('manage_options')){return;}
        $run=$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0' || sanitize_key((string)($run['status']??''))!=='failed'){return;}
        $loaded=$run;$code=sanitize_key((string)($run['error_code']??''));
        if(!in_array($code,array('private_public_gate_failed','private_public_cap_exceeded'),true)){return;}
        $failure=$this->ebay_run_last_failure_entry($run,$code);$details=is_array($failure['details']??null)?$failure['details']:array();
        if(sanitize_key((string)($details['phase']??''))!=='public_verify'){return;}
        $failure_build=sanitize_text_field((string)($details['build']??$run['build']??''));
        if($failure_build!=='6.56.0-safe-gap-churn-revalidation-rootfix-20260827'){return;}
        $routes=is_array($run['config_snapshot']['seller_routes']??null)?$run['config_snapshot']['seller_routes']:array();
        if(empty($routes['private']) || absint($run['gapfill']['attempts']??0)<1){return;}
        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        if(sanitize_key((string)($selection['status']??''))!=='complete' || sanitize_key((string)($selection['selection_scope']??''))!=='business'){return;}
        $uuid=sanitize_text_field((string)($run['run_uuid']??''));if($uuid===''){return;}
        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();
        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$uuid.'|'.$failure_at.'|private_public_tail_revalidation|6.63.0');
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $invalid=is_array($details['invalid']??null)?$details['invalid']:array();$reason_counts=array();
        foreach($invalid as $value){$k=sanitize_key((string)$value);if($k===''){$k='unknown';}$reason_counts[$k]=absint($reason_counts[$k]??0)+1;}
        $history[]=array('at'=>time(),'reason'=>'private_public_tail_revalidation','error_code'=>$code,'migration_key'=>$marker,'preserved_run_uuid'=>1,'preserved_business_candidates'=>count((array)($run['checkpoint_candidate']['business_campaign_ids']??array())),'failure_reason_counts'=>$reason_counts,'external_tick_bootstrap_requested'=>1);
        if(count($history)>8){$history=array_slice($history,-8);}
        $run['recovery_history']=$history;$run['status']='running';$run['phase']='selection_prepare';$run['finished_at']=0;
        $run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='external_tick';$run['resume_reason']='private_public_gate_recovery';$run['no_progress_count']=0;
        $run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();$run['progress_seq']=absint($run['progress_seq']??0)+1;
        $run['progress_contract_version']=$this->ebay_run_progress_contract_version();
        $run['private_public_revalidation']=array('status'=>'pending','attempts'=>1,'started_at'=>time(),'reason'=>'failed_public_gate_recovery','failure_reason_counts'=>$reason_counts,'private_candidate_count_before'=>count((array)($run['checkpoint_candidate']['private_listing_ids']??array())),'business_campaign_count'=>count((array)($run['checkpoint_candidate']['business_campaign_ids']??array())));
        $saved=$this->ebay_run_compare_and_swap($loaded,$run);if($saved===false){return;}
        $selection=$this->ebay_selection_request('private_public_gate_recovery','run:'.$uuid,true,'private');
        if(sanitize_key((string)($selection['status']??''))==='failed'){
            $this->ebay_run_fail('private_public_revalidation_start_failed','PRIVATE-Endrevalidierung konnte nach dem alten Public-Gate-Fehler nicht sicher gestartet werden.',array('selection'=>$selection));return;
        }
        $current=$this->ebay_run_load();if($this->ebay_run_is_open($current)){$state=is_array($current['private_public_revalidation']??null)?$current['private_public_revalidation']:array();$state['status']='running';$state['selection_owner']=sanitize_text_field((string)($selection['owner']??''));$current['private_public_revalidation']=$state;$this->ebay_run_save($current);}
        $this->ebay_run_bootstrap_recovered_external_tick_v6632($uuid);
    }

    /**
     * V6.63.3 state-only repair for the exact V6.63 PRIVATE-tail proof-loss
     * failure. The PRIVATE selector legitimately replaced phase_state.selection,
     * so the old safe-gap guard lost its BUSINESS proof and failed with
     * business_safe_gap_proof_missing. Do not invent that proof from partial
     * cleanup data: reopen the SAME run at the already-bounded gapfill_select
     * phase so the canonical BUSINESS selector regenerates authoritative proof.
     * Discovery, refresh, run UUID, public checkpoint and existing materialized
     * candidates remain untouched. A fresh PRIVATE tail is required afterwards.
     */
    /**
     * V6.63.4 state-only recovery for the exact live V6.63.0 proof-loss state.
     *
     * V6.63.3 was too strict: it required hidden/private tail bookkeeping fields
     * (`private_public_revalidation.status`, selection_scope and owner) that are
     * not part of the terminal invariant and can legitimately be absent after
     * the completed PRIVATE tail has been persisted/merged. That made a proven
     * live terminal state fail to reopen even though the admin read-only state
     * already proved: PRIVATE tail finished, run is at coverage_verify, the
     * recovery history is the V6.63 PRIVATE-tail recovery and the safe-gap proof
     * is the only failing invariant.
     *
     * This repair gates only on durable/observable terminal invariants, keeps the
     * same run UUID, preserves discovery and candidate checkpoints, and reopens
     * only gapfill_select so canonical BUSINESS selection can regenerate the
     * missing proof. A fresh PRIVATE tail is required after that rerun.
     */
    public function maybe_recover_ebay_business_gap_proof_v6634() {
        if(function_exists('current_user_can') && !current_user_can('manage_options')){return;}
        $run=$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0' || sanitize_key((string)($run['status']??''))!=='failed'){return;}
        $loaded=$run;$code=sanitize_key((string)($run['error_code']??''));
        if($code!=='business_safe_gap_proof_missing'){return;}
        $failure=$this->ebay_run_last_failure_entry($run,$code);$details=is_array($failure['details']??null)?$failure['details']:array();
        if(sanitize_key((string)($details['phase']??''))!=='coverage_verify'){return;}
        $failure_build=sanitize_text_field((string)($details['build']??''));
        if($failure_build!=='6.63.0-private-public-tail-revalidation-rootfix-20260828'){return;}
        $gap_contract=is_array($details['gap_contract']??null)?$details['gap_contract']:array();
        if(sanitize_key((string)($gap_contract['error_code']??''))!=='business_safe_gap_proof_missing'){return;}

        $uuid=sanitize_text_field((string)($run['run_uuid']??''));if($uuid===''){return;}
        $routes=is_array($run['config_snapshot']['seller_routes']??null)?$run['config_snapshot']['seller_routes']:array();
        if(empty($routes['business']) || empty($routes['private'])){return;}
        if(sanitize_key((string)($run['resume_reason']??''))!=='private_public_revalidated'){return;}

        // Use the same durable fields that the live admin read-only diagnostic
        // exposes. Hidden bookkeeping is intentionally not required here.
        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        if(sanitize_key((string)($selection['status']??''))!=='complete'
            || sanitize_key((string)($selection['phase']??''))!=='complete'
            || absint($selection['prepare_private_scanned']??0)<1){return;}

        $gap_missing=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($run['gapfill']['missing']??array())))));
        $failed_missing=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($gap_contract['missing']??array())))));
        sort($gap_missing,SORT_STRING);sort($failed_missing,SORT_STRING);
        if(absint($run['gapfill']['attempts']??0)<1 || !$gap_missing || !$failed_missing){return;}
        foreach($failed_missing as $id){if(!in_array($id,$gap_missing,true)){return;}}

        $history=is_array($run['recovery_history']??null)?$run['recovery_history']:array();
        $has_private_tail_recovery=false;
        foreach($history as $entry){
            if(is_array($entry) && sanitize_key((string)($entry['reason']??''))==='private_public_tail_revalidation'
                && in_array(sanitize_key((string)($entry['error_code']??'')),array('private_public_gate_failed','private_public_cap_exceeded'),true)){
                $has_private_tail_recovery=true;break;
            }
        }
        if(!$has_private_tail_recovery){return;}

        $failure_at=absint($failure['at']??$run['finished_at']??0);
        $marker=hash('sha256',$uuid.'|'.$failure_at.'|business_gap_proof_regeneration|6.63.4');
        foreach($history as $entry){if(is_array($entry)&&hash_equals($marker,(string)($entry['migration_key']??''))){return;}}
        $history[]=array(
            'at'=>time(),'reason'=>'business_gap_proof_regeneration','error_code'=>$code,
            'migration_key'=>$marker,'preserved_run_uuid'=>1,
            'preserved_business_candidates'=>count((array)($run['checkpoint_candidate']['business_campaign_ids']??array())),
            'preserved_private_candidates'=>count((array)($run['checkpoint_candidate']['private_listing_ids']??array())),
            'target_count'=>count($gap_missing),'discovery_restarted'=>0,'full_run_restarted'=>0,
            'live_observed_terminal_gate'=>1,'external_tick_bootstrap_requested'=>1,
        );
        if(count($history)>8){$history=array_slice($history,-8);}

        $run['recovery_history']=$history;
        $run['status']='running';$run['phase']='gapfill_select';$run['finished_at']=0;
        $run['owner']='';$run['lease_expires_at']=0;$run['worker_transport']='external_tick';
        $run['resume_reason']='business_gap_proof_recovery';$run['no_progress_count']=0;
        $run['error_code']='';$run['error_message']='';$run['last_progress_at']=time();
        $run['progress_seq']=absint($run['progress_seq']??0)+1;
        $run['progress_contract_version']=$this->ebay_run_progress_contract_version();
        if(!isset($run['phase_state'])||!is_array($run['phase_state'])){$run['phase_state']=array();}
        $run['phase_state']['selection']=array();
        unset($run['gapfill']['selection_proof']);
        // BUSINESS rerun after the completed PRIVATE tail invalidates that tail
        // for final publication. Force exactly one fresh PRIVATE tail afterwards.
        $run['private_public_revalidation']=array();
        $saved=$this->ebay_run_compare_and_swap($loaded,$run);if($saved===false){return;}
        $this->ebay_run_bootstrap_recovered_external_tick_v6632($uuid);
    }

    /**
     * V6.50 coverage-gap contract.
     *
     * A missing public BUSINESS family is not automatically a technical failure
     * after the one bounded canonical gap-fill. It may become an open safe supply
     * gap only when the terminal canonical gap-fill selection proves that no
     * safely selectable candidate remained for that exact family.
     *
     * This guard deliberately reuses the already completed production selection
     * state instead of weakening/re-running acceptance or quality rules. If a
     * safely selected candidate exists but public coverage is still missing, the
     * state is an invariant/materialization failure and remains fail-closed.
     */
    private function ebay_run_business_safe_supply_gap_contract($run, $coverage) {
        $run=is_array($run)?$run:array();$coverage=is_array($coverage)?$coverage:array();
        $missing=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($coverage['missing']??array())))));
        sort($missing,SORT_STRING);
        if(!$missing){$coverage['contract_status']='complete';$coverage['open_gap_count']=0;$coverage['open_gaps']=array();return array('status'=>'pass','coverage'=>$coverage);}

        $required_count=absint($coverage['required']??0);
        if($required_count<1 || absint($coverage['covered']??0)!==$required_count-count($missing)){
            return array('status'=>'failed','error_code'=>'business_coverage_state_inconsistent','missing'=>$missing);
        }
        // Production has the authoritative required-family manifest on the eBay
        // trait. Keep this run-trait guard self-contained for old isolated test
        // harnesses, but when the manifest method exists it remains mandatory and
        // authoritative. This is a compatibility guard, not a weakened runtime
        // contract: the production class always supplies this method.
        if(method_exists($this,'ebay_business_required_product_concept_ids')){
            $required=array_values(array_unique(array_filter(array_map('sanitize_key',(array)$this->ebay_business_required_product_concept_ids()))));
            sort($required,SORT_STRING);$required_map=array_fill_keys($required,true);
            if(!$required || $required_count!==count($required)){
                return array('status'=>'failed','error_code'=>'business_coverage_state_inconsistent','missing'=>$missing);
            }
            foreach($missing as $id){if(!isset($required_map[$id])){return array('status'=>'failed','error_code'=>'business_coverage_unknown_family','missing'=>$missing);}}
        }
        if(absint($run['gapfill']['attempts']??0)<1){
            return array('status'=>'failed','error_code'=>'business_safe_gap_without_gapfill','missing'=>$missing);
        }

        $uuid=sanitize_text_field((string)($run['run_uuid']??''));
        $proof=is_array($run['gapfill']['selection_proof']??null)?$run['gapfill']['selection_proof']:array();
        // Backward compatibility for active pre-V6.63.3 runs before a PRIVATE tail:
        // a still-current canonical BUSINESS selector may be promoted into the
        // same minimal proof shape. Once PRIVATE replaces phase_state.selection,
        // only the durable proof is accepted.
        if(!$proof){
            $current_selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
            $proof=$this->ebay_run_business_gapfill_proof_from_selection($current_selection,$uuid);
        }
        if($uuid==='' || sanitize_key((string)($proof['status']??''))!=='complete'
            || sanitize_key((string)($proof['reason']??''))!=='canonical_gapfill'
            || sanitize_key((string)($proof['selection_scope']??''))!=='business'
            || sanitize_text_field((string)($proof['owner']??''))!=='run:'.$uuid
            || sanitize_key((string)($proof['business_target_mode']??''))!=='gapfill'){
            return array('status'=>'failed','error_code'=>'business_safe_gap_proof_missing','missing'=>$missing);
        }

        $original=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($run['gapfill']['missing']??array())))));
        $targets=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($proof['business_target_concepts']??array())))));
        sort($original,SORT_STRING);sort($targets,SORT_STRING);
        if(!$original || $targets!==$original){
            return array('status'=>'failed','error_code'=>'business_safe_gap_scope_mismatch','missing'=>$missing,'targeted'=>$targets);
        }
        $target_map=array_fill_keys($targets,true);
        foreach($missing as $id){if(!isset($target_map[$id])){return array('status'=>'failed','error_code'=>'business_safe_gap_new_missing_family','missing'=>$missing,'targeted'=>$targets);}}

        $selected_concepts=array();
        foreach((array)($proof['selected_concepts']??array()) as $id){
            $id=sanitize_key((string)$id);if($id!==''){$selected_concepts[$id]=1;}
        }
        $unexpected=array_values(array_intersect($missing,array_keys($selected_concepts)));sort($unexpected,SORT_STRING);
        if($unexpected){
            return array(
                'status'=>'failed','error_code'=>'business_gapfill_public_invariant_failed',
                'missing'=>$missing,'selected_but_not_public'=>$unexpected,
            );
        }

        $exceptions=array();
        foreach($missing as $id){
            $exceptions[$id]=array(
                'code'=>'safe_supply_gap_open','approved'=>0,'public'=>0,
                'retry'=>'next_scheduled_canonical_run',
            );
        }
        $coverage['contract_status']='complete_with_safe_supply_gaps';
        $coverage['open_gap_count']=count($missing);
        $coverage['open_gaps']=$missing;
        $coverage['exceptions']=$exceptions;
        $coverage['gapfill_attempts']=absint($run['gapfill']['attempts']??0);
        $coverage['retry_contract']='next_scheduled_canonical_run';
        $coverage['gap_proof']=array(
            'selection_owner'=>'run:'.$uuid,
            'target_count'=>count($targets),
            'selected_concepts'=>count($selected_concepts),
        );
        return array('status'=>'pass','coverage'=>$coverage);
    }

    /**
     * V6.56 live-churn revalidation.
     *
     * A family that becomes newly missing while the already-running canonical
     * gap-fill is being worked is normal marketplace churn, not proof that the
     * existing safety contract may be skipped. Expand the durable proof scope
     * monotonically, discover only the newly missing delta, then rerun the same
     * canonical BUSINESS selector over the full accumulated proof scope. Public
     * promotion remains blocked until the unchanged safe-gap contract passes.
     */
    private function ebay_run_schedule_new_business_gap_revalidation($run, $coverage, $origin_phase = '') {
        $run=is_array($run)?$run:array();$coverage=is_array($coverage)?$coverage:array();
        $missing=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($coverage['missing']??array())))));
        $targeted=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($run['gapfill']['missing']??array())))));
        sort($missing,SORT_STRING);sort($targeted,SORT_STRING);
        if(!$missing || !$targeted || absint($run['gapfill']['attempts']??0)<1){return false;}
        $target_map=array_fill_keys($targeted,true);$new=array();
        foreach($missing as $id){if(!isset($target_map[$id])){$new[$id]=1;}}
        $new=array_keys($new);sort($new,SORT_STRING);
        if(!$new){return false;}

        $required=array_values(array_unique(array_filter(array_map('sanitize_key',(array)$this->ebay_business_required_product_concept_ids()))));
        sort($required,SORT_STRING);$required_map=array_fill_keys($required,true);
        if(!$required){
            $this->ebay_run_fail('business_coverage_state_inconsistent','BUSINESS-Versorgungsmanifest fehlt bei der dynamischen Lückenprüfung.',array('missing'=>$missing,'targeted'=>$targeted));
            return true;
        }
        foreach($missing as $id){
            if(!isset($required_map[$id])){
                $this->ebay_run_fail('business_coverage_unknown_family','Unbekannte BUSINESS-Produktfamilie in der dynamischen Lückenprüfung.',array('family'=>$id));
                return true;
            }
        }

        // Monotonic proof scope: each physical family can enter this scope only
        // once per run. Therefore marketplace churn cannot create an unbounded
        // restart loop and no already-proven family is silently forgotten.
        $expanded=$targeted;foreach($missing as $id){$expanded[]=$id;}
        $expanded=array_values(array_unique($expanded));sort($expanded,SORT_STRING);
        if(count($expanded)>count($required)){
            $this->ebay_run_fail('business_coverage_state_inconsistent','BUSINESS-Lückenbeweis überschreitet das verbindliche Versorgungsmanifest.',array('targeted'=>$expanded));
            return true;
        }

        $run['gapfill']['attempts']=max(1,absint($run['gapfill']['attempts']??0))+1;
        $run['gapfill']['missing']=$expanded;
        unset($run['gapfill']['selection_proof']);
        $run['gapfill']['discovery_missing']=$new;
        $run['gapfill']['revalidation_count']=absint($run['gapfill']['revalidation_count']??0)+1;
        $run['gapfill']['last_revalidation_at']=time();
        $run['gapfill']['last_revalidation_from']=sanitize_key((string)$origin_phase);
        if(!isset($run['phase_state'])||!is_array($run['phase_state'])){$run['phase_state']=array();}
        $run['phase_state']['discovery']=array();
        $run['phase_state']['selection']=array();
        // More BUSINESS work means the previously current PRIVATE tail can age
        // again before final publication. Force one fresh PRIVATE tail after this
        // new BUSINESS proof scope completes.
        $run['private_public_revalidation']=array();
        $run['coverage']=$coverage;
        $run['phase']='gapfill_discovery';
        $run['resume_reason']='business_safe_gap_dynamic_revalidation';
        $run['no_progress_count']=0;
        $run['progress_seq']=absint($run['progress_seq']??0)+1;
        $run['last_progress_at']=time();
        $this->ebay_run_save($run);
        return true;
    }

    private function ebay_run_tick_coverage($run, $settings) {
        $candidate=is_array($run['checkpoint_candidate']??null)?$run['checkpoint_candidate']:array();
        $coverage=empty($settings['business_enabled'])?array('required'=>0,'covered'=>0,'missing'=>array(),'counts'=>array()):$this->ebay_run_public_business_coverage((array)($candidate['business_campaign_ids']??array()));
        if(!empty($coverage['error_code'])){$this->ebay_run_fail((string)$coverage['error_code'],'BUSINESS-Coverage-Gate ist technisch oder fachlich fehlgeschlagen.',array('coverage'=>$coverage));return;}
        $run=$this->ebay_run_load();$run['coverage']=$coverage;$run['progress_seq']=absint($run['progress_seq']??0)+1;$run['last_progress_at']=time();$this->ebay_run_save($run);
        if(!empty($settings['business_enabled']) && !empty($coverage['missing'])){
            $attempts=absint($run['gapfill']['attempts']??0);
            if($attempts<1){$run['gapfill']['attempts']=$attempts+1;$run['gapfill']['missing']=$coverage['missing'];$run['phase']='gapfill_discovery';$run['resume_reason']='business_coverage_missing';$this->ebay_run_save($run);return;}
            if($this->ebay_run_schedule_new_business_gap_revalidation($run,$coverage,'coverage_verify')){return;}
            $run=$this->ebay_run_load();
            $result=$this->ebay_run_business_safe_supply_gap_contract($run,$coverage);
            if(($result['status']??'')!=='pass'){
                $code=sanitize_key((string)($result['error_code']??'business_safe_gap_contract_failed'));
                $this->ebay_run_fail($code,'BUSINESS-Versorgungslücke konnte nicht als sichere externe Angebotslücke bewiesen werden.',array('gap_contract'=>$result,'coverage'=>$coverage));return;
            }
            $run=$this->ebay_run_load();$run['coverage']=(array)$result['coverage'];$run['resume_reason']='business_safe_supply_gaps_open';$this->ebay_run_save($run);
        }
        $this->ebay_run_set_phase('public_verify','');
    }

    private function ebay_run_tick_gapfill($run, $settings) {
        $missing=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($run['gapfill']['missing']??array())))));
        if(!$missing){$this->ebay_run_set_phase('public_verify','');return;}
        // Store the exact missing list in canonical state. Existing discovery
        // profile construction reads this list through ebay_business_recovery_missing_concept_ids().
        $run['coverage']['missing']=$missing;$this->ebay_run_save($run);
        $job=$this->ebay_sync_job_load();
        // A completed full-discovery substate must not suppress the one targeted
        // recovery pass. Reset only the nested discovery phase state, never the run.
        if(sanitize_key((string)($job['status']??''))==='completed' && sanitize_key((string)($job['scope']??''))!=='business_recovery'){$this->ebay_run_phase_state_save('discovery',array());$job=array();}
        $status=sanitize_key((string)($job['status']??''));
        if($status==='partial'){
            if($this->ebay_sync_job_is_resumable_partial($job) && sanitize_key((string)($job['scope']??''))==='business_recovery'){
                $author_id=absint($job['listing_author_id']??0);
                $job=$this->ebay_sync_resume_partial_job($job,$author_id);
                if(!$job){$this->ebay_run_fail('gapfill_partial_resume_failed','Persistierter Gap-Fill-Checkpoint konnte nicht fortgesetzt werden.',array('stopped_reason'=>sanitize_key((string)($job['summary']['budget']['stopped_reason']??''))));return;}
            }else{
                $reason=sanitize_key((string)($job['summary']['budget']['stopped_reason']??'gapfill_partial_unresumable'));
                $this->ebay_run_fail('gapfill_partial_unresumable','BUSINESS-Gap-Fill endete in einem nicht fortsetzbaren PARTIAL-Zustand.',array('stopped_reason'=>$reason,'scope'=>sanitize_key((string)($job['scope']??''))));return;
            }
        }elseif(!$this->ebay_sync_job_is_open($job) && $status!=='completed'){
            $start=$this->ebay_start_sync_job(false,'business_recovery','background');if(is_wp_error($start)){$this->ebay_run_fail($start->get_error_code(),$start->get_error_message());return;}
        }
        $this->run_ebay_sync_worker(true);$this->ebay_run_capture_component_state(null,array('discovery'));$job=$this->ebay_sync_job_load();$status=sanitize_key((string)($job['status']??''));
        if($status==='failed'){$this->ebay_run_fail('gapfill_discovery_failed','Gezielte BUSINESS-Gap-Fill-Discovery ist fehlgeschlagen.');return;}
        if($status==='completed'){
            // Re-run BUSINESS selection through the same run. PRIVATE is frozen
            // and must not participate in gap-fill.
            $this->ebay_run_phase_state_save('selection',array());
            $run=$this->ebay_run_load();$run['phase']='gapfill_select';$run['resume_reason']='';$this->ebay_run_save($run);
        }
    }

    private function ebay_run_tick_gapfill_select($run, $settings) {
        $selection=$this->ebay_selection_state_load();
        $expected_owner='run:'.sanitize_text_field((string)$run['run_uuid']);
        $selection_status=sanitize_key((string)($selection['status']??''));
        $is_expected_terminal=$selection_status==='complete'
            && sanitize_key((string)($selection['reason']??''))==='canonical_gapfill'
            && sanitize_key((string)($selection['selection_scope']??''))==='business'
            && sanitize_text_field((string)($selection['owner']??''))===$expected_owner;
        // The initial all-routes selection is terminal when gap-fill begins.
        // It must never be mistaken for the required targeted BUSINESS rerun.
        // Production selection state lives in its own durable option, so clearing
        // only canonical phase_state is insufficient. Request a fresh terminal-to-
        // new BUSINESS selection unless the stored state already belongs to this
        // exact canonical gap-fill run.
        if(!$this->ebay_selection_state_is_open($selection) && !$is_expected_terminal){
            $selection=$this->ebay_selection_request('canonical_gapfill',$expected_owner,true,'business');
            $this->ebay_run_capture_component_state(null,array('selection'));
        }
        if(sanitize_key((string)($selection['status']??''))==='failed'){$this->ebay_run_fail(sanitize_key((string)($selection['failure_reason']??'gapfill_selection_failed')),sanitize_text_field((string)($selection['error']??'Gap-Fill-Auswahl ist fehlgeschlagen.')));return;}
        if(sanitize_key((string)($selection['status']??''))!=='complete'){$selection=$this->ebay_selection_process_tick($settings,$selection);$this->ebay_run_capture_component_state(null,array('selection'));}
        if(sanitize_key((string)($selection['status']??''))==='complete'){
            $this->ebay_run_checkpoint_capture_selection($selection,'gapfill');
            $this->ebay_run_set_phase('coverage_verify','');
        }
    }

    private function ebay_run_tick_public_verify($run, $settings) {
        $candidate=is_array($run['checkpoint_candidate']??null)?$run['checkpoint_candidate']:array();
        $business=empty($settings['business_enabled'])?array('required'=>0,'covered'=>0,'missing'=>array(),'counts'=>array()):$this->ebay_run_public_business_coverage((array)($candidate['business_campaign_ids']??array()));
        if(!empty($business['error_code'])){$this->ebay_run_fail((string)$business['error_code'],'BUSINESS-Public-Gate ist technisch oder fachlich fehlgeschlagen.',array('business'=>$business));return;}
        if(!empty($settings['business_enabled']) && !empty($business['missing'])){
            $current=$this->ebay_run_load();
            if($this->ebay_run_schedule_new_business_gap_revalidation($current,$business,'public_verify')){return;}
            $current=$this->ebay_run_load();
            $result=$this->ebay_run_business_safe_supply_gap_contract($current,$business);
            if(($result['status']??'')!=='pass'){
                $code=sanitize_key((string)($result['error_code']??'public_business_coverage_failed'));
                $this->ebay_run_fail($code,'BUSINESS-Public-Gate konnte fehlende Familien nicht als sichere Versorgungslücken bestätigen.',array('gap_contract'=>$result,'business'=>$business));return;
            }
            $business=(array)$result['coverage'];
            $current=$this->ebay_run_load();$current['coverage']=$business;$this->ebay_run_save($current);
        }elseif(!empty($settings['business_enabled'])){
            $business['contract_status']='complete';$business['open_gap_count']=0;$business['open_gaps']=array();
        }
        $current=$this->ebay_run_load();
        if($this->ebay_run_private_public_revalidation_required($current,$settings)){
            if($this->ebay_run_begin_private_public_revalidation($current,'post_business_gapfill')){return;}
            $this->ebay_run_fail('private_public_revalidation_start_failed','PRIVATE-Endrevalidierung nach BUSINESS-Gap-Fill konnte nicht sicher gestartet werden.');return;
        }
        $private=$this->ebay_run_verify_private_public($settings,(array)($candidate['private_listing_ids']??array()));
        if(($private['status']??'')==='failed'){
            $current=$this->ebay_run_load();
            if($this->ebay_run_private_public_freshness_only_failure($private)
                && $this->ebay_run_reopen_private_after_public_freshness_churn($current,$private,'public_gate_source_stale')){return;}
            $this->ebay_run_fail((string)($private['error_code']??'private_public_gate_failed'),'PRIVATE-Public-Gate ist fehlgeschlagen.',array('invalid'=>$private['invalid']??array(),'public'=>$private['public']??0));return;
        }

        // The one-row checkpoint write is the public visibility commit. Until
        // this exact point the frontend continues to serve the previous safe set.
        $current=$this->ebay_run_load();
        $checkpoint=$this->ebay_run_commit_public_checkpoint($current,$business,$private);
        if($checkpoint===false || is_wp_error($checkpoint)){
            $this->ebay_run_fail('public_checkpoint_commit_failed','Der vollständig geprüfte neue öffentliche Checkpoint konnte nicht atomar übernommen werden.');return;
        }
        $manifest=array('business'=>$business,'private'=>$private,'verified_at'=>time(),'run_uuid'=>(string)$run['run_uuid'],'checkpoint_id'=>(string)($checkpoint['checkpoint_id']??''));
        $current=$this->ebay_run_load();
        $current['checkpoint_id']=sanitize_text_field((string)($checkpoint['checkpoint_id']??''));
        $current['checkpoint_verified_manifest']=$manifest;
        $routes=is_array($current['config_snapshot']['seller_routes']??null)?$current['config_snapshot']['seller_routes']:array();
        if(!empty($routes['business'])){$current['phase']='checkpoint_cleanup_business';$current['resume_reason']='checkpoint_committed';}
        elseif(!empty($routes['private'])){$current['phase']='checkpoint_cleanup_private';$current['resume_reason']='checkpoint_committed';}
        else{$this->ebay_run_complete($manifest);return;}
        $current['progress_seq']=absint($current['progress_seq']??0)+1;$current['last_progress_at']=time();$current['no_progress_count']=0;
        $this->ebay_run_save($current);
    }

    /** Fail closed on any cleanup-engine failure after the new public checkpoint
     * was committed. Cleanup is technical housekeeping only: the verified public
     * checkpoint remains authoritative, while the run terminates with a precise
     * route-specific error instead of drifting into the generic no-progress guard. */
    private function ebay_run_checkpoint_cleanup_fail_if_needed($plan,$route) {
        $plan=is_array($plan)?$plan:array();$route=sanitize_key((string)$route);
        $status=sanitize_key((string)($plan['status']??''));$phase=sanitize_key((string)($plan['phase']??''));
        if($status!=='failed' && $phase!=='failed'){return false;}
        $reason=sanitize_key((string)($plan['failure_reason']??''));
        if($reason===''){$reason=sanitize_key((string)($plan['error']??''));}
        $code=$route==='private'?'checkpoint_private_cleanup_failed':'checkpoint_business_cleanup_failed';
        $message=$route==='private'?'PRIVATE-Checkpoint-Bereinigung ist fehlgeschlagen.':'BUSINESS-Checkpoint-Bereinigung ist fehlgeschlagen.';
        $this->ebay_run_fail($code,$message,array('route'=>$route,'cleanup_status'=>$status,'cleanup_phase'=>$phase,'cleanup_reason'=>$reason));
        return true;
    }

    private function ebay_run_tick_checkpoint_cleanup($run,$settings,$route) {
        $route=sanitize_key((string)$route);
        $plan=is_array($run['checkpoint_cleanup_selection']??null)?$run['checkpoint_cleanup_selection']:array();
        if(!$plan){
            $manifest=is_array($run['checkpoint_verified_manifest']??null)?$run['checkpoint_verified_manifest']:array();
            $this->ebay_run_complete($manifest);return;
        }
        if($route==='business'){
            if(empty($plan['checkpoint_business_cleanup_initialized'])){$plan['business_prune_cursor']=0;$plan['checkpoint_business_cleanup_initialized']=1;unset($plan['checkpoint_business_cleanup_done']);}
            if(!method_exists($this,'ebay_selection_prune_business_batch')){$this->ebay_run_fail('checkpoint_business_cleanup_missing','BUSINESS-Checkpoint-Bereinigung fehlt.');return;}
            $this->ebay_selection_prune_business_batch($settings,$plan,50,true,false);
            $current=$this->ebay_run_load();$current['checkpoint_cleanup_selection']=$plan;$this->ebay_run_save($current);
            if($this->ebay_run_checkpoint_cleanup_fail_if_needed($plan,'business')){return;}
            if(!empty($plan['checkpoint_business_cleanup_done'])){
                $routes=is_array($current['config_snapshot']['seller_routes']??null)?$current['config_snapshot']['seller_routes']:array();
                if(!empty($routes['private'])){$this->ebay_run_set_phase('checkpoint_cleanup_private','checkpoint_committed');}
                else{$this->ebay_run_complete((array)($current['checkpoint_verified_manifest']??array()));}
            }
            return;
        }
        if($route==='private'){
            if(empty($plan['checkpoint_private_cleanup_initialized'])){$plan['private_post_cursor']=0;$plan['checkpoint_private_cleanup_initialized']=1;unset($plan['checkpoint_private_cleanup_done']);}
            if(!method_exists($this,'ebay_selection_apply_private_post_batch')){$this->ebay_run_fail('checkpoint_private_cleanup_missing','PRIVATE-Checkpoint-Bereinigung fehlt.');return;}
            $this->ebay_selection_apply_private_post_batch($settings,$plan,50,true,false);
            $current=$this->ebay_run_load();$current['checkpoint_cleanup_selection']=$plan;$this->ebay_run_save($current);
            if($this->ebay_run_checkpoint_cleanup_fail_if_needed($plan,'private')){return;}
            if(!empty($plan['checkpoint_private_cleanup_done'])){$this->ebay_run_complete((array)($current['checkpoint_verified_manifest']??array()));}
            return;
        }
        $this->ebay_run_fail('checkpoint_cleanup_route_invalid','Ungültige Checkpoint-Bereinigungsphase.');
    }


    /**
     * V6.45 hard guard for the bounded selection_prepare phase.
     *
     * The limit is derived from the durable BUSINESS manifest/batch contract and,
     * once PRIVATE preparation has initialized, from its persisted leaf/candidate
     * budget. Before PRIVATE initialization exactly one bootstrap package is
     * allowed beyond the BUSINESS budget; after that package the real PRIVATE
     * bounds must be present in durable state.
     */
    private function ebay_run_selection_prepare_tick_limit($run) {
        $run=is_array($run)?$run:array();
        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        $scope=sanitize_key((string)($selection['selection_scope']??''));
        if(!in_array($scope,array('all','private','business'),true)){$scope=$this->ebay_run_selection_scope($run);}

        $business_ticks=0;
        if($scope!=='private'){
            $target_count=count((array)($selection['business_target_concepts']??array()));
            // Before the real selector has initialized its durable target list,
            // use the immutable current production ceiling. The selector itself
            // remains authoritative and fails closed if its manifest is invalid.
            if($target_count<1){$target_count=311;}
            $business_ticks=(int)ceil($target_count/8);
        }

        $private_ticks=0;
        if($scope!=='business'){
            if(!empty($selection['prepare_private_initialized'])){
                $leaf_count=count((array)($selection['prepare_private_leaf_ids']??array()));
                $candidate_limit=absint($selection['prepare_private_candidate_limit']??0);
                if($candidate_limit<1){$candidate_limit=1000;} // legacy/test state before this durable field existed.
                // Each PRIVATE prepare loop consumes max(1, rows_read) from the
                // 100-unit tick budget. Thus rows + at most one empty unit per
                // leaf is a strict persisted upper work bound.
                $private_units=max(1,$candidate_limit+$leaf_count);
                $private_ticks=max(1,(int)ceil($private_units/100))+1;
            }else{
                // Pre-initialization/legacy state has no leaf contract yet. Use
                // the established 1,000-candidate ceiling as a conservative
                // temporary bound; the next successful real prepare tick persists
                // the exact leaf/candidate values and tightens this dynamically.
                $private_ticks=12;
            }
        }
        return max(1,$business_ticks+$private_ticks+2);
    }

    /** True when this canonical package can execute the bounded nested
     * selection prepare step. Gap-fill reuses the same production selector under
     * canonical phase `gapfill_select`, so its prepare work needs the same hard
     * termination gate as the initial `selection_prepare` phase. */
    private function ebay_run_selection_prepare_guard_active($run) {
        $run=is_array($run)?$run:array();
        $phase=sanitize_key((string)($run['phase']??''));
        if($phase==='selection_prepare'){return true;}
        if($phase!=='gapfill_select'){return false;}

        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        $status=sanitize_key((string)($selection['status']??''));
        $nested_phase=sanitize_key((string)($selection['phase']??''));
        $expected_owner='run:'.sanitize_text_field((string)($run['run_uuid']??''));
        $is_expected_terminal=$status==='complete'
            && sanitize_key((string)($selection['reason']??''))==='canonical_gapfill'
            && sanitize_key((string)($selection['selection_scope']??''))==='business'
            && $expected_owner!=='run:'
            && hash_equals($expected_owner,sanitize_text_field((string)($selection['owner']??'')));
        if($is_expected_terminal){return false;}
        if($status==='running' && $nested_phase!=='' && $nested_phase!=='prepare'){return false;}
        return true;
    }

    /** Fail closed if durable selection-prepare cursors move backwards or reset.
     * The same nested selector is used by initial selection and targeted gap-fill. */
    private function ebay_run_selection_prepare_regression($before_run,$after_run) {
        $before_run=is_array($before_run)?$before_run:array();$after_run=is_array($after_run)?$after_run:array();
        $before_phase=sanitize_key((string)($before_run['phase']??''));
        $after_phase=sanitize_key((string)($after_run['phase']??''));
        if($before_phase!==$after_phase || !in_array($before_phase,array('selection_prepare','gapfill_select'),true)){return false;}
        $b=is_array($before_run['phase_state']['selection']??null)?$before_run['phase_state']['selection']:array();
        $a=is_array($after_run['phase_state']['selection']??null)?$after_run['phase_state']['selection']:array();

        if(!empty($b['prepare_business_initialized'])){
            if(empty($a['prepare_business_initialized'])){
                return new WP_Error('selection_prepare_business_state_regressed','Persistierter BUSINESS-Prepare-Zustand wurde während eines Worker-Ticks zurückgesetzt.');
            }
            $bi=absint($b['prepare_business_index']??0);$ai=absint($a['prepare_business_index']??0);
            if($ai<$bi){
                return new WP_Error('selection_prepare_business_cursor_regressed','Persistierter BUSINESS-Prepare-Cursor ist rückwärts gelaufen.');
            }
        }

        if(!empty($b['prepare_private_initialized'])){
            if(empty($a['prepare_private_initialized'])){
                return new WP_Error('selection_prepare_private_state_regressed','Persistierter PRIVATE-Prepare-Zustand wurde während eines Worker-Ticks zurückgesetzt.');
            }
            $bli=absint($b['prepare_private_leaf_index']??0);$ali=absint($a['prepare_private_leaf_index']??0);
            if($ali<$bli){
                return new WP_Error('selection_prepare_private_cursor_regressed','Persistierter PRIVATE-Leaf-Cursor ist rückwärts gelaufen.');
            }
            $bo=(array)($b['prepare_private_leaf_offsets']??array());$ao=(array)($a['prepare_private_leaf_offsets']??array());
            foreach($bo as $leaf_id=>$offset){
                if(array_key_exists((string)$leaf_id,$ao) && absint($ao[(string)$leaf_id])<absint($offset)){
                    return new WP_Error('selection_prepare_private_offset_regressed','Persistierter PRIVATE-Leaf-Offset ist rückwärts gelaufen.');
                }
                if(absint($offset)>0 && !array_key_exists((string)$leaf_id,$ao)){
                    return new WP_Error('selection_prepare_private_offset_lost','Persistierter PRIVATE-Leaf-Offset ist während eines Worker-Ticks verschwunden.');
                }
            }
        }
        return false;
    }

    /** Candidate-local errors are durable audit data, not run stoppers. Global
     * storage/checkpoint/runtime failures never enter this list and remain
     * fail-closed through the existing canonical gates. */
    private function ebay_run_nested_skipped_item_errors($run) {
        $run=is_array($run)?$run:array();
        $selection=is_array($run['phase_state']['selection']??null)?$run['phase_state']['selection']:array();
        $business=is_array($selection['stats']['business']??null)?$selection['stats']['business']:array();
        $private=is_array($selection['stats']['private']??null)?$selection['stats']['private']:array();
        $out=array();
        foreach((array)($business['recoverable_errors']??array()) as $entry){
            if(!is_array($entry)){continue;}
            $code=sanitize_key((string)($entry['code']??''));if($code===''){continue;}
            $out[]=array('seller_type'=>'BUSINESS','item_id'=>sanitize_text_field((string)($entry['item_id']??'')),'row_id'=>absint($entry['row_id']??0),'concept'=>sanitize_key((string)($entry['concept']??'')),'code'=>$code);
        }
        $fatal_private=array('storage_unavailable','database_unavailable','checkpoint_missing','checkpoint_invalid','checkpoint_verification_failed','canonical_worker_runtime_error');
        foreach((array)($private['errors']??array()) as $entry){
            if(!is_array($entry)){continue;}
            $code=sanitize_key((string)($entry['code']??''));
            if($code===''||in_array($code,$fatal_private,true)){continue;}
            $out[]=array('seller_type'=>'PRIVATE','item_id'=>sanitize_text_field((string)($entry['item_id']??'')),'row_id'=>absint($entry['row_id']??0),'concept'=>'','code'=>$code);
        }
        return $out;
    }

    private function ebay_run_record_nested_skipped_item_errors($run) {
        $run=is_array($run)?$run:$this->ebay_run_load();
        if((string)($run['schema']??'')!=='1.0'){return $run;}
        $log=is_array($run['skipped_item_errors']??null)?$run['skipped_item_errors']:array();
        $seen=array();
        foreach($log as $entry){
            if(!is_array($entry)){continue;}
            $key=hash('sha256',wp_json_encode(array($entry['seller_type']??'',$entry['item_id']??'',absint($entry['row_id']??0),$entry['concept']??'',$entry['code']??'')));
            $seen[$key]=1;
        }
        $added=0;
        foreach($this->ebay_run_nested_skipped_item_errors($run) as $entry){
            $key=hash('sha256',wp_json_encode(array($entry['seller_type'],$entry['item_id'],$entry['row_id'],$entry['concept'],$entry['code'])));
            if(isset($seen[$key])){continue;}
            $entry['at']=time();$log[]=$entry;$seen[$key]=1;$added++;
        }
        if($added>0){
            $run['skipped_item_errors_count']=absint($run['skipped_item_errors_count']??0)+$added;
            $run['skipped_item_errors']=count($log)>500?array_slice($log,-500):$log;
            $run['last_skipped_item_error_at']=time();
            return $this->ebay_run_save($run);
        }
        return $run;
    }

    public function run_ebay_canonical_worker() {
        $run=$this->ebay_run_load();
        if(sanitize_key((string)($run['status']??''))==='paused'){
            $run=$this->ebay_run_resume_paused_if_due($run);
            if(sanitize_key((string)($run['status']??''))==='paused'){
                return array('tick_result'=>'busy','reason'=>'paused_until_resume','progress_before'=>absint($run['progress_seq']??0),'progress_after'=>absint($run['progress_seq']??0));
            }
        }
        if(!$this->ebay_run_is_open($run)){
            $status=sanitize_key((string)($run['status']??''));
            $terminal=$status==='completed'?'completed':($status==='failed'?'failed':'retryable_error');
            return array('tick_result'=>$terminal,'reason'=>$status===''?'run_not_open':$status,'progress_before'=>absint($run['progress_seq']??0),'progress_after'=>absint($run['progress_seq']??0));
        }
        $progress_before=absint($run['progress_seq']??0);
        $current_progress_contract=$this->ebay_run_progress_contract_version();

        $token=$this->ebay_run_acquire_lease($run);
        if($token===false){
            $fresh=$this->ebay_run_load();
            return array(
                'tick_result'=>'busy','reason'=>'lease_busy',
                'progress_before'=>$progress_before,'progress_after'=>absint($fresh['progress_seq']??0),
                'lease_expires_at'=>absint($fresh['lease_expires_at']??0),
            );
        }
        $run=$this->ebay_run_load();
        if(!hash_equals($token,sanitize_text_field((string)($run['owner']??'')))){
            $this->ebay_run_fail('canonical_worker_lease_acquire_lost','Der eBay-Orchestrator hat seine Lease unmittelbar nach dem Erwerb verloren.');
            $fresh=$this->ebay_run_load();
            return array('tick_result'=>'failed','reason'=>'lease_acquire_lost','progress_before'=>$progress_before,'progress_after'=>absint($fresh['progress_seq']??0));
        }
        if(!hash_equals($current_progress_contract,sanitize_text_field((string)($run['progress_contract_version']??'')))){
            $run['progress_contract_version']=$current_progress_contract;
        }

        // One bounded canonical package remains the only fach-work unit. V6.63.8
        // drives those packages through a private signed self-chain; the public
        // external endpoint is watchdog/fallback only. Lease/progress semantics
        // are unchanged and still forbid parallel fach work.
        $now=time();
        $run['last_transport_tick_at']=$now;
        $run['transport_tick_count']=absint($run['transport_tick_count']??0)+1;
        $run['worker_transport']='self_drive';
        $run['orchestrator_contract']='self_drive_v1';

        $phase=sanitize_key((string)($run['phase']??''));
        if(sanitize_key((string)($run['phase_tick_phase']??''))!==$phase){
            $run['phase_tick_phase']=$phase;$run['phase_tick_count']=0;
        }
        $run['phase_tick_count']=absint($run['phase_tick_count']??0)+1;

        if($this->ebay_run_selection_prepare_guard_active($run)){
            $limit=$this->ebay_run_selection_prepare_tick_limit($run);
            $run['selection_prepare_tick_limit']=$limit;
            if(absint($run['phase_tick_count'])>$limit){
                $this->ebay_run_save($run);
                $this->ebay_run_fail('selection_prepare_tick_limit_exceeded','Selection-Prepare hat seine aus Manifest und Batchgrenzen abgeleitete maximale Paketanzahl überschritten.',array('phase'=>$phase,'phase_tick_count'=>absint($run['phase_tick_count']),'phase_tick_limit'=>$limit));
                $fresh=$this->ebay_run_load();
                return array('tick_result'=>'failed','reason'=>'selection_prepare_tick_limit_exceeded','progress_before'=>$progress_before,'progress_after'=>absint($fresh['progress_seq']??0));
            }
        }
        $run=$this->ebay_run_save($run);
        $before_run=$run;
        $before=$this->ebay_run_progress_fingerprint($before_run);

        $this->ebay_canonical_worker_active=true;
        $this->ebay_run_settings_override=$this->ebay_run_effective_settings($run);
        try{
            $run=$this->ebay_run_load();$settings=$this->ebay_run_settings_override;$phase=sanitize_key((string)($run['phase']??''));
            if($phase==='reconcile_local'){$this->ebay_run_tick_reconcile($run,$settings);}
            elseif($phase==='refresh_remote'){$this->ebay_run_tick_remote($run,$settings);}
            elseif(in_array($phase,array('selection_prepare','business_select','business_materialize','private_select','private_materialize'),true)){$this->ebay_run_tick_selection($run,$settings);}
            elseif($phase==='coverage_verify'){$this->ebay_run_tick_coverage($run,$settings);}
            elseif($phase==='gapfill_discovery'){$this->ebay_run_tick_gapfill($run,$settings);}
            elseif($phase==='gapfill_select'){$this->ebay_run_tick_gapfill_select($run,$settings);}
            elseif($phase==='public_verify'){$this->ebay_run_tick_public_verify($run,$settings);}
            elseif($phase==='checkpoint_cleanup_business'){$this->ebay_run_tick_checkpoint_cleanup($run,$settings,'business');}
            elseif($phase==='checkpoint_cleanup_private'){$this->ebay_run_tick_checkpoint_cleanup($run,$settings,'private');}
            else{$this->ebay_run_fail('canonical_phase_unknown','Unbekannte kanonische eBay-Phase: '.$phase);}
        }catch(Throwable $e){$this->ebay_run_fail('canonical_worker_runtime_error',$e->getMessage());}
        finally{
            $this->ebay_run_settings_override=null;$this->ebay_canonical_worker_active=false;
        }

        $fresh=$this->ebay_run_load();
        $fresh=$this->ebay_run_record_nested_skipped_item_errors($fresh);
        if(!$this->ebay_run_is_open($fresh)){
            $status=sanitize_key((string)($fresh['status']??''));
            return array('tick_result'=>$status==='completed'?'completed':'failed','reason'=>$status,'progress_before'=>$progress_before,'progress_after'=>absint($fresh['progress_seq']??0));
        }

        $owner=sanitize_text_field((string)($fresh['owner']??''));
        if($owner==='' || !hash_equals($token,$owner)){
            // In the single-clock contract no other writer is allowed to steal or
            // clear the active lease. Surface this immediately instead of lying
            // to the heartbeat with another generic "running" response.
            $this->ebay_run_fail('canonical_worker_lease_lost','Der eBay-Orchestrator hat während eines Arbeitspakets seine Lease verloren.',array('phase'=>$fresh['phase']??''));
            $failed=$this->ebay_run_load();
            return array('tick_result'=>'failed','reason'=>'lease_lost','progress_before'=>$progress_before,'progress_after'=>absint($failed['progress_seq']??0));
        }

        $regression=$this->ebay_run_selection_prepare_regression($before_run,$fresh);
        if(is_wp_error($regression)){
            $this->ebay_run_fail($regression->get_error_code(),$regression->get_error_message(),array(
                'before_selection'=>(array)($before_run['phase_state']['selection']??array()),
                'after_selection'=>(array)($fresh['phase_state']['selection']??array()),
            ));
            $failed=$this->ebay_run_load();
            return array('tick_result'=>'failed','reason'=>'selection_regression','progress_before'=>$progress_before,'progress_after'=>absint($failed['progress_seq']??0));
        }

        $after=$this->ebay_run_progress_fingerprint($fresh);
        if(hash_equals($before,$after)){
            $fresh['no_progress_count']=absint($fresh['no_progress_count']??0)+1;
            $fresh=$this->ebay_run_save($fresh);
            if(absint($fresh['no_progress_count']??0)>=3){
                $this->ebay_run_fail('canonical_worker_no_progress','Drei aufeinanderfolgende Worker-Ticks ohne echten Workflow-Fortschritt.',array('phase'=>$fresh['phase']??''));
                $failed=$this->ebay_run_load();
                return array('tick_result'=>'failed','reason'=>'no_progress_limit','progress_before'=>$progress_before,'progress_after'=>absint($failed['progress_seq']??0));
            }
            $this->ebay_run_release_lease($token);
            $fresh=$this->ebay_run_load();
            return array('tick_result'=>'retryable_error','reason'=>'no_progress','progress_before'=>$progress_before,'progress_after'=>absint($fresh['progress_seq']??0));
        }

        $fresh['no_progress_count']=0;
        $fresh['last_progress_at']=time();
        $fresh['progress_seq']=absint($fresh['progress_seq']??0)+1;
        $fresh=$this->ebay_run_save($fresh);
        $this->ebay_run_release_lease($token);
        $fresh=$this->ebay_run_load();
        return array('tick_result'=>'advanced','reason'=>'progress','progress_before'=>$progress_before,'progress_after'=>absint($fresh['progress_seq']??0));
    }

}
