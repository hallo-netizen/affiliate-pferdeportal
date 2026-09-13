#!/usr/bin/env bash
set -euo pipefail
BASE=${1:?base version 0.2.6 or 0.2.7 required}
case "$BASE" in 0.2.6|0.2.7) ;; *) echo BAD_BASE >&2; exit 2;; esac
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR

bash "$R/build-0.2.8-rc1.sh"
RC=/tmp/uge028rc1/universal-glossary-engine

test -f "$RC/universal-glossary-engine.php"
grep -q 'Version: 0.2.8-rc1' "$RC/universal-glossary-engine.php"
grep -q "REWRITE_SCHEMA_VERSION = '6'" "$RC/includes/class-uge-core.php"

# Build exact predecessor from the same bound chain.
bash "$R/exact-0.2.6-test/01_build.sh"
if [ "$BASE" = 0.2.6 ]; then
  rm -rf /tmp/base-plugin
  cp -a /tmp/uge026/universal-glossary-engine /tmp/base-plugin
else
  rm -rf /tmp/base-plugin
  cp -a /tmp/uge026/universal-glossary-engine /tmp/base-plugin
  python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/base-plugin/universal-glossary-engine.php')
s=p.read_text(); assert s.count('Version: 0.2.6')==1; assert s.count("define('UGE_VERSION', '0.2.6');")==1
p.write_text(s.replace('Version: 0.2.6','Version: 0.2.7').replace("define('UGE_VERSION', '0.2.6');","define('UGE_VERSION', '0.2.7');"))
PY
fi

test "$(grep -oE 'Version: 0\.2\.[67]' /tmp/base-plugin/universal-glossary-engine.php | awk '{print $2}')" = "$BASE"
grep -q "REWRITE_SCHEMA_VERSION = '5'" /tmp/base-plugin/includes/class-uge-core.php

rm -rf /tmp/runtime-plugin
mkdir -p /tmp/runtime-plugin
cp -a /tmp/base-plugin /tmp/runtime-plugin/universal-glossary-engine
mkdir -p /tmp/runtime-plugin/affiliate-portal-template-kit
cat >/tmp/runtime-plugin/affiliate-portal-template-kit/affiliate-portal-template-kit.php <<'PHP'
<?php
/* Plugin Name: Pferde Atelier Design Diagnostic Contract */
final class Pferde_Template_Kit { public static function design_profile(){return 'pferde_atelier';} public static function affiliate_page_type($id){return get_post_meta((int)$id,'_uge_test_portal_category',true)==='1'?'category':'';} }
add_action('uge_ad_slot',static function($slot){echo '<span>AD-'.esc_html($slot).'</span>';},10,1);
PHP

docker network create ugeupdate >/dev/null
docker run -d --name db --network ugeupdate -e MYSQL_ROOT_PASSWORD=r -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wp -e MYSQL_PASSWORD=wp --health-cmd='mysqladmin ping -h localhost -uroot -pr' --health-interval=3s --health-retries=30 mysql:8.0 >/dev/null
for i in $(seq 1 40); do test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy && break; sleep 2; done
test "$(docker inspect -f '{{.State.Health.Status}}' db)" = healthy

docker run -d --name wp --network ugeupdate -p 8080:80 -e WORDPRESS_DB_HOST=db:3306 -e WORDPRESS_DB_NAME=wordpress -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wp -v /tmp/runtime-plugin:/var/www/html/wp-content/plugins wordpress:php8.1-apache >/dev/null
for i in $(seq 1 60); do curl -fsS http://127.0.0.1:8080/ >/dev/null 2>&1 && break; sleep 2; done
curl -fsSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o /tmp/wp
docker cp /tmp/wp wp:/usr/local/bin/wp
docker exec wp chmod +x /usr/local/bin/wp
PASS=$(openssl rand -hex 16)
docker exec wp wp core install --allow-root --url=http://127.0.0.1:8080 --title='UGE RC Update Test' --admin_user=admin --admin_password="$PASS" --admin_email=x@example.test --skip-email >/dev/null
docker exec wp wp rewrite structure '/%postname%/' --hard --allow-root >/dev/null
docker exec wp wp theme install astra --activate --allow-root >/dev/null
docker exec wp wp plugin activate affiliate-portal-template-kit universal-glossary-engine --allow-root >/dev/null
bash "$R/exact-0.2.5-test/03_seed.sh"

