#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-real-design-1.50.469-0.2.10-rc2.sh"
sed \
  -e 's/test-fresh-0\.2\.10-rc2\.sh/test-fresh-0.2.10-rc3.sh/g' \
  -e 's/0\.2\.10-rc2/0.2.10-rc4/g' \
  -e 's/UGE0210RC2/UGE0210RC4/g' \
  "$SRC" > /tmp/test-real-design-0210-rc4.sh
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/test-real-design-0210-rc4.sh')
s=p.read_text()
s=s.replace('set -euo pipefail\n','set -euo pipefail\nset -x\n',1)
p.write_text(s)
PY
chmod +x /tmp/test-real-design-0210-rc4.sh
bash /tmp/test-real-design-0210-rc4.sh
for slug in hufrehe strahlfaeule hufabszess; do
  test "$(curl -sS -o /tmp/rd-$slug -w '%{http_code}' http://127.0.0.1:8080/glossar/begriff/$slug/)" = 200
  grep -q '<strong>Verwandte Begriffe:</strong>' /tmp/rd-$slug
  grep -q 'class="uge-primary-category"' /tmp/rd-$slug
  if grep -Eqi '<h[2-6][ >]' /tmp/rd-$slug; then echo UNNEEDED_SUBHEADING_REAL_DESIGN:$slug >&2; exit 1; fi
done
echo UGE0210RC4_REAL_DESIGN_RELATED_CLUSTER_PASS
