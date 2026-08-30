<?php
if (!defined('ABSPATH')) { exit; }

require_once __DIR__ . '/class-ppar-partner-analytics.php';
require_once __DIR__ . '/class-ppar-deal-radar.php';

/**
 * Bounded housekeeping for derived/cache/history data only.
 * Never removes current publication, manual veto/approval, active provider data,
 * canonical run state or current source facts.
 */
trait PPAR_Housekeeping_Trait {
    /**
     * Compatibility bridge for the automation suite. V6.63.8 calls these two
     * creative-library helpers, while the canonical implementations live in the
     * output-object trait as output_text()/output_tokens(). Keep one normalization
     * implementation and delegate instead of duplicating the algorithm.
     */
    private function creative_library_text($value) {
        return $this->output_text($value);
    }

    private function creative_library_tokens($value) {
        return $this->output_tokens($value);
    }

    private function housekeeping_state_defaults() {
        return array(
            'contract'=>'1.0','status'=>'never','started_at'=>0,'finished_at'=>0,
            'db_deleted'=>0,'db_compacted'=>0,'files_deleted'=>0,'bytes_deleted'=>0,
            'last_error'=>'',
        );
    }

    public function ensure_housekeeping_schedule() {
        if (!function_exists('wp_next_scheduled') || !function_exists('wp_schedule_event')) { return false; }
        if (!wp_next_scheduled(self::HOUSEKEEPING_CRON_HOOK)) {
            wp_schedule_event(time() + HOUR_IN_SECONDS, 'daily', self::HOUSEKEEPING_CRON_HOOK);
        }
        return true;
    }

    private function housekeeping_is_busy() {
        if (method_exists($this, 'ebay_run_load') && method_exists($this, 'ebay_run_is_open')) {
            $run = $this->ebay_run_load();
            if ($this->ebay_run_is_open($run)) { return true; }
        }
        return false;
    }

