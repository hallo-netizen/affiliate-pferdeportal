#!/usr/bin/env bash
set -euo pipefail
P26=/tmp/uge026/universal-glossary-engine

test -f "$P26/universal-glossary-engine.php"
grep -q 'Version: 0.2.6' "$P26/universal-glossary-engine.php"

cp -a "$P26"/. /tmp/runtime-plugin/universal-glossary-engine/
grep -q 'Version: 0.2.6' /tmp/runtime-plugin/universal-glossary-engine/universal-glossary-engine.php

SCHEMA=$(docker exec db mysql -uwp -pwp wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")
test "$SCHEMA" = 4

curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/post-upgrade-home
SCHEMA=$(docker exec db mysql -uwp -pwp wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")
test "$SCHEMA" = 5

docker exec db mysql -uwp -pwp wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='rewrite_rules'" | grep -q 'glossar/begriff'

test "$(curl -sS -o /tmp/post-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/post-term
grep -q FULL-HUFBEIN-SENTINEL /tmp/post-term
! grep -qiE 'fatal error|critical error' /tmp/post-term

echo UGE026_AUTOMATIC_REWRITE_MIGRATION_PASS
