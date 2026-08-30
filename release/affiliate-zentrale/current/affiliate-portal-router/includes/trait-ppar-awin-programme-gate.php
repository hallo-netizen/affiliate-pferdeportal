<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Awin-Eingangsweiche.
 *
 * Grundsatz: Positivliste, fail-closed. Ein synchronisiertes Awin-Programm darf
 * erst dann in Automatisierung, Werbemittelplanung oder öffentliche Ausgabe,
 * wenn es ausdrücklich für genau dieses Portal freigegeben wurde. Jede fehlende,
 * fremde oder negative Entscheidung blockiert den Partner.
 */
trait PPAR_Awin_Programme_Gate_Trait {
    private function awin_programme_gate_records() {
        $stored = get_option(self::OPTION_AWIN_PROGRAMME_GATE, array());
        return is_array($stored) ? $stored : array();
    }

    private function awin_programme_gate_statuses() {
        return array(
            'pending' => 'Nicht freigegeben',
            'allow_local' => 'Für dieses Portal aktiv',
            'other_portal' => 'Anderem Portal zugeordnet',
            'test_blocked' => 'Testpartner sperren',
            'excluded' => 'Dauerhaft ausschließen',
        );
    }

    private function awin_programme_gate_entry($advertiser_id) {
        $advertiser_id = absint($advertiser_id);
        $records = $this->awin_programme_gate_records();
        $row = $advertiser_id > 0 && is_array($records[(string) $advertiser_id] ?? null)
            ? $records[(string) $advertiser_id]
            : array();
        $status = sanitize_key((string) ($row['status'] ?? 'pending'));
        if (!array_key_exists($status, $this->awin_programme_gate_statuses())) {
            $status = 'pending';
        }
        return array(
            'advertiser_id' => $advertiser_id,
            'status' => $status,
            'portal_key' => sanitize_key((string) ($row['portal_key'] ?? '')),
            'programme_name' => sanitize_text_field((string) ($row['programme_name'] ?? '')),
            'updated_at' => absint($row['updated_at'] ?? 0),
            'updated_by' => absint($row['updated_by'] ?? 0),
        );
    }

    private function awin_programme_gate_current_joined($advertiser_id) {
        $advertiser_id = absint($advertiser_id);
        if ($advertiser_id <= 0) {
            return false;
        }
        $programmes = get_option(self::OPTION_NETWORK_AWIN_PROGRAMMES, array());
        foreach ((array) $programmes as $programme) {
            if (!is_array($programme) || absint($programme['id'] ?? 0) !== $advertiser_id) {
                continue;
            }
            return sanitize_key((string) ($programme['relationship'] ?? 'joined')) === 'joined';
        }
        return false;
    }

    private function awin_programme_gate_validate($advertiser_id, $portal_key = '') {
        $advertiser_id = absint($advertiser_id);
        if ($advertiser_id <= 0) {
            return new WP_Error('awin_partner_id_missing', 'Awin-Advertiser-ID fehlt; Partner bleibt gesperrt.');
        }
        $portal_key = sanitize_key((string) $portal_key);
        if ($portal_key === '' && method_exists($this, 'output_local_portal_key')) {
            $portal_key = sanitize_key((string) $this->output_local_portal_key());
        }
        if ($portal_key === '') {
            return new WP_Error('awin_partner_portal_missing', 'Portal-ID fehlt; Awin-Partner bleibt gesperrt.');
        }
        $entry = $this->awin_programme_gate_entry($advertiser_id);
        if ($entry['status'] !== 'allow_local') {
            $messages = array(
                'pending' => 'Awin-Partner ist nicht ausdrücklich freigegeben.',
                'other_portal' => 'Awin-Partner ist einem anderen Portal zugeordnet.',
                'test_blocked' => 'Awin-Partner ist als Testpartner gesperrt.',
                'excluded' => 'Awin-Partner ist dauerhaft ausgeschlossen.',
            );
            $codes = array(
                'pending' => 'awin_partner_not_approved',
                'other_portal' => 'awin_partner_other_portal',
                'test_blocked' => 'awin_partner_test_blocked',
                'excluded' => 'awin_partner_excluded',
            );
            return new WP_Error(
                $codes[$entry['status']] ?? 'awin_partner_not_approved',
                $messages[$entry['status']] ?? 'Awin-Partner ist nicht freigegeben.'
            );
        }
        if ($entry['portal_key'] === '' || !hash_equals($entry['portal_key'], $portal_key)) {
            return new WP_Error('awin_partner_portal_mismatch', 'Awin-Partner ist nicht für dieses Portal freigegeben.');
        }
        if (!$this->awin_programme_gate_current_joined($advertiser_id)) {
            return new WP_Error('awin_partner_not_joined_current', 'Awin-Programm ist in der aktuellen Programmliste nicht als joined bestätigt.');
        }
        return true;
    }

