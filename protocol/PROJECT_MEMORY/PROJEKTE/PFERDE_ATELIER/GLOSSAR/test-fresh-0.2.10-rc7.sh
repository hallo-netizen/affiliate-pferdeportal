#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-fresh-0.2.10-rc6.sh"
sed \
  -e 's/build-0\.2\.10-rc6\.sh/build-0.2.10-rc7.sh/g' \
  -e 's/uge0210rc6/uge0210rc7/g' \
  -e 's/0\.2\.10-rc6/0.2.10-rc7/g' \
  -e 's/UGE0210RC6/UGE0210RC7/g' \
  "$SRC" > /tmp/test-fresh-0210-rc7.sh
chmod +x /tmp/test-fresh-0210-rc7.sh
! grep -q '0\.2\.10-rc6' /tmp/test-fresh-0210-rc7.sh
bash /tmp/test-fresh-0210-rc7.sh
