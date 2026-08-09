<?php
/* DIAGNOSTIC EXTRACT ONLY — exact excerpts from V1.50.421 pferde-template-kit.php. Not a runnable plugin. */

/* ===== ORIGINAL LINES 200-255 ===== */
/* L00200 */         add_filter('body_class', [__CLASS__, 'portal_body_classes']);
/* L00201 */         // V1.50.384: Auf den portalinternen WordPress-Seitenebenen Hub 2,
/* L00202 */         // Kategorie und Leaf rendert das Designplugin das zugewiesene Seitenbild
/* L00203 */         // innerhalb des jeweils tatsaechlich aktiven Renderers. Astra 4.4+ nutzt
/* L00204 */         // fuer Einzelansichten den modernen Filter astra_post_featured_image_condition;
/* L00205 */         // aeltere/alternative Astra-Pfade nutzen astra_featured_image_enabled.
/* L00206 */         // Beide Pfade werden identisch und nur bei sicherer eigener Full-Ausgabe
/* L00207 */         // deaktiviert. Hub 1 bleibt unveraendert.
/* L00208 */         add_filter('astra_post_featured_image_condition', [__CLASS__, 'astra_portal_page_featured_image_v150385'], 999);
/* L00209 */         add_filter('astra_featured_image_enabled', [__CLASS__, 'astra_portal_page_featured_image_v150385'], 999);
/* L00210 */         // V1.50.386: Der Anzeigenmarkt rendert sein reales Seitenbild zusaetzlich
/* L00211 */         // an einem belastbaren Astra-Hook. Dadurch ist die Ausgabe nicht mehr davon
/* L00212 */         // abhaengig, ob der Intro-Shortcode direkt im gespeicherten Seiteninhalt steht.
/* L00213 */         add_action('astra_primary_content_top', [__CLASS__, 'render_market_page_image_v150386'], 0);
/* L00214 */         // V1.50.385: Normale WordPress-Kategoriearchive sowie die in der
/* L00215 */         // Bildzentrale konfigurierte HivePress-Taxonomie erhalten ihr reales
/* L00216 */         // Full-Termbild innerhalb der Astra-Inhaltsachse, nicht viewportbreit.
/* L00217 */         add_action('astra_primary_content_top', [__CLASS__, 'render_term_archive_image_v150385'], 1);
/* L00218 */         // V1.50.329: Astras eigenständiger Block „Ähnliche Beiträge“ ist auf
/* L00219 */         // Einzelbeiträgen deaktiviert. Die redaktionell kontrollierte
/* L00220 */         // Affiliate-Zentrale verwaltet den einzigen optionalen Abschlussblock.
/* L00221 */         add_filter('astra_related_posts_query_args', [__CLASS__, 'disable_astra_related_posts_query_v150329'], 99);
/* L00222 */         add_action('admin_menu', [__CLASS__, 'admin_menu']);
/* L00223 */         add_action('admin_init', [__CLASS__, 'admin_init']);
/* L00224 */         add_action('admin_enqueue_scripts', [__CLASS__, 'admin_assets']);
/* L00225 */         add_action('wp_ajax_pftk_search_published_pages', [__CLASS__, 'ajax_search_published_pages']);
/* L00226 */         // V1.50.297: Relevanssi Live Ajax Search bleibt die einzige Live-Suchlogik.
/* L00227 */         // Der Header markiert sein manuelles Formular explizit fuer das Plugin;
/* L00228 */         // die Ergebnisabfrage darf ausschliesslich veroeffentlichte Inhalte liefern.
/* L00229 */         add_filter('relevanssi_live_search_query_args', [__CLASS__, 'relevanssi_live_search_published_only_v150297']);
/* L00230 */         // V1.50.414: Die globale Header-Suche besitzt einen eng gescopten eigenen
/* L00231 */         // Transport. Dadurch ist sie nicht mehr vom Renderer oder Indexumfang der
/* L00232 */         // Relevanssi-Live-Ausgabe abhaengig. Relevanssi bleibt fuer Portalranking
/* L00233 */         // nutzbar; HivePress-Listings erhalten einen nativen WP-Fallback.
/* L00234 */         add_action('wp_ajax_pftk_header_search_v150414', [__CLASS__, 'header_search_ajax_v150414']);
/* L00235 */         add_action('wp_ajax_nopriv_pftk_header_search_v150414', [__CLASS__, 'header_search_ajax_v150414']);
/* L00236 */         add_action('pre_get_posts', [__CLASS__, 'portal_search_scope_v150408'], 20);
/* L00237 */         add_action('wp_head', [__CLASS__, 'print_header_search_css_v150414'], 100064);
/* L00238 */         add_action('wp_footer', [__CLASS__, 'print_header_search_js_v150414'], 100064);
/* L00239 */         // V1.50.414: Reale Affiliate-Produktkarten werden auf Bild, Titel und Preis
/* L00240 */         // reduziert. Ein einziger Hinweis steht rasterweit ausserhalb der Karte;
/* L00241 */         // der providerbezogene CTA liegt unterhalb des Kartenrahmens.
/* L00242 */         add_action('wp_head', [__CLASS__, 'print_real_affiliate_product_css_v150414'], 100065);
/* L00243 */         add_action('wp_footer', [__CLASS__, 'print_real_affiliate_product_js_v150414'], 100065);
/* L00244 */ 
/* L00245 */         // V1.49.0: kategoriebasierter, deterministischer Kategorie-Intro-Workflow.
/* L00246 */         // Texte werden als Seiten-Metadaten gespeichert, koennen manuell ueberschrieben
/* L00247 */         // werden und stehen direkt unter dem normalen WordPress-Seitentitel.
/* L00248 */         add_filter('the_content', [__CLASS__, 'prepend_category_intro_to_content'], 99);
/* L00249 */         add_filter('the_content', [__CLASS__, 'prepend_page_shortline_to_content'], 100);
/* L00250 */         add_action('add_meta_boxes', [__CLASS__, 'add_category_intro_meta_box']);
/* L00251 */         add_action('save_post_page', [__CLASS__, 'save_category_intro_meta_box'], 20, 2);
/* L00252 */         add_action('admin_post_pftk_save_category_text_settings', [__CLASS__, 'handle_save_category_text_settings']);
/* L00253 */         add_action('admin_post_pftk_generate_category_texts', [__CLASS__, 'handle_generate_category_texts']);
/* L00254 */         add_action('wp_ajax_pftk_generate_category_text_batch', [__CLASS__, 'ajax_generate_category_text_batch']);
/* L00255 */     }

