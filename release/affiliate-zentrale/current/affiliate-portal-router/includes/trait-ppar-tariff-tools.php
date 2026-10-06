<?php
if (!defined('ABSPATH')) { exit; }

trait PPAR_Tariff_Tools_Trait {
    private $tariff_tools_request_cache = null;

    private function tariff_tools_option_name() {
        return 'ppar_tariff_tools_v1';
    }

    public function tariff_tools_register_hooks() {
        add_filter('ppar_affiliate_tariff_placeholder_registry', array($this, 'tariff_tools_writer_registry'), 10, 1);
        if (is_admin()) {
            add_action('admin_post_ppar_tariff_tool_save', array($this, 'handle_tariff_tool_save'));
            add_action('admin_post_ppar_tariff_tool_delete', array($this, 'handle_tariff_tool_delete'));
        }
    }

    private function tariff_tools_normalize($raw) {
        $out = array();
        foreach ((array)$raw as $key => $tool) {
            if (!is_array($tool)) { continue; }
            $id = sanitize_key((string)($tool['id'] ?? $key));
            if ($id === '') { continue; }
            $name = sanitize_text_field((string)($tool['name'] ?? $id));
            $html = isset($tool['html']) && is_string($tool['html']) ? $tool['html'] : '';
            $out[$id] = array(
                'id' => $id,
                'name' => $name !== '' ? $name : $id,
                'html' => $html,
                'active' => !empty($tool['active']) ? 1 : 0,
                'created_at' => absint($tool['created_at'] ?? 0),
                'updated_at' => absint($tool['updated_at'] ?? 0),
            );
        }
        uasort($out, static function($a, $b) {
            return strnatcasecmp((string)$a['name'], (string)$b['name']);
        });
        return $out;
    }

    private function tariff_tools_all($force = false) {
        if ($force || $this->tariff_tools_request_cache === null) {
            $this->tariff_tools_request_cache = $this->tariff_tools_normalize(
                get_option($this->tariff_tools_option_name(), array())
            );
        }
        return $this->tariff_tools_request_cache;
    }

    private function tariff_tools_store_all($tools) {
        $normalized = $this->tariff_tools_normalize($tools);
        $option = $this->tariff_tools_option_name();

        // KISS: eine kleine Option fuer alle Rechner, bewusst NICHT autoload.
        // Normale Seiten ohne Platzhalter laden sie dadurch ueberhaupt nicht.
        $exists = get_option($option, null);
        if ($exists === null) {
            add_option($option, $normalized, '', 'no');
        } else {
            update_option($option, $normalized, false);
        }
        $this->tariff_tools_request_cache = $normalized;
        return $normalized;
    }

    private function tariff_tool_unique_id($name, $tools) {
        $base = sanitize_title(remove_accents((string)$name));
        $base = sanitize_key($base);
        if ($base === '') { $base = 'rechner'; }
        $id = $base;
        $n = 2;
        while (isset($tools[$id])) {
            $id = $base . '-' . $n;
            $n++;
        }
        return $id;
    }

    private function tariff_tool_placeholder($id) {
        $id = sanitize_key((string)$id);
        return $id === '' ? '' : '[affiliate_rechner id="' . $id . '"]';
    }

    public function tariff_tools_writer_registry($registry = array()) {
        $registry = is_array($registry) ? $registry : array();
        foreach ($this->tariff_tools_all() as $id => $tool) {
            if (empty($tool['active']) || trim((string)$tool['html']) === '') { continue; }
            $registry[$id] = array(
                'id' => $id,
                'name' => (string)$tool['name'],
                'placeholder' => $this->tariff_tool_placeholder($id),
            );
        }
        return $registry;
    }

    public function shortcode_tariff_tool($atts = array()) {
        $atts = shortcode_atts(array('id' => ''), (array)$atts, 'affiliate_rechner');
        $id = sanitize_key((string)($atts['id'] ?? ''));
        if ($id === '') { return ''; }

        $tools = $this->tariff_tools_all();
        if (empty($tools[$id]) || empty($tools[$id]['active'])) { return ''; }
        $html = (string)($tools[$id]['html'] ?? '');
        return trim($html) === '' ? '' : $html;
    }