    private function awin_programme_gate_is_allowed($advertiser_id, $portal_key = '') {
        return !is_wp_error($this->awin_programme_gate_validate($advertiser_id, $portal_key));
    }

    /**
     * Sperrt vorhandene Folgeobjekte sofort, wenn ein Partner nicht mehr erlaubt
     * ist. Eine spätere Freigabe reaktiviert bewusst nichts automatisch.
     */
    private function awin_programme_gate_deactivate_partner($advertiser_id, $reason) {
        $advertiser_id = absint($advertiser_id);
        if ($advertiser_id <= 0) {
            return;
        }
        $reason = sanitize_text_field((string) $reason);
        global $wpdb;

        if (method_exists($this, 'automation_jobs_table')) {
            $table = $this->automation_jobs_table();
            $wpdb->query($wpdb->prepare(
                "UPDATE {$table} SET status='failed', lock_token='', lock_expires_at=0, message=%s, updated_at=%d, finished_at=%d WHERE provider='awin' AND partner_external_id=%s AND status IN ('queued','running','retry')",
                $reason,
                time(),
                time(),
                (string) $advertiser_id
            ));
        }

        if (method_exists($this, 'creative_library_table')) {
            $table = $this->creative_library_table();
            $wpdb->query($wpdb->prepare(
                "UPDATE {$table} SET selected=0, availability_state='inactive_partner_gate' WHERE provider='awin' AND partner_external_id=%s",
                (string) $advertiser_id
            ));
        }

        if (method_exists($this, 'output_objects_table') && method_exists($this, 'output_deactivate_materialized_object')) {
            $table = $this->output_objects_table();
            $rows = $wpdb->get_results($wpdb->prepare(
                "SELECT * FROM {$table} WHERE provider='awin' AND partner_external_id=%s AND status NOT IN ('blocked_partner_gate','superseded')",
                (string) $advertiser_id
            ), ARRAY_A);
            foreach ((array) $rows as $row) {
                $this->output_deactivate_materialized_object($row, $reason);
                $wpdb->update($table, array(
                    'status' => 'blocked_partner_gate',
                    'decision_source' => 'partner_allowlist',
                    'decision_reason' => $reason,
                    'updated_at' => time(),
                ), array('id' => absint($row['id'] ?? 0)));
            }
        }
    }

