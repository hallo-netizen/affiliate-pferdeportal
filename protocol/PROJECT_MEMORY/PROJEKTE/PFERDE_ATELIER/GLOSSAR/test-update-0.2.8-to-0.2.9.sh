#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-update-0.2.8-to-0.2.9-rc2.sh"
sed \
  -e 's/build-0\.2\.9-rc2\.sh/build-0.2.9.sh/g' \
  -e 's/uge029rc2/uge029/g' \
  -e 's/0\.2\.9-rc2/0.2.9/g' \
  -e 's/UGE029RC2/UGE029FINAL/g' \
  "$SRC" > /tmp/test-update-028-to-029-final.sh
chmod +x /tmp/test-update-028-to-029-final.sh
! grep -q '0\.2\.9-rc2' /tmp/test-update-028-to-029-final.sh
bash /tmp/test-update-028-to-029-final.sh