    private function tariff_tool_redirect($args = array()) {
        $args = array_merge(array('page' => 'affiliate-portal-tariff-tools'), (array)$args);
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }

    public function handle_tariff_tool_save() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_tariff_tool_save', 'ppar_tariff_tool_nonce');

        $tools = $this->tariff_tools_all();
        $existing_id = sanitize_key((string)wp_unslash($_POST['tool_id'] ?? ''));
        $name = sanitize_text_field((string)wp_unslash($_POST['tool_name'] ?? ''));
        $html = trim((string)wp_unslash($_POST['tool_html'] ?? ''));
        $active = !empty($_POST['tool_active']) ? 1 : 0;

        if ($name === '') {
            $this->tariff_tool_redirect(array('ppar_tariff_error' => rawurlencode('Rechnername fehlt.')));
        }
        if ($html === '') {
            $this->tariff_tool_redirect(array('ppar_tariff_error' => rawurlencode('HTML-Code fehlt.')));
        }
        if (strlen($html) > 500000) {
            $this->tariff_tool_redirect(array('ppar_tariff_error' => rawurlencode('HTML-Code ist zu groß.')));
        }

        if ($existing_id !== '' && isset($tools[$existing_id])) {
            $id = $existing_id;
            $created_at = absint($tools[$id]['created_at'] ?? time());
        } else {
            $id = $this->tariff_tool_unique_id($name, $tools);
            $created_at = time();
        }

