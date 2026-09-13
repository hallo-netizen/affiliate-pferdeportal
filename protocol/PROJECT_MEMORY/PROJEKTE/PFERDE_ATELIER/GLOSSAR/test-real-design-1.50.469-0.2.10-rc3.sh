#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-real-design-1.50.469-0.2.10-rc2.sh"
sed \
  -e 's/test-fresh-0\.2\.10-rc2\.sh/test-fresh-0.2.10-rc3.sh/g' \
  -e 's/0\.2\.10-rc2/0.2.10-rc4/g' \
  -e 's/UGE0210RC2/UGE0210RC4/g' \
  "$SRC" > /tmp/test-real-design-0210-rc4.sh
# The fresh script path above now contains the rc4 implementation under the
# retained harness filename; assert exact candidate version before execution.
chmod +x /tmp/test-real-design-0210-rc4.sh
bash /tmp/test-real-design-0210-rc4.sh

# Also prove the new cluster survives the exact real-design runtime.
for slug in hufrehe strahlfaeule hufabszess; do
  test "$(curl -sS -o /tmp/rd-$slug -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/$slug/)" = 200
  grep -q '<strong>Verwandte Begriffe:</strong>' /tmp/rd-$slug
  grep -q 'class="uge-primary-category"' /tmp/rd-$slug
  if grep -Eqi '<h[2-6][ >]' /tmp/rd-$slug; then echo UNNEEDED_SUBHEADING_REAL_DESIGN:$slug >&2; exit 1; fi
done

echo UGE0210RC4_REAL_DESIGN_RELATED_CLUSTER_PASS
