#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-real-design-1.50.469-0.2.10-rc2.sh"
sed \
  -e 's/test-fresh-0\.2\.10-rc2\.sh/test-fresh-0.2.10-rc3.sh/g' \
  -e 's/0\.2\.10-rc2/0.2.10-rc3/g' \
  -e 's/UGE0210RC2/UGE0210RC3/g' \
  "$SRC" > /tmp/test-real-design-0210-rc3.sh
chmod +x /tmp/test-real-design-0210-rc3.sh
bash /tmp/test-real-design-0210-rc3.sh
