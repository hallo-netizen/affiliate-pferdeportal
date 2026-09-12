<?php
if (!defined('ABSPATH')) { exit; }

final class UGE_Frontend {
    public static function init(): void {
        add_shortcode('universal_glossary', [__CLASS__, 'shortcode']);
        add_filter('the_content', [__CLASS__, 'inject_main_page'], 20);
        add_filter('template_include', [__CLASS__, 'single_template'], 99);
        add_action('wp_enqueue_scripts', [__CLASS__, 'assets']);
        add_filter('body_class', [__CLASS__, 'body_class']);
        add_action('wp_footer', [__CLASS__, 'interactions'], 50);
    }

    public static function body_class(array $classes): array {
        if (is_singular(UGE_Core::POST_TYPE)) { $classes[] = 'uge-term-page'; }
        $cfg = UGE_Config::get();
        if ((int)$cfg['main_page_id'] > 0 && is_page((int)$cfg['main_page_id'])) { $classes[] = 'uge-glossary-page'; }
        return $classes;
    }

    public static function inject_main_page(string $content): string {
        $cfg = UGE_Config::get();
        if (!is_singular('page') || !in_the_loop() || !is_main_query() || (int)$cfg['main_page_id'] !== get_the_ID()) { return $content; }
        if (function_exists('has_shortcode') && has_shortcode($content, 'universal_glossary')) { return $content; }
        return $content . self::render_index();
    }

    public static function shortcode(): string { return self::render_index(); }

