#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.8.sh"
# Reuse proven boot harness but bind it to exact final source path/version.
rm -rf /tmp/uge028final
cp -a /tmp/uge028 /tmp/uge028final
SRC="$R/exact-0.2.6-test/02_boot.sh"
sed -e 's#/tmp/uge026#/tmp/uge028final#g' -e 's/0\.2\.6/0.2.8/g' -e 's/UGE026/UGE028/g' -e 's/uge026/uge028/g' "$SRC" > /tmp/boot-028-final.sh
chmod +x /tmp/boot-028-final.sh
bash /tmp/boot-028-final.sh
bash "$R/exact-0.2.5-test/03_seed.sh"
bash "$R/exact-0.2.5-test/04_frontend.sh"
bash "$R/exact-0.2.5-test/05_regression.sh"
test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.8
test "$(docker exec wp wp eval --allow-root 'echo get_option(UGE_Core::REWRITE_SCHEMA_OPTION,"");')" = 6
curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/home
grep -q 'body.uge-glossary-home #primary{margin-top:0!important}' /tmp/home
test "$(curl -sS -o /tmp/term -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/term
grep -q FULL-HUFBEIN-SENTINEL /tmp/term
test "$(curl -sS -o /tmp/cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'class="uge-category-head"' /tmp/cat
grep -q '/glossar/begriff/hufbein/' /tmp/cat
! grep -q 'class="uge-hero' /tmp/cat
! grep -q 'class="uge-tools"' /tmp/cat
test "$(curl -sS -o /tmp/missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/draft -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)" = 404
echo UGE028_FINAL_FRESH_FULL_POSITIVE_NEGATIVE_PASS