    private function housekeeping_delete_query($sql) {
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb, 'query')) { return 0; }
        $changed = $wpdb->query($sql);
        return $changed === false ? 0 : max(0, (int)$changed);
    }

    private function housekeeping_db_pass() {
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb, 'prepare') || !method_exists($wpdb, 'query')) {
            return array('deleted'=>0,'compacted'=>0);
        }
        $now = time();
        $history_cutoff = $now - 90 * DAY_IN_SECONDS;
        $derived_cutoff = $now - 180 * DAY_IN_SECONDS;
        $audit_cutoff = $now - 365 * DAY_IN_SECONDS;
        $deleted = 0; $compacted = 0;

        // Histories are terminal-only and bounded. Open/retry/running rows survive.
        if (method_exists($this, 'network_sync_table')) {
            $runs = $this->network_sync_table('runs');
            // Sync history is terminal by construction once finished_at is set. Keep
            // product/source rows intact: idealo/Awin/ADCELL may still need those
            // normalized facts for deterministic rematerialization, ranking or audit.
            // Housekeeping must never shrink the available result set.
            $deleted += $this->housekeeping_delete_query($wpdb->prepare(
                "DELETE FROM {$runs} WHERE status IN ('success','failed') AND finished_at>0 AND finished_at<%d ORDER BY id ASC LIMIT 500", $history_cutoff
            ));
        }

        if (method_exists($this, 'automation_jobs_table') && method_exists($this, 'automation_runs_table')) {
            $jobs = $this->automation_jobs_table();
            $runs = $this->automation_runs_table();
            $deleted += $this->housekeeping_delete_query($wpdb->prepare(
                "DELETE FROM {$jobs} WHERE status IN ('completed','failed','cancelled') AND finished_at>0 AND finished_at<%d ORDER BY id ASC LIMIT 500", $history_cutoff
            ));
            $deleted += $this->housekeeping_delete_query($wpdb->prepare(
                "DELETE FROM {$runs} WHERE id IN (SELECT id FROM (SELECT r.id FROM {$runs} r LEFT JOIN {$jobs} j ON j.run_uuid=r.run_uuid WHERE j.id IS NULL AND r.status IN ('completed','failed','cancelled') AND r.finished_at>0 AND r.finished_at<%d ORDER BY r.id ASC LIMIT 500) hk_runs)", $history_cutoff
            ));
        }

        if (method_exists($this, 'control_audit_table')) {
            $audit = $this->control_audit_table();
            $deleted += $this->housekeeping_delete_query($wpdb->prepare(
                "DELETE FROM {$audit} WHERE created_at>0 AND created_at<%d ORDER BY id ASC LIMIT 500", $audit_cutoff
            ));
        }

        // Old ended eBay facts remain as identity/tombstone rows, but their large
        // raw payload is compacted. Public/listing-linked rows are never touched.
        if (method_exists($this, 'ebay_items_table')) {
            $table = $this->ebay_items_table();
            $marker = wp_json_encode(array('_housekeeping'=>'ended_source_compacted_v1'));
            $changed = $wpdb->query($wpdb->prepare(
                "UPDATE {$table} SET source_payload=%s, short_description='' WHERE source_state='ended' AND listing_post_id=0 AND output_state IN ('none','purged_ended') AND updated_at>0 AND updated_at<%d AND source_payload<>%s LIMIT 250",
                $marker, $derived_cutoff, $marker
            ));
            if ($changed !== false) { $compacted += max(0, (int)$changed); }
        }

        // Stale, unselected, unreviewed creatives may keep their identity row but
        // not an indefinitely large provider payload. Referenced outputs and manual
        // approvals/vetos are hard exclusions.
        if (method_exists($this, 'creative_library_table') && method_exists($this, 'output_objects_table')) {
            $creative = $this->creative_library_table();
            $output = $this->output_objects_table();
            $marker = wp_json_encode(array('_housekeeping'=>'stale_creative_compacted_v1'));
            $changed = $wpdb->query($wpdb->prepare(
                "UPDATE {$creative} SET payload=%s WHERE id IN (SELECT id FROM (SELECT c.id FROM {$creative} c LEFT JOIN {$output} o ON o.creative_identity_hash=c.identity_hash WHERE o.id IS NULL AND c.selected=0 AND c.availability_state<>'active' AND c.review_status NOT IN ('approved','rejected') AND c.content_scope<>'other' AND c.last_seen>0 AND c.last_seen<%d AND c.payload<>%s ORDER BY c.id ASC LIMIT 250) hk_creatives)",
                $marker, $derived_cutoff, $marker
            ));
            if ($changed !== false) { $compacted += max(0, (int)$changed); }
        }
        return array('deleted'=>$deleted,'compacted'=>$compacted);
    }

    private function housekeeping_cache_file_referenced($basename) {
        global $wpdb;
        $basename = sanitize_file_name((string)$basename);
        if ($basename === '' || !is_object($wpdb) || !method_exists($wpdb, 'prepare') || !method_exists($wpdb, 'get_var')) { return true; }
        $like = '%' . (method_exists($wpdb, 'esc_like') ? $wpdb->esc_like($basename) : $basename) . '%';
        $checks = array();
        if (!empty($wpdb->postmeta)) { $checks[] = "SELECT 1 FROM {$wpdb->postmeta} WHERE meta_value LIKE %s LIMIT 1"; }
        if (!empty($wpdb->posts)) { $checks[] = "SELECT 1 FROM {$wpdb->posts} WHERE post_content LIKE %s OR post_excerpt LIKE %s LIMIT 1"; }
        if (!empty($wpdb->options)) { $checks[] = "SELECT 1 FROM {$wpdb->options} WHERE option_value LIKE %s LIMIT 1"; }
        foreach ($checks as $sql) {
            $args = substr_count($sql, '%s') === 2 ? array($like,$like) : array($like);
            $prepared = call_user_func_array(array($wpdb,'prepare'), array_merge(array($sql), $args));
            if ($wpdb->get_var($prepared)) { return true; }
        }
        $table_checks = array();
        if (method_exists($this, 'creative_library_table')) { $table_checks[] = array($this->creative_library_table(),'image_url'); }
        if (method_exists($this, 'output_objects_table')) { $table_checks[] = array($this->output_objects_table(),'image_url'); }
        if (method_exists($this, 'network_sync_table')) { $table_checks[] = array($this->network_sync_table('products'),'image_url'); }
        if (method_exists($this, 'ebay_items_table')) { $table_checks[] = array($this->ebay_items_table(),'image_url'); }
        foreach ($table_checks as $pair) {
            $sql = $wpdb->prepare("SELECT 1 FROM {$pair[0]} WHERE {$pair[1]} LIKE %s LIMIT 1", $like);
            if ($wpdb->get_var($sql)) { return true; }
        }
        return false;
    }

    private function housekeeping_disk_pass() {
        if (!function_exists('wp_upload_dir')) { return array('deleted'=>0,'bytes'=>0); }
        $uploads = wp_upload_dir(null, false);
        if (!is_array($uploads) || !empty($uploads['error']) || empty($uploads['basedir'])) { return array('deleted'=>0,'bytes'=>0); }
        $dir = rtrim((string)$uploads['basedir'], '/\\') . '/ppar-affiliate-product-images';
        if (!is_dir($dir) || !is_readable($dir)) { return array('deleted'=>0,'bytes'=>0); }
        $now=time();$deleted=0;$bytes=0;$seen=0;
        foreach ((array)scandir($dir) as $name) {
            if ($name==='.' || $name==='..') { continue; }
            if (++$seen > 200) { break; }
            if (!preg_match('/^(?:ebay-|idealo-).+\.(?:jpg|jpeg|png|webp|gif)(?:\.tmp-[a-z0-9]+)?$/i', $name)) { continue; }
            $path=$dir.'/'.$name; if (!is_file($path)) { continue; }
            $mtime=@filemtime($path); $size=max(0,(int)@filesize($path));
            $is_tmp=strpos($name,'.tmp-')!==false;
            if ($is_tmp) {
                if ($mtime!==false && $mtime > $now-DAY_IN_SECONDS) { continue; }
            } else {
                if ($mtime!==false && $mtime > $now-30*DAY_IN_SECONDS) { continue; }
                if ($this->housekeeping_cache_file_referenced($name)) { continue; }
            }
            if (@unlink($path)) { $deleted++;$bytes+=$size; }
        }
        return array('deleted'=>$deleted,'bytes'=>$bytes);
    }

    public function run_housekeeping() {
        $state = $this->housekeeping_state_defaults();
        $state['started_at']=time();
        if ($this->housekeeping_is_busy()) {
            $state['status']='deferred_busy';$state['finished_at']=time();
            update_option(self::OPTION_HOUSEKEEPING_STATE,$state,false);
            return $state;
        }
        try {
            $db=$this->housekeeping_db_pass();
            $disk=$this->housekeeping_disk_pass();
            $state['db_deleted']=absint($db['deleted']??0);
            $state['db_compacted']=absint($db['compacted']??0);
            $state['files_deleted']=absint($disk['deleted']??0);
            $state['bytes_deleted']=absint($disk['bytes']??0);
            $state['status']='complete';
        } catch (Throwable $e) {
            $state['status']='failed';$state['last_error']=sanitize_text_field($e->getMessage());
        }
        $state['finished_at']=time();
        update_option(self::OPTION_HOUSEKEEPING_STATE,$state,false);
        return $state;
    }
}

PPAR_Partner_Analytics_Admin::bootstrap();
PPAR_Deal_Radar::bootstrap();