/* ===== ORIGINAL LINES 4435-5060 ===== */
/* L04435 */                 || preg_match('~/(?:account|user-account)(?:/|$)~i', $path);
/* L04436 */             if ($is_account && $id !== 0) { $remove[$id] = true; }
/* L04437 */         }
/* L04438 */         do {
/* L04439 */             $changed = false;
/* L04440 */             foreach ($items as $item) {
/* L04441 */                 $id = intval($item->ID ?? 0);
/* L04442 */                 $parent = intval($item->menu_item_parent ?? 0);
/* L04443 */                 if ($id !== 0 && $parent !== 0 && !empty($remove[$parent]) && empty($remove[$id])) {
/* L04444 */                     $remove[$id] = true;
/* L04445 */                     $changed = true;
/* L04446 */                 }
/* L04447 */             }
/* L04448 */         } while ($changed);
/* L04449 */         return array_values(array_filter($items, static function ($item) use ($remove) {
/* L04450 */             return empty($remove[intval($item->ID ?? 0)]);
/* L04451 */         }));
/* L04452 */     }
/* L04453 */ 
/* L04454 */     /**
/* L04455 */      * V1.50.408: Nur das manuell gerenderte Headerformular darf die gruppierte
/* L04456 */      * AJAX-Ausgabe aktivieren. Andere Relevanssi-Live-Suchen bleiben unangetastet.
/* L04457 */      */
/* L04458 */     private static function is_header_live_search_request_v150408() {
/* L04459 */         $action = isset($_REQUEST['action']) ? sanitize_key(wp_unslash((string)$_REQUEST['action'])) : '';
/* L04460 */         $marker = isset($_REQUEST['pftk_header_search']) ? sanitize_text_field(wp_unslash((string)$_REQUEST['pftk_header_search'])) : '';
/* L04461 */         return $action === 'relevanssi_live_search' && $marker === '1';
/* L04462 */     }
/* L04463 */ 
/* L04464 */     /**
/* L04465 */      * V1.50.408: Eigenes Ergebnis-Template ausschliesslich fuer die globale
/* L04466 */      * Header-Live-Suche. Relevanssi bleibt Suchmaschine und AJAX-Transport.
/* L04467 */      */
/* L04468 */     public static function header_search_results_template_v150408($template, $config = '') {
/* L04469 */         if (!self::is_header_live_search_request_v150408()) { return $template; }
/* L04470 */         $candidate = plugin_dir_path(__FILE__) . 'templates/search-results-pftk-v150408.php';
/* L04471 */         return is_readable($candidate) ? $candidate : $template;
/* L04472 */     }
/* L04473 */ 
/* L04474 */ 
/* L04475 */     /**
/* L04476 */      * V1.50.413: Belastbarer Endpunkt fuer die Header-Live-Suche. Relevanssi
/* L04477 */      * Live Ajax Search ruft die Template-Funktion nach der eigentlichen Query
/* L04478 */      * auf; fremde Live-Suchformulare behalten ihren bisherigen Renderer.
/* L04479 */      */
/* L04480 */     public static function header_search_template_function_v150413($template_function) {
/* L04481 */         if (!self::is_header_live_search_request_v150408()) { return $template_function; }
/* L04482 */         return 'pftk_render_grouped_live_search_v150413';
/* L04483 */     }
/* L04484 */ 
/* L04485 */     /**
/* L04486 */      * Oeffentliche, durchsuchbare Portal-Inhaltstypen. HivePress-Modelle und
/* L04487 */      * Attachments werden fuer die PORTAL-Gruppe bewusst ausgeschlossen.
/* L04488 */      */
/* L04489 */     private static function portal_search_post_types_v150408() {
/* L04490 */         $types = [];
/* L04491 */         foreach ((array)get_post_types(['public' => true], 'objects') as $name => $object) {
/* L04492 */             $name = sanitize_key((string)$name);
/* L04493 */             if ($name === '' || $name === 'attachment' || $name === 'hp_listing' || strpos($name, 'hp_') === 0) { continue; }
/* L04494 */             if (is_object($object) && !empty($object->exclude_from_search)) { continue; }
/* L04495 */             $types[] = $name;
/* L04496 */         }
/* L04497 */         if (!$types) { $types = ['post', 'page']; }
/* L04498 */         return array_values(array_unique(apply_filters('pftk_portal_search_post_types_v150408', $types)));
/* L04499 */     }
/* L04500 */ 
/* L04501 */     /**
/* L04502 */      * Vollstaendige Portalsuche hinter "Alle Portalergebnisse ansehen". Die
/* L04503 */      * Taxonomie "category" bleibt als Relevanssi-Premium-Ergebnis moeglich,
/* L04504 */      * waehrend hp_listing und andere HivePress-Modelle ausgeschlossen bleiben.
/* L04505 */      */
/* L04506 */     public static function portal_search_scope_v150408($query) {
/* L04507 */         if (is_admin() || !is_object($query) || !method_exists($query, 'is_main_query') || !$query->is_main_query() || !$query->is_search()) { return; }
/* L04508 */         $scope = isset($_GET['pftk_scope']) ? sanitize_key(wp_unslash((string)$_GET['pftk_scope'])) : '';
/* L04509 */         if ($scope !== 'portal') { return; }
/* L04510 */         $types = self::portal_search_post_types_v150408();
/* L04511 */         // Relevanssi Premium repraesentiert indexierte Kategorien als Ergebnisobjekte
/* L04512 */         // mit post_type "category". Ohne Relevanssi ignoriert WP diesen Typ einfach.
/* L04513 */         $types[] = 'category';
/* L04514 */         $types = array_values(array_unique($types));
/* L04515 */         $query->set('post_type', $types);
/* L04516 */         $query->set('post_types', $types); // Relevanssi-spezifisch, u. a. fuer Seiten/Taxonomietreffer.
/* L04517 */         $query->set('post_status', 'publish');
/* L04518 */     }
/* L04519 */ 
/* L04520 */     /**
/* L04521 */      * Fuehrt eine getrennte Suchabfrage ueber denselben Relevanssi-Kern aus.
/* L04522 */      * Nur wenn Relevanssi selbst nicht verfuegbar ist, greift WordPress als
/* L04523 */      * funktionaler Fallback. Es wird keine parallele Suchmaschine eingefuehrt.
/* L04524 */      */
/* L04525 */     private static function grouped_search_query_v150408($search, $post_types, $limit = 5) {
/* L04526 */         $search = trim((string)$search);
/* L04527 */         if ($search === '') { return []; }
/* L04528 */         $limit = max(1, min(50, absint($limit)));
/* L04529 */         $args = [
/* L04530 */             's' => $search,
/* L04531 */             'posts_per_page' => $limit,
/* L04532 */             'post_status' => 'publish',
/* L04533 */             'ignore_sticky_posts' => true,
/* L04534 */             'no_found_rows' => true,
/* L04535 */         ];
/* L04536 */         if (is_array($post_types) && $post_types) { $post_types = array_values(array_unique($post_types)); $args['post_type'] = $post_types; $args['post_types'] = $post_types; }
/* L04537 */ 
/* L04538 */         if (function_exists('relevanssi_do_query')) {
/* L04539 */             $query = new WP_Query();
/* L04540 */             $query->parse_query($args);
/* L04541 */             relevanssi_do_query($query);
/* L04542 */             return is_array($query->posts ?? null) ? $query->posts : [];
/* L04543 */         }
/* L04544 */         $query = new WP_Query($args);
/* L04545 */         return is_array($query->posts ?? null) ? $query->posts : [];
/* L04546 */     }
/* L04547 */ 
/* L04548 */     private static function grouped_result_url_v150408($item) {
/* L04549 */         if (!is_object($item)) { return ''; }
/* L04550 */         foreach (['relevanssi_link', 'link'] as $key) {
/* L04551 */             if (!empty($item->{$key}) && is_string($item->{$key})) { return (string)$item->{$key}; }
/* L04552 */         }
/* L04553 */         if (!empty($item->term_id) && !empty($item->taxonomy)) {
/* L04554 */             $url = get_term_link(absint($item->term_id), sanitize_key((string)$item->taxonomy));
/* L04555 */             return is_wp_error($url) ? '' : (string)$url;
/* L04556 */         }
/* L04557 */         if (!empty($item->ID) && intval($item->ID) > 0) {
/* L04558 */             $url = get_permalink(absint($item->ID));
/* L04559 */             return $url ? (string)$url : '';
/* L04560 */         }
/* L04561 */         return '';
/* L04562 */     }
/* L04563 */ 
/* L04564 */     private static function grouped_result_title_v150408($item) {
/* L04565 */         if (!is_object($item)) { return ''; }
/* L04566 */         if (isset($item->post_title)) { return trim(wp_strip_all_tags((string)$item->post_title)); }
/* L04567 */         if (isset($item->name)) { return trim(wp_strip_all_tags((string)$item->name)); }
/* L04568 */         return '';
/* L04569 */     }
/* L04570 */ 
/* L04571 */     private static function grouped_result_key_v150408($item) {
/* L04572 */         if (!is_object($item)) { return ''; }
/* L04573 */         $type = sanitize_key((string)($item->post_type ?? $item->taxonomy ?? ''));
/* L04574 */         $id = isset($item->term_id) ? absint($item->term_id) : absint($item->ID ?? 0);
/* L04575 */         $url = self::grouped_result_url_v150408($item);
/* L04576 */         return $type . '|' . $id . '|' . $url;
/* L04577 */     }
/* L04578 */ 
/* L04579 */     private static function grouped_filter_results_v150408($items, $group, $limit = 5) {
/* L04580 */         $out = [];
/* L04581 */         $seen = [];
/* L04582 */         $portal_types = array_flip(self::portal_search_post_types_v150408());
/* L04583 */         foreach ((array)$items as $item) {
/* L04584 */             if (!is_object($item)) { continue; }
/* L04585 */             $type = sanitize_key((string)($item->post_type ?? $item->taxonomy ?? ''));
/* L04586 */             $is_listing = $type === 'hp_listing';
/* L04587 */             if ($group === 'anzeigen') {
/* L04588 */                 if (!$is_listing) { continue; }
/* L04589 */             } else {
/* L04590 */                 if ($is_listing || strpos($type, 'hp_') === 0 || $type === 'attachment') { continue; }
/* L04591 */                 // Kategorie-Treffer nur dann zeigen, wenn die bestehende Relevanssi-
/* L04592 */                 // Konfiguration sie tatsaechlich geliefert hat. Andere fremde
/* L04593 */                 // Pseudo-Objekte (z. B. Benutzer) werden nicht in PORTAL gemischt.
/* L04594 */                 if ($type !== 'category' && !isset($portal_types[$type])) { continue; }
/* L04595 */             }
/* L04596 */             $title = self::grouped_result_title_v150408($item);
/* L04597 */             $url = self::grouped_result_url_v150408($item);
/* L04598 */             if ($title === '' || $url === '') { continue; }
/* L04599 */             $key = self::grouped_result_key_v150408($item);
/* L04600 */             if ($key === '' || isset($seen[$key])) { continue; }
/* L04601 */             $seen[$key] = true;
/* L04602 */             $out[] = $item;
/* L04603 */             if (count($out) >= $limit) { break; }
/* L04604 */         }
/* L04605 */         return $out;
/* L04606 */     }
/* L04607 */ 
/* L04608 */     private static function render_grouped_result_rows_v150408($items, $label) {
/* L04609 */         $first = true;
/* L04610 */         foreach ((array)$items as $item) {
/* L04611 */             $title = self::grouped_result_title_v150408($item);
/* L04612 */             $url = self::grouped_result_url_v150408($item);
/* L04613 */             if ($title === '' || $url === '') { continue; }
/* L04614 */             $classes = 'relevanssi-live-search-result pftk-grouped-search-result-v150408';
/* L04615 */             if ($first) { $classes .= ' pftk-grouped-search-first-v150408'; }
/* L04616 */             echo '<div class="' . esc_attr($classes) . '">';
/* L04617 */             if ($first) { echo '<div class="pftk-grouped-search-label-v150408">' . esc_html($label) . '</div>'; }
/* L04618 */             echo '<p><a href="' . esc_url($url) . '">' . esc_html($title) . '</a></p></div>';
/* L04619 */             $first = false;
/* L04620 */         }
/* L04621 */     }
/* L04622 */ 
/* L04623 */     private static function render_grouped_more_row_v150408($label, $url) {
/* L04624 */         echo '<div class="relevanssi-live-search-result pftk-grouped-search-more-v150408"><p><a href="' . esc_url($url) . '">' . esc_html($label) . '</a></p></div>';
/* L04625 */     }
/* L04626 */ 
/* L04627 */     /**
/* L04628 */      * Sichtbare Live-Ausgabe: maximal 5 Anzeigen und 5 Portal-Ergebnisse. Beide
/* L04629 */      * Gruppen werden unabhaengig ueber Relevanssi abgefragt und leer komplett
/* L04630 */      * ausgeblendet.
/* L04631 */      */
/* L04632 */     public static function render_grouped_live_search_v150408($original_query = null) {
/* L04633 */         $search = isset($_REQUEST['rlvquery']) ? sanitize_text_field(wp_unslash((string)$_REQUEST['rlvquery'])) : '';
/* L04634 */         if ($search === '' && isset($_REQUEST['s'])) { $search = sanitize_text_field(wp_unslash((string)$_REQUEST['s'])); }
/* L04635 */         $search = trim($search);
/* L04636 */         echo '<div class="relevanssi-live-search-results pftk-grouped-live-search-v150408" role="listbox">';
/* L04637 */         if ($search === '') {
/* L04638 */             echo '<div class="relevanssi-live-search-result-status"><p>Keine Ergebnisse gefunden.</p></div></div>';
/* L04639 */             return;
/* L04640 */         }
/* L04641 */ 
/* L04642 */         $anzeigen_raw = self::grouped_search_query_v150408($search, ['hp_listing'], 12);
/* L04643 */         $anzeigen = self::grouped_filter_results_v150408($anzeigen_raw, 'anzeigen', 5);
/* L04644 */ 
/* L04645 */         $portal_types = self::portal_search_post_types_v150408();
/* L04646 */         $portal_query_types = array_values(array_unique(array_merge($portal_types, ['category'])));
/* L04647 */         $portal_raw = self::grouped_search_query_v150408($search, $portal_query_types, 18);
/* L04648 */         $portal = self::grouped_filter_results_v150408($portal_raw, 'portal', 5);
/* L04649 */ 
/* L04650 */         // Falls die installierte Relevanssi-Konfiguration Kategorieobjekte nur in
/* L04651 */         // der urspruenglichen Live-Abfrage liefert, koennen sie fehlende Portal-
/* L04652 */         // Plaetze ergaenzen. Vorhandene Portal-Treffer bleiben vorn und eindeutig.
/* L04653 */         if (count($portal) < 5 && is_object($original_query) && is_array($original_query->posts ?? null)) {
/* L04654 */             $fallback = self::grouped_filter_results_v150408($original_query->posts, 'portal', 10);
/* L04655 */             $seen = [];
/* L04656 */             foreach ($portal as $item) { $seen[self::grouped_result_key_v150408($item)] = true; }
/* L04657 */             foreach ($fallback as $item) {
/* L04658 */                 $key = self::grouped_result_key_v150408($item);
/* L04659 */                 if ($key === '' || isset($seen[$key])) { continue; }
/* L04660 */                 $portal[] = $item;
/* L04661 */                 $seen[$key] = true;
/* L04662 */                 if (count($portal) >= 5) { break; }
/* L04663 */             }
/* L04664 */         }
/* L04665 */ 
/* L04666 */         if (!$anzeigen && !$portal) {
/* L04667 */             echo '<div class="relevanssi-live-search-result-status"><p>Keine Ergebnisse gefunden.</p></div></div>';
/* L04668 */             return;
/* L04669 */         }
/* L04670 */ 
/* L04671 */         if ($anzeigen) {
/* L04672 */             self::render_grouped_result_rows_v150408($anzeigen, 'ANZEIGEN');
/* L04673 */             $all_ads = add_query_arg(['s' => $search], home_url('/anzeigenmarkt/'));
/* L04674 */             self::render_grouped_more_row_v150408('Alle Anzeigen ansehen', $all_ads);
/* L04675 */         }
/* L04676 */         if ($portal) {
/* L04677 */             self::render_grouped_result_rows_v150408($portal, 'PORTAL');
/* L04678 */             $all_portal = add_query_arg(['s' => $search, 'pftk_scope' => 'portal'], home_url('/'));
/* L04679 */             self::render_grouped_more_row_v150408('Alle Portalergebnisse ansehen', $all_portal);
/* L04680 */         }
/* L04681 */         echo '</div>';
/* L04682 */     }
/* L04683 */ 
/* L04684 */     /** Nur Darstellung des vorhandenen Header-Dropdowns; kein anderer Suchbereich. */
/* L04685 */     public static function print_grouped_header_search_css_v150408() {
/* L04686 */         if (is_admin()) { return; }
/* L04687 */         echo '<style id="pftk-grouped-header-search-v150408">'
/* L04688 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-label-v150408{padding:10px 14px 4px;color:#C89214;font-size:12px;font-weight:700;line-height:1.2;letter-spacing:.08em;text-transform:uppercase}'
/* L04689 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-result-v150408 p{margin:0!important;padding:6px 14px 10px!important;line-height:1.35!important}'
/* L04690 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-result-v150408:not(.pftk-grouped-search-first-v150408) p{padding-top:10px!important}'
/* L04691 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-result-v150408{border-bottom:1px solid rgba(53,66,42,.10)!important}'
/* L04692 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-first-v150408{border-top:1px solid rgba(53,66,42,.16)!important}'
/* L04693 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-first-v150408:first-child{border-top:0!important}'
/* L04694 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-more-v150408{border-bottom:1px solid rgba(53,66,42,.20)!important;background:#fff!important}'
/* L04695 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-more-v150408 p{margin:0!important;padding:9px 14px!important;font-size:13px!important;font-weight:600!important}'
/* L04696 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-more-v150408 a{color:#687066!important}'
/* L04697 */             . '#pftk-brand-live-results-v150297 .pftk-grouped-search-more-v150408:hover a,#pftk-brand-live-results-v150297 .pftk-grouped-search-more-v150408.relevanssi-live-search-result--focused a{color:#C89214!important}'
/* L04698 */             . '</style>';
/* L04699 */     }
/* L04700 */ 
/* L04701 */ 
/* L04702 */     /**
/* L04703 */      * V1.50.414: Nativer Query-Fallback fuer den eng gescopten Header-Suchpfad.
/* L04704 */      * suppress_filters verhindert, dass Relevanssi einen bewusst nativen
/* L04705 */      * HivePress-Fallback erneut ueber seinen Indexumfang begrenzt.
/* L04706 */      */
/* L04707 */     private static function direct_search_query_v150414($search, $post_type, $limit = 10) {
/* L04708 */         $search = trim((string)$search);
/* L04709 */         $post_type = sanitize_key((string)$post_type);
/* L04710 */         if ($search === '' || $post_type === '') { return []; }
/* L04711 */         $query = new WP_Query([
/* L04712 */             's' => $search,
/* L04713 */             'post_type' => $post_type,
/* L04714 */             'posts_per_page' => max(1, min(50, absint($limit))),
/* L04715 */             'post_status' => 'publish',
/* L04716 */             'ignore_sticky_posts' => true,
/* L04717 */             'no_found_rows' => true,
/* L04718 */             'suppress_filters' => true,
/* L04719 */         ]);
/* L04720 */         return is_array($query->posts ?? null) ? $query->posts : [];
/* L04721 */     }
/* L04722 */ 
/* L04723 */     /** Relevanssi zuerst, native Treffer nur zum Auffuellen bzw. als Index-Fallback. */
/* L04724 */     private static function merged_post_type_results_v150414($search, $post_type, $limit = 5) {
/* L04725 */         $post_type = sanitize_key((string)$post_type);
/* L04726 */         $limit = max(1, min(20, absint($limit)));
/* L04727 */         if ($post_type === '') { return []; }
/* L04728 */         $primary = self::grouped_search_query_v150408($search, [$post_type], max(10, $limit * 2));
/* L04729 */         $native = self::direct_search_query_v150414($search, $post_type, max(10, $limit * 2));
/* L04730 */         $out = []; $seen = [];
/* L04731 */         foreach (array_merge((array)$primary, (array)$native) as $item) {
/* L04732 */             if (!is_object($item) || sanitize_key((string)($item->post_type ?? '')) !== $post_type) { continue; }
/* L04733 */             $title = self::grouped_result_title_v150408($item);
/* L04734 */             $url = self::grouped_result_url_v150408($item);
/* L04735 */             if ($title === '' || $url === '') { continue; }
/* L04736 */             $key = $post_type . '|' . absint($item->ID ?? 0) . '|' . $url;
/* L04737 */             if (isset($seen[$key])) { continue; }
/* L04738 */             $seen[$key] = true; $out[] = $item;
/* L04739 */             if (count($out) >= $limit) { break; }
/* L04740 */         }
/* L04741 */         return $out;
/* L04742 */     }
/* L04743 */ 
/* L04744 */     private static function header_search_category_results_v150414($search, $limit = 5) {
/* L04745 */         $limit = max(1, min(10, absint($limit)));
/* L04746 */         $out = []; $seen = [];
/* L04747 */ 
/* L04748 */         // Echte WordPress-Kategorien zuerst: Sie sind die inhaltlichen Leaf-Ziele
/* L04749 */         // des Portals. Hoehere Portal-Hierarchieseiten fuellen danach freie Plaetze.
/* L04750 */         if (function_exists('get_terms')) {
/* L04751 */             $terms = get_terms([
/* L04752 */                 'taxonomy' => 'category',
/* L04753 */                 'hide_empty' => false,
/* L04754 */                 'search' => trim((string)$search),
/* L04755 */                 'number' => max(10, $limit * 3),
/* L04756 */             ]);
/* L04757 */             if (!is_wp_error($terms)) {
/* L04758 */                 foreach ((array)$terms as $term) {
/* L04759 */                     if (!is_object($term) || empty($term->term_id)) { continue; }
/* L04760 */                     $title = trim(wp_strip_all_tags((string)($term->name ?? '')));
/* L04761 */                     $url = get_term_link(absint($term->term_id), 'category');
/* L04762 */                     if ($title === '' || is_wp_error($url) || !$url) { continue; }
/* L04763 */                     $url = (string)$url; $key = strtolower($url);
/* L04764 */                     if (isset($seen[$key])) { continue; }
/* L04765 */                     $seen[$key] = true;
/* L04766 */                     $out[] = ['title' => $title, 'url' => $url, 'kind' => 'category'];
/* L04767 */                     if (count($out) >= $limit) { return $out; }
/* L04768 */                 }
/* L04769 */             }
/* L04770 */         }
/* L04771 */ 
/* L04772 */         // Portal-Hierarchieseiten sind fuer Besucher ebenfalls Kategorien/Themen,
/* L04773 */         // werden aber nie als technische "Seiten" beschriftet.
/* L04774 */         foreach (self::merged_post_type_results_v150414($search, 'page', $limit * 2) as $item) {
/* L04775 */             $title = self::grouped_result_title_v150408($item);
/* L04776 */             $url = self::grouped_result_url_v150408($item);
/* L04777 */             $key = strtolower($url);
/* L04778 */             if ($title === '' || $url === '' || isset($seen[$key])) { continue; }
/* L04779 */             $seen[$key] = true;
/* L04780 */             $out[] = ['title' => $title, 'url' => $url, 'kind' => 'page'];
/* L04781 */             if (count($out) >= $limit) { break; }
/* L04782 */         }
/* L04783 */         return $out;
/* L04784 */     }
/* L04785 */ 
/* L04786 */     private static function header_search_post_results_v150414($search, $post_type, $limit = 5) {
/* L04787 */         $out = [];
/* L04788 */         foreach (self::merged_post_type_results_v150414($search, $post_type, $limit) as $item) {
/* L04789 */             $title = self::grouped_result_title_v150408($item);
/* L04790 */             $url = self::grouped_result_url_v150408($item);
/* L04791 */             if ($title === '' || $url === '') { continue; }
/* L04792 */             $out[] = ['title' => $title, 'url' => $url, 'kind' => sanitize_key((string)$post_type)];
/* L04793 */         }
/* L04794 */         return $out;
/* L04795 */     }
/* L04796 */ 
/* L04797 */     /**
/* L04798 */      * V1.50.417: Eng gescopter Fuzzy-Fallback nur fuer HivePress-Anzeigen im
/* L04799 */      * globalen Header. Er dient ausschliesslich dazu, kleine Tippfehler wie
/* L04800 */      * "regendeckel" -> "Regendecke/Regendecken" abzufangen, ohne Relevanssi-
/* L04801 */      * Einstellungen oder andere Suchformulare zu veraendern.
/* L04802 */      */
/* L04803 */     private static function header_search_normalize_v150417($value) {
/* L04804 */         $value = trim((string)$value);
/* L04805 */         if ($value === '') { return ''; }
/* L04806 */         if (function_exists('remove_accents')) { $value = remove_accents($value); }
/* L04807 */         $value = function_exists('mb_strtolower') ? mb_strtolower($value, 'UTF-8') : strtolower($value);
/* L04808 */         $value = preg_replace('/[^a-z0-9]+/u', ' ', $value);
/* L04809 */         return trim(preg_replace('/\s+/', ' ', (string)$value));
/* L04810 */     }
/* L04811 */ 
/* L04812 */     private static function header_search_longest_token_v150417($value) {
/* L04813 */         $normalized = self::header_search_normalize_v150417($value);
/* L04814 */         if ($normalized === '') { return ''; }
/* L04815 */         $tokens = preg_split('/\s+/', $normalized, -1, PREG_SPLIT_NO_EMPTY);
/* L04816 */         $best = '';
/* L04817 */         foreach ((array)$tokens as $token) {
/* L04818 */             if (strlen($token) > strlen($best)) { $best = $token; }
/* L04819 */         }
/* L04820 */         return $best;
/* L04821 */     }
/* L04822 */ 
/* L04823 */     private static function header_search_fuzzy_score_v150417($search, $candidate) {
/* L04824 */         $needle = self::header_search_longest_token_v150417($search);
/* L04825 */         $haystack = self::header_search_normalize_v150417($candidate);
/* L04826 */         if ($needle === '' || $haystack === '' || strlen($needle) < 4) { return 0; }
/* L04827 */         if ($needle === $haystack) { return 120; }
/* L04828 */         if (strpos($haystack, $needle) !== false) { return 115; }
/* L04829 */ 
/* L04830 */         $tokens = preg_split('/\s+/', $haystack, -1, PREG_SPLIT_NO_EMPTY);
/* L04831 */         $best = 0;
/* L04832 */         foreach ((array)$tokens as $token) {
/* L04833 */             if ($token === $needle) { return 120; }
/* L04834 */             if (strlen($token) >= 4 && (strpos($token, $needle) !== false || strpos($needle, $token) !== false)) {
/* L04835 */                 $short = min(strlen($token), strlen($needle));
/* L04836 */                 if ($short >= 5) { $best = max($best, 108); }
/* L04837 */             }
/* L04838 */             if (strlen($token) < 5) { continue; }
/* L04839 */             $distance = levenshtein($needle, $token);
/* L04840 */             $allowed = strlen($needle) >= 9 ? 2 : 1;
/* L04841 */             if ($distance <= $allowed) { $best = max($best, 100 - ($distance * 5)); }
/* L04842 */         }
/* L04843 */         return $best;
/* L04844 */     }
/* L04845 */ 
/* L04846 */     private static function header_search_listing_fuzzy_title_candidates_v150417($search, $limit = 24) {
/* L04847 */         global $wpdb;
/* L04848 */         $limit = max(1, min(40, absint($limit)));
/* L04849 */         $token = self::header_search_longest_token_v150417($search);
/* L04850 */         if (strlen($token) < 4 || !is_object($wpdb) || empty($wpdb->posts)
/* L04851 */             || !method_exists($wpdb, 'prepare') || !method_exists($wpdb, 'get_results')) { return []; }
/* L04852 */ 
/* L04853 */         // Der DB-Pool nutzt sowohl den originalen Unicode-Anfang als auch die
/* L04854 */         // akzentbereinigte Form. Damit funktionieren z. B. "Führstrik" und
/* L04855 */         // "fuhrstrik" unabhaengig von der konkreten MySQL-Collation.
/* L04856 */         $raw = trim((string)$search);
/* L04857 */         $raw = function_exists('mb_strtolower') ? mb_strtolower($raw, 'UTF-8') : strtolower($raw);
/* L04858 */         $raw = trim(preg_replace('/[^\p{L}\p{N}]+/u', ' ', $raw));
/* L04859 */         $raw_tokens = preg_split('/\s+/', $raw, -1, PREG_SPLIT_NO_EMPTY);
/* L04860 */         $raw_token = '';
/* L04861 */         foreach ((array)$raw_tokens as $candidate) {
/* L04862 */             $candidate_len = function_exists('mb_strlen') ? mb_strlen($candidate, 'UTF-8') : strlen($candidate);
/* L04863 */             $current_len = function_exists('mb_strlen') ? mb_strlen($raw_token, 'UTF-8') : strlen($raw_token);
/* L04864 */             if ($candidate_len > $current_len) { $raw_token = $candidate; }
/* L04865 */         }
/* L04866 */         $raw_prefix = function_exists('mb_substr') ? mb_substr($raw_token, 0, 5, 'UTF-8') : substr($raw_token, 0, 5);
/* L04867 */         $norm_prefix = substr($token, 0, min(5, strlen($token)));
/* L04868 */         if (method_exists($wpdb, 'esc_like')) {
/* L04869 */             $raw_prefix = $wpdb->esc_like($raw_prefix);
/* L04870 */             $norm_prefix = $wpdb->esc_like($norm_prefix);
/* L04871 */         } else {
/* L04872 */             $raw_prefix = addcslashes($raw_prefix, '_%\\');
/* L04873 */             $norm_prefix = addcslashes($norm_prefix, '_%\\');
/* L04874 */         }
/* L04875 */         $raw_like = '%' . $raw_prefix . '%';
/* L04876 */         $norm_like = '%' . $norm_prefix . '%';
/* L04877 */         $sql = $wpdb->prepare(
/* L04878 */             "SELECT ID, post_title, post_type FROM {$wpdb->posts} WHERE post_type = %s AND post_status = 'publish' AND (post_title LIKE %s OR post_title LIKE %s) ORDER BY post_date DESC LIMIT %d",
/* L04879 */             'hp_listing', $raw_like, $norm_like, $limit
/* L04880 */         );
/* L04881 */         $rows = $wpdb->get_results($sql);
/* L04882 */         $scored = [];
/* L04883 */         foreach ((array)$rows as $row) {
/* L04884 */             if (!is_object($row)) { continue; }
/* L04885 */             $row->post_type = 'hp_listing';
/* L04886 */             $score = self::header_search_fuzzy_score_v150417($search, (string)($row->post_title ?? ''));
/* L04887 */             if ($score < 95) { continue; }
/* L04888 */             $scored[] = ['score' => $score, 'item' => $row];
/* L04889 */         }
/* L04890 */         usort($scored, static function($a, $b){ return intval($b['score']) <=> intval($a['score']); });
/* L04891 */         return array_values(array_map(static function($row){ return $row['item']; }, $scored));
/* L04892 */     }
/* L04893 */ 
/* L04894 */     private static function header_search_listing_fuzzy_terms_v150417($search, $limit = 8) {
/* L04895 */         if (!function_exists('get_terms')) { return []; }
/* L04896 */         $taxonomy = 'hp_listing_category';
/* L04897 */         $terms = get_terms(['taxonomy' => $taxonomy, 'hide_empty' => true, 'number' => 0]);
/* L04898 */         if (is_wp_error($terms) || !$terms) { return []; }
/* L04899 */         $scored = [];
/* L04900 */         foreach ((array)$terms as $term) {
/* L04901 */             if (!is_object($term) || empty($term->term_id)) { continue; }
/* L04902 */             $candidate = trim((string)($term->name ?? '') . ' ' . (string)($term->slug ?? ''));
/* L04903 */             $score = self::header_search_fuzzy_score_v150417($search, $candidate);
/* L04904 */             if ($score < 95) { continue; }
/* L04905 */             $scored[] = ['score' => $score, 'term_id' => absint($term->term_id)];
/* L04906 */         }
/* L04907 */         usort($scored, static function($a, $b){ return intval($b['score']) <=> intval($a['score']); });
/* L04908 */         $ids = [];
/* L04909 */         foreach ($scored as $row) {
/* L04910 */             $id = absint($row['term_id']);
/* L04911 */             if ($id > 0 && !in_array($id, $ids, true)) { $ids[] = $id; }
/* L04912 */             if (count($ids) >= max(1, min(20, absint($limit)))) { break; }
/* L04913 */         }
/* L04914 */         return $ids;
/* L04915 */     }
/* L04916 */ 
/* L04917 */     private static function header_search_listing_results_v150417($search, $limit = 5) {
/* L04918 */         $limit = max(1, min(10, absint($limit)));
/* L04919 */         $out = []; $seen = [];
/* L04920 */         $append = static function($item) use (&$out, &$seen, $limit) {
/* L04921 */             if (!is_object($item) || sanitize_key((string)($item->post_type ?? '')) !== 'hp_listing') { return; }
/* L04922 */             $title = Pferde_Template_Kit::grouped_result_title_v150408($item);
/* L04923 */             $url = Pferde_Template_Kit::grouped_result_url_v150408($item);
/* L04924 */             if ($title === '' || $url === '') { return; }
/* L04925 */             $key = absint($item->ID ?? 0) . '|' . strtolower($url);
/* L04926 */             if (isset($seen[$key]) || count($out) >= $limit) { return; }
/* L04927 */             $seen[$key] = true;
/* L04928 */             $out[] = ['title' => $title, 'url' => $url, 'kind' => 'hp_listing'];
/* L04929 */         };
/* L04930 */ 
/* L04931 */         // 1. Bestehende Relevanssi/native Direkttreffer behalten immer Prioritaet.
/* L04932 */         foreach (self::merged_post_type_results_v150414($search, 'hp_listing', $limit * 2) as $item) { $append($item); }
/* L04933 */ 
/* L04934 */         // 2. Tippfehler in konkreten Anzeigentiteln: enger Prefix-Pool + Fuzzy-Score.
/* L04935 */         if (count($out) < $limit) {
/* L04936 */             foreach (self::header_search_listing_fuzzy_title_candidates_v150417($search, 24) as $item) { $append($item); }
/* L04937 */         }
/* L04938 */ 
/* L04939 */         // 3. Tippfehler/Pluralformen in HivePress-Kategorien, anschliessend echte
/* L04940 */         //    veroeffentlichte Listings aus genau diesen Kategorien.
/* L04941 */         if (count($out) < $limit) {
/* L04942 */             $term_ids = self::header_search_listing_fuzzy_terms_v150417($search, 8);
/* L04943 */             if ($term_ids) {
/* L04944 */                 $query = new WP_Query([
/* L04945 */                     'post_type' => 'hp_listing',
/* L04946 */                     'posts_per_page' => max(10, $limit * 3),
/* L04947 */                     'post_status' => 'publish',
/* L04948 */                     'ignore_sticky_posts' => true,
/* L04949 */                     'no_found_rows' => true,
/* L04950 */                     'suppress_filters' => true,
/* L04951 */                     'tax_query' => [[
/* L04952 */                         'taxonomy' => 'hp_listing_category',
/* L04953 */                         'field' => 'term_id',
/* L04954 */                         'terms' => $term_ids,
/* L04955 */                         'include_children' => true,
/* L04956 */                         'operator' => 'IN',
/* L04957 */                     ]],
/* L04958 */                 ]);
/* L04959 */                 foreach ((array)($query->posts ?? []) as $item) { $append($item); }
/* L04960 */             }
/* L04961 */         }
/* L04962 */         return $out;
/* L04963 */     }
/* L04964 */ 
/* L04965 */     private static function header_search_render_group_v150414($items, $label, $group) {
/* L04966 */         $items = array_values(array_filter((array)$items, static function($item){
/* L04967 */             return is_array($item) && trim((string)($item['title'] ?? '')) !== '' && trim((string)($item['url'] ?? '')) !== '';
/* L04968 */         }));
/* L04969 */         if (!$items) { return; }
/* L04970 */         echo '<section class="pftk-header-search-group-v150414" data-pftk-search-group="' . esc_attr($group) . '">';
/* L04971 */         echo '<div class="pftk-header-search-label-v150414">' . esc_html($label) . '</div>';
/* L04972 */         foreach ($items as $item) {
/* L04973 */             echo '<div class="relevanssi-live-search-result pftk-header-search-result-v150414"><p><a href="' . esc_url($item['url']) . '">' . esc_html($item['title']) . '</a></p></div>';
/* L04974 */         }
/* L04975 */         echo '</section>';
/* L04976 */     }
/* L04977 */ 
/* L04978 */     /**
/* L04979 */      * V1.50.417: Header-Suche auf dem live bewaehrten V1.50.414-Transport; ANZEIGEN erhalten nur einen eng gescopten Tippfehler-Fallback. Ergebniswelten:
/* L04980 */      * ANZEIGEN = hp_listing, KATEGORIEN = Portal-Hierarchieseiten + WP-Kategorien,
/* L04981 */      * BEITRAEGE = normale WordPress-Beitraege. Maximal fuenf je Gruppe.
/* L04982 */      */
/* L04983 */     /** Testbarer Renderer fuer den exakt gescopten Header-Suchpfad. */
/* L04984 */     public static function header_search_html_v150414($search) {
/* L04985 */         $search = trim(sanitize_text_field((string)$search));
/* L04986 */         if (function_exists('mb_substr')) { $search = mb_substr($search, 0, 80); }
/* L04987 */         else { $search = substr($search, 0, 80); }
/* L04988 */         if ($search === '' || strlen($search) < 2) { return ''; }
/* L04989 */ 
/* L04990 */         $ads = self::header_search_listing_results_v150417($search, 5);
/* L04991 */         $categories = self::header_search_category_results_v150414($search, 5);
/* L04992 */         $posts = self::header_search_post_results_v150414($search, 'post', 5);
/* L04993 */ 
/* L04994 */         ob_start();
/* L04995 */         echo '<div class="relevanssi-live-search-results pftk-header-search-results-v150414" role="listbox">';
/* L04996 */         if (!$ads && !$categories && !$posts) {
/* L04997 */             echo '<div class="relevanssi-live-search-result-status"><p>Keine Ergebnisse gefunden.</p></div>';
/* L04998 */         } else {
/* L04999 */             self::header_search_render_group_v150414($ads, 'ANZEIGEN', 'anzeigen');
/* L05000 */             self::header_search_render_group_v150414($categories, 'KATEGORIEN', 'kategorien');
/* L05001 */             self::header_search_render_group_v150414($posts, 'BEITRÄGE', 'beitraege');
/* L05002 */         }
/* L05003 */         echo '</div>';
/* L05004 */         return (string)ob_get_clean();
/* L05005 */     }
/* L05006 */ 
/* L05007 */     public static function header_search_ajax_v150414() {
/* L05008 */         if (function_exists('check_ajax_referer')) { check_ajax_referer('pftk_header_search_v150414', 'nonce'); }
/* L05009 */         $search = isset($_REQUEST['q']) ? sanitize_text_field(wp_unslash((string)$_REQUEST['q'])) : '';
/* L05010 */         $html = self::header_search_html_v150414($search);
/* L05011 */         wp_send_json_success(['html' => $html]);
/* L05012 */     }
/* L05013 */ 
/* L05014 */     public static function print_header_search_css_v150414() {
/* L05015 */         if (is_admin()) { return; }
/* L05016 */         echo <<<'PFTK414SEARCHCSS'
/* L05017 */ <style id="pftk-header-search-v150414">
/* L05018 */ #pftk-brand-live-results-v150297 .pftk-header-search-label-v150414{padding:10px 14px 5px;color:#C89214;font-size:11px;font-weight:700;line-height:1.2;letter-spacing:.08em;text-transform:uppercase;background:#fff}
/* L05019 */ #pftk-brand-live-results-v150297 .pftk-header-search-group-v150414+ .pftk-header-search-group-v150414{border-top:1px solid rgba(53,66,42,.18)}
/* L05020 */ #pftk-brand-live-results-v150297 .pftk-header-search-result-v150414{border:0!important;border-bottom:1px solid rgba(53,66,42,.08)!important;background:#fff!important}
/* L05021 */ #pftk-brand-live-results-v150297 .pftk-header-search-result-v150414:last-child{border-bottom:0!important}
/* L05022 */ #pftk-brand-live-results-v150297 .pftk-header-search-result-v150414 p{margin:0!important;padding:7px 14px 9px!important;line-height:1.35!important}
/* L05023 */ #pftk-brand-live-results-v150297 .pftk-header-search-result-v150414 a{display:block;color:#35422A!important;text-decoration:none!important}
/* L05024 */ #pftk-brand-live-results-v150297 .pftk-header-search-result-v150414:hover a,#pftk-brand-live-results-v150297 .pftk-header-search-result-v150414 a:focus-visible{color:#C89214!important}
/* L05025 */ #pftk-brand-live-results-v150297 .pftk-header-search-results-v150414[aria-busy="true"]{opacity:.68}
/* L05026 */ </style>
/* L05027 */ PFTK414SEARCHCSS;
/* L05028 */     }
/* L05029 */ 
/* L05030 */     public static function print_header_search_js_v150414() {
/* L05031 */         if (is_admin()) { return; }
/* L05032 */         $ajax_url = function_exists('admin_url') ? admin_url('admin-ajax.php') : home_url('/wp-admin/admin-ajax.php');
/* L05033 */         $nonce = function_exists('wp_create_nonce') ? wp_create_nonce('pftk_header_search_v150414') : '';
/* L05034 */         $ajax_json = function_exists('wp_json_encode') ? wp_json_encode($ajax_url) : json_encode($ajax_url);
/* L05035 */         $nonce_json = function_exists('wp_json_encode') ? wp_json_encode($nonce) : json_encode($nonce);
/* L05036 */         echo '<script id="pftk-header-search-v150414-js">(function(){'
/* L05037 */             . 'var input=document.getElementById("pftk-brand-search-field"),box=document.getElementById("pftk-brand-live-results-v150297");if(!input||!box)return;'
/* L05038 */             . 'var ajax=' . $ajax_json . ',nonce=' . $nonce_json . ',timer=null,controller=null,last="";'
/* L05039 */             . 'function close(){box.innerHTML="";input.setAttribute("aria-expanded","false");}'
/* L05040 */             . 'function run(){var q=String(input.value||"").replace(/\\s+/g," ").trim();if(q.length<2){close();return;}if(q===last&&box.innerHTML)return;last=q;if(controller)controller.abort();controller=(typeof AbortController!=="undefined")?new AbortController():null;box.innerHTML="<div class=\\"relevanssi-live-search-results pftk-header-search-results-v150414\\" aria-busy=\\"true\\"><div class=\\"relevanssi-live-search-result-status\\"><p>Suche …</p></div></div>";input.setAttribute("aria-expanded","true");var body=new URLSearchParams();body.set("action","pftk_header_search_v150414");body.set("nonce",nonce);body.set("q",q);fetch(ajax,{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"},body:body.toString(),signal:controller?controller.signal:undefined}).then(function(r){return r.json();}).then(function(data){if(String(input.value||"").replace(/\\s+/g," ").trim()!==q)return;box.innerHTML=(data&&data.success&&data.data&&typeof data.data.html==="string")?data.data.html:"";input.setAttribute("aria-expanded",box.innerHTML?"true":"false");}).catch(function(err){if(err&&err.name==="AbortError")return;close();});}'
/* L05041 */             . 'input.addEventListener("input",function(){clearTimeout(timer);timer=setTimeout(run,180);});'
/* L05042 */             . 'input.addEventListener("keydown",function(e){if(e.key==="Escape"){close();input.blur();}});'
/* L05043 */             . 'document.addEventListener("click",function(e){if(e.target!==input&&!box.contains(e.target)&&!input.form.contains(e.target))close();});'
/* L05044 */             . '})();</script>';
/* L05045 */     }
/* L05046 */ 
/* L05047 */     /**
/* L05048 */      * V1.50.414: Reale Affiliate-Produkte werden als ruhige Portal-Karte
/* L05049 */      * dargestellt: ein Rahmen nur um Bild/Titel/Preis, CTA darunter.
/* L05050 */      * Provider-Markup, Beschreibung, Status und interne Buttons bleiben nicht
/* L05051 */      * sichtbar. Der vorhandene Provisionshinweis wird einmal pro Raster ausserhalb
/* L05052 */      * der Karten gezeigt und inhaltlich nicht umformuliert.
/* L05053 */      */
/* L05054 */     public static function print_real_affiliate_product_css_v150414() {
/* L05055 */         if (is_admin()) { return; }
/* L05056 */         echo <<<'PFTK414AFFCSS'
/* L05057 */ <style id="pftk-real-affiliate-products-v150414">
/* L05058 */ .pa255-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-1,.pa266-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-1,.pa272-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-1,.pa273-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-1{grid-template-columns:minmax(0,340px)!important;justify-content:center!important}
/* L05059 */ .pa255-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-2,.pa266-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-2,.pa272-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-2,.pa273-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-2{grid-template-columns:repeat(2,minmax(0,340px))!important;justify-content:center!important}
/* L05060 */ .pa255-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-3,.pa266-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-3,.pa272-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-3,.pa273-product-grid[data-pftk-affiliate-real-grid-v150414="1"].count-3{grid-template-columns:repeat(3,minmax(0,340px))!important;justify-content:center!important}

/* ===== ORIGINAL LINES 5155-5210 ===== */
/* L05155 */     if(price){var p=document.createElement('span');p.setAttribute('data-pftk-affiliate-price-v150414','1');p.textContent=price;bodyLink.appendChild(p);}
/* L05156 */     shell.appendChild(bodyLink);card.appendChild(shell);
/* L05157 */     var cta=document.createElement('a');cta.setAttribute('data-pftk-affiliate-cta-v150414','1');cloneLinkAttrs(link,cta);cta.textContent=provider.cta;card.appendChild(cta);
/* L05158 */   }
/* L05159 */   function scan(){document.querySelectorAll(CARD_SELECTOR).forEach(decorate);}
/* L05160 */   if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scan,{once:true});else scan();
/* L05161 */   new MutationObserver(scan).observe(document.documentElement,{childList:true,subtree:true});
/* L05162 */ })();
/* L05163 */ </script>
/* L05164 */ PFTK414AFFJS;
/* L05165 */     }
/* L05166 */ 
/* L05167 */     public static function relevanssi_live_search_published_only_v150297($args) {
/* L05168 */         $args = is_array($args) ? $args : [];
/* L05169 */         $args['post_status'] = 'publish';
/* L05170 */         // V1.50.408: Fuer das Header-Dropdown holen wir einen groesseren neutralen
/* L05171 */         // Relevanssi-Pool, damit bereits von Relevanssi gelieferte Taxonomie-Treffer
/* L05172 */         // erhalten bleiben. Sichtbar bleiben spaeter dennoch maximal 5 je Gruppe.
/* L05173 */         if (self::is_header_live_search_request_v150408()) {
/* L05174 */             $args['posts_per_page'] = 50;
/* L05175 */         }
/* L05176 */         return $args;
/* L05177 */     }
/* L05178 */ 
/* L05179 */     public static function render_brand_header_v15065() {
/* L05180 */         if (is_admin()) { return; }
/* L05181 */         $location = self::brand_menu_location_v15065();
/* L05182 */         $logo = plugin_dir_url(__FILE__) . 'assets/pferde-atelier-logo-pferd-b.png';
/* L05183 */         $brand = self::brand_settings_v15065();
/* L05184 */         $tagline = trim((string)($brand['header_tagline'] ?? ''));
/* L05185 */         echo '<header class="pftk-brand-header-v15065" aria-label="Pferde Atelier Hauptkopf">';
/* L05186 */         echo '<div class="pftk-brand-top-v15065"><a class="pftk-brand-lockup-v15065" href="' . esc_url(home_url('/')) . '">';
/* L05187 */         echo '<img src="' . esc_url($logo) . '" alt="" width="72" height="72">';
/* L05188 */         echo self::brand_wordmark_html_v15065($tagline, false) . '</a>';
/* L05189 */         echo '<button class="pftk-mobile-main-toggle-v15071" type="button" aria-expanded="false" aria-controls="pftk-main-navigation-v15071"><span></span><span></span><span></span><b class="screen-reader-text">Hauptmenü öffnen</b></button>';
/* L05190 */         echo '<form class="pftk-brand-search-v15065 search-form" role="search" method="get" action="' . esc_url(home_url('/')) . '"><label class="screen-reader-text" for="pftk-brand-search-field">Suche</label><input id="pftk-brand-search-field" class="search-field" type="search" name="s" placeholder="Suchen …" value="' . esc_attr(get_search_query()) . '" autocomplete="off" aria-autocomplete="list" aria-expanded="false" aria-controls="pftk-brand-live-results-v150297"><input type="hidden" name="pftk_header_search" value="1"><button type="submit" aria-label="Suche starten"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m16 16 4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></button><div id="pftk-brand-live-results-v150297" class="pftk-brand-live-results-v150297" aria-live="polite"></div></form></div>';
/* L05191 */         echo '<div class="pftk-brand-nav-v15065">';
/* L05192 */         if ($location !== '') {
/* L05193 */             add_filter('wp_nav_menu_objects', [__CLASS__, 'brand_menu_remove_hivepress_account_v150114'], 10000, 2);
/* L05194 */             add_filter('wp_nav_menu_objects', [__CLASS__, 'brand_menu_preview_items_v15069'], 999, 2);
/* L05195 */             wp_nav_menu([
/* L05196 */                 'theme_location' => $location,
/* L05197 */                 'container' => 'nav',
/* L05198 */                 'container_class' => 'pftk-brand-nav-inner-v15065',
/* L05199 */                 'menu_class' => 'pftk-brand-menu-v15065',
/* L05200 */                 'fallback_cb' => false,
/* L05201 */                 'depth' => 3,
/* L05202 */             ]);
/* L05203 */             remove_filter('wp_nav_menu_objects', [__CLASS__, 'brand_menu_preview_items_v15069'], 999);
/* L05204 */             wp_nav_menu([
/* L05205 */                 'theme_location' => $location,
/* L05206 */                 'container' => 'nav',
/* L05207 */                 'container_id' => 'pftk-main-navigation-v15071',
/* L05208 */                 'container_class' => 'pftk-mobile-nav-v15074',
/* L05209 */                 'menu_class' => 'pftk-mobile-menu-v15074',
/* L05210 */                 'fallback_cb' => false,

/* ===== ORIGINAL LINES 18415-18435 ===== */
/* L18415 */             . '@media(max-width:760px){.pa223-topic>.pa251-icon,.pftk-hub1-topic-v150210>.pa251-icon{width:64px!important;height:64px!important}}'
/* L18416 */             . '</style>';
/* L18417 */     }
/* L18418 */ 
/* L18419 */ }
/* L18420 */ 
/* L18421 */ // V1.50.413: Relevanssi Live Ajax Search erwartet fuer den stabilen
/* L18422 */ // template_function-Pfad einen global aufrufbaren Funktionsnamen.
/* L18423 */ if (!function_exists('pftk_render_grouped_live_search_v150413')) {
/* L18424 */     function pftk_render_grouped_live_search_v150413($mode = 'query_posts') {
/* L18425 */         global $wp_query, $relevanssi_query;
/* L18426 */         $source = ($mode === 'query_posts') ? $wp_query : $relevanssi_query;
/* L18427 */         Pferde_Template_Kit::render_grouped_live_search_v150408($source);
/* L18428 */     }
/* L18429 */ }
/* L18430 */ 
/* L18431 */ Pferde_Template_Kit::init();
/* L18432 */ add_action('wp_head', ['Pferde_Template_Kit', 'print_hub1_css_v150210'], 99);
/* L18433 */ 
/* L18434 */ 
/* L18435 */ /* V1.50.99 – Bildquellen-Regressionsfix aus dem Versionsvergleich V1.50.86 -> V1.50.87.

/* END EXTRACT */