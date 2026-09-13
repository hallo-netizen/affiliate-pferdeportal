#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/exact-0.2.6-test/01_build.sh"
rm -rf /tmp/uge027 && cp -a /tmp/uge026 /tmp/uge027
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/uge027/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text(); assert s.count('Version: 0.2.6')==1; assert s.count("define('UGE_VERSION', '0.2.6');")==1
p.write_text(s.replace('Version: 0.2.6','Version: 0.2.7').replace("define('UGE_VERSION', '0.2.6');","define('UGE_VERSION', '0.2.7');"))
PY

grep -q 'Version: 0.2.7' /tmp/uge027/universal-glossary-engine/universal-glossary-engine.php
grep -q "REWRITE_SCHEMA_VERSION = '5'" /tmp/uge027/universal-glossary-engine/includes/class-uge-core.php

rm -rf /tmp/runtime-plugin
mkdir -p /tmp/runtime-plugin
cp -a /tmp/uge026/universal-glossary-engine /tmp/runtime-plugin/
mkdir -p /tmp/runtime-plugin/affiliate-portal-template-kit
cat >/tmp/runtime-plugin/affiliate-portal-template-kit/affiliate-portal-template-kit.php <<'PHP'
<?php
/* Plugin Name: Pferde Atelier Design Glossar Diagnostic Contract */
final class Pferde_Template_Kit { public static function design_profile(){return 'pferde_atelier';} public static function affiliate_page_type($id){return get_post_meta((int)$id,'_uge_test_portal_category',true)==='1'?'category':'';} }
PHP

docker network create ugelivefail >/dev/null
docker run -d --name db --network ugelivefail -e MYSQL_ROOT_PASSWORD=r -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wp -e MYSQL_PASSWORD=wp --health-cmd='mysqladmin ping -h localhost -uroot -pr' --health-interval=3s --health-retries=30 mysql:8.0 >/dev/null
for i in $(seq 1 40); do test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy && break; sleep 2; done
docker run -d --name wp --network ugelivefail -p 8080:80 -e WORDPRESS_DB_HOST=db:3306 -e WORDPRESS_DB_NAME=wordpress -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wp -v /tmp/runtime-plugin:/var/www/html/wp-content/plugins wordpress:php8.1-apache >/dev/null
for i in $(seq 1 60); do curl -fsS http://127.0.0.1:8080/ >/dev/null 2>&1 && break; sleep 2; done
curl -fsSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o /tmp/wp
docker cp /tmp/wp wp:/usr/local/bin/wp
docker exec wp chmod +x /usr/local/bin/wp
PASS=$(openssl rand -hex 16)
docker exec wp wp core install --allow-root --url=http://127.0.0.1:8080 --title='UGE Livefail Diagnostic' --admin_user=admin --admin_password="$PASS" --admin_email=x@example.test --skip-email >/dev/null
docker exec wp wp rewrite structure '/%postname%/' --hard --allow-root >/dev/null
docker exec wp wp theme install astra --activate --allow-root >/dev/null
docker exec wp wp plugin activate affiliate-portal-template-kit universal-glossary-engine --allow-root >/dev/null
bash "$R/exact-0.2.5-test/03_seed.sh"

test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.6
test "$(docker exec db mysql -uroot -pr wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")" = 5
curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/home-clean
curl -fsS http://127.0.0.1:8080/glossar/gesundheit/ -o /tmp/cat-clean
grep -q 'class="uge-hero' /tmp/home-clean
grep -q 'class="uge-category-head"' /tmp/cat-clean
! grep -q 'class="uge-hero' /tmp/cat-clean
echo UGE_CLEAN_CATEGORY_DISTINCT_PASS

F=/tmp/uge026/universal-glossary-engine/includes/class-uge-frontend.php
grep -Fq '</form><div class="uge-search-suggestions" hidden></div>' "$F"
grep -Fq '.uge-search-suggestions{position:absolute' "$F"
! grep -Fq '.uge-tools{position:relative' "$F"
echo UGE_AJAX_OVERLAY_BUG_REPRODUCED
grep -Fq '.uge-hero{position:relative;min-height:360px' "$F"
grep -Fq '.uge-hero-image{position:absolute!important;inset:0!important;width:100%!important;height:100%!important' "$F"
grep -Fq '@media(max-width:720px)' "$F"
echo UGE_RESPONSIVE_GAP_REPRODUCED

docker exec wp wp eval --allow-root '$r=(array)get_option("rewrite_rules",[]);foreach(array_keys($r) as $k){if(strpos((string)$k,"glossar")===0)unset($r[$k]);}update_option("rewrite_rules",$r,false);'
test "$(docker exec db mysql -uroot -pr wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")" = 5
! docker exec wp wp option get rewrite_rules --format=json --allow-root | grep -q 'glossar/begriff'

(cd /tmp/uge027 && zip -X -qr /tmp/uge027-upgrade.zip universal-glossary-engine)
docker cp /tmp/uge027-upgrade.zip wp:/tmp/uge027-upgrade.zip
docker exec wp wp plugin install /tmp/uge027-upgrade.zip --force --allow-root >/dev/null
sleep 3
curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/027-home
test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.7
test "$(docker exec db mysql -uroot -pr wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")" = 5
! docker exec wp wp option get rewrite_rules --format=json --allow-root | grep -q 'glossar/begriff'
TC=$(curl -sS -o /tmp/027-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)
CC=$(curl -sS -o /tmp/027-cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)
echo "UGE_027_AFTER_026_TERM_HTTP=$TC UGE_027_AFTER_026_CAT_HTTP=$CC"
test "$TC" != 200 || ! grep -q '<article class="uge-single-wrap"' /tmp/027-term
test "$CC" != 200 || ! grep -q 'class="uge-category-head"' /tmp/027-cat
echo UGE_026_TO_027_UNCHANGED_SCHEMA_BUG_REPRODUCED
echo UGE_LIVEFAIL_DIAGNOSTIC_COMPLETE_NO_RELEASE
