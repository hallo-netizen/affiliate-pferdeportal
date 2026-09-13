#!/usr/bin/env bash
set -euo pipefail

# Data/configuration must remain byte-logically identical across the in-place update.
test "$(docker exec wp wp post list --allow-root --post_type=uge_term --post_status=any --format=count)" = "$(cat /tmp/term-count-before)"
test "$(docker exec wp wp eval --allow-root 'echo md5(wp_json_encode(UGE_Config::get()));')" = "$(cat /tmp/config-before)"
test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.6

echo UGE026_DATA_CONFIG_PERSISTENCE_PASS

# The three user-visible frontend repairs must be in the running 0.2.6 output.
grep -Fq 'body.uge-glossary-home #primary{margin-top:0!important}' /tmp/post-upgrade-home
grep -Fq 'var(--pftk-breadcrumb-axis-width,900px)' /tmp/post-upgrade-home
grep -Fq 'aspect-ratio:16/9!important' /tmp/post-upgrade-home
! grep -Fq 'height:240px!important' /tmp/post-upgrade-home

# Category breadcrumb must be real, ordered and rendered on the 900px design axis.
python3 - <<'PY'
import re
s=open('/tmp/cat',encoding='utf8').read()
b=re.search(r'<nav class="uge-breadcrumbs"[^>]*>(.*?)</nav>',s,re.S)
assert b, 'category breadcrumb missing'
bc=b.group(1)
pos=[bc.index(x) for x in ['>Startseite</a>','>Glossar</a>','aria-current="page">Gesundheit</span>']]
assert pos==sorted(pos), pos
assert 'var(--pftk-breadcrumb-axis-width,900px)' in s
PY

echo UGE026_FRONTEND_ACCEPTANCE_PASS

# Deactivate/reactivate is a regression guard, not the migration mechanism.
docker exec wp wp plugin deactivate universal-glossary-engine --allow-root >/dev/null
docker exec wp wp plugin activate universal-glossary-engine --allow-root >/dev/null
SCHEMA=$(docker exec db mysql -uwp -pwp wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")
test "$SCHEMA" = 5
test "$(curl -sS -o /tmp/react-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q FULL-HUFBEIN-SENTINEL /tmp/react-term

echo UGE026_REACTIVATION_NEGATIVE_REGRESSION_PASS