    public static function interactions(): void {
        $cfg = UGE_Config::get();
        if (!((int)$cfg['main_page_id'] > 0 && is_page((int)$cfg['main_page_id']))) { return; }
        ?>
        <script>
        (function(){
          var root=document.querySelector('[data-uge-glossary]'); if(!root)return;
          var q=root.querySelector('[data-uge-search]');
          var buttons=root.querySelectorAll('[data-uge-letter]');
          var active='';
          function apply(){
            var needle=q ? q.value.toLowerCase().trim() : '';
            root.querySelectorAll('.uge-term').forEach(function(el){
              var hay=(el.getAttribute('data-uge-title')||'');
              var letter=(el.getAttribute('data-uge-letter')||'');
              el.hidden = !!((needle && hay.indexOf(needle)===-1) || (active && letter!==active));
            });
            root.querySelectorAll('.uge-group').forEach(function(g){
              var visible=[].some.call(g.querySelectorAll('.uge-term'), function(el){return !el.hidden;});
              g.hidden=!visible;
            });
          }
          if(q)q.addEventListener('input',apply);
          buttons.forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();active=(active===b.dataset.ugeLetter?'':b.dataset.ugeLetter);buttons.forEach(function(x){x.setAttribute('aria-pressed',x.dataset.ugeLetter===active?'true':'false')});apply();});});
        })();
        </script>
        <?php
    }

    public static function single_template(string $template): string {
        if (is_singular(UGE_Core::POST_TYPE)) {
            $candidate = UGE_DIR . 'templates/single-uge-term.php';
            if (is_readable($candidate)) { return $candidate; }
        }
        return $template;
    }

    public static function assets(): void {
        $cfg = UGE_Config::get();
        if (!is_singular(UGE_Core::POST_TYPE) && !((int)$cfg['main_page_id'] > 0 && is_page((int)$cfg['main_page_id']))) { return; }
        wp_register_style('uge', false, [], UGE_VERSION);
        wp_enqueue_style('uge');
        wp_add_inline_style('uge', self::css());
    }

    private static function css(): string {
        $t = UGE_Config::design_tokens();
        $vars = sprintf('--uge-accent:%s;--uge-secondary:%s;--uge-ink:%s;--uge-muted:%s;--uge-line:%s;--uge-surface:%s;--uge-radius:%s;--uge-font-size:%s;--uge-line-height:%s;',
            esc_attr($t['accent']), esc_attr($t['secondary']), esc_attr($t['ink']), esc_attr($t['muted']), esc_attr($t['line']), esc_attr($t['surface']), esc_attr($t['radius']), esc_attr($t['font_size']), esc_attr($t['line_height'])
        );
        return '.uge{'.$vars.'color:var(--uge-ink);font-size:var(--uge-font-size);line-height:var(--uge-line-height)}.uge *{box-sizing:border-box}.uge a{color:inherit}.uge-toolbar{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.uge-search{flex:1 1 280px;min-height:44px;padding:10px 14px;border:1px solid var(--uge-line);border-radius:999px}.uge-az{display:flex;gap:6px;flex-wrap:wrap;margin:18px 0 28px}.uge-az a,.uge-group-nav a{display:inline-flex;align-items:center;justify-content:center;min-width:36px;min-height:36px;padding:7px 11px;border:1px solid var(--uge-line);border-radius:999px;text-decoration:none;background:var(--uge-surface)}.uge-group-nav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 30px}.uge-group{margin:30px 0}.uge-group>h2{margin-bottom:14px}.uge-term{border:1px solid var(--uge-line);border-top:0;border-radius:var(--uge-radius);background:var(--uge-surface);overflow:hidden;margin:12px 0;position:relative}.uge-term:before{content:"";position:absolute;left:0;right:0;top:0;height:5px;background:var(--uge-accent);border-radius:var(--uge-radius) var(--uge-radius) 55% 55%}.uge-term summary{cursor:pointer;font-weight:700;padding:22px 22px 16px;list-style:none}.uge-term summary::-webkit-details-marker{display:none}.uge-term-body{padding:0 22px 22px;color:var(--uge-muted)}.uge-term-body p{margin:0 0 12px}.uge-more{font-weight:700;color:var(--uge-accent)!important;text-decoration:none}.uge-single{max-width:900px;margin:0 auto;padding:24px 0}.uge-single-card{border:1px solid var(--uge-line);border-top:0;border-radius:var(--uge-radius);padding:34px;background:var(--uge-surface);position:relative;overflow:hidden}.uge-single-card:before{content:"";position:absolute;left:0;right:0;top:0;height:5px;background:var(--uge-accent)}.uge-kicker{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--uge-accent);font-weight:800}.uge-definition{font-size:18px;color:var(--uge-muted)}@media(max-width:560px){.uge-single-card{padding:26px 20px}.uge-term summary{padding:20px 18px 14px}.uge-term-body{padding:0 18px 20px}}';
    }

    private static function render_index(): string {
        $cfg = UGE_Config::get();
        $posts = get_posts([
            'post_type' => UGE_Core::POST_TYPE,
            'post_status' => 'publish',
            'numberposts' => -1,
            'orderby' => 'title',
            'order' => 'ASC',
        ]);
        $groups = get_terms(['taxonomy' => UGE_Core::TAXONOMY, 'hide_empty' => true]);
        if (is_wp_error($groups)) { $groups = []; }
        $by_group = [];
        foreach ($posts as $post) {
            $assigned = wp_get_post_terms($post->ID, UGE_Core::TAXONOMY);
            $gid = (!is_wp_error($assigned) && !empty($assigned)) ? (int)$assigned[0]->term_id : 0;
            $by_group[$gid][] = $post;
        }
        ob_start();
        echo '<section class="uge" data-uge-glossary>';
        if (!empty($cfg['show_search'])) {
            echo '<div class="uge-toolbar"><input class="uge-search" type="search" placeholder="Begriff suchen …" aria-label="Glossar durchsuchen" data-uge-search></div>';
        }
        if (!empty($cfg['show_az'])) {
            echo '<nav class="uge-az" aria-label="A bis Z">';
            foreach (range('A','Z') as $letter) { printf('<a href="#" role="button" aria-pressed="false" data-uge-letter="%1$s">%1$s</a>', esc_attr($letter)); }
            echo '</nav>';
        }
        if (!empty($cfg['show_groups']) && $groups) {
            echo '<nav class="uge-group-nav" aria-label="Oberbereiche">';
            foreach ($groups as $group) { printf('<a href="#uge-group-%d">%s</a>', (int)$group->term_id, esc_html($group->name)); }
            echo '</nav>';
        }
        foreach ($groups as $group) {
            $items = $by_group[(int)$group->term_id] ?? [];
            if (!$items) { continue; }
            printf('<section class="uge-group" id="uge-group-%d"><h2>%s</h2>', (int)$group->term_id, esc_html($group->name));
            foreach ($items as $post) { echo self::render_term($post); }
            echo '</section>';
        }
        if (!empty($by_group[0])) {
            echo '<section class="uge-group"><h2>Weitere Begriffe</h2>';
            foreach ($by_group[0] as $post) { echo self::render_term($post); }
            echo '</section>';
        }
        if (!$posts) { echo '<p>Es sind noch keine Glossarbegriffe veröffentlicht.</p>'; }
        echo '</section>';
        return (string)ob_get_clean();
    }

    private static function render_term(WP_Post $post): string {
        $definition = UGE_Core::term_value($post->ID, 'short_definition');
        $letter = strtoupper(remove_accents(mb_substr($post->post_title, 0, 1)));
        ob_start();
        printf('<details class="uge-term" data-uge-letter="%s" data-uge-title="%s"><summary>%s</summary><div class="uge-term-body">', esc_attr($letter), esc_attr(strtolower($post->post_title . ' ' . $definition)), esc_html($post->post_title));
        if ($definition !== '') { echo '<p>' . esc_html($definition) . '</p>'; }
        printf('<a class="uge-more" href="%s">Mehr erfahren</a>', esc_url(get_permalink($post)));
        echo '</div></details>';
        return (string)ob_get_clean();
    }
}
