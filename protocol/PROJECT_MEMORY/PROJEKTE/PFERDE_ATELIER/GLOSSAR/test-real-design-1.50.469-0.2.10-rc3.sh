#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-real-design-1.50.469-0.2.10-rc2.sh"
# Generic rc2→rc3 replacement already updates the nested fresh-test path; do it
# once only. The previous harness accidentally produced *-rc3-rc3.sh.
sed \
  -e 's/0\.2\.10-rc2/0.2.10-rc3/g' \
  -e 's/UGE0210RC2/UGE0210RC3/g' \
  "$SRC" > /tmp/test-real-design-0210-rc3.sh
chmod +x /tmp/test-real-design-0210-rc3.sh
grep -q 'test-fresh-0.2.10-rc3.sh' /tmp/test-real-design-0210-rc3.sh
! grep -q 'rc3-rc3' /tmp/test-real-design-0210-rc3.sh
bash /tmp/test-real-design-0210-rc3.sh
