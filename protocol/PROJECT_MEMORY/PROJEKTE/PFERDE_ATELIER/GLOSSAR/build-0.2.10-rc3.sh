#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc2.sh"
rm -rf /tmp/uge0210rc3
cp -a /tmp/uge0210rc2 /tmp/uge0210rc3
P=/tmp/uge0210rc3/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/uge0210rc3/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.10-rc2')==1
assert s.count("define('UGE_VERSION', '0.2.10-rc2');")==1
s=s.replace('Version: 0.2.10-rc2','Version: 0.2.10-rc3')
s=s.replace("define('UGE_VERSION', '0.2.10-rc2');","define('UGE_VERSION', '0.2.10-rc3');")
p.write_text(s)

p=Path('/tmp/uge0210rc3/universal-glossary-engine/templates/single-uge-term.php')
s=p.read_text()
old="""if (!$uge_post instanceof WP_Post) {
    $queried = get_queried_object();
    $uge_post = ($queried instanceof WP_Post && $queried->post_type === UGE_Core::POST_TYPE && $queried->post_status === 'publish') ? $queried : null;
}
"""
new="""if (!$uge_post instanceof WP_Post) {
    $queried = get_queried_object();
    $is_valid_term = $queried instanceof WP_Post && $queried->post_type === UGE_Core::POST_TYPE;
    $is_public = $is_valid_term && $queried->post_status === 'publish';
    $is_authorized_preview = $is_valid_term && is_preview() && current_user_can('edit_post', $queried->ID);
    $uge_post = ($is_public || $is_authorized_preview) ? $queried : null;
}
"""
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)
PY

grep -q 'Version: 0.2.10-rc3' "$P/universal-glossary-engine.php"
grep -q 'is_authorized_preview' "$P/templates/single-uge-term.php"
grep -q 'current_user_can' "$P/templates/single-uge-term.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

echo UGE0210RC3_BUILD_PASS
