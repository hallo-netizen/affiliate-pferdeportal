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
# Diagnostic evidence before the first content-pack assertion. This changes only
# the harness, never candidate bytes.
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/test-fresh-0210-rc3.sh')
s=p.read_text()
needle='echo UGE0210RC3_FRESH_BASE_REGRESSION_PASS\n'
assert needle in s
probe=r'''echo UGE0210RC3_FRESH_BASE_REGRESSION_PASS
echo "CONTENT_PACK_CLASS=$(docker exec wp wp eval --allow-root 'echo class_exists("UGE_Pferde_Content_Pack",false)?"1":"0";')"
echo "PFERDE_DESIGN_CLASS=$(docker exec wp wp eval --allow-root 'echo class_exists("Pferde_Template_Kit",false)?"1":"0";')"
echo "PACK_OPTION=$(docker exec wp wp option get uge_pferde_content_pack_0210 --allow-root 2>/dev/null || echo MISSING)"
echo "GESUNDHEIT_PAGE=$(docker exec wp wp post list --allow-root --post_type=page --name=gesundheit --fields=ID,post_status,post_title --format=json)"
echo "PACK_POSTS=$(docker exec wp wp post list --allow-root --post_type=uge_term --name=hufrehe,strahlfaeule,hufabszess --post_status=any --fields=ID,post_name,post_status,post_title --format=json 2>/dev/null || true)"
docker exec wp wp eval --allow-root 'UGE_Pferde_Content_Pack::maybe_install(); echo "PACK_MANUAL_TRIGGER_DONE\n";'
echo "PACK_OPTION_AFTER_MANUAL=$(docker exec wp wp option get uge_pferde_content_pack_0210 --allow-root 2>/dev/null || echo MISSING)"
echo "ALL_NEW_PACK_POSTS=$(docker exec wp wp post list --allow-root --post_type=uge_term --post_status=any --fields=ID,post_name,post_status,post_title --format=json | grep -E "hufrehe|strahlfaeule|hufabszess" || true)"
'''
s=s.replace(needle,probe,1)
p.write_text(s)
PY
chmod +x /tmp/test-fresh-0210-rc3.sh
bash /tmp/test-fresh-0210-rc3.sh
