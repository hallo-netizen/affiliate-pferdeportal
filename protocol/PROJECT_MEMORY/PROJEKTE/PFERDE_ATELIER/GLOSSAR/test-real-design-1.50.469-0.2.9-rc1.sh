#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
EXPECTED=580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5

# Build fresh runtime and deterministic glossary data.
bash "$R/test-fresh-0.2.9-rc1.sh"

# Replace the seed contract stub with exact real Pferde Design 1.50.469.
bash "$R/reconstruct-design-1.50.469.sh"
test "$(sha256sum /tmp/design-1.50.469/pferde-template-kit.php | awk '{print $1}')" = "$EXPECTED"
docker exec wp wp plugin deactivate affiliate-portal-template-kit --allow-root >/dev/null || true
docker exec wp rm -rf /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker exec wp mkdir -p /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker cp /tmp/design-1.50.469/pferde-template-kit.php wp:/var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php
docker exec wp php -l /var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php
docker exec wp wp plugin activate affiliate-portal-template-kit/pferde-template-kit.php --allow-root >/dev/null
test "$(docker exec wp wp plugin get affiliate-portal-template-kit/pferde-template-kit.php --field=version --allow-root)" = 1.50.469
test "$(docker exec wp wp eval --allow-root 'echo class_exists("Pferde_Template_Kit",false) ? "1" : "0";')" = 1
echo REAL_DESIGN_150469_RUNTIME_IDENTITY_PASS

# Deliberately remove all persisted Glossar rewrite rules again AFTER real Design
# is active while schema already says 7. A live cache/rewrite failure must not be
# able to make rendered cards lead to nowhere anymore.
docker exec wp wp eval --allow-root '$r=(array)get_option("rewrite_rules",[]);foreach(array_keys($r) as $k){if(strpos((string)$k,"glossar")!==false)unset($r[$k]);}update_option("rewrite_rules",$r,false);'
test "$(docker exec wp wp eval --allow-root 'echo get_option(UGE_Core::REWRITE_SCHEMA_OPTION,"");')" = 7
RULES=$(docker exec wp wp option get rewrite_rules --format=json --allow-root)
if printf '%s' "$RULES" | grep -q 'glossar'; then echo REAL_DESIGN_GLOSSAR_RULE_DELETE_FAILED >&2; exit 1; fi

# Server-side checks under exact real Design and zero persisted Glossar rules.
test "$(curl -sS -o /tmp/rd-home -w '%{http_code}' http://127.0.0.1:8080/glossar/)" = 200
grep -q '<span>WISSEN</span><h1>' /tmp/rd-home
! grep -qiE 'fatal error|critical error' /tmp/rd-home

test "$(curl -sS -o /tmp/rd-cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'class="uge-category-head"' /tmp/rd-cat
grep -q 'class="uge-hero' /tmp/rd-cat
grep -q 'class="uge-tools"' /tmp/rd-cat
grep -q 'class="uge-topic-nav"' /tmp/rd-cat
grep -q '>Gesundheit<' /tmp/rd-cat
grep -q '/glossar/begriff/hufbein/' /tmp/rd-cat
! grep -qiE 'fatal error|critical error' /tmp/rd-cat

test "$(curl -sS -o /tmp/rd-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/rd-term
grep -q '<h1[^>]*>Hufbein</h1>' /tmp/rd-term
grep -q FULL-HUFBEIN-SENTINEL /tmp/rd-term
! grep -qiE 'fatal error|critical error' /tmp/rd-term

test "$(curl -sS -o /tmp/rd-missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/rd-draft -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)" = 404

python3 -m pip install --quiet playwright
python3 -m playwright install chromium
python3 "$R/real-design-runtime-browser-029.py"

echo UGE029RC1_REAL_DESIGN_150469_ZERO_REWRITE_FULL_POSITIVE_NEGATIVE_PASS