        $tools[$id] = array(
            'id' => $id,
            'name' => $name,
            // HTML/JS stammt aus einer bewusst vom Administrator gepflegten
            // Affiliate-Quelle. Es wird nicht in Artikel kopiert oder dort editiert.
            'html' => $html,
            'active' => $active,
            'created_at' => $created_at,
            'updated_at' => time(),
        );
        $this->tariff_tools_store_all($tools);
        $this->tariff_tool_redirect(array(
            'ppar_tariff_saved' => '1',
            'tool_id' => $id,
        ));
    }

    public function handle_tariff_tool_delete() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_tariff_tool_delete', 'ppar_tariff_tool_nonce');

        $id = sanitize_key((string)wp_unslash($_POST['tool_id'] ?? ''));
        $tools = $this->tariff_tools_all();
        if ($id !== '' && isset($tools[$id])) {
            unset($tools[$id]);
            $this->tariff_tools_store_all($tools);
        }
        $this->tariff_tool_redirect(array('ppar_tariff_deleted' => '1'));
    }

    public function render_tariff_tools_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }

        $tools = $this->tariff_tools_all();
        $edit_id = sanitize_key((string)wp_unslash($_GET['edit'] ?? ''));
        $edit = ($edit_id !== '' && isset($tools[$edit_id])) ? $tools[$edit_id] : null;
        $saved_id = sanitize_key((string)wp_unslash($_GET['tool_id'] ?? ''));

        if (!empty($_GET['ppar_tariff_saved'])) {
            echo '<div class="notice notice-success is-dismissible"><p>Tarifrechner gespeichert'
                . ($saved_id !== '' ? ': <code>' . esc_html($this->tariff_tool_placeholder($saved_id)) . '</code>' : '')
                . '.</p></div>';
        }
        if (!empty($_GET['ppar_tariff_deleted'])) {
            echo '<div class="notice notice-success is-dismissible"><p>Tarifrechner gelöscht.</p></div>';
        }
        if (!empty($_GET['ppar_tariff_error'])) {
            echo '<div class="notice notice-error"><p>' . esc_html(rawurldecode((string)$_GET['ppar_tariff_error'])) . '</p></div>';
        }

        $writer_lines = array();
        foreach ($this->tariff_tools_writer_registry(array()) as $row) {
            $writer_lines[] = $row['name'] . ': ' . $row['placeholder'];
        }
        ?>
        <div class="wrap">
            <h1>Tarifrechner</h1>
            <p><strong>KISS:</strong> Rechnercode liegt nur hier zentral. Artikel enthalten ausschließlich den stabilen Platzhalter. Ändern oder deaktivieren Sie einen Rechner hier, wirkt das automatisch auf alle Artikel.</p>

            <h2><?php echo $edit ? 'Tarifrechner bearbeiten' : 'Tarifrechner anlegen'; ?></h2>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                <input type="hidden" name="action" value="ppar_tariff_tool_save">
                <?php wp_nonce_field('ppar_tariff_tool_save', 'ppar_tariff_tool_nonce'); ?>
                <?php if ($edit): ?>
                    <input type="hidden" name="tool_id" value="<?php echo esc_attr($edit_id); ?>">
                    <p><strong>Stabiler Platzhalter:</strong> <code><?php echo esc_html($this->tariff_tool_placeholder($edit_id)); ?></code></p>
                <?php endif; ?>
                <table class="form-table" role="presentation">
                    <tr>
                        <th scope="row"><label for="ppar-tool-name">Rechnername / Typ</label></th>
                        <td>
                            <input id="ppar-tool-name" name="tool_name" class="regular-text" required value="<?php echo esc_attr($edit ? (string)$edit['name'] : ''); ?>" placeholder="z. B. Kredit oder Pferdehaftpflicht">
                            <p class="description">Beim ersten Speichern erzeugt das Plugin daraus automatisch einen dauerhaften Platzhalter.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="ppar-tool-html">HTML-Code</label></th>
                        <td>
                            <textarea id="ppar-tool-html" name="tool_html" rows="14" class="large-text code" required><?php echo esc_textarea($edit ? (string)$edit['html'] : ''); ?></textarea>
                            <p class="description">Nur vertrauenswürdigen Rechner-/Widget-Code des Affiliate-Partners einfügen. Der Code wird niemals in die Artikel kopiert.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Status</th>
                        <td><label><input type="checkbox" name="tool_active" value="1" <?php checked($edit ? !empty($edit['active']) : true); ?>> aktiv</label></td>
                    </tr>
                </table>
                <?php submit_button($edit ? 'Tarifrechner speichern' : 'Tarifrechner anlegen'); ?>
            </form>

            <hr>
            <h2>Platzhalter für den Schreiber</h2>
            <p>Diese Liste enthält nur aktive Rechner. Der Schreiber setzt ausschließlich den passenden Platzhalter an die gewünschte Stelle.</p>
            <textarea id="ppar-tariff-writer-list" class="large-text code" rows="<?php echo max(3, min(12, count($writer_lines) + 1)); ?>" readonly><?php echo esc_textarea(implode("\n", $writer_lines)); ?></textarea>
            <p><button type="button" class="button" onclick="navigator.clipboard && navigator.clipboard.writeText(document.getElementById('ppar-tariff-writer-list').value);">Liste kopieren</button></p>

            <h2>Gespeicherte Tarifrechner</h2>
            <table class="widefat striped">
                <thead><tr><th>Rechner</th><th>Status</th><th>Platzhalter</th><th>Aktion</th></tr></thead>
                <tbody>
                <?php if (!$tools): ?>
                    <tr><td colspan="4">Noch kein Tarifrechner angelegt.</td></tr>
                <?php else: foreach ($tools as $id => $tool): ?>
                    <tr>
                        <td><?php echo esc_html((string)$tool['name']); ?></td>
                        <td><?php echo !empty($tool['active']) ? 'aktiv' : 'inaktiv'; ?></td>
                        <td><input class="regular-text code" readonly onclick="this.select();" value="<?php echo esc_attr($this->tariff_tool_placeholder($id)); ?>"></td>
                        <td>
                            <a class="button button-small" href="<?php echo esc_url(add_query_arg(array('page'=>'affiliate-portal-tariff-tools','edit'=>$id), admin_url('admin.php'))); ?>">Bearbeiten</a>
                            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline">
                                <input type="hidden" name="action" value="ppar_tariff_tool_delete">
                                <input type="hidden" name="tool_id" value="<?php echo esc_attr($id); ?>">
                                <?php wp_nonce_field('ppar_tariff_tool_delete', 'ppar_tariff_tool_nonce'); ?>
                                <button class="button button-small" type="submit" onclick="return confirm('Tarifrechner wirklich löschen?');">Löschen</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; endif; ?>
                </tbody>
            </table>
        </div>
        <?php
    }
}
