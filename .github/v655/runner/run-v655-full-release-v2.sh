#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v655/runner/run-v655-full-release.sh
[ "$(git hash-object "$BASE")" = "a8f259012e7662cc0a314ab527db2652b2cb0e50" ] || { echo 'BLOCKED: V6.55 base release runner drift'; exit 1; }
TMP=/tmp/run-v655-full-release-v2-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1]).read_text()
old='REAL_PRODUCT="$WORK/.github/v654/tests/real_article_product_v654.php"'
new='REAL_PRODUCT="$WORK/.github/v655/tests/real_article_product_v655.php"'
if src.count(old)!=1: raise SystemExit('BLOCKED: V6.54 product-test path anchor drift')
src=src.replace(old,new,1)
old_marker="REAL_ARTICLE_PRODUCT_V654=PASS"
if src.count(old_marker)!=3: raise SystemExit('BLOCKED: V6.54 product marker count drift')
src=src.replace(old_marker,"REAL_ARTICLE_PRODUCT_V655=PASS")
# The PHP built-in server used by the real-WP CI fixture has no WordPress rewrite
# rules. Exercise the same REST route through WordPress' canonical rest_route
# query form; the production scheduler keeps the normal /wp-json/ URL.
pretty='http://127.0.0.1:8091/wp-json/affiliate-zentrale/v1/ebay/tick'
query='http://127.0.0.1:8091/?rest_route=/affiliate-zentrale/v1/ebay/tick'
if src.count(pretty)!=3: raise SystemExit('BLOCKED: local HTTP route anchor drift')
src=src.replace(pretty,query)
Path(sys.argv[2]).write_text(src)
PY
test -f "$TMP"
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
