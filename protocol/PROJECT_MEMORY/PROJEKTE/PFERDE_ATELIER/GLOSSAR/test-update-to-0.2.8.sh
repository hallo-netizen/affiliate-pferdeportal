#!/usr/bin/env bash
set -euo pipefail
BASE=${1:?base version required}
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-update-to-0.2.8-rc1.sh"
sed \
  -e 's/build-0\.2\.8-rc1\.sh/build-0.2.8.sh/g' \
  -e 's#/tmp/uge028rc1#/tmp/uge028#g' \
  -e 's/0\.2\.8-rc1/0.2.8/g' \
  -e 's/UGE028RC1/UGE028FINAL/g' \
  "$SRC" > /tmp/test-update-028-final.sh
chmod +x /tmp/test-update-028-final.sh
! grep -q '0\.2\.8-rc1' /tmp/test-update-028-final.sh
bash /tmp/test-update-028-final.sh "$BASE"
