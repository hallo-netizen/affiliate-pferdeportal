#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-real-design-1.50.469-0.2.10-rc6.sh"
sed \
  -e 's/test-fresh-0\.2\.10-rc6\.sh/test-fresh-0.2.10-rc7.sh/g' \
  -e 's/0\.2\.10-rc6/0.2.10-rc7/g' \
  -e 's/UGE0210RC6/UGE0210RC7/g' \
  "$SRC" > /tmp/test-real-design-0210-rc7.sh
chmod +x /tmp/test-real-design-0210-rc7.sh
! grep -q '0\.2\.10-rc6' /tmp/test-real-design-0210-rc7.sh
bash /tmp/test-real-design-0210-rc7.sh
