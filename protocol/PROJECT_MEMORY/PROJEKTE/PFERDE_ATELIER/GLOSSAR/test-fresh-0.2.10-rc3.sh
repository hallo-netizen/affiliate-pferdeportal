#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-fresh-0.2.10-rc2.sh"
sed \
  -e 's/build-0\.2\.10-rc2\.sh/build-0.2.10-rc3.sh/g' \
  -e 's/uge0210rc2/uge0210rc3/g' \
  -e 's/0\.2\.10-rc2/0.2.10-rc3/g' \
  -e 's/UGE0210RC2/UGE0210RC3/g' \
  "$SRC" > /tmp/test-fresh-0210-rc3.sh
chmod +x /tmp/test-fresh-0210-rc3.sh
bash /tmp/test-fresh-0210-rc3.sh
