#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-real-design-1.50.469-0.2.8-rc1.sh"
sed \
  -e 's/test-fresh-0\.2\.8-rc1\.sh/test-fresh-0.2.8.sh/g' \
  -e 's/0\.2\.8-rc1/0.2.8/g' \
  -e 's/UGE028RC1/UGE028FINAL/g' \
  "$SRC" > /tmp/test-real-design-028-final.sh
chmod +x /tmp/test-real-design-028-final.sh
! grep -q '0\.2\.8-rc1' /tmp/test-real-design-028-final.sh
bash /tmp/test-real-design-028-final.sh
