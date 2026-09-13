#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc6.sh"
rm -rf /tmp/uge0210rc7
cp -a /tmp/uge0210rc6 /tmp/uge0210rc7
P=/tmp/uge0210rc7/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path

p=Path('/tmp/uge0210rc7/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.10-rc6')==1
assert s.count("define('UGE_VERSION', '0.2.10-rc6');")==1
s=s.replace('Version: 0.2.10-rc6','Version: 0.2.10-rc7')
s=s.replace("define('UGE_VERSION', '0.2.10-rc6');","define('UGE_VERSION', '0.2.10-rc7');")
p.write_text(s)

p=Path('/tmp/uge0210rc7/universal-glossary-engine/includes/class-uge-pferde-content-pack.php')
s=p.read_text()
# Diagnosis proved RC6 stopped at publish: all three pack terms existed as owned
# drafts, but the existing UGE publication policy rejected them because RC5 had
# removed the mandatory primary portal-category binding. Restore that prerequisite
# BEFORE any pack term is created, so installation remains atomic and recoverable.
needle="""        $group = get_term_by('slug','gesundheit',UGE_Core::TAXONOMY);
"""
insert="""        $portal = get_page_by_path('gesundheit', OBJECT, 'page');
        if (!$portal instanceof WP_Post || $portal->post_status !== 'publish') { return; }
        if (method_exists('Pferde_Template_Kit','affiliate_page_type') && (string)Pferde_Template_Kit::affiliate_page_type($portal->ID) !== 'category') { return; }
        $group = get_term_by('slug','gesundheit',UGE_Core::TAXONOMY);
"""
assert s.count(needle)==1
s=s.replace(needle,insert,1)
needle="""            update_post_meta($id,UGE_Core::meta_key('seo_description'),$item['meta_description']);
"""
replace="""            update_post_meta($id,UGE_Core::meta_key('seo_description'),$item['meta_description']);
            update_post_meta($id,UGE_Core::meta_key('primary_category_id'),(string)$portal->ID);
"""
assert s.count(needle)==1
s=s.replace(needle,replace,1)
p.write_text(s)
PY

grep -q 'Version: 0.2.10-rc7' "$P/universal-glossary-engine.php"
grep -q "get_page_by_path('gesundheit', OBJECT, 'page')" "$P/includes/class-uge-pferde-content-pack.php"
grep -q "affiliate_page_type" "$P/includes/class-uge-pferde-content-pack.php"
grep -q "primary_category_id" "$P/includes/class-uge-pferde-content-pack.php"
grep -q 'resolve_related_term' "$P/includes/class-uge-frontend.php"
grep -q 'render_design_breadcrumb_payload' "$P/includes/class-uge-frontend.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

echo UGE0210RC7_BUILD_PASS
