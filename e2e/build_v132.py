from pathlib import Path
p=Path("/tmp/candidate132/affiliate-portal-router/pferdeportal-affiliate-router.php")
s=p.read_text()
s=s.replace("Version: 6.72.131","Version: 6.72.132",1)
s=s.replace("const VERSION = '6.72.131';","const VERSION = '6.72.132';",1)
hook="        add_action('init', array($this, 'maybe_enforce_ebay_deletion_compliance'), 11);\n"
s=s.replace(hook,hook+"        add_action('init', array($this, 'maybe_aff043_automatic_state_restore'), 12);\n",1)
marker="    private function aff043_state() {"
method=r'''    public function maybe_aff043_automatic_state_restore() {
        if (method_exists($this, 'ebay_settings') && method_exists($this, 'ebay_deletion_compliance_complete') && $this->ebay_deletion_compliance_complete()) {
            $ebay = $this->ebay_settings();
            if (empty($ebay['enabled']) && (string)($ebay['environment'] ?? 'production') === 'production') {
                $access = method_exists($this, 'provider_access_state') ? $this->provider_access_state('ebay') : array();
                $message = (string)($access['message'] ?? '');
                if (strpos($message, 'Marketplace-Account-Deletion-Compliance hart deaktiviert') !== false) {
                    $ebay['enabled'] = true;
                    update_option(self::OPTION_NETWORK_EBAY, $this->ebay_normalize_settings($ebay, true), false);
                    if (method_exists($this, 'provider_set_access_state')) {
                        $this->provider_set_access_state('ebay', 'connected', 'eBay nach bereits vollstaendiger Marketplace-Account-Deletion-Compliance wieder aktiviert.');
                    }
                }
            }
        }
        $state = $this->aff043_state();
        $status = sanitize_key((string)($state['status'] ?? 'not_started'));
        if (in_array($status, array('complete','blocked','stopped'), true)) { return; }
        if ($status !== 'running') {
            $reithelme = $this->aff043_current_supply_for_key('page:reithelme');
            $stallhalfter = $this->aff043_current_supply_for_key('page:halfter-und-stricke-stallhalfter');
            $idealo = get_option(self::OPTION_NETWORK_IDEALO, array());
            $idealo = is_array($idealo) ? $idealo : array();
            $mode = $this->idealo_sanitize_output_mode($idealo['output_mode'] ?? 'ebay_only');
            $known_damage = $mode === 'idealo_only' || absint($reithelme['total'] ?? 0) < 3 || absint($stallhalfter['total'] ?? 0) < 3;
            if (!$known_damage) { return; }
            $snap = $this->aff043_snapshot();
            if (is_wp_error($snap)) {
                $this->aff043_save_state(array('schema'=>'1.0','status'=>'blocked','phase'=>'preflight','errors'=>array('snapshot'=>$snap->get_error_code()),'message'=>$snap->get_error_message(),'updated_at'=>time()));
                return;
            }
            $state = array('schema'=>'1.0','status'=>'running','phase'=>'augment','cursor'=>0,'started_at'=>time(),'started_by'=>0,'snapshot_sha256'=>$snap['sha256'],'source_sha256'=>$snap['source_sha256'],'stats'=>array(),'errors'=>array(),'automatic_start'=>1);
            $this->aff043_save_state($state);
        }
        $started = microtime(true);
        for ($i=0; $i<40 && (microtime(true)-$started)<20.0; $i++) {
            $state = $this->run_aff043_recovery_worker();
            if (sanitize_key((string)($state['status'] ?? '')) !== 'running') { break; }
        }
    }

'''
if "maybe_aff043_automatic_state_restore" not in s:
    s=s.replace(marker,method+marker,1)
else:
    # hook insertion introduces method name, so check actual declaration
    if "public function maybe_aff043_automatic_state_restore()" not in s:
        s=s.replace(marker,method+marker,1)
p.write_text(s)
r=Path("/tmp/candidate132/affiliate-portal-router/readme.txt")
rs=r.read_text().replace("V6.72.131 ","V6.72.132 ",1)
r.write_text(rs)
