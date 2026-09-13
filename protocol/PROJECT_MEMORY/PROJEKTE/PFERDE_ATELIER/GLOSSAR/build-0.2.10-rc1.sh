#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.9.sh"
rm -rf /tmp/uge0210rc1
cp -a /tmp/uge029 /tmp/uge0210rc1
P=/tmp/uge0210rc1/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path

# New bytes => new version. 0.2.9 is a real LIVE FAIL and is never reused.
p=Path('/tmp/uge0210rc1/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.9')==1
assert s.count("define('UGE_VERSION', '0.2.9');")==1
s=s.replace('Version: 0.2.9','Version: 0.2.10-rc1')
s=s.replace("define('UGE_VERSION', '0.2.9');","define('UGE_VERSION', '0.2.10-rc1');")
p.write_text(s)

# Frontend: bind the actual requested single from the URL itself as a final
# runtime truth. Do not depend on the global main-loop still containing the post.
p=Path('/tmp/uge0210rc1/universal-glossary-engine/includes/class-uge-frontend.php')
s=p.read_text()
old="""    public static function is_glossary_view(): bool {
        return self::is_home_page() || is_tax(UGE_Core::TAXONOMY) || is_singular(UGE_Core::POST_TYPE);
    }
"""
new="""    public static function requested_term_post(): ?WP_Post {
        if (empty($_SERVER['REQUEST_URI'])) { return null; }
        $cfg = UGE_Config::get();
        $base = trim((string)$cfg['rewrite_base'], '/');
        $segment = trim((string)$cfg['term_segment'], '/');
        if ($base === '' || $segment === '') { return null; }
        $path = trim((string)wp_parse_url(wp_unslash($_SERVER['REQUEST_URI']), PHP_URL_PATH), '/');
        $prefix = $base . '/' . $segment . '/';
        if (!str_starts_with($path, $prefix)) { return null; }
        $tail = substr($path, strlen($prefix));
        if ($tail === '' || str_contains($tail, '/')) { return null; }
        $slug = sanitize_title(rawurldecode($tail));
        if ($slug === '') { return null; }
        $post = get_page_by_path($slug, OBJECT, UGE_Core::POST_TYPE);
        return ($post instanceof WP_Post && $post->post_status === 'publish') ? $post : null;
    }

    public static function is_glossary_view(): bool {
        return self::is_home_page() || is_tax(UGE_Core::TAXONOMY) || is_singular(UGE_Core::POST_TYPE) || self::requested_term_post() instanceof WP_Post;
    }
"""
assert s.count(old)==1
s=s.replace(old,new)
old="""        if (is_singular(UGE_Core::POST_TYPE)) { $classes[] = 'uge-glossary-term'; }
"""
new="""        if (is_singular(UGE_Core::POST_TYPE) || self::requested_term_post() instanceof WP_Post) { $classes[] = 'uge-glossary-term'; }
"""
assert s.count(old)==1
s=s.replace(old,new)
old="""        if (is_singular(UGE_Core::POST_TYPE)) {
            $candidate = UGE_DIR . 'templates/single-uge-term.php';
            return is_readable($candidate) ? $candidate : $template;
        }
"""
new="""        if (is_singular(UGE_Core::POST_TYPE) || self::requested_term_post() instanceof WP_Post) {
            $candidate = UGE_DIR . 'templates/single-uge-term.php';
            return is_readable($candidate) ? $candidate : $template;
        }
"""
assert s.count(old)==1
s=s.replace(old,new)

# Remove the exact fallback sentence the user rejected. If no excerpt/content is
# configured, render no subtitle at all instead of silently restoring copy.
old="""            $excerpt = $plain !== '' ? wp_trim_words($plain, 28, '…') : 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.';
"""
new="""            $excerpt = $plain !== '' ? wp_trim_words($plain, 28, '…') : '';
"""
assert s.count(old)==1
s=s.replace(old,new)
old="""        return '<section class=\"uge-hero' . ($image === '' ? ' uge-hero-no-image' : '') . '\">' . $image_html . '<div class=\"uge-hero-copy\"><span>WISSEN</span><h1>' . esc_html($title) . '</h1><p>' . esc_html($excerpt) . '</p></div><i aria-hidden=\"true\"></i></section>';
"""
new="""        $excerpt_html = $excerpt !== '' ? '<p>' . esc_html($excerpt) . '</p>' : '';
        return '<section class=\"uge-hero' . ($image === '' ? ' uge-hero-no-image' : '') . '\">' . $image_html . '<div class=\"uge-hero-copy\"><span>WISSEN</span><h1>' . esc_html($title) . '</h1>' . $excerpt_html . '</div><i aria-hidden=\"true\"></i></section>';
"""
assert s.count(old)==1
s=s.replace(old,new)

# Home already had the correct primary top spacing. Apply that exact spacing
# contract to category and term views too; screenshots show taxonomy inherited
# Astra's default #primary top gap because only home was reset.
old='body.uge-glossary-home #primary{margin-top:0!important}'
new='body.uge-glossary-home #primary,body.uge-glossary-category #primary,body.uge-glossary-term #primary{margin-top:0!important}'
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)

# Single template: never render a blank shell merely because another plugin/theme
# emptied or altered the main WordPress loop. Resolve the published glossary post
# directly from the requested URL, set it up, and render exactly that object.
p=Path('/tmp/uge0210rc1/universal-glossary-engine/templates/single-uge-term.php')
s=p.read_text()
old="""get_header();
while (have_posts()) : the_post();
    $groups = wp_get_post_terms(get_the_ID(), UGE_Core::TAXONOMY);
    $nav_group = UGE_Core::navigation_group_for_post(get_the_ID());
"""
new="""get_header();
$uge_post = UGE_Frontend::requested_term_post();
if (!$uge_post instanceof WP_Post) {
    $queried = get_queried_object();
    $uge_post = ($queried instanceof WP_Post && $queried->post_type === UGE_Core::POST_TYPE && $queried->post_status === 'publish') ? $queried : null;
}
if ($uge_post instanceof WP_Post) :
    $GLOBALS['post'] = $uge_post;
    setup_postdata($uge_post);
    $groups = wp_get_post_terms($uge_post->ID, UGE_Core::TAXONOMY);
    $nav_group = UGE_Core::navigation_group_for_post($uge_post->ID);
"""
assert s.count(old)==1
s=s.replace(old,new)
old="""endwhile;
get_footer();
"""
new="""    wp_reset_postdata();
endif;
get_footer();
"""
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)
PY

# Hard build guards.
grep -q 'Version: 0.2.10-rc1' "$P/universal-glossary-engine.php"
grep -q "define('UGE_VERSION', '0.2.10-rc1');" "$P/universal-glossary-engine.php"
grep -q 'public static function requested_term_post' "$P/includes/class-uge-frontend.php"
grep -q 'body.uge-glossary-category #primary' "$P/includes/class-uge-frontend.php"
grep -q 'body.uge-glossary-term #primary' "$P/includes/class-uge-frontend.php"
! grep -R -F 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' "$P"
! grep -q 'while (have_posts())' "$P/templates/single-uge-term.php"
grep -q 'UGE_Frontend::requested_term_post' "$P/templates/single-uge-term.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

echo UGE0210RC1_BUILD_PASS
