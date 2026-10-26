<?php
if (!defined('ABSPATH')) { exit; }

trait PPAR_Tariff_Tools_Trait {
    private $tariff_tools_request_cache = null;
    private $text_links_request_cache = null;

    private function tariff_tools_option_name() {
        return 'ppar_tariff_tools_v1';
    }

    public function tariff_tools_register_hooks() {
        add_filter('ppar_affiliate_tariff_placeholder_registry', array($this, 'tariff_tools_writer_registry'), 10, 1);
        add_filter('ppar_affiliate_textlink_placeholder_registry', array($this, 'text_links_writer_registry'), 10, 1);
        if (is_admin() && !((function_exists('wp_doing_ajax') && wp_doing_ajax()) || (defined('DOING_AJAX') && DOING_AJAX))) {
            add_action('admin_post_ppar_tariff_tool_save', array($this, 'handle_tariff_tool_save'));
            add_action('admin_post_ppar_tariff_tool_delete', array($this, 'handle_tariff_tool_delete'));
            add_action('admin_post_ppar_text_link_save', array($this, 'handle_text_link_save'));
            add_action('admin_post_ppar_text_link_delete', array($this, 'handle_text_link_delete'));
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


    private function text_links_option_name() {
        return 'ppar_text_links_v1';
    }

    private function text_links_normalize($raw) {
        $out = array();
        foreach ((array)$raw as $key => $link) {
            if (!is_array($link)) { continue; }
            $id = sanitize_key((string)($link['id'] ?? $key));
            if ($id === '') { continue; }
            $partner = sanitize_text_field((string)($link['partner'] ?? ''));
            $name = sanitize_text_field((string)($link['name'] ?? $id));
            $link_text = sanitize_text_field((string)($link['link_text'] ?? ''));
            $tracking_url = esc_url_raw((string)($link['tracking_url'] ?? ''));
            $destination_url = esc_url_raw((string)($link['destination_url'] ?? ''));
            $partner_html = isset($link['partner_html']) && is_string($link['partner_html']) ? $link['partner_html'] : '';
            $out[$id] = array(
                'id' => $id,
                'partner' => $partner,
                'name' => $name !== '' ? $name : $id,
                'link_text' => $link_text,
                'tracking_url' => $tracking_url,
                'destination_url' => $destination_url,
                'partner_html' => $partner_html,
                'active' => !empty($link['active']) ? 1 : 0,
                'created_at' => absint($link['created_at'] ?? 0),
                'updated_at' => absint($link['updated_at'] ?? 0),
            );
        }
        uasort($out, static function($a, $b) {
            $partner_cmp = strnatcasecmp((string)$a['partner'], (string)$b['partner']);
            return $partner_cmp !== 0 ? $partner_cmp : strnatcasecmp((string)$a['name'], (string)$b['name']);
        });
        return $out;
    }

    private function text_links_all($force = false) {
        if ($force || $this->text_links_request_cache === null) {
            $this->text_links_request_cache = $this->text_links_normalize(
                get_option($this->text_links_option_name(), array())
            );
        }
        return $this->text_links_request_cache;
    }

    private function text_links_store_all($links) {
        $normalized = $this->text_links_normalize($links);
        $option = $this->text_links_option_name();
        $exists = get_option($option, null);
        if ($exists === null) {
            add_option($option, $normalized, '', 'no');
        } else {
            update_option($option, $normalized, false);
        }
        $this->text_links_request_cache = $normalized;
        return $normalized;
    }

    private function text_link_unique_id($partner, $name, $links) {
        $base = sanitize_title(remove_accents(trim((string)$partner . '-' . (string)$name)));
        $base = sanitize_key($base);
        if ($base === '') { $base = 'textlink'; }
        $id = $base;
        $n = 2;
        while (isset($links[$id])) {
            $id = $base . '-' . $n;
            $n++;
        }
        return $id;
    }

    private function text_link_placeholder($id) {
        $id = sanitize_key((string)$id);
        return $id === '' ? '' : '[affiliate_textlink id="' . $id . '"]';
    }

    public function text_links_writer_registry($registry = array()) {
        $registry = is_array($registry) ? $registry : array();
        foreach ($this->text_links_all() as $id => $link) {
            $has_partner_html = trim((string)($link['partner_html'] ?? '')) !== '';
            $has_simple_link = trim((string)($link['link_text'] ?? '')) !== '' && trim((string)($link['tracking_url'] ?? '')) !== '';
            if (empty($link['active']) || (!$has_partner_html && !$has_simple_link)) { continue; }
            $registry[$id] = array(
                'id' => $id,
                'partner' => (string)$link['partner'],
                'name' => (string)$link['name'],
                'link_text' => (string)$link['link_text'],
                'placeholder' => $this->text_link_placeholder($id),
            );
        }
        return $registry;
    }

    public function shortcode_text_link($atts = array()) {
        $atts = shortcode_atts(array('id' => ''), (array)$atts, 'affiliate_textlink');
        $id = sanitize_key((string)($atts['id'] ?? ''));
        if ($id === '') { return ''; }

        $links = $this->text_links_all();
        if (empty($links[$id]) || empty($links[$id]['active'])) { return ''; }
        $link = $links[$id];

        // Vollständiger Partnercode hat Vorrang. Er stammt ausschließlich aus
        // der manage_options-geschützten zentralen Pflege und wird wie der
        // bestehende Tarifrechner-Code bewusst unverändert ausgegeben.
        $partner_html = (string)($link['partner_html'] ?? '');
        if (trim($partner_html) !== '') {
            return $partner_html;
        }

        $tracking_url = esc_url_raw((string)($link['tracking_url'] ?? ''));
        $link_text = sanitize_text_field((string)($link['link_text'] ?? ''));
        if ($tracking_url === '' || $link_text === '' || !wp_http_validate_url($tracking_url)) { return ''; }

        return '<a class="ppar-affiliate-textlink" href="' . esc_url($tracking_url) . '" target="_blank" rel="sponsored nofollow noopener">' . esc_html($link_text) . '</a>';
    }

    public function handle_text_link_save() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_text_link_save', 'ppar_text_link_nonce');

        $links = $this->text_links_all();
        $existing_id = sanitize_key((string)wp_unslash($_POST['textlink_id'] ?? ''));
        $partner = sanitize_text_field((string)wp_unslash($_POST['textlink_partner'] ?? ''));
        $name = sanitize_text_field((string)wp_unslash($_POST['textlink_name'] ?? ''));
        $link_text = sanitize_text_field((string)wp_unslash($_POST['textlink_text'] ?? ''));
        $tracking_url = esc_url_raw((string)wp_unslash($_POST['textlink_tracking_url'] ?? ''));
        $destination_url = esc_url_raw((string)wp_unslash($_POST['textlink_destination_url'] ?? ''));
        $partner_html = trim((string)wp_unslash($_POST['textlink_partner_html'] ?? ''));
        $active = !empty($_POST['textlink_active']) ? 1 : 0;

        if ($partner === '' || $name === '') {
            $this->tariff_tool_redirect(array('ppar_textlink_error' => rawurlencode('Partner und Bezeichnung sind erforderlich.')));
        }
        if ($partner_html === '' && ($link_text === '' || $tracking_url === '' || !wp_http_validate_url($tracking_url))) {
            $this->tariff_tool_redirect(array('ppar_textlink_error' => rawurlencode('Entweder vollständigen Partnercode oder sichtbaren Linktext plus gültigen Affiliate-/Tracking-Link eintragen.')));
        }
        if (strlen($partner_html) > 500000) {
            $this->tariff_tool_redirect(array('ppar_textlink_error' => rawurlencode('Der Partnercode ist zu groß.')));
        }
        if ($destination_url !== '' && !wp_http_validate_url($destination_url)) {
            $this->tariff_tool_redirect(array('ppar_textlink_error' => rawurlencode('Die optionale Ziel-URL ist ungültig.')));
        }

        if ($existing_id !== '' && isset($links[$existing_id])) {
            $id = $existing_id;
            $created_at = absint($links[$id]['created_at'] ?? time());
        } else {
            $id = $this->text_link_unique_id($partner, $name, $links);
            $created_at = time();
        }

        $links[$id] = array(
            'id' => $id,
            'partner' => $partner,
            'name' => $name,
            'link_text' => $link_text,
            'tracking_url' => $tracking_url,
            'destination_url' => $destination_url,
            'partner_html' => $partner_html,
            'active' => $active,
            'created_at' => $created_at,
            'updated_at' => time(),
        );
        $this->text_links_store_all($links);
        $this->tariff_tool_redirect(array(
            'ppar_textlink_saved' => '1',
            'textlink_id' => $id,
        ));
    }

    public function handle_text_link_delete() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_text_link_delete', 'ppar_text_link_nonce');

        $id = sanitize_key((string)wp_unslash($_POST['textlink_id'] ?? ''));
        $links = $this->text_links_all();
        if ($id !== '' && isset($links[$id])) {
            unset($links[$id]);
            $this->text_links_store_all($links);
        }
        $this->tariff_tool_redirect(array('ppar_textlink_deleted' => '1'));
    }

