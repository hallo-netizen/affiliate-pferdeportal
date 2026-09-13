#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
EXPECTED=580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5

# Establish the already-green RC runtime and deterministic glossary data first.
# This stage may use the old contract stub only as a seed adapter. It is removed
# completely before any real-design assertion below.
bash "$R/test-fresh-0.2.8-rc1.sh"

# Reconstruct and SHA-bind the exact executable 1.50.469 source.
bash "$R/reconstruct-design-1.50.469.sh"
test "$(sha256sum /tmp/design-1.50.469/pferde-template-kit.php | awk '{print $1}')" = "$EXPECTED"

# Remove contract stub. From this point on only exact real 1.50.469 executes.
docker exec wp wp plugin deactivate affiliate-portal-template-kit --allow-root >/dev/null || true
docker exec wp rm -rf /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker exec wp mkdir -p /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker cp /tmp/design-1.50.469/pferde-template-kit.php wp:/var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php

test "$(docker exec wp sha256sum /var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php | awk '{print $1}')" = "$EXPECTED"
docker exec wp php -l /var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php
# Activate exact plugin file, not a directory alias.
docker exec wp wp plugin activate affiliate-portal-template-kit/pferde-template-kit.php --allow-root >/dev/null
test "$(docker exec wp wp plugin get affiliate-portal-template-kit/pferde-template-kit.php --field=version --allow-root)" = 1.50.469
# Fresh CLI request proves real class is loaded after stub deletion.
test "$(docker exec wp wp eval --allow-root 'echo class_exists("Pferde_Template_Kit",false) ? "1" : "0";')" = 1

echo REAL_DESIGN_150469_RUNTIME_IDENTITY_PASS

# Flush after swapping the design plugin so rewrite/filter interactions are real.
docker exec wp wp rewrite flush --hard --allow-root >/dev/null

# Server-side positive/negative routes under exact real Design.
test "$(curl -sS -o /tmp/rd-home -w '%{http_code}' http://127.0.0.1:8080/glossar/)" = 200
test -s /tmp/rd-home
! grep -qiE 'fatal error|critical error' /tmp/rd-home

test "$(curl -sS -o /tmp/rd-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/rd-term
grep -q FULL-HUFBEIN-SENTINEL /tmp/rd-term
! grep -qiE 'fatal error|critical error' /tmp/rd-term

test "$(curl -sS -o /tmp/rd-cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'class="uge-category-head"' /tmp/rd-cat
grep -q '/glossar/begriff/hufbein/' /tmp/rd-cat
! grep -q 'class="uge-hero' /tmp/rd-cat
! grep -q 'class="uge-tools"' /tmp/rd-cat
! grep -qiE 'fatal error|critical error' /tmp/rd-cat

test "$(grep -o 'class="uge-breadcrumbs"' /tmp/rd-cat | wc -l | tr -d ' ')" = 1

test "$(curl -sS -o /tmp/rd-missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/rd-draft -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)" = 404

# Same-name category/term collision remains separated.
test "$(curl -sS -o /tmp/rd-same-term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/gesundheit/)" = 200
grep -q CATEGORY-OVERLAP-SENTINEL /tmp/rd-same-term
! grep -q CATEGORY-OVERLAP-SENTINEL /tmp/rd-cat

# Ordinary WordPress post remains untouched.
normal=$(docker exec wp wp post list --allow-root --post_type=post --name=huf-normaler-beitrag --field=ID)
test -n "$normal"
test "$(docker exec wp wp post get "$normal" --field=post_status --allow-root)" = publish

# Real rendered browser: AJAX placement/results, responsive hero, category vs
# home distinction, real term page and negative routes.
python3 -m pip install --quiet playwright
python3 -m playwright install chromium
python3 "$R/real-design-runtime-browser.py"

echo UGE028RC1_REAL_DESIGN_150469_FULL_POSITIVE_NEGATIVE_PASS
