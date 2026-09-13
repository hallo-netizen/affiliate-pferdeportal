#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.8.sh"
rm -rf /tmp/uge029rc1
cp -a /tmp/uge028 /tmp/uge029rc1
P=/tmp/uge029rc1/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path
import re

# New bytes => new version. 0.2.8 is a real live FAIL and is never reused.
p=Path('/tmp/uge029rc1/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.8') == 1
assert s.count("define('UGE_VERSION', '0.2.8');") == 1
s=s.replace('Version: 0.2.8','Version: 0.2.9-rc1')
s=s.replace("define('UGE_VERSION', '0.2.8');","define('UGE_VERSION', '0.2.9-rc1');")
p.write_text(s)

# Routing must no longer depend solely on the persisted rewrite table.
p=Path('/tmp/uge029rc1/universal-glossary-engine/includes/class-uge-core.php')
s=p.read_text()
assert s.count("const REWRITE_SCHEMA_VERSION = '6';") == 1
s=s.replace("const REWRITE_SCHEMA_VERSION = '6';","const REWRITE_SCHEMA_VERSION = '7';")
hook="        add_action('init', [__CLASS__, 'maybe_upgrade_rewrites'], 99);\n"
assert s.count(hook)==1
s=s.replace(hook, hook + "        add_action('parse_request', [__CLASS__, 'bind_explicit_request'], 1);\n")
needle="    public static function redirect_legacy_term_url(): void {\n"
assert s.count(needle)==1
method=r'''    public static function bind_explicit_request(WP $wp): void {
        if (is_admin() || wp_doing_ajax() || empty($_SERVER['REQUEST_URI'])) { return; }
        $cfg = UGE_Config::get();
        $base = trim((string)$cfg['rewrite_base'], '/');
        $segment = trim((string)$cfg['term_segment'], '/');
        $path = trim((string)wp_parse_url(wp_unslash($_SERVER['REQUEST_URI']), PHP_URL_PATH), '/');
        if ($base === '' || $segment === '' || $path === '') { return; }

        $term_prefix = $base . '/' . $segment . '/';
        if (str_starts_with($path, $term_prefix)) {
            $tail = substr($path, strlen($term_prefix));
            if ($tail === '' || str_contains($tail, '/')) { return; }
            $slug = sanitize_title(rawurldecode($tail));
            $post = $slug !== '' ? get_page_by_path($slug, OBJECT, self::POST_TYPE) : null;
            // Bind the request directly. This remains valid even when a cache/plugin has
            // left WordPress' persisted rewrite_rules option stale or incomplete.
            $wp->query_vars = [
                'post_type' => self::POST_TYPE,
                'name' => ($post instanceof WP_Post && $post->post_status === 'publish') ? $post->post_name : '__uge_missing__',
            ];
            $wp->matched_rule = 'uge-direct-term';
            $wp->matched_query = 'post_type=' . self::POST_TYPE . '&name=' . rawurlencode((string)$wp->query_vars['name']);
            return;
        }

        $group_prefix = $base . '/';
        if (!str_starts_with($path, $group_prefix)) { return; }
        $tail = trim(substr($path, strlen($group_prefix)), '/');
        if ($tail === '' || $tail === $segment) { return; }
        $parts = array_values(array_filter(explode('/', $tail), 'strlen'));
        $slug = $parts ? sanitize_title(rawurldecode((string)end($parts))) : '';
        $group = $slug !== '' ? get_term_by('slug', $slug, self::TAXONOMY) : null;
        if (!$group instanceof WP_Term) { return; }
        $wp->query_vars = [self::TAXONOMY => $group->slug];
        $wp->matched_rule = 'uge-direct-group';
        $wp->matched_query = self::TAXONOMY . '=' . rawurlencode($group->slug);
    }

'''
s=s.replace(needle,method+needle)
p.write_text(s)

p=Path('/tmp/uge029rc1/universal-glossary-engine/includes/class-uge-frontend.php')
s=p.read_text()

# The hero image itself is now the sizing element: normal responsive <img>, no
# fixed height and no artificial aspect-ratio box. Desktop copy overlays it;
# mobile copy moves below it.
s=s.replace('.uge-hero{position:relative;aspect-ratio:5/2;min-height:0;margin:0 0 28px;overflow:hidden;background:#F9F7F2}',
            '.uge-hero{position:relative;min-height:0;margin:0 0 28px;overflow:hidden;background:#F9F7F2}')
s=s.replace('.uge-hero-image{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:cover!important;object-position:center!important;box-shadow:none!important}',
            '.uge-hero-image{display:block!important;position:relative!important;inset:auto!important;width:100%!important;max-width:100%!important;height:auto!important;min-height:0!important;aspect-ratio:auto!important;object-fit:contain!important;object-position:center!important;box-shadow:none!important}')
s=s.replace('.uge-hero-copy{position:relative;z-index:2;display:flex;height:100%;min-height:0;width:min(610px,50%);padding:42px 54px;flex-direction:column;justify-content:center}',
            '.uge-hero-copy{position:absolute;z-index:2;display:flex;inset:0 auto 0 0;height:auto;min-height:0;width:min(610px,50%);padding:42px 54px;flex-direction:column;justify-content:center}')
