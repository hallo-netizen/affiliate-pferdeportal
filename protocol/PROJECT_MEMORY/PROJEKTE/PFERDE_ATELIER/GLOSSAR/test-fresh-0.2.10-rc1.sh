#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-fresh-0.2.9.sh"
sed \
  -e 's/build-0\.2\.9\.sh/build-0.2.10-rc1.sh/g' \
  -e 's/uge029/uge0210rc1/g' \
  -e 's/0\.2\.9/0.2.10-rc1/g' \
  -e 's/UGE029FINAL/UGE0210RC1/g' \
  "$SRC" > /tmp/test-fresh-0210-rc1.sh
chmod +x /tmp/test-fresh-0210-rc1.sh
bash /tmp/test-fresh-0210-rc1.sh

P=/tmp/uge0210rc1/universal-glossary-engine
! grep -R -F 'Begriffe schnell finden, fachlich einordnen und verständlich nachschlagen.' "$P"
grep -q 'body.uge-glossary-category #primary' "$P/includes/class-uge-frontend.php"
grep -q 'body.uge-glossary-term #primary' "$P/includes/class-uge-frontend.php"
! grep -q 'while (have_posts())' "$P/templates/single-uge-term.php"
grep -q 'UGE_Frontend::requested_term_post' "$P/templates/single-uge-term.php"

echo UGE0210RC1_FRESH_BASE_REGRESSION_PASS