    public function render_tariff_tools_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }

        $tools = $this->tariff_tools_all();
        $edit_id = sanitize_key((string)wp_unslash($_GET['edit'] ?? ''));
        $edit = ($edit_id !== '' && isset($tools[$edit_id])) ? $tools[$edit_id] : null;
        $saved_id = sanitize_key((string)wp_unslash($_GET['tool_id'] ?? ''));
        $text_links = $this->text_links_all();
        $text_edit_id = sanitize_key((string)wp_unslash($_GET['text_edit'] ?? ''));
        $text_edit = ($text_edit_id !== '' && isset($text_links[$text_edit_id])) ? $text_links[$text_edit_id] : null;
        $text_saved_id = sanitize_key((string)wp_unslash($_GET['textlink_id'] ?? ''));

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

        if (!empty($_GET['ppar_textlink_saved'])) {
            echo '<div class="notice notice-success is-dismissible"><p>Textlink gespeichert'
                . ($text_saved_id !== '' ? ': <code>' . esc_html($this->text_link_placeholder($text_saved_id)) . '</code>' : '')
                . '.</p></div>';
        }
        if (!empty($_GET['ppar_textlink_deleted'])) {
            echo '<div class="notice notice-success is-dismissible"><p>Textlink gelöscht.</p></div>';
        }
        if (!empty($_GET['ppar_textlink_error'])) {
            echo '<div class="notice notice-error"><p>' . esc_html(rawurldecode((string)$_GET['ppar_textlink_error'])) . '</p></div>';
        }

        $writer_lines = array();
        foreach ($this->tariff_tools_writer_registry(array()) as $row) {
            $writer_lines[] = $row['name'] . ': ' . $row['placeholder'];
        }
        $text_writer_lines = array();
        foreach ($this->text_links_writer_registry(array()) as $row) {
            $label = trim((string)$row['partner'] . ' · ' . (string)$row['name']);
            $text_writer_lines[] = $label . ': ' . $row['placeholder'];
        }
        ?>
        <div class="wrap">
            <h1>Rechner &amp; Textlinks</h1>
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

            <hr style="margin:32px 0">
            <h2>Affiliate-Textlinks</h2>
            <p><strong>KISS:</strong> Textlinks werden zentral gepflegt. Artikel enthalten nur den stabilen Platzhalter. Möglich sind ein kompletter Partnercode oder ein einfacher Link aus Linktext + Tracking-URL. Kein Banner, keine Bildprüfung und keine automatische Textsuche.</p>

            <h3><?php echo $text_edit ? 'Textlink bearbeiten' : 'Textlink anlegen'; ?></h3>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                <input type="hidden" name="action" value="ppar_text_link_save">
                <?php wp_nonce_field('ppar_text_link_save', 'ppar_text_link_nonce'); ?>
                <?php if ($text_edit): ?>
                    <input type="hidden" name="textlink_id" value="<?php echo esc_attr($text_edit_id); ?>">
                    <p><strong>Stabiler Platzhalter:</strong> <code><?php echo esc_html($this->text_link_placeholder($text_edit_id)); ?></code></p>
                <?php endif; ?>
                <table class="form-table" role="presentation">
                    <tr><th scope="row"><label for="ppar-textlink-partner">Partner / Programm</label></th><td><input id="ppar-textlink-partner" name="textlink_partner" class="regular-text" required value="<?php echo esc_attr($text_edit ? (string)$text_edit['partner'] : ''); ?>" placeholder="z. B. LeadAlliance"></td></tr>
                    <tr><th scope="row"><label for="ppar-textlink-name">Bezeichnung</label></th><td><input id="ppar-textlink-name" name="textlink_name" class="regular-text" required value="<?php echo esc_attr($text_edit ? (string)$text_edit['name'] : ''); ?>" placeholder="z. B. Pferdeversicherung"></td></tr>
                    <tr><th scope="row"><label for="ppar-textlink-code">Kompletter Partnercode (optional)</label></th><td><textarea id="ppar-textlink-code" name="textlink_partner_html" rows="8" class="large-text code" placeholder="&lt;a href=&quot;https://…&quot;&gt;…&lt;img …&gt;&lt;/a&gt;"><?php echo esc_textarea($text_edit ? (string)($text_edit['partner_html'] ?? '') : ''); ?></textarea><p class="description"><strong>Empfohlen, wenn der Partner fertigen Code liefert:</strong> vollständigen Code unverändert einfügen, einschließlich Tracking-Pixel/Bild. Dieser Code hat Vorrang vor den beiden Feldern darunter. Nur vertrauenswürdigen Originalcode des Affiliate-Partners verwenden.</p></td></tr>
                    <tr><th scope="row"><label for="ppar-textlink-text">Sichtbarer Linktext (bei einfachem Link)</label></th><td><input id="ppar-textlink-text" name="textlink_text" class="large-text" value="<?php echo esc_attr($text_edit ? (string)$text_edit['link_text'] : ''); ?>" placeholder="z. B. Pferdeversicherung vergleichen"><p class="description">Nur nötig, wenn kein kompletter Partnercode verwendet wird.</p></td></tr>
                    <tr><th scope="row"><label for="ppar-textlink-url">Affiliate-/Tracking-Link (bei einfachem Link)</label></th><td><input id="ppar-textlink-url" type="url" name="textlink_tracking_url" class="large-text code" value="<?php echo esc_attr($text_edit ? (string)$text_edit['tracking_url'] : ''); ?>" placeholder="https://…"><p class="description">Nur nötig, wenn kein kompletter Partnercode verwendet wird. Der Link wird nicht automatisch verändert oder serverseitig aufgerufen.</p></td></tr>
                    <tr><th scope="row"><label for="ppar-textlink-destination">Reale Ziel-URL (optional)</label></th><td><input id="ppar-textlink-destination" type="url" name="textlink_destination_url" class="large-text code" value="<?php echo esc_attr($text_edit ? (string)$text_edit['destination_url'] : ''); ?>" placeholder="https://…"><p class="description">Nur zur Dokumentation. Keine Frontend-Auflösung und kein zusätzlicher HTTP-Aufruf.</p></td></tr>
                    <tr><th scope="row">Status</th><td><label><input type="checkbox" name="textlink_active" value="1" <?php checked($text_edit ? !empty($text_edit['active']) : true); ?>> aktiv</label></td></tr>
                </table>
                <?php submit_button($text_edit ? 'Textlink speichern' : 'Textlink anlegen'); ?>
            </form>

            <h3>Textlink-Platzhalter für den Schreiber</h3>
            <p>Nur aktive Textlinks. Der Schreibchat verwendet ausschließlich einen passenden vorhandenen Platzhalter und erfindet keine Affiliate-URLs.</p>
            <textarea id="ppar-textlink-writer-list" class="large-text code" rows="<?php echo max(3, min(12, count($text_writer_lines) + 1)); ?>" readonly><?php echo esc_textarea(implode("\n", $text_writer_lines)); ?></textarea>
            <p><button type="button" class="button" onclick="navigator.clipboard && navigator.clipboard.writeText(document.getElementById('ppar-textlink-writer-list').value);">Textlink-Liste kopieren</button></p>

            <h3>Gespeicherte Textlinks</h3>
            <table class="widefat striped">
                <thead><tr><th>Partner</th><th>Textlink</th><th>Status</th><th>Platzhalter</th><th>Aktion</th></tr></thead>
                <tbody>
                <?php if (!$text_links): ?>
                    <tr><td colspan="5">Noch kein Textlink angelegt.</td></tr>
                <?php else: foreach ($text_links as $id => $link): ?>
                    <tr>
                        <td><?php echo esc_html((string)$link['partner']); ?></td>
                        <td><strong><?php echo esc_html((string)$link['name']); ?></strong><br><span class="description"><?php echo trim((string)($link['partner_html'] ?? '')) !== '' ? 'Kompletter Partnercode' : esc_html((string)$link['link_text']); ?></span></td>
                        <td><?php echo !empty($link['active']) ? 'aktiv' : 'inaktiv'; ?></td>
                        <td><input class="regular-text code" readonly onclick="this.select();" value="<?php echo esc_attr($this->text_link_placeholder($id)); ?>"></td>
                        <td>
                            <a class="button button-small" href="<?php echo esc_url(add_query_arg(array('page'=>'affiliate-portal-tariff-tools','text_edit'=>$id), admin_url('admin.php'))); ?>">Bearbeiten</a>
                            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline">
                                <input type="hidden" name="action" value="ppar_text_link_delete">
                                <input type="hidden" name="textlink_id" value="<?php echo esc_attr($id); ?>">
                                <?php wp_nonce_field('ppar_text_link_delete', 'ppar_text_link_nonce'); ?>
                                <button class="button button-small" type="submit" onclick="return confirm('Textlink wirklich löschen?');">Löschen</button>
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
