#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
SRC="$R/test-real-design-1.50.469-0.2.10-rc2.sh"
sed \
  -e 's/test-fresh-0\.2\.10-rc2\.sh/test-fresh-0.2.10-rc3.sh/g' \
  -e 's/0\.2\.10-rc2/0.2.10-rc4/g' \
  -e 's/UGE0210RC2/UGE0210RC4/g' \
  "$SRC" > /tmp/test-real-design-0210-rc4.sh
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/test-real-design-0210-rc4.sh')
s=p.read_text()
s=s.replace('set -euo pipefail\n','set -euo pipefail\nset -x\n',1)
needle="test \"$(docker exec wp wp plugin get affiliate-portal-template-kit/pferde-template-kit.php --field=version --allow-root)\" = 1.50.469\n"
assert needle in s
probe=r'''test "$(docker exec wp wp plugin get affiliate-portal-template-kit/pferde-template-kit.php --field=version --allow-root)" = 1.50.469
HEALTH_ID=$(docker exec wp wp post list --allow-root --post_type=page --name=gesundheit --field=ID)
echo "REAL_DESIGN_HEALTH_ID=$HEALTH_ID"
docker exec wp wp eval --allow-root "\$id=$HEALTH_ID; echo 'REAL_DESIGN_AFFILIATE_PAGE_TYPE=' . (method_exists('Pferde_Template_Kit','affiliate_page_type') ? Pferde_Template_Kit::affiliate_page_type(\$id) : 'NO_METHOD') . PHP_EOL; echo 'UGE_PRIMARY_TARGET='; var_export(UGE_Core::primary_category_target(\$id)); echo PHP_EOL; echo 'HEALTH_META='; var_export(get_post_meta(\$id)); echo PHP_EOL;"
docker exec wp sh -c "grep -n -A100 -B20 'function affiliate_page_type' /var/www/html/wp-content/plugins/affiliate-portal-template-kit/pferde-template-kit.php || true"
'''
s=s.replace(needle,probe,1)
p.write_text(s)
PY
chmod +x /tmp/test-real-design-0210-rc4.sh
bash /tmp/test-real-design-0210-rc4.sh
