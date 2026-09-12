#!/usr/bin/env bash
set -euo pipefail
T=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR/exact-0.2.5
for spec in part01:8000 part02:8000 part03:8000 part04:8000 part05:8000 part06:8000 part07:16000 part09:16000 part11:16000 part13:11008; do
  f=${spec%%:*}; n=${spec##*:}; test "$(wc -c < "$T/$f.b64")" = "$n"
done
test "$(cat "$T"/part*.b64 | wc -c)" = 107008
cat "$T"/part*.b64 | base64 -d > /tmp/base-0.2.5.zip
test "$(sha256sum /tmp/base-0.2.5.zip | cut -d' ' -f1)" = a0ce7fea3252623aae77cf47cdc5f85e77f6747f46fcf0fca18348351e1c1a7b
rm -rf /tmp/u; mkdir -p /tmp/u
unzip -q /tmp/base-0.2.5.zip -d /tmp/u
P=/tmp/u/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path
root=Path('/tmp/u/universal-glossary-engine')
# AJAX: suggestion response contains only glossary term title + URL.
p=root/'includes/class-uge-frontend.php'
s=p.read_text()
old="""        if ($query === '') {
            wp_send_json_success(['html' => '', 'count' => 0]);
        }
        $posts = self::search_posts($query, 12);
        $headline = 'Suchergebnisse für „' . esc_html($query) . '“';
        $html = '<section class=\"uge-section uge-ajax-results\"><header class=\"uge-section-head\"><h2>' . $headline . '</h2></header>' . self::render_cards($posts) . (!$posts ? '<p>Keine passenden Glossarbegriffe gefunden.</p>' : '') . '</section>';
        $items = array_map(static function($post) {
            return [
                'title' => get_the_title($post),
                'url' => get_permalink($post),
            ];
        }, $posts);
        wp_send_json_success(['html' => $html, 'count' => count($posts), 'items' => $items]);
"""
new="""        if ($query === '') {
            wp_send_json_success(['count' => 0, 'items' => []]);
        }
        $posts = self::search_posts($query, 12);
        $items = array_map(static function($post) {
            return [
                'title' => esc_html(get_the_title($post)),
                'url' => get_permalink($post),
            ];
        }, $posts);
        wp_send_json_success(['count' => count($posts), 'items' => $items]);
"""
if s.count(old) != 1: raise SystemExit(f'ajax block mismatch: {s.count(old)}')
s=s.replace(old,new)
# WordPress returns false, not an empty string, when the Glossar page has no featured image.
# In that normal case the embedded stable/books image must be used.
old="""        if ($image === '') { $image = self::hero_fallback_url(); }
        $image_html = $image !== '' ? sprintf"""
new="""        if (empty($image)) { $image = self::hero_fallback_url(); }
        $image_html = !empty($image) ? sprintf"""
if s.count(old) != 1: raise SystemExit(f'hero fallback mismatch: {s.count(old)}')
s=s.replace(old,new)
# The vertical gap above the hero is owned by the portal/Astra page standard, not by Glossar CSS.
s=s.replace('body.uge-glossary-home .entry-content{margin-top:0!important;padding-top:0!important}', '')
p.write_text(s)

# Legacy /glossar/{term}/ redirects must not steal a real same-named Glossar category URL.
p=root/'includes/class-uge-core.php'
s=p.read_text()
old="""        $slug = sanitize_title(rawurldecode((string)$m[1]));
        if ($slug === '' || $slug === $segment) { return; }
        $post = get_page_by_path($slug, OBJECT, self::POST_TYPE);
"""
new="""        $slug = sanitize_title(rawurldecode((string)$m[1]));
        if ($slug === '' || $slug === $segment) { return; }
        // A real glossary category owns /{base}/{slug}/. Never redirect that URL
        // to a same-named glossary term; the term lives under /{base}/{segment}/{slug}/.
        $group = get_term_by('slug', $slug, self::TAXONOMY);
        if ($group instanceof WP_Term) { return; }
        $post = get_page_by_path($slug, OBJECT, self::POST_TYPE);
"""
if s.count(old) != 1: raise SystemExit(f'legacy redirect mismatch: {s.count(old)}')
p.write_text(s.replace(old,new))
PY
F="$P/includes/class-uge-frontend.php"
C="$P/includes/class-uge-core.php"
test "$(sha256sum "$F" | cut -d' ' -f1)" = 2f3aea25e0c073568157c73d9fb988ff21be11b6421857a992acf479b3505c95
test "$(sha256sum "$C" | cut -d' ' -f1)" = 50bcef85c9bda42b9e8112576c7dc7eca42c636d8b2025533f6c8c9c70f40686
test "$(sha256sum "$P/assets/glossar-hero-books-stall.webp" | cut -d' ' -f1)" = 85594735583ee25d318b6a7a98dfdcae2097e95b708107db5feb62edcf3fbdda
grep -q 'Version: 0.2.5' "$P/universal-glossary-engine.php"
grep -q 'uge-topic-icon' "$F"; grep -q 'data-uge-nonce' "$F"; grep -q 'q.length<2' "$F"
! grep -q "'html' => \$html" "$F"
! grep -R 'site-content .ast-container{padding-top:0' "$P"
! grep -R 'entry-content{margin-top:0!important;padding-top:0!important}' "$P"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l
echo UGE025_EXACT_BUILD_LINT_PASS
