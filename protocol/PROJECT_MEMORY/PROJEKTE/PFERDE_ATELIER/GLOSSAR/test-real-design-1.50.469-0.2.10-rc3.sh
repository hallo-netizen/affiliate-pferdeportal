#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
EXPECTED=580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5

# Historical filename; this harness is bound to the current rc4 bytes.
bash "$R/test-fresh-0.2.10-rc3.sh"

# Real Pferde category recognition is based on true WordPress page hierarchy.
HEALTH_ID=$(docker exec wp wp post list --allow-root --post_type=page --name=gesundheit --field=ID)
ROOT_ID=$(docker exec wp wp post create --allow-root --post_type=page --post_status=publish --post_title='Pferde Wissen' --post_name=pferde-wissen --porcelain)
HUB_ID=$(docker exec wp wp post create --allow-root --post_type=page --post_status=publish --post_title='Gesundheit und Pflege' --post_name=gesundheit-und-pflege --post_parent="$ROOT_ID" --porcelain)
docker exec wp wp post update "$HEALTH_ID" --allow-root --post_parent="$HUB_ID" >/dev/null
test "$(docker exec wp wp eval --allow-root "echo count(get_post_ancestors($HEALTH_ID));")" = 2

bash "$R/reconstruct-design-1.50.469.sh"
test "$(sha256sum /tmp/design-1.50.469/pferde-template-kit.php | awk '{print $1}')" = "$EXPECTED"
docker exec wp wp plugin deactivate affiliate-portal-template-kit --allow-root >/dev/null || true
docker exec wp rm -rf /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker exec wp mkdir -p /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker cp /tmp/design-1.50.469/pferde-template-kit.php wp:/var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php
docker exec wp wp plugin activate affiliate-portal-template-kit/pferde-template-kit.php --allow-root >/dev/null
test "$(docker exec wp wp plugin get affiliate-portal-template-kit/pferde-template-kit.php --field=version --allow-root)" = 1.50.469
test "$(docker exec wp wp eval --allow-root "echo Pferde_Template_Kit::affiliate_page_type($HEALTH_ID);")" = category
echo UGE0210RC4_REAL_DESIGN_CATEGORY_HIERARCHY_PASS

# Bind existing and new glossary terms to the real recognized portal category.
HUFBEIN_ID=$(docker exec wp wp post list --allow-root --post_type=uge_term --name=hufbein --field=ID)
docker exec wp wp eval --allow-root "update_post_meta($HUFBEIN_ID, UGE_Core::meta_key('primary_category_id'), '$HEALTH_ID');"
for slug in hufrehe strahlfaeule hufabszess; do
  ID=$(docker exec wp wp post list --allow-root --post_type=uge_term --name="$slug" --post_status=publish --field=ID)
  test -n "$ID"
  docker exec wp wp eval --allow-root "update_post_meta($ID, UGE_Core::meta_key('primary_category_id'), '$HEALTH_ID');"
done

# Worst-case rewrite state remains mandatory.
docker exec wp wp eval --allow-root '$r=(array)get_option("rewrite_rules",[]);foreach(array_keys($r) as $k){if(strpos((string)$k,"glossar")!==false)unset($r[$k]);}update_option("rewrite_rules",$r,false);'
RULES=$(docker exec wp wp option get rewrite_rules --format=json --allow-root)
if printf '%s' "$RULES" | grep -q 'glossar'; then echo GLOSSAR_RULE_DELETE_FAILED >&2; exit 1; fi

# Reproduce the live white-single failure class by emptying the normal main loop.
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

# Every tested term must still produce a real article, not a white shell.
for slug in hufbein hufrehe strahlfaeule hufabszess; do
  test "$(curl -sS -o /tmp/rd-$slug -w '%{http_code}' "http://127.0.0.1:8080/glossar/begriff/$slug/")" = 200
  grep -q '<article class="uge-single-wrap"' /tmp/rd-$slug
  grep -q '<h1' /tmp/rd-$slug
  grep -q 'class="uge-primary-category"' /tmp/rd-$slug
  ! grep -qiE 'fatal error|critical error' /tmp/rd-$slug
done
grep -q FULL-HUFBEIN-SENTINEL /tmp/rd-hufbein

python3 -m pip install --quiet playwright
python3 -m playwright install chromium
python3 "$R/real-design-runtime-browser-0210.py"

echo UGE0210RC4_REAL_DESIGN_BLANK_SINGLE_POSITIVE_NEGATIVE_PASS
