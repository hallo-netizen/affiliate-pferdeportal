#!/usr/bin/env bash
set -euo pipefail
docker network create uge025
docker run -d --name db --network uge025 \
  -e MYSQL_ROOT_PASSWORD=r -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wp -e MYSQL_PASSWORD=wp \
  --health-cmd='mysqladmin ping -h localhost -uroot -pr' --health-interval=3s --health-retries=30 mysql:8.0
for i in $(seq 1 40); do test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy && break; sleep 2; done
test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy
docker run -d --name wp --network uge025 -p 8080:80 \
  -e WORDPRESS_DB_HOST=db:3306 -e WORDPRESS_DB_NAME=wordpress -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wp \
  -v /tmp/u/universal-glossary-engine:/var/www/html/wp-content/plugins/universal-glossary-engine:ro wordpress:php8.1-apache
for i in $(seq 1 60); do curl -fsS http://127.0.0.1:8080/ >/dev/null 2>&1 && break; sleep 2; done
curl -fsSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o /tmp/wp
docker cp /tmp/wp wp:/usr/local/bin/wp; docker exec wp chmod +x /usr/local/bin/wp
PASS=$(openssl rand -hex 16); printf '%s' "$PASS" >/tmp/uge-admin-pass
docker exec wp wp core install --allow-root --url=http://127.0.0.1:8080 --title='UGE Test' --admin_user=admin --admin_password="$PASS" --admin_email=x@example.test --skip-email
docker exec wp wp rewrite structure '/%postname%/' --hard --allow-root
docker exec wp wp theme install astra --activate --allow-root
cat >/tmp/stub.php <<'PHP'
<?php
/* Plugin Name: Pferde Atelier Design Test Stub */
final class Pferde_Template_Kit {
    public static function affiliate_page_type($id){ return get_post_meta((int)$id,'_uge_test_portal_category',true)==='1' ? 'category' : ''; }
    public static function design_profile(){ return 'pferde_atelier'; }
}
add_action('uge_ad_slot', static function($slot){ echo '<span>AD-'.esc_html($slot).'</span>'; }, 10, 1);
PHP
docker exec wp mkdir -p /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker cp /tmp/stub.php wp:/var/www/html/wp-content/plugins/affiliate-portal-template-kit/affiliate-portal-template-kit.php
docker exec wp wp plugin activate affiliate-portal-template-kit universal-glossary-engine --allow-root
test "$(docker exec wp wp plugin get universal-glossary-engine --field=version --allow-root)" = 0.2.5
test "$(docker exec wp wp theme status astra --field=status --allow-root)" = active
echo UGE025_REAL_WP_ASTRA_BOOT_PASS
