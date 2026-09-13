#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
EXPECTED=580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5

bash "$R/test-fresh-0.2.10-rc2.sh"

bash "$R/reconstruct-design-1.50.469.sh"
test "$(sha256sum /tmp/design-1.50.469/pferde-template-kit.php | awk '{print $1}')" = "$EXPECTED"
docker exec wp wp plugin deactivate affiliate-portal-template-kit --allow-root >/dev/null || true
docker exec wp rm -rf /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker exec wp mkdir -p /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker cp /tmp/design-1.50.469/pferde-template-kit.php wp:/var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php
docker exec wp wp plugin activate affiliate-portal-template-kit/pferde-template-kit.php --allow-root >/dev/null
test "$(docker exec wp wp plugin get affiliate-portal-template-kit/pferde-template-kit.php --field=version --allow-root)" = 1.50.469

# Worst-case rewrite poison stays mandatory.
docker exec wp wp eval --allow-root '$r=(array)get_option("rewrite_rules",[]);foreach(array_keys($r) as $k){if(strpos((string)$k,"glossar")!==false)unset($r[$k]);}update_option("rewrite_rules",$r,false);'
RULES=$(docker exec wp wp option get rewrite_rules --format=json --allow-root)
if printf '%s' "$RULES" | grep -q 'glossar'; then echo GLOSSAR_RULE_DELETE_FAILED >&2; exit 1; fi

# Exact blank-single failure class: preserve the valid singular query/status but
# empty only the main-loop posts after query parsing. 0.2.9's while(have_posts())
# then rendered header/footer only. 0.2.10 resolves the requested glossary post
# directly from the URL and must still render the article.
cat >/tmp/uge-loop-poison.php <<'PHP'
<?php
/* Plugin Name: UGE Single Loop Poison Test */
add_action('wp', static function() {
    $uri = isset($_SERVER['REQUEST_URI']) ? (string)$_SERVER['REQUEST_URI'] : '';
    if (!str_contains($uri, '/glossar/begriff/')) { return; }
    global $wp_query;
    if (!$wp_query instanceof WP_Query) { return; }
    $wp_query->posts = [];
    $wp_query->post = null;
    $wp_query->post_count = 0;
    $wp_query->current_post = -1;
}, 9999);
PHP
docker exec wp mkdir -p /var/www/html/wp-content/mu-plugins
docker cp /tmp/uge-loop-poison.php wp:/var/www/html/wp-content/mu-plugins/uge-loop-poison.php

test "$(curl -sS -o /tmp/home-rd -w '%{http_code}' http://127.0.0.1:8080/glossar/)" = 200
! grep -Fq 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' /tmp/home-rd

test "$(curl -sS -o /tmp/cat-rd -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'class="uge-category-head"' /tmp/cat-rd
grep -q '/glossar/begriff/hufbein/' /tmp/cat-rd
! grep -Fq 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' /tmp/cat-rd

test "$(curl -sS -o /tmp/term-rd -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/term-rd
grep -q '<h1[^>]*>Hufbein</h1>' /tmp/term-rd
grep -q FULL-HUFBEIN-SENTINEL /tmp/term-rd
grep -q 'class="uge-primary-category"' /tmp/term-rd
! grep -qiE 'fatal error|critical error' /tmp/term-rd

python3 -m pip install --quiet playwright
python3 -m playwright install chromium
python3 "$R/real-design-runtime-browser-0210.py"

echo UGE0210RC2_REAL_DESIGN_BLANK_SINGLE_BREADCRUMB_POSITIVE_NEGATIVE_PASS
