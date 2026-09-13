#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc1.sh"
rm -rf /tmp/uge0210rc1boot
cp -a /tmp/uge0210rc1 /tmp/uge0210rc1boot
SRC="$R/exact-0.2.6-test/02_boot.sh"
sed -e 's#/tmp/uge026#/tmp/uge0210rc1boot#g' -e 's/0\.2\.6/0.2.10-rc1/g' -e 's/UGE026/UGE0210RC1/g' -e 's/uge026/uge0210rc1/g' "$SRC" > /tmp/boot-0210-rc1.sh
chmod +x /tmp/boot-0210-rc1.sh
bash /tmp/boot-0210-rc1.sh
bash "$R/exact-0.2.5-test/03_seed.sh"
bash "$R/exact-0.2.5-test/04_frontend.sh"
bash "$R/exact-0.2.5-test/05_regression.sh"

test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.10-rc1
test "$(docker exec wp wp eval --allow-root 'echo get_option(UGE_Core::REWRITE_SCHEMA_OPTION,"");')" = 7

curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/home
grep -q '<span>WISSEN</span><h1>' /tmp/home
! grep -Fq 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' /tmp/home

test "$(curl -sS -o /tmp/cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'class="uge-category-head"' /tmp/cat
grep -q 'class="uge-hero' /tmp/cat
grep -q 'class="uge-tools"' /tmp/cat
grep -q 'class="uge-topic-nav"' /tmp/cat
grep -q '>Gesundheit<' /tmp/cat
grep -q '/glossar/begriff/hufbein/' /tmp/cat
! grep -Fq 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' /tmp/cat

# Preserve the zero-rewrite hardlock.
docker exec wp wp eval --allow-root '$r=(array)get_option("rewrite_rules",[]);foreach(array_keys($r) as $k){if(strpos((string)$k,"glossar")!==false)unset($r[$k]);}update_option("rewrite_rules",$r,false);'
RULES=$(docker exec wp wp option get rewrite_rules --format=json --allow-root)
if printf '%s' "$RULES" | grep -q 'glossar'; then echo GLOSSAR_RULE_DELETE_FAILED >&2; exit 1; fi

test "$(curl -sS -o /tmp/term-norules -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)" = 200
grep -q '<article class="uge-single-wrap"' /tmp/term-norules
grep -q '<h1[^>]*>Hufbein</h1>' /tmp/term-norules
grep -q FULL-HUFBEIN-SENTINEL /tmp/term-norules

test "$(curl -sS -o /tmp/cat-norules -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
grep -q 'class="uge-category-head"' /tmp/cat-norules
grep -q '/glossar/begriff/hufbein/' /tmp/cat-norules

test "$(curl -sS -o /tmp/missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/draft -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)" = 404

P=/tmp/uge0210rc1/universal-glossary-engine
! grep -R -F 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' "$P"
grep -q 'body.uge-glossary-category #primary' "$P/includes/class-uge-frontend.php"
grep -q 'body.uge-glossary-term #primary' "$P/includes/class-uge-frontend.php"
! grep -q 'while (have_posts())' "$P/templates/single-uge-term.php"
grep -q 'UGE_Frontend::requested_term_post' "$P/templates/single-uge-term.php"

echo UGE0210RC1_FRESH_BASE_REGRESSION_PASS