s=s.replace('.uge-hero-no-image:after{display:none}.uge-hero-no-image .uge-hero-copy{width:100%;max-width:760px}',
            '.uge-hero-no-image{min-height:360px}.uge-hero-no-image:after{display:none}.uge-hero-no-image .uge-hero-copy{width:100%;max-width:760px}')
s=s.replace('.uge-hero{display:flex;min-height:0;aspect-ratio:auto;flex-direction:column}.uge-hero-image{position:relative!important;order:1;width:100%!important;max-width:100%!important;height:auto!important;aspect-ratio:5/2!important;object-fit:cover!important;object-position:right center!important}',
            '.uge-hero{display:flex;min-height:0;flex-direction:column}.uge-hero-image{display:block!important;position:relative!important;order:1;width:100%!important;max-width:100%!important;height:auto!important;min-height:0!important;aspect-ratio:auto!important;object-fit:contain!important;object-position:center!important}')
s=s.replace('.uge-hero-copy{order:2;height:auto;min-height:0;width:100%;padding:25px 22px 28px;background:#F9F7F2}',
            '.uge-hero-copy{position:relative;inset:auto;order:2;height:auto;min-height:0;width:100%;padding:25px 22px 28px;background:#F9F7F2}')

# Locked visual wording from the real Pferde requirement.
old="<span>' . esc_html($cfg['label']) . '</span><h1>"
assert s.count(old)>=1
# Only the hero's first occurrence: category kicker remains category-specific.
s=s.replace(old,"<span>WISSEN</span><h1>",1)

# Category pages are real category pages but use the same complete visual shell
# as the Glossar start page: hero + search/A-Z + icon navigation, then the
# category-specific heading/cards. This replaces the earlier wrong acceptance
# rule that explicitly forbade hero/tools on categories.
pat=r'''    public static function render_category_page\(\): string \{.*?\n    \}\n\n    private static function css\(\): string \{'''
m=re.search(pat,s,re.S)
assert m, 'render_category_page block not found'
new=r'''    public static function render_category_page(): string {
        $term = get_queried_object();
        if (!$term instanceof WP_Term || is_wp_error($term)) { return ''; }
        $cfg = UGE_Config::get();
        $page_content = (int)$cfg['main_page_id'] > 0 ? (string)get_post_field('post_content', (int)$cfg['main_page_id']) : '';
        $paged = max(1, (int)get_query_var('paged'));
        $q = new WP_Query([
            'post_type' => UGE_Core::POST_TYPE,
            'post_status' => 'publish',
            'posts_per_page' => (int)$cfg['category_per_page'],
            'paged' => $paged,
            'orderby' => 'title',
            'order' => 'ASC',
            'tax_query' => [[
                'taxonomy' => UGE_Core::TAXONOMY,
                'field' => 'term_id',
                'terms' => [(int)$term->term_id],
            ]],
        ]);
        ob_start();
        echo '<div class="uge">';
        echo self::render_breadcrumbs($term, null);
        echo self::render_hero($page_content);
        echo self::render_search_tools();
        echo self::render_navigation(true);
        echo '<section class="uge-section uge-category-section">';
        echo '<header class="uge-category-head"><span>WISSEN</span><h1>' . esc_html($term->name) . '</h1>';
        if (!empty($term->description)) { echo '<p>' . esc_html($term->description) . '</p>'; }
        echo '</header>';
        echo self::render_cards($q->posts);
        if (!$q->posts) { echo '<p>In diesem Bereich sind noch keine Begriffe veröffentlicht.</p>'; }
        if ($q->max_num_pages > 1) {
            echo '<nav class="uge-pagination" aria-label="Seitennavigation">';
            echo paginate_links(['total' => (int)$q->max_num_pages, 'current' => $paged, 'type' => 'list']);
            echo '</nav>';
        }
        echo '</section></div>';
        wp_reset_postdata();
        return (string)ob_get_clean();
    }

    private static function css(): string {'''
s=s[:m.start()]+new+s[m.end():]
p.write_text(s)
PY

# Exact guards.
grep -q 'Version: 0.2.9-rc1' "$P/universal-glossary-engine.php"
grep -q "define('UGE_VERSION', '0.2.9-rc1');" "$P/universal-glossary-engine.php"
grep -q "const REWRITE_SCHEMA_VERSION = '7';" "$P/includes/class-uge-core.php"
grep -q "add_action('parse_request', \[__CLASS__, 'bind_explicit_request'\], 1);" "$P/includes/class-uge-core.php"
grep -q 'uge-direct-term' "$P/includes/class-uge-core.php"
grep -q 'uge-direct-group' "$P/includes/class-uge-core.php"
grep -q 'echo self::render_hero($page_content);' "$P/includes/class-uge-frontend.php"
grep -q 'echo self::render_search_tools();' "$P/includes/class-uge-frontend.php"
grep -q 'echo self::render_navigation(true);' "$P/includes/class-uge-frontend.php"
! grep -q 'aspect-ratio:5/2!important' "$P/includes/class-uge-frontend.php"
! grep -q 'position:absolute!important;inset:0!important;width:100%!important;height:100%!important' "$P/includes/class-uge-frontend.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

echo UGE029RC1_BUILD_PASS
