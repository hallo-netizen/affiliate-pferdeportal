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
F="$P/includes/class-uge-frontend.php"
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/u/universal-glossary-engine/includes/class-uge-frontend.php')
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
p.write_text(s.replace(old,new))
PY
test "$(sha256sum "$F" | cut -d' ' -f1)" = 0af01357b0ab7bc14c80427bd39076fb1918099f472f9ecbd96f8fc7cf5b5076
test "$(sha256sum "$P/assets/glossar-hero-books-stall.webp" | cut -d' ' -f1)" = 85594735583ee25d318b6a7a98dfdcae2097e95b708107db5feb62edcf3fbdda
grep -q 'Version: 0.2.5' "$P/universal-glossary-engine.php"
grep -q 'uge-topic-icon' "$F"; grep -q 'data-uge-nonce' "$F"; grep -q 'q.length<2' "$F"
! grep -q "'html' => \$html" "$F"
! grep -R 'site-content .ast-container{padding-top:0' "$P"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l
echo UGE025_EXACT_BUILD_LINT_PASS
