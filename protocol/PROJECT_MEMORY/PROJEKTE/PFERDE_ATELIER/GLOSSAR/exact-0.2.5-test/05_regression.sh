#!/usr/bin/env bash
set -euo pipefail
curl -fsS 'http://127.0.0.1:8080/glossar/?glossar_letter=A' -o /tmp/A
grep -q Aalstrich /tmp/A
! grep -q Hufbein /tmp/A
D=$(cat /tmp/draftid)
test "$(curl -sS -o /tmp/draft-public -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)" != 200
PASS=$(cat /tmp/uge-admin-pass)
curl -sS -c /tmp/cookies --data-urlencode 'log=admin' --data-urlencode "pwd=$PASS" --data-urlencode 'wp-submit=Log In' --data-urlencode 'redirect_to=http://127.0.0.1:8080/wp-admin/' http://127.0.0.1:8080/wp-login.php >/dev/null
preview=$(docker exec wp wp eval --allow-root "echo get_preview_post_link($D);")
curl -fsS -b /tmp/cookies "$preview" -o /tmp/preview
grep -q DRAFT-SENTINEL /tmp/preview
grep -q '>Gesundheit</a>' /tmp/term
DUP=$(docker exec wp wp post create --allow-root --post_type=uge_term --post_status=draft --post_title=Hufbein --post_name=hufbein-zwei --post_content=DUPLICATE-SENTINEL --porcelain)
HEALTH=$(docker exec wp wp post list --allow-root --post_type=page --name=gesundheit --field=ID)
docker exec wp wp post meta update "$DUP" _uge_primary_category_id "$HEALTH" --allow-root >/dev/null
docker exec wp wp post update "$DUP" --post_status=publish --allow-root >/dev/null
test "$(docker exec wp wp post get "$DUP" --field=post_status --allow-root)" = draft
test "$(docker exec wp wp post list --allow-root --post_type=post --post_status=publish --search='Huf normaler Beitrag' --format=count)" = 1
echo UGE025_REGRESSION_PASS
