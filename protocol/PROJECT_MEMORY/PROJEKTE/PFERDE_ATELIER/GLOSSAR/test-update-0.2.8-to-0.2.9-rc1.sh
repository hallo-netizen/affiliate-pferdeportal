#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.8.sh"
bash "$R/build-0.2.9-rc1.sh"

rm -rf /tmp/runtime-plugin
mkdir -p /tmp/runtime-plugin
cp -a /tmp/uge028/universal-glossary-engine /tmp/runtime-plugin/universal-glossary-engine
mkdir -p /tmp/runtime-plugin/affiliate-portal-template-kit
cat >/tmp/runtime-plugin/affiliate-portal-template-kit/affiliate-portal-template-kit.php <<'PHP'
<?php
/* Plugin Name: Pferde Atelier Design Update Contract */
final class Pferde_Template_Kit { public static function design_profile(){return 'pferde_atelier';} public static function affiliate_page_type($id){return get_post_meta((int)$id,'_uge_test_portal_category',true)==='1'?'category':'';} }
add_action('uge_ad_slot',static function($slot){echo '<span>AD-'.esc_html($slot).'</span>';},10,1);
PHP

docker network create uge029update >/dev/null
docker run -d --name db --network uge029update -e MYSQL_ROOT_PASSWORD=r -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wp -e MYSQL_PASSWORD=wp --health-cmd='mysqladmin ping -h localhost -uroot -pr' --health-interval=3s --health-retries=30 mysql:8.0 >/dev/null
for i in $(seq 1 40); do test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy && break; sleep 2; done
test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy

docker run -d --name wp --network uge029update -p 8080:80 -e WORDPRESS_DB_HOST=db:3306 -e WORDPRESS_DB_NAME=wordpress -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wp -v /tmp/runtime-plugin:/var/www/html/wp-content/plugins wordpress:php8.1-apache >/dev/null
for i in $(seq 1 60); do curl -fsS http://127.0.0.1:8080/ >/dev/null 2>&1 && break; sleep 2; done
curl -fsSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o /tmp/wp
docker cp /tmp/wp wp:/usr/local/bin/wp
docker exec wp chmod +x /usr/local/bin/wp
PASS=$(openssl rand -hex 16)
docker exec wp wp core install --allow-root --url=http://127.0.0.1:8080 --title='UGE 029 Update' --admin_user=admin --admin_password="$PASS" --admin_email=x@example.test --skip-email >/dev/null
docker exec wp wp rewrite structure '/%postname%/' --hard --allow-root >/dev/null
docker exec wp wp theme install astra --activate --allow-root >/dev/null
docker exec wp wp plugin activate affiliate-portal-template-kit universal-glossary-engine --allow-root >/dev/null
bash "$R/exact-0.2.5-test/03_seed.sh"

test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.8
test "$(docker exec wp wp eval --allow-root 'echo get_option(UGE_Core::REWRITE_SCHEMA_OPTION,"");')" = 6

# Reproduce the live risk before the update.
docker exec wp wp eval --allow-root '$r=(array)get_option("rewrite_rules",[]);foreach(array_keys($r) as $k){if(strpos((string)$k,"glossar")!==false)unset($r[$k]);}update_option("rewrite_rules",$r,false);'
RULES=$(docker exec wp wp option get rewrite_rules --format=json --allow-root)
if printf '%s' "$RULES" | grep -q 'glossar'; then echo PRE_UPDATE_POISON_FAILED >&2; exit 1; fi

rm -f /tmp/uge029rc1-upgrade.zip
(cd /tmp/uge029rc1 && zip -X -qr /tmp/uge029rc1-upgrade.zip universal-glossary-engine)
docker cp /tmp/uge029rc1-upgrade.zip wp:/tmp/uge029rc1-upgrade.zip
docker exec wp wp plugin install /tmp/uge029rc1-upgrade.zip --force --allow-root >/tmp/wp-update-out
cat /tmp/wp-update-out
curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/home

test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.9-rc1
test "$(docker exec wp wp eval --allow-root 'echo get_option(UGE_Core::REWRITE_SCHEMA_OPTION,"");')" = 7

# Harder than a normal update test: destroy the rules once more after migration.
# With schema already current there will be no schema-triggered repair; links must
# still work through the explicit request binder.
docker exec wp wp eval --allow-root '$r=(array)get_option("rewrite_rules",[]);foreach(array_keys($r) as $k){if(strpos((string)$k,"glossar")!==false)unset($r[$k]);}update_option("rewrite_rules",$r,false);'
test "$(docker exec wp wp eval --allow-root 'echo get_option(UGE_Core::REWRITE_SCHEMA_OPTION,"");')" = 7

test "$(curl -sS -o /tmp/term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/term
grep -q FULL-HUFBEIN-SENTINEL /tmp/term

test "$(curl -sS -o /tmp/cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'class="uge-category-head"' /tmp/cat
grep -q 'class="uge-hero' /tmp/cat
grep -q 'class="uge-tools"' /tmp/cat
grep -q 'class="uge-topic-nav"' /tmp/cat
grep -q '/glossar/begriff/hufbein/' /tmp/cat

test "$(curl -sS -o /tmp/missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/draft -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)" = 404

echo UGE029RC1_UPDATE_FROM_028_ZERO_REWRITE_POSITIVE_NEGATIVE_PASS