    public function handle_awin_programme_gate_save() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_save_awin_programme_gate', 'ppar_awin_gate_nonce');
        $posted = isset($_POST['ppar_awin_gate']) && is_array($_POST['ppar_awin_gate'])
            ? wp_unslash($_POST['ppar_awin_gate'])
            : array();
        $joined = method_exists($this, 'partner_intake_joined_awin_programmes')
            ? $this->partner_intake_joined_awin_programmes()
            : array();
        $records = $this->awin_programme_gate_records();
        $allowed_statuses = array_keys($this->awin_programme_gate_statuses());
        $local_portal_key = method_exists($this, 'output_local_portal_key')
            ? sanitize_key((string) $this->output_local_portal_key())
            : '';
        $active = 0;
        foreach ((array) $joined as $advertiser_id => $programme_name) {
            $advertiser_id = absint($advertiser_id);
            if ($advertiser_id <= 0) {
                continue;
            }
            $status = sanitize_key((string) ($posted[(string) $advertiser_id] ?? 'pending'));
            if (!in_array($status, $allowed_statuses, true)) {
                $status = 'pending';
            }
            $portal_key = $status === 'allow_local' ? $local_portal_key : '';
            $records[(string) $advertiser_id] = array(
                'status' => $status,
                'portal_key' => $portal_key,
                'programme_name' => sanitize_text_field((string) $programme_name),
                'updated_at' => time(),
                'updated_by' => function_exists('get_current_user_id') ? absint(get_current_user_id()) : 0,
            );
            if (method_exists($this, 'control_set_decision') && $local_portal_key !== '') {
                $control_status = $status === 'allow_local' ? 'approved' : ($status === 'pending' ? 'review' : 'veto');
                $control_reason = 'Awin-Eingangsweiche: ' . (string) ($this->awin_programme_gate_statuses()[$status] ?? 'Nicht freigegeben') . '.';
                $this->control_set_decision($local_portal_key, 'partner', 'awin:' . $advertiser_id, $control_status, $control_reason, array('provider'=>'awin','partner_external_id'=>(string) $advertiser_id), 'partner_decision');
            }
            if ($status === 'allow_local' && $portal_key !== '') {
                $active++;
            } else {
                $label = $this->awin_programme_gate_statuses()[$status] ?? 'Nicht freigegeben';
                $this->awin_programme_gate_deactivate_partner($advertiser_id, 'Awin-Eingangsweiche: ' . $label . '.');
            }
        }
        update_option(self::OPTION_AWIN_PROGRAMME_GATE, $records, false);
        wp_safe_redirect(add_query_arg(array(
            'page' => 'affiliate-portal-networks',
            'ppar_awin_gate' => 'saved',
            'ppar_awin_gate_active' => $active,
        ), admin_url('admin.php')));
        exit;
    }

    private function render_awin_programme_gate_section($awin_programmes) {
        $joined = array();
        foreach ((array) $awin_programmes as $programme) {
            if (!is_array($programme)) {
                continue;
            }
            $id = absint($programme['id'] ?? 0);
            $name = sanitize_text_field((string) ($programme['name'] ?? ''));
            $relationship = sanitize_key((string) ($programme['relationship'] ?? 'joined'));
            if ($id > 0 && $name !== '' && $relationship === 'joined') {
                $joined[$id] = $name;
            }
        }
        asort($joined, SORT_NATURAL | SORT_FLAG_CASE);
        $statuses = $this->awin_programme_gate_statuses();
        $portal_label = get_bloginfo('name') ?: 'dieses Portal';
        ?>
        <section class="ppar-v240-card" style="margin-top:20px">
            <h2>Awin-Partnerfreigabe (Eingangsweiche)</h2>
            <p><strong>Positivliste:</strong> Nur Partner mit der Auswahl „Für dieses Portal aktiv“ dürfen Angebote, Produktfeeds oder Werbemittel automatisiert weiterverarbeiten. Alle neuen Partner stehen zunächst auf „Nicht freigegeben“.</p>
            <?php if (sanitize_key((string) ($_GET['ppar_awin_gate'] ?? '')) === 'saved') : ?>
                <div class="notice notice-success inline"><p>Awin-Partnerfreigaben gespeichert. Für <?php echo absint($_GET['ppar_awin_gate_active'] ?? 0); ?> Partner ist <?php echo esc_html($portal_label); ?> freigegeben.</p></div>
            <?php endif; ?>
            <?php if (!$joined) : ?>
                <p>Keine aktuell verbundenen Awin-Programme vorhanden. Zuerst „Speichern &amp; synchronisieren“ ausführen.</p>
            <?php else : ?>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                    <input type="hidden" name="action" value="ppar_save_awin_programme_gate">
                    <?php wp_nonce_field('ppar_save_awin_programme_gate', 'ppar_awin_gate_nonce'); ?>
                    <table class="widefat striped">
                        <thead><tr><th>Partner</th><th>Advertiser-ID</th><th>Freigabe</th><th>Aktueller Portalstatus</th></tr></thead>
                        <tbody>
                        <?php foreach ($joined as $id => $name) : $entry = $this->awin_programme_gate_entry($id); ?>
                            <tr>
                                <td><strong><?php echo esc_html($name); ?></strong></td>
                                <td><?php echo absint($id); ?></td>
                                <td><select name="ppar_awin_gate[<?php echo absint($id); ?>]">
                                    <?php foreach ($statuses as $status => $label) : ?><option value="<?php echo esc_attr($status); ?>" <?php selected($entry['status'], $status); ?>><?php echo esc_html($label); ?></option><?php endforeach; ?>
                                </select></td>
                                <td><?php echo $entry['status'] === 'allow_local' && $entry['portal_key'] !== ''
                                    ? '<strong style="color:#006b1b">' . esc_html($portal_label) . '</strong>'
                                    : esc_html($statuses[$entry['status']] ?? $statuses['pending']); ?></td>
                            </tr>
                        <?php endforeach; ?>
                        </tbody>
                    </table>
                    <?php submit_button('Partnerfreigaben speichern'); ?>
                </form>
            <?php endif; ?>
        </section>
        <?php
    }
}
