#!/usr/bin/env bash
set -euo pipefail
ROOT=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
P25=/tmp/uge025-tested

test -f "$P25/universal-glossary-engine.php"
grep -q 'Version: 0.2.5' "$P25/universal-glossary-engine.php"

rm -rf /tmp/runtime-plugin
mkdir -p /tmp/runtime-plugin
cp -a "$P25" /tmp/runtime-plugin/universal-glossary-engine

docker network create ugeup >/dev/null
docker run -d --name db --network ugeup -e MYSQL_ROOT_PASSWORD=r -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wp -e MYSQL_PASSWORD=wp --health-cmd='mysqladmin ping -h localhost -uroot -pr' --health-interval=3s --health-retries=30 mysql:8.0 >/dev/null
for i in $(seq 1 40); do test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy && break; sleep 2; done
test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy

docker run -d --name wp --network ugeup -p 8080:80 -e WORDPRESS_DB_HOST=db:3306 -e WORDPRESS_DB_NAME=wordpress -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wp -v /tmp/runtime-plugin/universal-glossary-engine:/var/www/html/wp-content/plugins/universal-glossary-engine wordpress:php8.1-apache >/dev/null
for i in $(seq 1 60); do curl -fsS http://127.0.0.1:8080/ >/dev/null 2>&1 && break; sleep 2; done

curl -fsSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o /tmp/wp
docker cp /tmp/wp wp:/usr/local/bin/wp
docker exec wp chmod +x /usr/local/bin/wp
PASS=$(openssl rand -hex 16)
docker exec wp wp core install --allow-root --url=http://127.0.0.1:8080 --title='UGE Upgrade Test' --admin_user=admin --admin_password="$PASS" --admin_email=x@example.test --skip-email >/dev/null
docker exec wp wp rewrite structure '/%postname%/' --hard --allow-root >/dev/null
docker exec wp wp theme install astra --activate --allow-root >/dev/null

cat >/tmp/design-contract.php <<'PHP'
<?php
/* Plugin Name: Pferde Atelier Design 1.50.469 Glossar Contract */
final class Pferde_Template_Kit {
 public static function design_profile(){return 'pferde_atelier';}
 public static function affiliate_page_type($id){return get_post_meta((int)$id,'_uge_test_portal_category',true)==='1'?'category':'';}
}
add_action('wp_head',static function(){
 if(is_admin()||is_feed()||is_front_page())return;
 if(!is_singular(['page','post'])&&!is_category()&&!is_tax())return;
 echo '<style id="pftk-universal-content-axis-v15061">:root{--pftk-breadcrumb-axis-width:900px;--pftk-navigation-content-gap:18px}body.tax .site-content{padding-top:var(--pftk-navigation-content-gap)!important}body.tax .ast-container{padding-top:0!important}</style>';
},100);
add_action('uge_ad_slot',static function($slot){echo '<span>AD-'.esc_html($slot).'</span>';},10,1);
PHP

docker exec wp mkdir -p /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker cp /tmp/design-contract.php wp:/var/www/html/wp-content/plugins/affiliate-portal-template-kit/affiliate-portal-template-kit.php
docker exec wp wp plugin activate affiliate-portal-template-kit universal-glossary-engine --allow-root >/dev/null
test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.5

bash "$ROOT/exact-0.2.5-test/03_seed.sh"

test "$(docker exec db mysql -uwp -pwp wordpress -Nse \"SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'\")" = 4
docker exec wp wp post list --allow-root --post_type=uge_term --post_status=any --format=count >/tmp/term-count-before
docker exec wp wp eval --allow-root 'echo md5(wp_json_encode(UGE_Config::get()));' >/tmp/config-before

test "$(curl -sS -o /tmp/pre-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/pre-term
grep -q FULL-HUFBEIN-SENTINEL /tmp/pre-term

docker exec wp wp eval --allow-root '$r=get_option("rewrite_rules",[]);foreach(array_keys((array)$r) as $k){if(strpos((string)$k,"glossar/begriff")!==false)unset($r[$k]);}update_option("rewrite_rules",$r,false);' >/dev/null

test "$(curl -sS -o /tmp/broken-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 404
test "$(docker exec db mysql -uwp -pwp wordpress -Nse \"SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'\")" = 4

echo UGE025_POISONED_REWRITE_NEGATIVE_PASS
