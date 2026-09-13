#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
cleanup(){ docker rm -f wp db >/dev/null 2>&1 || true; docker network rm uge0210rc11 >/dev/null 2>&1 || true; }
trap cleanup EXIT
cleanup

bash "$R/build-0.2.10-rc11-native-single.sh"
rm -rf /tmp/uge0210rc11boot
cp -a /tmp/uge0210rc11 /tmp/uge0210rc11boot

# Boot a real WordPress runtime from the established harness, with only path,
# version and isolated network names adapted to rc11.
SRC="$R/exact-0.2.6-test/02_boot.sh"
sed \
  -e 's#/tmp/uge026#/tmp/uge0210rc11boot#g' \
  -e 's/0\.2\.6/0.2.10-rc11-native-single/g' \
  -e 's/UGE026/UGE0210RC11/g' \
  -e 's/uge026/uge0210rc11/g' \
  "$SRC" > /tmp/boot-0210-rc11.sh
chmod +x /tmp/boot-0210-rc11.sh
bash /tmp/boot-0210-rc11.sh

# Seed the same published/draft/invalid glossary truth used by the established
# real WordPress regression suite.
bash "$R/exact-0.2.5-test/03_seed.sh"

# Reproduce the user's real frontend family instead of accepting Astra-only proof.
docker exec wp wp theme install kubio --activate --allow-root >/dev/null
docker exec wp wp plugin install kubio --activate --allow-root >/dev/null
KUBIO_THEME=$(docker exec wp wp theme list --status=active --field=name --allow-root)
test "$KUBIO_THEME" = kubio
KUBIO_PLUGIN=$(docker exec wp wp plugin list --name=kubio --field=status --allow-root)
test "$KUBIO_PLUGIN" = active

# Replace the small historical design contract with the exact reconstructed
# Pferde design plugin 1.50.469 used by the rc7 hardtest.
bash "$R/reconstruct-design-1.50.469.sh"
docker exec wp wp plugin deactivate affiliate-portal-template-kit --allow-root >/dev/null 2>&1 || true
docker exec wp rm -rf /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker exec wp mkdir -p /var/www/html/wp-content/plugins/affiliate-portal-template-kit
docker cp /tmp/design-1.50.469/pferde-template-kit.php wp:/var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php
docker exec wp wp plugin activate affiliate-portal-template-kit/pferde-template-kit.php --allow-root >/dev/null
test "$(docker exec wp wp plugin get affiliate-portal-template-kit/pferde-template-kit.php --field=version --allow-root)" = 1.50.469

docker exec wp wp rewrite flush --hard --allow-root >/dev/null

# POSITIVE: real published glossary term through real HTTP/Kubio/FSE.
CODE=$(curl -sS -L -o /tmp/rc11-hufbein.html -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufbein/)
test "$CODE" = 200
grep -q 'FULL-HUFBEIN-SENTINEL' /tmp/rc11-hufbein.html
grep -qi '>Hufbein<' /tmp/rc11-hufbein.html
grep -q 'id="kubio"' /tmp/rc11-hufbein.html

# The exact live failure supplied by the user is forbidden: a second document
# shell may not begin inside the first head/body.
DOCTYPE_COUNT=$(grep -oi '<!DOCTYPE html' /tmp/rc11-hufbein.html | wc -l | tr -d ' ')
HTML_COUNT=$(grep -oi '<html\b' /tmp/rc11-hufbein.html | wc -l | tr -d ' ')
HEAD_COUNT=$(grep -oi '<head\b' /tmp/rc11-hufbein.html | wc -l | tr -d ' ')
test "$DOCTYPE_COUNT" = 1
test "$HTML_COUNT" = 1
test "$HEAD_COUNT" = 1

# Native rendering proof: the old classic full-document UGE single template must
# not be the renderer under Kubio.
! grep -q 'class="uge-single-wrap"' /tmp/rc11-hufbein.html

# NEGATIVE: drafts and unknown slugs must not become public articles.
DRAFT_CODE=$(curl -sS -L -o /tmp/rc11-draft.html -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)
test "$DRAFT_CODE" = 404
! grep -q 'DRAFT-SENTINEL' /tmp/rc11-draft.html
MISSING_CODE=$(curl -sS -L -o /tmp/rc11-missing.html -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/gibt-es-nicht/)
test "$MISSING_CODE" = 404

# REGRESSION: unrelated normal posts remain native and visible.
NORMAL_CODE=$(curl -sS -L -o /tmp/rc11-normal.html -w '%{http_code}' http://127.0.0.1:8080/huf-normaler-beitrag/)
test "$NORMAL_CODE" = 200
grep -q 'NORMAL-POST-SENTINEL' /tmp/rc11-normal.html
test "$(grep -oi '<!DOCTYPE html' /tmp/rc11-normal.html | wc -l | tr -d ' ')" = 1

# REGRESSION: taxonomy routing remains available; rc11 only changes singles.
CAT_CODE=$(curl -sS -L -o /tmp/rc11-cat.html -w '%{http_code}' http://127.0.0.1:8080/glossar/huf-gliedmassen/)
test "$CAT_CODE" = 200
grep -qi 'Huf &amp; Gliedmaßen\|Huf & Gliedmaßen' /tmp/rc11-cat.html

# Exact installed source guards.
test "$(docker exec wp wp plugin list --name=universal-glossary-engine --field=version --allow-root)" = 0.2.10-rc11-native-single
docker exec wp grep -q "templates/taxonomy-uge-group.php" /var/www/html/wp-content/plugins/universal-glossary-engine/includes/class-uge-frontend.php
! docker exec wp grep -q "templates/single-uge-term.php" /var/www/html/wp-content/plugins/universal-glossary-engine/includes/class-uge-frontend.php

echo UGE0210RC11_KUBIO_PUBLISHED_SINGLE_VISIBLE_PASS
echo UGE0210RC11_KUBIO_SINGLE_DOCUMENT_SHELL_EXACTLY_ONCE_PASS
echo UGE0210RC11_DRAFT_AND_MISSING_NEGATIVE_PASS
echo UGE0210RC11_UNRELATED_POST_REGRESSION_PASS
echo UGE0210RC11_TAXONOMY_UNCHANGED_PASS
