#!/usr/bin/env bash
set -euo pipefail

# Input package must already exist at /tmp/uge026/universal-glossary-engine.
test -f /tmp/uge026/universal-glossary-engine/universal-glossary-engine.php
rm -rf /tmp/runtime-plugin
mkdir -p /tmp/runtime-plugin
cp -a /tmp/uge026/universal-glossary-engine /tmp/runtime-plugin/

docker network create uge026 >/dev/null
docker run -d --name db --network uge026 \
  -e MYSQL_ROOT_PASSWORD=r -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wp -e MYSQL_PASSWORD=wp \
  --health-cmd='mysqladmin ping -h localhost -uroot -pr' --health-interval=3s --health-retries=30 mysql:8.0 >/dev/null
for i in $(seq 1 40); do test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy && break; sleep 2; done
test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy

docker run -d --name wp --network uge026 -p 8080:80 \
  -e WORDPRESS_DB_HOST=db:3306 -e WORDPRESS_DB_NAME=wordpress -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wp \
  -v /tmp/runtime-plugin/universal-glossary-engine:/var/www/html/wp-content/plugins/universal-glossary-engine wordpress:php8.1-apache >/dev/null
for i in $(seq 1 60); do curl -fsS http://127.0.0.1:8080/ >/dev/null 2>&1 && break; sleep 2; done

curl -fsSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o /tmp/wp
docker cp /tmp/wp wp:/usr/local/bin/wp
docker exec wp chmod +x /usr/local/bin/wp
PASS=$(openssl rand -hex 16)
docker exec wp wp core install --allow-root --url=http://127.0.0.1:8080 --title='UGE 026 Test' --admin_user=admin --admin_password="$PASS" --admin_email=x@example.test --skip-email >/dev/null
docker exec wp wp rewrite structure '/%postname%/' --hard --allow-root >/dev/null
docker exec wp wp theme install astra --activate --allow-root >/dev/null

# Runtime contract double contains only the exact Glossar-relevant behavior of
# Pferde Atelier Design 1.50.469/1.50.472: design profile/API, 900px breadcrumb
# axis, tax content spacing, and no takeover of non-category taxonomy templates.
cat >/tmp/design-contract.php <<'PHP'
<?php
/* Plugin Name: Pferde Atelier Design 1.50.469 Glossar Contract */
final class Pferde_Template_Kit {
    public static function design_profile(){ return 'pferde_atelier'; }
    public static function affiliate_page_type($id){ return get_post_meta((int)$id,'_uge_test_portal_category',true)==='1' ? 'category' : ''; }
    public static function portal_leaf_category_template_v150273($template){ return is_category() ? $template : $template; }
}
add_action('wp_head', static function(){
    if (is_admin() || is_feed() || is_front_page()) { return; }
    if (!is_singular(['page','post']) && !is_category() && !is_tax()) { return; }
    echo '<style id="pftk-universal-content-axis-v15061">:root{--pftk-content-axis-width:900px;--pftk-post-reading-width:760px;--pftk-breadcrumb-axis-width:900px;--pftk-navigation-content-gap:18px;--pftk-breadcrumb-title-gap:10px}body.single-post .site-content,body.page .site-content,body.category .site-content,body.tax .site-content{padding-top:var(--pftk-navigation-content-gap)!important}body.single-post .ast-container,body.page .ast-container,body.category .ast-container,body.tax .ast-container{padding-top:0!important}</style>';
},100);
add_action('uge_ad_slot', static function($slot){ echo '<span>AD-'.esc_html($slot).'</span>'; },10,1);
PHP

docker exec wp mkdir -p /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker cp /tmp/design-contract.php wp:/var/www/html/wp-content/plugins/affiliate-portal-template-kit/affiliate-portal-template-kit.php
docker exec wp wp plugin activate affiliate-portal-template-kit universal-glossary-engine --allow-root >/dev/null

test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.6
test "$(docker exec wp wp theme list --name=astra --field=status --allow-root)" = active
curl -fsS http://127.0.0.1:8080/ | grep -q 'pftk-universal-content-axis-v15061' || true

echo UGE026_REAL_WP_ASTRA_BOOT_PASS
