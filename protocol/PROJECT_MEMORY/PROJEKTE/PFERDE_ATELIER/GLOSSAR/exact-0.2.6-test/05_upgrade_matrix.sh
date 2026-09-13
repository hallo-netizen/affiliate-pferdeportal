#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import re
s=open('/tmp/post-upgrade-home',encoding='utf8').read()
links=sorted(set(re.findall(r'href="(http://127\.0\.0\.1:8080/glossar/begriff/[^\"]+/)"',s)))
assert links, 'no glossary card links after upgrade'
open('/tmp/post-links','w').write('\n'.join(links)+'\n')
PY

while IFS= read -r u; do
 test "$(curl -sS -o /tmp/card-term -w '%{http_code}' "$u")" = 200
 grep -q '<article class="uge-single-wrap"' /tmp/card-term
 ! grep -qiE 'fatal error|critical error' /tmp/card-term
done </tmp/post-links

echo UGE026_ALL_CARD_LINKS_REAL_PAGE_PASS

# Negative routing / publication checks.
test "$(curl -sS -o /tmp/missing -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/nicht-da/)" = 404
test "$(curl -sS -o /tmp/draft -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/hufentwurf/)" = 404
test "$(curl -sS -o /tmp/legacy -w '%{http_code}' http://127.0.0.1:8080/glossar/hufbein/)" = 301

test "$(curl -sS -o /tmp/cat -w '%{http_code}' http://127.0.0.1:8080/glossar/gesundheit/)" = 200
! grep -q CATEGORY-OVERLAP-SENTINEL /tmp/cat
test "$(curl -sS -o /tmp/same -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/gesundheit/)" = 200
grep -q CATEGORY-OVERLAP-SENTINEL /tmp/same

BAD=$(curl -sS -o /tmp/badajax -w '%{http_code}' -X POST http://127.0.0.1:8080/wp-admin/admin-ajax.php --data action=uge_search --data nonce=bad --data q=Hu)
test "$BAD" != 200

echo UGE026_ROUTING_POLICY_NEGATIVE_PASS

# Negative blast radius: normal WordPress post stays normal.
NORMAL_URL=$(docker exec wp wp post list --allow-root --post_type=post --post_status=publish --field=url | head -1)
test -n "$NORMAL_URL"
test "$(curl -sS -o /tmp/normal -w '%{http_code}' "$NORMAL_URL")" = 200
grep -q NORMAL-POST-SENTINEL /tmp/normal
! grep -q 'uge-single-wrap' /tmp/normal

echo UGE026_NORMAL_WORDPRESS_NEGATIVE_PASS
