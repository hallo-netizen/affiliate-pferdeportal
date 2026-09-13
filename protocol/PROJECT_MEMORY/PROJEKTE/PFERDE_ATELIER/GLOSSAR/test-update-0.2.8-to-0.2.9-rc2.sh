#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-update-0.2.8-to-0.2.9-rc1.sh"
sed \
  -e 's/build-0\.2\.9-rc1\.sh/build-0.2.9-rc2.sh/g' \
  -e 's/uge029rc1/uge029rc2/g' \
  -e 's/0\.2\.9-rc1/0.2.9-rc2/g' \
  -e 's/UGE029RC1/UGE029RC2/g' \
  "$SRC" > /tmp/test-update-028-to-029-rc2.sh
chmod +x /tmp/test-update-028-to-029-rc2.sh
! grep -q '0\.2\.9-rc1' /tmp/test-update-028-to-029-rc2.sh
bash /tmp/test-update-028-to-029-rc2.sh
