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
bash "$R/exact-0.2.6-test/02_boot.sh"
bash "$R/exact-0.2.5-test/03_seed.sh"
test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.6
test "$(docker exec db mysql -uroot -pr wordpress -Nse "SELECT option_value FROM wp_options WHERE option_name='uge_rewrite_schema_version'")" = 5
curl -fsS http://127.0.0.1:8080/glossar/ -o /tmp/home-clean
curl -fsS http://127.0.0.1:8080/glossar/gesundheit/ -o /tmp/cat-clean
grep -q 'class="uge-hero' /tmp/home-clean
grep -q 'class="uge-category-head"' /tmp/cat-clean
! grep -q 'class="uge-hero' /tmp/cat-clean
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
rm -f /tmp/uge027-upgrade.zip
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
echo "UGE_027_TERM_HTTP=$TC UGE_027_CAT_HTTP=$CC"
test "$TC" != 200 || ! grep -q '<article class="uge-single-wrap"' /tmp/027-term
test "$CC" != 200 || ! grep -q 'class="uge-category-head"' /tmp/027-cat
echo UGE_026_TO_027_UNCHANGED_SCHEMA_BUG_REPRODUCED
echo UGE_LIVEFAIL_DIAGNOSTIC_COMPLETE_NO_RELEASE
