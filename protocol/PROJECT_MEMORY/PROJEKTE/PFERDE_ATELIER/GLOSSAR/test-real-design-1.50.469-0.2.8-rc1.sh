#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
FIX="$R/fixtures/design-1.50.469"
EXPECTED=580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5

bash "$R/build-0.2.8-rc1.sh"

for i in $(seq -w 0 21); do test -f "$FIX/pferde-template-kit.php.xz.b64.part$i"; done
for i in $(seq -w 0 20); do test "$(wc -c < "$FIX/pferde-template-kit.php.xz.b64.part$i")" = 15000; done
test "$(wc -c < "$FIX/pferde-template-kit.php.xz.b64.part21")" = 5696
cat "$FIX"/pferde-template-kit.php.xz.b64.part{00..21} | base64 -d | xz -d >/tmp/pferde-template-kit.php
test "$(sha256sum /tmp/pferde-template-kit.php | awk '{print $1}')" = "$EXPECTED"
php -l /tmp/pferde-template-kit.php
echo REAL_DESIGN_150469_EXACT_FIXTURE_PASS

SRC="$R/exact-0.2.6-test/02_boot.sh"
sed -e 's/0\.2\.6/0.2.8-rc1/g' -e 's/UGE026/UGE028RC1/g' -e 's/uge026/uge028rc1/g' "$SRC" >/tmp/boot-real-design-rc1.sh
chmod +x /tmp/boot-real-design-rc1.sh
bash /tmp/boot-real-design-rc1.sh

docker exec wp wp plugin deactivate affiliate-portal-template-kit --allow-root >/dev/null || true
docker exec wp rm -rf /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker exec wp mkdir -p /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker cp /tmp/pferde-template-kit.php wp:/var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php
docker exec wp php -l /var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php
docker exec wp wp plugin activate affiliate-portal-template-kit --allow-root

test "$(docker exec wp sha256sum /var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php | awk '{print $1}')" = "$EXPECTED"
echo REAL_DESIGN_150469_RUNTIME_IDENTITY_PASS

bash "$R/exact-0.2.5-test/03_seed.sh"
bash "$R/exact-0.2.5-test/04_frontend.sh"
bash "$R/exact-0.2.5-test/05_regression.sh"

for u in /glossar/ /glossar/begriff/hufbein/ /glossar/gesundheit/; do
  code=$(curl -sS -o /tmp/real-design-page -w '%{http_code}' "http://127.0.0.1:8080$u")
  test "$code" = 200
  test -s /tmp/real-design-page
  ! grep -qiE 'fatal error|critical error' /tmp/real-design-page
done

curl -fsS http://127.0.0.1:8080/glossar/begriff/hufbein/ -o /tmp/rd-term
grep -q '<article class="uge-single-wrap"' /tmp/rd-term
grep -q FULL-HUFBEIN-SENTINEL /tmp/rd-term

curl -fsS http://127.0.0.1:8080/glossar/gesundheit/ -o /tmp/rd-cat
test "$(grep -o 'class="uge-breadcrumbs"' /tmp/rd-cat | wc -l)" = 1
python3 - <<'PY'
import re
s=open('/tmp/rd-cat',encoding='utf8').read()
b=re.search(r'<nav class="uge-breadcrumbs"[^>]*>(.*?)</nav>',s,re.S)
assert b, 'glossary breadcrumb missing'
assert '>Startseite</a>' in b.group(1) and '>Glossar</a>' in b.group(1) and 'Gesundheit' in b.group(1)
assert 'var(--pftk-breadcrumb-axis-width,900px)' in s or '--pftk-breadcrumb-axis-width:900px' in s
PY

test "$(curl -sS -o /tmp/rd-missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/rd-draft -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)" = 404

echo UGE028RC1_REAL_DESIGN_150469_RUNTIME_POSITIVE_NEGATIVE_PASS
