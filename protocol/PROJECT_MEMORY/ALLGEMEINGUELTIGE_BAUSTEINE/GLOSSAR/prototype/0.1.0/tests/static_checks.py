from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]/'universal-glossary-engine'
files=list(root.rglob('*.php'))
text='\n'.join(p.read_text() for p in files)
transfer=(root/'includes/class-uge-transfer.php').read_text()
checks=[]
def check(name, cond):
    checks.append((name, bool(cond)))
check('no horse content hardcoded', not re.search(r'\b(Kolik|Hufrehe|Mauke|Gesundheit|Fütterung|Haltung)\b', text, re.I))
check('no auto publish', 'wp_publish_post' not in text and "'post_status' => 'publish'" not in transfer and "'post_status' => 'draft'" in transfer)
check('separate post type', "const POST_TYPE = 'uge_term'" in text)
check('separate taxonomy', "const TAXONOMY = 'uge_group'" in text)
check('field schema filter', "apply_filters('uge_field_schema'" in text)
check('config filter', "apply_filters('uge_config'" in text)
check('design token filter', "apply_filters('uge_design_tokens'" in text)
check('yoast integration optional', "defined('WPSEO_VERSION')" in text and 'wpseo_metadesc' in text)
check('no direct yoast meta writes', '_yoast_wpseo_' not in text)
check('main page configurable', 'main_page_id' in text)
check('rewrite configurable', 'rewrite_base' in text)
check('SEO patterns configurable', 'seo_title_pattern' in text and 'seo_description_pattern' in text)
check('no featured image support', "'thumbnail'" not in text)
check('structured import/export', 'uge-json-v1' in text and 'admin_post_uge_import' in text and 'admin_post_uge_export' in text)
check('import allowlists fields', 'if (!isset($allowed[$key])) { continue; }' in transfer)
for name,ok in checks: print(('PASS' if ok else 'FAIL')+': '+name)
if not all(ok for _,ok in checks): sys.exit(1)
print(f'TOTAL PASS {sum(ok for _,ok in checks)}/{len(checks)}')
