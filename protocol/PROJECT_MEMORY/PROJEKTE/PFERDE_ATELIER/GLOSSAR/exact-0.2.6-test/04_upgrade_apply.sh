#!/usr/bin/env bash
set -euo pipefail
P26=/tmp/uge026/universal-glossary-engine

test -f "$P26/universal-glossary-engine.php"
grep -q 'Version: 0.2.6' "$P26/universal-glossary-engine.php"

# Build an ephemeral update ZIP for the test only. It is not a release artifact.
rm -f /tmp/uge026-upgrade.zip
(cd /tmp/uge026 && zip -X -qr /tmp/uge026-upgrade.zip universal-glossary-engine)
unzip -t /tmp/uge026-upgrade.zip | grep -q 'No errors detected'
docker cp /tmp/uge026-upgrade.zip wp:/tmp/uge026-upgrade.zip

SCHEMA=$(docker exec db mysql -uroot -pr wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")
echo "UGE026_SCHEMA_PRE_UPDATE=$SCHEMA"
test "$SCHEMA" = 4

# Use WordPress' own plugin installer/overwrite path instead of raw cp over a live PHP process.
docker exec wp wp plugin install /tmp/uge026-upgrade.zip --force --allow-root >/tmp/wp-upgrade-output
cat /tmp/wp-upgrade-output

echo 'UGE026_INSTALLED_FILE_HEADER:'
docker exec wp grep -F 'Version: 0.2.6' /var/www/html/wp-content/plugins/universal-glossary-engine/universal-glossary-engine.php
echo 'UGE026_INSTALLED_CORE_SCHEMA:'
docker exec wp grep -F "REWRITE_SCHEMA_VERSION = '5'" /var/www/html/wp-content/plugins/universal-glossary-engine/includes/class-uge-core.php

echo 'UGE026_PHP_OPCACHE:'
docker exec wp php -i | grep -E '^opcache.enable =>|^opcache.validate_timestamps =>' || true

# The updater command booted under 0.2.5 before replacing files; stored schema must still be 4.
SCHEMA=$(docker exec db mysql -uroot -pr wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")
echo "UGE026_SCHEMA_PRE_FIRST_NEW_REQUEST=$SCHEMA"
test "$SCHEMA" = 4

# First normal web request under the installed 0.2.6 must migrate 4 -> 5.
curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/post-upgrade-home
SCHEMA=$(docker exec db mysql -uroot -pr wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")
echo "UGE026_SCHEMA_POST_REQUEST=$SCHEMA"
test "$SCHEMA" = 5

docker exec db mysql -uroot -pr wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='rewrite_rules'" | grep -q 'glossar/begriff'

test "$(curl -sS -o /tmp/post-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/post-term
grep -q FULL-HUFBEIN-SENTINEL /tmp/post-term
! grep -qiE 'fatal error|critical error' /tmp/post-term

echo UGE026_WORDPRESS_UPDATE_REWRITE_MIGRATION_PASS