test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = "$BASE"
test "$(docker exec wp wp eval --allow-root 'echo get_option(UGE_Core::REWRITE_SCHEMA_OPTION,"");')" = 5

# Positive predecessor baseline.
test "$(curl -sS -o /tmp/pre-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/pre-term
test "$(curl -sS -o /tmp/pre-cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'class="uge-category-head"' /tmp/pre-cat
! grep -q 'class="uge-hero' /tmp/pre-cat

# Poison every stored glossary rewrite rule while stored schema remains 5.
# Match "glossar" anywhere in the regex key so ^glossar/... is removed too.
docker exec wp wp eval --allow-root '$r=(array)get_option("rewrite_rules",[]);foreach(array_keys($r) as $k){if(strpos((string)$k,"glossar")!==false)unset($r[$k]);}update_option("rewrite_rules",$r,false);'
test "$(docker exec wp wp eval --allow-root 'echo get_option(UGE_Core::REWRITE_SCHEMA_OPTION,"");')" = 5
RULES=$(docker exec wp wp option get rewrite_rules --format=json --allow-root)
if printf '%s' "$RULES" | grep -q 'glossar'; then echo GLOSSAR_REWRITE_POISON_INCOMPLETE >&2; exit 1; fi
TC=$(curl -sS -o /tmp/broken-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)
CC=$(curl -sS -o /tmp/broken-cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)
if [ "$TC" = 200 ] && grep -q '<article class="uge-single-wrap"' /tmp/broken-term; then echo TERM_POISON_FAILED >&2; exit 1; fi
if [ "$CC" = 200 ] && grep -q 'class="uge-category-head"' /tmp/broken-cat; then echo CAT_POISON_FAILED >&2; exit 1; fi
echo "UGE028RC1_${BASE}_POISON_RED_PASS term=$TC cat=$CC"

# Real WordPress overwrite with RC.
rm -f /tmp/uge028rc1-upgrade.zip
(cd /tmp/uge028rc1 && zip -X -qr /tmp/uge028rc1-upgrade.zip universal-glossary-engine)
docker cp /tmp/uge028rc1-upgrade.zip wp:/tmp/uge028rc1-upgrade.zip
docker exec wp wp plugin install /tmp/uge028rc1-upgrade.zip --force --allow-root >/tmp/wp-update-out
cat /tmp/wp-update-out
sleep 3
# first normal request is allowed to trigger maybe_upgrade_rewrites
curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/rc-home

VERSION=$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)
SCHEMA=$(docker exec wp wp eval --allow-root 'echo get_option(UGE_Core::REWRITE_SCHEMA_OPTION,"");')
echo "UGE028RC1_FROM_${BASE}_VERSION=$VERSION SCHEMA=$SCHEMA"
test "$VERSION" = 0.2.8-rc1
test "$SCHEMA" = 6
docker exec wp wp option get rewrite_rules --format=json --allow-root | grep -q 'glossar/begriff'

# True term renderer, not foreign/blank HTTP 200.
test "$(curl -sS -o /tmp/rc-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/rc-term
grep -q '<h1[^>]*>Hufbein</h1>' /tmp/rc-term
grep -q FULL-HUFBEIN-SENTINEL /tmp/rc-term
! grep -qiE 'fatal error|critical error' /tmp/rc-term

# True category renderer, explicitly not home renderer.
test "$(curl -sS -o /tmp/rc-cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'class="uge-category-head"' /tmp/rc-cat
grep -q '>Gesundheit<' /tmp/rc-cat
grep -q '/glossar/begriff/hufbein/' /tmp/rc-cat
! grep -q 'class="uge-hero' /tmp/rc-cat
! grep -q 'class="uge-tools"' /tmp/rc-cat

# Negative routes.
test "$(curl -sS -o /tmp/missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/draft -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)" = 404

echo "UGE028RC1_UPDATE_FROM_${BASE}_ROUTING_POSITIVE_NEGATIVE_PASS"
