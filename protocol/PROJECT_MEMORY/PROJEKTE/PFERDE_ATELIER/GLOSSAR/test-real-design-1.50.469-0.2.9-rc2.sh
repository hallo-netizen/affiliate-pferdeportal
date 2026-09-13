#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-real-design-1.50.469-0.2.9-rc1.sh"
sed \
  -e 's/test-fresh-0\.2\.9-rc1\.sh/test-fresh-0.2.9-rc2.sh/g' \
  -e 's/0\.2\.9-rc1/0.2.9-rc2/g' \
  -e 's/UGE029RC1/UGE029RC2/g' \
  "$SRC" > /tmp/test-real-design-029-rc2.sh
chmod +x /tmp/test-real-design-029-rc2.sh
! grep -q '0\.2\.9-rc1' /tmp/test-real-design-029-rc2.sh
bash /tmp/test-real-design-029-rc2.sh
